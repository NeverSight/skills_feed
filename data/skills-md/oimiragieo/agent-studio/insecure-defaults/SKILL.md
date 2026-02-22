---
name: insecure-defaults
description: Detect hardcoded credentials, default passwords, fail-open configurations, insecure default settings, and other security misconfigurations that ship as default behavior in applications.
version: 1.0.0
model: sonnet
invoked_by: agent
tools: [Read, Write, Edit, Bash, Glob, Grep]
source: trailofbits/skills
source_license: CC-BY-SA-4.0
source_url: https://github.com/trailofbits/skills/tree/main/skills/insecure-defaults
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

<!-- Source: Trail of Bits | License: CC-BY-SA-4.0 | Adapted: 2026-02-09 -->
<!-- Agent: security-architect | Task: #4 | Session: 2026-02-09 -->

# Insecure Defaults

## Security Notice

**AUTHORIZED USE ONLY**: These skills are for DEFENSIVE security analysis and authorized research:

- **Configuration auditing** for owned applications
- **Pre-deployment security checks** in CI/CD pipelines
- **Compliance validation** (SOC2, PCI-DSS, HIPAA)
- **Security assessment** of third-party components
- **Educational purposes** in controlled environments

**NEVER use for**:

- Exploiting discovered credentials without authorization
- Accessing systems using found default passwords
- Circumventing security controls
- Any illegal activities

<identity>
You are an insecure defaults detection expert. You systematically identify hardcoded credentials, default passwords, fail-open configurations, weak cryptographic defaults, overly permissive access controls, and other security misconfigurations that ship as default behavior. You understand that insecure defaults are among the most common and easily exploitable vulnerability classes (OWASP A05: Security Misconfiguration).
</identity>

<capabilities>
- Detect hardcoded credentials (passwords, API keys, tokens, certificates)
- Identify default passwords and factory-set credentials
- Find fail-open error handling (errors that grant access instead of denying)
- Detect insecure cryptographic defaults (weak algorithms, short keys, ECB mode)
- Identify overly permissive default configurations (CORS *, 0.0.0.0 binding, debug mode)
- Find missing security headers and protections
- Detect disabled security features (CSRF, rate limiting, TLS verification)
- Identify insecure default file permissions
- Scan configuration files for security misconfigurations
- Report findings with severity classification and remediation guidance
</capabilities>

<instructions>

## Step 1: Credential Detection

### Hardcoded Credential Patterns

Search for credentials embedded directly in source code:

```bash
# Password patterns
grep -rnE "(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{3,}" --include="*.{js,ts,py,java,go,rb,php}" .

# API key patterns
grep -rnE "(api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*['\"][^'\"]{8,}" --include="*.{js,ts,py,java,go}" .

# Token patterns
grep -rnE "(token|secret|auth)\s*[=:]\s*['\"][A-Za-z0-9+/=]{16,}" --include="*.{js,ts,py,java,go}" .

# AWS credentials
grep -rnE "AKIA[0-9A-Z]{16}" .
grep -rnE "aws_secret_access_key\s*[=:]\s*['\"][^'\"]{20,}" .

# Private keys
grep -rnl "BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY" .

# Connection strings with embedded credentials
grep -rnE "(mysql|postgres|mongodb|redis)://[^:]+:[^@]+@" --include="*.{js,ts,py,java,go,yml,yaml,json,env}" .
```

### Semgrep Rules for Credential Detection

```yaml
rules:
  - id: hardcoded-password
    message: >
      Hardcoded password detected. Store passwords in environment
      variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault).
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-798]
      owasp: [A07:2021]
      confidence: HIGH
      impact: HIGH
      category: security
    patterns:
      - pattern-either:
          - pattern: |
              $VAR = "..."
          - pattern: |
              const $VAR = "..."
          - pattern: |
              let $VAR = "..."
      - metavariable-regex:
          metavariable: $VAR
          regex: (?i)(password|passwd|pwd|secret|credential|api.?key)
      - pattern-not: |
          $VAR = ""
      - pattern-not: |
          $VAR = "changeme"
      - pattern-not: |
          $VAR = "placeholder"

  - id: hardcoded-password-in-config
    message: >
      Password found in configuration file. Use environment variable
      references or encrypted secrets instead.
    severity: ERROR
    languages: [json, yaml]
    metadata:
      cwe: [CWE-798]
      owasp: [A07:2021]
      confidence: MEDIUM
      impact: HIGH
      category: security
    pattern-regex: (?i)(password|secret|api.?key|token)\s*[:=]\s*["']?[a-zA-Z0-9+/=!@#$%^&*]{8,}
```

## Step 2: Fail-Open Detection

### What is Fail-Open?

Fail-open occurs when error handling defaults to **granting access** instead of **denying access**. This is the opposite of the "fail-secure" principle.

### Fail-Open Patterns

```javascript
// FAIL-OPEN: Error in auth check grants access
try {
  const isAuthorized = await checkAuth(req);
  if (!isAuthorized) return res.status(403).send('Forbidden');
} catch (err) {
  // BUG: Error falls through, request proceeds without auth
  console.log('Auth error:', err);
}
// ... handler continues, even on auth error

// FAIL-SECURE: Error in auth check denies access
try {
  const isAuthorized = await checkAuth(req);
  if (!isAuthorized) return res.status(403).send('Forbidden');
} catch (err) {
  console.error('Auth error:', err);
  return res.status(500).send('Internal error'); // DENY on error
}
```

### Semgrep Rules for Fail-Open

```yaml
rules:
  - id: fail-open-auth-catch
    message: >
      Authentication/authorization error is caught but execution continues.
      This is a fail-open pattern. Ensure errors in auth checks result
      in access denial, not access grant.
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-636]
      owasp: [A07:2021]
      confidence: MEDIUM
      impact: HIGH
      category: security
    patterns:
      - pattern: |
          try {
            ...
            $AUTH(...)
            ...
          } catch ($ERR) {
            ...
          }
          ...
          $RESPONSE(...)
      - metavariable-regex:
          metavariable: $AUTH
          regex: (?i)(auth|authenticate|authorize|checkPermission|verifyToken|validateSession)
      - pattern-not-inside: |
          try { ... } catch ($ERR) { ... return ...; }
      - pattern-not-inside: |
          try { ... } catch ($ERR) { ... throw ...; }

  - id: fail-open-empty-catch
    message: >
      Empty catch block silently swallows errors. This can cause
      fail-open behavior if the try block contains security checks.
    severity: WARNING
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-390]
      confidence: MEDIUM
      impact: MEDIUM
      category: security
    pattern: |
      try { ... } catch ($ERR) { }
```

## Step 3: Insecure Configuration Detection

### Common Insecure Defaults

| Category        | Insecure Default                   | Secure Alternative                |
| --------------- | ---------------------------------- | --------------------------------- |
| **CORS**        | `origin: '*'`                      | Explicit allowed origins          |
| **Debug**       | `debug: true` in production        | `debug: false`                    |
| **Binding**     | `0.0.0.0` (all interfaces)         | `127.0.0.1` or specific IP        |
| **TLS**         | `rejectUnauthorized: false`        | `rejectUnauthorized: true`        |
| **Cookies**     | `secure: false`, `httpOnly: false` | `secure: true`, `httpOnly: true`  |
| **Session**     | `secret: 'keyboard cat'`           | Random secret from env var        |
| **Crypto**      | MD5, SHA1, DES, RC4                | SHA-256+, AES-256, ChaCha20       |
| **Permissions** | `0777` file permissions            | `0644` or `0600`                  |
| **JWT**         | `algorithm: 'none'`                | `algorithm: 'RS256'` or `'ES256'` |
| **Rate limit**  | No rate limiting                   | Rate limiting enabled             |
| **CSRF**        | CSRF protection disabled           | CSRF protection enabled           |
| **Helmet**      | No security headers                | Helmet middleware enabled         |

### Semgrep Rules for Insecure Config

```yaml
rules:
  - id: cors-wildcard-origin
    message: >
      CORS allows all origins ('*'). This permits any website to make
      cross-origin requests. Specify allowed origins explicitly.
    severity: WARNING
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-942]
      owasp: [A05:2021]
      confidence: HIGH
      impact: MEDIUM
      category: security
    pattern-either:
      - pattern: cors({ origin: '*' })
      - pattern: cors({ origin: true })
      - pattern: |
          $RES.setHeader("Access-Control-Allow-Origin", "*")

  - id: tls-verification-disabled
    message: >
      TLS certificate verification is disabled. This allows
      man-in-the-middle attacks. Remove rejectUnauthorized: false.
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-295]
      owasp: [A02:2021]
      confidence: HIGH
      impact: HIGH
      category: security
    pattern-either:
      - pattern: rejectUnauthorized: false
      - pattern: process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'
      - pattern: process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'

  - id: debug-mode-enabled
    message: >
      Debug mode appears to be enabled. Ensure debug mode is
      disabled in production to prevent information disclosure.
    severity: WARNING
    languages: [javascript, typescript, python]
    metadata:
      cwe: [CWE-489]
      owasp: [A05:2021]
      confidence: MEDIUM
      impact: MEDIUM
      category: security
    pattern-either:
      - pattern: "DEBUG = True"
      - pattern: "debug: true"
      - pattern: app.debug = true

  - id: weak-crypto-algorithm
    message: >
      Weak cryptographic algorithm detected. Use SHA-256 or stronger
      for hashing, AES-256 for encryption.
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: [CWE-327]
      owasp: [A02:2021]
      confidence: HIGH
      impact: HIGH
      category: security
    patterns:
      - pattern: crypto.createHash($ALGO)
      - metavariable-regex:
          metavariable: $ALGO
          regex: ['"]?(md5|sha1|md4|md2|ripemd)['"]?
```

## Step 4: Environment and Configuration File Scanning

### Files to Check

```bash
# Environment files
find . -name "*.env*" -not -path "*/node_modules/*"
find . -name ".env.example" -o -name ".env.sample"

# Configuration files
find . -name "config.*" -o -name "settings.*" -o -name "application.*" \
  | grep -E "\.(js|ts|json|yaml|yml|toml|ini|cfg)$"

# Docker configurations
find . -name "Dockerfile*" -o -name "docker-compose*"

# Cloud configurations
find . -name "*.tf" -o -name "*.tfvars" \
  -o -name "serverless.*" -o -name "*.cloudformation.*"
```

### Configuration Audit Checklist

```markdown
## Configuration Security Audit

### Credentials

- [ ] No hardcoded passwords in source code
- [ ] No API keys in source code
- [ ] No private keys committed
- [ ] No database credentials in config files
- [ ] .env files are in .gitignore
- [ ] .env.example has placeholder values only

### Network

- [ ] Not binding to 0.0.0.0 in production
- [ ] TLS/SSL enabled for all connections
- [ ] Certificate verification enabled
- [ ] CORS restricted to known origins

### Authentication

- [ ] Session secret is random and from env var
- [ ] JWT algorithm is not 'none'
- [ ] Password hashing uses bcrypt/argon2 (not MD5/SHA1)
- [ ] Cookie settings: secure, httpOnly, sameSite

### Error Handling

- [ ] Auth errors deny access (fail-secure)
- [ ] No empty catch blocks in security paths
- [ ] Stack traces not exposed in production
- [ ] Default error handler returns 500, not 200

### Infrastructure

- [ ] Debug mode disabled in production
- [ ] File permissions are restrictive
- [ ] Default admin accounts disabled/changed
- [ ] Rate limiting enabled
- [ ] Security headers configured (Helmet/equivalent)
```

## Step 5: Reporting

### Insecure Defaults Report

```markdown
## Insecure Defaults Assessment

**Date**: YYYY-MM-DD
**Scope**: [project/repository]

### Summary

| Category              | Findings | Critical | High  | Medium | Low   |
| --------------------- | -------- | -------- | ----- | ------ | ----- |
| Hardcoded credentials | X        | X        | X     | X      | X     |
| Fail-open patterns    | X        | X        | X     | X      | X     |
| Insecure config       | X        | X        | X     | X      | X     |
| Weak crypto           | X        | X        | X     | X      | X     |
| **Total**             | **X**    | **X**    | **X** | **X**  | **X** |

### Critical Findings

[Detailed findings with remediation]

### Recommended Secure Defaults

[Project-specific secure configuration template]
```

</instructions>

## Default Credential Databases

When auditing for default credentials, check against known defaults:

| Product/Service | Default Username | Default Password     |
| --------------- | ---------------- | -------------------- |
| PostgreSQL      | `postgres`       | `postgres`           |
| MySQL           | `root`           | (empty)              |
| MongoDB         | (none)           | (none - no auth)     |
| Redis           | (none)           | (none - no auth)     |
| RabbitMQ        | `guest`          | `guest`              |
| Elasticsearch   | `elastic`        | `changeme`           |
| Jenkins         | `admin`          | (from initial setup) |
| Grafana         | `admin`          | `admin`              |

**Rule**: If your application ships with any of these defaults, flag as CRITICAL.

## Related Skills

- [`static-analysis`](../static-analysis/SKILL.md) - CodeQL and Semgrep scanning
- [`variant-analysis`](../variant-analysis/SKILL.md) - Finding variants of insecure patterns
- [`semgrep-rule-creator`](../semgrep-rule-creator/SKILL.md) - Custom detection rules
- [`differential-review`](../differential-review/SKILL.md) - Detecting new insecure defaults in diffs
- [`security-architect`](../security-architect/SKILL.md) - STRIDE threat modeling
- [`auth-security-expert`](../auth-security-expert/SKILL.md) - Authentication best practices

## Agent Integration

- **security-architect** (primary): Security configuration assessment
- **code-reviewer** (primary): Configuration review in PRs
- **penetration-tester** (secondary): Credential verification
- **devops** (secondary): Infrastructure configuration auditing

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
