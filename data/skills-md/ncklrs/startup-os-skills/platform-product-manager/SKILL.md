---
name: platform-product-manager
description: Expert platform and API product management guidance for developer-focused products. Use when planning API product strategy, designing APIs, improving developer experience (DX), creating developer documentation, building SDKs, planning API versioning and deprecation, building developer communities, creating integration marketplaces, or measuring platform health. Covers REST, GraphQL, webhooks, and platform ecosystems.
---

# Platform Product Manager

Strategic product management expertise for API-first and developer-focused platforms — from API design and developer experience to ecosystem building and platform metrics.

## Philosophy

Great platform products aren't about features. They're about making developers **successful**.

The best API and platform products:
1. **Developer experience is product experience** — DX is your primary differentiator
2. **APIs are user interfaces** — Design them with the same care as visual UIs
3. **Documentation is product** — Great docs reduce support, increase adoption, drive success
4. **Ecosystem multiplies value** — Your integrations make your platform stickier

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `api-*` — API design principles, standards, and patterns
- `dx-*` — Developer experience, onboarding, and success
- `docs-*` — Developer documentation strategy and standards
- `sdk-*` — SDK and library strategy
- `versioning-*` — API versioning, deprecation, and migration
- `community-*` — Developer community and ecosystem building
- `marketplace-*` — Integration marketplace and partner strategy
- `metrics-*` — Platform health and success metrics

## Core Frameworks

### Platform Maturity Model

| Stage | Focus | Key Metrics | Team Structure |
|-------|-------|-------------|----------------|
| **Foundation** | Core API, basic docs | API uptime, error rates | PM + Engineers |
| **Growth** | DX, SDKs, onboarding | Time-to-first-call, activation | + DevRel, DX engineers |
| **Scale** | Ecosystem, marketplace | Integration count, partner revenue | + Partner team |
| **Platform** | Network effects, flywheel | Platform GMV, ecosystem value | Full platform org |

### The Developer Journey

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  DISCOVER   │ → │   EVALUATE  │ → │   ADOPT     │ → │   EXPAND    │
│             │   │             │   │             │   │             │
│ - Search    │   │ - Docs      │   │ - Signup    │   │ - More APIs │
│ - Content   │   │ - Sandbox   │   │ - First call│   │ - Higher    │
│ - Referral  │   │ - Pricing   │   │ - Use case  │   │   volume    │
│             │   │             │   │   solved    │   │ - Referral  │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

### API Design Hierarchy

```
                    ┌─────────────────┐
                    │   CONSISTENCY   │  ← Predictable patterns
                    ├─────────────────┤
                    │   SIMPLICITY    │  ← Easy to understand
                    ├─────────────────┤
                    │   DISCOVERABILITY│ ← Self-documenting
                    ├─────────────────┤
                    │   RELIABILITY   │  ← Stable and trustworthy
                    ├─────────────────┤
                    │   PERFORMANCE   │  ← Fast and efficient
                    └─────────────────┘
```

### Developer Success Metrics Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS OUTCOMES                            │
│        Revenue, Retention, Net Dollar Retention                 │
├─────────────────────────────────────────────────────────────────┤
│                    DEVELOPER SUCCESS                            │
│     Active Developers, API Calls, Use Cases Completed           │
├─────────────────────────────────────────────────────────────────┤
│                    DEVELOPER EXPERIENCE                         │
│   Time-to-First-Call, Activation Rate, Support Tickets          │
├─────────────────────────────────────────────────────────────────┤
│                    PLATFORM HEALTH                              │
│        Uptime, Latency, Error Rates, Documentation Quality      │
└─────────────────────────────────────────────────────────────────┘
```

## Platform Types

| Type | Examples | Key Success Factor | Primary Metric |
|------|----------|-------------------|----------------|
| **Infrastructure API** | Stripe, Twilio, AWS | Reliability + DX | API calls, uptime |
| **Data API** | Plaid, Clearbit | Data quality + freshness | Data coverage |
| **Aggregation Platform** | Zapier, Segment | Integrations + ease | Connections made |
| **Developer Tools** | GitHub, Vercel | Workflow fit + speed | Active projects |
| **Embedded Platform** | Shopify Apps | Distribution + value | Install rate, GMV |

## API Style Comparison

| Style | Best For | Complexity | Flexibility | Caching |
|-------|----------|------------|-------------|---------|
| **REST** | CRUD operations, simple resources | Low | Medium | Excellent |
| **GraphQL** | Complex data fetching, mobile | Medium | High | Manual |
| **gRPC** | Internal services, high perf | High | Low | N/A |
| **Webhooks** | Real-time events, async flows | Low | Medium | N/A |
| **WebSocket** | Bi-directional, real-time | Medium | High | N/A |

## Anti-Patterns

- **API-first without developer-first** — Technically great API that's hard to use
- **Documentation as afterthought** — Docs written after API is "done"
- **Breaking changes without warning** — Surprising developers with incompatibilities
- **Vanity integrations** — Building integrations nobody uses for marketing
- **Platform before product-market fit** — Building ecosystem before core value
- **Ignoring support signals** — Not treating support tickets as product feedback
- **One-size-fits-all SDK** — Same SDK strategy for all languages/use cases
- **Versioning without migration path** — New versions without upgrade guides
