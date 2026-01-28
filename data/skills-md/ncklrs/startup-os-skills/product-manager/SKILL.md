---
name: product-manager
description: Expert product management guidance for day-to-day PM work. Use when creating roadmaps, prioritizing features, managing stakeholders, planning sprints, grooming backlogs, scoping features, planning releases, defining OKRs, managing technical debt, or coordinating go-to-market. Covers RICE, ICE, MoSCoW frameworks, cross-functional collaboration, and product metrics.
---

# Product Manager

Strategic product management expertise for building the right things, in the right order, with the right people.

## Philosophy

Great product management isn't about features. It's about **outcomes** — solving real problems for real users in ways that drive business results.

The best product managers:
1. **Obsess over problems, not solutions** — Understand deeply before building
2. **Say no more than yes** — Focus is a feature
3. **Bridge all worlds** — Connect customers, engineering, design, and business
4. **Make decisions reversible** — Ship fast, learn faster
5. **Own outcomes, not outputs** — Features shipped means nothing without impact

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `roadmap-*` — Roadmap creation, maintenance, and communication
- `prioritization-*` — RICE, ICE, MoSCoW, and prioritization frameworks
- `stakeholder-*` — Managing up, down, and across the organization
- `sprint-*` — Sprint planning, backlog grooming, ceremonies
- `scoping-*` — Feature scoping, trade-offs, MVP definition
- `release-*` — Release planning, coordination, communication
- `metrics-*` — Product metrics, OKRs, success measurement
- `debt-*` — Technical debt management and balancing

## Core Frameworks

### The Product Trio

```
         ┌─────────────────┐
         │     Product     │
         │     Manager     │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│  UX    │  │Engineering│  │  Data    │
│Designer│  │   Lead    │  │ Analyst  │
└────────┘  └──────────┘  └──────────┘
```

### Prioritization Framework Comparison

| Framework | Best For | Scoring | Complexity |
|-----------|----------|---------|------------|
| **RICE** | Feature prioritization | Reach × Impact × Confidence / Effort | Medium |
| **ICE** | Quick decisions | Impact × Confidence × Ease | Low |
| **MoSCoW** | Release scoping | Must/Should/Could/Won't | Low |
| **Kano** | Customer satisfaction | Delight/Performance/Basic | High |
| **Value vs Effort** | Quick 2x2 plotting | Qualitative quadrants | Low |

### The Product Development Loop

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│   │ Discover │───▶│  Define  │───▶│  Develop │  │
│   └──────────┘    └──────────┘    └──────────┘  │
│         ▲                               │        │
│         │         ┌──────────┐          │        │
│         └─────────│  Measure │◀─────────┘        │
│                   └──────────┘                   │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Roadmap Types

| Type | Audience | Time Horizon | Detail Level |
|------|----------|--------------|--------------|
| **Vision** | Board, investors | 2-5 years | High-level themes |
| **Strategic** | Leadership | 1 year | Quarterly goals |
| **Release** | Stakeholders | Quarter | Features/epics |
| **Sprint** | Dev team | 2 weeks | Stories/tasks |

### The PM Decision Matrix

```
                    High Confidence
                         │
         ┌───────────────┼───────────────┐
         │   VALIDATE    │     SHIP      │
         │  (test more)  │   (execute)   │
Low      │               │               │   High
Impact───┼───────────────┼───────────────┼───Impact
         │    IGNORE     │  INVESTIGATE  │
         │  (say no)     │  (research)   │
         └───────────────┼───────────────┘
                         │
                    Low Confidence
```

## Stakeholder Map

| Stakeholder | Primary Interest | Communication Style |
|-------------|------------------|---------------------|
| **Executives** | Business outcomes, strategy | High-level, metrics-focused |
| **Engineering** | Technical feasibility, quality | Detailed, collaborative |
| **Design** | User experience, usability | Visual, user-centric |
| **Sales** | Revenue, competitive advantage | Customer stories, timelines |
| **Marketing** | Positioning, launch timing | Messaging, dates |
| **Support** | User satisfaction, volume | Pain points, frequency |
| **Customers** | Problems solved, value | Empathy, listening |

## Anti-Patterns

- **Feature factory** — Shipping without measuring outcomes
- **Roadmap theater** — Treating roadmaps as promises, not hypotheses
- **Stakeholder-driven development** — Building what's loudest, not what matters
- **Scope creep acceptance** — Never saying no to "just one more thing"
- **Velocity worship** — Optimizing for speed over impact
- **Documentation paralysis** — Perfect specs over shipping
- **The PM as order taker** — Writing tickets instead of solving problems
- **Ignoring technical debt** — Shipping features on a crumbling foundation
