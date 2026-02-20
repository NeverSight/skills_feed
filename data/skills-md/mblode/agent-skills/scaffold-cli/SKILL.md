---
name: scaffold-cli
description: Scaffolds a production-ready TypeScript CLI project with ESM, tsdown, vitest, biome, changesets, GitHub Actions, and an agent skill definition. Use when creating a new CLI tool, bootstrapping a TypeScript project, scaffolding a node CLI, starting a new npm package, or asking "scaffold a CLI project."
---

# Scaffold CLI

Scaffold a production-ready TypeScript CLI project (Node 22+) with ESM modules, dual-build (CLI + library), automated releases, and an agent skill definition.

## Reference Files

| File | Read When |
|------|-----------|
| `references/scaffold-configs.md` | Default: templates for package.json, tsconfig, tsdown, biome, gitignore, license, changeset config, GitHub Actions |
| `references/scaffold-source.md` | Default: templates for src/cli.ts, src/index.ts, src/types.ts, AGENTS.md, README.md, skills/SKILL.md |
| `references/post-scaffold.md` | After generating files: post-scaffold commands and validation checklist |

## Scaffold Workflow

Copy this checklist to track progress:

```text
Scaffold progress:
- [ ] Step 1: Gather project info
- [ ] Step 2: Create directory structure
- [ ] Step 3: Generate config files
- [ ] Step 4: Generate source files
- [ ] Step 5: Generate docs and skill
- [ ] Step 6: Run post-scaffold commands
- [ ] Step 7: Validate scaffold
```

### Step 1: Gather project info

Collect from the user (ask only what was not provided):

| Variable | Example | Default | Used in |
|----------|---------|---------|---------|
| `{{name}}` | `md-tools` | — (required) | package.json name, README title |
| `{{description}}` | `CLI tool to convert content to markdown` | — (required) | package.json, README, SKILL.md |
| `{{bin}}` | `md` | same as `{{name}}` | package.json bin field, CLI examples |
| `{{repo}}` | `acme/md-tools` | — (required) | package.json repository, badges |
| `{{author}}` | `Your Name` | — (required) | package.json, LICENSE |
| `{{year}}` | `2026` | current year | LICENSE |

### Step 2: Create directory structure

```
{{name}}/
  .changeset/
  .github/
    workflows/
  src/
  skills/{{bin}}/
```

### Step 3: Generate config files

Load `references/scaffold-configs.md`. Generate all config files, replacing every `{{placeholder}}` with actual values.

Files: `package.json`, `tsconfig.json`, `tsdown.config.ts`, `biome.jsonc`, `.gitignore`, `LICENSE.md`, `.changeset/config.json`, `.changeset/README.md`, `.github/workflows/ci.yml`, `.github/workflows/npm-publish.yml`

### Step 4: Generate source files

Load `references/scaffold-source.md`. Generate:
- `src/cli.ts` — Commander entry point
- `src/index.ts` — Public API exports
- `src/types.ts` — Shared type definitions

### Step 5: Generate docs and skill

Load `references/scaffold-source.md`. Generate:
- `AGENTS.md` — Commands, architecture, gotchas
- `README.md` — Badges, features, install, usage, API, license
- `skills/{{bin}}/SKILL.md` — Agent skill definition

Then create symlink: `ln -s AGENTS.md CLAUDE.md`

### Step 6: Run post-scaffold commands

Load `references/post-scaffold.md`. Run the full command sequence in order.

### Step 7: Validate scaffold

Load `references/post-scaffold.md`. Run all validation checks and confirm every item passes.

## Placeholder Reference

All templates use `{{variable}}` syntax. Do a final sweep to catch any missed placeholders before writing files.

| Placeholder | Source |
|-------------|--------|
| `{{name}}` | Project name (kebab-case) |
| `{{description}}` | One-line project description |
| `{{bin}}` | CLI binary name |
| `{{repo}}` | GitHub owner/repo |
| `{{author}}` | Author name |
| `{{year}}` | Current year |

## Dependencies

**Runtime:**
`@clack/prompts`, `commander`, `gray-matter`

**Development:**
`@biomejs/biome`, `@changesets/cli`, `@types/node`, `tsdown`, `typescript`, `ultracite`, `vitest`

**Built-in (no install needed):**
`node:util` styleText for colors (replaces chalk), `@clack/prompts` spinner for progress (replaces ora)

## Anti-patterns

- Do not use CommonJS — all output must be ESM with `"type": "module"`
- Do not skip AGENTS.md or `skills/` directory — every CLI project needs agent instructions
- Do not create test files in the scaffold — let the user add tests for their specific features
- Do not merge the dual tsdown builds — CLI (with shebang) and library (with dts) must stay separate
- Do not call biome directly — always use `ultracite fix` or `ultracite check`
- Do not configure git hooks manually — ultracite sets up husky and lint-staged automatically
- Do not add chalk or ora — use `node:util` styleText for colors and `@clack/prompts` spinner
