"""Parsers for the repository's list-shaped content.

Tool recommendations are markdown files of anchor lines under headings, the
filament notes are tiers of materials of brand notes, the STL sources are
labelled URLs and the bookmarks are a Netscape bookmark export. Each parser
returns frozen data; the page builders decide how it looks.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlparse

MAX_MATERIAL_WORDS = 4
MAX_ICON_CHARS = 4096
ICON_PREFIX = "data:image/"

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_ANCHOR = re.compile(r'<a\s+href="([^"]+)"\s*>(.*?)</?a>', re.IGNORECASE)
_URL = re.compile(r"https?://\S+")
_MARKDOWN_EMPHASIS = re.compile(r"(?<!\w)[_*]+|[_*]+(?!\w)")
_SEPARATOR = " - "


@dataclass(frozen=True, slots=True)
class LinkItem:
    name: str
    note: str
    url: str
    host: str


@dataclass(frozen=True, slots=True)
class LinkGroup:
    title: str
    items: tuple[LinkItem, ...]
    intro: str = ""


@dataclass(frozen=True, slots=True)
class FilamentNote:
    brand: str
    note: str
    url: str


@dataclass(frozen=True, slots=True)
class Material:
    name: str
    tip: str
    notes: tuple[FilamentNote, ...]


@dataclass(frozen=True, slots=True)
class Tier:
    title: str
    materials: tuple[Material, ...]


@dataclass(frozen=True, slots=True)
class ProseSection:
    title: str
    paragraphs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FilamentGuide:
    tiers: tuple[Tier, ...]
    prose: tuple[ProseSection, ...]


@dataclass(frozen=True, slots=True)
class Bookmark:
    title: str
    url: str
    icon: str


@dataclass(frozen=True, slots=True)
class BookmarkFolder:
    name: str
    folders: tuple[BookmarkFolder, ...]
    links: tuple[Bookmark, ...]

    def count(self) -> int:
        return len(self.links) + sum(folder.count() for folder in self.folders)

    def folder_count(self) -> int:
        return len(self.folders) + sum(f.folder_count() for f in self.folders)


def host_of(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    return netloc.removeprefix("www.")


def _strip_emphasis(text: str) -> str:
    return _MARKDOWN_EMPHASIS.sub("", text).strip()


def split_name_note(text: str) -> tuple[str, str]:
    """Split "Name - note" or "Name (note)" into its two halves."""
    text = text.strip()
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and text.startswith(_SEPARATOR, index):
            return text[:index].strip(), text[index + len(_SEPARATOR):].strip()
    if text.endswith(")") and " (" in text:
        index = text.index(" (")
        return text[:index].strip(), text[index + 2 : -1].strip()
    return text, ""


def parse_link_groups(source: str) -> tuple[LinkGroup, ...]:
    groups: list[LinkGroup] = []
    title = ""
    items: list[LinkItem] = []
    for line in source.splitlines():
        heading = _HEADING.match(line)
        if heading:
            if items:
                groups.append(LinkGroup(title, tuple(items)))
                items = []
            title = heading.group(2)
            continue
        for match in _ANCHOR.finditer(line):
            url = match.group(1)
            name, note = split_name_note(html.unescape(match.group(2)))
            items.append(LinkItem(name, note, url, host_of(url)))
    if items:
        groups.append(LinkGroup(title, tuple(items)))
    return tuple(groups)


def parse_url_groups(source: str) -> tuple[LinkGroup, ...]:
    """Groups of labelled URLs: "Label: https://..." or a bare URL per line."""
    groups: list[LinkGroup] = []
    title = ""
    intro: list[str] = []
    items: list[LinkItem] = []

    def close() -> None:
        if items:
            groups.append(LinkGroup(title, tuple(items), " ".join(intro)))

    for line in source.splitlines():
        heading = _HEADING.match(line)
        if heading:
            text = _strip_emphasis(heading.group(2))
            if items or not title:
                close()
                items = []
                intro = []
                label = text.rsplit(": ", 1)[-1]
                title = label.capitalize() if label.isupper() else label
            else:
                intro.append(text)
            continue
        match = _URL.search(line)
        if match:
            url = match.group(0)
            label = line[: match.start()].strip().rstrip(":").strip()
            items.append(LinkItem(host_of(url), label, url, host_of(url)))
    close()
    return tuple(groups)


def _paragraphs(lines: list[str]) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


# A semicolon only separates brand from note when the part before it is short.
MAX_BRAND_WORDS = 4


def _filament_note(paragraph: str) -> FilamentNote:
    url_match = _URL.match(paragraph)
    brand, note = split_name_note(paragraph)
    head, _, tail = paragraph.partition(";")
    if not note and tail and len(head.split()) <= MAX_BRAND_WORDS:
        brand, note = head.strip(), tail.strip()
    if not note:
        brand, _, note = paragraph.partition(" ")
    if " (" in brand and not url_match:
        brand, aside = brand.split(" (", 1)
        note = f"({aside} {note}".strip()
    if url_match:
        url = url_match.group(0)
        return FilamentNote(host_of(url), note, url)
    return FilamentNote(brand.strip(), note.strip(), "")


def _material(heading: str, lines: list[str]) -> Material:
    words = heading.split()
    name, tip = heading, ""
    if len(words) > MAX_MATERIAL_WORDS:
        name = words[0]
        rest = " ".join(words[1:])
        tip = rest[:1].upper() + rest[1:]
    notes = tuple(_filament_note(p) for p in _paragraphs(lines))
    return Material(name.rstrip(":"), tip, notes)


def parse_filament(source: str) -> FilamentGuide:
    """Top-level headings are tiers; second-level headings are materials."""
    sections: list[tuple[str, list[tuple[str, list[str]]], list[str]]] = []
    for line in source.splitlines():
        heading = _HEADING.match(line)
        if heading and len(heading.group(1)) == 1:
            sections.append((heading.group(2).rstrip(":").strip(), [], []))
        elif heading and sections:
            sections[-1][1].append((heading.group(2).strip(), []))
        elif sections:
            materials = sections[-1][1]
            (materials[-1][1] if materials else sections[-1][2]).append(line)
    tiers: list[Tier] = []
    prose: list[ProseSection] = []
    for title, materials, loose in sections:
        if materials:
            parsed = tuple(_material(heading, body) for heading, body in materials)
            tiers.append(Tier(title, parsed))
        elif _paragraphs(loose):
            prose.append(ProseSection(title, tuple(_paragraphs(loose))))
    return FilamentGuide(tuple(tiers), tuple(prose))


class _BookmarkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Node("")
        self.stack = [self.root]
        self.pending: _Node | None = None
        self.capture: str | None = None
        self.text: list[str] = []
        self.attrs: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "dl":
            self.stack.append(self.pending or self.stack[-1])
            self.pending = None
        elif tag in ("h3", "a"):
            self.capture = tag
            self.text = []
            self.attrs = {key: value or "" for key, value in attrs}

    def handle_endtag(self, tag: str) -> None:
        if tag == "dl" and len(self.stack) > 1:
            self.pending = None
            self.stack.pop()
        elif tag == self.capture:
            text = " ".join("".join(self.text).split())
            self.pending = None
            if tag == "h3":
                node = _Node(text)
                self.stack[-1].folders.append(node)
                self.pending = node
            else:
                icon = self.attrs.get("icon", "")
                usable = icon.startswith(ICON_PREFIX) and len(icon) <= MAX_ICON_CHARS
                href = self.attrs.get("href", "")
                link = Bookmark(text, href, icon if usable else "")
                self.stack[-1].links.append(link)
            self.capture = None

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.text.append(data)


class _Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.folders: list[_Node] = []
        self.links: list[Bookmark] = []

    def freeze(self) -> BookmarkFolder:
        folders = tuple(f.freeze() for f in self.folders)
        return BookmarkFolder(
            self.name, tuple(f for f in folders if f.count()), tuple(self.links)
        )


def parse_bookmarks(source: str) -> BookmarkFolder:
    """The bookmark tree, descending past wrapper folders that hold one folder."""
    parser = _BookmarkParser()
    parser.feed(source)
    parser.close()
    tree = parser.root.freeze()
    while not tree.links and len(tree.folders) == 1:
        tree = tree.folders[0]
    return tree
