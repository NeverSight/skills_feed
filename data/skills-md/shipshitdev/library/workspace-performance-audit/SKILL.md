---
name: workspace-performance-audit
description: Orchestrates comprehensive performance audits across full-stack monorepos. Coordinates performance-expert, design-consistency-auditor, accessibility, security-expert, and qa-reviewer skills to audit frontend, backend, database, browser extensions, and shared packages.
---

# Workspace Performance Audit

## Overview

Orchestrates comprehensive performance audits across entire monorepo workspaces. Coordinates multiple specialized skills to analyze frontend (Next.js), backend (NestJS), database (MongoDB), browser extensions (Plasmo), and shared packages—delivering consolidated reports with prioritized recommendations.

## When to Use

- Full workspace performance review
- Audit a monorepo
- "audit performance", "check workspace performance"
- Identify bottlenecks across frontend, backend, extensions
- Consolidated performance metrics needed

## Skills Orchestrated

| Skill | Focus Area | Phase |
|-------|------------|-------|
| `performance-expert` | Performance metrics & optimization | 1-4 |
| `design-consistency-auditor` | UI/UX consistency & design debt | 1 |
| `accessibility` | WCAG 2.1 AA compliance | 1 |
| `security-expert` | Security validation | 2 |
| `qa-reviewer` | Validation & prioritization | 5 |

## Orchestration Flow

```
Phase 0: Workspace Discovery
    → Identify apps, packages, tech stacks

Phase 1: Frontend Audit (Next.js)
    → Core Web Vitals, Bundle Analysis, Design, A11y

Phase 2: Backend Audit (NestJS)
    → API Response Times, N+1 Queries, Security

Phase 3: Database Audit (MongoDB)
    → Query Performance, Index Analysis

Phase 4: Extension & Packages
    → Bundle Sizes, Memory, Dependencies

Phase 5: Consolidation
    → Aggregate, Score, Prioritize, Report
```

## Key Metrics by Domain

| Domain | Key Metrics | Targets |
|--------|-------------|---------|
| Frontend | LCP, FID, CLS | <2.5s, <100ms, <0.1 |
| Backend | p50, p95 response | <100ms, <200ms |
| Database | Query p95, Index hit | <50ms, >95% |
| Extension | Content script size | <50KB |

## Usage Modes

**Quick Audit:** Essential checks only → 1-page summary
**Full Audit:** All phases → Complete report
**Domain-Specific:** Single domain focus

## Integration

Produces reports for `.agent/AUDITS/YYYY-MM-DD-performance.md`

---

**For detailed phase execution, metric collection commands, report templates, best practices, and example interactions, see:** `references/full-guide.md`
