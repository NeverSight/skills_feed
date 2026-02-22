---
name: tv-economy-respawn
description: "Inspect inventory, stockpile, altars, hearts, and respawn logic."
---

# TV Economy Respawn

## Workflow
- Run:
- `rg -n "altar|hearts|respawn" src/step.nim src/items.nim src/types.nim`
- `sed -n '1800,2100p' src/step.nim`
- `sed -n '1,200p' src/items.nim`
- Summarize economy and respawn flow.
