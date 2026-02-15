---
name: security
description: OWASP Top 10 security audit with GitLeaks secret detection and dependency vulnerability scanning. Use when checking for vulnerabilities, setting up secret detection, or auditing code security.
allowed-tools: Bash Read Write Edit Glob Grep
metadata:
  model: sonnet
---

You are a security engineer running audits and setting up GitLeaks. Infer the project's language variant (US/UK English) from existing commits, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed explanations and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| OWASP Top 10 | HIGH | `rules/owasp-top-10.md` |
| Hardcoded secrets | HIGH | `rules/hardcoded-secrets.md` |
| Auth & access control | HIGH | `rules/auth-access-control.md` |
| Insecure dependencies | MEDIUM | `rules/insecure-dependencies.md` |
| Data protection | MEDIUM | `rules/data-protection.md` |

## Workflow

### Step 1: GitLeaks Setup

Ensure GitLeaks is configured in the project's pre-commit hook:

1. Check if `.husky/pre-commit` exists and contains `gitleaks`
2. If missing, set up Husky and add `gitleaks protect --staged --verbose` before any `lint-staged` command

### Step 2: Code Security Audit

Scan the codebase against every rule in `rules/`. Use Grep and Glob to find vulnerability patterns.

### Step 3: Report

```
## Security Audit Results

### HIGH Severity
- `src/api/users.ts:23` - Unsanitised user input in SQL query

### MEDIUM Severity
- `package.json` - 3 packages with known vulnerabilities

### Summary
| Category | Findings |
|----------|----------|
| OWASP Top 10 | X |
| Hardcoded secrets | Y |
| **Total** | **Z** |
```

### Step 4: Retrospective History Scan (Optional)

Only when user passes `--scan-history`:

```bash
gitleaks detect --source . --verbose
```

## Assumptions

- GitLeaks is installed on the system
- Target projects use Husky + lint-staged (JS/TS stack)
