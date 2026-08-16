# Data Visualization & Dashboard Design

## Part 23: Data Visualization & Dashboard Design

Data-heavy interfaces require different design principles than marketing pages. Prioritize clarity, information density, and accurate representation.

### Tufte's Core Principles

Edward Tufte's foundational rules for honest, effective data graphics:

1. **Maximize data-ink ratio**: every pixel of ink should present data or aid comprehension of data. If a visual element doesn't encode data, remove it.
2. **Eliminate chart junk**: decorative gridlines, 3D effects, excessive legends, gradient fills, and ornamental elements that don't serve the data.
3. **Small multiples**: repeat the same chart type with different data slices for easy comparison. Faster to read than one complex chart.
4. **Graphical integrity**: represent quantities honestly. No truncated axes, no 3D distortion, no area tricks.

**Key Rule**: "If a visual element doesn't encode data, remove it." This applies to gridlines, backgrounds, borders, and decorative elements on charts.

### Information Density

```css
/* Sparkline: word-sized data graphic inline with text */
.sparkline {
  display: inline-block;
  width: 60px;
  height: 16px;
  vertical-align: middle;
}

.sparkline svg {
  width: 100%;
  height: 100%;
}

/* High-density table: condensed for scanning */
.data-table--dense th,
.data-table--dense td {
  padding: 4px 8px;
  font-size: var(--text-sm);
}

/* Monospace numbers for column alignment */
.data-table td.numeric {
  font-variant-numeric: tabular-nums;
  text-align: right;
  font-family: var(--font-mono);
}
```

### Dashboard Layout Patterns

```css
/* KPI bar: key metrics at top */
.kpi-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-3);
  padding: var(--space-3);
}

.kpi-card {
  padding: var(--space-3);
  background: var(--surface-1);
  border-radius: var(--radius-md);
}

.kpi-card .label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-1);
}

.kpi-card .value {
  font-size: var(--text-2xl);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.kpi-card .trend {
  font-size: var(--text-sm);
  margin-top: var(--space-1);
}

.kpi-card .trend--up { color: var(--color-success); }
.kpi-card .trend--down { color: var(--color-error); }

/* Grid dashboard with priority-based sizing */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-auto-rows: minmax(200px, auto);
  gap: var(--space-3);
}

.widget--primary { grid-column: span 8; grid-row: span 2; }
.widget--secondary { grid-column: span 4; }
.widget--full { grid-column: span 12; }

/* Mobile: single column, priority ordering */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .widget--primary,
  .widget--secondary,
  .widget--full {
    grid-column: span 1;
    grid-row: span 1;
  }
}
```

### Chart Accessibility

```html
<!-- Accessible chart container -->
<figure role="img" aria-label="Monthly revenue for 2025, showing growth from $2M in January to $3.4M in December">
  <div class="chart-container">
    <!-- Chart rendered here (SVG, Canvas, etc.) -->
  </div>
  <figcaption>Monthly Revenue 2025</figcaption>
</figure>

<!-- Provide data table fallback for screen readers -->
<details class="sr-data-table">
  <summary class="visually-hidden">View data as table</summary>
  <table>
    <caption>Monthly Revenue 2025</caption>
    <thead><tr><th>Month</th><th>Revenue</th></tr></thead>
    <tbody>
      <tr><td>January</td><td>$2,000,000</td></tr>
      <!-- ... -->
    </tbody>
  </table>
</details>
```

- Don't rely on color alone to distinguish data series: add patterns, labels, or distinct shapes
- Ensure keyboard navigable data points for interactive charts
- Provide `aria-label` or linked description for every chart

### Real-Time Data Display

```css
/* Animated counter for live metrics */
.live-metric {
  font-variant-numeric: tabular-nums;
  transition: color 0.3s ease;
}

/* Flash on value change */
.live-metric.updated {
  animation: valueFlash 0.6s ease;
}

@keyframes valueFlash {
  0% { background: var(--color-interactive-subtle); }
  100% { background: transparent; }
}

/* Stale data indicator */
.data-timestamp {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}

.data-timestamp.stale {
  color: var(--color-warning);
}

.data-timestamp.stale::before {
  content: '⚠ ';
}
```

**Key Rule**: Batch real-time updates to prevent visual noise. Update at most every 1-2 seconds for numbers, 5-10 seconds for charts. Always show the timestamp of the last update.

### Table Design

```css
/* Well-structured data table */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--surface-0);
}

.data-table th {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 2px solid var(--border);
  white-space: nowrap;
  user-select: none;
}

/* Sortable column indicator */
.data-table th[aria-sort] {
  cursor: pointer;
}

.data-table th[aria-sort="ascending"]::after {
  content: ' ↑';
}

.data-table th[aria-sort="descending"]::after {
  content: ' ↓';
}

.data-table td {
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--border);
  font-size: var(--text-sm);
}

/* Subtle zebra striping */
.data-table tbody tr:nth-child(even) {
  background: var(--surface-1);
}

/* Row hover */
.data-table tbody tr:hover {
  background: var(--color-interactive-subtle);
}

/* Sticky first column for wide tables */
@media (max-width: 768px) {
  .data-table-wrapper {
    overflow-x: auto;
  }

  .data-table th:first-child,
  .data-table td:first-child {
    position: sticky;
    left: 0;
    background: var(--surface-0);
    z-index: 1;
  }
}
```

Use pagination for data tables (not infinite scroll). Virtual scrolling only for datasets > 1,000 rows.

### Color in Data Visualization

| Palette Type | Use Case | Example |
|-------------|----------|---------|
| Sequential | Continuous data (0-100) | Light blue → dark blue |
| Diverging | Positive/negative around center | Red ← neutral → green |
| Categorical | Distinct groups (max 8-10) | Distinct hues per category |

Always test charts with colorblind simulators (deuteranopia, protanopia, tritanopia). Cross-reference: Color Palette skill for generation tools.

---


