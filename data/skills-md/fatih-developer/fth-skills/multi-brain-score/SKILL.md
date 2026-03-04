---
name: multi-brain-score
description: Confidence scoring overlay for multi-brain decisions. Each perspective rates its own confidence (1-10) with justification. Consensus uses scores as weights, flags low-confidence areas, and surfaces uncertainty explicitly.
---

# Multi-Brain Score Protocol

Add **quantified confidence scoring** to any multi-brain decision. Each perspective rates its own confidence, and the consensus uses scores as decision weights. Uncertainty becomes visible instead of hidden.

---

## Workflow

```
1. Run base multi-brain (3 perspectives)
2. Each instance scores its confidence (1-10)
3. Weighted consensus based on scores
4. Flag uncertainty zones
5. Produce full output with scores visible
```

---

## Step 1: Perspectives with Scores

Each instance provides their perspective **plus** a confidence score:

```markdown
## 🧠 Brainstorm (Scored)

**Instance A — Creative:** (Confidence: 6/10)
[2-3 sentences]
_Confidence rationale: Novel approach but limited precedent in production._

**Instance B — Pragmatic:** (Confidence: 9/10)
[2-3 sentences]
_Confidence rationale: Well-established pattern, used this successfully before._

**Instance C — Comprehensive:** (Confidence: 7/10)
[2-3 sentences]
_Confidence rationale: Good coverage of risks but missing data on edge case X._
```

---

## Step 2: Score Analysis

Before consensus, analyze the confidence landscape:

```markdown
## 📊 Confidence Analysis

| Instance | Score | Strength | Weakness |
|----------|-------|----------|----------|
| A — Creative | 6/10 | High potential impact | Unproven approach |
| B — Pragmatic | 9/10 | Battle-tested | May miss innovation |
| C — Comprehensive | 7/10 | Risk-aware | Incomplete data |

**Average Confidence:** 7.3/10
**Spread:** 3 points (moderate disagreement)
**Highest Confidence:** Instance B
```

---

## Step 3: Weighted Consensus

Use confidence scores to weight the consensus:

- **High confidence (8-10):** This perspective's core recommendation carries heavy weight.
- **Medium confidence (5-7):** Consider as a modifier or secondary input.
- **Low confidence (1-4):** Flag as an area needing more research before deciding. Do not ignore — surface it as a risk.

```markdown
## ⚖️ Weighted Consensus

**Primary direction:** [Based on highest-confidence perspective]
**Modified by:** [Elements from medium-confidence perspectives]
**Flagged for research:** [Low-confidence areas that need validation]

**Overall Decision Confidence:** [Weighted average]/10
```

---

## Step 4: Uncertainty Flags

If any perspective scores below 5, or if the spread between scores is > 4:

```markdown
> ⚠️ **Uncertainty Alert:** [Description of what is uncertain and what would resolve it]
```

---

## Step 5: Full Output

**Mandatory:** The final response must include all scored perspectives, the confidence analysis table, the weighted consensus, any uncertainty flags, and the complete deliverable.

---

## Scoring Rubric

| Score | Meaning | When to Use |
|-------|---------|-------------|
| 9-10 | Near-certain | Strong evidence, proven pattern, minimal unknowns |
| 7-8 | Confident | Good reasoning, some minor unknowns |
| 5-6 | Moderate | Reasonable approach but notable gaps |
| 3-4 | Low | Speculative, lacks supporting evidence |
| 1-2 | Guess | No solid basis, flagging for transparency |

---

## Guardrails

- **Always show scores inline with perspectives** — they are part of the deliverable.
- Confidence rationale is **mandatory** — a bare number without explanation is useless.
- **Never inflate scores** — honest uncertainty is more valuable than false confidence.
- If all scores are below 5, recommend **more research before deciding** instead of forcing a weak consensus.
- Scores should create **action items** — low scores become "things to validate."
- This protocol can be **combined** with base multi-brain or multi-brain-experts.

---

## References

- See `references/EXAMPLES.md` for scored decision examples.
