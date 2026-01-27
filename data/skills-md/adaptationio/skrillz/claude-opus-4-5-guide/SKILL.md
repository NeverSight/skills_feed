---
name: claude-opus-4-5-guide
description: Comprehensive guide to Claude Opus 4.5, Anthropic's most intelligent model with effort parameter for reasoning control. Covers model capabilities, benchmarks, effort levels (high/medium/low), hybrid reasoning, and model selection. Use when working with Opus 4.5, optimizing reasoning depth, choosing models, or understanding effort parameter trade-offs.
---

# Claude Opus 4.5 Guide

## Overview

Claude Opus 4.5 represents Anthropic's most capable and intelligent model, released November 24, 2025. It combines state-of-the-art reasoning abilities with a revolutionary "effort parameter" that lets you control the model's reasoning depth and token consumption dynamically.

**Key Positioning**: Opus 4.5 is the best model in the world for complex coding, autonomous agents, computer use automation, and advanced reasoning tasks. It succeeds where previous models required manual intervention and replaces what previously demanded multiple specialized models.

**What Makes Opus 4.5 Different**:

1. **Hybrid Reasoning**: Can instantly answer simple questions or extend thinking for complex problems—automatically adapting without explicit control
2. **Effort Parameter**: Controls token consumption and reasoning depth through simple high/medium/low configuration, independent of model selection
3. **Coding Excellence**: 80.9% SWE-bench accuracy (state-of-the-art), 92.3% MMLU, 83.1% GPQA Diamond—best-in-class performance
4. **Cost Efficiency**: $5/M input tokens, $25/M output tokens—5x cheaper than Opus 4.1 while more capable
5. **Extended Context**: 200K token window supports long conversations, multi-document analysis, and extended agentic workflows
6. **Computer Use**: Advanced automation capabilities including application control and office document processing

Opus 4.5 isn't just an incremental improvement—it's a model tier reduction. Tasks requiring Opus 4.1 now run on Sonnet with Opus 4.5 for complex work. Budget-conscious teams use Opus 4.5's effort parameter instead of maintaining multiple model versions.

## When to Use This Skill

Use claude-opus-4-5-guide when you need to:

- **Choose Claude Model**: Deciding between Opus 4.5, Sonnet 4.5, or Haiku 4.5 for a specific use case
- **Understand Effort Parameter**: Learn how to control reasoning depth with high/medium/low effort levels
- **Optimize Costs**: Understand pricing and effort trade-offs to reduce token consumption without sacrificing quality
- **Implement Opus 4.5**: Get started with model ID, API requirements, and basic examples
- **Benchmark Performance**: Understand Opus 4.5 capabilities through test scores and performance metrics
- **Migrate from Opus 4.1**: Plan upgrade path and understand what's new
- **Configure Reasoning**: Learn hybrid reasoning modes and thinking parameter integration

## Quick Start

### Basic Opus 4.5 Usage

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Explain how quantum computing could solve the traveling salesman problem"
        }
    ]
)

print(response.content[0].text)
```

### Using the Effort Parameter

The effort parameter is an exclusive Opus 4.5 feature that controls reasoning thoroughness:

```python
import anthropic

client = anthropic.Anthropic()

# High effort (default): Maximum capability for complex tasks
response = client.beta.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Design a distributed cache system"}],
    output_config={"effort": "high"},
    betas=["effort-2025-11-24"]
)

# Medium effort: Balanced efficiency for typical tasks
response = client.beta.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarize this meeting transcript"}],
    output_config={"effort": "medium"},
    betas=["effort-2025-11-24"]
)

# Low effort: Quick responses for simple tasks
response = client.beta.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Is this email spam?"}],
    output_config={"effort": "low"},
    betas=["effort-2025-11-24"]
)
```

## Key Features

### Model Specifications

| Specification | Opus 4.5 | Opus 4.1 | Sonnet 4.5 | Haiku 4.5 |
|---|---|---|---|---|
| **Model ID** | `claude-opus-4-5-20251101` | `claude-opus-4-1-20250125` | `claude-sonnet-4-5-20250929` | `claude-haiku-4-5-20251001` |
| **Intelligence** | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ |
| **Speed** | Fast/Instant | Fast | Instant | Instant |
| **Input Cost** | $5/M | $25/M | $3/M | $0.80/M |
| **Output Cost** | $25/M | $125/M | $15/M | $4/M |
| **Context Window** | 200K | 200K | 200K | 200K |
| **Effort Parameter** | ✓ | ✗ | ✗ | ✗ |
| **Knowledge Cutoff** | March 2025 | January 2025 | November 2024 | August 2024 |
| **Best For** | Complex reasoning, coding, agents | Maximum capability (expensive) | Fast, capable tasks | Speed-critical, simple tasks |

### Performance Benchmarks

Opus 4.5 achieves state-of-the-art results across benchmark suites:

| Benchmark | Score | Category | Significance |
|---|---|---|---|
| **SWE-bench** | 80.9% | Code | Autonomous coding—solves real GitHub issues |
| **MMLU** | 92.3% | Knowledge | Broad knowledge across domains |
| **GPQA Diamond** | 83.1% | Reasoning | Graduate-level science questions |
| **HumanEval** | 95%+ | Code | Python function implementation |
| **Coding Contests** | Top 10% | Code | Real programming competitions |

These scores demonstrate Opus 4.5 can handle autonomous coding tasks, complex reasoning, and knowledge-intensive applications previously requiring human expertise.

### Effort Parameter Levels

| Effort | Token Impact | Use Case | Example |
|---|---|---|---|
| **High** | Baseline (default) | Maximum quality needed, cost secondary | Complex system design, difficult debugging |
| **Medium** | ~20-40% reduction | Typical production use, balanced efficiency | General coding, research, most tasks |
| **Low** | ~50-70% reduction | Speed/cost priority, simple tasks | Classification, summarization, lookups |

**Best Practice**: Default to `high` effort, then measure and decrease strategically for known use cases.

### Availability

Opus 4.5 is available on:
- **Claude API** (platform.claude.com)
- **Amazon Bedrock** (AWS)
- **Google Vertex AI** (Google Cloud)
- **Microsoft Azure Foundry** (Microsoft)

## Related Skills

For deeper dives into specific topics:

- **[claude-context-management](../claude-context-management/SKILL.md)**: Manage long conversations and optimize token usage with context editing and memory tools
- **[claude-cost-optimization](../claude-cost-optimization/SKILL.md)**: Track costs, measure efficiency, and calculate ROI across your Claude deployment
- **[anthropic-expert](../anthropic-expert/SKILL.md)**: Comprehensive Anthropic product reference for API, SDKs, and integrations

For complete effort parameter documentation, API syntax details, and code examples in both Python and TypeScript, see **[references/effort-parameter-guide.md](references/effort-parameter-guide.md)**.

For model selection decision matrix and detailed capability comparisons, see **[references/model-selection-guide.md](references/model-selection-guide.md)**.

For full benchmark results and performance demonstrations, see **[references/model-capabilities.md](references/model-capabilities.md)**.
