#!/usr/bin/env python3
"""
Rebuild the shared chrome of every page on yuriytkach.com.

The site is plain static HTML with no framework. Before this script existed the
header, footer and <head> were copy-pasted into ~70 files, so any change to the
navigation or the design meant editing all of them by hand. This script owns
those regions instead:

  * <head>         — fonts, metadata, Open Graph, theme bootstrap
  * <header>       — logo, navigation, theme toggle, mobile menu
  * <footer>       — contact links, copyright
  * volunteer list — the post grid, grouped by year, rendered into the HTML
  * post pages     — English/Ukrainian pair link and previous/next navigation
  * sitemap.xml, robots.txt

Everything inside <main> on the non-post pages is hand-authored and left alone.

Usage:  python3 tools/build.py
"""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://yuriytkach.com"
POSTS_JSON = ROOT / "data" / "volunteer-posts.json"

FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Geologica:wght@300..800"
    "&family=IBM+Plex+Mono:wght@400;500;600"
    "&family=Literata:opsz,wght@7..72,400..700"
    "&display=swap"
)

# Applied before the stylesheet so a stored theme never flashes the wrong ground.
THEME_BOOTSTRAP = (
    "(function(){try{var t=localStorage.getItem('theme');"
    "if(t!=='light'&&t!=='dark')t='system';"
    "var r=document.documentElement;r.setAttribute('data-theme-pref',t);"
    "if(t!=='system')r.setAttribute('data-theme',t);}catch(e){}})();"
)

NAV = [
    ("/", "Home"),
    ("/resume/", "Experience"),
    ("/stats/", "Stats"),
    ("/volunteer/", "Volunteering"),
    ("/contact/", "Contact"),
]

SOCIAL = [
    ("https://www.linkedin.com/in/yuriytkach", "LinkedIn"),
    ("https://github.com/yuriytkach", "GitHub"),
    ("https://www.youtube.com/channel/UCdXqgQdGW5go6nkkBbUVSMA", "YouTube"),
    ("https://www.buymeacoffee.com/ytkach", "Buy Me a Coffee"),
]

# Per-page metadata for the hand-authored pages. Posts get theirs from the JSON.
PAGES = {
    "index.html": dict(
        url="/",
        title="Home",
        desc="Yuriy Tkach — software architect and team lead. Backend systems in "
             "Java and Scala, cloud-native architecture, engineering mentorship, "
             "and volunteer work supporting Ukraine.",
        hero="hero-home",
        priority="1.0",
    ),
    "resume/index.html": dict(
        url="/resume/",
        title="Experience",
        desc="Twenty years of hands-on software architecture and engineering "
             "leadership across fintech, blockchain, FX trading and developer "
             "productivity. Available for consulting and design reviews.",
        hero="hero-resume",
        priority="0.9",
    ),
    "stats/index.html": dict(
        url="/stats/",
        title="Coding Stats",
        desc="GitHub contributions and coding activity for Yuriy Tkach — what I "
             "work on, in which languages, and when.",
        hero="hero-stats",
        priority="0.5",
    ),
    "volunteer/index.html": dict(
        url="/volunteer/",
        title="Volunteering",
        desc="Fundraiser reports supporting Ukrainian soldiers since 2022 — what "
             "was raised, what it bought, and the receipts for all of it.",
        hero="hero-volunteer",
        priority="0.9",
    ),
    "contact/index.html": dict(
        url="/contact/",
        title="Contact",
        desc="Get in touch with Yuriy Tkach — email first, plus LinkedIn, GitHub "
             "and YouTube if a public channel suits you better.",
        hero="hero-contact",
        priority="0.7",
    ),
    "calendar/index.html": dict(
        url="/calendar/",
        title="Calendar",
        desc="Public free and busy calendar — pick a time that works and get in touch.",
        hero="hero-calendar",
        priority="0.4",
    ),
    "404.html": dict(
        url="/404.html",
        title="Page Not Found",
        desc="That page does not exist.",
        hero="hero-volunteer",
        priority=None,
        noindex=True,
    ),
}

ICON = {
    "system": '<svg class="ti ti-system" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16Z" fill="currentColor" stroke="none"/></svg>',
    "light": '<svg class="ti ti-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="4.4"/><path d="M12 2.6v2.2M12 19.2v2.2M21.4 12h-2.2M4.8 12H2.6M18.6 5.4l-1.6 1.6M7 17l-1.6 1.6M18.6 18.6 17 17M7 7 5.4 5.4"/></svg>',
    "dark": '<svg class="ti ti-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 13.6A8.2 8.2 0 1 1 10.4 4a6.6 6.6 0 0 0 9.6 9.6Z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3.5 7h17M3.5 12h17M3.5 17h17"/></svg>',
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def clip(text: str, limit: int = 165) -> str:
    """Trim to a whole word so a description never ends mid-syllable."""
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,.;:—-") + "…"


def clean_excerpt(text: str) -> str:
    """The Ghost export scraped the donation widget's button label into 28 of
    the excerpts, so they all open with 'View Donations'. Drop it."""
    return re.sub(r"^\s*View Donations\s*", "", text or "").strip()


def has_webp(stem: str) -> bool:
    return (ROOT / "assets" / "images" / f"{stem}.webp").exists()


def webp_for(src: str) -> str | None:
    """The WebP sibling of an image path, if tools/optimize_images.py made one."""
    if not src.startswith("/assets/images/"):
        return None
    candidate = Path(src).with_suffix(".webp").as_posix()
    return candidate if (ROOT / candidate.lstrip("/")).exists() else None


def thumb_for(cover: str) -> str | None:
    """The 640px cover thumbnail used by the volunteering index."""
    if not cover:
        return None
    candidate = f"/assets/images/covers/{Path(cover).stem}.webp"
    return candidate if (ROOT / candidate.lstrip("/")).exists() else None


# ---------------------------------------------------------------------------
# chrome
# ---------------------------------------------------------------------------

def build_head(*, title, desc, url, image, lang, extra_head, hero, og_type, noindex):
    canonical = SITE + url
    img_abs = SITE + image
    robots = '\n<meta name="robots" content="noindex, follow" />' if noindex else ""

    preload_hero = ""
    if hero and has_webp(hero):
        preload_hero = (
            f'\n<link rel="preload" as="image" type="image/webp" fetchpriority="high" '
            f'href="/assets/images/{hero}.webp" />'
        )

    og_locale = "uk_UA" if lang == "uk" else "en_US"

    return f"""<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="color-scheme" content="light dark" />
<title>{esc(title)} - Yuriy Tkach</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{canonical}" />{robots}
<link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico" />
<meta property="og:type" content="{og_type}" />
<meta property="og:site_name" content="Yuriy Tkach" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{img_abs}" />
<meta property="og:locale" content="{og_locale}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(title)}" />
<meta name="twitter:description" content="{esc(desc)}" />
<meta name="twitter:image" content="{img_abs}" />
<script>{THEME_BOOTSTRAP}</script>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="{FONTS}" />
<link rel="stylesheet" href="/assets/css/styles.css" />{preload_hero}{extra_head}
<script defer src="/assets/js/main.js"></script>
</head>"""


def build_header(current_url: str) -> str:
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current_url else ""
        links.append(f'        <a href="{href}"{cur}>{label}</a>')
    nav = "\n".join(links)

    return f"""<a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap nav-row">
      <a class="brand" href="/" aria-label="Yuriy Tkach — home"><img src="/assets/images/logo-software-developer.svg" alt="Yuriy Tkach" class="site-logo" width="86" height="38" /></a>
      <div class="nav-tools">
        <nav id="main-nav" class="site-nav" aria-label="Main navigation">
{nav}
        </nav>
        <button class="theme-toggle" type="button" aria-label="Colour theme: system. Activate to change." title="Theme: system">{ICON['system']}{ICON['light']}{ICON['dark']}</button>
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Menu">{ICON['menu']}</button>
      </div>
    </div>
  </header>"""


def build_footer() -> str:
    links = "\n".join(
        f'          <a href="{u}" target="_blank" rel="noopener">{t}</a>' for u, t in SOCIAL
    )
    return f"""<footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <a href="mailto:me@yuriytkach.com">me@yuriytkach.com</a>
        <div class="footer-links">
{links}
        </div>
      </div>
      <p class="copyright">&copy; <span id="year">{date.today().year}</span> Yuriy Tkach <span class="copyright-note">Built as plain HTML, no tracking</span></p>
    </div>
  </footer>"""


# ---------------------------------------------------------------------------
# posts
# ---------------------------------------------------------------------------

def load_posts():
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))

    for p in posts:
        page = ROOT / "volunteer" / "posts" / p["slug"] / "index.html"
        lang = "en"
        if page.exists():
            m = re.search(r'<html lang="([a-z]{2})"', page.read_text(encoding="utf-8"))
            if m:
                lang = m.group(1)
        p["lang"] = lang

    posts.sort(key=lambda p: (p["dateISO"], p["slug"]), reverse=True)

    # English ↔ Ukrainian pairs: "<slug>-ua" or "<slug>-ua-<n>" for "<slug>-<n>".
    by_slug = {p["slug"]: p for p in posts}
    for p in posts:
        p["pair"] = None
    for p in posts:
        if p["lang"] != "uk":
            continue
        slug = p["slug"]
        candidates = []
        if slug.endswith("-ua"):
            candidates.append(slug[:-3])
        m = re.match(r"^(.*)-ua-(\d+)$", slug)
        if m:
            candidates.append(f"{m.group(1)}-{m.group(2)}")
        for c in candidates:
            other = by_slug.get(c)
            if other is not None and other["lang"] == "en":
                p["pair"] = c
                other["pair"] = slug
                break

    return posts


def render_volunteer_list(posts) -> str:
    by_year: dict[str, list] = {}
    for p in posts:
        by_year.setdefault(p["dateISO"][:4], []).append(p)

    out = [
        '<div class="post-toolbar">',
        '    <p class="filter-label">Language</p>',
        '    <div class="filter-group" role="group" aria-label="Filter reports by language">',
        '      <button class="filter-btn is-on" type="button" data-lang="all" aria-pressed="true">All</button>',
        '      <button class="filter-btn" type="button" data-lang="en" aria-pressed="false">English</button>',
        '      <button class="filter-btn" type="button" data-lang="uk" aria-pressed="false">Українська</button>',
        "    </div>",
        f'    <p class="post-count">{len(posts)} reports</p>',
        "  </div>",
    ]

    for year in sorted(by_year, reverse=True):
        group = by_year[year]
        out.append(f'  <h2 class="post-year no-mark">{year} <span class="sr-only">reports</span></h2>')
        out.append('  <div class="post-grid">')
        for p in group:
            cover = p.get("cover")
            img = ""
            if cover:
                img = (
                    f'<img src="{esc(cover)}" alt="" loading="lazy" decoding="async" '
                    f'width="400" height="250" />'
                )
                thumb = thumb_for(cover)
                if thumb:
                    img = (
                        f'<picture><source srcset="{esc(thumb)}" type="image/webp" />{img}</picture>'
                    )
            tag = "UA" if p["lang"] == "uk" else "EN"
            out.append(
                f'    <a class="post-card" href="/volunteer/posts/{p["slug"]}/" data-lang="{p["lang"]}">'
                f"{img}"
                f'<div class="meta">'
                f'<div class="post-card-head"><time datetime="{p["dateISO"]}">{esc(p["dateHuman"])}</time>'
                f'<span class="lang-tag">{tag}</span></div>'
                f'<h3>{esc(p["title"])}</h3>'
                f'<p>{esc(clip(clean_excerpt(p.get("excerpt", "")), 130))}</p>'
                f"</div></a>"
            )
        out.append("  </div>")

    return "\n".join(out)


def picturize(src: str) -> str:
    """Serve post photographs as WebP with the original as the fallback.

    Idempotent: a previous run's <picture> wrapper is unwrapped first.
    """
    src = re.sub(
        r'<picture><source srcset="[^"]*" type="image/webp" />(<img [^>]*>)</picture>',
        r"\1", src,
    )

    # the Ghost export hides a broken image by hiding its parent — which is now
    # the <picture>, leaving an orphan caption behind
    src = src.replace(
        """onerror="this.parentElement.style.display='none'\"""",
        """onerror="this.closest('.post-gallery-item').style.display='none'\"""",
    )

    def wrap(mo):
        tag = mo.group(0)
        alt = webp_for(mo.group(1))
        if not alt:
            return tag
        return f'<picture><source srcset="{alt}" type="image/webp" />{tag}</picture>'

    return re.sub(r'<img [^>]*src="(/assets/images/posts/[^"]+)"[^>]*>', wrap, src)


def render_pair(post, by_slug) -> str:
    if not post.get("pair"):
        return ""
    other = by_slug[post["pair"]]
    if other["lang"] == "uk":
        label, cta = "Ukrainian", "Читати українською"
    else:
        label, cta = "English", "Read in English"
    return (
        f'<p class="post-pair">Also in {label}: '
        f'<a href="/volunteer/posts/{other["slug"]}/" hreflang="{other["lang"]}">{cta}</a></p>'
    )


def render_siblings(post, posts) -> str:
    same = [p for p in posts if p["lang"] == post["lang"]]
    try:
        i = same.index(post)
    except ValueError:
        return ""

    newer = same[i - 1] if i > 0 else None          # list is newest-first
    older = same[i + 1] if i + 1 < len(same) else None
    if not newer and not older:
        return ""

    def cell(p, direction, cls):
        if not p:
            return f'<span class="post-sibling {cls} post-sibling--empty"></span>'
        return (
            f'<a class="post-sibling {cls}" href="/volunteer/posts/{p["slug"]}/">'
            f'<span class="dir">{direction}</span>'
            f'<span class="t">{esc(clip(p["title"], 70))}</span></a>'
        )

    return (
        '<nav class="post-siblings" aria-label="More reports">'
        + cell(older, "← Older", "post-sibling--prev")
        + cell(newer, "Newer →", "post-sibling--next")
        + "</nav>"
    )


# ---------------------------------------------------------------------------
# rewriting
# ---------------------------------------------------------------------------

MARKER = "<!-- BUILD:{k} -->"
END = "<!-- /BUILD:{k} -->"


def strip_region(src: str, key: str, keep_anchor: bool = False) -> str:
    """Remove a generated region.

    With keep_anchor the opening marker is left behind, so a later insert can
    find its place again — without it, a second run has nothing to anchor to
    and the region silently disappears.
    """
    if keep_anchor:
        pattern = re.escape(MARKER.format(k=key)) + r".*?" + re.escape(END.format(k=key))
        return re.sub(pattern, MARKER.format(k=key), src, flags=re.S)

    # swallow the whitespace the region was inserted with, or every run leaves
    # another blank line behind and the build stops being idempotent
    pattern = r"[ \t]*\n?[ \t]*" + re.escape(MARKER.format(k=key)) + r".*?" + re.escape(END.format(k=key))
    return re.sub(pattern, "", src, flags=re.S)


def wrap_region(key: str, body: str) -> str:
    return f"{MARKER.format(k=key)}{body}{END.format(k=key)}"


def extra_head_for(rel: str, src: str) -> str:
    """Keep the per-page extras that are not part of the shared chrome."""
    out = ""
    if "fundraiser-widget.css" in src or "fundraiser-widget.js" in src:
        out += (
            '\n<link rel="stylesheet" href="/assets/css/fundraiser-widget.css" />'
            '\n<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>'
            '\n<script src="https://cdnjs.cloudflare.com/ajax/libs/easy-pie-chart/2.1.6/jquery.easypiechart.min.js"></script>'
            '\n<script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>'
            '\n<script src="https://unpkg.com/dayjs@1.8.21/dayjs.min.js"></script>'
            '\n<script defer src="/assets/js/fundraiser-widget.js"></script>'
        )
    if rel == "volunteer/index.html":
        out += '\n<script defer src="/assets/js/volunteer.js"></script>'
    return out


def process(path: Path, posts, by_slug) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    src = original = path.read_text(encoding="utf-8")

    lang = "en"
    m = re.search(r'<html lang="([a-z]{2})"', src)
    if m:
        lang = m.group(1)

    if rel in PAGES:
        cfg = PAGES[rel]
        title, desc, url = cfg["title"], cfg["desc"], cfg["url"]
        hero = cfg.get("hero")
        image = f"/assets/images/{hero}.jpg" if hero else "/assets/images/hero-home.jpg"
        og_type = "website"
        noindex = cfg.get("noindex", False)
    elif rel.startswith("volunteer/posts/"):
        slug = path.parent.name
        post = by_slug.get(slug)
        if post is None:
            print(f"  ! no JSON entry for {slug} — skipped")
            return False
        title = post["title"]
        desc = clip(clean_excerpt(post.get("excerpt", "")))
        url = f"/volunteer/posts/{slug}/"
        hero = None
        image = post.get("cover") or "/assets/images/hero-volunteer.jpg"
        og_type = "article"
        noindex = False
    else:
        print(f"  ? unknown page {rel} — skipped")
        return False

    # ---- head -------------------------------------------------------------
    head = build_head(
        title=title, desc=desc, url=url, image=image, lang=lang,
        extra_head=extra_head_for(rel, src), hero=hero, og_type=og_type, noindex=noindex,
    )
    src = re.sub(r"<head>.*?</head>", lambda _: head, src, count=1, flags=re.S)

    # ---- chrome -----------------------------------------------------------
    src = re.sub(
        r'(?:<a class="skip-link".*?</a>\s*)?<header class="site-header">.*?</header>',
        lambda _: build_header(url if rel in PAGES else "/volunteer/"),
        src, count=1, flags=re.S,
    )
    src = re.sub(
        r'<footer class="site-footer">.*?</footer>',
        lambda _: build_footer(),
        src, count=1, flags=re.S,
    )
    src = re.sub(r"<main[^>]*>", '<main id="main">', src, count=1)

    # a page-level script tag that used to sit after the footer is now in <head>
    src = re.sub(r'\s*<script defer src="/assets/js/(?:main|volunteer)\.js"></script>(?=\s*(?:</body>|<script>))', "", src)

    # ---- volunteer index --------------------------------------------------
    if rel == "volunteer/index.html":
        src = strip_region(src, "posts", keep_anchor=True)
        listing = wrap_region("posts", "\n" + render_volunteer_list(posts) + "\n")
        src, n = re.subn(
            r'<div id="posts" class="post-grid"[^>]*></div>|' + re.escape(MARKER.format(k="posts")),
            lambda _: listing,
            src, count=1,
        )
        if n != 1:
            raise SystemExit(
                "volunteer/index.html: no anchor for the post list — expected either "
                '<div id="posts" class="post-grid"></div> or a <!-- BUILD:posts --> marker'
            )

    # ---- post pages -------------------------------------------------------
    if rel.startswith("volunteer/posts/"):
        post = by_slug[path.parent.name]

        src = strip_region(src, "pair")
        src = strip_region(src, "siblings")
        src = picturize(src)

        src = src.replace(
            '<p><a class="btn alt" href="/volunteer/">&larr; Back to all posts</a></p>',
            '<p class="post-nav-top"><a class="btn alt" href="/volunteer/">&larr; All reports</a></p>',
        )

        pair = render_pair(post, by_slug)
        if pair:
            src = re.sub(
                r'(<p class="post-nav-top">.*?</p>)',
                lambda mo: mo.group(1) + "\n      " + wrap_region("pair", pair),
                src, count=1, flags=re.S,
            )

        sib = render_siblings(post, posts)
        if sib:
            src = src.replace(
                "</article>",
                "  " + wrap_region("siblings", sib) + "\n    </article>",
                1,
            )

    if src != original:
        path.write_text(src, encoding="utf-8")
        return True
    return False


# ---------------------------------------------------------------------------
# sitemap / robots
# ---------------------------------------------------------------------------

def write_sitemap(posts):
    urls = []
    for rel, cfg in PAGES.items():
        if cfg.get("priority") is None:
            continue
        urls.append((SITE + cfg["url"], None, cfg["priority"]))
    for p in posts:
        urls.append((SITE + f"/volunteer/posts/{p['slug']}/", p["dateISO"], "0.6"))

    body = "\n".join(
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        + (f"    <lastmod>{lastmod}</lastmod>\n" if lastmod else "")
        + f"    <priority>{prio}</priority>\n"
        "  </url>"
        for loc, lastmod, prio in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n",
        encoding="utf-8",
    )

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n" f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    print(f"  sitemap.xml  {len(urls)} urls")
    print("  robots.txt")


# ---------------------------------------------------------------------------

def main():
    posts = load_posts()
    by_slug = {p["slug"]: p for p in posts}

    POSTS_JSON.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    pages = sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("*/index.html")) \
        + sorted(ROOT.glob("volunteer/posts/*/index.html"))

    changed = 0
    for path in pages:
        if process(path, posts, by_slug):
            changed += 1

    paired = sum(1 for p in posts if p.get("pair"))
    print(f"  {changed} of {len(pages)} pages rewritten")
    print(f"  {len(posts)} posts, {paired} cross-linked EN/UA")
    write_sitemap(posts)


if __name__ == "__main__":
    main()
