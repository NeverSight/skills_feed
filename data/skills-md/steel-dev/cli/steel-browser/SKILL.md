---
name: steel-browser
description: Use this skill whenever a user needs terminal-first browser automation with `steel browser`, asks to navigate/click/fill/snapshot/get content from websites, needs explicit browser session lifecycle control (`start`, `stop`, `sessions`, `live`, `captcha solve`), or wants to migrate `agent-browser` scripts. Trigger even when the user does not mention this skill by name and instead asks for multi-step web workflows, CDP attach behavior, local runtime setup, CAPTCHA handling, or browser automation troubleshooting.
---

# Steel Browser Skill

Use this skill to produce reliable, executable `steel browser` workflows for agent-driven automation.

## Why this skill exists

`steel browser` keeps broad command compatibility with `agent-browser` while adding Steel-native session lifecycle and endpoint handling. Agents get better results when they use named sessions, deterministic mode selection, and task-specific command patterns instead of one-off ad-hoc commands.

## Use this workflow

1. Identify the operating mode first.
2. Start or attach a named session before interactive work.
3. Run task commands in small verifiable steps.
4. Validate results (`wait`, `snapshot`, `get ...`) before moving on.
5. Stop sessions when the task is done unless the user asks to keep them alive.

## Mode selection rules

- Use cloud mode by default.
- Use self-hosted mode if the user specifies `--local`, `--api-url`, or self-hosted infrastructure.
- Keep mode consistent for all commands in a sequence.

Read [references/steel-browser-lifecycle.md](references/steel-browser-lifecycle.md) for full lifecycle and endpoint precedence details.

## Session discipline

- Prefer `--session <name>` across all commands in one workflow.
- Parse and preserve session `id` from `steel browser start` when needed for downstream tooling.
- Treat `connect_url` as display-safe metadata; do not treat it as a raw secret-bearing URL.

## Task execution pattern

Use this skeleton and adapt commands to the task:

```bash
SESSION="task-$(date +%s)"
steel browser start --session "$SESSION"
steel browser open <url> --session "$SESSION"
steel browser snapshot -i --session "$SESSION"
# perform interactions/get/snapshot commands
steel browser stop --session "$SESSION"
```

For command families and examples, read [references/steel-browser-commands.md](references/steel-browser-commands.md).

## Migration behavior

When users provide `agent-browser` commands or scripts:

1. Convert command prefix from `agent-browser` to `steel browser`.
2. Preserve original behavior intent.
3. Add Steel lifecycle commands (`start`, `stop`, `sessions`, `live`) when explicit session control is needed.

Read [references/migration-agent-browser.md](references/migration-agent-browser.md).

## Troubleshooting behavior

On auth, local runtime, stale sessions, CAPTCHA blocks, or attach errors:

1. Diagnose with `sessions`, `live`, and mode/endpoint checks.
2. For CAPTCHA:
   use mode-aware guidance from the troubleshooting reference.
   Auto mode: wait and monitor screenshots.
   Manual mode: run `steel browser captcha solve`.
   Off mode: restart with CAPTCHA solving enabled and return to the blocked page.
3. Remind users that CAPTCHA solving and strong proxy evasion require a paid Steel plan.
4. Provide a minimal corrective command sequence.
5. Retry the original action sequence.

Read [references/troubleshooting.md](references/troubleshooting.md).

## Response format

When giving users commands, prefer this structure:

1. `Mode`: cloud/self-hosted and why.
2. `Session`: chosen session name and lifecycle steps.
3. `Commands`: exact executable sequence.
4. `Checks`: what output confirms success.

If the user asks for terse output, keep the same order but shorten prose.

## Guardrails

- Do not print or request raw API keys in command output.
- Do not mix cloud and local mode in one flow unless explicitly transitioning.
- Do not assume an existing active session without checking.
- For inherited command uncertainty, use `steel browser <command> --help`.
- There is no top-level `steel browser extract` command; use `steel browser get ...`, `steel browser snapshot`, and `steel browser find ...` instead.

## Reference routing table

- Lifecycle, endpoint precedence, attach rules:
  [references/steel-browser-lifecycle.md](references/steel-browser-lifecycle.md)
- Complete command families and examples:
  [references/steel-browser-commands.md](references/steel-browser-commands.md)
- Migration from upstream command usage:
  [references/migration-agent-browser.md](references/migration-agent-browser.md)
- Error handling and recovery playbooks:
  [references/troubleshooting.md](references/troubleshooting.md)
