---
name: code-review
description: Systematic code analysis with evidence collection
allowed-tools:
  - read_file
  - run_terminal_cmd
tier: 2
protocol: CODE-REVIEW
tags: [moollm, development, quality, review, security]
related: [adventure, debugging, research-notebook, session-log, rubric, evaluator]
templates:
  - file: REVIEW.yml.tmpl
    purpose: Structured review tracking
    parameters: [review_name, created_date, focus, files]
  - file: REVIEW.md.tmpl
    purpose: Formatted review document
    parameters: [review_name, created_date, files]
---

# Code Review

> *"Read with intent. Question with purpose. Document with care."*

Systematic code analysis with evidence collection. Code review IS an [adventure](../adventure/) — the codebase is the dungeon, findings are clues.

## Review Process

```
READ → NOTE ISSUES → CLASSIFY → REPORT
```

### Step 1: Setup
1. Create REVIEW.yml
2. Identify files to review
3. Define focus areas

### Step 2: Overview
1. List all changed files
2. Read PR/commit description
3. Note initial impressions

### Step 3: Deep Review
For each file:
1. Read the code
2. Check against criteria
3. Note findings
4. Run relevant checks

### Step 4: Verification
1. Run tests
2. Run linters
3. Check regressions

### Step 5: Synthesize
1. Compile findings
2. Prioritize issues
3. Generate REVIEW.md
4. State recommendation

## Finding Severity

| Level | Symbol | Meaning | Action |
|-------|--------|---------|--------|
| Blocking | 🚫 | Must fix before merge | Request changes |
| Important | ⚠️ | Should fix or explain | Request changes |
| Minor | 💡 | Nice to fix | Comment only |
| Praise | 🎉 | Good work! | Celebrate |

## Finding Types

- **Security** — Injection, auth, sensitive data
- **Correctness** — Logic errors, edge cases
- **Performance** — N+1 queries, memory leaks
- **Maintainability** — Clarity, DRY, naming
- **Style** — Formatting, conventions

## Review Checklist

### Security
- Input validation
- Output encoding
- Authentication/authorization
- Sensitive data handling
- Injection vulnerabilities
- Timing attacks

### Correctness
- Logic errors
- Edge cases handled
- Null/undefined handling
- Error handling
- Race conditions
- Resource cleanup

### Maintainability
- Code clarity
- Appropriate comments
- Consistent naming
- DRY (no duplication)
- Single responsibility
- Testability

### Performance
- Algorithmic complexity
- Memory usage
- Database queries
- Caching
- Unnecessary operations

## Core Files

### REVIEW.yml

```yaml
review:
  name: "PR #123: Add user authentication"
  status: "in_progress"
  
findings:
  blocking:
    - id: "B1"
      file: "src/auth/login.ts"
      line: 45
      type: "security"
      summary: "Timing attack vulnerability"
      
  important: []
  minor: []
  praise: []

verification:
  tests: { ran: true, passed: true }
  linter: { ran: true, passed: false, issues: 3 }
```

### REVIEW.md

Formatted document with:
- Summary and counts
- Issues by severity
- Verification results
- Recommendation

## Verification Commands

```yaml
tests:
  - "npm test"
  - "pytest"
  - "go test ./..."
  
linters:
  - "npm run lint"
  - "flake8"
  - "golangci-lint run"
```

## Recommendation Output

| Outcome | Meaning |
|---------|---------|
| `approve` | Good to merge |
| `request_changes` | Has blocking/important issues |
| `comment` | Minor feedback only |

## See Also

- [rubric](../rubric/) — **Explicit scoring criteria** for code quality
- [evaluator](../evaluator/) — Independent assessment pattern
- [adversarial-committee](../adversarial-committee/) — Multiple reviewers debating findings
