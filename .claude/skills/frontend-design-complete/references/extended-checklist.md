## Extended Pre-Implementation Checklist

Before finalizing any frontend design, verify:

### Aesthetics
- [ ] Committed to a bold, distinctive aesthetic direction
- [ ] Avoided AI slop patterns (cream backgrounds, terracotta accents, purple gradients)
- [ ] Used distinctive typography (not Inter, Roboto, Arial)
- [ ] Created cohesive color palette with CSS variables
- [ ] Researched inspiration from curated galleries (Godly, Minimal Gallery, Brutalist)

### Design System
- [ ] Established design tokens (colors, spacing, typography)
- [ ] Created consistent elevation/shadow system
- [ ] Defined typography scale with clear hierarchy
- [ ] Supported density variants if needed for data-heavy UI

### UX Heuristics
- [ ] System status visible (loading states, progress, confirmations)
- [ ] Language matches user expectations (no jargon)
- [ ] Undo/cancel options available for user control
- [ ] Consistent patterns throughout interface
- [ ] Error prevention through constraints and confirmations
- [ ] Recognition over recall (visible options, contextual help)
- [ ] Shortcuts available for power users
- [ ] Minimal design (no competing irrelevant information)

### Humane Design
- [ ] No infinite scroll without endpoints
- [ ] No autoplay media
- [ ] Clear exit/unsubscribe options
- [ ] No dark patterns or confirmation shaming
- [ ] User data practices transparent
- [ ] Respects user attention (appropriate notifications)

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
- [ ] All inputs have associated labels
- [ ] Error messages associated with inputs

### Color & Contrast
- [ ] Labels use semantic color variables (not hardcoded)
- [ ] Badge/pill text contrasts with background
- [ ] Color swatches have visible borders
- [ ] Dark theme elements properly contrasted
- [ ] Normal text: 4.5:1 contrast ratio minimum
- [ ] Large text/icons: 3:1 contrast ratio minimum
- [ ] Information not conveyed by color alone

### Accessibility
- [ ] Valid semantic HTML structure
- [ ] Proper heading hierarchy (one h1, logical sequence)
- [ ] Keyboard navigation works (visible focus, logical order)
- [ ] Skip link to main content provided
- [ ] All images have appropriate alt text
- [ ] Media has captions/transcripts
- [ ] Touch targets 44x44px minimum

### Spacing & Grid
- [ ] Using consistent spacing scale (8pt grid recommended)
- [ ] All spacing uses design tokens (not arbitrary values)
- [ ] Typography follows a mathematical scale ratio
- [ ] Elements align to pixel grid for crisp rendering

### Dieter Rams Principles
- [ ] Every element serves the user's goals (useful)
- [ ] Interface explains itself (understandable)
- [ ] Design doesn't demand unnecessary attention (unobtrusive)
- [ ] No deceptive elements or dark patterns (honest)
- [ ] Attention to every detail (thorough)
- [ ] Only essential elements included (as little design as possible)

### Motion
- [ ] Animations serve purpose (not just decoration)
- [ ] High-impact moments prioritized (page load, key interactions)
- [ ] Only transform/opacity animated for performance
- [ ] `prefers-reduced-motion` media query implemented
- [ ] No content that flashes more than 3 times per second

### Modern CSS (Part 18)
- [ ] Used container queries for component-level responsiveness where appropriate
- [ ] Leveraged `:has()` for parent-aware styling (reducing JavaScript)
- [ ] Considered CSS nesting (max 3 levels depth)
- [ ] Used Popover API for light-dismiss behaviors instead of custom JS

### Performance (Part 19)
- [ ] LCP element identified and optimized (`fetchpriority="high"`, preload)
- [ ] All images have explicit `width`/`height` or `aspect-ratio` (CLS prevention)
- [ ] Font loading uses `font-display: swap` with `size-adjust` fallback
- [ ] Skeleton loaders match exact dimensions of replaced content
- [ ] Only `transform`/`opacity` animated (no layout-triggering properties)
- [ ] Resource hints applied (preload, preconnect, prefetch)

### Dark Mode & Theming (Part 20)
- [ ] System preference detected via `prefers-color-scheme`
- [ ] User override available with three-state toggle (System/Light/Dark)
- [ ] Colors desaturated ~20% for dark mode
- [ ] No pure black backgrounds (use `#121212` or similar)
- [ ] Elevation through surface lightness, not shadows in dark mode
- [ ] `forced-colors` media query handled for Windows High Contrast

### AI Interfaces (Part 21)
- [ ] Streaming content has visible typing indicator and auto-scroll
- [ ] AI loading states communicate progress phases (not just spinners)
- [ ] Confidence levels visible when AI certainty varies
- [ ] User can cancel, undo, regenerate, and edit AI output
- [ ] Error states offer manual fallback when AI is unavailable

### Interaction Design (Part 22)
- [ ] Every state has a designed view (empty, loading, error, partial, complete)
- [ ] Gestures have non-gesture alternatives for accessibility
- [ ] Progressive disclosure used for complex features
- [ ] State transitions animated smoothly

### Data Visualization (Part 23)
- [ ] Charts have text alternatives for screen readers
- [ ] Color is not the only way to distinguish data series
- [ ] Tables have sticky headers and clear sort indicators
- [ ] Real-time data batched to prevent visual noise

### Typography (Part 24)
- [ ] Font sizes use `clamp()` for fluid scaling
- [ ] Line length constrained to 45-75 characters
- [ ] `text-wrap: balance` applied to headings
- [ ] Tabular numbers used for data columns

### Images (Part 25)
- [ ] Images served in AVIF/WebP with JPEG fallback
- [ ] LCP image uses `fetchpriority="high"` and is not lazy-loaded
- [ ] All images have `aspect-ratio` or explicit dimensions
- [ ] `sizes` attribute included on responsive images

### Component Architecture (Part 26)
- [ ] Components use design token inheritance
- [ ] Accessibility baked into components (not opt-in)
- [ ] CSS organized with cascade layers

### Forms (Part 27)
- [ ] Error messages are specific and appear inline with the field
- [ ] Validation triggers on blur, not on every keystroke
- [ ] Multi-step forms preserve data on back navigation
- [ ] All inputs use appropriate `autocomplete` attributes

### Internationalization (Part 28)
- [ ] CSS uses logical properties (`margin-inline`, `padding-block`)
- [ ] Layout accommodates 30% text expansion for translation
- [ ] Color semantics tested with target audience

### Cognitive Accessibility (Part 29)
- [ ] Body text at 1.5x line-height minimum, left-aligned
- [ ] One primary action per screen
- [ ] Reduced-motion mode is comprehensive (zero motion option)
- [ ] Focus mode available to reduce visual noise

### Design Tokens (Part 30)
- [ ] Tokens follow three-tier structure (constant → semantic → contextual)
- [ ] Token names describe purpose, not appearance
- [ ] Theme switching uses semantic tokens only (no hardcoded values)

### Cascade Layers (Part 31)
- [ ] CSS organized with `@layer` declarations
- [ ] Third-party CSS wrapped in low-priority layers
- [ ] Component styles don't rely on specificity to override
