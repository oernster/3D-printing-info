"""Punctuation house style for generated pages.

The site follows the portfolio's writing rules: no em or en dashes and no comma
touching a coordinating conjunction. The guides were written long before those
rules, so their prose is normalised on the way to the page. Code, preformatted
text and scripts pass through exactly as written.
"""

from __future__ import annotations

import html
import re
from collections.abc import Mapping

# Built from code points so this file never contains the characters it removes.
EM_DASH_CODEPOINT = 0x2014
EN_DASH_CODEPOINT = 0x2013
_EM = chr(EM_DASH_CODEPOINT)
_EN = chr(EN_DASH_CODEPOINT)
_DASHES = f"[{_EM}{_EN}]"
_RANGE = re.compile(rf"(\d)\s*{_DASHES}\s*(\d)")
_SPACED = re.compile(rf"\s+{_DASHES}\s+")
_BARE = re.compile(_DASHES)
_CONJUNCTIONS = "and|or|but"
_COMMA_BEFORE = re.compile(r",(\s+)(" + _CONJUNCTIONS + r")\b", re.IGNORECASE)
_COMMA_AFTER = re.compile(r"\b(" + _CONJUNCTIONS + r")(\s*),", re.IGNORECASE)

_TAG = re.compile(r"(<[^>]+>)")
_TAG_NAME = re.compile(r"^</?\s*([a-zA-Z][a-zA-Z0-9]*)")
_VERBATIM_TAGS = frozenset({"pre", "code", "script", "style", "textarea", "kbd"})
_LINK_TAG = "a"


def fix_prose(text: str) -> str:
    """Apply the punctuation rules to a run of plain prose."""
    text = _RANGE.sub(r"\1 to \2", text)
    text = _SPACED.sub(": ", text)
    text = _BARE.sub(", ", text)
    text = _COMMA_BEFORE.sub(r"\1\2", text)
    return _COMMA_AFTER.sub(r"\1\2", text)


def _mention_pattern(names: Mapping[str, str]) -> re.Pattern[str]:
    ordered = sorted(names, key=len, reverse=True)
    alternatives = "|".join(re.escape(name) for name in ordered)
    return re.compile(rf"(?<![\w/.-])({alternatives})(?![\w-])")


def fix_html(markup: str, mentions: Mapping[str, str] | None = None) -> str:
    """Fix prose inside HTML text nodes; link known file names where they appear."""
    pattern = _mention_pattern(mentions) if mentions else None
    verbatim = 0
    in_link = 0
    out: list[str] = []
    for part in _TAG.split(markup):
        if not part:
            continue
        name_match = _TAG_NAME.match(part)
        if name_match:
            name = name_match.group(1).lower()
            closing = part.startswith("</")
            step = -1 if closing else 1
            if name in _VERBATIM_TAGS and not part.endswith("/>"):
                verbatim = max(0, verbatim + step)
            if name == _LINK_TAG:
                in_link = max(0, in_link + step)
            out.append(part)
            continue
        if verbatim:
            out.append(part)
            continue
        text = fix_prose(part)
        if pattern is not None and mentions is not None and not in_link:
            text = pattern.sub(
                lambda m: (
                    f'<a href="{html.escape(mentions[m.group(1)], quote=True)}">'
                    f"{m.group(1)}</a>"
                ),
                text,
            )
        out.append(text)
    return "".join(out)
