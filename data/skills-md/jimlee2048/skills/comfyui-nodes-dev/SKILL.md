---
name: comfyui-nodes-dev
description: Develop ComfyUI server-side V3 custom nodes (Python) using Comfy API v0_0_2/latest, schema-based inputs/outputs, ComfyExtension entrypoints, and UI preview helpers. Use when asked to create or update ComfyUI custom_nodes, V3 nodes, or Comfy API-based nodepacks.
---

# ComfyUI V3 Custom Nodes (Server-Side)

ComfyUI baseline: v0.12.0 (Comfy API v0_0_2). Update this line when revising the skill.

## Scope

- Focus on server-side V3 nodes (Python).
- Exclude client-server extension patterns and frontend-only extensions.

## Quick Workflow

1. Choose API adapter: `comfy_api.v0_0_2` for stability or `comfy_api.latest` for newest features.
2. (Optional) Scaffold a nodepack using `comfy node scaffold`.
3. Implement a V3 node with `io.ComfyNode.define_schema()` and `execute()`.
4. Return `io.NodeOutput` (or tuple/dict) from `execute()`.
5. Register nodes via `ComfyExtension.get_node_list()` and `comfy_entrypoint()`.
6. Restart ComfyUI and validate in UI/API.

## Do / Don’t

- Do use classmethods `define_schema()` and `execute()`.
- Do return `io.NodeOutput` (or tuple/dict) from `execute()`.
- Do use `ui.Preview*` helpers for UI previews.
- Don’t store mutable instance state in nodes.
- Don’t use client-server extension patterns (out of scope for this skill).

## Reference Map

Use these references as needed (progressive disclosure):

- `references/v3-core.md`: API versions, ComfyExtension, progress reporting.
- `references/io-types.md`: IO types, widget inputs, custom types.
- `references/schema-nodeoutput.md`: Schema fields, flags, hidden inputs, NodeOutput patterns.
- `references/ui-helpers.md`: Preview and save helpers for UI outputs.
- `references/scaffold.md`: Scaffold workflow and V3 defaults.
- `references/lazy-evaluation.md`: Lazy inputs, check_lazy_status, execution blocking.
- `references/validation-and-caching.md`: validate_inputs and fingerprint_inputs patterns.
- `references/folder-paths-and-files.md`: folder_paths helpers and save/load patterns.
- `references/image-mask-performance.md`: Tensor shapes, resizing, batching, device tips.
- Official docs: [Comfy-Org/docs custom-nodes](https://github.com/Comfy-Org/docs/tree/main/custom-nodes)

## Template

- `assets/v3_extension_template.py`: Minimal V3 node + extension + entrypoint.
