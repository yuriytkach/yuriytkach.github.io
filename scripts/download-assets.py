#!/usr/bin/env python3
"""Download all remote assets from Squarespace CDN and save locally."""

import os
import urllib.request
import urllib.error

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Map: local filename -> URL
ASSETS = {
    # Site-wide
    "logo-software-developer.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439499651288-H5KQTH5NN6TJ106SI6YS/Software+Developer-logo-white.png",
    "favicon.ico": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439587110096-J5MYHJ6UQZJVT77YUJ37/favicon.ico",
    "hero-banner.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439064376139-5FRGEAIJ4VVYXDBK78GL/P1000424.JPG",
    # Resume - company logos
    "resume-sigmaledger.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1560553990178-JL6OL65DAHEMKGJG9VXY/SigmaLedger_final_250.png",
    "resume-schibsted.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1505395137433-AW62HTXA8UKIOF48HIUP/logo.jpg",
    "resume-epam.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1505393190673-D2B16FJTH4CM9DE53P5H/epam.png",
    "resume-epam-teamlead-2014.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439155100600-WABAPQE5A0HHTB2TNDXJ/image-asset.png",
    "resume-epam-lead-2012.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439155049809-KSQC9LXU8N0GV8DOBG7L/image-asset.png",
    "resume-epam-senior-2009.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439311877726-TRECHZ8O2ZLX16DRRVRC/image-asset.png",
    "resume-chernihiv-uni.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439311912839-JSP9L97QZ9NKI1835OK3/image-asset.png",
    "resume-smartymedia-dev.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439312027112-F4YTA8MWENNIWK4DXJB9/image-asset.png",
    "resume-smartymedia-arch.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439312091683-ND3KTD9PFV3RQ4LH82J8/image-asset.png",
    "resume-litera.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439312197935-9LN9EZMLZ5R3ES5MFWYU/image-asset.png",
    "resume-chernihiv-edu.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439157284736-NYVDGL22M8VA17K1ARED/image-asset.png",
}


def download_file(url, dest_path):
    """Download a file from URL to dest_path."""
    if os.path.exists(dest_path):
        print(f"  SKIP (exists): {os.path.basename(dest_path)}")
        return True
    print(f"  DOWNLOADING: {os.path.basename(dest_path)}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; site-clone/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        with open(dest_path, "wb") as f:
            f.write(data)
        print(f"    -> {len(data)} bytes saved")
        return True
    except urllib.error.HTTPError as e:
        print(f"    ERROR HTTP {e.code}: {url}")
        return False
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def download_post_images_from_file(urls_file):
    """Download all post inline images."""
    posts_img_dir = os.path.join(ASSETS_DIR, "posts")
    os.makedirs(posts_img_dir, exist_ok=True)
    with open(urls_file) as f:
        urls = [line.strip() for line in f if line.strip().startswith("http")]
    success = 0
    fail = 0
    for url in urls:
        # Derive filename from URL path segment
        path_part = url.split("/")[-1].split("?")[0]
        dest = os.path.join(posts_img_dir, path_part)
        ok = download_file(url, dest)
        if ok:
            success += 1
        else:
            fail += 1
    print(f"Post images: {success} downloaded/skipped, {fail} failed")


def main():
    success = 0
    fail = 0
    for filename, url in ASSETS.items():
        dest = os.path.join(ASSETS_DIR, filename)
        ok = download_file(url, dest)
        if ok:
            success += 1
        else:
            fail += 1
    print(f"\nDone: {success} downloaded/skipped, {fail} failed")


if __name__ == "__main__":
    main()
