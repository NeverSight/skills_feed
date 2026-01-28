---
name: hooks-builder
type: standard
depth: extended
description: >-
  Creates and configures Claude Code hooks for lifecycle automation. Use when
  implementing PreToolUse validation, PostToolUse formatting, PermissionRequest
  auto-approve, custom notifications, session management, or deterministic agent control.
---

# [H1][HOOKS-BUILDER]
>**Dictum:** *Deterministic behavior requires hooks; prompts fail execution guarantees.*

<br>

Build Claude Code hooks—shell commands execute at agent lifecycle events.

**Tasks:**
1. Read [index.md](./index.md) — Reference file listing for navigation
2. Read [lifecycle.md](./references/lifecycle.md) — Event table, input schemas, exit codes
3. Read [schema.md](./references/schema.md) — Configuration structure, matchers, JSON responses
4. (integration) Read [integration.md](./references/integration.md) — Environment variables, context injection
5. (scripting) Read [scripting.md](./references/scripting.md) — Python standards, security patterns
6. (recipes) Read [recipes.md](./references/recipes.md) — Proven implementation patterns
7. (troubleshooting) Read [troubleshooting.md](./references/troubleshooting.md) — Known issues, platform workarounds
8. (prose) Load `style-standards` skill — Voice, formatting, constraints
9. Validate — Quality gate; see §VALIDATION

**Scope:**
- *Event Selection:* Choose hook type by automation goal (blocking vs observing).
- *Configuration:* Author settings.json entries with matchers and timeouts.
- *Response Handling:* Control agent via exit codes, JSON responses, or prompt evaluation.

[REFERENCE]: [index.md](./index.md) — Complete reference file listing

---
## [1][EVENT_SELECTION]
>**Dictum:** *Automation goal determines hook type; blocking capability varies by event.*

<br>

**Decision Gate:**<br>
- *Intercept before execution?* → PreToolUse (validate/block/modify parameters)
- *Control permission dialogs?* → PermissionRequest (auto-approve/deny)
- *React after completion?* → PostToolUse (format, lint, add context)
- *Inject at session boundaries?* → SessionStart (context), UserPromptSubmit (per-message)
- *Evaluate task completion?* → Stop/SubagentStop (prompt type for LLM judgment)

**Blocking vs Observing:**
- *Blocking (exit 2):* PreToolUse, PermissionRequest, PostToolUse, UserPromptSubmit, Stop, SubagentStop
- *Observing only:* Notification, PreCompact, SessionStart, SessionEnd

---
## [2][CONFIGURATION]
>**Dictum:** *Centralized configuration enables scope-aware hook precedence.*

<br>

| [INDEX] | [SCOPE] | [PATH]                        | [USE]                | [GIT]  |
| :-----: | ------- | ----------------------------- | -------------------- | :----: |
|   [1]   | User    | `~/.claude/settings.json`     | Global, all projects |  N/A   |
|   [2]   | Project | `.claude/settings.json`       | Shared, committed    | Commit |
|   [3]   | Local   | `.claude/settings.local.json` | Personal, testing    | Ignore |

**Precedence:** Local > Project > User.

---
## [3][IMPLEMENTATION]
>**Dictum:** *Deterministic and evaluative patterns require distinct execution modes.*

<br>

| [INDEX] | [TYPE]  | [USE_CASE]                       | [TIMEOUT] | [CHARACTERISTICS]       |
| :-----: | ------- | -------------------------------- | :-------: | ----------------------- |
|   [1]   | command | Validation, formatting, rules    |    60s    | Deterministic, fast     |
|   [2]   | prompt  | Complex evaluation, LLM judgment |    30s    | Context-aware, flexible |

**Prompt Type Scope:** Stop and SubagentStop events only; Haiku provides fast LLM evaluation.

**Guidance:**<br>
- `Command hooks` — Deterministic scripts receive JSON stdin; return exit codes + optional JSON stdout.
- `Prompt hooks` — LLM evaluates decisions; response schema: `{"decision": "approve"|"block", "reason": "..."}`.
- `Blocking` — Exit code 2 blocks action; stderr routes to Claude. Exit 1 also blocks (known bug #4809).

---
## [4][SCRIPTING]
>**Dictum:** *Hook reliability requires functional pipeline patterns.*

<br>

Python 3.14+ with strict typing. Zero imperative patterns.

---
## [5][VALIDATION]
>**Dictum:** *Gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Event: Selected correct hook type for automation goal.
- [ ] Schema: Configuration structure validated per schema.md.
- [ ] Integration: Environment variables and context injection applied.
- [ ] Scripting: Security patterns and tooling gates passed.
- [ ] Quality: JSON syntax valid, timeouts appropriate.

[REFERENCE] Operational checklist: [→validation.md](./references/validation.md)
