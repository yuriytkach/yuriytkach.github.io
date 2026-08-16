# Component Architecture Patterns

## Part 26: Component Architecture Patterns

Structure components for reuse, composition, and maintainability. Design systems need architectural patterns, not just visual tokens.

### Headless UI Pattern

Separate behavior from presentation. Build logic once, style infinitely.

```jsx
/* Headless hook: manages dropdown behavior */
function useDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef(null);
  const menuRef = useRef(null);

  /* Keyboard navigation, focus management, outside click */
  useEffect(() => {
    if (!isOpen) return;
    const handleEscape = (e) => { if (e.key === 'Escape') setIsOpen(false); };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  return {
    isOpen,
    toggle: () => setIsOpen(!isOpen),
    close: () => setIsOpen(false),
    triggerProps: { ref: triggerRef, onClick: () => setIsOpen(!isOpen), 'aria-expanded': isOpen },
    menuProps: { ref: menuRef, role: 'menu', hidden: !isOpen },
  };
}

/* Styled implementation: your design system's look */
function StyledDropdown({ items }) {
  const { isOpen, triggerProps, menuProps, close } = useDropdown();
  return (
    <div className="dropdown">
      <button className="dropdown-trigger" {...triggerProps}>Options</button>
      <ul className="dropdown-menu" {...menuProps}>
        {items.map(item => (
          <li key={item.id} role="menuitem">
            <button onClick={() => { item.action(); close(); }}>{item.label}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Key Rule**: Build behavior once, style infinitely. Headless components handle accessibility (keyboard nav, focus management, ARIA) so every styled implementation gets it for free.

### Compound Components

Components that work together with shared implicit state.

```jsx
/* Tab component API: compound structure */
<Tabs defaultTab="overview">
  <TabList>
    <Tab id="overview">Overview</Tab>
    <Tab id="features">Features</Tab>
    <Tab id="pricing">Pricing</Tab>
  </TabList>
  <TabPanel id="overview">...</TabPanel>
  <TabPanel id="features">...</TabPanel>
  <TabPanel id="pricing">...</TabPanel>
</Tabs>
```

Use compound components when: multiple sub-elements share state, the structure is stable, and customization is at the content level (not the structural level).

### CSS Cascade Layers for Components

```css
/* Component library in its own layer */
@layer components {
  .button {
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    font-weight: 500;
  }

  .card {
    padding: var(--space-4);
    background: var(--surface-1);
    border-radius: var(--radius-lg);
  }
}

/* Consumer overrides always win without specificity battles */
@layer overrides {
  .button.custom-cta {
    border-radius: 0;
    text-transform: uppercase;
  }
}
```

Cross-reference: Part 31 (CSS Cascade Layers) for full layer architecture.

### Design Token Inheritance

Components inherit tokens from their context through CSS custom property scoping.

```css
/* Base component tokens */
.card {
  --card-padding: var(--space-4);
  --card-bg: var(--surface-1);
  padding: var(--card-padding);
  background: var(--card-bg);
}

/* Context-scoped overrides */
.hero .card {
  --card-padding: var(--space-6);
  --card-bg: var(--surface-2);
}

.sidebar .card {
  --card-padding: var(--space-3);
}

/* Component respects context without knowing about it */
```

Cross-reference: Part 30 (Design Token Architecture) for the full three-tier system.

### Component API Principles

| Principle | Good API | Bad API |
|-----------|----------|---------|
| Composition over configuration | `<Card><CardHeader/><CardBody/></Card>` | `<Card title="..." body="..." headerIcon="...">`|
| Sensible defaults | `<Button>Label</Button>` renders primary | Every prop required |
| Consistent naming | `variant`, `size` across all components | `type`, `kind`, `style`, `mode` mixed |
| Accessibility built-in | ARIA roles auto-applied | Requires manual aria props |
| Style escape hatches | `className` or `style` prop available | No way to customize |

---


