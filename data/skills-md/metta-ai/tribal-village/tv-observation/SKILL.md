---
name: tv-observation
description: "Inspect observation space and inventory encoding."
---

# TV Observation

## Workflow
- Run:
- `rg -n "ObservationName|ObservationLayers|TintLayer" src/types.nim`
- `sed -n '150,260p' src/types.nim`
- `rg -n "updateObservations|updateAgentInventoryObs" src/environment.nim`
- `sed -n '1,200p' src/environment.nim`
- Summarize observation layers and inventory handling.
