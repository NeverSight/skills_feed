---
name: auth-patterns
description: Use when implementing authentication. Use when storing passwords. Use when asked to store credentials insecurely.
---

# Authentication Patterns

## Overview

**Never store plain passwords. Use proven auth patterns. Security is not optional.**

Authentication is the front door to your system. Get it wrong and everything else is compromised.

## When to Use

- Implementing login/registration
- Storing user credentials
- Verifying user identity
- Working with sessions or tokens

## The Iron Rule

```
NEVER store passwords in plain text. ALWAYS use slow hashing.
```

**No exceptions:**
- Not for "internal users only"
- Not for "we'll encrypt later"
- Not for "it's behind a firewall"
- Not for "just for development"

## Detection: Insecure Auth Smell

If passwords aren't properly hashed, STOP:

```typescript
// ❌ VIOLATION: Plain text password
await db.users.create({
  email,
  password: password  // Stored as-is!
});

// ❌ VIOLATION: Fast hash (crackable)
const hashed = crypto.createHash('sha256').update(password).digest('hex');

// ❌ VIOLATION: Reversible encryption
const encrypted = encrypt(password, key);  // Can be decrypted!
```

## The Correct Pattern: Bcrypt/Argon2

```typescript
// ✅ CORRECT: Slow, salted hashing with bcrypt
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;  // Adjust based on your hardware

async function hashPassword(plain: string): Promise<string> {
  return bcrypt.hash(plain, SALT_ROUNDS);
}

async function verifyPassword(plain: string, hashed: string): Promise<boolean> {
  return bcrypt.compare(plain, hashed);
}

// Registration
app.post('/register', async (req, res) => {
  const { email, password } = validated(req.body);
  
  const hashedPassword = await hashPassword(password);
  
  await db.users.create({
    email,
    password: hashedPassword  // Store the hash
  });
  
  res.status(201).json({ success: true });
});

// Login
app.post('/login', async (req, res) => {
  const { email, password } = validated(req.body);
  
  const user = await db.users.findByEmail(email);
  
  // Constant-time comparison to prevent timing attacks
  // Always verify even if user not found
  const dummyHash = '$2b$12$dummy.hash.here';
  const isValid = await verifyPassword(password, user?.password ?? dummyHash);
  
  if (!user || !isValid) {
    // Same error for both cases - prevents user enumeration
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  const token = generateToken(user);
  res.json({ token });
});
```

## Authentication Checklist

### Password Storage
- [ ] Use bcrypt or Argon2 (slow hash)
- [ ] Salt rounds ≥ 12 for bcrypt
- [ ] Never store plain text
- [ ] Never use MD5/SHA1/SHA256 alone

### Login Security
- [ ] Constant-time comparison
- [ ] Same error for "user not found" and "wrong password"
- [ ] Rate limiting on login endpoint
- [ ] Account lockout after N failures

### Session/Token Security
- [ ] JWTs: short expiry, secure secret
- [ ] Sessions: secure, httpOnly cookies
- [ ] Implement token refresh properly
- [ ] Invalidate on logout/password change

## Pressure Resistance Protocol

### 1. "We'll Encrypt Later"
**Pressure:** "Just store it for now, we'll add encryption"

**Response:** Plain text passwords get leaked. Breaches happen fast.

**Action:** Hash from day one. It's 3 lines of code.

### 2. "It's Behind a Firewall"
**Pressure:** "Internal network, no one can access it"

**Response:** Firewalls get breached. Insiders exist. Defense in depth.

**Action:** Hash regardless of network security.

### 3. "SHA256 Is Secure"
**Pressure:** "SHA256 is a strong hash"

**Response:** SHA256 is fast - billions per second on GPU. Bcrypt is intentionally slow.

**Action:** Use bcrypt or Argon2. Speed is the enemy.

### 4. "Just for Development"
**Pressure:** "Dev database doesn't need security"

**Response:** Dev code becomes prod code. Dev habits become prod habits.

**Action:** Use proper hashing in all environments.

## Red Flags - STOP and Reconsider

- `password` column without "hash" in name
- Using `crypto.createHash` for passwords
- Comparing passwords with `===`
- Same error messages reveal user existence
- No rate limiting on auth endpoints

**All of these mean: Fix the auth implementation.**

## Quick Reference

| Insecure | Secure |
|----------|--------|
| Plain text storage | bcrypt/Argon2 hash |
| SHA256(password) | bcrypt.hash(password, 12) |
| `===` comparison | bcrypt.compare() |
| "User not found" error | "Invalid credentials" |
| Unlimited login attempts | Rate limiting + lockout |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "We'll encrypt later" | Do it now. Takes 3 lines. |
| "Behind firewall" | Defense in depth required. |
| "SHA256 is secure" | Too fast. Use slow hashes. |
| "Just development" | Dev becomes prod. |
| "Internal users only" | Insiders cause breaches too. |
| "We trust our database" | Databases get dumped. |

## The Bottom Line

**Hash passwords with bcrypt. Use constant-time comparison. Return generic errors.**

Password security is non-negotiable. Use slow hashes (bcrypt, Argon2). Prevent timing attacks. Don't leak user existence. Rate limit everything.
