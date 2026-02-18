---
name: agent-observability
description: Self-report agent issues by logging user corrections for later review, then resume with the correct skill. Use when a user says "don’t do that", "stop doing X", "always do Y", or requests self-correction.
---

# Agent Observability (Self-Reporting Log)

## Operating rules
- Treat user corrections as issues to log.
- Log locally in the current repo at `docs/observed-coding-agent-issues.md`.
- Create the report file if it doesn’t exist.
- **Mandatory routing checklist (do not skip):** (1) log the correction, (2) read the relevant skill file, (3) respond to the main task. This skill never handles the main task directly.
- After logging, **always** open the relevant skill file before continuing, even for small/obvious tasks.
- If the user request includes a concrete edit/implementation (README/docs/config/code), open `skills/coding/SKILL.md` **before** any questions, reads, or edits.
- If the user asks for a plan/spec, open `skills/planning/SKILL.md` **before** drafting the plan.
- If the user asks to create/update a skill or references `skills/`/`SKILL.md`, open `skills/skill-creator/SKILL.md` **before** continuing.
- On multi-turn requests, re-evaluate routing at the start of each turn; logging does not replace skill invocation.
- When opening references, use full repo paths like `skills/agent-observability/references/...` (not `references/...`).
- When a reference trigger clearly matches, open the referenced file before drafting output.
- If the user provides a word/length limit, keep the log entry short and minimize extra reads.
- Rate limit: at most one log entry per session unless the user explicitly asks to log more.
- Batch multiple corrections into a single entry by updating the existing root cause and guardrail notes; do not add verbatim quotes.

## Detect → Record → Resume

### 1) Detect correction
Trigger on phrases like or similar to:
- “don’t do that”, “stop doing X”, “always do Y”, “never do Z”
Friction alone is not sufficient; require a correction or explicit request.

### 2) Record issue (append)
Append a short entry to `docs/observed-coding-agent-issues.md`.
If a log has already been written this session, batch new corrections under the same entry unless the user explicitly asks for another log.

Entry format:
- Date/Time:
- Task/Context:
- What went wrong (root cause):
- Proposed guardrail:

### 3) Resume main task
Re-evaluate which skill applies next (coding/skill-creator/planning) and **open that SKILL.md before responding**. Do not continue the task until the relevant skill is loaded.

## Routing shortcuts (read immediately)
- README/docs/config/code edits → read `skills/coding/SKILL.md`
- Plan/spec request → read `skills/planning/SKILL.md`
- Skill creation/update or `skills/`/`SKILL.md` mention → read `skills/skill-creator/SKILL.md`
- If correction + task appear in the same prompt, **still** read the task skill before any tool calls.

## If unable to write
- Output a “Self-report draft” block in the response with the entry content.
- State that it was not written and needs manual application.

## Reference triggers (open when clearly relevant)
- Policy change / PR summary requested -> `skills/agent-observability/references/pr-template.md`

## References
- `skills/agent-observability/references/pr-template.md` - PR summary template for policy changes
