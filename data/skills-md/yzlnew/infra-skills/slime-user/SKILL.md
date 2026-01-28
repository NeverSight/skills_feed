---
name: slime-user
description: Guide for using SLIME (LLM post-training framework for RL Scaling). Use when working with SLIME for reinforcement learning training of language models, including setup, configuration, training execution, multi-turn interactions, custom reward models, tool calling scenarios, or troubleshooting SLIME workflows. Covers GRPO, GSPO, PPO, Reinforce++, multi-agent RL, VLM training, FSDP/Megatron backends, SGLang integration, dynamic sampling, and custom generation functions.
---

# SLIME User Guide

SLIME is an LLM post-training framework for RL Scaling developed by THUDM. It supports various RL algorithms (GRPO, GSPO, PPO, Reinforce++), multiple training backends (Megatron, FSDP), and advanced features like multi-turn interactions, tool calling, and dynamic sampling.

## Quick Start Workflow

### For First-Time Users

1. **Environment Setup**
   - Use Docker: `docker pull slimerl/slime:latest`
   - Or build from source: See `docs/en/get_started/quick_start.md`
   - Hardware: Supports H100/H200, B200 series

2. **Download Model and Data**
   ```bash
   hf download Qwen/Qwen3-4B --local-dir /root/Qwen3-4B
   hf download --repo-type dataset zhuzilin/dapo-math-17k --local-dir /root/dapo-math-17k
   ```

3. **Convert Weights** (Megatron backend only)
   ```bash
   source scripts/models/qwen3-4B.sh
   PYTHONPATH=/root/Megatron-LM python tools/convert_hf_to_torch_dist.py \
       ${MODEL_ARGS[@]} \
       --hf-checkpoint /root/Qwen3-4B \
       --save /root/Qwen3-4B_torch_dist
   ```

4. **Run Training**
   ```bash
   bash scripts/run-qwen3-4B.sh
   ```

### For Experienced Users

When user needs specific functionality:
- **Multi-turn/tool calling**: Read [references/examples_reference.md](references/examples_reference.md) Search-R1 section
- **Custom reward models**: See custom RM pattern in examples reference
- **FSDP instead of Megatron**: Use `--train-backend fsdp`, skip weight conversion
- **Large-scale training**: See multi-node examples (GLM-4.5, DeepSeek-R1)
- **Source code exploration**: Check [references/source_code_reference.md](references/source_code_reference.md)

## Documentation Navigation

SLIME has extensive documentation. Use this guide to find what you need quickly.

### Essential Documentation (Read These First)
1. **Quick Start Guide**: `docs/en/get_started/quick_start.md` - Setup and first training run
2. **Usage Guide**: `docs/en/get_started/usage.md` - Comprehensive parameter reference
3. **Example Docs**: `docs/en/examples/qwen3-4B.md` or `docs/en/examples/glm4-9B.md`

For detailed navigation of all documentation, see [references/doc_navigation.md](references/doc_navigation.md).

### Common Tasks → Documentation Mapping

| Task | Documentation |
|------|---------------|
| First-time setup | `docs/en/get_started/quick_start.md` |
| Understanding parameters | `docs/en/get_started/usage.md` |
| Basic training (8 GPUs) | `docs/en/examples/qwen3-4B.md` |
| Multi-turn tool use | `examples/search-r1/` |
| Custom generation logic | `docs/en/get_started/customization.md` |
| Multi-node training | `docs/en/examples/glm4.5-355B-A32B.md` |
| FSDP backend | `docs/en/get_started/usage.md` (FSDP section) |
| VLM training | `examples/geo3k_vlm/` |
| Troubleshooting | `docs/en/get_started/qa.md` |

## Core Concepts

### Training Loop
SLIME uses a "Rollout → Train" loop:
1. **Rollout**: Generate responses using SGLang inference
2. **Reward**: Compute rewards using reward model
3. **Train**: Update model weights using Megatron/FSDP
4. Repeat for `--num-rollout` iterations

### Key Constraint
```
rollout-batch-size × n-samples-per-prompt = global-batch-size × num-steps-per-rollout
```

### Resource Allocation Modes

**Colocated** (training and inference share GPUs):
```bash
--actor-num-nodes 1 \
--actor-num-gpus-per-node 8 \
--colocate \
--sglang-mem-fraction-static 0.7
```

**Disaggregated** (separate GPUs for training/inference):
```bash
--actor-num-nodes 1 \
--actor-num-gpus-per-node 4 \
--rollout-num-gpus 4
```

## Parameter Quick Reference

### Essential Parameters

**Model Loading**:
- `--hf-checkpoint`: HuggingFace model path (for SGLang and FSDP)
- `--ref-load`: Megatron reference model checkpoint
- `--load`: Megatron actor checkpoint (resume training)
- `--save`: Save path for checkpoints

**Data**:
- `--prompt-data`: JSONL dataset path
- `--input-key`: Field name for prompts (default: "prompt")
- `--label-key`: Field name for labels (default: "label")
- `--metadata-key`: Field name for metadata (default: "metadata")
- `--apply-chat-template`: Apply tokenizer chat template

**Rollout**:
- `--rollout-batch-size`: Prompts per rollout
- `--n-samples-per-prompt`: Responses per prompt
- `--rollout-max-response-len`: Max response length
- `--rollout-temperature`: Sampling temperature

**Training**:
- `--num-rollout`: Total training iterations
- `--num-steps-per-rollout`: Optimizer steps per rollout (default: 1)
- `--global-batch-size`: Samples per optimizer step
- `--advantage-estimator`: RL algorithm (grpo, gspo, ppo, reinforce_plus_plus)

**Reward Model**:
- `--rm-type`: Built-in RM type (e.g., "deepscaler")
- `--custom-rm-path`: Custom RM function path

**Backends**:
- `--train-backend`: Training backend (megatron or fsdp)
- `--rollout-num-gpus-per-engine`: GPUs per SGLang engine (like tp_size)

For complete parameter reference, see `docs/en/get_started/usage.md`.

## Common Workflows

### 1. Standard Single-Turn Training

Use example scripts as templates:
- `scripts/run-qwen3-4B.sh`: Basic 8xH100 setup
- `scripts/run-glm4-9B.sh`: With dynamic sampling

Key sections in script:
```bash
# Load model config
source scripts/models/qwen3-4B.sh

# Configure checkpoints
CKPT_ARGS=(--hf-checkpoint /root/Qwen3-4B ...)

# Configure rollout
ROLLOUT_ARGS=(
  --rollout-batch-size 32
  --n-samples-per-prompt 8
  --rm-type deepscaler
)

# Configure algorithm
GRPO_ARGS=(--advantage-estimator grpo ...)

# Run training
ray job submit ... -- python3 train.py \
  ${MODEL_ARGS[@]} ${CKPT_ARGS[@]} ${ROLLOUT_ARGS[@]} ...
```

### 2. Multi-Turn Tool Calling

For multi-turn scenarios (like Search-R1):

1. **Prepare Data** with metadata:
   ```json
   {
     "question": "User query",
     "final_answer": "Expected answer",
     "metadata": "{\"session_id\": \"123\", \"tool_code\": \"...\"}"
   }
   ```

2. **Implement Custom Generation Function**:
   ```python
   async def generate(args, sample: Sample, sampling_params) -> Sample:
       for turn in range(max_turns):
           # Generate action
           model_output = await call_sglang(...)
           sample.loss_mask += [1] * len(model_tokens)  # Train on actions

           # Execute tool
           tool_output = await execute_tool(...)
           sample.loss_mask += [0] * len(tool_tokens)  # Mask tool outputs

           if action == "answer":
               break

       sample.tokens = prompt_tokens + response_tokens
       sample.response_length = len(response_tokens)
       return sample
   ```

3. **Configure Custom Functions**:
   ```bash
   --custom-generate-function-path my_module.generate \
   --custom-rm-path my_module.reward_func \
   --metadata-key metadata
   ```

See `examples/search-r1/` for complete example.

### 3. Dynamic Sampling (DAPO-style)

Filter low-quality samples during generation:

```bash
ROLLOUT_ARGS+=(
  --over-sampling-batch-size 64 \
  --rollout-batch-size 32 \
  --dynamic-sampling-filter-path \
    slime.rollout.filter_hub.dynamic_sampling_filters.check_reward_nonzero_std
)
```

How it works:
- Samples 64 prompts (over-sampling)
- Filters groups based on reward diversity
- Keeps only 32 prompts × 8 samples that pass filter
- Automatically resamples if too many filtered out

### 4. FSDP Backend (No Weight Conversion)

```bash
--train-backend fsdp \
--hf-checkpoint /root/Qwen3-4B \
--gradient-checkpointing \
--context-parallel-size 2
```

Benefits:
- No HF → Megatron weight conversion needed
- Directly load HuggingFace checkpoints
- Simpler setup for supported models

See `examples/geo3k_vlm/` and `docs/en/get_started/usage.md` FSDP section.

### 5. Multi-Node Training

1. Start Ray cluster:
   ```bash
   # Head node
   ray start --head --node-ip-address ${MASTER_ADDR} --num-gpus 8

   # Worker nodes
   ray start --address=${MASTER_ADDR}:6379 --num-gpus 8
   ```

2. Submit job:
   ```bash
   ray job submit --address="http://127.0.0.1:8265" \
     --runtime-env-json='{"env_vars": {"PYTHONPATH": "/root/Megatron-LM/"}}' \
     -- python3 train.py \
     --actor-num-nodes 8 \
     --actor-num-gpus-per-node 8 \
     ...
   ```

See `docs/en/examples/glm4.5-355B-A32B.md` for large-scale example.

## Customization Guide

### Custom Reward Model

Implement async function:
```python
async def my_reward_func(args, sample: Sample, **kwargs) -> float:
    # Access sample fields
    prompt = sample.prompt
    response = sample.response
    label = sample.label

    # Compute reward
    reward = compute_score(response, label)
    return float(reward)
```

Use with: `--custom-rm-path module.path:my_reward_func`

### Custom Generation Function

Implement async function:
```python
async def my_generate(args, sample: Sample, sampling_params) -> Sample:
    # Load tokenizer
    from slime.utils.processing_utils import load_tokenizer
    tokenizer = load_tokenizer(args.hf_checkpoint, trust_remote_code=True)

    # Generate response (call SGLang API or custom logic)
    from slime.utils.http_utils import post
    output = await post(
        f"http://{args.sglang_router_ip}:{args.sglang_router_port}/generate",
        {"text": sample.prompt, "sampling_params": sampling_params}
    )

    # Set sample fields
    prompt_tokens = tokenizer(sample.prompt, add_special_tokens=False)["input_ids"]
    response_tokens = tokenizer(output["text"], add_special_tokens=False)["input_ids"]

    sample.tokens = prompt_tokens + response_tokens
    sample.response_length = len(response_tokens)
    sample.response = output["text"]
    sample.truncated = output["meta_info"]["finish_reason"]["type"] == "length"

    return sample
```

Use with: `--custom-generate-function-path module.path:my_generate`

### Custom Dynamic Filter

Implement filter function:
```python
def my_filter(args, samples: list[Sample], **kwargs) -> bool:
    # Return True to keep samples, False to discard
    return all(sample.reward > 0.5 for sample in samples)
```

Use with: `--dynamic-sampling-filter-path module.path:my_filter`

## Examples Reference

For detailed examples and patterns, see [references/examples_reference.md](references/examples_reference.md).

Quick finder:
- **Basic math training**: `scripts/run-qwen3-4B.sh`
- **Multi-turn tool use**: `examples/search-r1/`
- **Vision-language RL**: `examples/geo3k_vlm/`
- **Large-scale MOE**: `docs/en/examples/glm4.5-355B-A32B.md`
- **Custom generation**: `examples/search-r1/search_r1_logic.py`
- **FSDP backend**: `examples/geo3k_vlm/`

## Source Code Reference

For source code exploration, see [references/source_code_reference.md](references/source_code_reference.md).

Key files:
- **Arguments**: `slime/utils/arguments.py`
- **Rollout**: `slime/rollout/sglang_rollout.py`
- **Sample type**: `slime/utils/types.py`
- **Reward models**: `slime/rollout/rm_hub/`
- **Conversion tools**: `tools/convert_hf_to_torch_dist.py`

## Troubleshooting

### Common Issues

**OOM during colocated training**:
- Reduce `--sglang-mem-fraction-static` (try 0.7 or 0.6)
- Reduce `--max-tokens-per-gpu`
- Enable gradient checkpointing: `--recompute-granularity full`

**Mismatched batch sizes**:
- Ensure: `rollout-batch-size × n-samples-per-prompt = global-batch-size × num-steps-per-rollout`

**Weight conversion errors**:
- Check model config matches exactly (e.g., `--rotary-base`)
- Use FSDP backend to skip conversion: `--train-backend fsdp`

**Multi-node communication issues**:
- Set environment variables: `GLOO_SOCKET_IFNAME`, `NCCL_SOCKET_IFNAME`
- See `docs/en/get_started/quick_start.md` multi-node section

**SGLang concurrency issues**:
- Limit concurrency: `--sglang-server-concurrency 160`
- Increase CUDA graphs: `--sglang-cuda-graph-bs 1 2 4 8 $(seq 16 8 256)`

For more troubleshooting, see `docs/en/get_started/qa.md`.

## Additional Resources

### Reference Files
- **Doc Navigation**: [references/doc_navigation.md](references/doc_navigation.md) - Find documentation quickly
- **Examples Reference**: [references/examples_reference.md](references/examples_reference.md) - Example scripts and patterns
- **Source Code Reference**: [references/source_code_reference.md](references/source_code_reference.md) - Code structure and key functions

### External Links
- **GitHub Repository**: https://github.com/THUDM/slime
- **Docker Image**: `slimerl/slime:latest`
- **Megatron-LM**: https://github.com/NVIDIA/Megatron-LM
- **SGLang**: https://github.com/sgl-project/sglang
