---
name: ask
description: "Structured clarification and requirements gathering through focused dialogue. Use when a task is ambiguous, underspecified, or requires user input before any action can be taken. Do not plan or implement anything—only ask questions to collect the information needed. Triggers on: 'ask me', 'ask questions about', 'clarify requirements', 'gather requirements', 'I need you to ask', or when the user explicitly wants a question-and-answer session before work begins."
---

# Ask

## Purpose

Gather the information needed to proceed with a task through structured, focused dialogue.

This skill is for **asking only**. Do not plan, implement, or produce any artifacts.

## Scope Gate (Required Before Starting)

Use this skill only when:

1. **The task is underspecified** — key requirements, constraints, or decisions are missing
2. **User input is required** — the task cannot proceed without answers from the user
3. **No assumptions are safe** — guessing would risk wasted effort or wrong direction

If the task is clear enough to act on, use `brainstorm`, `write-plan`, or `quick-implement` instead.

## Workflow

### Step 1: Gather Project Context

Before asking questions, read available project documentation to avoid asking things already answered:

- `docs/project-pdr.md`
- `docs/architecture.md`
- `docs/codebase.md`
- `docs/code-standard.md`

Only gather what is relevant to the current task. Skip if no docs exist.

### Step 2: Identify Information Gaps

Determine exactly what is missing before a task can proceed:

- Objective and user value
- Scope boundaries and non-goals
- Constraints (technical, UX, performance, timeline)
- Success criteria
- Key decisions with multiple valid options

### Step 3: Ask Questions (One at a Time)

Ask targeted questions sequentially to close each gap.

Rules:

- Ask **exactly one question per message**
- Prefer **multiple-choice options** when practical (2–4 choices)
- Use open-ended questions only when no reasonable options exist
- Do not ask questions already answered by project documentation
- Do not ask about implementation details prematurely
- Do not bundle multiple questions into one message

### Step 4: Confirm and Hand Off

Once all gaps are closed:

1. Summarize the collected answers concisely
2. Confirm with the user that the summary is correct
3. Recommend the appropriate next skill based on complexity:
   - Simple, clear task → `quick-implement`
   - Complex or risky task → `write-plan`
   - Ambiguous, high-risk, or exploratory → `brainstorm`

## Rules

- Do not write code or modify any files
- Do not produce plans, designs, or implementation artifacts
- Do not make assumptions; ask instead
- Keep questions short and focused
- Apply YAGNI: only ask what is strictly necessary to proceed

## Integration

- Feeds into: `brainstorm`, `write-plan`, `quick-implement`
- Use `brainstorm` when exploration and design framing are needed after gathering requirements
- Use `write-plan` when requirements are clear and a structured plan is needed
- Use `quick-implement` when the task is small and well-defined after gathering requirements
