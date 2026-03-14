#!/usr/bin/env python3
"""Download post images from a URL list file."""

import sys
import os
import urllib.request
import urllib.error

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "posts")
os.makedirs(ASSETS_DIR, exist_ok=True)


def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"  SKIP: {os.path.basename(dest_path)}")
        return True
    print(f"  DL: {os.path.basename(dest_path)}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; site-clone/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        print(f"    -> {len(data)} bytes")
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


urls_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/post-images.txt"
with open(urls_file) as f:
    urls = [line.strip() for line in f if line.strip().startswith("http")]

s, f = 0, 0
for url in urls:
    fname = url.split("/")[-1].split("?")[0]
    ok = download_file(url, os.path.join(ASSETS_DIR, fname))
    if ok:
        s += 1
    else:
        f += 1
print(f"\nDone: {s} ok, {f} failed")
