---
name: form-accessibility
description: WCAG 2.2 AA compliance for forms, ARIA patterns, focus management, keyboard navigation, and screen reader support. Use when implementing accessible forms in any framework. The compliance foundation that ensures forms work for everyone.
---

# Form Accessibility

WCAG 2.2 AA compliance patterns for forms. Ensures forms work for keyboard users, screen reader users, and users with cognitive or motor disabilities.

## Quick Start

```tsx
// Accessible form field pattern
<div className="form-field">
  {/* 1. Visible label (never placeholder-only) */}
  <label htmlFor="email">
    Email
    <span className="required" aria-hidden="true">*</span>
  </label>
  
  {/* 2. Hint text (separate from label) */}
  <span id="email-hint" className="hint">
    We'll send your confirmation here
  </span>
  
  {/* 3. Input with full ARIA binding */}
  <input
    id="email"
    type="email"
    autoComplete="email"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby={hasError ? "email-error email-hint" : "email-hint"}
  />
  
  {/* 4. Error message (announced by screen readers) */}
  {hasError && (
    <span id="email-error" className="error" role="alert">
      Please enter a valid email address
    </span>
  )}
</div>
```

## WCAG 2.2 Form Requirements

### Critical Criteria

| Criterion | Level | Requirement | Implementation |
|-----------|-------|-------------|----------------|
| 1.3.1 Info & Relationships | A | Structure conveyed programmatically | `<label>`, `<fieldset>`, `aria-describedby` |
| 1.3.5 Identify Input Purpose | AA | Input purpose identifiable | `autocomplete` attributes |
| 2.1.1 Keyboard | A | All functionality via keyboard | Tab order, focus management |
| 2.4.6 Headings & Labels | AA | Labels describe purpose | Descriptive, visible labels |
| 2.4.11 Focus Not Obscured | AA | Focus not hidden by other content | Scroll behavior, sticky elements |
| 2.5.8 Target Size | AA | 24×24px minimum touch target | Button/input sizing |
| 3.3.1 Error Identification | A | Errors identified and described | `aria-invalid`, error messages |
| 3.3.2 Labels or Instructions | A | Labels provided | Visible labels, not just placeholders |
| 3.3.3 Error Suggestion | AA | Suggestions for fixing errors | Actionable error messages |
| 3.3.7 Redundant Entry | A | Don't re-ask for info already provided | Form state management |
| 3.3.8 Accessible Authentication | AA | No cognitive function tests | No CAPTCHAs requiring text recognition |

### New in WCAG 2.2 (October 2023)

**2.4.11 Focus Not Obscured (AA)**
```css
/* Ensure focus is never hidden by sticky headers */
.sticky-header {
  position: sticky;
  top: 0;
}

input:focus {
  /* Browser should scroll input into view above sticky elements */
  scroll-margin-top: 80px; /* Height of sticky header */
}
```

**2.5.8 Target Size (AA)**
```css
/* Minimum 24×24px touch targets */
button,
input[type="submit"],
input[type="checkbox"],
input[type="radio"] {
  min-width: 24px;
  min-height: 24px;
}

/* Better: 44×44px for comfortable touch */
.touch-friendly {
  min-width: 44px;
  min-height: 44px;
}
```

**3.3.7 Redundant Entry (A)**
```tsx
// ❌ BAD: Asking for email twice
<input name="email" />
<input name="confirmEmail" />

// ✅ GOOD: Ask once, show confirmation
<input name="email" />
<p>Confirmation will be sent to: {email}</p>
```

**3.3.8 Accessible Authentication (AA)**
```tsx
// ❌ BAD: CAPTCHA requiring text recognition
<img src="captcha.png" alt="Enter the text shown" />

// ✅ GOOD: Alternative verification methods
<button type="button" onClick={sendVerificationEmail}>
  Send verification code to email
</button>
```

## ARIA Patterns

### Error Message Binding

```tsx
// Pattern: aria-describedby links input to error
<input
  id="email"
  aria-invalid={hasError ? "true" : "false"}
  aria-describedby={hasError ? "email-error" : undefined}
/>

{hasError && (
  <span id="email-error" role="alert">
    {errorMessage}
  </span>
)}
```

### Multiple Descriptions

```tsx
// Pattern: Combine hint + error in aria-describedby
<input
  id="password"
  aria-describedby={[
    "password-hint",
    hasError && "password-error"
  ].filter(Boolean).join(" ")}
/>

<span id="password-hint">Must be at least 8 characters</span>
{hasError && <span id="password-error" role="alert">{error}</span>}
```

### Required Fields

```tsx
// Pattern: Announce required status
<label htmlFor="name">
  Name
  <span className="required" aria-hidden="true">*</span>
  {/* Visual indicator hidden from SR, aria-required announces it */}
</label>

<input
  id="name"
  aria-required="true"
/>

// Alternative: Required in label (simpler)
<label htmlFor="name">Name (required)</label>
<input id="name" required />
```

### Field Groups

```tsx
// Pattern: fieldset + legend for related fields
<fieldset>
  <legend>Shipping Address</legend>
  
  <label htmlFor="street">Street</label>
  <input id="street" autoComplete="street-address" />
  
  <label htmlFor="city">City</label>
  <input id="city" autoComplete="address-level2" />
</fieldset>
```

### Radio/Checkbox Groups

```tsx
// Pattern: fieldset groups options, legend is the question
<fieldset>
  <legend>Preferred contact method</legend>
  
  <label>
    <input type="radio" name="contact" value="email" />
    Email
  </label>
  
  <label>
    <input type="radio" name="contact" value="phone" />
    Phone
  </label>
</fieldset>
```

## Focus Management

### Focus on First Error

```tsx
// On form submit with errors, focus first invalid field
function handleSubmit(e: FormEvent) {
  e.preventDefault();
  
  const firstError = formRef.current?.querySelector('[aria-invalid="true"]');
  if (firstError) {
    (firstError as HTMLElement).focus();
    return;
  }
  
  // Submit if valid
  submitForm();
}
```

### Focus on Step Change (Multi-step)

```tsx
// Move focus to step heading when changing steps
function goToStep(stepNumber: number) {
  setCurrentStep(stepNumber);
  
  // Wait for render, then focus
  requestAnimationFrame(() => {
    const heading = document.getElementById(`step-${stepNumber}-heading`);
    heading?.focus();
  });
}

// Heading must be focusable
<h2 id="step-2-heading" tabIndex={-1}>Shipping Address</h2>
```

### Skip Links

```tsx
// Allow skipping to form
<a href="#main-form" className="skip-link">
  Skip to form
</a>

<form id="main-form">
  {/* Form content */}
</form>

// CSS for skip link
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Focus Trap (Modals)

```tsx
// Keep focus within modal form
function FocusTrap({ children }) {
  const trapRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const trap = trapRef.current;
    if (!trap) return;
    
    const focusableElements = trap.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
    
    trap.addEventListener('keydown', handleKeyDown);
    firstElement?.focus();
    
    return () => trap.removeEventListener('keydown', handleKeyDown);
  }, []);
  
  return <div ref={trapRef}>{children}</div>;
}
```

## Color & Contrast

### Error States (Colorblind-Safe)

```css
/* ❌ BAD: Color only */
.error {
  border-color: red;
}

/* ✅ GOOD: Color + icon + text */
.field-error {
  border-color: #dc2626;
  border-width: 2px;
}

.field-error::after {
  content: "";
  background-image: url("data:image/svg+xml,..."); /* Error icon */
}

.error-message {
  color: #dc2626;
  font-weight: 500;
}

.error-message::before {
  content: "⚠ "; /* Text indicator */
}
```

### Focus Indicators

```css
/* Focus must have 3:1 contrast ratio */
input:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* For dark backgrounds */
input:focus {
  outline: 2px solid #60a5fa;
  outline-offset: 2px;
}

/* Never remove outline without replacement */
/* ❌ BAD */
input:focus {
  outline: none;
}

/* ✅ GOOD: Custom focus style */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.5);
}
```

### Validation States (Colorblind-Friendly)

```tsx
// Use icons + text, not just color
function ValidationIndicator({ state }: { state: 'valid' | 'invalid' | 'idle' }) {
  if (state === 'idle') return null;
  
  return (
    <span className={`indicator ${state}`} aria-hidden="true">
      {state === 'valid' && '✓'}
      {state === 'invalid' && '✗'}
    </span>
  );
}
```

## Keyboard Navigation

### Tab Order

```tsx
// Natural tab order (no positive tabindex needed)
// ❌ BAD: Manual tab order
<input tabIndex={2} />
<input tabIndex={1} />
<input tabIndex={3} />

// ✅ GOOD: Natural DOM order
<input /> {/* tabIndex implicitly 0 */}
<input />
<input />
```

### Escape Key Handling

```tsx
// Allow Escape to close dropdowns, cancel modals
function Modal({ onClose, children }) {
  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        onClose();
      }
    }
    
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);
  
  return <div role="dialog" aria-modal="true">{children}</div>;
}
```

### Enter to Submit

```tsx
// Forms submit on Enter by default
// For buttons that shouldn't submit:
<button type="button" onClick={handleAction}>
  Add Item
</button>

// For preventing Enter submit on specific fields:
<input
  onKeyDown={(e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      // Do something else
    }
  }}
/>
```

## Live Regions

### Error Announcements

```tsx
// Announce errors when they appear
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {errorCount > 0 && `${errorCount} errors in form`}
</div>

// Or use role="alert" for immediate announcement
{hasError && (
  <span role="alert">{errorMessage}</span>
)}
```

### Loading States

```tsx
// Announce loading state
<button type="submit" disabled={isLoading}>
  {isLoading ? (
    <>
      <span aria-hidden="true">Loading...</span>
      <span className="sr-only">Submitting form, please wait</span>
    </>
  ) : (
    'Submit'
  )}
</button>

// Or use aria-busy
<form aria-busy={isLoading}>
  {/* ... */}
</form>
```

### Success Messages

```tsx
// Announce successful submission
{isSuccess && (
  <div role="status" aria-live="polite">
    Form submitted successfully!
  </div>
)}
```

## Screen Reader Only Content

```css
/* Visually hidden but announced by screen readers */
.sr-only {
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

/* Allow focus for skip links */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

## Testing Accessibility

### Automated Tools

```bash
# axe-core (recommended)
npm install @axe-core/react

# In development
import React from 'react';
import ReactDOM from 'react-dom';
import axe from '@axe-core/react';

if (process.env.NODE_ENV !== 'production') {
  axe(React, ReactDOM, 1000);
}
```

### Manual Testing Checklist

1. **Keyboard only**: Can you complete the form using only Tab, Enter, Space, and Arrow keys?
2. **Screen reader**: Does VoiceOver/NVDA announce labels, errors, and required status?
3. **Zoom 200%**: Is the form usable at 200% browser zoom?
4. **High contrast**: Is everything visible in Windows High Contrast mode?
5. **Focus visible**: Can you always see which element is focused?

### Testing Script

```typescript
// Automated accessibility test
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('form is accessible', async () => {
  const { container } = render(<LoginForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

test('error state is accessible', async () => {
  const { container } = render(<LoginForm />);
  
  // Trigger error
  fireEvent.blur(screen.getByLabelText(/email/i));
  
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## File Structure

```
form-accessibility/
├── SKILL.md
├── references/
│   ├── wcag-2.2-forms.md       # Full WCAG criteria breakdown
│   └── aria-patterns.md        # Complete ARIA reference
└── scripts/
    ├── aria-form-wrapper.tsx   # Automatic ARIA binding
    ├── focus-manager.ts        # Focus trap, error focus
    ├── error-announcer.ts      # Live region management
    └── accessibility-validator.ts  # Runtime a11y checks
```

## Reference

- `references/wcag-2.2-forms.md` — Complete WCAG 2.2 criteria for forms
- `references/aria-patterns.md` — Detailed ARIA implementation patterns
