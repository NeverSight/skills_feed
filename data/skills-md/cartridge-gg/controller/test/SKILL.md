---
name: test
description: Run appropriate test suites based on changed files or user request. Use to run tests intelligently based on the type of changes.
---

# Test Skill

Run appropriate test suites based on changed files or user request.

## Usage

Run tests intelligently:
- Unit tests for code changes
- Storybook visual regression for component changes
- Integration tests for example apps
- Full test suite before release

## Steps

1. Check git status to identify changed files
2. Determine appropriate test scope:
   - Keychain changes → `pnpm test`
   - Component/UI changes → `pnpm test:storybook`
   - Example app changes → Test specific example
   - Controller SDK changes → Controller tests + integration
3. Run selected test suite
4. Report results and any failures
5. If visual regressions detected, inform about `pnpm test:storybook:update`

## Notes

- E2E tests currently disabled in CI but can run locally
- Storybook snapshot updates require Docker setup
- Pre-commit hooks automatically run linting/formatting
