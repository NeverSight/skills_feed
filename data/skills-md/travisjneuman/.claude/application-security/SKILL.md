---
name: application-security
description: >-
  OWASP Top 10 with code examples, SAST/DAST tools, dependency scanning, CSP headers, and input validation patterns. Use when hardening applications, reviewing security posture, or implementing defensive coding practices.
---

# Application Security Skill

Secure coding patterns, vulnerability prevention, and security tooling for web applications.

---

## OWASP Top 10 (2021) with Code Examples

### A01: Broken Access Control

```typescript
// BAD - No authorization check
app.get('/api/users/:id', async (req, res) => {
  const user = await db.user.findUnique({ where: { id: req.params.id } });
  res.json(user);
});

// GOOD - Verify ownership or role
app.get('/api/users/:id', authenticate, async (req, res) => {
  if (req.user.id !== req.params.id && req.user.role !== 'ADMIN') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = await db.user.findUnique({ where: { id: req.params.id } });
  res.json(user);
});
```

### A02: Cryptographic Failures

```typescript
// BAD - Weak hashing
import crypto from 'crypto';
const hash = crypto.createHash('md5').update(password).digest('hex');

// GOOD - Use bcrypt with proper rounds
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
const isValid = await bcrypt.compare(password, hash);
```

### A03: Injection

```typescript
// BAD - SQL injection
const query = `SELECT * FROM users WHERE email = '${email}'`;

// GOOD - Parameterized queries (Prisma handles this automatically)
const user = await prisma.user.findUnique({ where: { email } });

// GOOD - Parameterized raw SQL when needed
const users = await prisma.$queryRaw`SELECT * FROM users WHERE email = ${email}`;
```

### A07: Cross-Site Scripting (XSS)

```typescript
// BAD - Rendering raw HTML
element.innerHTML = userInput;

// GOOD - Use textContent or framework escaping
element.textContent = userInput;

// GOOD - React auto-escapes by default
return <div>{userInput}</div>;

// BAD in React - dangerouslySetInnerHTML
return <div dangerouslySetInnerHTML={{ __html: userInput }} />;
```

---

## Content Security Policy (CSP)

### Recommended Headers

```typescript
// Next.js middleware
import { NextResponse } from 'next/server';

export function middleware(request: Request) {
  const nonce = crypto.randomUUID();
  const csp = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}'`,
    `style-src 'self' 'unsafe-inline'`,
    `img-src 'self' data: https:`,
    `font-src 'self'`,
    `connect-src 'self' https://api.example.com`,
    `frame-ancestors 'none'`,
    `base-uri 'self'`,
    `form-action 'self'`,
  ].join('; ');

  const response = NextResponse.next();
  response.headers.set('Content-Security-Policy', csp);
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  return response;
}
```

---

## SAST/DAST Tooling

### Static Analysis (SAST)

| Tool | Language | Usage |
|------|----------|-------|
| ESLint security plugins | JS/TS | `eslint-plugin-security`, `@microsoft/eslint-plugin-sdl` |
| Semgrep | Multi | `semgrep --config=auto .` |
| Bandit | Python | `bandit -r src/` |
| gosec | Go | `gosec ./...` |
| cargo-audit | Rust | `cargo audit` |

### Dynamic Analysis (DAST)

| Tool | Purpose | Usage |
|------|---------|-------|
| OWASP ZAP | Web app scanning | Proxy-based scanner, API scan mode |
| Nuclei | Vulnerability scanning | Template-based scanner |
| Burp Suite | Manual + automated | Professional penetration testing |

### Dependency Scanning

```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# Go
govulncheck ./...

# Rust
cargo audit
```

---

## Input Validation Patterns

### Server-Side Validation (Always Required)

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).regex(/^[a-zA-Z\s'-]+$/),
  age: z.number().int().min(0).max(150).optional(),
});

function createUser(input: unknown) {
  const validated = CreateUserSchema.parse(input);
  // validated is now typed and safe
}
```

### Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/auth/login', authLimiter);
```

---

## Security Checklist

- [ ] All user input validated server-side
- [ ] Parameterized queries for all database operations
- [ ] CSP headers configured
- [ ] Rate limiting on auth endpoints
- [ ] CORS properly restricted
- [ ] Secrets in environment variables, not code
- [ ] Dependencies scanned for vulnerabilities
- [ ] Authentication tokens in httpOnly cookies
- [ ] HTTPS enforced in production
- [ ] Error messages don't leak internal details

---

## Related Resources

- `~/.claude/rules/checklists/security-hardening.md` - Security hardening checklist
- `~/.claude/agents/security-auditor.md` - Security audit agent
- `~/.claude/skills/authentication-patterns/SKILL.md` - Auth patterns

---

_Secure by default. Validate at boundaries. Defense in depth._
