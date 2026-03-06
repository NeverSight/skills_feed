---
name: ralph
description: "Convert PRDs to prd.json format for the Ralph autonomous agent system. Use when you have an existing PRD and need to convert it to Ralph's JSON format. Triggers on: convert this prd, turn this into ralph format, create prd.json from this, ralph json."
user-invocable: true
---

# Ralph PRD Converter

Converts existing PRDs to `prd.json` for Ralph's autonomous execution loop.

## The Job

Convert a PRD (markdown or text) into `prd.json`, then run Pre-flight Setup to create the worktree and configure the environment inside it.

**YOU MUST create a git worktree.** Do NOT skip worktree creation. Do NOT write prd.json to the main working tree. The worktree is where Ralph runs — all files go there.

## Pre-flight Setup

1. **Project name** — read `package.json` `name` field; fall back to directory basename.
2. **MANDATORY: Create worktree & cd into it** (do this FIRST after determining `branchName` — do NOT proceed without it):
   - Derive `<feature-name>` by stripping `ralph/` from prd.json `branchName`
   - `mkdir -p .claude/worktrees/ralph`
   - If branch exists locally: `git worktree add .claude/worktrees/ralph/<feature-name> <branchName>`
   - Otherwise: `git worktree add -b <branchName> .claude/worktrees/ralph/<feature-name> main`
   - Skip if worktree already exists
   - `cd .claude/worktrees/ralph/<feature-name>/` — **all subsequent steps operate inside the worktree**
3. **Copy runtime files** — copy from this skill's `ralph/` subdirectory into worktree's `scripts/ralph/`:
   - `ralph.sh`, `ralph-tree.sh` → `chmod +x`
   - `CLAUDE.md`, `ralph-audit.ts`, `prd.json`
   - Copy `progress.txt` if it exists in source project
4. **Set NTFY_TOPIC** — in worktree's `scripts/ralph/ralph.sh`, replace `<project-name>` placeholder with actual project name. Skip if already customized.
5. **Add package.json scripts** — if worktree's `package.json` exists, add missing entries:
   - `"ralph-tree": "bash scripts/ralph/ralph-tree.sh"`
   - `"ralph-audit": "bun scripts/ralph/ralph-audit.ts"`
6. **Verify curl** — required by ralph.sh for ntfy.sh notifications.
7. **Confirm setup & commit** — print summary: file status, NTFY_TOPIC, worktree path, curl availability.
   - `git add scripts/ralph/{prd.json,CLAUDE.md,progress.txt}` then `git commit -m "chore(ralph): add PRD for <feature-name>"`
   - Print launch command: `bun run ralph-tree ralph/<feature-name>`

## Output Format

```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Story Size — The Number One Rule

Each story must be completable in ONE Ralph iteration (one context window). Ralph spawns a fresh instance per iteration with no memory of previous work.

**Right-sized:** add a DB column, add a UI component, update a server action, add a filter.
**Too big (split):** "build the dashboard", "add auth", "refactor the API".

Rule of thumb: if you can't describe the change in 2-3 sentences, split it.

## Story Ordering

Dependencies first: schema/migrations → backend logic → UI components → aggregation views.

## Acceptance Criteria

Must be verifiable — something Ralph can CHECK.

**Good:** "Add `status` column with default 'pending'", "Filter has options: All, Active, Done", "Typecheck passes"
**Bad:** "Works correctly", "Good UX", "Handles edge cases"

Always include `"Typecheck passes"` as final criterion.
Add `"Tests pass"` for testable logic.
Add `"Use nuxt-ui, tailwind-ui, and frontend-design skills"` for UI changes.
Add `"Verify in browser using dev-browser skill"` for UI changes.
Add `"Use nuxt-terraform skill"` for stories involving AWS infrastructure or GraphQL (AppSync, DynamoDB, Cognito, Lambda, schema changes).

## Conversion Rules

1. Each user story → one JSON entry
2. IDs: sequential `US-001`, `US-002`, ...
3. Priority: dependency order, then document order
4. All stories: `passes: false`, empty `notes`
5. branchName: kebab-case from feature name, prefixed `ralph/`
6. Every story gets `"Typecheck passes"` criterion

## Splitting Large PRDs

Break big features into focused, independent stories. Example: "Add notification system" becomes: 1) notifications table, 2) notification service, 3) bell icon, 4) dropdown panel, 5) mark-as-read, 6) preferences page.

See `references/example.md` for a full input/output conversion example.

## Archiving Previous Runs

Before writing new `prd.json`, check for an existing one with a different `branchName`. If different and `progress.txt` has content beyond the header: archive to `archive/YYYY-MM-DD-feature-name/` in the source project, copy the archive directory into the worktree's `archive/` as well, then reset `progress.txt`.

## Checklist

- [ ] Worktree created at `.claude/worktrees/ralph/<feature-name>/`
- [ ] Pre-flight complete (runtime files copied, NTFY_TOPIC set, package.json scripts added)
- [ ] Previous run archived if needed
- [ ] Each story fits one iteration
- [ ] Dependency order respected
- [ ] Every story has "Typecheck passes"
- [ ] UI stories have "Use nuxt-ui, tailwind-ui, and frontend-design skills"
- [ ] UI stories have "Verify in browser using dev-browser skill"
- [ ] Criteria are verifiable, not vague
- [ ] No story depends on a later story
