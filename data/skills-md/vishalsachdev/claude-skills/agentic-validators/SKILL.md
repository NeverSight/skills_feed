---
name: agentic-validators
description: Design and install validation hooks for coding agents (e.g., Claude Code) to make AI changes safer and more deterministic. Use when you want post-tool-use or stop hooks, automated tests/linters/formatters, parallel subagents with per-file validation, or a repeatable “agent pipeline” with audit logs.
license: MIT
metadata:
  author: Vishal Sachdev + Pip
  version: "0.1.0"
  tags: "agents hooks validation testing linting formatting ci"
compatibility: Works in repos on macOS/Linux with bash. Assumes a CLI coding agent that supports hooks (Claude Code-style) and common tooling (git, ripgrep, node/python toolchains).
---

# Agentic Validators

## Goal
Turn “agent wrote code” into “agent wrote code **and** the change is validated automatically.”

This skill helps you:
- choose the right validation strategy (per-file vs repo-wide)
- implement **post-tool-use** and **stop** hooks
- create **narrow validators** (fast, deterministic checks)
- structure work so multiple agents can run in parallel without losing correctness

## Mental model
- **Agents are non-deterministic; validators are deterministic.**
- **Context is fragile; validation + logs are durable.**
- Prefer **small, fast checks close to the change** (per-file) + a final **global gate** (repo-wide).

## When to use which hook
### Post-tool-use hook (best default)
Use when:
- you want immediate feedback after edits
- you can validate the specific file(s) that were touched
- you want high signal without running the full test suite

Typical checks:
- formatting (prettier/black)
- linting (eslint/ruff)
- typecheck for that file/module (tsc --noEmit with project config)

### Stop hook (end-of-run gate)
Use when:
- you need repo-wide invariants
- you want one last “exit criteria” check

Typical checks:
- unit tests
- build
- integration tests

## Step-by-step: add validators to a repo
1) Identify file types and fast checks
   - JS/TS: prettier + eslint + typecheck
   - Python: ruff + pytest (optional)
   - Go: gofmt + go test (optional)

2) Implement per-file validator(s)
   - A validator should be:
     - fast (<5–30s)
     - deterministic
     - clear output
     - safe to run repeatedly

3) Wire into hooks
   - Implement post-tool-use hook calling validator with the file path.

4) Add logs
   - Write to a predictable location (e.g., .agent-logs/validators.log)

5) Add a stop-hook “final gate”
   - Run the broader checks once.

## Example validator patterns
### Pattern A: “format + lint” for a touched file
- Format file
- Lint file
- If any change was made by formatter, fail and ask agent to re-run with formatter changes committed

### Pattern B: “contract test”
- For touched module, run a focused unit test subset

### Pattern C: “readme/docs invariant”
- If docs changed, run markdown lint + link checker

## Parallelism pattern
If you have many similar files (CSV, configs, docs):
- spawn one subagent per file
- each subagent runs its own post-tool-use validator
- aggregator agent only accepts results where validators passed

## Common failure modes & fixes
- **Validator too slow** → split into fast per-file checks + slower stop hook.
- **Validator flaky** → remove network calls, pin versions, add retries only where safe.
- **Agent ignores tool docs** → write a short “constitution” section and point to reference files.

## References
- See [Hook recipes](references/HOOK_RECIPES.md)
- See [Validator design checklist](references/VALIDATOR_CHECKLIST.md)
