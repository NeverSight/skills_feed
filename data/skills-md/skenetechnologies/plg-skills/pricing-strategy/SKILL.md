---
name: pricing-strategy
description: When the user wants to design or optimize pricing, packaging, or monetization -- including tier structure, freemium design, value metrics, or price research. Also use when the user says "pricing page," "how to price," "freemium vs free trial," "Good-Better-Best tiers," or "value-based pricing." For feature gating, see feature-gating. For trial optimization, see trial-optimization. For usage-based models, see usage-based-pricing.
---

# Pricing Strategy

You are a pricing strategist. A comprehensive framework for designing pricing, packaging, and monetization for product-led growth companies. Pricing is the single highest-leverage growth lever most companies underinvest in.

---

## 1. [Phil Carter's 5 Ps of PLG Monetization](https://philgcarter.substack.com/p/the-subscription-value-loop)

Before diving into specific tactics, understand the five interconnected dimensions of PLG monetization:

| Dimension | Definition | Key Question |
|-----------|-----------|--------------|
| **Pricing** | How much you charge | What price point maximizes revenue and growth? |
| **Packaging** | What is included in each tier | Which features go in which plan? |
| **Paywalls** | Where and how you gate value | What triggers the upgrade moment? |
| **Payments** | How customers pay | What is the purchase flow and billing mechanics? |
| **Promotions** | Discounts, trials, and incentives | How do you reduce friction to first purchase? |

These five dimensions must be designed together. Optimizing one in isolation creates misalignment. For example, a great pricing model with a broken payment flow still loses conversions.

---

## 2. Value-Based Pricing Methodology

### Principle

Price should reflect the value your product delivers to the customer, not your cost to deliver it. Cost-plus pricing leaves money on the table. Competitor-based pricing ignores your unique value.

### Steps to Value-Based Pricing

1. **Identify the customer's alternative** -- What would they do without your product? (Manual process, competitor, custom build, hire someone)
2. **Quantify the value gap** -- How much time, money, or risk does your product save compared to the alternative?
3. **Apply the value capture ratio** -- Typically capture 10-25% of the value you create. If you save a customer $100K/year, pricing at $10K-$25K/year is defensible.
4. **Segment by willingness-to-pay** -- Different customer segments derive different value. Use tiered pricing to capture value from each segment.
5. **Validate with research** -- Use the methods in Section 9 to validate your pricing hypothesis.

### Value-Based Pricing Worksheet

```
Customer segment:        [e.g., Mid-market marketing teams]
Current alternative:     [e.g., Manual reporting in spreadsheets]
Time saved per week:     [e.g., 8 hours]
Hourly cost of that time:[e.g., $75/hour]
Annual value created:    [e.g., 8 x $75 x 52 = $31,200]
Value capture ratio:     [e.g., 15%]
Target price point:      [e.g., $31,200 x 0.15 = $4,680/year = $390/month]
```

---

## 3. Value Metric Identification

The value metric is the unit you charge on. It is the single most important pricing decision.

### What Makes a Good Value Metric

A strong value metric satisfies all four criteria:

| Criterion | Test | Example |
|-----------|------|---------|
| **Scales with value** | As the customer gets more value, the metric increases | Seats scale with team adoption |
| **Easy to understand** | Customer can predict their bill | "Per user per month" is clear |
| **Predictable** | Customer can forecast spend | API calls can spike unexpectedly -- less predictable |
| **Hard to game** | Customer cannot easily reduce the metric without reducing usage | "Active users" is harder to game than "registered users" |

### Common Value Metrics by Product Type

| Product Type | Common Metrics | Notes |
|-------------|---------------|-------|
| Collaboration tools | Seats / active users | Slack, Notion, Figma |
| Infrastructure / API | API calls, compute, storage | Twilio, AWS, Snowflake |
| Marketing tools | Contacts, emails sent, visitors tracked | HubSpot, Mailchimp |
| Sales tools | Seats + contacts/records | Salesforce, Apollo |
| Analytics | Events tracked, MTUs | Amplitude, Mixpanel |
| AI products | Credits, tokens, generations | OpenAI, Jasper |
| Design tools | Projects, exports, editors | Canva, Figma |

### Value Metric Selection Process

1. List 5-8 candidate metrics
2. Score each on the four criteria (1-5 scale)
3. Evaluate operational feasibility (can you meter it accurately?)
4. Test customer understanding (do they intuitively get it?)
5. Model revenue impact (does it grow as customers grow?)

---

## 4. Three Pricing Dimensions

Every pricing model is defined by three dimensions. Design them in this order:

### Dimension 1: Packaging (What is in each tier)

This is covered in depth in the `feature-gating` skill. Key principles:
- Each tier should serve a distinct buyer persona or use case
- Moving up a tier should feel like a natural graduation, not a tax
- Every tier must deliver standalone value

### Dimension 2: Metric (How you charge)

Choose from:
- **Flat rate**: One price for everything (simple but leaves money on the table)
- **Per seat**: Charge per user (most common in B2B SaaS)
- **Usage-based**: Charge per unit consumed (see `usage-based-pricing` skill)
- **Hybrid**: Base platform fee + usage or seat component
- **Credit-based**: Pre-purchased credits consumed by usage

### Dimension 3: Price Point (How much)

Set using value-based methodology (Section 2) and validated with research (Section 9).

---

## 5. Tier Structure: Good-Better-Best

### The Standard 3-Tier Model

| Tier | Purpose | Typical Features | Buyer |
|------|---------|-----------------|-------|
| **Good** (Starter/Basic) | Entry point, proves value | Core features, limited usage | Individual / small team |
| **Better** (Pro/Growth) | Workhorse plan, drives most revenue | All core + advanced features, higher limits | Growing team / department |
| **Best** (Business/Enterprise) | Premium, high-value | Everything + admin, security, support, integrations | Large team / organization |

### Design Principles

1. **The "Better" plan should be most popular** -- Design it to be the obvious choice. Highlight it as "Most Popular" or "Recommended."
2. **The "Good" plan should be a real product** -- Not a crippled demo. Users should be able to accomplish real work.
3. **The "Best" plan justifies its price** -- Include features that genuinely matter to larger organizations (SSO, SAML, audit logs, SLAs, dedicated support).
4. **Price anchoring** -- The "Best" plan makes the "Better" plan look like a great deal.

### When to Add a 4th Tier

Add a dedicated Free tier (making it 4 tiers total: Free, Starter, Pro, Enterprise) when:
- Your product benefits from network effects
- You want broad top-of-funnel adoption
- The marginal cost of free users is low
- Free users generate data, content, or referrals that benefit paid users

### Enterprise Tier Design

Enterprise tiers typically include:
- SSO/SAML authentication
- Advanced admin controls and role management
- Audit logs and compliance features
- Custom data retention
- Dedicated support (SLA, named CSM)
- Custom integrations
- Volume discounts
- Custom contracts and invoicing
- Uptime SLAs

Pricing: "Contact Sales" is standard for enterprise. Provide enough information on the pricing page that prospects self-qualify.

---

## 6. Freemium Design

### What to Give Free

A strong free tier should include:

- **Core functionality** that demonstrates the product's value proposition
- **Enough capacity** for a single user or small team to do real work
- **Collaboration features** that drive viral growth (invite teammates)
- **Integrations** that increase stickiness

### What to Gate

Gate features that:
- Deliver premium value beyond basic use cases
- Serve team/organizational needs (admin, security, compliance)
- Require meaningful compute or storage resources
- Differentiate your paid plans from competitors

### Freemium Decision Tree

```
Is the feature essential to understanding the product's value?
├── YES → Include in free tier
└── NO
    ├── Does the feature drive viral or collaborative behavior?
    │   ├── YES → Include in free tier
    │   └── NO
    │       ├── Does the feature serve advanced/power users?
    │       │   ├── YES → Gate behind Pro or Business tier
    │       │   └── NO
    │       │       └── Does the feature serve team/org needs?
    │       │           ├── YES → Gate behind Team or Business tier
    │       │           └── NO → Evaluate case-by-case
    └── (see feature-gating skill for complete framework)
```

---

## 7. Free Trial Design

### Trial Type Selection

| Factor | No-Card Trial | Card-Required Trial | Reverse Trial |
|--------|--------------|-------------------|---------------|
| Signup volume | High | Lower (30-50% fewer) | High |
| Conversion rate | 3-8% | 40-60% | Varies (5-15%) |
| Lead quality | Mixed | Higher intent | Mixed |
| Best for | Broad market, low ACV | Focused market, higher ACV | Strong free tier exists |
| Risk | Low-quality signups | Friction at signup | Users upset at downgrade |

### Trial Length Decision Framework

1. **How long does it take to reach the aha moment?** Measure time-to-activation for successful users.
2. **Add a buffer.** If aha moment takes 3 days, a 7-day trial works. If it takes 7 days, use 14 days.
3. **Consider the buying process.** Enterprise buyers need more time for procurement and team evaluation.
4. **Shorter is usually better.** Shorter trials create urgency. Only extend if users genuinely need more time.

| Trial Length | Best For | Examples |
|-------------|---------|---------|
| 7 days | Simple products, fast time-to-value | Productivity apps, simple tools |
| 14 days | Standard B2B SaaS | Most mid-market products |
| 30 days | Complex products, team deployment | Enterprise tools, data platforms |

### [Reverse Trial (Elena Verna Framework)](https://amplitude.com/blog/reverse-trial)

The reverse trial gives new users access to the full premium product for a limited time, then downgrades them to the free tier. This approach:

1. Shows users the full value before asking them to pay
2. Creates a sense of loss when premium features are removed
3. Works best when the free tier is genuinely useful (so users stay)
4. Requires clear communication about what changes at trial end

**When reverse trial works:** Strong free tier, obvious premium features, product where you need time to build data/content.

**When it does not work:** No viable free tier, premium value is not obvious, users churn instead of downgrading.

See `trial-optimization` for detailed implementation guidance.

---

## 8. Annual vs Monthly Pricing

### Standard Approach

- Offer both monthly and annual billing
- Annual discount: 15-20% (equivalent to "2 months free" or "save 17%")
- Display annual pricing as monthly equivalent ("$29/mo billed annually")
- Default the pricing page toggle to annual

### Nudging Annual Plans

1. **Visual emphasis** -- Make annual the default selection, show savings prominently
2. **Framing** -- "Save $348/year" is more compelling than "Save 17%"
3. **In-app upgrade prompts** -- After a few months of monthly billing, suggest switching to annual
4. **Checkout incentive** -- Offer an additional perk for annual (e.g., bonus features, onboarding session)

### When Monthly-Only Works

- Very early stage (need flexibility to change pricing)
- Usage-based models where annual commitment is hard to predict
- Very low price points where annual savings are trivial

---

## 9. Pricing Research Methods

### Van Westendorp Price Sensitivity Meter

Ask four questions:
1. At what price would this be **too expensive** (would not consider)?
2. At what price would this be **expensive but worth considering**?
3. At what price would this be a **bargain**?
4. At what price would this be **too cheap** (suspect quality)?

Plot the cumulative distributions. The intersections reveal:
- **Point of Marginal Cheapness**: intersection of "too cheap" and "expensive"
- **Point of Marginal Expensiveness**: intersection of "too expensive" and "bargain"
- **Optimal Price Point**: intersection of "too cheap" and "too expensive"
- **Acceptable Price Range**: between marginal cheapness and marginal expensiveness

**Sample size needed:** 100-300 respondents per segment.

### MaxDiff Analysis

Present sets of features and ask respondents to pick the most and least important. Produces a ranked list of feature importance that informs packaging decisions. More reliable than direct importance ratings because it forces tradeoffs.

### Willingness-to-Pay (WTP) Survey

Simple direct approach:
1. Describe the product and its benefits
2. Ask: "How much would you be willing to pay per month for this product?"
3. Ask: "At what price would you definitely NOT buy this product?"
4. Segment responses by persona

**Limitation:** Stated WTP is typically 15-30% higher than actual WTP. Adjust accordingly.

### Competitive Benchmarking

1. Document competitor pricing (tiers, features per tier, price points)
2. Identify where you are positioned (budget, mid-market, premium)
3. Map your unique features to identify pricing leverage
4. Note: Do not let competitor pricing drive your strategy entirely -- use it as a reference point.

---

## 10. Price Increase Strategies

### Grandfather vs Migrate

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Grandfather** (existing users keep old price) | No churn risk, goodwill | Revenue left on table, complexity | Small price changes, loyal customers |
| **Migrate with notice** (existing users move to new price) | Revenue uplift, simplicity | Churn risk, customer pushback | Significant price changes, clear value increase |
| **Hybrid** (grandfather for N months, then migrate) | Balanced approach | Complexity | Most situations |

### Price Increase Communication Template

```
Subject: Updates to [Product] pricing

Hi [Name],

We are writing to let you know about upcoming changes to [Product] pricing,
effective [date -- give at least 30 days notice, ideally 60-90].

What is changing:
- [Specific changes, clearly stated]

Why:
- [Honest reason: investment in product, new features, rising costs]

What this means for you:
- Your current plan ([plan name]) will change from [$X/mo] to [$Y/mo]
- This reflects a [Z%] increase

What you get:
- [List recent and upcoming improvements that justify the increase]

Your options:
- Continue on your current plan at the new price
- [Downgrade option if available]
- [Annual billing option if it saves money]

If you have any questions, reply to this email or [contact support link].

Thank you for being a [Product] customer.

[Signature]
```

### Timing Best Practices

- Give 30-90 days notice (longer for enterprise)
- Avoid holidays, year-end, or budget cycle conflicts
- Pair with a major product update or feature release
- Offer a "lock in" period at the old price for annual commitments
- Communicate directly (email, not just a blog post)

---

## 11. SaaS Pricing Page Best Practices

### Essential Elements

1. **Clear tier names** with one-line descriptions
2. **Highlighted recommended plan** (visual emphasis, "Most Popular" badge)
3. **Plan comparison table** with feature checkmarks
4. **Price displayed prominently** with billing period (monthly/annual toggle)
5. **CTA buttons** on every plan (with differentiated copy: "Start Free" vs "Start Trial" vs "Contact Sales")
6. **FAQ section** addressing common objections (Can I switch plans? What happens when I cancel? Is there a setup fee?)
7. **Social proof** (customer logos, testimonial, number of customers)
8. **Trust signals** (security badges, uptime guarantee, money-back guarantee)

### Design Principles

- Limit to 3-4 plans (decision fatigue reduces conversion)
- Make the recommended plan visually prominent (larger card, different color, badge)
- Use progressive disclosure for feature lists (show 5-8 key features, expandable "see all features")
- Include a plan comparison toggle between monthly and annual
- Put enterprise "Contact Sales" as the last option, not a full pricing card

---

## 12. Pricing Metrics

Track these metrics to evaluate your pricing strategy:

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **ARPU** | Total revenue / total customers | Varies by market; track trend |
| **Expansion rate** | Expansion MRR / beginning MRR | >5% monthly is strong |
| **Plan distribution** | % of customers on each plan | "Better" plan should be 40-60% |
| **Upgrade rate** | Upgrades / eligible customers per period | 3-7% monthly |
| **Downgrade rate** | Downgrades / paid customers per period | <2% monthly |
| **Free-to-paid rate** | Conversions / free users per period | 2-5% for freemium, higher for trials |
| **Price sensitivity** | Churn rate change after price increase | <5% incremental churn is acceptable |
| **Revenue per employee** | ARR / headcount | $200K-$400K+ for efficient SaaS |

---

## 13. Diagnostic Questions

When helping a user with pricing strategy, ask these questions to understand their context:

1. What does your product do and who is it for?
2. What is your current pricing model? (If any)
3. What alternatives do your customers have? (Competitors, manual processes, doing nothing)
4. What is the primary value your product delivers? (Time savings, revenue increase, cost reduction, risk reduction)
5. Can you quantify the value for a typical customer?
6. What is your current free-to-paid conversion rate?
7. What does your customer size distribution look like? (Individual, SMB, mid-market, enterprise)
8. Are there natural usage dimensions that scale with value? (Users, volume, features)
9. What is your current ARPU and target ARPU?
10. Have you done any pricing research? (Customer interviews, surveys, A/B tests)

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find pricing page**: Search for `*pricing*`, `*plans*`, `*billing*` in page/route components
2. **Find tier definitions**: Search for `plan`, `tier`, `PLANS`, `PRICING`, `subscription` in constants or config files
3. **Check payment integration**: Search for `stripe`, `paddle`, `chargebee`, `recurly`, `braintree`, `lemonsqueezy` in dependencies and imports
4. **Find price values**: Search for dollar amounts, price variables, or pricing API calls
5. **Check billing intervals**: Search for `monthly`, `annual`, `yearly`, `interval`, `billing_period`
6. **Find feature-tier mapping**: Look for which features are included in which plan -- often in a features matrix or plan config
7. **Check for free tier**: Search for `free`, `starter`, `hobby` plan definitions -- what's included?
8. **Find upgrade triggers**: Search for code that prompts upgrades -- usage limits, feature locks, trial expiry

Report: describe the current pricing structure, payment provider, tier definitions, and what's included in each plan.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 14. Output Format

When completing a pricing strategy engagement, deliver the following document:

```markdown
# Pricing Strategy: [Product Name]

## Executive Summary
[2-3 sentences on the recommended approach]

## Value Metric
- Primary metric: [e.g., per seat per month]
- Secondary metric: [e.g., usage-based add-on for storage]
- Rationale: [Why this metric aligns with customer value]

## Tier Structure

### Free Tier
- Target user: [persona]
- Included: [key features and limits]
- Purpose: [acquisition, activation, viral growth]

### Starter / Pro / Business (repeat for each tier)
- Target user: [persona]
- Price: [$X/seat/month billed annually, $Y/seat/month billed monthly]
- Included: [key features and limits]
- Upgrade trigger: [what drives users to this tier]

### Enterprise
- Target user: [persona]
- Pricing model: [custom quote, starting at $X]
- Included: [key features: SSO, admin, compliance, SLA, support]

## Feature-Tier Matrix
| Feature | Free | Starter | Pro | Business | Enterprise |
|---------|------|---------|-----|----------|------------|
| [Feature 1] | Y | Y | Y | Y | Y |
| [Feature 2] | - | Y | Y | Y | Y |
| ... | ... | ... | ... | ... | ... |

## Pricing Page Recommendations
[Layout, copy, CTA, FAQ recommendations]

## Migration Plan
[How to move from current pricing to new pricing]

## Metrics and Success Criteria
[KPIs to track and targets to hit]
```

---

## 15. Related Skills

- `feature-gating` -- Detailed framework for deciding what goes in each tier
- `trial-optimization` -- Maximizing conversion from free trial to paid
- `expansion-revenue` -- Growing revenue from existing customers through upgrades
- `usage-based-pricing` -- Deep dive into consumption and metered billing models
- `paywall-upgrade-cro` -- Optimizing the upgrade flow and paywall experience
