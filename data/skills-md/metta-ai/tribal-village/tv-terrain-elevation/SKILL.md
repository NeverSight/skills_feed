---
name: tv-terrain-elevation
description: "Investigate cliffs, ramps, and elevation traversal."
---

# TV Terrain Elevation

## Workflow
- Run:
- `rg -n "applyBiomeElevation|applyCliffRamps|applyCliffs" src/spawn.nim`
- `sed -n '120,260p' src/spawn.nim`
- `rg -n "canTraverseElevation" src/environment.nim`
- `sed -n '400,460p' src/environment.nim`
- `rg -n "RampUp|RampDown|Cliff" src/terrain.nim src/types.nim src/registry.nim`
- Explain how elevation traversal is handled.
