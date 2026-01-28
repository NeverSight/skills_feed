---
name: agent-evaluation
description: Evaluate and improve Claude Code commands, skills, and agents. Use when testing prompt effectiveness, validating context engineering choices, or measuring improvement quality.
---

# Evaluation Methods for Claude Code Agents

Evaluation of agent systems requires different approaches than traditional software or even standard language model applications. Agents make dynamic decisions, are non-deterministic between runs, and often lack single correct answers. Effective evaluation must account for these characteristics while providing actionable feedback. A robust evaluation framework enables continuous improvement, catches regressions, and validates that context engineering choices achieve intended effects.

## Core Concepts

Agent evaluation requires outcome-focused approaches that account for non-determinism and multiple valid paths. Multi-dimensional rubrics capture various quality aspects: factual accuracy, completeness, citation accuracy, source quality, and tool efficiency. LLM-as-judge provides scalable evaluation while human evaluation catches edge cases.

The key insight is that agents may find alternative paths to goals—the evaluation should judge whether they achieve right outcomes while following reasonable processes.

**Performance Drivers: The 95% Finding**
Research on the BrowseComp evaluation (which tests browsing agents' ability to locate hard-to-find information) found that three factors explain 95% of performance variance:

| Factor | Variance Explained | Implication |
|--------|-------------------|-------------|
| Token usage | 80% | More tokens = better performance |
| Number of tool calls | ~10% | More exploration helps |
| Model choice | ~5% | Better models multiply efficiency |

Implications for Claude Code development:

- **Token budgets matter**: Evaluate with realistic token constraints
- **Model upgrades beat token increases**: Upgrading models provides larger gains than increasing token budgets
- **Multi-agent validation**: Validates architectures that distribute work across subagents with separate context windows

## Progressive Loading

**L2 Content** (loaded when methodology details needed):
- See: [references/methodologies.md](./references/methodologies.md)
  - Evaluation Challenges
  - Evaluation Rubric Design
  - Evaluation Methodologies
  - Test Set Design
  - Context Engineering Evaluation

**L3 Content** (loaded when advanced techniques or examples needed):
- See: [references/advanced.md](./references/advanced.md)
  - Advanced Evaluation: LLM-as-Judge
  - Evaluation Metrics Reference
  - Bias Mitigation Techniques
  - LLM-as-Judge Implementation Patterns
  - Metric Selection Guide
  - Practical Examples
