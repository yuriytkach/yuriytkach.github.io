#!/usr/bin/env python3
"""
Shrink the site's images to the sizes it actually displays them at.

The hero photographs were 2500–3400px wide originals — one of them 2.3 MB for a
background that is never rendered above 1800px, and the volunteering index alone
pulled 32 MB of cover photos. This resizes in place and, for the images used as
CSS backgrounds, also writes a WebP alongside so `image-set()` can prefer it.

Originals are in git, so `git checkout -- assets/images` undoes everything.

Usage:  python3 tools/optimize_images.py [--dry-run]
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "assets" / "images"

# Images used as CSS backgrounds — these get a WebP sibling for image-set().
BACKGROUNDS = {
    "hero-home", "hero-resume", "hero-volunteer",
    "hero-calendar", "hero-contact", "hero-stats",
    "home-card-resume", "home-card-youtube",
}

# max width, JPEG/WebP quality
RULES = [
    (IMAGES, 1800, 80),            # heroes and home cards
    (IMAGES / "posts", 1500, 82),  # covers, photos, receipts (kept legible when zoomed)
]

# Post photographs are served through <picture>, so every one gets a WebP.
# Many of them are photographs that were saved as PNG, where the saving is large.
POSTS = IMAGES / "posts"

# The volunteering index renders covers into a ~400px card; full-size photos
# there were the single heaviest thing on the site.
THUMBS = IMAGES / "covers"
THUMB_WIDTH = 640

# 2.3 MB fallback that every page overrides — nothing ever requests it.
DEAD = [IMAGES / "hero-banner.jpg"]

SKIP_SUFFIXES = {".svg", ".ico"}


def human(n: int) -> str:
    return f"{n / 1024 / 1024:.2f} MB" if n >= 1024 * 1024 else f"{n / 1024:.0f} KB"


def process(path: Path, max_w: int, quality: int, dry: bool) -> tuple[int, int]:
    before = path.stat().st_size
    try:
        im = Image.open(path)
    except Exception as exc:  # noqa: BLE001 — a bad file should not stop the run
        print(f"  ! {path.name}: {exc}")
        return before, before

    fmt = (im.format or "").upper()
    w, h = im.size
    resized = w > max_w
    if resized:
        im = im.resize((max_w, round(h * max_w / w)), Image.LANCZOS)

    stem = path.stem
    want_webp = stem in BACKGROUNDS or path.parent == POSTS
    webp_path = path.with_suffix(".webp")

    if dry:
        note = f"{w}x{h} -> {im.size[0]}x{im.size[1]}" if resized else f"{w}x{h} (kept)"
        print(f"  {path.name:52s} {human(before):>9s}  {note}")
        return before, before

    if fmt == "PNG":
        # Photographic PNGs (screenshots of receipts) are far smaller as JPEG,
        # but converting changes the filename the HTML references — so only
        # re-save, with optimisation, at the smaller size.
        im.save(path, "PNG", optimize=True)
    else:
        rgb = im.convert("RGB") if im.mode not in ("RGB", "L") else im
        rgb.save(path, "JPEG", quality=quality, optimize=True, progressive=True)

    if want_webp:
        im.convert("RGB").save(webp_path, "WEBP", quality=quality, method=6)

    after = path.stat().st_size
    if after > before:  # optimisation made it bigger — keep neither the loss nor the churn
        pass
    return before, after


def build_thumbnails(dry: bool) -> None:
    """640px WebP versions of the covers the volunteering index renders."""
    import json

    posts = json.loads((ROOT / "data" / "volunteer-posts.json").read_text(encoding="utf-8"))
    covers = {p["cover"] for p in posts if p.get("cover")}

    if not dry:
        THUMBS.mkdir(exist_ok=True)

    total = 0
    for cover in sorted(covers):
        src = ROOT / cover.lstrip("/")
        if not src.exists():
            print(f"  ! missing cover {cover}")
            continue
        out = THUMBS / (src.stem + ".webp")
        if dry:
            continue
        im = Image.open(src)
        w, h = im.size
        if w > THUMB_WIDTH:
            im = im.resize((THUMB_WIDTH, round(h * THUMB_WIDTH / w)), Image.LANCZOS)
        im.convert("RGB").save(out, "WEBP", quality=76, method=6)
        total += out.stat().st_size

    print(f"\n{THUMBS.relative_to(ROOT)}  {len(covers)} cover thumbnails, {human(total)} total")


def main() -> None:
    dry = "--dry-run" in sys.argv
    total_before = total_after = 0

    for base, max_w, quality in RULES:
        files = sorted(
            p for p in base.iterdir()
            if p.is_file() and p.suffix.lower() not in SKIP_SUFFIXES and p.suffix.lower() != ".webp"
        )
        print(f"\n{base.relative_to(ROOT)}  ({len(files)} files, max {max_w}px)")
        for path in files:
            if path in DEAD:
                continue
            b, a = process(path, max_w, quality, dry)
            total_before += b
            total_after += a

    if not dry:
        for path in DEAD:
            if path.exists():
                size = path.stat().st_size
                path.unlink()
                total_before += size
                print(f"\n  removed {path.name} ({human(size)}) — referenced only as an "
                      f"unused CSS fallback")

    build_thumbnails(dry)

    print(f"\nre-encoded originals: {human(total_before)} -> {human(total_after)} "
          f"({100 - total_after * 100 // max(total_before, 1)}% smaller)")
    webp = sum(p.stat().st_size for p in POSTS.glob("*.webp"))
    print(f"WebP siblings for post photos: {human(webp)} "
          f"(served in place of the originals wherever the browser supports it)")


if __name__ == "__main__":
    main()
