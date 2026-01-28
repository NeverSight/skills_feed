---
name: llm-fine-tuning-guide
description: Master fine-tuning of large language models for specific domains and tasks. Covers data preparation, training techniques, optimization strategies, and evaluation methods. Use when adapting models for specialized applications, reducing inference costs, or improving domain-specific performance.
---

# LLM Fine-Tuning Guide

Master the art of fine-tuning large language models to create specialized models optimized for your specific use cases, domains, and performance requirements.

## Overview

Fine-tuning adapts pre-trained LLMs to specific tasks, domains, or styles by training them on curated datasets. This improves accuracy, reduces hallucinations, and optimizes costs.

### When to Fine-Tune

- **Domain Specialization**: Legal documents, medical records, financial reports
- **Task-Specific Performance**: Better results on specific tasks than base model
- **Cost Optimization**: Smaller fine-tuned model replaces expensive large model
- **Style Adaptation**: Match specific writing styles or tones
- **Compliance Requirements**: Keep sensitive data within your infrastructure
- **Latency Requirements**: Smaller models deploy faster

### When NOT to Fine-Tune

- One-off queries (use prompting instead)
- Rapidly changing information (use RAG instead)
- Limited training data (< 100 examples typically insufficient)
- General knowledge questions (base model sufficient)

## Quick Start

**Full Fine-Tuning**:
```bash
python examples/full_fine_tuning.py
```

**LoRA (Recommended for most cases)**:
```bash
python examples/lora_fine_tuning.py
```

**QLoRA (Single GPU)**:
```bash
python examples/qlora_fine_tuning.py
```

**Data Preparation**:
```bash
python scripts/data_preparation.py
```

## Fine-Tuning Approaches

### 1. Full Fine-Tuning

Update all model parameters during training.

**Pros**:
- Maximum performance improvement
- Can completely rewrite model behavior
- Best for significant domain shifts

**Cons**:
- High computational cost
- Requires large dataset (1000+ examples)
- Risk of catastrophic forgetting
- Long training time

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

model_id = "meta-llama/Llama-2-7b"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

training_args = TrainingArguments(
    output_dir="./fine-tuned-llama",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_steps=10,
    save_steps=100,
    eval_strategy="steps",
    eval_steps=50,
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

### 2. Parameter-Efficient Fine-Tuning (PEFT)

Train only a small fraction of parameters.

#### LoRA (Low-Rank Adaptation)

Adds trainable low-rank matrices to existing weights.

**Pros**:
- 99% fewer trainable parameters
- Maintains base model knowledge
- Fast training (10-20x faster)
- Easy to switch between adapters

**Cons**:
- Slightly lower performance than full fine-tuning
- Requires base model at inference

```python
from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model_id = "meta-llama/Llama-2-7b"
model = AutoModelForCausalLM.from_pretrained(base_model_id)
tokenizer = AutoTokenizer.from_pretrained(base_model_id)

# Configure LoRA
lora_config = LoraConfig(
    r=8,  # Rank of low-rank matrices
    lora_alpha=16,  # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Wrap model with LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,738,415,616 || trainable%: 0.06

# Train as normal
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()

# Save only LoRA weights
model.save_pretrained("./llama-lora-adapter")
```

#### QLoRA (Quantized LoRA)

Combines LoRA with quantization for extreme efficiency.

```python
from peft import prepare_model_for_kbit_training, get_peft_model, LoraConfig
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# Quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for training
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)

# Train on single GPU
trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./qlora-output",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=5e-4,
        num_train_epochs=3,
    ),
    train_dataset=train_dataset,
)
trainer.train()
```

#### Prefix Tuning

Prepends trainable tokens to input.

```python
from peft import get_peft_model, PrefixTuningConfig

config = PrefixTuningConfig(
    num_virtual_tokens=20,
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, config)
# Only 20 * embedding_dim parameters trained
```

### 3. Instruction Fine-Tuning

Train model to follow instructions with examples.

```python
# Training data format
training_data = [
    {
        "instruction": "Translate to French",
        "input": "Hello, how are you?",
        "output": "Bonjour, comment allez-vous?"
    },
    {
        "instruction": "Summarize this text",
        "input": "Long document...",
        "output": "Summary..."
    }
]

# Template for training
template = """Below is an instruction that describes a task, paired with an input that provides further context.

### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}"""

# Create formatted dataset
formatted_data = [
    template.format(**example) for example in training_data
]
```

### 4. Domain-Specific Fine-Tuning

Tailor models for specific industries or fields.

#### Legal Domain Example

```python
legal_training_data = [
    {
        "prompt": "What are the key clauses in an NDA?",
        "completion": """Key clauses typically include:
1. Definition of Confidential Information
2. Non-Disclosure Obligations
3. Permitted Disclosures
4. Term and Termination
5. Return of Information
6. Remedies"""
    },
    # ... more legal examples
]

# Train on legal domain
model = fine_tune_on_domain(
    base_model="gpt-3.5-turbo",
    training_data=legal_training_data,
    epochs=3,
    learning_rate=0.0002,
)
```

## Data Preparation

### 1. Dataset Quality

```python
class DatasetValidator:
    def validate_dataset(self, data):
        issues = {
            "empty_samples": 0,
            "duplicates": 0,
            "outliers": 0,
            "imbalance": {}
        }

        # Check for empty samples
        for sample in data:
            if not sample.get("text"):
                issues["empty_samples"] += 1

        # Check for duplicates
        texts = [s.get("text") for s in data]
        issues["duplicates"] = len(texts) - len(set(texts))

        # Check for length outliers
        lengths = [len(t.split()) for t in texts]
        mean_length = sum(lengths) / len(lengths)
        issues["outliers"] = sum(1 for l in lengths if l > mean_length * 3)

        return issues

# Validate before training
validator = DatasetValidator()
issues = validator.validate_dataset(training_data)
print(f"Dataset Issues: {issues}")
```

### 2. Data Augmentation

```python
from nlpaug.augmenter.word import SynonymAug, RandomWordAug
import nlpaug.flow as naf

# Create augmentation pipeline
text = "The quick brown fox jumps over the lazy dog"

# Synonym replacement
aug_syn = SynonymAug(aug_p=0.3)
augmented_syn = aug_syn.augment(text)

# Random word insertion
aug_insert = RandomWordAug(action="insert", aug_p=0.3)
augmented_insert = aug_insert.augment(text)

# Combine augmentations
flow = naf.Sequential([
    SynonymAug(aug_p=0.2),
    RandomWordAug(action="swap", aug_p=0.2)
])
augmented = flow.augment(text)
```

### 3. Train/Validation Split

```python
from sklearn.model_selection import train_test_split

# Create splits
train_data, eval_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

eval_data, test_data = train_test_split(
    eval_data,
    test_size=0.5,
    random_state=42
)

print(f"Train: {len(train_data)}, Eval: {len(eval_data)}, Test: {len(test_data)}")
```

## Training Techniques

### 1. Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR

# Linear warmup + cosine annealing
def get_scheduler(optimizer, num_steps):
    lr_scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=500,
        num_training_steps=num_steps
    )
    return lr_scheduler

training_args = TrainingArguments(
    learning_rate=1e-4,
    lr_scheduler_type="cosine",
    warmup_steps=500,
    warmup_ratio=0.1,
)
```

### 2. Gradient Accumulation

```python
training_args = TrainingArguments(
    gradient_accumulation_steps=4,  # Accumulate gradients over 4 steps
    per_device_train_batch_size=1,   # Effective batch size: 1 * 4 = 4
)

# Simulates larger batch on limited GPU memory
```

### 3. Mixed Precision Training

```python
training_args = TrainingArguments(
    fp16=True,  # Use 16-bit floats
    bf16=False,
)

# Reduces memory usage by 50%, speeds up training
```

### 4. Multi-GPU Training

```python
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=4,
    dataloader_pin_memory=True,
    dataloader_num_workers=4,
)

# Automatically uses all available GPUs
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)
```

## Popular Models for Fine-Tuning

### Open Source Models

#### Llama 3.2 (Meta)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-7b")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-7b")

# Fine-tune on custom data
# ... training code
```

**Characteristics**:
- 7B, 70B parameter versions
- Strong instruction-following
- Excellent for domain adaptation
- Apache 2.0 license

#### Gemma 3 (Google)

```python
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-2b")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-2b")

# Gemma 3 sizes: 2B, 7B, 27B
# Very efficient, great for fine-tuning
```

**Characteristics**:
- Small, medium, large sizes
- Efficient architecture
- Good for edge deployment
- Built on cutting-edge research

#### Mistral 7B

```python
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

# Strong performance, efficient architecture
```

**Characteristics**:
- Sliding window attention
- Efficient inference
- Strong performance-to-size ratio

### Commercial Models

#### OpenAI Fine-Tuning API

```python
import openai

# Prepare training data
training_file = openai.File.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Create fine-tuning job
fine_tune_job = openai.FineTuningJob.create(
    training_file=training_file.id,
    model="gpt-3.5-turbo",
    hyperparameters={
        "n_epochs": 3,
        "learning_rate_multiplier": 0.1,
    }
)

# Wait for completion
fine_tuned_model = openai.FineTuningJob.retrieve(fine_tune_job.id)
print(f"Status: {fine_tuned_model.status}")

# Use fine-tuned model
response = openai.ChatCompletion.create(
    model=fine_tuned_model.fine_tuned_model,
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Evaluation and Metrics

### 1. Perplexity

```python
import torch
from math import exp

def calculate_perplexity(model, eval_dataset):
    model.eval()
    total_loss = 0
    total_tokens = 0

    with torch.no_grad():
        for batch in eval_dataset:
            outputs = model(**batch)
            loss = outputs.loss
            total_loss += loss.item() * batch["input_ids"].shape[0]
            total_tokens += batch["input_ids"].shape[0]

    perplexity = exp(total_loss / total_tokens)
    return perplexity

perplexity = calculate_perplexity(model, eval_dataset)
print(f"Perplexity: {perplexity:.2f}")
```

### 2. Task-Specific Metrics

```python
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

def evaluate_task(predictions, ground_truth):
    return {
        "accuracy": accuracy_score(ground_truth, predictions),
        "precision": precision_score(ground_truth, predictions, average='weighted'),
        "recall": recall_score(ground_truth, predictions, average='weighted'),
        "f1": f1_score(ground_truth, predictions, average='weighted'),
    }

# Evaluate on task
predictions = [model.predict(x) for x in test_data]
metrics = evaluate_task(predictions, test_labels)
print(f"Metrics: {metrics}")
```

### 3. Human Evaluation

```python
class HumanEvaluator:
    def evaluate_response(self, prompt, response):
        criteria = {
            "relevance": self._score_relevance(prompt, response),
            "coherence": self._score_coherence(response),
            "factuality": self._score_factuality(response),
            "helpfulness": self._score_helpfulness(response),
        }
        return sum(criteria.values()) / len(criteria)

    def _score_relevance(self, prompt, response):
        # Score 1-5
        pass

    def _score_coherence(self, response):
        # Score 1-5
        pass
```

## Common Challenges & Solutions

### Challenge: Catastrophic Forgetting

Model forgets pre-trained knowledge while adapting to new domain.

**Solutions**:
- Use lower learning rates (2e-5 to 5e-5)
- Smaller training epochs (1-3)
- Regularization techniques
- Continual learning approaches

```python
# Conservative training settings
training_args = TrainingArguments(
    learning_rate=2e-5,  # Lower learning rate
    num_train_epochs=2,   # Few epochs
    weight_decay=0.01,    # L2 regularization
    warmup_steps=500,
    save_total_limit=3,
    load_best_model_at_end=True,
)
```

### Challenge: Overfitting

Model performs well on training data but poorly on new data.

**Solutions**:
- Use more training data
- Implement dropout
- Early stopping
- Validation monitoring

```python
training_args = TrainingArguments(
    eval_strategy="steps",
    eval_steps=50,
    load_best_model_at_end=True,
    early_stopping_patience=3,
    metric_for_best_model="eval_loss",
)
```

### Challenge: Insufficient Training Data

Few examples for fine-tuning.

**Solutions**:
- Data augmentation
- Use PEFT (LoRA) instead of full fine-tuning
- Few-shot learning with prompting
- Transfer learning

```python
# Use LoRA when data is limited
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
)
```

## Best Practices

### Before Fine-Tuning
- ✓ Start with a strong base model
- ✓ Prepare high-quality training data (100+ examples recommended)
- ✓ Define clear evaluation metrics
- ✓ Set up proper train/validation splits
- ✓ Document your objectives

### During Fine-Tuning
- ✓ Monitor training/validation loss
- ✓ Use appropriate learning rates
- ✓ Save checkpoints regularly
- ✓ Validate on held-out data
- ✓ Watch for overfitting/underfitting

### After Fine-Tuning
- ✓ Evaluate on test set
- ✓ Compare against baseline
- ✓ Perform qualitative analysis
- ✓ Document configuration and results
- ✓ Version your fine-tuned models

## Implementation Checklist

- [ ] Determine fine-tuning approach (full, LoRA, QLoRA, instruction)
- [ ] Prepare and validate training dataset (100+ examples)
- [ ] Choose base model (Llama 3.2, Gemma 3, Mistral, etc.)
- [ ] Set up PEFT if using parameter-efficient methods
- [ ] Configure training arguments and hyperparameters
- [ ] Implement data loading and preprocessing
- [ ] Set up evaluation metrics
- [ ] Train model with monitoring
- [ ] Evaluate on test set
- [ ] Save and version fine-tuned model
- [ ] Test in production environment
- [ ] Document process and results

## Resources

### Frameworks
- **Hugging Face Transformers**: https://huggingface.co/transformers/
- **PEFT (Parameter-Efficient Fine-Tuning)**: https://github.com/huggingface/peft
- **Hugging Face Datasets**: https://huggingface.co/datasets

### Models
- **Llama 3.2**: https://www.meta.com/llama/
- **Gemma 3**: https://deepmind.google/technologies/gemma/
- **Mistral**: https://mistral.ai/

### Papers
- "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al.)
- "QLoRA: Efficient Finetuning of Quantized LLMs" (Dettmers et al.)

