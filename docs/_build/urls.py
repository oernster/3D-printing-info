"""Site URL arithmetic: where a page lives and how one page links to another.

Every generated link is relative, so the site works on GitHub Pages under its
project path and from a local static server alike.
"""

from __future__ import annotations

import posixpath
from urllib.parse import quote

import catalog as cat

HOME_SLUG = "index"
INDEX_SUFFIX = "/index"
CONFIG_VIEWER = "configs/view.html"


def page_url(slug: str) -> str:
    """The site-root-relative URL of the page with this slug."""
    if slug == HOME_SLUG:
        return ""
    if slug.endswith(INDEX_SUFFIX):
        return slug[: -len(HOME_SLUG)]
    return f"{slug}.html"


def section_url(section: cat.Section) -> str:
    return f"{section.key}/"


def root_prefix(url: str) -> str:
    """The relative path from the page at `url` back to the site root."""
    return "../" * url.count("/")


def rel(from_url: str, to_url: str) -> str:
    """A link from the page at `from_url` to the site-root-relative `to_url`."""
    return (root_prefix(from_url) + to_url) or "./"


def viewer_url(path: str) -> str:
    return f"{CONFIG_VIEWER}?f={quote(path)}"


def is_viewable(path: str) -> bool:
    name = posixpath.basename(path)
    return name.endswith(cat.VIEWABLE_SUFFIXES) or name in cat.VIEWABLE_NAMES


def output_file(url: str) -> str:
    """The file under docs/ that serves `url`."""
    return f"{url}index.html" if not url or url.endswith("/") else url
