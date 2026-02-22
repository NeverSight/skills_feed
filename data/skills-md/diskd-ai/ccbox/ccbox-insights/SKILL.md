---
name: ccbox-insights
description: Summarize lessons learned from ccbox session logs (projects/sessions/history/skills) so the agent can do better next time. Produce copy-ready instruction updates (project + global) backed by evidence, with optional skill-span context to attribute failures to specific skills. Use when asked to run /ccbox:insights, generate a "lessons learned" memo, or propose standing instructions from session history.
---

# ccbox-insights

Use `ccbox` session logs to produce an evidence-based "lessons learned" memo for the agent (and humans), plus copy-ready instruction snippets that improve future sessions.

Tool-call failures are an important signal, but the goal is broader than errors: capture what worked, what did not, and what should become standing behavior in the future.

## Requirements

- `ccbox` on your `$PATH`.
- Access to the local sessions directory scanned by `ccbox` (see `ccbox --help` if discovery looks empty).

## Quick start (single session)

1. Find the latest session for the current folder:

```bash
ccbox sessions --limit 5 --offset 0 --size
```

2. Inspect the latest session timeline (increase `--limit` if needed):

```bash
ccbox history --full --limit 200 --offset 0
```

## Workflow (recommended)

Follow a staged pipeline: collect -> filter -> summarize -> label -> aggregate -> synthesize -> propose instructions.

### Stage 0: Choose scope

- **Session**: one `.jsonl` log for deep root-cause analysis.
- **Project**: last N sessions for one project to find recurring failure patterns.
- **Global**: a sample across projects to find cross-project patterns.

### Stage 1: Collect evidence with `ccbox`

- Project discovery: `ccbox projects`
- Session listing: `ccbox sessions [project-path] --limit N --offset 0 --size`
- Timeline capture: `ccbox history [log-or-project] --full --limit N --offset 0`
- Skill spans (optional): `ccbox skills [log-or-project] --json`

When triaging quickly, scan the timeline for failure signals (examples): `error`, `failed`, `non-zero`, `rejected`, `permission`, `timeout`.

### Stage 1.5: Identify clarifications, corrections, and interruptions

Treat user clarifications/corrections as high-signal evidence of workflow breakdowns. Your goal is to pinpoint where the agent went off-track and what rule would prevent it next time.

Look for user messages that:

- Clarify intent ("I meant X", "not that", "use Y instead").
- Correct mistakes ("this is wrong", "stop", "revert", "you didn't follow the instructions").
- Restate constraints after the fact ("do not run X", "no emojis", "do not use cargo", "do not change version", "do not release automatically").
- Interrupt the session due to friction (hangs, repeated retries, "cancel", abandoning the thread).

For each such moment, capture a small "course-correction record":

- Trigger: what the agent did immediately before (tool call, plan, edit, or assumption).
- Correction: the exact user sentence(s) that clarified/corrected.
- Fix: what changed after the correction (new approach, different tool, narrower scope).
- Lesson: one rule that would have prevented the detour (copy-ready, scoped project/global).

If the session ends without a clear resolution (or the user abandons it), mark the outcome accordingly and explain the likely interruption reason using evidence (for example: hang/timeout, repeated invalid tool use, conflicting constraints).

### Stage 2: Summarize long timelines (only if needed)

If the timeline is too large to analyze in one pass, summarize in chunks:

- Focus on: user request, tool calls, tool outputs/errors, and outcome.
- Preserve: tool names, command lines, error messages, and user feedback.
- Keep each chunk summary to 3-5 sentences.

### Stage 3: Extract per-session tool-call facets

For each session in scope, produce one JSON object matching `references/facets.md`.

If skill spans are available (via `ccbox skills --json`), annotate each failure with the active skill context when possible (e.g., "this failure happened inside the commit skill span").

Hard rules:

- Use only evidence from the session log; do not guess missing details.
- Separate "tool failed" from "wrong approach" (a tool can succeed but still be the wrong move).
- Count explicit user rejections as their own category (the tool did not fail; the action was declined).

### Stage 4: Aggregate and analyze

Aggregate the facet set to produce:

- Top failing tools and failure categories.
- Three root-cause themes with concrete evidence snippets.
- Repeated user constraints that should become standing instructions.
- Engine-neutral recommendations that reduce tool-call failures and improve UX.

Use `references/report.md` as the output template.

### Stage 5: Propose instruction updates (project + global)

Produce two additive sets of copy-ready snippets:

- **Project-level**: bullets to add to `AGENTS.md`.
- **Global**: bullets for the user's global agent instructions.

Guidelines:

- Do not include local paths, repository names, or one-off incident details.
- Prefer rules that prevent repeated errors (2+ occurrences) over one-time fixes.
- Each instruction should include: what to do, what to avoid, and why (1 sentence).

### Stage 6: Deliverables

Deliver:

- A concise lessons learned memo (Markdown), following `references/report.md`.
- Proposed additive `AGENTS.md` snippet (project-level).
- Proposed additive global instruction snippet.

Optional (for future memory systems):
- "AutoMemorial candidates": a short, structured list of rules that should become standing agent memory, each backed by evidence and scoped (project vs global).

## References

- Facet schema + taxonomy: `references/facets.md`
- Report template + instruction templates: `references/report.md`
