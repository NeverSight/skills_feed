---
name: funsloth-upload
description: Generate comprehensive model cards and upload fine-tuned models to Hugging Face Hub with professional documentation
---

# Model Upload & Card Generator

Create model cards and upload fine-tuned models to Hugging Face Hub.

## Gather Context

If coming from training manager, you should have:
- `model_path`, `base_model`, `dataset`, `technique`
- `training_config` (LoRA rank, LR, epochs)
- `final_loss`, `training_time`, `hardware`

If missing, ask for essential information.

## Configuration

### 1. Repository Settings

Ask for:
- **Repo name**: `username/model-name`
- **Visibility**: Public or Private
- **License**: MIT, Apache 2.0, CC-BY-4.0, Llama 3 Community, etc.

### 2. Export Formats

Options:
1. **LoRA adapter only** (~50-200MB) - Users merge themselves
2. **Merged 16-bit** (15-140GB) - Ready to use
3. **GGUF quantized** (4-8GB) - For llama.cpp/Ollama
4. **All of the above** (Recommended)

### 3. GGUF Quantization

If GGUF selected, ask which levels. See [references/GGUF_GUIDE.md](references/GGUF_GUIDE.md).

| Method | Size | Quality |
|--------|------|---------|
| Q4_K_M | ~4GB | Good (Recommended) |
| Q5_K_M | ~5GB | Better |
| Q8_0 | ~8GB | Best |

## Generate Model Card

Create README.md with:

1. **YAML Metadata** - license, tags, base_model, datasets
2. **Model Description** - Table with key attributes
3. **Training Details** - Hyperparameters, LoRA config, results
4. **Usage Examples** - Transformers, Unsloth, Ollama, llama.cpp
5. **Intended Use** - Primary use cases, out-of-scope
6. **Limitations** - Biases, known issues
7. **Citation** - BibTeX entry

## Execute Upload

### 1. Create Repository

```python
from huggingface_hub import create_repo
create_repo("username/model-name", private=False, exist_ok=True)
```

### 2. Upload Files

```python
from huggingface_hub import HfApi
api = HfApi()

# LoRA adapter
api.upload_folder(folder_path="./outputs/lora_adapter", repo_id="username/model")

# Model card
api.upload_file(path_or_fileobj="README.md", path_in_repo="README.md", repo_id="username/model")
```

### 3. Generate GGUF (if selected)

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained("./outputs/lora_adapter")
model.save_pretrained_gguf("./gguf", tokenizer, quantization_method="q4_k_m")
```

Use [scripts/convert_gguf.py](scripts/convert_gguf.py) for multiple quantizations.

### 4. Verify

```python
from huggingface_hub import list_repo_files
print(list_repo_files("username/model"))
```

## Final Report

> **Upload Complete!**
>
> Model: https://huggingface.co/{repo_name}
>
> **Uploaded:**
> - LoRA adapter
> - Model card
> - GGUF files (if selected)
>
> **Next steps:**
> - Verify model page
> - Add example outputs
> - Run benchmarks
> - Share on social media

## Model Card Best Practices

1. **Be specific about limitations**
2. **Include usage examples** - copy-pasteable
3. **Document training details**
4. **Credit sources** - base model, dataset, tools
5. **Use tables** - easier to scan

## Error Handling

| Error | Resolution |
|-------|------------|
| Repo exists | Use `exist_ok=True` |
| Permission denied | Check HF token has write access |
| Upload timeout | Use chunked upload |

## Bundled Resources

- [scripts/convert_gguf.py](scripts/convert_gguf.py) - GGUF conversion
- [references/GGUF_GUIDE.md](references/GGUF_GUIDE.md) - GGUF details and Ollama setup
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Upload issues
