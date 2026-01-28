---
name: obsidian-canvas
description: Create, edit, and manipulate Obsidian Canvas (.canvas) files. Use this skill when the user wants to visualize concepts, build flowcharts, or organize information spatially using the JSON Canvas format.
---

# Obsidian Canvas

This skill handles the creation and manipulation of `.canvas` files (JSON Canvas).

## Core Workflow

1.  **Library**: Utilization of the provided `scripts/canvas_lib.py` is **MANDATORY**. Do not write raw JSON.
2.  **Execution**: Construct a JSON payload and pipe it to the library script via stdin (CLI mode). Do not create temporary Python scripts.
3.  **Layout**: Focus on logical coordinates (x,y). The library handles ID generation, node height, and edge routing automatically.

## Resources

- **Library**: `scripts/canvas_lib.py` (Core logic for nodes, groups, and smart edges).
- **CLI Spec**: [references/library_spec.md](references/library_spec.md) - **Read strictly for JSON format**.
- **Specification**: See [references/spec.md](references/spec.md) for the detailed JSON schema.
- **Example**: See [assets/flowchart.canvas](assets/flowchart.canvas).

## Layout & Aesthetics (Senior Designer Standards)
- **Whitespace**: Use generous vertical gaps (120px-180px) between related nodes to provide "shelf space" for edge labels.
- **Z-Indexing**: The library handles z-indexing (groups render behind nodes). Always use groups to bound track-specific content.
- **Hierarchy**: Use H1 (#) for canvas titles, H2 (##) for major sections, and H3 (###) for individual node titles.
- **Colors**: 
	- `1` (Red): Friction, Error, Filing.
	- `2` (Orange): Interaction, Support, Outreach.
	- `3` (Yellow): Evidence, Documentation, Data.
	- `4` (Green): Success, Resolution, Start.
	- `5` (Blue/Cyan): Neutral, Operations.
	- `6` (Purple): Titles, Meta-info, Outcome.
- **Edges**: Keep labels short. If multiple edges cross the same path, the library tries to route them, but manual `x` adjustments help.

## Output
To create a new canvas, construct a JSON payload and pipe it to the library script:

```bash
cat <<EOF | python3 /path/to/skills/obsidian-canvas/scripts/canvas_lib.py
{
  "output": "Project_Flow.canvas",
  "nodes": [
    {"node_id": "start", "text": "Start", "x": 0, "y": 0, "color": "6"},
    {"node_id": "end", "text": "End", "x": 0, "y": 200, "color": "1"}
  ],
  "edges": [
    {"from_node": "start", "to_node": "end"}
  ],
  "groups": [
    {"label": "Phase 1", "nodes_in_group": ["start", "end"], "color": "5"}
  ]
}
EOF
```
