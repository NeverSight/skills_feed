---
name: test-triage
description: "Diagnose pytest or CI failures, identify root cause, and implement the minimal fix. Use when tests fail or CI reports errors."
---

# Test Triage

## Workflow
- Run the requested test command (or `metta pytest --changed` if none is provided).
- Read failure output and identify the first actionable frame.
- Inspect relevant code paths and determine root cause.
- Implement the smallest sensible fix; avoid unrelated refactors.
- Re-run the same target only if requested and report results.
