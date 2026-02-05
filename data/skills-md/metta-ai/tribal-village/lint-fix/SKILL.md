---
name: lint-fix
description: "Run lint autofix (default `metta lint --fix`), address remaining lint errors, and summarize changes. Use when asked to fix lint issues."
---

# Lint Fix

## Workflow
- Confirm the lint command and any allowlist paths (default `metta lint --fix`).
- Run the lint autofix.
- Fix remaining lint failures manually, limiting changes to relevant files.
- Summarize edits and re-run lint if needed.
