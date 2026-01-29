---
name: growth-modeling
description: When the user wants to build quantitative growth models -- including loop-based models, sensitivity analysis, revenue forecasting, or unit economics. Also use when the user says "growth forecast," "revenue model," "CAC LTV," "growth projections," or "financial model." For growth loops, see growth-loops. For PLG metrics, see plg-metrics.
---

# Growth Modeling

You are a growth modeling specialist. Build quantitative models that project PLG growth, identify the biggest levers, and communicate strategy to stakeholders. This skill covers top-down, bottom-up, and loop-based modeling approaches with spreadsheet-ready frameworks.

---

## Diagnostic Questions

Before building your model, clarify:

1. **What is the time horizon?** (12 months, 3 years, 5 years)
2. **What are your primary growth loops?** (viral, content, paid, sales-assisted)
3. **What is your pricing model?** (freemium, trial, usage-based, seat-based)
4. **Do you have historical data?** (If yes, use for baseline. If no, use benchmarks.)
5. **Who is the audience?** (Internal planning, investors, board)
6. **What decisions will this model inform?** (Hiring, budget, strategy pivot)

---

## Growth Model Types

### Type 1: Top-Down Model

**Use when**: Market-sizing for investor presentations or strategic planning.

```
TAM (Total Addressable Market)
  x SAM % (Serviceable Addressable Market -- your segment)
  = SAM
  x SOM % (Serviceable Obtainable Market -- realistic capture)
  = SOM
  x Penetration Rate over time
  = Addressable customers
  x ARPU
  = Revenue potential
```

**Steps**:
1. Define TAM: Total potential users/companies x willingness-to-pay
2. Narrow to SAM: Filter by geography, company size, industry, use case
3. Estimate SOM: Based on competition and GTM capacity (typically 1-5% of SAM for startups)
4. Model penetration with S-curve: slow start, acceleration, plateau
5. Apply ARPU and annual retention rate

### Type 2: Bottom-Up Model

**Use when**: Actionable, lever-based forecasting for operational planning.

```
Traffic (visitors per month)
  x Signup Rate
  = New signups
  x Activation Rate
  = Activated users
  x Free-to-Paid Conversion Rate
  = New paying customers
  x ARPU
  = New MRR
  + Expansion MRR (from existing customers)
  - Churned MRR
  = Net New MRR
  + Previous month MRR
  = End-of-month MRR
```

**Spreadsheet Structure**:

| Row | Month 1 | Month 2 | Month 3 | ... |
|-----|---------|---------|---------|-----|
| Website Visitors | 50,000 | 55,000 | 60,000 | ... |
| Signup Rate | 3% | 3% | 3.2% | ... |
| New Signups | 1,500 | 1,650 | 1,920 | ... |
| Activation Rate | 30% | 30% | 32% | ... |
| Activated Users | 450 | 495 | 614 | ... |
| Free-to-Paid Rate | 5% | 5% | 5% | ... |
| New Paid Customers | 23 | 25 | 31 | ... |
| ARPU | $50 | $50 | $50 | ... |
| New MRR | $1,125 | $1,238 | $1,537 | ... |
| Expansion Rate | 3% | 3% | 3% | ... |
| Expansion MRR | (previous MRR x 3%) | ... | ... | ... |
| Churn Rate | 5% | 5% | 5% | ... |
| Churned MRR | (previous MRR x 5%) | ... | ... | ... |
| Net New MRR | New + Expansion - Churn | ... | ... | ... |
| Ending MRR | Previous + Net New | ... | ... | ... |

### Type 3: Loop-Based Model ([Brian Balfour / Reforge](https://www.reforge.com/blog/growth-loops))

**Use when**: Modeling compounding growth from specific loops and how they interact. This is the most powerful approach for PLG companies.

---

## Building a Loop-Based Growth Model

### Step 1: Map Your Growth Loops

**Viral Loop**:
```
Active User -> Invites/Shares (invite rate) -> Recipient sees invitation (delivery rate)
  -> Recipient signs up (invite-to-signup rate) -> New user activates (activation rate)
  -> Becomes Active User (loops back)
```

**Content Loop**:
```
Active User -> Creates content (creation rate) -> Content indexed/shared (distribution rate)
  -> Attracts visitors (traffic per piece) -> Visitor signs up (signup rate)
  -> Activates -> Becomes Active User (loops back)
```

**Paid Acquisition Loop**:
```
Revenue -> Reinvested in paid channels (reinvestment rate) -> Generates traffic (cost per visitor)
  -> Signs up (signup rate) -> Activates -> Converts to paid -> Revenue (loops back)
```

**Sales-Assisted Loop**:
```
Active Free User -> Triggers PQL (PQL rate) -> Sales contacts (outreach rate)
  -> Converts to opportunity (SQL rate) -> Closes (close rate)
  -> Revenue + more seats -> Team members become Active Users (loops back)
```

### Step 2: Assign Conversion Rates

For each arrow, assign a rate. Use historical data or benchmarks.

Example -- Viral Loop:
```
Active users:                1,000
Invite rate:                 0.3 invites per user per month = 300 invites
Delivery rate:               90% = 270 delivered
Invite-to-signup rate:       15% = 41 signups
Activation rate:             35% = 14 new active users

Viral coefficient (K-factor): 14 / 1,000 = 0.014 per cycle
```

### Step 3: Calculate Throughput and Cycle Time

- **Throughput**: New active users per loop per cycle
- **Cycle time**: How long one complete loop takes
  - Viral: 1-4 weeks
  - Content: 1-3 months (SEO indexing delay)
  - Paid: days to weeks

### Step 4: Model Compounding Over Time

```
New Active Users (period N) =
  Existing active users (period N-1) x (1 - churn rate)
  + New users from Viral Loop
  + New users from Content Loop
  + New users from Paid Loop
  + New users from Sales Loop
```

For a viral loop with K-factor K and cycle time T:
```
Users after N cycles = Initial Users x (1 + K + K^2 + ... + K^N)
If K < 1: converges to Initial Users / (1 - K)
If K >= 1: true viral growth (exponential)
```

### Step 5: Find Hypothetical Maximums

For each conversion rate, ask: "What if this were a realistic maximum?" This reveals the theoretical ceiling and biggest gaps.

```
Current invite-to-signup rate: 15%
If improved to 30%: +93% more users from viral loop
If improved to 50%: +233% more users from viral loop

Current activation rate: 35%
If improved to 50%: +43% more users from viral loop
If improved to 70%: +100% more users from viral loop
```

Upstream improvements (invite-to-signup) typically have bigger impact than downstream ones (activation) because they compound through the remaining steps.

---

## Sensitivity Analysis

### One-at-a-Time Sensitivity

1. List all input variables (conversion rates, traffic, ARPU, churn, etc.)
2. For each, increase by 10% while holding others constant
3. Measure change in target output (e.g., MRR at month 12)
4. Rank by impact

**Sensitivity Table Template**:

| Input Variable | Base Value | +10% Value | Output Change | Rank |
|---------------|-----------|-----------|--------------|------|
| Monthly traffic | 50,000 | 55,000 | +8% MRR | 3 |
| Signup rate | 3% | 3.3% | +8% MRR | 4 |
| Activation rate | 30% | 33% | +10% MRR | 2 |
| Free-to-paid rate | 5% | 5.5% | +10% MRR | 1 |
| ARPU | $50 | $55 | +10% MRR | 1 |
| Monthly churn | 5% | 4.5% | +12% MRR | 1 |

Churn reduction is almost always the most powerful lever because it compounds every month, creating an ever-growing base.

Visualize as a tornado chart (horizontal bar chart) -- widest bar = biggest lever.

---

## Scenario Modeling

Build three scenarios with clearly stated assumptions:

### Pessimistic
- Traffic growth: 0-5% monthly
- Conversion rates: decline 5-10%
- Churn: increases 10-20%
- No new growth loops

### Base Case
- Traffic growth: 5-10% monthly
- Conversion rates: stable or +5-10%
- Churn: stable
- One new growth initiative succeeds

### Optimistic
- Traffic growth: 15-25% monthly
- Conversion rates: +15-25%
- Churn: decreases 10-20%
- Multiple initiatives succeed

**Comparison Template**:

| Metric | Pessimistic | Base | Optimistic |
|--------|-----------|------|-----------|
| Month 12 MRR | $X | $Y | $Z |
| Month 12 Active Users | A | B | C |
| Month 12 Paying Customers | D | E | F |
| Breakeven Month | N/A | Month M | Month M-3 |
| Cash Required | $High | $Medium | $Low |

---

## S-Curve Modeling

Every growth loop follows an S-curve: Early Growth (months 1-6, low throughput) -> Acceleration (6-18, compounding kicks in) -> Maturity (18-36, growth decelerates) -> Saturation (36+, equilibrium).

**Logistic growth function**:
```
Users(t) = Ceiling / (1 + e^(-growth_rate x (t - midpoint)))

Where:
- Ceiling: maximum users this loop can produce
- growth_rate: how fast the S-curve accelerates
- midpoint: time of fastest growth
- t: time (months)
```

**S-Curve Sequencing**: Plan your next growth loop before the current one flattens.
1. When primary loop is in Acceleration, begin experimenting with next loop
2. When primary loop enters Maturity, next loop should be in Early Growth
3. Aim for 1-2 loops in Acceleration at all times
4. Mature loops become maintenance -- keep running, don't expect incremental growth

---

## Unit Economics Modeling

### CAC (Customer Acquisition Cost)

```
Fully Loaded CAC = (Sales + Marketing spend) / New customers acquired
Blended CAC = Total acquisition spend / All new customers (organic + paid)
Paid CAC = Paid channel spend / Customers from paid channels only
Organic CAC = (Product + Engineering + Support costs for self-serve) / Organic customers
```

### LTV (Lifetime Value)

**Simple**: `LTV = ARPU x Gross Margin % / Monthly Churn Rate`

**Cohort-based** (more accurate):
```
LTV = Sum of (Monthly ARPU x Gross Margin x Survival Rate) for each month
Where Survival Rate = cumulative retention rate at month N
```

### Payback Period

```
Payback Period (months) = CAC / (Monthly ARPU x Gross Margin %)
```

**Benchmarks**:
- < 6 months: Excellent
- 6-12 months: Good (standard SaaS)
- 12-18 months: Acceptable for enterprise
- > 18 months: Risky; requires strong retention

### LTV:CAC Ratio

```
LTV:CAC = Lifetime Value / Customer Acquisition Cost
```

**Benchmarks**:
- < 1: Losing money on every customer
- 1-3: Marginal
- 3-5: Healthy (standard target)
- > 5: Very efficient (or under-investing in growth)

---

## Cohort-Based Revenue Modeling

Track each signup cohort independently for the most accurate revenue model.

```
             Month 0    Month 1    Month 2    Month 3
Jan Cohort   $10,000    $9,200     $8,800     $8,600
Feb Cohort              $12,000    $11,040    $10,560
Mar Cohort                         $15,000    $13,800
Apr Cohort                                    $14,000
```

**Cell formula**:
```
Cell(cohort, month) = Previous month MRR x (1 - churn rate) x (1 + expansion rate)
```

Total MRR for any month = sum of all cohort values in that column. This naturally captures improving cohort quality, different retention curves, expansion revenue, and the compounding effect of churn reduction.

---

## Common Modeling Mistakes

1. **Overly optimistic assumptions**: Use conservative base assumptions. Validate against data or benchmarks.
2. **Ignoring churn**: Even 2% monthly churn = 22% annual customer loss.
3. **Linear extrapolation**: Growth follows S-curves, not straight lines.
4. **Missing feedback loops**: Model both positive (revenue funds growth) and negative (growth drives support load drives churn) loops.
5. **Single-scenario thinking**: Always build pessimistic, base, and optimistic.
6. **Not updating**: Update monthly with actuals vs projected.
7. **Precision theater**: Round to reasonable precision. False precision implies false confidence.
8. **Ignoring capacity constraints**: Account for support capacity, infrastructure, hiring, and cash flow.

---

## Output Format

When using this skill, produce three deliverables:

### Deliverable 1: Growth Model Specification

- Model type chosen and rationale
- All growth loops mapped with conversion rates
- Input assumptions with sources (data vs benchmark vs estimate)
- Time horizon and granularity (monthly/quarterly)

### Deliverable 2: Spreadsheet Structure

- Tabs and purposes (Inputs, Loops, Revenue, Scenarios, Sensitivity)
- Key formulas with cell references
- Instructions for updating assumptions
- Charts to include

### Deliverable 3: Sensitivity Analysis and Key Findings

- Ranked list of input variables by impact
- Top 3 levers the team should focus on
- Scenario comparison table
- Recommended targets based on the model

---

## Cross-References

Related skills: `plg-metrics`, `growth-loops`, `plg-strategy`
