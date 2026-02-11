---
name: code-review
description: Review code changes for quality, security, and best practices; save report to docs/reviews/
---

# Code Review

## Overview

Perform comprehensive code review across multiple dimensions: **Security**, **Quality**, **Performance**, and **Best Practices**. Support two review modes: Git changes or specified files.

**Core principle:** Read and analyze, never modify code. Always provide concrete code references with specific recommendations.

**Announce at start:** "I'm reviewing the code and will save the report to docs/reviews/"

${languageInstruction}

## Critical Constraints

- **READ-ONLY** - Do not edit any source code files
- **ALWAYS CITE** - Include `file:line` references for all issues found
- **SAVE REPORT** - Always save the report to `docs/reviews/YYYY-MM-DD-<scope>.md`

## Review Process

### Phase 1: Scope Determination

**Goal:** Identify what code to review.

**Steps:**

1. Parse arguments to determine review mode:
   - No args or `--staged`: Review Git staged changes (`git diff --cached`)
   - No args (no staged): Review all uncommitted changes (`git diff`)
   - File path(s): Review specified files
   - `--commit <hash>`: Review specific commit (`git show <hash>` to get the diff)
2. If the diff is empty or no files match, inform the user and stop — do not produce an empty report
3. Gather project context (language, framework, existing patterns)
4. List files to be reviewed with change summary

### Phase 2: Multi-dimensional Analysis

**Goal:** Analyze code across all quality dimensions.

**Dimensions:**

| Dimension | Focus Areas |
| --------- | ----------- |
| **Security** | Injection vulnerabilities (SQL, command, XSS), sensitive data exposure, authentication/authorization flaws, OWASP Top 10 |
| **Quality** | Code readability, cyclomatic complexity, code duplication, error handling, naming conventions |
| **Performance** | Algorithm efficiency, resource leaks, unnecessary allocations, N+1 queries, caching opportunities |
| **Best Practices** | Design patterns, SOLID principles, test coverage, documentation, project conventions |

**Detailed Checklist:**

Security (CRITICAL):

- Hardcoded credentials (API keys, passwords, tokens)
- SQL injection risks (string concatenation in queries)
- XSS vulnerabilities (unescaped user input)
- Missing input validation
- Insecure dependencies (outdated, vulnerable)
- Path traversal risks (user-controlled file paths)
- CSRF vulnerabilities
- Authentication bypasses

Code Quality (HIGH):

- Large functions (>50 lines)
- Large files (>800 lines)
- Deep nesting (>4 levels)
- Missing error handling (try/catch)
- console.log statements left in code
- Mutation of shared state
- Missing tests for new code

Performance (MEDIUM):

- Inefficient algorithms (O(n²) when O(n log n) possible)
- Unnecessary re-renders in React
- Missing memoization opportunities
- Large bundle sizes
- Unoptimized images
- Missing caching
- N+1 database queries

Best Practices (MEDIUM):

- Emoji usage in code/comments (unless project convention)
- TODO/FIXME without issue tickets
- Missing JSDoc for public APIs
- Accessibility issues (missing ARIA labels, poor contrast)
- Poor variable naming (x, tmp, data)
- Magic numbers without explanation
- Inconsistent formatting

**Steps:**

1. Read each file/diff in the review scope
2. For each dimension, identify issues with severity:
   - **Critical**: Security vulnerabilities, data loss risks, breaking bugs
   - **Warning**: Code smells, potential bugs, performance issues
   - **Suggestion**: Style improvements, refactoring opportunities
3. Note positive patterns worth highlighting:
   - Well-structured abstractions or clean separation of concerns
   - Thorough error handling or defensive coding
   - Good test coverage or meaningful test cases
   - Effective use of design patterns appropriate to the context
   - Clear naming, documentation, or self-documenting code

### Phase 3: Report Generation

**Goal:** Produce actionable review report.

**Steps:**

1. Group findings by severity (critical first)
2. Ensure each finding includes:
   - File and line reference
   - Clear issue description
   - Specific recommendation with code example if helpful
3. Write summary with overall assessment
4. Save report to `docs/reviews/YYYY-MM-DD-<scope>.md`
   - `<scope>` should be descriptive: feature name, PR number, or "staged-changes"

## Output Format

```markdown
# Code Review Report

**Date:** YYYY-MM-DD
**Scope:** [files or git changes reviewed]
**Summary:** X critical, Y warnings, Z suggestions

## Critical Issues

| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|
| 1 | `src/auth.ts:42` | SQL injection vulnerability | Use parameterized queries |

## Warnings

| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|
| 1 | `src/api.ts:105` | Missing error handling | Wrap in try-catch, return proper error response |

## Suggestions

| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|
| 1 | `src/utils.ts:23` | Magic number | Extract to named constant |

## Positive Highlights

- Good use of dependency injection in `src/services/user.ts:15`
- Comprehensive input validation in `src/validators/`

## Summary

[Overall assessment: code quality level, key risks, priority recommendations]

## Verdict

[One of: ✅ APPROVED | ⚠️ APPROVED WITH WARNINGS | ❌ CHANGES REQUESTED]
```

## Approval Criteria

| Verdict | Condition | Action |
| ------- | --------- | ------ |
| ✅ APPROVED | No issues found | Safe to merge |
| ⚠️ APPROVED WITH WARNINGS | Suggestions only | Can merge, consider addressing suggestions |
| ❌ CHANGES REQUESTED | Any Critical or Warning issues | Must fix before merge |

## Usage Examples

| Command | Description |
| ------- | ----------- |
| `/code-review` | Review current Git changes (staged if any, otherwise all uncommitted) |
| `/code-review src/auth.ts` | Review specific file |
| `/code-review src/auth.ts src/api.ts` | Review multiple files |
| `/code-review --staged` | Review only staged changes |
| `/code-review --commit abc123` | Review specific commit |

## Edge Cases

| Scenario | Action |
| -------- | ------ |
| Empty diff / no files to review | Inform the user and stop — do not generate a report |
| Very large scope (>20 files or >2000 lines of diff) | Summarize scope first, ask user whether to review all or focus on specific areas |
| Generated / minified / vendor files | Skip by default; note them as skipped in the report unless user explicitly requests review |
| Binary files in diff | Skip and note as not reviewable |
| File outside your expertise (e.g., unfamiliar language) | Review what you can, flag uncertainty, and note the limitation in the report |

## Guidelines

- Prioritize security issues - they should always be flagged as critical
- Be specific in recommendations - "improve error handling" is too vague
- Consider the project's existing patterns before suggesting changes
- Don't flag style issues that contradict project conventions
- Include positive feedback to balance constructive criticism
- Keep the report concise - group similar issues when appropriate
- When reviewing a `--commit`, use `git show <hash>` to obtain the diff rather than comparing working tree state

Arguments: ${args}
