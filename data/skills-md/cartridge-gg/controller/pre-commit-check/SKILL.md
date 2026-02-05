---
name: pre-commit-check
description: Run all pre-commit checks before committing changes. Use to manually verify changes pass all quality gates before committing.
---

# Pre-commit Check Skill

Run all pre-commit checks before committing changes.

## Usage

Manually verify changes pass all quality gates before committing.

## Steps

1. Run `pnpm format` to format code and fix auto-fixable lint issues
2. Run `pnpm lint` to check for remaining lint/format issues
3. Run appropriate tests based on changed files
4. Verify TypeScript compilation succeeds
5. Review changes one final time
6. Ready to commit if all checks pass

## Notes

- Husky pre-commit hook automatically runs format + lint:check
- This skill useful for checking before pushing or during development
- Consider running `pnpm build` for major changes
