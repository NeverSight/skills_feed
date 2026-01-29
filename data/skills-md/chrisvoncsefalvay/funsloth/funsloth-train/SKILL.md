---
name: funsloth-train
description: Generate Unsloth training notebooks and scripts. Use when the user wants to create a training notebook, configure fine-tuning parameters, or set up SFT/DPO/GRPO training.
---

# Unsloth Training Notebook Generator

Generate training notebooks for fine-tuning with Unsloth.

## Quick Start

Copy and customize the template notebook:
```
notebooks/sft_template.ipynb
```

Or use a training script directly:
```bash
python scripts/train_sft.py  # Supervised fine-tuning
python scripts/train_dpo.py  # Direct preference optimization
python scripts/train_grpo.py # Group relative policy optimization
```

## Configuration Modes

Ask the user which mode they prefer:

1. **Sensible defaults** - Production-ready notebook with recommended settings
2. **Guide me** - Walk through each option with explanations
3. **Leave it empty** - Notebook with ipywidgets for runtime configuration

## Mode 1: Sensible Defaults

Use these production-ready defaults:

| Parameter | Default | Reasoning |
|-----------|---------|-----------|
| Model | `unsloth/llama-3.1-8b-unsloth-bnb-4bit` | Good balance |
| Max seq length | 2048 | Covers most use cases |
| Load in 4-bit | True | 70% VRAM reduction |
| LoRA rank | 16 | Good trade-off |
| Batch size | 2 | Works on 8GB+ VRAM |
| Gradient accumulation | 4 | Effective batch of 8 |
| Learning rate | 2e-4 | Unsloth recommended |
| Epochs | 1 | Often sufficient |

## Mode 2: Guide Me

Ask questions in order. See [MODEL_SELECTION.md](references/MODEL_SELECTION.md) for model options and [TRAINING_METHODS.md](references/TRAINING_METHODS.md) for technique details.

### Key Questions

1. **Model family**: Llama, Qwen, Gemma, Phi, Mistral, DeepSeek?
2. **Model size**: Based on VRAM (see [HARDWARE_GUIDE.md](references/HARDWARE_GUIDE.md))
3. **Training technique**: SFT, DPO, GRPO, ORPO, KTO?
4. **Quantization**: 4-bit (recommended), 8-bit, 16-bit?
5. **LoRA rank**: 8, 16, 32, 64?
6. **Sequence length**: 512, 1024, 2048, 4096?
7. **Batch size**: 1, 2, 4, 8?
8. **Learning rate**: 1e-5, 5e-5, 2e-4, 5e-4?
9. **Training duration**: 1 epoch, 3 epochs, or specific steps?

## Mode 3: ipywidgets

Generate a notebook with interactive configuration widgets. Users select options at runtime.

## Notebook Structure

Generate notebooks with these sections:

1. **Title and Overview** - What the notebook does
2. **Installation** - Install Unsloth
3. **Imports and GPU Check** - Verify environment
4. **Configuration** - All tunable parameters
5. **Load Model** - FastLanguageModel.from_pretrained()
6. **Apply LoRA** - FastLanguageModel.get_peft_model()
7. **Load Dataset** - Format-appropriate loading
8. **Training** - SFTTrainer/DPOTrainer/GRPOTrainer
9. **Save Model** - LoRA adapter + merged model
10. **Test Inference** - Quick verification

## After Generation

Ask where to run training:
1. **Hugging Face Jobs** - Cloud GPUs (`funsloth-hfjobs`)
2. **RunPod** - Flexible GPU rentals (`funsloth-runpod`)
3. **Local** - Your own GPU (`funsloth-local`)

## Context to Pass

```yaml
notebook_path: "./training_notebook.ipynb"
model_name: "unsloth/llama-3.1-8b-unsloth-bnb-4bit"
dataset_name: "mlabonne/FineTome-100k"
technique: "SFT"
lora_rank: 16
max_seq_length: 2048
batch_size: 2
learning_rate: 2e-4
num_epochs: 1
```

## Bundled Resources

- [notebooks/sft_template.ipynb](notebooks/sft_template.ipynb) - Ready-to-use SFT template
- [scripts/train_sft.py](scripts/train_sft.py) - SFT script template
- [scripts/train_dpo.py](scripts/train_dpo.py) - DPO script template
- [scripts/train_grpo.py](scripts/train_grpo.py) - GRPO script template
- [references/MODEL_SELECTION.md](references/MODEL_SELECTION.md) - Model recommendations
- [references/HARDWARE_GUIDE.md](references/HARDWARE_GUIDE.md) - VRAM requirements
- [references/TRAINING_METHODS.md](references/TRAINING_METHODS.md) - SFT vs DPO vs GRPO
