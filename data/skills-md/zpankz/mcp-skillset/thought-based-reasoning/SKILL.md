---
name: thought-based-reasoning
description: Use when tackling complex reasoning tasks requiring step-by-step logic, multi-step arithmetic, commonsense reasoning, symbolic manipulation, or problems where simple prompting fails - provides comprehensive guide to Chain-of-Thought and related prompting techniques
---

# Thought-Based Reasoning Techniques for LLMs

## Overview

Chain-of-Thought (CoT) prompting and its variants encourage LLMs to generate intermediate reasoning steps before arriving at a final answer, significantly improving performance on complex reasoning tasks. These techniques transform how models approach problems by making implicit reasoning explicit.

## Quick Reference

| Technique | When to Use | Complexity | Accuracy Gain |
|-----------|-------------|------------|---------------|
| Zero-shot CoT | Quick reasoning, no examples available | Low | +20-60% |
| Few-shot CoT | Have good examples, consistent format needed | Medium | +30-70% |
| Self-Consistency | High-stakes decisions, need confidence | Medium | +10-20% over CoT |
| Tree of Thoughts | Complex problems requiring exploration | High | +50-70% on hard tasks |
| Least-to-Most | Multi-step problems with subproblems | Medium | +30-80% |
| ReAct | Tasks requiring external information | Medium | +15-35% |
| PAL | Mathematical/computational problems | Medium | +10-15% |
| Reflexion | Iterative improvement, learning from errors | High | +10-20% |

## When to Use Thought-Based Reasoning

**Use CoT techniques when:**
- Multi-step arithmetic or math word problems
- Commonsense reasoning requiring logical deduction
- Symbolic reasoning tasks
- Complex problems where simple prompting fails

**Start with:**
- **Zero-shot CoT** for quick prototyping ("Let's think step by step")
- **Few-shot CoT** when you have good examples
- **Self-Consistency** for high-stakes decisions

## Progressive Loading

**L2 Content** (loaded when core techniques needed):
- See: [references/core-techniques.md](./references/core-techniques.md)
  - Chain-of-Thought (CoT) Prompting
  - Zero-shot Chain-of-Thought
  - Self-Consistency Decoding
  - Tree of Thoughts (ToT)
  - Least-to-Most Prompting
  - ReAct (Reasoning + Acting)
  - PAL (Program-Aided Language Models)
  - Reflexion

**L3 Content** (loaded when decision guidance and best practices needed):
- See: [references/guidance.md](./references/guidance.md)
  - Decision Matrix: Which Technique to Use
  - Best Practices
  - Common Mistakes
  - References
