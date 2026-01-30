---
name: audit-code-health
description: Scans codebases for security vulnerabilities, bugs, and code health issues. Creates structured work items for remediation. Triggers on "audit", "code review", "security scan", "find bugs", "tech debt", or "assess code quality".
license: MIT
metadata:
  author: vercel
  version: '1.1.0'
---

# Code Health Auditor

Systematic audit process that scans directories to identify security issues, bugs, and code health problems. Findings are tracked as work items for remediation.

## Quick Start

Example: `For @native-yield-operations/automation-service/ do /audit-code-health`

1. **Scan** the target directory for issues
2. **Document** findings in a table (Security → Bugs → Code Health)
3. **File** work items or create a findings summary

For deeper audits, follow the [Workflow](#workflow-overview) below.

## When to Apply

Use this skill when:

- Auditing a codebase for security vulnerabilities
- Identifying bugs and edge cases
- Assessing technical debt and code health
- Creating structured work items for remediation
- Running systematic code reviews

## When NOT to Apply

Do not use this skill when:

- Developing a new feature
- Writing a new test

## Core Principles

1. **Audit only, no fixes**: Discover and document—never modify code
2. **Track everything**: All findings become work items
3. **Scoped analysis**: Stay within the target directory unless context requires external references
4. **Prioritize by impact**: Security → Bugs → Code Health

## Audit Categories by Priority

| Priority | Category    | Severity | Reference                                          |
| -------- | ----------- | -------- | -------------------------------------------------- |
| 1        | Security    | CRITICAL | [security-issues.md](reference/security-issues.md) |
| 2        | Bugs        | HIGH     | [bugs-checklist.md](reference/bugs-checklist.md)   |
| 3        | Code Health | MEDIUM   | [code-health.md](reference/code-health.md)         |

## Quick Reference

### Security Issues (CRITICAL)

- Auth/authz errors
- Injection risks (SQL, command, XSS)
- SSRF, path traversal
- Secrets or insecure defaults
- Broken crypto usage
- Missing input validation
- Dependency vulnerabilities

### Bugs (HIGH)

- Edge cases and boundary conditions
- Concurrency / race conditions
- Error handling gaps
- Resource leaks
- Numeric overflow/underflow
- Retry / timeout bugs

### Code Health (MEDIUM)

- Oversized or high-complexity modules
- Low test coverage near critical logic
- Duplicated abstractions
- Dead code or unused exports
- Poor documentation
- Misleading names

## Related Skills

- **Smart Contracts**: If you detect `*.sol` files, use the `developing-smart-contracts` skill for Solidity-specific security patterns
- **Unit Testing**: Use the `unit-testing-guidelines` skill to assess test quality and coverage gaps

## Workflow Overview

Audits run in cycles. Choose depth based on scope:

| Scope          | Cycles | When to Use                            |
| -------------- | ------ | -------------------------------------- |
| Quick scan     | 1-2    | Small PRs, single files, targeted review |
| Standard audit | 3-5    | Feature modules, API surfaces          |
| Deep audit     | 6-10   | Full codebase, security-critical systems |

Each cycle follows: **SCAN → FINDINGS → VERIFY → FILE → TRIAGE**

## Cycle Process

For each cycle, execute these steps:

```
Cycle Progress:
- [ ] Step 1: SCAN - Inspect target directory
- [ ] Step 2: FINDINGS - Document issues by category
- [ ] Step 3: VERIFY - Validate findings before filing
- [ ] Step 4: FILE - Create work items
- [ ] Step 5: TRIAGE - Assign priorities
```

### Step 1: SCAN

Analyze the target directory:

- Review code for security issues, bugs, and health problems
- Run read-only tooling: build, tests, lint, typecheck
- Use `code-simplifier` on hotspots (if available)

### Step 2: FINDINGS

Produce a findings table grouped by Security, Bugs, Code Health:

| Severity | Type     | File(s)       | Description        | Confidence |
| -------- | -------- | ------------- | ------------------ | ---------- |
| P0       | Security | `auth/jwt.ts` | Token not verified | High       |

### Step 3: VERIFY

Before filing, validate each finding:

- [ ] Confirmed the issue exists (not a false positive)
- [ ] Identified the correct file and line number
- [ ] Assessed severity accurately
- [ ] Checked if issue is already tracked

### Step 4: FILE

Create work items for verified findings.

**If using Beads (`bd`):**
- See [beads-format.md](reference/beads-format.md) for epic/issue structure
- Use `bd` commands to create and link items

**If bd is not available:**
- Use Markdown task lists for tracking findings
- Format: `- [ ] [P0/Security] auth/jwt.ts: Token not verified`

### Step 5: TRIAGE

- Assign P0/P1/P2 priorities
- Identify quick wins vs deep refactors
- Group related issues under epics (if using bd)

## Output Format

Each cycle produces:

```markdown
## Cycle N Summary

### Findings Table
| Severity | Type | File(s) | Description | Confidence | Status |

### Work Items Created
- [P0] ...
- [P1] ...

### Triage Notes
...

### Backlog Overview
Open items grouped by priority
```

## Constraints

- **DO NOT** implement code changes
- **STAY WITHIN** target directory unless minimal external context needed
- **PREFER** many small issues over large vague ones
- **VERIFY** findings before filing to avoid false positives

## Reference Files

- [Security Issues Checklist](reference/security-issues.md)
- [Bugs Checklist](reference/bugs-checklist.md)
- [Code Health Checklist](reference/code-health.md)
- [Beads Format Guide](reference/beads-format.md)
- [Audit Examples](reference/examples.md)
