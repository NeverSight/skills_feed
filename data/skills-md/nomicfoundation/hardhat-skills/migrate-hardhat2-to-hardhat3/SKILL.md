---
name: migrate-hardhat2-to-hardhat3
description: Systematically migrate a Hardhat V2 project to Hardhat V3, covering core changes (ESM, declarative config, hooks system, network connections) and the full plugin ecosystem (hardhat-deploy, hardhat-verify, @openzeppelin/hardhat-upgrades, and others), coverage tools, and test migration. Use when upgrading any production Hardhat V2 repository to V3.
---

This skill runs the full V2→V3 migration as **six sequential phases**. **A single agent running them top-to-bottom is the default** — it handles small and medium projects (and large ones up to ~150 `.ts` test files on a 1M-token context window). Beyond that, or on a smaller-context harness (~200k tokens) past a trivial project, fan the file-heavy phases (4 and 5) out to sub-agents so a single context doesn't overflow mid-migration (see "Optional: sub-agent fan-out" in [references/migration-conventions.md](references/migration-conventions.md)).

## Before you start

1. **Read [references/migration-conventions.md](references/migration-conventions.md)** — the rules every phase depends on (no VCS commands, package-manager detection, scoping, gates, change presentation, and the optional parallel-execution model). Don't proceed until you have.
2. **Detect the package manager** (lockfile check) and remember it for the whole migration.
3. **Choose the execution mode.** Estimate your context window and the project size (count `.ts` test files) and pick single-agent (the default) vs. sub-agent fan-out using the thresholds in the conventions doc. If you can't tell which window you're on, assume the smaller one. Most projects stay single-agent.
4. **Phases are strictly sequential** — each depends on the previous one's output. After every phase, stop at a **user checkpoint** and wait for approval before continuing. Present the checkpoint in this order:
   - **Step done** — the title of the phase just completed (e.g. *Phase 1 — Project Setup*) and its changes: list the changed files and surface any unexpected ones verbatim (see core rule 5 in the conventions doc).
   - **Suggested commit message** — the checkpoint commit for the completed phase.
   - **Next step** — the title of the phase coming next (e.g. *Phase 2 — Config*) and a one-line description of what it will do, or "the migration is complete" after Phase 6.

## Phases

Run each phase by following its phase guide. Each ends with a gate; the checklist below is your confirmation that the phase is truly done before moving on.

### Phase 1 — Project Setup → [phase guide](references/phase-1-project-setup/phase.md)
Creates `.env` from templates, updates `tsconfig.json` for ESM, converts `package.json` (ESM flag, V2→V3 dependency swap, scripts).

- [ ] Phase reported all gates passed
- [ ] `npx hardhat --version` runs and prints a `3.x` version (e.g. `3.9.0`)
- [ ] Checkpoint commit: `[CHECK] HH3 project setup: env, tsconfig, package.json`

### Phase 2 — Config → [phase guide](references/phase-2-config/phase.md)
Rewrites `hardhat.config.ts` to V3 declarative `defineConfig` (plugins, networks, custom tasks, solidity, verify, test settings).

- [ ] Phase reported all gates passed
- [ ] Checkpoint commit: `[CHECK] HH3 config: declarative defineConfig (solidity, networks, plugins, tasks, verify)`

### Phase 3 — Solidity Tests → [phase guide](references/phase-3-solidity-tests/phase.md)
Migrates `.t.sol` test files to V3 conventions. May need `config` changes (e.g. `paths.tests.solidity` to relocate Solidity test files, or `paths.sources.solidity` if test contracts must be compiled as sources).

- [ ] `npx hardhat test solidity` passes with zero errors (or skipped — no Solidity tests)
- [ ] Checkpoint commit: `[CHECK] HH3 solidity test migration`

### Phase 4 — Source Files → [phase guide](references/phase-4-source-files/phase.md)
Converts all `.ts` (and any CommonJS `.js`) source files CJS→ESM and updates V2 API calls to V3 (+ TypeChain import fixes).

- [ ] Phase reported all gates passed
- [ ] `npx tsc --noEmit` passes with zero errors
- [ ] `npx hardhat test solidity` still passes (regression check — source changes can break Solidity tests)
- [ ] Checkpoint commit: `[CHECK] HH3 source file migration: ESM conversion, V3 API updates, and TypeChain import fixes`

### Phase 5 — Test Fix-Up → [phase guide](references/phase-5-test-fixup/phase.md)
Gets the `.ts` test suite passing under V3.

- [ ] `npx tsc --noEmit` still passes with zero errors
- [ ] Every test file passes individually (`npx hardhat test {file}`)
- [ ] `npx hardhat test solidity` still passes (regression check — test-helper/config fixes can break Solidity tests)
- [ ] Checkpoint commit: `[CHECK] HH3 test suite fix-up: all tests passing under V3`

### Phase 6 — Script Validation → [phase guide](references/phase-6-validate-scripts/phase.md)
Interactive: the user picks `package.json` scripts to validate; the skill runs and fixes them one at a time.

- [ ] Phase reported all gates passed
- [ ] `npx tsc --noEmit` still passes with zero errors
- [ ] Checkpoint commit: `[CHECK] HH3 script validation: all package.json scripts passing`

## Done

Stop and tell the user the migration is complete.
