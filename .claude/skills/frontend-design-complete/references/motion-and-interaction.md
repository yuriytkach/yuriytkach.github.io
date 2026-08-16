# Motion & Advanced Interaction Design

## Part 8: Motion Design Principles

Create intentional, impactful animations that enhance rather than distract.

### High-Impact Moments

Focus animation budget on key moments:

```css
/* Page load - staggered reveals */
.hero-content > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease-out forwards;
}

.hero-content > *:nth-child(1) { animation-delay: 0ms; }
.hero-content > *:nth-child(2) { animation-delay: 100ms; }
.hero-content > *:nth-child(3) { animation-delay: 200ms; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Scroll-Triggered Effects

```css
/* Use Intersection Observer to add class when visible */
.section {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.section.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Hover States That Surprise

```css
/* Unexpected but delightful */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px) rotate(-1deg);
  box-shadow: 8px 8px 0 var(--color-accent);
}

/* Or for brutalist/neubrutalist */
.card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 4px 4px 0 #000;
}
```

### Performance Considerations

```css
/* Only animate transform and opacity for smooth 60fps */
.animate-safe {
  transition: transform 0.3s ease, opacity 0.3s ease;
  /* Avoid: width, height, margin, padding, top, left */
}

/* Use will-change sparingly for heavy animations */
.heavy-animation {
  will-change: transform;
}

/* Remove will-change after animation completes */
```

**Modern CSS Alternatives**: Scroll-driven animations (Part 18) can replace JavaScript Intersection Observer patterns. View Transitions API (Part 18) provides native page transition support. For AI-specific loading and streaming animations, see Part 21.

---


## Part 22: Advanced Interaction Design

Good interaction design makes an interface feel alive and responsive. Every component has multiple states, and transitions between them matter as much as the states themselves.

### Micro-Interaction Taxonomy

Micro-interactions follow a four-part structure: Trigger → Rules → Feedback → Loops/Modes.

```css
/* Button with multi-state feedback */
.button {
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

/* Hover: anticipation */
.button:hover {
  transform: translateY(-1px);
  box-shadow: var(--elevation-2);
}

/* Active: confirmation */
.button:active {
  transform: translateY(0) scale(0.98);
  box-shadow: none;
}

/* Loading: system status */
.button[aria-busy="true"] {
  pointer-events: none;
  opacity: 0.7;
}

.button[aria-busy="true"]::after {
  content: '';
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin-left: 8px;
}

/* Success: completion feedback */
.button.success {
  background: var(--color-success);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

**Key Rule**: Every interactive element needs at least four visual states: default, hover, active/pressed, and disabled. Important actions also need loading and success/error states.

### Gesture Design

Design for touch interfaces with gesture alternatives for keyboard/mouse users.

| Gesture | Common Use | Non-Gesture Alternative |
|---------|-----------|------------------------|
| Swipe horizontal | Dismiss, navigate | Delete button, back/forward buttons |
| Swipe vertical | Pull-to-refresh, reveal | Refresh button, scroll to load |
| Long-press | Context menu, selection | Right-click, checkbox selection |
| Pinch | Zoom | Zoom buttons, slider |
| Double-tap | Quick action, zoom | Button, toggle |

**Key Rule**: Every gesture must have a visible, tappable alternative. Gestures are shortcuts, not the only path. Include onboarding hints for discoverable gestures.

### Progressive Disclosure

Show only essential options first. Reveal complexity on demand.

```html
<!-- Zero-JS progressive disclosure with details/summary -->
<details>
  <summary>Advanced settings</summary>
  <div class="advanced-options">
    <!-- Complex options hidden until requested -->
  </div>
</details>
```

```css
details .advanced-options {
  padding-top: var(--space-3);
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

summary {
  cursor: pointer;
  color: var(--color-interactive);
  font-weight: 500;
  list-style: none;
}

summary::before {
  content: '+ ';
}

details[open] summary::before {
  content: '− ';
}
```

### State-Based Design

Every component exists in multiple states. Design all of them intentionally.

| State | Design Treatment | Example |
|-------|-----------------|---------|
| Empty | Illustration + CTA + explanation | "No messages yet. Start a conversation." |
| Loading | Skeleton matching content dimensions | Shimmer placeholders |
| Partial | Show what's available + loading indicator | 3 of 10 items loaded |
| Complete | Full content with actions | List with items |
| Error | Explain problem + retry action + manual fallback | "Couldn't load. Retry / Go to settings" |
| Offline | Cached content + offline indicator | "You're offline. Showing saved data." |

```css
/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-4);
  text-align: center;
  color: var(--text-secondary);
}

.empty-state .illustration {
  width: 200px;
  height: 200px;
  margin-bottom: var(--space-4);
  opacity: 0.6;
}

.empty-state .title {
  font-size: var(--text-lg);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.empty-state .cta {
  margin-top: var(--space-4);
}
```

**Key Rule**: Empty states and error states are design opportunities, not afterthoughts. A well-designed empty state guides users toward their first action.

### State Transitions

Animate between states to help users understand what changed.

```css
/* Smooth transition from loading to populated */
.content-area {
  transition: opacity 0.3s ease;
}

.content-area[data-state="loading"] {
  opacity: 0.6;
}

.content-area[data-state="complete"] {
  opacity: 1;
}

/* List items enter with stagger */
.list-item {
  opacity: 0;
  transform: translateY(10px);
  animation: enterItem 0.3s ease forwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
.list-item:nth-child(4) { animation-delay: 150ms; }
/* Cap at ~5 staggered items to avoid slow-feeling loads */

@keyframes enterItem {
  to { opacity: 1; transform: translateY(0); }
}
```

### Scroll-Based Storytelling

Use scroll position to drive narrative through content sections.

```css
/* Sticky context retention */
.story-section {
  position: relative;
  min-height: 100vh;
}

.story-section .sticky-context {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.story-section .scroll-content {
  position: relative;
  z-index: 1;
}

/* Parallax done right: subtle, single-axis, respects user preference */
@media (prefers-reduced-motion: no-preference) {
  .parallax-element {
    animation: parallax linear;
    animation-timeline: scroll();
  }

  @keyframes parallax {
    from { transform: translateY(-20px); }
    to { transform: translateY(20px); }
  }
}
```

Cross-reference: Part 18 (Modern CSS) for scroll-driven animation syntax. Part 8 (Motion) for performance rules.

---


