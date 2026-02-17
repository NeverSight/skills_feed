---
name: repo-hygiene
description: >-
  Periodic repository health check — dependencies, git, CI/CD, code quality, docs, security.
  Use when: onboarding to a repo, weekly maintenance, after big refactors, before audits,
  "is this repo in good shape?". Triggers: "repo hygiene", "health check", "repo health",
  "clean up repo", "maintenance check", "audit repo", "repo audit".
---

# repo-hygiene — Repository Health Check

A structured, periodic health check for repositories. Run anytime to detect drift,
accumulation of tech debt, and configuration issues before they become problems.

**Not a release gate.** For pre-release checks, use the `pre-release` skill instead.
This skill is for ongoing maintenance — run it weekly, after major refactors, when
onboarding to a repo, or whenever things feel "off".

## When to Use

- Onboarding to a new (or forgotten) repo — "what shape is this in?"
- Weekly/monthly maintenance sweep
- After a large refactor or dependency upgrade
- Before starting a new feature sprint
- When CI starts failing mysteriously
- After a team member leaves and you inherit their repo

## Supported Stacks

| Stack | Package manager | Detected by |
|-------|----------------|-------------|
| Node.js / TypeScript | npm | `package.json` + `package-lock.json` |
| Python | uv / pip | `pyproject.toml` or `requirements.txt` |
| Go | go modules | `go.mod` |

Detect the stack from the project root. Multiple stacks in one repo is fine — run
applicable checks for each. If the stack isn't listed, skip stack-specific checks
and run the universal ones (git, CI, docs, security).

## The Workflow

### Step 0: Detect Project

```bash
# What are we working with?
ls package.json pyproject.toml go.mod 2>/dev/null
git rev-parse --show-toplevel
```

Determine: stack(s), git remote, default branch, CI system (GitHub Actions, GitLab CI, etc.).

### Step 1: Dependency Health

#### Node.js / npm

| # | Check | Command | Severity |
|---|-------|---------|----------|
| D1 | Known vulnerabilities | `npm audit --json` | 🔴 critical/high = Fix Now, moderate = Fix Soon |
| D2 | Outdated dependencies | `npm outdated --json` | 🟡 major bumps = Fix Soon, minor/patch = Info |
| D3 | Unused dependencies | `npx depcheck --json` | 🟡 Fix Soon |
| D4 | Phantom dependencies (used but undeclared) | `npx depcheck --json` → `missing` | 🔴 Fix Now |
| D5 | Lockfile freshness | See below | 🟡 Fix Soon |
| D6 | Duplicate dependencies | `npm ls --all --json 2>/dev/null \| grep -c '"deduped"'` | ℹ️ Info |

**D5 — Lockfile freshness check:**

```bash
# package.json changed more recently than lockfile?
LOCK_DATE=$(git log -1 --format=%ct -- package-lock.json 2>/dev/null || echo 0)
PKG_DATE=$(git log -1 --format=%ct -- package.json 2>/dev/null || echo 0)
if [ "$PKG_DATE" -gt "$LOCK_DATE" ]; then
  echo "⚠️ package.json modified after lockfile — run npm install"
fi
```

**How to fix:**

- D1: `npm audit fix` for compatible fixes; `npm audit fix --force` for breaking (review changes). For stubborn advisories: check if the vuln is reachable, or override in `package.json` `overrides`.
- D2: `npm update` for minor/patch; `npm install <pkg>@latest` for major (check changelogs).
- D3: `npm uninstall <pkg>` for each unused dep.
- D4: `npm install <pkg>` for each missing dep.
- D5: `npm install` to regenerate lockfile, commit it.
- D6: `npm dedupe` then verify tests pass.

#### Python (uv / pip)

| # | Check | Command | Severity |
|---|-------|---------|----------|
| D1 | Known vulnerabilities | `pip-audit --format=json` | 🔴 Fix Now |
| D2 | Outdated dependencies | `uv pip list --outdated` or `pip list --outdated --format=json` | 🟡 Fix Soon |
| D3 | Unused dependencies | `deptry . --json` (if available) | 🟡 Fix Soon |
| D5 | Lockfile freshness | Compare `uv.lock` vs `pyproject.toml` timestamps | 🟡 Fix Soon |

**How to fix:**

- D1: `uv pip install --upgrade <pkg>` for each vulnerable package. Check advisories for minimum safe version.
- D2: `uv pip install --upgrade <pkg>` per package, or `uv lock --upgrade` for all.
- D3: Remove from `[project.dependencies]` in `pyproject.toml`, then `uv sync`.
- D5: `uv lock && uv sync`.

#### Go

| # | Check | Command | Severity |
|---|-------|---------|----------|
| D1 | Known vulnerabilities | `govulncheck ./...` | 🔴 Fix Now |
| D2 | Outdated dependencies | `go list -m -u all` | 🟡 Fix Soon |
| D3 | Unused dependencies | `go mod tidy -v` (reports removed) | 🟡 Fix Soon |

**How to fix:**

- D1: `go get <module>@latest` for vulnerable deps, then `go mod tidy`.
- D2: `go get -u ./...` for all, or `go get <module>@latest` selectively.
- D3: `go mod tidy` removes unused; commit `go.mod` and `go.sum`.

---

### Step 2: Git Hygiene

| # | Check | Command | Severity |
|---|-------|---------|----------|
| G1 | Stale local branches (merged) | `git branch --merged main \| grep -v '^\*\|main\|develop'` | 🟡 Fix Soon |
| G2 | Stale remote branches (merged) | `git branch -r --merged origin/main \| grep -v 'HEAD\|main\|develop'` | 🟡 Fix Soon |
| G3 | Large files in repo | See below | 🟡 Fix Soon (🔴 if >10MB) |
| G4 | `.gitignore` completeness | See below | 🟡 Fix Soon |
| G5 | Untracked files that should be ignored | `git status --porcelain \| grep '^??'` — look for build artifacts, IDE files, env files | ℹ️ Info |
| G6 | Uncommitted changes | `git status --porcelain` | ℹ️ Info |

**G3 — Large files check:**

```bash
# Top 10 largest tracked files
git ls-files -z | xargs -0 -I{} git log --diff-filter=A --format='%H' -1 -- '{}' | head -20
# Simpler: just check current tree
git ls-files -z | xargs -0 du -sh 2>/dev/null | sort -rh | head -10
```

**G4 — .gitignore completeness:**

Must include (per stack):

- **Universal**: `.env`, `.env.*`, `*.local`, `.DS_Store`, `Thumbs.db`, `*.swp`, `.idea/`, `.vscode/` (or be deliberate about tracking it)
- **Node**: `node_modules/`, `dist/`, `build/`, `coverage/`, `.turbo/`, `.next/`
- **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.mypy_cache/`, `.pytest_cache/`, `*.egg-info/`
- **Go**: binary name (check `go build -o`), `vendor/` (if not vendoring)

**How to fix:**

- G1: `git branch -d <branch>` for each merged local branch.
- G2: `git push origin --delete <branch>` for each merged remote branch. Be careful — confirm with team.
- G3: For files that shouldn't be tracked: add to `.gitignore`, `git rm --cached <file>`. For files already in history: `git filter-repo` or BFG Repo-Cleaner (destructive — confirm first).
- G4: Add missing patterns to `.gitignore`. Use a generator like [gitignore.io](https://gitignore.io) as a starting point.
- G5: Either add to `.gitignore` or `git add` if they should be tracked.

---

### Step 3: CI/CD Health

Skip if no CI configuration found.

| # | Check | Command | Severity |
|---|-------|---------|----------|
| C1 | Workflow files exist | `ls .github/workflows/*.yml 2>/dev/null` | ℹ️ Info |
| C2 | Actions pinned by SHA | `grep -rE 'uses: [^@]+@v[0-9]' .github/workflows/` — should return nothing | 🟡 Fix Soon |
| C3 | Least-privilege permissions | Scan for `permissions:` blocks; flag `write-all` or missing job-level perms | 🟡 Fix Soon |
| C4 | No secret leaks in workflows | Check for `echo ${{ secrets.* }}`, secret in `$GITHUB_OUTPUT`/`$GITHUB_ENV` | 🔴 Fix Now |
| C5 | Deprecated actions | Check for known deprecated: `actions/create-release@v1`, `set-output` commands, `::set-env` | 🟡 Fix Soon |
| C6 | Node/Python version matches project | Compare workflow matrix with `engines`, `.nvmrc`, `pyproject.toml [requires-python]` | 🟡 Fix Soon |

**How to fix:**

- C2: Replace `uses: actions/checkout@v4` with `uses: actions/checkout@<full-sha>`. Find SHA: `gh api repos/actions/checkout/git/ref/tags/v4 --jq .object.sha` or check the releases page.
- C3: Add explicit `permissions:` at job level. Start with `contents: read` and add only what's needed.
- C4: Remove secret interpolation. Use `environment:` blocks or write to files with masking.
- C5: Replace deprecated actions with current equivalents. `set-output` → `$GITHUB_OUTPUT` file.
- C6: Align versions. Use `.nvmrc` or `engines` as the source of truth.

---

### Step 4: Code Quality Drift

| # | Check | Command | Severity |
|---|-------|---------|----------|
| Q1 | TODO/FIXME/HACK count | `git grep -ciE '(TODO\|FIXME\|HACK)' -- '*.ts' '*.js' '*.py' '*.go' ':!node_modules' ':!vendor' ':!.venv'` | ℹ️ Info (🟡 if >20) |
| Q2 | `console.log` in src (JS/TS) | `git grep -c 'console\.log' -- 'src/**/*.ts' 'src/**/*.js' ':!*.test.*' ':!*.spec.*'` | 🟡 Fix Soon |
| Q3 | Disabled/skipped tests | `git grep -cE '(it\.skip\|test\.skip\|describe\.skip\|xit\|xdescribe\|@pytest\.mark\.skip\|t\.Skip)' -- '*.test.*' '*.spec.*' '*_test.*' '*_test.go'` | 🟡 Fix Soon |
| Q4 | Lint passes | `npm run lint` / `ruff check .` / `golangci-lint run` | 🟡 Fix Soon |
| Q5 | Tests pass | `npm test` / `pytest` / `go test ./...` | 🔴 Fix Now |
| Q6 | Build succeeds | `npm run build` / `uv build` / `go build ./...` | 🔴 Fix Now |
| Q7 | Type errors (TS) | `npx tsc --noEmit` | 🟡 Fix Soon |
| Q8 | Dead exports (TS) | `npx ts-prune 2>/dev/null \| grep -v '(used in module)'` | ℹ️ Info |

**How to fix:**

- Q1: Triage each TODO — either do it, create an issue/task for it, or remove it if obsolete.
- Q2: Replace with a proper logger, or remove debug logging. `grep -rn 'console.log' src/` to find them.
- Q3: Either fix the underlying issue and un-skip, or delete the test if the feature was removed.
- Q4–Q7: Fix the errors. Run the tool, address each issue.
- Q8: Remove unused exports, or add `// ts-prune-ignore-next` if they're part of the public API.

---

### Step 5: Documentation Freshness

| # | Check | Command | Severity |
|---|-------|---------|----------|
| F1 | README.md exists | File check | 🔴 Fix Now |
| F2 | README freshness vs. source | Compare `git log -1 --format=%cr -- README.md` vs `git log -1 --format=%cr -- src/` | 🟡 if src is >30 days newer |
| F3 | CHANGELOG exists | File check | 🟡 Fix Soon (for published packages) |
| F4 | Broken internal links | See below | 🟡 Fix Soon |
| F5 | LICENSE file present | File check | 🔴 Fix Now |
| F6 | LICENSE matches package metadata | Compare LICENSE text with `package.json` `license` / `pyproject.toml` `license` | 🟡 Fix Soon |
| F7 | AGENTS.md references valid paths | If `.pi/AGENTS.md` exists, check that referenced files/dirs exist | 🟡 Fix Soon |

**F4 — Broken link check:**

```bash
# Find markdown links and verify targets exist
grep -roE '\[([^]]+)\]\(([^)]+)\)' *.md docs/**/*.md 2>/dev/null | \
  grep -v 'http' | \
  while IFS= read -r line; do
    # Extract path from markdown link
    path=$(echo "$line" | sed 's/.*](\([^)]*\)).*/\1/' | sed 's/#.*//')
    if [ -n "$path" ] && [ ! -e "$path" ]; then
      echo "BROKEN: $line"
    fi
  done
```

**How to fix:**

- F1: Write a README with: what it does, how to install, how to use, prerequisites, license.
- F2: Review README against current code — update examples, API docs, feature lists.
- F3: Add a CHANGELOG.md. Consider `@changesets/cli` for automated generation (see `pre-release` skill).
- F4: Update or remove broken links.
- F5: Add a LICENSE file. Use [choosealicense.com](https://choosealicense.com) if unsure.
- F6: Make LICENSE file and metadata agree.
- F7: Update AGENTS.md to reflect current project structure.

---

### Step 6: Configuration Consistency

| # | Check | How | Severity |
|---|-------|-----|----------|
| X1 | EditorConfig present | `.editorconfig` exists | ℹ️ Info |
| X2 | Strict mode (TS) | `tsconfig.json` → `"strict": true` | 🟡 Fix Soon |
| X3 | Formatter configured | `.prettierrc` / `ruff.toml` / `gofmt` (built-in) | 🟡 Fix Soon |
| X4 | Linter configured | `.eslintrc*` or `eslint.config.*` / `ruff.toml` / `golangci-lint` config | 🟡 Fix Soon |
| X5 | Engine constraints match CI | `package.json` `engines` vs CI matrix; `pyproject.toml` `requires-python` vs CI | 🟡 Fix Soon |
| X6 | `.nvmrc` / `.python-version` matches | Compare with `engines` / `requires-python` / CI config | ℹ️ Info |

**How to fix:**

- X1: Add `.editorconfig`. Minimal: `root = true`, `[*]` block with `indent_style`, `indent_size`, `end_of_line`, `insert_final_newline`.
- X2: Set `"strict": true` in `tsconfig.json`. Fix resulting type errors (usually worth it).
- X3–X4: Add config files. Use the project's existing style as a baseline.
- X5–X6: Pick one source of truth (recommend `engines` / `requires-python`) and align everything else.

---

### Step 7: Security Posture

Lightweight security checks for ongoing hygiene. For the full pre-release security audit
(gitleaks, trufflehog, workflow audit), use the `pre-release` skill.

| # | Check | Command | Severity |
|---|-------|---------|----------|
| S1 | No tracked `.env` or `.local` files | `git ls-files '*.env' '*.env.*' '*.local' '*.local.*' '.env' '.env.local'` | 🔴 Fix Now |
| S2 | `.env.example` exists (if `.env` in `.gitignore`) | File check | 🟡 Fix Soon |
| S3 | No hardcoded secrets in source | `git grep -iE '(api[_-]?key\|secret\|password\|token)\s*[:=]\s*["\x27][^"\x27]{8,}' -- ':!*.lock' ':!node_modules' ':!*.example' ':!*.sample'` | 🔴 Fix Now |
| S4 | Secrets scanning config present | `.gitleaks.toml` or pre-commit hooks | ℹ️ Info |
| S5 | No broad file permissions | Check for `chmod 777` or `0777` in scripts | 🔴 Fix Now |

**How to fix:**

- S1: `git rm --cached <file>`, add to `.gitignore`, commit. If the file contained real secrets, rotate them immediately — they're in git history.
- S2: Create `.env.example` with placeholder values (`<REPLACE_ME>`) for every var in `.env`.
- S3: Move secrets to env vars or a secrets manager. Replace in code with `process.env.VAR` / `os.environ["VAR"]`.
- S4: Add `.gitleaks.toml` (even a minimal one enables CI scanning). Or add `gitleaks` to pre-commit hooks.
- S5: Use least-privilege permissions (`644` for files, `755` for executables).

---

### Step 8: Project Metadata

| # | Check | How | Severity |
|---|-------|-----|----------|
| M1 | Required package fields | `name`, `version`, `description`, `license` in `package.json` / `pyproject.toml` | 🟡 Fix Soon |
| M2 | Repository URL set | `repository` field in package metadata | 🟡 Fix Soon |
| M3 | Keywords present | `keywords` array | ℹ️ Info |
| M4 | `FUNDING.yml` (public repos) | `.github/FUNDING.yml` exists | ℹ️ Info |
| M5 | Pi package compliance | If ships skills/extensions: `pi-package` keyword, `pi` manifest, `files` includes skill dirs | 🟡 Fix Soon (if applicable) |

**How to fix:**

- M1–M3: Add the missing fields to `package.json` or `pyproject.toml`.
- M4: Create `.github/FUNDING.yml` with `github: <username>`.
- M5: See [pi package docs](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#pi-packages) for required fields.

---

## Baseline Tracking

Save a baseline after each run to detect drift over time. Store at `.pi/hygiene-baseline.json`:

```json
{
  "timestamp": "2026-02-14T23:00:00Z",
  "stack": ["node"],
  "scores": {
    "dependencies": { "status": "healthy", "vulns": 0, "outdated": 3, "unused": 0 },
    "git": { "status": "healthy", "stale_branches": 0, "large_files": 0 },
    "ci": { "status": "warning", "unpinned_actions": 2, "permission_issues": 0 },
    "quality": { "status": "healthy", "todos": 5, "skipped_tests": 0, "lint_clean": true },
    "docs": { "status": "warning", "readme_stale_days": 45, "broken_links": 1 },
    "config": { "status": "healthy", "strict_ts": true, "formatter": true, "linter": true },
    "security": { "status": "healthy", "tracked_env": 0, "hardcoded_secrets": 0 },
    "metadata": { "status": "healthy", "complete": true }
  },
  "overall": "7/10"
}
```

On subsequent runs, compare with baseline and flag regressions:

```text
📉 Dependencies: 0 → 3 vulnerabilities (regression since last check)
📈 Quality: 15 → 5 TODOs (improvement!)
→  CI: unchanged — 2 unpinned actions remain
```

When the user approves the report, offer to update the baseline.

---

## Report Format

Present the final report as a health scorecard:

```markdown
# Repo Health: <project-name>
## Score: 7/10 — GOOD
## Stack: Node.js + TypeScript
## Last check: 2026-01-15 (30 days ago) | Baseline: 6/10 📈

### 🔴 Fix Now (2)
| # | Category | Issue | Fix |
|---|----------|-------|-----|
| S1 | Security | `.env.local` tracked in git | `git rm --cached .env.local` |
| D1 | Deps | 2 high-severity npm audit findings | `npm audit fix` |

### 🟡 Fix Soon (4)
| # | Category | Issue | Fix |
|---|----------|-------|-----|
| D2 | Deps | 8 outdated packages (2 major) | `npm outdated` → upgrade |
| C2 | CI | 3 actions not pinned by SHA | Pin to commit SHA |
| F2 | Docs | README 45 days behind source | Review and update |
| Q3 | Quality | 2 skipped tests | Fix or remove |

### 🟢 Healthy (12)
- ✅ Dependencies: no unused, no phantom, lockfile fresh
- ✅ Git: clean tree, no stale branches, no large files
- ✅ Code: lint clean, build passes, tests pass, strict TS
- ✅ Config: EditorConfig, Prettier, ESLint all configured
- ✅ Security: no tracked secrets, .env.example present
- ✅ Metadata: all fields present, license matches

### 📊 Trends (vs. baseline 2026-01-15)
| Category | Then | Now | Trend |
|----------|------|-----|-------|
| Vulnerabilities | 0 | 2 | 📉 |
| Outdated deps | 5 | 8 | 📉 |
| TODOs | 15 | 8 | 📈 |
| Skipped tests | 0 | 2 | 📉 |

### Recommendations
1. **Immediate**: Fix the 2 security/vulnerability items above
2. **This week**: Pin CI actions and update stale README
3. **Ongoing**: Address skipped tests and outdated deps in next sprint

Use your project's task tracking to schedule these items.
```

---

## Scoring

Calculate the score from check results:

| Result | Points deducted |
|--------|----------------|
| Each 🔴 Fix Now | −1.5 |
| Each 🟡 Fix Soon | −0.5 |
| ℹ️ Info | 0 |

Start at 10, apply deductions, floor at 0. Round to nearest integer.

| Score | Label |
|-------|-------|
| 9–10 | 🟢 EXCELLENT |
| 7–8 | 🟢 GOOD |
| 5–6 | 🟡 FAIR |
| 3–4 | 🟠 NEEDS WORK |
| 0–2 | 🔴 POOR |

---

## Auto-Fix Offers

After presenting the report, offer to fix issues that are safe and mechanical.
**Always present what will be done and get confirmation before executing.**

### Safe to offer (low risk, reversible)

- Delete merged local branches (`git branch -d`)
- Run `npm audit fix` (compatible fixes only, not `--force`)
- Run `npm dedupe` / `go mod tidy`
- Add missing `.gitignore` patterns
- Add `.editorconfig` from template
- Remove `console.log` from source files
- Create `.env.example` from `.env` (with values replaced by `<REPLACE_ME>`)
- Add missing `package.json` fields (description, repository, keywords)
- Create `.github/FUNDING.yml`

### Offer with warning (confirm carefully)

- Delete merged remote branches (`git push origin --delete`)
- Run `npm audit fix --force` (may have breaking changes)
- Major dependency upgrades
- Enable TypeScript strict mode (may produce many errors)
- Update CI action pinning (must verify correct SHAs)

### Never auto-fix (explain, let user decide)

- Removing tracked `.env` files (may need secret rotation)
- Rewriting git history (BFG / filter-repo)
- Changing license files
- Modifying CI permissions model
- Removing hardcoded secrets (need to determine replacement strategy)

---

## Tips

- **Run early, run often.** A monthly cadence catches drift before it compounds.
- **Don't try to fix everything at once.** Focus on 🔴 items first, batch 🟡 items into a maintenance sprint.
- **Baseline tracking is your friend.** Even if the score isn't perfect, trending upward means you're winning.
- **Pair with pre-release.** Run `repo-hygiene` for ongoing health, `pre-release` when you're ready to ship. They complement each other — hygiene keeps the baseline high so pre-release has fewer surprises.
- **New repos start clean.** Run this right after `git init` to establish a perfect baseline. It's easier to maintain 10/10 than to recover from 4/10.
