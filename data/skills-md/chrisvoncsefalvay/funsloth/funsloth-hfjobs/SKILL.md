---
name: funsloth-hfjobs
description: Training manager for Hugging Face Jobs - launch fine-tuning on HF cloud GPUs with optional WandB monitoring
---

# Hugging Face Jobs Training Manager

Run Unsloth training on Hugging Face Jobs (cloud GPU training).

## Prerequisites

1. **HF Authentication**: `huggingface-cli whoami` (login if needed)
2. **HF Jobs Access**: Requires PRO subscription or org compute access
3. **Training notebook/script**: From `funsloth-train`

## Workflow

### 1. Select Hardware

| GPU | VRAM | Cost | Best For |
|-----|------|------|----------|
| A10G | 24GB | ~$1.50/hr | 7-14B LoRA |
| A100 40GB | 40GB | ~$4/hr | 14-34B |
| A100 80GB | 80GB | ~$6/hr | 70B |
| H100 | 80GB | ~$8/hr | Fastest |

See [references/HARDWARE_GUIDE.md](references/HARDWARE_GUIDE.md) for model-to-GPU mapping.

### 2. Convert Notebook to Script

HF Jobs requires PEP 723 script format:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git",
#     "torch>=2.0",
#     "transformers>=4.45",
#     "trl>=0.12",
#     "peft>=0.13",
#     "datasets>=2.18",
# ]
# ///
```

Use [scripts/train_sft.py](scripts/train_sft.py) as a template.

### 3. Optional: WandB Integration

Add to script:
```python
import wandb
wandb.init(project="funsloth-training")
# Add report_to="wandb" in TrainingArguments
```

Set: `export WANDB_API_KEY="your-key"`

### 4. Estimate Costs

Use the cost estimator:
```bash
python scripts/estimate_cost.py --tokens {total_tokens} --platform hfjobs
```

### 5. Launch Job

```bash
# Create job config
cat > job_config.yaml << 'EOF'
compute:
  gpu: {gpu_type}
  gpu_count: 1
script: train_hfjobs.py
outputs:
  - /outputs/*
EOF

# Submit
huggingface-cli jobs create --config job_config.yaml
```

### 6. Monitor Progress

```bash
huggingface-cli jobs status {job_id}
huggingface-cli jobs logs {job_id} --follow
```

WandB: `https://wandb.ai/{username}/funsloth-training`

### 7. Download Artifacts

```python
from huggingface_hub import snapshot_download
snapshot_download(repo_id="{username}/funsloth-job", local_dir="./outputs")
```

### 8. Handoff

Offer `funsloth-upload` for Hub upload with model card.

## Error Handling

| Error | Resolution |
|-------|------------|
| No HF Jobs access | Get PRO subscription |
| OOM | Reduce batch size or upgrade GPU |
| Job timeout | Enable checkpointing |
| Script error | Check PEP 723 dependencies |

## Bundled Resources

- [scripts/train_sft.py](scripts/train_sft.py) - PEP 723 script template
- [scripts/estimate_cost.py](scripts/estimate_cost.py) - Cost estimation
- [references/PLATFORM_COMPARISON.md](references/PLATFORM_COMPARISON.md) - HF Jobs vs alternatives
- [references/HARDWARE_GUIDE.md](references/HARDWARE_GUIDE.md) - VRAM requirements
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues
