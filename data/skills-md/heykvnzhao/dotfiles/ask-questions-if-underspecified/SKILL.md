---
name: ask-questions-if-underspecified
description: Clarify requirements before implementing by asking the minimum must-have questions. Use when a request is underspecified or ambiguous, when the user asks to “ask clarifying questions”, or when multiple plausible interpretations exist and you risk doing the wrong work.
---

# Ask Questions If Underspecified

## Goal

Ask the minimum set of clarifying questions needed to avoid wrong work. Do not start implementing until the must-have questions are answered (or the user explicitly approves proceeding with stated assumptions).

## Workflow

### 1) Decide whether the request is underspecified

Treat a request as underspecified if one or more are unclear:
- Objective (what should change vs. stay the same)
- “Done” (acceptance criteria, examples, edge cases)
- Scope (which files/components/users are in/out)
- Constraints (compatibility, performance, style, deps, time)
- Environment (runtime versions, OS, build/test runner)
- Safety/reversibility (migration/rollback risk)

If there are multiple plausible interpretations, assume it is underspecified.

### 2) Ask must-have questions first (keep it small)

Ask 1–5 questions in the first pass. Prefer questions that eliminate whole branches of work.

Make them easy to answer:
- Use numbered questions with short options (yes/no or a/b/c)
- Recommend defaults when reasonable
- Provide a fast-path response (e.g., “reply `defaults`”)
- Separate “Need to know” vs “Nice to know” when helpful

### 3) Pause before acting

Until must-have answers arrive:
- Do not run commands, edit files, or produce a detailed plan that depends on unknowns
- Do allow low-risk discovery reads (repo structure/configs) if they do not commit to a direction

If the user explicitly wants you to proceed without answers:
1. State assumptions as a short numbered list
2. Ask for confirmation
3. Proceed only after confirm/correct

### 4) Confirm interpretation, then proceed

Once answered, restate requirements in 1–3 sentences (including key constraints and what success looks like), then start work.

## Templates

- “Before I start, I need: (1) … (2) … (3) …. If you don’t care about (2), I’ll assume ….”
- “Which should it be? A) … B) … C) … (pick one)”
- “What would you consider ‘done’? For example: …”
- “Any constraints (versions, perf, style, deps)? If none, I’ll target existing project defaults.”

Example (compact decision format):

```text
1) Scope?
a) Minimal change (default)
b) Refactor while touching the area
c) Not sure - use default

2) Compatibility target?
a) Current project defaults (default)
b) Also support older versions: <specify>
c) Not sure - use default

Reply with: defaults (or 1a 2a)
```

## Anti-patterns

- Don’t ask questions you can answer via quick, low-risk discovery (configs/docs/grep).
- Don’t ask open-ended questions when a tight multiple-choice would resolve ambiguity faster.
