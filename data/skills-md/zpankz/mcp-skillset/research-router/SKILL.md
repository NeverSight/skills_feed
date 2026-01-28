---
name: research-router
description: Routes research and investigation tasks. Triggers on research, investigate, deep-dive, explore, understand, learn, study, compare, thorough, comprehensive.
---

# Research Router

Routes research, learning, and investigation tasks to specialized skills.

## Subcategories

### Deep Research
```yaml
triggers: [comprehensive, thorough, multi-source, citations, verify, deep-dive]
skills:
  - deep-research: 7-phase research protocol with Graph of Thoughts
  - mcp-skillset-workflows: Multi-skill orchestration patterns
```

### Reasoning / Thinking
```yaml
triggers: [think, reason, analyze-deeply, complex-problem, multi-step]
skills:
  - think: Cognitive enhancement toolkit
  - reason: Recursive decomposition
  - AoT: Atom of Thoughts (formal)
  - urf: Universal Reasoning Framework
```

### Learning
```yaml
triggers: [learn, understand, explain, study, compare, evaluate]
skills:
  - sc:explain: Clear explanations
  - deepstudy: Deep study workflows
  - notebooklm: Query NotebookLM
```

## Routing Decision Tree

```
research request
    │
    ├── "deep research" explicit?
    │   └── deep-research
    │
    ├── Reasoning/thinking focus?
    │   ├── Lightweight? → think
    │   ├── Formal proof? → AoT
    │   └── Multi-scale? → urf
    │
    ├── Learning focus?
    │   ├── Explanation? → sc:explain
    │   └── Study → deepstudy
    │
    └── General investigation?
        └── deep-research
```

## Progressive Loading

1. **Light Analysis**: Load `think` or `reason` first
2. **Deep Dive**: If complexity increases, add `deep-research`
3. **Formal Verification**: If proof needed, add `AoT` or `urf`

## Managed Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| deep-research | 7-phase research | "deep research", "thorough" |
| think | Non-linear reasoning | "think", "analyze" |
| reason | Recursive decomposition | "reason", "understand" |
| AoT | Atom of Thoughts | "prove", "verify", "formal" |
| urf | Universal framework | "multi-scale", "complex" |
| sc:explain | Explanations | "explain", "describe" |
