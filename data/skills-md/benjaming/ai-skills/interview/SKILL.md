---
name: interview
description: Interview user to clarify any topic - exploring codebase, investigating issues, planning features, understanding requirements, or drilling into plans. Socratic questioning to uncover details.
argument-hint: "[topic or file]"
model: claude-opus-4-6
disable-model-invocation: true
---

Topic: $0

If topic is a file path, read it first. Otherwise, use topic as context.

Interview the user using AskUserQuestion. Adapt questions to topic type:

**Codebase exploration:** Architecture decisions, patterns used, why certain approaches
**Issue investigation:** Symptoms, reproduction steps, what changed, when started
**New feature:** Requirements, constraints, affected systems, acceptance criteria
**Plan/spec review:** Implementation details, UI/UX, tradeoffs, edge cases, dependencies

Guidelines:
- Ask non-obvious questions only
- One question at a time
- Go deep on answers before moving on
- Challenge assumptions
- Uncover hidden complexity

After each answer, either:
1. Ask follow-up or new question
2. If topic exhausted, summarize findings and ask what to do with them (write spec, create tasks, document, etc.)

Continue until user says "done" or all meaningful questions exhausted.
