# Site Fidelity Improvements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve the remaining fidelity gaps on the static site by upgrading hero treatment, restoring image-backed home cards, modernizing the contact page, and matching the original calendar embed behavior more closely.

**Architecture:** Keep the existing static HTML/CSS/JS structure and upgrade the shared visual system instead of introducing new frameworks. Implement page-specific hero variants through HTML classes/data attributes, add lightweight progressive-enhancement scroll behavior in JavaScript, and restore original visual assets locally so the site remains GitHub Pages-friendly.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, local image assets, Python/shell verification

---

### Task 1: Gather original assets and calendar/embed references

**Files:**
- Create: `assets/images/home-card-resume.jpg`
- Create: `assets/images/home-card-youtube.jpg`
- Create: `assets/images/contact-hero.jpg`
- Create: `assets/images/calendar-hero.jpg`
- Modify: `assets/images/` (download new files if source assets exist)

**Step 1: Inspect the original live pages for image/card/embed details**

Run:

```bash
python3 - <<'PY'
import urllib.request
for url in [
    'https://yuriytkach.com',
    'https://yuriytkach.com/contact',
    'https://yuriytkach.com/calendar',
]:
    print('\nURL:', url)
    html = urllib.request.urlopen(url).read().decode('utf-8', errors='ignore')
    print('hero refs:', html.count('images.squarespace-cdn.com'))
PY
```

Expected: live HTML fetched successfully.

**Step 2: Download the original card/hero imagery that will be reused**

Run:

```bash
python3 - <<'PY'
import os, urllib.request
targets = {
    'assets/images/home-card-resume.jpg': 'https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439146613484-YPEODE2SAEE3T7QQA4A6/image-asset.jpeg',
    'assets/images/home-card-youtube.jpg': 'https://images.squarespace-cdn.com/content/v1/55c36c6fe4b0e4120b157100/1439145564098-MDK6OTU14KBRA4S45QUB/image-asset.jpeg',
}
for path, url in targets.items():
    urllib.request.urlretrieve(url, path)
    print('downloaded', path)
PY
```

Expected: the two home card images exist locally.

**Step 3: Determine whether dedicated contact/calendar hero images exist**

Run a small fetch/inspection script or manual source inspection and either:
- download dedicated assets if clear originals exist, or
- document fallback to improved default hero asset.

Expected: exact hero asset decision recorded before editing HTML/CSS.

**Step 4: Verify files exist**

Run:

```bash
ls assets/images
```

Expected: newly downloaded files appear in the listing.

### Task 2: Upgrade shared hero CSS and add page-specific hero variants

**Files:**
- Modify: `assets/css/styles.css`
- Modify: `index.html`
- Modify: `resume/index.html`
- Modify: `volunteer/index.html`
- Modify: `calendar/index.html`
- Modify: `contact/index.html`

**Step 1: Add failing verification checklist**

Before editing, verify the current hero is too shallow and identical across pages by checking class usage.

Run:

```bash
python3 - <<'PY'
from pathlib import Path
for path in ['index.html','resume/index.html','volunteer/index.html','calendar/index.html','contact/index.html']:
    text = Path(path).read_text()
    print(path, 'hero-banner' in text, text.count('hero-banner'))
PY
```

Expected: all pages currently use the same hero structure.

**Step 2: Write minimal hero variant markup**

Update each main page hero wrapper to add a page-specific hook, for example:

```html
<div class="hero-banner hero-banner-home" data-parallax="hero">
```

Apply equivalent page-specific classes for resume, volunteer, calendar, and contact.

**Step 3: Replace the hero CSS with a taller, more spacious system**

Add CSS for:
- larger min-height (desktop and mobile)
- better `background-position`
- stronger but cleaner overlay
- optional inner layer or variable needed for parallax
- page-specific hero background images/classes

Example target rules:

```css
.hero-banner { min-height: 54vh; max-height: 760px; background-size: cover; background-position: center center; }
.hero-banner-home { background-image: ... }
.hero-banner-volunteer { background-image: ... }
```

**Step 4: Verify markup and CSS exist**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
css = Path('assets/css/styles.css').read_text()
for token in ['hero-banner-home','hero-banner-volunteer','hero-banner-contact','hero-banner-calendar']:
    print(token, token in css)
PY
```

Expected: all page-specific hero selectors present.

### Task 3: Add subtle parallax hero motion

**Files:**
- Modify: `assets/js/main.js`

**Step 1: Add failing verification checklist**

Read the current file and confirm there is no hero scroll behavior.

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('assets/js/main.js').read_text()
print('parallax' in text)
PY
```

Expected: `False`

**Step 2: Implement minimal progressive-enhancement parallax**

Add JS that:
- targets only main-page heroes marked with `data-parallax="hero"`
- updates a CSS custom property or transform on scroll
- bails out for `prefers-reduced-motion: reduce`
- avoids heavy work on mobile/narrow viewports

Pseudo-shape:

```javascript
const hero = document.querySelector('[data-parallax="hero"]')
if (hero && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // requestAnimationFrame scroll update
}
```

**Step 3: Verify code was added**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('assets/js/main.js').read_text()
for token in ['prefers-reduced-motion', 'data-parallax', 'requestAnimationFrame']:
    print(token, token in text)
PY
```

Expected: all tokens present.

### Task 4: Restructure the home page intro and restore image-backed cards

**Files:**
- Modify: `index.html`
- Modify: `assets/css/styles.css`

**Step 1: Remove the old CTA row and move the short professional sentence above the bio**

Change `index.html` so the short summary lead appears immediately after the hero and before `brief about(me)`. Remove:

```html
<p>
  <a class="btn" href="/resume/">View resume</a>
  <a class="btn alt" href="/volunteer/">See volunteering work</a>
</p>
```

**Step 2: Replace the plain cards with image-backed cards that keep text**

Use markup like:

```html
<a class="feature-card" href="/resume/">
  <img src="/assets/images/home-card-resume.jpg" alt="Resume preview" />
  <div class="feature-card-body">
    <h2>Professional experience</h2>
    <p>...</p>
  </div>
</a>
```

And a second card for YouTube.

**Step 3: Add CSS for the new feature cards**

Add selectors for `.feature-grid`, `.feature-card`, `.feature-card img`, `.feature-card-body`.

**Step 4: Verify button removal and new cards**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('index.html').read_text()
checks = ['View resume' not in text, 'See volunteering work' not in text, 'feature-card' in text, 'home-card-resume.jpg' in text, 'home-card-youtube.jpg' in text]
print(checks)
PY
```

Expected: all checks `True`.

### Task 5: Redesign the contact page to match the rest of the site

**Files:**
- Modify: `contact/index.html`
- Modify: `assets/css/styles.css`

**Step 1: Read original contact content and preserve the message**

The page should still communicate:
- email first
- alternate contact channels second

**Step 2: Replace the old section/card structure with the newer page rhythm**

Introduce a richer layout using the shared hero and a better section below it, for example:
- intro lead
- primary contact card
- secondary channels card/grid

**Step 3: Add any CSS needed for the updated contact layout**

Add reusable styles rather than inline styling where possible.

**Step 4: Verify the page uses the new structure**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('contact/index.html').read_text()
for token in ['hero-banner-contact', 'LinkedIn', 'GitHub', 'YouTube', 'Buy Me a Coffee']:
    print(token, token in text)
PY
```

Expected: all tokens present.

### Task 6: Correct the calendar embed default view and page presentation

**Files:**
- Modify: `calendar/index.html`

**Step 1: Inspect the original embed parameters**

Fetch or inspect the original calendar page source and compare the iframe URL.

**Step 2: Update the iframe query string**

Add or correct the parameter that controls the default view so it matches the original instead of defaulting to month. Keep the other validated parameters already copied.

**Step 3: Verify the iframe URL changed as intended**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('calendar/index.html').read_text()
print('mode=' in text or 'showTitle=' in text or 'mode=WEEK' in text)
PY
```

Expected: the relevant view-setting parameter is present.

### Task 7: Run end-to-end verification and independent review

**Files:**
- Review: `index.html`
- Review: `contact/index.html`
- Review: `calendar/index.html`
- Review: `assets/css/styles.css`
- Review: `assets/js/main.js`
- Review: `404.html`

**Step 1: Run local verification checks**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
checks = {
  'home hero class': 'hero-banner-home' in Path('index.html').read_text(),
  'contact hero class': 'hero-banner-contact' in Path('contact/index.html').read_text(),
  'calendar hero class': 'hero-banner-calendar' in Path('calendar/index.html').read_text(),
  '404 exists': Path('404.html').exists(),
  'no home CTA buttons': 'View resume' not in Path('index.html').read_text(),
}
print(checks)
PY
```

Expected: all checks `True`.

**Step 2: Run a fresh independent reviewer**

Have a clean subagent compare the updated files with the live site and explicitly verify:
- hero height/crop improved
- per-page hero differentiation present
- home page order and cards updated
- contact page no longer looks out of system
- calendar no longer defaults to month view if the original differs

**Step 3: Fix any real issues from the independent review**

Apply only targeted fixes.

**Step 4: Final verification**

Re-run the checklist from Step 1 and summarize results.
