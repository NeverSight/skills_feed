---
name: orchestration
description: MANDATORY - Load this skill first. Routes to bootstrap + domain rules.
impact: CRITICAL
version: 3.0.0
invokes:
  - rlm-process
---

# Clorch -- Claude Orchestration

```
   ─────────────────◆─────────────────
           ░█████╗░██╗░░░░░░█████╗░██████╗░░█████╗░██╗░░██╗
           ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗██║░░██║
           ██║░░╚═╝██║░░░░░██║░░██║██████╔╝██║░░╚═╝███████║
           ██║░░██╗██║░░░░░██║░░██║██╔══██╗██║░░██╗██╔══██║
           ╚█████╔╝███████╗╚█████╔╝██║░░██║╚█████╔╝██║░░██║
           ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
   ─────────────────◆─────────────────
```

---

## Step 1: Load Bootstrap (ALWAYS)

**Read `bootstrap.md` first.** It contains:
- Role detection (Orchestrator vs Worker)
- Iron Law + Iron Claw (UNBREAKABLE)
- Tool ownership table
- Worker preamble templates
- Memory recovery protocol

Workers: Load bootstrap.md, execute task, return.

---

## Step 2: Detect Task Type

| Request Pattern | Domain |
|-----------------|--------|
| "build", "implement", "add feature" | software-development |
| "fix", "debug", "bug" | software-development |
| "refactor", "clean up" | software-development |
| "review PR", "security audit" | code-review |
| "explore", "understand codebase" | research |
| "write tests", "add coverage" | testing |
| "document", "README" | documentation |
| "deploy", "CI/CD", "pipeline" | devops |
| "analyze data", "chart" | data-analysis |
| "plan", "roadmap" | project-management |
| "trading", "chart", "market", "stock", "crypto" | trading-analysis |
| "UI", "UX", "design", "frontend", "CSS", "accessibility", "performance", "responsive" | frontend-development |

---

## Step 3: Load Rules JIT

| Trigger | Load |
|---------|------|
| After compact detected | rules/memory-recovery.md |
| Planning task decomposition | rules/swarm-patterns.md |
| Choosing which agent | rules/agent-routing.md |
| Large-context tasks | rules/rlm-routing.md |
| External/current data needed | rules/mcp-integration.md |
| Token pressure | rules/cost-management.md |
| Managing multi-agent sessions | rules/context-management.md |
| Multi-task coordination | rules/task-coordination.md |

---

## Rule Index

| Rule | Impact | Purpose |
|------|--------|---------|
| scope-discipline.md | UNBREAKABLE | Iron Claw details |
| core-identity.md | CRITICAL | Clorch identity |
| user-control.md | CRITICAL | Confirmation points |
| worker-preamble.md | CRITICAL | Spawn templates |
| memory-recovery.md | CRITICAL | Post-compact recovery |
| task-coordination.md | HIGH | Claude Code Tasks integration |
| swarm-patterns.md | HIGH | Task decomposition |
| context-management.md | HIGH | Multi-agent sessions |
| thread-pattern.md | HIGH | Output filtering |
| agent-routing.md | HIGH | Agent selection |
| rlm-routing.md | HIGH | Large-context routing |
| mcp-integration.md | MEDIUM | External data |
| cost-management.md | MEDIUM | Token optimization |
| GITIGNORE.md | LOW | Project gitignore patterns |

---

## Domain References

| Domain | Path |
|--------|------|
| Software | references/domains/software-development.md |
| Code Review | references/domains/code-review.md |
| Research | references/domains/research.md |
| Testing | references/domains/testing.md |
| Documentation | references/domains/documentation.md |
| DevOps | references/domains/devops.md |
| Data | references/domains/data-analysis.md |
| Planning | references/domains/project-management.md |
| Trading | references/domains/trading-analysis.md |
| Frontend | references/domains/frontend-development.md |

```
───◆─── Routing Ready ───◆───
```
