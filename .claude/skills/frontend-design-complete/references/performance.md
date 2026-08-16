# Performance-First Design (Core Web Vitals)

## Part 19: Performance-First Design (Core Web Vitals)

Beautiful design means nothing if it takes 5 seconds to load. Design decisions directly impact performance metrics.

### The Three Metrics

| Metric | Good | Needs Work | Poor | What It Measures |
|--------|------|------------|------|------------------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s | Largest visible element loads |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms | Interactions feel instant |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 | Nothing jumps around |

### CLS Prevention Patterns

Layout shift is the most common design-caused performance issue. Prevent it at the design level.

```css
/* ALWAYS set dimensions on images */
img {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9; /* Browser reserves space before load */
}

/* Reserve space for dynamic content */
.embed-container {
  min-height: 300px;
  contain: layout;
}

/* Prevent font swap layout shift */
@font-face {
  font-family: 'Display';
  src: url('/fonts/display.woff2') format('woff2');
  font-display: swap;
  /* Match fallback metrics to reduce reflow */
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 20%;
}
```

**Key Rule**: Every element that loads asynchronously (images, embeds, fonts, lazy content) must have its space reserved before it arrives.

### LCP Optimization

Identify your LCP element (usually a hero image or headline) and prioritize it.

```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="/hero.avif" type="image/avif">

<!-- High priority on LCP image - never lazy-load this -->
<img src="/hero.avif" alt="Hero" fetchpriority="high" width="1200" height="600">

<!-- Inline critical CSS for above-the-fold content -->
<style>
  /* Only styles needed for initial viewport */
  .hero { display: grid; grid-template-columns: 1fr 1fr; min-height: 80vh; }
  .hero-title { font-size: clamp(2rem, 5vw, 4rem); }
</style>

<!-- Defer non-critical CSS -->
<link rel="stylesheet" href="/styles.css" media="print" onload="this.media='all'">
```

### INP Optimization

Keep interactions feeling instant by yielding to the main thread.

```javascript
/* Break up long tasks */
async function handleFilterChange(filters) {
  updateFilterUI(filters);       /* Visual feedback first */
  await scheduler.yield();        /* Let browser paint */
  const results = filterData(filters);  /* Heavy computation */
  await scheduler.yield();
  renderResults(results);         /* Update DOM */
}
```

```css
/* Use CSS for interactions where possible - no JS overhead */
details[open] .content {
  animation: slideDown 0.2s ease-out;
}

/* CSS-only accordion is faster than JS accordion */
```

### Skeleton Loaders

Skeletons prevent CLS by reserving exact space for incoming content.

```css
.skeleton {
  --skeleton-base: hsl(0 0% 88%);
  --skeleton-shine: hsl(0 0% 96%);
  background: linear-gradient(
    90deg,
    var(--skeleton-base) 25%,
    var(--skeleton-shine) 50%,
    var(--skeleton-base) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
  border-radius: var(--radius-sm);
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}

/* Dark mode skeleton */
@media (prefers-color-scheme: dark) {
  .skeleton {
    --skeleton-base: hsl(0 0% 18%);
    --skeleton-shine: hsl(0 0% 25%);
  }
}

/* Skeleton must match exact dimensions of real content */
.skeleton-title { height: 28px; width: 60%; }
.skeleton-text { height: 16px; width: 100%; }
.skeleton-avatar { height: 48px; width: 48px; border-radius: 50%; }
```

**Key Rule**: Skeletons must match the exact dimensions of the content they replace. A mismatched skeleton is worse than no skeleton because it causes shift when real content arrives.

### Animation Performance Budget

```css
/* SAFE to animate (compositor-only, GPU-accelerated) */
.animate-safe {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

/* NEVER animate (triggers layout recalculation) */
/* width, height, margin, padding, top, left, right, bottom,
   border, box-shadow (with spread changes), font-size */

/* Use will-change sparingly - only for heavy animations */
.heavy-animation {
  will-change: transform;
}
/* Remove will-change after animation completes */

/* Contain layout-heavy sections */
.animated-section {
  contain: layout paint;
}
```

### Resource Hints

```html
<!-- Preload: critical resources for THIS page -->
<link rel="preload" as="font" href="/fonts/display.woff2" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="/hero.avif">

<!-- Preconnect: establish early connections to critical origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://api.example.com">

<!-- Prefetch: resources for NEXT likely navigation -->
<link rel="prefetch" href="/dashboard.js">

<!-- DNS Prefetch: resolve DNS for third-party domains -->
<link rel="dns-prefetch" href="https://analytics.example.com">
```

| Hint | When to Use | Impact |
|------|-------------|--------|
| `preload` | Critical above-the-fold resources | Reduces LCP |
| `preconnect` | APIs, font hosts, CDNs | Reduces connection time |
| `prefetch` | Next page resources | Faster navigation |
| `dns-prefetch` | Third-party domains | Minor latency reduction |
| `fetchpriority="high"` | LCP image/resource | Browser prioritization |

### Performance Checklist

- [ ] LCP element identified and has `fetchpriority="high"`
- [ ] All images have explicit `width`/`height` or `aspect-ratio`
- [ ] Fonts use `font-display: swap` with `size-adjust` fallback
- [ ] Skeleton loaders match exact content dimensions
- [ ] Only `transform`/`opacity` animated (never layout properties)
- [ ] Critical CSS inlined for above-the-fold content
- [ ] Resource hints applied for key assets and origins

---


