---
name: work-with-justfiles
description: Guidance for structuring and organizing justfiles. Use when creating, editing, or discussing justfile organization, command grouping, or repo CLI conventions.
---

<objective>
Justfiles capture the common commands of a repository in one place. This skill provides principles for organizing justfiles effectively - preventing scope creep, documenting workflows, and creating clear command aliases that work consistently.

The goal is a single source of truth for "how do I do X in this repo" that anyone can read and understand.
</objective>

<quick_start>
<core_rule>
**Justfiles always run from the repo root.** Never `cd` in recipes. Use absolute paths or paths relative to the justfile location.
</core_rule>

<basic_structure>
```just
# Group: Development
dev:
    npm run dev

# Group: Testing
test:
    npm test

test-watch:
    npm test -- --watch
```
</basic_structure>
</quick_start>

<essential_principles>
<principle name="root_execution">
**Always run from root, never cd**

Justfiles execute from the repository root. This is a feature, not a limitation:
- Predictable behavior regardless of where you invoke `just`
- Paths in recipes are always relative to repo root
- No confusion about "where am I running this from"

```just
# Good - explicit path from root
build:
    cd packages/app && npm run build

# Bad - assumes current directory
build:
    npm run build
```

If a command needs to run in a subdirectory, use `cd dir &&` prefix explicitly.
</principle>

<principle name="command_aliasing">
**Capture every common command as an alias**

The justfile should be the single source of truth for repo commands. If someone asks "how do I run tests?" or "how do I deploy?", the answer is in the justfile.

```just
# Instead of remembering: npm run test:unit -- --coverage --reporter=html
test-coverage:
    npm run test:unit -- --coverage --reporter=html

# Instead of remembering: docker compose -f docker-compose.dev.yml up -d
dev-services:
    docker compose -f docker-compose.dev.yml up -d
```

**Benefits:**
- No tribal knowledge ("oh you need to pass --reporter=html")
- Commands are documented by their existence
- Easy to discover: `just --list`
</principle>

<principle name="group_by_purpose">
**Organize commands into logical groups**

Use comments to create visual groupings. Let the groups emerge from your actual commands:

```just
# ─────────────────────────────────────────────────────────────
# Development
# ─────────────────────────────────────────────────────────────

dev:
    npm run dev

# ─────────────────────────────────────────────────────────────
# Testing
# ─────────────────────────────────────────────────────────────

test:
    npm test

test-watch:
    npm test -- --watch
```

**Common groupings** (adapt to your project):
- Setup / Installation
- Development
- Testing
- Building
- Deployment
- Database / Migrations
- Utilities / Helpers
</principle>

<principle name="prevent_scope_creep">
**One place for CLI commands, not everything**

Justfiles replace scattered shell commands and npm scripts for common operations. They don't replace:
- Build tool configuration (webpack, vite, etc.)
- CI/CD pipeline definitions
- Complex scripting (use actual scripts in `scripts/`)

**Rule of thumb:** If a recipe is longer than 5-10 lines, extract it to a script file and call that from the justfile:

```just
# Good - justfile calls the script
deploy:
    ./scripts/deploy.sh

# Avoid - complex logic inline
deploy:
    if [ "$ENV" = "prod" ]; then
        # ... 20 lines of logic
    fi
```
</principle>

<principle name="document_workflows">
**Make common workflows discoverable**

Use recipe names that describe the workflow, not the tool:

```just
# Good - describes what you're doing
setup:
    npm install
    cp .env.example .env
    just db-migrate

# Less good - just wraps the tool
npm-install:
    npm install
```

Chain related commands with dependencies:

```just
# Running `just deploy` runs lint, test, build first
deploy: lint test build
    ./scripts/deploy.sh
```
</principle>
</essential_principles>

<patterns>
<pattern name="default_recipe">
**Set a sensible default**

The first recipe (or one named `default`) runs when you type just `just`:

```just
# Show available commands by default
default:
    @just --list

# Or start development by default
default:
    just dev
```
</pattern>

<pattern name="arguments">
**Accept arguments for flexibility**

```just
# Positional argument
test file:
    npm test {{file}}

# With default value
build env="dev":
    npm run build -- --env={{env}}

# Variadic arguments
run *args:
    npm run {{args}}
```
</pattern>

<pattern name="environment_variables">
**Use environment variables**

```just
# From .env file
set dotenv-load

# Inline variable
db_name := "myapp_dev"

# Recipe-local export
migrate:
    export DATABASE_URL=$DATABASE_URL && npm run migrate
```
</pattern>

<pattern name="confirmation">
**Require confirmation for dangerous operations**

```just
[confirm("Are you sure you want to reset the database?")]
db-reset:
    dropdb myapp && createdb myapp && just db-migrate
```
</pattern>

<pattern name="private_recipes">
**Hide helper recipes**

Prefix with `_` to hide from `just --list`:

```just
# Public - shows in list
build: _check-deps
    npm run build

# Private - hidden helper
_check-deps:
    @command -v node >/dev/null || (echo "Node required" && exit 1)
```
</pattern>

<pattern name="documentation">
**Add descriptions for complex recipes**

```just
# Deploy to production (requires VPN connection)
[doc("Deploy the application to production environment")]
deploy-prod:
    ./scripts/deploy.sh prod
```
</pattern>
</patterns>

<anti_patterns>
<pitfall name="cd_in_recipes">
**Avoid changing directory implicitly**

```just
# Bad - unclear where this runs
build:
    cd src
    npm run build

# Good - explicit and stays in root
build:
    cd src && npm run build
```
</pitfall>

<pitfall name="duplicating_npm_scripts">
**Don't just wrap every npm script**

If `npm run dev` is obvious and memorable, you don't need `just dev` unless it adds value (like running setup first).

Add justfile recipes when:
- The command has flags that are hard to remember
- Multiple commands need to run together
- The command needs environment setup
</pitfall>

<pitfall name="tool_sprawl">
**Consolidate CLI tools**

Before: Developers need to know npm, docker-compose, aws, terraform, kubectl...

After: `just --list` shows everything, actual tools are implementation details.

```just
# These hide complexity behind simple names
deploy:
    terraform apply -auto-approve

db-shell:
    kubectl exec -it postgres-0 -- psql
```
</pitfall>
</anti_patterns>

<success_criteria>
A well-organized justfile:

- Runs all commands from repo root (no implicit cd)
- Has logical groupings with clear visual separation
- Captures common commands as aliases (single source of truth)
- Uses descriptive recipe names (workflow-focused, not tool-focused)
- Keeps recipes short (complex logic in scripts/)
- Has a sensible default recipe
- Is discoverable via `just --list`
</success_criteria>
