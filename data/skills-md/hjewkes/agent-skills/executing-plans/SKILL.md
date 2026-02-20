---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan

**Plan directory format** (`.claude/plans/<plan-id>/`):
1. Read orchestration plan at `plan.md` and manifest at `manifest.json`
2. For each task in the current batch, read its briefing file from `briefings/task-NN.md`
3. Only load briefings for the current batch (default 3), not all tasks at once
4. Review critically — identify any questions or concerns about the plan
5. If concerns: Raise them with your human partner before starting
6. If no concerns: Create TodoWrite and proceed

**Legacy monolithic format** (`docs/plans/*.md`):
1. Read the plan file directly
2. Follow the same review and batch process below

**Format detection:** If the path contains `manifest.json` or points to a directory, use plan directory format. If it points to a `.md` file, use legacy format. If no path given, check `.claude/plans/` for the most recent directory, fall back to `docs/plans/` for the most recent `.md`.

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (briefing files have bite-sized steps)
3. Run verifications as specified in the briefing's Success Criteria
4. Mark as completed

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch (load next batch's briefing files)
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified:
1. If using plan directory format, clean up:
   - Optionally write `.claude/plans/<plan-id>/summary.md` with execution notes
   - Delete the plan directory: `rm -rf .claude/plans/<plan-id>/`
   - If deletion fails, warn but do not block
2. Announce: "I'm using the git-workflow skill to complete this work."
3. **REQUIRED SUB-SKILL:** Use git-workflow stack
4. Follow that skill to verify tests, present options, execute choice

## Guardrails

Stop and ask when blocked — don't guess. See [references/guardrails.md](references/guardrails.md) for full stop conditions and checklist.

## Integration

**Required workflow skills:**
- **git-workflow** - REQUIRED: Worktrees for isolated workspaces, stack for completing development
- **writing-plans** - Creates the plan this skill executes
