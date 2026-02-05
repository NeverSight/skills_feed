---
name: lint-build-fixer
description: "Used to systematically fix TypeScript build errors and ESLint linting issues. Triggers when asked to 'fix the build', 'resolve lint errors', 'fix type errors', or when build/lint failures are detected. Follows a strict priority: 1) Identify scripts, 2) Fix TS/Build errors first, 3) Verify & Commit build fix, 4) Fix Lint (Auto-fix first, then rule-by-rule), 5) Final Full Verification."
---

# Lint and Build Fixer

This skill provides a systematic workflow for resolving TypeScript and ESLint errors in a project.

## Workflow

### 1. Discovery
Analyze `package.json` to identify relevant scripts:
- **Build/Type-check**: Look for `build`, `type-check`, `tsc`, `check-types`.
- **Lint**: Look for `lint`, `eslint`.

### 2. TypeScript/Build Fixes (Priority 1)
Fix all TypeScript or build-related errors before addressing linting.
1. **Identify Errors**: Run the identified build or type-check command (e.g., `npm run type-check`). Alternatively, use IDE/editor TypeScript diagnostics.
2. **Iterative Fix**: Address errors one by one or in small batches.
3. **Verify**: Re-run the build/type-check command to ensure all errors are resolved.
4. **Commit**: Use `git commit -m "fixing the build"` once the build is green.

### 3. ESLint/Lint Fixes (Priority 2)
After the build is passing, address linting issues.
1. **Auto-fix**: Execute ESLint with the `--fix` flag. Check `package.json` for an existing fix script (e.g., `lint:fix`) or manually append `--fix` to the lint command.
2. **Categorize Remaining Errors**: If errors remain, group them by **Rule**, not by file.
    - Use `scripts/sort_eslint_by_rule.py` to get a rule-based summary:
      `npx eslint . -f json | python3 scripts/sort_eslint_by_rule.py`
3. **Fix Rule-by-Rule**: Address one rule at a time across all affected files.
    - Fix all instances of `rule-a` in all files before moving to `rule-b`.
4. **Incremental Verification**: After fixing a specific rule in a set of files, verify the fix by running ESLint on those specific files:
    - `npx eslint path/to/file1.ts path/to/file2.ts`
5. **Repeat**: Continue until all lint rules are addressed.

### 4. Final Verification
Once all individual rules are fixed:
1. Run a full ESLint check on the entire project.
2. Run a final TypeScript build/type-check to ensure no regressions were introduced.

## Reusable Resources

### Scripts
- `scripts/sort_eslint_by_rule.py`: A Python script that takes ESLint JSON output via stdin and prints a summary of issues grouped by rule.
  - **Usage**: `[eslint command] -f json | python3 path/to/scripts/sort_eslint_by_rule.py`