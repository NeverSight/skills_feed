---
name: megatron-memory-estimator
description: Estimate GPU memory usage for Megatron-based MoE (Mixture of Experts) and dense models. Use when users need to (1) estimate memory from HuggingFace model configs (DeepSeek-V3, Qwen, etc.), (2) plan GPU resource allocation for training, (3) compare different parallelism strategies (TP/PP/EP/CP), (4) determine if a model fits in available GPU memory, or (5) optimize training configurations for memory efficiency.
---

# Megatron Memory Estimator

Estimate GPU memory usage for Megatron-based models directly from HuggingFace configs or custom specifications.

## Quick Start

### Option 1: From HuggingFace Model (Recommended)

Estimate directly from HuggingFace model paths:

```bash
# DeepSeek-V3 (61 layers, requires layer distribution when pp>1)
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 4 --pp 4 --ep 8 --num-gpus 128 --num-layers-in-last-pipeline-stage 16

# Qwen 3
python scripts/estimate_from_hf.py Qwen/Qwen3-235B-A22B \
    --tp 8 --pp 4 --ep 4 --num-gpus 128
```

### Option 2: From Local HF Config

```bash
python scripts/estimate_from_hf.py /path/to/config.json \
    --tp 2 --pp 2 --num-gpus 8
```

### Option 3: Quick Parameter Testing

```bash
# Test different parallelism strategies
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 8 --pp 2 --ep 16 --num-layers-in-last-pipeline-stage 31  # Strategy 1 (30+31=61)

python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 4 --pp 4 --ep 8 --num-layers-in-last-pipeline-stage 16   # Strategy 2 (15+15+15+16=61)

# Test different batch sizes
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 4 --pp 4 --ep 8 --micro-batch-size 2 --num-layers-in-last-pipeline-stage 16
```

## Available Scripts

### estimate_from_hf.py (Primary Script)

Automatically converts HuggingFace configs to Megatron format and estimates memory.

**Key Arguments:**
- `model_path`: HF model path or local config.json path
- `--tp N`: Tensor parallel size (default: 1)
- `--pp N`: Pipeline parallel size (default: 1)
- `--ep N`: Expert parallel size (default: 1, for MoE)
- `--cp N`: Context parallel size (default: 1)
- `--etp N`: Expert tensor parallel size (optional)
- `--vpp N`: Virtual pipeline parallel size (optional)
- `--micro-batch-size N`: Micro batch size (default: 1)
- `--seq-length N`: Sequence length (default: 4096)
- `--num-gpus N`: Total GPU count (default: 8)
- `--recompute-granularity {full,selective}`: Enable activation checkpointing
- `--num-layers-in-first-pipeline-stage N`: Number of layers in the first pipeline stage (use when model layers cannot be evenly divided by `--pp`)
- `--num-layers-in-last-pipeline-stage N`: Number of layers in the last pipeline stage (use when model layers cannot be evenly divided by `--pp`)
- `--verbose`: Show detailed model breakdown
- `--json`: Output as JSON

**Examples:**

```bash
# Basic estimation
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 --num-gpus 64

# With memory optimization
python scripts/estimate_from_hf.py Qwen/Qwen3-235B-A22B \
    --tp 8 --pp 4 --ep 4 \
    --recompute-granularity full \
    --recompute-method uniform \
    --num-gpus 128

# Verbose output
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 4 --pp 4 --ep 8 --verbose --num-layers-in-last-pipeline-stage 16

# JSON output for automation
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 4 --pp 4 --ep 8 --json --num-layers-in-last-pipeline-stage 16 > result.json
```



## Common Workflows

### Find Optimal Parallelism for a Model

```bash
# Start with model path
MODEL="deepseek-ai/DeepSeek-V3"
GPUS=128

# Test different strategies
python scripts/estimate_from_hf.py $MODEL --tp 4 --pp 4 --ep 8 --num-gpus $GPUS --num-layers-in-last-pipeline-stage 16
python scripts/estimate_from_hf.py $MODEL --tp 8 --pp 2 --ep 8 --num-gpus $GPUS --num-layers-in-last-pipeline-stage 31


# Choose strategy that fits GPU memory with best efficiency
```

### Optimize for Memory Efficiency

Progressive memory reduction:

```bash
# 1. Baseline
python scripts/estimate_from_hf.py $MODEL --tp 4 --pp 2 --num-gpus 16

# 2. Add recomputation
python scripts/estimate_from_hf.py $MODEL --tp 4 --pp 2 --num-gpus 16 \
    --recompute-granularity full

# 3. Increase expert parallelism (MoE only)
python scripts/estimate_from_hf.py $MODEL --tp 4 --pp 2 --ep 4 --num-gpus 16 \
    --recompute-granularity full

# 4. Increase pipeline parallelism
python scripts/estimate_from_hf.py $MODEL --tp 4 --pp 4 --ep 4 --num-gpus 16 \
    --recompute-granularity full

# 5. Last resort: reduce batch size
python scripts/estimate_from_hf.py $MODEL --tp 4 --pp 4 --ep 4 --num-gpus 16 \
    --recompute-granularity full --micro-batch-size 1
```

### Check if Model Fits Available GPUs

```bash
# Check if DeepSeek-V3 fits in 128x A100 80GB
python scripts/estimate_from_hf.py deepseek-ai/DeepSeek-V3 \
    --tp 4 --pp 4 --ep 8 --num-gpus 128 --num-layers-in-last-pipeline-stage 16

# Output will show peak memory per GPU
# If < 80 GB: ✓ Fits
# If > 80 GB: Need more parallelism or optimization
```

## Understanding Output

The estimator shows:

```
================================================================================
CONFIGURATION SUMMARY
================================================================================

Model Type: deepseek_v3
Architecture: 61L-7168H
MoE: 256 experts, top-8

Parallelism:
  TP=4, PP=4, EP=8, CP=1

Training:
  Micro Batch Size: 1
  Sequence Length: 4096
  Total GPUs: 128

================================================================================
MEMORY ESTIMATION RESULTS
================================================================================

Pipeline Stage 0:
  Parameters: 3.15B
  Activations: 1.23B
  Memory Breakdown:
    - Weights + Gradients: 18.90 GB
    - Weights + Gradients + Optimizer: 37.80 GB
    - Activations: 2.46 GB
    - Total: 40.26 GB

================================================================================
Peak Memory per GPU: 40.26 GB
✓ Fits in: A100 80GB, H100
================================================================================
```

**Memory Components:**
- **Weights + Gradients**: Parameters and gradients (2+2=4 bytes/param in FP16)
- **Optimizer States**: Adam momentum + variance (8 bytes/param)
- **Activations**: Forward pass activations stored for backward

**GPU Fit Guidelines:**
- < 40 GB: A100 40GB, A100 80GB, H100
- < 80 GB: A100 80GB, H100 80GB
- \> 80 GB: H200 141GB or consider more parallelism or smaller batch

## Memory Optimization Techniques

Ranked by effectiveness:

1. **Enable Distributed Optimizer** (included by default)
   - Shards optimizer states across data parallel ranks
   - ~6 bytes/param saving

2. **Activation Recomputation** (`--recompute-granularity full`)
   - 50-70% activation memory reduction
   - Trade compute for memory

3. **Increase Expert Parallelism** (MoE only) (`--ep N`)
   - Linear memory reduction for expert layers
   - Minimal performance impact

4. **Increase Pipeline Parallelism** (`--pp N`)
   - Splits model across more stages
   - Some pipeline bubble overhead

5. **Reduce Batch Size** (`--micro-batch-size 1`)
   - Direct activation memory reduction
   - Impacts throughput

## Supported Models

The script automatically handles:

- **DeepSeek**: DeepSeek-V2, DeepSeek-V3
- **Qwen**: Qwen2.5, Qwen3 (dense and MoE)
- **Moonlight**: Kimi models
- **Any HuggingFace model with config.json**


## Setup & Troubleshooting
   
Because this tool relies on Megatron-LM components, you need to add both the tool directory and Megatron-LM to your `PYTHONPATH`.

**Recommended Setup:**

```bash
# Add current directory and Megatron-LM to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd):/path/to/Megatron-LM
```

If you encounter `ImportError: No module named 'megatron_memory_estimator'`, ensure the root directory of this skill is in your `PYTHONPATH`.

## Dependencies

**Required:**
- `mbridge`: HuggingFace to Megatron config bridge
- `transformers`: HuggingFace transformers library
- `torch`: PyTorch (CPU version sufficient)
- `megatron-core`: Megatron core library

**Installation:**
```bash
pip install mbridge transformers torch megatron-core==0.13.0
```

For full Megatron-LM support (optional):
```bash
pip install git+https://github.com/NVIDIA/Megatron-LM.git@core_r0.13.0
```

## Reference Documentation

For detailed configuration options:
- `references/configuration_guide.md`: All configuration parameters
- `references/parallelism_strategies.md`: Parallelism strategy guide

## Notes

- Estimates are theoretical based on model architecture
- Actual memory may vary ±10-15% due to framework overhead
- Always leave 10-20% memory headroom for safety
- Test on small scale before full deployment
- MoE models: Expert parallelism (EP) is critical for memory efficiency
