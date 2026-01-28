---
name: agent-coding-workflows
description: Choose and run the standard AI coding workflows by chaining the other skills; use when the user asks for a workflow or uses /flow, /workflow, /andrej, or /AndrejHide, and when the task type is standard change, algo/perf, or urgent bugfix.
---

# Agent Coding Workflows

## Quick start

- Detect invocation: user asks for a workflow or uses /flow, /workflow, /andrej, or /AndrejHide.
- If /AndrejHide is used, pick the workflow automatically.
- Classify the task: standard change, algo/perf, or urgent bugfix.
- Run the matching workflow steps in order.
- Pull in other skills as needed.

## Workflow selection

- Standard change: most feature or refactor tasks.
- Algo/perf: algorithms, hotspots, or scaling work.
- Urgent bugfix: regressions or production-impacting issues.

## Auto mode

Use this when the user says `/AndrejHide`.

1) If the task mentions performance, scaling, optimization, latency, or complexity -> choose Algo/perf.
2) If the task mentions regression, outage, production bug, or urgent fix -> choose Urgent bugfix.
3) Otherwise -> choose Standard change.
4) If still ambiguous -> run `assumption-clarifier` first, then decide.

## Thresholds (tunable)

Default triggers for plan-lite and review. The user can override by stating new thresholds.

- **Plan-lite required** if any are true:
  - Estimated > 30 minutes, or
  - Touches > 3 files, or
  - Diff > 150 lines, or
  - Changes a production or critical path.

- **Conceptual-reviewer required** if any are true:
  - Any non-trivial task, or
  - Touches > 2 files, or
  - Ambiguous requirements, or
  - Risk of regression.

If the user provides overrides (e.g., "thresholds: files=5 lines=300"), use them for this task.

## Preflight (from Andrej’s post)

Do this before any workflow if the task is non-trivial:

1) Convert the request into explicit success criteria or tests.
2) Surface assumptions and ambiguities early.
3) Keep a lightweight plan (3–5 steps) if risk is non-trivial.
4) Bias toward minimal diffs and simplicity.
5) Reserve a conceptual review pass for subtle errors.

## Workflow A: Standard change

1) Use `assumption-clarifier` to surface missing info.
2) Use `plan-lite` if the task is non-trivial.
3) Use `minimal-diff-implementer` for the smallest safe change.
4) Use `criteria-test-loop` if tests exist or can be added.
5) Use `conceptual-reviewer` before handoff.

## Workflow B: Algo or performance

1) Use `assumption-clarifier` to lock requirements.
2) Use `plan-lite` for a short path to success.
3) Use `criteria-test-loop` to build naive-correct first.
4) Optimize only after tests pass.
5) Use `conceptual-reviewer` to validate correctness and tradeoffs.

## Workflow C: Urgent bugfix

1) Use `assumption-clarifier` for a rapid repro and scope.
2) Use `minimal-diff-implementer` to keep the fix tight.
3) Use `criteria-test-loop` with a focused test.
4) Use `conceptual-reviewer` for regression risk.

## Output format

- Chosen workflow: name and reason.
- Steps executed: short bullets.
- Open questions: if any.
- Next action: what happens next.

## Guardrails

- Do not invent a new workflow unless asked.
- Do not skip `conceptual-reviewer` on medium+ changes.
- If information is missing, run `assumption-clarifier` first.
- Prefer naive-correct first, then optimize.
- Avoid extra abstraction and unrelated cleanup.
