---
name: anti-fraud
description: "Multi-layered anti-fraud and bot detection system for registration flows. Use when implementing: (1) Registration form security, (2) Bot detection and shadow banning, (3) Behavioral analysis (keystroke, mouse tracking), (4) Risk scoring systems, (5) Honeypot field implementation, (6) Disposable email detection, or any fraud prevention for user registration"
---

# Anti-Fraud & Bot Detection System

A three-layer defense system for registration forms that detects bots while minimizing false positives for legitimate users.

## Architecture Overview

```
Layer 1: SERVER-SIDE (tamper-proof)
├── Encrypted timestamp token verification
├── Device fingerprint matching
└── Minimum fill time enforcement (3s)

Layer 2: MANIPULATION DETECTION (server comparison)
├── Client vs Server timing mismatch
├── Keystroke/input inconsistency
└── Impossible value detection

Layer 3: CLIENT SIGNALS (informational)
├── Honeypot fields
├── Behavioral analysis
└── Content analysis
```

**Key Principle:** Never trust client-side data alone.

## Quick Implementation

### 1. Form Token Endpoint

```typescript
// /api/auth/form-token
// Generate AES-256-GCM encrypted token with timestamp
const token = encrypt({ timestamp: Date.now(), fingerprint, nonce });
```

### 2. Behavior Tracking Hook

```typescript
interface BehaviorSignals {
  totalFillTimeMs: number;
  fieldTimings: Record<string, number>;
  inputMethods: Record<string, 'typed' | 'pasted' | 'autofilled' | 'mixed'>;
  keystrokes: KeystrokeData[];
  keystrokeVariance: number;
  mouseMovements: MouseMovement[];
  hasMouseActivity: boolean;
  focusSequence: string[];
  tabKeyUsed: boolean;
  backspaceCount: number;
}
```

### 3. Honeypot Fields

Add hidden fields (CSS hidden, aria-hidden, tabIndex=-1):
- `website`, `phone2`, `address`, `company`

**Any content in honeypot → Instant shadow ban**

## Risk Scoring

### Shadow Ban Triggers (ANY = ban)

| Trigger | Condition |
|---------|-----------|
| Server timing | Fill time < 3 seconds |
| Token | Invalid or missing |
| Manipulation | High confidence detection |
| Score | >= 80 points |
| Honeypot | Any field filled |
| Email | Disposable domain |

### Signal Weights

See `references/signal-weights.md` for complete weight tables.

**Critical (+100):** `HONEYPOT_FILLED`, `DISPOSABLE_EMAIL`  
**High (+25-40):** `INSTANT_SUBMIT`, `ALL_FIELDS_PASTED`, `BOT_PASSWORD_PATTERN`, `NO_MOUSE_MOVEMENT`  
**Positive (-5 to -40):** `PASSWORD_MANAGER_LIKELY`, `KEYBOARD_ONLY_USER`, `NATURAL_TYPING_RHYTHM`

## Shadow Ban Response

```typescript
if (shouldShadowBan) {
  await delay(1000 + Math.random() * 2000); // Appear legitimate
  return Response.json({ message: 'Registration successful' }, { status: 200 });
  // No account created, no backend call
}
```

## False Positive Prevention

### Password Manager Detection (-40 points)

```typescript
const isPasswordManager = 
  allFieldsAutofilledOrPasted && 
  keystrokeCount < 5 && 
  fillTime >= 1000 && fillTime < 15000;
```

### Keyboard-Only User Detection (-15 points)

```typescript
const isKeyboardOnly = 
  tabKeyUsed && 
  focusSequence.length >= 2 && 
  !hasMouseActivity && 
  totalFieldTime > 1000;
```

## File Structure

```
src/
├── lib/anti-fraud/
│   ├── index.ts
│   ├── types.ts
│   ├── constants.ts
│   ├── risk-scoring.ts
│   ├── server-token.ts
│   ├── manipulation-detector.ts
│   └── validators/
│       ├── email-validator.ts
│       ├── name-validator.ts
│       └── password-validator.ts
├── hooks/use-behavior-tracking.ts
├── components/anti-fraud/honeypot-fields.tsx
└── app/api/auth/
    ├── form-token/route.ts
    └── register/route.ts
```

## Resources

- **Signal weights & thresholds:** See `references/signal-weights.md`
- **Validators (email, name, password):** See `references/validators.md`
- **XML patterns & detection:** See `references/detection-patterns.md`

## Environment

```env
AUTH_SECRET=your-secret-key-for-token-encryption
```

## Logging

All decisions logged with `[ANTI_FRAUD]` prefix:
```
[ANTI_FRAUD] { timestamp, emailDomain, serverFillTimeMs, summary: 'Risk: 25/100 (low) - allow' }
```
