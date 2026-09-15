"""Markdown to HTML for the repository's guides.

The guides were written for GitHub, where heading markup is often used for
emphasis: whole sentences, shell commands and numbered steps all appear as
headings. Rendering that literally gives a page of shouting, so each block is
classified first and rendered as what it actually is:

* a heading that is really a command becomes a code block;
* a heading that is a numbered step becomes a styled step;
* a heading that is a sentence, a link or too long becomes a paragraph;
* a heading with no content under it becomes a paragraph;
* a short heading ending in an exclamation mark becomes a banner;
* NOTE and CAVEAT paragraphs become callouts.

The first heading of a file is its title, which the page already shows.
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass

import markdown

from textfix import fix_html

MAX_HEADING_WORDS = 9
TOC_WORDS = 8
TOP_LEVEL = 2
DEEPEST_LEVEL = 4
COMMAND_WORDS = frozenset(
    {
        "sudo", "git", "cd", "make", "ssh", "ls", "lsusb", "systemctl", "ln",
        "chown", "chmod", "rsync", "wsl", "mkdir", "v4l2-ctl", "apt", "nano",
        "tar", "alsamixer", "aplay",
    }
)
# Words that show a line starting with a command word is really a sentence.
SENTENCE_WORDS = frozenset(
    {"the", "into", "to", "a", "your", "if", "then", "e.g.", "for", "of", "on",
     "with", "from", "it", "you", "this"}
)
EXTENSIONS = ("fenced_code", "tables", "sane_lists", "md_in_html", "toc")

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_STEP = re.compile(r"^(\d+[a-z]?|[a-z])\)\s+(.+)$")
_PLAIN_NUMBER = re.compile(r"^(\s*)(\d+)\)\s+")
_PLAIN_LETTER = re.compile(r"^(\s*)(\d+[a-z]|[a-z])\)\s+")
_LIST_ITEM = re.compile(r"^\s*(?:\d+\.|[*+-])\s+")
_CODE_ONLY = re.compile(r"^`+([^`]+)`+$")
_MACRO = re.compile(r"^[A-Z0-9]+_[A-Z0-9_]+(?=\s|$)")
_MACRO_SPLIT = re.compile(r"^(\S+(?:\s+[A-Za-z_]+=\S+)*)\s*(.*)$")
_NOTE = re.compile(r"^(?:\*\*)?(?:NOTE\s?\d*|CAVEAT|WARNING)\b")
_LINKISH = re.compile(r"https?://|\]\(|<a\s", re.IGNORECASE)
_BARE_URL = re.compile(r"(?<![<(\"'=\w/])(https?://\w[^\s<>\"'`]*)")
_TRAILING = ".,;:!?)"
_IMAGE_LINE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
_CODE_SPAN = re.compile(r"(`+[^`]*`+)")
# A "<" that does not open an inline tag or an autolink is literal text, such as
# "<your username>", which markdown would otherwise swallow as unknown HTML.
_STRAY_ANGLE = re.compile(
    r"<(?!/?(?:a|b|i|em|strong|code|br|img|span|sup|sub|kbd)\b|https?://)"
)

_IMG_PARAGRAPH = re.compile(r"<p>\s*(<img\s[^>]*>)\s*</p>")
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_LINK_PARAGRAPHS = re.compile(r"(?:<p>\s*<a\s[^>]*>.*?</a>\s*</p>\s*)+", re.DOTALL)
_LINK_PARAGRAPH = re.compile(r"<p>\s*(<a\s[^>]*>.*?</a>)\s*</p>", re.DOTALL)
_ADJACENT_CODE = re.compile(r"</code></pre>\s*<pre><code>")
_HREF = re.compile(r'(<a\s[^>]*?href=")([^"]*)(")')
_TOC_HEADING = re.compile(r'<h([23])([^>]*)\sid="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL)
_STEP_NUMBER = re.compile(r'<span class="step-n">.*?</span>', re.DOTALL)
_TAGS = re.compile(r"<[^>]+>")


@dataclass(frozen=True, slots=True)
class Rendered:
    html: str
    toc: tuple[tuple[int, str, str], ...]
    text: str


@dataclass(frozen=True, slots=True)
class _Item:
    kind: str
    lines: tuple[str, ...] = ()
    level: int = 0
    marker: str = ""
    from_heading: bool = False


def _words(text: str) -> int:
    return len(text.split())


def _is_command(text: str) -> bool:
    tokens = text.split()
    if not tokens:
        return False
    first = tokens[0]
    if not (first in COMMAND_WORDS or first.startswith("./")):
        return False
    return not any(token.lower() in SENTENCE_WORDS for token in tokens[1:])


def _autolink(line: str) -> str:
    def wrap(match: re.Match[str]) -> str:
        url = match.group(1)
        trail = ""
        while url and url[-1] in _TRAILING:
            trail = url[-1] + trail
            url = url[:-1]
        return f"<{url}>{trail}"

    parts = _CODE_SPAN.split(line)
    for index in range(0, len(parts), 2):
        escaped = _STRAY_ANGLE.sub("&lt;", parts[index])
        parts[index] = _BARE_URL.sub(wrap, escaped)
    return "".join(parts)


def _split_blocks(text: str) -> list[_Item]:
    lines = text.replace("\r\n", "\n").split("\n")
    blocks: list[_Item] = []
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            blocks.append(_Item("para", tuple(buffer)))
            buffer.clear()

    index = 0
    while index < len(lines):
        line = lines[index]
        if _FENCE.match(line):
            flush()
            fence = [line]
            index += 1
            while index < len(lines) and not _FENCE.match(lines[index]):
                fence.append(lines[index])
                index += 1
            if index < len(lines):
                fence.append(lines[index])
            blocks.append(_Item("fence", tuple(fence)))
        elif (match := _HEADING.match(line)) is not None:
            flush()
            blocks.append(_Item("heading", (match.group(2),), len(match.group(1))))
        elif line.strip():
            buffer.append(line)
        else:
            flush()
        index += 1
    flush()
    return blocks


def _classify_heading(block: _Item) -> list[_Item]:
    text = block.lines[0].strip()
    level = block.level
    if (match := _CODE_ONLY.match(text)) is not None:
        return [_Item("code", (match.group(1).strip(),))]
    if _is_command(text):
        return [_Item("code", (text,))]
    if _MACRO.match(text):
        split = _MACRO_SPLIT.match(text)
        code, note = (split.group(1), split.group(2).strip()) if split else (text, "")
        items = [_Item("code", (code,))]
        if note:
            items.append(_Item("para", (note,)))
        return items
    if (match := _STEP.match(text)) is not None:
        return [_Item("step", (match.group(2),), level, match.group(1))]
    if _NOTE.match(text) and _words(text) > 1:
        return [_Item("callout", (text,))]
    sentence = text.endswith((".", "?")) and not text.endswith("...")
    if _LINKISH.search(text) or _words(text) > MAX_HEADING_WORDS or sentence:
        return [_Item("para", (text,), from_heading=True)]
    if text.endswith("!"):
        return [_Item("shout", (text,), level)]
    return [_Item("heading", (text.rstrip(":"),), level)]


def _classify_para(block: _Item) -> list[_Item]:
    if len(block.lines) == 1:
        text = block.lines[0].strip()
        if _is_command(text) or _MACRO.match(text):
            return [_Item("code", (text,))]
    if _NOTE.match(block.lines[0].strip()):
        return [_Item("callout", block.lines)]
    return [block]


def _classify(blocks: list[_Item]) -> list[_Item]:
    items: list[_Item] = []
    for position, block in enumerate(blocks):
        if block.kind == "heading":
            text = block.lines[0].strip()
            title_like = not _STEP.match(text) and not _is_command(text)
            if position == 0 and title_like and _words(text) <= MAX_HEADING_WORDS:
                continue
            items.extend(_classify_heading(block))
        elif block.kind == "para":
            items.extend(_classify_para(block))
        else:
            items.append(block)
    if items and items[0].kind == "para" and items[0].from_heading:
        items[0] = _Item("lead", items[0].lines)
    return _demote_empty_headings(items)


def _demote_empty_headings(items: list[_Item]) -> list[_Item]:
    """A heading with nothing under it (and no deeper heading) is not a heading."""
    result = list(items)
    has_content = False
    next_level: int | None = None
    for index in range(len(result) - 1, -1, -1):
        item = result[index]
        if item.kind == "heading":
            parent = next_level is not None and next_level > item.level
            if has_content or parent:
                has_content = False
                next_level = item.level
            else:
                result[index] = _Item("para", item.lines)
                has_content = True
        elif item.kind == "shout":
            has_content = False
            next_level = item.level
        else:
            has_content = True
    return result


def _para_markdown(lines: tuple[str, ...]) -> str:
    out: list[str] = []
    previous_was_item = False
    for line in lines:
        if _IMAGE_LINE.match(line):
            # An image written straight under a sentence becomes its own figure.
            if out and out[-1]:
                out.append("")
            out.extend([line, ""])
            previous_was_item = False
            continue
        letter = _PLAIN_LETTER.match(line)
        if letter and not _PLAIN_NUMBER.match(line):
            line = f"{letter.group(1)}**{letter.group(2)})** {line[letter.end():]}"
        else:
            line = _PLAIN_NUMBER.sub(lambda m: f"{m.group(1)}{m.group(2)}. ", line, 1)
        is_item = bool(_LIST_ITEM.match(line))
        if is_item and out and not previous_was_item:
            out.append("")
        previous_was_item = is_item
        out.append(_autolink(line))
    return "\n".join(out)


def _assemble(items: list[_Item]) -> str:
    levels = [item.level for item in items if item.kind == "heading"]
    shallowest = min(levels) if levels else TOP_LEVEL
    parts: list[str] = []
    for item in items:
        text = "\n".join(item.lines)
        if item.kind == "heading":
            level = min(DEEPEST_LEVEL, item.level - shallowest + TOP_LEVEL)
            parts.append(f"{'#' * level} {text}")
        elif item.kind == "step":
            css = "step step-sub" if item.marker.isalpha() else "step"
            marker = html.escape(item.marker)
            parts.append(
                f'<h3 class="{css}" markdown="span">'
                f'<span class="step-n">{marker}</span> {_autolink(text)}</h3>'
            )
        elif item.kind == "lead":
            parts.append(f'<p class="lead" markdown="span">{_autolink(text)}</p>')
        elif item.kind == "shout":
            parts.append(f'<p class="shout" markdown="span">{text}</p>')
        elif item.kind == "callout":
            body = _para_markdown(item.lines)
            parts.append(f'<div class="callout" markdown="1">\n\n{body}\n\n</div>')
        elif item.kind == "code":
            parts.append("```\n" + text + "\n```")
        elif item.kind == "fence":
            parts.append(text)
        else:
            parts.append(_para_markdown(item.lines))
    return "\n\n".join(parts) + "\n"


def _figure(match: re.Match[str]) -> str:
    attrs = dict(_ATTR.findall(match.group(1)))
    src = attrs.get("src", "")
    alt = attrs.get("alt", "")
    caption = attrs.get("title") or alt
    return (
        f'<figure class="shot"><a class="zoom" href="{src}" data-caption="{caption}">'
        f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async"></a>'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def _link_list(match: re.Match[str]) -> str:
    anchors = _LINK_PARAGRAPH.findall(match.group(0))
    items = "".join(f"<li>{anchor}</li>" for anchor in anchors)
    return f'<ul class="linklist">{items}</ul>\n'


def _finish(
    raw: str, resolve_href: Callable[[str], str], mentions: Mapping[str, str]
) -> str:
    out = _IMG_PARAGRAPH.sub(_figure, raw)
    out = _LINK_PARAGRAPHS.sub(_link_list, out)
    out = _ADJACENT_CODE.sub("\n", out)
    out = _HREF.sub(
        lambda m: m.group(1)
        + html.escape(resolve_href(html.unescape(m.group(2))), quote=True)
        + m.group(3),
        out,
    )
    return fix_html(out, mentions)


def _toc(rendered: str) -> tuple[tuple[int, str, str], ...]:
    entries: list[tuple[int, str, str]] = []
    for level, _attrs, anchor, inner in _TOC_HEADING.findall(rendered):
        text = html.unescape(_TAGS.sub("", _STEP_NUMBER.sub("", inner))).strip()
        words = text.split()
        if len(words) > TOC_WORDS:
            text = " ".join(words[:TOC_WORDS]) + "…"
        entries.append((int(level), anchor, text))
    return tuple(entries)


def plain_text(rendered: str) -> str:
    return " ".join(html.unescape(_TAGS.sub(" ", rendered)).split())


def render_markdown(
    source: str,
    *,
    resolve_href: Callable[[str], str],
    mentions: Mapping[str, str],
) -> Rendered:
    """Render a guide, classifying its blocks first (see the module docstring)."""
    prepared = _assemble(_classify(_split_blocks(source)))
    raw = markdown.markdown(prepared, extensions=list(EXTENSIONS))
    finished = _finish(raw, resolve_href, mentions)
    return Rendered(finished, _toc(finished), plain_text(finished))


def render_snippet(
    source: str,
    *,
    resolve_href: Callable[[str], str],
    mentions: Mapping[str, str],
) -> str:
    """Render short markdown written for the site, without classification."""
    raw = markdown.markdown(_autolink(source), extensions=list(EXTENSIONS))
    return _finish(raw, resolve_href, mentions)
