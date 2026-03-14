# Website Faithful Reproduction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the GitHub Pages static clone of yuriytkach.com into a faithful reproduction of the original Squarespace site by downloading all assets locally, restoring missing content, and fixing broken volunteer post pages.

**Architecture:** Pure static HTML/CSS/JS site on GitHub Pages. No build tooling. Images stored under `assets/images/`. Volunteer posts are standalone HTML files. A Python download script fetches all remote assets. All pages share the same header/footer HTML structure.

**Tech Stack:** HTML5, CSS3 (existing styles.css), vanilla JS, Python 3 (for download scripts only - not deployed), GitHub Pages hosting.

---

## Overview of Changes

1. **Task 1** - Download all remote images/assets (script)
2. **Task 2** - Add favicon and header logo image
3. **Task 3** - Add hero banner photo to all pages
4. **Task 4** - Restore full resume page content + company logos
5. **Task 5** - Rewrite volunteer post pages (remove Squarespace boilerplate, fix image refs, fix cross-links)
6. **Task 6** - Update volunteer-posts.json to use local image paths
7. **Task 7** - Fix calendar page description text
8. **Task 8** - Fix contact page description text
9. **Task 9** - Final assessment by fresh subagent

---

## Key URLs and Image Paths on Original Site

### Site-wide assets (Squarespace CDN)
- **Site logo:** `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439499651288-H5KQTH5NN6TJ106SI6YS/Software+Developer-logo-white.png`
- **Favicon:** `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439587110096-J5MYHJ6UQZJVT77YUJ37/favicon.ico`
- **Homepage banner photo:** `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439064376139-5FRGEAIJ4VVYXDBK78GL/P1000424.JPG`

### Resume page company logos
- SigmaLedger: `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1560553990178-JL6OL65DAHEMKGJG9VXY/SigmaLedger_final_250.png`
- Schibsted: `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1505395137433-AW62HTXA8UKIOF48HIUP/logo.jpg`
- EPAM (team lead Dec 2016): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1505393190673-D2B16FJTH4CM9DE53P5H/epam.png`
- EPAM (team lead Sep 2014): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439155100600-WABAPQE5A0HHTB2TNDXJ/image-asset.png`
- EPAM (lead engineer Nov 2012): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439155049809-KSQC9LXU8N0GV8DOBG7L/image-asset.png`
- EPAM (senior engineer Nov 2009): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439311877726-TRECHZ8O2ZLX16DRRVRC/image-asset.png`
- Chernihiv University (lecturer): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439311912839-JSP9L97QZ9NKI1835OK3/image-asset.png`
- Smartymedia (developer): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439312027112-F4YTA8MWENNIWK4DXJB9/image-asset.png`
- Smartymedia (consultant): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439312091683-ND3KTD9PFV3RQ4LH82J8/image-asset.png`
- Litera Corp: `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439312197935-9LN9EZMLZ5R3ES5MFWYU/image-asset.png`
- University (education): `https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439157284736-NYVDGL22M8VA17K1ARED/image-asset.png`

---

## Task 1: Download All Remote Assets

**Files:**
- Create: `scripts/download-assets.py`
- Create: `assets/images/` directory (empty - will be populated by script)
- Modify: `scripts/` dir (create it)

This script downloads all images referenced across the site and saves them locally with predictable filenames.

**Step 1: Create the download script**

Create `scripts/download-assets.py`:

```python
#!/usr/bin/env python3
"""Download all remote assets from Squarespace CDN and save locally."""
import os
import urllib.request
import urllib.error
import hashlib

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
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

# Volunteer post images - derived from volunteer-posts.json and post HTML files
# These are the cover images referenced in volunteer-posts.json
VOLUNTEER_COVER_IMAGES = {
    "vol-laser-rangefinder-report.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1729789831837-AXCRKVMVX8YPYOW727SL/soldier_with_vortex.jpg",
    "vol-laser-rangefinder-ua.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1727542113417-6XKGPYUPKTUOCV55NPFR/telemetro-fundraiser.png",
    "vol-uav-fundraiser.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1707592698089-0ZU7T5BMPUYS0LSO5HO0/drone-huge-fundraiser.png",
    "vol-night-vision-report.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1719741334443-V1694I5Z1BCTQMKIESDY/soldier.jpg",
    "vol-night-vision-fundraiser.png": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1714561461883-5EIKBEHHHSS0H4YE9RVU/-fundraiser-nx-olx-round.png",
    "vol-endoprosthesis-report.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1712505597778-LI1WR3FQVN2K5SEL42VC/done.jpg",
    "vol-truck-report-cover.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1707585680667-01GUZ0QOEY5JVOBFJQ6K/car.jpg",
    "vol-fpv-report2.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1704695421026-G5DUE2S92JMLV38KZY3D/20240107_112222.jpg",
    "vol-fpv-report1.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1704696209506-QRKQED72A95TBYJZ3SJ9/20240107_112823.jpg",
    "vol-everyday-needs2.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1697629299744-FFRMYNSQCOW16JMKKV4G/pulsar-accessories.jpg",
    "vol-aug-sep-fundraisers.jpg": "https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1695826863179-K7JKRFMSD7SPA694ZUL8/all-cars.jpg",
}

def download_file(url, dest_path):
    """Download a file from URL to dest_path."""
    if os.path.exists(dest_path):
        print(f"  SKIP (exists): {os.path.basename(dest_path)}")
        return True
    print(f"  DOWNLOADING: {os.path.basename(dest_path)}")
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; site-clone/1.0)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        with open(dest_path, 'wb') as f:
            f.write(data)
        print(f"    -> {len(data)} bytes saved")
        return True
    except urllib.error.HTTPError as e:
        print(f"    ERROR HTTP {e.code}: {url}")
        return False
    except Exception as e:
        print(f"    ERROR: {e}")
        return False

def main():
    all_assets = {**ASSETS, **VOLUNTEER_COVER_IMAGES}
    success = 0
    fail = 0
    for filename, url in all_assets.items():
        dest = os.path.join(ASSETS_DIR, filename)
        ok = download_file(url, dest)
        if ok:
            success += 1
        else:
            fail += 1
    print(f"\nDone: {success} downloaded/skipped, {fail} failed")

if __name__ == '__main__':
    main()
```

**Step 2: Also scan all volunteer post HTML files for image URLs**

The script above handles cover images. We also need inline images in each post. Create a second script `scripts/scan-post-images.py` to scan all post HTML files and extract Squarespace CDN image URLs:

```python
#!/usr/bin/env python3
"""Scan volunteer post HTML files for squarespace image URLs and print them."""
import os
import re

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'volunteer', 'posts')
PATTERN = re.compile(r'https://images\.squarespace-cdn\.com/[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|ico|webp)', re.IGNORECASE)

found = set()
for slug in os.listdir(POSTS_DIR):
    post_file = os.path.join(POSTS_DIR, slug, 'index.html')
    if not os.path.exists(post_file):
        continue
    with open(post_file) as f:
        content = f.read()
    urls = PATTERN.findall(content)
    for url in urls:
        found.add(url)

for url in sorted(found):
    print(url)
print(f"\nTotal unique image URLs: {len(found)}")
```

**Step 3: Run the scan script to get all post image URLs**

```bash
python3 scripts/scan-post-images.py > /tmp/post-images.txt
cat /tmp/post-images.txt | head -30
```

Expected: A list of ~200+ Squarespace CDN image URLs found across 63 post files.

**Step 4: Extend download script to handle all post images**

After reviewing `/tmp/post-images.txt`, add a `download_post_images` function to `scripts/download-assets.py` that:
1. Reads URLs from stdin or a file
2. Derives a local filename: take the last path segment before `?` (e.g., `soldier_with_vortex.jpg`)
3. Saves to `assets/images/posts/`

Add this to `download-assets.py`:

```python
def download_post_images_from_file(urls_file):
    """Download all post inline images."""
    posts_img_dir = os.path.join(ASSETS_DIR, 'posts')
    os.makedirs(posts_img_dir, exist_ok=True)
    with open(urls_file) as f:
        urls = [line.strip() for line in f if line.strip().startswith('http')]
    for url in urls:
        # Derive filename from URL path segment
        path_part = url.split('/')[-1].split('?')[0]
        # Strip squarespace ID prefix (format: ID-HASH/filename.ext)
        if '/' in path_part:
            path_part = path_part.split('/')[-1]
        dest = os.path.join(posts_img_dir, path_part)
        download_file(url, dest)
```

**Step 5: Run the full download**

```bash
python3 scripts/download-assets.py
python3 scripts/scan-post-images.py > /tmp/post-images.txt
# Then manually add the post images download call or run a one-liner:
python3 -c "
import sys; sys.path.insert(0, 'scripts')
exec(open('scripts/download-assets.py').read())
download_post_images_from_file('/tmp/post-images.txt')
"
```

Expected output: All images downloaded to `assets/images/` and `assets/images/posts/`.

**Step 6: Verify downloads**

```bash
ls assets/images/ | wc -l
ls assets/images/posts/ | wc -l
```

Expected: At least 20 files in `assets/images/`, and 150+ files in `assets/images/posts/`.

**Step 7: Commit**

```bash
git add scripts/ assets/images/
git commit -m "feat: add asset download scripts and download all remote images locally"
```

---

## Task 2: Add Favicon and Header Logo

**Files:**
- Modify: `index.html`
- Modify: `resume/index.html`
- Modify: `volunteer/index.html`
- Modify: `calendar/index.html`
- Modify: `contact/index.html`
- Modify: `assets/css/styles.css`

The favicon is at `assets/images/favicon.ico` (downloaded in Task 1).
The logo PNG is at `assets/images/logo-software-developer.png`.

The original site uses the logo image as the header brand link instead of text. It's a white PNG on a dark/transparent header.

**Step 1: Add favicon to all HTML `<head>` sections**

In every HTML file (all pages + all 63 volunteer post files), add within `<head>`:
```html
<link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico" />
```

Use a script to do this in bulk:

```bash
# Add favicon line after <meta charset> line in all HTML files
find . -name "index.html" -not -path "./.git/*" | while read f; do
  if ! grep -q "favicon.ico" "$f"; then
    sed -i 's|<meta charset="UTF-8" />|<meta charset="UTF-8" />\n<link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico" />|' "$f"
    echo "Updated: $f"
  fi
done
```

**Step 2: Replace text brand with logo image in all HTML files**

The current header has:
```html
<a class="brand" href="/">Yuriy Tkach</a>
```

Replace with logo image in all pages:
```html
<a class="brand logo-brand" href="/"><img src="/assets/images/logo-software-developer.png" alt="Yuriy Tkach" class="site-logo" /></a>
```

Use sed or a Python script to do this in bulk across all HTML files.

**Step 3: Add logo CSS to styles.css**

Add to `assets/css/styles.css`:
```css
.site-logo { height: 48px; width: auto; display: block; }
.logo-brand { display: flex; align-items: center; }
```

Note: The logo is white (`Software+Developer-logo-white.png`). The header background is light (`#f8f8f5`). We need to check if logo is visible. If it's a white-on-transparent PNG, it won't show on light background. In that case, add a CSS filter or use the logo differently:

```css
/* If logo is white-on-transparent, invert to show on light header */
.site-logo { height: 48px; width: auto; filter: invert(1) brightness(0.3); }
```

Or alternatively, just check what the logo looks like (it's labeled "Software Developer logo white") - if it's white text on transparent, apply `filter: invert(0.8) hue-rotate(180deg)` or similar to make it visible on light background. Test visually.

**Step 4: Commit**

```bash
git add -A
git commit -m "feat: add favicon and site logo to header across all pages"
```

---

## Task 3: Add Hero Banner Photo to Pages

**Files:**
- Modify: `index.html`
- Modify: `volunteer/index.html`
- Modify: `resume/index.html`
- Modify: `calendar/index.html`
- Modify: `contact/index.html`
- Modify: All `volunteer/posts/*/index.html` (63 files)
- Modify: `assets/css/styles.css`

The original site has a full-width banner image at the top of every page with the page title and tagline overlaid.

**Step 1: Add hero-banner CSS to styles.css**

Add to `assets/css/styles.css`:
```css
.hero-banner {
  position: relative;
  width: 100%;
  min-height: 320px;
  background: url('/assets/images/hero-banner.jpg') center/cover no-repeat;
  display: flex;
  align-items: flex-end;
}
.hero-banner::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 100%);
}
.hero-banner .hero-banner-content {
  position: relative;
  z-index: 1;
  color: #fff;
  padding: 2rem;
  width: 100%;
}
.hero-banner .hero-banner-content h1,
.hero-banner .hero-banner-content p {
  color: #fff;
  margin: 0;
}
.hero-banner .hero-banner-content p {
  font-size: 1.1rem;
  margin-top: 0.3rem;
  opacity: 0.9;
}
```

**Step 2: Update index.html homepage**

Replace the existing `<section class="hero wrap">` with a two-part structure:
- A full-width hero banner with background photo
- Keep the existing "brief about me" content section below

On the homepage, the original shows the banner photo with "Systems Architect / Team Lead" and "Yuriy Tkach" overlaid. Replace:

```html
<!-- BEFORE (existing hero): -->
<section class="hero wrap">
  <p class="kicker">Systems Architect / Team Lead</p>
  <h1>Yuriy Tkach</h1>
  ...
</section>

<!-- AFTER: -->
<div class="hero-banner">
  <div class="hero-banner-content wrap">
    <p style="font-size:0.9rem;text-transform:uppercase;letter-spacing:0.1em;opacity:0.85;margin-bottom:0.4rem;">Systems Architect / Team Lead</p>
    <h1 style="font-size:clamp(2rem,5vw,3.5rem);font-weight:700;">Yuriy Tkach</h1>
  </div>
</div>
<section class="section wrap" style="padding-top:2rem;">
  <p class="lead">I build robust backend systems, design scalable architecture, and support teams through pragmatic engineering leadership across Java, Scala, and cloud-native stacks.</p>
  <p>
    <a class="btn" href="/resume/">View resume</a>
    <a class="btn alt" href="/volunteer/">See volunteering work</a>
  </p>
</section>
```

**Step 3: Update other pages (resume, volunteer, calendar, contact)**

Each page gets the hero banner at top with the page title. For example, on resume page:

```html
<div class="hero-banner">
  <div class="hero-banner-content wrap">
    <p style="font-size:0.9rem;text-transform:uppercase;letter-spacing:0.1em;opacity:0.85;margin-bottom:0.4rem;">Resume</p>
    <h1 style="font-size:clamp(2rem,5vw,3.5rem);font-weight:700;">Professional Profile</h1>
  </div>
</div>
```

Replace the `<section class="hero wrap">` block with the hero-banner div + move the lead text to the first content section.

**Step 4: Update volunteer index page**

```html
<div class="hero-banner">
  <div class="hero-banner-content wrap">
    <p style="...">Volunteering initiative</p>
    <h1 style="...">Direct Help for Ukraine</h1>
    <p>Fundraisers and reports supporting Ukrainian Armed Forces.</p>
  </div>
</div>
```

**Step 5: Update all volunteer post pages with a narrower hero banner**

Each post page should show the post hero image (first image from the post) or fall back to the site-wide banner. For now, use the site-wide banner. Update each post's current `<section class="hero wrap">` to use the hero banner with the post title.

Since there are 63 post files, use a Python script for bulk replacement.

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: add hero banner photo to all pages"
```

---

## Task 4: Restore Full Resume Page

**Files:**
- Modify: `resume/index.html`

The current resume has 6 compressed job entries. The original has 10 detailed entries with full descriptions, bullet points, YouTube links, and company logos. See `Key URLs` section above for logo image paths (already downloaded in Task 1).

**Step 1: Rewrite resume/index.html with full content**

The full resume structure (from original site, faithfully reproduced):

```html
<!-- After hero-banner section, the experience section: -->
<section class="section wrap resume-block">
  <h2>Experience</h2>
  <div class="timeline">

    <article>
      <div class="timeline-logo">
        <a href="http://sigmaledger.com" target="_blank" rel="noopener">
          <img src="/assets/images/resume-sigmaledger.png" alt="SigmaLedger" />
        </a>
      </div>
      <time>February 2019 - present</time>
      <h3>Software Architect — SigmaLedger, Inc., Kyiv, Ukraine</h3>
      <p>Building next-generation blockchain-based platform for combating counterfeit.</p>
      <p><strong>Technologies:</strong> Java, Ethereum Blockchain, Solidity, Spring Boot, Quarkus, Kafka, Elasticsearch, Redis, PostgreSQL, Vault, Kubernetes, Docker, AWS, Lambda</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://www.schibsted.com/" target="_blank" rel="noopener">
          <img src="/assets/images/resume-schibsted.jpg" alt="Schibsted" />
        </a>
      </div>
      <time>May 2017 - January 2019</time>
      <h3>Backend Software Engineer — Schibsted Media Group, Barcelona, Spain</h3>
      <p>As a member of the Engineering Productivity team creating tools and services that empower engineers across the whole organization to be more productive in developing apps/services in different languages for different platforms, ensuring high code quality with continuous delivery.</p>
      <p>The services include gathering and processing different reports from dev repositories, calculating various metrics, providing quality gate checks. Additionally, services include automatic processing and actioning on different events, and provide tools to improve testing, building and releasing of software.</p>
      <p><strong>Technologies:</strong> Java, Scala, Spring Boot, Kafka, Elasticsearch, Docker, github-api, REST, microservices, Gatling</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://epam.com" target="_blank" rel="noopener">
          <img src="/assets/images/resume-epam.png" alt="EPAM Systems" />
        </a>
      </div>
      <time>December 2016 - May 2017 (6 months)</time>
      <h3>Team Lead — EPAM Systems, Kyiv, Ukraine</h3>
      <p>Took active part in the start, design, analysis and initial development of the consumer information project for CoreLogic. The project is a complete rewrite from the ground of the legacy application, with the adopting of Pivotal Cloud technologies. Took part in analyzing different technologies, architecture design, closely working with business analysts and project managers. Programmed parts of the new system paying great attention to testing, performance, reliability. Lead a small team of highly professional developers working in SCRUM.</p>
      <p><strong>Technologies:</strong> Spring Framework, Spring Boot, Pivotal Cloud Foundry, Hibernate, REST, Oracle, microservices</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://epam.com" target="_blank" rel="noopener">
          <img src="/assets/images/resume-epam-teamlead-2014.png" alt="EPAM Systems" />
        </a>
      </div>
      <time>September 2014 - December 2016 (2 years)</time>
      <h3>Software Engineering Team Lead — EPAM Systems, Kyiv, Ukraine</h3>
      <p>Continue to lead a small group of developers in building applications for international investment bank, perform managerial tasks as well as hands-on programming tasks. Main accomplishments:</p>
      <ul>
        <li>Organized software development process to ensure stable delivery of high quality products</li>
        <li>Setup continuous integration, enforced auto testing</li>
        <li>Prepared pre-release documentation, development documentation, user guides</li>
        <li>Interviewed and hired candidates for the team</li>
        <li>Mentored junior developers</li>
        <li>Worked with team members to ensure their professional growth and satisfaction</li>
        <li>Initiated and negotiated several rounds of refactoring and improving of applications</li>
        <li>Performed requirements analysis and tasks break down</li>
        <li>Continued to successfully implement development tasks within required scope</li>
      </ul>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://epam.com" target="_blank" rel="noopener">
          <img src="/assets/images/resume-epam-lead-2012.png" alt="EPAM Systems" />
        </a>
      </div>
      <time>November 2012 - September 2014 (2 years)</time>
      <h3>Lead Software Engineer — EPAM Systems, Kyiv, Ukraine</h3>
      <p>Leading a small group of developers in building applications for international investment bank. Creating front-office Foreign Exchange applications that integrate with different internal and external APIs using FIX-protocol and JMS. Applications are built on Spring and Apache Camel with heavy use of multithreading.</p>
      <ul>
        <li>Perform requirements analysis having close communication with customer and create program architecture</li>
        <li>Distribute development tasks and monitor their activity, review and verify colleagues' code</li>
        <li>Investigate the use of new technologies and create prototypes</li>
        <li>Develop different application modules, write unit and regression tests</li>
        <li>Collaborate with other teams to ensure stable and correct work of integrated systems</li>
        <li>Take on responsibility to deliver application on time, properly tested and documented</li>
      </ul>
      <p>Prepared, conducted and produced <a href="https://www.youtube.com/user/ytkach/playlists?shelf_id=1&view=50&sort=dd" target="_blank" rel="noopener">Advanced Java learning course</a> for junior developers.</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://epam.com" target="_blank" rel="noopener">
          <img src="/assets/images/resume-epam-senior-2009.png" alt="EPAM Systems" />
        </a>
      </div>
      <time>November 2009 - November 2012 (3 years)</time>
      <h3>Senior Software Engineer — EPAM Systems, Kyiv, Ukraine</h3>
      <p>Working on several projects for international investment bank. Implemented business functionality related to FX trading. Designed and implemented components of multithreaded systems that work with large data expecting high load. Created pure server-side as well as client side components. Refactored and reimplemented legacy code, wrote integration with 3rd party systems.</p>
      <p>Prepared, conducted and produced Java for Testers learning courses: <a href="https://www.youtube.com/playlist?list=PLB0276A0A62BDEF06" target="_blank" rel="noopener">Videos of lectures</a> and <a href="https://www.youtube.com/playlist?list=PLD964614607573AFD" target="_blank" rel="noopener">videos of practice</a>.</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://stu.cn.ua" target="_blank" rel="noopener">
          <img src="/assets/images/resume-chernihiv-uni.png" alt="Chernihiv State Technological University" />
        </a>
      </div>
      <time>September 2007 - November 2009 (2 years)</time>
      <h3>Lecturer — Chernihiv State Technological University, Ukraine</h3>
      <p>Lectured advanced course of program system design and architecture, where modern approaches to developing corporate systems using Java language are taught. Introduced to students various design patterns, layered architecture, technologies including Spring, JPA, JSF, AOP, application testing and building using JUnit and Ant.</p>
      <p>Recorded some lectures in Java technologies: <a href="https://www.youtube.com/playlist?list=PLCA5CB42F5A816A17" target="_blank" rel="noopener">Videos of lectures</a>.</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://smartymedia.biz" target="_blank" rel="noopener">
          <img src="/assets/images/resume-smartymedia-dev.png" alt="Smartymedia.biz" />
        </a>
      </div>
      <time>September 2008 - June 2009 (1 year)</time>
      <h3>Senior Java Developer — Smartymedia.biz, Chernihiv, Ukraine</h3>
      <p>Implemented various portlets for the web-portal including tv-schedule, online-tv, horoscope, weather, advertisement. Wrote separate modules for rss processing and cache-management. Refactored and fixed code for the core of the web-portal, wrote missing junit tests. Wrote ant scripts for building portal modules and deploying to the server.</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://smartymedia.biz" target="_blank" rel="noopener">
          <img src="/assets/images/resume-smartymedia-arch.png" alt="Smartymedia.biz" />
        </a>
      </div>
      <time>June 2006 - September 2008 (2 years)</time>
      <h3>Architecture Designer and Consultant — Smartymedia.biz, Chernihiv, Ukraine</h3>
      <p>Assisted in designing of general architecture of the web-portal. Designed the architecture of the separate portal portlet. Wrote generic classes and facades for database access, portlet configuration, etc.</p>
    </article>

    <article>
      <div class="timeline-logo">
        <a href="http://litera.com" target="_blank" rel="noopener">
          <img src="/assets/images/resume-litera.png" alt="Litera Corp." />
        </a>
      </div>
      <time>September 2006 - August 2008 (2 years)</time>
      <h3>Software Engineer — Litera Corp., Chernihiv, Ukraine</h3>
      <p>Refactored, redesigned and remade the application for comparing Excel documents. Increased comparing speed and accuracy dramatically. Added many new features including support for Office 2007 formats, export in different formats, launching from Excel toolbar, connecting to document management systems. Re-designed the program architecture to modular one.</p>
      <p>Implemented patent-pending technology for comparing embedded Excel sheets in Word documents. Wrote a separate DLL module providing a general interface for working with various document-management-systems (Interwoven, Netdocs, DocsOpen, Dm51 and others).</p>
    </article>

  </div>
</section>

<section class="section wrap resume-block">
  <h2>Education</h2>
  <article class="card">
    <div class="timeline-logo">
      <a href="http://stu.cn.ua" target="_blank" rel="noopener">
        <img src="/assets/images/resume-chernihiv-edu.png" alt="Chernihiv State Technological University" />
      </a>
    </div>
    <h3>MS Computer Science</h3>
    <p>Chernihiv State Technological University (September 2001 - February 2007)</p>
    <p>Studied courses covering algorithms, design patterns, specific technologies (COM, RMI, J2EE), application security, discrete mathematics, electrical engineering. GPA – 5.0 (highest in Ukraine). Diploma with excellence award.</p>
  </article>
</section>

<section class="section wrap resume-block">
  <h2>Skills</h2>
  <div class="grid cards-3">
    <article class="card">
      <h3>Languages</h3>
      <ul>
        <li>Java</li><li>Scala</li><li>JavaScript</li><li>Python</li><li>Bash</li>
      </ul>
    </article>
    <article class="card">
      <h3>Frameworks</h3>
      <ul>
        <li>Spring</li><li>Quarkus</li><li>Apache Kafka</li><li>Apache Camel</li>
        <li>Hibernate</li><li>Web3j</li><li>JMS</li>
      </ul>
    </article>
    <article class="card">
      <h3>Technologies & Platforms</h3>
      <ul>
        <li>Ethereum Blockchain</li><li>FX Trading</li><li>Kubernetes</li>
        <li>Docker</li><li>AWS</li><li>PCF</li><li>Azure</li>
        <li>OOP/OOD</li><li>Design Patterns</li><li>SCRUM</li>
      </ul>
    </article>
    <article class="card">
      <h3>Tools</h3>
      <ul>
        <li>JIRA</li><li>Jenkins</li><li>Travis</li>
        <li>Gradle, Maven, Ant</li><li>Git, SVN</li>
        <li>Linux</li><li>Windows</li>
      </ul>
    </article>
  </div>
</section>
```

**Step 2: Add timeline-logo CSS to styles.css**

```css
.timeline article { display: grid; grid-template-columns: 64px 1fr; gap: 0.5rem 1rem; border-left: none; padding-left: 0; }
.timeline-logo { grid-column: 1; grid-row: 1 / span 10; }
.timeline-logo img { width: 56px; height: auto; border-radius: 6px; }
.timeline time { grid-column: 2; }
.timeline h3 { grid-column: 2; }
.timeline p, .timeline ul { grid-column: 2; }
.cards-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
@media (max-width: 900px) { .cards-3 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .cards-3 { grid-template-columns: 1fr; } }
```

**Step 3: Commit**

```bash
git add resume/index.html assets/css/styles.css
git commit -m "feat: restore full resume page with company logos and complete job history"
```

---

## Task 5: Rewrite Volunteer Post Pages

**Files:**
- Modify: All 63 `volunteer/posts/*/index.html` files

**Problem with current state:**
1. Post HTML files contain raw Squarespace boilerplate (sqs-block, sqs-gallery, summary-v2-block, etc.)
2. Images use `data-src` with Squarespace lazy-load - won't work without Squarespace JS
3. The "REPORTS FOR PREVIOUS FUNDRAISERS AND PURCHASES" carousel at the bottom of each post uses Squarespace gallery carousel - broken
4. Cross-links between posts use original Squarespace paths which work (they map to `/volunteer/posts/SLUG/`) but some may be missing

**Approach:**
Write a Python script `scripts/rewrite-posts.py` that:
1. Parses each post's current HTML
2. Extracts: title, date, text content (from `sqs-html-content` divs), images (from `data-src` attributes and `<noscript>` img tags)
3. Rewrites as clean HTML with:
   - Proper shared header/footer
   - Hero banner
   - Text content (preserving links)
   - Images as a CSS grid gallery using locally stored images
   - A "Related Reports" section with hardcoded links (from the data in volunteer-posts.json)
   - Back button to `/volunteer/`

**Step 1: Write the rewrite script**

Create `scripts/rewrite-posts.py`:

```python
#!/usr/bin/env python3
"""Rewrite volunteer post HTML files to remove Squarespace boilerplate."""
import os
import re
import json
from html.parser import HTMLParser

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'volunteer', 'posts')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
IMAGES_DIR = '/assets/images/posts'

# Load posts JSON for cross-reference links
with open(os.path.join(DATA_DIR, 'volunteer-posts.json')) as f:
    ALL_POSTS = json.load(f)

def squarespace_url_to_local(url):
    """Convert a Squarespace CDN URL to a local assets path."""
    # Extract filename from URL: last path segment before ?
    filename = url.split('/')[-1].split('?')[0]
    return f"{IMAGES_DIR}/{filename}"

def fix_volunteer_links(html):
    """Fix internal volunteer links: /volunteer/SLUG -> /volunteer/posts/SLUG/"""
    # Fix links that go to /volunteer/SLUG (old squarespace paths)
    # These should become /volunteer/posts/SLUG/ if that post exists
    slugs = {p['slug'] for p in ALL_POSTS}
    def replace_link(m):
        href = m.group(1)
        # Extract slug from href like /volunteer/slug-name
        parts = href.strip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'volunteer':
            slug = parts[1]
            if slug in slugs:
                return f'href="/volunteer/posts/{slug}/"'
        return m.group(0)
    return re.sub(r'href="(/volunteer/[^"]+)"', replace_link, html)

def extract_content_from_sqs(html):
    """Extract text content and images from Squarespace HTML."""
    # Extract text from sqs-html-content divs
    text_blocks = re.findall(
        r'<div class="sqs-html-content"[^>]*>(.*?)</div>\s*(?:</div>\s*)*(?=<div class="sqs(?:-block|s-html)|</article>)',
        html, re.DOTALL
    )
    
    # Extract images: from data-src attributes or noscript img tags
    # Priority: noscript img src (actual URLs) over data-src
    images = []
    
    # From noscript tags
    noscript_imgs = re.findall(r'<noscript><img src="(https://images\.squarespace-cdn\.com[^"]+)"[^>]*alt="([^"]*)"', html)
    for url, alt in noscript_imgs:
        if 'squarespace-cdn' in url:
            images.append({'url': url, 'alt': alt, 'local': squarespace_url_to_local(url)})
    
    # Also from data-src (dedup)
    datasrc_imgs = re.findall(r'data-src="(https://images\.squarespace-cdn\.com[^"]+)"[^>]*alt="([^"]*)"', html)
    seen_filenames = {img['local'].split('/')[-1] for img in images}
    for url, alt in datasrc_imgs:
        local = squarespace_url_to_local(url)
        fname = local.split('/')[-1]
        if fname not in seen_filenames:
            images.append({'url': url, 'alt': alt, 'local': local})
            seen_filenames.add(fname)
    
    return text_blocks, images

def make_html_page(slug, title, date_human, date_iso, text_blocks, images, lang='en'):
    """Generate clean HTML for a volunteer post."""
    
    # Build image gallery section
    gallery_html = ''
    if images:
        img_items = '\n'.join(
            f'    <figure class="post-gallery-item">'
            f'<img src="{img["local"]}" alt="{img["alt"]}" loading="lazy" onerror="this.style.display=\'none\'">'
            f'{"<figcaption>" + img["alt"] + "</figcaption>" if img["alt"] and img["alt"] != img["local"].split("/")[-1] else ""}'
            f'</figure>'
            for img in images
        )
        gallery_html = f'<div class="post-gallery">\n{img_items}\n</div>'
    
    # Build text content
    content_html = '\n'.join(text_blocks) if text_blocks else '<p>See original post for content.</p>'
    content_html = fix_volunteer_links(content_html)
    
    # Replace squarespace image URLs in text content too
    def replace_img_url(m):
        url = m.group(1)
        local = squarespace_url_to_local(url)
        return f'src="{local}"'
    content_html = re.sub(r'src="(https://images\.squarespace-cdn\.com[^"]+)"', replace_img_url, content_html)
    
    html_lang = 'uk' if lang == 'uk' else 'en'
    
    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
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
    <p style="font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;opacity:0.85;margin-bottom:0.3rem;">Volunteering post</p>
    <h1 style="font-size:clamp(1.5rem,4vw,2.8rem);font-weight:700;">{title}</h1>
    <p style="opacity:0.85;margin-top:0.3rem;"><time datetime="{date_iso}">{date_human}</time></p>
  </div>
</div>
<article class="post-content">
  <p><a class="btn alt" href="/volunteer/">&larr; Back to all posts</a></p>
  {content_html}
  {gallery_html}
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

def process_post(slug, post_meta):
    post_file = os.path.join(POSTS_DIR, slug, 'index.html')
    if not os.path.exists(post_file):
        print(f"  SKIP (no file): {slug}")
        return
    
    with open(post_file, encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already rewritten (no squarespace classes)
    if 'sqs-block' not in html and 'sqs-html-content' not in html:
        print(f"  SKIP (already clean): {slug}")
        return
    
    title = post_meta.get('title', slug)
    date_human = post_meta.get('dateHuman', '')
    date_iso = post_meta.get('dateISO', '')
    
    # Detect language (Ukrainian posts have Cyrillic in title)
    lang = 'uk' if re.search(r'[а-яА-ЯіїєІЇЄ]', title) else 'en'
    
    text_blocks, images = extract_content_from_sqs(html)
    
    new_html = make_html_page(slug, title, date_human, date_iso, text_blocks, images, lang)
    
    with open(post_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"  REWROTE: {slug} ({len(images)} images, {len(text_blocks)} text blocks)")

def main():
    # Build slug->meta map
    meta_map = {p['slug']: p for p in ALL_POSTS}
    
    processed = 0
    for slug in sorted(os.listdir(POSTS_DIR)):
        if os.path.isdir(os.path.join(POSTS_DIR, slug)):
            meta = meta_map.get(slug, {'slug': slug, 'title': slug, 'dateHuman': '', 'dateISO': ''})
            process_post(slug, meta)
            processed += 1
    
    print(f"\nProcessed {processed} posts")

if __name__ == '__main__':
    main()
```

**Step 2: Add post gallery CSS to styles.css**

```css
.post-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.75rem;
  margin: 1.5rem 0;
}
.post-gallery-item {
  margin: 0;
  border-radius: 10px;
  overflow: hidden;
  background: var(--surface);
  border: 1px solid var(--line);
}
.post-gallery-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}
.post-gallery-item figcaption {
  padding: 0.4rem 0.6rem;
  font-size: 0.82rem;
  color: var(--muted);
}
```

**Step 3: Run the rewrite script**

```bash
python3 scripts/rewrite-posts.py
```

Expected output: `REWROTE: <slug> (N images, M text blocks)` for each of 63 posts.

**Step 4: Manually review 3-4 posts**

Open the following post files and verify they look correct:
- `volunteer/posts/fundraiser-uav/index.html` - English fundraiser post
- `volunteer/posts/fundraiser-laser-rangerinder-ua/index.html` - Ukrainian post
- `volunteer/posts/report-fundraiser-laser-rangefinder/index.html` - Report post
- `volunteer/posts/2022-03-27-fund-raise-to-help-ukrainian-soldiers/index.html` - Early post

Check that:
1. No `sqs-block` classes remain
2. Images use local `/assets/images/posts/filename` paths
3. Cross-links to other posts use `/volunteer/posts/SLUG/` format
4. Text content is readable

**Step 5: Commit**

```bash
git add volunteer/posts/
git commit -m "feat: rewrite volunteer post pages removing Squarespace boilerplate, fix image refs and cross-links"
```

---

## Task 6: Update volunteer-posts.json with Local Image Paths

**Files:**
- Modify: `data/volunteer-posts.json`

The `cover` field in each post entry currently points to Squarespace CDN. These should point to local images.

**Step 1: Write update script**

Create `scripts/update-posts-json.py`:

```python
#!/usr/bin/env python3
"""Update volunteer-posts.json to use local image paths."""
import json
import os
import re

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'volunteer-posts.json')

def squarespace_url_to_local(url):
    filename = url.split('/')[-1].split('?')[0]
    return f"/assets/images/posts/{filename}"

with open(DATA_FILE) as f:
    posts = json.load(f)

for post in posts:
    if post.get('cover') and 'squarespace-cdn' in post['cover']:
        post['cover'] = squarespace_url_to_local(post['cover'])

with open(DATA_FILE, 'w') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print(f"Updated {len(posts)} posts in volunteer-posts.json")
```

**Step 2: Run the update script**

```bash
python3 scripts/update-posts-json.py
```

Expected: `Updated 63 posts in volunteer-posts.json`

**Step 3: Verify the JSON**

Check that cover paths now look like `/assets/images/posts/filename.jpg` and no longer reference squarespace-cdn.com.

**Step 4: Commit**

```bash
git add data/volunteer-posts.json
git commit -m "fix: update volunteer-posts.json cover images to use local paths"
```

---

## Task 7: Fix Calendar and Contact Pages

**Files:**
- Modify: `calendar/index.html`
- Modify: `contact/index.html`

**Calendar page:**
The original calendar page has different text. The current clone says "Free and busy information for daytime slots. If a time works for you, reach out on the contact page." The original says "Free and busy information of my daytime" with a personal note: "I can be busy, I can be free, and even when I am free I might still be busy :) In any case, below you can see my public calendar, so if you want to chat just pick a time and contact me."

The Google Calendar iframe embed also needs a `wkst=2` (week starts Monday) and `showNav=1&showDate=1&showPrint=0&showTabs=1&showCalendars=0&showTz=0` parameters to match the original settings.

Update `calendar/index.html`:
- Replace hero text with original wording  
- Update iframe `src` to: `https://calendar.google.com/calendar/embed?src=yuriytkach%40gmail.com&ctz=Europe%2FKyiv&wkst=2&showNav=1&showDate=1&showPrint=0&showTabs=1&showCalendars=0&showTz=0`

**Contact page:**
The original contact page has: "You can always reach me by e-mail me@yuriytkach.com or contact using the following form." (the form is Squarespace-specific, we can just keep the email/social links). The current clone already has a reasonable contact page.

Add the social media profiles to the contact page (Facebook, Buy Me A Coffee, YouTube, LinkedIn, GitHub).

**Step 1: Update calendar/index.html hero text and iframe**

**Step 2: Update contact/index.html to add more complete social links**

**Step 3: Commit**

```bash
git add calendar/index.html contact/index.html
git commit -m "fix: update calendar embed parameters and contact page text"
```

---

## Task 8: Final Cleanup and Cross-Check

**Files:**
- Review all pages for consistency

**Step 1: Check all pages have:**
- [ ] Favicon link in `<head>`
- [ ] Logo image in header (not text)
- [ ] Hero banner photo
- [ ] Correct nav links

**Step 2: Check volunteer posts:**

```bash
# Verify no Squarespace classes remain
grep -r "sqs-block\|squarespace-cdn" volunteer/posts/ | head -20
```

Expected: No results (or only in comments).

**Step 3: Check all images exist locally**

```bash
# Find any remaining squarespace CDN references
grep -r "squarespace-cdn" . --include="*.html" --include="*.json" | grep -v ".git"
```

Expected: No results.

**Step 4: Commit any remaining fixes**

```bash
git add -A
git commit -m "fix: final cleanup and consistency check across all pages"
```

---

## Task 9: Final Assessment by Fresh Subagent

**Purpose:** Have a fresh subagent (with no accumulated context) independently compare the GitHub Pages site against the original yuriytkach.com and produce an honest assessment.

The fresh subagent should:
1. Fetch the original site pages: `/`, `/resume`, `/volunteer`, `/calendar`, `/contact`
2. Read the corresponding pages in the repo
3. Check volunteer post pages (sample 5-10)
4. Produce a report covering:
   - What was successfully reproduced
   - What still differs or is missing
   - What improved vs original
   - What regressed or is worse
   - Any broken links or missing images detected
   - Overall quality assessment

**Prompt for the subagent:**

> "You are a web QA assessor. Your task is to compare a GitHub Pages static clone of a website against the original Squarespace site.
>
> Original site: https://www.yuriytkach.com (fetch each page)
> Clone repo: /home/yuriy/workspace/yuriytkach.github.io (read HTML files)
>
> Pages to compare: home (index.html), resume, volunteer, volunteer posts (sample 10), calendar, contact.
>
> For each page: compare structure, content completeness, images, links, and visual design intent.
> Report: what was done well, what is still missing or broken, what improved vs original, what regressed.
> Be honest and specific - cite exact filenames and line numbers where issues are found."

---

## Notes on Script Execution Order

Always run scripts in this order:
1. `scripts/download-assets.py` (download all images)
2. `scripts/scan-post-images.py` + extended download (post inline images)
3. HTML bulk edits (favicon, logo, hero banner)
4. `scripts/rewrite-posts.py` (rewrite post pages)
5. `scripts/update-posts-json.py` (fix JSON cover paths)

Each task should be committed separately for clean git history.
