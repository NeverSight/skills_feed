---
name: forge-setup-project
description: Set up a project's meta-structure for agentic engineering — CLAUDE.md, AGENTS.md, docs/, README, and CHANGELOG. Use when starting a new project or retrofitting an existing codebase for the forge workflow.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Set Up Project Meta-Structure

Set up a project's meta-structure for agentic engineering — the foundational files that make a codebase navigable and maintainable by both humans and AI agents.

## Input

Optional: A path to the project root: $ARGUMENTS

If no argument is provided, use the current working directory.

## Process

### Step 1: Determine Project State

Scan the project root to classify what exists:

```bash
# Check for existing meta files
ls -la CLAUDE.md AGENTS.md README.md CHANGELOG.md .claude/settings.local.json 2>/dev/null

# Check for docs directory
ls docs/ 2>/dev/null

# Check for any code at all
ls -la
```

**Classify the project into one of four states:**

| State | Description | Behavior |
|-------|-------------|----------|
| **Greenfield** | No code, no meta files | Generate everything from user input |
| **Existing, no meta** | Has code but no CLAUDE.md/docs/ | Explore codebase first, then generate |
| **Partial meta** | Has some meta files (e.g., README exists) | Ask user how to handle each existing file |
| **Full meta** | All meta files already present | Offer to audit and update |

**If existing meta files are found**, use AskUserQuestion to ask:
- Which files to overwrite vs. keep
- Whether to merge content (for README.md especially)

### Step 2: Explore the Codebase

**Skip this step for greenfield projects.**

For existing projects, perform a thorough exploration:

```bash
# Directory structure (top 3 levels)
find . -maxdepth 3 -type f -not -path './.git/*' -not -path './node_modules/*' -not -path './vendor/*' -not -path './.next/*' -not -path './dist/*' -not -path './build/*' | head -100

# Detect language/runtime
ls package.json go.mod Cargo.toml pyproject.toml setup.py Gemfile build.gradle pom.xml mix.exs deno.json bunfig.toml composer.json 2>/dev/null

# Package manager and scripts
cat package.json 2>/dev/null | head -80
cat Makefile 2>/dev/null | head -80
cat Taskfile.yml 2>/dev/null | head -80

# Entry points
ls -la src/ app/ cmd/ lib/ main.* index.* 2>/dev/null

# CI/CD configuration
ls .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile .circleci/config.yml 2>/dev/null

# Lint/format configuration
ls .eslintrc* biome.json .prettierrc* .golangci.yml rustfmt.toml .rubocop.yml pyproject.toml 2>/dev/null

# Test configuration
ls jest.config* vitest.config* pytest.ini .mocharc* 2>/dev/null

# Docker
ls Dockerfile docker-compose*.yml 2>/dev/null

# Existing documentation
ls docs/*.md *.md 2>/dev/null
```

**Record what you discover:**
- Language(s) and runtime
- Package manager
- Available scripts/make targets (build, test, lint, format, dev, etc.)
- Project structure pattern (monorepo, single app, CLI tool, library, etc.)
- Test framework
- CI/CD setup
- Entry points and architecture style

### Step 3: Gather Project Information

Use AskUserQuestion to collect what can't be determined from code:

**Always ask:**
1. **One-line project description** — "What does this project do in one sentence?"
2. **Core principles** — "What are 3-5 rules that should always guide development in this project?" (Offer examples based on what you've seen in the codebase)
3. **Project story** — Suggest a short metaphor or narrative that connects the project name to its purpose (2-3 sentences). This goes in the README header to give the project personality. Look for a metaphor grounded in what the name evokes — a physical object, a place, an action — and connect it to what the software actually does. Propose a suggestion and let the user refine it.

**Ask only if ambiguous from code:**
4. Confirm detected commands if multiple options exist (e.g., `npm` vs `bun`)
5. Confirm project structure if unclear (monorepo vs single app)
6. **External dependencies** — "Does this project depend on external services or APIs? List them with how to verify they're working (e.g., health-check endpoints, test commands)."
7. **Debugging patterns** — "When something breaks, what should be checked first?" (e.g., env/config files, specific log locations, common failure modes)
8. **Preferred libraries** — "Are there preferred libraries or patterns for common tasks that new code should follow?"

**Never ask what's discoverable from code:**
- Language, framework, test runner, linter — detect these automatically
- Available scripts — read package.json/Makefile
- Directory structure — explore it

### Step 4: Generate CLAUDE.md

Create `CLAUDE.md` following this exact structure:

```markdown
# <Project Name>

<one-line description from Step 3>

## Commands

<all discovered commands in a code block — install, dev, build, check, lint, format, typecheck, test, etc.>

## Documentation

| Document | Purpose |
|----------|---------|
| [Architecture](docs/architecture.md) | System design, data flow, package responsibilities |
| [Development](docs/development.md) | Prerequisites, setup, daily workflow |
| [Coding Guidelines](docs/coding-guidelines.md) | Code style, error handling, naming conventions |
| [Testing](docs/testing.md) | Test commands, conventions, patterns |
| [PR Workflow](docs/pr-workflow.md) | Commits, PRs, branch naming, review process |
<additional project-specific docs rows if applicable>

## Core Principles

<3-5 principles from Step 3, as a numbered list>

## Commits

Format: `<type>(<scope>): <description>`

Types: feat, fix, docs, refactor, test, chore, perf

<2-3 example commit messages using actual project scopes>

## External Dependencies

<services, APIs, and tools the project depends on — with verification commands>

## Debugging

<what to check first when things break — project-specific troubleshooting patterns>

## Conventions

<naming patterns, preferred libraries, and project-specific rules beyond commit format>
```

**Optional sections:** Include `## External Dependencies`, `## Debugging`, and `## Conventions` only when the user provides relevant information in Step 3. Do not generate empty sections or invent content.

**Critical rules:**
- Commands block must contain ONLY commands that actually exist in the project
- Every command must be verified against package.json scripts, Makefile targets, or equivalent
- Use `<!-- TODO: verify this command -->` if uncertain about a command
- Core principles must come from user input, not be invented

### Step 5: Create AGENTS.md, .claude/settings.local.json, and .gitignore

```bash
# Create AGENTS.md as a symlink to CLAUDE.md
ln -sf CLAUDE.md AGENTS.md

# Create .claude directory
mkdir -p .claude
```

If `.claude/settings.local.json` already exists, merge the attribution keys into it. If it doesn't exist, create it:

```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

The empty attribution fields suppress Claude Code's default Co-Authored-By lines. This file is user-local and not committed — the "no attribution" rule is also documented in CLAUDE.md for enforcement.

**Create `.gitignore` if it doesn't exist.** If it already exists, ensure `.claude/` is listed.

The `.claude/` directory contains only user-specific settings (`settings.local.json` with tool permissions and attribution) and should not be committed.

```bash
# Check if .gitignore exists
if [ ! -f .gitignore ]; then
  # Create with .claude/ entry
  echo ".claude/" > .gitignore
else
  # Add .claude/ if not already present
  grep -qxF '.claude/' .gitignore || echo '.claude/' >> .gitignore
fi
```

Add other standard entries based on the detected tech stack:
- **Node/Bun**: `node_modules/`, `dist/`, `.env`, `.env.local`
- **Go**: binary name, `vendor/` (if not committed)
- **Python**: `__pycache__/`, `.venv/`, `*.pyc`
- **Rust**: `target/`
- **General**: `.DS_Store`, `*.log`, `coverage/`

**IMPORTANT**: If `.gitignore` already exists, do NOT overwrite it. Only append missing entries.

### Step 6: Generate /docs

Create the `docs/` directory and generate five core documentation files plus any project-specific extras.

```bash
mkdir -p docs
```

**Five core docs (always created):**

#### docs/architecture.md

```markdown
# Architecture

<system design overview — what the project is, how it's structured>

## Project Structure

<directory tree with annotations for key directories>

## Data Flow

<how data moves through the system — request lifecycle, processing pipeline, etc.>

## Package/Module Responsibilities

<table or list of key packages/modules and what they do>

<!-- TODO: Add diagrams if helpful -->
```

#### docs/development.md

```markdown
# Development

## Prerequisites

<runtime, language version, tools needed — detected from project>

## Setup

<step-by-step from clone to running — based on actual project setup>

## Daily Workflow

<common development loop — start dev server, run tests, etc.>

## Available Commands

<full list of all scripts/make targets with descriptions>
```

#### docs/coding-guidelines.md

```markdown
# Coding Guidelines

## Code Style

<detected style rules — formatter, linter config, import ordering, etc.>

## Error Handling

<project's error handling patterns — detected from code or marked TODO>

## Naming Conventions

<file naming, function naming, variable naming patterns detected>

## Documentation

<when to add comments, docstring conventions, etc.>

<!-- TODO: Add examples from the codebase -->
```

#### docs/testing.md

```markdown
# Testing

## Running Tests

<exact test commands from project>

## Test Conventions

<test file location, naming, framework-specific patterns>

## Writing Tests

<patterns detected in existing tests — describe what you see>

## Coverage

<coverage commands if available, coverage expectations>
```

#### docs/pr-workflow.md

```markdown
# PR Workflow

## Commit Conventions

Format: `<type>(<scope>): <description>`

Types: feat, fix, docs, refactor, test, chore, perf

### Examples

<2-3 examples using actual project scopes>

## Branch Naming

Format: `<type>/<issue-number>-<short-kebab-description>`

### Examples

<2-3 examples relevant to the project>

## PR Checklist

- [ ] Code follows project guidelines (see [Coding Guidelines](coding-guidelines.md))
- [ ] Tests added/updated (see [Testing](testing.md))
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated for user-facing changes
- [ ] Lint/format checks pass
- [ ] All tests pass

## Review Process

<project-specific review norms, or standard forge workflow>
```

**Additional project-specific docs — offer based on detection:**

| Detected Signal | Suggested Doc |
|-----------------|---------------|
| REST/GraphQL routes, OpenAPI spec | `docs/api-reference.md` |
| Dockerfile, docker-compose | `docs/deployment.md` |
| CI workflow files | `docs/ci.md` |
| Auth middleware, security headers | `docs/security.md` |
| React/Vue/Svelte components | `docs/frontend.md` |
| Database migrations, ORM config | `docs/database.md` |
| Multiple packages/workspaces | `docs/monorepo.md` |

Use AskUserQuestion to offer detected extras:
```
Based on what I found in the codebase, I'd also suggest creating:
- docs/api-reference.md (detected REST routes in src/routes/)
- docs/deployment.md (detected Dockerfile and docker-compose.yml)

Which of these would you like me to create?
```

**Content rules for all docs:**
- Every sentence must be specific to THIS project — no generic filler
- Use `<!-- TODO: ... -->` for anything that can't be determined from code
- Reference actual file paths, actual commands, actual patterns found in the codebase
- Keep each doc focused — if it's getting long, you're adding too much

### Step 7: Generate README.md

**If no README.md exists**, create one following this structure:

```markdown
<p align="center">
  <strong><one-line project description></strong><br>
  <short tagline — a punchy subtitle that complements the description>
</p>

<p align="center">
  <a href="docs/architecture.md">Architecture</a> &middot;
  <a href="docs/development.md">Development</a> &middot;
  <a href="docs/coding-guidelines.md">Guidelines</a> &middot;
  <a href="docs/testing.md">Testing</a> &middot;
  <a href="docs/pr-workflow.md">PR Workflow</a>
</p>

---

<project story from Step 3 — the metaphor connecting the name to the purpose>

---

## Quick Start

<minimal steps to get running — clone, install, start>

## Features

<bullet list of key features — derived from codebase exploration>

## Development

<essential dev commands — install, dev, test, lint>

See [Development Guide](docs/development.md) for full setup instructions.

## Documentation

| Document | Purpose |
|----------|---------|
| [Architecture](docs/architecture.md) | System design and data flow |
| [Development](docs/development.md) | Setup and daily workflow |
| [Coding Guidelines](docs/coding-guidelines.md) | Code style and conventions |
| [Testing](docs/testing.md) | Test commands and patterns |
| [PR Workflow](docs/pr-workflow.md) | Commits, PRs, and review process |

## Contributing

1. Create an issue: `/forge-create-issue`
2. Implement: `/forge-implement-issue <number>`
3. Self-review: `/forge-reflect-pr`
4. Address feedback: `/forge-address-pr-feedback`
5. Update changelog: `/forge-update-changelog`
```

**Header rules:**
- If the project has a logo (`assets/logo.svg` or similar), add a centered `<img>` above the tagline
- The story paragraph goes between two `---` dividers, right after the nav links
- Keep the story to 2-3 sentences — evocative, not verbose

**If README.md already exists**, use AskUserQuestion:
```
A README.md already exists. How would you like to proceed?
1. Replace it entirely with the new structure
2. Merge — keep existing content and add missing sections
3. Keep the existing README.md unchanged
```

### Step 8: Generate CHANGELOG.md

**If no CHANGELOG.md exists**, create one with header only:

```markdown
# Changelog

All notable user-facing changes to this project will be documented in this file.

Changes are grouped by release date and category. Only user-facing changes are included — internal refactors, test updates, and CI changes are omitted.
```

**If the project has existing git history**, use AskUserQuestion:
```
This project has existing git history. Would you like me to backfill the changelog from recent commits?
1. Yes — scan recent commits and create initial entries
2. No — start fresh from this point forward
```

If backfilling, follow the `forge-update-changelog` conventions (user-facing, plain language, no jargon).

### Step 9: Commit

Stage all new and modified meta files and commit:

```bash
# Stage only the meta files we created/modified
git add CLAUDE.md AGENTS.md .gitignore docs/ README.md CHANGELOG.md

# Commit with conventional format
git commit -m "docs: add agentic engineering meta-structure"
```

**Do NOT commit if:**
- The user asked for a dry run
- There are unrelated staged changes (unstage them first)
- Any generated file has unresolved questions (ask user first)

### Step 10: Summary

Present a summary of everything that was created:

```text
## Setup Complete

### Files Created
- CLAUDE.md — Project guide with commands, docs table, principles, commit conventions
- AGENTS.md — Symlink → CLAUDE.md
- .claude/settings.local.json — Attribution settings (user-local, not committed)
- .gitignore — Git ignore rules (includes .claude/)
- docs/architecture.md — System design and structure
- docs/development.md — Prerequisites, setup, workflow
- docs/coding-guidelines.md — Code style and conventions
- docs/testing.md — Test commands and patterns
- docs/pr-workflow.md — Commit, PR, and review conventions
<any additional docs created>
- README.md — Project overview and quick start
- CHANGELOG.md — Ready for entries

### Next Steps
1. Review each generated file and fill in any <!-- TODO --> markers
2. Use /forge-create-issue to plan your first piece of work
3. Use /forge-implement-issue to start implementing
```

## Important Guidelines

### Content Quality

- **No generic boilerplate**: Every sentence must be specific to the project. "This project uses React" is specific. "Follow best practices" is not.
- **Placeholders over fiction**: If you can't determine something from the code, use `<!-- TODO: describe X -->` rather than making something up.
- **Derived from exploration**: Commands, structure, patterns — all must come from actual codebase analysis, not assumptions.

### What NOT to Do

- Don't generate docs for a tech stack you didn't detect
- Don't invent project principles — ask the user
- Don't include attribution lines (Co-Authored-By, etc.) in any commits
- Don't include time estimates anywhere
- Don't add commands to CLAUDE.md that don't exist in the project
- Don't create AGENTS.md as a regular file — it must be a symlink
- Don't generate content that contradicts existing project configuration

### Handling Edge Cases

- **Monorepo**: Create root-level meta files that reference sub-packages. Suggest per-package CLAUDE.md files as a follow-up.
- **No tests yet**: Create `docs/testing.md` with `<!-- TODO -->` markers and recommend setting up a test framework.
- **No CI yet**: Skip `docs/ci.md` but mention it as a follow-up in the summary.
- **Multiple languages**: Document all detected languages in CLAUDE.md commands section, grouped by language.

## Related Skills

**Next step:** Use `forge-create-issue` to plan your first piece of work.
**Full workflow:** `forge-setup-project` → `forge-create-issue` → `forge-implement-issue` → `forge-reflect-pr` → `forge-address-pr-feedback` → `forge-update-changelog`

## Example Usage

```
/forge-setup-project
/forge-setup-project /path/to/project
```
