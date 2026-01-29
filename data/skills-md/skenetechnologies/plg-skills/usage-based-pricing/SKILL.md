---
name: usage-based-pricing
description: When the user wants to design or implement usage-based, consumption, or metered pricing -- including credit systems, overage handling, or billing infrastructure. Also use when the user says "pay per use," "metered billing," "credit system," "usage pricing," or "consumption pricing." For broader pricing strategy, see pricing-strategy. For expansion, see expansion-revenue.
---

# Usage-Based Pricing

You are a usage-based pricing specialist. A comprehensive framework for designing, implementing, and optimizing consumption-based and metered billing models. Usage-based pricing aligns cost with value and enables customers to start small and grow, making it a natural fit for product-led growth.

---

## 1. Fit Decision Framework

```
Can you identify a clear unit that scales with customer value?
|- NO -> Use seat-based or feature-based pricing instead
+- YES
    |- Do customers have highly variable usage patterns?
    |   |- NO -> Usage-based adds complexity without benefit. Consider tiered flat-rate.
    |   +- YES
    |       |- Do customers need cost predictability?
    |       |   |- YES -> Hybrid model (base + usage) or prepaid credits
    |       |   +- NO -> Pure usage-based can work
    |       +- Can you meter this unit accurately?
    |           |- NO -> Solve metering first, then adopt usage-based
    |           +- YES -> Usage-based pricing is a strong fit
```

---

## 2. Usage-Based Model Types

### 2.1 Pure Usage (Pay Per Use)

Customers pay only for what they use. No base fee, no commitment. Best for APIs, infrastructure, transactional services. Revenue is highly variable.

**Pricing page format:**
```
$0.001 per API call
$0.05 per SMS message
2.9% + $0.30 per transaction
```

### 2.2 Hybrid (Base + Usage)

Monthly base fee includes baseline usage, plus per-unit overage. Best for SaaS platforms with variable feature usage. Provides predictable revenue floor.

**Pricing page format:**
```
Starter: $49/month -- includes 1,000 events
  Additional events: $0.01 each

Growth: $199/month -- includes 10,000 events
  Additional events: $0.008 each

Scale: $499/month -- includes 50,000 events
  Additional events: $0.005 each
```

### 2.3 Credit-Based

Pre-purchased credits consumed by various product actions at different rates. Best for multi-feature products, AI products, platforms with diverse actions.

**Pricing page format:**
```
Credit Packs:
  100 credits: $10 ($0.10/credit)
  500 credits: $40 ($0.08/credit)
  2,000 credits: $120 ($0.06/credit)

Credit Consumption:
  Text generation: 1 credit per 1,000 tokens
  Image generation: 5 credits per image
  Video generation: 20 credits per minute
```

### 2.4 Tiered Usage (Volume Tiers)

Unit price decreases as volume increases. Two sub-types:

**Graduated tiers** (each unit in a tier costs that tier's rate):
```
0 - 1,000 events:     $0.01 each  (max $10)
1,001 - 10,000:        $0.008 each
10,001 - 100,000:      $0.005 each
100,001+:              $0.003 each

Example: 15,000 events = (1,000 x $0.01) + (9,000 x $0.008) + (5,000 x $0.005)
                        = $10 + $72 + $25 = $107
```

**Volume tiers** (all units priced at the achieved tier):
```
0 - 1,000 events:     $0.01 each
1,001 - 10,000:        $0.008 each (all units)
10,001 - 100,000:      $0.005 each (all units)

Example: 15,000 events = 15,000 x $0.005 = $75
```

Graduated tiers are more common and avoid the "cliff" problem where passing a threshold reduces total cost.

---

## 3. Value Metric Selection

### Selection Criteria

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Measurability** | Can you accurately meter this in real-time? | Must-have |
| **Predictability** | Can customers estimate their usage in advance? | High |
| **Value alignment** | Does more usage = more value for the customer? | High |
| **Simplicity** | Can customers easily understand the metric? | High |
| **Gaming resistance** | Is it hard to artificially reduce the metric? | Medium |
| **Growth correlation** | Does the metric naturally increase as the customer succeeds? | Medium |

### Common Value Metrics by Product Type

| Product Type | Value Metric |
|-------------|-------------|
| **API / Infrastructure** | API calls, requests |
| **Compute** | Compute hours, vCPU-seconds |
| **Storage** | GB stored |
| **Communication** | Messages, emails, SMS |
| **Analytics** | Events tracked, MTUs |
| **AI / ML** | Tokens, queries, generations |
| **Marketplace** | Transaction value (%) |
| **Data** | Records, contacts, rows |

### Evaluation Template

```
Candidate Metric: [________________]

Measurability (1-5):    [  ] Can we accurately track this in real-time?
Predictability (1-5):   [  ] Can customers forecast their monthly usage?
Value alignment (1-5):  [  ] Does more usage = more value for the customer?
Simplicity (1-5):       [  ] Would a customer immediately understand the unit?
Gaming resistance (1-5):[  ] Is it hard to artificially minimize this metric?
Growth correlation (1-5):[  ] Does it naturally grow as the customer succeeds?

Total score: [  ] / 30
```

Score 3+ candidate metrics. Select highest scorer. If tied, choose the simpler one.

---

## 4. Credit System Design

### When to Use Credits

- Multiple actions with different costs
- Customers need budget flexibility
- AI features with variable cost per action
- Need to decouple pricing from underlying cost fluctuations

### Credit Denominations

```
1 credit = 1 standard action (most common action = 1 credit)

Actions and their credit costs:
  Basic text generation:    1 credit
  Advanced text generation: 3 credits
  Image generation (small): 5 credits
  Image generation (large): 10 credits
  Video generation (1 min): 25 credits
```

### Purchase Packages

```
| Package | Credits | Price | Per-Credit Cost | Savings |
|---------|---------|-------|-----------------|---------|
| Starter | 100 | $10 | $0.100 | -- |
| Growth | 500 | $40 | $0.080 | 20% |
| Pro | 2,000 | $120 | $0.060 | 40% |
| Business | 10,000 | $500 | $0.050 | 50% |
| Enterprise | Custom | Custom | Custom | Custom |
```

### Expiry Policies

| Policy | Best For |
|--------|----------|
| **No expiry** | Low-frequency products |
| **Monthly expiry** | Subscription + credits hybrid |
| **Annual expiry** | Most credit-based products (recommended) |
| **Rolling 12-month** | Large credit volumes |

### Top-Up Mechanics

- **Self-serve top-up:** One-click purchase in billing dashboard
- **Auto top-up:** Automatically purchase when balance drops below threshold
- **Threshold alerts:** Notify at 20%, 10%, and 0% remaining
- **Overage prevention:** Hard-stop or auto-top-up at zero

---

## 5. Overage Handling

### Overage Models

| Model | Behavior | Best For |
|-------|----------|----------|
| **Hard stop** | Usage stops at limit | Non-critical features |
| **Soft limit** | Warning shown, usage continues | Most SaaS products |
| **Automatic upgrade** | Moves to next tier | Seamless expansion |
| **Overage billing** | Extra units at overage rate | High-usage products |
| **Throttle** | Service degrades but continues | Infrastructure/API |

### Overage Decision Framework

```
What is the consequence of stopping the service?
|- Critical (data loss, business disruption)
|   -> Soft limit or overage billing. NEVER hard stop.
|- Significant (workflow interrupted, team blocked)
|   -> Automatic upgrade or soft limit with 24-48hr grace
+- Minor (convenience feature)
    -> Hard stop or throttle is acceptable
```

### Warning Ladder

```
At 50% usage:  Informational notification (in-product)
At 75% usage:  Reminder (in-product + email)
At 90% usage:  Urgent notification (in-product + email)
At 95% usage:  Critical alert + upgrade/top-up CTA
At 100% usage: [Action based on overage model]
At 150% usage: (If soft limit) Force decision: upgrade or throttle
```

---

## 6. Usage Dashboard Design

```
+------------------------------------------+
|  Current Period: Jan 1 - Jan 31, 2025    |
|                                          |
|  API Calls                               |
|  ||||||||||||||||||||....  8,234 / 10,000|
|                            82% used       |
|                                          |
|  Credits Remaining                       |
|  ||||||||||||||||........  156 / 200     |
|                            78% remaining  |
|                                          |
|  Estimated bill this period: $87.40      |
|  [View detailed usage ->]                |
+------------------------------------------+
```

**Forecasting:**
```
Based on your current usage rate:
  Estimated end-of-month usage: 12,400 API calls
  Estimated end-of-month bill: $124.00
  You may exceed your plan limit by ~2,400 calls

  [Upgrade plan ->]  [Set budget alert ->]
```

**Customer controls:** Usage alerts, budget caps, rate alerts, anomaly detection.

---

## 7. Billing Implementation

### Metering Infrastructure

```
User Action -> Metering Event -> Event Pipeline -> Aggregation
                                                     |
                                              Usage Store
                                                     |
Invoice Generation <- Billing Engine <- Rating Engine
```

### Key Components

| Component | Responsibility |
|-----------|---------------|
| **Metering** | Capture every usage event (reliable, low-latency, idempotent) |
| **Event pipeline** | Process/validate events (handle duplicates, late events, retries) |
| **Aggregation** | Sum usage by account, period, metric |
| **Rating engine** | Apply pricing rules (tiers, discounts, minimums, overages) |
| **Billing engine** | Generate invoices, charge customers (proration, credits, dunning) |
| **Usage store** | Audit trail, dispute resolution, analytics |

### Build vs Buy

| Approach | Best For |
|----------|----------|
| **Build in-house** | Large companies with unique needs |
| **Billing platform** (Stripe Billing, Chargebee, Recurly) | Hybrid models with simple metering |
| **Usage-based billing platform** (Metronome, Orb, Amberflo, Lago) | Pure usage-based or complex credit models |

Start with Stripe for subscriptions; add usage-based billing layer (Metronome, Orb, or custom) when usage-based pricing is validated.

---

## 8. Revenue Predictability

### Strategies

| Strategy | How It Works |
|----------|-------------|
| **Minimum commitments** | Customers commit to minimum monthly spend |
| **Prepaid packages** | Customers buy usage in advance |
| **Base + usage hybrid** | Platform fee provides revenue floor |
| **Reserved capacity** | Reserve capacity at a discount (like AWS Reserved Instances) |
| **Annual contracts** | Lock in annual spend with monthly usage reporting |

### Revenue Forecasting Template

```
Next Quarter Revenue Forecast:

Existing customers:
  Current monthly usage revenue:       $[X]
  Expected per-customer growth rate:    [Y]%
  Expected churn rate:                  [Z]%
  Forecasted existing customer revenue: $[A] x 3 months

New customers:
  Expected new customers:              [N]
  Average starting monthly usage:      $[B]
  Ramp rate:                           [C]%/month
  Forecasted new customer revenue:     $[D] x 3 months

Total forecasted revenue:             $[E]
Confidence interval:                  +/- [F]%
```

---

## 9. Usage-Based Pricing for AI Products

### Common AI Pricing Models

| Model | Unit | Example |
|-------|------|---------|
| **Per-token** | Input/output tokens | OpenAI API |
| **Per-query** | Each request | Perplexity, search APIs |
| **Per-generation** | Each output | Image generators |
| **Credit-based** | Abstracted credits | Many AI SaaS products |
| **Seat + AI usage** | Base seat + AI credits | Notion AI, GitHub Copilot |

### Cost vs Price Margin Analysis

```
Per-unit cost analysis:
  LLM inference cost per query:      $0.003
  Embedding cost per query:          $0.0005
  Infrastructure overhead:           $0.001
  Total cost per query:              $0.0045

  Target gross margin:               70-80%
  Required price per query:          $0.015 - $0.0225
  Rounded to customer-friendly:      $0.02 per query (77.5% margin)
```

### AI-Specific Considerations

1. **Cost volatility:** LLM costs drop rapidly. Credits help decouple pricing from underlying cost changes.
2. **Quality tiers:** Offer faster/cheaper vs slower/better at different prices.
3. **Token estimation:** Provide examples and calculators for usage estimation.
4. **Rate limiting:** Prevent abuse and control costs.

---

## 10. Pricing Page Template

```
# Pricing -- Pay only for what you use

No minimum commitment. Start free. Scale as you grow.

| Resource | Price | Free Tier |
|----------|-------|-----------|
| API Calls | $0.01 per call | First 1,000 free/month |
| Storage | $0.10 per GB/month | 1 GB free |
| Compute | $0.05 per hour | 10 hours free/month |

### Estimate your cost
[Interactive calculator]
  Expected monthly API calls: [slider: 0 - 1M]
  Estimated monthly cost: $XX.XX

### Example scenarios
| Scenario | Usage | Monthly Cost |
|----------|-------|-------------|
| Hobby project | 500 calls, 1 GB | Free |
| Growing startup | 50K calls, 10 GB | $XX |
| Scale-up | 500K calls, 100 GB | $XX |
| Enterprise | 5M calls, 1 TB | Contact us |
```

---

## 11. Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **Revenue per unit** | Total revenue / total units consumed | Track trend |
| **Consumption growth rate** | (This period - last period) / last period | >5% MoM |
| **Billing predictability** | Actual revenue / forecasted revenue | 0.9 - 1.1 |
| **Cost per unit** | Total cost / total units delivered | Must be below price |
| **Gross margin per unit** | (Revenue - cost) / revenue per unit | >70% for software |
| **Free tier conversion** | Free users who convert / total free users | 2-5% |
| **Usage concentration** | Revenue from top 10% / total revenue | <40% is healthy |
| **Expansion NRR** | Usage revenue growth from existing customers | >110% |

---

## 12. Diagnostic Questions

When helping a user with usage-based pricing, ask:

1. What does your product do and what is the unit of value you deliver?
2. How variable is usage across your customer base? (Range from smallest to largest)
3. What is your cost to deliver one unit of the service?
4. Can customers predict their usage in advance?
5. What alternatives do customers have and how are they priced?
6. Do you have metering infrastructure? Can you track usage in real-time?
7. Are there different types of actions with different costs (suggesting credits)?
8. What is your target gross margin?
9. Do you need revenue predictability for fundraising or financial planning?
10. Are you considering pure usage or hybrid (base + usage)?

---

## 13. Output Format

```markdown
# Usage-Based Pricing Model: [Product Name]

## Model Type
- Type: [Pure usage / Hybrid / Credit-based / Tiered usage]
- Rationale: [Why this model fits]

## Value Metric
- Primary metric: [e.g., API calls]
- Secondary metrics: [e.g., storage, compute]
- Scoring: [Measurability, predictability, value alignment, simplicity scores]

## Pricing Structure

### [If pure usage or tiered]
| Unit | Price | Volume Discount |
|------|-------|----------------|
| [Unit] | $[X] per unit | [Tier structure] |

### [If hybrid]
| Tier | Base Fee | Included Usage | Overage Rate |
|------|----------|---------------|-------------|
| Starter | $[X]/mo | [Y] units | $[Z] per unit |

### [If credit-based]
| Package | Credits | Price | Per-Credit |
|---------|---------|-------|-----------|
| [Name] | [N] | $[X] | $[Y] |

## Overage Handling
- Model: [Hard stop / soft limit / auto-upgrade / overage billing]
- Warning ladder: [thresholds and notifications]

## Free Tier
- Included: [free usage allowance]

## Billing Infrastructure
- Metering approach: [build vs buy]
- Billing platform: [recommendation]

## Revenue Forecast Model
- [Predictability strategy]
- [Forecasting methodology]

## Metrics and Monitoring
- Key metrics: [list with targets]
- Review cadence: [frequency]
```

---

## 14. Related Skills

- `pricing-strategy` -- Overall pricing and packaging framework
- `expansion-revenue` -- How usage growth drives revenue expansion
- `self-serve-motion` -- Building the self-serve purchase and billing flow
