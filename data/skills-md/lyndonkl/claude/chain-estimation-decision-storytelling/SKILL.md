---
name: chain-estimation-decision-storytelling
description: Use when making high-stakes decisions under uncertainty that require stakeholder buy-in. Invoke when evaluating strategic options (build vs buy, market entry, resource allocation), quantifying tradeoffs with uncertain outcomes, justifying investments with expected value analysis, pitching recommendations to decision-makers, or creating business cases with cost-benefit estimates. Use when user mentions "should we", "ROI analysis", "make a case for", "evaluate options", "expected value", "justify decision", or needs to combine estimation, decision analysis, and persuasive communication.
---

# Chain Estimation → Decision → Storytelling

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Chain Estimation → Decision → Storytelling?](#what-is-chain-estimation--decision--storytelling)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Systematically quantify uncertain choices, make defensible decisions using expected value analysis, and communicate recommendations through persuasive narratives. This meta-skill chains estimation → decision → storytelling to transform ambiguous options into clear, stakeholder-ready recommendations.

## When to Use This Skill

- Evaluating strategic options with uncertain outcomes (build vs buy, market entry, product investment)
- Creating business cases for resource allocation or budget approval
- Justifying technical decisions with cost-benefit analysis (architecture, tooling, infrastructure)
- Pitching recommendations to executives or board with quantified tradeoffs
- Making investment decisions with ROI projections and risk assessment
- Prioritizing initiatives with expected value comparison
- Evaluating partnerships, acquisitions, or major contracts
- Designing pricing strategies with revenue/cost modeling
- Resource planning with capacity and utilization estimates
- Risk mitigation decisions with probability-weighted outcomes
- Product roadmap decisions with effort/impact estimates
- Organizational change decisions (hiring, restructuring, policy)
- Technology adoption with TCO and benefit quantification
- Market positioning decisions with competitive analysis
- Portfolio management with probability-adjusted returns

**Trigger phrases:** "should we", "evaluate options", "make a case for", "ROI analysis", "expected value", "justify decision", "quantify tradeoffs", "pitch to", "business case", "cost-benefit", "probability-weighted"

## What is Chain Estimation → Decision → Storytelling?

A three-phase meta-skill that combines:

1. **Estimation**: Quantify uncertain variables with ranges, probabilities, and sensitivity analysis
2. **Decision**: Apply expected value, decision trees, or scoring to identify best option
3. **Storytelling**: Package analysis into compelling narrative for stakeholders

**Quick Example:**

```markdown
# Should we build custom analytics or buy a SaaS tool?

## Estimation
Build custom: $200k-$400k dev cost (60% likely $300k), $50k/year maintenance
Buy SaaS: $120k/year subscription, $20k implementation

## Decision
Expected 3-year cost:
- Build: $300k + (3 × $50k) = $450k
- Buy: $20k + (3 × $120k) = $380k
- Difference: $70k savings with Buy

Expected value with risk adjustment:
- Build: 30% chance of 2x cost overrun → $510k expected
- Buy: 95% confidence in pricing → $380k expected
- Recommendation: Buy (lower cost, lower risk)

## Story
"We evaluated building custom analytics vs. buying a SaaS solution. While building seems cheaper initially ($300k vs. $380k over 3 years), custom development carries significant risk—30% of similar projects experience 2x cost overruns, bringing expected cost to $510k. The SaaS solution offers predictable pricing, faster time-to-value (2 months vs. 8 months), and proven reliability. Recommendation: Buy the SaaS tool, saving $130k in expected costs and delivering value 6 months earlier."
```

## Workflow

Copy this checklist and track your progress:

```
Chain Estimation → Decision → Storytelling Progress:
- [ ] Step 1: Clarify decision and gather inputs
- [ ] Step 2: Estimate uncertain variables
- [ ] Step 3: Analyze decision with expected value
- [ ] Step 4: Craft persuasive narrative
- [ ] Step 5: Validate and deliver
```

**Step 1: Clarify decision and gather inputs**

Define the choice (what decision needs to be made?), identify alternatives (2-5 options to compare), list uncertainties (what variables are unknown or probabilistic?), determine audience (who needs to be convinced?), and clarify constraints (budget, timeline, requirements). Ensure the decision is actionable and the options are mutually exclusive.

**Step 2: Estimate uncertain variables**

For each alternative, quantify costs (fixed, variable, opportunity), estimate benefits (revenue, savings, productivity), assign probabilities to scenarios (best case, base case, worst case), and perform sensitivity analysis (which inputs matter most?). Use ranges rather than point estimates. For simple cases → Use `resources/template.md` for structured estimation. For complex cases → Study `resources/methodology.md` for advanced techniques (Monte Carlo, decision trees, real options).

**Step 3: Analyze decision with expected value**

Calculate expected outcomes for each alternative (probability-weighted averages), compare using decision criteria (NPV, payback period, IRR, utility), identify dominant option (best expected value or risk-adjusted return), and test robustness (does conclusion hold across reasonable input ranges?). Document assumptions explicitly. See [Common Patterns](#common-patterns) for decision-type specific approaches.

**Step 4: Craft persuasive narrative**

Structure story with: problem statement (why this decision matters), alternatives considered (show you did the work), analysis summary (key numbers and logic), recommendation (clear choice with reasoning), next steps (what happens if approved). Tailor to audience: executives want bottom line and risks, technical teams want methodology and assumptions, finance wants numbers and sensitivity.

**Step 5: Validate and deliver**

Self-check using `resources/evaluators/rubric_chain_estimation_decision_storytelling.json`. Verify: estimates are justified with sources/logic, probabilities are calibrated (not overconfident), expected value calculation is correct, sensitivity analysis identifies key drivers, narrative is clear and persuasive, assumptions are stated explicitly, risks and limitations are acknowledged. Minimum standard: Score ≥ 3.5. Create `chain-estimation-decision-storytelling.md` output file with full analysis and recommendation.

## Common Patterns

**For build vs buy decisions:**
- Estimate: Development cost (effort × rate), maintenance cost, SaaS subscription, implementation cost
- Decision: 3-5 year TCO, risk-adjusted for schedule overruns and feature gaps
- Story: "Build gives us control but costs $X more and takes Y months longer..."

**For market entry decisions:**
- Estimate: TAM/SAM/SOM, CAC, LTV, time-to-profitability
- Decision: Expected NPV with market uncertainty (optimistic/pessimistic scenarios)
- Story: "If we enter now, base case is $X revenue by year 3, but if market adoption is slower..."

**For resource allocation:**
- Estimate: Cost per initiative, expected impact (revenue, cost savings, strategic value)
- Decision: Impact/effort scoring or expected value ranking
- Story: "Given $X budget, these 3 initiatives deliver $Y expected return vs. $Z for alternatives..."

**For technology decisions:**
- Estimate: Migration cost, operational cost, performance improvement, risk reduction
- Decision: TCO over 3-5 years plus risk-adjusted benefits
- Story: "Migrating to X costs $Y upfront but saves $Z annually and reduces outage risk from..."

**For hiring/staffing decisions:**
- Estimate: Compensation, recruiting cost, ramp time, productivity impact
- Decision: Cost per incremental output vs. alternatives (contractors, vendors, automation)
- Story: "Adding 3 engineers at $X cost delivers $Y additional capacity, enabling..."

## Guardrails

**Do:**
- Use ranges for uncertain estimates (not false precision)
- Assign probabilities based on data or explicit reasoning
- Calculate expected value correctly (probability-weighted outcomes)
- Perform sensitivity analysis (test assumptions)
- State assumptions explicitly
- Acknowledge risks and limitations
- Tailor narrative to audience (exec vs technical vs finance)
- Include "what would change my mind" conditions
- Show your work (transparent methodology)
- Test robustness (does conclusion hold with different assumptions?)

**Don't:**
- Use single-point estimates for highly uncertain variables
- Claim false precision ("$347,291" when uncertainty is ±50%)
- Ignore risk or downside scenarios
- Cherry-pick optimistic assumptions
- Hide assumptions or methodology
- Overstate confidence in estimates
- Skip sensitivity analysis
- Make recommendation before analyzing alternatives
- Use jargon without defining terms for audience
- Forget to state next steps or decision criteria

**Common Pitfalls:**
- **Anchoring bias**: First estimate becomes "default" without testing alternatives
- **Optimism bias**: Best-case scenarios feel more likely than they are
- **Sunk cost fallacy**: Including past costs that shouldn't affect forward-looking decision
- **Overconfidence**: Narrow ranges that don't reflect true uncertainty
- **Ignoring opportunity cost**: Not considering what else could be done with resources
- **Analysis paralysis**: Spending too much time estimating vs. deciding with available info

## Quick Reference

- **Template**: `resources/template.md` - Structured estimation → decision → story framework
- **Methodology**: `resources/methodology.md` - Advanced techniques (Monte Carlo, decision trees, real options)
- **Examples**: `resources/examples/` - Worked examples (build vs buy, market entry, hiring decision)
- **Quality rubric**: `resources/evaluators/rubric_chain_estimation_decision_storytelling.json`
- **Output file**: `chain-estimation-decision-storytelling.md`
- **Key distinction**: Combines quantitative rigor (estimation, expected value) with qualitative persuasion (narrative, stakeholder alignment)
- **When to use**: High-stakes decisions with uncertainty that need buy-in (not routine choices or purely data-driven optimizations)
