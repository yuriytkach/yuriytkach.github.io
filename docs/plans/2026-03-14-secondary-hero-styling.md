# Secondary Hero Styling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Give `404.html` and all volunteer post pages dedicated secondary hero variants so they no longer rely on the generic fallback hero treatment.

**Architecture:** Keep the existing shared `.hero-banner` system as the base, then add two explicit secondary variants in CSS: one for volunteer post pages and one for the 404 page. Make the volunteer post variant durable by updating `scripts/rewrite-posts.py` so regenerated posts keep the correct hero class automatically, then regenerate the post HTML and verify that fallback leakage is gone.

**Tech Stack:** Static HTML, CSS, Python 3 rewrite script, bash/grep verification

---

### Task 1: Add dedicated secondary hero CSS variants

**Files:**
- Modify: `assets/css/styles.css`

**Step 1: Write the failing verification command**

Run:
```bash
grep -n "hero-banner--post\|hero-banner--404" assets/css/styles.css
```

Expected: no matches yet.

**Step 2: Add minimal implementation**

Add two variant blocks near the existing hero modifiers:

```css
.hero-banner--post {
  --hero-image: url('/assets/images/hero-banner.jpg');
  --hero-position: center 44%;
  --hero-overlay: linear-gradient(180deg, rgba(8, 28, 46, 0.18) 0%, rgba(8, 28, 46, 0.78) 100%);
}

.hero-banner--404 {
  --hero-image: url('/assets/images/hero-banner.jpg');
  --hero-position: center 34%;
  --hero-overlay: linear-gradient(180deg, rgba(16, 24, 34, 0.16) 0%, rgba(16, 24, 34, 0.82) 100%);
}
```

Adjust positions/overlay values if needed, but keep both in the same volunteer-family look.

**Step 3: Run verification**

Run:
```bash
grep -n "hero-banner--post\|hero-banner--404" assets/css/styles.css
```

Expected: both variant selectors present.

**Step 4: Commit**

```bash
git add assets/css/styles.css
git commit -m "fix: add dedicated secondary hero variants"
```

### Task 2: Update the volunteer post generator and regenerate post pages

**Files:**
- Modify: `scripts/rewrite-posts.py`
- Modify: `volunteer/posts/*/index.html`

**Step 1: Write the failing verification command**

Run:
```bash
grep -n 'class="hero-banner hero-banner--post"' scripts/rewrite-posts.py && grep -r 'class="hero-banner hero-banner--post"' volunteer/posts --include="index.html" | wc -l
```

Expected: no script match yet, post count is `0`.

**Step 2: Add minimal implementation**

In the HTML template inside `build_page(...)`, change:

```html
<div class="hero-banner">
```

to:

```html
<div class="hero-banner hero-banner--post">
```

**Step 3: Regenerate posts**

Run:
```bash
python3 scripts/rewrite-posts.py
```

Expected: all 63 posts rewritten.

**Step 4: Run verification**

Run:
```bash
grep -n 'class="hero-banner hero-banner--post"' scripts/rewrite-posts.py && grep -r 'class="hero-banner hero-banner--post"' volunteer/posts --include="index.html" | wc -l
```

Expected: script template updated; post count `63`.

**Step 5: Commit**

```bash
git add scripts/rewrite-posts.py volunteer/posts
git commit -m "fix: give volunteer posts a dedicated hero variant"
```

### Task 3: Update 404 page to use the dedicated 404 hero variant

**Files:**
- Modify: `404.html`

**Step 1: Write the failing verification command**

Run:
```bash
grep -n 'class="hero-banner hero-banner--404"' 404.html
```

Expected: no matches yet.

**Step 2: Add minimal implementation**

Change:

```html
<div class="hero-banner">
```

to:

```html
<div class="hero-banner hero-banner--404">
```

**Step 3: Run verification**

Run:
```bash
grep -n 'class="hero-banner hero-banner--404"' 404.html
```

Expected: one match.

**Step 4: Commit**

```bash
git add 404.html
git commit -m "fix: give 404 page a dedicated hero variant"
```

### Task 4: End-to-end verification and fresh review

**Files:**
- Verify: `assets/css/styles.css`
- Verify: `scripts/rewrite-posts.py`
- Verify: `404.html`
- Verify: `volunteer/posts/*/index.html`

**Step 1: Run structural verification**

Run:
```bash
test "$(grep -r 'class="hero-banner hero-banner--post"' volunteer/posts --include="index.html" | wc -l)" -eq 63 && grep -q 'class="hero-banner hero-banner--404"' 404.html && grep -q 'hero-banner--post' scripts/rewrite-posts.py && grep -q 'hero-banner--post' assets/css/styles.css && grep -q 'hero-banner--404' assets/css/styles.css
```

Expected: exit code `0`.

**Step 2: Spot-check one post and the 404 page**

Run:
```bash
grep -n 'hero-banner' volunteer/posts/report-fundraiser-laser-rangefinder/index.html && grep -n 'hero-banner' 404.html
```

Expected: the post uses `hero-banner hero-banner--post`; `404.html` uses `hero-banner hero-banner--404`.

**Step 3: Run a fresh independent review**

Review against the current live site and confirm the previous low-severity note is resolved:
- `404.html` no longer uses bare `.hero-banner`
- volunteer posts no longer use bare `.hero-banner`
- main-page hero variants remain unchanged

**Step 4: Commit**

```bash
git add assets/css/styles.css scripts/rewrite-posts.py 404.html volunteer/posts
git commit -m "fix: stop secondary pages from using the generic hero fallback"
```
