---
name: git-orchestrator
description: |
  Meta-orchestrator for managing ~/.claude as a private git repository with automatic
  versioning, branch orchestration, and DAG-based issue tracking. Use when initializing
  the config repo, committing configuration changes, managing feature branches, creating
  worktrees for parallel experimentation, or investigating configuration history.
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob, TodoWrite
model: opus
context: fork
agent: git-orchestrator-agent
user-invocable: true
---

# Git-Orchestrator

##Trigger Patterns

- "/git-orchestrator init"
- "/git-orchestrator commit"
- "/git-orchestrator worktree"
- "initialize claude config repo"
- "commit my configuration changes"
- "create worktree for experiment"
- "show configuration history"

## Applicable Agents

- git-orchestrator-agent (primary meta-orchestrator)
- refactor-agent (consumer for 24hr commits)
- build-domain-agent (git-master integration)

## Infrastructure Dependencies

| Tool | Purpose | Health Check |
|------|---------|--------------|
| bv | Graph analysis, metrics | `bv --version` |
| bd | Issue tracking, DAG | `bd --version` |
| git | Version control | `git --version` |
| claude-mem | Activity logging | `curl localhost:37777/health` |

## Core Operations

### 1. Repository Initialization
```bash
~/.claude/skills/git-orchestrator/scripts/init-repo.sh
```

### 2. Session Lifecycle
- SessionStart: Record initial state, create session branch
- PostToolUse (Write|Edit): Track pending changes
- SessionEnd: Auto-commit with detailed message

### 3. Worktree Management
- Create: Isolated experimentation environments
- Switch: Parallel configuration testing
- Cleanup: Remove stale worktrees

## Integration Points

| Pillar | Hook | Purpose |
|--------|------|---------|
| refactor-agent | PostToolUse | Commit optimizations |
| code-skill | PreToolUse | Preflight validation |
| claude-mem | SessionStart | Activity context |
| ralph-loop | Notification | Activity logging |
| learn-skill | Stop | Crystallize learnings |

## Progressive Loading

### L0 - Trigger (50 tokens)
Frontmatter only - activation check

### L1 - Core (300 tokens)
Core architecture, session hooks, commit automation

### L2 - Worktree Operations (500 tokens)
Branch management, parallel experimentation, worktree lifecycle

### L3 - Pillar Integration (800 tokens)
Cross-pillar coordination, bv/bd integration, compound engineering

## Scripts Reference

| Script | Purpose | Hook |
|--------|---------|------|
| init-repo.sh | Initialize ~/.claude as git repository | Manual |
| session-start.sh | Record session state, create branch | SessionStart |
| track-change.sh | Log file modifications, bd tracking | PostToolUse |
| session-commit.sh | Auto-commit, merge, push | SessionEnd |
| worktree-manager.sh | Create/list/remove worktrees | Manual |
| atomic-write.sh | Resilience layer for safe writes | Utility |
| lock-manager.sh | Detect and fix stale locks | Utility |
| secret-scanner.sh | Pre-commit secret validation | Utility |

## Commands

| Command | Usage |
|---------|-------|
| `/git-orchestrator init` | Initialize repository |
| `/git-orchestrator commit` | Manual commit |
| `/git-orchestrator worktree create <name>` | Create worktree |
| `/git-orchestrator worktree list` | List worktrees |
| `/git-orchestrator worktree cleanup` | Remove stale worktrees |

## Invariants

- **K-Monotonicity**: Configuration changes preserve history (git never loses commits)
- **Homoiconicity**: Meta-orchestrator manages its own versioning
- **Vertex-Sharing**: Integration preserved across all pillars
- **Orthogonality**: Worktrees enable parallel experimentation without conflict

## See Also

- [Git-Orchestrator Agent](../../agents/git-orchestrator-agent.md) — Meta-orchestrator implementation
- [Refactor Agent](../../agents/refactor-agent.md) — Consumer for 24hr auto-commits
- [Git-Master Skill](../git-master/SKILL.md) — Git operations expert
- [Learn Skill](../architecture/learn/SKILL.md) — Knowledge compounding integration
