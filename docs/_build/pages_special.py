"""Builders for pages that are not plain articles.

Home, the tool and filament lists, STL sources, the bookmark explorer, image
galleries, related projects, the config library with its viewer and the 404.
"""

from __future__ import annotations

import json
import posixpath

import catalog as cat
from context import Site
from layout import attr, crumbs_html, esc, icon, render_page
from mdrender import render_markdown
from pages import (
    CARD_THUMB_EDGE,
    HOME_LABEL,
    Neighbours,
    figure_gallery,
    files_list,
    meta_row,
    page_head,
    page_jsonld,
    page_trail,
    pager,
)
from parsers import (
    Bookmark,
    BookmarkFolder,
    LinkItem,
    host_of,
    parse_bookmarks,
    parse_filament,
    parse_link_groups,
    parse_url_groups,
)
from urls import CONFIG_VIEWER, page_url, rel, section_url, viewer_url

HERO_EDGE = 1400
FEATURE_THUMBS = 4
TILE_LINKS = 3
TIER_CLASSES = ("tier-good", "tier-ok", "tier-bad")
NOT_FOUND_URL = "404.html"
CONFIG_INDEX_ID = "config-index"


def _output(site: Site, section: cat.Section, page: cat.Page, url: str, body: str) -> None:
    site.output(
        url,
        render_page(
            url=url,
            title=page.title,
            description=page.summary,
            body=body,
            active=section.key,
            jsonld=(page_jsonld(section, page),),
        ),
    )


def _filter_bar(key: str, placeholder: str) -> str:
    return (
        f'<div class="filter"><label class="filter-field">{icon("search")}'
        f'<span class="sr-only">Filter</span><input type="search" data-filter="{key}" '
        f'placeholder="{esc(placeholder)}" autocomplete="off"></label>'
        f'<span class="filter-count" data-filter-count="{key}" aria-live="polite"></span></div>'
    )


def _head(site: Site, section: cat.Section, page: cat.Page, url: str) -> str:
    return page_head(url, page_trail(section, page), page.title, page.summary, meta_row(section, page))


def _readme(site: Site, page: cat.Page, url: str) -> str:
    if not page.source:
        return ""
    doc = render_markdown(
        site.source_text(page),
        resolve_href=site.link_resolver(page.source, url),
        mentions=site.mention_hrefs(url),
    )
    return f'<div class="prose intro">{doc.html}</div>'


def _count(site: Site, key: str, amount: int) -> None:
    site.stats[key] = site.stats.get(key, 0) + amount


# Tools -----------------------------------------------------------------------


def _pick(site: Site, section: cat.Section, item: LinkItem) -> str:
    note = f'<span class="pick-note">{esc(item.note)}</span>' if item.note else ""
    site.add_search(item.name, item.url, section.title, " · ".join(p for p in (item.note, item.host) if p))
    return (
        f'<li class="pick" data-filter-item><a href="{attr(item.url)}" rel="noopener">'
        f'<span class="pick-name">{esc(item.name)}</span>{note}'
        f'<span class="pick-host">{attr(item.host)}{icon("external")}</span></a></li>'
    )


def build_tools(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    groups = parse_link_groups(site.read(page.source or ""))
    total = sum(len(g.items) for g in groups)
    _count(site, section.key, total)
    blocks = []
    for group in groups:
        items = "".join(_pick(site, section, item) for item in group.items)
        blocks.append(
            f'<section class="group" data-filter-group><h2 class="group-title">{esc(group.title)}'
            f'<span class="count">{len(group.items)}</span></h2><ul class="picks">{items}</ul></section>'
        )
    body = (
        _head(site, section, page, url)
        + _filter_bar("picks", f"Filter {total} picks")
        + f'<div data-filter-scope="picks">{"".join(blocks)}</div>'
        + pager(url, neighbours)
    )
    _output(site, section, page, url, body)
    site.add_search(page.title, url, section.title, page.summary)


def build_filament(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    guide = parse_filament(site.read(page.source or ""))
    tiers = []
    total = 0
    for position, tier in enumerate(guide.tiers):
        css = TIER_CLASSES[min(position, len(TIER_CLASSES) - 1)]
        materials = []
        count = 0
        for material in tier.materials:
            notes = []
            for note in material.notes:
                brand = esc(note.brand)
                if note.url:
                    brand = f'<a href="{attr(note.url)}" rel="noopener">{brand}</a>'
                notes.append(
                    f'<li data-filter-item><span class="brand">{brand}</span>'
                    f'<span class="brand-note">{esc(note.note)}</span></li>'
                )
                site.add_search(f"{note.brand} {material.name}", url, section.title, note.note)
            count += len(material.notes)
            tip = f'<p class="material-tip">{esc(material.tip)}</p>' if material.tip else ""
            materials.append(
                f'<div class="material" data-filter-group><h3>{esc(material.name)}</h3>{tip}'
                f'<ul class="brands">{"".join(notes)}</ul></div>'
            )
        total += count
        tiers.append(
            f'<section class="tier {css}" data-filter-group><h2 class="tier-title">'
            f'<span class="tier-dot"></span>{esc(tier.title)}<span class="count">{count}</span></h2>'
            f'{"".join(materials)}</section>'
        )
    _count(site, section.key, total)
    prose = "".join(
        f'<section class="prose closing"><h2>{esc(p.title)}</h2>'
        + "".join(f"<p>{esc(text)}</p>" for text in p.paragraphs)
        + "</section>"
        for p in guide.prose
    )
    body = (
        _head(site, section, page, url)
        + _filter_bar("filament", f"Filter {total} brand notes")
        + f'<div class="tiers" data-filter-scope="filament">{"".join(tiers)}</div>'
        + prose
        + pager(url, neighbours)
    )
    _output(site, section, page, url, body)
    site.add_search(page.title, url, section.title, page.summary)


# STL sources -----------------------------------------------------------------


def build_stls(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    groups = []
    for source in (page.source, *page.extra_sources):
        if source:
            groups.extend(parse_url_groups(site.read(source)))
    blocks = []
    total = 0
    for group in groups:
        total += len(group.items)
        cards = []
        for item in group.items:
            note = f'<span class="source-note">{esc(item.note)}</span>' if item.note else ""
            cards.append(
                f'<a class="source-card" href="{attr(item.url)}" rel="noopener">'
                f'<span class="source-host">{attr(item.host)}{icon("external")}</span>{note}</a>'
            )
            site.add_search(item.host, item.url, section.title, item.note)
        intro = f'<p class="group-intro">{esc(group.intro)}</p>' if group.intro else ""
        blocks.append(
            f'<section class="group"><h2 class="group-title">{esc(group.title)}'
            f'<span class="count">{len(group.items)}</span></h2>{intro}'
            f'<div class="source-grid">{"".join(cards)}</div></section>'
        )
    _count(site, section.key, total)
    body = _head(site, section, page, url) + "".join(blocks) + pager(url, neighbours)
    _output(site, section, page, url, body)
    site.add_search(page.title, url, section.title, page.summary)


# Bookmarks -------------------------------------------------------------------


def _bookmark(site: Site, section: cat.Section, link: Bookmark, trail: str) -> str:
    host = host_of(link.url)
    if link.icon:
        glyph = f'<img class="bm-icon" src="{attr(link.icon)}" width="16" height="16" alt="" loading="lazy">'
    else:
        glyph = f'<span class="bm-icon bm-letter" aria-hidden="true">{attr(host[:1].upper())}</span>'
    site.add_search(link.title, link.url, section.title, f"{trail} · {host}")
    return (
        f'<li data-filter-item><a href="{attr(link.url)}" rel="noopener">{glyph}'
        f'<span class="bm-title">{esc(link.title)}</span><span class="bm-host">{attr(host)}</span></a></li>'
    )


def _folder(site: Site, section: cat.Section, folder: BookmarkFolder, trail: str, depth: int) -> str:
    here = f"{trail} / {folder.name}" if trail else folder.name
    links = "".join(_bookmark(site, section, link, here) for link in folder.links)
    children = "".join(_folder(site, section, child, here, depth + 1) for child in folder.folders)
    open_attr = " open data-default-open" if depth == 0 else ""
    link_list = f'<ul class="bm-links">{links}</ul>' if links else ""
    return (
        f'<details class="bm-folder" data-filter-group{open_attr}><summary>{icon("folder")}'
        f'<span class="bm-name">{esc(folder.name)}</span><span class="count">{folder.count()}</span></summary>'
        f'<div class="bm-body">{link_list}{children}</div></details>'
    )


def build_bookmarks(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    export = page.files[0]
    tree = parse_bookmarks(site.read(export.path))
    total = tree.count()
    _count(site, section.key, total)
    site.highlights["bookmark_folders"] = tuple(f.name for f in tree.folders)
    folders = "".join(_folder(site, section, f, "", 0) for f in tree.folders)
    loose = "".join(_bookmark(site, section, link, tree.name) for link in tree.links)
    loose_block = f'<ul class="bm-links">{loose}</ul>' if loose else ""
    summary = (
        f'<div class="bm-summary"><div class="bm-stats"><span><strong>{total}</strong> links</span>'
        f'<span><strong>{tree.folder_count()}</strong> folders</span></div>'
        f'{files_list(site, url, page.files, "files files-inline")}</div>'
    )
    body = (
        _head(site, section, page, url)
        + _readme(site, page, url)
        + summary
        + _filter_bar("bookmarks", f"Filter {total} bookmarks")
        + f'<div class="bm-tree" data-filter-scope="bookmarks">{loose_block}{folders}</div>'
    )
    _output(site, section, page, url, body)
    site.add_search(page.title, url, section.title, page.summary)


# Galleries -------------------------------------------------------------------


def build_gallery(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    groups: list[str] = []
    for figure in page.figures:
        if figure.group not in groups:
            groups.append(figure.group)
    blocks = []
    for group in groups:
        members = tuple(f for f in page.figures if f.group == group)
        heading = (
            f'<h2 class="group-title">{esc(group)}<span class="count">{len(members)}</span></h2>'
            if group
            else ""
        )
        blocks.append(f'<section class="group">{heading}{figure_gallery(site, url, members, "gallery gallery-grid")}</section>')
        for figure in members:
            site.add_search(figure.caption, url, section.title, page.title)
    if page.files:
        blocks.append(
            f'<section class="group"><h2 class="group-title">Downloads</h2>'
            f'{files_list(site, url, page.files, "files files-wide")}</section>'
        )
        for ref in page.files:
            site.add_search(ref.label, url, section.title, ref.note)
    _count(site, section.key, len(page.figures) + len(page.files))
    body = _head(site, section, page, url) + _readme(site, page, url) + "".join(blocks)
    _output(site, section, page, url, body)
    site.add_search(page.title, url, section.title, page.summary)


# Projects --------------------------------------------------------------------


def project_card(from_url: str, project: cat.Project) -> str:
    extra = (
        f'<p class="project-extra">Command: <code>{attr(project.extra)}</code></p>' if project.extra else ""
    )
    return (
        f'<article class="project"><a class="project-media" href="{attr(project.site)}">'
        f'<img src="{attr(project.image)}" alt="{esc(project.image_alt)}" loading="lazy" decoding="async"></a>'
        f'<div class="project-body"><h3><img class="project-icon" src="{attr(rel(from_url, project.icon))}" '
        f'width="32" height="32" alt="">{esc(project.name)}</h3>'
        f'<p class="project-tagline">{esc(project.tagline)}</p><p>{esc(project.body)}</p>{extra}'
        f'<div class="project-actions"><a class="btn btn-primary btn-sm" href="{attr(project.site)}">Visit the site{icon("arrow")}</a>'
        f'<a class="btn btn-ghost btn-sm" href="{attr(project.repo)}">{icon("github")}Source</a></div></div></article>'
    )


def build_projects(site: Site, section: cat.Section, page: cat.Page, neighbours: Neighbours) -> None:
    url = page_url(page.slug)
    _count(site, section.key, len(cat.PROJECTS))
    cards = "".join(project_card(url, p) for p in cat.PROJECTS)
    for project in cat.PROJECTS:
        site.add_search(project.name, project.site, section.title, project.tagline)
    body = _head(site, section, page, url) + f'<div class="projects">{cards}</div>'
    _output(site, section, page, url, body)
    site.add_search(page.title, url, section.title, page.summary)


# Config library --------------------------------------------------------------


def build_configs(site: Site, section: cat.Section) -> None:
    hub_url = section_url(section)
    files = site.config_files()
    _count(site, section.key, len(files))
    grouped: dict[str, tuple[cat.Page, list[cat.FileRef]]] = {}
    for owner, ref in files:
        site.mark(ref.path)
        grouped.setdefault(owner.slug, (owner, []))[1].append(ref)

    hub_groups = []
    nav_groups = []
    index = []
    for owner, refs in grouped.values():
        rows = []
        links = []
        for ref in refs:
            name = posixpath.basename(ref.path)
            lines = site.line_count(ref.path)
            rows.append(
                f'<li data-filter-item><a class="config-row" href="{attr(rel(hub_url, viewer_url(ref.path)))}">'
                f'{icon("file")}<span class="config-label">{esc(ref.label)}</span>'
                f'<span class="config-path">{attr(ref.path)}</span><span class="config-lines">{lines} lines</span></a></li>'
            )
            links.append(
                f'<li data-filter-item><a data-viewer-link data-path="{attr(ref.path)}" '
                f'href="{attr(rel(CONFIG_VIEWER, viewer_url(ref.path)))}"><span>{esc(ref.label)}</span>'
                f"<small>{attr(name)}</small></a></li>"
            )
            index.append({"path": ref.path, "label": ref.label, "group": owner.title, "page": page_url(owner.slug)})
            site.add_search(ref.label, viewer_url(ref.path), section.title, f"{name} · {owner.title}")
        owner_link = f'<a class="group-link" href="{attr(rel(hub_url, page_url(owner.slug)))}">{esc(owner.title)}</a>'
        hub_groups.append(
            f'<section class="group" data-filter-group><h2 class="group-title">{owner_link}'
            f'<span class="count">{len(refs)}</span></h2><ul class="config-rows">{"".join(rows)}</ul></section>'
        )
        nav_groups.append(
            f'<div class="viewer-group" data-filter-group><p class="viewer-group-title">{esc(owner.title)}</p>'
            f'<ul>{"".join(links)}</ul></div>'
        )

    trail: list[tuple[str, str | None]] = [(HOME_LABEL, ""), (section.title, None)]
    hub_body = (
        page_head(hub_url, trail, section.title, section.blurb)
        + _filter_bar("configs", f"Filter {len(files)} files")
        + f'<div data-filter-scope="configs">{"".join(hub_groups)}</div>'
    )
    site.output(
        hub_url,
        render_page(url=hub_url, title=section.title, description=section.blurb, body=hub_body, active=section.key),
    )
    site.add_search(section.title, hub_url, "Sections", section.blurb)

    viewer_trail: list[tuple[str, str | None]] = [(HOME_LABEL, ""), (section.title, hub_url), ("Viewer", None)]
    payload = json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    viewer_body = f"""{crumbs_html(CONFIG_VIEWER, viewer_trail)}
<div class="viewer" data-viewer data-raw-base="{attr(cat.RAW_BASE)}" data-blob-base="{attr(cat.BLOB_BASE)}">
<aside class="viewer-nav">{_filter_bar("viewer", "Filter files")}<nav data-filter-scope="viewer" aria-label="Config files">{"".join(nav_groups)}</nav></aside>
<section class="viewer-main" aria-live="polite">
<header class="viewer-head"><div class="viewer-titles"><p class="viewer-group-name" data-viewer-group>Config library</p><h1 data-viewer-title>Choose a file</h1><p class="viewer-path" data-viewer-path></p></div>
<div class="viewer-actions"><button type="button" class="btn btn-ghost btn-sm" data-viewer-wrap aria-pressed="false">Wrap lines</button><button type="button" class="btn btn-ghost btn-sm" data-viewer-copy>Copy</button><button type="button" class="btn btn-ghost btn-sm" data-viewer-download>{icon("download")}Download</button><a class="btn btn-ghost btn-sm" data-viewer-github href="{attr(cat.REPO_URL)}">{icon("github")}GitHub</a></div></header>
<p class="viewer-context" data-viewer-context></p>
<div class="viewer-code" data-viewer-code><p class="viewer-empty">Pick a file from the list to read it here with highlighting.</p></div>
<noscript><p class="viewer-empty">The viewer needs JavaScript. Every file is also on <a href="{attr(cat.REPO_URL)}">GitHub</a>.</p></noscript>
</section>
</div>
<script type="application/json" id="{CONFIG_INDEX_ID}">{payload}</script>"""
    site.output(
        CONFIG_VIEWER,
        render_page(
            url=CONFIG_VIEWER,
            title="Config viewer",
            description=section.blurb,
            body=viewer_body,
            active=section.key,
        ),
    )


# Home ------------------------------------------------------------------------


def _find_page(slug: str) -> tuple[cat.Section, cat.Page]:
    for section in cat.SECTIONS:
        for page in section.pages:
            if page.slug == slug:
                return section, page
    raise KeyError(f"no page with slug {slug!r}")


def _home_jsonld() -> tuple[dict[str, object], ...]:
    return (
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": cat.SITE_URL + "#website",
                    "url": cat.SITE_URL,
                    "name": cat.SITE_NAME,
                    "description": cat.HOME_DESCRIPTION,
                    "inLanguage": "en-GB",
                    "publisher": {"@id": cat.SITE_URL + "#author"},
                },
                {
                    "@type": "Person",
                    "@id": cat.SITE_URL + "#author",
                    "name": cat.AUTHOR,
                    "url": cat.AUTHOR_URL,
                    "sameAs": [cat.GITHUB_PROFILE, cat.AUTHOR_URL],
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in cat.HOME_FAQ
                    ],
                },
            ],
        },
    )


def _home_hero(site: Site) -> str:
    hero = site.thumbs.get(f"docs/{cat.HERO_IMAGE}", HERO_EDGE)
    return f"""<section class="hero">
<div class="hero-copy">
<p class="eyebrow"><span class="pulse" aria-hidden="true"></span>{esc(cat.HOME_EYEBROW)}</p>
<h1 class="hero-title">{esc(cat.HOME_HEADLINE)} <span class="hero-accent">{esc(cat.HOME_HEADLINE_ACCENT)}</span></h1>
<p class="hero-lead">{esc(cat.HOME_LEAD)}</p>
<div class="hero-actions"><a class="btn btn-primary" href="guides/">Browse the guides{icon("arrow")}</a>
<button type="button" class="btn btn-ghost" data-search-open>{icon("search")}Search everything<kbd>Ctrl K</kbd></button></div>
<ul class="hero-points">{"".join(f"<li>{esc(point)}</li>" for point in cat.HOME_POINTS)}</ul>
</div>
<div class="hero-art"><img src="{attr(hero.url)}" width="{hero.width}" height="{hero.height}" alt="{esc(cat.HERO_ALT)}" fetchpriority="high" decoding="async"></div>
</section>"""


def _home_stats(site: Site) -> str:
    stats = []
    for section in cat.SECTIONS:
        if not section.unit:
            continue
        count = site.stats.get(section.key, len(section.pages))
        stats.append(
            f'<a class="stat" href="{section_url(section)}"><span class="stat-n">{count}</span>'
            f'<span class="stat-l">{esc(section.unit)}</span></a>'
        )
    return f'<section class="stats" aria-label="What is inside">{"".join(stats)}</section>'


def _home_paths() -> str:
    paths = []
    for path in cat.START_PATHS:
        links = []
        for slug in path.slugs:
            section, page = _find_page(slug)
            links.append(
                f'<li><a href="{attr(page_url(page.slug))}">{icon(section.icon)}<span>{esc(page.title)}</span></a></li>'
            )
        paths.append(f'<article class="path"><h3>{esc(path.title)}</h3><p>{esc(path.blurb)}</p><ul>{"".join(links)}</ul></article>')
    return (
        '<section class="block"><div class="block-head"><h2>Where to start</h2>'
        f'<p>{esc(cat.HOME_PATHS_LEAD)}</p></div><div class="paths">{"".join(paths)}</div></section>'
    )


def _home_tiles(site: Site) -> str:
    tiles = []
    for section in cat.SECTIONS:
        count = site.stats.get(section.key, len(section.pages))
        unit = f'<span class="tile-count">{count} {esc(section.unit)}</span>' if section.unit else ""
        tiles.append(
            f'<a class="tile" href="{section_url(section)}"><span class="tile-icon">{icon(section.icon)}</span>'
            f'<span class="tile-body"><span class="tile-title">{esc(section.title)}</span>{unit}'
            f'<span class="tile-blurb">{esc(section.blurb)}</span></span></a>'
        )
    return (
        '<section class="block"><div class="block-head"><h2>Everything in the notebook</h2>'
        f'<p>{esc(cat.HOME_TILES_LEAD)}</p></div><div class="tiles">{"".join(tiles)}</div></section>'
    )


def _home_features(site: Site) -> str:
    folders = "".join(
        f'<li class="chip">{esc(name)}</li>' for name in site.highlights.get("bookmark_folders", ())
    )
    schematic_page = cat.SCHEMATICS.pages[0]
    thumbs = "".join(
        f'<img src="{attr(t.url)}" width="{t.width}" height="{t.height}" alt="" loading="lazy" decoding="async">'
        for t in (site.thumbs.get(f.path, CARD_THUMB_EDGE) for f in schematic_page.figures[:FEATURE_THUMBS])
    )
    build_section, build_page = _find_page(cat.HOME_FEATURED_BUILD)
    photo = site.thumbs.get(build_page.figures[0].path, CARD_THUMB_EDGE)
    bookmarks = site.stats.get(cat.BOOKMARKS.key, 0)
    diagrams = site.stats.get(cat.SCHEMATICS.key, 0)
    return f"""<section class="block features">
<a class="feature feature-bookmarks" href="{section_url(cat.BOOKMARKS)}"><p class="feature-kicker">{icon("bookmark")}Bookmark explorer</p><h3>{bookmarks} curated links</h3><p>{esc(cat.BOOKMARKS.blurb)}</p><ul class="chip-row">{folders}</ul></a>
<a class="feature feature-pinouts" href="{section_url(cat.SCHEMATICS)}"><div class="feature-thumbs">{thumbs}</div><p class="feature-kicker">{icon("cpu")}Pinout library</p><h3>{diagrams} diagrams and models</h3><p>{esc(schematic_page.summary)}</p></a>
<a class="feature feature-build" href="{attr(page_url(build_page.slug))}"><div class="feature-photo"><img src="{attr(photo.url)}" width="{photo.width}" height="{photo.height}" alt="{esc(build_page.figures[0].caption)}" loading="lazy" decoding="async"></div><p class="feature-kicker">{icon(build_section.icon)}Featured build</p><h3>{esc(build_page.title)}</h3><p>{esc(build_page.summary)}</p></a>
</section>"""


def _home_about() -> str:
    why = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in cat.HOME_WHY)
    faq = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in cat.HOME_FAQ
    )
    return f"""<section class="block split">
<div class="why"><h2>Why this exists</h2>{why}<p><a class="text-link" href="{attr(cat.ESSAY_URL)}">The full reasoning on crankthecode.com{icon("arrow")}</a></p></div>
<div class="faq"><h2>Questions</h2>{faq}</div>
</section>
<section class="support"><div class="support-copy">{icon("heart")}<div><h2>{esc(cat.HOME_SUPPORT_TITLE)}</h2><p>{esc(cat.HOME_SUPPORT_TEXT)}</p></div></div>
<a class="btn btn-primary" href="{attr(cat.DONATE_URL)}">Buy me a coffee</a></section>"""


def build_home(site: Site) -> None:
    url = page_url("index")
    projects = "".join(project_card(url, p) for p in cat.PROJECTS)
    body = (
        _home_hero(site)
        + _home_stats(site)
        + _home_paths()
        + _home_tiles(site)
        + _home_features(site)
        + '<section class="block"><div class="block-head"><h2>Related projects</h2>'
        + f'<p>{esc(cat.PROJECTS_SECTION.blurb)}</p></div><div class="projects">{projects}</div></section>'
        + _home_about()
    )
    site.output(
        url,
        render_page(
            url=url,
            title=cat.SITE_NAME,
            head_title=cat.HOME_TITLE,
            description=cat.HOME_DESCRIPTION,
            body=body,
            jsonld=_home_jsonld(),
        ),
    )
    site.add_search(cat.SITE_NAME, url or "./", "Home", cat.HOME_DESCRIPTION)


def build_not_found(site: Site) -> None:
    body = f"""<section class="not-found">
<p class="nf-code">404</p>
<h1>That page has come unstuck from the bed</h1>
<p>The address may have changed when the site was rebuilt. Search for it or start from the home page.</p>
<div class="hero-actions"><a class="btn btn-primary" href="./">Go to the home page{icon("arrow")}</a>
<button type="button" class="btn btn-ghost" data-search-open>{icon("search")}Search</button></div>
</section>"""
    site.output(
        NOT_FOUND_URL,
        render_page(
            url=NOT_FOUND_URL,
            title="Page not found",
            description=cat.HOME_DESCRIPTION,
            body=body,
            base_href=cat.SITE_PATH,
            noindex=True,
        ),
    )
