---
name: security-review
description: Security audit for vulnerabilities, compliance issues, and sensitive data exposure. Use before production deployments or when reviewing security-sensitive code.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Review

Comprehensive security audit for the MuRP codebase.

## Security Checklist

### Authentication & Authorization
- [ ] No hardcoded credentials
- [ ] API keys only in environment variables
- [ ] Proper token handling
- [ ] RLS policies on Supabase tables

### Data Protection
- [ ] No sensitive data in logs
- [ ] PII properly handled
- [ ] Encryption for sensitive fields
- [ ] Input sanitization

### API Security
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS protection
- [ ] CSRF tokens where needed
- [ ] Rate limiting configured

### Dependencies
- [ ] Run `npm audit`
- [ ] Check for known vulnerabilities
- [ ] Verify dependency integrity

### Infrastructure
- [ ] Environment variables not exposed to frontend
- [ ] Edge functions use proper auth
- [ ] Webhook endpoints validated

## Scan Commands

```bash
# Check for hardcoded secrets
grep -r "sk_" --include="*.ts" --include="*.tsx" .
grep -r "password.*=" --include="*.ts" --include="*.tsx" .

# Check npm vulnerabilities
npm audit

# Check for console.log with sensitive data
grep -r "console.log.*token\|password\|secret" --include="*.ts" .
```

## Report Format

| Severity | File | Issue | Remediation |
|----------|------|-------|-------------|
| Critical | path | desc  | fix         |

## Trigger Phrases

- "security review"
- "security audit"
- "check for vulnerabilities"
- "/security-review"
