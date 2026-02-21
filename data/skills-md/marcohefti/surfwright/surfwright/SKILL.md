---
name: surfwright
description: Use when controlling a browser through the SurfWright CLI in deterministic agent loops. Prefer default JSON output, explicit `sessionId`/`targetId` handles, and typed error-code handling.
---

# SurfWright Skill

## When To Use

- You need deterministic browser control through the `surfwright` CLI.
- You need explicit handles (`sessionId`, `targetId`) instead of implicit active-tab state.
- You need typed errors (`code`, `message`, `retryable`) for stable automation branches.

## Runtime Source Of Truth

Always refresh command/error truth from runtime before non-trivial loops:

```bash
surfwright contract
```

Do not assume docs are fresher than the contract payload.
For high-traffic commands, prefer `contract.guidance[]` examples/proof schemas over guesswork.

## Default Task Lifecycle (Unless Prompt Overrides)

1. Use a unique task-scoped namespace via `--agent-id <taskId>` on every command.
2. Start a fresh headless session for that task: `session fresh --browser-mode headless`.
3. Open pages using that same session (`open --session <id> --reuse off --browser-mode headless`).
4. Use only target/session handles created in that task namespace.
5. On completion, tear down only task-owned browser state and processes with `session clear` (same `--agent-id`).

Do not use `--reuse active` or `--isolation shared` unless the prompt explicitly asks for shared continuity.
Do not reuse `--agent-id` across tasks.

## Operating Protocol

1. Keep JSON output on (default). Use `--no-json` only for human-facing summaries.
2. Start with explicit handles: `open` -> persist returned `sessionId` + `targetId`.
3. Run short loops: orient -> act -> verify -> repeat.
4. Default to a fresh task-scoped headless session, not shared/global session state.
5. Use workspace profiles for durable auth: `workspace init`, then `open --profile <name>`.
6. Use `session cookie-copy` for cross-session auth handoff.
7. Treat every non-zero exit as typed failure and branch on `code`, never message text.
8. Keep capture volumes bounded (`--max-*`, `--limit`, `--capture-ms`) for token and runtime control.
9. Use `state reconcile` after restart/crash before deeper debugging.
10. End task runs with owned-teardown (`session clear` in the task `--agent-id`) unless prompt says to keep session/process alive.

## Minimal Agent Loop

```bash
AID="task-$(date +%s)"
SESSION=$(surfwright --agent-id "$AID" session fresh --browser-mode headless | jq -r '.sessionId')
OPEN=$(surfwright --agent-id "$AID" open https://example.com --session "$SESSION" --reuse off --browser-mode headless)
TARGET=$(printf '%s' "$OPEN" | jq -r '.targetId')

surfwright --agent-id "$AID" target snapshot "$TARGET" --mode orient --visible-only
surfwright --agent-id "$AID" target find "$TARGET" --text "Pricing" --first --visible-only --href-host example.com --href-path-prefix /pricing
surfwright --agent-id "$AID" target click "$TARGET" --text "Pricing" --visible-only --delta
surfwright --agent-id "$AID" target read "$TARGET" --selector main --chunk-size 1200 --chunk 1
surfwright --agent-id "$AID" session clear
```

## Handle Discipline

- `open` returns `sessionId`, `sessionSource`, and `targetId`; store all of them.
- `target *` can infer session from `targetId`; pass `--session` only when recovery needs it.
- If handles are lost, recover with `target list --session <id>` and continue from returned `targetId`.

## Reference Map

- Goal-based command recipes: `references/workflows.md`
- Symptom-based debugging runbook: `references/troubleshooting.md`
- Error codes and retry discipline: `references/error-handling.md`
