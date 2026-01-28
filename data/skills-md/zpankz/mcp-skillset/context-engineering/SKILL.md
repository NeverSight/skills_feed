---
name: context-engineering
description: Understand the components, mechanics, and constraints of context in agent systems. Use when writing, editing, or optimizing commands, skills, or sub-agents prompts.
---

# Context Engineering Fundamentals

Context is the complete state available to a language model at inference time. It includes everything the model can attend to when generating responses: system instructions, tool definitions, retrieved documents, message history, and tool outputs. Understanding context fundamentals is prerequisite to effective context engineering.

## Core Concepts

Context comprises several distinct components, each with different characteristics and constraints. The attention mechanism creates a finite budget that constrains effective context usage. Progressive disclosure manages this constraint by loading information only as needed. The engineering discipline is curating the smallest high-signal token set that achieves desired outcomes.

### Key Principles

**Context as Finite Resource**
Context must be treated as a finite resource with diminishing marginal returns. Like humans with limited working memory, language models have an attention budget drawn on when parsing large volumes of context. Every new token introduced depletes this budget by some amount.

**Progressive Disclosure**
Progressive disclosure manages context efficiently by loading information only as needed. At startup, agents load only skill names and descriptions--sufficient to know when a skill might be relevant. Full content loads only when a skill is activated for specific tasks.

**Quality Over Quantity**
The assumption that larger context windows solve memory problems has been empirically debunked. Context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of desired outcomes.

**Informativity Over Exhaustiveness**
Include what matters for the decision at hand, exclude what does not, and design systems that can access additional information on demand.

## Progressive Loading

**L2 Content** (loaded when fundamentals or patterns needed):
- See: [references/fundamentals.md](./references/fundamentals.md)
  - The Anatomy of Context
  - Context Windows and Attention Mechanics
  - Practical Guidance
  - Examples

- See: [references/degradation-patterns.md](./references/degradation-patterns.md)
  - Lost-in-Middle Phenomenon
  - Context Poisoning
  - Context Distraction
  - Context Confusion and Clash
  - Architectural Patterns

**L3 Content** (loaded when workflows or optimization needed):
- See: [references/workflows.md](./references/workflows.md)
  - Hallucination Detection Workflow
  - Lost-in-Middle Detection Workflow
  - Error Propagation Analysis
  - Context Relevance Scoring
  - Context Health Monitoring

- See: [references/optimization.md](./references/optimization.md)
  - Compaction Strategies
  - Observation Masking
  - Context Partitioning
  - Optimization Decision Framework
