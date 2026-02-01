---
name: tinker
description: Fine-tune LLMs using the Tinker API. Covers supervised fine-tuning, reinforcement learning, LoRA training, vision-language models, and both high-level Cookbook patterns and low-level API usage.
---

# Tinker API - LLM Fine-Tuning

## Overview

Tinker is a training API for large language models from Thinking Machines Lab. It provides:

- **Supervised Fine-Tuning (SFT)**: Train models on instruction/completion pairs
- **Reinforcement Learning (RL)**: PPO and policy gradient losses; cookbook patterns include GRPO-like group rollouts/advantage centering
- **Vision-Language Models**: VLM support via Qwen3-VL
- **LoRA Training**: Efficient parameter-efficient fine-tuning

Two abstraction levels:
- **Tinker Cookbook**: High-level patterns with automatic training loops
- **Low-Level API**: Manual control for custom training logic

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Setup & Core Concepts | [Getting Started](references/getting-started.md) |
| API Classes & Types | [API Reference](references/api-reference.md) |
| Supervised Learning | [Supervised Learning](references/supervised-learning.md) |
| RL Training | [Reinforcement Learning](references/reinforcement-learning.md) |
| Loss Functions | [Loss Functions](references/loss-functions.md) |
| Chat Templates | [Rendering](references/rendering.md) |
| Models & LoRA | [Models & LoRA](references/models-and-lora.md) |
| Example Scripts | [Recipes](references/recipes.md) |

## Installation

```bash
pip install tinker tinker-cookbook
export TINKER_API_KEY=your_api_key_here
```

## Minimal Example

```python
import numpy as np
import tinker
from tinker import types

# Create clients
service_client = tinker.ServiceClient()
training_client = service_client.create_lora_training_client(
    base_model="Qwen/Qwen3-30B-A3B", rank=32
)
tokenizer = training_client.get_tokenizer()

# Prepare data
prompt = "English: hello\nPig Latin:"
completion = " ello-hay\n"
prompt_tokens = tokenizer.encode(prompt, add_special_tokens=True)
completion_tokens = tokenizer.encode(completion, add_special_tokens=False)
tokens = prompt_tokens + completion_tokens
weights = np.array(([0] * len(prompt_tokens)) + ([1] * len(completion_tokens)), dtype=np.float32)
target_tokens = np.array(tokens[1:], dtype=np.int64)

datum = types.Datum(
    model_input=types.ModelInput.from_ints(tokens=tokens[:-1]),
    loss_fn_inputs={
        "target_tokens": target_tokens,
        "weights": weights[1:]
    }
)

# Train
fwdbwd = training_client.forward_backward([datum], "cross_entropy")
optim = training_client.optim_step(types.AdamParams(learning_rate=1e-4))
fwdbwd.result(); optim.result()

# Sample
sampling_client = training_client.save_weights_and_get_sampling_client(name="v1")
result = sampling_client.sample(
    prompt=types.ModelInput.from_ints(tokens=tokenizer.encode("English: world\nPig Latin:", add_special_tokens=True)),
    sampling_params=types.SamplingParams(max_tokens=20),
    num_samples=1
).result()
print(tokenizer.decode(result.sequences[0].tokens))
```

## Common Imports

```python
# Low-level API
import tinker
from tinker import types
from tinker.types import Datum, ModelInput, TensorData, AdamParams, SamplingParams

# Cookbook (high-level)
import chz
import asyncio
from tinker_cookbook.supervised import train
from tinker_cookbook.supervised.types import ChatDatasetBuilder, ChatDatasetBuilderCommonConfig
from tinker_cookbook.supervised.data import (
    SupervisedDatasetFromHFDataset,
    StreamingSupervisedDatasetFromHFDataset,
    FromConversationFileBuilder,
    conversation_to_datum,
)
from tinker_cookbook.renderers import get_renderer, TrainOnWhat
from tinker_cookbook.model_info import get_recommended_renderer_name
from tinker_cookbook.tokenizer_utils import get_tokenizer
```

## When to Use What

| Scenario | Approach |
|----------|----------|
| Standard SFT with HF/JSONL data | Cookbook `ChatDatasetBuilder` + `tinker_cookbook.supervised.train.main()` |
| Custom preprocessing | Custom `SupervisedDataset` class |
| Large datasets (>1M) | `StreamingSupervisedDatasetFromHFDataset` |
| RL / GRPO | Cookbook RL patterns |
| Research / custom loops | Low-level `forward_backward()` + `optim_step()` |
| Vision-language | Qwen3-VL + `ImageChunk` |

## External Resources

- Documentation: https://tinker-docs.thinkingmachines.ai/
- Cookbook Repo: https://github.com/thinking-machines-lab/tinker-cookbook
- Console: https://tinker-console.thinkingmachines.ai
