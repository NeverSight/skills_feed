---
name: agents-md
description: Audits AGENTS.md and CLAUDE.md files using execution-first standards. Checks commands, gotchas, and signal-to-noise ratio. Use when asked to audit, review, score, refactor, or improve agent instruction files, fix stale commands, or reduce bloat.
---

# AGENTS.md / CLAUDE.md Audit

AGENTS.md and CLAUDE.md are execution contracts, not knowledge bases.

**Litmus test for every line:** "Would removing this cause the agent to make a mistake?" If no, cut it. Bloated instruction files cause agents to ignore actual rules.

## Reference Files

| File | Read When |
|------|-----------|
| `references/quick-checklist.md` | Default: fast triage (10 checks, target >= 8/10) |
| `references/quality-criteria.md` | Full audit mode or when quick audit fails |
| `references/refactor-workflow.md` | File is bloated (>150 lines) or low-signal |
| `references/root-content-guidance.md` | Deciding what stays in root vs separate files |
| `references/templates.md` | Drafting new file or rebuilding from scratch |

## Quick Example

**Input:** AGENTS.md with stale commands and generic advice
**Quick audit result:** 5/10 (Fail)
**Key issues:** Missing test command, generic "follow best practices" advice, dead link to deleted folder
**Fix:** Add `npm test`, replace generic advice with specific gotcha, remove dead link
**After:** 9/10 (Pass)

## How to Use

Default path:
- Start with quick audit using `references/quick-checklist.md` (10 checks)
- Escalate to full audit (`references/quality-criteria.md`) only when quick audit fails, file is high-risk, or user requests it
- Apply edits only after reporting findings and getting confirmation

Progressive loading:
- Always load the checklist for the selected audit mode
- Load `references/refactor-workflow.md` only for low-signal files (below target score, stale commands, or root file over ~150 lines)
- Load `references/templates.md` only when drafting a new file or rebuilding from scratch
- Load `references/root-content-guidance.md` only when deciding what stays in root vs moved out

## Audit Workflow

Copy this checklist to track progress:

```
Audit Progress:
- [ ] Step 1: Discover files
- [ ] Step 2: Select audit mode (quick or full)
- [ ] Step 3: Run audit against checklist
- [ ] Step 4: Report findings with score table
- [ ] Step 5: Propose minimal diffs
- [ ] Step 6: Validate changes
- [ ] Step 7: Apply and verify
```

### Step 1: Discover files

Run:

```bash
find . \( -name "AGENTS.md" -o -name "CLAUDE.md" -o -name "CLAUDE.local.md" \) 2>/dev/null | sort
```

Also check for a home-level file: `~/.claude/CLAUDE.md` (applies to all sessions).

CLAUDE.md files can exist at multiple levels — project root, parent directories, and child directories are all loaded automatically. `CLAUDE.local.md` is the gitignored personal variant. Audit each level independently.

For monorepos, include workspace-level instruction files.

### Step 2: Select audit mode

- **Quick audit:** Default for most files (10 checks, target >= 8/10)
- **Full audit:** When quick audit fails, file is high-risk, or user requests full scoring

### Step 3: Run audit

- Quick audit target: **>= 8/10** checks from `references/quick-checklist.md`
- Full audit file-quality target: **>= 91% of applicable points** from `references/quality-criteria.md`
- Full audit execution target: **2/2** when producing an edit proposal
- Score each root file independently

### Step 4: Report findings

Output a concise report before edits:

```markdown
## AGENTS.md Quality Report

| File | Mode | Score | Grade | Key Issues |
|------|------|-------|-------|------------|
| ./AGENTS.md | Quick | 6/10 | Fail | Missing test command, stale path, doc-heavy section |
```

### Step 5: Propose minimal diffs

- Fix broken/stale commands first
- Remove generic, duplicate, or obsolete guidance
- Move deep detail into linked files using `@path/to/file.md` import syntax
- Use emphasis ("IMPORTANT:", "YOU MUST") on critical rules that agents tend to skip
- Keep rewrites incremental and preserve useful wording when possible

Show each proposed change with rationale and a diff snippet.

### Step 6: Validate changes

Validation loop:
1. Run smoke checks for core commands (`dev`, `test`, `build`, `lint/typecheck`) when applicable
2. If commands cannot be run, verify script existence and note the limitation
3. Check that linked paths resolve
4. Confirm no contradictory rules remain
5. If issues found → revise → validate again
6. Only proceed when validation passes

### Step 7: Apply and verify

- Apply approved edits
- After each PR, add at most one new gotcha only if it prevented or fixed a real mistake
- Verify changes by re-running relevant commands
