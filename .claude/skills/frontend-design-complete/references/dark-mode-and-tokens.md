# Dark Mode, Theming & Design Tokens

## Part 20: Dark Mode & Theming

Dark mode is not "invert the colors." It requires intentional design decisions about depth, contrast, and color behavior.

### System Preference Detection

```css
/* CSS-first approach (recommended) */
:root {
  color-scheme: light dark; /* Tells browser to style form controls */

  /* Light mode tokens (default) */
  --color-surface-0: #ffffff;
  --color-surface-1: #f5f5f5;
  --color-surface-2: #ebebeb;
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #666666;
  --color-border: #e0e0e0;
  --color-interactive: hsl(220, 90%, 50%);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-0: #121212;
    --color-surface-1: #1e1e1e;
    --color-surface-2: #2a2a2a;
    --color-text-primary: #e5e5e5;
    --color-text-secondary: #a0a0a0;
    --color-border: rgba(255, 255, 255, 0.12);
    --color-interactive: hsl(220, 70%, 65%);
  }
}
```

### User Override Pattern

Always allow users to override system preference. Use a three-state toggle: System / Light / Dark.

```css
/* Theme applied via data attribute */
[data-theme="light"] {
  --color-surface-0: #ffffff;
  --color-text-primary: #1a1a1a;
  /* ... light tokens ... */
}

[data-theme="dark"] {
  --color-surface-0: #121212;
  --color-text-primary: #e5e5e5;
  /* ... dark tokens ... */
}
```

```javascript
/* Three-state toggle with system fallback */
function setTheme(preference) {
  if (preference === 'system') {
    document.documentElement.removeAttribute('data-theme');
    localStorage.removeItem('theme');
  } else {
    document.documentElement.setAttribute('data-theme', preference);
    localStorage.setItem('theme', preference);
  }
}

/* Restore on page load (run in <head> to prevent flash) */
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
```

**Key Rule**: Always default to system preference. Never force a theme. Run the restore script in `<head>` to prevent a flash of wrong theme (FOWT).

### The light-dark() CSS Function

Concise inline theme switching for simple cases.

```css
:root {
  color-scheme: light dark;
}

.text {
  color: light-dark(#1a1a1a, #e5e5e5);
}

.surface {
  background: light-dark(#ffffff, #121212);
}

.border {
  border-color: light-dark(#e0e0e0, rgba(255, 255, 255, 0.12));
}
```

Use `light-dark()` for simple one-off values. Use custom properties for values referenced in multiple places.

### Color Adjustments for Dark Mode

Colors that look great on light backgrounds often look harsh on dark backgrounds.

```css
:root {
  /* Light mode: high saturation, lower lightness */
  --color-primary: hsl(220, 90%, 50%);
  --color-success: hsl(145, 80%, 38%);
  --color-error: hsl(0, 85%, 50%);
}

@media (prefers-color-scheme: dark) {
  :root {
    /* Dark mode: reduce saturation ~20%, increase lightness */
    --color-primary: hsl(220, 70%, 65%);
    --color-success: hsl(145, 60%, 55%);
    --color-error: hsl(0, 65%, 60%);
  }
}

/* Text: never use pure white on dark. Use off-white. */
/* #e5e5e5 or rgba(255, 255, 255, 0.87) reduces eye strain */
```

**Key Rule**: Desaturate colors ~20% and increase lightness for dark mode. Pure white text on pure black is harder to read than off-white on dark gray.

### Depth Without Shadows

Shadows are nearly invisible on dark backgrounds. Use surface elevation instead.

```css
/* Dark mode depth = lighter surfaces at higher elevation */
:root {
  --surface-0: #121212; /* Base/background */
  --surface-1: #1e1e1e; /* Cards, bottom sheets */
  --surface-2: #232323; /* Raised cards, app bars */
  --surface-3: #292929; /* Modals, dropdowns */
  --surface-4: #333333; /* Tooltips, popovers */
}

/* Subtle borders for edge definition */
.card {
  background: var(--surface-1);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.modal {
  background: var(--surface-3);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

/* Light mode still uses shadows normally */
@media (prefers-color-scheme: light) {
  .card { box-shadow: var(--elevation-1); border: none; }
  .modal { box-shadow: var(--elevation-4); border: none; }
}
```

### Multi-Theme Token Architecture

Support more than just light/dark. High-contrast and brand themes use the same token system.

| Token | Light | Dark | High Contrast |
|-------|-------|------|---------------|
| `--surface-0` | `#ffffff` | `#121212` | `#000000` |
| `--text-primary` | `#1a1a1a` | `#e5e5e5` | `#ffffff` |
| `--border` | `#e0e0e0` | `rgba(255,255,255,0.12)` | `#ffffff` |
| `--interactive` | `hsl(220,90%,50%)` | `hsl(220,70%,65%)` | `hsl(220,100%,70%)` |

```css
/* Windows High Contrast Mode */
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;
    background: ButtonFace;
    color: ButtonText;
  }

  .button:hover {
    background: Highlight;
    color: HighlightText;
  }

  /* forced-colors uses system keywords, not custom values */
}
```

Cross-reference: Part 30 (Design Token Architecture) for the full three-tier token system.

### Image & Media in Dark Mode

```css
/* Reduce image brightness in dark mode to prevent glare */
@media (prefers-color-scheme: dark) {
  img:not([src$=".svg"]) {
    filter: brightness(0.85);
  }

  /* SVG icons using currentColor adapt automatically */
  .icon { color: var(--text-primary); }
}
```

```html
<!-- Serve different images per theme -->
<picture>
  <source srcset="/hero-dark.avif" media="(prefers-color-scheme: dark)">
  <img src="/hero-light.avif" alt="Hero illustration">
</picture>
```

### Dark Mode Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Pure black (`#000`) backgrounds | Harsh contrast, eye strain | Use `#121212` or similar dark gray |
| Saturated colors on dark | Optical vibration, fatigue | Desaturate ~20%, increase lightness |
| Inverted shadows | Shadows invisible on dark | Use surface elevation (lighter = higher) |
| Forgetting scrollbar | System scrollbar clashes | `color-scheme: dark` or custom scrollbar CSS |
| Forgetting form defaults | Native inputs stay light | `color-scheme: dark` on `:root` |
| Flash of wrong theme | Theme loads after paint | Run theme script in `<head>` |

---


## Part 30: Design Token Architecture

Tokens are the single source of truth for your design system. Get the architecture right and theming, maintenance, and consistency follow naturally.

### Three-Tier Token Structure

```css
/* TIER 1: Constant/Primitive tokens - raw values, never used directly in components */
:root {
  /* Values below are placeholders — substitute your brand's palette.
     Shipping Tailwind defaults (#3b82f6 etc.) as tokens is an AI-slop tell. */
  --primitive-petrol-50: #eef4f4;
  --primitive-petrol-500: #1f6f6b;
  --primitive-petrol-700: #124c49;
  --primitive-gray-50: #f6f7f7;
  --primitive-gray-900: #16181a;
  --primitive-radius-sm: 4px;
  --primitive-radius-md: 8px;
  --primitive-space-1: 4px;
  --primitive-space-2: 8px;
  --primitive-space-4: 16px;
  --primitive-space-6: 24px;
}

/* TIER 2: Semantic tokens - purpose-based, reference primitives */
:root {
  --color-interactive: var(--primitive-petrol-500);
  --color-interactive-hover: var(--primitive-petrol-700);
  --color-surface: var(--primitive-gray-50);
  --color-text-primary: var(--primitive-gray-900);
  --radius-component: var(--primitive-radius-md);
  --spacing-component-padding: var(--primitive-space-4);
}

/* TIER 3: Component tokens - scoped to specific components */
.button {
  --button-bg: var(--color-interactive);
  --button-bg-hover: var(--color-interactive-hover);
  --button-padding: var(--spacing-component-padding);
  --button-radius: var(--radius-component);

  background: var(--button-bg);
  padding: var(--button-padding);
  border-radius: var(--button-radius);
}

.button:hover {
  background: var(--button-bg-hover);
}
```

**Flow**: Primitive → Semantic → Component. Components only reference component tokens. Semantic tokens only reference primitives. This creates clean separation of concerns.

### Naming Conventions

Pattern: `category-subcategory-variant-state`

| Category | Examples |
|----------|---------|
| `color-` | `color-text-primary`, `color-surface-elevated`, `color-border-subtle` |
| `spacing-` | `spacing-component-gap`, `spacing-section-padding` |
| `typography-` | `typography-heading-size`, `typography-body-weight` |
| `elevation-` | `elevation-card`, `elevation-modal` |
| `radius-` | `radius-button`, `radius-input`, `radius-card` |
| `motion-` | `motion-duration-fast`, `motion-easing-default` |

**Key Rule**: Names describe purpose, never appearance. Use `--color-interactive`, not `--color-blue`. Use `--color-error`, not `--color-red`. When the brand color changes from blue to green, only primitive tokens change.

### Multi-Theme Token Mapping

```css
/* Theme mapping through semantic tokens */
[data-theme="light"] {
  --color-surface: #ffffff;
  --color-surface-elevated: #f5f5f5;
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #666666;
  --color-border: #e0e0e0;
  --color-interactive: hsl(220, 90%, 50%);
}

[data-theme="dark"] {
  --color-surface: #121212;
  --color-surface-elevated: #1e1e1e;
  --color-text-primary: #e5e5e5;
  --color-text-secondary: #a0a0a0;
  --color-border: rgba(255, 255, 255, 0.12);
  --color-interactive: hsl(220, 70%, 65%);
}

[data-theme="high-contrast"] {
  --color-surface: #000000;
  --color-surface-elevated: #1a1a1a;
  --color-text-primary: #ffffff;
  --color-text-secondary: #e0e0e0;
  --color-border: #ffffff;
  --color-interactive: hsl(220, 100%, 70%);
}
```

Components don't change at all between themes -- only the semantic token values change. Cross-reference: Part 20 (Dark Mode) for implementation patterns.

### Token Maintenance

- **Audit regularly**: search for hardcoded values (`#`, `rgb(`, `hsl(`, `px` outside tokens)
- **Deprecation strategy**: rename → alias old to new → remove old after migration
- **Avoid token explosion**: don't create `--button-primary-hover-border-color` if `--color-interactive-hover` works
- **Document usage**: each token should have a description of where and when to use it
- **W3C Design Tokens format**: use JSON tokens as source of truth if integrating with design tools

```json
{
  "color": {
    "interactive": {
      "$value": "{primitive.petrol.500}",
      "$type": "color",
      "$description": "Primary interactive elements: buttons, links, toggles"
    }
  }
}
```

### Quick Reference

| Tier | Changes When | Example |
|------|-------------|---------|
| Primitive | Brand refresh, new palette | `--primitive-petrol-500: #1f6f6b` |
| Semantic | Feature redesign, new patterns | `--color-interactive: var(--primitive-petrol-500)` |
| Component | Component-specific tweaks | `--button-bg: var(--color-interactive)` |

---


