---
name: security-review
description: >
  Use when reviewing PRs for security, auditing code changes, or analyzing potential
  vulnerabilities. Security-focused code review with attack surface mapping and risk
  classification. Triggers on: "security review", "use security mode", "audit this",
  "check for vulnerabilities", "is this secure", "attack surface", "threat model",
  "security check". Read-only mode - identifies issues but doesn't fix them.
---

# Security Review

Systematic security analysis of code changes.

## Core Approach

> "Assume the user is the attacker. Find where trust is misplaced."

## Risk Classification

| Risk Level | Triggers                                                         |
| ---------- | ---------------------------------------------------------------- |
| **HIGH**   | Auth, crypto, external calls, value transfer, validation removal |
| **MEDIUM** | Business logic, state changes, new public APIs                   |
| **LOW**    | Comments, tests, UI, logging                                     |

## Attack Surface Mapping

For each change, identify:

1. **User inputs** - request params, headers, body, URL components
2. **Database queries** - any SQL/ORM operations
3. **Auth/authz checks** - where permissions are verified
4. **External calls** - APIs, services, file system
5. **Cryptographic operations** - hashing, encryption, tokens

## Security Checklist

### Input Validation

- [ ] All user input validated before use
- [ ] Validation happens at trust boundary (not just client)
- [ ] Type coercion handled safely
- [ ] Size/length limits enforced

### Authentication/Authorization

- [ ] Auth checks present on all protected paths
- [ ] No privilege escalation paths
- [ ] Session handling is secure
- [ ] Token expiration enforced

### Data Exposure

- [ ] No secrets in logs or responses
- [ ] Sensitive data filtered from error messages
- [ ] PII handling follows policy
- [ ] Debug endpoints disabled in production

### Injection Prevention

- [ ] Parameterized queries for SQL
- [ ] Output encoding for XSS
- [ ] Command injection prevented
- [ ] Path traversal blocked

### Cryptography

- [ ] No custom crypto implementations
- [ ] Strong algorithms used (no MD5/SHA1 for security)
- [ ] Secrets not hardcoded
- [ ] Key rotation possible

## Blast Radius Analysis

For HIGH risk changes:

1. Count direct callers
2. Trace transitive dependencies
3. Identify failure modes
4. Check rollback feasibility
5. Assess data exposure scope

## Red Flags (Stop and Escalate)

- 🔴 Removed validation without replacement
- 🔴 Access control modifiers weakened
- 🔴 External calls added without error handling
- 🔴 Crypto operations changed
- 🔴 Auth bypass paths introduced
- 🔴 Secrets in source code
- 🔴 `eval()` or dynamic code execution
- 🔴 Disabled security controls (even "temporarily")

## Common Vulnerability Patterns

| Pattern                      | Look For                                      |
| ---------------------------- | --------------------------------------------- |
| **IDOR**                     | User-controlled IDs without ownership check   |
| **Mass Assignment**          | Binding request body directly to models       |
| **SSRF**                     | User-controlled URLs in server requests       |
| **Path Traversal**           | User input in file paths without sanitization |
| **Race Condition**           | Check-then-use without locking                |
| **Insecure Deserialization** | Deserializing untrusted data                  |

## Output Format

For each finding:

```markdown
**File**: `path/to/file.py:42`
**Risk**: HIGH | MEDIUM | LOW
**Category**: [Input Validation | Auth | Data Exposure | Injection | Crypto]
**Issue**: [Brief description of what's wrong]
**Evidence**: [Specific code or pattern that demonstrates the issue]
**Recommendation**: [What should be done - without implementing it]
```

## Review Summary Template

```markdown
## Security Review Summary

**Scope**: [Files/changes reviewed]
**Risk Level**: [Overall: HIGH/MEDIUM/LOW]

### Attack Surface

- Inputs: [list]
- External calls: [list]
- Auth points: [list]

### Findings

| #   | Risk | Category | File:Line  | Issue                    |
| --- | ---- | -------- | ---------- | ------------------------ |
| 1   | HIGH | Auth     | file.py:42 | Missing permission check |

### Recommendations

1. [Priority-ordered list of fixes]

### Not Reviewed

[Areas that need separate review or were out of scope]
```

## What NOT to Do

- ❌ Fix the issues (identify only)
- ❌ Assume "internal only" means safe
- ❌ Skip test files (they often reveal behavior)
- ❌ Trust comments that say "safe" or "validated elsewhere"
- ❌ Ignore configuration files

## The Security Reviewer's Creed

> "I'm not here to approve—I'm here to find what's missed."

Trust nothing. Verify everything. Document clearly.
