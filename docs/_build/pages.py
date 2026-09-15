"""Builders for article pages, section hubs and the pieces they share."""

from __future__ import annotations

import posixpath
from urllib.parse import quote

import catalog as cat
from context import Site
from layout import attr, crumbs_html, esc, icon, render_page
from mdrender import render_markdown, render_snippet
from urls import is_viewable, page_url, rel, section_url, viewer_url

THUMB_EDGE = 960
CARD_THUMB_EDGE = 640
BYTES_PER_UNIT = 1024
SIZE_UNITS = ("B", "KB", "MB", "GB")
HOME_LABEL = "Home"

Neighbours = tuple[cat.Page | None, cat.Page | None]


def ordered_pages(section: cat.Section) -> tuple[cat.Page, ...]:
    if not section.groups:
        return section.pages
    return tuple(p for g in section.groups for p in section.pages if p.group == g)


def human_size(size: int) -> str:
    value = float(size)
    for unit in SIZE_UNITS:
        if value < BYTES_PER_UNIT or unit == SIZE_UNITS[-1]:
            return f"{value:.0f} {unit}" if unit == SIZE_UNITS[0] else f"{value:.1f} {unit}"
        value /= BYTES_PER_UNIT
    return f"{size} {SIZE_UNITS[0]}"


def page_trail(section: cat.Section, page: cat.Page) -> list[tuple[str, str | None]]:
    trail: list[tuple[str, str | None]] = [(HOME_LABEL, "")]
    if page_url(page.slug) == section_url(section):
        trail.append((section.title, None))
    else:
        trail.extend([(section.title, section_url(section)), (page.title, None)])
    return trail


def page_head(
    from_url: str,
    trail: list[tuple[str, str | None]],
    title: str,
    lead: str,
    meta: str = "",
) -> str:
    return (
        f'<header class="page-head">{crumbs_html(from_url, trail)}'
        f'<h1>{esc(title)}</h1><p class="page-lead">{esc(lead)}</p>{meta}</header>'
    )


def source_chip(path: str) -> str:
    href = cat.BLOB_BASE + quote(path)
    return f'<a class="chip chip-link" href="{attr(href)}">{icon("github")}Source on GitHub</a>'


def meta_row(section: cat.Section, page: cat.Page) -> str:
    chips = [f'<span class="chip">{icon(section.icon)}{esc(page.group or section.title)}</span>']
    if page.source:
        chips.append(source_chip(page.source))
    return f'<div class="page-meta">{"".join(chips)}</div>'


def figure_gallery(
    site: Site, from_url: str, figures: tuple[cat.Figure, ...], css: str = "gallery"
) -> str:
    items = []
    for figure in figures:
        site.mark(figure.path)
        thumb = site.thumbs.get(figure.path, THUMB_EDGE)
        full = cat.RAW_BASE + quote(figure.path)
        small = rel(from_url, thumb.url)
        items.append(
            f'<figure class="shot"><a class="zoom" href="{attr(full)}" '
            f'data-thumb="{attr(small)}" data-caption="{esc(figure.caption)}">'
            f'<img src="{attr(small)}" width="{thumb.width}" height="{thumb.height}" '
            f'alt="{esc(figure.caption)}" loading="lazy" decoding="async"></a>'
            f"<figcaption>{esc(figure.caption)}</figcaption></figure>"
        )
    return f'<div class="{css}">{"".join(items)}</div>'


def file_item(site: Site, from_url: str, ref: cat.FileRef) -> str:
    site.mark(ref.path)
    name = posixpath.basename(ref.path.rstrip("/"))
    if ref.path.endswith("/"):
        href, glyph, meta = cat.TREE_BASE + quote(ref.path.rstrip("/")), "folder", "Folder on GitHub"
    elif is_viewable(ref.path):
        lines = site.line_count(ref.path)
        href, glyph, meta = rel(from_url, viewer_url(ref.path)), "eye", f"{name} · {lines} lines"
    else:
        size = human_size(site.size(ref.path))
        href, glyph, meta = cat.BLOB_BASE + quote(ref.path), "download", f"{name} · {size} on GitHub"
    note = f'<span class="file-note">{esc(ref.note)}</span>' if ref.note else ""
    return (
        f'<li><a class="file" href="{attr(href)}">{icon(glyph)}<span class="file-body">'
        f'<span class="file-label">{esc(ref.label)}</span>'
        f'<span class="file-meta">{attr(meta)}</span>{note}</span></a></li>'
    )


def files_list(site: Site, from_url: str, files: tuple[cat.FileRef, ...], css: str = "files") -> str:
    items = "".join(file_item(site, from_url, ref) for ref in files)
    return f'<ul class="{css}">{items}</ul>'


def pager(from_url: str, neighbours: Neighbours) -> str:
    previous, following = neighbours
    links = []
    if previous is not None:
        links.append(
            f'<a class="pager-link" href="{attr(rel(from_url, page_url(previous.slug)))}">'
            f'<span class="pager-dir">{icon("arrow-left")}Previous</span>'
            f'<span class="pager-title">{esc(previous.title)}</span></a>'
        )
    else:
        links.append('<span class="pager-gap"></span>')
    if following is not None:
        links.append(
            f'<a class="pager-link pager-next" href="{attr(rel(from_url, page_url(following.slug)))}">'
            f'<span class="pager-dir">Next{icon("arrow")}</span>'
            f'<span class="pager-title">{esc(following.title)}</span></a>'
        )
    if previous is None and following is None:
        return ""
    return f'<nav class="pager" aria-label="More in this section">{"".join(links)}</nav>'


def page_jsonld(section: cat.Section, page: cat.Page) -> dict[str, object]:
    url = cat.SITE_URL + page_url(page.slug)
    crumbs = [
        {"@type": "ListItem", "position": 1, "name": HOME_LABEL, "item": cat.SITE_URL},
        {"@type": "ListItem", "position": 2, "name": section.title,
         "item": cat.SITE_URL + section_url(section)},
    ]
    if page_url(page.slug) != section_url(section):
        crumbs.append({"@type": "ListItem", "position": 3, "name": page.title, "item": url})
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": page.title,
                "description": page.summary,
                "url": url,
                "inLanguage": "en-GB",
                "author": {"@type": "Person", "name": cat.AUTHOR, "url": cat.AUTHOR_URL},
                "isPartOf": {"@type": "WebSite", "name": cat.SITE_NAME, "url": cat.SITE_URL},
            },
            {"@type": "BreadcrumbList", "itemListElement": crumbs},
        ],
    }


def og_image(site: Site, page: cat.Page) -> str:
    if not page.figures:
        return ""
    return cat.SITE_URL + site.thumbs.get(page.figures[0].path, THUMB_EDGE).url


def _toc_box(toc: tuple[tuple[int, str, str], ...]) -> str:
    if not toc:
        return ""
    items = "".join(
        f'<li class="toc-l{level}"><a href="#{attr(anchor)}">{esc(text)}</a></li>'
        for level, anchor, text in toc
    )
    return (
        '<nav class="aside-box toc" aria-label="On this page">'
        f'<h2 class="aside-title">On this page</h2><ol>{items}</ol></nav>'
    )


def build_article(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    resolve = site.link_resolver(page.source, url)
    mentions = site.mention_hrefs(url)
    parts: list[str] = []
    texts: list[str] = []
    toc: tuple[tuple[int, str, str], ...] = ()
    if page.intro:
        parts.append(render_snippet(page.intro, resolve_href=resolve, mentions=mentions))
        texts.append(page.intro)
    if page.source:
        doc = render_markdown(site.source_text(page), resolve_href=resolve, mentions=mentions)
        parts.append(doc.html)
        texts.append(doc.text)
        toc = doc.toc
    if page.figures:
        parts.append(figure_gallery(site, url, page.figures))
    aside_boxes = [_toc_box(toc)]
    if page.kind == "files":
        parts.append(f'<h2>Files</h2>{files_list(site, url, page.files, "files files-wide")}')
    elif page.files:
        aside_boxes.append(
            f'<div class="aside-box"><h2 class="aside-title">Files</h2>'
            f"{files_list(site, url, page.files)}</div>"
        )
    aside_boxes = [box for box in aside_boxes if box]
    aside = (
        f'<aside class="doc-aside"><div class="aside-sticky">{"".join(aside_boxes)}</div></aside>'
        if aside_boxes
        else ""
    )
    layout = "doc" if aside else "doc doc-single"
    body = (
        page_head(url, page_trail(section, page), page.title, page.summary, meta_row(section, page))
        + f'<div class="{layout}"><article class="prose" id="content">{"".join(parts)}</article>{aside}</div>'
        + pager(url, neighbours)
    )
    site.output(
        url,
        render_page(
            url=url,
            title=page.title,
            description=page.summary,
            body=body,
            active=section.key,
            jsonld=(page_jsonld(section, page),),
            og_image=og_image(site, page),
        ),
    )
    site.add_search(page.title, url, section.title, page.summary, " ".join(texts))


def page_card(site: Site, from_url: str, page: cat.Page) -> str:
    media = ""
    if page.figures:
        thumb = site.thumbs.get(page.figures[0].path, CARD_THUMB_EDGE)
        media = (
            f'<div class="card-media"><img src="{attr(rel(from_url, thumb.url))}" '
            f'width="{thumb.width}" height="{thumb.height}" alt="" loading="lazy" decoding="async"></div>'
        )
    css = "card has-media" if media else "card"
    return (
        f'<a class="{css}" href="{attr(rel(from_url, page_url(page.slug)))}">{media}'
        f'<div class="card-body"><h3>{esc(page.title)}</h3><p>{esc(page.summary)}</p>'
        f'<span class="card-more">Open{icon("arrow")}</span></div></a>'
    )


def build_hub(site: Site, section: cat.Section) -> None:
    url = section_url(section)
    groups = []
    for group in section.groups or ("",):
        members = [p for p in section.pages if p.group == group] if group else list(section.pages)
        if not members:
            continue
        heading = (
            f'<h2 class="group-title">{esc(group)}<span class="count">{len(members)}</span></h2>'
            if group
            else ""
        )
        cards = "".join(page_card(site, url, p) for p in members)
        groups.append(f'<section class="group">{heading}<div class="cards">{cards}</div></section>')
    trail: list[tuple[str, str | None]] = [(HOME_LABEL, ""), (section.title, None)]
    body = page_head(url, trail, section.title, section.blurb) + "".join(groups)
    site.output(
        url,
        render_page(url=url, title=section.title, description=section.blurb, body=body, active=section.key),
    )
    site.add_search(section.title, url, "Sections", section.blurb)
