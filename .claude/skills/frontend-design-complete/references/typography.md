# Fluid & Responsive Typography

## Part 24: Fluid & Responsive Typography

Stop using breakpoints for font sizes. Use fluid typography that scales smoothly between any viewport width.

### CSS clamp() for Fluid Type

```css
/* Syntax: clamp(minimum, preferred, maximum) */
/* preferred uses viewport units for smooth scaling */

:root {
  --text-xs: clamp(0.625rem, 0.55rem + 0.3vw, 0.75rem);
  --text-sm: clamp(0.75rem, 0.65rem + 0.4vw, 0.875rem);
  --text-base: clamp(0.875rem, 0.75rem + 0.5vw, 1rem);
  --text-lg: clamp(1rem, 0.8rem + 0.8vw, 1.25rem);
  --text-xl: clamp(1.25rem, 0.9rem + 1.4vw, 1.75rem);
  --text-2xl: clamp(1.5rem, 1rem + 2vw, 2.25rem);
  --text-3xl: clamp(1.875rem, 1rem + 3.5vw, 3rem);
  --text-4xl: clamp(2.25rem, 1rem + 5vw, 4rem);
}

/* Apply semantically */
h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
body { font-size: var(--text-base); }
.caption { font-size: var(--text-sm); }
```

**Key Rule**: Set `min` for mobile readability, `max` for desktop restraint, `preferred` for smooth scaling. Use https://utopia.fyi/ to generate fluid scales.

### Variable Fonts

One font file, infinite weights and widths. Better performance and design flexibility.

```css
@font-face {
  font-family: 'Display';
  src: url('/fonts/display-variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

/* Fine-tuned weight hierarchy */
.heading { font-weight: 720; }
.subheading { font-weight: 580; }
.body { font-weight: 400; }
.caption { font-weight: 350; }

/* Animate weight on interaction */
.nav-link {
  font-weight: 400;
  transition: font-weight 0.2s ease;
}

.nav-link:hover,
.nav-link[aria-current="page"] {
  font-weight: 650;
}

/* Responsive weight: bolder on large screens, lighter on small */
h1 {
  font-weight: clamp(600, 500 + 2vw, 800);
}
```

Performance benefit: one variable font file replaces multiple static font files, significantly improving LCP. Cross-reference: Part 19 (Performance) for font loading.

### Line-Length Optimization

Optimal line length for readability: 45-75 characters per line. 66 characters is ideal.

```css
/* Constrain content width with ch units */
.prose {
  max-width: 65ch;
  margin-inline: auto;
}

/* Responsive: shorter lines on mobile */
@media (max-width: 768px) {
  .prose {
    max-width: 55ch;
  }
}

/* Wide layout with constrained text */
.section {
  width: 100%;
  padding: var(--space-8) var(--space-4);
}

.section .content {
  max-width: 65ch;
  margin-inline: auto;
}
```

### OpenType Features

Unlock typographic refinement built into quality fonts.

```css
/* Tabular numbers for aligned data columns */
.data-value {
  font-variant-numeric: tabular-nums;
}

/* Oldstyle numbers for body text (more readable inline) */
.prose {
  font-variant-numeric: oldstyle-nums;
}

/* Fractions */
.recipe-amount {
  font-variant-numeric: diagonal-fractions;
}

/* Small caps for labels and abbreviations */
.abbreviation {
  font-variant-caps: all-small-caps;
  letter-spacing: 0.05em;
}

/* Ligatures for refined body text */
.prose {
  font-variant-ligatures: common-ligatures contextual;
}
```

Cross-reference: Part 23 (Data Viz) for tabular numbers in tables.

### Text Rendering & Wrapping

```css
/* Optimize legibility for headings (enables kerning + ligatures) */
h1, h2, h3 {
  text-rendering: optimizeLegibility;
}

/* Balanced headings: prevent orphans */
h1, h2, h3 {
  text-wrap: balance;
}

/* Pretty body text: avoid single-word last lines */
p {
  text-wrap: pretty;
}

/* Font smoothing: use judiciously, test on both light and dark */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

---


