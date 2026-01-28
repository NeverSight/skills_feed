---
name: faion-software-architect
description: "Software architecture: system design, patterns, ADRs, quality attributes."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Task, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Software Architect Skill

**Communication: User's language. Docs: English.**

## Purpose

Make informed architecture decisions balancing quality attributes (scalability, performance, security, maintainability) with business constraints (time, cost, team skills).

---

## Quick Decision Reference

| If you need... | Use | File |
|----------------|-----|------|
| **Architecture style** for small team/MVP | Monolith or Modular Monolith | [monolith-architecture.md](monolith-architecture.md), [modular-monolith.md](modular-monolith.md) |
| **Architecture style** for large team | Microservices | [microservices-architecture.md](microservices-architecture.md) |
| **Database** for relational data | PostgreSQL/MySQL | [database-selection.md](database-selection.md) |
| **Database** for documents | MongoDB/DynamoDB | [database-selection.md](database-selection.md) |
| **Database** for cache | Redis | [caching-architecture.md](caching-architecture.md) |
| **API** for external devs | REST + OpenAPI | [patterns.md](patterns.md) |
| **API** for internal | gRPC | [patterns.md](patterns.md) |
| **Communication** async | Kafka/RabbitMQ | [event-driven-architecture.md](event-driven-architecture.md) |
| **Pattern** for distributed transactions | Saga | [distributed-patterns.md](distributed-patterns.md) |
| **Pattern** for resilience | Circuit Breaker | [distributed-patterns.md](distributed-patterns.md) |

---

## Methodologies (30)

**Fundamentals (5):** system-design-process | c4-model | architecture-decision-records | quality-attributes-analysis | trade-off-analysis

**Styles (5):** monolith-architecture | microservices-architecture | modular-monolith | serverless-architecture | event-driven-architecture

**Patterns (5):** creational-patterns | structural-patterns | behavioral-patterns | architectural-patterns | distributed-patterns

**Data (4):** data-modeling | database-selection | caching-architecture | data-pipeline-design

**Infrastructure (4):** cloud-architecture | container-orchestration | api-gateway-design | service-mesh

**Quality (4):** security-architecture | performance-architecture | reliability-architecture | observability-architecture

**Templates (3):** adr-template | quality-attributes | workflows

---

## Quality Attributes

**Scalability:** Handle 10x load? | **Performance:** p95 < 200ms? | **Availability:** 99.9%+ uptime? | **Security:** Threat model done? | **Maintainability:** Deploy daily?

**Framework:** [quality-attributes.md](quality-attributes.md) | **Analysis:** [quality-attributes-analysis.md](quality-attributes-analysis.md)

---

## C4 Model

| Level | Audience | Shows | File |
|-------|----------|-------|------|
| Context (C1) | Business | External systems, users | [c4-model.md](c4-model.md) |
| Container (C2) | Architects | Apps, databases, services | [c4-model.md](c4-model.md) |
| Component (C3) | Developers | Internal components | [c4-model.md](c4-model.md) |

---

## ADR Template

```markdown
# ADR-NNN: Title
## Status: Proposed/Accepted
## Context: Why needed?
## Decision: What we decided
## Consequences: Trade-offs
## Alternatives: Other options
```

**Full template:** [adr-template.md](adr-template.md)

---

## Workflows

**System Design:** Requirements → Scale estimation → High-level design → Components → Quality attributes → Documentation

**Technology Selection:** Define criteria → Research → Evaluate → Decide → Document ADR

**Full workflows:** [workflows.md](workflows.md)

---

*faion-software-architect v1.2*
*30 Methodologies*
