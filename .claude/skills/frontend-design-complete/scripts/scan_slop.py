#!/usr/bin/env python3
"""Scan a frontend codebase for AI-generated design signals ("AI slop").

Usage: python scan_slop.py <path> [--max-hits N]

Outputs a hex-color census and tiered signature hits with file:line evidence,
plus a co-occurrence score. Interpret results with references/design-audit.md —
in particular, run the intentionality test before trusting the score.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

EXTENSIONS = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".jsx",
              ".tsx", ".vue", ".svelte", ".js", ".ts", ".astro", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "vendor",
             "coverage", "__pycache__"}

# (tier, name, compiled regex)
SIGNATURES = [
    (1, "Purple/indigo gradient",
     re.compile(r"linear-gradient[^;\"']*(purple|violet|indigo|#[78][0-9a-f]{2}[0-9a-f]{3})|"
                r"(from|via|to)-(purple|indigo|violet)-\d+", re.I)),
    (1, "Generic display font (Inter/Roboto/Poppins/Space Grotesk...)",
     re.compile(r"(font-family[^;}]*|fonts\.googleapis[^\"']*)"
                r"(inter|roboto|poppins|dm\+?\s?sans|plus\+?\s?jakarta|manrope|space\+?\s?grotesk)", re.I)),
    (1, "Sparkle/rocket/robot emoji branding",
     re.compile(r"[✨\U0001F680\U0001F916]")),
    (2, "Pill border-radius (9999px/999px/50rem)",
     re.compile(r"border-radius:\s*(9999px|999px|50rem|100px)|rounded-full", re.I)),
    (2, "Uniform generous radius 12-24px / rounded-xl+",
     re.compile(r"border-radius:\s*(1[2-9]|2[0-4])px|rounded-(xl|2xl|3xl)", re.I)),
    (2, "transition: all",
     re.compile(r"transition:\s*all|transition-all", re.I)),
    (2, "Hover lift (translateY negative on hover)",
     re.compile(r"translateY\(-\d|hover:-translate-y", re.I)),
    (2, "Left-border accent stripe",
     re.compile(r"border-left:\s*[3-6]px\s+solid", re.I)),
    (2, "Gradient text (background-clip: text)",
     re.compile(r"background-clip:\s*text|text-fill-color|bg-clip-text", re.I)),
    (2, "Interchangeable startup copy",
     re.compile(r"supercharge|seamless|unlock (your|their)|everything you need to"
                r"|all[- ]in[- ]one platform|transform your (workflow|business)", re.I)),
    (2, "Emoji used as feature icon",
     re.compile(r"class=[\"'][^\"']*icon[^\"']*[\"'][^<]*[\U0001F300-\U0001FAFF☀-➿]"
                r"|[\U0001F4C8\U0001F4CA⚡\U0001F91D\U0001F680\U0001F512\U0001F3AF]")),
    (3, "Raw Tailwind default blue (#3b82f6 family)",
     re.compile(r"#3b82f6|#2563eb|#60a5fa|(bg|text|border)-blue-[456]00", re.I)),
    (3, "Fixed px font sizes, no clamp()",
     re.compile(r"font-size:\s*\d+px", re.I)),
]

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def norm_hex(h):
    h = h.lower()
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h


def rgb(h):
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def classify_hex(h):
    """Tier-1 palette families detectable only from color values."""
    r, g, b = rgb(h)
    if r >= 0xF6 and r >= g >= b and (r - b) >= 4 and (r - b) <= 24:
        return (1, "Cream/warm off-white background family")
    if 0xA0 <= r <= 0xE8 and 0.38 <= (g / max(r, 1)) <= 0.65 and b < g:
        return (1, "Terracotta/coral/rust accent family")
    return None


def iter_files(root):
    root = Path(root)
    if root.is_file():
        yield root
        return
    for p in sorted(root.rglob("*")):
        # Only skip directories *below* the scan root — the root itself may
        # legitimately live inside a dist/ or build/ folder.
        rel_parts = p.relative_to(root).parts[:-1]
        if p.is_file() and p.suffix in EXTENSIONS \
                and not any(part in SKIP_DIRS for part in rel_parts):
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--max-hits", type=int, default=5,
                    help="max example locations shown per signal")
    args = ap.parse_args()

    hits = {}          # name -> (tier, [locations])
    hex_census = Counter()
    hex_where = {}

    files = list(iter_files(args.path))
    if not files:
        sys.exit(f"No frontend source files found under {args.path}")

    for f in files:
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        rel = str(f)
        for i, line in enumerate(text.splitlines(), 1):
            for tier, name, rx in SIGNATURES:
                if rx.search(line):
                    hits.setdefault(name, (tier, []))[1].append(f"{rel}:{i}")
            for m in HEX_RE.findall(line):
                h = norm_hex(m)
                hex_census[h] += 1
                hex_where.setdefault(h, f"{rel}:{i}")

    # Fold hex-family findings into hits
    for h, count in hex_census.items():
        fam = classify_hex(h)
        if fam:
            tier, name = fam
            hits.setdefault(name, (tier, []))[1].append(
                f"{h} x{count} (first at {hex_where[h]})")

    score = sum({1: 3, 2: 2, 3: 1}[tier] for tier, _ in hits.values())
    verdict = "Low" if score <= 3 else "Medium" if score <= 8 else "High"

    print(f"# Slop scan: {args.path}  ({len(files)} files)\n")
    print("## Signature hits\n")
    if not hits:
        print("None found.\n")
    for name, (tier, locs) in sorted(hits.items(), key=lambda kv: kv[1][0]):
        shown = ", ".join(locs[:args.max_hits])
        more = f" (+{len(locs) - args.max_hits} more)" if len(locs) > args.max_hits else ""
        print(f"- [Tier {tier}] {name}: {shown}{more}")

    print("\n## Hex color census (top 15)\n")
    for h, count in hex_census.most_common(15):
        print(f"- {h} x{count}")

    print(f"\n## Raw score: {score}  ->  verdict: {verdict}")
    print("\nCAUTION: apply the intentionality test in references/design-audit.md "
          "before reporting this verdict — committed aesthetics legitimately use "
          "some of these ingredients.")


if __name__ == "__main__":
    main()
