---
name: code-review
description: Review code written by Claude Code or humans across multiple languages. Use when asked to review, audit, critique, or analyze code quality. Supports R, Python, JavaScript, SQL, C++, Rust, Go, Ansible, Kustomize/Kubernetes, Dockerfiles, Docker Compose, and Bash. Covers correctness, security, performance, testing, documentation, and architecture. Produces actionable output for Claude Code to fix issues plus human-readable REVIEW.md summaries.
---

# Code Review Skill

Review code for correctness, security, performance, testing, documentation, and architecture. Produces two outputs:
1. **Structured findings** for Claude Code to act on
2. **REVIEW.md** human-readable summary

## Review Workflow

### 0. MANDATORY: Use context7 Before Any Code Changes

**CRITICAL**: Before creating, editing, or suggesting code changes, ALWAYS use context7 to look up current documentation.

**When to use context7:**
- Before suggesting fixes or improvements
- When reviewing library/framework usage
- Before writing code examples or snippets
- When uncertain about API behavior or best practices

**How to use:**
```
1. Resolve library: context7 resolve <library-name>
2. Get docs: context7 get-library-docs --library <library> --topic <topic>
```

**Example:**
```
context7 resolve react
context7 get-library-docs --library react --topic "useEffect dependencies"
```

### 1. Determine Review Scope

Identify what's being reviewed:
- **Single file**: Review that file
- **Directory**: Review all relevant files
- **Diff/PR**: Focus on changed lines with surrounding context
- **Entire codebase**: Start with entry points, follow dependencies

### 2. Select Review Depth

Choose automatically based on context, or accept user override:

| Depth | When to Use | Focus |
|-------|-------------|-------|
| **Quick** | Small changes, trivial files, time-sensitive | Critical issues only |
| **Standard** | Most reviews, single files, typical PRs | All categories, balanced |
| **Deep** | Pre-production, security-sensitive, complex systems | Exhaustive, security-focused |

### 3. Detect Languages and Load References

Identify languages present, then load relevant reference files:

- **R** → [references/r.md](references/r.md)
- **Python** → [references/python.md](references/python.md)
- **JavaScript** → [references/javascript.md](references/javascript.md)
- **SQL** → [references/sql.md](references/sql.md)
- **C++** → [references/cpp.md](references/cpp.md)
- **Rust** → [references/rust.md](references/rust.md)
- **Go** → [references/go.md](references/go.md)
- **Ansible** → [references/ansible.md](references/ansible.md)
- **Kubernetes/Kustomize** → [references/kubernetes.md](references/kubernetes.md)
- **Dockerfile** → [references/dockerfile.md](references/dockerfile.md)
- **Docker Compose** → [references/docker-compose.md](references/docker-compose.md)
- **Bash** → [references/bash.md](references/bash.md)

### 4. Use context7 MCP for Documentation (MANDATORY)

**ALWAYS query context7 when:**
- Reviewing ANY library/framework usage (not just unfamiliar ones)
- Before suggesting code changes or fixes
- Checking if APIs are used correctly
- Verifying deprecated patterns
- Confirming best practices for specific versions
- Writing code examples or snippets in review feedback

**Process:**
1. Identify libraries/frameworks in the code being reviewed
2. Use `context7 resolve <library>` for each one
3. Use `context7 get-library-docs` to verify API usage and patterns
4. Only THEN proceed with review findings

**Example queries:**
- `context7 resolve react` then `context7 get-library-docs --library react --topic "hooks"`
- `context7 resolve tensorflow` then `context7 get-library-docs --library tensorflow --topic "layers"`
- `context7 resolve tidyverse` for R tidyverse patterns
- `context7 resolve kubernetes` for K8s manifest validation
- `context7 resolve express` for Node.js API patterns

**Never skip this step** - outdated or incorrect documentation can lead to poor review suggestions.

### 5. Spawn Subagents for Parallel Review

Use subagents to parallelize review work:

**Language Subagent** (one per language detected):
```
Task: Review [language] code in [files] for idioms, patterns, and language-specific issues.
Focus: Style, idioms, language-specific performance, common pitfalls.
Reference: Load references/[language].md
Output: Structured findings list
```

**Security Subagent**:
```
Task: Analyze [files] for security vulnerabilities.
Focus: Injection, auth issues, secrets exposure, unsafe operations, dependency risks.
Output: Security findings with severity and remediation
```

**Architecture Subagent**:
```
Task: Review overall structure and design of [files/project].
Focus: Coupling, cohesion, separation of concerns, design patterns, testability.
Output: Architecture findings and recommendations
```

### 6. Review Categories

Each category produces findings with severity ratings.

#### Correctness
- Logic errors and bugs
- Edge cases not handled
- Off-by-one errors
- Null/undefined handling
- Type mismatches
- Race conditions

#### Security
- Injection vulnerabilities (SQL, command, XSS)
- Authentication/authorization flaws
- Secrets in code
- Unsafe deserialization
- Path traversal
- Dependency vulnerabilities

#### Performance
- Algorithmic complexity issues
- Unnecessary allocations
- N+1 queries
- Missing caching opportunities
- Blocking operations
- Memory leaks

#### Testing
- Missing test coverage
- Untested edge cases
- Brittle tests
- Missing integration tests
- Inadequate mocking

#### Documentation
- Missing function/class docstrings
- Outdated comments
- Unclear variable names
- Missing README updates
- Undocumented public APIs

#### Architecture
- Tight coupling
- God objects/functions
- Circular dependencies
- Layer violations
- Missing abstractions
- Poor separation of concerns

### 7. Classify Findings

Rate each finding:

| Severity | Definition | Action |
|----------|------------|--------|
| **Critical** | Security vulnerability, data loss risk, crash in production | Must fix before merge |
| **Major** | Significant bug, performance issue, maintainability blocker | Should fix before merge |
| **Minor** | Code smell, style issue, minor inefficiency | Fix when convenient |
| **Nitpick** | Preference, very minor style, optional improvement | Consider fixing |

### 8. Generate Outputs

#### Output 1: Claude Code Action Format

Produce structured findings Claude Code can act on directly:

```
## File: [filepath]

### [Line X-Y]: [Brief title]
**Severity**: Critical|Major|Minor|Nitpick
**Category**: Correctness|Security|Performance|Testing|Documentation|Architecture

**Issue**: [Clear description of the problem]

**Current code**:
[relevant code snippet]

**Suggested fix**:
[corrected code snippet]

**Rationale**: [Why this change improves the code]

---
```

Group findings by file, ordered by severity (Critical first).

#### Output 2: REVIEW.md Human Summary

Write to `REVIEW.md` in the project root:

```markdown
# Code Review Summary

**Reviewed**: [files/scope]
**Depth**: Quick|Standard|Deep
**Date**: [timestamp]

## Overview

[2-3 sentence summary of overall code quality and key concerns]

## Findings by Severity

### Critical ([count])
- [one-line summary with file:line reference]

### Major ([count])
- [one-line summary with file:line reference]

### Minor ([count])
- [one-line summary with file:line reference]

### Nitpicks ([count])
- [one-line summary with file:line reference]

## Category Breakdown

| Category | Critical | Major | Minor | Nitpick |
|----------|----------|-------|-------|---------|
| Correctness | X | X | X | X |
| Security | X | X | X | X |
| Performance | X | X | X | X |
| Testing | X | X | X | X |
| Documentation | X | X | X | X |
| Architecture | X | X | X | X |

## Recommendations

[Prioritized list of recommended actions]

## Positive Observations

[Things done well - important for balanced feedback]
```

### 9. Iterate on Critical/Major Issues

After generating outputs:
1. **Use context7 to verify fix approaches** before implementing
2. If user confirms, apply fixes for Critical and Major issues
3. Re-review changed code to verify fixes don't introduce new issues
4. Update REVIEW.md with resolution status

**REMINDER**: Use context7 to look up correct API usage before suggesting or implementing any code changes.
