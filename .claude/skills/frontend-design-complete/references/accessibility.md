# Accessibility, i18n & Cognitive Accessibility

## Part 11: Comprehensive Accessibility Checklist

Reference checklist based on WCAG guidelines and A11Y Project standards.

### HTML & Structure
- [ ] Valid HTML (consistent browser/assistive technology support)
- [ ] `lang` attribute on `<html>` element
- [ ] Unique, descriptive page `<title>`
- [ ] Semantic landmark elements (`<nav>`, `<main>`, `<header>`, `<footer>`)
- [ ] Linear content flow (avoid problematic `tabindex` values)
- [ ] No `autofocus` attributes that disrupt navigation

### Headings
- [ ] Heading elements introduce content logically
- [ ] Only one `<h1>` per page
- [ ] Headings in logical sequence (no skipping levels)
- [ ] Headings describe the content that follows

### Keyboard Navigation
- [ ] Visible focus styles on all interactive elements
- [ ] Focus order matches visual layout logically
- [ ] Skip link to main content (visible on focus)
- [ ] All functionality accessible via keyboard
- [ ] No keyboard traps

### Images
- [ ] `alt` attributes on all `<img>` elements
- [ ] Descriptive alt text for informative images
- [ ] Empty `alt=""` for decorative images
- [ ] Text alternatives for complex graphics (charts, maps)

### Forms
- [ ] All inputs have associated `<label>` elements
- [ ] Labels use `for`/`id` pairing correctly
- [ ] Related inputs grouped with `<fieldset>` and `<legend>`
- [ ] Appropriate `autocomplete` attributes
- [ ] Error messages associated with corresponding inputs
- [ ] Don't communicate state through color alone
- [ ] Form errors displayed in list above form after submission

### Links & Buttons
- [ ] Links use `<a>` with `href` attribute
- [ ] Buttons use `<button>` element (not styled `<div>`)
- [ ] Link text is descriptive (not "click here")
- [ ] Links distinguishable not by color alone
- [ ] Warning when links open new tabs/windows

### Color & Contrast
- [ ] Normal text: 4.5:1 contrast ratio minimum
- [ ] Large text (18px+ or 14px+ bold): 3:1 minimum
- [ ] Icons and input borders: 3:1 minimum
- [ ] Information not conveyed by color alone
- [ ] Content tested in high contrast mode
- [ ] Text readable at 200% zoom

### Media
- [ ] No automatic media playback
- [ ] All media can be paused (including via spacebar)
- [ ] Video has captions
- [ ] Audio has transcripts
- [ ] No flashing content that could trigger seizures

### Motion & Animation
- [ ] `prefers-reduced-motion` media query respected
- [ ] Animations subtle, not excessive
- [ ] Parallax and decorative motion can be disabled
- [ ] Infinite scrolling can be turned off

### Mobile & Touch
- [ ] Viewport zoom not disabled
- [ ] Content works in any orientation
- [ ] No horizontal scrolling required
- [ ] Adequate spacing between touch targets (44x44px minimum)
- [ ] Touch targets easily activatable

### Cognitive Accessibility
- [ ] Content chunked into manageable sections (Part 29)
- [ ] Reduced-motion mode eliminates ALL animation, not just reduces it
- [ ] Focus mode available to reduce visual noise
- [ ] Text uses 1.5x line-height minimum, left-aligned (not justified)

---


## Part 28: Internationalization & RTL Design

If your interface will ever be translated, build for it from day one. Retrofitting RTL and text expansion is painful.

### Logical CSS Properties

Replace physical properties (left/right/top/bottom) with logical ones. They automatically adapt to writing direction.

```css
/* WRONG - Only works for LTR */
.sidebar {
  margin-left: 16px;
  padding-right: 24px;
  border-left: 2px solid var(--border);
  text-align: left;
}

/* CORRECT - Works for both LTR and RTL */
.sidebar {
  margin-inline-start: 16px;
  padding-inline-end: 24px;
  border-inline-start: 2px solid var(--border);
  text-align: start;
}
```

| Physical Property | Logical Property |
|-------------------|------------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `margin-top` | `margin-block-start` |
| `margin-bottom` | `margin-block-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `border-left` | `border-inline-start` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `width` | `inline-size` |
| `height` | `block-size` |

**Key Rule**: Every new CSS you write should use logical properties. There is no downside -- they work identically to physical properties in LTR and automatically adapt for RTL.

### RTL Design Considerations

```css
/* Set direction on root */
html[dir="rtl"] {
  direction: rtl;
}

/* Icons that need mirroring (directional meaning) */
html[dir="rtl"] .icon-arrow-forward,
html[dir="rtl"] .icon-chevron-right,
html[dir="rtl"] .icon-reply {
  transform: scaleX(-1);
}

/* Icons that DON'T mirror (universal meaning) */
/* checkmarks, close/X, search, download, play, pause */

/* Bidirectional text isolation */
.mixed-direction-text {
  unicode-bidi: isolate;
}
```

### Text Expansion & Contraction

Design for variable text lengths. Never hardcode widths on text containers.

| Language | Typical Change from English |
|----------|----------------------------|
| German | +30% longer |
| French | +20% longer |
| Finnish | +30-40% longer |
| Chinese | -50% shorter |
| Japanese | -40% shorter |
| Korean | -30% shorter |
| Arabic | +25% longer |

```css
/* Flexible button: accommodates translation expansion */
.button {
  padding-inline: var(--space-4);
  white-space: nowrap;
  min-inline-size: 0; /* Don't force minimum width */
  /* Let text determine width */
}

/* Truncation safety for constrained areas */
.nav-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-inline-size: 160px;
}
```

### Cultural Color Considerations

| Color | Western | East Asian | Middle Eastern |
|-------|---------|-----------|----------------|
| Red | Danger, stop | Prosperity, luck | Danger |
| White | Purity, clean | Mourning, death | Purity |
| Green | Go, success, nature | Youth, fertility | Islam (sacred), paradise |
| Yellow | Caution, warmth | Royalty, sacred | Happiness, prosperity |
| Black | Mourning, elegance | Power, formality | Mourning, mystery |
| Purple | Royalty, luxury | Nobility | Wealth |

**Key Rule**: Test color semantics with your target audience. Never assume universal meaning. Semantic color tokens like `--color-error` are safer than `--color-red` because their meaning transcends cultural interpretation.

### Number & Date Formatting

```javascript
/* Always use Intl APIs for locale-aware formatting */

/* Numbers */
new Intl.NumberFormat('de-DE').format(1234567.89);
// → "1.234.567,89"

new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
  .format(1234.50);
// → "$1,234.50"

/* Dates */
new Intl.DateTimeFormat('ja-JP', { dateStyle: 'long' })
  .format(new Date());
// → "2025年1月30日"
```

---


## Part 29: Cognitive Accessibility

Accessibility isn't just about screen readers. Design for how brains work -- including brains that work differently.

### Designing for ADHD

```css
/* Focus mode: reduce visual noise on demand */
[data-focus-mode="true"] .sidebar,
[data-focus-mode="true"] .notifications,
[data-focus-mode="true"] .decorative {
  display: none;
}

[data-focus-mode="true"] .main-content {
  max-width: 65ch;
  margin-inline: auto;
}

[data-focus-mode="true"] .nav {
  /* Simplified navigation */
  opacity: 0.4;
  transition: opacity 0.2s;
}

[data-focus-mode="true"] .nav:hover,
[data-focus-mode="true"] .nav:focus-within {
  opacity: 1;
}
```

Key principles for ADHD:
- Reduce visual noise: clear hierarchy, minimal competing elements
- Chunk information: short paragraphs, bullet points, clear headings
- Provide focus mode: ability to hide sidebar, notifications, decorative elements
- Undo support: forgiveness for impulsive actions
- Clear progress indicators: show where the user is and what's left

### Designing for Autism Spectrum

```css
/* Sensory-reduced mode */
[data-sensory-reduced="true"] {
  --transition-speed: 0s;
  --animation-speed: 0s;
}

[data-sensory-reduced="true"] * {
  animation-duration: 0s !important;
  transition-duration: 0s !important;
}

[data-sensory-reduced="true"] .decorative-bg,
[data-sensory-reduced="true"] .particle-effect,
[data-sensory-reduced="true"] .video-background {
  display: none;
}
```

Key principles:
- Predictable layouts: consistent navigation placement, no surprise modals
- Clear, literal language: no idioms in button labels ("Get started" not "Jump in")
- Warn before changes: transitions, redirects, automatic content updates
- Consistent patterns: same action should always look and work the same way

### Designing for Dyslexia

```css
/* Dyslexia-friendly typography */
.content {
  font-family: 'Open Sans', 'Verdana', sans-serif; /* Avoid serif and italic */
  font-size: 1rem;    /* Minimum 16px */
  line-height: 1.6;   /* 1.5x minimum */
  letter-spacing: 0.02em;
  word-spacing: 0.05em;
  text-align: left;   /* NEVER justify - irregular spacing is harder to read */
}

/* Avoid pure white backgrounds (glare) */
.content {
  background: #fafafa; /* Slight off-white reduces contrast fatigue */
  color: #2d2d2d;      /* Dark gray, not pure black */
}

/* Adequate paragraph spacing */
.content p + p {
  margin-top: 1.2em;
}

/* Short line lengths improve tracking */
.content {
  max-width: 60ch;
}
```

**Key Rule**: These patterns benefit ALL readers, not just those with dyslexia. Good reading ergonomics are universal.

### Vestibular Disorder Considerations

```css
/* Comprehensive reduced motion -- go further than the basics */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Remove parallax, zoom, and rotation effects */
  .parallax { transform: none !important; }
  .zoom-on-hover:hover { transform: none !important; }

  /* Disable video backgrounds */
  .video-background video { display: none; }
  .video-background { background-image: url('/static-fallback.jpg'); }

  /* Remove scroll-driven animations */
  * { animation-timeline: none !important; }
}
```

Some users need ZERO motion, not just reduced motion. Provide an explicit "disable all animations" toggle beyond what `prefers-reduced-motion` offers.

Cross-reference: Part 8 (Motion), Part 11 (Accessibility Checklist).

### Aging-Friendly Patterns

- Touch targets: 48px minimum (larger than the standard 44px)
- Contrast: target 7:1 for body text (higher than WCAG AA 4.5:1)
- Default text: 18px minimum body size
- Navigation: fewer levels, clearer labels, no hover-only reveals
- Error recovery: generous timeouts, clear confirmation dialogs, large undo buttons

### Cognitive Load Reduction

| Principle | Implementation |
|-----------|----------------|
| One primary action per screen | Single prominent CTA, secondary actions visually subdued |
| Progressive disclosure | Hide advanced options behind "More" or `<details>` |
| Consistent patterns | Same action looks and works the same everywhere |
| Meaningful defaults | Pre-select the most common option |
| Chunked information | Break long forms into steps, long text into sections |
| Clear wayfinding | Breadcrumbs, progress bars, "you are here" indicators |

Cross-reference: Part 9 (UX Principles) for Hick's Law and Miller's Law.

---


