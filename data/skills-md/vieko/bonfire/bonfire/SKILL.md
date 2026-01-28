---
name: bonfire
description: Session context persistence for AI coding. Start/end sessions, create specs and docs, review work. Use for session management, "start session", "end session", implementation specs, documentation, code review, or questions about previous work, decisions, blockers, "last time", "what we decided".
license: MIT
allowed-tools: Bash(git:*), Bash(gh:*), Bash(mkdir:*), Bash(rm .bonfire/*), Bash(linear:*), Read, Write, Edit, Glob, Grep, Task, AskUserQuestion
metadata:
  author: vieko
  version: "4.0.0"
---

# Bonfire

Session context persistence for AI coding - save your progress at the bonfire.

Git root: !`git rev-parse --show-toplevel`

## Commands

| Command | Purpose | Details |
|---------|---------|---------|
| `/bonfire start` | Begin session, load context | [commands/start.md](commands/start.md) |
| `/bonfire end` | Save context, archive, health check | [commands/end.md](commands/end.md) |
| `/bonfire config` | Change settings | [commands/config.md](commands/config.md) |
| `/bonfire spec <topic>` | Create implementation spec | [commands/spec.md](commands/spec.md) |
| `/bonfire doc <topic>` | Create documentation | [commands/doc.md](commands/doc.md) |
| `/bonfire review` | Review current work | [commands/review.md](commands/review.md) |

## Command Routing

Parse `$ARGUMENTS` to determine which command to run:

| Input | Action |
|-------|--------|
| `start` | Read [commands/start.md](commands/start.md) and execute |
| `end` | Read [commands/end.md](commands/end.md) and execute |
| `config` or `configure` | Read [commands/config.md](commands/config.md) and execute |
| `spec <topic>` | Read [commands/spec.md](commands/spec.md) and execute |
| `doc <topic>` or `document <topic>` | Read [commands/doc.md](commands/doc.md) and execute |
| `review` | Read [commands/review.md](commands/review.md) and execute |
| Empty or context question | Read session context and answer |

## Quick Reference

### Start Session
- Check/create `.bonfire/` directory
- Read `index.md` for session context
- Set up tasks for cross-session persistence
- Ask what to work on

### End Session
- Update `index.md` with accomplishments
- Sync priorities to tasks
- Run health check (garbage detection)
- Smart archive detection

### Config
- Set specs/docs locations
- Choose git strategy (ignore-all, hybrid, commit-all)
- Enable/disable Linear integration

### Spec
- Research codebase (subagent)
- Interview user for decisions
- Write spec (subagent)
- Verify required sections

### Doc
- Research codebase (subagent)
- Write documentation (subagent)
- Verify required sections

### Review
- Gather context (branch diff, session notes)
- Analyze for blindspots (subagent)
- Present findings by severity
- Offer to fix, spec, or create issues

## Passive Context

When user asks about previous work, decisions, blockers, or references "last time", "previously", "what we decided":

1. Read `<git-root>/.bonfire/index.md`
2. Summarize relevant context
3. Answer the user's question

## Bootstrap

If `.bonfire/index.md` doesn't exist when any command runs, create defaults:

1. Create `.bonfire/` with `specs/`, `docs/`, `archive/`
2. Create `config.json` with defaults
3. Create minimal `index.md`
4. Create `.gitignore`

See [templates/](templates/) for default content.

## File Structure

```
.bonfire/
├── index.md          # Session context (main file)
├── config.json       # Settings
├── specs/            # Implementation specs
├── docs/             # Documentation
├── archive/          # Completed sessions
└── .gitignore        # Git strategy
```
