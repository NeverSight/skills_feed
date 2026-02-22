---
name: revenue-optimizer
description: "Monetization expert that analyzes codebases to discover features, calculate service costs, model usage patterns, and create data-driven pricing with revenue projections. Use when: (1) Analyzing app features and their costs, (2) Modeling user consumption and usage patterns, (3) Calculating ARPU, LTV, and revenue projections, (4) Setting optimal tier limits based on usage percentiles, (5) Creating pricing tiers with adequate margins, (6) Implementing payment systems (Stripe, etc.), (7) Break-even and profitability analysis, (8) Subscription and billing systems."
---

# Revenue Optimizer

Build revenue features and monetization systems. Analyze existing codebases to understand features, calculate costs, and create data-driven pricing strategies.

## Workflow

1. **Discover** - Scan codebase for features, services, and integrations
2. **Cost Analysis** - Calculate per-user and per-feature costs from services
3. **Design** - Create pricing tiers based on value + cost data
4. **Implement** - Build payment integration, pricing logic, and checkout flows
5. **Optimize** - Add conversion optimization and revenue tracking

## Feature Discovery

Scan codebase to build feature inventory:

```
Feature Discovery Process:
1. Scan routes/endpoints → identify user-facing features
2. Scan components/pages → map UI features
3. Scan service integrations → identify cost-generating features
4. Scan database models → understand data entities
5. Cross-reference → map features to their cost drivers
```

Look for these patterns:
- **Routes/Controllers**: Each endpoint = potential feature
- **React/Vue components**: Feature-specific UI modules
- **Service clients**: AWS SDK, OpenAI, Stripe, Twilio, etc.
- **Background jobs**: Compute-intensive operations
- **Storage operations**: S3, database writes, file uploads

Example feature inventory output:
```
Features Discovered:
├── Core Features (low cost)
│   ├── User authentication (Cognito/Auth0)
│   ├── Dashboard views (read-only)
│   └── Basic CRUD operations
├── Premium Features (medium cost)
│   ├── PDF export (uses Puppeteer/Lambda)
│   ├── Email notifications (SendGrid)
│   └── File storage (S3)
└── High-Value Features (high cost)
    ├── AI analysis (OpenAI API)
    ├── Video processing (FFmpeg/Lambda)
    └── Real-time sync (WebSockets)
```

## Cost Analysis

Analyze services to calculate true costs per user/feature. See [references/cost-analysis.md](references/cost-analysis.md) for detailed patterns.

### Service Detection

Scan for these cost sources:
- **Config files**: `.env`, `config/`, secrets
- **Package.json/requirements.txt**: SDK dependencies
- **Infrastructure**: `terraform/`, `cloudformation/`, `docker-compose`
- **Code imports**: `aws-sdk`, `openai`, `stripe`, `twilio`, etc.

### Cost Mapping

```
Cost Analysis Output:
├── Fixed Costs (monthly)
│   ├── Hosting: $50 (Vercel Pro)
│   ├── Database: $25 (PlanetScale)
│   └── Monitoring: $20 (Datadog)
│   └── Total Fixed: $95/month
├── Variable Costs (per user/month)
│   ├── Auth: $0.05/MAU (Auth0)
│   ├── Storage: $0.023/GB (S3)
│   └── Email: $0.001/email (SendGrid)
├── Feature Costs (per use)
│   ├── AI Analysis: $0.03/request (GPT-4)
│   ├── PDF Export: $0.01/export (Lambda)
│   └── SMS: $0.0075/message (Twilio)
└── Recommended Minimums:
    ├── Break-even at 100 users: $0.95/user
    ├── With 70% margin: $3.17/user
    └── AI feature: charge $0.10/use or limit free tier
```

## Pricing Strategy Design

Combine feature value + cost data:

```
Pricing Strategy Framework:
1. Calculate cost floor (break-even)
2. Assess feature value (what users pay for alternatives)
3. Set price = max(cost + margin, perceived value)
4. Group features into tiers by cost similarity
```

### Cost-Informed Tier Design

```
Tier Design Process:
├── Free Tier
│   ├── Include: Low-cost features only
│   ├── Limit: Usage caps on variable costs
│   └── Goal: < $0.50 cost/user/month
├── Pro Tier  
│   ├── Include: Medium-cost features
│   ├── Price: 3-5x your cost (healthy margin)
│   └── Goal: Primary revenue driver
└── Enterprise
    ├── Include: High-cost features (AI, video, etc.)
    ├── Price: Value-based (10x+ cost acceptable)
    └── Goal: High-margin, lower volume
```

See [references/pricing-patterns.md](references/pricing-patterns.md) for implementation examples.

## Complete Analysis Example

When asked to create a pricing strategy, produce a full analysis:

```
═══════════════════════════════════════════════════════════
                    PRICING STRATEGY REPORT
═══════════════════════════════════════════════════════════

📁 CODEBASE ANALYSIS
───────────────────────────────────────────────────────────
Services Detected:
  • AWS S3 (file storage)
  • OpenAI GPT-4 (AI features)
  • SendGrid (email)
  • Auth0 (authentication)
  • Vercel (hosting)
  • PlanetScale (database)

Features Discovered:
  ├── Core (6 features)
  │   ├── User dashboard
  │   ├── Project management
  │   ├── Team collaboration
  │   └── Basic reporting
  ├── Premium (3 features)
  │   ├── PDF export → uses Lambda
  │   ├── Advanced analytics → uses Postgres aggregations
  │   └── API access → rate-limited endpoints
  └── AI-Powered (2 features)
      ├── AI writing assistant → uses GPT-4
      └── Smart suggestions → uses GPT-4

💰 COST BREAKDOWN
───────────────────────────────────────────────────────────
Fixed Costs (Monthly):
  Vercel Pro .............. $20
  PlanetScale Scaler ...... $29
  Auth0 (base) ............ $0
  ─────────────────────────────
  Total Fixed             $49/month

Variable Costs (Per Active User):
  Auth0 MAU ............... $0.02
  Storage (avg 500MB) ..... $0.01
  Email (avg 10/month) .... $0.01
  ─────────────────────────────
  Total Variable          $0.04/user/month

Feature Costs (Per Use):
  AI Writing (1K tokens) .. $0.03/use
  PDF Export .............. $0.01/use
  API Call ................ $0.001/call

📊 USAGE PATTERN ANALYSIS
───────────────────────────────────────────────────────────
Feature Usage Distribution:

  API Calls/month:
  ├── Casual (50%):     ~50 calls    │██░░░░░░░░│
  ├── Regular (40%):    ~500 calls   │██████░░░░│
  └── Power (10%):      ~5,000 calls │██████████│
  
  AI Generations/month:
  ├── Casual (50%):     ~5 uses      │█░░░░░░░░░│
  ├── Regular (40%):    ~50 uses     │█████░░░░░│
  └── Power (10%):      ~300 uses    │██████████│

Tier Limit Strategy:
  ├── Free:   100 API, 10 AI     (80% casual under)
  ├── Pro:    5,000 API, 100 AI  (95% regular under)
  └── Business: Unlimited

📈 REVENUE MODEL
───────────────────────────────────────────────────────────
User Distribution: Free 80% │ Pro 15% │ Business 5%

ARPU: (80%×$0) + (15%×$19) + (5%×$49) = $5.30/user

LTV = (ARPU × Margin) / Churn
    = ($5.30 × 0.87) / 0.04 = $115

Cost to Serve:
  Free: $0.10 │ Pro: $2.50 │ Business: $12

Break-Even: 62 users

12-Month Projection (15% growth):
  M1:  100 users │ $530 MRR
  M6:  266 users │ $1,410 MRR  
  M12: 814 users │ $4,314 MRR → $51,768 ARR

🏷️ RECOMMENDED TIERS
───────────────────────────────────────────────────────────
FREE ($0)
  ✓ 3 projects │ 100 API │ 10 AI │ 500MB
  Cost: $0.10 │ Purpose: Lead generation

PRO ($19/mo · $190/yr save 17%)
  ✓ Unlimited │ 5K API │ 100 AI │ 10GB │ Email support
  Cost: $2.50 │ Margin: 87%

BUSINESS ($49/mo · $490/yr) ⭐ RECOMMENDED
  ✓ All Pro + 50K API │ 500 AI │ 50GB │ 5 seats │ Priority
  Cost: $12 │ Margin: 76%

ENTERPRISE (Custom · $200+)
  ✓ Unlimited │ SSO │ SLA │ Dedicated support

⚠️ OVERAGE: AI $0.10/use │ API $0.005/call

═══════════════════════════════════════════════════════════
```

## Payment Provider Selection

| Provider | Best For | Integration Complexity |
|----------|----------|------------------------|
| Stripe | SaaS, subscriptions, global | Low |
| Paddle | SaaS with tax compliance | Low |
| LemonSqueezy | Digital products, simple | Very Low |
| PayPal | Marketplaces, existing users | Medium |

For detailed integration patterns, see:
- **Stripe**: [references/stripe.md](references/stripe.md)

## Pricing Tier Design

Common patterns:
- **Good-Better-Best**: 3 tiers with clear value escalation
- **Freemium**: Free tier with premium upsell
- **Usage-Based**: Pay per API call, storage, or compute
- **Per-Seat**: Charge per team member

For tier structure examples and implementation, see [references/pricing-patterns.md](references/pricing-patterns.md).

## Subscription Implementation

Key components:
1. **Subscription state management** - Track active, canceled, past_due
2. **Webhook handling** - Process payment events reliably
3. **Entitlement system** - Gate features based on plan
4. **Billing portal** - Self-service plan management

For subscription system patterns, see [references/subscription-patterns.md](references/subscription-patterns.md).

## Usage Pattern Analysis

Analyze how users consume features to set optimal tier limits:

```
Usage Analysis Output:
├── Feature Usage Distribution
│   ├── API Calls
│   │   ├── Casual users (50%): ~50/month
│   │   ├── Regular users (40%): ~500/month
│   │   └── Power users (10%): ~5,000/month
│   └── AI Generations
│       ├── Casual: ~5/month
│       ├── Regular: ~50/month
│       └── Power: ~500/month
├── Consumption Patterns
│   ├── Peak usage: Mon-Fri, 9am-6pm
│   ├── Seasonal spikes: Q4 (+30%)
│   └── Growth trend: +15%/month
└── Tier Limit Recommendations
    ├── Free: 100 API calls (covers 80% of casual)
    ├── Pro: 5,000 API calls (covers 95% of regular)
    └── Enterprise: Unlimited
```

Set limits so users naturally upgrade:
- **Free tier**: Limit at 80th percentile of casual users
- **Pro tier**: Limit at 95th percentile of regular users
- **Enterprise**: Unlimited or custom

See [references/usage-revenue-modeling.md](references/usage-revenue-modeling.md) for detailed patterns.

## Revenue Modeling

Calculate key SaaS metrics for pricing decisions:

```
Revenue Model:
├── ARPU (Average Revenue Per User)
│   ├── Free (80%): $0
│   ├── Pro (15%): $29
│   ├── Enterprise (5%): $99
│   └── Blended ARPU: $9.30
├── LTV Calculation
│   ├── ARPU: $9.30
│   ├── Gross Margin: 85%
│   ├── Monthly Churn: 3%
│   └── LTV = ($9.30 × 0.85) / 0.03 = $263
├── Break-Even Analysis
│   ├── Fixed costs: $500/month
│   ├── Variable cost/user: $0.50
│   ├── ARPU: $9.30
│   └── Break-even: 57 users
└── 12-Month Projection
    ├── Month 1: 100 users, $930 MRR
    ├── Month 6: 400 users, $3,720 MRR
    └── Month 12: 1,200 users, $11,160 MRR
```

### Optimal Tier Pricing Formula

```
Optimal Price = (Cost Floor × 0.3) + (Value Ceiling × 0.7)

Where:
- Cost Floor = Cost to Serve / (1 - Target Margin)
- Value Ceiling = min(Perceived Value, Competitor Price × 1.2)

Example:
- Cost to serve Pro user: $3/month
- Target margin: 80%
- Cost floor: $3 / 0.20 = $15
- Competitor price: $25
- Value ceiling: $30
- Optimal: ($15 × 0.3) + ($30 × 0.7) = $25.50 → $25/month
```

See [references/usage-revenue-modeling.md](references/usage-revenue-modeling.md) for full revenue modeling.

## Checkout Optimization

Conversion-focused checkout implementation:
- Minimize form fields (email → payment in 2 steps max)
- Show trust signals (security badges, money-back guarantee)
- Display social proof near purchase button
- Offer annual discount prominently (20-40% standard)
- Pre-select recommended plan

For checkout implementation details, see [references/checkout-optimization.md](references/checkout-optimization.md).

## Feature Gating Pattern

```typescript
// Entitlement check pattern
async function checkFeatureAccess(userId: string, feature: string): Promise<boolean> {
  const subscription = await getSubscription(userId);
  const plan = PLANS[subscription.planId];
  return plan.features.includes(feature);
}

// Usage in route/component
if (!await checkFeatureAccess(user.id, 'advanced_export')) {
  return showUpgradePrompt('advanced_export');
}
```

## Revenue Tracking

Essential metrics to implement:
- **MRR** (Monthly Recurring Revenue)
- **Churn Rate** (cancellations / total subscribers)
- **LTV** (Lifetime Value = ARPU / churn rate)
- **Conversion Rate** (paid / total signups)

Implementation: Send events to analytics (Mixpanel, Amplitude, or custom) on:
- `subscription.created`
- `subscription.upgraded`
- `subscription.canceled`
- `payment.succeeded`
- `payment.failed`

## Quick Implementation Checklist

- [ ] Payment provider account and API keys configured
- [ ] Webhook endpoint receiving and verifying events
- [ ] Subscription state synced to database
- [ ] Feature entitlement checks on protected routes
- [ ] Billing portal or plan management UI
- [ ] Upgrade prompts at key user moments
- [ ] Revenue events tracked in analytics
- [ ] Failed payment retry and dunning emails
