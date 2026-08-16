# Mobile-First & Responsive Patterns

## Part 2: Mobile-First Responsive Patterns

### Hero Sections

**Problem**: 2-column grid layouts leave empty space when one column is hidden on mobile.

```css
/* Desktop: 2-column grid */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}

/* Mobile: Switch to centered flex */
@media (max-width: 768px) {
  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 40px 20px;
    gap: 24px;
  }

  .hero-content {
    align-items: center;
  }

  .hero-badge {
    align-self: center;
  }

  .hero-title {
    font-size: 32px;
    text-align: center;
  }

  .hero-subtitle {
    font-size: 14px;
    text-align: center;
  }

  .hero-cta {
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  .hero-cta .btn {
    width: 100%;
    max-width: 280px;
  }

  .hero-visual {
    display: none;
  }
}
```

**Key Rule**: When hiding grid columns on mobile, switch from `display: grid` to `display: flex` to eliminate reserved empty space.

### Large Selection Lists (Accordion Pattern)

**Problem**: Horizontal scroll for many items (20+) is unusable on mobile - text gets cut off.

**Solution**: Use collapsible accordion with category headers.

```jsx
function StyleSelector({ items, categories }) {
  const [expandedCategory, setExpandedCategory] = useState(null);

  return (
    <div className="selector">
      {categories.map(category => (
        <div key={category.name} className={`category ${expandedCategory === category.name ? 'expanded' : ''}`}>
          <button
            className="category-header"
            onClick={() => setExpandedCategory(
              expandedCategory === category.name ? null : category.name
            )}
          >
            <span>{category.name}</span>
            <ChevronIcon />
          </button>
          <div className="category-items">
            {category.items.map(item => (
              <button key={item.id} className="item">{item.name}</button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

```css
@media (max-width: 768px) {
  .category-items {
    display: none;
  }

  .category.expanded .category-items {
    display: flex;
    flex-direction: column;
  }

  .chevron-icon {
    transition: transform 0.2s ease;
  }

  .category.expanded .chevron-icon {
    transform: rotate(180deg);
  }
}
```

### Form Layouts

**Problem**: Multi-column form layouts get cut off on mobile.

```css
.form-row {
  display: flex;
  gap: 16px;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }

  .form-group {
    width: 100%;
  }
}
```

### Status/Alert Cards

**Problem**: Inconsistent text alignment when stacking horizontally-laid elements vertically.

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

@media (max-width: 768px) {
  .alert {
    flex-direction: column;
    align-items: center;  /* Center the flex items */
    text-align: center;   /* Center the text within items */
    gap: 8px;
  }

  .alert strong {
    text-align: center;  /* Explicit for block elements */
  }
}
```

**Key Rule**: Stacked flex items need BOTH `align-items: center` AND `text-align: center` for proper centering.

### Grid Layouts

```css
@media (max-width: 768px) {
  .pricing-grid,
  .feature-grid,
  .team-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
```

### Breakpoint Reference

```css
/* Tablet - Stack sidebars, maintain content width */
@media (max-width: 1200px) { }

/* Mobile - Full single-column, centered hero */
@media (max-width: 768px) { }

/* Small Mobile - Compact spacing, reduced font sizes */
@media (max-width: 480px) { }
```

### Mobile Font Scaling

```css
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;  /* Down from ~48px */
  }

  .section-title {
    font-size: 24px;  /* Down from ~32px */
  }

  .section-subtitle {
    font-size: 14px;  /* Down from ~16px */
  }
}
```

**Modern Alternative**: Container queries (Part 18) can replace many media queries by making components responsive to their container width rather than the viewport. For fluid font sizing without breakpoints, see Part 24.

---


## Part 25: Responsive Image Strategies

Images are typically the largest assets on a page and the most common LCP element. Get them right for both aesthetics and performance.

### Format Hierarchy

```
AVIF (best compression) → WebP (wide support) → JPEG (fallback)
SVG for icons, logos, illustrations
PNG only for transparency where AVIF/WebP unavailable
```

```html
<!-- Format fallback chain -->
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img src="/hero.jpg" alt="Hero image" width="1200" height="600">
</picture>
```

### Art Direction with picture

Serve different crops for different viewports. Not just different sizes -- different compositions.

```html
<!-- Portrait crop on mobile, landscape on desktop -->
<picture>
  <source
    srcset="/hero-portrait.avif"
    media="(max-width: 768px)"
    type="image/avif"
    width="600" height="800">
  <source
    srcset="/hero-landscape.avif"
    media="(min-width: 769px)"
    type="image/avif"
    width="1200" height="600">
  <img src="/hero-landscape.jpg" alt="Product hero" width="1200" height="600">
</picture>
```

Use `<picture>` when the image composition changes per viewport (art direction). Use `srcset` when the same image is just served at different resolutions.

### srcset and sizes

```html
<!-- Resolution switching: same image, different sizes -->
<img
  srcset="
    /product-400.avif 400w,
    /product-800.avif 800w,
    /product-1200.avif 1200w,
    /product-1600.avif 1600w"
  sizes="
    (max-width: 768px) 100vw,
    (max-width: 1200px) 50vw,
    33vw"
  src="/product-800.jpg"
  alt="Product photo"
  width="800"
  height="600"
  loading="lazy">
```

**Key Rule**: Always include `sizes`. Without it, the browser assumes the image is 100vw and downloads the largest version. The `sizes` attribute tells the browser how wide the image will actually be rendered.

### Lazy Loading

```html
<!-- LCP image: eager load, high priority -->
<img src="/hero.avif" alt="Hero" fetchpriority="high" decoding="async"
     width="1200" height="600">

<!-- Below-the-fold images: lazy load -->
<img src="/feature.avif" alt="Feature" loading="lazy" decoding="async"
     width="800" height="600">
```

**Key Rule**: Never lazy-load the LCP image. Use `fetchpriority="high"` on the LCP image and `loading="lazy"` on everything below the fold. Cross-reference: Part 19 (Performance) for LCP optimization.

### aspect-ratio CSS Property

Prevent CLS by reserving space before images load. Replaces the old padding-bottom hack.

```css
/* Fixed aspect ratio container */
.image-container {
  aspect-ratio: 16 / 9;
  width: 100%;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Responsive video embed */
.video-embed {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.video-embed iframe {
  width: 100%;
  height: 100%;
  border: 0;
}
```

### object-fit / object-position

Create uniform image grids despite varied source dimensions.

```css
/* Uniform card images */
.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  object-position: center top; /* Focus on faces/content */
}

/* Avatar: always square, always centered */
.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center;
}

/* Contain for logos (show full logo, no cropping) */
.partner-logo {
  width: 120px;
  height: 60px;
  object-fit: contain;
}
```

---


