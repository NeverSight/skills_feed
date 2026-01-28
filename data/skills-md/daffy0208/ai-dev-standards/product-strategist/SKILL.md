---
name: Product Strategist
description: Validate product-market fit and strategic direction. Use when defining new products, validating problem-solution fit, prioritizing features, or making build-vs-buy decisions. Focuses on discovery and validation before development.
version: 1.0.0
---

# Product Strategist

Validate that products solve **real problems** for **viable markets** before investing in development.

## Core Principle

**Evidence over intuition.** Test the riskiest assumptions first, fail fast, and validate with real user behavior—not opinions.

## 5-Phase Validation Process

### Phase 1: Problem Validation

**Goal**: Confirm the problem is frequent, painful, and urgent enough that users will pay to solve it

**Activities**:

- Define problem hypothesis: What problem are you solving?
- Identify target customer segments
- Conduct customer discovery interviews (10-15 per segment)
- Quantify problem severity: time/money cost to users
- Document current workarounds and their pain points

**The "Mom Test" Questions**:

✅ **Good Questions** (reveal behavior):

- "Tell me about the last time you encountered [problem]."
- "How are you currently solving this?"
- "How much time/money do you spend on this problem?"
- "What have you tried that didn't work?"

❌ **Bad Questions** (confirmation bias):

- "Would you use this product?" (Everyone says yes)
- "Do you think this is a good idea?" (Asks opinion, not behavior)
- "How much would you pay for this?" (Hypothetical)

**Problem Severity Matrix**:

| Dimension               | Low (Don't Build) | Medium (Validate More) | High (Build It)   |
| ----------------------- | ----------------- | ---------------------- | ----------------- |
| **Frequency**           | Happens rarely    | Monthly                | Daily/Weekly      |
| **Impact**              | Minor annoyance   | Wastes 1-2 hours       | Critical blocker  |
| **Urgency**             | Can wait          | Should fix eventually  | Need it now       |
| **Willingness to Pay**  | Won't pay         | Might pay $5-20/mo     | Will pay $50+/mo  |
| **Current Workarounds** | Works fine        | Tolerable              | Painful/expensive |

**Decision Rule**:

- 4-5 High → Build immediately
- 2-3 High → Validate solution
- 0-1 High → Don't build (problem not severe enough)

**Validation Gate**:

- [ ] 10+ customer discovery interviews completed
- [ ] Problem validated as frequent, painful, and urgent
- [ ] Current workarounds documented and evaluated
- [ ] Willingness to pay signals collected
- [ ] 70%+ of interviewees confirm problem is severe

---

### Phase 2: Solution Validation

**Goal**: Test that your solution actually solves the problem, not just adds features

**Validation Methods**:

**1. Smoke Test** (Fastest - 1-2 days)

- Create landing page describing solution with "Sign up for early access" CTA
- Drive 100-500 visitors via ads or outreach
- **Success**: >5% conversion to email signup

**2. Concierge MVP** (1 week)

- Manually deliver solution to 5-10 early customers
- Walk them through process yourself (no automation)
- **Success**: Users achieve outcome and ask for more

**3. Wizard of Oz MVP** (1-2 weeks)

- Build front-end UI only
- Handle requests manually behind the scenes
- **Success**: Users continue using despite imperfections

**4. Prototype Testing** (3-5 days)

- Show clickable prototypes (Figma, InVision) to 10-15 users
- Watch them attempt key tasks without guidance
- **Success**: >70% complete core tasks without help

**Activities**:

- Create low-fidelity prototypes (paper, Figma, landing page)
- Test solution concepts with target users
- Identify must-have vs. nice-to-have features
- Test willingness to pay and pricing expectations

**Validation Gate**:

- [ ] Solution concepts tested with prototypes
- [ ] Must-have features identified
- [ ] 50%+ of testers say they'd pay for it
- [ ] Solution validated as solving the problem

---

### Phase 3: Market Validation

**Goal**: Confirm the market is large enough and growing

**Market Sizing**:

**TAM (Total Addressable Market)**:

```
TAM = (Number of potential users globally) × (Annual revenue per user)
```

**SAM (Serviceable Addressable Market)**:

```
SAM = TAM × (Percentage reachable with your channels)
```

**SOM (Serviceable Obtainable Market)**:

```
SOM = SAM × (Realistic market share % in 1-3 years)
```

**Minimum Viable Market**:

- SOM ≥ $10M for VC-backed startups
- SOM ≥ $1M for bootstrapped products
- Market growing at >10% annually

**Competitive Analysis**:

| Competitor   | Strengths       | Weaknesses      | Your Differentiation |
| ------------ | --------------- | --------------- | -------------------- |
| Competitor 1 | Features, price | UX, support     | Your advantage       |
| Competitor 2 | Brand, scale    | Slow, expensive | Your advantage       |

**Key Questions**:

- Why will users switch from competitors to you?
- What can you do 10x better (not 10% better)?
- What barriers prevent competitors from copying you?

**Validation Gate**:

- [ ] Market sized (TAM, SAM, SOM)
- [ ] SOM ≥ $1M with >10% growth
- [ ] Competitive landscape analyzed
- [ ] Differentiation clearly defined
- [ ] Go-to-market channels identified

---

### Phase 4: Business Model Validation

**Goal**: Validate unit economics demonstrate path to profitability

**Customer Lifetime Value (LTV)**:

```
LTV = (ARPU per month) × (Customer lifetime in months) × (Gross margin %)

Example: $50/mo × 24 months × 80% = $960 LTV
```

**Customer Acquisition Cost (CAC)**:

```
CAC = (Total sales & marketing spend) / (New customers acquired)

Example: $50,000 / 100 customers = $500 CAC
```

**LTV:CAC Ratio**:

```
Ratio = LTV / CAC

Example: $960 / $500 = 1.92:1 (NOT VIABLE)
```

**Success Criteria**:

- ✅ LTV:CAC ≥ 3:1 (healthy business)
- ⚠️ LTV:CAC 2:1 - 3:1 (needs optimization)
- ❌ LTV:CAC < 2:1 (not viable)

**Pricing Validation (Van Westendorp Method)**:

Survey questions:

1. At what price would this be so expensive you wouldn't consider it?
2. At what price would you consider it expensive, but still consider buying?
3. At what price would you consider it a bargain?
4. At what price would it be so cheap you'd question the quality?

**Optimal Price**: Where "too expensive" and "too cheap" curves intersect

**Validation Gate**:

- [ ] Revenue model defined (subscription, usage, freemium, etc.)
- [ ] LTV and CAC estimated
- [ ] LTV:CAC ≥ 3:1 achievable
- [ ] Pricing tested with real users
- [ ] Key business risks identified

---

### Phase 5: MVP Definition

**Goal**: Define minimum set of features needed to validate core value proposition

**MVP Scope Framework**:

**Must-Have (Core Value Proposition)**:

- Features that deliver the primary benefit
- Without these, the product doesn't solve the problem
- Example: For Uber, "request ride" and "track driver"

**Should-Have (Important but not Critical)**:

- Enhance experience but aren't core to problem
- Add in V1.1 or V1.2
- Example: For Uber, "driver ratings" and "fare estimates"

**Nice-to-Have (Delight Features)**:

- Add polish but don't solve core problem
- Postpone indefinitely
- Example: For Uber, "music preferences" and "pet-friendly rides"

**MVP = Must-Haves ONLY. Scope to 4-8 weeks.**

**Success Metrics**:

- Activation rate: % of signups who complete core action
- Retention (Week 1): % who return after first use
- Referral: % who recommend to others
- Revenue: % who convert to paid (if monetized)

**Validation Gate**:

- [ ] Must-have features defined (core value only)
- [ ] Should-have and nice-to-have deferred
- [ ] MVP scoped to 4-8 weeks
- [ ] Success metrics defined and measurable
- [ ] Launch and feedback strategy planned

---

## Key Principles

### 1. Test the Riskiest Assumptions First

Focus on what could kill the product, not what's easy to test

### 2. Fail Fast, Fail Cheap

Invalidate bad ideas before they consume significant resources

### 3. Evidence Over Intuition

Your opinion is not validation. Real user behavior is.

### 4. Problem Before Solution

Fall in love with the problem, not your solution

### 5. MVP is Not V1

MVP should test assumptions, not delight customers

### 6. Pivots Are Normal

Most successful products pivot based on validation findings

---

## Standard Output Format

```yaml
discovery_validation_summary:
  problem_validation:
    hypothesis: '<problem statement>'
    interviews_conducted: <number>
    severity:
      frequency: '<daily/weekly/monthly/rare>'
      impact: '<critical/high/medium/low>'
      urgency: '<urgent/important/nice-to-have>'
    validation_status: '<validated/needs-more-research/invalidated>'

  solution_validation:
    concepts_tested: <number>
    user_feedback: ['<key feedback>']
    must_have_features: ['<feature>']
    validation_status: '<validated/needs-iteration/invalidated>'

  market_validation:
    tam: '$<amount>'
    sam: '$<amount>'
    som: '$<amount>'
    growth_rate: '<percentage>'
    competitive_differentiation: '<summary>'

  business_model:
    revenue_model: '<subscription/usage/freemium/etc>'
    estimated_ltv: '$<amount>'
    estimated_cac: '$<amount>'
    ltv_cac_ratio: '<ratio>'
    pricing: '$<amount> per <month/year/user>'

  mvp_definition:
    must_have_features: ['<feature 1>', '<feature 2>']
    success_metrics:
      - metric: '<activation rate>'
        target: '<percentage>'
      - metric: '<retention (Week 1)>'
        target: '<percentage>'
    estimated_timeline: '<weeks>'

  recommendation: '<go/pivot/no-go>'
  risks: ['<key risk and mitigation>']
```

---

## Common Pitfalls

❌ **Skipping problem validation** → Build solutions to non-problems
❌ **Falling in love with your solution** → Ignore evidence it doesn't work
❌ **Talking to the wrong people** → Friends/family say what you want to hear
❌ **Overbuilding the MVP** → 6-month build for an experiment
❌ **Vanity metrics** → Track page views instead of paying customers
❌ **Ignoring unit economics** → Acquire customers at a loss forever

---

## Approval Gate

Before proceeding to full design and development:

- [ ] Problem validated with at least 10 customer interviews
- [ ] Solution concept tested with low-fidelity prototypes
- [ ] Market sized and confirmed viable (SOM ≥ $1M)
- [ ] Unit economics demonstrate path to profitability (LTV:CAC ≥ 3:1)
- [ ] MVP scope defined and approved by stakeholders
- [ ] Success metrics defined with measurement plan

**Rationale**: Investing in development without validation is gambling. This gate ensures product-market fit is achievable before significant resource commitment.

---

## Related Resources

**Related Skills**:

- `mvp-builder` - For rapid MVP development after validation
- `user-researcher` - For customer discovery interviews
- `go-to-market-planner` - For launch strategy after validation

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Build vs. buy decisions
- `STANDARDS/best-practices/user-research.md` - Interview best practices (when created)

**Related Playbooks**:

- `PLAYBOOKS/conduct-discovery-interviews.md` - Interview procedure (when created)
- `PLAYBOOKS/validate-business-model.md` - Unit economics validation (when created)
