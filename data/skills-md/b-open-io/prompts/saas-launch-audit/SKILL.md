---
name: SaaS Launch Audit
description: This skill should be used when the user asks to "audit my SaaS", "check if I'm ready to launch", "review my launch checklist", "verify my pricing", "audit my payment setup", "check my AI visibility", "prepare for Product Hunt", "validate my SaaS for launch", or mentions launching a SaaS product. Provides a comprehensive, repeatable checklist with PASS/FAIL verification and actionable next steps.
version: 1.0.0
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Grep
  - Glob
  - mcp__claude-in-chrome__*
  - AskUserQuestion
---

# SaaS Launch Audit

A comprehensive, repeatable audit workflow for SaaS products approaching launch. Provides clear PASS/FAIL states with single actionable next steps.

## Purpose

Validate launch readiness across 10 critical areas: validation, pricing, payments, AI economics, discovery, competitors, social presence, legal, trust infrastructure, and launch day operations. Incorporates 2026-specific guidance on outcome-based pricing, AI visibility optimization, and modern SaaS metrics.

## Workflow Overview

1. **Discovery Survey** - Gather project context (product type, audience, stage)
2. **Interactive Verification** - Actively verify items using browser tools and web queries
3. **PASS/FAIL Report** - Output each item with status and next step for failures
4. **Iterate** - Re-run audit after fixes until all items pass

## Discovery Survey

Before running the checklist, gather project context. Use AskUserQuestion:

**Questions to ask:**
1. Product type: B2B SaaS, B2C, Developer Tool, Marketplace, or Other?
2. Target audience/ICP: Who is the primary customer?
3. Current stage: Pre-MVP, Beta/Early Access, or Ready to Launch?
4. Does the product use AI/ML that affects unit economics?
5. Primary domain/URL to audit (if live)

**Platform recommendations based on product type:**
- **Developer Tools**: GitHub, Hacker News, Reddit, X, Dev.to
- **B2B SaaS**: LinkedIn, Product Hunt, G2/Capterra
- **B2C/Consumer**: X, TikTok, Instagram, YouTube
- **Indie Hacker**: Product Hunt, Indie Hackers, X, Reddit

## Audit Checklist (10 Sections)

### 1. Pre-Launch Validation

| Item | Verification Method |
|------|---------------------|
| 50+ discovery calls completed | Ask user |
| Pre-payment secured from 3+ customers | Ask user |
| Problem validated (not just interest) | Ask user for evidence |
| Manual service delivery tested | Ask user |

### 2. Pricing Strategy

Consult `references/pricing-2026.md` for detailed guidance.

| Item | Verification Method |
|------|---------------------|
| Pricing model selected (outcome/usage/hybrid) | Ask user, verify NOT per-seat only |
| Value metric identified | Ask user what outcome they charge for |
| 3-4 tiers with clear differentiation | Browser: check pricing page |
| Annual contract incentives configured | Browser: verify discount shown |
| Pricing page live and scannable | Browser: visual check |

### 3. Payment Integration

Consult `references/payment-verification.md` for Stripe go-live checklist.

| Item | Verification Method |
|------|---------------------|
| Stripe account activated (live keys) | Ask user to confirm |
| Test transactions successful | Ask user |
| Webhook endpoints configured | Ask about endpoint URL |
| Billing portal accessible | Browser: test billing portal link |
| Tax/KYC requirements met | Ask user |

### 4. AI Economics (if applicable)

Consult `references/metrics-2026.md` for AI-first metrics.

| Item | Verification Method |
|------|---------------------|
| Inference costs calculated per action | Ask user for cost breakdown |
| AI costs < 30% of revenue | Calculate: inference cost / revenue per user |
| Gross margin > 50% (AI-adjusted) | Verify: traditional SaaS 80-90%, AI-first 50-65% |
| Margin protection strategy exists | Ask about usage caps, tiering |
| Cost monitoring/alerts configured | Ask user |

> **Note:** IER (Inference Efficiency Ratio) is a useful internal metric but not an industry standard. Target AI costs < 30% of revenue as the primary benchmark.

### 5. GEO & AI Discovery

Consult `references/geo-visibility.md` for optimization guide.

| Item | Verification Method |
|------|---------------------|
| AI visibility audit completed | WebSearch: query ChatGPT/Perplexity for brand |
| Structured data/FAQ schema | Browser: check page source |
| Content uses authoritative language | Browser: check for excessive hedging |
| SSR/pre-rendering for LLM crawlers | Ask about rendering strategy |
| Server response time < 200ms | Run `scripts/tech-audit.sh` |
| Core Web Vitals passing (LCP < 2.5s, INP ≤ 200ms, CLS < 0.1) | Check PageSpeed Insights |

> **2026 Fact:** AI agents account for ~33% of organic search activity. Only 12% of companies appear across ChatGPT, Perplexity, and Claude.

### 6. Competitor Intelligence

Run `scripts/competitor-visibility.sh` for automated checks.

| Item | Verification Method |
|------|---------------------|
| 3+ direct competitors identified | Ask user to list |
| Competitor pricing documented | WebSearch: research each competitor |
| Differentiation statement written | Ask user for positioning |
| AI visibility comparison done | WebSearch: query "[category] tools" |
| Citation sentiment analyzed | Review AI responses for tone |

### 7. Social Media & Launch Prep

Consult `references/launch-tactics.md` and `references/platform-guides.md`.

| Item | Verification Method |
|------|---------------------|
| Primary platform profiles created | Browser: check each platform |
| LinkedIn founder profile optimized | Browser: review profile |
| X/Twitter presence established | Browser: check account |
| Product Hunt profile ready | Browser: check PH profile |
| 400+ PH supporters lined up | Ask user about DM outreach (warm contacts preferred) |
| Launch email sequence drafted | Ask user |
| Content calendar for 30 days | Ask user |
| "Magic Triangle" ready | Ask about founder content + outreach + retargeting |

### 8. Legal & Compliance

| Item | Verification Method |
|------|---------------------|
| Privacy Policy live | Browser: check /privacy or footer link |
| Terms of Service live | Browser: check /terms or footer link |
| Cookie consent banner | Browser: verify banner appears |
| DPA template ready (if B2B) | Ask user |

### 9. Trust Infrastructure

Consult `references/trust-infrastructure.md` for Trust-as-a-Product guide.

| Item | Verification Method |
|------|---------------------|
| Auth system production-ready | Ask user about auth provider |
| Audit logging enabled | Ask user |
| Error tracking configured | Ask about Sentry or similar |
| Uptime monitoring active | Ask user |
| Security headers configured | Run `scripts/tech-audit.sh` |

### 10. Launch Day Readiness

| Item | Verification Method |
|------|---------------------|
| Support channels operational | Browser: check support links |
| FAQ/Knowledge base published | Browser: check /help or /docs |
| Analytics tracking verified | Ask about GA4, PostHog setup |
| Team roles assigned | Ask user |
| Rollback plan documented | Ask user |

## Output Format

Report each item as:

```
[PASS] Item description
```

or

```
[FAIL] Item description
  → Next step: Single actionable instruction
```

Example output:
```
## Pricing Strategy

[PASS] Pricing model selected (usage-based)
[PASS] Value metric identified (API calls)
[FAIL] 3-4 tiers with clear differentiation
  → Next step: Add a middle tier between Free and Pro to capture mid-market
[PASS] Annual contract incentives configured (20% discount)
[FAIL] Pricing page not found
  → Next step: Create /pricing page with tier comparison table
```

## Verification Tools

### Browser Verification
Use `mcp__claude-in-chrome__*` tools to:
- Navigate to pricing, terms, privacy pages
- Check for cookie banners, structured data
- Verify billing portal accessibility
- Review social media profiles

### Web Search Verification
Use WebSearch to:
- Query AI assistants for brand visibility
- Research competitor pricing
- Check product mentions and sentiment

### Script Verification
Use provided scripts:
- `scripts/tech-audit.sh` - Core Web Vitals, SSL, security headers
- `scripts/competitor-visibility.sh` - AI visibility comparison

## Reference Files

Consult these for detailed guidance:

- **`references/pricing-2026.md`** - Outcome/usage-based pricing strategies
- **`references/payment-verification.md`** - Stripe go-live checklist
- **`references/geo-visibility.md`** - GEO/AI discovery optimization
- **`references/launch-tactics.md`** - Product Hunt and social strategies
- **`references/trust-infrastructure.md`** - Trust-as-a-Product requirements
- **`references/metrics-2026.md`** - AI-first SaaS metrics (gross margins, cost optimization)
- **`references/platform-guides.md`** - Platform-specific launch guides

## Completion Criteria

The audit is complete when:
1. All 10 sections have been evaluated
2. Each item shows PASS or FAIL with next step
3. User has a prioritized list of fixes

Re-run the audit after implementing fixes until all critical items pass.

## Key 2026 Insights (Research-Verified)

Embedded throughout this audit:

1. **Pricing**: Per-seat is declining (126% YoY growth in credit models). Use outcome-based or hybrid models. Note: pendulum swinging back toward simplicity.
2. **AI Economics**: Target AI costs < 30% of revenue. Traditional SaaS: 80-90% margins. AI-first: 50-65% margins.
3. **Discovery**: AI agents now ~33% of organic search. Only 12% of companies appear across all AI platforms. Server response < 200ms critical.
4. **Trust**: Trust-as-a-Product is a differentiator, not just compliance.
5. **Product Hunt**: 26.5% of launches get 500-1000 users. 49% fail by relying on PH alone. Warm outreach > cold DMs.
