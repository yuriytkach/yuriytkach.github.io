# Secondary Hero Styling Design

**Goal:** Give `404.html` and all volunteer post pages their own secondary hero treatments so they no longer inherit the generic fallback hero.

## Approach

Use a shared volunteer-family visual language with two explicit variants:
- `hero-banner--post` for volunteer post pages
- `hero-banner--404` for `404.html`

This keeps both page types visually related to the volunteer section while making them distinct from each other and from the five main page heroes.

## Structure

### Volunteer posts
- Update generated volunteer post markup from bare `hero-banner` to `hero-banner hero-banner--post`
- Keep existing hero content structure (`hero-kicker`, `hero-title`, `hero-subtitle`)
- Preserve no-parallax behavior on post pages

### 404 page
- Update `404.html` hero wrapper from bare `hero-banner` to `hero-banner hero-banner--404`
- Keep the existing 404 copy and redirect logic unchanged
- Use a calmer, darker overlay so it feels related to the volunteer family without reading like a fundraiser page

## Styling

Add CSS variants in `assets/css/styles.css`:
- `hero-banner--post` uses the secondary volunteer-family image treatment and a readability-first overlay for long titles and dates
- `hero-banner--404` uses the same family base with a quieter overlay and crop

The generic `.hero-banner` fallback remains available for resilience, but these secondary pages should stop relying on it.

## Source of truth

Volunteer posts are generated content, so the durable fix is in `scripts/rewrite-posts.py`, not manual edits alone. The script should emit the post-specific hero class so future rewrites preserve the new styling.

## Testing

Verify:
- `404.html` contains `hero-banner--404`
- all files in `volunteer/posts/*/index.html` contain `hero-banner--post`
- `scripts/rewrite-posts.py` emits `hero-banner--post`
- main-page hero variants remain unchanged
- a fresh audit no longer reports generic fallback leakage on `404.html` or volunteer posts

## Non-goals

- No redesign of hero copy
- No parallax on secondary pages
- No changes to post content extraction or 404 redirect logic
