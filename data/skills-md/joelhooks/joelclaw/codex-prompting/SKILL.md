---
name: codex-prompting
displayName: Codex Prompting
description: "Use this skill for any request to trigger, coordinate, or craft prompts for Codex. Use when user says 'send to codex', 'use codex', 'prompt codex', 'ask codex', 'delegate to codex', 'run in codex', or asks for a Codex-first execution handoff."
version: 1.0.2
author: Joel Hooks
tags: [codex, prompting, automation, pi, operations]
---

# Codex Prompting Skill

## What this skill is for

Use this when the request is any of the following:
- "send to codex"
- "prompt codex"
- "use codex"
- "ask codex"
- "delegate to codex"
- "delegate this to codex"
- "run this in codex"
- "run in codex"
- "handoff to codex"
- "handoff this to codex"
- "codex this"

The job is to produce a high-signal Codex request that gets directly executed with minimal ambiguity.

## Required model default

- Codex tasks must set model to `gpt-5.3-codex` when unspecified.
- Use an explicit model override only when user explicitly requests another.

## Local runtime defaults (Panda)

- Global defaults live in `~/.codex/config.toml`:
  - `approval_policy = "never"`
  - `sandbox_mode = "danger-full-access"`
  - `allow_login_shell = false`
- Hard safety rails live in `~/.codex/rules/safety.rules`:
  - forbid force/mirror pushes
  - forbid obvious filesystem root wipe commands
  - forbid disk-destruction primitives (`diskutil eraseDisk`, `mkfs`, `dd`)
- `pi-tools` `codex` extension defaults to:
  - `--ask-for-approval never`
  - `--sandbox danger-full-access`
  - `full_auto = false` (opt-in legacy mode)
- Expected behavior:
  - normal `git commit` and `git push` should run without permission friction
  - blocked commands fail fast with explicit `forbidden` decision

## System shape to anchor Codex prompts

- Orchestrated by `packages/system-bus` and durable `Inngest` functions.
- Event bridge and notifications flow through Redis, gateway, and Telegram.
- Observability is required: OTEL -> Typesense (`otel_events`) -> Convex/UI surfaces.
- CLI-first operations are expected; prefer `joelclaw`, `slog`, and skill commands instead of direct daemon/db/process pokes.

## Always-follow execution contract (from OpenAI Codex prompting guide)

1. No preamble, no plans, and no “I’ll do X then Y” narration.
2. Preserve strict action-first output:
   - do exactly what the user asked
   - include only necessary confirmation
   - return direct results.
3. Keep prompts structured and executable.
4. Preserve one clear objective and constrained scope.
5. Prioritize safe shell/tool actions and explicit failure handling.
6. Use parallel tool calls whenever independent work can run concurrently.
7. Use durable workflow patterns in Codex loops:
   - explicit IDs
   - explicit rollback/retry context
   - structured outputs for downstream steps.

## Canonical request format for Codex handoff

Use this exact shape unless the user already provided a better one:

- Goal: `<single concrete outcome>`
- Context: `<repo/path/runtime facts>`
- Constraints: `<time/risk/tool limits>`
- Do:
  - `<task 1>`
  - `<task 2>`
- Deliver:
  - `<artifact paths>`
  - `<verification commands + expected signals>`
- Rollback:
  - `<quick recovery command>`

If asking Codex to operate this repo, include absolute paths and the owning system paths (`apps/web`, `packages/system-bus`, etc.).

## Skill routing reminders

When Codex output needs deeper execution, remind Codex to use these local/system skills first:

- `inngest` and `inngest-durable-functions` for durable work definitions and retries
- `gateway` and `gateway-diagnose` for session/event bridge and Telegram path checks
- `o11y-logging` for telemetry-first implementations
- `joelclaw-system-check` for full environment health checks
- `skill-creator` when defining/expanding skill content
- `joelclaw` CLI (`status`, `runs`, `logs`, etc.) for validation

If context is web work, add:
- `joelclaw-web`, `frontend-design`, and any relevant `next-*` skill.

## Do NOT poll codex_tasks

After dispatching a codex task, **do not poll `codex_tasks` in a loop**. The widget shows live status automatically. Polling every 2-3 seconds wastes tokens, clutters the conversation, and adds no value.

Instead:
- Dispatch the task
- Do other useful work (read files, update ADRs, prepare next steps)
- Check `codex_tasks` **once** after ~60 seconds, or when the widget shows completion
- If the task is still running after 60s, check once more at ~120s
- Never poll more than 3 times total for a single task

The task result is reported back automatically when it finishes. Trust the widget.

## What to include in prompts

For any Codex-requested operational run:
- exact paths
- exact command(s) to run
- expected signals for success/failure
- idempotency strategy
- rollback command.

For any code change:
- file targets (absolute or repo-relative)
- compatibility constraints
- observability check to prove behavior.

## Mac volume mounting note

- Do not assume this is solved universally.
- Treat macOS volume mount failures as environmental and include explicit mount/permission checks before retries.
- If failures recur, route through retry + diagnostic signal collection before reattempt.

## Trigger and detection notes

- This is an intent skill: treat natural language variants as valid.
- If user includes any of:
  - "send to codex"
  - "prompt codex"
  - "use codex"
  - "ask codex"
  - "delegate to codex"
  - "run in codex"
  then route here first.
- If phrasing is vague, ask one minimal clarification and keep the response minimal.

## Quick command patterns

```bash
rg -n "toolName\\\":\\\"codex\\\"|send to codex|prompt codex|use codex|ask codex|delegate to codex|delegate this to codex|run this in codex|run in codex|handoff to codex|handoff this to codex|codex this" ~/.pi/agent/sessions
joelclaw status
joelclaw runs --count 10 --hours 24
joelclaw otel stats --hours 24
```
