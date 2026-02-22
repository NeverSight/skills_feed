---
name: tv-tint-freeze
description: "Investigate tint layers and frozen tiles."
---

# TV Tint Freeze

## Workflow
- Run:
- `rg -n "Tint|tint|Clippy|frozen" src/tint.nim src/colors.nim src/step.nim src/renderer.nim`
- `sed -n '1,200p' src/tint.nim`
- `sed -n '1,160p' src/colors.nim`
- `rg -n "TintLayer" src/environment.nim`
- Summarize tint and freeze mechanics.
