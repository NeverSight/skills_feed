---
name: context-router
description: |
  Routes context extraction requests to appropriate CLI tools. Triggers on /context,
  /limitless, /research, /pieces, or detected context needs from intent hook.
  Supports single, parallel, and augmented extraction modes.
---

# Context Router

Routes external context extraction to the three-CLI system.

**Trigger Keywords**: context, lifelog, research, ltm, recall, lookup, pieces, limitless, pendant, documentation

## Trigger Conditions

Activate when:
- Explicit commands: `/context`, `/limitless`, `/research`, `/pieces`
- Intent hook signals context need (balanced detection)
- User asks about past conversations, technical docs, or code history

## Source Categories

| Source | CLI | Triggers | Data Type |
|:-------|:----|:---------|:----------|
| **Personal** | limitless | lifelog, pendant, daily, personal, meeting | Transcripts, chats |
| **Research** | research | fact-check, docs, academic, verify, sdk | Citations, documentation |
| **Local** | pieces | ltm, saved, snippets, my code, history | Code, snippets |

## Routing Decision Tree

```
Request Received
    │
    ├── Explicit Command?
    │   ├── /context → Parallel (all sources)
    │   ├── /limitless → Single (limitless)
    │   ├── /research → Single (research)
    │   └── /pieces → Single (pieces)
    │
    ├── Hook Signal Present?
    │   ├── need_limitless=true → Route to limitless
    │   ├── need_research=true → Route to research
    │   ├── need_pieces=true → Route to pieces
    │   └── Multiple → Parallel mode
    │
    └── No Signal
        └── Skip (no context needed)
```

## Mode Selection

| Mode | Trigger | Process |
|------|---------|---------|
| **Single** | Clear single-source intent | Route to one CLI |
| **Parallel** | `/context` or multi-domain | Spawn all relevant CLIs |
| **Augmented** | With deep-research | Pre-enrich Phase 0 |

## CLI Commands

### Limitless (Personal)
```bash
limitless lifelogs search "query" --limit 10 --format json
limitless workflow daily YYYY-MM-DD --format json
limitless workflow recent --hours 24 --format json
```

### Research (Online)
```bash
research docs -t "query" -k "framework" --format json
research fact-check -t "claim" --format json
research pex-grounding -t "medical query" --format json
```

### Pieces (Local)
```bash
pieces ask "query" --ltm
pieces search --mode ncs "pattern"
```

## Integration

- **Skill**: `skill-db/context-orchestrator/SKILL.md`
- **Rules**: `rules/context/*.md`
- **Subagents**: `skill-db/context-orchestrator/agents/*.md`
- **Commands**: `skill-db/context-orchestrator/commands/*.md`
- **Also listed in**: `skills/routers/skills-router/SKILL.md` (Context Skills category)
- **Hooks**: `hooks/context-intent-detector.ts`, `hooks/session-context-primer.sh`
