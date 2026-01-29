---
name: security
description: Security auditing for code vulnerabilities (OWASP Top 10, XSS, SQL injection) and dependency scanning (pnpm audit, Snyk). Use when handling user input, adding authentication, before deployments, or resolving CVEs.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Security Skill

## Dependency Scanning

### pnpm audit

```bash
# Run audit
pnpm audit

# Only high/critical
pnpm audit --audit-level=high

# Auto-fix
pnpm audit --fix

# JSON report
pnpm audit --json > audit.json
```

### Fix Vulnerabilities

**Direct dependencies:** Update version in `pnpm-workspace.yaml` catalog

**Transitive dependencies:**
```bash
# Find dependency chain
pnpm why vulnerable-package

# Use overrides as last resort
# package.json
{
  "pnpm": {
    "overrides": {
      "vulnerable-package": "^3.1.0"
    }
  }
}
```

### Snyk

```bash
snyk auth          # Authenticate
snyk test          # Test for vulnerabilities
snyk monitor       # Monitor for new vulnerabilities
snyk fix           # Auto-fix
```

## OWASP Top 10 Checks

### 1. Broken Access Control

```typescript
// ❌ No authorization
export async function deletePost(postId: string) {
  await db.delete(posts).where(eq(posts.id, postId));
}

// ✅ With authorization
export async function deletePost(postId: string, userId: string) {
  const post = await db.query.posts.findFirst({ where: eq(posts.id, postId) });
  if (post.authorId !== userId) throw new Error("Unauthorized");
  await db.delete(posts).where(eq(posts.id, postId));
}
```

### 2. Injection Prevention

```typescript
// ❌ SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Parameterized query (Drizzle ORM)
const user = await db.query.users.findFirst({ where: eq(users.id, userId) });
```

### 3. XSS Prevention

React escapes content by default. When rendering HTML:
- Sanitize with `sanitize-html` library before rendering
- Never render untrusted content directly

### 4. Rate Limiting

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { redis } from "@sgcarstrends/utils";

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, "15 m"),
});

export async function login(email: string, password: string, ip: string) {
  const { success } = await ratelimit.limit(ip);
  if (!success) throw new Error("Too many login attempts");
  return verifyCredentials(email, password);
}
```

### 5. Password Security

```typescript
import bcrypt from "bcrypt";

// ✅ Hash passwords
const hashedPassword = await bcrypt.hash(password, 10);

// ✅ Strong password validation
const passwordSchema = z.string()
  .min(12)
  .regex(/[A-Z]/, "Must contain uppercase")
  .regex(/[a-z]/, "Must contain lowercase")
  .regex(/[0-9]/, "Must contain number")
  .regex(/[^A-Za-z0-9]/, "Must contain special character");
```

### 6. SSRF Prevention

```typescript
// ❌ SSRF vulnerability
export async function fetchUrl(url: string) {
  return await fetch(url);
}

// ✅ Whitelist approach
const ALLOWED_DOMAINS = ["api.example.com", "data.gov.sg"];

export async function fetchUrl(url: string) {
  const parsedUrl = new URL(url);
  if (!ALLOWED_DOMAINS.includes(parsedUrl.hostname)) {
    throw new Error("Domain not allowed");
  }
  return await fetch(url);
}
```

## Input Validation

```typescript
import { z } from "zod";

const userInputSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
});

export async function createUser(data: unknown) {
  const validated = userInputSchema.parse(data);
  // Now safe to use
}
```

## CORS Configuration

```typescript
// ❌ Too permissive
app.use(cors({ origin: "*" }));

// ✅ Whitelist specific origins
app.use(cors({
  origin: [
    "https://sgcarstrends.com",
    "https://staging.sgcarstrends.com",
    process.env.NODE_ENV === "development" ? "http://localhost:3001" : "",
  ].filter(Boolean),
  credentials: true,
}));
```

## Security Headers

```typescript
// next.config.js
const securityHeaders = [
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  { key: "X-Frame-Options", value: "SAMEORIGIN" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-XSS-Protection", value: "1; mode=block" },
  { key: "Referrer-Policy", value: "origin-when-cross-origin" },
];

module.exports = {
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};
```

## Environment Variables

```typescript
// ❌ Hardcoded secret
const apiKey = "sk_live_EXAMPLE_NOT_REAL";

// ✅ From environment with validation
import { z } from "zod";

const envSchema = z.object({
  API_KEY: z.string().min(1),
  DATABASE_URL: z.string().url(),
});

const env = envSchema.parse(process.env);
```

## CI Integration

```yaml
# .github/workflows/security.yml
name: Security Audit

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm audit --audit-level=high
```

## Security Checklist

- [ ] All user input validated (Zod schemas)
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (React escaping, sanitization)
- [ ] Authentication implemented correctly
- [ ] Authorization checks in place
- [ ] Passwords hashed (bcrypt/argon2)
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] CORS configured properly
- [ ] HTTPS enforced
- [ ] Dependencies audited (pnpm audit)
- [ ] Secrets in environment variables
- [ ] Error messages don't leak info

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten
- pnpm Audit: https://pnpm.io/cli/audit
- Snyk: https://snyk.io
