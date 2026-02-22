---
name: quality-commit
description: Stage, lint, scan, review, and commit changes with full quality gates in a single standardized flow.
---

# Quality Commit

Run all quality gates (lint, typecheck, Semgrep, CodeRabbit, tests) on staged changes, then commit. This replaces the manual multi-step process that frequently causes pre-commit hook friction.

## Steps

### 1. Determine Scope

Identify which workspace(s) have staged changes:

```bash
cd "$CLAUDE_PROJECT_DIR"
STAGED=$(git diff --cached --name-only --diff-filter=ACMR)
```

Categorize staged files into:

- **frontend**: `apps/frontend/src/**/*.{ts,svelte,js}`
- **api**: `apps/api/src/**/*.ts`
- **shared**: `packages/shared/src/**/*.ts`

If no files are staged, print a warning and exit.

### 2. Lint Staged Files

For each workspace with staged files:

- **frontend**: `cd apps/frontend && npx eslint <staged-files>`
- **api**: `cd apps/api && npx eslint <staged-files>` (if eslint is configured)
- **shared**: `cd packages/shared && npx eslint <staged-files>` (if eslint is configured)

**On failure**: Print the specific errors. Do NOT proceed to commit. Fix the issues first.

### 3. Type Check

Run type checks only on affected workspaces:

- **frontend**: `cd apps/frontend && npx svelte-check --tsconfig ./tsconfig.json --threshold error`
  - Note: 11 pre-existing errors in test files are known baseline — ignore those.
- **api**: `cd apps/api && npx tsc --noEmit`
- **shared**: `cd packages/shared && npx tsc --noEmit`

**On failure**: Print errors. Do NOT proceed.

### 4. Semgrep Security Scan

**Important**: Semgrep crashes when given multiple file arguments (`Invalid_argument: invalid path` bug in 1.146.0–1.151.0+). Always scan files one at a time:

```bash
SEMGREP_FINDINGS=""
for f in <staged-files>; do
  RESULT=$(semgrep scan --config auto --json "$f" 2>/dev/null) || true
  SEMGREP_FINDINGS="$SEMGREP_FINDINGS$RESULT"
done
```

- Parse JSON output from each file and aggregate findings with file:line and rule ID.
- **On critical/high findings**: Block the commit and show the findings.
- **On medium/low findings**: Warn but allow proceeding (print them for visibility).
- If `semgrep` is not installed, skip with a warning.

### 5. CodeRabbit Review (Optional)

If `$ARGUMENTS` contains `--review` or `--full`:

```bash
coderabbit review --plain -t uncommitted 2>&1
```

- Parse output and group by severity (Critical, Suggestions, Positive).
- **On critical findings**: Block the commit and show details.
- If `coderabbit` CLI is not installed, skip with a warning.

### 6. Run Related Tests

For each staged `.ts`/`.svelte` file, look for a colocated `.test.ts`:

```bash
# Example: src/lib/server/auth/rbac.ts → src/lib/server/auth/rbac.test.ts
# Example: src/routes/chat.ts → src/routes/chat.test.ts
```

Run discovered test files with `npx vitest run <test-files> --reporter=verbose`.

**On failure**: Print failing tests. Do NOT proceed.

### 7. Commit

If all gates pass:

1. Review the staged diff one more time.
2. Draft a commit message following the project convention:

   ```
   type(scope): description

   Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
   ```

3. Create the commit using a HEREDOC for the message.

**Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
**Scopes**: `security`, `phaseX.Y`, `api`, `frontend`, `database`, `auth`, `workflows`

### 8. Push (only with `--push`)

If `$ARGUMENTS` contains `--push`:

1. Run semgrep on files from the last commit (one file at a time — see Step 4 note on multi-file bug):

   ```bash
   COMMITTED_FILES=$(git diff --name-only HEAD~1 -- '*.ts' '*.svelte' '*.js')
   SEMGREP_FINDINGS=""
   for f in $COMMITTED_FILES; do
     RESULT=$(semgrep scan --config auto --json "$f" 2>/dev/null) || true
     SEMGREP_FINDINGS="$SEMGREP_FINDINGS$RESULT"
   done
   ```

   - **On critical/high findings**: Abort push, print findings. The commit stays intact.
   - **On medium/low findings**: Warn but continue.
   - If `semgrep` is not installed, skip with a warning.

2. Determine branch and upstream:

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   UPSTREAM=$(git rev-parse --abbrev-ref @{u} 2>/dev/null || echo "")
   ```

3. Push:
   - If upstream exists: `git push`
   - If no upstream: `git push -u origin $BRANCH`
   - If `--dry-run` is also set: Print "would push to origin/$BRANCH" and skip the actual push.

4. On push failure: Report the error. The commit remains intact — do NOT attempt to undo it.

If `--push` is not passed, skip this step entirely.

### 9. Summary

Print a summary table:

```
| Gate        | Status | Details                    |
|-------------|--------|----------------------------|
| Lint        | PASS   | 5 files, 0 errors          |
| TypeCheck   | PASS   | api + frontend             |
| Semgrep     | PASS   | 0 findings                 |
| CodeRabbit  | SKIP   | (use --review to enable)   |
| Tests       | PASS   | 3 test files, 12 tests     |
| Commit      | DONE   | abc1234                    |
| Push        | PASS   | pushed to origin/feature-x |
```

When push is not requested, show:

```
| Push        | SKIP   | (use --push to enable)     |
```

## Arguments

- `$ARGUMENTS`: Optional flags:
  - `--review` or `--full`: Include CodeRabbit review (slower, ~30s)
  - `--dry-run`: Run all gates but skip the actual commit (and push)
  - `--push`: After successful commit, run semgrep on committed files and push to remote
  - `--message "custom message"`: Use a custom commit message instead of auto-generating one
  - If empty: Run lint + typecheck + semgrep + tests + commit (skip CodeRabbit, skip push)

## Error Recovery

If any gate fails:

1. Print the specific errors clearly
2. Suggest targeted fixes
3. Do NOT attempt to auto-fix and retry — let the user (or agent) fix first, then re-run `/quality-commit`

## Examples

- `/quality-commit` — Standard flow: lint, typecheck, semgrep, tests, commit
- `/quality-commit --review` — Full flow with CodeRabbit review included
- `/quality-commit --dry-run` — Validate everything but don't commit or push
- `/quality-commit --push` — Standard flow + push after commit
- `/quality-commit --review --push` — Full flow with CodeRabbit + push
- `/quality-commit --push --dry-run` — Run all gates, print "would push", skip actual commit and push
- `/quality-commit --message "fix(security): add IPv6 SSRF checks"` — Custom commit message
