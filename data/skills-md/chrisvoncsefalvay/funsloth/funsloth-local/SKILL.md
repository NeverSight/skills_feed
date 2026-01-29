---
name: funsloth-local
description: Training manager for local GPU training - validate CUDA, manage GPU selection, monitor progress, handle checkpoints
---

# Local GPU Training Manager

Run Unsloth training on your local GPU.

## Prerequisites Check

### 1. Verify CUDA

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

If CUDA not available:
- Check NVIDIA drivers: `nvidia-smi`
- Check CUDA: `nvcc --version`
- Reinstall PyTorch: `pip install torch --index-url https://download.pytorch.org/whl/cu121`

### 2. Check VRAM

See [references/HARDWARE_GUIDE.md](references/HARDWARE_GUIDE.md) for requirements:

| VRAM | Recommended Setup |
|------|-------------------|
| 8GB | 7B, 4-bit, batch=1, LoRA r=8 |
| 12GB | 7B, 4-bit, batch=2, LoRA r=16 |
| 16GB | 7-13B, 4-bit, batch=2, LoRA r=16-32 |
| 24GB | 7-14B, 4-bit, batch=4, LoRA r=32 |

### 3. Check Dependencies

```bash
pip install unsloth torch transformers trl peft datasets accelerate bitsandbytes
```

## Docker Option

Use the [official Unsloth Docker image](https://docs.unsloth.ai/new/how-to-fine-tune-llms-with-unsloth-and-docker) for a pre-configured environment (supports all GPUs including Blackwell/50-series):

```bash
docker run -d \
  -e JUPYTER_PASSWORD="unsloth" \
  -p 8888:8888 \
  -v $(pwd)/work:/workspace/work \
  --gpus all \
  unsloth/unsloth
```

Access Jupyter at `http://localhost:8888`. Example notebooks are in `/workspace/unsloth-notebooks/`.

Environment variables:

- `JUPYTER_PASSWORD` - Jupyter auth (default: `unsloth`)
- `JUPYTER_PORT` - Port (default: `8888`)
- `USER_PASSWORD` - User/sudo password (default: `unsloth`)

## Run Training

### Option 1: Notebook

```bash
jupyter notebook notebooks/sft_template.ipynb
```

### Option 2: Script

```bash
# Edit configuration in script, then run
python scripts/train_sft.py
```

### GPU Selection (Multi-GPU)

```python
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Use first GPU
```

## Monitor Training

### Terminal

```bash
# Watch GPU usage
watch -n 1 nvidia-smi

# Or use nvitop (more detailed)
pip install nvitop && nvitop
```

### WandB (Optional)

```bash
export WANDB_API_KEY="your-key"
# Add report_to="wandb" in TrainingArguments
```

## Troubleshooting

### OOM Error

Try in order:
1. Reduce batch_size (to 1)
2. Increase gradient_accumulation
3. Reduce max_seq_length
4. Reduce LoRA rank
5. `torch.cuda.empty_cache()`

### Loss Not Decreasing

1. Check learning rate (try higher or lower)
2. Verify chat template matches model
3. Inspect data format

### Training Too Slow

1. Enable bf16 if supported
2. Use `packing=True` for short sequences
3. Reduce logging_steps

See [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for more solutions.

## Resume from Checkpoint

```python
TrainingArguments(
    resume_from_checkpoint=True,  # Auto-find latest
    # Or: resume_from_checkpoint="outputs/checkpoint-500"
)
```

## Save Model

Training script automatically saves:
- `outputs/lora_adapter/` - LoRA weights
- `outputs/merged_16bit/` - Merged model (optional)

## Test Inference

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained("outputs/lora_adapter")
FastLanguageModel.for_inference(model)

messages = [{"role": "user", "content": "Hello!"}]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
outputs = model.generate(inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0]))
```

## Handoff

Offer `funsloth-upload` for Hub upload with model card.

## Tips

1. **Close other GPU apps** before training
2. **Monitor temps** - keep under 85C
3. **Use UPS** for long runs
4. **Save frequently** with `save_steps`

## Bundled Resources

- [notebooks/sft_template.ipynb](notebooks/sft_template.ipynb) - Notebook template
- [scripts/train_sft.py](scripts/train_sft.py) - Script template
- [references/HARDWARE_GUIDE.md](references/HARDWARE_GUIDE.md) - VRAM requirements
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common issues
