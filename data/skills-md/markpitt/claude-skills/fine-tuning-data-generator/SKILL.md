---
name: fine-tuning-data-generator
description: Generates comprehensive synthetic fine-tuning datasets in ChatML format (JSONL) for use with Unsloth, Axolotl, and similar training frameworks. Gathers requirements, creates datasets with diverse examples, validates quality, and provides framework integration guidance.
version: 2.0
allowed-tools: Read, Write, Edit, Bash
---

# Fine-Tuning Data Generator

This skill generates high-quality synthetic training data in ChatML format for fine-tuning language models using frameworks like Unsloth, Axolotl, or similar tools.

## What Do I Need?

| Need | Resource |
|------|----------|
| **Planning my dataset** - requirements, strategy, quality checklist | [`resources/dataset-strategy.md`](resources/dataset-strategy.md) |
| **How to create diverse examples** - variation techniques, multi-turn patterns, format-specific guidance | [`resources/generation-techniques.md`](resources/generation-techniques.md) |
| **ChatML format details** - structure, specification, common issues, framework compatibility | [`resources/chatml-format.md`](resources/chatml-format.md) |
| **Example datasets** - inspiration across domains, multi-turn samples, edge cases | [`resources/examples.md`](resources/examples.md) |
| **Validating quality** - validation workflow, analyzing datasets, troubleshooting | [`resources/quality-validation.md`](resources/quality-validation.md) |
| **Training & deployment** - framework setup, hyperparameters, optimization, deployment | [`resources/framework-integration.md`](resources/framework-integration.md) |

## Workflow

### Phase 1: Gather Requirements

Start with these essential clarifying questions:

**Task Definition:**
- What is the model being trained to do? (e.g., customer support, code generation, creative writing)
- What specific domain or subject matter? (e.g., legal, medical, e-commerce, software development)
- How many training examples are needed? (Recommend: 100+ for simple tasks, 500-1000+ for complex)

**Quality & Diversity:**
- Complexity range: simple to complex mix, or focus on specific difficulty level?
- Diversity: edge cases, error handling, unusual scenarios?
- Tone/style: professional, friendly, technical, concise, detailed?
- Response length preferences?
- Any specific formats: code blocks, lists, tables, JSON?

**Dataset Composition:**
- Distribution across subtopics: evenly distributed or weighted?
- Include negative examples (what NOT to do)?
- Need validation split? (Recommend 10-20% of total)

See [`resources/dataset-strategy.md`](resources/dataset-strategy.md) for detailed question templates.

### Phase 2: Create Generation Plan

Present a plan covering:
- Number and distribution of examples across categories
- Key topics/scenarios to cover
- Diversity strategies (phrasing variations, complexity levels, edge cases)
- System prompt approach (consistent vs. varied)
- Quality assurance approach

**Get user approval before generating.**

### Phase 3: Generate Synthetic Data

Create examples following these quality standards:

**Key Principles:**
- Realistic scenarios reflecting real-world use cases
- Natural language with varied phrasing and formality levels
- Accurate, helpful responses aligned with desired behavior
- Consistent ChatML formatting throughout
- Balanced difficulty (unless specified)
- Meaningful variety (no repetition)
- Include edge cases and error scenarios

**Diversity Techniques:**
- Vary query phrasing (questions, commands, statements)
- Include different expertise levels (beginner, intermediate, expert)
- Cover both positive and negative examples
- Mix short and long-form responses
- Include multi-step reasoning when appropriate
- Add context variations

See [`resources/generation-techniques.md`](resources/generation-techniques.md) for detailed techniques, domain-specific guidance, and batch generation workflow.

### Phase 4: Validate & Document

Run validation tools and checks:

```bash
# Validate JSON formatting and structure
python scripts/validate_chatml.py training_data.jsonl

# Analyze dataset statistics and diversity
python scripts/analyze_dataset.py training_data.jsonl

# Export statistics
python scripts/analyze_dataset.py training_data.jsonl --export stats.json
```

**Quality Checklist:**
- [ ] JSON validation passed (no errors)
- [ ] Analysis shows good diversity metrics
- [ ] Manual sample review passed
- [ ] No duplicate or near-duplicate examples
- [ ] All required fields present
- [ ] Realistic user queries
- [ ] Accurate, helpful responses
- [ ] Balanced category distribution
- [ ] Dataset metadata documented

See [`resources/quality-validation.md`](resources/quality-validation.md) for validation details, troubleshooting, and documentation templates.

### Phase 5: Integration & Training

Prepare for training with your framework of choice:

**Output Files:**
- `training_data.jsonl` - Main training set
- `validation_data.jsonl` - Optional validation set
- `dataset_info.txt` - Metadata and statistics

**Framework Setup:**
- Unsloth: Automatic ChatML detection, efficient 4-bit training
- Axolotl: Specify `type: chat_template` and `chat_template: chatml`
- Hugging Face: Use tokenizer's `apply_chat_template()` method
- Custom: Load from JSONL, handle ChatML formatting

See [`resources/framework-integration.md`](resources/framework-integration.md) for setup code, hyperparameters, deployment options, and best practices.

## ChatML Format Overview

Each training example is a JSON object with a `messages` array:

```json
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "How do I reverse a string in Python?"}, {"role": "assistant", "content": "Use slicing: `text[::-1]`"}]}
```

**Roles:**
- `system`: Sets assistant behavior (optional but recommended)
- `user`: User's input/query
- `assistant`: Model's expected response

**Multi-turn:** Add additional user/assistant message pairs for conversations.

See [`resources/chatml-format.md`](resources/chatml-format.md) for detailed specification, validation, common issues, and framework-specific notes.

## Tool Reference

### Scripts in `scripts/`

#### validate_chatml.py
Validates ChatML format JSONL files:
```bash
python scripts/validate_chatml.py training_data.jsonl
python scripts/validate_chatml.py training_data.jsonl --verbose
```

**Checks:**
- Valid JSON formatting
- Required fields (messages, role, content)
- Valid role values (system, user, assistant)
- Proper message order
- Duplicate detection
- Diversity metrics

#### analyze_dataset.py
Provides comprehensive statistics and analysis:
```bash
python scripts/analyze_dataset.py training_data.jsonl
python scripts/analyze_dataset.py training_data.jsonl --export stats.json
```

**Provides:**
- Dataset overview (total examples, message counts)
- Message length statistics
- System prompt variations
- User query patterns (questions, commands, code-related, length categories)
- Assistant response patterns (code blocks, lists, headers, length categories)
- Quality indicators (diversity score, balance ratio)
- Token estimates and cost projection

## Common Workflows

### Small Dataset (100-200 examples)
1. Gather requirements
2. Create generation plan for 1-2 categories
3. Generate in single batch, review quality
4. Validate and document
5. Ready for training

### Medium Dataset (500-1000 examples)
1. Gather requirements
2. Create detailed plan with multiple categories
3. Generate in 2-3 batches, reviewing after each
4. Analyze diversity and adjust approach
5. Fill any gaps
6. Final validation and documentation

### Large Dataset (2000+ examples)
1. Gather comprehensive requirements
2. Create multi-batch generation plan
3. Batch 1 (50-100): Foundation examples
4. Batch 2 (100-200): Complexity expansion
5. Batch 3 (100-200): Coverage filling
6. Batch 4 (50-100): Polish and validation
7. Run full validation suite
8. Generate comprehensive documentation

## Best Practices

### Start Small, Iterate
1. Generate 10-20 examples first
2. Review and get feedback
3. Refine approach based on feedback
4. Scale up to full dataset

### Quality Over Quantity
- Better to have 500 diverse, high-quality examples than 5,000 repetitive ones
- Each example should teach something new
- Maintain consistent response quality throughout

### Diversify Systematically
- Vary query phrasing (questions, commands, statements)
- Cover different expertise levels
- Mix response complexities
- Include edge cases (typically 20-30% of dataset)
- Use batch generation workflow for large datasets

### Test Before Deployment
- Test dataset with actual training framework
- Monitor training metrics for issues
- Test fine-tuned model outputs before deployment
- Compare results to base model

### Document Everything
- Keep notes on generation parameters
- Save different dataset versions
- Document any modifications made
- Record generation strategies used
- Track model performance metrics

## Advanced Features

### Batch Generation Strategy

For datasets 500+ examples:
- Generate 50-100 examples at a time
- Review distribution and diversity after each batch
- Adjust generation strategy based on identified gaps
- Prevents repetition and maintains creativity

### Common Pitfalls to Avoid

- **Over-templating**: Creates repetitive patterns (vary naturally)
- **Unrealistic Queries**: Overly formal/robotic user inputs (use varied phrasing)
- **Narrow Coverage**: Limited scenarios and phrasing (ensure diversity)
- **Inconsistent Quality**: Quality degradation over time (use quality checklist)
- **JSON Errors**: Invalid formatting breaking training (always validate)
- **Missing Context**: System prompts without detail (provide clear instructions)
- **Response Mismatch**: Responses don't address queries (verify relevance)

## Dataset Size Recommendations

| Task Complexity | Recommended Size | Notes |
|---|---|---|
| Simple tasks | 100-500 | Well-defined, limited variation |
| Medium tasks | 500-2,000 | Multiple scenarios, moderate complexity |
| Complex tasks | 2,000-10,000+ | Many edge cases, high variability |
| Domain adaptation | 1,000-5,000 | Specialized knowledge required |

## Resources

- **Planning & Strategy**: [`resources/dataset-strategy.md`](resources/dataset-strategy.md) - Requirements gathering, planning, quality checklists
- **Generation Techniques**: [`resources/generation-techniques.md`](resources/generation-techniques.md) - Diversity techniques, domain-specific guidance, batch workflows
- **ChatML Specification**: [`resources/chatml-format.md`](resources/chatml-format.md) - Format details, validation, framework notes
- **Example Datasets**: [`resources/examples.md`](resources/examples.md) - Diverse domain examples, multi-turn patterns
- **Quality Validation**: [`resources/quality-validation.md`](resources/quality-validation.md) - Validation workflow, analysis, troubleshooting
- **Framework Integration**: [`resources/framework-integration.md`](resources/framework-integration.md) - Setup for Unsloth, Axolotl, HuggingFace; deployment options

---

**Version**: 2.0 | **Updated**: 2024 | **Pattern**: Modular Orchestration
