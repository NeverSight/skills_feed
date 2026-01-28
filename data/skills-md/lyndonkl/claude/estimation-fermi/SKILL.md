---
name: estimation-fermi
description: Use when making quick order-of-magnitude estimates under uncertainty (market sizing, resource planning, feasibility checks), decomposing complex quantities into estimable parts, bounding unknowns with upper/lower limits, sanity-checking strategic assumptions, or when user mentions Fermi estimation, back-of-envelope calculation, order of magnitude, ballpark estimate, triangulation, or needs to assess feasibility before detailed analysis.
---
# Fermi Estimation

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Fermi estimation provides rapid order-of-magnitude answers to seemingly impossible questions by decomposing them into smaller, estimable parts. This skill guides you through decomposition strategies, bounding techniques, sanity checks, and triangulation to make defensible estimates when data is scarce, time is limited, or precision is unnecessary for the decision at hand.

## When to Use

Use this skill when:

- **Market sizing**: Estimating TAM/SAM/SOM for product launch, addressable market for new feature, competitive market share
- **Resource planning**: Infrastructure capacity (servers, storage, bandwidth), staffing needs, budget allocation, inventory requirements
- **Feasibility checks**: Can we build this in 6 months? Will customers pay $X? Is this market big enough?
- **Strategic decisions**: Build vs buy tradeoffs, enter new market assessment, fundraising/runway calculations, pricing validation
- **Business metrics**: Revenue projections, customer acquisition costs, LTV estimates, unit economics, break-even analysis
- **Impact assessment**: Carbon footprint, energy consumption, social reach, cost savings from initiative
- **Interview questions**: Consulting case interviews (piano tuners in Chicago), product sense questions, analytical reasoning tests
- **Quick validation**: Sanity-checking detailed models, pressure-testing assumptions, getting directional answer before investing in precision

Trigger phrases: "ballpark estimate", "order of magnitude", "back-of-envelope", "roughly how many", "feasibility check", "gut check", "triangulate", "sanity check"

## What Is It?

Fermi estimation (named after physicist Enrico Fermi) breaks down complex unknowns into simpler components that can be estimated using common knowledge, constraints, and reasoning. The goal is not precision but being "right to within a factor of 10" quickly.

**Quick example:**

**Question**: How many piano tuners are in Chicago?

**Fermi decomposition**:
1. **Population**: Chicago ~3 million people
2. **Households**: 3M people ÷ 3 people/household = 1M households
3. **Pianos**: ~1 in 20 households has piano = 50,000 pianos
4. **Tuning frequency**: Piano tuned once/year on average
5. **Tunings needed**: 50,000 tunings/year
6. **Tuner capacity**: Tuner works 250 days/year, 4 tunings/day = 1,000 tunings/year per tuner
7. **Tuners needed**: 50,000 ÷ 1,000 = **~50 piano tuners**

**Actual**: ~80-100 piano tuners in Chicago (within order of magnitude ✓)

**Business example - Market sizing:**

**Question**: What's the TAM for a B2B sales automation SaaS in the US?

**Decomposition**:
1. **Total businesses in US**: ~30M
2. **With sales teams**: ~10% = 3M businesses
3. **With >10 employees** (can afford SaaS): ~2M businesses
4. **Addressable** (tech-savvy, not enterprise with custom solutions): ~500k businesses
5. **Price point**: $500/month average
6. **TAM**: 500k × $500/month × 12 = **$3B/year**

**Validation**: Quick search confirms B2B sales tech market ~$5-7B (same order of magnitude ✓)

## Workflow

Copy this checklist and track your progress:

```
Fermi Estimation Progress:
- [ ] Step 1: Clarify the question and define metric
- [ ] Step 2: Decompose into estimable components
- [ ] Step 3: Estimate components using anchors
- [ ] Step 4: Bound with upper/lower limits
- [ ] Step 5: Calculate and sanity-check
- [ ] Step 6: Triangulate with alternate path
```

**Step 1: Clarify the question and define metric**

Restate question precisely (units, scope, timeframe). Identify what decision hinges on estimate (directional answer sufficient? order of magnitude?). See [resources/template.md](resources/template.md#clarification-template) for question clarification framework.

**Step 2: Decompose into estimable components**

Break unknown into product/quotient of knowable parts. Choose decomposition strategy (top-down, bottom-up, dimensional analysis). See [resources/template.md](resources/template.md#decomposition-strategies) for decomposition patterns.

**Step 3: Estimate components using anchors**

Ground estimates in known quantities (population, physical constants, market sizes, personal experience). State assumptions explicitly. See [resources/methodology.md](resources/methodology.md#anchoring-techniques) for anchor sources and calibration.

**Step 4: Bound with upper/lower limits**

Calculate optimistic (upper) and pessimistic (lower) bounds to bracket answer. Check if decision changes across range. See [resources/methodology.md](resources/methodology.md#bounding-techniques) for constraint-based bounding.

**Step 5: Calculate and sanity-check**

Compute estimate, round to 1-2 significant figures. Sanity-check against reality (does answer pass smell test?). See [resources/template.md](resources/template.md#sanity-check-template) for validation criteria.

**Step 6: Triangulate with alternate path**

Re-estimate using different decomposition to validate. Check if both paths yield same order of magnitude. Validate using [resources/evaluators/rubric_estimation_fermi.json](resources/evaluators/rubric_estimation_fermi.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Market Sizing (TAM/SAM/SOM)**
- **Decomposition**: Total population → Target segment → Addressable → Reachable → Price point
- **Anchors**: Census data, industry reports, analogous markets, penetration rates
- **Bounds**: Optimistic (high penetration, premium pricing) vs Pessimistic (low penetration, discount pricing)
- **Sanity check**: Compare to public company revenues in space, VC market size estimates
- **Example**: E-commerce TAM = US population × online shopping % × avg spend/year

**Pattern 2: Infrastructure Capacity**
- **Decomposition**: Users → Requests per user → Compute/storage per request → Overhead
- **Anchors**: Similar services (Instagram, Twitter), known capacity (EC2 instance limits), load testing data
- **Bounds**: Peak (Black Friday) vs Average load, Growth trajectory (2x/year vs 10x/year)
- **Sanity check**: Cost per user should be < LTV, compare to public cloud bills of similar scale
- **Example**: Servers needed = (DAU × requests/user × ms/request) ÷ (instance capacity × utilization)

**Pattern 3: Staffing/Headcount**
- **Decomposition**: Work to be done (features, tickets, customers) → Productivity per person → Overhead (meetings, support)
- **Anchors**: Industry benchmarks (engineer per X users, support agent per Y customers), team velocity, hiring timelines
- **Bounds**: Experienced team (high productivity) vs New team (ramp time), Aggressive timeline (crunch) vs Sustainable pace
- **Sanity check**: Headcount growth should match revenue growth curve, compare to peers at similar scale
- **Example**: Engineers needed = (Story points in roadmap ÷ Velocity per engineer) + 20% overhead

**Pattern 4: Financial Projections**
- **Decomposition**: Revenue = Users × Conversion rate × ARPU, Costs = COGS + Sales/Marketing + R&D + G&A
- **Anchors**: Cohort data, industry CAC/LTV benchmarks, comparable company metrics, historical growth
- **Bounds**: Bull case (high growth, efficient scaling) vs Bear case (slow growth, rising costs)
- **Sanity check**: Margins should approach industry norms at scale, growth rate should follow S-curve not exponential forever
- **Example**: Year 2 revenue = Year 1 revenue × (1 + growth rate) × (1 - churn)

**Pattern 5: Impact Assessment**
- **Decomposition**: Total impact = Units affected × Impact per unit × Duration
- **Anchors**: Emission factors (kg CO2/kWh), conversion rates (program → behavior change), precedent studies
- **Bounds**: Conservative (low adoption, small effect) vs Optimistic (high adoption, large effect)
- **Sanity check**: Impact should scale linearly or sub-linearly (diminishing returns), compare to similar interventions
- **Example**: Carbon saved = (Users switching × Miles driven/year × Emissions/mile) - Baseline

## Guardrails

**Critical requirements:**

1. **State assumptions explicitly**: Every Fermi estimate rests on assumptions. Make them visible ("Assuming 250 workdays/year", "If conversion rate ~3%"). Allows others to challenge/refine. Unstated assumptions create false precision.

2. **Aim for order of magnitude, not precision**: Goal is 10^X, not X.XX. Round to 1-2 significant figures (50 not 47.3, 3M not 2,847,291). False precision wastes time and misleads. If decision needs precision, don't use Fermi—get real data.

3. **Decompose until components are estimable**: Break down until you reach quantities you can estimate from knowledge/experience. If a component is still "how would I know that?", decompose further. Avoid plugging in wild guesses for complex sub-problems.

4. **Use multiple paths (triangulation)**: Estimate same quantity via different decompositions (top-down vs bottom-up, supply-side vs demand-side). If paths agree within factor of 3, confidence increases. If they differ by 10x+, investigate which decomposition is flawed.

5. **Bound the answer**: Calculate optimistic and pessimistic cases to bracket reality. If decision is same across range (market is $1B or $10B, either way we enter), bounds matter less. If decision flips (profitable at $10M, not at $1M), need precision or better estimate.

6. **Sanity-check against reality**: Does answer pass smell test? Compare to known quantities (your estimate for Starbucks revenue should be within 10x of actual ~$35B). Use dimensional analysis (units should cancel correctly). Check extreme cases (what if everyone did X? does it break physics?).

7. **Calibrate on known problems**: Practice on questions with verifiable answers (US population, Disney World attendance, wheat production). Identify your biases (overestimate? underestimate? anchoring?). Improves future estimates.

8. **Acknowledge uncertainty ranges**: Express estimates as ranges or confidence intervals when appropriate ("10-100k users", "likely $1-5M"). Communicates epistemic humility. Avoids false precision trap.

**Common pitfalls:**

- ❌ **Anchoring on the wrong number**: Using irrelevant or biased starting point. If someone says "Is it 1 million?" you anchor there even if no reason to.
- ❌ **Double-counting**: Including same quantity twice in decomposition (counting both businesses and employees when businesses already includes employees).
- ❌ **Unit errors**: Mixing per-day and per-year, confusing millions and billions, wrong currency conversion. Always check units.
- ❌ **Survivor bias**: Estimating based on successful cases (average startup revenue from unicorns, not including failures).
- ❌ **Linear extrapolation**: Assuming linear growth when exponential (or vice versa). Growth rates change over time.
- ❌ **Ignoring constraints**: Physical limits (can't exceed speed of light), economic limits (market can't grow faster than GDP forever).

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: Clarification framework, decomposition strategies, estimation template, sanity-check criteria
- **[resources/methodology.md](resources/methodology.md)**: Anchoring techniques, bounding methods, triangulation approaches, calibration exercises
- **[resources/evaluators/rubric_estimation_fermi.json](resources/evaluators/rubric_estimation_fermi.json)**: Quality criteria for decomposition, assumptions, bounds, sanity checks

**Common Anchors:**

**Demographics:**
- US population: ~330M, Households: ~130M, Labor force: ~165M
- World population: ~8B, Urban: ~55%, Internet users: ~5B

**Business:**
- Fortune 500 revenue: $100k to $600B (median ~$30B)
- Startup valuations: Seed ~$5-10M, Series A ~$30-50M, Unicorn >$1B
- SaaS metrics: CAC ~$1-5k, LTV/CAC ratio >3, Churn <5%/year

**Technology:**
- AWS EC2 instance: ~10k requests/sec, S3 storage: $0.023/GB/month
- Mobile app: ~5-10 screens/day per user, 50-100 API calls/session
- Website: ~2-3 pages/session, 1-2min session duration

**Physical:**
- Person: ~70kg, 2000 kcal/day, 8 hours sleep
- Car: ~25 mpg, 12k miles/year, $30k new, 200k mile lifetime
- House: ~2000 sq ft, $300k median US, 30-year mortgage

**Conversion factors:**
- 1 year ≈ 250 workdays ≈ 2000 work hours
- 1 million seconds ≈ 11.5 days, 1 billion seconds ≈ 32 years
- 1 mile ≈ 1.6 km, 1 kg ≈ 2.2 lbs, 1 gallon ≈ 3.8 liters

**Decomposition Strategies:**

- **Top-down**: Start with total population, filter down (US population → Car owners → EV buyers)
- **Bottom-up**: Start with unit, scale up (1 store revenue × Number of stores)
- **Rate × Time**: Flow rate × Duration (Customers/day × Days/year)
- **Density × Area/Volume**: Concentration × Space (People/sq mile × City area)
- **Analogous scaling**: Known similar system, adjust for size (Competitor revenue × Our market share)

**Typical estimation time:**
- Simple question (1-2 levels of decomposition): 3-5 minutes
- Market sizing (3-4 levels): 10-15 minutes
- Complex business case (multiple metrics, triangulation): 20-30 minutes

**When to escalate:**

- Decision requires precision (< factor of 2 uncertainty)
- Estimate spans >2 orders of magnitude even with bounds
- No reasonable decomposition path (too many unknowns)
- Stakeholders need confidence intervals and statistical rigor
→ Invest in data collection, detailed modeling, expert consultation

**Inputs required:**

- **Question** (what are we estimating? units? scope?)
- **Decision context** (what decision hinges on this estimate? required precision?)
- **Known anchors** (what related quantities do we know?)

**Outputs produced:**

- `estimation-fermi.md`: Question, decomposition, assumptions, calculation, bounds, sanity check, triangulation, final estimate with confidence range
