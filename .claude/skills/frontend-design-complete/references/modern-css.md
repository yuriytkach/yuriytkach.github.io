# Modern CSS Techniques & Cascade Layers

## Part 18: Modern CSS Techniques

These features are baseline-available in all evergreen browsers (2025-2026). No polyfills needed. Use them to reduce JavaScript dependency and build more resilient interfaces.

### Container Queries

Make components responsive to their container, not the viewport. Essential for reusable component libraries.

```css
/* Define a containment context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Component adapts to its container width */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 16px;
  }
}

@container card (max-width: 399px) {
  .card {
    display: flex;
    flex-direction: column;
  }

  .card img {
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
  }
}
```

**Key Rule**: Use container queries for component-level responsiveness, media queries for page-level layout. A sidebar card and a main-content card can now use the same component with different layouts.

### The :has() Selector

The most powerful CSS selector added in years. Enables parent-aware styling without JavaScript.

```css
/* Style parent based on child state */
.form-group:has(:invalid) {
  border-color: var(--color-error);
}

/* Layout changes based on content */
.card:has(> img) {
  grid-template-rows: 200px 1fr;
}

.card:not(:has(> img)) {
  grid-template-rows: 1fr;
}

/* Interactive states without JS */
.nav:has(.dropdown:focus-within) .overlay {
  opacity: 1;
  pointer-events: auto;
}

/* Style sibling based on state */
.checkbox:has(:checked) + .label {
  text-decoration: line-through;
  opacity: 0.6;
}
```

**Key Rule**: `:has()` eliminates many JavaScript DOM manipulation patterns. Before writing `classList.toggle()` in JS, check if `:has()` can achieve the same result in CSS.

### CSS Subgrid

Align nested grid children to their parent's grid tracks. Solves the perennial "align cards in a grid" problem.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* title, description, CTA */
}

/* Titles, descriptions, and CTAs now align across all cards
   regardless of content length */
```

### View Transitions API

Animate between view states with native browser support. Replaces complex JavaScript transition libraries.

```css
/* Define elements that should morph between views */
.product-image {
  view-transition-name: product-hero;
}

.product-title {
  view-transition-name: product-title;
}

/* Style the transition */
::view-transition-old(product-hero) {
  animation: fadeOut 0.3s ease-out;
}

::view-transition-new(product-hero) {
  animation: fadeIn 0.3s ease-in;
}
```

```javascript
/* Trigger a view transition */
document.startViewTransition(() => {
  updateDOM(); /* Your state change */
});
```

Cross-reference: Part 8 (Motion Design) for animation principles.

### Scroll-Driven Animations

Replace JavaScript Intersection Observer with pure CSS scroll-triggered animations.

```css
/* Progress bar tied to page scroll */
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-primary);
  transform-origin: left;
  animation: growWidth linear;
  animation-timeline: scroll();
}

@keyframes growWidth {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

/* Fade-in on scroll into view */
.section {
  animation: fadeInUp linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Key Rule**: Scroll-driven animations run off-main-thread, making them smoother than JavaScript-based scroll handlers. Always prefer these over Intersection Observer for visual effects.

### CSS Nesting

Write nested styles without a preprocessor. Keeps component styles co-located and readable.

```css
.card {
  padding: var(--space-4);
  border-radius: var(--radius-md);

  & .title {
    font-size: var(--text-lg);
    font-weight: 600;
  }

  & .description {
    color: var(--text-secondary);
  }

  &:hover {
    box-shadow: var(--elevation-2);
  }

  @media (max-width: 768px) {
    padding: var(--space-3);
  }
}
```

**Key Rule**: Limit nesting to 3 levels maximum. Deeper nesting creates specificity problems and is hard to read.

### Anchor Positioning

Position tooltips, popovers, and dropdowns relative to anchor elements without JavaScript positioning libraries.

```css
.trigger {
  anchor-name: --tooltip-anchor;
}

.tooltip {
  position: fixed;
  position-anchor: --tooltip-anchor;
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 8px;

  /* Auto-flip if overflowing viewport */
  position-try-fallbacks: flip-block;
}
```

### Popover API

Build dismissable overlays with zero JavaScript. Handles focus trapping, backdrop, and light-dismiss behavior natively.

```html
<button popovertarget="menu">Open Menu</button>

<div id="menu" popover>
  <nav>
    <a href="/settings">Settings</a>
    <a href="/profile">Profile</a>
    <a href="/logout">Log out</a>
  </nav>
</div>
```

```css
[popover] {
  /* Positioned in top layer automatically */
  padding: var(--space-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--elevation-3);
}

/* Style the backdrop */
[popover]::backdrop {
  background: rgba(0, 0, 0, 0.3);
}
```

**Key Rule**: Use Popover API for any light-dismiss behavior (dropdown menus, tooltips, popovers) instead of custom click-outside handlers.

### Quick Reference

Also usable as an audit map: the "Legacy signature" column is what to grep for in an existing codebase — each hit is a modernization candidate.

| Feature | Replaces | Legacy signature to grep for | Use Case |
|---------|----------|------------------------------|----------|
| Container queries | Media queries for components | `@media` rules scoped to component classes | Reusable responsive components |
| `:has()` | JS class toggling | `classList.toggle\|classList.add` in UI-state handlers | Parent-aware styling |
| Subgrid | Manual alignment hacks | Fixed heights/margins syncing sibling cards | Consistent grid children |
| View Transitions | JS transition libraries | FLIP libs, `framer-motion` page transitions | Page/state transitions |
| Scroll-driven animations | Intersection Observer | `new IntersectionObserver` for reveal effects | Scroll-triggered effects |
| CSS nesting | Sass/Less nesting | `.scss` files used only for nesting | Scoped component styles |
| Anchor positioning | JS positioning | `@popperjs\|@floating-ui` imports | Tooltips, dropdowns |
| Popover API | Custom modal/dropdown JS | click-outside handlers (`document.addEventListener('click'`) | Light-dismiss overlays |
| `@layer` | Specificity management hacks | `!important`, chains like `.a .b .c` to out-specify | Design system CSS ordering |

(Cascade layers deep dive: Part 31 below.)

---


## Part 31: CSS Cascade Layers

Cascade layers solve specificity wars in design systems. They give you explicit control over which styles win, regardless of selector complexity.

### Why Layers Matter

```css
/* WITHOUT layers: specificity battles */
.component .button { background: blue; }        /* specificity: 0-2-0 */
.sidebar .component .button { background: red; } /* specificity: 0-3-0, wins */
.button.primary { background: green; }           /* specificity: 0-2-0, loses to red */

/* WITH layers: explicit priority */
@layer components, overrides;

@layer components {
  .component .button { background: blue; }
}

@layer overrides {
  .button.primary { background: green; } /* Wins because overrides layer > components layer */
}
```

**Key Rule**: Layers give you explicit control over which styles win. A simple selector in a higher-priority layer beats a complex selector in a lower-priority layer.

### Layer Ordering for Design Systems

```css
/* Declare order: first = lowest priority, last = highest */
@layer reset, base, tokens, layouts, components, utilities, overrides;

@layer reset {
  /* Normalize or CSS reset */
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer base {
  /* Default element styles */
  body { font-family: var(--font-body); color: var(--color-text-primary); }
  a { color: var(--color-interactive); }
}

@layer tokens {
  /* Design token definitions */
  :root { --color-primary: #1f6f6b; /* your brand value, not a framework default */ }
}

@layer layouts {
  /* Page structure */
  .container { max-width: 1200px; margin-inline: auto; }
  .grid { display: grid; }
}

@layer components {
  /* Component library */
  .button { /* ... */ }
  .card { /* ... */ }
}

@layer utilities {
  /* Utility classes (always beat components) */
  .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; }
  .hidden { display: none; }
}

@layer overrides {
  /* Project-specific overrides */
}
```

### Importing Third-Party CSS into Layers

```css
/* Wrap third-party CSS in a low-priority layer */
@import url('normalize.css') layer(reset);
@import url('component-library.css') layer(components);

/* Your styles in higher-priority layers always win */
@layer overrides {
  .their-button { /* Your customization */ }
}
```

### Nested Layers

```css
/* Organize complex component libraries */
@layer components {
  @layer buttons {
    .button { /* base button */ }
    .button--primary { /* primary variant */ }
  }

  @layer forms {
    .input { /* base input */ }
    .select { /* base select */ }
  }

  @layer cards {
    .card { /* base card */ }
  }
}

/* Reference nested layers */
@layer components.buttons {
  .button--custom { /* additional button style */ }
}
```

### Migration Strategy

Adopt layers incrementally in existing projects:

1. Wrap your existing CSS in a single layer: `@layer legacy { /* all existing CSS */ }`
2. New CSS goes in properly named layers
3. Gradually move code from `legacy` into structured layers
4. Unlayered CSS always beats layered CSS -- use this sparingly for critical overrides

Cross-reference: Part 26 (Component Architecture) for component-scoped layer patterns.

---


