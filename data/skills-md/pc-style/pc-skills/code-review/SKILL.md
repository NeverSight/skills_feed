---
name: code-review
description: Run automated code review using cubic review with amp review fallback. Use when the user wants to review code changes, check PR quality, analyze code for issues, or run automated code review tools.
---

# Code Review

Run automated code review using `cubic review` with `amp review` as fallback.

## When to Use

- Review code changes before committing
- Check PR quality
- Analyze code for issues
- Any request to "review code", "run code review", or "check quality"

## Workflow

### 1. Check What to Review

**Review staged changes:**
```bash
git diff --staged --stat
```

**Review specific files:**
```bash
git diff path/to/file
```

**Review current branch vs main:**
```bash
git diff main...HEAD --stat
```

### 2. Run Code Review

**Primary: cubic review**
```bash
cubic review
```

**With options:**
```bash
cubic review --staged
cubic review path/to/file.ts
cubic review --diff main...HEAD
```

### 3. Fallback if cubic fails

If `cubic review` fails or is unavailable, use `amp review`:

```bash
amp review
```

**With options:**
```bash
amp review --staged
amp review path/to/file.ts
```

## Complete Flow with Fallback

```bash
# Try cubic first
cubic review

# If cubic fails, fall back to amp
amp review
```

## What They Check

**cubic review** typically analyzes:
- Code quality and best practices
- Potential bugs and issues
- Performance concerns
- Security vulnerabilities
- Style violations

**amp review** typically provides:
- Similar code quality checks
- Alternative analysis engine
- Different rule sets and heuristics

## Review Scenarios

**Review all staged changes:**
```bash
cubic review --staged || amp review --staged
```

**Review before committing:**
```bash
git add .
cubic review --staged || amp review --staged
# Fix issues, then commit
git commit -m "fix: resolve review issues"
```

**Review specific file:**
```bash
cubic review src/auth.ts || amp review src/auth.ts
```

**Review branch changes:**
```bash
cubic review --diff main...HEAD || amp review --diff main...HEAD
```

## Interpreting Results

- Address critical issues first (security, bugs)
- Consider warnings for maintainability
- Style issues can be auto-fixed in many cases
- Not all suggestions need to be implemented

## Best Practices

- Run review before committing
- Fix critical issues immediately
- Use reviews to learn patterns
- Don't blindly accept all suggestions
- Consider the context of changes
- Run in CI/CD for automated checks