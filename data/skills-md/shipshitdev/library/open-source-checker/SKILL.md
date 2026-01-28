---
name: open-source-checker
description: Expert in detecting private information, secrets, API keys, credentials, and sensitive data in codebases before open sourcing
---

# Open Source Checker

Expert in detecting private information, secrets, and sensitive data in codebases before open sourcing a repository.

## When to Use This Skill

Use when you're:

- Preparing to open source a repository
- Reviewing code for exposed secrets
- Auditing codebase for sensitive data
- Performing security audits before public release
- Setting up pre-commit hooks for secret detection

## What to Check

### Critical Items

- API keys (OpenAI, Stripe, AWS, GitHub tokens)
- Database credentials and connection strings
- Private keys and certificates (`.pem`, `.key`)
- Personal information (emails, phone numbers)
- Environment files (`.env` should be gitignored)

### Git History (CRITICAL)

- Secrets remain in git history even after deletion
- Must scan all branches, tags, and deleted files
- Use `gitleaks`, `truffleHog`, or `git-secrets`

## Quick Workflow

1. **File scan**: Check for secret files, patterns
2. **Code analysis**: Search for hardcoded secrets
3. **Git history**: Scan entire history with tools
4. **Setup hooks**: Prevent future commits with secrets
5. **Clean history**: Use `git-filter-repo` if needed

## Tools

- `gitleaks`: Best for git history scanning
- `truffleHog`: Alternative history scanner
- `git-secrets`: AWS-focused with pre-commit hooks
- `detect-secrets`: Baseline-based detection

## References

- [Full guide: Patterns, scanning workflow, git hooks, cleanup](references/full-guide.md)
