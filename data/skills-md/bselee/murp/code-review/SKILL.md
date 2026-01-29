---
name: code-review
description: Review code for quality, security, and best practices. Use when reviewing recent changes, PRs, or checking code quality. Proactively use after significant code modifications.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review

Comprehensive code review following project standards.

## Review Checklist

### Code Quality
- Clear naming conventions
- No code duplication
- Proper error handling with `{ success, error }` pattern
- TypeScript types explicit (no `any`)

### Project Patterns
- Uses hooks for Supabase queries (not direct queries in components)
- Services return `{ success, data?, error? }`
- AI calls go through `aiGatewayService.ts`
- Data transforms follow 4-layer schema (Raw → Parsed → Database → Display)

### Security
- No hardcoded secrets or API keys
- Input validation on external data
- SQL injection prevention
- XSS protection

### Testing
- E2E tests use `?e2e=1` for auth bypass
- Schema transformers have validation tests

## Output Format

For each finding:
- **Severity**: Critical / Warning / Suggestion
- **File:Line**: Location
- **Issue**: Description
- **Fix**: Recommended solution

## Trigger Phrases

- "review my changes"
- "code review"
- "check this code"
- "/review"
