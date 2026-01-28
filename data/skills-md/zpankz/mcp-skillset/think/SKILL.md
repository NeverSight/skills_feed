---
name: think
description: Cognitive enhancement toolkit combining non-linear reasoning, mental models, and literate programming. Use for complex analysis, system design, debugging, deep learning, and research workflows.
---

# Think Skill

Orchestrate three MCP tools for structured reasoning.

## Quick Navigation

| Need | Go To |
|------|-------|
| Non-linear reasoning | [THOUGHTBOX.md](THOUGHTBOX.md) |
| Reasoning frameworks | [MODELS.md](MODELS.md) |
| Executable notebooks | [NOTEBOOK.md](NOTEBOOK.md) |
| Tool combinations | [PATTERNS.md](PATTERNS.md) |
| Problem→Solution routing | [SELECTION.md](SELECTION.md) |
| Concrete examples | [EXAMPLES.md](EXAMPLES.md) |

## Tools At a Glance

| Tool | Purpose | Key Feature |
|------|---------|-------------|
| `thoughtbox` | Step-by-step reasoning | 7 patterns: forward, backward, branching, revision, interleaved, first principles, meta-reflection |
| `mental_models` | Structured schemas | 15 models across 9 tags |
| `notebook` | Literate programming | 10 operations, executable JS/TS |

## When to Use This Skill

- **Complex problems** → decomposition + branching
- **Debugging** → five-whys + backward thinking
- **Architecture decisions** → pre-mortem + trade-off matrix
- **Deep learning** → Sequential Feynman notebook
- **Research tasks** → interleaved reasoning loops

## Minimal Invocation

```javascript
// Reasoning
thoughtbox({ thought: "...", thoughtNumber: 1, totalThoughts: 10, nextThoughtNeeded: true })

// Framework
mental_models({ operation: "get_model", args: { model: "five-whys" } })

// Notebook
notebook({ operation: "create", args: { title: "...", language: "typescript" }})
```

## MCP Resources (On-Demand)

| Resource | Access |
|----------|--------|
| Patterns cookbook | `thoughtbox({ includeGuide: true })` |
| Model content | `mental_models({ operation: "get_model", args: { model: "..." } })` |
| Notebook ops | `thoughtbox://notebook/operations` |
| Interleaved guides | `thoughtbox://interleaved/{mode}` |

---

*For deeper content, follow links above. Each file is self-contained.*
