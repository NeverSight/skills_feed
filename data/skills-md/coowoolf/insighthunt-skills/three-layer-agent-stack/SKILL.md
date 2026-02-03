---
name: three-layer-agent-stack
description: Use when building AI-powered products or agents, when raw model intelligence isn't enough to solve user problems, or when designing the architecture for agentic workflows
---

# The Three-Layer Agent Stack

## Overview

A framework for building effective AI agents by synchronizing innovation across **three distinct layers**: Model, API, and Harness. Success requires tight integration—not treating the model as a black box.

**Core principle:** Features like "compaction" (long-running tasks) require simultaneous changes across all three layers.

## The Stack

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: HARNESS / PRODUCT LAYER                               │
│  ─────────────────────────────────────────────────────────────  │
│  The environment that executes actions and provides context     │
│  • VS Code / IDE integration                                    │
│  • Terminal / Shell access                                      │
│  • Sandbox / Secure execution environment                       │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 2: API LAYER                                             │
│  ─────────────────────────────────────────────────────────────  │
│  Interface handling state, context windows, and orchestration   │
│  • Context management / Compaction                              │
│  • State handoff between sessions                               │
│  • Tool routing and formatting                                  │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 1: MODEL LAYER                                           │
│  ─────────────────────────────────────────────────────────────  │
│  Foundation model providing reasoning and intelligence          │
│  • Code generation / Reasoning                                  │
│  • Summarization for compaction                                 │
│  • Environment-specific training                                │
└─────────────────────────────────────────────────────────────────┘
```

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Full-Stack Iteration** | Changes often need Model + API + Harness together |
| **Harness Specificity** | Models perform best when trained for specific environments |
| **Feedback Loops** | Product usage (Harness) must inform model training |
| **Safety Sandboxing** | Harness provides secure environment for code execution |

## Common Mistakes

- **Model-only optimization**: Changing model without adapting harness
- **Generic API assumptions**: Assuming generic API supports agentic behaviors
- **No feedback loop**: Harness doesn't feed back to model training

## Real-World Example

Implementing "Compaction" to allow Codex to run 24 hours:
- **Model**: Must understand summarization
- **API**: Must handle the context handoff
- **Harness**: Must prepare and format the payload

---

*Source: Alexander Embiricos (OpenAI Codex) via Lenny's Podcast*
