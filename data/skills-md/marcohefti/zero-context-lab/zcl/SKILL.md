---
name: zcl
description: Orchestrator workflow for running ZeroContext Lab (ZCL) attempts/suites with deterministic artifacts, trace-backed evidence, and fast post-mortems (shim support for "agent only types tool name").
---

# ZCL Orchestrator (Codex Skill)

This skill is for the *orchestrator* (you), not the spawned "zero context" agent.

## Goal

Run a mission through ZCL with funnel-first evidence and deterministic artifacts under `.zcl/`.

Primary evidence:
- `.zcl/.../tool.calls.jsonl`
- `.zcl/.../feedback.json` (authoritative outcome)

Secondary evidence (optional):
- `.zcl/.../notes.jsonl`
- `.zcl/.../runner.*.json`
- `.zcl/.../runner.command.txt`, `.zcl/.../runner.stdout.log`, `.zcl/.../runner.stderr.log` (suite runner IO capture)

## Operator Invocation Story

When an operator says "run this through ZCL: <mission>", do this:

1. Resolve entrypoint: prefer `zcl` on `PATH`.
2. Preflight version policy for agent reliability:
   - Check latest metadata: `zcl update status --json`
   - Prefer explicit harness floor: set `ZCL_MIN_VERSION=<semver>`; ZCL fails fast with `ZCL_E_VERSION_FLOOR` when below floor.
3. Initialize project if needed: `zcl init` (idempotent).
4. Prefer native host spawning when available (Mode A):
   - Single attempt: `zcl attempt start --suite <suiteId> --mission <missionId> --prompt <promptText> --isolation-model native_spawn --json`
   - Suite batch planning: `zcl suite plan --file <suite.(yaml|yml|json)> --json`
   - Spawn exactly one fresh native agent session per attempt and pass the returned `env`.
5. Use process-runner orchestration only as an explicit fallback (Mode B):
   - `zcl suite run --file <suite.(yaml|yml|json)> --session-isolation process --feedback-policy auto_fail --campaign-id <campaignId> --progress-jsonl <path|-> --shim surfwright --json -- <runner-cmd> [args...]`
   - `--shim surfwright` lets the agent *visibly* type `surfwright ...` while ZCL still records invocations to `tool.calls.jsonl`.
   - Suite run captures runner IO by default into `runner.*` logs for post-mortems.
   - `--feedback-policy strict` disables synthetic feedback finalization; `auto_fail` writes canonical infra-failure feedback when missing.
6. Require the agent to finish by running:
   - `zcl feedback --ok|--fail --result ...` or `--result-json ...`
7. Optionally ask for self-report feedback and persist it as secondary evidence:
   - `zcl note --kind agent --message "..."`
8. Report back from artifacts (not from transcript):
   - Primary: `tool.calls.jsonl`, `feedback.json`
   - Derived: `attempt.report.json`
   - Post-mortem: `zcl attempt explain [<attemptDir>]` (tail trace + pointers)
9. For retrieval/reporting automation use native query commands:
   - Latest attempt: `zcl attempt latest --suite <suiteId> --mission <missionId> --status ok --json`
   - Attempt index rows: `zcl attempt list --suite <suiteId> --status any --json`
   - Run index rows: `zcl runs list --suite <suiteId> --json`

## Fixed Harness Preamble (Turn 1)

You must tell the spawned agent:
- Finish rule: must end with `zcl feedback ...` (required for scoring).
- Attempt context: ZCL attempt env vars are already provided (do not invent ids).
- Tool execution rule depends on how you launched the attempt:
  - If running under `zcl suite run --session-isolation process --shim surfwright`: the agent should invoke `surfwright ...` normally (no `zcl run` ceremony).
  - If no shim is installed: all actions must go through ZCL funnels (e.g. `zcl run -- ...`) so evidence exists.

## Turn 2 (Default)

One sentence mission prompt. Example:

"Use the SurfWright CLI to navigate to https://example.com and record TITLE=<...> via `zcl feedback --ok --result ...`."

## Turn 3 (Optional)

Only if needed: request structured formatting or classification, but do not lead the agent during discovery.

## Expectations (Suite Guardrails)

Suite `expects` can be grounded in:
- `feedback.json` (`expects.ok`, `expects.result.*`)
- trace-derived constraints (`expects.trace.*`), e.g.:
  - `maxToolCallsTotal`, `maxFailuresTotal`, `maxRepeatStreak`
  - `requireCommandPrefix: ["surfwright"]` to ensure SurfWright was actually invoked

## Local Install (CLI + Skill)

If `zcl` is not on `PATH` (or you want it rebuilt from this checkout):
1. Build + install the CLI and link the skill:
   - `scripts/dev-local-install.sh`
2. Optional: auto-install on `git pull` / branch switch:
   - `scripts/dev-install-git-hooks.sh`
