---
name: amp-review
description: Code review using amp. Triggers on "amp-review". Reviews uncommitted local changes by default.
---

# Amp Review

Run code reviews using `amp review` on uncommitted changes.

## Usage

```bash
amp review --dangerously-allow-all --stream-json
```

This reviews all uncommitted changes (staged + unstaged + untracked).

## Workflow

1. User triggers with `amp-review` optionally describing what to focus on
2. Run the review command and parse the JSON output
3. Present findings to user with actionable feedback

## Guidelines

- Always use `--dangerously-allow-all` to bypass permission prompts
- Use `--stream-json` for structured output parsing
- If user specifies a focus area, relay that context before interpreting results
- Summarize critical issues first, then minor suggestions
