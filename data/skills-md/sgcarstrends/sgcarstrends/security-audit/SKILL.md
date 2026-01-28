---
name: security-audit
description: Audit code for security vulnerabilities (SQL injection, XSS, OWASP Top 10). Use when adding authentication logic, handling user input, or before production deployments.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Audit Skill

This skill helps you identify and fix security vulnerabilities in the codebase.

## When to Use This Skill

- Before production deployments
- When adding authentication/authorization
- When handling user input
- After dependency updates
- During code reviews
- When integrating third-party services

## OWASP Top 10 (2021)

### 1. Broken Access Control

**Issue**: Users can access resources they shouldn't

**Check For:**
```bash
# Search for authorization checks
grep -r "hasPermission\|canAccess\|isAuthorized" apps/ --include="*.ts"

# Look for missing auth checks
grep -r "export.*function\|export.*async function" apps/api/src/routes --include="*.ts"
```

**Example Vulnerability:**
```typescript
// ❌ No authorization check
export async function deletePost(postId: string) {
  await db.delete(posts).where(eq(posts.id, postId));
}

// ✅ With authorization
export async function deletePost(postId: string, userId: string) {
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, postId),
  });

  if (post.authorId !== userId) {
    throw new Error("Unauthorized");
  }

  await db.delete(posts).where(eq(posts.id, postId));
}
```

### 2. Cryptographic Failures

**Issue**: Sensitive data exposed or poorly encrypted

**Check For:**
```bash
# Look for hardcoded secrets
grep -ri "password.*=\|api[_-]key.*=\|secret.*=" apps/ packages/ --include="*.ts"

# Check for sensitive data in logs
grep -r "console.log" apps/ --include="*.ts" | grep -i "password\|token\|secret"
```

**Example Vulnerability:**
```typescript
// ❌ Storing passwords in plain text
await db.insert(users).values({
  email,
  password,  // Plain text!
});

// ✅ Hashing passwords
import bcrypt from "bcrypt";

const hashedPassword = await bcrypt.hash(password, 10);
await db.insert(users).values({
  email,
  password: hashedPassword,
});
```

### 3. Injection

**Issue**: SQL injection, command injection, etc.

**Check For:**
```bash
# Look for string concatenation in queries
grep -r "SELECT.*\${" apps/ packages/ --include="*.ts"
grep -r "WHERE.*\${" apps/ packages/ --include="*.ts"

# Check for eval usage
grep -r "eval(" apps/ packages/ --include="*.ts"
```

**Example Vulnerability:**
```typescript
// ❌ SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Parameterized query (Drizzle ORM)
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
});

// ❌ Command Injection
const result = exec(`git log ${userInput}`);

// ✅ Sanitized input
import { z } from "zod";

const schema = z.string().regex(/^[a-zA-Z0-9-]+$/);
const sanitized = schema.parse(userInput);
const result = exec(`git log ${sanitized}`);
```

### 4. Insecure Design

**Issue**: Flawed security architecture

**Check For:**
- Missing rate limiting
- No input validation
- Weak session management
- Missing CSRF protection

**Example Vulnerability:**
```typescript
// ❌ No rate limiting
export async function login(email: string, password: string) {
  // Anyone can brute force passwords
  const user = await verifyCredentials(email, password);
  return createSession(user);
}

// ✅ With rate limiting
import { Ratelimit } from "@upstash/ratelimit";
import { redis } from "@sgcarstrends/utils";

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, "15 m"),  // 5 attempts per 15 min
});

export async function login(email: string, password: string, ip: string) {
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    throw new Error("Too many login attempts");
  }

  const user = await verifyCredentials(email, password);
  return createSession(user);
}
```

### 5. Security Misconfiguration

**Issue**: Insecure default configs, unnecessary services

**Check For:**
```bash
# Look for debug mode in production
grep -r "debug.*true" apps/ --include="*.ts" --include="*.json"

# Check for exposed error messages
grep -r "error.stack\|error.message" apps/ --include="*.ts"
```

**Example Vulnerability:**
```typescript
// ❌ Exposing stack traces in production
export async function handler(req: Request) {
  try {
    // ...
  } catch (error) {
    return Response.json({ error: error.stack }, { status: 500 });
  }
}

// ✅ Safe error handling
export async function handler(req: Request) {
  try {
    // ...
  } catch (error) {
    console.error("Error:", error);  // Log internally
    return Response.json(
      { error: "Internal server error" },  // Generic message
      { status: 500 }
    );
  }
}
```

### 6. Vulnerable Components

**Issue**: Using outdated or vulnerable dependencies

**Check For:**
```bash
# Audit dependencies
pnpm audit

# Check for outdated packages
pnpm outdated

# Look for specific vulnerable packages
pnpm list | grep "package-name"
```

**Fix:**
```bash
# Update vulnerable packages
pnpm update package-name

# Or update all
pnpm update -r

# Check audit after update
pnpm audit
```

### 7. Authentication Failures

**Issue**: Weak authentication mechanisms

**Check For:**
```bash
# Look for weak password requirements
grep -r "password.*length" apps/ --include="*.ts"

# Check for missing password hashing
grep -r "password.*=" apps/ --include="*.ts" | grep -v "bcrypt\|argon2\|hash"
```

**Example Vulnerability:**
```typescript
// ❌ Weak password validation
const passwordSchema = z.string().min(6);

// ✅ Strong password validation
const passwordSchema = z.string()
  .min(12)
  .regex(/[A-Z]/, "Must contain uppercase")
  .regex(/[a-z]/, "Must contain lowercase")
  .regex(/[0-9]/, "Must contain number")
  .regex(/[^A-Za-z0-9]/, "Must contain special character");
```

### 8. Software and Data Integrity Failures

**Issue**: Unverified updates, insecure CI/CD

**Check For:**
```bash
# Look for unsigned packages
grep -r "npm install\|pnpm add" .github/ --include="*.yml"

# Check for pinned versions
cat package.json | grep -v "^\s*\".*\":\s*\"[\^~]"
```

**Example Fix:**
```json
// ❌ Unpinned versions
{
  "dependencies": {
    "react": "^18.0.0",  // Could install 18.9.9
    "next": "~15.0.0"    // Could install 15.0.9
  }
}

// ✅ Pinned versions (with pnpm catalog)
{
  "dependencies": {
    "react": "catalog:",  // Exact version from catalog
    "next": "catalog:"
  }
}
```

### 9. Logging and Monitoring Failures

**Issue**: Insufficient logging, no alerting

**Check For:**
```bash
# Look for authentication logging
grep -r "login\|authenticate" apps/api --include="*.ts" | grep -c "log\|console"

# Check for error logging
grep -r "catch.*error" apps/ --include="*.ts" | grep -v "log\|console"
```

**Example Vulnerability:**
```typescript
// ❌ No logging
export async function login(email: string, password: string) {
  const user = await verifyCredentials(email, password);
  return createSession(user);
}

// ✅ With security logging
export async function login(email: string, password: string, ip: string) {
  try {
    const user = await verifyCredentials(email, password);

    // Log successful login
    console.log(`Login success: ${email} from ${ip}`);

    return createSession(user);
  } catch (error) {
    // Log failed attempt
    console.warn(`Login failed: ${email} from ${ip}`);
    throw error;
  }
}
```

### 10. Server-Side Request Forgery (SSRF)

**Issue**: Server makes requests to attacker-controlled URLs

**Check For:**
```bash
# Look for user-controlled URLs
grep -r "fetch(.*req\|axios(.*req" apps/ --include="*.ts"
```

**Example Vulnerability:**
```typescript
// ❌ SSRF vulnerability
export async function fetchUrl(url: string) {
  return await fetch(url);  // User controls URL!
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

### Always Validate User Input

```typescript
import { z } from "zod";

// Define schema
const userInputSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  website: z.string().url().optional(),
});

// Validate
export async function createUser(data: unknown) {
  const validated = userInputSchema.parse(data);  // Throws if invalid
  // Now safe to use validated data
}
```

### Sanitize HTML

```typescript
import sanitizeHtml from "sanitize-html";

export function sanitizeUserInput(html: string): string {
  return sanitizeHtml(html, {
    allowedTags: ["b", "i", "em", "strong", "a", "p"],
    allowedAttributes: {
      a: ["href"],
    },
  });
}
```

## XSS Prevention

### React Automatic Escaping

```tsx
// ✅ Safe - React escapes by default
<div>{userInput}</div>

// ❌ Dangerous
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ Safe if sanitized
<div dangerouslySetInnerHTML={{ __html: sanitizeHtml(userInput) }} />
```

### URL Sanitization

```typescript
// ❌ XSS via javascript: protocol
<a href={userUrl}>Click</a>

// ✅ Validate URL
function isSafeUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

<a href={isSafeUrl(userUrl) ? userUrl : "#"}>Click</a>
```

## CORS Configuration

```typescript
// ❌ Too permissive
app.use(cors({
  origin: "*",  // Allows any origin!
}));

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

## Environment Variables

### Never Commit Secrets

```bash
# Check for committed secrets
git log -p | grep -i "password\|secret\|key" | head -20

# Use git-secrets to prevent commits
git secrets --scan
```

### Use Environment Variables

```typescript
// ❌ Hardcoded secret
const apiKey = "sk_live_abc123";

// ✅ From environment
const apiKey = process.env.API_KEY!;

// ✅ With validation
const envSchema = z.object({
  API_KEY: z.string().min(1),
  DATABASE_URL: z.string().url(),
});

const env = envSchema.parse(process.env);
```

## Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  {
    key: "X-Frame-Options",
    value: "SAMEORIGIN",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "X-XSS-Protection",
    value: "1; mode=block",
  },
  {
    key: "Referrer-Policy",
    value: "origin-when-cross-origin",
  },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=()",
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};
```

## Automated Security Scanning

### npm/pnpm Audit

```bash
# Check for vulnerabilities
pnpm audit

# Fix automatically
pnpm audit --fix

# Get JSON report
pnpm audit --json > audit-report.json
```

### Snyk

```bash
# Install Snyk
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor
```

### OWASP Dependency Check

```bash
# Run dependency check
dependency-check --project sgcarstrends --scan .
```

## Security Testing

### Test Authentication

```typescript
// __tests__/security/auth.test.ts
describe("Authentication Security", () => {
  it("rejects invalid credentials", async () => {
    const response = await login("user@example.com", "wrong-password");
    expect(response.status).toBe(401);
  });

  it("rate limits login attempts", async () => {
    const attempts = Array(10).fill(null).map(() =>
      login("user@example.com", "wrong-password")
    );

    await Promise.all(attempts);

    const response = await login("user@example.com", "wrong-password");
    expect(response.status).toBe(429);  // Too many requests
  });

  it("does not leak user existence", async () => {
    const response1 = await login("exists@example.com", "wrong");
    const response2 = await login("noexist@example.com", "wrong");

    // Same error message for both
    expect(response1.message).toBe(response2.message);
  });
});
```

### Test Input Validation

```typescript
describe("Input Validation", () => {
  it("rejects SQL injection attempts", async () => {
    const malicious = "'; DROP TABLE users; --";

    await expect(
      createUser({ name: malicious })
    ).rejects.toThrow();
  });

  it("rejects XSS attempts", async () => {
    const xss = "<script>alert('xss')</script>";

    const result = await createPost({ content: xss });

    expect(result.content).not.toContain("<script>");
  });
});
```

## Security Checklist

Before deployment:

- [ ] All user input validated
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (React escaping, sanitization)
- [ ] CSRF protection enabled
- [ ] Authentication implemented correctly
- [ ] Authorization checks in place
- [ ] Passwords hashed (bcrypt/argon2)
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] CORS configured properly
- [ ] HTTPS enforced
- [ ] Dependencies audited
- [ ] Secrets in environment variables
- [ ] Error messages don't leak info
- [ ] Logging enabled for security events

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org
- Node.js Security: https://nodejs.org/en/docs/guides/security
- Related files:
  - Root CLAUDE.md - Security guidelines

## Best Practices

1. **Validate Everything**: Never trust user input
2. **Use ORM**: Prevent SQL injection
3. **Hash Passwords**: Use bcrypt or argon2
4. **Rate Limit**: Prevent brute force
5. **Security Headers**: Set proper headers
6. **HTTPS Only**: Enforce HTTPS everywhere
7. **Audit Dependencies**: Regularly check for vulnerabilities
8. **Least Privilege**: Grant minimum necessary permissions
