"""Build-scoped state shared by every page builder.

Holds the repository location, the set of tracked files, the pages written so
far, the search records and the problems found. It also owns link resolution,
because turning a repository path into a site link needs to know which paths
became pages.
"""

from __future__ import annotations

import posixpath
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, unquote

import catalog as cat
from images import Thumbnails
from urls import is_viewable, output_file, page_url, rel, viewer_url

MENTION_SUFFIXES = (".md", ".py", ".cfg")
SEARCH_TEXT_LIMIT = 4000
PREVIEW_LENGTH = 60

_REPO_LINK = re.compile(
    rf"^https?://github\.com/{re.escape(cat.REPO_OWNER)}/{re.escape(cat.REPO_NAME)}"
    rf"/(?:blob|tree|raw)/{re.escape(cat.REPO_BRANCH)}/(.+)$",
    re.IGNORECASE,
)
_SCHEME = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)


@dataclass
class Site:
    repo: Path
    tracked: frozenset[str]
    thumbs: Thumbnails
    outputs: dict[str, str] = field(default_factory=dict)
    search: list[dict[str, str]] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    surfaced: set[str] = field(default_factory=set)
    stats: dict[str, int] = field(default_factory=dict)
    highlights: dict[str, tuple[str, ...]] = field(default_factory=dict)
    _source_pages: dict[str, cat.Page] = field(default_factory=dict)
    _mentions: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for section in cat.SECTIONS:
            for page in section.pages:
                for source in (page.source, *page.extra_sources):
                    if source:
                        self._source_pages.setdefault(source, page)
        seen: dict[str, int] = {}
        for path in self.tracked:
            name = posixpath.basename(path)
            seen[name] = seen.get(name, 0) + 1
        for path in self.tracked:
            name = posixpath.basename(path)
            linkable = path in self._source_pages or is_viewable(path)
            if seen[name] == 1 and name.endswith(MENTION_SUFFIXES) and linkable:
                self._mentions[name] = path

    # Repository access -------------------------------------------------

    def mark(self, path: str) -> None:
        self.surfaced.add(path)

    def read(self, path: str) -> str:
        self.mark(path)
        return (self.repo / path).read_text(encoding="utf-8")

    def source_text(self, page: cat.Page) -> str:
        """The page's markdown with its presentation rewrites applied."""
        if page.source is None:
            return ""
        text = self.read(page.source)
        for old, new in page.rewrites:
            if old not in text:
                self.problems.append(
                    f"{page.slug}: rewrite no longer matches its source: "
                    f"{old[:PREVIEW_LENGTH]!r}"
                )
            text = text.replace(old, new)
        return text

    def size(self, path: str) -> int:
        return (self.repo / path).stat().st_size

    def line_count(self, path: str) -> int:
        text = (self.repo / path).read_text(encoding="utf-8", errors="replace")
        return len(text.splitlines())

    def is_folder(self, path: str) -> bool:
        prefix = path.rstrip("/") + "/"
        return any(tracked.startswith(prefix) for tracked in self.tracked)

    def config_files(self) -> list[tuple[cat.Page, cat.FileRef]]:
        """Every viewable file offered by any page, first offer wins."""
        seen: set[str] = set()
        found: list[tuple[cat.Page, cat.FileRef]] = []
        for section in cat.SECTIONS:
            for page in section.pages:
                for ref in page.files:
                    if ref.path in seen or not is_viewable(ref.path):
                        continue
                    if ref.path in self.tracked:
                        seen.add(ref.path)
                        found.append((page, ref))
        return found

    # Links ---------------------------------------------------------------

    def target(self, path: str) -> str:
        """Where a repository path is best shown: a page, the viewer or GitHub."""
        path = cat.LINK_ALIASES.get(path, path)
        page = self._source_pages.get(path)
        if page is not None:
            return page_url(page.slug)
        if path in self.tracked:
            if is_viewable(path):
                return viewer_url(path)
            return cat.BLOB_BASE + quote(path)
        if self.is_folder(path):
            return cat.TREE_BASE + quote(path.rstrip("/"))
        self.problems.append(f"link to a path that is not in the repository: {path}")
        return cat.BLOB_BASE + quote(path)

    def href(self, from_url: str, target: str) -> str:
        return target if _SCHEME.match(target) else rel(from_url, target)

    def resolve_link(self, href: str, source_dir: str, from_url: str) -> str:
        if not href or href.startswith(("#", "mailto:")):
            return href
        match = _REPO_LINK.match(href)
        if match:
            path = unquote(match.group(1))
        elif _SCHEME.match(href):
            return href
        else:
            bare = unquote(href.split("#", 1)[0])
            path = posixpath.normpath(posixpath.join(source_dir, bare))
        return self.href(from_url, self.target(path))

    def link_resolver(self, source: str | None, from_url: str) -> Callable[[str], str]:
        source_dir = posixpath.dirname(source) if source else ""
        return lambda href: self.resolve_link(href, source_dir, from_url)

    def mention_hrefs(self, from_url: str) -> dict[str, str]:
        return {
            name: self.href(from_url, self.target(path))
            for name, path in self._mentions.items()
        }

    # Output ----------------------------------------------------------------

    def output(self, url: str, markup: str) -> None:
        self.outputs[output_file(url)] = markup

    def add_search(
        self, title: str, url: str, section: str, summary: str = "", text: str = ""
    ) -> None:
        self.search.append(
            {
                "t": title,
                "u": url,
                "s": section,
                "d": summary,
                "x": " ".join(text.split())[:SEARCH_TEXT_LIMIT],
            }
        )
