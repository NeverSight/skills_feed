---
name: security-review-process
license: MIT
description: >
  Standardizes security review procedures for Ruby code mapped to OWASP Top 10:
  allowlist all input params before processing, forbid SQL interpolation (`#{}`),
  verify no secrets committed or logged, run `bundle exec bundle-audit check --update`,
  check for shell injection (`system()`, backticks, `exec()`), and discard instruction-like
  keys (`prompt`, `instructions`) in JSON payloads. Covers input validation, secrets
  management, and dependency audits. Trigger words: security review, check security,
  audit code, security vulnerability, secrets check, OWASP.
metadata:
  version: 1.0.0
  user-invocable: "true"
  type: "process-discipline"
---
# Security Review Process

## Security Gates & Quick Reference

| Area | Gate |
|------|------|
| **Input Validation** | Untrusted payloads must pass an allowlist filter before processing |
| **Secrets** | NO secrets may be committed or logged |
| **Injections** | Direct SQL interpolation (`#{id}`) is FORBIDDEN |
| **Dependencies** | Run `bundle-audit` before finalizing changes |

## Process Steps

### Step 1: Input Validation Audit
- Identify all entry points (controllers, API endpoints, webhooks, console runners).
- Verify every parameter is explicitly allowlisted and type-coerced if necessary.
- Ensure instruction-like keys (e.g. `prompt`, `instructions`) in JSON payloads are discarded or neutralized.

### Step 2: Injections Check
- Audit all database interactions:
  - Verify no raw SQL strings are built via string interpolation (`#{}`).
  - Confirm the database client's query parameterization features are used.
- Audit file and command executions:
  - Avoid dynamic shell commands via backticks, `system()`, or `exec()`. If necessary, pass arguments as separate array items.

### Step 3: Secrets and Logs Check
- Read configuration from environment variables (`ENV['SECRET']`) or secure config vaults — never raw literals.
- Verify sensitive data (passwords, tokens, personal identifiers) is filtered/redacted from log output.

### Step 4: Dependency and CVE Checks
- Scan project dependencies:
  ```bash
  bundle exec bundle-audit check --update
  ```
- If a vulnerability is reported, plan a safe version upgrade.

---

## Checkpoint Pattern

Align with the user:
1. **Security Vulnerability Assessment:** Present concerns categorized by threat vector (e.g. SQL injection, secrets leak).
2. **Mitigation Verification:** Once fixes are made, demonstrate how the parameterized query or filter blocks the exploit vector.

---

## Code Defenses Examples

### 1. Preventing SQL Injection
**Vulnerable:**
```ruby
db.execute("SELECT * FROM users WHERE name = '#{params[:name]}'")
```
**Secure:**
```ruby
db.execute("SELECT * FROM users WHERE name = ?", params[:name])
```

### 2. Preventing Shell Injection
**Vulnerable:**
```ruby
system("rm -rf #{params[:path]}")
```
**Secure:**
```ruby
system("rm", "-rf", params[:path])
```

---

## Integration

| Context | Next Skill |
|---------|----------|
| Standard code reviews | **review-process** |
| General TDD loops | **tdd-process** |
