# Layout, Grid & Spacing Systems

## Part 13: The 8-Point Grid System

Use multiples of 8 for all spacing, sizing, and layout decisions.

### Core Rules

```css
/* Base spacing scale */
:root {
  --space-1: 4px;   /* Half-step for icons/small text */
  --space-2: 8px;   /* Base unit */
  --space-3: 16px;  /* 2x */
  --space-4: 24px;  /* 3x */
  --space-5: 32px;  /* 4x */
  --space-6: 48px;  /* 6x */
  --space-7: 64px;  /* 8x */
  --space-8: 96px;  /* 12x */
}
```

### Why 8pt Works

- **Consistency**: All measurements follow the same rules
- **Reduced decisions**: Fewer spacing options = faster design + development
- **Multi-platform**: Most screen sizes divide evenly by 8 on at least one axis
- **Scaling**: Works cleanly at 1x, 2x, 3x resolutions

### Implementation Methods

**Hard Grid**: Display actual grid, align all elements to it (like Material Design's 4pt grid)

**Soft Grid**: Measure 8pt between elements without visible grid (better for iOS, faster workflow)

### Typography Exception

Text sizing and line-height don't always conform to 8pt while maintaining readability. Use platform guidelines and typeface-specific metrics, then build UI around established text dimensions.

---


## Part 14: Typography Scale Ratios

Use mathematical ratios for harmonious type hierarchies:

| Ratio | Name | Use Case |
|-------|------|----------|
| 1.067 | Minor Second | Subtle hierarchy, dense UI |
| 1.125 | Major Second | Conservative, professional |
| 1.200 | Minor Third | Balanced, versatile |
| 1.250 | Major Third | Clear distinction |
| 1.333 | Perfect Fourth | Strong hierarchy |
| 1.414 | Augmented Fourth | Dramatic contrast |
| 1.500 | Perfect Fifth | Bold statements |
| 1.618 | Golden Ratio | Classic proportion |

### Applying a Scale

```css
/* Using 1.250 (Major Third) with 16px base */
:root {
  --text-xs: 10px;    /* 16 ÷ 1.25 ÷ 1.25 */
  --text-sm: 13px;    /* 16 ÷ 1.25 */
  --text-base: 16px;  /* Base */
  --text-lg: 20px;    /* 16 × 1.25 */
  --text-xl: 25px;    /* 16 × 1.25² */
  --text-2xl: 31px;   /* 16 × 1.25³ */
  --text-3xl: 39px;   /* 16 × 1.25⁴ */
  --text-4xl: 49px;   /* 16 × 1.25⁵ */
}
```

**Tool**: Use https://typescale.com/ to generate scales with different ratios.

For fluid typography that scales smoothly between breakpoints using `clamp()`, see Part 24. For variable fonts and OpenType features, also Part 24.

---


## Part 15: Spatial System Approaches

### Element-First (Strict Sizing)

Prioritize component dimensions matching your spatial system:

```css
.button {
  height: 40px;  /* Fixed to grid */
  padding: 0 16px;
}
```

Best for: Buttons, form inputs, fixed-height components

### Content-First (Strict Padding)

Enforce consistent padding, let element sizes adapt:

```css
.card {
  padding: 24px;  /* Fixed padding */
  /* Height determined by content */
}
```

Best for: Cards, tables, variable-length content

---


