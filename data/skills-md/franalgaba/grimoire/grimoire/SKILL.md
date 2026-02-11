---
name: grimoire
description: Install and operate Grimoire, author .spell files with full syntax coverage (including advisory decision logic), and run compile/validate/simulate/cast safely. Use when users ask to create, edit, debug, validate, simulate, execute, or explain Grimoire strategies.
compatibility: "Requires one of: global grimoire CLI, npx access to @grimoirelabs/cli, or repo-local Bun execution."
metadata:
  version: "2.2"
  focus: "installation usage syntax advisory execution"
---

# Grimoire CLI Skill

This skill is the base operating playbook for Grimoire.

## When To Use

Use this skill when the task includes:

- install/setup of Grimoire tooling
- creating or editing `.spell` files
- syntax questions about DSL capability
- advisory (`advise`) authoring, debugging, and replay workflows
- compile/validate/simulate/cast workflows
- debugging spell compile/runtime failures

## Mandatory Loading Rules

These rules are required and solve syntax coverage gaps.

1. For any `.spell` authoring/editing task:
   - first read `references/syntax-capabilities.md`
   - then read `references/authoring-workflow.md`
2. For CLI flag details:
   - read `references/cli-quick-reference.md`
3. For any advisory task (`advise`, `advisors`, replay):
   - read `docs/how-to/use-advisory-decisions.md`
   - read `docs/explanation/advisory-decision-flow.md`
4. Do not rely on memory for DSL syntax when authoring; use the references above.
5. For local fork preview workflows:
   - read `docs/how-to/simulate-on-anvil-fork.md`
6. For wallet setup and execution key flows:
   - read `docs/how-to/use-wallet-commands-end-to-end.md`

## Installation Resolution

Select the first working invocation and reuse it for the session.

1. Global:
   - `npm i -g @grimoirelabs/cli`
   - command prefix: `grimoire`
2. No-install:
   - command prefix: `npx -y @grimoirelabs/cli`
3. Repo-local:
   - command prefix: `bun run packages/cli/src/index.ts`

If one path fails, move to the next path automatically.

## Fast Start (Immediate Success Path)

Use this sequence before writing custom spells:

1. `<grimoire-cmd> --help`
2. `<grimoire-cmd> validate spells/compute-only.spell`
3. `<grimoire-cmd> simulate spells/compute-only.spell --chain 1`

If all three pass, proceed to spell authoring.

## Authoring and Execution Policy

1. Read syntax references first (mandatory rule above).
2. Author/update spell.
3. Run `validate` (use `--strict` for advisory-heavy spells).
4. Fix errors/warnings and re-run until validation passes.
5. Run `simulate`.
6. For advisory steps intended for deterministic execution, record and then use `--advisory-replay <runId>` in dry-run/live cast.
7. If spell includes irreversible actions, require `cast --dry-run` before any live cast.
8. Ask for explicit user confirmation before live value-moving `cast`.

## Command Surface (Core)

- `init`
- `compile`
- `compile-all`
- `validate`
- `simulate`
- `cast`
- `venues`
- `venue`
- `history`
- `log`
- `wallet` (`generate`, `address`, `balance`, `import`, `wrap`, `unwrap`)

Use `references/cli-quick-reference.md` for concise command signatures and safety-critical flags.

## Runtime Behavior Model

- One runtime semantics: preview first, commit only for execute paths.
- `simulate` and `cast --dry-run` are preview-only flows.
- Live `cast` can commit irreversible actions when policy and runtime checks pass.

## Advisory Operating Rules

- Advisory must be explicit statement form: `x = advise advisor: "prompt" { ... }`.
- Treat advisory outputs as typed contracts; enforce schema with `output`.
- Require `timeout` and `fallback` in every advisory block.
- Prefer `validate --strict` when advisory logic gates value-moving actions.
- Use replay for determinism when moving from preview/dry-run to live execution.

## Venue Metadata and Snapshots

Use venue skills for snapshot parameters and market metadata:

- `grimoire-aave`
- `grimoire-uniswap`
- `grimoire-morpho-blue`
- `grimoire-hyperliquid`

## References

- `references/syntax-capabilities.md`
- `references/authoring-workflow.md`
- `references/cli-quick-reference.md`
- `docs/how-to/simulate-on-anvil-fork.md`
- `docs/how-to/use-wallet-commands-end-to-end.md`
- `docs/how-to/use-advisory-decisions.md`
- `docs/explanation/advisory-decision-flow.md`
- `docs/reference/cli.md`
- `docs/reference/spell-syntax.md`
- `docs/reference/grimoire-dsl-spec.md`
- `docs/reference/compiler-runtime.md`
