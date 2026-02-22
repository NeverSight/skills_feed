---
name: pipeline-reflection-ux
description: Improve router-facing pipeline and reflection narration to reduce noisy status churn and make Step 0/Reflection outcomes explicit. Use when updating Router output contract, reflection reminder wording, or post-pipeline notification batching.
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Pipeline Reflection UX

Use this skill to keep pipeline/reflection output concise, explicit, and low-noise.

## Workflow

1. Make Step 0 visible in router narration.
2. Emit Step 0 completion before `TaskList()`.
3. Emit a one-line reflection outcome with report path.
4. Batch late post-pipeline notifications into one summary.
5. Keep guardrail semantics unchanged (`block` stays `block`).

## Required Checks

- Add/adjust tests before behavior changes.
- Confirm no regression in routing/taskupdate/read-safety tests.
- Verify debug-log counts improve for repeated violations/noise.

## References

- Detailed UX review: `references/ui-reflection-review.md`
- Troubleshooting runbook: `.claude/docs/TROUBLESHOOTING.md`
- Task tracking protocol: `.claude/docs/@TASK_TRACKING_GUIDE.md`
