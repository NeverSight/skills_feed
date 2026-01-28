---
name: feature-development-workflow
description: "Orchestrate end-to-end feature development from requirements through implementation, testing, and review. Use when: (1) planning feature development stages, (2) coordinating multi-agent feature workflows, (3) understanding SDLC phases for new features."
layer: 4
tech_stack: [agnostic]
topics: [sdlc, feature-development, orchestration, multi-agent, workflow]
depends_on: []
complements: []
keywords: [Feature, SDLC, Stage, Agent, Workflow, Requirements, Design, Implementation, Test]
---

# Feature Development Workflow

For complete feature implementation, use the `/add-feature` command.

## Quick Reference

| Command | Time | Use Case |
|---------|------|----------|
| `/add-feature <name> "<reqs>" --minimal` | ~2 min | Simple CRUD, no docs |
| `/add-feature <name> "<reqs>" --fast` | ~2.5 min | Skip BA, requirements clear |
| `/add-feature <name> "<reqs>"` | ~3 min | Standard (progressive handoff) |
| `/add-feature <name> "<reqs>" --full-review` | ~4.5 min | With code + security review |

## Dependency Chain (Signal-Based)

```
BA(entity+perms) ─┬──→ [Architect + QA-Data] ──→ [Developer + QA-Tests]
🟢 ENTITY_READY   │    🟢 CONTRACTS_READY        (parallel implementation)
                  │
BA(reqs+rules) ───┘    (continues in background, non-blocking)
```

**Signal Protocol**: Agents emit signals (`🟢 ENTITY_READY`, `🟢 CONTRACTS_READY`) to trigger dependent agents immediately.

## Agent Roles

| Stage | Agent | Trigger | Output |
|-------|-------|---------|--------|
| Analyze | `business-analyst` | Start | Entity definition, permissions, requirements |
| Design | `backend-architect` | 🟢 ENTITY_READY | Technical design, interface contracts |
| Test Data | `qa-engineer` | 🟢 ENTITY_READY | TestData.cs, Seeder.cs (parallel with Architect) |
| Implement | `abp-developer` | 🟢 CONTRACTS_READY | Domain, Application, EF Core layers |
| Tests | `qa-engineer` | 🟢 CONTRACTS_READY | Unit tests (parallel with Developer) |
| Review | `abp-code-reviewer` | Phase 2 complete | Review report (optional) |
| Security | `security-engineer` | Phase 2 complete | Security audit (optional) |

## Parallelism Optimizations

- **Phase 1b**: Architect + QA-Data run in parallel (on ENTITY_READY)
- **Phase 2**: Developer + QA-Tests run in parallel (on CONTRACTS_READY)
- **BA secondary outputs**: Non-blocking (requirements.md, business-rules.md)
- **Skipped by default**: ANALYSIS.md, impact-analysis.md (use `--impact` flag)

## Full Documentation

See `.claude/commands/feature/add-feature.md` for complete workflow documentation.
