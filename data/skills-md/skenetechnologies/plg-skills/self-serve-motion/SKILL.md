---
name: self-serve-motion
description: When the user wants to reduce friction in the self-serve buying experience, optimize in-product checkout, remove "contact sales" gates, or design self-serve onboarding and support. Also use when the user says "frictionless," "self-service," "remove sales gates," "no-demo experience," or "friction audit." For signup flow optimization, see signup-flow-cro. For pricing page design, see pricing-strategy.
---

# Self-Serve Motion

You are a self-serve motion designer. Help the user audit, design, and optimize a frictionless self-service experience from first touch through purchase and expansion. The goal is to enable users to discover value, activate, convert, and expand without ever needing to talk to a human -- unless they choose to.

## Diagnostic Questions

Before auditing the self-serve motion, ask the user:

1. Can a user sign up, onboard, and start getting value without talking to anyone?
2. Can a user upgrade to a paid plan without talking to sales?
3. Where in the user journey do you currently require human interaction? (Demo, sales call, support)
4. What is your current self-serve conversion rate (signup to paid)?
5. What is the average time from signup to first purchase?
6. Do you have in-product checkout, or does upgrading redirect to an external page?
7. What percentage of revenue comes from self-serve vs sales-assisted?
8. What are the top support tickets from users trying to do things self-serve?

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Trace the signup-to-value flow**: Starting from the signup route, follow the code path a new user takes -- signup, onboarding, first action, core value
2. **Find checkout flow**: Search for `*checkout*`, `*payment*`, `*subscribe*`, `*purchase*` -- is there an in-product checkout or does it redirect externally?
3. **Check for "Contact Sales" gates**: Search for `contact-sales`, `book-demo`, `talk-to-sales`, `request-demo` -- where do these appear?
4. **Find self-serve upgrade path**: Can a user upgrade their plan entirely within the product? Trace the upgrade flow
5. **Check for self-serve support**: Search for `*help*`, `*support*`, `*knowledge-base*`, `*docs*`, `*faq*` -- what self-serve support exists?
6. **Find friction points**: Look for places where the user flow stops -- required fields, manual approval, waiting states, "we'll get back to you"
7. **Check seat/team management**: Can users add team members self-serve? Search for `invite`, `add-member`, `team`, `seat`
8. **Find billing management**: Search for `billing`, `invoice`, `payment-method`, `cancel`, `downgrade` -- can users manage billing self-serve?

Report: map the self-serve journey with friction points highlighted. Flag anywhere users are forced out of self-serve.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 1. Self-Serve Spectrum

Design along a spectrum -- push as much of the journey as possible toward self-serve, reserving sales assistance for where it genuinely adds value:

```
Fully Self-Serve <------------------------------------------------> Fully Sales-Assisted

  Stripe checkout    Notion team plan    Figma enterprise    Salesforce enterprise
  (100% self-serve)  (mostly self-serve) (self-serve trial,  (fully sales-led)
                                          sales for contract)
```

---

## 2. Self-Serve Audit: Mapping the Full Journey

### Journey Map

```
AWARENESS -> LANDING -> SIGNUP -> ONBOARDING -> ACTIVATION -> ENGAGEMENT
  -> UPGRADE CONSIDERATION -> PURCHASE -> EXPANSION -> RENEWAL
```

At each step, identify: what the user does, what friction exists, and whether the step is self-serve or requires human intervention.

### Friction Inventory Checklist

**Signup Friction**
- [ ] More than 3 form fields required
- [ ] Email verification required before product access
- [ ] Phone number or company info required upfront
- [ ] Credit card required upfront (for freemium)
- [ ] No social/SSO signup option
- [ ] No clear value proposition on signup page

**Onboarding Friction**
- [ ] Mandatory product tour that cannot be skipped
- [ ] Empty state with no guidance (blank canvas problem)
- [ ] Requires data import or integration before any value
- [ ] No templates, sample data, or quickstart content
- [ ] Demo or sales call required before product access

**Pricing/Evaluation Friction**
- [ ] Pricing hidden behind "Contact Sales"
- [ ] Plan comparison confusing or incomplete
- [ ] No free tier or trial available
- [ ] Value metric unclear
- [ ] No calculator for usage-based pricing

**Checkout Friction**
- [ ] Checkout requires leaving the product
- [ ] Only annual billing available (no monthly)
- [ ] Only credit card accepted (no invoice for mid-market)
- [ ] Complex multi-step checkout
- [ ] Tax calculation unclear or surprising
- [ ] Purchase requires approval workflow

**Expansion Friction**
- [ ] Adding seats requires contacting sales or support
- [ ] Upgrading plan requires contacting sales
- [ ] No self-serve plan change (up or down)
- [ ] Usage overages trigger sales contact instead of self-serve upgrade

**Support Friction**
- [ ] No searchable knowledge base
- [ ] No in-app help or contextual docs
- [ ] Support requires phone call or email only
- [ ] Documentation outdated or incomplete

---

## 3. In-Product Checkout Design

### Checkout Flow Template

```
TRIGGER: User clicks "Upgrade" (in-product button, limit notification, or pricing page)
  |
STEP 1: PLAN SELECTION
  Show 2-3 plans side by side with feature comparison
  Highlight recommended plan, show monthly/annual toggle with savings %
  Pre-select plan most relevant to user's current usage
  |
STEP 2: CONFIGURATION
  Number of seats (pre-filled with current team size + buffer)
  Billing period (monthly vs annual, show savings)
  Add-ons (if applicable), show calculated total
  |
STEP 3: PAYMENT
  Credit card form (Stripe Elements or equivalent)
  OR invoice option for annual plans > $1K/year
  Show total with tax, apply promo code
  |
STEP 4: CONFIRMATION
  What plan they are on, new features/limits, next billing date
  Immediate feature unlock (no delay)
  |
STEP 5: POST-PURCHASE ACTIVATION
  Guide user to newly unlocked feature: "You now have access to [Feature]. Try it now."
```

### Upgrade Prompt Patterns

**Contextual (most effective):**
- User hits usage limit: "You've reached your 3-project limit. Upgrade to Pro for unlimited."
- User tries premium feature: "Custom branding is a Pro feature. Upgrade to unlock."
- User's team grows: "You've invited 6 members. The Team plan supports unlimited with admin controls."

**Milestone-based:**
- After activation: "You've created your first project! Upgrade for advanced features."
- After consistent usage: "You've used [Product] for 3 weeks. Teams like yours typically upgrade for [benefit]."

**Anti-patterns to avoid:**
- Pop-up prompts during critical workflows
- Upgrade prompts before user has experienced value
- More than 1-2 upgrade prompts per session
- Hiding the "close" or "not now" option

---

## 4. Self-Serve vs Sales-Assist Decision Framework

### Decision Matrix by Segment and ACV

| Segment | ACV Range | Signup | Onboarding | Purchase | Expansion | Support |
|---------|-----------|--------|------------|----------|-----------|---------|
| Individual | $0-$500/yr | Self-serve | Self-serve | Self-serve | Self-serve | Self-serve |
| Small Team | $500-$5K/yr | Self-serve | Self-serve | Self-serve | Self-serve | Self-serve + chat |
| Mid-Market | $5K-$25K/yr | Self-serve | Self-serve + optional call | Self-serve or sales-assist | Self-serve + CSM | Priority support |
| Upper Mid-Market | $25K-$100K/yr | Self-serve | Guided call offered | Sales-assisted | CSM-driven | Dedicated support |
| Enterprise | $100K+/yr | Self-serve (never gate!) | Dedicated onboarding | Sales-negotiated | AE + CSM | Named support team |

**Key principle:** Make the self-serve path available to ALL segments. Even enterprise buyers should be able to sign up and try the product. Sales adds value on top of self-serve; it does not replace it.

### When Sales-Assist Adds Value (Keep)

- Custom contracts with specific terms (SLA, DPA, BAA)
- Security and compliance reviews (SOC 2, HIPAA)
- Volume discounts requiring negotiation
- Multi-year commitments, on-prem or private cloud

### When Sales-Assist Destroys Value (Remove)

- Standard plan purchases under $10K/year
- Seat additions to existing plans
- Plan upgrades within standard tiers
- Basic product questions docs could answer
- Demo requests for features available in-product

---

## 5. Payment Flow Optimization

### Card-First vs Invoice

| Approach | Best For |
|----------|----------|
| Card-first | SMB, individual, quick transactions |
| Invoice option | Mid-market, annual plans > $1K |
| Hybrid (card default, invoice available) | All segments |

Default to card-first. Offer invoice as self-serve alternative (user fills billing details, receives invoice automatically) for annual plans above $1K-$5K/year.

### Monthly vs Annual Toggle

```
[Monthly: $30/mo]   [Annual: $24/mo (save 20%)]  <-- highlight annual
```

- Show monthly price on annual plans, not total annual cost
- Display savings as percentage and/or absolute amount
- Pre-select annual for 30+ day users (already committed)
- Pre-select monthly for new users (lower commitment)

### Checkout UI Examples

**Seat-based:**
```
How many seats? [Current team: 8 members]
Suggested: 10 seats (includes 2 buffer)
$24/seat/month x 10 seats = $240/month
Billed annually: $2,880/year (save 20%)
```

**Usage-based:**
```
Estimate your monthly usage:
[Slider: 0 --------|-------------- 100K]
Current usage: ~15K events/month
Estimated cost: $49/month (includes 20K events)
Overage rate: $0.002/event beyond 20K
```

---

## 6. Self-Serve Onboarding

Design so no user needs a demo to understand and extract value:

1. **Immediate value**: Pre-populated sample data or templates. First task completable in < 5 minutes.
2. **Contextual guidance**: Tooltips when relevant (not all at once). Empty states with clear CTAs. Inline help in context.
3. **Templates and presets**: Industry/use-case templates, one-click setup, sample projects.
4. **Progressive complexity**: Start simple, reveal advanced features as users demonstrate readiness.

### Onboarding Checklist Design

- [ ] 3-5 steps maximum
- [ ] First step auto-completed (Endowed Progress Effect)
- [ ] Each step completable in < 2 minutes
- [ ] Steps lead sequentially to the aha moment
- [ ] Progress is visible and persistent across sessions
- [ ] Each step teaches a core feature through doing, not reading

---

## 7. Self-Serve Support

| Support Channel | Self-Serve Level |
|----------------|------------------|
| In-app tooltips and contextual help | Fully self-serve |
| Searchable knowledge base / docs | Fully self-serve |
| AI chatbot | Fully self-serve |
| Community forum | Community-driven |
| Email support | Semi-self-serve (async) |
| Live chat | Semi-self-serve (human-assisted) |

---

## 8. Self-Serve Expansion

### In-Product Seat Addition

```
Settings -> Team -> Add Members

[Current plan: Team Pro - 10 seats ($240/month)]
[8 of 10 seats used]

Add seats:  [-] [2] [+]
New total: 12 seats ($288/month)
Prorated charge for this billing cycle: $32

[Add Seats]    [Cancel]
```

### In-Product Plan Upgrades

```
Settings -> Billing -> Change Plan

Current: Team ($24/seat/month)
Upgrade to: Business ($36/seat/month)

What you'll get:
  [x] Everything in Team, plus:
  [x] SSO / SAML integration
  [x] Advanced permissions
  [x] Priority support

Price change: $24 -> $36/seat/month (10 seats: $240 -> $360/month)
Effective: Immediately (prorated)

[Upgrade to Business]    [Compare all plans]
```

### Self-Serve Expansion Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Self-serve expansion rate | % of expansion revenue from self-serve | > 60% SMB, > 40% mid-market |
| Upgrade completion rate | % who start upgrade and complete it | > 70% |
| Time to expand | Days from first user to paid expansion | Track by segment |

---

## 9. Removing "Contact Sales" Gates

### Remove From

| Surface | Replace With |
|---------|-------------|
| Pricing page for standard plans | Transparent pricing + self-serve checkout |
| Feature comparison page | Interactive comparison with upgrade button |
| Seat addition requests | Self-serve seat management |
| Plan upgrade for standard tiers | Self-serve plan change |
| Basic product questions | Knowledge base, chatbot, or community |

### Keep For

| Situation | Why |
|-----------|-----|
| Custom enterprise contracts (> $50K/year) | Negotiation, custom terms, legal review |
| Custom security/compliance requirements | Security questionnaire, custom DPA |
| Volume discounts beyond published tiers | Pricing negotiation |
| On-premise or private cloud deployment | Infrastructure planning |

### Better Pattern

**Before:**
```
Enterprise Plan
[Contact Sales for Pricing]
```

**After:**
```
Enterprise Plan - $49/seat/month
  Includes: SSO, SCIM, Audit Logs, 99.9% SLA, Priority Support

[Start Free Trial]   [See Full Feature List]

Need custom terms, volume pricing, or security review?
[Talk to our team] (expected response time: < 4 hours)
```

---

## 10. Self-Serve Metrics

### Conversion Rate by Step

```
Visitors to signup page:           100,000
Started signup:                     25,000  (25.0%)
Completed signup:                   18,000  (72.0% of started)
Completed first key action:         8,750   (50.0% of onboarded)
Reached aha moment:                 5,250   (60.0% of first action)
Returned for second session:        3,675   (70.0% of aha moment)
Started checkout:                   735     (50.0% of pricing viewers)
Completed purchase:                 588     (80.0% of started checkout)

Overall visitor-to-paid:            0.59%
Signup-to-paid:                     3.27%
```

### Time-to-Purchase Benchmarks

| Metric | Benchmark |
|--------|-----------|
| Time from signup to first purchase | PLG leaders: 1-7 days for SMB |
| Time from aha moment to purchase | < 14 days |
| Time from pricing page view to purchase | < 48 hours for self-serve |
| Checkout completion time | < 3 minutes |

---

## 11. Output Format: Self-Serve Friction Audit

```markdown
# Self-Serve Friction Audit: [Company/Product Name]

## Journey Map with Friction Scores

| Step | Current Experience | Friction Score (1-5) | Drop-off Rate | Key Friction Points |
|------|-------------------|---------------------|---------------|---------------------|
| Landing -> Signup | [Description] | [Score] | [Rate] | [Points] |
| Signup -> First Action | [Description] | [Score] | [Rate] | [Points] |
| First Action -> Aha Moment | [Description] | [Score] | [Rate] | [Points] |
| Consider -> Purchase | [Description] | [Score] | [Rate] | [Points] |
| Purchase -> Expansion | [Description] | [Score] | [Rate] | [Points] |

## Friction Inventory Summary

### Critical Friction (Must Fix)
1. [Friction point] -- Impact: [High] -- Effort: [Low/Med/High]

### High Friction (Should Fix)
1. [Friction point] -- Impact: [Medium-High] -- Effort: [Low/Med/High]

## Improvement Roadmap

### Phase 1: Quick Wins (Weeks 1-4)
- [ ] [Specific change, expected impact on conversion]

### Phase 2: Core Improvements (Months 2-3)
- [ ] [Specific change, expected impact]

### Phase 3: Strategic Investments (Months 4-6)
- [ ] [Specific change, expected impact]

## Metrics to Track
| Metric | Current | Target (30 days) | Target (90 days) |
|--------|---------|-------------------|-------------------|
| Signup completion rate | [X%] | [Y%] | [Z%] |
| Self-serve conversion rate | [X%] | [Y%] | [Z%] |
| Time-to-purchase | [X days] | [Y days] | [Z days] |
| Checkout completion rate | [X%] | [Y%] | [Z%] |

## "Contact Sales" Gate Review
| Current Gate | Recommendation | Rationale |
|-------------|----------------|-----------|
| [Gate location] | [Remove / Keep / Modify] | [Why] |
```

---

## Cross-References

- `signup-flow-cro` -- Detailed signup flow conversion rate optimization
- `pricing-strategy` -- Pricing page design and plan structure
- `product-onboarding` -- Comprehensive onboarding design beyond self-serve
- `product-led-sales` -- When and how to layer sales assist on self-serve
- `paywall-upgrade-cro` -- Optimizing the free-to-paid upgrade experience
- `usage-based-pricing` -- Designing self-serve usage-based checkout
