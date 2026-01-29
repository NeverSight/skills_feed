---
name: knowledge-discovery
description: "Discover relevant skills and knowledge using tiered approach. SKIP for simple tasks, QUICK for single-skill, STANDARD for multi-skill, DEEP for full feature implementation. Auto-selects tier based on task complexity."
layer: 4
tech_stack: [agnostic]
topics: [discovery, index, skills, knowledge, flows, context7, efficiency]
depends_on: []
complements: []
keywords: [discover, find, search, related, skills, knowledge, workflow, flow, tier, quick]
---

# Knowledge Discovery

Adaptive discovery skill with tiered efficiency for different task complexities.

## Discovery Tiers

| Tier | When to Use | Files Read | Time Cost |
|------|-------------|------------|-----------|
| **SKIP** | Simple/obvious tasks, single file edits | 0 | ~0s |
| **QUICK** | Single-skill tasks, known patterns | Quick ref only | ~2s |
| **STANDARD** | Multi-skill tasks, unfamiliar patterns | INDEX + GRAPH | ~10s |
| **DEEP** | Full feature implementation, CRUD flows | All 4 steps | ~15-20s |

## Tier Selection Guide

```
START: What's the task?
│
├─ "Fix typo" / "Add comment" / "Simple edit"
│   └─ SKIP (no discovery needed)
│
├─ "Write tests" / "Add validation" / "Single pattern"
│   └─ QUICK (use inline reference below)
│
├─ "Design API" / "Debug error" / "Multi-step task"
│   └─ STANDARD (read SKILL-INDEX + CONTEXT-GRAPH)
│
└─ "Implement CRUD" / "Add feature" / "Full workflow"
    └─ DEEP (full 4-step protocol)
```

## QUICK Tier: Inline Reference

**Use this for single-skill tasks without reading any files:**

| Task | Skill | No Lookup Needed |
|------|-------|------------------|
| Entity/DTO/AppService | `abp-framework-patterns` | ✓ |
| DbContext/Migration | `efcore-patterns` | ✓ |
| Input validation | `fluentvalidation-patterns` | ✓ |
| Permissions/Auth | `openiddict-authorization` | ✓ |
| Unit/Integration tests | `xunit-testing-patterns` | ✓ |
| E2E tests | `e2e-testing-patterns` | ✓ |
| Query optimization | `linq-optimization-patterns` | ✓ |
| API design | `api-design-principles` | ✓ |
| Technical design doc | `technical-design-patterns` | ✓ |
| Debug/errors | `debugging-patterns` | ✓ |
| Docker/.NET | `docker-dotnet-containerize` | ✓ |
| Git advanced | `git-advanced-workflows` | ✓ |
| Security audit | `security-patterns` | ✓ |

**Common Error → Skill:**

| Error | Skill |
|-------|-------|
| N+1 query | `linq-optimization-patterns` |
| Authorization failed | `openiddict-authorization` |
| Validation failed | `fluentvalidation-patterns` |
| DbUpdateException | `efcore-patterns` |
| Task was canceled | `dotnet-async-patterns` |

## STANDARD Tier Protocol

For multi-skill tasks, read these files:

```
1. DISCOVER  →  Check SKILL-INDEX.md for relevant skills
2. RELATE    →  Check CONTEXT-GRAPH.md for dependencies
```

## DEEP Tier Protocol

For full feature implementation:

```
1. DISCOVER  →  Check SKILL-INDEX.md for relevant skills
2. RELATE    →  Check CONTEXT-GRAPH.md for dependencies
3. REFERENCE →  Read /knowledge/ for shared patterns
4. FOLLOW    →  Use /flows/ for multi-step workflows
```

## Discovery by Task Type

### Creating a New Entity/Feature

1. **Check flow**: [flows/crud-implementation.md](../../flows/crud-implementation.md)
2. **Primary skills**: `abp-framework-patterns`, `efcore-patterns`, `fluentvalidation-patterns`
3. **Knowledge**:
   - [knowledge/entities/base-classes.md](../../knowledge/entities/base-classes.md)
   - [knowledge/examples/crud-entity.md](../../knowledge/examples/crud-entity.md)

### Adding Validation

1. **Primary skill**: `fluentvalidation-patterns`
2. **Knowledge**:
   - [knowledge/examples/validation-chain.md](../../knowledge/examples/validation-chain.md)
   - [knowledge/conventions/naming.md](../../knowledge/conventions/naming.md)

### Implementing Authorization

1. **Primary skill**: `openiddict-authorization`
2. **Related**: `security-patterns`, `abp-framework-patterns`
3. **Knowledge**: [knowledge/conventions/permissions.md](../../knowledge/conventions/permissions.md)

### Writing Tests

1. **Primary skill**: `xunit-testing-patterns`
2. **Knowledge**:
   - [knowledge/conventions/folder-structure.md](../../knowledge/conventions/folder-structure.md)
   - [knowledge/examples/crud-entity.md](../../knowledge/examples/crud-entity.md)

### Debugging an Error

1. **Check index**: Search error message in [SKILL-INDEX.md](../../SKILL-INDEX.md) (Error Message section)
2. **Primary skill**: `debugging-patterns`
3. **Related**: Check skill by keyword match

### Designing an API

1. **Primary skills**: `api-design-principles`, `technical-design-patterns`
2. **Related**: `domain-modeling`, `requirements-engineering`

### Optimizing Queries

1. **Primary skill**: `linq-optimization-patterns`
2. **Related**: `efcore-patterns`
3. **Check index**: Search "N+1" in [SKILL-INDEX.md](../../SKILL-INDEX.md)

## Skill Layer Loading

Load skills in dependency order:

```
Layer 1 (Foundations) → Load first
    csharp-advanced-patterns, dotnet-async-patterns, error-handling-patterns

Layer 2 (Framework) → Load second
    abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Layer 3 (Features) → Load third
    xunit-testing-patterns, security-patterns, distributed-events

Layer 4 (Workflows) → Load as needed
    feature-development-workflow
```

## Index Files Reference

| File | Purpose | Location |
|------|---------|----------|
| **SKILL-INDEX.md** | Find skills by task/keyword/error | [SKILL-INDEX.md](../../SKILL-INDEX.md) |
| **CONTEXT-GRAPH.md** | Skill dependencies, layers, relationships | [CONTEXT-GRAPH.md](../../CONTEXT-GRAPH.md) |
| **knowledge/INDEX.md** | Shared patterns and conventions | [knowledge/INDEX.md](../../knowledge/INDEX.md) |
| **flows/INDEX.md** | Multi-step workflows | [flows/INDEX.md](../../flows/INDEX.md) |

## Quick Lookup Commands

### By Task
```
"I need to create an entity" → abp-framework-patterns + efcore-patterns
"I need to validate input" → fluentvalidation-patterns
"I need to add permissions" → openiddict-authorization
"I need to write tests" → xunit-testing-patterns
"I need to optimize queries" → linq-optimization-patterns
```

### By Error
```
"N+1 query" → linq-optimization-patterns
"Authorization failed" → openiddict-authorization
"Validation failed" → fluentvalidation-patterns
"DbUpdateException" → efcore-patterns
```

### By Keyword
```
"Entity" → abp-framework-patterns
"DbContext" → efcore-patterns
"FluentValidation" → fluentvalidation-patterns
"[Authorize]" → openiddict-authorization
"xUnit" → xunit-testing-patterns
```

## Integration

This skill should be invoked:
- Automatically at the start of complex tasks
- When the user asks "what skills do I need for..."
- Before implementing multi-step workflows
- When encountering unfamiliar patterns or errors

## Related Skills

After discovery, typically load:
- `abp-framework-patterns` - Core ABP patterns
- `efcore-patterns` - Database layer
- `fluentvalidation-patterns` - Input validation
- `openiddict-authorization` - Permissions
- `xunit-testing-patterns` - Testing
