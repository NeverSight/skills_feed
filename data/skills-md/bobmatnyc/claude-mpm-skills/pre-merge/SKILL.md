---
name: pre-merge
description: "Comprehensive verification workflow before merging changes to production."
version: 1.0.0
tags: []
progressive_disclosure:
  entry_point:
    summary: "Comprehensive verification workflow before merging changes to production."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Pre-Merge Verification

Comprehensive verification workflow before merging changes to production.

## When to Use This Skill

Use this skill when:
- Creating a pull request for review
- About to merge code to main/production branch
- Need systematic verification checklist
- Want to catch issues before code review

## Pre-Commit Verification

Before committing code, verify:
- [ ] Type checking passes (language-appropriate: `tsc --noEmit`, `mypy`, etc.)
- [ ] Linting passes with no errors (ESLint, Pylint, etc.)
- [ ] All existing tests pass locally
- [ ] No console.log/debug statements left in code
- [ ] Code follows project style guide
- [ ] No commented-out code blocks

### Commands by Language

**TypeScript/JavaScript**:
```bash
# Type check
npx tsc --noEmit

# Lint
npm run lint
# or: pnpm lint
# or: npx eslint .

# Tests
npm test
# or: pnpm test
```

**Python**:
```bash
# Type check
mypy src/

# Lint
pylint src/
# or: flake8 src/
# or: ruff check src/

# Tests
pytest
# or: python -m pytest
```

**Go**:
```bash
# Format check
gofmt -l .

# Lint
golangci-lint run

# Tests
go test ./...
```

## Pre-PR Verification

Before creating a pull request, ensure:

### Required Information
- [ ] Changeset added for user-facing changes (if using changesets)
- [ ] PR description is complete with:
  - [ ] Summary of changes
  - [ ] Related ticket references (ENG-XXX, HEL-XXX, JIRA-XXX, etc.)
  - [ ] Screenshots for UI changes (desktop, tablet, mobile)
  - [ ] Breaking changes documented
  - [ ] Migration guide (if breaking changes)
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed (README, API docs, etc.)

### Security Checklist (if API changes)
- [ ] Authentication required on protected routes
- [ ] Authorization checks implemented
- [ ] Input validation with schema (Zod, Pydantic, etc.)
- [ ] No sensitive data in logs
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Rate limiting considered

### Database Changes (if schema changes)
- [ ] Migration file created
- [ ] Migration tested on local database
- [ ] Migration tested on staging database
- [ ] Down migration available (rollback plan)
- [ ] No breaking changes without migration guide
- [ ] Schema changes documented

### UI Changes (if applicable)
- [ ] Screenshots included:
  - [ ] Desktop view (1920x1080)
  - [ ] Tablet view (768x1024)
  - [ ] Mobile view (375x667)
- [ ] Responsive behavior verified
- [ ] Accessibility checked (keyboard navigation, screen readers)
- [ ] Loading states implemented
- [ ] Error states implemented

## Pre-Merge Verification

Before merging to main branch, confirm:

### CI/CD Checks
- [ ] All CI checks pass (lint, type-check, tests, build)
- [ ] Code review approved by at least one reviewer
- [ ] No TypeScript errors in changed files
- [ ] No merge conflicts with target branch
- [ ] Build succeeds without warnings

### Functional Verification
- [ ] Database migrations run successfully (if applicable)
- [ ] No regression in existing functionality
- [ ] Performance benchmarks within acceptable range
- [ ] Manual testing completed for critical paths

### Documentation
- [ ] CHANGELOG.md updated (if using)
- [ ] API documentation updated (if API changes)
- [ ] README updated (if setup/usage changes)
- [ ] Migration guide provided (if breaking changes)

## PR Description Template

Use this template for comprehensive PR descriptions:

```markdown
## Summary
[Brief description of what this PR does]

## Related Tickets
- Fixes #123
- Closes ENG-456
- Related to HEL-789

## Changes
- [ ] Feature: [Description]
- [ ] Bug Fix: [Description]
- [ ] Refactor: [Description]
- [ ] Documentation: [Description]

## Testing
### Unit Tests
- Added tests for [feature/function]
- Coverage: X%

### Manual Testing
- [ ] Tested on desktop (Chrome, Firefox, Safari)
- [ ] Tested on mobile (iOS Safari, Android Chrome)
- [ ] Tested edge cases: [list specific cases]

## Screenshots
### Desktop
![Desktop view](screenshot-url)

### Tablet
![Tablet view](screenshot-url)

### Mobile
![Mobile view](screenshot-url)

## Breaking Changes
[List any breaking changes or write "None"]

### Migration Guide
[If breaking changes, provide migration steps]

## Performance Impact
[Describe any performance implications or write "No impact"]

## Security Considerations
[Describe security implications or write "No security impact"]

## Rollback Plan
[Describe how to rollback if issues occur]

## Deployment Notes
[Any special deployment considerations or write "Standard deployment"]
```

## Common Pitfalls to Avoid

### Pre-Commit
- ❌ Committing code with failing tests
- ❌ Leaving console.log/debug statements
- ❌ Committing without running type checker
- ❌ Committing large blocks of commented code

### Pre-PR
- ❌ Creating PR without description
- ❌ Missing screenshots for UI changes
- ❌ Not linking to related tickets
- ❌ Not documenting breaking changes
- ❌ Missing test coverage for new code

### Pre-Merge
- ❌ Merging with failing CI checks
- ❌ Merging without code review approval
- ❌ Merging with merge conflicts
- ❌ Merging without testing migrations
- ❌ Merging without considering rollback plan

## Quick Verification Script

Create a pre-commit verification script:

**JavaScript/TypeScript (pre-commit.sh)**:
```bash
#!/bin/bash
set -e

echo "Running type check..."
npx tsc --noEmit

echo "Running linter..."
npm run lint

echo "Running tests..."
npm test -- --run

echo "✅ All checks passed!"
```

**Python (pre-commit.sh)**:
```bash
#!/bin/bash
set -e

echo "Running type check..."
mypy src/

echo "Running linter..."
pylint src/

echo "Running tests..."
pytest

echo "✅ All checks passed!"
```

Make executable:
```bash
chmod +x pre-commit.sh
```

## Automation with Git Hooks

Set up automatic pre-commit checks:

### Using Husky (JavaScript/TypeScript)
```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm run lint && npm test"
```

### Using pre-commit (Python)
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: type-check
        name: Type Check
        entry: mypy src/
        language: system
        pass_filenames: false
      - id: lint
        name: Lint
        entry: pylint src/
        language: system
        pass_filenames: false
      - id: test
        name: Test
        entry: pytest
        language: system
        pass_filenames: false
```

Install hooks:
```bash
pre-commit install
```

## Success Criteria

### Pre-Commit Success
- ✅ All local checks pass
- ✅ Code is formatted correctly
- ✅ No debug statements remain
- ✅ Tests pass locally

### Pre-PR Success
- ✅ PR description is comprehensive
- ✅ All required information included
- ✅ Screenshots attached (if UI changes)
- ✅ Breaking changes documented

### Pre-Merge Success
- ✅ CI pipeline is green
- ✅ Code review approved
- ✅ No conflicts with target branch
- ✅ Manual testing completed

## Related Skills

- `universal-verification-screenshot` - Screenshot verification for UI changes
- `universal-verification-bug-fix` - Bug fix verification workflow
- `toolchains-universal-security-api-review` - API security testing
- `universal-collaboration-git-workflow` - Git workflow best practices
