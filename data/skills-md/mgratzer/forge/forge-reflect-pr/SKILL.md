---
name: forge-reflect-pr
description: Review the current PR branch for refactoring opportunities, missing tests, documentation updates, and cleanup before finalizing. Use when the user has finished implementing a feature and wants to self-review before requesting peer review.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Reflect on PR

Review the current PR branch for cleanup opportunities before finalizing.

## When to Use

Run this after completing the main implementation work on a PR, before requesting review.

## Process

### Step 1: Identify Changed Files

```bash
# Detect the default branch, then get list of changed files
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
git diff --name-only $DEFAULT_BRANCH...HEAD
```

### Step 2: Check for Refactoring Opportunities

For each changed file, assess:
1. **Code duplication**: Are there repeated patterns that should be extracted?
2. **Function size**: Are any functions too long and should be split?
3. **Naming**: Are variable/function names clear and consistent?
4. **Abstractions**: Is logic in the right layer (routes vs services vs repositories)?
5. **Dead code**: Any unused imports, variables, or functions introduced?
6. **Pattern consistency**: If a pattern was changed in this PR (error handling, component structure, API call convention), are ALL files using that pattern updated? Search for remaining instances:
   ```bash
   grep -rn "<changed-pattern>" src/
   ```

### Step 3: Check Environment and Configuration

Review changes for configuration correctness:

1. **New environment variables** — Are they documented (e.g., in `.env.example` or equivalent)?
2. **Configuration placement** — Are settings placed where they're consumed? (runtime config vs build config vs compile-time constants)
3. **External service dependencies** — Are new integrations noted? Are credentials properly handled (not hardcoded)?
4. **Deployment needs** — Do changes require manual steps not yet captured in the PR description?

### Step 4: Assess Test Coverage

1. For each new/modified module, check if corresponding `.test.ts` file exists
2. Run coverage on changed files:
   ```bash
   # Run the project's coverage command with a path filter (check package.json for the exact script)
   # e.g.: npm run test:coverage -- --testPathPattern="<pattern>"
   ```
3. Identify untested code paths, especially:
   - Error handling branches
   - Edge cases
   - New public functions/methods

### Step 5: Review Documentation

Check if any of these need updates based on changes made:

1. **`/docs/*.md`** - Architecture, API reference, development guides
   ```bash
   # Search for references to changed functionality
   grep -r "<feature-keyword>" docs/
   ```

2. **`CLAUDE.md`** - Project conventions, patterns, quick reference
   - New patterns or conventions established?
   - New scripts or commands added?
   - Architecture changes?

3. **Code comments** - Outdated comments in changed files?
   - Search for dimension references, format mentions, etc.
   ```bash
   grep -rn "<old-value>" src/
   ```

4. **JSDoc/TSDoc** - Public function documentation accurate?

### Step 6: Cleanup Checklist

Verify:
- [ ] No `console.log` debugging statements left
- [ ] No commented-out code that should be removed
- [ ] No TODO comments that should be addressed now
- [ ] Import statements are clean (no unused imports)
- [ ] No hardcoded values that should be constants
- [ ] Error messages are user-friendly and actionable

### Step 7: Run Quality Gates

Run the project's quality check commands. Discover available scripts from CLAUDE.md or `package.json`. Typical checks include lint/format, type checking, and tests.

### Step 8: Report Findings

Provide a summary of:
1. **Refactoring done** (if any)
2. **Tests added** (if any)
3. **Documentation updated** (if any)
4. **Items deferred** - Valid improvements that should be separate PRs/issues

For each deferred item, create a GitHub issue — do not leave deferred items as untracked notes:
```bash
gh issue create --title "<title>" --body "<description>"
```

## Output Format

```text
## PR Reflection Summary

### Refactoring
- [x] Extracted `<function>` to reduce duplication
- [ ] No refactoring needed

### Tests
- [x] Added tests for `<module>`
- [ ] Coverage adequate for changes

### Documentation
- [x] Updated `docs/api-reference.md` with new endpoint
- [x] Fixed outdated comments in `<file>`
- [ ] No documentation updates needed

### Cleanup
- [x] Removed debug logging
- [x] Fixed lint warnings
- [ ] No cleanup needed

### Deferred Items
- Created issue #<num>: <title> (required for every deferred item)
- None identified
```

## Related Skills

**Before:** Use `forge-implement-issue` to implement the feature/fix.
**After review:** Use `forge-address-pr-feedback` to address reviewer feedback.
**Full workflow:** `forge-setup-project` → `forge-create-issue` → `forge-implement-issue` → `forge-reflect-pr` → `forge-address-pr-feedback` → `forge-update-changelog`

## Example Usage

```bash
/forge-reflect-pr
```
