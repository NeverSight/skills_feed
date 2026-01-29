---
name: ted-mosby
description: Generate architectural wikis with source code traceability. Creates comprehensive documentation including architecture overviews, module docs, data flow diagrams, and interactive static sites. Use when asked to document a codebase, generate architecture docs, create a wiki, or explain how a project is structured.
---

# Ted Mosby - Architecture Wiki Generator

Generate comprehensive architectural documentation for any codebase with source code traceability (file:line references).

## Overview

Ted Mosby creates architectural wikis that help developers understand codebases. Every concept links directly to source code, so you can navigate from documentation to implementation.

**Output includes:**
- Architecture overview with Mermaid diagrams
- Module documentation with source traceability
- Data flow documentation
- Getting started guides
- Interactive static site with search, keyboard nav, dark mode

## When to Use This Skill

Use this skill when the user wants to:
- Document a codebase or project architecture
- Generate a wiki or documentation site
- Create architecture diagrams with source references
- Understand and document how a project is structured
- Produce navigable documentation with file:line traceability

**Trigger phrases:**
- "Generate docs for this project"
- "Create architecture documentation"
- "Document this codebase"
- "Make a wiki for this repo"
- "Help me understand this project's structure"

## Prerequisites

### Required
- Node.js >= 18.0.0
- Anthropic API key (`ANTHROPIC_API_KEY` environment variable)

### Check Prerequisites
```bash
# Verify Node.js version
node --version  # Should be >= 18.0.0

# Verify API key is set
echo $ANTHROPIC_API_KEY  # Should show your key
```

### Install Ted Mosby
```bash
npm install -g ted-mosby
```

## Quick Start Commands

### Basic Wiki Generation
```bash
# Generate wiki for current directory
ted-mosby generate -r .

# Generate wiki for a specific project
ted-mosby generate -r ./my-project

# Generate wiki for a GitHub repository
ted-mosby generate -r https://github.com/user/repo
```

### With Interactive Site
```bash
# Generate wiki + interactive static site
ted-mosby generate -r ./my-project --site

# Custom title and theme
ted-mosby generate -r ./my-project --site --site-title "My Project Docs" --theme dark

# Generate site only (if wiki already exists)
ted-mosby generate -r ./my-project --site-only
```

### Other Useful Options
```bash
# Focus on specific subdirectory
ted-mosby generate -r ./my-project -p src/core

# Custom output directory
ted-mosby generate -r ./my-project -o ./docs/architecture

# Verbose output (see agent progress)
ted-mosby generate -r ./my-project -v

# Estimate time/cost before running (dry run)
ted-mosby generate -r ./my-project -e
```

## Workflow

### Step 1: Gather Requirements

Before running Ted Mosby, clarify with the user:

1. **Target path** - What directory or repo to document?
2. **Output location** - Where should the wiki go? (default: `./wiki`)
3. **Site generation** - Do they want an interactive static site?
4. **Focus area** - Any specific subdirectory to focus on?
5. **Theme preference** - Light, dark, or auto?

### Step 2: Pre-flight Checks

Verify the environment is ready:

```bash
# Check Node.js version
node --version

# Verify ted-mosby is installed
which ted-mosby || echo "Run: npm install -g ted-mosby"

# Check API key
[ -z "$ANTHROPIC_API_KEY" ] && echo "Set ANTHROPIC_API_KEY environment variable"
```

### Step 3: Run Generation

Choose the appropriate command based on user needs:

| User Wants | Command |
|------------|---------|
| Basic wiki only | `ted-mosby generate -r ./project` |
| Wiki + interactive site | `ted-mosby generate -r ./project --site` |
| Site with custom title | `ted-mosby generate -r ./project --site --site-title "Docs"` |
| Dark theme site | `ted-mosby generate -r ./project --site --theme dark` |
| Focus on subdirectory | `ted-mosby generate -r ./project -p src/core` |
| Large codebase | `ted-mosby generate -r ./project --max-chunks 5000` |
| Quick iteration | `ted-mosby generate -r ./project --skip-index` |

### Step 4: Review Output

After generation completes:

1. **Wiki location:** `./wiki/README.md` (or custom output dir)
2. **Site location:** `./wiki/site/index.html` (if `--site` used)
3. **Open site:** Open `index.html` in browser

### Step 5: Fix Issues (if needed)

If there are broken links or missing pages:

```bash
# Check for and generate missing pages
ted-mosby continue -r ./my-project -o ./wiki

# Verify only (don't generate)
ted-mosby continue -r ./my-project -o ./wiki --verify-only
```

## Output Structure

```
wiki/
├── README.md                    # Navigation entry point
├── architecture/
│   ├── overview.md              # System architecture + Mermaid diagrams
│   └── data-flow.md             # Data flow documentation
├── components/
│   └── {module}/
│       └── index.md             # Per-module documentation
├── guides/
│   └── getting-started.md       # Quick start guide
├── glossary.md                  # Concept index
└── site/                        # (with --site flag)
    ├── index.html               # Interactive site entry
    ├── styles.css
    └── scripts.js
```

## Source Traceability

Every architectural concept includes clickable source references:

```markdown
## Authentication Flow

The authentication system uses JWT tokens for stateless auth.

**Source:** [`src/auth/jwt-provider.ts:23-67`](../../../src/auth/jwt-provider.ts#L23-L67)
```

This allows developers to navigate directly from documentation to implementation.

## Interactive Site Features

When `--site` is used, the generated site includes:

| Feature | Description |
|---------|-------------|
| Full-text search | Instant search across all pages (Cmd/Ctrl+K) |
| Keyboard navigation | Arrow keys, vim-style (j/k/h/l) |
| Dark/light mode | Respects system preference or manual toggle |
| Table of contents | Auto-generated from headings |
| Mobile responsive | Works on all devices |
| Offline capable | No server required |
| Mermaid diagrams | Rendered automatically |

## Command Reference

### `generate` - Create wiki documentation

| Option | Description | Default |
|--------|-------------|---------|
| `-r, --repo <path/url>` | Repository path or GitHub URL (required) | - |
| `-o, --output <dir>` | Output directory for wiki | `./wiki` |
| `-p, --path <path>` | Focus on specific directory | - |
| `-s, --site` | Generate interactive static site | - |
| `--site-only` | Generate site only (skip wiki) | - |
| `--site-title <title>` | Custom site title | Project name |
| `--theme <theme>` | Site theme: light, dark, auto | `auto` |
| `-v, --verbose` | Show detailed progress | - |
| `-e, --estimate` | Estimate time/cost (dry run) | - |
| `--max-chunks <n>` | Limit indexed chunks (for large repos) | unlimited |
| `--skip-index` | Use cached embeddings index | - |
| `--direct-api` | Use Anthropic API directly | - |
| `-m, --model <model>` | Claude model to use | `claude-sonnet-4-20250514` |
| `--max-turns <n>` | Limit agent iterations | 200 |

### `continue` - Resume/fix wiki generation

| Option | Description | Default |
|--------|-------------|---------|
| `-r, --repo <path>` | Repository path (required) | - |
| `-o, --output <dir>` | Wiki output directory | `./wiki` |
| `--verify-only` | Only check, don't generate | - |
| `--skip-index` | Use cached embeddings index | - |
| `-v, --verbose` | Show detailed progress | - |

## Large Codebase Options

For repositories with 10,000+ files:

```bash
# Limit indexed chunks (reduces memory usage)
ted-mosby generate -r ./large-project --max-chunks 5000

# Reduce search results per query
ted-mosby generate -r ./large-project --max-results 5

# Batched processing (for very large repos)
ted-mosby generate -r ./large-project --batch-size 3000
```

## Typical Runtime

| Codebase Size | Approximate Time |
|---------------|------------------|
| Small (<50 files) | 1-2 minutes |
| Medium (50-200 files) | 2-5 minutes |
| Large (200+ files) | 5-10 minutes |

Use `--estimate` to get a cost/time estimate before running.

## Troubleshooting

### "Credit balance is too low" error
Use direct API mode:
```bash
ted-mosby generate -r ./my-project --direct-api
```

### Out of memory on large repos
Limit indexed chunks:
```bash
ted-mosby generate -r ./large-project --max-chunks 5000 --batch-size 3000
```

### Slow re-runs during development
Skip re-indexing:
```bash
ted-mosby generate -r ./my-project --skip-index
```

### Missing pages / broken links
Use the continue command:
```bash
ted-mosby continue -r ./my-project -o ./wiki
```

## Example Conversation

**User:** "Can you document this project's architecture?"

**Assistant:** I'll use Ted Mosby to generate architectural documentation for your project.

First, let me verify the prerequisites are in place, then generate the wiki with an interactive site:

```bash
# Generate wiki with interactive site
ted-mosby generate -r . --site --site-title "Project Architecture"
```

This will create:
- `wiki/README.md` - Main navigation
- `wiki/architecture/overview.md` - Architecture diagrams
- `wiki/site/index.html` - Interactive documentation site

## Resources

- [Ted Mosby GitHub](https://github.com/your-username/ted-mosby)
- [Build an Agent Workshop](https://buildanagentworkshop.com)
