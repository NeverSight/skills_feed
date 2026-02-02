---
name: code-quality
description: "Run comprehensive code quality checks including TypeScript typecheck, ESLint linting, Prettier formatting, and Markdown validation. Auto-fixes formatting issues in agent mode or provides read-only checks for CI pipelines. Use when: (1) Before committing code changes, (2) In CI/CD pipelines for automated quality gates, (3) After making significant code changes, (4) When preparing code for review, (5) When ensuring code meets quality standards, (6) For type checking, linting, formatting, and markdown validation, (7) In pre-commit hooks, or (8) For automated quality gates before merging. Triggers: finalize, code quality, typecheck, lint, format, check code, quality check, run checks, pre-commit, before commit, CI checks, validate code."
metadata:
  author: ai-dev-atelier
  version: "1.0"
---

# Code Quality

Run comprehensive code quality checks: TypeScript typecheck, ESLint linting, Prettier formatting, and Markdown validation.

## Scripts

Scripts are embedded in `skills/code-quality/scripts/finalize.sh`. Agents execute:
- `bash skills/code-quality/scripts/finalize.sh agent` - Auto-fixes formatting issues (agent mode)
- `bash skills/code-quality/scripts/finalize.sh ci` - Read-only checks for CI pipelines (no auto-fixes)

## Checks Performed

1. **TypeScript Type Checking** - Validates type safety
2. **ESLint Linting** - Checks code style and potential issues
3. **Prettier Formatting** - Ensures consistent code formatting
4. **Markdown Quality** - Validates markdown files (trailing whitespace, missing newlines)

## Workflow

### Running Quality Checks

1. **Choose mode**:
   - Agent mode: Execute `bash skills/code-quality/scripts/finalize.sh agent` - Auto-fixes formatting issues while checking for type and lint errors
   - CI mode: Execute `bash skills/code-quality/scripts/finalize.sh ci` - Read-only checks suitable for CI pipelines (no auto-fixes)

2. **Review results**: Check terminal output for errors and warnings
   - TypeScript errors show file paths and line numbers
   - ESLint warnings include rule names and suggestions
   - Prettier issues are auto-fixed in agent mode
   - Markdown issues show file paths and line numbers

3. **Fix issues**: Address any errors that weren't auto-fixed
   - Type errors: Fix type mismatches, missing types, or incorrect imports
   - Lint errors: Follow ESLint suggestions or disable rules with comments if needed
   - Markdown issues: Fix trailing whitespace or add missing newlines

4. **Re-run checks**: Execute the same command again to verify all issues are resolved
   - Script exits with code 0 if all checks pass
   - Script exits with code 1 if any check fails (useful for CI pipelines)

### Integration with Other Skills

- Run after code-review skill to ensure reviewed code meets quality standards
- Run before docs-check skill to ensure code is clean before documentation review
- Use in CI pipelines as a quality gate before merging PRs

## Examples

When agents use this skill, they execute:

```bash
# Agent mode (auto-fixes)
bash skills/code-quality/scripts/finalize.sh agent

# CI mode (read-only)
bash skills/code-quality/scripts/finalize.sh ci
```

## Integration

- Run after code-review skill to ensure reviewed code meets quality standards
- Run before docs-check skill to ensure code is clean before documentation review
- Use in CI pipelines as a quality gate before merging PRs

## References

- `references/documentation-guide.md` - Documentation standards

## Output

Terminal output. Exits with code 0 (pass) or 1 (fail) for CI pipelines.
