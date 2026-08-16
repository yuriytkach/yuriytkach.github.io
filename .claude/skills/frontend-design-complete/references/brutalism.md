# Brutalist Design Principles

## Part 7: Brutalist Design Principles

For projects requiring anti-conventional aesthetics, study these brutalist principles:

### Core Philosophy

Brutalism in web design is "a reaction by a younger generation to the lightness, optimism, and frivolity of today's web design." Key principles:

1. **Technical Honesty** - Expose the scaffolding of web design rather than masking code and structure
2. **Anti-Commercial Stance** - Reject polish, persuasion, and visual manipulation
3. **Content-First** - Information hierarchy stripped to essentials; aesthetics serve function
4. **Deliberate Austerity** - Uncompromising, deliberately austere, defiantly unfashionable

### Implementation Patterns

```css
/* Brutalist typography */
body {
  font-family: monospace;
  font-size: 16px;
  line-height: 1.4;
}

/* Raw layout - no decorative margins */
.container {
  max-width: none;
  padding: 20px;
}

/* Harsh contrast */
body {
  background: #fff;
  color: #000;
}

/* Or inverted */
body.dark {
  background: #000;
  color: #fff;
}

/* Utilitarian navigation */
nav a {
  text-decoration: underline;
  color: inherit;
}

/* No hover effects or transitions */
a:hover {
  /* intentionally minimal or none */
}

/* Raw HTML elements, no embellishment */
button {
  border: 2px solid currentColor;
  background: transparent;
  padding: 8px 16px;
  font-family: inherit;
  cursor: pointer;
}
```

### When to Use Brutalism

- Artistic and experimental projects
- Anti-establishment brand positioning
- Developer tools and documentation
- Editorial/magazine content prioritizing text
- Portfolios for designers wanting to stand out

---


