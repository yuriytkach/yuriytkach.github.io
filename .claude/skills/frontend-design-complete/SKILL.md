---
name: frontend-design-complete
description: Create distinctive, production-grade frontend interfaces AND audit existing ones for generic "AI-generated" design. Use when building any web UI, and whenever the user asks to review, scan, or critique an app or website's design, asks "does this look AI-generated?", or wants their site to look unique, less generic, or less like a template. Covers anti-AI-slop detection and scoring, aesthetics, mobile-first patterns, modern CSS, performance (Core Web Vitals), dark mode/theming, AI-era patterns, interaction design, data visualization, typography, component architecture, forms, internationalization, accessibility, and design tokens. Use this as your single frontend design skill.
---

# Complete Frontend Design Guidelines

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics while ensuring proper mobile responsiveness and cross-element consistency.

## Two Modes — Pick One First

- **Audit mode** — the user has an *existing* app or website and wants it reviewed: "does this look AI-generated?", "make it look unique", "design review/critique". Read **`references/design-audit.md`** and follow its workflow: scan the source for slop signatures (optionally with `scripts/scan_slop.py`), apply the intentionality test, score, and deliver the report template. The AI Slop Patterns list below is your shared vocabulary for what to look for. Deliver the audit before rewriting anything.
- **Create mode** — building or restyling a UI. The aesthetic direction below (Part 1) applies to **every** creation task — read it first.

Deeper, topic-specific guidance lives in the `references/` folder; load the relevant file(s) on demand using the routing table further down.

---

## Part 1: Design Thinking & Aesthetics

### Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail
- **Fully mobile responsive** (see `references/mobile-and-responsive.md`)

### Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects that match the overall aesthetic: gradient meshes, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors. (Noise/grain/paper texture overlays have become an AI-slop tell — see the avoid-list below — reach for structure and geometry instead of texture.)

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

### AI Slop Patterns to Avoid

These specific patterns have become telltale signs of AI-generated design. Avoid them:

**Colors:**
- Cream/off-white backgrounds (`#f8f6f3`, `#fdfcfb`, `#faf8f5` type colors)
- Terracotta/coral/rust accents (`#c45c48`, `#e07860`, `#d4715f`, `#bf4a37`)
- Orange and teal combinations
- Purple/blue gradients on white backgrounds
- Warm shadows with colored tints

**Layout & Components:**
- Generous rounded corners (12-16px+ border-radius)
- Left-border accent lines on cards (the colored vertical stripe)
- Pill-shaped tabs and buttons
- Cards with subtle warm shadows and hover lift effects
- Overly "friendly" and "approachable" feeling

**Visual Effects:**
- Texture overlays (noise, grain, paper textures)
- Glow effects and colored shadows
- Gradient backgrounds with warm color temperature
- Soft, diffused aesthetic everywhere

**Overall Aesthetic:**
- The "cozy webapp" look - warm, soft, inviting
- Designs that feel like Notion/Linear clones
- Safe, inoffensive, "premium but accessible" feeling
- Lack of sharp contrast or bold decisions

Instead, make distinctive choices: cooler color temperatures, sharper geometry, unexpected color combinations, higher contrast, or commit fully to a specific design tradition (Swiss, Japanese, Brutalist, Editorial, etc.) rather than the generic "modern SaaS" look.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

---

## Reference Files — When to Read What

Part 1 above is always in play. For everything else, open the matching file(s) in `references/` as the task requires. Each file preserves the original numbered "Part" sections, so cross-references like "see Part 20" resolve to the corresponding part heading inside these files.

| If the task involves… | Read |
|---|---|
| **Auditing an existing app/site** — "looks AI-generated", design review, make it unique | `references/design-audit.md` + `scripts/scan_slop.py` |
| Mobile layout, breakpoints, responsive images | `references/mobile-and-responsive.md` (Parts 2, 25) |
| Form inputs, selects, validation, multi-step forms | `references/forms.md` (Parts 3, 27) |
| Color contrast / WCAG legibility | `references/color-and-contrast.md` (Part 4) |
| Design-system thinking, UX / humane principles, Dieter Rams, settings | `references/foundations-and-principles.md` (Parts 6, 9, 10, 12, 16) |
| Grids, 8-point spacing, type scale, spatial systems | `references/layout-and-spacing.md` (Parts 13, 14, 15) |
| Fluid / responsive typography (`clamp()`, etc.) | `references/typography.md` (Part 24) |
| Container queries, `:has()`, scroll-driven animation, view transitions, cascade layers | `references/modern-css.md` (Parts 18, 31) |
| Core Web Vitals, CLS/LCP, font & asset loading | `references/performance.md` (Part 19) |
| Dark mode, theming, design token architecture | `references/dark-mode-and-tokens.md` (Parts 20, 30) |
| Motion design, micro-interactions, advanced interaction | `references/motion-and-interaction.md` (Parts 8, 22) |
| Streaming UI, confidence indicators, human-in-the-loop, chat/agent UIs | `references/ai-era-patterns.md` (Part 21) |
| Charts, dashboards, data-dense views | `references/data-visualization.md` (Part 23) |
| Component architecture & composition patterns | `references/components.md` (Part 26) |
| Accessibility checklist, i18n / RTL, cognitive accessibility | `references/accessibility.md` (Parts 11, 28, 29) |
| Brutalist aesthetic specifically | `references/brutalism.md` (Part 7) |
| Where to find inspiration, learning resources, troubleshooting common issues | `references/resources.md` (Parts 5, 17 + Common Issues table) |

---

## Pre-Implementation Checklist

(Create mode. In audit mode, the deliverable is the report template in `references/design-audit.md` instead.)

Before finalizing any frontend design, verify:

### Aesthetics
- [ ] Committed to a bold, distinctive aesthetic direction
- [ ] Avoided AI slop patterns (cream backgrounds, terracotta accents, purple gradients)
- [ ] Used distinctive typography (not Inter, Roboto, Arial)
- [ ] Created cohesive color palette with CSS variables

### Mobile Responsiveness
- [ ] Hero section centers on mobile (not left-aligned with empty space)
- [ ] Grid layouts collapse to single column on mobile
- [ ] Large selection lists use accordion on mobile (not horizontal scroll)
- [ ] Status/alert cards center properly on mobile
- [ ] Font sizes scale appropriately for mobile

### Form Elements
- [ ] All form fields (input, select, textarea) styled consistently
- [ ] Radio buttons and checkboxes visible (especially for transparent-border styles)
- [ ] Dropdown options have readable backgrounds
- [ ] Textarea has appropriate border-radius (not pill-shaped)

### Color Contrast
- [ ] Labels use semantic color variables (not hardcoded)
- [ ] Badge/pill text contrasts with background
- [ ] Color swatches have visible borders
- [ ] Dark theme elements properly contrasted

For the full, in-depth verification list covering modern CSS, performance, dark mode, AI patterns, accessibility, i18n, tokens, and cascade layers, see **`references/extended-checklist.md`**.

---

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision - while ensuring it works beautifully on every screen size.
