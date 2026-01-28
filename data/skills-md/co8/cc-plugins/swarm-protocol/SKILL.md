---
name: swarm-protocol
description: "Multi-agent development orchestration for complex projects. Use this skill when orchestrating parallel development workstreams, coordinating multiple agent tasks, managing project documentation structure, or executing `/swarm-protocol` commands. Triggers on: (1) `/swarm-protocol <project-name>` to initialize new projects with full planning, (2) `/swarm-protocol` (no args) to continue existing or start new project, (3) requests involving parallel agent coordination, milestone commits, or multi-phase development workflows."
---

# Swarm Protocol

Multi-agent orchestration framework for complex software development projects. Coordinates parallel workstreams, manages project documentation, and automates milestone commits.

## Commands

| Command | Purpose |
|---------|---------|
| `/swarm-protocol-protocol <project-name>` | Initialize new project with full planning phase |
| `/swarm-protocol-protocol` | Continue existing project, convert a plan, or start new |
| `/swarm-protocol-protocol --from-plan=<name>` | Convert a specific plan file to swarm project |

---

## `/swarm-protocol` (No Arguments)

Smart detection: Check branch (`feature/<name>`) → `docs/projects/` → `~/.claude/plans/` → prompt user.

**Detection priority**:
1. Current branch `feature/<name>` → match project in `docs/projects/<name>/`
2. List recent projects by modified date with status from CHANGELOG.md
3. List plans from `~/.claude/plans/` available for conversion
4. Offer new project with random name suggestions

**Project names**: Random from Barcelona region pool (rubi, sitges, mura, tiana, etc.)

**Plan conversion**: Parse plan → auto-populate PROJECT_PLAN.md, IMPLEMENTATION_PLAN.md, AGENT_SWARM_SPEC.md → review before execution.

---

## `/swarm-protocol <project-name>`

Initialize and execute a multi-agent development project.

### Phase 0: Project Setup

1. Create `docs/projects/<name>/` with: PROJECT_PLAN.md, IMPLEMENTATION_PLAN.md, AGENT_SWARM_SPEC.md, CODE_REVIEW.md, CHANGELOG.md
2. Create worktree: `git worktree add ../<repo>-<name> -b feature/<name>`
3. Supabase preview (if DB changes): `supabase branches create <name>`

### Phase 1: Planning (Sequential)

Generate all planning documents before implementation. See `references/templates.md` for document templates.

**Planning sequence**:
1. PROJECT_PLAN.md → Goals, success criteria, dependencies, risks
2. IMPLEMENTATION_PLAN.md → Architecture, file changes, migrations, API endpoints
3. AGENT_SWARM_SPEC.md → Phase breakdown, agent definitions, parallelization strategy

### Phase 2-N: Execution

**Parallelization rules**:
- Agents within a phase run parallel when no file conflicts exist
- Phases with dependencies wait for blockers to complete
- Use `Task` tool for parallel agent invocations

**Progress display**: See `references/templates.md` for colored box format, ANSI codes, and ASCII art variants.

**Status symbols**: `●` (green/complete), `◐` (yellow/in-progress), `○` (dim gray/pending)

**Milestone commits** (after each phase):
```bash
git add -A
git commit -m "feat(<project>): complete phase N - <description>

- Agent N.1: <summary>
- Agent N.2: <summary>

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

### Phase Final: Review

Generate CODE_REVIEW.md with quality metrics, issues found, optimizations applied.

**Final steps**:
1. `npm run test && npm run typecheck && npm run lint`
2. Update project CLAUDE.md
3. **If Supabase preview used**: Execute database deployment workflow (see below)
4. Final commit with review summary

### Options

| Flag | Purpose |
|------|---------|
| `--skip-worktree` | Use current branch instead of creating worktree |
| `--skip-preview` | Skip Supabase preview branch creation |
| `--phases=1,2` | Run only specific phases |
| `--dry-run` | Generate plans only, no execution |
| `--from-phase=N` | Resume from specific phase |
| `--agent=N.M` | Run single agent only |
| `--from-plan=<name>` | Convert a specific plan file to project (e.g., `--from-plan=scalable-forging-lovelace`) |
| `--resume` | Auto-detect last incomplete agent and resume from there |
| `--max-agents=N` | Limit concurrent parallel agents (default: 4) |
| `--graph` | Output agent dependency graph in Mermaid format |

---

## Supabase Database Deployment

If project uses Supabase preview branches, see `references/supabase-deployment.md` for the full deployment workflow including migration validation loops, advisor checks, and production deployment steps.

**Quick ref**: `supabase db push --linked` → fix errors → run advisors → consolidate → deploy to production.

---

## Agent Design Principles

**Parallelization**: Safe when different files/dirs, independent features, tests for completed work. Sequential for dependency chains (Schema→Types→API), base→composite components, core→integration.

**Agent scope**: Single responsibility, own specific files (no overlap), define completion criteria, include validation.

**Communication**: IMPLEMENTATION_PLAN.md + type definitions (shared context), file system (deliverables), CHANGELOG.md (progress).

### Agent Failure Protocol

| Failure | Action |
|---------|--------|
| **Timeout** (>15min) | Log to CHANGELOG, mark blocked, continue non-dependent, prompt user |
| **Error** | Log, retry once, if fails pause and prompt, block dependents |
| **File Conflict** | Halt agents, alert user, request resolution |

**Recovery**: `/swarm-protocol --resume` (auto-resume) | `/swarm-protocol-protocol --agent=2.3 --retry` | `/swarm-protocol-protocol --skip-agent=2.3`

---

## Project Archival

After merge: move docs to `docs/archive/`, remove worktree, delete feature branch, clean Supabase preview if used.

```bash
mv docs/projects/<name> docs/archive/<name>
git worktree remove ../<repo>-<name>
git branch -d feature/<name>
supabase branches delete <name>  # if applicable
```

---

## Best Practices

Plan thoroughly → Keep agents focused → Define interfaces first → Commit per phase → Validate continuously → Document decisions in CODE_REVIEW.md

## Reference Files

| File | Load When |
|------|-----------|
| `references/templates.md` | Always (document templates) |
| `references/agent-patterns.md` | Always (agent configurations) |
| `references/supabase-deployment.md` | DB migrations present |
| `references/progress-art.md` | Display customization |
