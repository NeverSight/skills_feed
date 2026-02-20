---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

- Have an implementation plan with mostly independent tasks
- Want to stay in the current session (otherwise use `executing-plans`)
- See [references/process-detail.md](references/process-detail.md) for decision tree and full process flow diagrams

## The Process

1. **Load plan** — Read `plan.md` + `manifest.json`. Note task IDs and waves. Do NOT read briefing files into your context.
2. **Dispatch per task** — Send implementer a 2-3 sentence summary + briefing file path. Agent reads its own briefing from disk.
3. **Two-stage review** — Spec compliance first, then code quality. Both must pass before marking complete.
4. **Wave boundaries** — Re-read `manifest.json` to recover state after context compaction.

## Prompt Templates

- `./implementer-prompt.md` — `./spec-reviewer-prompt.md` — `./code-quality-reviewer-prompt.md`

## Red Flags

**Never:** skip reviews, proceed with unfixed issues, dispatch parallel implementers to overlapping files (use wave plan file ownership to determine — parallel is encouraged when files don't overlap), paste full briefing text inline instead of pointing to briefing file, skip reading the manifest at wave boundaries, start code quality review before spec compliance passes.

- Dispatch prompts missing key sections (see skills-management/references/dispatch-prompt-template.md for the canonical 6-section structure)

**If subagent asks questions:** Answer before proceeding.
**If reviewer finds issues:** Implementer fixes, re-review until approved.

## Cleanup

After all tasks complete and final review passes, before calling `git-workflow stack`:
1. Optionally write `.claude/plans/<plan-id>/summary.md` with execution notes
2. Delete the plan directory: `rm -rf .claude/plans/<plan-id>/`
3. If deletion fails, warn but do not block

## References

- [references/workflow-example.md](references/workflow-example.md) — full walkthrough
- [references/advantages-and-costs.md](references/advantages-and-costs.md) — comparison vs manual/executing plans

**Required skills:** git-workflow, writing-plans, code-review, test-driven-development
