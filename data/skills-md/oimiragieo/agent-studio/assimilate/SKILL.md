---
name: assimilate
description: Benchmark external agent frameworks and convert findings into a concrete TDD upgrade backlog for agent-studio evolution.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Skill]
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Assimilate

## Overview

Use this skill when the user asks the framework to improve itself, or when EVOLVE identifies a capability gap that should be benchmarked against other codebases.

## When to Use

- User request: "improve the framework", "compare to competitor repos", "adopt best ideas"
- EVOLVE phase where external pattern benchmarking is needed before creating new artifacts
- Reflection/recommend-evolution output calls for concrete upgrade candidates

## The Iron Law

Do not implement borrowed ideas directly. First produce a comparable feature map, explicit gap list, and TDD backlog with checkpoints.

## Four-Phase Execution

Default kickoff message:

```text
I’ll do this in four phases: clone competitor repos into a temp workspace, extract comparable features/tooling surfaces, build a gap list against our repo, then convert that into a concrete TDD backlog with checkpoints to implement and validate improvements. I’m starting by creating the temp comparison workspace and cloning the repos.
```

### Phase 1: Clone + Stage

1. Create workspace under `.claude/context/runtime/assimilate/<run-id>/`.
2. Clone target repos into `externals/<repo-name>/` using shallow clones where possible.
3. Capture inventory:
   - commit hash
   - default branch
   - top-level structure snapshot
4. Never execute untrusted project scripts during assimilation.

### Phase 2: Comparable Surface Extraction

Extract structured comparisons for each external repo and local repo across these surfaces:

- Memory model (tiers, retrieval APIs, persistence, indexing)
- Search stack (lexical, semantic, hybrid, daemon/prewarm, ranking)
- Agent communication/orchestration (task protocol, hooks, event/state flow)
- Creator system (templates, validators, CI gates, policy enforcement)
- Observability/quality (metrics, eval harnesses, state guards)

Output one normalized comparison table per surface.

### Phase 3: Gap List

Build a local gap list with:

- `gap_id`
- current state
- reference pattern (external source + path)
- expected benefit
- complexity (`S|M|L`)
- risk (`low|medium|high`)
- recommended artifact type (`skill|workflow|hook|schema|tool|agent`)

Prioritize by impact and implementation feasibility.

### Phase 4: TDD Upgrade Backlog

Convert prioritized gaps into implementable TDD items:

1. RED: failing test(s) and measurable acceptance criteria
2. GREEN: minimal implementation path
3. REFACTOR: hardening/cleanup
4. VERIFY: integration checks, hook/CI gates, docs updates

Each backlog item must include:

- owner agent
- target files
- command-level validation steps
- rollback/safety notes

## Output Contract

Return markdown with sections in this order:

1. `## Repo Set`
2. `## Comparable Surfaces`
3. `## Gap List`
4. `## TDD Backlog`
5. `## Execution Checkpoints`

If comparison repos are missing, return a blocked state with exact clone commands needed.

## Tooling Notes

- Prefer `pnpm search:code`/`ripgrep` in local repo for precise parity checks.
- Use `research-synthesis` when external research context is needed before scoring gaps.
- Use `framework-context` before writing system-level recommendations.
- Use `recommend-evolution` to record high-priority changes after backlog generation.

## Memory Protocol (MANDATORY)

Before work:

```bash
cat .claude/context/memory/learnings.md
```

After work:

- Record assimilated patterns: `.claude/context/memory/learnings.md`
- Record adoption risks/tradeoffs: `.claude/context/memory/decisions.md`
- Record unresolved blockers: `.claude/context/memory/issues.md`
