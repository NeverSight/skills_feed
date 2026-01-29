---
name: evals
description: Run and create evals for testing agent behavior. Use when the user wants to create or run an eval.
---

# Eval Skill

Run and create evals for testing agent behavior.

## Discovering Evals

Evals are markdown files matching `*.eval.md`. Use glob to find them:

```
**/*.eval.md
```

A common pattern is to collect evals in an `evals/` directory.

## Eval Structure

An eval file contains a prompt and an expectation:

```markdown
# Eval Title

<prompt>
Instructions for the agent to execute.
</prompt>

<expectation>
Success criteria - describe what must be true for the eval to pass.
</expectation>
```

## Running an Eval

1. Read the eval file
2. Extract the `<prompt>` content
3. Spawn a subagent with the prompt (runs in current working directory with shared state)
4. The subagent evaluates its own result against the `<expectation>` using LLM judgment
5. Subagent outputs `SUCCESS` or `FAIL` with reasoning

When running multiple evals, spawn all subagents in parallel. Report aggregate results at the end.

**Always end output with exactly one of these lines for CI parsing:**
- `eval result: pass` — all evals passed
- `eval result: fail` — one or more evals failed

### Subagent Instructions

**IMPORTANT:** The subagent must only test and observe. It must NOT attempt to fix, modify, or change anything to make the expectation pass. The subagent executes the prompt, observes the outcome, and reports whether the expectation was met. If the expectation fails, report `FAIL` — do not try to make it pass.

### Commands

Run a single eval:
```
/eval run <path-to-eval.eval.md>
```

Run all evals:
```
/eval run-all
```

## Creating an Eval

Gather from the user:
1. **Context** - The process or flow to evaluate
2. **Expectation** - Success criteria in natural language

```
/eval create <name>
```

Write the eval to `<name>.eval.md` in the current directory.

### Isolation

When creating an eval, try to make it self-contained and reproducible. This isn't critical, but helps:

- **Try to avoid hardcoded paths** — prefer relative paths or have the prompt create its own working directory rather than encoding specific temp directories or absolute paths.
- **Try to avoid external state** — if the process relied on existing files or services, consider whether the eval should create that state itself.
- **Parameterize where possible** — replace specific values (ports, filenames, IDs) with generic ones the eval can generate.

If you see an opportunity to improve isolation but need clarification, ask the user.
