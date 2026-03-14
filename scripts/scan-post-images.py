#!/usr/bin/env python3
"""Scan volunteer post HTML files for squarespace image URLs and print them."""

import os
import re

POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "volunteer", "posts")
PATTERN = re.compile(
    r'https://images\.squarespace-cdn\.com/[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|ico|webp)',
    re.IGNORECASE,
)

found = set()
for slug in os.listdir(POSTS_DIR):
    post_file = os.path.join(POSTS_DIR, slug, "index.html")
    if not os.path.exists(post_file):
        continue
    with open(post_file) as f:
        content = f.read()
    urls = PATTERN.findall(content)
    for url in urls:
        found.add(url)

for url in sorted(found):
    print(url)
print(f"\nTotal unique image URLs: {len(found)}", flush=True)
