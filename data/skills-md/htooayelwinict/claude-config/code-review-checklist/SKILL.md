---
name: code-review-checklist
description: |
  Review code changes for correctness, security, performance, and maintainability. Use for PR reviews,
  code audits, pre-merge checks, or quality validation of Laravel + React + Python code. EXCLUSIVE to reviewer agent.
allowed-tools: Read, Grep, Glob, Bash, mcp_gemini-bridge, mcp_open-bridge, mcp_codex-bridge, mcp_context7
---
# Code Review Checklist

**Exclusive to:** `reviewer` agent

## MCP Helpers (Brain + Memory)

### 🧠 Gemini-Bridge — Deep Code Analysis
```
mcp_gemini-bridge_consult_gemini(query="Review this code for best practices, security, and performance: [code snippet]", directory=".")
```

### 🌉 Open-Bridge — Alternative Analysis
```
mcp_open-bridge_consult_gemini(query="Review this code for best practices, security, and performance: [code snippet]", directory=".")
```

### 💻 Codex-Bridge — Code-Focused Review
```
mcp_codex-bridge_consult_codex(query="Analyze this code for bugs, anti-patterns, and improvements: [code]", directory=".")
```

### 📚 Context7 (Memory) — Up-to-Date Docs

Lookup best practices and anti-patterns:
```
mcp_context7_resolve-library-id(libraryName="[library]", query="best practices")
mcp_context7_query-docs(libraryId="/[resolved-id]", query="[specific pattern to validate]")
```

## Validation Loop (MANDATORY)

Before completing any review, verify the codebase passes all checks:
```bash
composer test           # All PHP tests pass
npm run types          # No TypeScript errors
npm run lint           # No linting errors
./vendor/bin/pint --test  # PHP style OK
```

Report any failures as Critical findings.

## Instructions

1. Review against project standards in `docs/code-standards.md`
2. Run through the checklist below
3. Report issues by severity (Critical → Warning → Suggestion)

## Review Checklist

### ✅ Correctness
- [ ] Logic handles edge cases
- [ ] Error handling is appropriate
- [ ] Types are correct (no `any` unless justified)
- [ ] Tests cover new/changed behavior
- [ ] No dead code or unused imports

### 🔒 Security (OWASP)
- [ ] No secrets or credentials in code
- [ ] User input validated and sanitized
- [ ] Authorization checks in place
- [ ] No SQL injection (use Eloquent/query builder)
- [ ] No XSS (proper escaping, sanitization)
- [ ] CSRF protection enabled
- [ ] Rate limiting considered

### ⚡ Performance
- [ ] No N+1 queries (use eager loading: `with()`)
- [ ] No unnecessary database calls
- [ ] Large datasets are paginated
- [ ] Indexes exist for filtered/joined columns

### 🧹 Maintainability
- [ ] Follows patterns in `docs/code-standards.md`
- [ ] Names are clear and consistent
- [ ] No unnecessary complexity
- [ ] DRY — no copy-paste duplication

### 🎨 Frontend
- [ ] Uses existing shadcn/ui components
- [ ] Loading and error states handled
- [ ] Accessible (keyboard, labels, contrast)
- [ ] Responsive (mobile + desktop)

### 📝 Documentation
- [ ] Code comments for non-obvious logic
- [ ] Docs updated if behavior changed
- [ ] Types documented with JSDoc if complex

## Laravel Security Checks

| Check | Verify |
|-------|--------|
| Mass assignment | `$fillable` or `$guarded` defined |
| Authorization | Policy or Gate used |
| Validation | FormRequest with rules |
| CSRF | `@csrf` in forms |
| SQL injection | No raw queries with user input |

## React Security Checks

| Check | Verify |
|-------|--------|
| XSS | No `dangerouslySetInnerHTML` |
| Props | TypeScript interfaces used |
| Secrets | No sensitive data in client |

## Severity Guide

| Level | Criteria | Action |
|-------|----------|--------|
| 🚨 Critical | Security flaw, data loss, breaks functionality | Block merge |
| ⚠️ Warning | Performance issue, code smell, missing test | Request fix |
| 💡 Suggestion | Style improvement, better pattern | Optional |

## Output Format

```markdown
## 🔍 Review Summary
[One paragraph overview]

## 🚨 Critical (must fix)
1. [Issue]: [File:Line] — [Why critical]

## ⚠️ Warnings (should fix)
1. [Issue]: [File:Line] — [Recommendation]

## 💡 Suggestions (nice to have)
1. [Suggestion]: [File:Line] — [Improvement]

## ✅ What's Good
- [Positive observation]
```

## Examples
- "Review this PR before merge"
- "Check this code for security issues"
- "Audit changes for performance"
