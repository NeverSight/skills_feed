---
name: gpu
description: |
  GPU CLI assistant - run NVIDIA GPU workloads from your Mac. Use when users:
  - Want to run ML/AI on cloud GPUs ("train a model", "run inference", "generate images")
  - Need help creating GPU projects (ComfyUI, vLLM, training, inference)
  - Have GPU CLI errors (OOM, sync, connection, model loading issues)
  - Want to optimize GPU costs or choose the right GPU
  - Need help with gpu.jsonc configuration
  - Ask about GPU CLI commands (gpu run, gpu use, gpu status, etc.)
---

# GPU CLI

Run NVIDIA GPU workloads from your Mac. `gpu run <command>` provisions cloud GPUs, syncs code, streams output.

## Current Status

```
!gpu status 2>/dev/null || echo "No active pods"
```
Config: !`ls gpu.jsonc 2>/dev/null || echo "No config"`

## Commands

| Command | Purpose |
|---------|---------|
| `gpu run <cmd>` | Execute on remote GPU |
| `gpu use <template>` | One-click apps (ComfyUI, vLLM) |
| `gpu status` | Show pods, jobs, costs |
| `gpu logs [-f]` | View/stream job output |
| `gpu stop` | Stop pod immediately |
| `gpu events` | Stream all activity |
| `gpu inventory` | List GPUs with pricing |
| `gpu dashboard` | Interactive TUI |

## Routing

**Read the appropriate reference based on user intent:**

| User Intent | Reference File |
|-------------|----------------|
| Create project, run ML task, "I want to..." | [references/create.md](references/create.md) |
| Error, OOM, failed, stuck, debug | [references/debug.md](references/debug.md) |
| Cost, GPU selection, optimize, pricing | [references/optimize.md](references/optimize.md) |
| Config help, gpu.jsonc fields | [references/config.md](references/config.md) |
| Volumes, persistent storage, large models | [references/volumes.md](references/volumes.md) |

## Quick Config

```jsonc
{
  "$schema": "https://gpu-cli.sh/schema/v1/gpu.json",
  "project_id": "my-project",
  "gpu_types": [{ "type": "RTX 4090" }],
  "outputs": ["results/", "*.pt"]
}
```

## GPU Quick Reference

| VRAM | GPU | $/hr | Best For |
|------|-----|------|----------|
| 12GB | RTX 4070 Ti | $0.25 | Small models |
| 24GB | RTX 4090 | $0.44 | SD, FLUX, 7B LLMs |
| 48GB | RTX A6000 | $0.80 | Large training |
| 80GB | A100 PCIe | $1.79 | 70B LLMs, video |

## Sync Behavior

- **TO pod**: `.gitignore` controls (gitignored files don't sync)
- **FROM pod**: `outputs` in config controls (only matching patterns sync back)
