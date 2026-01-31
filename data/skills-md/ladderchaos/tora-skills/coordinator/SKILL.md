---
name: coordinator
description: Coordinate project context, track changes, and ensure collaboration coherence across sessions. Use this skill for maintaining project status, tracking decisions, managing handoffs between sessions, and keeping coordination documents up to date.
---

# Coordinator

Responsible for maintaining project context, tracking changes, and ensuring collaboration coherence across sessions.

## When This Skill Activates

- Start of a new session (context loading)
- After major changes (documentation update)
- Before switching focus areas (handoff documentation)
- When project state is unclear
- After deployments or releases

## Core Responsibilities

1. **Context Continuity**: Maintain awareness of recent changes, decisions, and pending work
2. **Change Tracking**: Keep a living record of what's been modified and why
3. **Collaboration Sync**: Ensure consistent understanding across sessions
4. **Decision Memory**: Document architectural decisions and their rationale

## Coordination Artifacts

### 1. STATUS.md (Project Root)

Track current state:
```markdown
# Project Status

## Current Focus
[What we're actively working on]

## Recent Changes (Last 5 Sessions)
- [Date] - [Summary of changes]

## Pending/Blocked
- [Items waiting on dependencies or decisions]

## Known Issues
- [Active bugs or technical debt]
```

### 2. CHANGELOG.md (Project Root)

Keep a living changelog:
```markdown
# Changelog

## [Unreleased]
### Added
### Changed
### Fixed
### Removed
```

### 3. DECISIONS.md (Project Root)

Record significant decisions:
```markdown
# Architectural Decision Records

## ADR-001: [Title]
- **Date**: YYYY-MM-DD
- **Status**: Accepted/Superseded
- **Context**: [Why was this decision needed?]
- **Decision**: [What did we decide?]
- **Consequences**: [What are the implications?]
```

## Session Start Protocol

1. **Read STATUS.md** - Understand current state
2. **Check recent commits** - `git log -10 --oneline`
3. **Review CHANGELOG.md** - What's changed recently
4. **Summarize context** - Brief the session on current priorities

## Session End Protocol

1. **Update STATUS.md** - Reflect new current state
2. **Update CHANGELOG.md** - Add entries for changes made
3. **Document decisions** - Add ADRs if significant choices were made
4. **Note pending work** - What remains to be done next

## Quick Reference Commands

```bash
# Check recent changes
git log -10 --oneline --all

# Check modified files
git status

# Check deployment state (if applicable)
cat apps/web/src/config/deployments.json | jq '.networks'
```

## Anti-Patterns to Avoid

- Making changes without updating coordination docs
- Assuming previous session context is remembered
- Not documenting why a decision was made
- Leaving work in an unclear state
