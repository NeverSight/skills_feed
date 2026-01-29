---
name: trial-optimization
description: When the user wants to optimize free trial conversion -- including trial length, trial type selection, expiry flows, or trial email sequences. Also use when the user says "trial conversion," "trial length," "trial design," "opt-in vs opt-out trial," or "trial-to-paid." For activation, see activation-metrics. For feature gating, see feature-gating.
---

# Trial Optimization

You are a trial optimization specialist. A comprehensive framework for designing, measuring, and optimizing free trials to maximize conversion to paid. The trial is the highest-leverage moment in the PLG funnel -- it is where product value and purchase intent intersect.

---

## 1. Trial Types Comparison

### 1.1 Opt-In Trial (No Card Required)

| Attribute | Detail |
|-----------|--------|
| Signup friction | Very low |
| Signup volume | High |
| Conversion rate | 3-8% typical |
| Lead quality | Mixed (many tire-kickers) |
| Best for | Broad market, low ACV (<$50/mo), strong PLG motion |
| Risk | Many signups never engage; harder to follow up |

**Examples:** Slack, Notion, Asana, Figma

### 1.2 Opt-Out Trial (Card Required)

| Attribute | Detail |
|-----------|--------|
| Signup friction | Higher (30-50% fewer signups than no-card) |
| Signup volume | Lower |
| Conversion rate | 40-60% typical |
| Lead quality | Higher intent |
| Best for | Focused market, higher ACV (>$50/mo), clear value proposition |
| Risk | Users forget to cancel (chargebacks, bad sentiment); regulatory scrutiny |

**Examples:** Netflix, Spotify, most subscription services

### 1.3 Reverse Trial

| Attribute | Detail |
|-----------|--------|
| Signup friction | Low |
| Signup volume | High |
| Conversion rate | 5-15% to paid (but many stay on free tier) |
| Lead quality | Mixed, but builds long-term pipeline |
| Best for | Products with strong free tier, obvious premium value |
| Risk | Users upset by downgrade; free tier must be viable |

**Examples:** Notion, Airtable

### 1.4 Freemium + Trial Hybrid

| Attribute | Detail |
|-----------|--------|
| Signup friction | None for free tier; low for trial opt-in |
| Signup volume | High |
| Conversion rate | Varies by when users start the trial |
| Lead quality | Higher (users have already experienced free product) |
| Best for | Mature PLG products with clear tier differentiation |
| Risk | Timing the trial offer; user confusion about tiers |

**Examples:** Dropbox, Canva

### Trial Type Decision Framework

```
Do you have a viable, long-term free tier?
├── YES
│   ├── Is premium value obvious without extended use?
│   │   ├── YES → Freemium + opt-in trial of premium features
│   │   └── NO → Reverse trial (full product → downgrade to free)
│   └── Are you focused on broad adoption?
│       ├── YES → Reverse trial
│       └── NO → Freemium + trial
└── NO
    ├── Is your ACV > $50/month?
    │   ├── YES → Opt-out trial (card required)
    │   └── NO → Opt-in trial (no card)
    └── Can users reach the aha moment quickly (<3 days)?
        ├── YES → Opt-out trial (shorter is fine)
        └── NO → Opt-in trial (longer, lower friction)
```

---

## 2. Trial Length Optimization

The trial should last long enough for users to complete onboarding, experience the aha moment, build switching costs, and (for B2B) involve stakeholders.

### Measuring Ideal Trial Length

1. **Analyze activation data:** What is the median time for successful converters to reach the aha moment?
2. **Add buffer:** Multiply by 1.5-2x to account for slower users, weekends, and holidays.
3. **Check engagement drop-off:** At what point do trial users stop engaging? The trial should not extend much beyond this.
4. **Consider the buying process:** For enterprise, procurement and legal may need additional time.

### Trial Length by Product Type

| Trial Length | Best For | Characteristics |
|-------------|---------|----------------|
| **7 days** | Simple products, individual users | Fast time-to-value (hours, not days). Productivity apps, simple tools. Creates urgency. |
| **14 days** | Standard B2B SaaS | Most common. Enough time to explore and involve teammates. Good balance of urgency and exploration. |
| **30 days** | Complex products, team deployment | Products requiring setup, data import, team onboarding. Enterprise tools, data platforms. |
| **Custom** | Variable complexity | Consider adaptive trial length based on user behavior (extend for engaged users, shorten for inactive). |

### Common Mistake: Trial Too Long

Longer trials do not always mean better conversion. A 30-day trial for a simple product reduces urgency, extends the sales cycle, and results in users forgetting about the product. Start with a shorter trial and extend only if data shows users need more time.

---

## 3. Trial Experience Design

### Day 1: First Impressions (make or break for conversion)

1. **Immediate value delivery** -- The user should accomplish something meaningful within 30 minutes
2. **Setup completion** -- Account configuration, integrations, data import
3. **Aha moment introduction** -- Guide the user to the core feature that demonstrates premium value
4. **Social proof** -- Show that others like them are successfully using the product
5. **Clear timeline** -- Communicate trial length and what happens at expiry

**Day 1 Checklist:**
- [ ] Welcome email sent within 5 minutes of signup
- [ ] In-product onboarding flow launched
- [ ] Key integration connected or sample data provided
- [ ] Core feature used at least once
- [ ] Trial duration and terms communicated clearly

### Mid-Trial: Building Commitment

1. **Explored key features** -- At least 3-5 premium features used
2. **Built data or content** -- Created enough that switching away feels costly
3. **Involved others** -- Invited teammates, shared output, collaborated
4. **Established a workflow** -- Product is part of their routine

**Mid-Trial Checkpoint:**
- [ ] User has returned to the product at least 3 times
- [ ] Multiple premium features explored
- [ ] Data/content created in the product
- [ ] Usage trend is stable or increasing
- [ ] If team product: at least 1 teammate invited

### Pre-Expiry: Creating Conversion Pressure

1. **Urgency messaging** -- Clear communication that trial is ending
2. **Value summary** -- Show what the user has accomplished and what they would lose
3. **Friction removal** -- One-click upgrade with pre-filled billing information
4. **Objection handling** -- Address common concerns (cost, commitment, alternative plans)
5. **Extension option** -- For engaged users who need more time

**Pre-Expiry Tactics:**
- In-product banner: "Your trial ends in 3 days. Upgrade to keep your [specific thing they built]."
- Email with usage summary: "During your trial, you created X projects, collaborated with Y people, and saved Z hours."
- Offer annual billing discount: "Save 20% by choosing annual billing."
- Address the #1 objection proactively (usually price or feature fit)

---

## 4. Trial Email Sequence

### Complete Email Sequence Template

| Day | Email | Subject Line | Purpose | Key Content |
|-----|-------|-------------|---------|-------------|
| 0 | Welcome | Welcome to [Product] -- here's how to get started | Orient and activate | Quick-start guide, key first action, trial duration, support link |
| 1 | Quick win | Get your first [outcome] in 5 minutes | Drive first value | Step-by-step guide to one specific use case |
| 3 | Key feature | Have you tried [premium feature]? | Feature discovery | Highlight a premium feature they have not used yet |
| 7 (mid-trial for 14-day) | Check-in | How is [Product] working for you? | Engagement + support | Ask if they need help, offer a demo/call, share tips |
| N-3 | Expiry warning | Your [Product] trial ends in 3 days | Create urgency | Usage summary, what they will lose, upgrade CTA |
| N-1 | Last chance | Tomorrow is your last day on [Product] Pro | Final urgency | Final upgrade CTA, payment link, extension option |
| N | Expired | Your [Product] trial has ended | Convert or retain | Two paths: upgrade now, or continue on free tier |
| N+3 | Win-back | We miss you -- here's 20% off [Product] Pro | Re-engage | Special offer, limited time, reminder of value |
| N+7 | Final win-back | Last chance: your [Product] data is waiting | Final attempt | Urgency about data/content, final discount offer |

### Email Best Practices

1. **Personalize with product usage data.** "You created 12 projects during your trial" is more compelling than generic copy.
2. **One CTA per email.** Do not overwhelm with options.
3. **Segment by engagement.** Highly active trial users get different emails than inactive ones.
4. **Use plain text for some emails.** Personal-feeling emails from a real person convert better than marketing emails for mid-trial check-ins.
5. **Track opens, clicks, and conversions** for each email. Optimize the sequence over time.

### Engagement-Based Email Branching

```
Day 3: Check user engagement level

High engagement (daily active, multiple features used):
  → Send "power user tips" email
  → Introduce team/collaboration features
  → Mention upcoming premium features

Medium engagement (used 2-3 times, limited features):
  → Send "quick win" email with guided tutorial
  → Offer a 15-minute onboarding call
  → Highlight the single most valuable feature for their use case

Low engagement (signed up but barely used):
  → Send "need help getting started?" email
  → Offer one-click setup or sample data
  → Share customer success story relevant to their use case
  → If no engagement by day 5: direct outreach from a person
```

---

## 5. Trial Extensions

### When to Offer Extensions

Offer a trial extension when:
- User is actively engaged but has not reached the aha moment yet
- User's team is evaluating the product (enterprise context)
- User explicitly requests more time
- User engaged early but went inactive mid-trial (re-engagement opportunity)

Do NOT offer extensions when:
- User has never logged in (no engagement = extension will not help)
- User is clearly not the right fit (wrong use case, wrong market)
- User is gaming extensions to avoid paying

### Extension Framework

| Scenario | Extension Length | Condition |
|----------|----------------|-----------|
| Active user, needs more time | 7 days | Must have completed onboarding |
| Team evaluation in progress | 14 days | Must have 2+ team members active |
| Re-engagement opportunity | 7 days | Was active early, went inactive |
| Enterprise procurement process | 30 days | Must have scheduled a demo/call |

### Automatic vs Manual Extensions

**Automatic:** Trigger based on behavior rules (e.g., "active in last 3 days + not upgraded = extend 7 days"). Lower touch, scalable. **Manual:** Sales/CS reviews and selectively offers. Higher touch, more targeted. **Recommendation:** Use automatic for self-serve users, manual for users who have engaged with sales.

---

## 6. Trial-to-Paid Conversion Optimization

### Removing Friction in the Upgrade Flow

1. **Pre-fill billing information** where possible (company name, email)
2. **One-click upgrade** from any in-product gate or notification
3. **Show clear pricing** in the upgrade flow (no surprises)
4. **Offer multiple payment methods** (card, invoice, PayPal)
5. **Provide plan comparison** in the upgrade modal
6. **Allow mid-trial upgrade** (do not force users to wait until expiry)
7. **Prorate charges** if upgrading mid-billing cycle

### Addressing Common Objections

| Objection | Response Strategy |
|-----------|------------------|
| "Too expensive" | Show ROI calculation, offer annual discount, suggest starter plan |
| "Not sure I need it" | Show usage data ("You used X feature 47 times this week") |
| "Need to get approval" | Provide ROI justification template, offer to join a call with their manager |
| "Want to try alternatives" | Share competitive comparison, offer extension |
| "Not the right time" | Offer to pause and resume later, downgrade to free tier |
| "Missing a feature" | Log the request, show roadmap if applicable, offer workaround |

### Incentives for Conversion

Use sparingly -- incentives can devalue your product if overused:

- **First-month discount** (20-30% off first month)
- **Extended annual discount** (save 25% instead of the usual 17%)
- **Bonus feature or capacity** (extra storage, seats, credits for first 3 months)
- **Onboarding session** (free setup call with upgrade)
- **Money-back guarantee** (30-day refund if not satisfied)

---

## 7. In-Trial Engagement Tracking

### Key Metrics to Track During Trial

| Metric | What It Indicates | Action if Low |
|--------|-------------------|---------------|
| **Day 1 activation rate** | Is onboarding working? | Redesign first-run experience |
| **Daily/weekly active usage** | Is the product sticky? | Send engagement emails, offer help |
| **Feature breadth** | Are users exploring premium features? | Send feature discovery prompts |
| **Collaboration signals** | Is the user involving their team? | Prompt team invitations |
| **Data/content creation** | Is the user investing in the product? | Help with data import, templates |
| **Return visits** | Is the user building a habit? | Improve notification and reminder system |
| **Time in product** | How engaged are sessions? | Improve UX, reduce friction |
| **Support interactions** | Is the user seeking help? | Ensure fast response during trial |

### Building a Trial Health Score

Create a composite score (0-100) combining:

```
Trial Health Score = weighted sum of:
  - Activation completed (0 or 1) x 25
  - Days active / trial length x 20
  - Features explored / key features x 20
  - Team members invited (0 or 1+) x 15
  - Data/content created (0 or 1+) x 10
  - Recency (days since last login) x 10

Segments:
  - 80-100: Hot lead (likely to convert, nurture carefully)
  - 50-79: Warm lead (needs guidance, offer help)
  - 20-49: Cool lead (at risk, intervention needed)
  - 0-19: Cold lead (likely lost, low-touch win-back)
```

---

## 8. Trial Segmentation

### Different Trials for Different Users

Not all trial users are the same. Consider segmenting by:

| Segment | Trial Variation | Rationale |
|---------|----------------|-----------|
| **Individual vs Team** | Individuals: shorter trial, simpler onboarding. Teams: longer trial, team setup guidance | Teams need time to deploy |
| **Role** | Customize onboarding and feature highlights by role (marketer vs developer vs designer) | Different aha moments |
| **Company size** | SMB: self-serve trial. Enterprise: trial + sales touch | Enterprise buying process is different |
| **Use case** | Customize sample data, templates, and guides by use case | Faster time-to-value |
| **Source** | Users from paid ads: more aggressive conversion. Organic: more nurturing | Different intent levels |
| **Engagement level** | Active users: premium feature nudges. Inactive: re-engagement campaigns | Meet users where they are |

### Implementation

1. Capture segmentation signals at signup (role, company size, use case -- but keep the form short)
2. Use progressive profiling to gather more data during the trial
3. Route users into segment-specific onboarding flows
4. Customize email sequences and in-product messaging per segment
5. Track conversion rates per segment to identify which segments convert best

---

## 9. Conversion Benchmarks

### Industry Benchmarks

| Trial Type | Conversion Rate | Notes |
|-----------|----------------|-------|
| Opt-in (no card) | 3-8% | Higher for products with strong aha moment |
| Opt-out (card required) | 40-60% | Includes users who forget to cancel |
| Reverse trial | 5-15% to paid | Many stay on free tier (total retained: 60-80%) |
| Freemium + trial | Varies | Depends on when trial is offered |

### Factors That Increase Conversion

- Strong Day 1 experience with clear first win
- Personalized onboarding based on use case
- Team adoption during trial (2+ users = 3x more likely to convert)
- Data import or content creation (switching cost)
- Multiple feature discovery (3+ features = 2x more likely)
- Engagement with support or sales during trial

### Factors That Decrease Conversion

- Slow or broken onboarding
- No clear aha moment reached
- Solo usage without team involvement
- Competing alternatives evaluated simultaneously
- Price shock at conversion (pricing not visible during trial)
- Complex checkout or billing process

---

## 10. A/B Test Ideas for Trials

### High-Impact Tests

| Test | Hypothesis | Metric |
|------|-----------|--------|
| Trial length (7 vs 14 days) | Shorter trial creates urgency | Conversion rate, time-to-upgrade |
| Card required vs not | Card required improves lead quality | Conversion rate, signup volume, revenue |
| Onboarding flow (guided vs self-serve) | Guided onboarding improves activation | Day 1 activation, feature adoption, conversion |
| Expiry email copy (urgency vs value) | Value-focused copy converts better | Email CTR, conversion rate |
| Extension offer (yes vs no) | Extensions increase total conversions | Conversion rate, delayed conversion rate |
| Upgrade CTA placement (in-app vs email) | In-app CTAs convert better | Upgrade click rate, conversion rate |
| Trial start (immediate vs delayed) | Delaying premium features until aha moment | Conversion rate, engagement |
| Pricing visibility (shown vs hidden during trial) | Showing price early sets expectations | Conversion rate, upgrade flow drop-off |

### How to Prioritize Tests

Use ICE scoring:
- **Impact:** How much will this move the conversion rate? (1-10)
- **Confidence:** How confident are you in the hypothesis? (1-10)
- **Ease:** How easy is this to implement? (1-10)

Score = (Impact + Confidence + Ease) / 3. Run highest-scoring tests first.

---

## 11. Diagnostic Questions

When helping a user with trial optimization, ask:

1. What type of trial do you currently offer? (Opt-in, opt-out, reverse, hybrid)
2. What is your current trial length and conversion rate?
3. How long does it take users to reach the aha moment?
4. What does your trial onboarding flow look like?
5. Do you have a trial email sequence? How many emails, what cadence?
6. Do you track engagement during the trial? What metrics?
7. Do you offer trial extensions? Under what conditions?
8. Do you segment trial users? How?
9. What is your upgrade flow like? (Steps, friction points)
10. Do you have a free tier that users fall back to after trial expiry?
11. What are the top reasons users give for not converting?
12. What A/B tests have you run on the trial?

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find trial logic**: Search for `trial`, `trial_start`, `trial_end`, `trial_days`, `trialExpires`, `isTrial` in models and business logic
2. **Check trial type**: Is it opt-in (no card) or opt-out (card required)? Search for payment collection during signup
3. **Find trial duration**: Search for trial length constants -- `14`, `30`, `TRIAL_DAYS`, `trial_period`
4. **Find expiry handling**: Search for trial expiry logic -- what happens when the trial ends? Search for `expired`, `trial_ended`, `downgrade`
5. **Check trial emails**: Search for email templates related to trials -- `trial-welcome`, `trial-reminder`, `trial-expiring`, `trial-expired`
6. **Find trial extension logic**: Search for `extend`, `trial_extension`, `extra_days` -- can trials be extended?
7. **Check conversion flow**: What happens at trial end? Search for the upgrade/payment flow triggered by expiry
8. **Find trial analytics**: Search for tracking events on trial starts, activations, conversions, expirations

Report: describe the current trial implementation -- type, length, expiry behavior, email sequence, and conversion flow.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 12. Output Format

When completing a trial optimization engagement, deliver:

```markdown
# Trial Optimization Strategy: [Product Name]

## Trial Model
- Type: [Opt-in / Opt-out / Reverse / Hybrid]
- Length: [N days]
- Rationale: [Why this model and length]

## Trial Experience Design

### Day 1 Experience
- [ ] [Specific action 1]
- [ ] [Specific action 2]
- [ ] [Specific action 3]

### Mid-Trial Milestone (Day [N/2])
- [ ] [What should have happened by midpoint]

### Pre-Expiry (Day [N-3] to Day [N])
- [ ] [Urgency and conversion tactics]

## Email Sequence

| Day | Email Type | Subject Line | Key Content |
|-----|-----------|-------------|-------------|
| 0 | Welcome | [Subject] | [Content summary] |
| 1 | Quick win | [Subject] | [Content summary] |
| ... | ... | ... | ... |

## Engagement Tracking
- Key metrics: [list]
- Health score model: [components and weights]
- Intervention triggers: [when to take action]

## Conversion Optimization
- Upgrade flow: [steps and optimizations]
- Objection handling: [top 3 objections and responses]
- Incentives: [if applicable]

## Segmentation
- Segments: [list]
- Per-segment variations: [differences in experience]

## A/B Test Roadmap
1. [Test 1]: [Hypothesis, metric, priority]
2. [Test 2]: [Hypothesis, metric, priority]
3. [Test 3]: [Hypothesis, metric, priority]

## Success Metrics
- Current conversion rate: [X%]
- Target conversion rate: [Y%]
- Timeline: [when to evaluate]
```

---

## 13. Related Skills

- `activation-metrics` -- Measuring and optimizing the aha moment that trials depend on
- `feature-gating` -- Deciding what to include in the trial vs gate behind payment
- `pricing-strategy` -- Overall pricing framework that the trial supports
- `product-onboarding` -- First-run experience design that drives trial activation
