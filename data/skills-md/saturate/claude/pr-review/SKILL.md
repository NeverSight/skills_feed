---
name: pr-review
description: Performs comprehensive code reviews checking for bugs, security issues, performance problems, testing gaps, and code quality. Use when reviewing PRs, code changes, or when asked to review code.
compatibility: Basic tools only - grep, file reading
allowed-tools: Read Grep Glob Bash
metadata:
  author: Saturate
  version: "1.0"
---

# Code Review

Review code like a senior engineer - thorough but practical. Focus on things that actually matter. Don't waste time on style nitpicks a linter should catch.

## Review Checklist

Use this checklist to guide your review. Need examples of what to look for? Check out [references/common-issues.md](references/common-issues.md) for code patterns.

### Security (Critical)
- [ ] Input validation and sanitization
- [ ] SQL injection, XSS, command injection risks
- [ ] Auth checks in place and correct
- [ ] Sensitive data handling (passwords, tokens, PII)
- [ ] Dependency vulnerabilities

### Bugs & Logic (Critical)
- [ ] Null/undefined handling
- [ ] Edge cases (empty arrays, null values, boundaries)
- [ ] Error handling in place
- [ ] Race conditions or concurrency issues
- [ ] State management issues

### Performance (Important)
- [ ] Algorithm complexity (watch for O(n²) where O(n) exists)
- [ ] N+1 query problems
- [ ] Memory leaks (listeners, subscriptions, closures)
- [ ] Blocking operations that should be async

### Testing (Important)
- [ ] Changes covered by tests
- [ ] Tests verify actual behavior
- [ ] Edge cases tested
- [ ] Error conditions tested

### Code Quality
- [ ] Code is understandable
- [ ] No unnecessary complexity or clever code
- [ ] Duplication worth extracting
- [ ] Names match what they do

### Architecture
- [ ] Fits existing patterns (or has good reason not to)
- [ ] No breaking changes without migration
- [ ] Avoids unnecessary coupling

## Output Format

Structure your review like this (see [references/review-template.md](references/review-template.md) for detailed examples):

- **Summary:** One line verdict (Good to merge / Has issues / Needs work)
- **Critical:** Security, data loss, crashes - must fix before merge
- **Important:** Bugs, performance, missing tests - should fix
- **Minor:** Quality improvements - nice to have
- **Questions:** Things to clarify with the author
- **Prevent This:** Suggest tooling/config to catch these issues automatically in the future
- **Positive Notes:** Briefly acknowledge what's done well

## Guidelines

- Be specific: file:line, what's wrong, why it matters, how to fix
- Skip style issues that linters catch
- Explain impact, not just "this is wrong"
- Consider trade-offs - sometimes simple is better than perfect
- Briefly note if something is done well, but keep it short

### Suggesting Future Mitigations

Only suggest mitigations for recurring patterns or critical issues. Don't suggest tools for one-off mistakes. Focus on automatable checks, not process changes.

**TypeScript configuration:**
- Type safety issues (`any`, implicit types) → Suggest `strict: true`, `noImplicitAny`, `strictNullChecks` in tsconfig.json
- Missing null checks → Suggest `strictNullChecks: true`

**Linting rules:**
- Code quality patterns ESLint could catch → Suggest specific ESLint rules
- Framework-specific issues → Suggest framework ESLint plugins (react-hooks, vue, etc.)
- Formatting inconsistencies → Suggest Prettier in pre-commit hook

**Pre-commit hooks:**
- Secrets/credentials committed → Suggest trufflehog or git-secrets
- Test failures → Suggest running tests before commit
- Type errors → Suggest tsc --noEmit check

**CI/CD checks:**
- Security vulnerabilities → Suggest npm audit / dependency scanning
- Missing tests → Suggest coverage thresholds
- Build errors → Ensure build runs in CI

## References

Need more guidance? Check these out:

- **[Review Template](references/review-template.md)** - What your review output should look like, with severity categories and example issues
- **[Common Issues](references/common-issues.md)** - Quick reference of problems that come up often in reviews, with good/bad code examples
