# Foundations & Design Principles

## Part 6: Design System Principles

Learn from production design systems to create more cohesive, maintainable interfaces.

### Token-Based Design

Use semantic design tokens instead of hardcoded values:

```css
/* Define tokens at root level */
:root {
  /* Primitive tokens — use YOUR brand's values here, not framework
     defaults (#3b82f6 Tailwind blue is itself an AI-slop tell) */
  --color-petrol-500: #1f6f6b;
  --color-ink-900: #16181a;
  --spacing-4: 1rem;

  /* Semantic tokens (reference primitives) */
  --color-primary: var(--color-petrol-500);
  --color-text-primary: var(--color-ink-900);
  --spacing-component-padding: var(--spacing-4);
}

/* Apply semantically */
.button {
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  padding: var(--spacing-component-padding);
}
```

### Typography Scale

Establish a clear type hierarchy (inspired by Material 3):

```css
:root {
  /* Display - Hero headlines */
  --type-display-large: 57px/64px;
  --type-display-medium: 45px/52px;

  /* Headline - Section headers */
  --type-headline-large: 32px/40px;
  --type-headline-medium: 28px/36px;

  /* Title - Card titles, dialogs */
  --type-title-large: 22px/28px;
  --type-title-medium: 16px/24px;

  /* Body - Paragraph text */
  --type-body-large: 16px/24px;
  --type-body-medium: 14px/20px;

  /* Label - Buttons, form labels */
  --type-label-large: 14px/20px;
  --type-label-medium: 12px/16px;
}
```

### Elevation & Depth

Create visual hierarchy through consistent elevation (from Carbon/Material):

```css
:root {
  --elevation-1: 0 1px 2px rgba(0, 0, 0, 0.05);
  --elevation-2: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --elevation-3: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --elevation-4: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

/* Apply based on component importance */
.card { box-shadow: var(--elevation-1); }
.dropdown { box-shadow: var(--elevation-2); }
.modal { box-shadow: var(--elevation-4); }
```

### Density Variants

Support different density contexts (from Carbon):

```css
.component {
  --component-padding: var(--spacing-4);
}

.component--condensed {
  --component-padding: var(--spacing-2);
}

/* Data tables often need condensed density */
.data-table--condensed .table-cell {
  padding: var(--spacing-1) var(--spacing-2);
}
```

### Accessibility Patterns (from Primer)

```css
/* Visually hidden but accessible to screen readers */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focus visible for keyboard navigation */
.interactive:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

For a full three-tier token architecture (constant → semantic → contextual) with multi-theme mapping, see Part 30. For cascade management of token layers, see Part 31.

---


## Part 9: Foundational UX Principles

Master these timeless principles that form the foundation of effective interface design.

### Nielsen's 10 Usability Heuristics

**1. Visibility of System Status**
Keep users informed through appropriate feedback within reasonable time. Show loading states, progress indicators, and confirmation messages.

**2. Match Between System and Real World**
Use familiar language and concepts. Follow real-world conventions; make information appear in natural, logical order.

**3. User Control and Freedom**
Provide clear "emergency exits" - undo, redo, cancel buttons. Users often perform actions by mistake and need escape routes.

**4. Consistency and Standards**
Follow platform conventions. Users shouldn't wonder whether different words, situations, or actions mean the same thing.

**5. Error Prevention**
Design to prevent errors before they occur. Use confirmation dialogs for destructive actions; provide helpful constraints.

**6. Recognition Rather Than Recall**
Make elements, actions, and options visible. Minimize memory load by showing information contextually.

**7. Flexibility and Efficiency of Use**
Offer shortcuts for expert users while keeping the interface simple for novices. Support personalization.

**8. Aesthetic and Minimalist Design**
Every extra unit of information competes with relevant information. Remove elements that don't serve the user's goals.

**9. Help Users Recognize, Diagnose, and Recover from Errors**
Express errors in plain language, precisely indicate the problem, and constructively suggest solutions.

**10. Help and Documentation**
Provide searchable, task-focused documentation accessible in context when users need it.

### Key Laws of UX

**Cognitive & Attention**
- **Hick's Law**: Decision time increases with choice quantity and complexity. Minimize options to accelerate decisions.
- **Miller's Law**: Working memory holds ~7±2 items. Present information in groups of 5-9 maximum.
- **Cognitive Load**: Simplify tasks to reduce mental demand. Users have limited processing capacity.

**Visual Perception (Gestalt)**
- **Law of Proximity**: Objects near each other appear grouped. Position related items close together.
- **Law of Similarity**: Similar elements appear unified. Use consistent styling to show relationships.
- **Law of Common Region**: Boundaries create perceived grouping. Use borders/backgrounds to organize.

**Interaction**
- **Fitts's Law**: Target acquisition time depends on distance and size. Make clickable areas appropriately sized.
- **Doherty Threshold**: Response times under 400ms improve productivity. Optimize for perceived speed.
- **Jakob's Law**: Users prefer familiar patterns. Match conventions from platforms users already know.

**Memory & Experience**
- **Peak-End Rule**: Users judge experiences by peak moments and conclusions, not averages. Design memorable highs and strong endings.
- **Von Restorff Effect**: Distinctive items stand out in memory. Highlight important elements through differentiation.
- **Serial Position Effect**: Users remember first and last items best. Prioritize critical information at boundaries.

**Design Philosophy**
- **Aesthetic-Usability Effect**: Beautiful design is perceived as more usable. Visual appeal enhances perceived functionality.
- **Occam's Razor**: Prefer simpler solutions with fewer assumptions over complex ones.
- **Tesler's Law**: All systems contain irreducible complexity. Distribute it appropriately between system and user.
- **Pareto Principle**: 80% of effects stem from 20% of causes. Focus effort on high-impact elements.

---


## Part 10: Humane Design Principles

Design ethically by prioritizing user well-being over engagement metrics.

### The 7 Principles

**1. Empowering**
Prioritize value delivered to users over revenue generation.
- Give users authority over algorithms shaping their experience
- Grant control over personal data and identity management
- Technology should strengthen abilities without intruding unnecessarily
- Maintain user understanding and trust in AI decisions (human in the loop)

**2. Finite**
Respect users' time and attention as limited resources.
- Show "all caught up" indicators when content is exhausted
- Replace infinite scroll with explicit "load more" controls
- Disable autoplay; require conscious user action
- Design experiences with clear endings, not endless engagement

**3. Inclusive**
Enable and draw on the full range of human diversity.
- Build diverse teams to create broader perspectives
- Design for disabilities first; solutions often benefit everyone
- Provide control over accessibility preferences (zoom, contrast, animations)
- Don't disable platform features users depend on

**4. Intentional**
Employ friction to prevent misuse and encourage healthier habits.
- Use confirmation dialogs to minimize mistakes
- Embrace positive friction for more deliberate choices
- Provide mechanisms for users to manage consumption patterns
- Prioritize long-term user benefit over immediate engagement

**5. Respectful**
Safeguard people's time, attention, and digital well-being.
- Align notification delivery with actual urgency
- Allow personalization of notification sources, timing, formats
- Include full content in notifications rather than requiring app visits
- Design technology that adapts to user context

**6. Transparent**
Be clear about intentions, honest in actions, free of dark patterns.
- Clearly explain what users commit to when adopting products
- Articulate what data is gathered and why
- Allow users to view collected information
- Provide the right to be forgotten with easy deletion
- Avoid misdirection; separate ads from content clearly
- Make unsubscribe and exit options easily discoverable

**7. Resilient**
Ensure systems remain stable, reliable, and sustainable.
- Design for long-term user relationships, not exploitation
- Build systems that degrade gracefully
- Support user autonomy rather than dependency

### Anti-Patterns to Avoid

These manipulative patterns violate humane design principles:

- **Infinite scroll** without endpoints (violates Finite)
- **Autoplay** that consumes attention without consent (violates Respectful)
- **Dark patterns** that trick users into actions (violates Transparent)
- **Notification spam** designed to maximize engagement (violates Respectful)
- **Hidden unsubscribe** options (violates Transparent)
- **Confirmation shaming** ("No, I don't want to save money") (violates Respectful)
- **Forced continuity** with difficult cancellation (violates Empowering)

---


## Part 12: Dieter Rams' 10 Principles for Good Design

These timeless principles from industrial designer Dieter Rams apply directly to interface design:

1. **Good design is innovative** - Push boundaries; don't settle for conventional solutions
2. **Good design makes a product useful** - Every element must serve the user's goals
3. **Good design is aesthetic** - Visual quality is integral, not superficial
4. **Good design makes a product understandable** - The interface explains itself
5. **Good design is unobtrusive** - Serve the user's purpose without demanding attention
6. **Good design is honest** - Don't pretend to be more than you are; no dark patterns
7. **Good design is long-lasting** - Avoid trendy elements that age quickly
8. **Good design is thorough down to the last detail** - Every pixel matters
9. **Good design is environmentally-friendly** - Optimize performance; respect resources
10. **Good design is as little design as possible** - "Less, but better" - only the essential

---


## Part 16: Settings Philosophy

From Linear: "Settings are not a design failure."

### Key Principles

1. **Distinguish preferences from failures** - Some settings address legitimate individual differences, not poor defaults
2. **Settings as onboarding** - Use settings to educate users about capabilities
3. **Emotional connection through details** - Customization creates user attachment
4. **Respect habits** - "Create products that fit into people's lives, not the other way around"

### When to Add Settings

- User habits genuinely vary (keyboard shortcuts, themes)
- Platform conventions differ (Mac vs Windows)
- Accessibility needs vary (motion, contrast)
- Power users need efficiency (density, defaults)

### When NOT to Add Settings

- You're avoiding a design decision
- The "right" answer is knowable through research
- Adding complexity without clear user benefit

---


