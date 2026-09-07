---
name: longgraph
description: Route and author durable long-horizon loop-graph runs. Use for multi-round work needing durable state, gated milestones, owner boundaries, host switching, or independent audit. Route code cleanup to /loop-converge, feature requirements to /loop-deliver, and evidence-backed solution comparison to /loop-research; use loop-graph directly only for a custom run shape. For a self-contained task, recommend the host's ordinary task or goal directly. Do not execute or resume generated runtime node files.
---

# longgraph — route to the right durable run

longgraph has one shared compiler, [`loop-graph`](skills/loop-graph/SKILL.md),
and focused entries that bind only goal-specific rules. All compile the same
executor, supervisor, ledger, directives, and ops artifacts. Do not execute the
generated runtime nodes from this authoring skill.

## Fit and route

- Use [`loop-converge`](skills/loop-converge/SKILL.md) for multi-round unused
  code, duplication, consolidation, reuse, or slimming.
- Use [`loop-deliver`](skills/loop-deliver/SKILL.md) for a product or engineering
  requirement that needs incremental implementation and acceptance proof.
- Use [`loop-research`](skills/loop-research/SKILL.md) to compare feasible
  approaches with open-source implementations, primary research, and controlled
  experiments before committing to one.
- Use [`loop-graph`](skills/loop-graph/SKILL.md) directly only when none of the
  focused packs fits but the work still needs durable state, gates, owner
  boundaries, host switching, or independent verification.
- If the request is one self-contained task that fits a normal host goal/task,
  explain that longgraph adds no value and recommend sending the task directly. Do
  not wrap it in another objective or invent a lighter longgraph mode.

Shared reference: [`lib/methodology.md`](lib/methodology.md) explains why the graph's
discipline exists. The baseline and pack boundary is in
[`skills/loop-graph/docs/preset-contract.md`](skills/loop-graph/docs/preset-contract.md).
