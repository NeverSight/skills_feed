---
name: coordinator
description: Use when the user says "vm", "voice mode", "team", "coordinate", or needs to orchestrate multiple agents working on related tasks in parallel
---

# Coordinator

## Overview

Manages two concerns: **output mode switching** (voice vs text) and **agent team orchestration** for parallel task execution.

## Voice/Text Mode Toggle

**Trigger words**: "vm", "voice mode" -> switch to VOICE. "tm", "text mode" -> switch to TEXT.

### VOICE Mode Rules
- Short sentences, max 2 lines each
- Bullet points for all lists
- No code blocks longer than 3 lines — summarize verbally instead
- Confirm before executing any tool: "I'll [action]. Go ahead?"
- Use plain language, avoid jargon
- When showing code changes, describe what changed rather than showing diffs

### TEXT Mode Rules (Default)
- Full detailed responses with code blocks
- Show diffs, full implementations, detailed explanations
- Execute tools without pre-confirmation (unless destructive)

## Agent Team Orchestration

### When to Use Teams
- Task has 3+ independent subtasks
- Different subtasks need different expertise (e.g., implementation + testing + review)
- Work can be parallelized without merge conflicts

### Orchestration Details

Read [references/team-orchestration.md](references/team-orchestration.md) for the full coordination pattern (DECOMPOSE -> WAVE PLAN -> DISPATCH -> GATE -> VERIFY), agent spawn rules, model selection table, context budget management, and conflict resolution.

## Plan-Driven Orchestration

When orchestrating execution of a structured plan (`.claude/plans/<plan-id>/`):

### At Session Start
Read `plan.md` and `manifest.json`. The manifest defines waves and task dependencies. Use the manifest's wave grouping directly — do not re-derive wave structure.

### At Each Wave Boundary
Re-read `manifest.json` from disk. This protects against context compaction loss. Update task statuses in the manifest after each wave completes.

### Agent Dispatch
Point each agent at its briefing file. Do NOT paste briefing content inline. Include in dispatch prompt: plan-id, task-id, briefing path, working directory.

### After Final Wave
1. Optionally write `.claude/plans/<plan-id>/summary.md` with execution notes
2. Delete the plan directory: `rm -rf .claude/plans/<plan-id>/`
3. If deletion fails, warn but do not block

## Common Mistakes
- Spawning agents without full context in the prompt
- Letting multiple agents modify the same file
- Skipping verification after merging agent outputs
- Using teams for tasks that are naturally sequential
- Putting dependent tasks in the same wave (task B needs task A's output -> different waves)
- Pasting full briefing text inline instead of pointing agents to their briefing file
- Not re-reading manifest at wave boundaries (context compaction can lose state)
