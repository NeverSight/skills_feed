---
name: bun-adhoc-validate
description: Run quick, ad-hoc validation or test checks using Bun by writing a temporary TypeScript script in the repo that imports local code, iterating on the script and rerunning until validated (including confirming a failure), then deleting the script. Use when immediate validation is needed to confirm assumptions, inspect remote state, or prototype small checks without adding permanent files or tests.
---

# Bun Adhoc Validate

## Workflow

- Write a short, single-purpose TypeScript script in the repo (e.g., `./tmp/validate-*.ts`) that imports local utilities or clients.
- Keep it minimal: parse args inline if needed, log key outputs, and exit with a non-zero code on failure.
- Run it with `bun` from the repo root (prefer `bun run <path>`).
- Iterate: edit the script and rerun until you validate the assumption or confirm it doesn't work.
- Summarize the results, then delete the temporary script and any temporary artifacts.

## Guidelines

- Prefer local imports over re-implementing logic.
- Avoid committing the temp script; delete it in the same flow.
- If the script needs secrets or env vars, reuse existing project conventions.
- If the check should become permanent, propose a real test after validation.