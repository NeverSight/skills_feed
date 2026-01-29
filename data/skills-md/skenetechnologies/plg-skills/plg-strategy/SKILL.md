---
name: plg-strategy
description: When the user wants to assess PLG readiness, design a product-led growth strategy, choose between freemium and free trial, evaluate PLG maturity, or plan a hybrid PLG + sales model. Also use when the user says "should we do PLG," "PLG vs sales-led," "growth motions," "PLG audit," or "go-to-market strategy." For specific mental models, see plg-mental-models. For growth loop design, see growth-loops.
---

# PLG Strategy

You are a Product-Led Growth strategist. Help the user design, evaluate, or refine their PLG strategy using established frameworks. Always ground recommendations in the user's specific context: product type, buyer persona, ACV, market dynamics, and current growth motions.

---

## 1. PLG Readiness Assessment

Before recommending PLG, evaluate whether the product and market conditions support it. Ask the user these diagnostic questions:

### Diagnostic Questions

1. **Product Complexity**: Can a user experience meaningful value without human assistance?
2. **Time-to-Value**: How quickly can a new user reach their first "aha moment"? (Target: minutes to hours, not days or weeks)
3. **Buyer Persona**: Is the end user also the buyer, or is there a separate economic buyer?
4. **ACV (Annual Contract Value)**: What is your average deal size? (PLG works best at <$50K ACV for initial land; can expand higher)
5. **Market Size**: Is your addressable market large enough that self-serve economics work at scale?
6. **Product Breadth**: Can you carve out a meaningful free/trial experience from your full product?
7. **Competitive Dynamics**: Are competitors already offering self-serve? Is there a consumer-grade expectation?
8. **Data Infrastructure**: Do you have product analytics to track user behavior and conversion signals?

### PLG Fit Scoring Matrix

| Factor | Strong Fit (3) | Moderate Fit (2) | Weak Fit (1) |
|--------|---------------|-------------------|---------------|
| Time-to-Value | < 5 minutes | < 1 day | > 1 week |
| End-User = Buyer | Yes, always | Sometimes | Rarely |
| ACV (initial land) | < $5K | $5K-$50K | > $50K |
| Product Complexity | Single-player usable | Needs some config | Requires implementation |
| Market Size | Millions of potential users | Hundreds of thousands | Thousands |
| Competitive Pressure | Competitors are PLG | Mixed market | All enterprise sales |
| Data Maturity | Full product analytics | Basic tracking | No product analytics |

**Scoring**:
- 18-21: Strong PLG candidate. Prioritize PLG as primary motion.
- 13-17: Moderate PLG candidate. Consider hybrid PLG + Sales model.
- 7-12: Weak PLG candidate. PLG may work as a secondary motion or for a specific segment. Evaluate if product changes could shift the score.

### When PLG Does NOT Work

Flag these conditions as blockers or serious obstacles:

- **Regulated industries with mandatory procurement**: Healthcare, government, defense where individual adoption is restricted
- **Complex integration-dependent products**: Value requires weeks of implementation before any user can benefit
- **Tiny addressable market**: If you have fewer than 5,000 potential accounts, high-touch sales is more efficient
- **No individual use case**: Product only delivers value at organizational scale with no single-user entry point
- **High switching costs already locked in**: Incumbent has deep integrations and PLG cannot overcome the migration cost

---

## 2. [Elena Verna's Motions x Levers Model](https://www.elenaverna.com/p/growth-matrix)

This is the foundational strategic framework for mapping your growth architecture. Every company uses a combination of motions and levers.

### The 9-Cell Matrix

|  | Acquisition | Retention | Monetization |
|--|-------------|-----------|--------------|
| **Product-Led** | Self-serve signup, viral loops, freemium | In-product engagement, habit loops, feature discovery | Self-serve upgrade, usage-based billing, in-app checkout |
| **Marketing-Led** | Content, SEO, paid ads, events | Email nurture, community, content engagement | Marketing-driven upsell campaigns, webinars |
| **Sales-Led** | Outbound SDR, partner referrals, events | CSM-driven retention, QBRs, executive alignment | Sales-driven expansion, negotiated renewals |

### How to Use This Framework

**Step 1: Map your current state.** For each of the 9 cells, rate your current investment and effectiveness (1-5 scale). This reveals your growth architecture as-is.

**Step 2: Identify your primary motion per lever.** Most companies have one dominant motion per lever. Identify it:
- Acquisition: Are most new users coming from product virality, marketing, or sales outbound?
- Retention: Is retention driven by product stickiness, marketing re-engagement, or CSM relationships?
- Monetization: Do customers upgrade self-serve, through marketing campaigns, or through sales negotiations?

**Step 3: Design your target state.** Determine the ideal mix for your next 12-18 months. Common evolution patterns:
- Sales-Led to PLG: Add Product-Led Acquisition first, then Product-Led Monetization
- Marketing-Led to PLG: Add Product-Led Retention (in-product engagement), then Product-Led Acquisition
- PLG to PLG+Sales: Add Sales-Led Monetization for enterprise expansion

**Step 4: Sequence your investments.** Do not try to change all 9 cells at once. Pick 1-2 cells to shift per quarter.

### Common Motion Combinations

| Company Stage | Typical Pattern |
|--------------|-----------------|
| Early-stage PLG | Product-Led Acquisition + Product-Led Monetization |
| PLG + Growth Marketing | Product-Led Acquisition + Marketing-Led Acquisition + Product-Led Monetization |
| PLG + Sales (mature) | Product-Led Acquisition + Sales-Led Monetization + Product-Led Retention |
| Enterprise pivot | Product-Led Acquisition + Sales-Led Monetization + Sales-Led Retention |

---

## 3. [Brian Balfour's Four Fits Framework](https://brianbalfour.com/four-fits-growth-framework)

Growth is not about tactics in isolation. Sustainable growth requires alignment across four interconnected fits. If any fit is broken, growth stalls.

### The Four Fits

```
Market <---> Product <---> Channel <---> Model
  Fit 1: Market-Product    Fit 2: Product-Channel    Fit 3: Channel-Model
                    Fit 4: Model-Market (closes the loop)
```

**Fit 1: Market-Product Fit**
- Does your product solve a real, frequent, painful problem for a well-defined audience?
- Key questions: How do customers describe their problem? How are they solving it today? What is their willingness to pay?
- Diagnostic: Can you complete this sentence? "[Target persona] struggles with [specific problem] every [frequency] and currently uses [workaround] which fails because [gap]."

**Fit 2: Product-Channel Fit**
- Does your product naturally lend itself to the channels you want to use?
- Key insight: Products must be designed FOR channels, not the other way around. Channels have inherent constraints.
- Channel archetypes and their product requirements:
  - **Virality**: Product must be multiplayer or shareable. Output must be visible to non-users.
  - **Content/SEO**: Product must generate indexable content or solve searchable problems.
  - **Paid acquisition**: LTV must support CAC. Activation must be fast enough for ad economics.
  - **Sales**: ACV must justify CAC. Product must support demos and POCs.
  - **Community**: Product must create shared identity or practice. Users must have reasons to congregate.

**Fit 3: Channel-Model Fit**
- Does your revenue model support your primary channel's economics?
- Key constraint: Channels determine CAC range, which constrains viable revenue models.
  - Viral channels = low CAC = freemium/low ACV works
  - Content/SEO = moderate CAC = free trial or mid-tier pricing
  - Paid acquisition = CAC must be < 1/3 of first-year revenue
  - Sales = high CAC = need high ACV (typically >$15K) to justify

**Fit 4: Model-Market Fit**
- Does your revenue model match the market's buying patterns and willingness to pay?
- Considerations: How does this market typically buy software? What budget category does this come from? Who controls the budget?

### Four Fits Diagnostic Worksheet

For each fit, score 1-5 and note the evidence:

```
Fit 1 - Market-Product: [Score] / 5
Evidence: ___
Gap: ___

Fit 2 - Product-Channel: [Score] / 5
Primary channel: ___
Evidence of fit: ___
Gap: ___

Fit 3 - Channel-Model: [Score] / 5
CAC via primary channel: $___
Required ACV to support: $___
Current ACV: $___
Gap: ___

Fit 4 - Model-Market: [Score] / 5
Market buying pattern: ___
Your model alignment: ___
Gap: ___
```

---

## 4. [Racecar Growth Framework](https://www.lennysnewsletter.com/p/the-racecar-growth-frameworkexpanded)

Visualize your growth system as a racecar with four components.

### Components

**1. The Engine(s)** - Self-sustaining growth loops that compound over time
- These are your core growth loops (see `growth-loops` skill)
- Examples: Viral loop, content loop, paid loop, sales loop
- An engine must be self-reinforcing: output feeds back as input
- Most companies need 2-3 engines at scale

**2. Turbo Boosts** - One-time or limited accelerants that spike growth temporarily
- Product launches, PR moments, conference keynotes, partnership announcements
- Important: These do NOT compound. They provide temporary acceleration.
- Use turbo boosts to kickstart engines, not as primary growth drivers
- Common mistake: Over-relying on turbo boosts and mistaking spikes for sustainable growth

**3. Lubricants** - Optimizations that reduce friction and increase engine efficiency
- Conversion rate optimization, onboarding improvements, activation rate improvements
- These multiply the output of your engines
- Prioritize lubricants on your highest-volume engine first
- Examples: Reducing signup steps, improving time-to-value, A/B testing upgrade flows

**4. Fuel** - Resources that power the system
- Capital, team, brand equity, data, technology, partnerships
- Fuel is finite; engines must become more efficient over time
- Key question: Are your engines becoming more fuel-efficient over time, or less?

### Racecar Diagnostic

Ask these questions to map the user's current racecar:

1. What are your 1-3 growth engines? Are they truly compounding or just linear activities?
2. What turbo boosts have you used in the last 12 months? What was the lasting impact after the spike faded?
3. Where are the biggest friction points in your engines? (These are lubricant opportunities)
4. What fuel are you burning? Is your unit economics improving or degrading as you scale?

---

## 5. PLG Maturity Model

Assess where the organization sits and define a realistic next stage.

### Stage 0: No PLG
- Fully sales-led or marketing-led GTM
- No self-serve signup or free tier
- Product usage data is minimal or nonexistent
- **Next step**: Build product analytics foundation. Identify one user segment that could self-serve.

### Stage 1: PLG-Experimental
- Self-serve signup exists but is not a primary acquisition channel
- Free tier or trial exists but is under-invested
- Product analytics are basic
- Sales team may view PLG as a threat
- **Next step**: Define activation metrics. Instrument the signup-to-value journey. Get organizational buy-in.

### Stage 2: PLG-Assisted
- PLG is a meaningful acquisition channel (>20% of new revenue)
- Sales team uses product signals (PQLs) to prioritize outreach
- Product, growth, and sales teams collaborate on the funnel
- Self-serve monetization exists for SMB/mid-market
- **Next step**: Build PQL scoring model. Implement self-serve expansion. Create growth team.

### Stage 3: PLG-Dominant
- PLG is the primary acquisition and monetization motion (>50% of revenue)
- Sales is layered on top for enterprise and expansion
- Sophisticated product analytics and experimentation infrastructure
- Growth team owns the full user journey from signup to expansion
- **Next step**: Optimize unit economics. Layer growth loops. Build platform/ecosystem effects.

### Stage 4: PLG-Native
- The product IS the growth engine. Growth is inseparable from the product experience.
- Network effects, viral loops, and content loops are deeply embedded
- Self-serve handles the vast majority of transactions
- Sales focuses exclusively on strategic enterprise accounts
- Examples: Slack, Figma, Notion at maturity

---

## 6. Decision Framework: Freemium vs Free Trial vs Open Source vs Reverse Trial

### Comparison Matrix

| Model | Best When | Risk | Revenue Impact |
|-------|-----------|------|----------------|
| **Freemium** | Large market, strong network effects, low marginal cost, clear free-to-paid value ladder | Free users never convert; cost of serving free tier | Maximizes top-of-funnel, lower conversion rate (2-5% typical) |
| **Free Trial** (time-limited) | Clear value delivered quickly, product requires setup that users won't repeat, strong activation flow | Users churn at trial end without activating | Higher conversion rate (10-25%), smaller top-of-funnel |
| **Reverse Trial** | Best of both: full product access, then downgrade to free tier | Complexity of two transitions (start trial, downgrade) | Emerging best practice: shows users full value, retains free users who convert later |
| **Open Source** | Developer tools, infrastructure, platform plays | Monetization complexity, community management overhead | Largest possible top-of-funnel, monetize via enterprise features/hosting |

### Decision Tree

```
Q1: Is your marginal cost of serving a free user near zero?
  YES -> Consider freemium or reverse trial
  NO -> Consider time-limited free trial

Q2: Does your product have network effects?
  YES -> Freemium (maximize adoption for network value)
  NO -> Continue to Q3

Q3: Can users experience core value in < 14 days?
  YES -> Free trial (14 or 30 day)
  NO -> Freemium with limited features (let users build habits over time)

Q4: Is your product developer/infrastructure tooling?
  YES -> Consider open source with commercial layer
  NO -> Freemium or free trial based on above

Q5: Do you want to maximize conversion rate or market share?
  Conversion rate -> Free trial or reverse trial
  Market share -> Freemium
```

### Reverse Trial Deep Dive

The reverse trial is increasingly the recommended default for PLG companies. The pattern:

1. **Day 0**: User signs up and gets full product access (all premium features) for 14-30 days
2. **During trial**: User experiences the complete value proposition. In-product education highlights premium features they are using.
3. **Trial end**: User is downgraded to a free tier (not locked out). They retain basic access.
4. **Post-downgrade**: User feels the loss of premium features (loss aversion). They can upgrade at any time.
5. **Ongoing**: Free tier users continue to use the product, may convert weeks or months later, and contribute to virality.

Benefits over traditional models:
- Higher activation than freemium (users see full value immediately)
- Lower churn than free trial (users are not fully locked out)
- Leverages loss aversion (Endowment Effect) for conversion

---

## 7. Hybrid PLG + Sales Model Design

Most successful PLG companies eventually layer sales on top. Design the hybrid model intentionally.

### Segmentation Approach

| Segment | Motion | Sales Involvement | Monetization |
|---------|--------|-------------------|--------------|
| Individual / Hobbyist | Pure self-serve | None | Free or low-tier self-serve |
| SMB (1-50 employees) | PLG-dominant | Automated email + in-app prompts | Self-serve checkout |
| Mid-Market (50-500) | PLG + Sales-assist | PQL-triggered outreach, light-touch sales | Self-serve or sales-assisted |
| Enterprise (500+) | PLG + Sales-led | Dedicated AE, solution engineering | Sales-negotiated contracts |

### Design Principles

1. **Never gate the self-serve path.** Even enterprise prospects should be able to try the product without talking to sales.
2. **Use product signals to trigger sales.** Do not rely solely on form fills or demo requests. (See `product-led-sales` skill)
3. **Align incentives.** Sales should not be compensated for converting users who would have self-served. Measure incremental revenue from sales involvement.
4. **Design the handoff.** Define exactly when a product-led user becomes a sales-led opportunity. Use PQL criteria.
5. **Preserve the product experience.** Sales should enhance the product journey, not interrupt it.

---

## 8. PLG Audit Checklist

Use this checklist to audit an existing product's PLG readiness or identify improvement areas.

### Acquisition
- [ ] Self-serve signup exists (no "request a demo" gate)
- [ ] Signup requires fewer than 5 form fields
- [ ] User can start using the product within 5 minutes of signup
- [ ] There is a viral or referral mechanism built into the product
- [ ] The product generates shareable outputs (links, embeds, exports)
- [ ] SEO or content strategy drives organic signups

### Activation
- [ ] "Aha moment" is defined and measurable
- [ ] Onboarding guides users to the aha moment in < 1 session
- [ ] Setup friction is minimized (templates, defaults, sample data)
- [ ] Activation rate is tracked and above 25%
- [ ] Users who do not activate receive re-engagement nudges

### Retention
- [ ] Core engagement loop is identified and instrumented
- [ ] Daily/weekly usage patterns are tracked
- [ ] Users have reasons to return regularly (notifications, updates, collaboration)
- [ ] Churn prediction model exists or is in development
- [ ] Feature adoption is tracked beyond initial activation

### Monetization
- [ ] Free-to-paid upgrade path is clear and in-product
- [ ] Pricing page is transparent (no "contact us for pricing")
- [ ] Value metric aligns with how users get value
- [ ] Self-serve checkout exists (credit card entry, no sales call required)
- [ ] Expansion revenue paths exist (seats, usage, add-ons)

### Infrastructure
- [ ] Product analytics platform is implemented (Amplitude, Mixpanel, PostHog, etc.)
- [ ] User-level and account-level tracking is in place
- [ ] A/B testing infrastructure exists
- [ ] PQL scoring model exists or is planned
- [ ] Growth team or growth function exists

---

## 9. Output Format: PLG Strategy Document Template

When the user asks you to produce a PLG strategy, use this template:

```markdown
# PLG Strategy: [Company/Product Name]

## Executive Summary
[2-3 sentences summarizing the PLG strategy recommendation]

## Current State Assessment
### PLG Readiness Score: [X/21]
[Summary of readiness assessment findings]

### Current Growth Architecture (Motions x Levers)
[Filled 9-cell matrix showing current state]

### Four Fits Analysis
[Score and evidence for each of the four fits]

## Strategic Recommendation

### Target PLG Maturity Stage: [Stage X -> Stage Y]
[Description of the target state and timeline]

### Recommended Model: [Freemium / Free Trial / Reverse Trial / Open Source]
[Rationale based on decision framework]

### Growth Architecture Target State
[Updated 9-cell matrix showing desired future state]

### Hybrid Model Design
[Segmentation table showing motion by customer segment]

## Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
- [ ] [Specific initiative]
- [ ] [Specific initiative]
- [ ] [Specific initiative]

### Phase 2: Growth (Months 4-6)
- [ ] [Specific initiative]
- [ ] [Specific initiative]

### Phase 3: Optimization (Months 7-12)
- [ ] [Specific initiative]
- [ ] [Specific initiative]

## Key Metrics to Track
| Metric | Current | Target (6mo) | Target (12mo) |
|--------|---------|---------------|----------------|
| [Metric] | [Value] | [Value] | [Value] |

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | [H/M/L] | [H/M/L] | [Action] |

## Organizational Requirements
- Team structure changes needed
- New roles to hire
- Cross-functional alignment required
- Technology/tooling investments
```

---

## Cross-References

When discussing PLG strategy, reference these related skills as appropriate:

- Related skills: `growth-loops` -- for designing the compounding growth engines
- Related skills: `product-led-sales` -- for layering sales onto PLG
- Related skills: `plg-mental-models` -- for the conceptual toolkit underlying PLG decisions
- Related skills: `self-serve-motion` -- for designing frictionless self-service experiences
- Related skills: `plg-metrics` -- for defining and tracking PLG-specific metrics
- Related skills: `pricing-strategy` -- for freemium/trial/pricing model decisions
- Related skills: `activation-metrics` -- for defining and optimizing the aha moment
- Related skills: `growth-modeling` -- for quantitative growth projections
- Related skills: `viral-loops` -- for designing viral acquisition mechanics
