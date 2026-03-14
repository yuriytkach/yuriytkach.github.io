#!/usr/bin/env python3
"""Add favicon and logo to all volunteer post pages."""

import os
import re

POSTS_DIR = "volunteer/posts"

for slug in os.listdir(POSTS_DIR):
    filepath = os.path.join(POSTS_DIR, slug, "index.html")
    if not os.path.exists(filepath):
        continue
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Add favicon after charset meta
    if "favicon.ico" not in content:
        content = content.replace(
            '<meta charset="UTF-8" />',
            '<meta charset="UTF-8" />\n<link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico" />',
        )

    # Replace text brand with logo image
    content = content.replace(
        '<a class="brand" href="/">Yuriy Tkach</a>',
        '<a class="brand logo-brand" href="/"><img src="/assets/images/logo-software-developer.png" alt="Yuriy Tkach" class="site-logo" /></a>',
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {slug}")
