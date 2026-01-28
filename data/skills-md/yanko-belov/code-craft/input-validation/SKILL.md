---
name: input-validation
description: Use when accepting user input. Use when handling request data. Use when trusting external data without validation.
---

# Input Validation

## Overview

**Never trust input. Validate everything at system boundaries.**

All external data is potentially malicious or malformed. Validate at the point of entry, fail fast on invalid input.

## When to Use

- Handling HTTP request bodies, params, headers
- Reading files or environment variables
- Accepting data from external APIs
- Any function that receives untrusted input

## The Iron Rule

```
NEVER use external input without explicit validation.
```

**No exceptions:**
- Not for "the frontend validates it"
- Not for "it's an internal API"
- Not for "we trust the source"
- Not for "it's just a simple field"

## Detection: Trust Smell

If you're using input directly, STOP:

```typescript
// ❌ VIOLATION: Trusting input
app.post('/users', async (req, res) => {
  const { email, age } = req.body;  // Direct destructure - no validation
  await db.users.create({ email, age });
  res.json({ success: true });
});
```

Problems:
- `email` could be empty, null, or not a string
- `age` could be negative, a string, or missing
- SQL injection, XSS possible depending on usage

## The Correct Pattern: Validate at Boundary

```typescript
// ✅ CORRECT: Validate with schema
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  age: z.number().int().min(13).max(120),
  name: z.string().min(1).max(100),
});

app.post('/users', async (req, res) => {
  // Validate
  const result = createUserSchema.safeParse(req.body);
  
  if (!result.success) {
    return res.status(400).json({ 
      error: 'Validation failed',
      details: result.error.flatten().fieldErrors 
    });
  }
  
  // Now data is typed and validated
  const { email, age, name } = result.data;
  await db.users.create({ email, age, name });
  res.status(201).json({ success: true });
});
```

## Validation Rules

### Always Validate:
- **Type**: Is it a string, number, boolean?
- **Format**: Valid email? Valid UUID?
- **Range**: Min/max length? Numeric bounds?
- **Required**: Is it present?
- **Sanitize**: Strip dangerous characters if needed

### Validation Library Examples:

```typescript
// Zod (recommended for TypeScript)
const schema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(0).max(150),
  role: z.enum(['user', 'admin']),
  tags: z.array(z.string()).max(10),
});

// Yup
const schema = yup.object({
  email: yup.string().email().required(),
  age: yup.number().positive().integer(),
});

// class-validator
class CreateUserDto {
  @IsEmail()
  email: string;
  
  @IsInt()
  @Min(13)
  age: number;
}
```

## Pressure Resistance Protocol

### 1. "Frontend Validates It"
**Pressure:** "The form already validates this data"

**Response:** Frontend validation is for UX. Backend validation is for security. Attackers bypass frontends.

**Action:** Validate on backend regardless of frontend validation.

### 2. "It's an Internal API"
**Pressure:** "Only our services call this endpoint"

**Response:** Internal services have bugs too. Defense in depth requires validation everywhere.

**Action:** Validate internal API inputs too.

### 3. "We Trust the Source"
**Pressure:** "This data comes from our partner's API"

**Response:** Their API can have bugs, be compromised, or change format. Trust no one.

**Action:** Validate external API responses before using.

### 4. "Just a Simple Field"
**Pressure:** "It's just a string, what could go wrong?"

**Response:** Strings can be empty, too long, contain scripts, SQL, or null bytes.

**Action:** Define what "valid" means and enforce it.

## Red Flags - STOP and Reconsider

- `const { x } = req.body` without validation
- Using `any` type for input
- No error response for invalid input
- "The client sends this correctly"
- Parsing input without try/catch

**All of these mean: Add validation.**

## Quick Reference

| Input Type | Validate |
|------------|----------|
| Email | Format, length, required |
| Password | Length, complexity |
| ID | Format (uuid/int), exists |
| Number | Type, range, integer? |
| String | Length, pattern, sanitize |
| Array | Length, item validation |
| Object | Schema validation |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Frontend validates" | Attackers bypass frontends. |
| "Internal API" | Internal bugs exist too. |
| "We trust the source" | Sources can be compromised. |
| "Simple field" | Simple fields cause complex bugs. |
| "Validation is slow" | Validation is faster than breaches. |
| "TypeScript types are enough" | Types disappear at runtime. |

## The Bottom Line

**Validate all input. Trust nothing. Fail fast on invalid data.**

Every external boundary should have explicit validation. Use schema validation libraries. Return clear error messages for invalid input. Never let unvalidated data into your system.
