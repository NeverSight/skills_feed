---
name: skill-awareness
description: Always active. Tracks usage of code-craft skills across sessions. Log skill applications to enable analytics and identify gaps.
---

# Skill Awareness

## Overview

**Track every skill application to build a practice record.**

When you apply any code-craft skill, log it. This creates a persistent record across Claude Code and OpenCode sessions for analytics, identifying underused skills, and measuring improvement.

## The Iron Rule

```
ALWAYS log when applying a code-craft skill. No silent applications.
```

## Usage Log

Append one JSON line to `~/.claude/skills/skill-usage.jsonl`:

```json
{"ts":"2026-01-22T10:30:00Z","skill":"single-responsibility","agent":"opencode","project":"/path/to/project","ctx":"Split UserManager into UserAuth and UserProfile"}
```

| Field | Value |
|-------|-------|
| `ts` | ISO 8601 timestamp |
| `skill` | Skill name (kebab-case) |
| `agent` | `claude-code` or `opencode` |
| `project` | Working directory path |
| `ctx` | Brief description of application (< 100 chars) |

## Skill Detection Matrix

| If you're doing... | Check these skills |
|-------------------|-------------------|
| Creating/modifying classes | `single-responsibility`, `open-closed`, `composition-over-inheritance`, `encapsulation` |
| Inheritance hierarchy | `liskov-substitution`, `composition-over-inheritance` |
| Adding dependencies | `dependency-inversion`, `interface-segregation` |
| Error handling | `fail-fast`, `exception-hierarchies`, `error-boundaries` |
| Writing API endpoints | `rest-conventions`, `error-responses`, `api-versioning`, `idempotency`, `input-validation` |
| Database queries | `n-plus-one-prevention`, `caching`, `lazy-loading` |
| Writing tests | `tdd`, `test-isolation`, `aaa-pattern` |
| Handling secrets/auth | `secrets-handling`, `auth-patterns`, `input-validation` |
| Concurrent operations | `race-conditions`, `deadlock-prevention`, `idempotency` |
| Copy-pasting code | `dry` |
| Adding "future" features | `yagni`, `kiss` |
| Complex logic | `kiss`, `separation-of-concerns`, `law-of-demeter` |
| Modifying state | `immutability`, `encapsulation` |

## Logging Protocol

After applying a skill:

```bash
echo '{"ts":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","skill":"SKILL_NAME","agent":"AGENT","project":"PROJECT_PATH","ctx":"BRIEF_CONTEXT"}' >> ~/.claude/skills/skill-usage.jsonl
```

## Analytics Commands

**View total usage:**
```bash
cat ~/.claude/skills/skill-usage.jsonl | jq -s 'group_by(.skill) | map({skill: .[0].skill, count: length}) | sort_by(-.count)'
```

**Recent applications:**
```bash
tail -20 ~/.claude/skills/skill-usage.jsonl | jq .
```

**Underused skills (applied < 3 times):**
```bash
cat ~/.claude/skills/skill-usage.jsonl | jq -s 'group_by(.skill) | map({skill: .[0].skill, count: length}) | map(select(.count < 3))'
```

**Never-used skills:**
```bash
# Compare logged skills against all 31
comm -23 <(ls ~/.claude/skills/ | grep -v '\.' | sort) <(cat ~/.claude/skills/skill-usage.jsonl | jq -r '.skill' | sort -u)
```

**Usage by project:**
```bash
cat ~/.claude/skills/skill-usage.jsonl | jq -s 'group_by(.project) | map({project: .[0].project, skills: (group_by(.skill) | map({skill: .[0].skill, count: length}))})'
```

## Available Skills Reference

### SOLID (5)
`single-responsibility`, `open-closed`, `liskov-substitution`, `interface-segregation`, `dependency-inversion`

### Core (6)
`dry`, `yagni`, `kiss`, `composition-over-inheritance`, `law-of-demeter`, `fail-fast`

### Testing (3)
`tdd`, `test-isolation`, `aaa-pattern`

### Security (3)
`input-validation`, `secrets-handling`, `auth-patterns`

### API Design (4)
`rest-conventions`, `error-responses`, `idempotency`, `api-versioning`

### Performance (3)
`n-plus-one-prevention`, `lazy-loading`, `caching`

### Code Quality (3)
`separation-of-concerns`, `encapsulation`, `immutability`

### Error Handling (2)
`exception-hierarchies`, `error-boundaries`

### Concurrency (2)
`race-conditions`, `deadlock-prevention`

## Pre-Completion Checklist

Before finishing any coding task, ask:

1. Which skills from the detection matrix applied?
2. Did I follow them?
3. Did I log each application?
4. Any violations I should flag to the user?

## The Bottom Line

**Every skill application gets logged. No exceptions.**

This builds a record of practice, reveals blind spots, and enables continuous improvement. When in doubt about whether a skill applies—log it and note the uncertainty.
