---
name: scan
description: Scans the codebase against another skill's criteria using a parallel agent team. Use when the user says /scan <skill-name> to audit code quality, find violations, or assess conformance to best practices.
---

# Codebase Scan

Audit the codebase against another skill's criteria using a parallel agent team.

## Workflow

### 1. Parse args & load skill

Extract the skill name from the args passed to this skill.

- If no skill name provided, list available skills in `.claude/skills/` and ask the user which to scan against.
- If skill doesn't exist, list available skills and tell the user.
- Read `.claude/skills/<name>/SKILL.md` plus any files in `references/` and `rules/` subdirectories.
- Distill the skill's content into a numbered **criteria checklist**: a flat list of concrete, testable rules labeled C1, C2, C3, etc. Each criterion should be a single sentence describing what to check for.
- If the skill has no evaluable code criteria (e.g., workflow-only skills like `why` that don't define code patterns or rules), tell the user it's not scannable and stop.

### 2. Discover relevant files

Use the skill's criteria to infer file scope:

- React/frontend criteria → `app/**/*.tsx`, `app/**/*.ts`
- Backend criteria → `services/**/*.ts`
- General/mixed → both of the above
- CSS/styling → `app/**/*.css`, `app/**/*.tsx`

Always exclude: `node_modules/`, `dist/`, `*.test.*`, `*.spec.*`, `**/migrations/**`, `**/*.d.ts`, generated files.

Count candidate files. If zero, tell the user and stop.

### 3. Plan team composition

Split files into chunks by directory subtree so no file is assigned to two agents:

| Candidate files | Teammates |
|----------------|-----------|
| < 100          | 2 (or skip team for < 20) |
| 100–500        | 3 |
| 500+           | 4–5, split by top-level directory |

For very small scans (< 20 files), skip the team — scan inline and jump to step 6.

### 4. Spawn scan team

1. `spawnTeam` with name `scan-<skill-name>`
2. Create one `TaskCreate` per chunk with:
   - Subject: `Scan <directory-area> against <skill-name> criteria`
   - Description: Include the **full criteria checklist**, the file scope (glob patterns), and the teammate instructions from `references/teammate-instructions.md`
3. Spawn teammates as `general-purpose` subagent_type (they need Read, Glob, Grep + team communication)
4. Name teammates `scanner-1`, `scanner-2`, etc.
5. Assign tasks via `TaskUpdate` with `owner`

### 5. Collect & synthesize

Wait for all teammates to complete their tasks. Each teammate reports findings in structured format:

```
FINDING: C<n> | SEVERITY | file/path.ts:LINE | Description
```

Collect all findings from teammate messages.

### 6. Generate report

Create `.claude-scan/<skill-name>.md` using the format in `references/report-format.md`.

Key sections:
- Executive Summary (2-3 sentences)
- Criteria Evaluated (table with violation counts)
- Findings by Severity (Critical → Warning → Info tables)
- Patterns Observed
- Statistics
- Recommended Fix Order (batched by non-overlapping file groups)

### 7. Cleanup & present

- If a team was spawned: send `shutdown_request` to all teammates, then `cleanup`
- Display inline summary: total findings by severity, top violated criteria, scan scope
- Tell the user the full report is at `.claude-scan/<skill-name>.md`
- Ask: "Want me to spawn a fix team to address these findings?"

### 8. Fix team (if user says yes)

1. Read the report's "Recommended Fix Order" section
2. Group fixes into non-overlapping file batches
3. `spawnTeam` with name `fix-<skill-name>`
4. Create tasks per batch — each task description includes:
   - The specific violations to fix (from the report)
   - The relevant criteria definitions
   - Instructions from `references/fix-team-instructions.md`
5. Spawn `general-purpose` teammates named `fixer-1`, `fixer-2`, etc. (need Edit/Write)
6. Assign tasks and wait for completion
7. Shutdown and cleanup fix team
8. Ask user if they want to re-scan to verify fixes
