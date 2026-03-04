---
name: summarize-current-session
description: Summarize the current conversation session and write the summary to docs/sessions/ in the project root. Use when the user asks to "summarize this session", "write a session log", "save what we did today", or similar.
---

# summarize-current-session

Summarize everything done in the current conversation session and persist it as
a Markdown file under `<project-root>/docs/sessions/`. Create the directory if
it does not exist.

## Workflow

1. Review the full conversation to identify all changes made, problems solved,
   and decisions taken.
2. Run `date +%Y-%m-%d` in a terminal to get today's date.
3. Run `git log --oneline` (or `git log --oneline <range>`) to collect commits
   made during the session.
4. Derive a short English session title from the session content.
5. Write the file to `docs/sessions/YYYY-MM-DD-<session-title>.md`.

## File naming

```
YYYY-MM-DD-<session-title>.md
```

- Date: obtained from `date +%Y-%m-%d` — never guess or hardcode it.
- `<session-title>`: a short English phrase summarising the session, words
  joined with `-` (e.g. `add-liveness-probe-action-threshold`).

## File structure

### H1 — Session title

One sentence describing what the session accomplished.

### H2 — Summary

One paragraph covering: background / motivation, the problem or request,
the approach taken, and the outcome.

### H2 — Changed files

A list of every file touched during the session. For each file include:

- The file path (as a relative path from the project root)
- A one-line description of what changed and why

### H2 — Git commits

List every commit made during the session in the format:

```
- `a1b2c3d` <commit message>
```

Use the short hash (`git log --oneline`). If no commits were made during the
session, write: "No commits were made in this session."

### H2 — Notes

Distil the most reusable or noteworthy insights from the session, such as:

- Reusable patterns or best practices discovered
- Mistakes made and how to avoid them in future
- Non-obvious design decisions and their rationale
- Anything a future agent or developer should know before touching the same code

## Style rules

- Write in **English** throughout.
- Keep each section concise — prefer bullet lists over prose.
- The "Notes" section is the most valuable part; do not leave it empty.
- Never hardcode dates; always retrieve them with `date +%Y-%m-%d`.
