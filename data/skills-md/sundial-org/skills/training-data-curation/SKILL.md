---
name: training-data-curation
description: Guidelines for creating high-quality datasets for LLM post-training (SFT/DPO/RLHF). Use when preparing data for fine-tuning, evaluating data quality, or designing data collection strategies.
---

# Training Data Curation Guidelines

Best practices for gathering and preparing training data for LLM fine-tuning.

## Data Quality Principles

**Quality over quantity.** Llama 2 used only 27,540 high-quality SFT examples and outperformed models trained on larger noisy datasets [[1]](#references). Focus on clean, diverse, well-formatted data.

**Garbage in, garbage out.** The model will learn patterns from your data—including errors, biases, and formatting issues. Inspect samples manually before training.

**Match the target distribution.** Training data should reflect the tasks and style you want the model to perform. If you want formal responses, don't train on casual chat data.

## Format Requirements

### Supervised Fine-Tuning (SFT)

Use the **messages format** (OpenAI/Anthropic/Tinker standard) [[5]](#references):

```
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

- Each sample is a complete conversation
- Multi-turn: alternate user/assistant messages
- System prompts optional: `{"role": "system", "content": "..."}`
- JSONL format, one sample per line

### Preference Learning (DPO/ORPO/KTO)

Requires **paired comparisons** [[2]](#references):

```
{"prompt": "...", "chosen": "...", "rejected": "..."}
```

- `chosen` and `rejected` must respond to the same prompt
- Quality difference should be clear and consistent
- Annotator agreement >70% indicates usable samples [[1]](#references)

For KTO, pairs aren't required—just binary labels on completions [[7]](#references):
```
{"prompt": "...", "completion": "...", "label": true/false}
```

### Reward Modeling (RLHF)

Needs **ranked responses** [[1]](#references):

```
{"prompt": "...", "responses": ["best", "second", "worst"]}
```

## Quality Checklist

Before training, verify:

- [ ] **No duplicates** — exact and near-duplicate removal [[3]](#references)
- [ ] **No empty fields** — all required fields populated
- [ ] **Consistent format** — schema matches throughout
- [ ] **Appropriate length** — not too short (noise) or too long (truncation)
- [ ] **Clean text** — proper encoding, no HTML/boilerplate artifacts [[8]](#references)
- [ ] **Manual inspection** — reviewed random sample of 50-100 examples
- [ ] **No PII/sensitive data** — unless intentionally included
- [ ] **License verified** — legal to use for training

## Common Quality Issues

| Issue | Detection | Fix | Source |
|-------|-----------|-----|--------|
| Duplicates | Hash-based dedup | Remove exact matches, MinHash for near-dupes | [[3]](#references) |
| Boilerplate | Keyword filter | Remove "subscribe", "cookie policy", etc. | [[8]](#references) |
| Repetitive text | N-gram analysis | Flag if <30% unique trigrams | [[4]](#references) |
| Low-quality text | Alpha ratio | Remove if <50% alphabetic characters | [[8]](#references) |
| Wrong language | Language detection | fastText classifier, filter to target | [[3]](#references) |
| Too short | Length check | Minimum 3-5 sentences, 100+ words for documents | [[8]](#references) |

## Data Sources

**High quality:**
- Curated human annotations [[1]](#references)
- Expert-written examples
- Filtered high-quality web data [[3]](#references)

**Medium quality:**
- Synthetic data from stronger models (distillation)
- Community Q&A with voting signals
- Filtered user-generated content

**Use with caution:**
- Raw web scrapes
- Unfiltered synthetic data
- Data without clear provenance [[6]](#references)

## Sizing Guidelines

| Dataset Size | Use Case | Source |
|--------------|----------|--------|
| 100-1K | Quick experiments, specific behaviors | — |
| 1K-10K | Production SFT, domain adaptation | — |
| 10K-100K | Comprehensive instruction tuning | [[1]](#references) |
| 1M+ preference pairs | Large-scale RLHF | [[1]](#references) |

Llama 2 used ~27K SFT examples and 1M+ preference comparisons [[1]](#references).

## File Format

- **JSONL** — one JSON object per line, human-readable
- **Parquet** — efficient for large datasets, built-in compression [[3]](#references)
- **Sharding** — split files >500MB into chunks

## References

1. [Llama 2 Paper](https://arxiv.org/abs/2307.09288) — Touvron et al. (2023). SFT/RLHF data quality practices, 27K SFT examples, >70% annotator agreement threshold
2. [TRL Library](https://huggingface.co/docs/trl/) — HuggingFace trainer implementations for SFT, DPO, KTO, ORPO
3. [FineWeb Paper](https://arxiv.org/abs/2406.17557) — Penedo et al. (2024). Large-scale filtering: MinHash dedup, language detection, quality classifiers
4. [Data-Juicer](https://github.com/alibaba/data-juicer) — Alibaba's quality filtering toolkit with repetition filters, n-gram analysis
5. [Tinker API](https://tinker-docs.thinkingmachines.ai/) — Training API using messages format for SFT, DPO/RLHF support
6. [Data Provenance Initiative](https://arxiv.org/abs/2310.16787) — Longpre et al. (2023). Dataset licensing and attribution audit
7. [KTO Paper](https://arxiv.org/abs/2402.01306) — Ethayarajh et al. (2024). Binary preference learning without pairs
8. [C4/T5 Paper](https://arxiv.org/abs/1910.10683) — Raffel et al. (2020). Foundational filtering: terminal punctuation, min sentences, alpha ratio, boilerplate removal
