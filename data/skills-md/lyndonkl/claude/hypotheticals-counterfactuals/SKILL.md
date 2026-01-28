---
name: hypotheticals-counterfactuals
description: Use when exploring alternative scenarios, testing assumptions through "what if" questions, understanding causal relationships, conducting pre-mortem analysis, stress testing decisions, or when user mentions counterfactuals, hypothetical scenarios, thought experiments, alternative futures, what-if analysis, or needs to challenge assumptions and explore possibilities.
---
# Hypotheticals and Counterfactuals

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Hypotheticals and Counterfactuals uses "what if" thinking to explore alternative scenarios, test assumptions, understand causal relationships, and prepare for uncertainty. This skill guides you through counterfactual reasoning (what would have happened differently?), scenario exploration (what could happen?), pre-mortem analysis (imagine failure, identify causes), and stress testing decisions against alternative futures.

## When to Use

Use this skill when:

- **Testing assumptions**: Challenge underlying beliefs by asking "what if this assumption is wrong?"
- **Pre-mortem analysis**: Imagine project failure, identify potential causes before they occur
- **Causal inference**: Understand "what caused X?" by asking "would X have happened without Y?"
- **Scenario planning**: Explore alternative futures (best case, worst case, surprising case)
- **Risk identification**: Uncover hidden risks through "what could go wrong?" analysis
- **Strategic planning**: Test strategy robustness across different market conditions
- **Learning from failures**: Counterfactual analysis "what if we had done X instead?"
- **Decision stress testing**: Check if decision holds across optimistic/pessimistic scenarios
- **Innovation exploration**: "What if we removed constraint X?" to unlock new possibilities
- **Historical analysis**: "What would have happened if..." to understand key factors

Trigger phrases: "what if", "counterfactual", "hypothetical scenario", "thought experiment", "alternative future", "pre-mortem", "stress test", "what could go wrong", "imagine if", "suppose that"

## What Is It?

**Hypotheticals and Counterfactuals** combines forward-looking scenario exploration (hypotheticals) with backward-looking alternative history analysis (counterfactuals):

**Core components**:
- **Counterfactuals**: "What would have happened if X had been different?" Understand causality by imagining alternatives.
- **Pre-mortem**: Imagine future failure, work backward to identify causes. Inversion of post-mortem.
- **Scenario Planning**: Explore multiple plausible futures (2×2 matrix, three scenarios, cone of uncertainty).
- **Stress Testing**: Test decisions/plans against extreme scenarios (best/worst case, black swans).
- **Thought Experiments**: Explore ideas through imagined scenarios (Einstein's elevator, trolley problem).
- **Assumption Reversal**: "What if our key assumption is backwards?" to challenge mental models.

**Quick example:**

**Scenario**: Startup deciding whether to pivot from B2B to B2C.

**Counterfactual Analysis** (Learning from past):
- **Actual**: We focused on B2B, growth slow (5% MoM)
- **Counterfactual**: "What if we had gone B2C from start?"
  - Hypothesis: Faster growth (viral potential) but higher CAC, lower LTV
  - Evidence: Competitor X did B2C, grew 20% MoM but 60% churn
  - Insight: B2C growth faster BUT unit economics worse. B2B slower but sustainable.

**Pre-Mortem** (Preparing for future):
- Imagine: It's 1 year from now, B2C pivot failed
- Why did it fail?
  1. CAC higher than projected (Facebook ads too expensive)
  2. Churn higher than B2B (no contracts, easy to switch)
  3. Team lacked consumer product expertise
  4. Existing B2B customers churned (felt abandoned)
- **Action**: Before pivoting, test assumptions with small B2C experiment. Don't abandon B2B entirely.

**Outcome**: Decision to run parallel B2C pilot while maintaining B2B, de-risking pivot through counterfactual insights and pre-mortem preparation.

**Core benefits**:
- **Causal clarity**: Understand what drives outcomes by imagining alternatives
- **Risk identification**: Pre-mortem uncovers failure modes before they happen
- **Assumption testing**: Stress test beliefs against extreme scenarios
- **Strategic flexibility**: Prepare for multiple futures, not just one forecast
- **Learning enhancement**: Counterfactuals reveal what mattered vs. what didn't

## Workflow

Copy this checklist and track your progress:

```
Hypotheticals & Counterfactuals Progress:
- [ ] Step 1: Define the focal question
- [ ] Step 2: Generate counterfactuals or scenarios
- [ ] Step 3: Develop each scenario
- [ ] Step 4: Identify implications and insights
- [ ] Step 5: Extract actions or decisions
- [ ] Step 6: Monitor and update
```

**Step 1: Define the focal question**

What are you exploring? Past decision (counterfactual)? Future possibility (hypothetical)? Assumption to test? See [resources/template.md](resources/template.md#focal-question-template).

**Step 2: Generate counterfactuals or scenarios**

Counterfactual: Change one key factor, ask "what would have happened?" Hypothetical: Imagine future scenarios (2-4 plausible alternatives). See [resources/template.md](resources/template.md#scenario-generation-template) and [resources/methodology.md](resources/methodology.md#1-counterfactual-reasoning).

**Step 3: Develop each scenario**

Describe what's different, trace implications, identify key assumptions. Make it vivid and concrete. See [resources/template.md](resources/template.md#scenario-development-template) and [resources/methodology.md](resources/methodology.md#2-scenario-planning-techniques).

**Step 4: Identify implications and insights**

What does each scenario teach? What assumptions are tested? What risks revealed? See [resources/methodology.md](resources/methodology.md#3-extracting-insights-from-scenarios).

**Step 5: Extract actions or decisions**

What should we do differently based on these scenarios? Hedge against downside? Prepare for upside? See [resources/template.md](resources/template.md#action-extraction-template).

**Step 6: Monitor and update**

Track which scenario is unfolding. Update plans as reality diverges from expectations. See [resources/methodology.md](resources/methodology.md#4-monitoring-and-adaptation).

Validate using [resources/evaluators/rubric_hypotheticals_counterfactuals.json](resources/evaluators/rubric_hypotheticals_counterfactuals.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Pre-Mortem (Prospective Hindsight)**
- **Format**: Imagine it's future date, project failed. List reasons why.
- **Best for**: Project planning, risk identification before launch
- **Process**: (1) Set future date, (2) Assume failure, (3) List causes, (4) Prioritize top 3-5 risks, (5) Mitigate now
- **When**: Before major launch, strategic decision, resource commitment
- **Output**: Risk list with mitigations

**Pattern 2: Counterfactual Causal Analysis**
- **Format**: "What would have happened if we had done X instead of Y?"
- **Best for**: Learning from past decisions, understanding what mattered
- **Process**: (1) Identify decision, (2) Imagine alternative, (3) Trace different outcome, (4) Identify causal factor
- **When**: Post-mortem, retrospective, learning from success/failure
- **Output**: Causal insight (X caused Y because...)

**Pattern 3: Three Scenarios (Optimistic, Baseline, Pessimistic)**
- **Format**: Describe best case, expected case, worst case futures
- **Best for**: Strategic planning, forecasting, resource allocation
- **Process**: (1) Define time horizon, (2) Describe three futures, (3) Assign probabilities, (4) Plan for each
- **When**: Annual planning, market uncertainty, investment decisions
- **Output**: Three detailed scenarios with implications

**Pattern 4: 2×2 Scenario Matrix**
- **Format**: Two key uncertainties create four quadrants (scenarios)
- **Best for**: Exploring interaction of two critical unknowns
- **Process**: (1) Identify two key uncertainties, (2) Define extremes, (3) Develop four scenarios, (4) Name each world
- **When**: Strategic planning with multiple drivers of uncertainty
- **Output**: Four distinct future worlds with narratives

**Pattern 5: Assumption Reversal**
- **Format**: "What if our key assumption is backwards?"
- **Best for**: Challenging mental models, unlocking innovation
- **Process**: (1) List key assumptions, (2) Reverse each, (3) Explore implications, (4) Identify if reversal plausible
- **When**: Stuck in conventional thinking, need breakthrough
- **Output**: New perspectives, potential pivots

**Pattern 6: Stress Test (Extreme Scenarios)**
- **Format**: Push key variables to extremes, test if decision holds
- **Best for**: Risk management, decision robustness testing
- **Process**: (1) Identify decision, (2) List key variables, (3) Set to extremes, (4) Check if decision still valid
- **When**: High-stakes decisions, need to ensure resilience
- **Output**: Decision validation or hedges needed

## Guardrails

**Critical requirements:**

1. **Plausibility constraint**: Scenarios must be possible, not just imaginable. "What if gravity reversed?" is not useful counterfactual. Stay within bounds of plausibility given current knowledge.

2. **Minimal rewrite principle** (counterfactuals): Change as little as possible. "What if we had chosen Y instead of X?" not "What if we had chosen Y and market doubled and competitor failed?" Isolate causal factor.

3. **Avoid hindsight bias**: Pre-mortem assumes failure, but don't just list things that went wrong in similar past failures. Generate new failure modes specific to this context.

4. **Specify mechanism**: Don't just state outcome ("sales would be higher"), explain HOW ("sales would be higher because lower price → higher conversion → more customers despite lower margin").

5. **Assign probabilities** (scenarios): Don't treat all scenarios as equally likely. Estimate rough probabilities (e.g., 60% baseline, 25% pessimistic, 15% optimistic). Avoids equal-weight fallacy.

6. **Time horizon clarity**: Specify WHEN in future. "Product fails" is vague. "In 6 months, adoption <1000 users" is concrete. Enables tracking.

7. **Extract actions, not just stories**: Scenarios are useless without implications. Always end with "so what should we do?" Prepare, hedge, pivot, or double-down.

8. **Update scenarios**: Reality evolves. Quarterly review: which scenario is unfolding? Update probabilities and plans accordingly.

**Common pitfalls:**

- ❌ **Confusing counterfactual with fantasy**: "What if we had $100M funding from start?" vs. realistic "What if we had raised $2M seed instead of $1M?"
- ❌ **Too many scenarios**: 10 scenarios = analysis paralysis. Stick to 2-4 meaningful, distinct futures.
- ❌ **Scenarios too similar**: Three scenarios that differ only in magnitude (10% growth, 15% growth, 20% growth). Need qualitatively different worlds.
- ❌ **No causal mechanism**: "Sales would be 2× higher" without explaining why. Must specify how change leads to outcome.
- ❌ **Hindsight bias in pre-mortem**: Just listing past failures. Need to imagine new, context-specific risks.
- ❌ **Ignoring low-probability, high-impact**: "Black swan won't happen" until it does. Include tail risks.

## Quick Reference

**Counterfactual vs. Hypothetical:**

| Type | Direction | Question | Purpose | Example |
|------|-----------|----------|---------|---------|
| **Counterfactual** | Backward (past) | "What would have happened if...?" | Understand causality, learn from past | "What if we had launched in EU first?" |
| **Hypothetical** | Forward (future) | "What could happen if...?" | Explore futures, prepare for uncertainty | "What if competitor launches free tier?" |

**Scenario types:**

| Type | # Scenarios | Structure | Best For |
|------|-------------|-----------|----------|
| **Three scenarios** | 3 | Optimistic, Baseline, Pessimistic | General forecasting, strategic planning |
| **2×2 matrix** | 4 | Two uncertainties create quadrants | Exploring interaction of two drivers |
| **Cone of uncertainty** | Continuous | Range widens over time | Long-term planning (5-10 years) |
| **Pre-mortem** | 1 | Imagine failure, list causes | Risk identification before launch |
| **Stress test** | 2-4 | Extreme scenarios (best/worst) | Decision robustness testing |

**Pre-mortem process** (6 steps):

1. **Set future date**: "It's 6 months from now..."
2. **Assume failure**: "...the project has failed completely."
3. **Individual brainstorm**: Each person writes 3-5 reasons (5 min, silent)
4. **Share and consolidate**: Round-robin sharing, group similar items
5. **Vote on top risks**: Dot voting or force-rank top 5 causes
6. **Mitigate now**: For each top risk, assign owner and mitigation action

**2×2 Scenario Matrix** (example):

**Uncertainties**: (1) Market adoption rate, (2) Regulatory environment

|                     | Slow Adoption | Fast Adoption |
|---------------------|---------------|---------------|
| **Strict Regulation** | "Constrained Growth" | "Regulated Scale" |
| **Loose Regulation** | "Patient Build" | "Wild West Growth" |

**Assumption reversal questions:**

- "What if our biggest advantage is actually a liability?"
- "What if the problem we're solving isn't the real problem?"
- "What if our target customer is wrong?"
- "What if cheaper/slower is better than premium/fast?"
- "What if we're too early/too late, not right on time?"

**Inputs required:**
- **Focal decision or event**: What are you analyzing?
- **Key uncertainties**: What factors most shape outcomes?
- **Time horizon**: How far into future/past?
- **Constraints**: What must remain fixed vs. what can vary?
- **Stakeholders**: Who should contribute scenarios?

**Outputs produced:**
- `counterfactual-analysis.md`: Alternative history analysis with causal insights
- `pre-mortem-risks.md`: List of potential failure modes and mitigations
- `scenarios.md`: 2-4 future scenarios with narratives and implications
- `action-plan.md`: Decisions and preparations based on scenario insights
