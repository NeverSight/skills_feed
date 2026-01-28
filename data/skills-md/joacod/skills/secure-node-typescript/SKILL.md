---
name: secure-node-typescript
description: 'Write secure-by-default Node.js and TypeScript applications following security best practices. Use when: (1) Writing new Node.js/TypeScript code, (2) Creating API endpoints or middleware, (3) Handling user input or form data, (4) Implementing authentication or authorization, (5) Working with secrets or environment variables, (6) Setting up project configurations (tsconfig, eslint), (7) User mentions security concerns, (8) Reviewing code for vulnerabilities, (9) Working with file paths or child processes, (10) Setting up HTTP headers or CORS.'
---

# Secure Node.js TypeScript

## Overview

Write secure-by-default Node.js and TypeScript applications that neutralize common server-side threats. This skill provides security guidelines organized by domain, with inline patterns for the most critical controls.

All guidelines are mapped to [OWASP Top 10:2025](https://owasp.org/Top10/) categories for compliance tracking and audit purposes. See `references/security-index.md` for the complete OWASP mapping.

## Security Tiers

Apply guidelines based on the code context:

| Tier         | When to Apply             | Key Focus Areas                                                                |
| ------------ | ------------------------- | ------------------------------------------------------------------------------ |
| **Always**   | All Node.js/TS code       | Strict TypeScript, input validation, no hardcoded secrets, safe error handling |
| **API/HTTP** | Web endpoints, middleware | Headers (helmet), rate limiting, CORS, body limits, Content-Type validation    |
| **Auth**     | Authentication features   | Password hashing (argon2), JWT validation, secure cookies, RBAC                |
| **Data**     | External data processing  | SQL injection, XSS sanitization, prototype pollution, schema validation        |
| **Runtime**  | Dynamic code, processes   | No eval, safe child_process, path traversal prevention                         |

## Quick Patterns

The 10 most critical security controls. Apply these by default.

### 1. Enable Strict TypeScript

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### 2. Validate All Inputs with Zod

```typescript
// DO: Schema validation at entry points
import { z } from 'zod'

const UserSchema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
})

// In route handler
const result = UserSchema.safeParse(req.body)
if (!result.success) {
  return res.status(400).json({ error: 'Invalid input' })
}
const user = result.data // Type-safe validated data
```

### 3. Use Parameterized Queries

```typescript
// DON'T: String concatenation (SQL injection)
const query = `SELECT * FROM users WHERE id = ${userId}`

// DO: Parameterized queries
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId])
```

### 4. Hash Passwords with Argon2

```typescript
import argon2 from 'argon2'

// Hash password
const hash = await argon2.hash(password, { type: argon2.argon2id })

// Verify password
const valid = await argon2.verify(hash, password)
```

### 5. Set Security Headers with Helmet

```typescript
import helmet from 'helmet'
import express from 'express'

const app = express()
app.use(helmet()) // Sets HSTS, CSP, X-Frame-Options, etc.
app.disable('x-powered-by')
```

### 6. Limit Request Body Size

```typescript
// DO: Enforce strict body limits
app.use(express.json({ limit: '1kb' })) // Adjust based on expected payload

// DON'T: Unlimited body parsing (DoS risk)
app.use(express.json())
```

### 7. Sanitize File Paths

```typescript
import path from 'node:path'

// DO: Resolve and validate paths
const ALLOWED_DIR = '/app/uploads'
const safePath = path.resolve(ALLOWED_DIR, userInput)

if (!safePath.startsWith(ALLOWED_DIR)) {
  throw new Error('Path traversal attempt blocked')
}
```

### 8. Never Expose Stack Traces

```typescript
// DO: Generic error response to clients
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err) // Log full error internally
  res.status(500).json({ error: 'Internal server error' }) // Generic to client
})

// DON'T: Expose error details
res.status(500).json({ error: err.message, stack: err.stack })
```

### 9. Use Environment Variables for Secrets

```typescript
// DO: Load secrets from environment
import 'dotenv/config'

const dbPassword = process.env.DB_PASSWORD
if (!dbPassword) throw new Error('DB_PASSWORD required')

// DON'T: Hardcoded secrets
const dbPassword = 'secret123' // Never do this
```

### 10. Import with node: Protocol

```typescript
// DO: Explicit Node.js built-in imports (prevents typosquatting)
import { createServer } from 'node:http'
import { readFile } from 'node:fs/promises'
import path from 'node:path'

// DON'T: Implicit imports
import { createServer } from 'http' // Could resolve to malicious package
```

## Reference Loading Guide

Load reference files based on the task at hand:

| Task                                     | Load Reference                    |
| ---------------------------------------- | --------------------------------- |
| Project setup, tsconfig, type safety     | `references/typescript-safety.md` |
| Form validation, user input, API params  | `references/input-validation.md`  |
| Login, sessions, JWT, passwords, RBAC    | `references/authentication.md`    |
| Headers, CORS, rate limiting, CSP        | `references/http-security.md`     |
| eval, child_process, prototype pollution | `references/runtime-safety.md`    |
| File uploads, path handling, regex       | `references/filesystem-paths.md`  |
| npm audit, lockfiles, supply chain       | `references/dependencies.md`      |
| Error handling, logging, monitoring      | `references/error-logging.md`     |
| Linters, CI/CD, threat modeling          | `references/operational.md`       |
| Full guideline lookup                    | `references/security-index.md`    |

## Audit Script

Validate a project's `tsconfig.json` for security-relevant settings:

```bash
python3 scripts/audit-tsconfig.py /path/to/project
```

The script checks for:

- `strict: true` enabled
- `noImplicitAny` enabled
- `strictNullChecks` enabled
- `noUncheckedIndexedAccess` enabled
- Other security-relevant compiler options

## Assets

Template configurations available in `assets/`:

- `tsconfig.secure.json` - Strict TypeScript configuration template
- `eslint-security.config.js` - ESLint security plugin configuration

Copy and adapt these to your project as a starting point.

## Resources

- Security index: `references/security-index.md`
- TypeScript safety: `references/typescript-safety.md`
- Input validation: `references/input-validation.md`
- Authentication: `references/authentication.md`
- HTTP security: `references/http-security.md`
- Runtime safety: `references/runtime-safety.md`
- Filesystem paths: `references/filesystem-paths.md`
- Dependencies: `references/dependencies.md`
- Error logging: `references/error-logging.md`
- Operational: `references/operational.md`
