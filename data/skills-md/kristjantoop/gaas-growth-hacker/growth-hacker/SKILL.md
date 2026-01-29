---
name: growth-hacker
description: "Ultimate growth skill: playbooks, viral loops, acquisition, funnel, retention, competitor intel, personas, content/SEO, growth ideas, product-led growth (PLG), growth audits, and launch execution via MCPs. Use when the user wants growth playbooks, viral/referral, channels, funnel optimization, retention, PLG, product-led, time-to-value, PQL, signup/onboarding/paywall optimization, free-to-paid conversion, expansion revenue, competitor analysis, personas, content/SEO, growth ideas, growth audit, or launch execution (email, ads, analytics, payments, social) with Resend, Meta/Google Ads, PostHog, Stripe, or Twitter MCPs."
---

# Growth Hacker

Expert in growth hacking: playbooks, viral loops, acquisition, funnel optimization, retention, competitor intel, personas, and growth audits for startups and SMEs.

---

## When to Use

Apply this skill when the user mentions or asks for: **growth playbook**, **viral loop**, **referral**, **acquisition channels**, **funnel optimization**, **retention**, **churn**, **competitor analysis**, **personas**, **content strategy**, **SEO for growth**, **growth ideas**, **growth audit**, **AARRR**, **North Star metric**, **launch strategy**, **growth experiments**, **launch execution**, **product-led growth**, **PLG**, **time-to-value**, **TTV**, **PQL**, **product-qualified lead**, **signup flow**, **onboarding**, **activation**, **aha moment**, **paywall**, **free-to-paid**, **freemium conversion**, **expansion revenue**, **self-serve**, **set up email/ads/analytics/payments**, **run campaigns**, **post to Twitter/social**, or **MCP** for growth/launch tasks.

---

## Initial Context

**Check for existing context:** If `.claude/product-marketing-context.md` or a business-context file exists, use it before asking.

Otherwise, gather (or infer):

- **Company**: name, stage (pre-seed, seed, Series A+), industry, business model (saas, marketplace, ecommerce, subscription, freemium), team size, monthly budget.
- **Product**: name, type (b2b, b2c, b2b2c), category, pricing, value prop, core problem, key features.
- **Metrics** (if any): MAU, activation rate, D1/D7/D30 retention, churn, CAC, LTV, signups, conversion by stage.
- **Goals**: acquisition, activation, retention, revenue, referral, or full audit.

---

## Frameworks

- **AARRR (Pirate Metrics)**: Acquisition → Activation → Retention → Revenue → Referral. Prioritize by where the biggest leak or opportunity is.
- **ICE**: Impact × Confidence × Ease. Use to rank experiments and ideas.
- **North Star Metric**: One metric that best reflects value delivered. Align tactics to move it.
- **Growth Loops**: Viral, content, paid, sales. Reinforcing loops beat one-off campaigns.
- **Hook Model**: Trigger → Action → Variable Reward → Investment. For retention and habit.

---

## MCPs & Execution

**When the user wants to execute** (not just plan)—set up email, run ads, configure analytics, create Stripe products, post to social—**use any available MCP tools** from the environment. MCP access is provided by Cursor, Claude Code, or your agent’s MCP config; this skill does not grant MCP access, it directs you to use it when relevant.

### Relevant MCPs

| MCP | Purpose | Example tasks |
|-----|---------|---------------|
| **resend-mcp** | Transactional & marketing email | `create_domain`, `verify_domain`, `send_email`, `send_batch` — welcome, activation, win-back flows |
| **meta-ads-mcp** | Meta (Facebook/Instagram) ads | `create_campaign`, `create_ad_set`, `create_ad`, `create_custom_audience`, `create_lookalike_audience`, `get_pixel_events` — pixel, retargeting, launch campaigns |
| **google-ads-mcp** | Google Ads | `create_conversion_action`, `create_campaign`, `upload_customer_list` — conversion tracking, Performance Max, customer match |
| **posthog-mcp** | Product analytics | `capture`, `identify`, `create_action`, `create_cohort`, `query_insights` — events, funnels, retention, cohorts |
| **stripe-mcp** | Payments & subscriptions | `create_product`, `create_price`, `create_checkout_session`, `create_customer_portal_session` — products, prices, checkout, billing portal |
| **twitter-mcp** | Twitter/X | `post_tweet`, `post_thread`, `upload_media` — launch posts, threads, scheduled social |

### When to use which

- **Launch setup (email)**: resend-mcp → domain + verify, then `send_email` for welcome/activation sequences.
- **Launch setup (ads)**: meta-ads-mcp and/or google-ads-mcp → pixel/audiences first, then campaign/ad set/ad.
- **Launch setup (analytics)**: posthog-mcp → `capture`/`identify` for key events; `create_action` for activation; `query_insights` for funnels/retention.
- **Launch setup (payments)**: stripe-mcp → `create_product`, `create_price`, `create_checkout_session` for paywall/upgrade.
- **Distribution / social**: twitter-mcp → `post_tweet` or `post_thread` for launch and follow-up.

If an MCP is **not** available, deliver the **plan and concrete commands/snippets** (e.g. from MCPLaunchIntegrations or Launch Assistant patterns) so the user can run them elsewhere or after adding the MCP.

---

## 1. Growth Playbook

**Inputs:** target stage (acquisition, activation, retention, revenue, referral), business model, main challenge, budget (bootstrap, seed, funded).

**Output structure:**

```markdown
# [Stage] Playbook: [Name]

## Goal
[One sentence]

## Steps (ordered)
1. **Step name** — What to do, why, and how to measure.
2. ...

## Tactics per step
- Tactic 1 (effort: low/med/high)
- Tactic 2
- ...

## Expected outcomes
- Metric/behavior change and rough timeline

## Resources / tools
- [Concrete tools or templates]

## Risks & mitigations
- Risk → mitigation
```

**Stage-specific focus:**
- **Acquisition**: channels, messaging, landing, signup. CAC and volume.
- **Activation**: first value, onboarding, aha moment, time-to-value.
- **Retention**: cohort curves, hooks, habit, win-backs, churn reasons.
- **Revenue**: pricing, packaging, paywall, upgrade paths, expansion.
- **Referral**: incentives, mechanics, K-factor, sharing triggers.

---

## 2. Viral Loop Design

**Inputs:** product type (b2b, b2c, b2b2c), current K-factor if known, preferred type, constraints.

**Viral loop types:**
- **Word-of-mouth** — Stories, NPS, case studies. Good for b2b and high-touch.
- **Inherent virality** — Collaboration, invites, shared workspaces. Product-native.
- **Incentivized referral** — Reward for invite + signup. Simple, needs unit economics.
- **Content/viral** — Shareable output (calcs, exports, UGC). Good for b2c and tools.

**Output:**
- Recommended loop(s) with mechanism and triggers.
- K-factor target and how to measure.
- Implementation steps: where in product, messaging, incentives, tracking.
- Integration with existing acquisition and retention.

---

## 3. Acquisition Channel Analysis

**Inputs:** industry, product type (b2b/b2c/b2b2c), monthly budget, current channels, target CAC.

**Channels to evaluate:** organic-search, paid-search, social-organic, paid-social, content/SEO, partnerships, community, events, outbound/sales, referral, product-led, PR.

**Per channel, assess:**
- **Fit** to industry and product type (score 1–10).
- **Time to results**: immediate, short, medium, long.
- **Scalability** and **typical CAC** (b2b vs b2c).
- **Difficulty** and **budget feasibility**.

**Output:**
- Ranked channel list with fit, priority, and 2–3 concrete tactics each.
- Recommended **channel mix** (e.g. 50% content, 30% paid, 20% community) and rationale.
- Implementation order and quick wins.

---

## 4. Funnel Optimization

**Inputs:** funnel stages with conversion rates, primary goal (signups, activation, conversion, retention), current metrics.

**Process:**
1. Map stages (e.g. Visit → Signup → Activate → First value → Pay).
2. Compute conversion per step and identify largest drop-offs.
3. For each **bottleneck**: cause, impact, severity (critical/high/medium/low).
4. Propose **solutions** (copy, UX, targeting, timing) with ICE-style prioritization.
5. Suggest **metrics** and simple experiments (A/B or before/after).

**Output:**
- Funnel viz (ascii or list) with conversion %.
- Bottlenecks table: stage, cause, impact, severity, solutions.
- Top 3–5 experiments to run first.

---

## 5. Retention Strategy

**Inputs:** retention metrics (D1, D7, D30, churn), product type, segments, known churn reasons.

**Process:**
1. Compare to benchmarks: D1 >40%, D7 >20%, D30 >10%; churn <5%/mo for SaaS.
2. Find **drop-off points** (onboarding, first value, first week, first month).
3. Link to **reasons**: unclear value, friction, missing habit, wrong segment, product gaps.
4. Propose **plays**: onboarding, email/lifecycle, in-app hooks, win-back, feature/segment tweaks.

**Output:**
- Retention view and benchmarks.
- Root causes and prioritized actions.
- Retention playbook (steps, triggers, messaging, metrics).

---

## 6. Competitor Intelligence

**Inputs:** competitor names/sites, depth (quick, standard, deep), focus (pricing, features, marketing, positioning).

**Assess:**
- Positioning, messaging, and differentiators.
- Features, pricing, packaging.
- Marketing and channel presence.
- Gaps and **opportunities** (positioning, feature, pricing, segment, content).
- **Threats** and possible responses.

**Output:**
- Summary per competitor.
- Opportunity vs threat matrix.
- Recommended differentiators and moves.

---

## 7. User Personas

**Inputs:** product description, target market, any user data, number of personas (default 3).

**Per persona:**
- Name, role, goals, pain points.
- Demographics and behavior (where they are, how they decide).
- Preferred channels and influencers.
- Objections and how the product addresses them.
- Quotes and use cases.

**Output:**
- 2–4 personas in a consistent template.
- Implications for messaging, channels, and product.

---

## 8. Growth Metrics Analysis

**Inputs:** current metrics, optional benchmarks, timeframe.

**Process:**
1. Define **North Star** and supporting metrics.
2. Check **health**: trends, segment performance, funnel, retention.
3. Compare to benchmarks where possible.
4. Call out **anomalies** and likely causes.
5. Suggest **next metrics** to add or refine.

**Output:**
- Metric review and trend comments.
- Issues and hypotheses.
- 3–5 recommended actions or experiments.

---

## 9. Content & SEO Strategy

**Inputs:** industry, target audience, goals, existing content, competitors.

**Deliver:**
- **Topics** (pillar + clusters) aligned to intent and keywords.
- **Content types** (blog, guides, tools, comparison, G2/Capterra, etc.).
- **SEO**: keywords, on-page, internal linking, technical basics.
- **Distribution**: organic, social, email, partnerships.
- **Cadence** and quick wins.

**Output:**
- Content pillars and 10–20 topic ideas.
- SEO and distribution checklist.
- 90-day plan outline.

---

## 10. Growth Ideas / Experiments

**Inputs:** business context, constraints, previous experiments, risk tolerance (conservative, moderate, aggressive).

**Process:**
1. Generate **quick wins** (low effort, fast learning).
2. **Medium-term** plays (new channels, loops, segments).
3. **Moonshots** (high impact, higher risk).
4. Score with **ICE** and filter by risk and resources.

**Output:**
- 5–10 ideas per bucket with hypothesis, method, and success metric.
- Top 3–5 to run next.

---

## 11. Product-Led Growth (PLG)

**Inputs:** product type (b2b, b2c, b2b2c), business model (freemium, free trial, product-led sales), current signup/activation/free-to-paid rates, North Star (if any).

Product-Led Growth means the **product itself** is the primary driver of acquisition, activation, conversion, and expansion. Self-serve and low-touch beat high-touch sales for many SaaS and tools.

### PLG fundamentals

- **PQL (Product-Qualified Lead)**: A user who has experienced enough value in-product to be a strong sales or upgrade candidate. Define the in-app behavior that signals intent.
- **Time-to-Value (TTV)**: Minutes or actions from signup to “aha moment.” Shorter TTV = higher activation and conversion.
- **Self-serve funnel**: Try → Activate → Convert → Expand. Each step should be measurable and improvable in-product.

### Signup flow (first touch)

- **Minimize required fields**: Email + password (or social) first. Defer name, company, role to onboarding or progressive profiling.
- **Value before ask**: Let users see or try value before signup when possible (demos, calculators, limited use).
- **Reduce perceived effort**: Progress indicators, smart defaults, inline validation, clear “what happens next.”
- **Social / SSO**: Prominent Google, Apple, Microsoft, or GitHub; often converts better than email-only.

### Onboarding & activation

- **Aha moment**: The action that correlates most with retention. Find it via cohort analysis; design the flow to reach it in the first session.
- **One goal per session**: Get one clear win in the first use. Save advanced features for later.
- **Do, don’t show**: Interactive > tutorial. Empty states that invite “add your first X” beat long tours.
- **Onboarding checklist**: 3–7 items, ordered by impact, with progress and a dismiss option. Don’t trap.
- **Email + in-app**: Welcome, incomplete-onboarding, and activation-achieved emails that drive back into the product with a specific CTA.

### Free-to-paid conversion & paywalls

- **Value before ask**: Show the upgrade only after the user has felt value (post–aha moment or when hitting a real limit).
- **Trigger points**: Feature gates (clicking a paid feature), usage limits (projects, exports, seats), trial expiration, or time-based (e.g. after 7 days of use).
- **Paywall copy**: Headline on benefit (“Unlock X to get Y”), short value demo, clear plan comparison, specific CTA, and a respectful “Not now” or “Continue with Free.”
- **Timing**: Not during onboarding; limit frequency per session; cool-down after dismiss (days, not hours).

### Expansion revenue

- **Usage-based**: More usage → higher plan or overage. Align pricing with value.
- **Seat expansion**: Encourage team invites and team plans; make “add teammate” obvious at the right moment.
- **Land-and-expand**: Single user → team → org. Track expansion MRR and time-to-expand.

### Free tools (try-before-buy / lead gen)

- **When it fits PLG**: Calculators, generators, analyzers, or limited-use versions that mirror the core product. Tool = lead and first value.
- **Gating**: Fully gated, partial (preview + email for full), or ungated for reach. Balance capture vs. usage.
- **Path to product**: Clear next step from tool to full product or trial.

### PLG audit output

For a **PLG audit**, run through:

1. **Signup**: Friction, fields, social auth, post-submit flow.
2. **TTV & activation**: Aha moment defined? Steps to reach it? Activation rate and time-to-activation.
3. **Onboarding**: First session flow, checklist, empty states, email triggers.
4. **Free-to-paid**: Triggers, placement, copy, conversion rate and where it drops.
5. **Expansion**: Usage-based or seat-based plays; expansion MRR; time-to-expand.

**Output:**
- PLG funnel (Signup → Activate → Convert → Expand) with current rates and benchmarks.
- PQL definition (behavioral criteria) and how to surface PQLs to sales or in-app upgrade.
- Findings table: area, issue, impact, recommendation, priority.
- Top 3–5 experiments (e.g. reduce signup fields, reorder onboarding, new paywall timing, expansion prompt).

---

## 12. Full Growth Audit

**Inputs:** full business context (company, product, market, metrics, personas, competitors, objectives).

**Process:**
1. Run through: playbooks (prioritized stages), viral potential, channels, funnel, retention, **PLG** (signup, TTV, activation, free-to-paid, expansion), competitors, personas, metrics, content.
2. Synthesize **insights** (stage-specific, metrics-based, channel, viral, PLG).
3. Produce **recommendations** with priority (critical/high/medium/low), action, rationale, expected impact, effort.

**Output:**
- Executive summary (3–5 insights).
- Prioritized recommendations table.
- Optional deeper sections per area.

---

## 13. Launch Execution (with MCPs)

**Inputs:** app/product name, tagline, URL, category, target audience, pricing model, launch date, budget. Optionally: `.claude/product-marketing-context.md` or business-context.

**When the user wants to execute** (e.g. “set up our launch,” “create the welcome email,” “create a Meta campaign,” “add PostHog events,” “create Stripe products,” “post our launch on Twitter”):

1. **Gather context** — app name, URL, pricing, audience. Reuse product-marketing-context if present.
2. **Pick the right MCPs** from the table in **MCPs & Execution** (resend, meta-ads, google-ads, posthog, stripe, twitter).
3. **Call the MCP tools** to perform the task (e.g. `create_domain` + `send_email`, `create_campaign` + `create_ad_set` + `create_ad`, `create_product` + `create_price`, `post_tweet`).
4. **If an MCP is missing** — output a ready-to-run snippet or command block so the user can run it after configuring that MCP.

**Typical launch flow:** email domain + templates → pixel + audiences → first campaign (paused until launch) → PostHog events/actions → Stripe products/prices → launch-day Twitter post. Run only the steps the user asked for, unless they request a “full launch setup.”

**Output:** confirm what was created (IDs, URLs) and any follow-up (DNS records, env vars, “activate campaign on launch day”).

---

## Output Conventions

- **Concise first**: lead with the 3–5 most important points, then detail.
- **Actionable**: every recommendation = clear next step and how to measure.
- **Prioritized**: critical/high first; use ICE when comparing experiments.
- **Structured**: use headers, lists, and tables so the user can skim and share.

---

## Programmatic Use

For scripted or agent use, the `gaasai-growth-hacker-skill` package provides the same capabilities via TypeScript:

```bash
npm install gaasai-growth-hacker-skill
```

```typescript
import growthHackerSkill, { BusinessContext } from 'gaasai-growth-hacker-skill';

const result = await growthHackerSkill.execute({ sessionId: 'x', businessContext });
// result.insights, result.nextActions, result.data
```

Use this skill for **interactive** guidance in chat; use the package when you need **structured, repeatable** runs (e.g. in pipelines or dashboards). For **launch execution**, the agent uses MCPs (resend, meta-ads, google-ads, posthog, stripe, twitter) when configured in Cursor/Claude Code; the package’s `MCP_SERVERS` and `mcpCommandGenerator` document the same tools and patterns for automation.
