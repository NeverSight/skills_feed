---
name: transformers
description: Use when "HuggingFace Transformers", "pre-trained models", "pipeline API", or asking about "text generation", "text classification", "question answering", "NER", "fine-tuning transformers", "AutoModel", "Trainer API"
version: 1.0.0
---

# HuggingFace Transformers

Access thousands of pre-trained models for NLP, vision, audio, and multimodal tasks.

## When to Use

- Quick inference with pipelines
- Text generation, classification, QA, NER
- Image classification, object detection
- Fine-tuning on custom datasets
- Loading pre-trained models from HuggingFace Hub

---

## Pipeline Tasks

### NLP Tasks

| Task | Pipeline Name | Output |
|------|---------------|--------|
| **Text Generation** | `text-generation` | Completed text |
| **Classification** | `text-classification` | Label + confidence |
| **Question Answering** | `question-answering` | Answer span |
| **Summarization** | `summarization` | Shorter text |
| **Translation** | `translation_en_to_fr` | Translated text |
| **NER** | `ner` | Entity spans + types |
| **Fill Mask** | `fill-mask` | Predicted tokens |

### Vision Tasks

| Task | Pipeline Name | Output |
|------|---------------|--------|
| **Image Classification** | `image-classification` | Label + confidence |
| **Object Detection** | `object-detection` | Bounding boxes |
| **Image Segmentation** | `image-segmentation` | Pixel masks |

### Audio Tasks

| Task | Pipeline Name | Output |
|------|---------------|--------|
| **Speech Recognition** | `automatic-speech-recognition` | Transcribed text |
| **Audio Classification** | `audio-classification` | Label + confidence |

---

## Model Loading Patterns

### Auto Classes

| Class | Use Case |
|-------|----------|
| **AutoModel** | Base model (embeddings) |
| **AutoModelForCausalLM** | Text generation (GPT-style) |
| **AutoModelForSeq2SeqLM** | Encoder-decoder (T5, BART) |
| **AutoModelForSequenceClassification** | Classification head |
| **AutoModelForTokenClassification** | NER, POS tagging |
| **AutoModelForQuestionAnswering** | Extractive QA |

**Key concept**: Always use Auto classes unless you need a specific architecture—they handle model detection automatically.

---

## Generation Parameters

| Parameter | Effect | Typical Values |
|-----------|--------|----------------|
| **max_new_tokens** | Output length | 50-500 |
| **temperature** | Randomness (0=deterministic) | 0.1-1.0 |
| **top_p** | Nucleus sampling threshold | 0.9-0.95 |
| **top_k** | Limit vocabulary per step | 50 |
| **num_beams** | Beam search (disable sampling) | 4-8 |
| **repetition_penalty** | Discourage repetition | 1.1-1.3 |

**Key concept**: Higher temperature = more creative but less coherent. For factual tasks, use low temperature (0.1-0.3).

---

## Memory Management

### Device Placement Options

| Option | When to Use |
|--------|-------------|
| **device_map="auto"** | Let library decide GPU allocation |
| **device_map="cuda:0"** | Specific GPU |
| **device_map="cpu"** | CPU only |

### Quantization Options

| Method | Memory Reduction | Quality Impact |
|--------|------------------|----------------|
| **8-bit** | ~50% | Minimal |
| **4-bit** | ~75% | Small for most tasks |
| **GPTQ** | ~75% | Requires calibration |
| **AWQ** | ~75% | Activation-aware |

**Key concept**: Use `torch_dtype="auto"` to automatically use the model's native precision (often bfloat16).

---

## Fine-Tuning Concepts

### Trainer Arguments

| Argument | Purpose | Typical Value |
|----------|---------|---------------|
| **num_train_epochs** | Training passes | 3-5 |
| **per_device_train_batch_size** | Samples per GPU | 8-32 |
| **learning_rate** | Step size | 2e-5 for fine-tuning |
| **weight_decay** | Regularization | 0.01 |
| **warmup_ratio** | LR warmup | 0.1 |
| **evaluation_strategy** | When to eval | "epoch" or "steps" |

### Fine-Tuning Strategies

| Strategy | Memory | Quality | Use Case |
|----------|--------|---------|----------|
| **Full fine-tuning** | High | Best | Small models, enough data |
| **LoRA** | Low | Good | Large models, limited GPU |
| **QLoRA** | Very Low | Good | 7B+ models on consumer GPU |
| **Prefix tuning** | Low | Moderate | When you can't modify weights |

---

## Tokenization Concepts

| Parameter | Purpose |
|-----------|---------|
| **padding** | Make sequences same length |
| **truncation** | Cut sequences to max_length |
| **max_length** | Maximum tokens (model-specific) |
| **return_tensors** | Output format ("pt", "tf", "np") |

**Key concept**: Always use the tokenizer that matches the model—different models use different vocabularies.

---

## Best Practices

| Practice | Why |
|----------|-----|
| Use pipelines for inference | Handles preprocessing automatically |
| Use device_map="auto" | Optimal GPU memory distribution |
| Batch inputs | Better throughput |
| Use quantization for large models | Run 7B+ on consumer GPUs |
| Match tokenizer to model | Vocabularies differ between models |
| Use Trainer for fine-tuning | Built-in best practices |

## Resources

- Docs: <https://huggingface.co/docs/transformers>
- Model Hub: <https://huggingface.co/models>
- Course: <https://huggingface.co/course>
