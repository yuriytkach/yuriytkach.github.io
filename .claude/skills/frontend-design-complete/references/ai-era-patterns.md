# AI-Era Design Patterns

## Part 21: AI-Era Design Patterns

AI interfaces break traditional UI conventions: response times are unpredictable, outputs vary in length and quality, and confidence is uncertain. These patterns address the unique UX challenges of AI-powered products.

### Streaming UI

Chat and generative interfaces must handle token-by-token output gracefully.

```css
/* Streaming text with typing cursor */
.message.streaming {
  /* Content appended via JavaScript */
}

.message.streaming::after {
  content: '|';
  color: var(--color-interactive);
  animation: blink 1s step-end infinite;
  margin-left: 2px;
}

@keyframes blink {
  50% { opacity: 0; }
}

/* Auto-scroll container */
.chat-messages {
  overflow-y: auto;
  overscroll-behavior: contain;
  scroll-behavior: smooth;
}
```

```javascript
/* Smart auto-scroll: only scroll if user is at bottom */
function shouldAutoScroll(container) {
  const threshold = 100;
  const distanceFromBottom =
    container.scrollHeight - container.scrollTop - container.clientHeight;
  return distanceFromBottom < threshold;
}

/* Pause auto-scroll when user scrolls up to read history */
```

**Key Rule**: Always auto-scroll during streaming if the user is at the bottom. Stop auto-scrolling if they've scrolled up to read history. Show a "scroll to bottom" button when they're not at the latest message.

### AI Loading States

AI loading is different from traditional loading: duration is unpredictable and can range from 1 second to 2 minutes.

```css
/* Phase-based loading indicator */
.ai-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.ai-loading .dots span {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-interactive);
  animation: pulse 1.4s ease-in-out infinite;
}

.ai-loading .dots span:nth-child(2) { animation-delay: 0.2s; }
.ai-loading .dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}

/* Show elapsed time after 3 seconds */
.ai-loading .elapsed {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  opacity: 0;
  animation: fadeIn 0.3s ease forwards 3s;
}
```

```html
<div class="ai-loading">
  <div class="dots"><span></span><span></span><span></span></div>
  <span class="phase">Analyzing your request...</span>
  <span class="elapsed">12s</span>
  <button class="cancel" aria-label="Cancel generation">Stop</button>
</div>
```

**Key Rule**: Skeleton loaders are wrong for AI content because the structure is unknown. Use animated indicators with phase text. Always show a cancel button. Show elapsed time after 3+ seconds.

### Confidence Indicators

When AI certainty varies, make it visible. Users trust AI more when it admits what it doesn't know.

```css
/* Confidence badge */
.confidence {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
}

.confidence--high {
  background: hsl(145, 60%, 90%);
  color: hsl(145, 80%, 25%);
}

.confidence--medium {
  background: hsl(40, 80%, 90%);
  color: hsl(40, 90%, 25%);
}

.confidence--low {
  background: hsl(0, 60%, 92%);
  color: hsl(0, 70%, 30%);
}
```

```html
<!-- Source attribution inline -->
<p>
  The population of Tokyo is approximately 14 million.
  <a href="#source-1" class="source-ref" aria-label="Source 1">[1]</a>
</p>
```

### Explainability & Transparency UX

```html
<!-- Expandable reasoning panel -->
<div class="ai-response">
  <div class="response-content">...</div>
  <details class="reasoning">
    <summary>How AI reached this conclusion</summary>
    <ol class="reasoning-steps">
      <li>Analyzed 3 data sources for population statistics</li>
      <li>Cross-referenced with 2023 census data</li>
      <li>Applied seasonal adjustment factor</li>
    </ol>
  </details>
</div>
```

```css
.reasoning {
  margin-top: var(--space-3);
  padding: var(--space-3);
  background: var(--surface-1);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}

.reasoning summary {
  cursor: pointer;
  color: var(--text-secondary);
  font-weight: 500;
}

.reasoning summary:hover {
  color: var(--text-primary);
}
```

### Human-in-the-Loop Controls

AI output should be editable, not read-only. Users need to correct, refine, and direct.

```css
/* Action bar for AI responses */
.response-actions {
  display: flex;
  gap: 4px;
  padding-top: var(--space-2);
  border-top: 1px solid var(--border);
  margin-top: var(--space-3);
}

.response-actions button {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.response-actions button:hover {
  background: var(--surface-1);
  color: var(--text-primary);
}
```

```html
<div class="response-actions">
  <button aria-label="Copy response"><svg>...</svg> Copy</button>
  <button aria-label="Edit response"><svg>...</svg> Edit</button>
  <button aria-label="Regenerate response"><svg>...</svg> Regenerate</button>
  <button aria-label="Report issue"><svg>...</svg> Report</button>
  <div class="feedback" role="group" aria-label="Rate response">
    <button aria-label="Good response"><svg>...</svg></button>
    <button aria-label="Bad response"><svg>...</svg></button>
  </div>
</div>
```

### Error Handling for AI

AI failures need different patterns than traditional errors because users need manual fallback paths.

```html
<div class="ai-error" role="alert">
  <div class="error-icon"><!-- warning icon --></div>
  <div class="error-content">
    <p class="error-title">AI couldn't complete this request</p>
    <p class="error-detail">The model is temporarily overloaded. Your input has been saved.</p>
  </div>
  <div class="error-actions">
    <button class="retry">Try again</button>
    <button class="manual-fallback">Do it manually</button>
  </div>
</div>
```

Design principles for AI errors:
- **Explain what happened** in plain language (not error codes)
- **Preserve user input** so they don't have to re-type
- **Offer retry** with a single click
- **Provide manual fallback** so the user isn't stuck
- **Show partial results** if the AI got partway through

### User Control Over AI

```html
<!-- Settings that respect user agency -->
<div class="ai-settings">
  <label>
    Response length
    <select>
      <option>Concise</option>
      <option>Balanced</option>
      <option>Detailed</option>
    </select>
  </label>

  <label>
    <input type="checkbox" checked>
    Show confidence indicators
  </label>

  <label>
    <input type="checkbox" checked>
    Show reasoning steps
  </label>

  <button class="clear-context">Clear conversation history</button>
</div>
```

**Key Rule**: User control > perceived AI capability. Explicit controls and predictability matter more than hidden automation. Always let users stop, undo, regenerate, and edit AI output.

### AI Interface Quick Reference

| Pattern | Use When | Anti-Pattern |
|---------|----------|--------------|
| Streaming with cursor | Real-time text generation | Waiting for full response then dumping it |
| Phase-based loading | AI processing > 1 second | Generic spinner with no context |
| Confidence indicators | Output certainty varies | Presenting everything with equal authority |
| Expandable reasoning | Complex multi-step AI decisions | Black-box output with no explanation |
| Response action bar | Users need to act on AI output | Read-only AI responses |
| Manual fallback | AI unavailable or fails | Dead-end error states |

---


