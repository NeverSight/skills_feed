---
name: create-plan
description: Create a concise plan. Use when a user explicitly asks for a plan related to a coding task.
metadata:
  short-description: Create a plan
---

# Create Plan

## Goal

Turn a user prompt into a single, actionable plan stored as a markdown file in `.cursor/plans/`, then obtain explicit approval before any buildout begins.

## Minimal workflow

1. **Scan context quickly**
   - Read `README.md` and any obvious docs (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Skim relevant files (the ones most likely touched).
   - Identify constraints (language, frameworks, CI/test commands, deployment shape).

2. **Ask follow-ups only if blocking**
   - Ask **at most 1–2 questions**.
   - Only ask if you cannot responsibly plan without the answer; prefer multiple-choice.
   - If unsure but not blocked, make a reasonable assumption and proceed.
   - Ask open questions directly to the user; do not append them to the plan file.

3. **Create a plan file in `.cursor/plans/`**
   - Ensure `.cursor/plans/` exists; create it if missing.
   - Name the file `<agent_name>__<short summary no more than 5 words snake-cased>.plan.md`.
   - The plan file must contain YAML frontmatter in the format below, followed by human-readable details (headings + short sections) that expand on the plan.
   - Include 6–10 ordered, verb-first action items.
   - Each item should be atomic and include files/commands when useful.
   - Use `pending`, `in_progress`, or `completed` for `status`.

4. **Handle the follow-up loop before building**
   - If you asked questions, stop after writing the plan file and wait for answers.
   - When answers arrive, update the plan file to reflect the new information.
   - If the user adds new requirements or changes scope, update the plan file again.
   - Always refer back to this plan during the planning loop.
   - Ask for explicit permission to begin building after each update.

5. **Output formatting**
   - Initial plan: confirm the plan file path and request permission to proceed.
   - Follow-up after answers: confirm updates, mention the plan file path, and request permission again.

## Plan template (follow exactly)

```markdown
---
name: <Short Title Case name>
overview: <1–3 sentences describing intent and approach.>
todos:
  - id: <kebab-case-id>
    content: <Verb-first action item>
    status: pending
  - id: <kebab-case-id>
    content: <Verb-first action item>
    status: pending
---

# <Readable Title>

## Overview

<Short summary of the change and why.>

## Key Files

- <List key files and why they matter.>

## Implementation Notes

<Bullets or short paragraphs that clarify approach, constraints, and data flow.>

## Testing

- <Concrete manual or automated test steps.>
```

## Checklist item guidance

Good items:
- Point to likely files/modules: `src/...`, `app/...`, `services/...`.
- Name concrete validation: `Run npm test`, `Add unit tests for X`.
- Include edge cases or risk checks when applicable.

Avoid:
- Vague steps ("handle backend", "do auth").
- Too many micro-steps.
- Writing code snippets (keep the plan implementation-agnostic).
