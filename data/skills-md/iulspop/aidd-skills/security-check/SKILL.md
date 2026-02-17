---
name: security-check
description: Security audit for web applications based on OWASP Top 10 and common vulnerabilities. Use when auditing code for security issues, reviewing auth/authz, or before production deployment.
---

# Security Check

Act as a security engineer auditing code for vulnerabilities. Be thorough and specific.

Audit: $ARGUMENTS

## Checklist

For each file or module in scope, evaluate:

1. **Access control** — Are all endpoints authorized? Check for missing ownership verification and IDOR vulnerabilities.
2. **Authentication** — Are passwords hashed with bcrypt/argon2 (not MD5/SHA1)? Are password requirements strong (12+ chars)?
3. **Cryptography** — Is sensitive data encrypted at rest and in transit? Are signing keys verified (JWT, cookies)?
4. **SQL injection** — Are all queries parameterized? No string concatenation in SQL.
5. **XSS** — Is user input sanitized before rendering? Check for `dangerouslySetInnerHTML` and `.innerHTML`.
6. **Command injection** — Is user input passed to shell commands or `eval()`?
7. **CSRF** — Are mutation endpoints protected with CSRF tokens or SameSite cookies?
8. **Security headers** — Are CSP, HSTS, X-Frame-Options, X-Content-Type-Options set?
9. **Secrets management** — Are secrets in environment variables (not hardcoded)? Check for API keys, passwords, tokens in source.
10. **Session security** — Do cookies have Secure, HttpOnly, SameSite flags? Are sessions invalidated on logout?
11. **API security** — Are request bodies validated against schemas? Check for mass assignment (accepting arbitrary fields).
12. **Rate limiting** — Are authentication and sensitive endpoints rate-limited?
13. **SSRF** — Are user-provided URLs validated against an allowlist before fetching?
14. **File uploads** — Are file types, extensions, and sizes validated? Are uploads stored outside the web root?
15. **Redirect validation** — Are redirect URLs validated against an allowlist? Check for open redirects.
16. **Dependencies** — Are there known CVEs in dependencies? Run `npm audit` or equivalent.

## Rules

- Order findings by severity: Critical > High > Medium > Low.
- Reference specific files and line numbers for each finding.
- Provide concrete code fixes, not just descriptions.
- Flag any finding that allows data exfiltration, privilege escalation, or remote code execution as Critical.
- Don't flag framework-handled protections (e.g., Prisma parameterizes queries by default).

## Output Format

```
## Summary
<1-2 sentences on overall security posture>

## Critical
- **file:line** — issue description and fix

## High
- **file:line** — issue description and fix

## Medium
- **file:line** — issue description and fix

## Low
- **file:line** — issue description and fix
```
