---
name: expansion-revenue
description: When the user wants to grow revenue from existing customers -- including seat expansion, plan upgrades, usage upsells, or cross-sell strategies. Also use when the user says "NRR," "net revenue retention," "upsell," "expansion MRR," or "how to increase revenue from existing customers." For pricing, see pricing-strategy. For upgrade screens, see paywall-upgrade-cro.
---

# Expansion Revenue

You are an expansion revenue strategist. A framework for systematically growing revenue from existing customers through seat expansion, plan upgrades, usage increases, add-on purchases, and cross-sell. In mature PLG companies, expansion revenue is the primary growth engine -- often contributing more new ARR than new customer acquisition.

---

## 1. Expansion Types

| Expansion Type | Mechanism | Example | Revenue Impact |
|---------------|-----------|---------|---------------|
| **Seat expansion** | More users added to the account | Team grows from 5 to 15 seats | Linear: 3x seats = 3x revenue |
| **Plan upgrade** | Customer moves to a higher tier | Starter → Pro or Pro → Business | Step function: 2-5x per upgrade |
| **Usage increase** | Customer consumes more of a metered resource | API calls grow from 10K to 100K/month | Proportional to consumption |
| **Add-on purchase** | Customer buys supplementary features or products | Adds premium support, advanced analytics module | Incremental per add-on |
| **Cross-sell** | Customer adopts an adjacent product | Slack customer adds Slack Connect or Slack Atlas | Multiplied across product portfolio |

### Which Expansion Types to Prioritize

```
Is your pricing per-seat?
├── YES → Seat expansion is your primary expansion lever
│         Focus on driving team adoption and new team onboarding
└── NO
    ├── Is your pricing usage-based?
    │   ├── YES → Usage increase is your primary expansion lever
    │   │         Focus on helping customers get more value from usage
    │   └── NO → Plan upgrades are your primary expansion lever
    │             Focus on demonstrating premium tier value
    └── Do you have multiple products?
        ├── YES → Cross-sell is an additional lever
        └── NO → Consider add-ons as supplementary expansion
```

---

## 2. Net Revenue Retention (NRR) Framework

### Formula

```
NRR = (Beginning MRR + Expansion MRR - Contraction MRR - Churned MRR) / Beginning MRR

Example:
Beginning MRR:     $1,000,000
Expansion MRR:     +$150,000 (upgrades, seats, usage)
Contraction MRR:   -$30,000  (downgrades)
Churned MRR:       -$50,000  (cancellations)
NRR = ($1,000,000 + $150,000 - $30,000 - $50,000) / $1,000,000 = 107%
```

### NRR Benchmarks

| NRR Range | Quality | Typical Profile |
|-----------|---------|-----------------|
| <90% | Concerning | High churn, minimal expansion |
| 90-100% | Acceptable | Expansion barely offsets churn |
| 100-110% | Good | Healthy expansion motion |
| 110-130% | Excellent | Strong expansion, top-quartile PLG |
| >130% | Exceptional | Usage-based models with high growth (Snowflake, Twilio) |

---

## 3. Expansion Signals from Product Data

### 3.1 Seat Expansion Signals

| Signal | Indicator | Action |
|--------|-----------|--------|
| New invites sent | User invites teammates | Surface team plan benefits |
| Shared content increasing | Reports, dashboards, docs shared with non-users | Prompt: "Invite [name] to collaborate directly" |
| Multiple login IPs | Same account accessed from different locations | Suggest additional seats |
| Approaching seat limit | 80%+ of seats used | Proactive notification |
| Cross-department usage | Different teams or roles accessing the product | Propose organization-wide deployment |

### 3.2 Plan Upgrade Signals

| Signal | Indicator | Action |
|--------|-----------|--------|
| Hitting plan limits | Storage, projects, API calls approaching cap | Upgrade prompt at the limit moment |
| Gated feature attempts | User clicks on locked features repeatedly | Show feature value and upgrade path |
| Power user behavior | Usage in top 10% of current tier | Proactive upgrade recommendation |
| Admin feature requests | Requests for SSO, audit logs, permissions | Enterprise tier pitch |
| Support ticket patterns | Questions about advanced features or capabilities | Guide toward the tier that includes those features |

### 3.3 Usage Increase Signals

| Signal | Indicator | Action |
|--------|-----------|--------|
| Accelerating consumption | Week-over-week usage growth >10% | Ensure customer is aware of usage tier benefits |
| New use case adoption | Different API endpoints or features being used | Help expand into adjacent use cases |
| Data volume growth | Increasing records, events, or storage | Proactive capacity planning conversation |
| Integration expansion | New integrations connected | Usage typically increases after integration |

### 3.4 Cross-Sell Signals

| Signal | Indicator | Action |
|--------|-----------|--------|
| Adjacent feature exploration | Users browsing or requesting related product features | Introduce adjacent product |
| Workflow gaps | Users exporting data to use in other tools | Position your product as the replacement |
| Team overlap | Different teams using different tools for related workflows | Propose unified platform |
| Customer feedback | Feature requests that map to another product | Route to cross-sell conversation |

---

## 4. Expansion Timing

### Timing Framework

```
For self-serve expansion (< $1,000 ACV):
  → Primarily moment-of-need triggers
  → Supplemented by monthly usage summary emails
  → Automated upgrade flows

For mid-market expansion ($1,000 - $25,000 ACV):
  → Moment-of-need triggers + in-product prompts
  → Quarterly usage reviews (automated or CSM)
  → Annual renewal conversation

For enterprise expansion (> $25,000 ACV):
  → Product signals routed to CSM/AE
  → Quarterly business reviews with stakeholders
  → Annual strategic planning and renewal
  → Executive sponsorship for major expansion
```

---

## 5. In-Product Expansion Triggers

### Trigger Specifications

Design each trigger with these components:

#### 5.1 Limit-Approaching Notification

```
Trigger: User reaches 80% of plan limit
Location: In-product banner or notification
Copy: "You have used [X] of [Y] [resource]. Upgrade to [Plan] for
       [higher limit or unlimited]."
CTA: "Upgrade Now" (primary) | "Remind Me Later" (secondary)
Frequency: Show once per session, max 3 times total
Suppress: If user dismissed 3 times, stop showing for 30 days
```

#### 5.2 Feature Discovery Prompt

```
Trigger: User navigates near a gated feature or searches for it
Location: Contextual tooltip or inline prompt near the feature
Copy: "[Feature name] helps you [specific benefit]. Available on [Plan]."
CTA: "Learn More" → feature explainer with upgrade option
Frequency: Show once per feature per user
Suppress: After user has seen 3 feature prompts in one session
```

#### 5.3 Team Growth Prompt

```
Trigger: Account has new active users approaching seat limit, or
         user attempts to invite beyond seat limit
Location: Invite flow or team settings
Copy: "Your team is growing! Add more seats to bring everyone onto
       [Product]."
CTA: "Add Seats" → seat purchase flow
Frequency: At the moment of need
Suppress: Not applicable (this is a hard block if at seat limit)
```

#### 5.4 Usage Milestone Celebration

```
Trigger: User reaches a meaningful usage milestone
Location: In-product celebration modal or notification
Copy: "Congratulations! You have [created 100 projects / processed
       1,000 transactions / sent 10,000 messages]. Unlock [benefit]
       with [Plan]."
CTA: "See What's Next" → plan comparison with upgrade option
Frequency: At each milestone (define 3-5 meaningful milestones)
Suppress: Not after milestone; this is a positive moment
```

### Anti-Patterns for In-Product Triggers

- **Too frequent:** More than 2-3 expansion prompts per session feels aggressive
- **Irrelevant:** Showing upgrade prompts for features the user has no interest in
- **Blocking:** Interrupting the user's workflow with a modal they must dismiss
- **No value context:** "Upgrade now!" without explaining what they gain
- **One-size-fits-all:** Same prompt for a solo user and a team admin

---

## 6. Expansion Pricing

### Seat-Based Uplift

| Approach | Description | Best For |
|----------|-------------|----------|
| Per-seat pricing | Each additional seat costs the same | Simple, predictable, transparent |
| Tiered seat pricing | Price per seat decreases at volume (e.g., 1-10: $20, 11-50: $15, 51+: $10) | Encouraging bulk purchase, enterprise |
| Seat bundles | Buy in packs (5, 10, 25 seats) | Reducing purchase frequency, encouraging growth |

### Usage-Based Overages

| Approach | Description | Best For |
|----------|-------------|----------|
| Hard stop | Usage stops at limit, must upgrade | Clear boundaries, no surprise bills |
| Automatic upgrade | Automatically moves to next tier | Seamless experience, higher revenue |
| Overage billing | Charged per unit above limit | Maximum flexibility, but surprise bill risk |
| Grace period | Allow overages temporarily, then require upgrade | Balance of flexibility and conversion |

### Prorated Upgrades

Always prorate when a customer upgrades mid-billing cycle:

```
Days remaining in cycle: 15 of 30
Current plan cost: $50/month
New plan cost: $100/month
Prorated charge: ($100 - $50) x (15/30) = $25
Next full cycle: $100/month
```

Communicate this clearly in the upgrade flow: "You will be charged $25 now for the remainder of this billing period, then $100/month starting [date]."

---

## 7. Self-Serve vs Sales-Assisted Expansion

| Factor | Self-Serve | Sales-Assisted |
|--------|-----------|---------------|
| Deal size | <$1,000 ACV expansion | >$1,000 ACV expansion |
| Complexity | Adding seats, simple upgrade | Multi-product, custom pricing, enterprise |
| Customer preference | Fast, autonomous | Consultative, negotiated |
| Scalability | High (automated) | Lower (requires human) |
| Conversion rate | Lower per opportunity | Higher per opportunity |
| Cost to serve | Very low | Higher (sales/CS time) |

### Hybrid Model

Most PLG companies use a hybrid approach:

1. **Self-serve for small expansions:** Adding seats, upgrading from Starter to Pro, purchasing add-ons
2. **Sales-assisted for large expansions:** Enterprise upgrades, multi-year deals, cross-sell, volume discounts
3. **Product-qualified leads (PQLs):** Product signals trigger sales outreach for high-potential accounts

### PQL Criteria for Expansion

An account becomes an expansion PQL when:
- Usage has grown >50% in the last 30 days
- User hit a plan limit 3+ times in the last 14 days
- Account has 5+ active users on a plan designed for smaller teams
- Account uses features that indicate readiness for the next tier
- Account health score is high AND approaching plan limits

---

## 8. Expansion Playbook for Customer Success

### Quarterly Business Review (QBR) Template

```markdown
# QBR: [Customer Name] -- [Quarter/Year]

## Account Summary
- Current plan: [Plan name]
- Seats: [X active / Y purchased]
- MRR: [$X]
- Account age: [N months]
- Health score: [X/100]

## Usage Review
- Key metrics this quarter:
  - [Metric 1]: [Value] (trend: up/down/flat vs last quarter)
  - [Metric 2]: [Value] (trend)
  - [Metric 3]: [Value] (trend)
- Feature adoption:
  - Using: [features actively used]
  - Not using: [features available but unused]
  - Approaching limits: [features near plan ceiling]

## Value Delivered
- [Quantified outcome 1]: "You saved X hours this quarter using [feature]"
- [Quantified outcome 2]: "Your team processed X more [things] than last quarter"
- [ROI calculation]: "Based on your usage, [Product] is delivering
  [$X] in value against your [$Y] investment"

## Growth Opportunities
1. [Opportunity 1]: [Description, business case, recommended plan/add-on]
2. [Opportunity 2]: [Description, business case]
3. [Opportunity 3]: [Description, business case]

## Recommended Next Steps
- [ ] [Action 1] -- [Owner] -- [Due date]
- [ ] [Action 2] -- [Owner] -- [Due date]

## Questions for the Customer
1. What are your priorities for next quarter?
2. Are there new teams or use cases where [Product] could help?
3. Are there any challenges or gaps in the current product?
```

### Usage Review Framework

When reviewing an account for expansion opportunities, check:

1. **Utilization rate:** What percentage of purchased capacity (seats, limits) is being used?
   - <50% → Focus on adoption before expansion
   - 50-80% → Healthy, monitor for growth
   - >80% → Expansion conversation is timely

2. **Growth trajectory:** Is usage increasing, stable, or declining?
   - Increasing → Proactive expansion conversation
   - Stable → Focus on new use cases or teams
   - Declining → Focus on retention before expansion

3. **Feature adoption breadth:** How many available features are being used?
   - Narrow usage → Help expand feature adoption (may unlock upgrade desire)
   - Broad usage → User is ready for more advanced features (upgrade pitch)

4. **Team coverage:** How many potential users in the organization are on the platform?
   - Low coverage → Land-and-expand opportunity (new teams, departments)
   - High coverage → Upgrade or add-on opportunity

---

## 9. Account Health Scoring for Expansion Readiness

### Health Score Components

| Component | Weight | Measurement |
|-----------|--------|------------|
| **Product engagement** | 30% | DAU/MAU ratio, session frequency, feature adoption breadth |
| **Growth trajectory** | 25% | Usage growth rate, seat growth, data volume trend |
| **Utilization rate** | 20% | % of plan limits consumed, seats used vs purchased |
| **Relationship health** | 15% | NPS/CSAT score, support ticket sentiment, executive engagement |
| **Expansion history** | 10% | Previous upgrades, responsiveness to expansion offers |

### Scoring Matrix

```
Health Score: 0-100

90-100: Champion Account
  → Strong candidate for expansion
  → Approach with confidence
  → Ask for referrals and case studies too

70-89: Healthy Account
  → Good candidate for targeted expansion
  → Focus on specific growth areas
  → Address any minor gaps first

50-69: Moderate Account
  → Fix engagement issues before expanding
  → Focus on increasing value realization
  → Expansion only if clear unmet need exists

<50: At-Risk Account
  → Do NOT pursue expansion
  → Focus entirely on retention
  → Understand and resolve pain points
```

---

## 10. Downsell as Retention

Sometimes the best expansion strategy is preventing contraction. When a customer signals they want to cancel, offering a lower-tier plan can retain them in the ecosystem.

### When to Downsell

- Customer initiates cancellation
- Customer says the product is "too expensive for what we use"
- Customer's usage has significantly declined
- Customer is on a plan with features they do not use

### Downsell Framework

```
Customer signals intent to cancel
├── Is the customer using the product regularly?
│   ├── YES → Understand why they want to cancel
│   │         (Cost? Missing feature? Competitor? Internal change?)
│   │         → Address root cause first
│   │         → If cost: offer downsell to lower tier
│   │         → If feature: show roadmap or workaround
│   │         → If competitor: competitive differentiation
│   │         → If internal: offer to pause account
│   └── NO → Attempt re-engagement
│           → If no re-engagement: offer downsell or free tier
│           → Retain the account for future expansion potential
```

---

## 11. Metrics

| Metric | Formula | Benchmark | Frequency |
|--------|---------|-----------|-----------|
| **NRR** | (Beginning MRR + Expansion - Contraction - Churn) / Beginning MRR | 110-130% | Monthly |
| **Expansion MRR** | MRR added from existing customers | Track trend | Monthly |
| **Expansion rate** | Expansion MRR / Beginning MRR | >5% monthly | Monthly |
| **ARPA growth** | Change in avg revenue per account over time | Positive trend | Quarterly |
| **Seat expansion rate** | New seats / existing seats per period | Varies | Monthly |
| **Upgrade rate** | Plan upgrades / eligible accounts per period | 3-7% monthly | Monthly |
| **Downgrade rate** | Plan downgrades / paid accounts per period | <2% monthly | Monthly |
| **Expansion efficiency** | Expansion ARR / cost to generate expansion ARR | >3x | Quarterly |
| **Time to first expansion** | Days from initial purchase to first expansion | <180 days | Cohort |
| **Expansion by source** | % of expansion from self-serve vs sales-assisted | Track mix | Monthly |

---

## 12. Diagnostic Questions

When helping a user with expansion revenue, ask:

1. What is your current NRR? Do you track it?
2. What expansion motions exist today? (Seat, upgrade, usage, add-on, cross-sell)
3. Is expansion primarily self-serve or sales-assisted?
4. Do you track product usage signals that indicate expansion readiness?
5. What does your account health scoring look like?
6. Do you have in-product expansion triggers? What are they?
7. How do you handle customers approaching plan limits?
8. Do you have a QBR or account review process?
9. What is your current expansion MRR as a percentage of total new MRR?
10. Have you ever used downsell as a retention tactic?

---

## 13. Output Format

When completing an expansion revenue engagement, deliver:

```markdown
# Expansion Revenue Strategy: [Product Name]

## Current State
- NRR: [X%]
- Primary expansion motion: [seat/upgrade/usage/add-on]
- Expansion MRR: [$X/month]
- Self-serve vs sales-assisted split: [X% / Y%]

## Expansion Opportunity Map

| Expansion Type | Current State | Opportunity | Priority |
|---------------|--------------|-------------|----------|
| Seat expansion | [status] | [opportunity] | [H/M/L] |
| Plan upgrade | [status] | [opportunity] | [H/M/L] |
| Usage increase | [status] | [opportunity] | [H/M/L] |
| Add-on | [status] | [opportunity] | [H/M/L] |
| Cross-sell | [status] | [opportunity] | [H/M/L] |

## In-Product Expansion Triggers
For each trigger:
- Trigger condition: [when it fires]
- Location: [where in the product]
- Copy: [what it says]
- CTA: [what the user clicks]
- Expected impact: [estimated conversion rate]

## Expansion Playbook
- Self-serve expansion flow: [description]
- Sales-assisted expansion criteria: [PQL definition]
- QBR framework: [cadence and structure]

## Account Health Model
- Scoring components: [list with weights]
- Expansion readiness threshold: [score]
- Action triggers: [what happens at each level]

## Metrics and Targets
- NRR target: [X%]
- Expansion MRR target: [$X/month]
- Key leading indicators: [list]

## 90-Day Roadmap
1. [Action 1] -- [Owner] -- [Timeline]
2. [Action 2] -- [Owner] -- [Timeline]
3. [Action 3] -- [Owner] -- [Timeline]
```

---

## 14. Related Skills

- `pricing-strategy` -- Overall pricing and packaging that enables expansion
- `paywall-upgrade-cro` -- Optimizing the upgrade flow that expansion triggers lead to
- `product-led-sales` -- Sales-assisted expansion for larger accounts
- `plg-metrics` -- Measuring PLG health including NRR and expansion metrics
