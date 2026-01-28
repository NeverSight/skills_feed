---
name: expected-value
description: Use when making decisions under uncertainty with quantifiable outcomes, comparing risky options (investments, product bets, strategic choices), prioritizing projects by expected return, assessing whether to take a gamble, or when user mentions expected value, EV calculation, risk-adjusted return, probability-weighted outcomes, decision tree, or needs to choose between uncertain alternatives.
---
# Expected Value

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Expected Value (EV) provides a framework for making rational decisions under uncertainty by calculating the probability-weighted average of all possible outcomes. This skill guides you through identifying scenarios, estimating probabilities and payoffs, computing expected values, and interpreting results while accounting for risk preferences and real-world constraints.

## When to Use

Use this skill when:

- **Investment decisions**: Should we invest in project A (high risk, high return) or project B (low risk, low return)?
- **Product bets**: Launch feature X (uncertain adoption) or focus on feature Y (safer bet)?
- **Resource allocation**: Which initiatives have highest expected return given limited budget?
- **Go/no-go decisions**: Is expected value of launching positive after accounting for probabilities of success/failure?
- **Pricing & negotiation**: What's expected value of accepting vs. rejecting an offer?
- **Insurance & hedging**: Should we buy insurance (guaranteed small loss) vs. risk large loss?
- **A/B test interpretation**: Which variant has higher expected conversion rate accounting for uncertainty?
- **Portfolio optimization**: Diversify to maximize expected return for given risk tolerance?

Trigger phrases: "expected value", "EV calculation", "risk-adjusted return", "probability-weighted outcomes", "decision tree", "should I take this gamble", "compare risky options"

## What Is It?

**Expected Value (EV)** = Σ (Probability of outcome × Value of outcome)

For each possible outcome, multiply its probability by its value (payoff), then sum across all outcomes.

**Core formula**:
```
EV = (p₁ × v₁) + (p₂ × v₂) + ... + (pₙ × vₙ)

where:
- p₁, p₂, ..., pₙ are probabilities of each outcome (must sum to 1.0)
- v₁, v₂, ..., vₙ are values (payoffs) of each outcome
```

**Quick example:**

**Scenario**: Launch new product feature. Estimate 60% chance of success ($100k revenue), 40% chance of failure (-$20k sunk cost).

**Calculation**:
- EV = (0.6 × $100k) + (0.4 × -$20k)
- EV = $60k - $8k = **$52k**

**Interpretation**: On average, launching this feature yields $52k. Positive EV → launch is rational choice (if risk tolerance allows).

**Core benefits:**
- **Quantitative comparison**: Compare disparate options on same scale (expected return)
- **Explicit uncertainty**: Forces estimation of probabilities instead of gut feel
- **Repeatable framework**: Same method applies to investments, products, hiring, etc.
- **Risk-adjusted**: Weights outcomes by likelihood, not just best/worst case
- **Portfolio thinking**: Optimal long-term strategy is maximize expected value over many decisions

## Workflow

Copy this checklist and track your progress:

```
Expected Value Analysis Progress:
- [ ] Step 1: Define decision and alternatives
- [ ] Step 2: Identify possible outcomes
- [ ] Step 3: Estimate probabilities
- [ ] Step 4: Estimate payoffs (values)
- [ ] Step 5: Calculate expected values
- [ ] Step 6: Interpret and adjust for risk preferences
```

**Step 1: Define decision and alternatives**

What decision are you making? What are the mutually exclusive options? See [resources/template.md](resources/template.md#decision-framing-template).

**Step 2: Identify possible outcomes**

For each alternative, what could happen? List scenarios from best case to worst case. See [resources/template.md](resources/template.md#outcome-identification-template).

**Step 3: Estimate probabilities**

What's the probability of each outcome? Use base rates, reference classes, expert judgment, data. See [resources/methodology.md](resources/methodology.md#1-probability-estimation-techniques).

**Step 4: Estimate payoffs (values)**

What's the value (gain or loss) of each outcome? Quantify in dollars, time, utility. See [resources/methodology.md](resources/methodology.md#2-payoff-quantification).

**Step 5: Calculate expected values**

Multiply probabilities by payoffs, sum across outcomes for each alternative. See [resources/template.md](resources/template.md#ev-calculation-template).

**Step 6: Interpret and adjust for risk preferences**

Choose option with highest EV? Or adjust for risk aversion, non-monetary factors, strategic value. See [resources/methodology.md](resources/methodology.md#4-risk-preferences-and-utility).

Validate using [resources/evaluators/rubric_expected_value.json](resources/evaluators/rubric_expected_value.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Investment Decision (Discrete Outcomes)**
- **Structure**: Go/no-go choice with 3-5 discrete scenarios (best, base, worst case)
- **Use case**: Product launch, hire vs. not hire, accept investment offer, buy vs. lease
- **Pros**: Simple, intuitive, easy to communicate (decision tree visualization)
- **Cons**: Oversimplifies continuous distributions, binary framing may miss nuance
- **Example**: Launch product feature (60% success $100k, 40% fail -$20k) → EV = $52k

**Pattern 2: Portfolio Allocation (Multiple Options)**
- **Structure**: Allocate budget across N projects, each with own EV and risk profile
- **Use case**: Venture portfolio, R&D budget, marketing spend allocation, team capacity
- **Pros**: Diversification reduces variance, can optimize for risk/return tradeoff
- **Cons**: Requires estimates for many variables, correlations matter (not independent)
- **Example**: Invest in 3 startups ($50k each), EVs = [$20k, $15k, -$10k]. Total EV = $25k. Diversified portfolio reduces risk vs. single $150k bet.

**Pattern 3: Sequential Decision (Decision Tree)**
- **Structure**: Series of decisions over time, outcomes of early decisions affect later options
- **Use case**: Clinical trials (Phase I → II → III), staged investment, explore then exploit
- **Pros**: Captures optionality (can stop if early results bad), fold-back induction finds optimal strategy
- **Cons**: Tree grows exponentially, need probabilities for all branches
- **Example**: Phase I drug trial (70% pass, $1M cost) → if pass, Phase II (50% pass, $5M) → if pass, Phase III (40% approve, $50M revenue). Calculate EV working backwards.

**Pattern 4: Continuous Distribution (Monte Carlo)**
- **Structure**: Outcomes are continuous (revenue could be $0-$1M), use probability distributions
- **Use case**: Financial modeling, project timelines, resource planning, sensitivity analysis
- **Pros**: Captures full uncertainty, avoids discrete scenario bias, provides confidence intervals
- **Cons**: Requires distributional assumptions, computationally intensive, harder to communicate
- **Example**: Revenue ~ Normal($500k, $100k std dev). Run 10,000 simulations → mean = $510k, 90% CI = [$350k, $670k].

**Pattern 5: Competitive Game (Payoff Matrix)**
- **Structure**: Your outcome depends on competitor's choice, create payoff matrix
- **Use case**: Pricing strategy, product launch timing, negotiation, auction bidding
- **Pros**: Incorporates strategic interaction, finds Nash equilibrium
- **Cons**: Requires estimating competitor's probabilities and payoffs, game-theoretic complexity
- **Example**: Price high vs. low, competitor prices high vs. low → 2×2 matrix. Calculate EV for each strategy given beliefs about competitor.

## Guardrails

**Critical requirements:**

1. **Probabilities must sum to 1.0**: If you list outcomes, their probabilities must be exhaustive (cover all possibilities) and mutually exclusive (no overlap). Check: p₁ + p₂ + ... + pₙ = 1.0.

2. **Don't use EV for one-shot, high-stakes decisions without risk adjustment**: EV is long-run average. For rare, irreversible decisions (bet life savings, critical surgery), consider risk aversion. A 1% chance of $1B (EV = $10M) doesn't mean you should bet your house.

3. **Quantify uncertainty, don't hide it**: Probabilities and payoffs are estimates, often uncertain. Use ranges (optimistic/pessimistic), sensitivity analysis, or distributions. Don't pretend false precision.

4. **Consider non-monetary value**: EV in dollars is convenient, but some outcomes have utility not captured by money (reputation, learning, optionality, morale). Convert to common scale or use multi-attribute utility.

5. **Probabilities must be calibrated**: Don't use gut-feel probabilities without grounding. Use base rates, reference classes, data, expert forecasts. Test: are your "70% confident" predictions right 70% of the time?

6. **Account for correlated outcomes**: If outcomes aren't independent (economic downturn affects all portfolio companies), correlation reduces diversification benefit. Model dependencies.

7. **Time value of money**: Payoffs at different times aren't equivalent. Discount future cash flows to present value (NPV = Σ CF_t / (1+r)^t). EV should use NPV, not nominal values.

8. **Stopping rules and option value**: In sequential decisions, fold-back induction finds optimal strategy. Don't ignore option to stop early, pivot, or wait for more information.

**Common pitfalls:**

- ❌ **Ignoring risk aversion**: EV($100k, 50/50) = EV($50k, certain) but most prefer certain $50k. Use utility functions for risk-averse agents.
- ❌ **Anchor on single scenario**: "Best case is $1M!" → but probability is 5%. Focus on EV, not cherry-picked scenarios.
- ❌ **False precision**: "Probability = 67.3%" when you're guessing. Use ranges, express uncertainty.
- ❌ **Sunk cost fallacy**: Past costs are sunk, don't include in forward-looking EV. Only future costs/benefits matter.
- ❌ **Ignoring tail risk**: Low-probability, high-impact events (0.1% chance of -$10M) can dominate EV. Don't round to zero.
- ❌ **Static analysis**: Assume you can't update beliefs or change course. Real decisions allow learning and pivoting.

## Quick Reference

**Key formulas:**

**Expected Value**: EV = Σ (pᵢ × vᵢ) where p = probability, v = value

**Expected Utility** (for risk aversion): EU = Σ (pᵢ × U(vᵢ)) where U = utility function
- Risk-neutral: U(x) = x (EV = EU)
- Risk-averse: U(x) = √x or U(x) = log(x) (concave)
- Risk-seeking: U(x) = x² (convex)

**Net Present Value**: NPV = Σ (CF_t / (1+r)^t) where CF = cash flow, r = discount rate, t = time period

**Variance** (risk measure): Var = Σ (pᵢ × (vᵢ - EV)²)

**Standard Deviation**: σ = √Var

**Coefficient of Variation** (risk/return ratio): CV = σ / EV (lower = better risk-adjusted return)

**Breakeven probability**: p* where EV = 0. Solve: p* × v_success + (1-p*) × v_failure = 0.

**Decision rules**:
- **Maximize EV**: Choose option with highest EV (risk-neutral, repeated decisions)
- **Maximize EU**: Choose option with highest expected utility (risk-averse, incorporates preferences)
- **Minimax regret**: Minimize maximum regret across scenarios (conservative, avoid worst mistake)
- **Satisficing**: Choose first option above threshold EV (bounded rationality)

**Sensitivity analysis questions**:
- How much do probabilities need to change to flip decision?
- What's EV in best case? Worst case? Which variables have most impact?
- At what probability does EV break even (EV = 0)?

**Key resources:**
- **[resources/template.md](resources/template.md)**: Decision framing, outcome identification, EV calculation templates, sensitivity analysis
- **[resources/methodology.md](resources/methodology.md)**: Probability estimation, payoff quantification, decision tree analysis, utility functions
- **[resources/evaluators/rubric_expected_value.json](resources/evaluators/rubric_expected_value.json)**: Quality criteria (scenario completeness, probability calibration, payoff quantification, EV interpretation)

**Inputs required:**
- **Decision**: What are you choosing between? (2+ mutually exclusive alternatives)
- **Outcomes**: For each alternative, what could happen? (3-5 scenarios typical)
- **Probabilities**: How likely is each outcome? (sum to 1.0)
- **Payoffs**: What's the value (gain/loss) of each outcome? (dollars, time, utility)

**Outputs produced:**
- `expected-value-analysis.md`: Decision framing, outcome scenarios with probabilities and payoffs, EV calculations, sensitivity analysis, recommendation with risk considerations
