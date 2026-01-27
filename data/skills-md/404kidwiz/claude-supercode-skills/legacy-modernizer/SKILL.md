---
name: legacy-modernizer
description: Expert in migrating monolithic, legacy systems to modern architectures using patterns like Strangler Fig, CDC, and Anti-Corruption Layers. Use when modernizing legacy codebases, breaking monoliths, or planning incremental migrations. Triggers include "legacy migration", "modernization", "strangler fig", "monolith to microservices", "legacy rewrite", "incremental migration".
---

# Legacy Modernizer

## Purpose
Provides expertise in incrementally modernizing legacy systems without full rewrites. Specializes in migration patterns like Strangler Fig, Change Data Capture (CDC), and Anti-Corruption Layers to safely evolve systems while maintaining business continuity.

## When to Use
- Planning migration from monolith to microservices
- Implementing Strangler Fig pattern
- Designing Anti-Corruption Layers between old and new systems
- Setting up Change Data Capture for data synchronization
- Modernizing legacy databases incrementally
- Replacing legacy APIs while maintaining compatibility
- Assessing legacy codebase for modernization priority
- Managing dual-write scenarios during transitions

## Quick Start
**Invoke this skill when:**
- Migrating legacy monoliths to modern architectures
- Implementing Strangler Fig or Branch by Abstraction
- Designing Anti-Corruption Layers
- Setting up CDC for data sync between systems
- Planning incremental modernization roadmaps

**Do NOT invoke when:**
- Greenfield microservices design → use `/microservices-architect`
- General refactoring without migration → use `/refactoring-specialist`
- Database optimization without migration → use `/database-optimizer`
- API design without legacy concerns → use `/api-designer`

## Decision Framework
```
Migration Strategy?
├── Replace Incrementally
│   └── Strangler Fig: Route traffic to new service gradually
├── Abstract and Replace
│   └── Branch by Abstraction: Interface → implement new → switch
├── Data Sync Required
│   └── CDC with Debezium/similar for real-time sync
└── Protect New from Old
    └── Anti-Corruption Layer: Translate between domains
```

## Core Workflows

### 1. Strangler Fig Implementation
1. Identify bounded context to extract
2. Create facade/proxy in front of legacy system
3. Build new service implementing same interface
4. Route subset of traffic to new service
5. Gradually increase traffic percentage
6. Retire legacy component when fully migrated

### 2. Anti-Corruption Layer Setup
1. Define clean domain model for new system
2. Identify integration points with legacy
3. Build translator layer between models
4. Implement adapters for legacy APIs/data
5. Add monitoring for translation failures
6. Document mapping rules

### 3. CDC Data Migration
1. Set up CDC tool (Debezium, AWS DMS)
2. Configure change capture on legacy database
3. Build consumer to apply changes to new system
4. Handle schema differences with transformations
5. Implement validation and reconciliation
6. Plan cutover and fallback strategy

## Best Practices
- Migrate incrementally—avoid big-bang rewrites
- Maintain feature parity during transition
- Use feature flags to control traffic routing
- Implement comprehensive monitoring during migration
- Keep legacy and new systems in sync until cutover
- Document all integration points and dependencies

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Big-bang rewrite | High risk, long timeline | Incremental migration |
| No Anti-Corruption Layer | New system polluted by legacy | Isolate with ACL |
| Dual-write without CDC | Data inconsistency | Use CDC for sync |
| Migrating everything at once | Overwhelming complexity | Prioritize by business value |
| No rollback plan | Stuck if migration fails | Always plan fallback |
