---
name: effective-questioning
description: Use when the user asks you to gather requirements, or when the request is vague and needs clarity before acting.
version: 0.2.0
---

# Effective Questioning

Gather just enough info to confidently choose an implementation path.

## When to Use
- User asks ("ask me questions", "help me figure out what I need")
- Request is vague or ambiguous
- Multiple valid approaches exist

## When to Skip
- Request is specific and actionable
- User says "just do it"

## Method: Use AskUserQuestion

**Always use the `AskUserQuestion` tool** — not plain text questions.

- Ask 3-4 related questions per round
- Include an "Other" option so users aren't boxed in
- Use `multiSelect: true` when choices aren't mutually exclusive
- Build each round on previous answers

## Question Flow

1. **Big picture:** Goal, audience, constraints, priority tradeoffs
2. **Requirements:** Core behavior, edge cases, non-functional needs
3. **Scope:** MVP vs. full, in/out of scope, integration points
4. **Confirm:** Summarize understanding, get approval, then proceed

**Stop when** the implementation path is obvious and success criteria are clear.

## Principles
- Concrete > abstract ("what happens when X?" beats "what do you want?")
- Build on previous answers—don't repeat
- Never fake understanding; ask if unclear