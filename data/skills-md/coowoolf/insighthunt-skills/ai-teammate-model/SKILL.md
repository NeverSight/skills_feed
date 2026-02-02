---
name: ai-teammate-model
description: Use when designing AI agent products, defining roadmaps for agentic workflows, or evaluating how to evolve AI from passive tool to proactive partner in software development
---

# The AI Teammate Model

## Overview

A framework for evolving AI agents from **simple tools** into **autonomous partners**. A true AI teammate must move beyond code generation to participate in the entire software lifecycle while possessing proactivity.

**Core principle:** Treat the AI like a new intern—verify work initially, then build trust and grant autonomy incrementally.

## Evolution Phases

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: THE SMART INTERN                                      │
│  ─────────────────────────────────────────────────────────────  │
│  • Reactive (needs explicit prompts)                            │
│  • No context (can't read Slack/Datadog)                        │
│  • Requires full review                                         │
│  • "Prompt-to-Patch" workflow                                   │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 2: THE PAIR PROGRAMMER                                   │
│  ─────────────────────────────────────────────────────────────  │
│  • Collaborative (works in IDE/Terminal)                        │
│  • Human-in-the-loop validation                                 │
│  • Gaining context awareness                                    │
│  • Handles environment setup                                    │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 3: THE PROACTIVE TEAMMATE                                │
│  ─────────────────────────────────────────────────────────────  │
│  • Autonomous (monitors Slack/Logs/Metrics)                     │
│  • Signal-driven (acts without prompts)                         │
│  • Asynchronous execution                                       │
│  • High trust delegation                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Contextual Integration** | Agent must access full environment (runtime, logs, comms) |
| **Proactivity by Default** | Shift from prompt-driven to signal-driven action |
| **Trust Evolution** | Move from micro-management to delegation gradually |
| **Full Lifecycle** | Agent contributes to planning, coding, reviewing, deploying |

## Enablement Checklist

To evolve from Phase 1 → Phase 3:

- [ ] Grant access to communication tools (Slack, Email)
- [ ] Connect to observability (Datadog, Logs)
- [ ] Enable autonomous execution (background tasks)
- [ ] Build feedback loops (run → error → fix → run)

## Common Mistakes

- **Treating as black box** → Give it access to validation tools
- **Expecting instant autonomy** → "Onboard" it with context first
- **No feedback loops** → Agent can't learn from execution results

## Real-World Example

OpenAI has Codex "on-call" for its own training runs—monitoring graphs and fixing configuration mistakes without human intervention.

---

*Source: Alexander Embiricos (OpenAI Codex) via Lenny's Podcast*
