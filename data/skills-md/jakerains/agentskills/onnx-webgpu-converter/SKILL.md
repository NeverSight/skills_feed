---
name: onnx-webgpu-converter
description: Convert HuggingFace transformer models to ONNX format for browser inference with Transformers.js and WebGPU. Use when given a HuggingFace model link to convert to ONNX, when setting up optimum-cli for ONNX export, when quantizing models (fp16, q8, q4) for web deployment, when configuring Transformers.js with WebGPU acceleration, or when troubleshooting ONNX conversion errors. Triggers on mentions of ONNX conversion, Transformers.js, WebGPU inference, optimum export, model quantization for browser, or running ML models in the browser.
---

# ONNX WebGPU Model Converter

Convert any HuggingFace model to ONNX and run it in the browser with Transformers.js + WebGPU.

## Workflow Overview

1. **Check if ONNX version already exists** on HuggingFace
2. **Set up Python environment** with optimum
3. **Export model to ONNX** with optimum-cli
4. **Quantize** for target deployment (WebGPU vs WASM)
5. **Upload to HuggingFace Hub** (optional)
6. **Use in Transformers.js** with WebGPU

## Step 1: Check for Existing ONNX Models

Before converting, check if the model already has an ONNX version:

- Search `onnx-community/<model-name>` on HuggingFace Hub
- Check the model repo for an `onnx/` folder
- Browse https://huggingface.co/models?library=transformers.js (1200+ pre-converted)

If found, skip to Step 6.

## Step 2: Environment Setup

```bash
# Create venv (recommended)
python -m venv onnx-env && source onnx-env/bin/activate

# Install optimum with ONNX support
pip install "optimum[onnx]" onnxruntime

# For GPU-accelerated export (optional)
pip install onnxruntime-gpu
```

**Verify installation:**
```bash
optimum-cli export onnx --help
```

## Step 3: Export to ONNX

### Basic Export (auto-detect task)

```bash
optimum-cli export onnx --model <model_id_or_path> ./output_dir/
```

### With Explicit Task

```bash
optimum-cli export onnx \
  --model <model_id> \
  --task <task> \
  ./output_dir/
```

**Common tasks:** `text-generation`, `text-classification`, `feature-extraction`, `image-classification`, `automatic-speech-recognition`, `object-detection`, `image-segmentation`, `question-answering`, `token-classification`, `zero-shot-classification`

For decoder models, append `-with-past` for KV cache reuse (default behavior):
`text-generation-with-past`, `text2text-generation-with-past`, `automatic-speech-recognition-with-past`

### Full CLI Reference

| Flag | Description |
|------|-------------|
| `-m MODEL, --model MODEL` | HuggingFace model ID or local path (required) |
| `--task TASK` | Export task (auto-detected if on Hub) |
| `--opset OPSET` | ONNX opset version (default: auto) |
| `--device DEVICE` | Export device, `cpu` (default) or `cuda` |
| `--optimize {O1,O2,O3,O4}` | ONNX Runtime optimization level |
| `--monolith` | Force single ONNX file (vs split encoder/decoder) |
| `--no-post-process` | Skip post-processing (e.g., decoder merging) |
| `--trust-remote-code` | Allow custom model code from Hub |
| `--pad_token_id ID` | Override pad token (needed for some models) |
| `--cache_dir DIR` | Cache directory for downloaded models |
| `--batch_size N` | Batch size for dummy inputs |
| `--sequence_length N` | Sequence length for dummy inputs |
| `--framework {pt}` | Source framework |
| `--atol ATOL` | Absolute tolerance for validation |

### Optimization Levels

| Level | Description |
|-------|-------------|
| O1 | Basic general optimizations |
| O2 | Basic + extended + transformer fusions |
| O3 | O2 + GELU approximation |
| O4 | O3 + mixed precision fp16 (GPU only, requires `--device cuda`) |

## Step 4: Quantize for Web Deployment

### Quantization Types for Transformers.js

| dtype | Precision | Best For | Size Reduction |
|-------|-----------|----------|----------------|
| `fp32` | Full 32-bit | Maximum accuracy | None (baseline) |
| `fp16` | Half 16-bit | WebGPU default quality | ~50% |
| `q8` / `int8` | 8-bit | WASM default, good balance | ~75% |
| `q4` / `bnb4` | 4-bit | Maximum compression | ~87% |
| `q4f16` | 4-bit weights, fp16 compute | WebGPU + small size | ~87% |

### Using optimum-cli quantization

```bash
# Dynamic quantization (post-export)
optimum-cli onnxruntime quantize \
  --onnx_model ./output_dir/ \
  --avx512 \
  -o ./quantized_dir/
```

### Using Python API for finer control

```python
from optimum.onnxruntime import ORTQuantizer, ORTModelForSequenceClassification
from optimum.onnxruntime.configuration import AutoQuantizationConfig

model = ORTModelForSequenceClassification.from_pretrained("./output_dir/")
quantizer = ORTQuantizer.from_pretrained(model)
config = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)
quantizer.quantize(save_dir="./quantized_dir/", quantization_config=config)
```

### Producing Multiple dtype Variants for Transformers.js

To provide fp32, fp16, q8, and q4 variants (like `onnx-community` models), organize output as:

```
model_onnx/
├── onnx/
│   ├── model.onnx              # fp32
│   ├── model_fp16.onnx         # fp16
│   ├── model_quantized.onnx    # q8
│   └── model_q4.onnx           # q4
├── config.json
├── tokenizer.json
└── tokenizer_config.json
```

## Step 5: Upload to HuggingFace Hub (Optional)

```bash
# Login
huggingface-cli login

# Upload
huggingface-cli upload <your-username>/<model-name>-onnx ./output_dir/

# Add transformers.js tag to model card for discoverability
```

## Step 6: Use in Transformers.js with WebGPU

### Install

```bash
npm install @huggingface/transformers
```

### Basic Pipeline with WebGPU

```javascript
import { pipeline } from "@huggingface/transformers";

const pipe = await pipeline("task-name", "model-id-or-path", {
  device: "webgpu",    // GPU acceleration
  dtype: "q4",         // Quantization level
});

const result = await pipe("input text");
```

### Per-Module dtypes (encoder-decoder models)

Some models (Whisper, Florence-2) need different quantization per component:

```javascript
const model = await Florence2ForConditionalGeneration.from_pretrained(
  "onnx-community/Florence-2-base-ft",
  {
    dtype: {
      embed_tokens: "fp16",
      vision_encoder: "fp16",
      encoder_model: "q4",
      decoder_model_merged: "q4",
    },
    device: "webgpu",
  },
);
```

**For detailed Transformers.js WebGPU usage patterns:** See references/webgpu-usage.md

## Troubleshooting

**For conversion errors and common issues:** See references/conversion-guide.md

### Quick Fixes

- **"Task not found"**: Use `--task` flag explicitly. For decoder models try `text-generation-with-past`
- **"trust_remote_code"**: Add `--trust-remote-code` flag for custom model architectures
- **Out of memory**: Use `--device cpu` and smaller `--batch_size`
- **Validation fails**: Try `--no-post-process` or increase `--atol`
- **Model not supported**: Check [supported architectures](https://huggingface.co/docs/optimum-onnx/onnx/package_reference/configuration#supported-architectures) — 120+ architectures supported
- **WebGPU fallback to WASM**: Ensure browser supports WebGPU (Chrome 113+, Edge 113+)

## Supported Task → Pipeline Mapping

| Task | Transformers.js Pipeline | Example Model |
|------|-------------------------|---------------|
| text-classification | `sentiment-analysis` | distilbert-base-uncased-finetuned-sst-2 |
| text-generation | `text-generation` | Qwen2.5-0.5B-Instruct |
| feature-extraction | `feature-extraction` | mxbai-embed-xsmall-v1 |
| automatic-speech-recognition | `automatic-speech-recognition` | whisper-tiny.en |
| image-classification | `image-classification` | mobilenetv4_conv_small |
| object-detection | `object-detection` | detr-resnet-50 |
| image-segmentation | `image-segmentation` | segformer-b0 |
| zero-shot-image-classification | `zero-shot-image-classification` | clip-vit-base-patch32 |
| depth-estimation | `depth-estimation` | depth-anything-small |
| translation | `translation` | nllb-200-distilled-600M |
| summarization | `summarization` | bart-large-cnn |
