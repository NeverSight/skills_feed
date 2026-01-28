---
name: ocr-super-surya
description: "GPU-optimized OCR using Surya. Use when: (1) Extracting text from images/screenshots, (2) Processing PDFs with embedded images, (3) Multi-language document OCR, (4) Layout analysis and table detection. Supports 90+ languages with 2x accuracy over Tesseract."
license: CC BY-NC 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# OCR Super Surya

GPU-optimized OCR skill using [Surya](https://github.com/datalab-to/surya) - a modern, high-accuracy OCR engine.

## When to Use

- Extracting text from screenshots, photos, or scanned images
- Processing PDFs with embedded images
- Multi-language document OCR (90+ languages including Japanese)
- Layout analysis and table detection
- When GPU acceleration is available and desired

## Key Features

| Feature         | Description                                        |
| --------------- | -------------------------------------------------- |
| **Accuracy**    | 2x better than Tesseract (0.97 vs 0.88 similarity) |
| **GPU Support** | PyTorch-based, CUDA optimized                      |
| **Languages**   | 90+ languages including CJK                        |
| **Layout**      | Document layout analysis, table recognition        |
| **LaTeX**       | Inline math equation recognition                   |

## Quick Start

### Installation

#### Step 1: GPU Check

Before installing, check if GPU is available:

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
```

**⚠️ If CUDA = False but you have an NVIDIA GPU:**

You have CPU-only PyTorch installed. Reinstall with CUDA support:

```bash
# Uninstall CPU version
pip uninstall torch torchvision torchaudio -y

# Install CUDA version (check your CUDA version with: nvidia-smi)
# CUDA 12.1 (recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8 (older GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**No GPU?** Surya works on CPU too (slower, but functional).

#### Step 2: Install Surya

```bash
# Core OCR (includes pypdfium2 for PDF support)
pip install surya-ocr
```

**Note:** Surya includes `pypdfium2` for PDF processing. No external dependencies (Poppler) required.

### Basic Usage

```python
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from surya.foundation import FoundationPredictor

# Load image
image = Image.open("document.png")

# Initialize predictors (auto-detects GPU)
foundation_predictor = FoundationPredictor()
recognition_predictor = RecognitionPredictor(foundation_predictor)
detection_predictor = DetectionPredictor()

# Run OCR
predictions = recognition_predictor([image], det_predictor=detection_predictor)

# Get text
for page in predictions:
    for line in page.text_lines:
        print(line.text)
```

### CLI Usage

```bash
# OCR single image
surya_ocr image.png

# OCR with output to JSON
surya_ocr image.png --output_dir ./results

# Launch GUI (requires streamlit)
pip install streamlit
surya_gui
```

### Helper Script CLI

```bash
# Basic usage
python scripts/ocr_helper.py image.png

# With verbose logging
python scripts/ocr_helper.py image.png -v

# Specify languages and output file
python scripts/ocr_helper.py document.pdf -l ja en -o result.txt

# Disable OOM auto-retry
python scripts/ocr_helper.py large_image.png --no-retry
```

## GPU Configuration

Surya auto-detects GPU. Adjust VRAM usage with environment variables:

| Variable                 | Default | Description                                |
| ------------------------ | ------- | ------------------------------------------ |
| `RECOGNITION_BATCH_SIZE` | 512     | Reduce for lower VRAM (e.g., 256 for 12GB) |
| `DETECTOR_BATCH_SIZE`    | 36      | Reduce if OOM errors occur                 |

```bash
# Linux/macOS
export RECOGNITION_BATCH_SIZE=256
export DETECTOR_BATCH_SIZE=16
surya_ocr image.png
```

```powershell
# Windows PowerShell
$env:RECOGNITION_BATCH_SIZE = 256
$env:DETECTOR_BATCH_SIZE = 16
surya_ocr image.png
```

### OOM Auto-Retry

The helper script automatically retries with reduced batch size on GPU OOM:

```python
# Auto-retry enabled by default
text = ocr_image("large_image.png")  # Retries up to 3x

# Disable if you want manual control
text = ocr_image("large_image.png", auto_retry=False)
```

## Use Cases

| Use Case         | Command / Function                                     |
| ---------------- | ------------------------------------------------------ |
| Screenshot OCR   | `python scripts/ocr_helper.py screenshot.png`          |
| PDF Processing   | `ocr_pdf("document.pdf")` → returns list of page texts |
| Batch Processing | `ocr_batch(["img1.png", "img2.png"])` → returns dict   |
| Japanese/CJK     | Auto-detected, no config needed                        |

## Scripts

| Script                  | Description                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| `scripts/ocr_helper.py` | Helper functions with OOM auto-retry, verbose logging, batch support |

### Helper Script Features

| Feature         | Description                                          |
| --------------- | ---------------------------------------------------- |
| `verbose`       | Enable detailed logging (`-v` in CLI)                |
| `auto_retry`    | Automatically reduce batch size on OOM (default: on) |
| `ocr_image()`   | Single image OCR                                     |
| `ocr_pdf()`     | PDF OCR (all pages)                                  |
| `ocr_batch()`   | Batch OCR for multiple images                        |
| `set_verbose()` | Enable/disable logging programmatically              |

## Troubleshooting

### GPU Not Detected (CUDA = False)

**Symptom:** `CUDA available: False` even with NVIDIA GPU

**Cause:** CPU-only PyTorch installed instead of CUDA version

**Fix:**

```bash
# 1. Check your CUDA version
nvidia-smi  # Look for "CUDA Version: X.X"

# 2. Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Verify:**

```python
import torch
print(torch.cuda.is_available())  # Should be True
print(torch.cuda.get_device_name(0))  # Should show your GPU name
```

### CUDA Out of Memory

Reduce batch sizes:

```bash
export RECOGNITION_BATCH_SIZE=128
export DETECTOR_BATCH_SIZE=8
```

### CPU Fallback

If no GPU available, Surya automatically falls back to CPU (slower but works).

### Model Download

First run downloads models (~2GB). Ensure internet connection.

## References

- [Surya GitHub](https://github.com/datalab-to/surya) - Official repository
- [Surya Documentation](https://github.com/datalab-to/surya#readme) - Usage guide
- [Benchmark Results](https://github.com/datalab-to/surya#benchmarks) - Accuracy comparisons

## License Notice

**This skill**: CC BY-NC 4.0 (wrapper scripts only)

**Surya (underlying OCR engine)**:

- Code: GPL-3.0
- Models: Free for research, personal use, and startups under $2M funding/revenue
- Commercial use beyond $2M: See [Surya Pricing](https://www.datalab.to/pricing)
