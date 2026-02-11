---
name: shareful-init
description: Guides setup of a shareful.ai shares repository. Runs npx shareful-ai init to create the directory structure, explains the repo layout, and walks through next steps. Use when the user wants to "set up shareful", "create a shares repo", "start sharing solutions", or "initialize shareful".
---

# Shareful Init

Set up a shareful.ai shares repository so you can start capturing and sharing coding solutions.

## When to Use This Skill

Use this skill when the user:

- Wants to set up a shares repository for the first time
- Asks "how do I start sharing solutions" or "set up shareful"
- Wants to contribute fixes back to the community
- Needs a repo to store SHARE.md files

## What Init Creates

`npx shareful-ai init [name]` creates a ready-to-use shares repository:

```
my-shares/
  .gitignore
  README.md
  AGENTS.md
  shares/
    example-share/
      SHARE.md
```

- **`shares/`** -- directory for all SHARE.md solution files
- **`AGENTS.md`** -- documents the SHARE.md format for AI agents working in the repo
- **`README.md`** -- repo overview with quick start instructions
- **`example-share/SHARE.md`** -- template share to get started

The command also initializes a git repository with an initial commit and saves the repo path to `~/.shareful/config.json`.

## Setup Workflow

**IMPORTANT**: You MUST complete all 3 steps. After pushing to GitHub, you MUST run `npx shareful-ai register` -- without it the repo will never appear on shareful.ai.

### Step 1: Create the Repository

```bash
npx shareful-ai init my-shares
```

The name must be alphanumeric with dots, hyphens, or underscores (max 128 characters). Defaults to `shares` if not provided. The command creates an initial git commit automatically.

### Step 2: Push to GitHub

```bash
cd my-shares
gh repo create my-shares --source . --public --push
```

Or create the repository manually on GitHub and push:

```bash
cd my-shares
git remote add origin git@github.com:username/my-shares.git
git push -u origin main
```

### Step 3: Register for Indexing

Immediately after pushing, register the repo. This is required -- the repo will not be indexed and shares will not be discoverable without it:

```bash
npx shareful-ai register
```

Optionally, create your first share with `npx shareful-ai create`.

## Name Validation Rules

- Letters, numbers, dots, hyphens, and underscores only
- Max 128 characters
- Examples: `my-shares`, `company.solutions`, `team_fixes`

## Related Skills

- `shareful-create` for writing high-quality SHARE.md files
- `shareful-search` for finding existing solutions on shareful.ai
