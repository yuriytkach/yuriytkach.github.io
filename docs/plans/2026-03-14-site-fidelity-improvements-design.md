# Site Fidelity Improvements Design

## Goal

Improve the remaining fidelity gaps between the GitHub Pages version of `yuriytkach.com` and the original Squarespace site without undoing the static-site migration. The work focuses on hero imagery and behavior, home page structure, contact page consistency, and calendar embed fidelity.

## Scope

- Make hero sections less cramped and closer to the original site.
- Use page-specific hero imagery where the original had distinct visual identity.
- Add subtle scroll motion to main-page heroes.
- Reorder and refine the home page intro content.
- Restore image-backed home cards for resume and YouTube while keeping text.
- Rebuild the contact page so it matches the rest of the site visually.
- Re-check and correct the Google Calendar iframe so it opens in the same default view as the original.
- Finish with a fresh independent verification pass and fix any gaps it finds.

## Design Decisions

### 1. Hero System

The current hero is too short and crops the image too aggressively. We will replace the single shallow hero treatment with a taller reusable hero pattern for main pages. The new hero will reveal more vertical image area, use a more controlled overlay, and support per-page background images.

Main pages will use page-specific background assets where the original site clearly used different imagery. The system will keep a safe fallback image for pages without a dedicated asset.

### 2. Hero Motion

Use subtle parallax, not a heavy fixed-background effect. The implementation should feel alive while remaining readable and stable across browsers. The motion will be lightweight, disabled or reduced on constrained/mobile contexts, and respect reduced-motion preferences.

### 3. Home Page Content Flow

The home page content order will become:

1. Hero
2. Short professional summary sentence
3. `brief about(me)` section with original text
4. Resume / YouTube image-backed cards with text

The two CTA buttons under the short summary will be removed.

### 4. Home Cards

The current text-only cards lose a key visual cue from the original home page. We will restore image-backed cards inspired by the original resume and YouTube blocks, but preserve the current text headings and descriptions so the cards remain informative and clickable.

### 5. Contact Page

The contact page currently feels older and flatter than the rest of the site. It will be rebuilt using the same visual language as the other main pages: strong hero, section rhythm, better card composition, and clearer hierarchy. The content intent remains simple: direct email first, channels second.

### 6. Calendar Embed

The Google Calendar iframe will be compared directly to the original site and updated so the default view matches the original instead of opening in month view. The surrounding section copy and layout should stay aligned with the established main-page structure.

## Files Expected To Change

- `index.html`
- `contact/index.html`
- `calendar/index.html`
- `assets/css/styles.css`
- `assets/js/main.js` or a new small page-effects script if separation is cleaner
- `assets/images/` for any newly downloaded hero/card imagery

## Behavior Notes

- Hero motion applies only to main pages, not volunteer post pages.
- The site must remain usable with JavaScript disabled; parallax is progressive enhancement.
- Card imagery must not replace the existing text; it should support it.
- Contact page content stays lightweight and static.

## Verification Plan

- Compare updated home, contact, and calendar pages against the original live site.
- Confirm hero height/crop improvement visually in desktop and mobile layouts.
- Confirm per-page imagery is actually different where intended.
- Confirm home page order matches the approved design.
- Confirm calendar opens in the correct default view.
- Run a fresh independent review subagent after implementation and fix any real issues found.

## Constraints

- Preserve the static GitHub Pages architecture.
- Avoid introducing heavy JS for hero motion.
- Keep styling consistent with the existing site while moving closer to the original where it matters most.
