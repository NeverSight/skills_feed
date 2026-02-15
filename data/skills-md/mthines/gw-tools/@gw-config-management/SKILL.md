---
name: '@gw-config-management'
description: Configure and optimize gw-tools for different project types and team needs. Use this skill when setting up gw for new projects, configuring auto-copy files, troubleshooting configuration issues, or customizing gw for Next.js, Node.js APIs, monorepos, or React SPAs. Triggers on tasks involving .gw/config.json, auto-copy patterns, environment files, or gw init commands.
license: MIT
metadata:
  author: mthines
  version: '1.0.0'
---

# Configuration Management - Comprehensive Guide

This guide teaches you how to configure gw for optimal workflows across different project types.

## Table of Contents

1. [Understanding gw Configuration](#1-understanding-gw-configuration)
2. [Configuration Options Reference](#2-configuration-options-reference)
3. [Initial Setup: Secrets in the Default Branch](#3-initial-setup-secrets-in-the-default-branch)
4. [Auto-Copy Strategies](#4-auto-copy-strategies)
5. [Project-Type Configuration Patterns](#5-project-type-configuration-patterns)
6. [Team Configuration Management](#6-team-configuration-management)
7. [Advanced Configuration Techniques](#7-advanced-configuration-techniques)
8. [Troubleshooting Configuration](#8-troubleshooting-configuration)

---

## 1. Understanding gw Configuration

### Config File Location

gw stores configuration at `.gw/config.json` in your repository:

```
/projects/myapp.git/
├── main/                  # Main worktree
│   ├── src/
│   ├── .gw/
│   │   └── config.json   # ← Configuration file
│   └── package.json
├── feature-a/             # Other worktrees
└── feature-b/
```

### Auto-Detection vs Manual Configuration

**Auto-detection (recommended for most cases):**

```bash
$ cd /projects/myapp/main
$ gw init

Repository root detected: /projects/myapp.git
Default branch detected: main
Configuration created at .gw/config.json
```

gw automatically detects:

- Repository root (parent directory containing worktrees)
- Default branch (main, master, or current branch)

**Manual configuration (when auto-detection fails):**

```bash
$ gw init --root /projects/myapp.git \
          --default-branch main \
          --auto-copy-files .env,.env.local,secrets/
```

**Interactive configuration (for guided setup):**

```bash
$ gw init --interactive

Interactive Configuration

Press Enter to accept defaults. Leave blank to skip optional settings.

Default source worktree name [main]: main
Do you want to auto-copy files when creating worktrees? (y/n) [n]: y
  Enter comma-separated file/directory paths (e.g., .env,secrets/)
  Files to auto-copy: .env,.env.local,secrets/
Do you want to add post-add hooks? (y/n) [n]: y
  Enter commands to run after creating worktrees
  Variables: {worktree}, {worktreePath}, {gitRoot}, {branch}
  Post-add hook 1 (leave blank to finish): pnpm install
  Post-add hook 2 (leave blank to finish):
Days before worktrees are considered stale [7]: 14
Prompt to cleanup stale worktrees after add/list? (y/n) [n]: n

✓ Configuration created successfully
```

Interactive mode is useful when:

- Setting up gw for the first time
- You're unsure about configuration options
- You want to explore all available settings
- Onboarding new team members who need guidance

### Network Behavior and Offline Support

The `gw add` command follows a **remote-first approach** when creating new branches to ensure you're always working with the latest code:

**Remote-First Design:**

When you create a new branch (e.g., `gw add feat/new-feature`), gw:

1. Fetches the latest version of the source branch from the remote (e.g., `origin/main`)
2. Creates your new branch from the fresh remote ref
3. Sets up tracking to your new branch's remote counterpart (e.g., `origin/feat/new-feature`)

**Why this matters:**

- **Prevents conflicts**: Your branch starts from the latest remote code, not a potentially outdated local branch
- **Ensures fresh code**: You're building on the most recent changes from your team
- **Reduces merge pain**: Fewer surprises when you eventually merge back
- **Team synchronization**: Everyone starts from the same point

**Automatic Fallback for Offline Work:**

The command has intelligent fallback behavior based on how you use it:

| Command                          | Fetch Behavior           | Fallback                                |
| -------------------------------- | ------------------------ | --------------------------------------- |
| `gw add feat/new`                | Fetches `origin/main`    | Falls back to local `main` with warning |
| `gw add feat/new --from develop` | Fetches `origin/develop` | **No fallback** - exits with error      |

**When `--from` is specified**, gw assumes you need that exact source and requires a successful remote fetch. If the fetch fails, you'll get:

- Clear error message about why the fetch failed
- Troubleshooting steps (check network, verify branch exists, check auth)
- Alternative command suggestions

**When using default branch** (no `--from`), gw allows local fallback for offline development or when no remote is configured. You'll see:

- Warning that remote fetch failed
- Explanation that start point may not be current
- Note that this is acceptable for offline work
- Confirmation that local branch is being used

**Example output (offline scenario):**

```bash
$ gw add feat/offline

Branch feat/offline doesn't exist, creating from main...
Fetching latest from remote to ensure fresh start point...

⚠ WARNING Could not fetch from remote

Falling back to local branch. The start point may not be up-to-date with remote.
This is acceptable for offline development or when remote is unavailable.

Creating from main (local branch)

Creating worktree: feat/offline
```

**Strictness Levels:**

- **Lenient**: `gw add feat/new` - Allows local fallback for offline work
- **Strict**: `gw add feat/new --from develop` - Requires fresh remote ref, no fallback
- **Manual override**: Can always use local branches explicitly with `git worktree add`

**Clone and initialize (new repositories):**

```bash
# Clone a repository and automatically set up gw
$ gw init git@github.com:user/repo.git

Cloning repository from git@github.com:user/repo.git...
✓ Repository cloned to repo

Setting up gw_root branch...
✓ Created gw_root branch

Initializing gw configuration...
✓ Configuration created

Creating main worktree...
✓ Created main worktree

✓ Repository initialized successfully!

  Repository: /projects/repo
  Config: /projects/repo/.gw/config.json
  Default worktree: main
```

Clone mode automatically:

- Clones the repository with `--no-checkout`
- Creates a `gw_root` branch
- Auto-detects the default branch from the remote
- Creates gw configuration
- Creates the default branch worktree
- Uses `.git` suffix for the repository directory (bare repo convention)
- Navigates you to the repository directory (with shell integration)

You can also specify a custom directory and configuration:

```bash
# Clone into a specific directory with configuration
$ gw init git@github.com:user/repo.git my-project \
          --auto-copy-files .env,secrets/ \
          --post-add "pnpm install"

# Clone and configure interactively
$ gw init https://github.com/user/repo.git --interactive
```

### Configuration Scope

Configuration is **per-repository**, not global:

- Each repository has its own `.gw/config.json`
- Different repos can have different configurations
- Configuration is shared across all worktrees in that repo

### Config Precedence and Defaults

If no configuration exists:

1. `gw` searches for `.gw/config.json` walking up from current directory
2. If not found, attempts auto-detection on first `gw add` command
3. Uses fallback defaults:
   - `root`: Auto-detected from `git worktree list`
   - `defaultBranch`: "main"
   - `autoCopyFiles`: `[]` (nothing copied automatically)

---

## 2. Configuration Options Reference

### Complete Configuration Structure

```json
{
  "root": "/absolute/path/to/repo.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env", ".env.local", "secrets/", "config/local.json"],
  "updateStrategy": "merge",
  "cleanThreshold": 7,
  "autoClean": true
}
```

### `root`: Repository Root Path

**Purpose:** Absolute path to the parent directory containing all worktrees.

**Example:**

```json
{
  "root": "/Users/you/projects/myapp.git"
}
```

**How it's used:**

- Resolving worktree names to absolute paths
- Finding source files for auto-copy
- Determining worktree relationships

**When to set manually:**

- Auto-detection fails (unusual directory structure)
- Repository has non-standard naming
- Using symlinks or network drives

### `defaultBranch`: Default Source Worktree

**Purpose:** Which worktree to copy files from by default.

**Example:**

```json
{
  "defaultBranch": "develop"
}
```

**Common values:**

- `"main"` - Most projects
- `"master"` - Older projects
- `"develop"` - Gitflow workflow
- `"staging"` - Copy from staging environment

**How it's used:**

- `gw add feature-x` copies from `defaultBranch` worktree
- `gw sync target file.txt` syncs from `defaultBranch` unless `--from` specified
- `gw sync target` (without files) syncs `autoCopyFiles` from `defaultBranch`
- `gw update` fetches and updates from `defaultBranch` unless `--from` specified
- **Auto-clean never removes this worktree** - it's protected as the source for file syncing

**Important:** Ensure your secrets and environment files exist in the `defaultBranch` worktree **before** using `gw add` or `gw sync`. This worktree is the source from which files are copied.

### `updateStrategy`: Default Update Strategy

**Purpose:** Choose default strategy for `gw update` command - merge or rebase.

**Example:**

```json
{
  "updateStrategy": "rebase"
}
```

**Valid values:**

- `"merge"` (default) - Creates merge commits, preserves complete history
- `"rebase"` - Replays commits for linear history, rewrites history

**How it's used:**

- `gw update` uses this strategy by default
- Can be overridden per-command with `--merge` or `--rebase` flags
- Strategy precedence: CLI flags > config > default (merge)

**Which strategy to choose:**

Use **merge** when:

- You want to preserve complete commit history
- Working on shared branches where others may have pulled your commits
- You prefer explicit merge commits showing when branches were integrated
- Team prefers "true history" approach

Use **rebase** when:

- You want a linear, clean commit history
- Working on personal feature branches not shared with others
- You're comfortable with rewriting history
- Team prefers clean, linear history approach

**Important:** Rebase rewrites commit history. Only use it on branches you haven't shared with others, or ensure your team understands the implications.

### `autoCopyFiles`: File Patterns to Auto-Copy

**Purpose:** Files/directories automatically copied when creating worktrees.

**Example:**

```json
{
  "autoCopyFiles": [".env", ".env.local", "secrets/api-keys.json", "config/", "ssl/"]
}
```

**Pattern types:**

1. **Exact files:** `".env"` - Single file
2. **Directories:** `"secrets/"` - Entire directory (recursive)
3. **Nested paths:** `"config/local.json"` - Specific nested file

**How it's used:**

- `gw add feature-x` automatically copies these files when creating worktrees
- `gw sync feature-x` (without file arguments) syncs these files to existing worktrees

**Important notes:**

- Paths are relative to repository root
- Directories should end with `/`
- Files are copied, not symlinked
- Non-existent files are skipped with warning

### `cleanThreshold`: Worktree Cleanup Age

**Purpose:** Number of days before worktrees are considered stale when using `gw clean --use-autoclean-threshold` or auto-cleanup.

**Example:**

```json
{
  "cleanThreshold": 7
}
```

**Common values:**

- `7` - Default (one week)
- `14` - Two weeks (more lenient)
- `3` - Three days (aggressive cleanup)
- `30` - One month (very lenient)

**How it's used:**

- `gw clean` (default) removes ALL safe worktrees regardless of age
- `gw clean --use-autoclean-threshold` removes only worktrees older than this threshold
- Auto-cleanup (via `autoClean` setting) respects this threshold
- Only removes worktrees with no uncommitted changes and no unpushed commits (unless `--force`)
- `gw clean --dry-run` or `gw clean --use-autoclean-threshold --dry-run` previews which worktrees would be removed

**Setting the threshold:**

```bash
# Set during initialization
gw init --clean-threshold 14

# Or manually edit .gw/config.json
```

**Important notes:**

- Age is calculated from the worktree's `.git` file modification time
- Bare/main repository worktrees are never removed
- Use `--force` flag to bypass safety checks (not recommended)

### `autoClean`: Interactive Cleanup Prompts

**Purpose:** Enable interactive prompts to clean up stale worktrees automatically after `gw add` and `gw list` commands.

**Example:**

```json
{
  "autoClean": true,
  "cleanThreshold": 7
}
```

**How it works:**

- Prompts appear after `gw add` or `gw list` when stale worktrees are detected
- Only prompts once per 24 hours (cooldown period)
- Shows: `🧹 Found 2 stale worktrees (7+ days old). Clean them up? [Y/n]:`
- Press Enter or `y` to remove them, or `n` to skip
- Uses the same safety checks as `gw clean` (no uncommitted/unpushed changes)
- Never removes the `defaultBranch` worktree

**Setting auto-clean:**

```bash
# Enable during initialization
gw init --auto-clean

# With custom threshold
gw init --auto-clean --clean-threshold 14
```

**When to use:**

- Teams that frequently create feature branches
- Repositories with many short-lived worktrees
- Projects where disk space is a concern
- Development workflows with regular cleanup needs

**When NOT to use:**

- You prefer manual cleanup control
- Long-lived feature branches are common
- You want to review worktrees before removing them

**Tip:** If you decline the prompt, you can always run `gw clean` manually to review and clean worktrees interactively.

---

## 3. Initial Setup: Secrets in the Default Branch

Before using `gw add` with auto-copy, your secrets and environment files **must exist** in your `defaultBranch` worktree. This worktree is the **source** from which files are copied.

### First-Time Setup Flow

```bash
# 1. Set up your bare repository structure
git clone --bare https://github.com/user/repo.git repo.git
cd repo.git

# 2. Create the main worktree (your defaultBranch)
git worktree add main main

# 3. Set up secrets in the main worktree FIRST
cd main
cp .env.example .env           # Create your environment file
# Edit .env with your actual secrets, API keys, etc.
mkdir -p secrets/
# Add any other secret files your project needs

# 4. Initialize gw with auto-copy configuration
gw init --auto-copy-files .env,secrets/

# 5. Now create feature worktrees - files are copied automatically
cd ..
gw add feat-new-feature
# .env and secrets/ are automatically copied from main
```

### Why This Order Matters

1. **Source must exist first** - `gw add` copies from `defaultBranch`, so files must be there
2. **Auto-clean protection** - The `defaultBranch` worktree is never auto-cleaned, ensuring your source files are always available
3. **Sync depends on source** - `gw sync` also uses `defaultBranch` as the source

### Keeping Secrets Updated

When you update secrets in your `defaultBranch` worktree:

```bash
# Sync all autoCopyFiles to an existing worktree
gw sync feat-existing-branch

# Or sync specific files
gw sync feat-existing-branch .env
```

---

## 4. Auto-Copy Strategies

### Files That Should Be Copied

**Environment variables:**

```json
".env",
".env.local",
".env.development"
```

**Secrets and credentials:**

```json
"secrets/",
"keys/",
"ssl/certificates/"
```

**Local configuration:**

```json
"config/local.json",
".vscode/settings.json",
"components/ui/.vercel/"
```

**Cache directories (sometimes):**

```json
".next/cache/",
"public/uploads/"
```

### Files That Should NOT Be Copied

**Dependencies:**

```
❌ node_modules/
❌ vendor/
❌ .pnpm-store/
```

**Build artifacts:**

```
❌ dist/
❌ build/
❌ .next/ (except cache)
❌ out/
```

**Version control:**

```
❌ .git (handled automatically)
❌ .gitignore (in source control)
```

**IDE settings (usually):**

```
❌ .idea/
❌ .vscode/ (unless team-shared)
```

### Directory vs File Copying

**Directory (recursive):**

```json
{
  "autoCopyFiles": ["secrets/"]
}
```

Copies:

```
secrets/
├── api-key.json      ← Copied
├── database.env      ← Copied
└── ssl/
    └── cert.pem      ← Copied (recursive)
```

**Specific file:**

```json
{
  "autoCopyFiles": ["secrets/api-key.json"]
}
```

Copies only:

```
secrets/
└── api-key.json      ← Only this file
```

### Glob Patterns (Not Currently Supported)

Currently, gw doesn't support glob patterns like:

- `"*.env"` - All .env files
- `"config/**/*.json"` - All JSON in config

**Workaround:** List files explicitly or copy parent directory.

---

## 5. Project-Type Configuration Patterns

### Next.js Projects

**Typical structure:**

```
myapp/
├── .env
├── .env.local
├── .next/
├── public/
│   └── uploads/
├── components/
│   └── ui/
│       └── .vercel/
└── pages/
```

**Recommended configuration:**

```json
{
  "root": "/projects/myapp.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env", ".env.local", ".env.development", ".vercel/", "public/uploads/", "components/ui/.vercel/"]
}
```

**Why these files:**

- `.env*` - Environment variables for different modes
- `.vercel/` - Vercel deployment configuration
- `public/uploads/` - User-uploaded assets
- `components/ui/.vercel/` - Component-specific Vercel settings

**See also:** [Next.js Setup Example](./examples/nextjs-setup.md)

### Node.js APIs

**Typical structure:**

```
api/
├── .env
├── src/
├── ssl/
│   ├── private.key
│   └── certificate.crt
└── config/
    └── local.json
```

**Recommended configuration:**

```json
{
  "root": "/projects/api.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env", "ssl/", "keys/", "secrets/", "config/local.json"]
}
```

**Why these files:**

- `.env` - Database URLs, API keys, service credentials
- `ssl/` - SSL certificates for HTTPS
- `keys/` - JWT keys, encryption keys
- `secrets/` - Service account credentials
- `config/local.json` - Local-only configuration overrides

### React SPAs

**Typical structure:**

```
webapp/
├── .env
├── .env.local
├── public/
│   └── config.json
└── src/
```

**Recommended configuration:**

```json
{
  "root": "/projects/webapp.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env", ".env.local", "public/config.json"]
}
```

**Why these files:**

- `.env` - Build-time environment variables
- `.env.local` - Local API endpoints, feature flags
- `public/config.json` - Runtime configuration

### Monorepos (pnpm/Yarn/npm workspaces)

**Typical structure:**

```
monorepo/
├── .env                      # Root environment
├── packages/
│   ├── api/
│   │   └── .env             # Package-specific
│   ├── web/
│   │   └── .env
│   └── shared/
└── pnpm-workspace.yaml
```

**Recommended configuration:**

```json
{
  "root": "/projects/monorepo.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env", "packages/api/.env", "packages/web/.env", "packages/shared/config.local.json", ".vercel/"]
}
```

**Why these files:**

- Root `.env` - Shared environment variables
- Package-specific `.env` - Service-specific configuration
- Shared config files - Cross-package configuration

**See also:** [Monorepo Setup Example](./examples/monorepo-setup.md)

### Full-Stack Apps (Frontend + Backend)

**Typical structure:**

```
fullstack/
├── .env.backend
├── .env.frontend
├── backend/
│   ├── ssl/
│   └── secrets/
└── frontend/
    └── .vercel/
```

**Recommended configuration:**

```json
{
  "root": "/projects/fullstack.git",
  "defaultBranch": "main",
  "autoCopyFiles": [".env.backend", ".env.frontend", "backend/ssl/", "backend/secrets/", "frontend/.vercel/"]
}
```

---

## 6. Team Configuration Management

### Committing Configuration to Version Control

**Recommended approach:**

```bash
# Add .gw/config.json to git
git add .gw/config.json
git commit -m "chore: add gw configuration for team"
git push
```

**Benefits:**

- Team members get configuration automatically
- Consistent workflow across team
- Version-controlled changes to auto-copy patterns
- Easy onboarding for new developers

**What to include:**

- `root` - Can be a template, team members adjust locally
- `defaultBranch` - Should match team's workflow
- `autoCopyFiles` - Should include all shared secrets/configs

### Team-Wide vs Personal File Patterns

**Team-wide (commit to repo):**

```json
{
  "autoCopyFiles": [".env.template", "ssl/development-cert.pem", "config/shared.json"]
}
```

**Personal (each developer customizes):**

```bash
# Copy team config
cp .gw/config.json .gw/config.local.json

# Add personal files
vim .gw/config.local.json
# Add: "path/to/my-secrets.env"

# .gw/config.local.json is in .gitignore
```

### Documenting Auto-Copy Patterns

**In README.md:**

```markdown
## Development Setup

### 1. Install gw

npm install -g @gw-tools/gw-tool

### 2. Configuration

The repository includes gw configuration (`.gw/config.json`) that automatically copies:

- `.env` - Environment variables (copy from `.env.example`)
- `ssl/` - Development SSL certificates
- `secrets/` - Service credentials (get from team lead)

### 3. Create Feature Worktree

gw add feature-name -b feature-name main

Files will be automatically copied from the main worktree.
```

### Generating Documentation from Config

Use `gw show-init` to automatically generate a setup command from your current configuration:

```bash
# Generate the init command from current config
gw show-init
# Output: gw init --auto-copy-files .env,secrets/ --post-add 'pnpm install'

# Add to documentation automatically
echo "## Setup\n\n\`\`\`bash\n$(gw show-init)\n\`\`\`" >> README.md

# Copy to clipboard for sharing (macOS)
gw show-init | pbcopy

# Copy to clipboard for sharing (Linux)
gw show-init | xclip -selection clipboard
```

**Benefits:**

- Always accurate - generated from actual config
- Easy to share with team members
- Simple to document in README files
- Shows exact command to replicate your setup

**Example documentation update:**

```markdown
## Quick Setup

To configure gw for this project, run:

\`\`\`bash
gw init --auto-copy-files .env,secrets/ --post-add 'pnpm install' --clean-threshold 14
\`\`\`

This will:

- Auto-copy `.env` and `secrets/` directory when creating worktrees
- Run `pnpm install` after each worktree creation
- Clean up worktrees older than 14 days
```

### Onboarding New Developers

**Onboarding checklist:**

1. Clone repository
2. Install gw: `npm install -g @gw-tools/gw-tool`
3. Set up secrets (one-time):
   ```bash
   cp .env.example .env
   # Get secrets from team lead or secret manager
   ```
4. Create first worktree:
   ```bash
   gw add feature-onboarding -b feature-onboarding main
   # Automatically copies configured files
   ```

---

## 7. Advanced Configuration Techniques

### Multiple Source Worktrees

**Scenario:** Different features copy from different sources.

```bash
# Feature branches copy from develop
gw add feature-x -b feature-x

# Hotfixes copy from main
gw add hotfix-y --from main -b hotfix-y
```

**Configuration supports one default:**

```json
{
  "defaultBranch": "develop"
}
```

**Override at runtime:**

```bash
gw sync --from staging target-worktree .env
```

### Environment-Specific Configurations

**Scenario:** Different environments need different files.

**Approach:** Use custom config files.

```bash
# Development
cp .gw/config.development.json .gw/config.json

# Production
cp .gw/config.production.json .gw/config.json
```

### Integration with Secret Management Tools

**1Password:**

```bash
# After creating worktree, inject secrets
gw add feature-x
op inject -i feature-x/.env.template -o feature-x/.env
```

**AWS Secrets Manager:**

```bash
gw add feature-x
aws secretsmanager get-secret-value --secret-id myapp/dev \
  --query SecretString --output text > feature-x/.env
```

**HashiCorp Vault:**

```bash
gw add feature-x
vault kv get -field=.env secret/myapp > feature-x/.env
```

---

## 8. Troubleshooting Configuration

### Config Not Being Detected

**Problem:**

```bash
$ gw add feature-x
Error: Could not find .gw/config.json
```

**Solution:**

```bash
# Initialize configuration
gw init

# Or specify root manually
gw init --root $(gw root)
```

### Files Not Being Auto-Copied

**Problem:**

```bash
$ gw add feature-x
✓ Worktree created
# But .env is missing!
```

**Diagnostics:**

```bash
# Check configuration
cat .gw/config.json

# Check if file exists in source
ls ../main/.env
```

**Solutions:**

**Solution A:** Add to auto-copy:

```bash
gw init --auto-copy-files .env,.env.local
```

**Solution B:** Manual sync:

```bash
# Sync all autoCopyFiles from config
gw sync feature-x

# Or sync specific files
gw sync feature-x .env
```

### Wrong Files Being Copied

**Problem:** Copying too many or wrong files.

**Solution:** Review and update `autoCopyFiles`:

```bash
# Edit configuration
vim .gw/config.json

# Remove unwanted patterns
# Add specific files instead of directories
```

### Path Resolution Issues

**Problem:**

```bash
$ gw add feature-x
Error: Source file not found: secrets/api-key.json
```

**Solution:**

Ensure paths are relative to repository root:

```json
{
  "autoCopyFiles": [
    "secrets/api-key.json" // ✓ Relative to root
  ]
}
```

Not:

```json
{
  "autoCopyFiles": [
    "/Users/you/projects/myapp/secrets/api-key.json" // ✗ Absolute path
  ]
}
```

---

## Summary

You now understand:

- ✅ How gw configuration works (`.gw/config.json`)
- ✅ All configuration options (`root`, `defaultBranch`, `autoCopyFiles`)
- ✅ What files to auto-copy for different project types
- ✅ Team configuration management and onboarding
- ✅ Advanced techniques for complex workflows
- ✅ Troubleshooting common configuration issues

### Next Steps

1. Configure gw for your project using a [template](./templates/)
2. Read project-specific examples ([Next.js](./examples/nextjs-setup.md), [Monorepo](./examples/monorepo-setup.md))
3. Explore [autonomous workflow](../autonomous-workflow/)

---

_Part of the [gw-tools skills collection](../README.md)_
