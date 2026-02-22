---
name: critical-thinking
description: Analyze arguments, detect biases, evaluate claims, and improve reasoning. Use when asked to fact-check, identify logical fallacies, evaluate arguments, analyze predictions, find root causes, or think adversarially about plans. Triggers include "evaluate this argument", "logical fallacies", "fact check", "analyze the claims", "identify biases", "devil's advocate", "red team this", "root cause".
---

# Critical Thinking

Rigorous analysis of arguments, claims, and reasoning.

## Pattern Selection

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| Claim evaluation | `analyze_claims` | Assess truth claims with evidence |
| Prediction analysis | `extract_predictions` | Identify and assess predictions |
| Extraordinary claims | `extract_extraordinary_claims` | Claims contradicting consensus |
| Controversial ideas | `extract_controversial_ideas` | Contested viewpoints analysis |
| Error analysis | `analyze_mistakes` | Learn from past errors |
| Problem finding | `extract_primary_problem` | Root cause identification |
| Solution analysis | `extract_primary_solution` | Evaluate proposed solutions |
| Adversarial thinking | `t_red_team_thinking` | Find weaknesses in plans |
| Decision upgrade | `create_upgrade_pack` | Improve decision-making |
| Novel insights | `extract_alpha` | Most surprising/novel ideas |
| Thought organization | `create_idea_compass` | Structure complex ideas |
| Mind mapping | `create_markmap_visualization` | Visual thinking maps |

## Decision Flow

```
User request
    │
    ├─ "evaluate claims/fact check" ──→ analyze_claims
    ├─ "predictions/forecasts" ──→ extract_predictions
    ├─ "controversial/contested" ──→ extract_controversial_ideas
    ├─ "what went wrong/mistakes" ──→ analyze_mistakes
    ├─ "root cause/core problem" ──→ extract_primary_problem
    ├─ "red team/devil's advocate" ──→ t_red_team_thinking
    ├─ "surprising/novel insights" ──→ extract_alpha
    └─ "organize my thinking" ──→ create_idea_compass
```

## Pattern References

See `references/` for full patterns:
- [analyze_claims.md](references/analyze_claims.md)
- [extract_predictions.md](references/extract_predictions.md)
- [analyze_mistakes.md](references/analyze_mistakes.md)
- [extract_primary_problem.md](references/extract_primary_problem.md)
- [t_red_team_thinking.md](references/t_red_team_thinking.md)
- [extract_alpha.md](references/extract_alpha.md)
- [create_idea_compass.md](references/create_idea_compass.md)

## Output Guidelines

- Always distinguish claims from evidence
- Rate confidence levels explicitly
- Identify logical fallacies by name
- Present steelman versions of arguments before critiquing
- Note when evidence is insufficient to conclude
- Acknowledge uncertainty and areas of genuine disagreement

## Chaining Suggestions

- After `analyze_claims` → offer `extract_primary_problem` to find root issues
- After `t_red_team_thinking` → offer `create_upgrade_pack` to address weaknesses
- After `extract_primary_problem` → offer `extract_primary_solution` for solutions
