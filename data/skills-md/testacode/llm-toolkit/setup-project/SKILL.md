---
name: setup-project
description: Configura proyectos con scripts de check y detecta CLIs. Usa cuando el usuario diga "configurar proyecto", "setup", "inicializar proyecto", "agregar npm run check", "qué CLIs tengo", o empiece a trabajar en un proyecto nuevo.
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Setup Project

Skill for auto-configuring new projects with standardized scripts and detecting available CLI tools.

## When to Use

- Starting work on a new project
- User asks to "setup", "configurar", or "initialize" a project
- User wants to check available CLI tools
- User wants to add a "check" script to package.json

## Workflow

### Phase 1: Detect Project Type

Check for project indicators:

```bash
# Check for Node/Bun project
ls package.json 2>/dev/null && echo "Node/Bun project detected"

# Check for Python project
ls pyproject.toml 2>/dev/null && echo "Python project (pyproject.toml)"
ls requirements.txt 2>/dev/null && echo "Python project (requirements.txt)"
```

| File Found | Project Type |
|------------|--------------|
| `package.json` | Node.js / Bun |
| `pyproject.toml` | Python (modern) |
| `requirements.txt` | Python (legacy) |
| None of above | Other (inform user) |

If no project type detected, inform the user:
> "No package.json, pyproject.toml, or requirements.txt found. This skill currently supports Node.js and Python projects."

### Phase 2: Add Check Script (Node.js only)

For Node.js projects, read `package.json` and analyze existing scripts:

```bash
cat package.json | grep -A 50 '"scripts"'
```

**Build the check script based on available scripts:**

| Script Exists | Include in check |
|---------------|------------------|
| `lint` | `npm run lint` |
| `typecheck` | `npm run typecheck` |
| `test` | `npm run test` |
| `build` | `npm run build` |

**Example check script compositions:**

If all exist:
```json
"check": "npm run lint && npm run typecheck && npm run test && npm run build"
```

If only lint and test exist:
```json
"check": "npm run lint && npm run test"
```

If only build exists:
```json
"check": "npm run build"
```

**Add the check script to package.json using Edit tool.**

### Phase 3: Detect Installed CLIs

Run detection for each CLI:

```bash
which gh && echo "installed" || echo "not installed"
which supabase && echo "installed" || echo "not installed"
which vercel && echo "installed" || echo "not installed"
which wrangler && echo "installed" || echo "not installed"
which turso && echo "installed" || echo "not installed"
which bun && echo "installed" || echo "not installed"
which pnpm && echo "installed" || echo "not installed"
which docker && echo "installed" || echo "not installed"
```

**Display results as a table:**

```
CLI Detection Results
=====================

| Status | CLI | Description |
|--------|-----|-------------|
| ✓ | gh | GitHub CLI |
| ✓ | bun | Bun runtime |
| ✓ | pnpm | Fast package manager |
| ✗ | supabase | Supabase CLI |
| ✗ | vercel | Vercel CLI |
| ✗ | wrangler | Cloudflare Workers CLI |
| ✗ | turso | Turso database CLI |
| ✗ | docker | Docker container runtime |
```

### Phase 4: Offer to Install Missing CLIs

If any CLIs are missing, ask the user:

> "Would you like to install the missing CLIs? I can show you the installation commands."

If user agrees, display installation table:

| CLI | Installation Command |
|-----|---------------------|
| gh | `brew install gh` |
| supabase | `brew install supabase/tap/supabase` |
| vercel | `npm i -g vercel` |
| wrangler | `npm i -g wrangler` |
| turso | `brew install tursodatabase/tap/turso` |
| bun | `curl -fsSL https://bun.sh/install \| bash` |
| pnpm | `npm i -g pnpm` |
| docker | `brew install --cask docker` |

**Only show commands for missing CLIs.**

### Phase 5: Detect CI/CD Workflows

Check if GitHub Actions workflows exist:

```bash
ls .github/workflows/*.yml 2>/dev/null || echo "NO_WORKFLOWS"
```

**If no workflows found:**

Ask the user:
> "No hay workflows de GitHub Actions configurados. ¿Querés que configure CI básico para este proyecto?"

If user agrees:
1. Suggest running `/github-actions` skill
2. Or offer to create a basic CI workflow based on detected stack

**If workflows exist:**

Report existing workflows:
```
GitHub Actions
==============
✓ Workflows detected:
  - ci.yml
  - deploy.yml
```

### Phase 6: Update/Create Project CLAUDE.md

Check if CLAUDE.md exists in the project root:

```bash
ls CLAUDE.md 2>/dev/null
```

**If CLAUDE.md exists:**
- Read it and add/update a "## Available CLIs" section with detected tools
- Preserve existing content

**If CLAUDE.md doesn't exist:**
- Create a minimal CLAUDE.md with:
  - Repository overview (ask user or infer from package.json/pyproject.toml)
  - Available CLIs section
  - Quick start commands

**Available CLIs section template:**

```markdown
## Available CLIs

The following CLI tools are available in this environment:

| CLI | Purpose |
|-----|---------|
| gh | GitHub operations (issues, PRs, releases) |
| bun | Fast JavaScript runtime and package manager |
| pnpm | Efficient package manager |
```

Only include CLIs that are installed.

## CLI Descriptions Reference

| CLI | Full Description |
|-----|------------------|
| gh | GitHub CLI for issues, PRs, releases, and repo management |
| supabase | Supabase local development and database management |
| vercel | Vercel deployment and serverless functions |
| wrangler | Cloudflare Workers development and deployment |
| turso | Turso edge database CLI |
| bun | Fast JavaScript runtime, bundler, and package manager |
| pnpm | Fast, disk-efficient package manager |
| docker | Container runtime for development and deployment |

## Output Summary

At the end, provide a summary:

```
Setup Complete
==============

Project Type: Node.js
Check Script: Added to package.json
  - Includes: lint, typecheck, test, build

Available CLIs: 5/8
  - Installed: gh, bun, pnpm, docker, vercel
  - Missing: supabase, wrangler, turso

GitHub Actions: ✓ ci.yml detected
  (or: ✗ No workflows - run /github-actions to configure)

CLAUDE.md: Updated with available CLIs
```
