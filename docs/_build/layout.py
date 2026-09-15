"""The shell every page shares: head, header, footer, search dialog and image viewer.

Icons are from Feather (https://feathericons.com), MIT licence.
"""

from __future__ import annotations

import html
import json
from collections.abc import Iterable, Sequence

import catalog as cat
from textfix import fix_prose
from urls import rel, root_prefix, section_url

LANG = "en-GB"
OG_LOCALE = "en_GB"
THEME_COLOUR = "#0b0f17"
THEME_STORAGE_KEY = "3dpi-theme"

ICONS = {
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
    "tool": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "bookmark": '<path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "sun": '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>',
    "moon": '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    "menu": '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "external": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "arrow": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
    "heart": '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "chevron-left": '<polyline points="15 18 9 12 15 6"/>',
    "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
}

_BOOT = (
    "(function(){var d=document.documentElement,k=d.getAttribute('data-theme-key'),t=null;"
    "try{t=localStorage.getItem(k);}catch(e){}"
    "if(t!=='light'&&t!=='dark'){t=window.matchMedia&&"
    "window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}"
    "d.setAttribute('data-theme',t);})();"
)


def esc(text: str) -> str:
    """Escape prose for HTML, applying the punctuation rules on the way."""
    return html.escape(fix_prose(text), quote=True)


def attr(value: str) -> str:
    """Escape a URL or other verbatim value for an attribute."""
    return html.escape(value, quote=True)


def icon(name: str, css: str = "icon") -> str:
    return (
        f'<svg class="{css}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        f"{ICONS[name]}</svg>"
    )


def crumbs_html(from_url: str, trail: Sequence[tuple[str, str | None]]) -> str:
    parts = []
    for label, url in trail:
        if url is None:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
        else:
            parts.append(f'<a href="{attr(rel(from_url, url))}">{esc(label)}</a>')
    separator = '<span class="crumb-sep" aria-hidden="true">/</span>'
    return f'<nav class="crumbs" aria-label="Breadcrumb">{separator.join(parts)}</nav>'


def _json_ld(block: dict[str, object]) -> str:
    text = json.dumps(block, ensure_ascii=False, separators=(",", ":"))
    return text.replace("</", "<\\/")


def _nav(root: str, active: str) -> str:
    links = []
    for section in cat.SECTIONS:
        if not section.in_main_nav:
            continue
        current = ' aria-current="page"' if section.key == active else ""
        links.append(
            f'<a href="{root}{section_url(section)}"{current}>{esc(section.nav_title)}</a>'
        )
    return "".join(links)


def _footer(root: str) -> str:
    knowledge = "".join(
        f'<li><a href="{root}{section_url(s)}">{esc(s.title)}</a></li>'
        for s in cat.SECTIONS
        if s.in_main_nav
    )
    more = "".join(
        f'<li><a href="{root}{section_url(s)}">{esc(s.title)}</a></li>'
        for s in cat.SECTIONS
        if not s.in_main_nav
    )
    projects = "".join(
        f'<li><a href="{attr(p.site)}">{esc(p.name)}</a></li>' for p in cat.PROJECTS
    )
    return f"""<footer class="site-footer">
<div class="wrap footer-grid">
<div class="footer-brand">
<a class="brand" href="{root or './'}"><img src="{root}icon-32.png" width="28" height="28" alt=""><span>{esc(cat.SITE_NAME)}</span></a>
<p>{esc(cat.SITE_TAGLINE)}, created and maintained by <a href="{attr(cat.GITHUB_PROFILE)}">{esc(cat.AUTHOR)}</a>.</p>
<a class="btn btn-ghost btn-sm" href="{attr(cat.DONATE_URL)}">{icon("heart")}Buy me a coffee</a>
</div>
<div><h2>Knowledge</h2><ul>{knowledge}</ul></div>
<div><h2>More</h2><ul>{more}{projects}</ul></div>
<div><h2>Source</h2><ul>
<li><a href="{attr(cat.REPO_URL)}">Repository on GitHub</a></li>
<li><a href="{attr(cat.LICENCE_URL)}">GPL-3.0 licence</a></li>
<li><a href="{attr(cat.ESSAY_URL)}">Why it exists</a></li>
</ul></div>
</div>
<div class="wrap footer-base">Free and open source under GPL-3.0. Icons from Feather (MIT).</div>
</footer>"""


_SEARCH_DIALOG = f"""<div class="search" data-search hidden>
<div class="search-backdrop" data-search-close></div>
<div class="search-panel" role="dialog" aria-modal="true" aria-label="Search the site">
<div class="search-field">{icon("search")}<input type="search" placeholder="Search guides, configs, bookmarks and tools" autocomplete="off" spellcheck="false" data-search-input aria-label="Search" aria-controls="search-results"><button type="button" class="kbd-btn" data-search-close>Esc</button></div>
<ul class="search-results" id="search-results" role="listbox" data-search-results></ul>
<p class="search-hint" data-search-hint data-default="Type to search every page, config file, bookmark and tool pick.">Type to search every page, config file, bookmark and tool pick.</p>
</div>
</div>"""

_LIGHTBOX = f"""<div class="lightbox" data-lightbox hidden role="dialog" aria-modal="true" aria-label="Image viewer">
<button type="button" class="lb-btn lb-close" data-lb-close aria-label="Close">{icon("x")}</button>
<button type="button" class="lb-btn lb-prev" data-lb-prev aria-label="Previous image">{icon("chevron-left")}</button>
<figure class="lb-figure"><img data-lb-img alt=""><figcaption><span data-lb-caption></span><a data-lb-full href="#">Open full size {icon("external")}</a></figcaption></figure>
<button type="button" class="lb-btn lb-next" data-lb-next aria-label="Next image">{icon("chevron-right")}</button>
</div>"""


def render_page(
    *,
    url: str,
    title: str,
    description: str,
    body: str,
    active: str = "",
    jsonld: Iterable[dict[str, object]] = (),
    og_image: str = "",
    head_title: str = "",
    base_href: str = "",
    noindex: bool = False,
) -> str:
    root = "" if base_href else root_prefix(url)
    page_title = head_title or f"{title} | {cat.SITE_NAME}"
    canonical = cat.SITE_URL + url
    image = og_image or cat.SITE_URL + cat.HERO_IMAGE
    blocks = "".join(
        f'<script type="application/ld+json">{_json_ld(block)}</script>' for block in jsonld
    )
    base = f'<base href="{attr(base_href)}">\n' if base_href else ""
    robots = "noindex" if noindex else "index, follow, max-image-preview:large"
    return f"""<!DOCTYPE html>
<html lang="{LANG}" data-root="{attr(root)}" data-theme-key="{THEME_STORAGE_KEY}">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="{esc(cat.AUTHOR)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{attr(canonical)}">
<meta name="theme-color" content="{THEME_COLOUR}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{attr(image)}">
<meta property="og:url" content="{attr(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(cat.SITE_NAME)}">
<meta property="og:locale" content="{OG_LOCALE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{root}icon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{root}icon-16.png">
<link rel="apple-touch-icon" href="{root}icon-180.png">
<script>{_BOOT}</script>
<link rel="stylesheet" href="{root}assets/site.css">
<script defer src="{root}assets/site.js"></script>
{blocks}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap header-inner">
<a class="brand" href="{root or './'}"><img src="{root}icon-32.png" width="28" height="28" alt=""><span>{esc(cat.SITE_NAME)}</span></a>
<nav class="main-nav" id="main-nav" aria-label="Sections">{_nav(root, active)}</nav>
<div class="header-tools">
<button type="button" class="search-trigger" data-search-open>{icon("search")}<span>Search</span><kbd>Ctrl K</kbd></button>
<button type="button" class="icon-btn" data-theme-toggle aria-label="Switch between light and dark theme">{icon("sun", "icon icon-sun")}{icon("moon", "icon icon-moon")}</button>
<a class="icon-btn" href="{attr(cat.REPO_URL)}" aria-label="Repository on GitHub">{icon("github")}</a>
<button type="button" class="icon-btn nav-toggle" data-nav-toggle aria-controls="main-nav" aria-expanded="false" aria-label="Menu">{icon("menu")}</button>
</div>
</div>
</header>
<main id="main" class="wrap main">
{body}
</main>
{_footer(root)}
{_SEARCH_DIALOG}
{_LIGHTBOX}
</body>
</html>
"""
