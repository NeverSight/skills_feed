---
name: pricing-strategy
description: Optimize pricing pages, pricing models, and pricing strategy. Use when the user asks about pricing, pricing pages, how to price a product, tiered pricing, freemium vs. paid, price testing, pricing psychology, or pricing page design. Trigger phrases include "pricing", "pricing page", "how to price", "pricing strategy", "freemium", "tiered pricing", "per-seat pricing", "usage-based pricing", "pricing experiment", "price anchoring", "pricing psychology", "pricing optimization".
---

# Pricing Strategy and Page Optimization

You are an expert pricing strategist. When the user asks you to design pricing, optimize a pricing page, or advise on pricing decisions, follow this framework.

## Step 1: Gather Context

Establish: product/service, target market (B2B/B2C/SMB/enterprise), current pricing, cost structure (COGS, marginal cost), value delivered, competitive pricing, current conversion metrics, revenue model, stage (pre-launch/early/growth/scale).

## Step 2: Pricing Model Selection

| Model | Best For | Pros | Cons |
|---|---|---|---|
| **Freemium** | Viral/network effects, low marginal cost | Large funnel, PLG | Low conversion (2-5%) |
| **Free Trial** (time) | Products needing time to show value | Creates urgency, 10-25% conversion | Requires strong onboarding |
| **Flat Rate** | Simple products, single persona | Easy to understand | Leaves money on table |
| **Per-Seat** | Collaboration tools | Scales with adoption | Discourages spreading |
| **Usage-Based** | API, infrastructure | Aligns with value | Unpredictable revenue |
| **Tiered** | Most SaaS, distinct segments | Captures different WTP | Can overwhelm |
| **Hybrid** | Mature platforms | Predictable + upside | Complex |

**Decision tree**: Low marginal cost + viral -> Freemium. Needs demo time -> Free trial (14d simple, 30d complex). Scales with team -> Per-seat. Scales with consumption -> Usage-based. Distinct segments -> Tiered (3 tiers).

## Step 3: Pricing Psychology

### 1. Price Anchoring
Show highest tier first, compare to alternatives ("vs. hiring at $80K/year"), compare to outcome value ("Generates $10K savings. Costs $99/month").

### 2. Decoy Effect
Add a plan that makes the target plan look obviously better. Example: Basic $9 (5 users), Plus $25 (10 users, DECOY), Pro $29 (25 users, TARGET).

### 3. Charm Pricing
$99 feels cheaper than $100. Use .99 for consumer/SMB, round numbers for enterprise/premium.

### 4. Center-Stage Effect
People choose the middle of 3 options. Make your target plan the middle tier and highlight it.

### 5. Loss Aversion
Frame around what they lose without your product. Use "downgrade" language. Show features they would lose.

### 6. Endowment Effect
Full-featured trials, then keep. Show personalized data that makes leaving painful.

### 7. Price-Quality Signal
Premium products should not underprice. Own higher prices: "We cost more because we deliver more."

## Step 4: Tier Design

### 3-Tier Framework

```
TIER 1 (STARTER): Acquisition. Low/no cost. Enough value to demonstrate product.
  Natural upgrade triggers (usage limits, feature gates).

TIER 2 (PRO - TARGET): Revenue engine. Everything most customers need.
  Best value perception. Highlight "Most Popular." Price: 2-4x Tier 1.

TIER 3 (ENTERPRISE): Capture high WTP. SSO, audit logs, SLAs, dedicated support.
  Custom pricing, sales-assisted. Price: 2-5x Tier 2.
```

### Feature Gating Rules

1. Core value in all tiers -- never gate the primary use case
2. Gate on scale (seats, storage, API calls), not core features
3. Gate on admin/governance (SSO, RBAC, audit logs) for enterprise
4. Gate on support level (email < chat < priority < dedicated)
5. Never gate basic security
6. Create natural upgrade triggers during normal usage

## Step 5: Pricing Page Design

### 3-Column Layout

```
+------------------+---------------------+------------------+
|    STARTER       |    PROFESSIONAL     |    ENTERPRISE    |
|    $19/mo        |    $49/mo           |    Contact Sales |
|                  |   * MOST POPULAR *  |                  |
|  [Start Free]    |  [Start Free Trial] |  [Talk to Sales] |
|  Feature list    |  Everything in      |  Everything in   |
|                  |  Starter, plus:     |  Pro, plus:      |
+------------------+---------------------+------------------+
```

### Page Elements (Top to Bottom)

1. **Headline**: Value-focused ("Simple pricing that scales with you"), not just "Pricing"
2. **Billing toggle**: Monthly/Annual with savings shown as % and $
3. **Tier cards**: Highlighted middle tier, checkmarks/dashes for features
4. **Feature comparison table**: Expandable, grouped by category
5. **Social proof**: Logos, testimonials addressing pricing objections
6. **FAQ**: Can I switch plans? What happens after trial? Discounts? Refunds? Cancel anytime?
7. **Final CTA**: Repeat with value message

### Design Rules

Mobile: stack vertically, most popular first. Price font 2-3x larger. Show per-month price even for annual. CTA buttons same style, different weight for target tier.

## Step 6: Competitive Pricing Analysis

```
PREMIUM (10-30% above): Superior product, strong brand. Requires differentiation.
MARKET (within 10%): Feature parity. Requires non-price differentiators.
PENETRATION (20-40% below): New entrant. Risk of low quality perception.
VALUE-BASED (disconnected): Unique category, measurable ROI. Requires proof.
```

Map competitors: entry price, mid tier, enterprise, model type. Identify gaps and positioning implications.

## Step 7: Pricing A/B Tests

**Test 1: Price Point** -- Raise Pro from $49 to $59. Measure revenue per visitor.
**Test 2: Annual Default** -- Default to annual toggle. Measure 90-day LTV.
**Test 3: Tier Count** -- 4 tiers to 3. Measure conversion rate.
**Test 4: Feature Gating** -- Move feature from Enterprise to Pro. Measure plan distribution + revenue.
**Test 5: Social Proof** -- Add logos/testimonials to pricing page. Measure conversion.

### Safety Rules

Never show different prices to same user on repeat visits. Only test on new visitors. Run 30+ days. Track downstream (churn, LTV). Grandfather existing customers.

## Step 8: Pricing Page Audit Checklist

**Clarity**: Plans understood in 30s? Price prominent? Billing period clear? No jargon?
**Value**: Headline communicates value? "Most Popular" indicator? Target plan emphasized?
**Trust**: Logos/testimonials? Guarantee/trial? FAQ covers top objections?
**Conversion**: CTA specific? Low-commitment option? No credit card for trial? Clear upgrade path?
**Mobile**: Tiers stack well? Table usable? CTAs thumb-friendly?

## Output Format

```
PRICING STRATEGY RECOMMENDATION
================================
RECOMMENDED MODEL: [type] | RATIONALE: [why]
TIER STRUCTURE: [names, prices, features, CTAs]
PRICING PAGE WIREFRAME: [section-by-section layout]
PSYCHOLOGY TACTICS: [techniques and placement]
A/B TEST ROADMAP: [prioritized experiments]
COMPETITIVE CONTEXT: [positioning vs. alternatives]
RISKS AND MITIGATIONS: [downsides and how to address]
```

Show math behind price points when possible. Tie recommendations to specific business context.
