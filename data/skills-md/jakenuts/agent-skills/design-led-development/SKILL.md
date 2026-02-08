---
name: design-led-development
description: Build software with elite design principles focusing on user outcomes, trust, accessibility, and performance. Use when creating UI components, designing user flows, writing production code, reviewing code quality, or when the user mentions UX, accessibility, performance, or trust-focused development.
---

# Design-Led Development

Build systems that feel inevitable, trustworthy, and delightful. Every line of code serves a human outcome.

## Core Decision Framework

Before writing any feature, answer these questions in order:

1. **User outcome**: "This helps [user] achieve [outcome] by [mechanism]"
2. **Anxiety/control**: Does this reduce user anxiety or increase user control?
3. **Simplicity**: Is this the simplest solution?
4. **Measurability**: Can we measure success?
5. **Failure mode**: What's the failure mode? If catastrophic, add safeguards
6. **Recovery**: Can users recover from errors?

If you cannot articulate the user outcome in one sentence, do not code it yet.

## Code Principles

### Clarity Over Cleverness

```typescript
// ✅ DO: Name for humans reading at 2am
const userAuthenticationStatus = checkAuth(userId);
const formattedOrderDate = formatDate(order.createdAt);

// ❌ DON'T: Clever but obscure
const x = chk(u);
const d = fmt(o.c);
```

Comments explain *why*, not *what*. Red flag phrases: "just", "simply", "obviously".

### Explicit Error Handling

```typescript
// ✅ DO: Error states as return types
type Result<T> = 
  | { success: true; data: T } 
  | { success: false; error: UserFacingError };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await api.getUser(id);
    return { success: true, data: user };
  } catch (error) {
    return { 
      success: false, 
      error: { 
        message: "Unable to load user profile",
        action: "Please try again or contact support"
      }
    };
  }
}

// ❌ NEVER: Generic errors or silent failures
throw new Error("Something went wrong");
```

### Network Resilience

```typescript
// ✅ DO: Exponential backoff with jitter
const retryWithBackoff = async <T>(
  fn: () => Promise<T>, 
  maxRetries = 3
): Promise<T> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.min(1000 * 2 ** i + Math.random() * 1000, 10000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Max retries exceeded');
};

// ✅ DO: Timeout promises
const withTimeout = <T>(promise: Promise<T>, ms: number): Promise<T> =>
  Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), ms)
    )
  ]);
```

## Performance Budgets

Set these before coding:

| Metric | Budget |
|--------|--------|
| Cold start | < 2s on median device |
| Interaction response | < 100ms perceived |
| Animations | < 16ms per frame (60fps) |
| API calls (p95) | < 500ms |

Treat performance regressions as P0 bugs. Profile on low-end devices.

## UI Component States

Every interactive component MUST handle all states:

```
✅ Default (idle)
✅ Hover (pointer devices)
✅ Active/pressed
✅ Focus (keyboard navigation)
✅ Disabled (with explanation why)
✅ Loading (with progress indication)
✅ Error (with recovery action)
✅ Success (with next step)
✅ Empty (with helpful onboarding)
```

## Visual System

### Spacing (8pt Grid)

```
4px:  Tight grouping (icon + label)
8px:  Related items (form fields in group)
16px: Section separation
24px: Component boundaries
32px: Major sections
48px: Screen-level padding
```

### Typography Scale

```
H1: 32-40px, bold, line-height 1.2
H2: 24-28px, semibold, line-height 1.3
H3: 20-24px, semibold, line-height 1.4
Body: 16-18px, regular, line-height 1.5
Caption: 14px, regular, line-height 1.4

RULE: Never below 14px for body text (accessibility)
```

### Motion

| Purpose | Duration | Easing |
|---------|----------|--------|
| Micro-interactions | 100-200ms | ease-out |
| Screen transitions | 300-400ms | ease-in-out |
| Loading states | 600ms+ | linear |

Rules:
- Animation explains, never decorates
- Respect `prefers-reduced-motion`
- Never delay user actions

## Accessibility Requirements

Non-negotiable checklist:

- [ ] Semantic HTML with ARIA labels
- [ ] Keyboard navigation for all interactions
- [ ] Color contrast: 4.5:1 minimum (7:1 for body text)
- [ ] Touch targets: 44x44pt minimum
- [ ] Screen reader tested
- [ ] Respects `prefers-reduced-motion`
- [ ] Respects `prefers-color-scheme`

## Trust Architecture

Every feature must answer:

1. **Data collected**: What data? (Collect minimum)
2. **Failure modes**: What could go wrong? (Design failures first)
3. **Trust signals**: How do I prove safety? (Make visible)
4. **Reversibility**: Can users undo? (Preview before commit)
5. **Data fate**: What happens to their data? (Explicit, not ToS)

### Privacy Defaults

```typescript
// ✅ DO: Default private, opt-in sharing
const defaultSettings = {
  shareAnalytics: false,
  publicProfile: false,
  dataRetention: 'minimum'
};

// ✅ DO: Redact PII in logs
logger.info('user_action', {
  action: 'profile_update',
  userId: hashUserId(user.id), // Never raw PII
  duration_ms: 234,
  success: true
});
```

## Form Validation

- Validate on blur, not on every keystroke
- Show errors inline, near the field
- Preserve user input on errors (never clear)
- Auto-save drafts for long forms
- Disable submit only if invalid, explain why

## Feedback Loops

Every user action needs acknowledgment:

| Type | Timing | Example |
|------|--------|---------|
| Immediate | < 100ms | Button press visual |
| Progress | > 1s operations | Loading indicator |
| Completion | After success | "Saved" with next step |
| Failure | On error | What happened + how to fix |

Never blame the user in error messages.

## Anti-Patterns

### Code Anti-Patterns (Never Do)

```
❌ Magic numbers without constants
❌ Functions over 50 lines
❌ God objects over 300 lines
❌ Mutable global state
❌ Side effects not in function name
❌ Catching errors without handling
❌ Copy-pasted code
```

### UX Anti-Patterns (Never Do)

```
❌ Forced account creation before value
❌ Dark patterns (hidden costs, trick questions)
❌ Generic error messages ("Error 500")
❌ Modal dialogs for everything
❌ Destroying data without confirmation
❌ Disabling paste in password fields
❌ Auto-playing video/audio
❌ Infinite scroll without pagination option
```

## Security Checklist

- [ ] Sanitize all user input (XSS prevention)
- [ ] Parameterized queries (SQL injection prevention)
- [ ] Rate limit all endpoints
- [ ] CSRF tokens for state-changing operations
- [ ] Encrypt PII at rest (AES-256)
- [ ] TLS 1.3 for all network traffic
- [ ] Hash passwords with bcrypt/Argon2
- [ ] HttpOnly, Secure, SameSite cookies

## Quality Gates (Before Ship)

- [ ] Lighthouse score > 90
- [ ] Zero critical/high security vulnerabilities
- [ ] Core flows work offline or degrade gracefully
- [ ] Keyboard navigation works
- [ ] Screen reader tested (VoiceOver + NVDA)
- [ ] Error states tested
- [ ] Load tested at 2x expected peak
- [ ] Mobile tested on real devices
- [ ] Privacy review completed
- [ ] Rollback procedure documented

## Final Mandate

Every piece of code should make someone's life measurably better.

- If you cannot explain the user benefit, do not ship it
- If you cannot measure the outcome, instrument it
- If you cannot maintain it, simplify it
- If it does not feel inevitable, redesign it

**Quality is not negotiable. Speed is achieved through clarity, not shortcuts.**
