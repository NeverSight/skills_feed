---
name: cleanup-refactor
description: "Simplify code and remove legacy/backcompat shims while preserving behavior. Use when asked to clean up or simplify code."
---

# Cleanup Refactor

## Workflow
- Identify legacy shims, redundant helpers, or dead code in the target paths.
- Simplify or remove while keeping behavior stable and the diff minimal.
- Avoid unrelated refactors; focus on the requested cleanup.
- Summarize what was removed and why it is safe.
