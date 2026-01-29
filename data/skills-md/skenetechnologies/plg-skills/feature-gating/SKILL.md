---
name: feature-gating
description: When the user wants to decide what features to gate vs keep free, design usage limits, implement reverse trials, or plan a free tier. Also use when the user says "what should be free," "feature gate," "paywall placement," "usage limits," or "reverse trial." For pricing strategy, see pricing-strategy. For upgrade screens, see paywall-upgrade-cro.
---

# Feature Gating

You are a feature gating strategist. A decision framework for determining what to include in your free tier, what to gate behind paid plans, and how to design gates that drive conversion without destroying the free user experience.

---

## 1. Core Principle

Your free tier must accomplish two goals simultaneously:

1. **Deliver enough value to drive adoption** -- Users must be able to do real, meaningful work. If the free tier feels like a demo, users will leave.
2. **Create desire for more** -- Users must encounter natural moments where they want features, capacity, or capabilities that require an upgrade.

The tension between these goals is the art of feature gating. Gate too aggressively and you kill adoption. Gate too loosely and you kill conversion.

### The "Feel Free" Test

Ask yourself: "Would I use this free product if no paid plan existed?" If the answer is no, your free tier is too restrictive. A free tier should feel like a real product, not a marketing funnel with a login page.

---

## 2. Feature Gating Decision Tree

For every feature in your product, walk through this decision tree:

```
1. Does this feature drive activation (help users reach the aha moment)?
   ├── YES → KEEP FREE -- Gating activation features kills growth.
   └── NO → Continue

2. Does this feature drive viral or collaborative behavior?
   ├── YES → KEEP FREE -- These features bring in new users.
   │         (Examples: sharing, inviting teammates, public profiles,
   │          commenting, @mentions)
   └── NO → Continue

3. Is this feature a key differentiator vs competitors' free tiers?
   ├── YES → STRONGLY CONSIDER KEEPING FREE -- This is your moat.
   │         Gating it removes your competitive advantage in acquisition.
   └── NO or N/A → Continue

4. Does this feature serve primarily advanced/power users?
   ├── YES → GATE -- Power users have demonstrated willingness to pay.
   │         (Examples: advanced analytics, automation, custom workflows,
   │          API access, bulk operations)
   └── NO → Continue

5. Does this feature serve team or organizational needs?
   ├── YES → GATE -- Team features naturally map to paid tiers.
   │         (Examples: admin controls, role permissions, SSO, audit logs,
   │          team workspaces, shared billing)
   └── NO → Continue

6. Does this feature require significant compute, storage, or cost?
   ├── YES → GATE or USAGE-LIMIT -- Protect your unit economics.
   │         (Examples: AI features, video processing, large storage,
   │          high-volume API calls)
   └── NO → Continue

7. Is the feature a "nice to have" enhancement?
   ├── YES → GATE -- Good candidate for paid tier differentiation.
   │         (Examples: custom themes, priority support, advanced exports,
   │          white-labeling)
   └── NO → Default to FREE and re-evaluate based on data.
```

---

## 3. Gate Types

Not all gates are created equal. Choose the gate type that matches the feature and the user experience you want to create.

### 3.1 Hard Gate

**Definition:** Feature is completely unavailable to free users. No preview, no indication it exists.

**When to use:**
- Features that require a completely different infrastructure path
- Enterprise-only features (SSO, SAML, compliance)
- Features where even a glimpse adds no value

**Risk:** Users may never discover the feature exists, reducing upgrade motivation.

**Example:** Salesforce hides many enterprise features entirely from lower-tier users.

### 3.2 Soft Gate

**Definition:** Feature is visible but locked. User can see it exists, often with an upgrade prompt, lock icon, or preview.

**When to use:**
- Features where awareness drives upgrade desire
- Features that are easy to understand from a preview
- Any feature you want to use as an upgrade trigger

**Best practices:**
- Show the feature in the UI with a clear visual indicator (lock icon, "Pro" badge)
- When clicked, show a contextual upgrade prompt explaining the value
- Include a preview or screenshot of what the feature does
- Make the upgrade CTA specific: "Upgrade to Pro to unlock advanced analytics"

**Example:** Notion shows database views with a lock icon and "Upgrade to unlock" prompt.

### 3.3 Usage Gate

**Definition:** Feature is available but with limited quantity. Users can experience the full feature but hit a ceiling.

**When to use:**
- Core features that users need to try before buying
- Features with natural quantity dimensions (projects, records, storage)
- When you want users to build commitment before hitting the gate

**Best practices:**
- Set limits that allow meaningful usage but create natural upgrade moments
- Show usage progress: "3 of 5 projects used"
- Send notifications as users approach limits: "You have used 80% of your free projects"
- Make it easy to upgrade at the moment of need (inline upgrade CTA)

**Examples of usage limits by product type:**

| Product Type | Free Limit | Paid Limit |
|-------------|-----------|-----------|
| Project management | 3-5 projects | Unlimited |
| CRM | 250-1,000 contacts | Unlimited or tiered |
| Storage | 5-15 GB | 100 GB - Unlimited |
| Email marketing | 500-2,000 contacts | Tiered by volume |
| Design tool | 3 projects, limited exports | Unlimited |
| Analytics | 1,000-10,000 events/month | Tiered by volume |
| AI product | 50-100 generations/month | Tiered or usage-based |
| API | 100-1,000 calls/month | Tiered by volume |

**Setting the right limit:** The free limit should be enough for a single user working on a personal or small project. It should become restrictive when the user is doing serious work or involving a team.

### 3.4 Time Gate (Reverse Trial)

**Definition:** Feature is fully available for a limited time, then reverts to free tier.

**When to use:**
- When features need time to demonstrate value
- When you have a viable free tier to fall back to
- When the loss aversion of losing features drives conversion

**Best practices:**
- Clearly communicate the timeline from day one
- Send reminders before the trial ends (see `trial-optimization`)
- Ensure the downgrade is graceful -- do not delete user data
- Allow users to re-access premium features immediately if they upgrade

**Example:** Notion gives new users a free trial of the paid plan, then downgrades to the free tier.

### 3.5 Team Gate

**Definition:** Feature is free for individuals but gated for teams.

**When to use:**
- Collaboration features that are more valuable at team scale
- When individual usage drives adoption but team usage drives revenue
- When team features have genuine additional complexity (permissions, admin)

**Best practices:**
- Free for 1 user, paid when adding team members
- Or: free up to 3 team members, paid beyond that
- Keep core collaboration (sharing, commenting) free to drive viral growth

**Example:** Figma is free for individual designers but requires a paid plan for team features.

---

## 4. [Reverse Trial Pattern (Elena Verna Framework)](https://amplitude.com/blog/reverse-trial)

The reverse trial inverts the traditional freemium model:

### Traditional Freemium Flow
```
Sign up → Free tier → Upgrade to paid (if convinced)
```

### Reverse Trial Flow
```
Sign up → Full product free for N days → Downgrade to free tier → Upgrade to paid (to restore)
```

### When Reverse Trial Works

- You have a strong, usable free tier (users stay after downgrade)
- Premium features are clearly more valuable but need time to experience
- The product builds data or content over time that makes premium features more valuable
- Loss aversion is a strong motivator for your users

### When Reverse Trial Does Not Work

- No viable free tier (users churn instead of downgrading)
- Premium value is not obvious even after extended use
- Product does not build switching costs during the trial period
- Users feel tricked by the downgrade (poor communication)

### Reverse Trial Implementation Checklist

1. [ ] Define clear premium features that will be removed at trial end
2. [ ] Set trial length (typically 14 days)
3. [ ] Build onboarding that specifically highlights premium features
4. [ ] Create "you are using a premium feature" indicators throughout the trial
5. [ ] Send progress emails showing premium features used
6. [ ] Send pre-downgrade warnings (3 days, 1 day before)
7. [ ] Ensure graceful downgrade (data preserved, premium features locked, clear upgrade path)
8. [ ] Design post-downgrade experience that reminds users what they lost
9. [ ] Track: trial-to-paid rate, trial-to-free rate, free-to-churn rate, delayed conversion rate

---

## 5. Feature Gating Architecture

### Implementation Pattern

```
User Action → Check Entitlement → Allow or Gate

Entitlement check:
1. User's current plan → determines base entitlements
2. Feature flags → allows overrides (trials, beta access, promotions)
3. Usage counters → tracks consumption against limits
4. Result: ALLOW | SOFT_GATE | HARD_GATE | USAGE_EXCEEDED
```

### Technical Considerations

1. **Entitlement service**: Centralize entitlement checks in a single service. Do not scatter plan-checking logic across your codebase.
2. **Feature flags**: Use feature flags to control gate behavior independently of deployments. This lets you adjust gates without code changes.
3. **Graceful degradation**: When a user hits a gate, show what they are missing, not an error. The gate moment is a marketing opportunity.
4. **Caching**: Cache entitlement checks to avoid latency on every action. Invalidate on plan change.
5. **Audit trail**: Log gate interactions to understand which gates drive upgrades and which cause frustration.

### Gate UI Patterns

| Gate Type | UI Pattern | Example Copy |
|-----------|-----------|-------------|
| Soft gate | Lock icon + tooltip | "Advanced analytics is available on Pro. Upgrade to unlock." |
| Usage gate | Progress bar + limit | "3 of 5 projects used. Upgrade for unlimited projects." |
| Usage exceeded | Blocking modal + upgrade CTA | "You have reached your project limit. Upgrade to continue creating." |
| Time gate (ending) | Banner + countdown | "Your Pro trial ends in 3 days. Upgrade to keep these features." |
| Team gate | Invite flow + upgrade prompt | "To invite team members, upgrade to a Team plan." |

---

## 6. Competitive Free Tier Analysis

### How to Audit Competitor Free Tiers

1. **Sign up for every competitor's free tier** (not just read their pricing page)
2. **Document the actual experience:** What can you do? Where do you hit walls?
3. **Map features to a matrix:**

```
| Feature | Your Free | Competitor A Free | Competitor B Free |
|---------|----------|-------------------|-------------------|
| [Feature 1] | Y | Y | Limited |
| [Feature 2] | Limited (3) | Y | - |
| [Feature 3] | - | - | Y |
```

4. **Identify your advantage:** Where is your free tier stronger? Lean into this.
5. **Identify gaps:** Where are competitors more generous? Decide if you need to match.
6. **Test switching costs:** How easy is it for a free user to switch from your product to a competitor? If it is easy, your free tier needs to be more competitive.

### Competitive Positioning Strategies

- **More generous free tier**: Win on adoption volume. Works when you have strong paid-tier differentiation or network effects.
- **Equivalent free tier, better product**: Compete on quality, not quantity. Works when your product is genuinely better.
- **More restrictive free tier, faster time-to-value**: Offer less for free but make the free experience exceptional. Works for focused tools with clear value.

---

## 7. Gating Anti-Patterns

Avoid these common mistakes:

### Anti-Pattern 1: Gating Activation Features
**Mistake:** Putting features behind a paywall that users need to reach the aha moment.
**Result:** Users never experience enough value to want to pay.
**Fix:** Map your activation flow. Every feature in that flow should be free.

### Anti-Pattern 2: Over-Gating to Force Sales
**Mistake:** Making the free tier so restrictive that users must talk to sales to do anything meaningful.
**Result:** Users leave for competitors with better free tiers.
**Fix:** PLG requires a self-serve value experience. If you want sales-led, do not pretend to be PLG.

### Anti-Pattern 3: Hiding the Free Tier
**Mistake:** Not showing the free tier on the pricing page or making it hard to find.
**Result:** Missed acquisition volume.
**Fix:** Feature the free tier prominently. Free is a growth channel, not an afterthought.

### Anti-Pattern 4: Inconsistent Gate Behavior
**Mistake:** Gating features inconsistently (e.g., same feature free in one context but gated in another).
**Result:** User confusion and frustration.
**Fix:** Define clear, consistent rules. A feature is either free or gated, everywhere.

### Anti-Pattern 5: Gating Without Context
**Mistake:** Showing a generic "upgrade to access" message without explaining the feature's value.
**Result:** Users do not know what they are missing.
**Fix:** Every gate should include: what the feature does, why it matters, and a clear path to upgrade.

### Anti-Pattern 6: Punishing Free Users
**Mistake:** Adding watermarks, nagware popups, or degraded performance to free accounts.
**Result:** Users feel disrespected and leave.
**Fix:** Free users are your future customers and advocates. Treat them well.

---

## 8. Migration Strategy: Changing Gates on Existing Users

When you change your gating strategy (e.g., moving a free feature to paid), you must handle existing users carefully.

### Decision Framework

```
Is the feature core to existing users' workflows?
├── YES → Grandfather existing users (keep access for 6-12 months minimum)
│         and gate for new users only
└── NO
    ├── Have users built significant data/content using this feature?
    │   ├── YES → Grandfather with long notice period (90+ days)
    │   └── NO → Migrate with standard notice (30-60 days)
    └── Will this affect a large % of free users?
        ├── YES → Consider grandfathering to avoid mass churn
        └── NO → Migrate with notice
```

### Communication Template for Gate Changes

```
Subject: Changes to [Product] free plan

Hi [Name],

We are making changes to what is included in [Product]'s free plan,
effective [date].

What is changing:
- [Feature X] will now be part of our [Tier] plan
- [Feature Y] limits are changing from [old] to [new]

What this means for you:
- [Specific impact on this user]
- [If grandfathered: "You will keep access until [date]"]
- [If migrated: "After [date], you will need [Tier] to access this feature"]

Why:
- [Honest explanation: product investment, sustainability, better free tier focus]

Your options:
- Upgrade to [Tier] for [$X/month] to keep access
- [Export/download option if applicable]
- Continue using [Product] free with [remaining free features]

We appreciate you being part of the [Product] community.

[Signature]
```

---

## 9. Metrics

Track these metrics to evaluate your gating strategy:

| Metric | What It Tells You | Target |
|--------|-------------------|--------|
| **Free-to-paid conversion rate** | Overall gating effectiveness | 2-5% for freemium |
| **Conversion rate by gate** | Which gates drive upgrades | Varies; compare gates to each other |
| **Gate encounter rate** | How often free users hit gates | 30-50% of active free users should encounter a gate monthly |
| **Gate-to-upgrade rate** | Conversion at each specific gate | 5-15% is strong |
| **Feature request rate** | Demand for gated features | High requests = gate is working |
| **Free user retention** | Is the free tier good enough to retain users | 40-60% monthly retention |
| **Time to first gate encounter** | How quickly users discover paid value | Within first 3 sessions ideally |
| **Upgrade path diversity** | Do users upgrade from multiple gates or just one | Multiple paths = healthier funnel |

### Analysis Framework

1. **Map the gate funnel:** For each gated feature, track: impressions (saw the gate) -> clicks (engaged with upgrade CTA) -> conversions (upgraded)
2. **Identify top-performing gates:** Which gates have the highest conversion rate? Invest in these.
3. **Identify underperforming gates:** Are any gates frequently encountered but never converting? The feature may not be compelling enough to gate, or the gate UX needs improvement.
4. **Segment by user type:** Do different user segments hit different gates? Customize the gate experience per segment.

---

## 10. Diagnostic Questions

When helping a user with feature gating, ask:

1. What is your product's aha moment? What features are required to reach it?
2. What does your current free tier include?
3. What is your current free-to-paid conversion rate?
4. Which features do free users request most often?
5. What do competitor free tiers include?
6. What are your product's viral/collaborative features?
7. What is the marginal cost of a free user?
8. Have you identified which features correlate with upgrade behavior?
9. What is your target user for the free tier vs paid tiers?
10. Are there natural usage dimensions that could serve as limits (projects, storage, users)?

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find plan/tier definitions**: Search for `plan`, `tier`, `subscription`, `pricing` in models, configs, or constants files
2. **Find feature flag logic**: Search for `feature_flag`, `featureFlag`, `isFeatureEnabled`, `hasFeature`, `canAccess`, `isAllowed`
3. **Check for gate components**: Search for `paywall`, `upgrade`, `locked`, `premium`, `pro-only`, `gate`, `restricted` in UI components
4. **Find permission checks**: Search for middleware or guards that check user plan/tier before allowing access
5. **Check for usage limits**: Search for `limit`, `quota`, `usage`, `allowance`, `rate_limit` in business logic
6. **Find trial logic**: Search for `trial`, `trial_end`, `trial_expires`, `isTrial`, `trialDaysRemaining`
7. **List gated features**: From the above, build a map of which features are gated and how (hard gate, soft gate, usage limit, time-limited)
8. **Check for feature flag services**: Search for `launchdarkly`, `split`, `flagsmith`, `growthbook`, `statsig`, `unleash`

Report: produce a feature-gate inventory showing what's free, what's gated, and how each gate works.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 11. Output Format

When completing a feature gating engagement, deliver the following:

```markdown
# Feature Gating Strategy: [Product Name]

## Gating Philosophy
[2-3 sentences on the approach: generous free, tight gates, etc.]

## Feature-Tier-Gate Matrix

| Feature | Free | Starter | Pro | Enterprise | Gate Type |
|---------|------|---------|-----|------------|-----------|
| [Core feature 1] | Y | Y | Y | Y | -- |
| [Core feature 2] | Limited (N) | Higher limit | Unlimited | Unlimited | Usage gate |
| [Advanced feature 1] | Preview only | Y | Y | Y | Soft gate |
| [Team feature 1] | -- | -- | Y | Y | Hard gate |
| [Enterprise feature 1] | -- | -- | -- | Y | Hard gate |

## Free Tier Design
- Target user: [persona]
- Core value: [what free users can accomplish]
- Key limits: [specific limits that create upgrade moments]
- Viral features included: [sharing, invites, etc.]

## Gate UX Specifications
For each gated feature, define:
- Gate type (hard/soft/usage/time/team)
- Gate UI (where it appears, what it shows)
- Upgrade CTA copy
- Upgrade destination (which plan)

## Migration Plan (if changing existing gates)
- Features being moved: [list]
- Grandfather policy: [details]
- Communication plan: [timeline and channels]
- Risk mitigation: [contingency plans]

## Measurement Plan
- Metrics to track: [list]
- Success criteria: [targets]
- Review cadence: [monthly/quarterly]
```

---

## 12. Related Skills

- `pricing-strategy` -- Overall pricing, packaging, and monetization framework
- `paywall-upgrade-cro` -- Optimizing conversion at the gate/paywall moment
- `trial-optimization` -- Designing and optimizing free trial experiences
- `self-serve-motion` -- Building the self-serve purchase and upgrade flow
