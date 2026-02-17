---
name: llm-training
description: Use when "training LLM", "finetuning", "RLHF", "distributed training", "DeepSpeed", "Accelerate", "PyTorch Lightning", "Ray Train", "TRL", "Unsloth", "LoRA training", "flash attention", "gradient checkpointing"
version: 1.0.0
---

# LLM Training

Frameworks and techniques for training and finetuning large language models.

## Framework Comparison

| Framework | Best For | Multi-GPU | Memory Efficient |
|-----------|----------|-----------|------------------|
| **Accelerate** | Simple distributed | Yes | Basic |
| **DeepSpeed** | Large models, ZeRO | Yes | Excellent |
| **PyTorch Lightning** | Clean training loops | Yes | Good |
| **Ray Train** | Scalable, multi-node | Yes | Good |
| **TRL** | RLHF, reward modeling | Yes | Good |
| **Unsloth** | Fast LoRA finetuning | Limited | Excellent |

---

## Accelerate (HuggingFace)

Minimal wrapper for distributed training. Run `accelerate config` for interactive setup.

**Key concept**: Wrap model, optimizer, dataloader with `accelerator.prepare()`, use `accelerator.backward()` for loss.

---

## DeepSpeed (Large Models)

Microsoft's optimization library for training massive models.

**ZeRO Stages:**

- **Stage 1**: Optimizer states partitioned across GPUs
- **Stage 2**: + Gradients partitioned
- **Stage 3**: + Parameters partitioned (for largest models, 100B+)

**Key concept**: Configure via JSON, higher stages = more memory savings but more communication overhead.

---

## TRL (RLHF/DPO)

HuggingFace library for reinforcement learning from human feedback.

**Training types:**

- **SFT (Supervised Finetuning)**: Standard instruction tuning
- **DPO (Direct Preference Optimization)**: Simpler than RLHF, uses preference pairs
- **PPO**: Classic RLHF with reward model

**Key concept**: DPO is often preferred over PPO - simpler, no reward model needed, just chosen/rejected response pairs.

---

## Unsloth (Fast LoRA)

Optimized LoRA finetuning - 2x faster, 60% less memory.

**Key concept**: Drop-in replacement for standard LoRA with automatic optimizations. Best for 7B-13B models.

---

## Memory Optimization Techniques

| Technique | Memory Savings | Trade-off |
|-----------|---------------|-----------|
| **Gradient checkpointing** | ~30-50% | Slower training |
| **Mixed precision (fp16/bf16)** | ~50% | Minor precision loss |
| **4-bit quantization (QLoRA)** | ~75% | Some quality loss |
| **Flash Attention** | ~20-40% | Requires compatible GPU |
| **Gradient accumulation** | Effective batch↑ | No memory cost |

---

## Decision Guide

| Scenario | Recommendation |
|----------|----------------|
| Simple finetuning | Accelerate + PEFT |
| 7B-13B models | Unsloth (fastest) |
| 70B+ models | DeepSpeed ZeRO-3 |
| RLHF/DPO alignment | TRL |
| Multi-node cluster | Ray Train |
| Clean code structure | PyTorch Lightning |

## Resources

- Accelerate: <https://huggingface.co/docs/accelerate>
- DeepSpeed: <https://www.deepspeed.ai/>
- TRL: <https://huggingface.co/docs/trl>
- Unsloth: <https://github.com/unslothai/unsloth>
