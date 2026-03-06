---
name: security
description: Security audits, vulnerability detection, and secure coding. Use for security reviews, auth implementation, or OWASP compliance.
---

# Security Audit

Identify vulnerabilities and implement secure coding practices.

## When to Use

- Security review of code or architecture
- Implementing authentication/authorization
- Before deploying to production
- User asks about security best practices
- Handling sensitive data

## OWASP Top 10 Checklist

1. **Injection** - Parameterized queries, input sanitization
2. **Broken Auth** - Strong sessions, MFA, secure password storage
3. **Sensitive Data** - Encryption at rest and transit, minimal exposure
4. **XXE** - Disable external entities, use JSON over XML
5. **Broken Access Control** - RBAC, deny by default
6. **Misconfiguration** - Secure defaults, remove debug info
7. **XSS** - Output encoding, CSP headers
8. **Insecure Deserialization** - Validate input, avoid native serialization
9. **Vulnerable Components** - Dependency scanning, updates
10. **Logging** - Audit logs, no sensitive data in logs

## Security Headers

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Auth Implementation

```javascript
// Password hashing
const hash = await bcrypt.hash(password, 12);

// JWT with short expiry
const token = jwt.sign({ userId }, secret, { expiresIn: "15m" });

// Refresh token rotation
const refreshToken = crypto.randomBytes(32).toString("hex");
```

## Audit Output Format

```markdown
## Security Audit Report

**Severity Levels:** Critical | High | Medium | Low

### Critical

- [Issue]: [Description] → [Fix]

### High

- [Issue]: [Description] → [Fix]

### Recommendations

- [Improvement suggestion]
```

## Examples

**Input:** "Review auth implementation"
**Action:** Check password storage, session management, token handling, report findings

**Input:** "Make this API secure"
**Action:** Add input validation, auth checks, rate limiting, security headers
