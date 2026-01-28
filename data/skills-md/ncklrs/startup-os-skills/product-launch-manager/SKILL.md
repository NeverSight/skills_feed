---
name: product-launch-manager
description: Expert product launch strategist for SaaS and technology companies. Use when planning product launches, coordinating cross-functional launch teams, managing beta programs, creating launch communication plans, planning launch day execution, setting up post-launch monitoring, running launch retrospectives, or defining launch metrics. Covers launch tiering, internal enablement, rollback planning, and contingency strategies.
---

# Product Launch Manager

Strategic product launch expertise for technology companies — from launch planning and tiering to execution, monitoring, and retrospectives.

## Philosophy

Great launches aren't about the big bang. They're about **orchestrated precision** that maximizes impact while minimizing risk.

The best product launches:
1. **Tier based on impact** — Not every feature deserves a keynote
2. **Coordinate ruthlessly** — Cross-functional alignment is non-negotiable
3. **Validate before announcing** — Beta programs de-risk everything
4. **Plan for failure** — Rollback plans aren't pessimism, they're professionalism
5. **Measure what matters** — Success criteria before, not after, launch

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `planning-*` — Launch strategy, tiering, timelines, success criteria
- `coordination-*` — Cross-functional alignment, RACI, stakeholder management
- `beta-*` — Early access programs, beta cohorts, feedback loops
- `communication-*` — Internal enablement, external messaging, launch comms
- `execution-*` — Launch day operations, war rooms, monitoring
- `postlaunch-*` — Retrospectives, metrics analysis, iteration

## Core Frameworks

### Launch Tier Model

| Tier | Criteria | Timeline | Channels | Example |
|------|----------|----------|----------|---------|
| **Tier 1** | New product, major platform shift | 8-12 weeks | Full press, event, keynote | New product line |
| **Tier 2** | Major feature, significant expansion | 4-8 weeks | Blog, email, social, PR | Enterprise feature |
| **Tier 3** | Feature enhancement, integration | 2-4 weeks | Blog, changelog, email | New integration |
| **Tier 4** | Bug fix, minor improvement | 1-2 weeks | Changelog, in-app | UI improvement |

### Launch Readiness Model

```
┌─────────────────────────────────────────────────────────┐
│                    LAUNCH READINESS                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Product │  │Marketing│  │  Sales  │  │ Support │    │
│  │  Ready  │  │  Ready  │  │  Ready  │  │  Ready  │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │            │          │
│       └────────────┴─────┬──────┴────────────┘          │
│                          │                              │
│                    ┌─────▼─────┐                        │
│                    │  GO/NO-GO │                        │
│                    │  DECISION │                        │
│                    └───────────┘                        │
└─────────────────────────────────────────────────────────┘
```

### Launch RACI Matrix

| Activity | Product | Marketing | Sales | Support | Eng | Exec |
|----------|---------|-----------|-------|---------|-----|------|
| Feature requirements | A | C | C | C | R | I |
| Launch tier decision | R | C | C | I | C | A |
| Launch date | R | C | I | I | C | A |
| External messaging | C | R | C | I | I | A |
| Internal enablement | C | R | R | R | I | I |
| Technical readiness | C | I | I | I | R | A |
| Support documentation | C | I | I | R | C | I |
| Go/no-go decision | R | R | R | R | R | A |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

### Launch Timeline Template

```
Week -8: Launch brief, tier decision, stakeholder alignment
Week -6: Beta program begins, messaging draft
Week -4: Sales/support enablement starts, PR outreach
Week -2: Go/no-go checkpoint, final content review
Week -1: War room setup, monitoring configured, runbook complete
Day 0:   LAUNCH
Week +1: Post-launch monitoring, quick fixes
Week +2: Launch retrospective, metrics review
```

### Success Criteria Framework

| Category | Metric Type | Example |
|----------|-------------|---------|
| **Adoption** | Usage metrics | DAU, feature adoption rate, activation |
| **Quality** | Stability metrics | Error rate, P0 incidents, rollback rate |
| **Business** | Revenue metrics | Conversion, upsell, pipeline influence |
| **Sentiment** | Feedback metrics | NPS, support tickets, social sentiment |

## Communication Templates

### Launch Brief Structure

```
1. Executive Summary
2. Launch Tier & Rationale
3. Target Audience
4. Key Messages (3 max)
5. Success Criteria
6. Timeline & Milestones
7. RACI & Stakeholders
8. Risks & Mitigations
9. Budget (if applicable)
10. Approval Sign-offs
```

### Go/No-Go Checklist

```
□ Product: Feature complete and tested
□ Product: Performance benchmarks met
□ Engineering: Rollback plan documented
□ Engineering: Monitoring/alerts configured
□ Marketing: All content published/scheduled
□ Marketing: PR embargo lifted
□ Sales: Enablement complete, battlecards ready
□ Support: Documentation live, team trained
□ Legal: Compliance review complete
□ Exec: Final approval received
```

## Anti-Patterns

- **Launch without tiers** — Treating every release like a Tier 1 burns out teams and audiences
- **Big bang only** — Skipping beta means learning in production
- **Engineering complete = launch ready** — Code done ≠ market ready
- **No rollback plan** — Hope is not a strategy
- **Post-hoc success criteria** — Defining success after launch is rationalization
- **Siloed launches** — Marketing finds out when customers do
- **Launch and leave** — No post-launch monitoring or iteration
- **Vanity launch metrics** — Press mentions ≠ product success
