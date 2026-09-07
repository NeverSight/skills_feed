---
name: website-automation-builder
description: Build, repair or extend portable website skills with registered TypeScript/POM actions, compact observation and a fixed local CLI using playwright-cli in the user's already-open browser.
---

# Website Automation Builder

Produce one independent `<site>-automation` skill. Its only agent requirements are reading SKILL.md, using local files and starting a process. No harness tools, MCP, plugins or special agent permissions.

Runtime: intent → known action/observation → fixed CLI → precompiled POM code → playwright-cli → user's existing browser → bounded JSON.

## Modes

- **Runtime:** registered domain actions and global observation. No raw commands, selectors, arbitrary code, free clicks or new automation.
- **Diagnostic:** observation only, with bounded accessibility excerpts and locator counts. No mutation.
- **Builder/Repair:** direct playwright-cli exploration, locator development and tested action changes. Only enter for an explicit build, repair or extension task.

Never launch, replace, restart or close the user's browser. Extension attach to Chrome with one fixed site session is the default; explicit CDP configuration is the only alternative. Never bypass login, MFA, CAPTCHA or bot protection.

## Workflow

Follow PRECHECK → INPUT → DISCOVER → BUILD → VERIFY → HANDOFF. Maintain `references/build-state.json`; block only affected actions.

1. PRECHECK: run `node "<BUILDER_ROOT>/scripts/preflight.mjs"`. Inventory is not proof of attach. If unavailable, continue browser-free work and record the precise live-test boundary.
2. INPUT/DISCOVER: read [intake-and-discovery](references/intake-and-discovery.md). Ask immediately about ambiguous routes, prerequisites, risky writes or unclear controls; ask no later than two targeted failed navigation attempts.
3. BUILD: read [runtime-contract](references/runtime-contract.md), [pom-and-selectors](references/pom-and-selectors.md), [observation-contract](references/observation-contract.md) and [generated-skill-contract](references/generated-skill-contract.md). For writes also read [write-safety](references/write-safety.md).
   `node "<BUILDER_ROOT>/scripts/scaffold.mjs" --name <site>-automation --url https://example.org --out <target>/<site>-automation`
   Implement observed POMs, actions and evidence; run `npm install` and `npm run build` in the generated directory. Compilation belongs here, never in normal Runtime.
4. VERIFY: read [verification](references/verification.md). Run `npm run verify`; test safe reads in the attached browser and only authorized writes. Fixture and live evidence must remain distinguishable.
5. HANDOFF: deliver SKILL.md, compiled CLI and runtime, maintained TypeScript sources, references, tests and lockfile. Report ready only after validation, with concrete limitations for untested live behavior.

For a reproducible local demo, scaffold with `--demo`. Builder regression suite: `node scripts/test-scaffold.mjs`; full generated-demo verification: `node scripts/test-demo.mjs`.

Do not distribute .local, node_modules, browser profiles, cookies, credentials, snapshots, personal test data or traces. Read [sources](references/sources.md) when changing version-sensitive CLI behavior.
