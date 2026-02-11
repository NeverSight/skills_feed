---
name: skill-system-soul
description: "Agent behavioral profiles that standardize how different LLMs behave. Load this skill when you need to: (1) adopt a specific behavioral mode for a task, (2) switch between creative/strict/talkative modes, (3) ensure consistent behavior across different models. Profiles define personality, decision heuristics, communication style, and quality standards."
license: MIT
compatibility: opencode
metadata:
  os: windows, linux, macos
---

# Skill System Soul

Soul profiles define **how** you behave, not what you can do. Load a profile to adopt its behavioral guidelines.

## Why

Different models (Claude, GPT, Gemini) have different default behaviors. Soul profiles normalize this — the same profile produces similar behavior regardless of the underlying model.

Different tasks also need different behavioral modes:
- Exploring ideas → be creative, divergent, ask lots of questions
- Reviewing code → be strict, one rule at a time, no mercy
- Discussing with a user → be talkative, dig deep, use question tools

## Selecting a Profile

Match the task to a profile:

| Task Type | Profile | When |
|-----------|---------|------|
| Brainstorming, exploration, research | `creative` | Ideas > correctness, divergent thinking needed |
| Code review, linting, compliance | `strict` | Correctness > speed, zero tolerance for ambiguity |
| User interviews, requirements gathering, discussions | `talkative` | Understanding > efficiency, deep-dive into user intent |
| Standard development work | `balanced` | Default. Blend of all modes. |

Read the profile file: `profiles/<name>.md`

## Profile Structure

Each profile defines:

1. **Identity** — Who you are in this mode
2. **Decision Heuristics** — How to make choices when uncertain
3. **Communication Style** — How to express yourself
4. **Quality Bar** — What counts as "done"
5. **Tool Preferences** — Which tools to favor
6. **Anti-Patterns** — What to avoid in this mode

## Available Profiles

### `balanced` (default)

Standard operating mode. Use when no specific behavioral mode is needed.

Read: `profiles/balanced.md`

### `creative`

Divergent thinking mode. For exploration, brainstorming, and research.

Read: `profiles/creative.md`

### `strict`

Convergent precision mode. For code review, compliance, and rule enforcement.

Read: `profiles/strict.md`

### `talkative`

Deep engagement mode. For user interviews, requirements gathering, and discussions.

Read: `profiles/talkative.md`

## Creating Custom Profiles

Copy `profiles/balanced.md` as template. Adjust the 6 sections to match your needs. Place in `profiles/` directory with a descriptive name.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-soul",
  "version": "1.0.0",
  "capabilities": ["soul-profile-load", "soul-profile-list"],
  "effects": ["fs.read"],
  "operations": {
    "load-profile": {
      "description": "Load a behavioral profile by name. Agent reads and adopts the profile.",
      "input": {
        "profile_name": { "type": "string", "required": true, "description": "Profile name: balanced, creative, strict, talkative, or a user name" }
      },
      "output": {
        "description": "Profile markdown content",
        "fields": { "content": "markdown text" }
      },
      "entrypoints": {
        "agent": "Read profiles/<profile_name>.md"
      }
    },
    "list-profiles": {
      "description": "List available soul profiles.",
      "input": {},
      "output": {
        "description": "Array of profile names",
        "fields": { "profiles": "array of strings" }
      },
      "entrypoints": {
        "agent": "List files in profiles/ directory"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed; profiles are markdown files read directly."
  }
}
```
