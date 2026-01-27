---
name: review
description: "Code review with semantic diffs, expert routing, and auto-TaskCreate. Triggers on: code review, review changes, check code, review PR, security audit."
allowed-tools: "Read Write Edit Bash Glob Grep Task TaskCreate TaskUpdate"
---

# Review Skill - AI Code Review

Perform comprehensive code reviews on staged changes, specific files, or pull requests. Routes to expert agents based on file types and automatically creates tasks for critical issues.

## Architecture

```
review [target] [--focus] [--depth]
    │
    ├─→ Step 1: Determine Scope
    │     ├─ No args → git diff --cached (staged)
    │     ├─ --all → git diff HEAD (all uncommitted)
    │     ├─ File path → specific file diff
    │     └─ --pr N → gh pr diff N
    │
    ├─→ Step 2: Analyze Changes (parallel)
    │     ├─ delta for syntax-highlighted diff
    │     ├─ difft for semantic diff (structural)
    │     ├─ Categorize: logic, style, test, docs, config
    │     └─ Identify touched modules/components
    │
    ├─→ Step 3: Load Project Standards
    │     ├─ AGENTS.md, CLAUDE.md conventions
    │     ├─ .eslintrc, .prettierrc, pyproject.toml
    │     ├─ Detect test framework
    │     └─ Check CI config for existing linting
    │
    ├─→ Step 4: Route to Expert Reviewers
    │     ├─ TypeScript → typescript-expert
    │     ├─ React/JSX → react-expert
    │     ├─ Python → python-expert
    │     ├─ Go → go-expert
    │     ├─ Rust → rust-expert
    │     ├─ Vue → vue-expert
    │     ├─ SQL/migrations → postgres-expert
    │     ├─ Claude extensions → claude-architect
    │     └─ Multi-domain → parallel expert dispatch
    │
    ├─→ Step 5: Generate Review
    │     ├─ Severity: CRITICAL / WARNING / SUGGESTION / PRAISE
    │     ├─ Line-specific comments (file:line refs)
    │     ├─ Suggested fixes as diff blocks
    │     └─ Overall verdict: Ready to commit? Y/N
    │
    └─→ Step 6: Integration
          ├─ Auto-create tasks (TaskCreate) for CRITICAL issues
          ├─ Link to /save for tracking
          └─ Suggest follow-up: /testgen, /explain
```

## Execution Steps

### Step 1: Determine Scope

```bash
# Default: staged changes
git diff --cached --name-only

# Check if anything is staged
STAGED=$(git diff --cached --name-only | wc -l)
if [ "$STAGED" -eq 0 ]; then
    echo "No staged changes. Use --all for uncommitted or specify a file."
    git status --short
fi
```

**For PR review:**
```bash
gh pr diff $PR_NUMBER --patch
```

**For specific file:**
```bash
git diff HEAD -- "$FILE"
```

**For baseline comparison (--base):**
```bash
git diff $BASE_BRANCH...HEAD
```

### Step 2: Analyze Changes

Run semantic diff analysis (parallel where possible):

**With difft (semantic):**
```bash
command -v difft >/dev/null 2>&1 && git difftool --tool=difftastic --no-prompt HEAD~1 || git diff HEAD~1
```

**With delta (syntax highlighting):**
```bash
command -v delta >/dev/null 2>&1 && git diff --cached | delta || git diff --cached
```

**Categorize changes:**
```bash
git diff --cached --name-only | while read file; do
    case "$file" in
        *.test.* | *.spec.*) echo "TEST: $file" ;;
        *.md | docs/*) echo "DOCS: $file" ;;
        *.json | *.yaml | *.toml) echo "CONFIG: $file" ;;
        *) echo "CODE: $file" ;;
    esac
done
```

**Get diff statistics:**
```bash
git diff --cached --stat
```

### Step 3: Load Project Standards

```bash
# Claude Code conventions
cat AGENTS.md 2>/dev/null | head -50
cat CLAUDE.md 2>/dev/null | head -50

# Linting configs
cat .eslintrc* 2>/dev/null | head -30
cat .prettierrc* 2>/dev/null
cat pyproject.toml 2>/dev/null | head -30

# Test framework detection
cat package.json 2>/dev/null | jq '.devDependencies | keys | map(select(test("jest|vitest|mocha|cypress|playwright")))' 2>/dev/null
```

**Check CI for existing linting:**
```bash
cat .github/workflows/*.yml 2>/dev/null | grep -E "eslint|prettier|pylint|ruff" | head -10
```

### Step 4: Route to Expert Reviewers

| File Pattern | Primary Expert | Secondary Expert |
|--------------|----------------|------------------|
| `*.ts` | typescript-expert | - |
| `*.tsx` | react-expert | typescript-expert |
| `*.vue` | vue-expert | typescript-expert |
| `*.py` | python-expert | sql-expert (if ORM) |
| `*.go` | go-expert | - |
| `*.rs` | rust-expert | - |
| `*.sql`, `migrations/*` | postgres-expert | - |
| `agents/*.md`, `skills/*`, `commands/*` | claude-architect | - |
| `*.test.*`, `*.spec.*` | cypress-expert | (framework expert) |
| `*.cy.ts`, `cypress/*` | cypress-expert | typescript-expert |
| `*.spec.ts` (Playwright) | typescript-expert | - |
| `playwright/*`, `e2e/*` | typescript-expert | - |
| `wrangler.toml`, `workers/*` | wrangler-expert | cloudflare-expert |
| `*.sh`, `*.bash` | bash-expert | - |

**Invoke via Task tool:**
```
Task tool with subagent_type: "[detected]-expert"
Prompt includes:
  - Diff content
  - Project conventions from AGENTS.md
  - Linting config summaries
  - Requested focus area
  - Request for structured review output
```

### Step 5: Generate Review

The expert produces a structured review:

```markdown
# Code Review: [scope description]

## Summary

| Metric | Value |
|--------|-------|
| Files reviewed | N |
| Lines changed | +X / -Y |
| Issues found | N (X critical, Y warnings) |

## Verdict

**Ready to commit?** Yes / No

[1-2 sentence summary of overall quality]

---

## Critical Issues

### `src/auth/login.ts:42`

**Issue:** SQL injection vulnerability in user input handling

**Risk:** Attacker can execute arbitrary SQL queries

**Fix:**
```diff
- const query = `SELECT * FROM users WHERE id = ${userId}`;
+ const query = `SELECT * FROM users WHERE id = $1`;
+ const result = await db.query(query, [userId]);
```

---

## Warnings

### `src/components/Form.tsx:89`

**Issue:** Missing dependency in useEffect

**Suggestion:** Add `userId` to dependency array

```diff
- useEffect(() => { fetchUser(userId) }, []);
+ useEffect(() => { fetchUser(userId) }, [userId]);
```

---

## Suggestions

[Style improvements, optional enhancements]

---

## Praise

[Good patterns worth noting]

---

## Files Reviewed

| File | Changes | Issues |
|------|---------|--------|
| `src/auth/login.ts` | +42/-8 | 1 critical |
```

### Step 6: Integration

**Auto-create tasks for CRITICAL issues:**
```
TaskCreate:
  subject: "Fix: SQL injection in login.ts:42"
  description: "SQL injection vulnerability found in user input handling."
  activeForm: "Fixing SQL injection in login.ts:42"
```

**Link with dependencies for related issues:**
```
TaskCreate: #1 "Fix SQL injection in login.ts"
TaskCreate: #2 "Fix SQL injection in register.ts"
TaskUpdate: taskId: "2", addBlockedBy: ["1"]
```

**After fixing issues:**
```
TaskUpdate:
  taskId: "1"
  status: "completed"
```

---

## Severity System

| Level | Icon | Meaning | Action | Auto-Task? |
|-------|------|---------|--------|------------|
| CRITICAL | :red_circle: | Security bug, data loss risk, crashes | Must fix before merge | Yes |
| WARNING | :yellow_circle: | Logic issues, performance problems | Should address | No |
| SUGGESTION | :blue_circle: | Style, minor improvements | Optional | No |
| PRAISE | :star: | Good patterns worth noting | Recognition | No |

---

## Focus Modes

| Mode | What It Checks |
|------|----------------|
| `--security` | OWASP top 10, secrets in code, injection, auth issues |
| `--perf` | N+1 queries, unnecessary re-renders, complexity, memory |
| `--types` | Type safety, `any` usage, generics, null handling |
| `--tests` | Coverage gaps, test quality, mocking patterns |
| `--style` | Naming, organization, dead code, comments |
| (default) | All of the above |

---

## Depth Modes

| Mode | Behavior |
|------|----------|
| `--quick` | Surface-level scan, obvious issues only |
| `--normal` | Standard review, all severity levels (default) |
| `--thorough` | Deep analysis, traces data flow, checks edge cases |

---

## Advanced Flags

### `--base <branch>` - Baseline Comparison

Compare changes against a specific branch instead of HEAD:

```bash
/review --base main
/review src/ --base develop --thorough
```

### `--json` - CI/CD Integration

Output review results as JSON:

```json
{
  "summary": {
    "files_reviewed": 3,
    "lines_changed": { "added": 42, "removed": 8 },
    "issues": { "critical": 1, "warning": 2, "suggestion": 1 }
  },
  "verdict": {
    "ready_to_commit": false,
    "reason": "1 critical issue requires attention"
  },
  "issues": [...]
}
```

**CI/CD usage:**
```yaml
- name: Code Review
  run: |
    claude "/review --json" > review.json
    if jq -e '.issues[] | select(.severity == "critical")' review.json; then
      exit 1
    fi
```

### `--fix` - Auto-Apply Fixes

Automatically apply suggested fixes:

1. Performs standard review
2. For each fixable issue, prompts for confirmation
3. Uses Edit tool to apply approved fixes
4. Creates TaskUpdate for resolved issues

**Non-interactive mode:**
```bash
/review --fix --auto-approve
```

---

## CLI Tool Integration

| Tool | Purpose | Fallback |
|------|---------|----------|
| `delta` | Syntax-highlighted diffs | `git diff` |
| `difft` | Semantic/structural diffs | `git diff` |
| `gh` | GitHub PR operations | Manual diff |
| `rg` | Search for patterns | Grep tool |
| `jq` | Parse JSON configs | Read manually |

**Graceful degradation:**
```bash
command -v delta >/dev/null 2>&1 && git diff --cached | delta || git diff --cached
```

---

## Reference Files

For framework-specific checks, see:
- `framework-checks.md` - React, TypeScript, Python, Go, Rust, Vue, SQL patterns

---

## Integration

| Command | Relationship |
|---------|--------------|
| `/explain` | Deep dive into flagged code |
| `/testgen` | Generate tests for issues found |
| `/save` | Persist review findings to session state |
