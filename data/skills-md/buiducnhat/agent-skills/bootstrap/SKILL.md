---
name: bootstrap
description: "Initialize and scaffold a new project with structured requirements gathering. Use when starting a project from scratch, after running a framework initializer (npm init, create-next-app, etc.), or when an existing minimal project needs proper structure, documentation, and conventions. Triggers on: 'bootstrap project', 'start new project', 'scaffold project', 'initialize project', 'setup new project', or when the user wants to go from zero to a well-structured project foundation."
---

# Bootstrap

Collect project requirements through structured dialogue, generate foundational documentation, and scaffold the project structure — then hand off to downstream workflow skills.

## Parameters

- `--scratch`: Start from nothing. Full scaffold: directories, configs, docs, README.
- `--existing`: Project already initialized (e.g., `npm init` done, framework scaffolded). Enhance with docs and structure without overwriting existing files.

## Requirement Categories

Collect information across these 8 dimensions. All categories except **Techstack** and **Product definition** are optional and may fall back to smart defaults.

| #   | Category               | What to collect                                                 |
| --- | ---------------------- | --------------------------------------------------------------- |
| 1   | **Techstack**          | Language, framework, runtime, package manager                   |
| 2   | **Product definition** | Purpose, target users, core features, success criteria          |
| 3   | **Architecture**       | Component structure, data flow, API design, deployment target   |
| 4   | **Roadmap**            | Phases, milestones, MVP scope                                   |
| 5   | **Tooling**            | Linter, formatter, test framework, CI provider                  |
| 6   | **Code standards**     | Naming conventions, file structure patterns, commit conventions |
| 7   | **Design system**      | UI library, styling approach — _frontend projects only_         |
| 8   | **Auth & data**        | Auth method, database, ORM — _if applicable_                    |

## Workflow

### Step 1: Detect Project State

1. Check if a `package.json`, `pyproject.toml`, `Cargo.toml`, or similar manifest exists.
2. Check if a `docs/` directory and documentation files exist.
3. Determine mode:
   - If the user passed `--scratch` or nothing exists → proceed as `--scratch`.
   - If the user passed `--existing` or a project manifest exists → proceed as `--existing`.
4. Announce the detected mode and ask for confirmation before continuing.

### Step 2: Gather Requirements

Ask one question at a time. Use multiple-choice options (2–4 choices) when possible. Pause for full user input only when a question requires detailed explanation.

**Sequence:**

1. **Techstack** (required) — Ask about language/framework first. Offer common options based on context clues.
2. **Product definition** (required) — Ask: what does this project do, who uses it, what are the 2-3 core features?
3. **Architecture** — Ask: what are the main components, is there an API, where will it deploy?
4. **Roadmap** — Ask: what is the MVP scope, are there phases?
5. **Tooling** — Offer defaults from the Smart Defaults table; ask to confirm or override.
6. **Code standards** — Ask about naming conventions, file layout preferences, commit style (Conventional Commits?).
7. **Design system** — _Skip for non-frontend projects._ Ask about UI library and styling approach.
8. **Auth & data** — _Skip if not applicable._ Ask about authentication and database/ORM if the project has these concerns.

**Rules for gathering:**

- If user says "I don't know", "default", or is vague → apply Smart Defaults for the detected stack and confirm.
- Skip categories that are clearly irrelevant (e.g., Design system for a CLI tool, Auth & data for a static site).
- Minimum required: Techstack + Product definition. All others can use defaults.

### Step 3: Confirm Requirements Summary

Present a concise summary of all collected requirements in a structured list. Ask for approval before proceeding:

- `Looks good` / `Confirmed` → proceed to Step 4.
- User provides corrections → update the relevant category and re-present the summary.

### Step 4: Generate Documentation

Create the `docs/` directory if it doesn't exist. Generate all four foundational docs populated with concrete project-specific content — no placeholders.

| File                    | Source categories                            |
| ----------------------- | -------------------------------------------- |
| `docs/project-pdr.md`   | Product definition, Roadmap                  |
| `docs/architecture.md`  | Architecture, Techstack, Auth & data         |
| `docs/codebase.md`      | Generated from actual structure after Step 5 |
| `docs/code-standard.md` | Techstack, Code standards, Tooling           |

Follow the same content requirements as the `docs --init` skill for each file.

For `--existing` mode: read existing docs first. Only add missing sections; do not overwrite content that is already accurate.

### Step 5: Scaffold Project Structure

Create standard directories and essential config files based on the chosen techstack.

**General rules:**

- Create `src/`, `tests/` (or framework equivalent), `public/` for web projects.
- Create config files: `tsconfig.json`, `.eslintrc.json`, `.prettierrc`, `.gitignore`, etc.
- Initialize git (`git init`) if not already a repository.
- For `--existing` mode: only add missing files/directories. Never overwrite files that already exist.

**Common scaffolds:**

- **Next.js**: `src/app/`, `src/components/`, `src/lib/`, `public/`, `tests/`
- **React (Vite)**: `src/components/`, `src/hooks/`, `src/lib/`, `public/`, `tests/`
- **Express/Node**: `src/routes/`, `src/middleware/`, `src/lib/`, `tests/`
- **Python**: `src/<package>/`, `tests/`, `scripts/`
- **CLI (Node)**: `src/commands/`, `src/lib/`, `tests/`

After scaffolding, regenerate `docs/codebase.md` to reflect the actual directory structure.

### Step 6: Initialize Tooling

Install and configure selected tools:

1. Run package manager install: `npm install`, `bun install`, `pnpm install`, `pip install`, etc.
2. Install linter/formatter dev dependencies.
3. Write or update linter config (`biome.json`, `.eslintrc.json`, `ruff.toml`, etc.).
4. Write or update formatter config (`biome.json`, `.prettierrc`, etc.).
5. Add lint/format scripts to `package.json` (or equivalent).
6. If a test framework was selected, install it and create one example test file under `tests/`.

Skip any sub-step where the file already exists (`--existing` mode).

### Step 7: Generate README

Create `README.md` with:

- Project name and one-sentence description
- Tech stack badges or a concise stack list
- Prerequisites
- Quick start (install + run commands)
- Documentation links section pointing to all 4 docs files
- License (if specified)

For `--existing` mode: update README only if it is missing or significantly incomplete.

### Step 8: Handoff

Summarize everything created:

- List all new files/directories created
- List all docs generated
- List all tools configured

Then recommend the next skill based on project readiness:

- If requirements are exploratory or architecture is uncertain → recommend `brainstorm`
- If the plan is clear → recommend `write-plan` to create the first implementation plan
- If there's an immediate small task → recommend `quick-implement`

## Smart Defaults

| Stack           | Package Manager | Linter | Formatter | Test Framework | Styling      |
| --------------- | --------------- | ------ | --------- | -------------- | ------------ |
| Next.js         | bun             | Biome  | Biome     | Vitest         | Tailwind CSS |
| React (Vite)    | bun             | Biome  | Biome     | Vitest         | Tailwind CSS |
| Express/Node    | bun             | Biome  | Biome     | Vitest         | N/A          |
| CLI tool (Node) | bun             | Biome  | Biome     | Vitest         | N/A          |
| Python          | uv              | Ruff   | Ruff      | pytest         | N/A          |
| Rust            | cargo           | clippy | rustfmt   | cargo test     | N/A          |

## Rules

- Never overwrite existing files in `--existing` mode unless the user explicitly approves.
- Do not invent product requirements — always collect them from the user.
- Skip irrelevant categories; don't ask questions that don't apply to the project type.
- Generate documentation with concrete, project-specific content — no generic placeholders.
- Keep `docs/codebase.md` in sync with the actual scaffolded structure.
- If unsure about a decision, apply the smart default and confirm with the user.
- Do not run destructive commands (e.g., `rm -rf`) without explicit user approval.
