# tools

Two scripts. No dependencies beyond Python 3 and Pillow (`pip install Pillow`).

## `build.py`

Owns the parts of every page that are the same on every page, so a nav or design
change is one edit instead of seventy:

- `<head>` — fonts, description, canonical, Open Graph / Twitter cards, the
  no-flash theme bootstrap, hero preload
- `<header>` and `<footer>`
- the volunteering index — post grid grouped by year, rendered into the HTML so
  it works without JavaScript and search engines can read it
- post pages — English/Ukrainian pair link, previous/next navigation, and
  `<picture>` wrappers so photos are served as WebP
- `sitemap.xml` and `robots.txt`

```bash
python3 tools/build.py
```

Run it after editing `data/volunteer-posts.json`, adding a post, or changing
anything in the nav. It is idempotent — running it twice changes nothing.

Everything inside `<main>` on the hand-written pages (home, experience, stats,
contact, calendar, 404) is yours; the script never touches it. Generated regions
inside a page are fenced with `<!-- BUILD:name -->` markers — leave those in
place, they are how the script finds its way back.

Per-page titles and descriptions for the hand-written pages live in the `PAGES`
dict at the top of the script.

## `optimize_images.py`

Resizes images to the sizes the site actually displays, writes WebP siblings for
everything under `assets/images/posts/`, and builds 640px cover thumbnails in
`assets/images/covers/` for the volunteering index.

```bash
python3 tools/optimize_images.py --dry-run   # report only
python3 tools/optimize_images.py             # rewrite in place
```

It edits files in place. Originals are in git, so `git checkout -- assets/images`
undoes a run. Run it after adding new photos, then run `build.py` so the new
WebP files get referenced.
