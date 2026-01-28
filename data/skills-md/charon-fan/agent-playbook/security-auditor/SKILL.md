---
name: security-auditor
description: Security vulnerability expert covering OWASP Top 10 and common security issues. Use when conducting security audits or reviewing code for vulnerabilities.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
metadata:
  hooks:
    after_complete:
      - trigger: self-improving-agent
        mode: background
        reason: "Learn from security patterns"
      - trigger: session-logger
        mode: auto
        reason: "Log security audit"
---

# Security Auditor

Expert in identifying security vulnerabilities following OWASP Top 10 and security best practices.

## When This Skill Activates

Activates when you:
- Request a security audit
- Mention "security" or "vulnerability"
- Need security review
- Ask about OWASP

## OWASP Top 10 Coverage

### A01: Broken Access Control

**Checks:**
```bash
# Check for missing auth on protected routes
grep -r "@RequireAuth\|@Protected" src/

# Check for IDOR vulnerabilities
grep -r "req.params.id\|req.query.id" src/

# Check for role-based access
grep -r "if.*role.*===" src/
```

**Common Issues:**
- Missing authentication on sensitive endpoints
- IDOR: Users can access other users' data
- Missing authorization checks
- API keys in URL

### A02: Cryptographic Failures

**Checks:**
```bash
# Check for hardcoded secrets
grep -ri "password.*=.*['\"]" src/
grep -ri "api_key.*=.*['\"]" src/
grep -ri "secret.*=.*['\"]" src/

# Check for weak hashing
grep -r "md5\|sha1" src/

# Check for http URLs
grep -r "http:\/\/" src/
```

**Common Issues:**
- Hardcoded credentials
- Weak hashing algorithms (MD5, SHA1)
- Unencrypted sensitive data
- HTTP instead of HTTPS

### A03: Injection

**Checks:**
```bash
# SQL injection patterns
grep -r "\".*SELECT.*+.*\"" src/
grep -r "\".*UPDATE.*SET.*+.*\"" src/

# Command injection
grep -r "exec(\|system(\|spawn(" src/
grep -r "child_process.exec" src/

# Template injection
grep -r "render.*req\." src/
```

**Common Issues:**
- SQL injection
- NoSQL injection
- Command injection
- XSS (Cross-Site Scripting)
- Template injection

### A04: Insecure Design

**Checks:**
```bash
# Check for rate limiting
grep -r "rateLimit\|rate-limit\|throttle" src/

# Check for 2FA
grep -r "twoFactor\|2fa\|mfa" src/

# Check for session timeout
grep -r "maxAge\|expires\|timeout" src/
```

**Common Issues:**
- No rate limiting on auth endpoints
- Missing 2FA for sensitive operations
- Session timeout too long
- No account lockout after failed attempts

### A05: Security Misconfiguration

**Checks:**
```bash
# Check for debug mode
grep -r "DEBUG.*=.*True\|debug.*=.*true" src/

# Check for CORS configuration
grep -r "origin.*\*" src/

# Check for error messages
grep -r "console\.log.*error\|console\.error" src/
```

**Common Issues:**
- Debug mode enabled in production
- Overly permissive CORS
- Verbose error messages
- Default credentials not changed

### A06: Vulnerable Components

**Checks:**
```bash
# Check package files
cat package.json | grep -E "\"dependencies\"|\"devDependencies\""
cat requirements.txt
cat go.mod

# Run vulnerability scanner
npm audit
pip-audit
```

**Common Issues:**
- Outdated dependencies
- Known vulnerabilities in dependencies
- Unused dependencies
- Unmaintained packages

### A07: Authentication Failures

**Checks:**
```bash
# Check password hashing
grep -r "bcrypt\|argon2\|scrypt" src/

# Check password requirements
grep -r "password.*length\|password.*complex" src/

# Check for password in URL
grep -r "password.*req\." src/
```

**Common Issues:**
- Weak password hashing
- No password complexity requirements
- Password in URL
- Session fixation

### A08: Software/Data Integrity

**Checks:**
```bash
# Check for subresource integrity
grep -r "integrity\|crossorigin" src/

# Check for signature verification
grep -r "verify.*signature\|validate.*token" src/
```

**Common Issues:**
- No integrity checks
- Unsigned updates
- Unverified dependencies

### A09: Logging Failures

**Checks:**
```bash
# Check for sensitive data in logs
grep -r "log.*password\|log.*token\|log.*secret" src/

# Check for audit trail
grep -r "audit\|activity.*log" src/
```

**Common Issues:**
- Sensitive data in logs
- No audit trail for critical operations
- Logs not protected
- No log tampering detection

### A10: SSRF (Server-Side Request Forgery)

**Checks:**
```bash
# Check for arbitrary URL fetching
grep -r "fetch(\|axios(\|request(\|http\\.get" src/

# Check for webhook URLs
grep -r "webhook.*url\|callback.*url" src/
```

**Common Issues:**
- No URL validation
- Fetching user-supplied URLs
- No allowlist for external calls

## Security Audit Checklist

### Code Review
- [ ] No hardcoded secrets
- [ ] Input validation on all inputs
- [ ] Output encoding for XSS prevention
- [ ] Parameterized queries for SQL
- [ ] Proper error handling
- [ ] Authentication on protected routes
- [ ] Authorization checks
- [ ] Rate limiting on public APIs

### Configuration
- [ ] Debug mode off
- [ ) HTTPS enforced
- [ ] CORS configured correctly
- [ ] Security headers set
- [ ] Environment variables for secrets
- [ ] Database not exposed

### Dependencies
- [ ] No known vulnerabilities
- [ ] Dependencies up to date
- [ ] Unused dependencies removed

## Scripts

Run security audit:
```bash
python scripts/security_audit.py
```

Check for secrets:
```bash
python scripts/find_secrets.py
```

## References

- `references/owasp.md` - OWASP Top 10 details
- `references/checklist.md` - Security audit checklist
- `references/remediation.md` - Vulnerability remediation guide
