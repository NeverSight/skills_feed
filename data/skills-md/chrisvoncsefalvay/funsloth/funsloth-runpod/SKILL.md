---
name: funsloth-runpod
description: Training manager for RunPod GPU instances - configure pods, launch training, monitor progress, retrieve checkpoints
---

# RunPod Training Manager

Run Unsloth training on RunPod GPU instances.

## Prerequisites

1. **RunPod API Key**: `echo $RUNPOD_API_KEY` (get at runpod.io/console/user/settings)
2. **RunPod SDK**: `pip install runpod`
3. **Training notebook/script**: From `funsloth-train`

## Workflow

### 1. Select GPU

| GPU | VRAM | Cost | Best For |
|-----|------|------|----------|
| RTX 3090 | 24GB | ~$0.35/hr | Budget 7-14B |
| RTX 4090 | 24GB | ~$0.55/hr | Fast 7-14B |
| A100 40GB | 40GB | ~$1.50/hr | 14-34B |
| A100 80GB | 80GB | ~$2.00/hr | 70B |
| H100 | 80GB | ~$3.50/hr | Fastest |

RunPod typically has better prices than HF Jobs.

### 2. Choose Deployment

- **Pod** (Recommended): Persistent, SSH access, network storage
- **Serverless**: Pay per second, complex setup (better for inference)

### 3. Configure Network Volume (Recommended)

```python
import runpod
volume = runpod.create_network_volume(name="funsloth-training", size_gb=50, region="US")
```

Allows: resume training, download checkpoints, share between pods.

### 4. Launch Pod

Use the [official Unsloth Docker image](https://docs.unsloth.ai/new/how-to-fine-tune-llms-with-unsloth-and-docker) for a pre-configured environment:

```python
import runpod

pod = runpod.create_pod(
    name="funsloth-training",
    image_name="unsloth/unsloth",  # Official image, supports all GPUs incl. Blackwell
    gpu_type_id="{gpu_type}",
    volume_in_gb=50,
    network_volume_id="{volume_id}",
    env={
        "HF_TOKEN": "{token}",
        "WANDB_API_KEY": "{key}",
        "JUPYTER_PASSWORD": "unsloth",
    },
    ports="8888/http,22/tcp",
)
```

The Unsloth image includes Jupyter Lab (port 8888) and example notebooks in `/workspace/unsloth-notebooks/`.

### 5. Upload and Run

```bash
# SSH into pod
ssh root@{pod_ip}

# Upload script
scp train.py root@{pod_ip}:/workspace/

# Run training (use tmux for persistence)
tmux new -s training
cd /workspace && python train.py
# Ctrl+B, D to detach
```

### 6. Monitor

```bash
# SSH monitoring
tail -f /workspace/training.log
nvidia-smi -l 1

# Dashboard
https://runpod.io/console/pods/{pod_id}
```

### 7. Retrieve Checkpoints

```bash
# Save to network volume
cp -r /workspace/outputs /runpod-volume/

# Download via SCP
scp -r root@{pod_ip}:/workspace/outputs ./

# Or push to HF Hub from pod
```

### 8. Stop Pod

```python
runpod.stop_pod(pod_id)    # Can resume later
runpod.terminate_pod(pod_id)  # Deletes pod, keeps volume
```

### 9. Handoff

Offer `funsloth-upload` for Hub upload with model card.

## Best Practices

1. **Always use network volumes** - pod storage is ephemeral
2. **Use spot instances** for lower costs (risk of preemption)
3. **Set up SSH keys** before creating pods
4. **Stop pods when not training** - charges per minute
5. **Save checkpoints frequently** with `save_steps`

## Error Handling

| Error | Resolution |
|-------|------------|
| Pod creation failed | Try different GPU type or region |
| SSH refused | Wait 1-2 min, check IP |
| Out of disk | Increase volume or clean up |
| Volume not mounting | Check same region as pod |

## Bundled Resources

- [scripts/train_sft.py](scripts/train_sft.py) - Training script template
- [scripts/estimate_cost.py](scripts/estimate_cost.py) - Cost estimation
- [references/PLATFORM_COMPARISON.md](references/PLATFORM_COMPARISON.md) - RunPod vs alternatives
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues
