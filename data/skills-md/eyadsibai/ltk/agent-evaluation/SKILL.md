---
name: agent-evaluation
description: Use when evaluating agent performance, building test frameworks, measuring quality, or asking about "agent evaluation", "LLM-as-judge", "agent testing", "quality metrics", "evaluation rubrics", "agent benchmarks"
version: 1.0.0
---

# Agent Evaluation Methods

Agent evaluation requires different approaches than traditional software. Agents are non-deterministic, may take different valid paths, and lack single correct answers.

## Key Finding: 95% Performance Drivers

Research on BrowseComp found three factors explain 95% of variance:

| Factor | Variance | Implication |
|--------|----------|-------------|
| Token usage | 80% | More tokens = better performance |
| Tool calls | ~10% | More exploration helps |
| Model choice | ~5% | Better models multiply efficiency |

**Implications**: Model upgrades beat token increases. Multi-agent architectures validate.

## Multi-Dimensional Rubric

| Dimension | Excellent | Good | Acceptable | Failed |
|-----------|-----------|------|------------|--------|
| Factual accuracy | All correct | Minor errors | Some errors | Wrong |
| Completeness | All aspects | Most aspects | Key aspects | Missing |
| Citation accuracy | All match | Most match | Some match | Wrong |
| Tool efficiency | Optimal | Good | Adequate | Wasteful |

## LLM-as-Judge

```python
evaluation_prompt = """
Task: {task_description}
Agent Output: {agent_output}
Ground Truth: {ground_truth}

Evaluate on:
1. Factual accuracy (0-1)
2. Completeness (0-1)
3. Citation accuracy (0-1)
4. Tool efficiency (0-1)

Provide scores and reasoning.
"""
```

## Test Set Design

```python
test_set = [
    {"name": "simple", "complexity": "simple",
     "input": "What is capital of France?"},
    {"name": "medium", "complexity": "medium",
     "input": "Compare Apple and Microsoft revenue"},
    {"name": "complex", "complexity": "complex",
     "input": "Analyze Q1-Q4 sales trends"},
    {"name": "very_complex", "complexity": "very_complex",
     "input": "Research AI tech, evaluate impact, recommend strategy"}
]
```

## Evaluation Pipeline

```python
def evaluate_agent(agent, test_set):
    results = []
    for test in test_set:
        output = agent.run(test["input"])
        scores = llm_judge(output, test)
        results.append({
            "test": test["name"],
            "scores": scores,
            "passed": scores["overall"] >= 0.7
        })
    return results
```

## Complexity Stratification

| Level | Characteristics |
|-------|-----------------|
| Simple | Single tool call |
| Medium | Multiple tool calls |
| Complex | Many calls, ambiguity |
| Very Complex | Extended interaction, deep reasoning |

## Context Engineering Evaluation

Test context strategies systematically:

1. Run agents with different strategies on same tests
2. Compare quality scores, token usage, efficiency
3. Identify degradation cliffs at different context sizes

## Continuous Evaluation

- Run evaluations on all agent changes
- Track metrics over time
- Set alerts for quality drops
- Sample production interactions

## Avoiding Pitfalls

| Pitfall | Solution |
|---------|----------|
| Path overfitting | Evaluate outcomes, not steps |
| Ignoring edge cases | Include diverse scenarios |
| Single metric | Multi-dimensional rubrics |
| Ignoring context | Test realistic context sizes |
| No human review | Supplement automated eval |

## Best Practices

1. Use multi-dimensional rubrics
2. Evaluate outcomes, not specific paths
3. Cover complexity levels
4. Test with realistic context sizes
5. Run evaluations continuously
6. Supplement LLM with human review
7. Track metrics for trends
8. Set clear pass/fail thresholds
