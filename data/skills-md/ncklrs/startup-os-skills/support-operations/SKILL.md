---
name: support-operations
description: Expert support operations guidance for customer service excellence. Use when designing ticket management systems, creating SLA policies, building support tier structures (L1/L2/L3), optimizing knowledge bases, defining severity levels and escalation procedures, implementing support metrics (CSAT, FRT, TTR, FCR), configuring support tool stacks, or building support-to-CS feedback loops. Covers Zendesk, Intercom, Freshdesk, and help desk best practices.
---

# Support Operations

Strategic support operations expertise for customer-facing teams — from ticket management and SLA design to escalation workflows and self-service optimization.

## Philosophy

Great support isn't about closing tickets fast. It's about **solving customer problems permanently** while building scalable systems.

The best support operations teams:
1. **Prevent before they support** — Self-service and proactive help reduce ticket volume
2. **Measure what drives loyalty** — Resolution quality beats response speed
3. **Escalate with context** — Every handoff preserves customer history
4. **Feed insights upstream** — Support data drives product and success improvements

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `ticket-*` — Ticket management, prioritization, queue optimization
- `sla-*` — SLA design, compliance monitoring, escalation triggers
- `tier-*` — Support tier structure, skill-based routing, specialization
- `knowledge-*` — Knowledge base strategy, self-service, deflection
- `metrics-*` — CSAT, FRT, TTR, FCR, quality scoring
- `escalation-*` — Severity definitions, escalation paths, incident management
- `tooling-*` — Support stack optimization, integrations, automation
- `feedback-*` — Support-to-CS handoffs, product feedback loops, voice of customer

## Core Frameworks

### The Support Operations Hierarchy

| Level | Focus | Metrics | Owner |
|-------|-------|---------|-------|
| **Tickets** | Individual resolution | Handle time, CSAT | Agents |
| **Queue** | Flow optimization | Wait time, backlog | Team leads |
| **Channel** | Channel effectiveness | Deflection, containment | Managers |
| **Operations** | System performance | Cost per ticket, NPS | Directors |
| **Strategy** | Business impact | Retention, expansion | VP/C-level |

### The Support Tier Model

```
┌─────────────────────────────────────────────────────────────────┐
│                         TIER 3 (L3)                              │
│  Engineering escalation, code-level issues, custom development  │
│  Target: <5% of tickets | SLA: Best effort                      │
├─────────────────────────────────────────────────────────────────┤
│                         TIER 2 (L2)                              │
│  Technical specialists, complex troubleshooting, integrations   │
│  Target: 15-25% of tickets | SLA: 4-8 hours                     │
├─────────────────────────────────────────────────────────────────┤
│                         TIER 1 (L1)                              │
│  First response, common issues, documentation guidance          │
│  Target: 60-80% resolution | SLA: 15-60 minutes                 │
├─────────────────────────────────────────────────────────────────┤
│                      SELF-SERVICE (L0)                           │
│  Knowledge base, chatbots, community forums, in-app help        │
│  Target: 30-50% deflection | SLA: Instant                       │
└─────────────────────────────────────────────────────────────────┘
```

### Ticket Priority Matrix

| Priority | Business Impact | Response SLA | Resolution SLA | Examples |
|----------|-----------------|--------------|----------------|----------|
| **P1 Critical** | Complete outage, data loss | 15 min | 4 hours | System down, security breach |
| **P2 High** | Major feature broken | 1 hour | 8 hours | Key workflow blocked |
| **P3 Medium** | Feature impaired | 4 hours | 24 hours | Partial functionality |
| **P4 Low** | Minor issue, cosmetic | 8 hours | 72 hours | UI bug, minor inconvenience |
| **P5 Request** | Feature request, how-to | 24 hours | 5 days | Enhancement, training |

### Support Metrics Framework

| Metric | Definition | Target | Warning |
|--------|------------|--------|---------|
| **CSAT** | Customer satisfaction score | 90%+ | <85% |
| **FRT** | First response time | <1 hour | >4 hours |
| **TTR** | Time to resolution | <24 hours | >72 hours |
| **FCR** | First contact resolution | 70%+ | <50% |
| **NPS** | Net promoter score | 30+ | <10 |
| **Ticket Volume** | Tickets per 100 customers | 5-15 | >25 |
| **Deflection Rate** | Self-service success | 30-50% | <20% |
| **Escalation Rate** | Tickets escalated | 10-20% | >30% |
| **Reopen Rate** | Tickets reopened | <5% | >10% |
| **Agent Utilization** | Productive time | 70-80% | <60% or >90% |

### The Ticket Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  NEW → TRIAGED → ASSIGNED → IN PROGRESS → PENDING → RESOLVED   │
│                                    │          │                  │
│                                    ▼          ▼                  │
│                              ESCALATED    WAITING                │
│                                    │     (Customer)              │
│                                    ▼                             │
│                              ENGINEERING                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Channel Strategy Matrix

| Channel | Best For | Cost | Scalability | Personal |
|---------|----------|------|-------------|----------|
| **Self-service** | Common issues | Lowest | Highest | Lowest |
| **Chatbot** | Quick questions | Low | High | Low |
| **Live chat** | Real-time help | Medium | Medium | Medium |
| **Email/Ticket** | Complex issues | Medium | Medium | Medium |
| **Phone** | Urgent/sensitive | High | Low | High |
| **Video** | Technical demos | High | Low | Highest |

## Severity Levels

| Severity | Definition | Escalation Path | Communication |
|----------|------------|-----------------|---------------|
| **SEV1** | System-wide outage | Immediate to engineering + exec | Status page, proactive email |
| **SEV2** | Major feature broken | 1 hour to L3 | Affected users notified |
| **SEV3** | Feature degraded | 4 hours to L2 | Standard ticket updates |
| **SEV4** | Minor impact | Normal queue | Standard ticket updates |

## Key Formulas

### Cost Per Ticket
```
Cost Per Ticket = (Total Support Cost) / (Total Tickets Handled)
Target: $5-25 depending on complexity
```

### Support Capacity Planning
```
Required Agents = (Ticket Volume × Handle Time) / (Available Hours × Utilization Rate)

Example:
(500 tickets × 20 min) / (8 hours × 60 min × 0.75) = 28 agents
```

### Self-Service ROI
```
Savings = (Deflected Tickets × Cost Per Ticket) - Self-Service Investment
```

## Anti-Patterns

- **Speed over quality** — Fast wrong answers create repeat contacts
- **Ticket tennis** — Multiple handoffs without resolution
- **Knowledge hoarding** — Solutions in heads, not documentation
- **Metric gaming** — Closing tickets prematurely to hit targets
- **Escalation avoidance** — L1 struggling when L2 is needed
- **Channel forcing** — Making customers switch channels unnecessarily
- **Copy-paste responses** — Generic answers that don't address the issue
- **Invisible backlog** — Tickets aging without visibility
- **No feedback loop** — Support insights never reach product
- **Over-automation** — Bots handling issues that need humans
