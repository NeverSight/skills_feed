---
name: security-audit
description: Security review of application code, dependencies, configurations, and architecture. Covers OWASP Top 10, dependency scanning, secret management, authentication patterns, and API security. Use this skill when reviewing security of code, auditing dependencies for vulnerabilities, checking configuration security, assessing API endpoints, or answering security concerns about implementations. Triggers on "security", "audit", "vulnerability", "CVE", "OWASP", "injection", "XSS", "CSRF", "authentication security", "authorization flaw".
---

# Security Audit

Systematic security review for application code, dependencies, and configuration.

**This skill is NOT a replacement for professional penetration testing or security audits.** It identifies common vulnerabilities and provides remediation guidance within the scope of code review.

## Audit Process

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY AUDIT                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SCOPE           2. SCAN              3. ANALYZE         │
│  ┌─────────────┐   ┌─────────────┐      ┌─────────────┐    │
│  │ Define area │ → │ Run tools   │  →   │ Review      │    │
│  │ Set depth   │   │ Check deps  │      │ findings    │    │
│  │ Identify    │   │ Grep code   │      │ Classify    │    │
│  │ constraints │   │             │      │ severity    │    │
│  └─────────────┘   └─────────────┘      └─────────────┘    │
│                                                             │
│  4. REMEDIATE       5. DOCUMENT                             │
│  ┌─────────────┐   ┌─────────────┐                         │
│  │ Fix critical│ → │ Report      │                         │
│  │ Create      │   │ Create ohno │                         │
│  │ guidance    │   │ tasks       │                         │
│  └─────────────┘   └─────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Audit Types

| Type | Focus | When to Use |
|------|-------|-------------|
| Code Review | OWASP Top 10, injection, auth | New features, PRs, suspicious code |
| Dependency | CVEs, outdated packages | Before deploy, periodic, CI/CD |
| Configuration | Secrets, permissions, hardening | Infrastructure changes, new envs |
| Architecture | Attack surface, data flow | Design phase, major refactors |
| API Security | Auth, authz, rate limiting | New endpoints, public APIs |

## Quick Start Checklist

Run through this checklist for any security review:

### Critical (P0)
- [ ] No hardcoded secrets in code or config files
- [ ] SQL queries use parameterized statements
- [ ] User input is validated and sanitized
- [ ] Authentication tokens have expiration
- [ ] Sensitive routes require authentication
- [ ] Dependencies have no known critical CVEs

### High Priority (P1)
- [ ] CORS configured restrictively (not `*`)
- [ ] CSRF protection on state-changing operations
- [ ] Rate limiting on authentication endpoints
- [ ] Error messages don't leak internal details
- [ ] Logging doesn't include sensitive data
- [ ] File uploads validated (type, size, content)

### Medium Priority (P2)
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Cookies have Secure, HttpOnly, SameSite flags
- [ ] Password requirements meet standards
- [ ] Session timeout configured
- [ ] Input length limits enforced

## Severity Classification

| Severity | Definition | SLA | ohno Priority |
|----------|------------|-----|---------------|
| **Critical** | Exploitable, high impact (RCE, auth bypass, data breach) | 24-48h | P0 |
| **High** | Exploitable, significant impact (XSS, IDOR, SQLi) | 1 week | P1 |
| **Medium** | Exploitable with conditions, limited impact | 2-4 weeks | P2 |
| **Low** | Best practice violation, minimal risk | Backlog | P3 |
| **Info** | Observation, no direct security impact | Optional | — |

### Severity Decision Tree

```
Is there a known exploit?
├── Yes → Can attacker access sensitive data or execute code?
│         ├── Yes → Without authentication? → CRITICAL
│         │         └── With authentication → HIGH
│         └── Limited impact → MEDIUM
└── No → Is it a security best practice violation?
         ├── Could lead to future vulnerability → LOW
         └── Cosmetic/informational → INFO
```

## Code Review Patterns

### Injection Detection

Search patterns for common injection vulnerabilities:

```bash
# SQL Injection (string concatenation in queries)
grep -rn "SELECT.*\+" --include="*.ts" --include="*.js"
grep -rn "INSERT.*\+" --include="*.ts" --include="*.js"
grep -rn "query\s*(\s*['\`]" --include="*.ts" --include="*.js"

# Command Injection
grep -rn "exec\s*(" --include="*.ts" --include="*.js"
grep -rn "spawn\s*(" --include="*.ts" --include="*.js"
grep -rn "child_process" --include="*.ts" --include="*.js"

# Path Traversal
grep -rn "\.\./" --include="*.ts" --include="*.js"
grep -rn "req\.\(params\|query\|body\).*path" --include="*.ts"
```

### Authentication/Authorization Flaws

```bash
# Missing auth checks
grep -rn "router\.\(get\|post\|put\|delete\)" --include="*.ts" | grep -v "auth"

# Hardcoded credentials
grep -rn "password\s*=" --include="*.ts" --include="*.env*"
grep -rn "api_key\s*=" --include="*.ts" --include="*.js"
grep -rn "secret\s*=" --include="*.ts" --include="*.js"

# JWT issues
grep -rn "algorithm.*none" --include="*.ts" --include="*.js"
grep -rn "verify.*false" --include="*.ts" --include="*.js"
```

### Sensitive Data Exposure

```bash
# Logging sensitive data
grep -rn "console\.log.*password" --include="*.ts"
grep -rn "console\.log.*token" --include="*.ts"
grep -rn "logger.*req\.body" --include="*.ts"

# Exposing stack traces
grep -rn "stack" --include="*.ts" | grep -v "node_modules"
grep -rn "Error\s*(" --include="*.ts" | grep "res\.\(send\|json\)"
```

## Dependency Audit

### npm/Node.js

```bash
# Built-in audit
npm audit
npm audit --json > audit-results.json

# Check for outdated
npm outdated

# Detailed view of vulnerabilities
npm audit --audit-level=moderate
```

### Interpreting npm audit

| Severity | Action |
|----------|--------|
| Critical | Update immediately, block deploy |
| High | Update within 1 week |
| Moderate | Update within 1 month |
| Low | Track in backlog |

**False positives**: Some vulnerabilities are in dev dependencies or don't affect your usage. Document exclusions with justification.

### Python

```bash
# pip-audit
pip-audit
pip-audit --format=json > audit-results.json

# Safety check
safety check
safety check --full-report
```

**See [references/dependency-security.md](references/dependency-security.md) for Snyk integration, CI/CD setup, and CVE tracking.**

## Configuration Review

### Secrets Detection

```bash
# Git secrets scan
git secrets --scan

# Trufflehog (history scan)
trufflehog git file://. --json

# Gitleaks
gitleaks detect --source . --verbose
```

### Common Secret Patterns

| Type | Pattern | Risk |
|------|---------|------|
| AWS Keys | `AKIA[0-9A-Z]{16}` | Critical |
| GitHub Token | `ghp_[a-zA-Z0-9]{36}` | High |
| Slack Token | `xox[baprs]-` | High |
| Generic API Key | `[aA]pi[_-]?[kK]ey` | Medium |
| Private Key | `-----BEGIN.*PRIVATE KEY` | Critical |
| Connection String | `mongodb://`, `postgres://` | Critical |

**See [references/secrets-management.md](references/secrets-management.md) for proper secret management patterns.**

## API Security Checklist

### Authentication
- [ ] Tokens expire (reasonable TTL)
- [ ] Refresh token rotation implemented
- [ ] Password reset tokens single-use
- [ ] Account lockout after failed attempts
- [ ] Secure password storage (bcrypt, argon2)

### Authorization
- [ ] Every endpoint has explicit auth check
- [ ] Resource ownership validated (no IDOR)
- [ ] Role checks on sensitive operations
- [ ] API keys have scoped permissions

### Input Validation
- [ ] Request body schema validated
- [ ] Query params sanitized
- [ ] File uploads restricted (type, size)
- [ ] No arbitrary object property access

### Rate Limiting
- [ ] Auth endpoints rate limited
- [ ] API calls rate limited per user/IP
- [ ] Expensive operations throttled
- [ ] Rate limit headers exposed

**See [references/api-security.md](references/api-security.md) for detailed API security patterns.**

## Audit Report Template

```markdown
# Security Audit Report

## Summary
| Metric | Count |
|--------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |
| **Total** | X |

**Scope**: [What was audited]
**Date**: [Date]
**Auditor**: [Agent/Human]

## Critical Findings

### [VULN-001]: [Brief Title]
- **Severity**: Critical
- **Category**: [OWASP category]
- **Location**: `path/to/file.ts:123`
- **Description**: [What's wrong]
- **Impact**: [What an attacker could do]
- **Remediation**: [How to fix]
- **Code Sample**:
  ```typescript
  // Vulnerable
  const user = await db.query(`SELECT * FROM users WHERE id = ${id}`);
  
  // Fixed
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  ```

[Repeat for each finding]

## Recommendations

### Immediate Actions
1. [Action with ohno task link]

### Short-term (1-2 weeks)
1. [Action]

### Long-term
1. [Action]
```

## Integration with pokayokay

### Task Creation

Create ohno tasks for findings with appropriate priority:

```bash
# Critical finding
ohno add "VULN-001: SQL injection in user lookup" -p P0 -t security

# High finding  
ohno add "VULN-002: Missing rate limiting on /api/auth" -p P1 -t security

# Medium finding
ohno add "VULN-003: CORS configured too permissively" -p P2 -t security
```

### Skill Routing

This skill routes from:
- Keywords: "security", "audit", "vulnerability", "CVE"
- Task types containing "security" in `tasks.db`
- Features with security implications in their description

### Multi-Skill Workflow

Security audit often follows other skills:

```
1. api-design      → Design endpoints
2. security-audit  → Review endpoint security
3. api-testing     → Include security test cases
```

## Out of Scope

This skill does NOT cover:
- Penetration testing or active exploitation
- Compliance certifications (SOC2, HIPAA, PCI-DSS)
- Network security and firewall configuration
- Physical security
- Social engineering assessment
- Mobile app security (use platform-specific tools)

For compliance requirements, engage professional security auditors.

## References

- [references/owasp-top-10.md](references/owasp-top-10.md) — OWASP vulnerabilities with detection and fixes
- [references/dependency-security.md](references/dependency-security.md) — npm audit, pip-audit, Snyk, CI/CD integration
- [references/auth-patterns.md](references/auth-patterns.md) — Secure authentication and authorization patterns
- [references/api-security.md](references/api-security.md) — API-specific security concerns
- [references/secrets-management.md](references/secrets-management.md) — Handling sensitive configuration
