# Forms: Consistency & Advanced Design

## Part 3: Form Element Consistency

### Always Style as a Group

**Problem**: Styling only `.input` leaves `.select` and `.textarea` unstyled.

```css
/* WRONG - Only targets input */
.style-brutalist .input {
  border: 2px solid var(--border);
  border-radius: 0;
}

/* CORRECT - Targets all form fields */
.style-brutalist .input,
.style-brutalist .select,
.style-brutalist .textarea {
  border: 2px solid var(--border);
  border-radius: 0;
}
```

### Textarea Border Radius Exceptions

Pill-shaped inputs (border-radius: 100px) look wrong on textareas:

```css
.style-kawaii .input,
.style-kawaii .select {
  border-radius: 100px;
}

/* Textarea needs smaller radius */
.style-kawaii .textarea {
  border-radius: 20px;
}
```

### Dropdown Option Styling

`<option>` elements can't inherit backdrop-filter or complex backgrounds:

```css
.style-glassmorphism .select {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
}

/* Options need solid backgrounds */
.style-glassmorphism .select option {
  background: #1a1a2e;
  color: white;
}
```

### Transparent Border Styles (Neomorphism, Claymorphism)

**Problem**: Styles with `border: transparent` make form controls invisible.

```css
/* These styles use transparent borders */
.style-neomorphism .radio-mark,
.style-claymorphism .radio-mark {
  border: 2px solid #B8BEC7;  /* Add visible border */
  background: var(--bg-primary);
  box-shadow: inset 2px 2px 4px rgba(163,177,198,0.3),
              inset -2px -2px 4px rgba(255,255,255,0.8);
}
```

---


## Part 27: Advanced Form Design

Forms are where design meets user patience. Every friction point costs conversions.

### Error State Best Practices

```css
/* Inline error: validate on blur, not on every keystroke */
.form-group.has-error .input {
  border-color: var(--color-error);
  box-shadow: 0 0 0 3px rgba(var(--color-error-rgb), 0.15);
}

.form-group .error-message {
  display: none;
  font-size: var(--text-sm);
  color: var(--color-error);
  margin-top: var(--space-1);
}

.form-group.has-error .error-message {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Use :user-invalid for CSS-only validation styling */
/* Only shows error AFTER user has interacted with the field */
input:user-invalid {
  border-color: var(--color-error);
}

input:user-invalid + .error-message {
  display: block;
}

input:user-valid {
  border-color: var(--color-success);
}
```

```html
<!-- Error associated with input via aria-describedby -->
<div class="form-group">
  <label for="email">Email</label>
  <input id="email" type="email" required
         aria-describedby="email-error" aria-invalid="true">
  <p id="email-error" class="error-message" role="alert">
    <svg aria-hidden="true"><!-- error icon --></svg>
    Please enter a valid email (e.g., name@company.com)
  </p>
</div>
```

**Key Rule**: Error messages must be specific ("Password must include a number") not generic ("Invalid password"). Show errors on blur, not on every keystroke. Never show errors before the user has interacted with a field.

### Progressive Enhancement

Start with native HTML validation. Layer JavaScript on top for better UX.

```html
<!-- HTML-first: works without JavaScript -->
<form method="POST" action="/submit">
  <input type="email" required autocomplete="email"
         pattern="[^@]+@[^@]+\.[^@]+" minlength="5">
  <input type="password" required minlength="8"
         autocomplete="new-password">
  <button type="submit">Sign up</button>
</form>
```

```javascript
/* JavaScript enhances the form, doesn't replace native validation */
const form = document.querySelector('form');

/* Only add novalidate when JS is available */
form.setAttribute('novalidate', '');

form.addEventListener('submit', (e) => {
  /* Custom validation UX with better error messages */
  if (!form.checkValidity()) {
    e.preventDefault();
    showCustomErrors(form);
  }
});
```

### Form Accessibility Deep-Dive

```html
<!-- Group related inputs with fieldset and legend -->
<fieldset>
  <legend>Shipping address</legend>

  <div class="form-group">
    <label for="street">Street address</label>
    <input id="street" type="text" autocomplete="street-address" required>
  </div>

  <div class="form-row">
    <div class="form-group">
      <label for="city">City</label>
      <input id="city" type="text" autocomplete="address-level2" required>
    </div>
    <div class="form-group">
      <label for="zip">ZIP code</label>
      <input id="zip" type="text" autocomplete="postal-code"
             inputmode="numeric" pattern="[0-9]*" required>
    </div>
  </div>
</fieldset>

<!-- Required field indicator -->
<label for="name">
  Full name <span class="required" aria-label="required">*</span>
</label>
```

Key attributes:
- `autocomplete`: helps browsers and password managers fill fields correctly
- `inputmode="numeric"`: shows number keyboard on mobile for non-number inputs (ZIP, credit card)
- `aria-describedby`: links error messages and help text to inputs
- `aria-invalid`: announces error state to screen readers

### Multi-Step Form Patterns

```css
/* Step indicator */
.step-indicator {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
}

.step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.step.active {
  color: var(--color-interactive);
  font-weight: 600;
}

.step.completed {
  color: var(--color-success);
}

.step .number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid currentColor;
  font-size: var(--text-xs);
  font-weight: 700;
}

.step.completed .number::after {
  content: '✓';
}

.step-connector {
  flex: 1;
  height: 2px;
  background: var(--border);
}

.step-connector.completed {
  background: var(--color-success);
}
```

Form principles:
- Validate each step before allowing advancement
- Preserve data on back navigation (never lose user input)
- Show a summary/review step before final submission
- Single-column forms convert better than multi-column
- Labels above inputs (not beside) for mobile and faster scanning

Cross-reference: Part 3 (Form Element Consistency) for styling rules.

---


