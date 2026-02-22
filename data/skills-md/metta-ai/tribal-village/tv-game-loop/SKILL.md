---
name: tv-game-loop
description: "Open the main step loop and action handlers."
---

# TV Game Loop

## Workflow
- Run:
- `sed -n '1,220p' src/step.nim`
- `rg -n "case verb|attackAction|useAction|buildAction" src/step.nim`
- `sed -n '220,900p' src/step.nim`
- Summarize the step loop and action cases.
