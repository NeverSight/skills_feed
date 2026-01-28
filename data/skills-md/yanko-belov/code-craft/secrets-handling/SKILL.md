---
name: secrets-handling
description: Use when working with API keys, passwords, or credentials. Use when asked to hardcode secrets. Use when secrets might leak.
---

# Secrets Handling

## Overview

**Never hardcode secrets. Never commit secrets. Never log secrets.**

Secrets in code end up in version control, logs, error messages, and eventually in attackers' hands.

## When to Use

- Working with API keys, tokens, passwords
- Configuring database connections
- Setting up third-party service credentials
- Asked to "just hardcode it for now"

## The Iron Rule

```
NEVER put secrets in source code.
```

**No exceptions:**
- Not for "just for testing"
- Not for "it's a private repo"
- Not for "I'll remove it later"
- Not for "it's not a real secret"

## Detection: Hardcoded Secret Smell

If you see literal credentials, STOP:

```typescript
// ❌ VIOLATION: Hardcoded secrets
const stripe = new Stripe('sk_live_abc123xyz');

const db = mysql.connect({
  password: 'super_secret_password'
});

const API_KEY = 'AIzaSyD-xxxxxxxxxxxxx';
```

Problems:
- Secrets in git history forever
- Visible in code reviews
- Exposed in error stack traces
- Shared with anyone who has repo access

## The Correct Pattern: Environment Variables

```typescript
// ✅ CORRECT: Environment variables
import { z } from 'zod';

// Validate env vars at startup
const envSchema = z.object({
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
});

const env = envSchema.parse(process.env);

// Use validated env vars
const stripe = new Stripe(env.STRIPE_SECRET_KEY);
```

```bash
# .env (NEVER commit this file)
STRIPE_SECRET_KEY=sk_live_abc123xyz
DATABASE_URL=postgres://user:pass@host:5432/db
API_KEY=your-api-key

# .gitignore (ALWAYS include)
.env
.env.*
!.env.example
```

```bash
# .env.example (commit this - no real values)
STRIPE_SECRET_KEY=sk_test_xxx
DATABASE_URL=postgres://localhost:5432/myapp
API_KEY=your-api-key-here
```

## Secrets Hygiene Rules

### 1. Environment Variables
```typescript
const secret = process.env.SECRET_KEY;
```

### 2. Validate at Startup
```typescript
if (!process.env.API_KEY) {
  throw new Error('API_KEY environment variable is required');
}
```

### 3. Never Log Secrets
```typescript
// ❌ BAD
console.log('Connecting with:', connectionString);

// ✅ GOOD
console.log('Connecting to database...');
```

### 4. Mask in Error Messages
```typescript
// ❌ BAD
throw new Error(`Auth failed for key: ${apiKey}`);

// ✅ GOOD
throw new Error('Authentication failed');
```

### 5. Use Secret Managers in Production
```typescript
// AWS Secrets Manager, HashiCorp Vault, etc.
const secret = await secretsManager.getSecret('my-api-key');
```

## Pressure Resistance Protocol

### 1. "Just for Testing"
**Pressure:** "Hardcode it for now, we'll fix it later"

**Response:** "Later" never comes. Secrets in history stay forever.

**Action:** Use env vars from the start. It takes 30 seconds.

### 2. "It's a Private Repo"
**Pressure:** "Only the team has access"

**Response:** Teams change. Repos get cloned. Access expands.

**Action:** Never commit secrets regardless of repo visibility.

### 3. "I'll Remove It Later"
**Pressure:** "Just for this one commit"

**Response:** Git history is permanent. The secret is already leaked.

**Action:** If you committed a secret, rotate it immediately.

### 4. "It's Not a Real Secret"
**Pressure:** "This is just a test key"

**Response:** Test keys become production keys. Treat all secrets equally.

**Action:** Use env vars for all credentials.

## Red Flags - STOP and Reconsider

- Literal strings that look like keys/tokens
- `password:`, `secret:`, `key:` in source
- `.env` file not in `.gitignore`
- Secrets in error messages or logs
- Credentials in config files that get committed

**All of these mean: Move to environment variables immediately.**

## If You Accidentally Committed a Secret

1. **Rotate the secret immediately** - consider it compromised
2. Remove from code and commit
3. Consider git history rewriting (but assume it's leaked)
4. Check for unauthorized usage

## Quick Reference

| Do | Don't |
|----|-------|
| Environment variables | Hardcoded strings |
| `.env` in `.gitignore` | Commit `.env` files |
| `.env.example` with placeholders | Real values in examples |
| Validate env at startup | Fail silently on missing |
| Secret managers in prod | Env vars in containers |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Just for testing" | Testing secrets become production secrets. |
| "Private repo" | Private today, leaked tomorrow. |
| "I'll remove it" | Git history is forever. |
| "Not a real secret" | All credentials deserve protection. |
| "It's encrypted" | Keys to decrypt are also secrets. |
| "Only local use" | Local files get committed. |

## The Bottom Line

**Secrets live in environment, never in code.**

Use environment variables. Validate at startup. Never log credentials. Never commit `.env` files. If you leak a secret, rotate it immediately.
