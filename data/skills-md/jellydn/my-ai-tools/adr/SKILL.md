---
name: adr
description: Manages Architecture Decision Records (ADR) for tracking important architectural decisions
license: MIT
compatibility: claude, opencode, amp, codex, gemini
hint: Use when managing architecture decisions, creating ADRs, or tracking architectural choices
user-invocable: true
metadata:
  audience: all
  workflow: documentation
---

# Architecture Decision Records (ADR)

Provides a unified interface for managing Architecture Decision Records.

## Usage

`/adr <ACTION> [ARGUMENTS]`

## Actions

- **init [DIRECTORY]** - Initialize ADR directory structure
- **new <TITLE>** - Create new ADR with given title
- **supersede <NUMBER> <TITLE>** - Create ADR that supersedes existing one
- **list** - List all ADRs in the project
- **search <TERM>** - Search ADRs by content
- **view <NUMBER>** - View specific ADR
- **help** - Show this help

## What are ADRs?

Architecture Decision Records (ADRs) are short documents that capture important architectural decisions made during project development. They help teams:

- Record the context and reasoning behind decisions
- Track the evolution of architectural choices
- Onboard new team members
- Avoid revisiting already-settled decisions

## ADR Structure

Each ADR typically contains:
- **Title**: Brief description of the decision
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: The situation requiring a decision
- **Decision**: The chosen solution
- **Consequences**: Positive and negative outcomes

## ADR Template

A template is available at `$SKILL_PATH/templates/adr-template.md`:

```markdown
# [NUMBER]. [TITLE]

Date: [DATE]

## Status

[Proposed | Accepted | Deprecated | Superseded by [ADR-NUMBER]]

## Context

[Describe the context and problem statement]

## Decision

[Describe the decision and solution]

## Consequences

### Positive
- [Positive outcome 1]
- [Positive outcome 2]

### Negative
- [Negative outcome 1]
- [Risk or trade-off]
```

## ADR Directory Detection

Common ADR locations to check:
- `doc/adr/` (default)
- `docs/adr/`
- `docs/architecture/decisions/`
- `architecture/decisions/`

## Process Examples

### Create new ADR:
```bash
/adr new "Use PostgreSQL for primary database"
```

### List all ADRs:
```bash
/adr list
```

### Search ADRs:
```bash
/adr search "database"
```

### View specific ADR:
```bash
/adr view 5
```
