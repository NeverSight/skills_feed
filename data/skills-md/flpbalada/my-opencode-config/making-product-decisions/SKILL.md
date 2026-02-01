---
name: making-product-decisions
description:
  Framework for structured product decision-making. Use when facing complex
  tradeoffs, aligning stakeholders, documenting decisions, or choosing between
  multiple valid approaches.
---

# Making Product Decisions - Structured Decision Framework

A meta-framework for making and documenting product decisions. Combines decision
science principles with practical product management needs to ensure better
decisions, stakeholder alignment, and organizational learning.

## When to Use This Skill

- Choosing between competing priorities or approaches
- Making irreversible or high-stakes decisions
- Aligning stakeholders with different perspectives
- Documenting decisions for future reference
- Evaluating past decisions for learning
- Delegating decision-making authority

## Core Concepts

### Decision Types (Bezos Framework)

```
+------------------+------------------+
|   Type 1         |   Type 2         |
|   (One-way door) |   (Two-way door) |
+------------------+------------------+
| Irreversible     | Reversible       |
| High stakes      | Lower stakes     |
| Slow, careful    | Fast, iterate    |
| Senior decision  | Delegate widely  |
+------------------+------------------+
```

### Decision Quality vs. Outcome

|                   | Good Outcome     | Bad Outcome      |
| ----------------- | ---------------- | ---------------- |
| **Good Decision** | Deserved success | Bad luck         |
| **Bad Decision**  | Good luck        | Deserved failure |

Judge decisions by process quality, not just outcomes.

### Data-Informed vs. Data-Driven

| Approach          | When to Use                                        |
| ----------------- | -------------------------------------------------- |
| **Data-driven**   | Clear metrics, sufficient data, understood system  |
| **Data-informed** | Incomplete data, novel situations, judgment needed |
| **Intuition-led** | Time pressure, expert domain, pattern matching     |

Most product decisions should be data-informed, not purely data-driven.

## Analysis Framework

### Step 1: Frame the Decision

| Element           | Question                       |
| ----------------- | ------------------------------ |
| **What**          | What exactly are we deciding?  |
| **Why**           | Why does this decision matter? |
| **Who**           | Who should be involved?        |
| **When**          | When must we decide by?        |
| **Reversibility** | Type 1 or Type 2 door?         |

### Step 2: Generate Options

Always have at least 3 options:

1. Do nothing / status quo
2. Option A
3. Option B

Avoid binary framing - it limits thinking.

### Step 3: Establish Criteria

| Criterion     | Weight | Why It Matters |
| ------------- | ------ | -------------- |
| [Criterion 1] | [1-5]  | [Explanation]  |
| [Criterion 2] | [1-5]  | [Explanation]  |
| [Criterion 3] | [1-5]  | [Explanation]  |

### Step 4: Evaluate Options

| Option     | Criterion 1 | Criterion 2 | Criterion 3 | Total |
| ---------- | ----------- | ----------- | ----------- | ----- |
| Status quo | [Score]     | [Score]     | [Score]     | [Sum] |
| Option A   | [Score]     | [Score]     | [Score]     | [Sum] |
| Option B   | [Score]     | [Score]     | [Score]     | [Sum] |

### Step 5: Document and Decide

Record:

- Decision made
- Rationale
- Dissenting views
- Success criteria
- Review date

## Output Template

```markdown
## Product Decision Record

**Decision:** [Clear statement of what was decided] **Date:** [Date] **Decision
maker:** [Name] **Status:** [Proposed/Approved/Implemented]

### Context

**Problem/Opportunity:** [What prompted this decision]

**Constraints:** [Time, resources, dependencies]

**Reversibility:** [Type 1 / Type 2]

### Options Considered

| Option     | Description | Pros | Cons |
| ---------- | ----------- | ---- | ---- |
| Status quo | [Desc]      | [+]  | [-]  |
| Option A   | [Desc]      | [+]  | [-]  |
| Option B   | [Desc]      | [+]  | [-]  |

### Decision Criteria

| Criterion | Weight | Rationale |
| --------- | ------ | --------- |
| [C1]      | [1-5]  | [Why]     |
| [C2]      | [1-5]  | [Why]     |

### Evaluation

| Option  | [C1]  | [C2]  | Weighted Total |
| ------- | ----- | ----- | -------------- |
| [Opt 1] | [x/5] | [x/5] | [Score]        |
| [Opt 2] | [x/5] | [x/5] | [Score]        |

### Decision

**Chosen option:** [Option name]

**Rationale:** [Why this option best meets criteria]

**Dissenting views:** [Captured disagreements and concerns]

### Success Criteria

| Metric | Current | Target  | Measure By |
| ------ | ------- | ------- | ---------- |
| [M1]   | [Value] | [Value] | [Date]     |

### Review

**Review date:** [Date] **What we'll evaluate:** [Criteria for success/failure]
```

## Real-World Examples

### Example 1: Build vs. Buy

**Decision**: Build custom analytics or use third-party tool?

| Criterion          | Weight | Build | Buy |
| ------------------ | ------ | ----- | --- |
| Time to market     | 5      | 2     | 5   |
| Customization      | 3      | 5     | 2   |
| Long-term cost     | 4      | 3     | 4   |
| Maintenance burden | 4      | 2     | 5   |
| **Total**          |        | 42    | 66  |

Decision: Buy, despite customization limitations.

### Example 2: Feature Prioritization

**Decision**: Next quarter focus - mobile app or API improvements?

Applied decision criteria:

- Revenue impact (weight: 5)
- User retention (weight: 4)
- Strategic positioning (weight: 3)
- Engineering complexity (weight: 2)

Result: Mobile app scored higher on revenue and retention despite higher
complexity.

## Best Practices

### Do

- Make decision criteria explicit before evaluating
- Include "do nothing" as an option
- Document dissenting opinions
- Set review dates for major decisions
- Separate decision quality from outcome

### Avoid

- Analysis paralysis on Type 2 decisions
- HiPPO (Highest Paid Person's Opinion) decisions
- Retroactive justification
- Ignoring intuition entirely
- Forgetting to review past decisions

### Decision Speed Guidelines

| Type                | Approach                                |
| ------------------- | --------------------------------------- |
| Type 1, high stakes | Take time, involve stakeholders         |
| Type 2, reversible  | Decide quickly, iterate                 |
| Unclear type        | Default to faster, can always slow down |

## Integration with Other Methods

| Method              | Combined Use                    |
| ------------------- | ------------------------------- |
| **Hypothesis Tree** | Structure analysis of options   |
| **Jobs-to-be-Done** | Ground criteria in user needs   |
| **Five Whys**       | Understand decision root causes |

## Resources

- [Thinking in Bets - Annie Duke](https://www.amazon.com/Thinking-Bets-Making-Smarter-Decisions/dp/0735216355)
- [Decisive - Chip & Dan Heath](https://www.amazon.com/Decisive-Make-Better-Choices-Life/dp/0307956393)
