---
name: code-review
description: Review code changes for quality, correctness, and best practices. Use when asked to review a PR, review changes, or assess code quality before merge.
---

# Code Review

## Overview

This skill provides guidance for reviewing code in the Cartridge Controller monorepo, which implements a gaming-specific smart contract wallet ecosystem for StarkNet.

## Review Process

### 1. Understand the Change Scope

```bash
# For a PR
gh pr view <PR_NUMBER>
gh pr diff <PR_NUMBER>

# For local changes
git diff origin/main...HEAD
git log origin/main..HEAD --oneline
```

### 2. Review Checklist

#### Code Quality
- [ ] Code follows existing patterns in the codebase
- [ ] No unnecessary complexity or over-engineering
- [ ] Clear variable and function names
- [ ] Appropriate comments for complex logic
- [ ] No dead code or console.log statements

#### TypeScript
- [ ] Proper type annotations (avoid `any`)
- [ ] Interfaces/types defined for complex objects
- [ ] No TypeScript errors (`pnpm build` passes)

#### Security (Critical for this codebase)
- [ ] No secrets or credentials in code
- [ ] Iframe communication properly validated
- [ ] Origin checks for postMessage handlers
- [ ] Session tokens handled securely
- [ ] No XSS vulnerabilities in UI components
- [ ] WebAuthn/Passkey operations follow best practices

#### StarkNet/Blockchain Specific
- [ ] Transaction calls properly structured
- [ ] Gas estimation handled appropriately
- [ ] Error handling for chain interactions
- [ ] Address validation where needed

#### Testing
- [ ] New functionality has tests
- [ ] Edge cases covered
- [ ] Tests are meaningful (not just for coverage)
- [ ] Storybook stories updated for UI changes

#### Package-Specific Considerations

**controller/** (SDK):
- Public API changes are intentional and documented
- Backward compatibility considered
- Iframe communication protocols maintained

**keychain/** (Secure iframe):
- UI components follow design system
- Sensitive operations properly isolated
- State management is clean

**connector/** (Integration layer):
- Compatible with starknet-react patterns
- Minimal dependencies

### 3. Run Automated Checks

```bash
# Lint and format check
pnpm lint:check

# Type checking via build
pnpm build

# Unit tests
pnpm test

# Visual regression (if UI changes)
pnpm test:storybook
```

### 4. Provide Feedback

Structure your review as:

```markdown
## Summary
Brief overall assessment of the changes.

## Positive Aspects
- What's done well

## Required Changes
- Critical issues that must be fixed

## Suggestions
- Nice-to-have improvements

## Questions
- Clarifications needed
```

## Review Severity Levels

- **Blocking**: Must be fixed before merge (security issues, bugs, breaking changes)
- **Important**: Should be fixed, but can be follow-up PR
- **Suggestion**: Optional improvements
- **Nitpick**: Style preferences, can be ignored

## Common Issues to Watch For

### In React Components
- Missing dependency arrays in useEffect/useMemo/useCallback
- State updates in loops without proper batching
- Memory leaks from uncleared subscriptions

### In Async Code
- Missing error handling in try/catch
- Unhandled promise rejections
- Race conditions in concurrent operations

### In Type Definitions
- Overly permissive types (`any`, `unknown` without narrowing)
- Missing null checks for optional fields
- Incorrect generic constraints

## Example Review Comment

```markdown
**[Blocking]** Security concern in `packages/keychain/src/hooks/connection.ts:45`

The origin validation is missing for this postMessage handler. This could allow malicious sites to send messages to the iframe.

Suggested fix:
```typescript
if (event.origin !== expectedOrigin) {
  return;
}
```
```
