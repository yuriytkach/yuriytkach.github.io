#!/usr/bin/env python3
"""Update volunteer-posts.json cover URLs to local paths."""

import json
import os

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "volunteer-posts.json"
)


def sqs_url_to_local(url):
    """Convert Squarespace CDN URL to local /assets/images/posts/filename."""
    if url.startswith("/assets/"):
        return url  # Already local
    filename = url.split("/")[-1].split("?")[0]
    return f"/assets/images/posts/{filename}"


with open(DATA_FILE, encoding="utf-8") as f:
    posts = json.load(f)

updated = 0
for post in posts:
    old = post.get("cover", "")
    if old and "squarespace-cdn" in old:
        post["cover"] = sqs_url_to_local(old)
        updated += 1

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"Updated {updated} cover URLs")
