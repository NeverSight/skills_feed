---
name: visual-overlay
description: |
  Add visual animations (cursor, typing, click effects) to AgentPulse-enabled React apps.
  Use when: showing users what AI is doing, adding visual feedback for agent actions,
  configuring element targeting for animations.
license: MIT
compatibility: React >=18 with AgentPulse installed.
metadata:
  author: agentpulse
  version: "1.0"
allowed-tools: Read Write Edit Glob
---

# Visual Overlay for AgentPulse

Add animated cursor, typing, and click effects to show users what the AI agent is doing.

## Quick Start

Add `VisualOverlay` inside your `AgentPulseProvider`:

```tsx
import { AgentPulseProvider, VisualOverlay } from 'agentpulse';

function App() {
  return (
    <AgentPulseProvider endpoint="ws://localhost:3100/ws">
      <VisualOverlay />
      <MyApp />
    </AgentPulseProvider>
  );
}
```

When an AI agent calls `expose_set` or `expose_call`, users see:
- Animated cursor moving to the target element
- Character-by-character typing for text inputs
- Click ripple effects for button actions

## Configuration

```tsx
<VisualOverlay
  enabled={true}           // Master toggle (default: true)
  cursor={true}            // Show AI cursor (default: true)
  clickRipple={true}       // Show click effects (default: true)
  typingAnimation={true}   // Character-by-character typing (default: true)
  typingSpeed={12}         // Characters per second (default: 12)
/>
```

## Element Targeting

The overlay finds elements using `data-agentpulse-id` attributes.

### Naming Convention

Format: `data-agentpulse-id="componentId-normalizedKey"`

Where `normalizedKey` = binding key with `set` prefix removed, lowercased.

| Binding | Normalized Key | Attribute |
|---------|---------------|-----------|
| `setName` | `name` | `data-agentpulse-id="form-name"` |
| `setEmail` | `email` | `data-agentpulse-id="form-email"` |
| `submitForm` | `submitform` | `data-agentpulse-id="form-submitform"` |
| `setValue` | `value` | `data-agentpulse-id="input-value"` |

### Example

```tsx
function ContactForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  useExpose('contact-form', {
    setName: (v) => setName(v),
    setEmail: (v) => setEmail(v),
    submitForm: () => handleSubmit(),
  });

  return (
    <form>
      <input data-agentpulse-id="contact-form-name" value={name} />
      <input data-agentpulse-id="contact-form-email" value={email} />
      <button data-agentpulse-id="contact-form-submitform">Submit</button>
    </form>
  );
}
```

## Auto-Discovery Fallback Chain

If `data-agentpulse-id` is missing, the resolver tries (in order):

1. `[data-agentpulse-id="componentId-normalizedKey"]`
2. Form container `[data-agentpulse-id="componentId"]` → input by name
3. `input[name="key"]` or `textarea[name="key"]`
4. `getElementById(key)` or `getElementById("componentId-key")`
5. `input[placeholder*="key"]` (case-insensitive)
6. `[aria-label*="key"]` (case-insensitive)
7. Submit button detection for `submitForm` actions
8. Open/close button detection for modal actions

## Custom CSS Selectors

For complex layouts where auto-discovery fails:

```tsx
<VisualOverlay
  targets={{
    'contact-form': {
      name: 'input[name="fullName"]',
      email: 'input[type="email"]',
      submit: 'button[type="submit"]',
    },
    'sidebar': {
      toggle: '#sidebar-toggle',
    },
  }}
/>
```

Or configure programmatically:

```tsx
import { setAnimationConfig, clearAnimationConfig } from 'agentpulse';

setAnimationConfig({
  'my-form': {
    username: '#username-input',
    password: '#password-input',
  },
});

// Clear when done
clearAnimationConfig();
```

## Common Patterns

### Form with Multiple Fields

```tsx
useExpose('signup-form', {
  setEmail: (v) => setEmail(v),
  setPassword: (v) => setPassword(v),
  submit: () => handleSubmit(),
});

// Add data attributes to each input
<input data-agentpulse-id="signup-form-email" />
<input data-agentpulse-id="signup-form-password" />
<button data-agentpulse-id="signup-form-submit">Sign Up</button>
```

### Third-Party Component Libraries

For MUI, Chakra, etc., wrap or pass the data attribute:

```tsx
// MUI TextField
<TextField
  inputProps={{ 'data-agentpulse-id': 'form-email' }}
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>

// Or use CSS selector config
<VisualOverlay
  targets={{
    'form': {
      email: '.MuiTextField-root input',
    },
  }}
/>
```

### Search Box

```tsx
useExpose('search', {
  query,
  setQuery,
  search: () => performSearch(),
});

<input data-agentpulse-id="search-query" />
<button data-agentpulse-id="search-search">Search</button>
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cursor goes to wrong element | Key mismatch | Check normalized key matches attribute |
| No animation on action | Missing attribute | Add `data-agentpulse-id` to element |
| Animation on wrong form field | Duplicate attributes | Make each attribute unique per component |
| Third-party input not found | Nested DOM structure | Use CSS selector config |

### Debug Targeting

Open browser console and look for resolver logs:

```
[TargetResolver] Found element for contact-form.name using selector: ...
[TargetResolver] Auto-discovered element for contact-form.email
[TargetResolver] No element found for contact-form.phone
```

## Process

1. **Add VisualOverlay** - Import and add inside AgentPulseProvider
2. **Identify target elements** - Which inputs/buttons need animations?
3. **Add data attributes** - Use `data-agentpulse-id="componentId-normalizedKey"`
4. **Test with agent** - Call `expose_set` or `expose_call` and verify animations
5. **Configure fallbacks** - Use CSS selectors for complex layouts

## More Details

See `references/TARGETING_PATTERNS.md` for:
- Full fallback chain explanation
- Naming convention edge cases
- Third-party component strategies
- Debug techniques
