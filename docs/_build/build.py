"""Build the GitHub Pages site from the repository's own content.

    python docs/_build/build.py

Needs Python 3.11 or newer with Markdown and Pillow (see requirements.txt).
Every page under docs/ is generated from the repository's markdown, configs
and images, so edit the guides rather than the HTML. The catalog in
catalog.py decides where each piece of content appears.

The build exits non-zero when a guard fails: a tracked repository file that no
page surfaces, a presentation rewrite that no longer matches its guide or a
link to a path that is not in the repository. Pages are still written, so the
result can be inspected while the catalog is brought up to date.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import catalog as cat
import pages
import pages_special as special
from context import Site
from images import Thumbnails
from pages import Neighbours

BUILD_DIR = Path(__file__).resolve().parent
DOCS_DIR = BUILD_DIR.parent
REPO_DIR = DOCS_DIR.parent
IMAGE_PREFIX = "assets/img/"
MANIFEST = BUILD_DIR / "generated.txt"
SEARCH_FILE = "search.json"
SITEMAP_FILE = "sitemap.xml"
INDEX_FILE = "index.html"
UNLISTED = frozenset({special.NOT_FOUND_URL})
MIN_PAGES_FOR_HUB = 2

Builder = Callable[[Site, cat.Section, cat.Page, Neighbours], None]

KIND_BUILDERS: dict[str, Builder] = {
    "article": pages.build_article,
    "files": pages.build_article,
    "tools": special.build_tools,
    "filament": special.build_filament,
    "stls": special.build_stls,
    "bookmarks": special.build_bookmarks,
    "gallery": special.build_gallery,
    "projects": special.build_projects,
}


def tracked_files(repo: Path) -> frozenset[str]:
    listing = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"], capture_output=True, check=True
    ).stdout.decode("utf-8")
    return frozenset(path for path in listing.split("\0") if path)


def build(site: Site) -> None:
    for section in cat.SECTIONS:
        if section.key == cat.CONFIGS.key:
            special.build_configs(site, section)
            continue
        ordered = pages.ordered_pages(section)
        if len(ordered) >= MIN_PAGES_FOR_HUB:
            pages.build_hub(site, section)
        for position, page in enumerate(ordered):
            previous = ordered[position - 1] if position > 0 else None
            following = ordered[position + 1] if position + 1 < len(ordered) else None
            KIND_BUILDERS[page.kind](site, section, page, (previous, following))
    special.build_home(site)
    special.build_not_found(site)


def _sitemap(files: list[str]) -> str:
    entries = []
    for file in sorted(files):
        if file in UNLISTED:
            continue
        url = file.removesuffix(INDEX_FILE)
        entries.append(f"<url><loc>{cat.SITE_URL}{url}</loc></url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_outputs(site: Site) -> set[str]:
    for relative, markup in site.outputs.items():
        _write(DOCS_DIR / relative, markup)
    search = json.dumps(site.search, ensure_ascii=False, separators=(",", ":"))
    _write(DOCS_DIR / SEARCH_FILE, search)
    _write(DOCS_DIR / SITEMAP_FILE, _sitemap(list(site.outputs)))
    return set(site.outputs) | {SEARCH_FILE, SITEMAP_FILE} | site.thumbs.written


def prune(written: set[str]) -> None:
    """Delete files an earlier build wrote that this build no longer produces."""
    if MANIFEST.exists():
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            stale = DOCS_DIR / line
            if line and line not in written and stale.is_file():
                stale.unlink()
                print(f"removed stale {line}")
    _write(MANIFEST, "\n".join(sorted(written)) + "\n")


def unsurfaced(site: Site) -> list[str]:
    shown = set(site.surfaced)
    for section in cat.SECTIONS:
        for page in section.pages:
            shown.update(page.covers)
    folders = tuple(path for path in shown if path.endswith("/"))
    missing = []
    for path in sorted(site.tracked):
        if path in cat.NOT_CONTENT or path.startswith(cat.NOT_CONTENT_PREFIXES):
            continue
        if path in shown or (folders and path.startswith(folders)):
            continue
        missing.append(path)
    return missing


def main() -> int:
    site = Site(
        repo=REPO_DIR,
        tracked=tracked_files(REPO_DIR),
        thumbs=Thumbnails(REPO_DIR, DOCS_DIR, IMAGE_PREFIX),
    )
    build(site)
    prune(write_outputs(site))
    missing = [f"not shown on any page: {path}" for path in unsurfaced(site)]
    problems = site.problems + missing
    print(
        f"wrote {len(site.outputs)} pages, {len(site.thumbs.written)} images, "
        f"{len(site.search)} search records"
    )
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
