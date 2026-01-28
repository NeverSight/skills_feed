---
name: faion-ml-ops
description: "ML operations: fine-tuning (LoRA, QLoRA), model evaluation, cost optimization, observability."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# ML Ops Skill

**Communication: User's language. Code: English.**

## Purpose

Handles ML model operations. Covers fine-tuning, evaluation, cost management, and observability.

## Scope

| Area | Coverage |
|------|----------|
| **Fine-tuning** | LoRA, QLoRA, OpenAI fine-tuning, datasets |
| **Evaluation** | Metrics, benchmarks, frameworks |
| **Cost Optimization** | Token management, caching, batch APIs |
| **Observability** | LLM monitoring, tracing, logging |

## Quick Start

| Task | Files |
|------|-------|
| Fine-tune OpenAI | fine-tuning-openai-basics.md → fine-tuning-openai-production.md |
| Fine-tune LoRA | lora-qlora.md → finetuning-basics.md |
| Cost optimization | llm-cost-basics.md → cost-reduction-strategies.md |
| Evaluation | evaluation-metrics.md → evaluation-framework.md |
| Observability | llm-observability.md → llm-observability-stack-2026.md |

## Methodologies (15)

**Fine-tuning (5):**
- finetuning-basics: Fundamentals, when to fine-tune
- finetuning-datasets: Data preparation, quality
- fine-tuning-openai-basics: OpenAI API fine-tuning
- fine-tuning-openai-production: Production deployment
- lora-qlora: Efficient fine-tuning, parameter selection

**Evaluation (3):**
- evaluation-metrics: Accuracy, F1, perplexity, task metrics
- evaluation-framework: LLM-as-judge, human eval
- evaluation-benchmarks: MMLU, HumanEval, industry benchmarks

**Cost Optimization (2):**
- llm-cost-basics: Token counting, pricing models
- cost-reduction-strategies: Caching, compression, batching

**Observability (5):**
- llm-observability: Fundamentals, why monitor
- llm-observability-stack: Tools selection
- llm-observability-stack-2026: Latest tools (LangSmith, Langfuse)
- llm-management-observability: End-to-end management

## Code Examples

### OpenAI Fine-tuning

```python
from openai import OpenAI

client = OpenAI()

# Upload training data
file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={"n_epochs": 3}
)

# Monitor
while True:
    job = client.fine_tuning.jobs.retrieve(job.id)
    if job.status == "succeeded":
        break
```

### LoRA Fine-tuning

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3-8b")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none"
)

model = get_peft_model(model, lora_config)
```

### Cost Tracking

```python
import tiktoken

def count_tokens(text, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(prompt, completion, model="gpt-4o"):
    prompt_tokens = count_tokens(prompt, model)
    completion_tokens = count_tokens(completion, model)

    # GPT-4o pricing
    prompt_cost = prompt_tokens * 0.000005
    completion_cost = completion_tokens * 0.000015

    return prompt_cost + completion_cost
```

### LLM Observability with LangSmith

```python
from langsmith import traceable

@traceable
def rag_pipeline(query: str) -> str:
    # Retrieval
    docs = retrieve(query)

    # Generation
    response = generate(query, docs)

    return response
```

## Fine-tuning Decision Matrix

| Scenario | Approach |
|----------|----------|
| Small dataset (<100 examples) | Few-shot prompting |
| Medium dataset (100-1000) | OpenAI fine-tuning |
| Large dataset (>1000) | LoRA/QLoRA |
| Custom behavior | Fine-tuning |
| New knowledge | RAG (not fine-tuning) |

## Cost Reduction Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Prompt caching | 90% on cached | Cold start cost |
| Batch API | 50% | 24h latency |
| Smaller models | 80%+ | Lower quality |
| Context pruning | Variable | May lose context |
| Output limits | Variable | Truncated responses |

## Evaluation Frameworks

| Framework | Use Case |
|-----------|----------|
| **LangSmith** | Production monitoring, traces |
| **Langfuse** | Open-source observability |
| **PromptLayer** | Prompt versioning |
| **Weights & Biases** | Experiment tracking |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-llm-integration | Provides APIs to optimize |
| faion-rag-engineer | RAG evaluation |
| faion-devops-engineer | Model deployment |

---

*ML Ops v1.0 | 15 methodologies*
