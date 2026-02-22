---
name: quality-gate
description: Run parallel quality reviews (React, SOLID, Security, Simplification, Slop) on branch changes and auto-fix issues
argument-hint: "[base-branch]"
---

# Quality Gate

!IMPORTANT: Follow this process exactly. Do not skip steps.

**Arguments:** `$0` (optional) — base branch to diff against. If omitted, auto-detect.

## Step 1: Get the Diff

Detect the base branch:
```bash
git rev-parse --verify main >/dev/null 2>&1 && echo "main" || (git rev-parse --verify master >/dev/null 2>&1 && echo "master" || echo "develop")
```

Then get the full diff and changed file list:
```bash
git diff <base>...HEAD --name-only
git diff <base>...HEAD
```

Store the diff output — you will pass it to review agents.

Also detect the project stack:
```bash
# Check if React/Next.js project
cat package.json 2>/dev/null | jq -r '.dependencies // {} | keys[]' | grep -E '^(react|next)$'
```

## Step 2: Parallel Review (Agent Team)

### 2a. Create Team

```
TeamCreate  team_name: "quality-gate"  description: "Parallel quality review of branch changes"
```

### 2b. Create Review Tasks

Create one `TaskCreate` per review dimension. **Skip Task 1 if the project does not use React/Next.js.**

Each task `description` MUST include:
1. The full diff from Step 1 (if diff exceeds ~50KB, list changed files and instruct teammate to read files directly)
2. The list of changed files
3. The skill command to invoke and review instructions (see table below)
4. The classification rules (see below)
5. The required output format (see below)
6. Instruction: **Do NOT modify any files. Report findings only.**
7. Instruction: Send findings to the lead via `SendMessage` with `type: "message"` and `recipient: "lead"`
8. Instruction: Mark task completed via `TaskUpdate` with `status: "completed"` after sending findings

| Task | subject | activeForm | Skill command & instructions |
|------|---------|------------|------------------------------|
| 1 | Review React/Next.js best practices | Reviewing React best practices | `/vercel-react-best-practices Review ONLY the changed code in the diff against the rules. Categorize each finding as FIX or NITPICK` |
| 2 | Review SOLID principles | Reviewing SOLID principles | `/applying-solid-principles Review ONLY the changed code in the diff against SOLID principles and clean code practices. Categorize each finding as FIX or NITPICK` |
| 3 | Review security | Reviewing security | `/security-review Review ONLY the changed code in the diff against the security checklist. Categorize each finding as FIX or NITPICK` |
| 4 | Review simplification opportunities | Reviewing simplification | `/simplify Review ONLY the changed code in the diff for simplification opportunities (clarity, consistency, maintainability). Categorize each finding as FIX or NITPICK. Do NOT modify any files — report only.` |
| 5 | Review code slop | Reviewing code slop | `/code-slop` but **override**: Do NOT modify any files. Instead, identify all slop issues and report them in FIX/NITPICK format below. |

### 2c. Spawn Teammates (all in parallel)

Spawn all teammates **in a single response** using the `Task` tool with `team_name: "quality-gate"` and each teammate's `name`:

| name | Assigned task |
|------|---------------|
| `react-reviewer` | Task 1 (skip if not React) |
| `solid-reviewer` | Task 2 |
| `security-reviewer` | Task 3 |
| `simplify-reviewer` | Task 4 |
| `slop-cleaner` | Task 5 |

Each teammate's prompt must instruct them to:
1. Check `TaskList` and claim their assigned task via `TaskUpdate` with `status: "in_progress"` and `owner: "<their-name>"`
2. Invoke the designated skill via the `Skill` tool with the review instructions
3. Format findings per the output format below
4. Send findings to the lead via `SendMessage` with `type: "message"`, `recipient: "lead"`, and `summary: "<reviewer-name> findings"`
5. Mark task completed via `TaskUpdate` with `status: "completed"`

### 2d. Assign Tasks

After spawning, assign each task to its teammate via `TaskUpdate` with `owner: "<teammate-name>"`.

### Classification Rules (include in each task description)

**FIX** (will be auto-applied):
- Bugs or logic errors
- Security vulnerabilities
- Performance issues with measurable impact
- Clear violations of critical rules
- Obvious simplifications that reduce complexity without trade-offs

**NITPICK** (user decides):
- Style preferences or minor readability tweaks
- Debatable architectural choices
- Low-impact optimizations
- "Nice to have" improvements

### Required Output Format (include in each task description)

```
## FIX
- `file/path.ts:42` — [RULE-ID] Description of the issue. Suggested fix: <concrete suggestion>
- `file/path.ts:85` — [RULE-ID] Description. Suggested fix: <suggestion>

## NITPICK
- `file/path.ts:15` — [RULE-ID] Description. Suggestion: <suggestion>

## NO ISSUES
(use this section if nothing found in a category)
```

If no issues at all, return: `No issues found.`

## Step 3: Consolidate Findings and Tear Down Team

### 3a. Collect Results

Monitor `TaskList` until all review tasks reach `completed` status. Findings arrive automatically via `SendMessage` from each teammate.

### 3b. Shut Down Team

Send `SendMessage` with `type: "shutdown_request"` to each teammate. After all teammates confirm shutdown, call `TeamDelete`.

### 3c. Consolidate

1. Collect all **FIX** items across all reviewers
2. Deduplicate overlapping findings on the same file:line
3. Display a summary:

```
### Quality Gate Results

**Fixes to auto-apply:** N items
- [React] file:line — description (x items)
- [SOLID] file:line — description (x items)
- [Security] file:line — description (x items)
- [Simplify] file:line — description (x items)
- [Slop Cleaner] file:line — description (x items)
**Nitpicks for review:** N items
```

## Step 4: Auto-Fix

Apply all FIX items to the codebase:
- Read each affected file
- Apply the suggested fixes using the Edit tool
- After all fixes, run the project's linter/formatter if configured (check package.json scripts for lint/format)

## Step 5: Present Nitpicks

If there are nitpicks, display them grouped by category and use AskUserQuestion:

```
### Nitpicks for your review

**React/Next.js:**
- `file:line` — description — suggestion

**SOLID:**
- `file:line` — description — suggestion

**Security:**
- `file:line` — description — suggestion

**Simplification:**
- `file:line` — description — suggestion

**Slop Cleaner:**
- `file:line` — description — suggestion
```

Ask: "Which nitpicks should I apply?" with options:
- All of them
- None
- Let me pick (then list individually)

## Step 6: Apply Selected Nitpicks

Apply whichever nitpicks the user selected.

## Step 7: Commit & Push (if changes made)

If any changes were applied (fixes or nitpicks):

```bash
git add .
git commit -m "refactor: apply quality gate fixes"
```

If a remote branch exists and the branch was already pushed:
```bash
git push
```

## Execution Notes

- **Requires**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable in settings
- **Total teammates**: 4-5 (skip react-reviewer if not a React project)
- **Team lifecycle**: `TeamCreate` at Step 2a, `TeamDelete` at Step 3b
- **All review teammates are read-only** — they report findings via SendMessage, the lead applies fixes
- **Teammate idle is normal** — teammates go idle after each turn; do not treat idle notifications as errors
- **Deduplication matters** — multiple reviewers may flag the same issue differently; apply only once
- **Preserve behavior** — fixes must not change functionality, only improve quality
- **Be surgical** — only modify code that was part of the original diff, do not refactor unrelated code
