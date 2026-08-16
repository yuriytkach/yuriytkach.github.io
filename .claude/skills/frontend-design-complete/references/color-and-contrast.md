# Color Contrast Rules

## Part 4: Color Contrast Rules

### Badge/Pill Elements

Always verify badge text contrasts with its background:

```css
/* WRONG - May be invisible on light backgrounds */
.badge {
  color: white;
}

/* CORRECT - Uses semantic variable */
.badge {
  color: var(--bg-primary);  /* Inverts with background */
}
```

### Color Swatches Display

Swatches showing colors need visible borders regardless of swatch color:

```css
.color-swatch {
  border: 2px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.3);
}
```

### Dark Theme Form Labels

**Problem**: Assuming labels should be white/light on dark themes.

```css
/* WRONG - Hardcoded color */
.label {
  color: white;
}

/* CORRECT - Uses semantic variable */
.label {
  color: var(--text-primary);
}
```

---


