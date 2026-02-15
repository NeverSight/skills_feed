---
name: comfy-edit
description: Use when editing ComfyUI workflow JSON, adding nodes, wiring connections, modifying workflows, adding ControlNet/LoRA/upscaling to a workflow, or submitting workflows to ComfyUI.
version: 1.0.0
---

# ComfyUI Workflow Editing

Edit workflow JSON files using the VibeComfy CLI.

**Repo**: https://github.com/peteromallet/VibeComfy

When working in the repo, see CLAUDE.md for full command reference.

## CLI Commands

All edit commands require `-o output.json`. Use `--dry-run` to preview changes.

| Command | Purpose |
|---------|---------|
| `trace WF NODE` | Show node inputs/outputs with slot names |
| `upstream WF NODE` | Find nodes feeding into target |
| `downstream WF NODE` | Find nodes fed by source |
| `wire WF SRC_ID SRC_SLOT DST_ID DST_SLOT -o OUT` | Connect nodes |
| `copy WF NODE -o OUT` | Duplicate a node |
| `set WF NODE key=val -o OUT` | Set widget values |
| `delete WF NODE -o OUT` | Remove nodes |
| `create WF TYPE -o OUT` | Create new node |
| `batch WF SCRIPT -o OUT` | Multi-step edits |
| `submit WF` | Run workflow in ComfyUI |

**Tip**: Use `trace` first to find slot numbers, then `wire` to connect.

## Adding Nodes Workflow

1. **Find the node**: `comfy_search("controlnet")` (use comfy-registry skill)
2. **Get the spec**: `comfy_spec("ControlNetLoader")` - see inputs/outputs
3. **Understand the flow**: `python we_vibin.py trace workflow.json <ksampler_id>`
4. **Create and wire**:
```bash
python we_vibin.py create workflow.json ControlNetLoader -o step1.json
python we_vibin.py trace step1.json <new_node_id>  # Find the slot numbers
python we_vibin.py wire step1.json <src_id> <src_slot> <dst_id> <dst_slot> -o step2.json
```

Or use batch scripts for multi-step edits (slot names work in batch mode):
```bash
create ControlNetLoader as $cn
wire $cn:control_net -> 15:control_net
```

## Common Patterns

What nodes go together. See [references/PATTERNS.md](references/PATTERNS.md) for details.

### Image Generation

| Pattern | Flow |
|---------|------|
| txt2img | Checkpoint → CLIP (x2) → EmptyLatent → KSampler → VAEDecode → Save |
| img2img | LoadImage → VAEEncode → KSampler (denoise<1) → VAEDecode → Save |
| inpaint | LoadImage + Mask → VAEEncodeForInpaint → KSampler → VAEDecode |

### Enhancements

| Pattern | Flow |
|---------|------|
| ControlNet | LoadControlNet → ControlNetApply → KSampler |
| LoRA | Checkpoint → LoraLoader → KSampler |
| Upscale | LoadUpscaleModel → ImageUpscaleWithModel → Save |
| IPAdapter | LoadIPAdapter → IPAdapterApply → KSampler |

### Video

| Pattern | Flow |
|---------|------|
| AnimateDiff | Checkpoint → ADE_LoadAnimateDiff → ADE_Apply → KSampler → VHS_Combine |
| Wan t2v | WanModelLoader → WanTextEncode → WanSampler → WanDecode |
| LTX | LTXVLoader → LTXVTextEncode → LTXVSampler → LTXVDecode |
| v2v | VHS_LoadVideo → VAEEncode → KSampler → VAEDecode → VHS_Combine |

### Flux

| Pattern | Flow |
|---------|------|
| Flux txt2img | UNETLoader + DualCLIPLoader + VAELoader → FluxGuidance → KSampler |

## Batch Scripts

For multi-step edits, use batch scripts:

```bash
# Copy node, assign to variable
copy 1183 as $selector

# Set widgets
set $selector indexes="0:81"

# Wire using slot names
wire 1140:IMAGE -> $selector:image

# Delete nodes
delete 1220 1228
```

Run with: `python we_vibin.py batch workflow.json script.txt -o out.json --dry-run`
