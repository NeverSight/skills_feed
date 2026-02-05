---
name: comfy-analyze
description: Use when understanding a ComfyUI workflow, analyzing what a workflow does, tracing node connections, finding upstream/downstream nodes, or reading workflow JSON.
version: 1.0.0
---

# ComfyUI Workflow Analysis

Understand workflow structure and node connections.

## MCP Tools

| Tool | When to use |
|------|-------------|
| `comfy_read` | First step - get human-readable summary of any workflow |
| `comfy_trace` | See a specific node's inputs and outputs with slot names |
| `comfy_upstream` | Find all nodes feeding INTO a target node |
| `comfy_downstream` | Find all nodes FED BY a source node |

## Workflow

1. **Summarize**: `comfy_read(workflow)` → pattern, key params, flow
2. **Deep dive**: `comfy_trace(workflow, node_id)` → specific connections
3. **Follow data**: `comfy_upstream`/`comfy_downstream` → trace the graph

## What comfy_read Returns

```
## Pattern: Flux txt2img +LoRA

## Key Parameters
  model: flux-dev.safetensors
  steps: 20
  cfg: 3.5

## Variables (3)
  $model <- Node 1 (CheckpointLoader)

## Flow
  [image] 1 -> 5 -> 12 -> 15
```

## What comfy_trace Returns

```
[Node 577] WanVideoSampler

  INPUTS:
    [0] model <- Node 608 (GetNode, slot 0)
    [1] image_embeds <- Node 1179 (WanVideoVACEEncode, slot 0)

  OUTPUTS:
    [0] samples -> Node 595 (WanVideoDecode, slot 1)
```

## CLI Equivalents

If MCP isn't available, use CLI commands:

| MCP Tool | CLI Command |
|----------|-------------|
| `comfy_read` | `python we_vibin.py analyze workflow.json` |
| `comfy_trace` | `python we_vibin.py trace workflow.json NODE` |
| `comfy_upstream` | `python we_vibin.py upstream workflow.json NODE` |
| `comfy_downstream` | `python we_vibin.py downstream workflow.json NODE` |

## Setup

Requires MCP server. See [MCP_SETUP.md](../comfy-edit/MCP_SETUP.md).
