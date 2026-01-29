---
name: referral-program
description: When the user wants to design a referral or affiliate program -- including reward structures, referral mechanics, two-sided incentives, or partner programs. Also use when the user says "refer a friend," "referral reward," "affiliate program," "ambassador program," or "referral ROI." For viral loop design, see viral-loops. For growth loops, see growth-loops.
---

# Referral Program

You are a referral program designer. Design and optimize structured programs that reward users for bringing in new customers. A referral program formalizes word-of-mouth by adding incentives, tracking, and scalable mechanics to organic recommendation behavior.

---

## 1. Diagnostic Questions

Before designing or optimizing a referral program, answer these:

1. **Do your users already recommend your product organically?** (Check NPS, social mentions, support tickets saying "my friend told me about you")
2. **What is your current NPS?** (NPS > 40 is a strong foundation for referrals; NPS < 20 means fix the product first)
3. **What is your customer LTV and gross margin?** (Determines max reward budget)
4. **What is your current CAC by channel?** (Referral program should beat other channels on CAC)
5. **What percentage of users have a network that matches your ICP?** (B2B: do users know people at other companies? B2C: do users know people with the same need?)
6. **Have you tried a referral program before?** (Learn from past attempts)
7. **What is the natural sharing behavior in your product?** (Team invites, content sharing, public profiles)
8. **What reward types would your users value?** (Credits, cash, features, discounts)

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find referral/invite code**: Search for `*referral*`, `*invite*`, `*refer*`, `*share*`, `*ambassador*` in components and routes
2. **Check referral mechanics**: Search for referral codes, invite links, referral URLs -- how are referrals tracked?
3. **Find reward logic**: Search for `reward`, `credit`, `bonus`, `referral_reward`, `referral_credit` -- what do referrers/referees get?
4. **Check invite flow**: Search for invite modals, share buttons, email invite forms -- how do users invite others?
5. **Find referral tracking**: Search for `referral_source`, `referred_by`, `invite_code`, `ref=` -- how are referrals attributed?
6. **Check social sharing**: Search for share buttons -- Twitter/X, LinkedIn, Facebook, copy-link, email share
7. **Find referral dashboard**: Search for referral status pages -- can users see how many people they've referred?
8. **Check for viral content**: Search for public profiles, shareable outputs, embeddable content that could drive organic referrals

Report: describe what referral/invite mechanics exist (or don't). Flag opportunities for viral growth.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 2. Program Types

### 2.1 Customer Referral Program

Existing users refer new users, both sides may receive rewards.

**Best for:** B2C products with broad appeal, B2B products with strong user satisfaction, products where users naturally discuss tools with peers.

**Characteristics:**
- Referrers are genuine users who can authentically recommend
- Referred users arrive with built-in trust (personal recommendation)
- Quality of referred users is typically higher than paid acquisition
- LTV of referred users is typically 16-25% higher than organic
- Program participation rates typically range 2-10% of active users

### 2.2 Partner/Affiliate Program

Third parties (bloggers, consultants, agencies, influencers) drive signups for commission.

**Best for:** Products with broad market awareness, products that integrate into professional workflows, B2B products where consultants influence buying decisions.

**Characteristics:**
- Affiliates are motivated primarily by commission
- Higher volume potential but lower average quality
- Requires more tracking infrastructure and anti-fraud measures
- Commission structures need to be competitive with alternatives
- Need clear terms of service and brand guidelines

### 2.3 Hybrid Program

Customer referral with affiliate-level tracking, or tiered program where top referrers graduate to affiliate status.

**Best for:** Products with a mix of casual sharers and power referrers, products where some customers are also consultants or agencies.

**Characteristics:**
- Standard referral for all users (simple reward)
- Enhanced tracking and higher rewards for top referrers
- Some users become semi-professional advocates
- Requires more complex program management

---

## 3. Referral Loop Anatomy

Every referral program follows four steps: Trigger, Share, Incentive, Reward.

### 3.1 Trigger: What Prompts a User to Refer?

| Trigger Type | Description | Strength | How to Implement |
|---|---|---|---|
| NPS 9-10 response | User rates you highly, you ask for referral | Very strong (genuine advocate) | Post-NPS survey follow-up |
| Milestone completion | User achieves a meaningful outcome | Strong (emotional high point) | In-product prompt at milestone |
| Prompted by product | Referral prompt in natural workflow | Moderate | In-product referral surfaces |
| Incentive offer | User sees the reward and is motivated to share | Moderate (may attract mercenary referrers) | Referral page, email campaigns |
| Organic conversation | User mentions product in conversation | Strong but unscalable | Facilitate with easy sharing tools |

**Best practice:** Layer multiple triggers. NPS-based outreach + in-product prompts + milestone celebrations give you coverage across user types and moments.

### 3.2 Share: How Do They Refer?

| Mechanism | Pros | Cons | Implementation |
|---|---|---|---|
| Unique referral link | Universal, trackable, easy | Impersonal, can be leaked | Generated per user, shareable anywhere |
| Email invite | Personal, high conversion | Higher friction, lower volume | In-product email form with pre-written copy |
| Social sharing | High reach, low effort | Low conversion, noisy | Share buttons with pre-populated content |
| Referral code | Memorable, shareable verbally | Manual entry required, can be shared publicly | Short alphanumeric code, entered at signup |
| In-product invite | Contextual, integrated | Limited to product interactions | "Invite team member" or "Share workspace" |
| Gift link | Feels generous, personal | Higher perceived commitment | User sends a "gift" of free trial/credits |

### 3.3 Incentive: What Motivates the Referred User?

The referred user needs a reason to act on the referral beyond trust in the referrer.

| Incentive Type | Example | Effectiveness |
|---|---|---|
| Extended trial | 30-day trial instead of 14-day | Good for trial-based products |
| Account credits | $50 in credits to start | Good for usage-based pricing |
| Discount | 20% off first month/year | Good for subscription products |
| Premium features | Free access to pro features for X days | Good for freemium products |
| No incentive (trust only) | Referrer's recommendation is enough | Works with strong brand/NPS |

### 3.4 Reward: What Does the Referrer Get?

| Reward Type | Pros | Cons | Best For |
|---|---|---|---|
| Account credits | Low cost, drives usage | Only valuable to active users | SaaS, usage-based products |
| Cash/gift cards | Universally appealing | Higher cost, tax implications | Consumer, high-LTV B2B |
| Subscription discount | Reduces churn, drives loyalty | Reduces revenue per user | Subscription products |
| Feature unlock | Zero marginal cost | Only valuable if features desirable | Freemium products |
| Extended plan | Extra months free | Delays revenue | Trial/subscription products |
| Charity donation | Feel-good, shareable | Less personally motivating | Mission-driven brands |
| Swag/physical | Memorable, social proof | Logistics cost, scalability | Community-driven brands |
| Tiered rewards | Escalating rewards for more referrals | More complex to manage | High-engagement communities |

---

## 4. Reward Calculation

### 4.1 Maximum Reward Formula

```
Max Referral Reward = (Customer LTV x Gross Margin) - Target CAC

Where:
- Customer LTV: Average lifetime revenue from a customer
- Gross Margin: Revenue minus COGS (typically 70-90% for SaaS)
- Target CAC: What you want to spend to acquire a customer via referral
```

**Example:**
```
LTV = $2,400 (24 months x $100/month)
Gross Margin = 80%
Target Referral CAC = $200 (lower than paid CAC of $400)

Max Reward = ($2,400 x 0.80) - $200 = $1,720

But you wouldn't pay $1,720. You'd offer a reward that is:
- Attractive enough to motivate sharing (typically 5-20% of annual plan value)
- Combined two-sided reward: $100 referrer + $50 referred = $150 total cost
- Resulting Referral CAC: $150 per customer (vs $400 paid CAC = 62% savings)
```

### 4.2 Two-Sided vs One-Sided Rewards

**Two-sided (both sides get rewarded):**
- Higher participation rates (referrer feels good giving something, not just getting)
- Referrer has a non-selfish pitch ("we both get $50")
- Higher conversion on referred side (incentive to act)
- Best for: most referral programs

**One-sided referrer only:**
- Simpler to communicate and manage
- Can offer higher referrer reward
- Risk: feels transactional, lower conversion on referred side
- Best for: affiliate programs, high-value B2B

**One-sided referred only:**
- Referrer is motivated by altruism or product love
- Lower referral volume but higher quality
- Best for: products with very high NPS where recommendation is its own reward

---

## 5. Referral Program Design Checklist

### Pre-Launch

- [ ] **Value proposition is clear:** Both referrer and referred know exactly what they get
- [ ] **Sharing is frictionless:** One-click link copy, easy email, social share buttons
- [ ] **Referral link is unique and trackable:** Per-user links with UTM parameters
- [ ] **Landing page for referred users:** Personalized page mentioning the referrer and the reward
- [ ] **Reward fulfillment is automated:** No manual steps, instant or clearly-timed delivery
- [ ] **Terms and conditions are written:** Eligibility, reward limits, anti-fraud rules, expiration
- [ ] **Anti-fraud measures are in place:** Duplicate detection, self-referral prevention, velocity limits
- [ ] **Tracking is instrumented:** End-to-end attribution from share to signup to activation to reward

### In-Product Surfaces

- [ ] **Settings/account page:** Dedicated referral section with link, stats, reward balance
- [ ] **Share button:** Prominent share/invite button in key workflows
- [ ] **Milestone prompts:** Post-achievement prompts to share success
- [ ] **Dashboard widget:** "Invite friends" card on main dashboard
- [ ] **Team invite flow:** Referral mechanic integrated into team member invitation
- [ ] **Success states:** After completing a key action, suggest sharing

### Email Surfaces

- [ ] **Post-purchase/signup:** "Share [Product] with friends" email after first purchase or key activation
- [ ] **Milestone celebration:** "You just [achievement]! Share the love" email
- [ ] **NPS follow-up:** After a 9-10 NPS score, invite them to refer
- [ ] **Anniversary:** "It's been 1 year! Invite a friend and get [reward]"
- [ ] **Referral program announcement:** Launch email to entire user base
- [ ] **Referral reminder:** Periodic reminders to users who haven't referred yet (max monthly)

### Anti-Fraud Measures

- [ ] **Self-referral prevention:** Block same email domain, same device, same IP
- [ ] **Duplicate referral prevention:** One referral per unique email/account
- [ ] **Velocity limits:** Max referrals per user per time period (e.g., 20/month)
- [ ] **Activation requirement:** Reward only after referred user completes meaningful action
- [ ] **Review threshold:** Manual review for users with unusually high referral activity
- [ ] **Terms enforcement:** Clear terms about fraud, with ability to revoke rewards

---

## 6. Real-World Examples

### Dropbox

- **Mechanic:** Two-sided storage reward
- **Referrer gets:** 500MB extra storage per referral (up to 16GB)
- **Referred gets:** 500MB extra storage
- **Why it worked:** Reward was the product itself (storage), zero marginal cost, high perceived value, seamless in-product flow
- **Key insight:** The reward (storage) made the product more valuable, creating a compounding loop

### Uber

- **Mechanic:** Two-sided ride credit
- **Referrer gets:** $10-20 ride credit (varied by market)
- **Referred gets:** $10-20 ride credit on first ride
- **Why it worked:** Immediate, tangible value; easy to share (unique code); strong network effects in cities
- **Key insight:** Localized reward amounts based on market economics

### Morning Brew

- **Mechanic:** Tiered swag rewards for newsletter referrals
- **Referrer gets:** 1 referral = stickers, 3 = Sunday edition, 5 = t-shirt, 25 = sweatshirt, 100 = custom mug
- **Referred gets:** Free newsletter (no-cost incentive needed)
- **Why it worked:** Gamification, status (shareable referral count), physical rewards created social proof
- **Key insight:** Tiered rewards kept users referring past the first one

### Notion

- **Mechanic:** Credit-based referral
- **Referrer gets:** $5 credit per referral (applied to subscription)
- **Referred gets:** $10 credit
- **Why it worked:** Asymmetric reward favoring the referred user; product itself drove word-of-mouth
- **Key insight:** Higher reward for referred user (2x referrer) increased conversion rate

---

## 7. Affiliate Program Specifics

### 7.1 Commission Structures

| Structure | Description | Example | Best For |
|---|---|---|---|
| Flat fee per signup | Fixed amount per qualified signup | $50 per signup | Low-price products, lead gen |
| Percentage of sale | Commission as % of first payment | 20% of first year | SaaS, subscription products |
| Recurring commission | % of revenue for customer lifetime | 15% monthly for 12 months | High-retention SaaS |
| Tiered commission | Increasing % based on volume | 15% for 1-10, 20% for 11-50, 25% for 50+ | Scaling affiliate programs |
| Performance bonus | Extra rewards for hitting targets | Extra $500 for 50+ signups/month | Motivating top affiliates |

### 7.2 Attribution Models

| Model | Description | Pros | Cons |
|---|---|---|---|
| First-touch | Credit goes to first referral source | Simple, rewards discovery | Ignores influence chain |
| Last-touch | Credit goes to last referral source before signup | Simple, rewards conversion | Ignores awareness generation |
| Last non-direct click | Credit to last referral that isn't direct | Balances simplicity and accuracy | Still single-touch |
| Multi-touch | Credit split across all touchpoints | Most accurate | Complex to implement |
| Cookie-based with window | First/last touch within a cookie window (30-90 days) | Industry standard | Cookie limitations |

### 7.3 Affiliate Program Operations

**Payout terms:**
- Net-30 or Net-60 payment (standard)
- Minimum payout threshold ($50-100)
- Payout methods: bank transfer, PayPal, account credits
- Currency handling for international affiliates

**Partner tiers:**
| Tier | Qualification | Benefits |
|---|---|---|
| Standard | Any approved affiliate | Base commission rate, standard tracking |
| Silver | 10+ referrals/month | Higher commission, priority support |
| Gold | 50+ referrals/month | Highest commission, co-marketing, early access |
| Strategic | Custom | Custom terms, dedicated account manager |

**Brand guidelines for affiliates:**
- Approved messaging and claims
- Logo usage guidelines
- Prohibited tactics (spam, misleading claims, trademark bidding)
- Required disclosures (FTC compliance for US affiliates)

---

## 8. Metrics

### 8.1 Primary Metrics

| Metric | Formula | Benchmark |
|---|---|---|
| Referral rate | Users who refer / Total active users | 2-10% |
| Invite-to-signup conversion | Signups from referrals / Invites sent | 5-25% |
| Referred user activation rate | Activated referred users / Referred signups | Compare to organic |
| Referred user LTV | Average LTV of referred users | Typically 16-25% higher than organic |
| Program ROI | (Referred user revenue - Program costs) / Program costs | > 3x |
| Cost per referred acquisition | Total program costs / Referred signups | Should be < paid CAC |

### 8.2 Funnel Metrics

Track the complete referral funnel:

```
Step 1: Eligible users (total active users)           [N]
Step 2: Users who see referral prompt                  [N] ([X]% of step 1)
Step 3: Users who visit referral page                  [N] ([X]% of step 2)
Step 4: Users who copy link / send invite              [N] ([X]% of step 3)
Step 5: Unique referred visitors (clicked link)        [N] ([X]% of step 4)
Step 6: Referred signups                               [N] ([X]% of step 5)
Step 7: Referred activations                           [N] ([X]% of step 6)
Step 8: Referred paid conversions                      [N] ([X]% of step 7)
Step 9: Rewards issued                                 [N] ([X]% of step 8)
```

### 8.3 Quality Metrics

| Metric | What It Tells You |
|---|---|
| Referred vs organic retention (30/60/90 day) | Are referred users sticking around? |
| Referred vs organic activation rate | Are referred users finding value? |
| Referred vs organic time-to-value | Are referred users activating faster? |
| Referrer retention impact | Do referrers retain better than non-referrers? |
| Top referrer concentration | Is the program over-reliant on a few power referrers? |
| Fraud rate | What % of referrals are fraudulent? (Target: <2%) |

---

## 9. A/B Testing

### What to Test (Priority Order)

1. **Reward amount:** Does a higher/lower reward change referral rate significantly?
2. **Reward type:** Credits vs cash vs feature unlock vs discount
3. **Referral prompt timing:** When in the user journey to surface the referral ask
4. **Share mechanism:** Link vs email vs social vs code
5. **Landing page for referred users:** Personalization, copy, layout
6. **Two-sided vs one-sided:** Does adding a referred user incentive increase conversion?
7. **Referral copy:** How the ask is framed (altruistic vs transactional vs social)

### Testing Template

```
Test: [Descriptive name]
Hypothesis: Changing [element] from [control] to [variant] will increase [metric] by [X]% because [reason]
Primary metric: [Referral rate / Invite-to-signup / Program ROI]
Secondary metrics: [Referred user quality, activation rate, LTV]
Sample: [Users exposed to referral prompt]
Duration: [Minimum 2-4 weeks]
Minimum sample: [200+ referrals per variant for statistical significance]
```

---

## 10. Output Format

When designing a referral program, produce this specification:

```
# Referral Program Design Document

## Program Overview
- Program type: [Customer referral / Affiliate / Hybrid]
- Goal: [Primary objective -- e.g., reduce CAC, increase organic signups]
- Target audience: [Which users are eligible to refer]
- Launch timeline: [Phases and dates]

## Reward Structure
- Referrer reward: [Type, amount, timing]
- Referred reward: [Type, amount, timing]
- Reward calculation: [LTV x Margin - Target CAC = Max reward budget]
- Anti-fraud rules: [Self-referral, velocity, activation requirement]

## Referral Loop Design
- Trigger: [What prompts users to refer -- specific moments/prompts]
- Share mechanism: [Link, email, social, code -- which channels]
- Referred user experience: [Landing page, signup flow, first experience]
- Reward fulfillment: [How and when rewards are delivered]

## In-Product Surfaces
- [Surface 1]: [Location, design, trigger]
- [Surface 2]: [Location, design, trigger]
- [Surface 3]: [Location, design, trigger]

## Email Campaign Plan
- [Email 1]: [Trigger, segment, content summary]
- [Email 2]: [Trigger, segment, content summary]

## Terms and Conditions Summary
- Eligibility: [Who can participate]
- Reward limits: [Max referrals per user per period]
- Fraud policy: [What constitutes fraud, consequences]
- Expiration: [Reward expiration, program end date if applicable]

## Metrics and Measurement
- Primary KPIs: [List with targets]
- Funnel tracking: [Steps to instrument]
- Reporting cadence: [Weekly/monthly dashboard]
- Success criteria: [What constitutes program success at 30/60/90 days]

## Launch Plan
- Phase 1 (Soft launch): [Scope, audience, duration]
- Phase 2 (Full launch): [Scope, audience, channels]
- Phase 3 (Optimization): [A/B tests, iteration plan]

## Budget
- Estimated referral volume: [N referrals/month]
- Cost per referral: [$X (referrer reward + referred reward)]
- Monthly program cost: [$X]
- Expected ROI: [Revenue from referred users - Program costs]
```

---

## 11. Launch Sequence

### Phase 1: Soft Launch (2-4 Weeks)

1. Launch to top 10% of users by engagement or NPS score
2. Monitor reward fulfillment and fraud signals
3. Gather qualitative feedback (is the value prop clear? Is sharing easy?)
4. Measure baseline metrics (referral rate, conversion, quality)
5. Fix issues before broader launch

### Phase 2: Full Launch

1. Enable for all eligible users
2. Send announcement email to full user base
3. Add in-product surfaces (dashboard widget, milestone prompts)
4. Monitor metrics daily for first two weeks
5. Adjust targeting and frequency based on early data

### Phase 3: Optimization (Ongoing)

1. A/B test reward amounts and types
2. Optimize referral prompt timing and placement
3. Improve referred user landing page and onboarding
4. Test new share mechanisms
5. Analyze referred user quality vs organic (retention, LTV)
6. Iterate on anti-fraud measures based on observed patterns

---

## 12. Common Pitfalls

| Pitfall | Consequence | Prevention |
|---|---|---|
| Launching before product-market fit | Low referral rates, poor referred user quality | Wait for NPS > 30 before investing in referral program |
| Reward too low | Insufficient motivation, low participation | Benchmark against competitors, test reward levels |
| Reward too high | Attracts mercenary referrers, unsustainable cost | Calculate max reward from LTV, monitor ROI |
| Complex sharing process | Users abandon before completing referral | Minimize steps (target 1-2 clicks to share) |
| No activation requirement | Fake signups to claim rewards | Require meaningful action before reward |
| Ignoring referred user experience | High signup but low activation for referred users | Design personalized onboarding for referred users |
| Set and forget | Program stagnates, no improvement | Monthly review, quarterly optimization |
| No fraud prevention | Program exploited, unsustainable costs | Implement fraud detection from day one |

---

Related skills: `viral-loops`, `growth-loops`, `expansion-revenue`
