---
name: prompt-engineering
description: Use when "writing prompts", "prompt optimization", "few-shot learning", "chain of thought", or asking about "RAG systems", "agent workflows", "LLM integration", "prompt templates"
version: 1.0.0
---

# Prompt Engineering Guide

Effective prompts, RAG systems, and agent workflows.

## When to Use

- Optimizing LLM prompts
- Building RAG systems
- Designing agent workflows
- Creating few-shot examples
- Structuring chain-of-thought reasoning

---

## Prompt Structure

### Core Components

| Component | Purpose | Include When |
|-----------|---------|--------------|
| **Role/Context** | Set expertise, persona | Complex domain tasks |
| **Task** | Clear instruction | Always |
| **Format** | Output structure | Need structured output |
| **Examples** | Few-shot learning | Pattern demonstration needed |
| **Constraints** | Boundaries, rules | Need to limit scope |

### Prompt Patterns

| Pattern | Use Case | Key Concept |
|---------|----------|-------------|
| **Chain of Thought** | Complex reasoning | "Think step by step" |
| **Few-Shot** | Pattern learning | 2-5 input/output examples |
| **Role Playing** | Domain expertise | "You are an expert X" |
| **Structured Output** | Parsing needed | Specify JSON/format exactly |
| **Self-Consistency** | Improve accuracy | Generate multiple, vote |

---

## Chain of Thought Variants

| Variant | Description | When to Use |
|---------|-------------|-------------|
| **Standard CoT** | "Think step by step" | Math, logic problems |
| **Zero-Shot CoT** | Just add "step by step" | Quick reasoning boost |
| **Structured CoT** | Numbered steps | Complex multi-step |
| **Self-Ask** | Ask sub-questions | Research-style tasks |
| **Tree of Thought** | Explore multiple paths | Creative/open problems |

**Key concept**: CoT works because it forces the model to show intermediate reasoning, reducing errors in the final answer.

---

## Few-Shot Learning

### Example Selection

| Criteria | Why |
|----------|-----|
| **Representative** | Cover common cases |
| **Diverse** | Show range of inputs |
| **Edge cases** | Handle boundaries |
| **Consistent format** | Teach output pattern |

### Number of Examples

| Count | Trade-off |
|-------|-----------|
| 0 (zero-shot) | Less context, more creative |
| 2-3 | Good balance for most tasks |
| 5+ | Complex patterns, use tokens |

**Key concept**: Examples teach format more than content. The model learns "how" to respond, not "what" facts to include.

---

## RAG System Design

### Architecture Flow

Query → Embed → Search → Retrieve → Augment Prompt → Generate

### Chunking Strategies

| Strategy | Best For | Trade-off |
|----------|----------|-----------|
| **Fixed size** | General documents | May split sentences |
| **Sentence-based** | Precise retrieval | Many small chunks |
| **Paragraph-based** | Context preservation | May be too large |
| **Semantic** | Mixed content | More complex |

### Retrieval Quality Factors

| Factor | Impact |
|--------|--------|
| **Chunk size** | Too small = no context, too large = noise |
| **Overlap** | Prevents splitting important content |
| **Metadata filtering** | Narrows search space |
| **Re-ranking** | Improves relevance of top-k |
| **Hybrid search** | Combines keyword + semantic |

**Key concept**: RAG quality depends more on retrieval quality than generation quality. Fix retrieval first.

---

## Agent Patterns

### ReAct Pattern

| Step | Description |
|------|-------------|
| **Thought** | Reason about what to do |
| **Action** | Call a tool |
| **Observation** | Process tool result |
| **Repeat** | Until task complete |

### Tool Design Principles

| Principle | Why |
|-----------|-----|
| **Single purpose** | Clear when to use |
| **Good descriptions** | Model selects correctly |
| **Structured inputs** | Reliable parsing |
| **Informative outputs** | Model understands result |
| **Error messages** | Guide retry attempts |

---

## Prompt Optimization

### Token Efficiency

| Technique | Savings |
|-----------|---------|
| Remove redundant instructions | 10-30% |
| Use abbreviations in examples | 10-20% |
| Compress context with summaries | 50%+ |
| Remove verbose explanations | 20-40% |

### Quality Improvement

| Technique | Effect |
|-----------|--------|
| Add specific examples | Reduces errors |
| Specify output format | Enables parsing |
| Include edge cases | Handles boundaries |
| Add confidence scoring | Calibrates uncertainty |

---

## Common Task Patterns

| Task | Key Prompt Elements |
|------|---------------------|
| **Extraction** | List fields, specify format (JSON), handle missing |
| **Classification** | List categories, one-shot per category, single answer |
| **Summarization** | Specify length, focus areas, format (bullets/prose) |
| **Generation** | Style guide, length, constraints, examples |
| **Q&A** | Context placement, "based only on context" |

---

## Best Practices

| Practice | Why |
|----------|-----|
| Be specific and explicit | Reduces ambiguity |
| Provide clear examples | Shows expected format |
| Specify output format | Enables parsing |
| Test with diverse inputs | Find edge cases |
| Iterate based on failures | Targeted improvement |
| Separate instructions from data | Prevent injection |

## Resources

- Anthropic Prompt Engineering: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering>
- OpenAI Cookbook: <https://cookbook.openai.com/>
