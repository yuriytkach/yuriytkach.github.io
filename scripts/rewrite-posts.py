#!/usr/bin/env python3
"""Rewrite volunteer post HTML files to remove Squarespace boilerplate."""

import os
import re
import json

POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "volunteer", "posts")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
IMAGES_DIR = "/assets/images/posts"

# Load posts JSON for metadata and cross-reference
with open(os.path.join(DATA_DIR, "volunteer-posts.json")) as f:
    ALL_POSTS = json.load(f)


def sqs_url_to_local(url):
    """Convert a Squarespace CDN URL to a local path."""
    filename = url.split("/")[-1].split("?")[0]
    return f"{IMAGES_DIR}/{filename}"


def fix_volunteer_links(html):
    """Fix /volunteer/SLUG links to /volunteer/posts/SLUG/"""
    slugs = {p["slug"] for p in ALL_POSTS}
    # Build bare-slug -> full-slug map for date-prefixed slugs (YYYY-M-D-REST)
    bare_to_slug = {}
    for p in ALL_POSTS:
        m = re.match(r"^\d{4}-\d{1,2}-\d{1,2}-(.+)$", p["slug"])
        if m:
            bare_to_slug[m.group(1)] = p["slug"]

    def replace_link(m):
        href = m.group(1)
        parts = href.strip("/").split("/")
        # Handle /volunteer/SLUG (2-segment)
        if len(parts) == 2 and parts[0] == "volunteer" and parts[1] in slugs:
            return f'href="/volunteer/posts/{parts[1]}/"'
        # Handle /volunteer/YYYY/M/D/SLUG (date-path)
        if len(parts) >= 4 and parts[0] == "volunteer":
            bare = parts[-1].rstrip("-")
            if bare in slugs:
                return f'href="/volunteer/posts/{bare}/"'
            if bare in bare_to_slug:
                return f'href="/volunteer/posts/{bare_to_slug[bare]}/"'
            # Prefix-match fallback (e.g. trailing-dash URLs with jdhz suffix stripped)
            candidates = [k for k in bare_to_slug if k.startswith(bare)]
            if len(candidates) == 1:
                return f'href="/volunteer/posts/{bare_to_slug[candidates[0]]}/"'
        return m.group(0)

    return re.sub(r'href="(/volunteer/[^/"#][^"]*)"', replace_link, html)


def strip_summary_blocks(html):
    """Remove Squarespace summary/collection blocks that embed other posts' content."""
    # Remove entire blocks with these classes
    for cls in [
        "sqs-block-summary-v2",
        "summary-block-wrapper",
        "sqs-block-collection",
    ]:
        # Find and remove div blocks containing these classes
        pattern = f'<div[^>]*class="[^"]*{cls}[^"]*"'
        pos = 0
        while True:
            m = re.search(pattern, html[pos:])
            if not m:
                break
            start = pos + m.start()
            # Find matching closing </div>
            tag_end = html.find(">", start)
            if tag_end == -1:
                break
            depth = 1
            search = tag_end + 1
            while depth > 0 and search < len(html):
                o = html.find("<div", search)
                c = html.find("</div>", search)
                if c == -1:
                    break
                if o != -1 and o < c:
                    depth += 1
                    search = o + 4
                else:
                    depth -= 1
                    if depth == 0:
                        html = html[:start] + html[c + 6 :]
                        pos = start
                    search = c + 6
            else:
                pos = tag_end + 1
    return html


def extract_sqs_content(html):
    """Extract text blocks and images from Squarespace HTML."""
    html = strip_summary_blocks(html)
    # Extract ALL sqs-html-content div contents (using a simple iterative parser)
    text_blocks = []
    pos = 0
    while True:
        start = html.find('<div class="sqs-html-content"', pos)
        if start == -1:
            # Also try class with extra classes
            start = html.find('class="sqs-html-content ', pos)
            if start == -1:
                break
            # Find the opening tag start
            tag_start = html.rfind("<div", 0, start)
            start = tag_start
        else:
            tag_start = start

        # Find the matching closing </div> by counting depth
        tag_end = html.find(">", start)
        if tag_end == -1:
            break

        depth = 1
        search_pos = tag_end + 1
        content_start = tag_end + 1
        while depth > 0 and search_pos < len(html):
            open_tag = html.find("<div", search_pos)
            close_tag = html.find("</div>", search_pos)
            if close_tag == -1:
                break
            if open_tag != -1 and open_tag < close_tag:
                depth += 1
                search_pos = open_tag + 4
            else:
                depth -= 1
                if depth == 0:
                    content = html[content_start:close_tag].strip()
                    if content and len(content) > 10:
                        text_blocks.append(content)
                search_pos = close_tag + 6

        pos = tag_end + 1

    # Extract images from noscript tags (highest quality, actual src)
    images = []
    seen = set()

    # noscript images
    for url, alt in re.findall(
        r'<noscript[^>]*><img[^>]*src="(https://images\.squarespace-cdn\.com[^"]+)"[^>]*alt="([^"]*)"',
        html,
        re.DOTALL,
    ):
        fname = url.split("/")[-1].split("?")[0]
        if fname not in seen:
            images.append({"url": url, "alt": alt, "local": sqs_url_to_local(url)})
            seen.add(fname)

    # data-src images (fallback if not already found)
    for url, alt in re.findall(
        r'data-src="(https://images\.squarespace-cdn\.com[^"]+)"[^>]*alt="([^"]*)"',
        html,
        re.DOTALL,
    ):
        fname = url.split("/")[-1].split("?")[0]
        if fname not in seen:
            images.append({"url": url, "alt": alt, "local": sqs_url_to_local(url)})
            seen.add(fname)

    # Also try reversed attribute order
    for alt, url in re.findall(
        r'alt="([^"]*)"[^>]*data-src="(https://images\.squarespace-cdn\.com[^"]+)"',
        html,
        re.DOTALL,
    ):
        fname = url.split("/")[-1].split("?")[0]
        if fname not in seen:
            images.append({"url": url, "alt": alt, "local": sqs_url_to_local(url)})
            seen.add(fname)

    return text_blocks, images


def build_gallery(images):
    if not images:
        return ""
    items = []
    for img in images:
        alt = img["alt"]
        # Suppress captions that are filenames (e.g. photo.jpg) or paths
        is_filename = bool(re.search(r"\.\w{2,5}$", alt.strip())) if alt else False
        show_caption = alt and not alt.startswith("/assets") and not is_filename
        caption = f"<figcaption>{alt}</figcaption>" if show_caption else ""
        items.append(
            f'    <figure class="post-gallery-item"><img src="{img["local"]}" alt="{alt}" loading="lazy" onerror="this.parentElement.style.display=\'none\'">{caption}</figure>'
        )
    return '<div class="post-gallery">\n' + "\n".join(items) + "\n</div>"


def build_page(slug, title, date_human, date_iso, text_blocks, images):
    # Fix squarespace image references in text content
    content = (
        "\n".join(text_blocks)
        if text_blocks
        else "<p><em>Content not available in static format.</em></p>"
    )
    content = fix_volunteer_links(content)
    content = re.sub(
        r'src="(https://images\.squarespace-cdn\.com[^"]+)"',
        lambda m: f'src="{sqs_url_to_local(m.group(1))}"',
        content,
    )

    # Detect language from title
    lang = "uk" if re.search(r"[\u0400-\u04ff]", title) else "en"

    gallery = build_gallery(images)

    date_html = f'<time datetime="{date_iso}">{date_human}</time>' if date_human else ""

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Literata:opsz,wght@7..72,500;7..72,700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/css/styles.css" />
  <script defer src="/assets/js/main.js"></script>
  <title>{title} - Yuriy Tkach</title>
</head>
<body>
  <header class="site-header">
    <div class="wrap nav-row">
      <a class="brand logo-brand" href="/"><img src="/assets/images/logo-software-developer.png" alt="Yuriy Tkach" class="site-logo" /></a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">Menu</button>
      <nav id="main-nav" class="site-nav" aria-label="Main navigation">
        <a href="/">Home</a>
        <a href="/resume/">Resume</a>
        <a href="/volunteer/" aria-current="page">Volunteering</a>
        <a href="/calendar/">Calendar</a>
        <a href="/contact/">Contact</a>
      </nav>
    </div>
  </header>
  <main>
    <div class="hero-banner">
      <div class="hero-banner-content wrap">
        <p class="hero-kicker">Volunteering post</p>
        <h1 class="hero-title">{title}</h1>
        {f'<p class="hero-subtitle">{date_html}</p>' if date_html else ""}
      </div>
    </div>
    <article class="post-content">
      <p><a class="btn alt" href="/volunteer/">&larr; Back to all posts</a></p>
      {content}
      {gallery}
    </article>
  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <p class="footer-title">Kyiv, Ukraine</p>
        <a href="mailto:me@yuriytkach.com">me@yuriytkach.com</a>
      </div>
      <div class="footer-links">
        <a href="https://www.linkedin.com/in/yuriytkach" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://github.com/yuriytkach" target="_blank" rel="noopener">GitHub</a>
        <a href="https://www.youtube.com/channel/UCdXqgQdGW5go6nkkBbUVSMA" target="_blank" rel="noopener">YouTube</a>
        <a href="https://www.buymeacoffee.com/ytkach" target="_blank" rel="noopener">Buy Me a Coffee</a>
      </div>
    </div>
    <p class="copyright">&copy; <span id="year"></span> Yuriy Tkach</p>
  </footer>
</body>
</html>'''


def process_post(slug, meta):
    filepath = os.path.join(POSTS_DIR, slug, "index.html")
    if not os.path.exists(filepath):
        print(f"  SKIP (no file): {slug}")
        return 0

    with open(filepath, encoding="utf-8") as f:
        html = f.read()

    # Skip if already clean
    if "sqs-block" not in html and "sqs-html-content" not in html:
        print(f"  SKIP (clean): {slug}")
        return 0

    title = meta.get("title", slug)
    date_human = meta.get("dateHuman", "")
    date_iso = meta.get("dateISO", "")

    text_blocks, images = extract_sqs_content(html)
    new_html = build_page(slug, title, date_human, date_iso, text_blocks, images)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  REWROTE: {slug} ({len(text_blocks)} blocks, {len(images)} images)")
    return 1


def main():
    meta_map = {p["slug"]: p for p in ALL_POSTS}
    rewrote = 0
    for slug in sorted(os.listdir(POSTS_DIR)):
        if os.path.isdir(os.path.join(POSTS_DIR, slug)):
            meta = meta_map.get(
                slug,
                {
                    "slug": slug,
                    "title": slug.replace("-", " ").title(),
                    "dateHuman": "",
                    "dateISO": "",
                },
            )
            rewrote += process_post(slug, meta)
    print(f"\nTotal rewrote: {rewrote}")


if __name__ == "__main__":
    main()
