---
name: run-validation
description: "Run the standard local validation steps for tribal-village (alias: tv-validate)."
---

# Run Validation

## Workflow
- Run:
- `nim c -d:release tribal_village.nim`
- `timeout 15s nim r -d:release tribal_village.nim` (or `gtimeout` on macOS)
- `nim r --path:src tests/ai_harness.nim`
- Summarize results and failures.
