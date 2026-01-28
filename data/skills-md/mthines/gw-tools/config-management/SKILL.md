---
name: "@gw-config-management"
description: Configure and optimize gw-tools for different project types and team needs. Use this skill when setting up gw for new projects, configuring auto-copy files, troubleshooting configuration issues, or customizing gw for Next.js, Node.js APIs, monorepos, or React SPAs. Triggers on tasks involving .gw/config.json, auto-copy patterns, environment files, or gw init commands.
license: MIT
metadata:
  author: mthines
  version: "1.0.0"
---

# Configuration Management - Comprehensive Guide

This guide teaches you how to configure gw for optimal workflows across different project types.

## Table of Contents

1. [Understanding gw Configuration](#1-understanding-gw-configuration)
2. [Configuration Options Reference](#2-configuration-options-reference)
3. [Auto-Copy Strategies](#3-auto-copy-strategies)
4. [Project-Type Configuration Patterns](#4-project-type-configuration-patterns)
5. [Team Configuration Management](#5-team-configuration-management)
6. [Advanced Configuration Techniques](#6-advanced-configuration-techniques)
7. [Troubleshooting Configuration](#7-troubleshooting-configuration)

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
  "autoCopyFiles": [
    ".env",
    ".env.local",
    "secrets/",
    "config/local.json"
  ],
  "cleanThreshold": 7
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

### `autoCopyFiles`: File Patterns to Auto-Copy

**Purpose:** Files/directories automatically copied when creating worktrees.

**Example:**

```json
{
  "autoCopyFiles": [
    ".env",
    ".env.local",
    "secrets/api-keys.json",
    "config/",
    "ssl/"
  ]
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

**Purpose:** Number of days before worktrees are considered stale for `gw clean`.

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
- `gw clean` removes worktrees older than this threshold
- Only removes worktrees with no uncommitted changes and no unpushed commits (unless `--force`)
- `gw clean --dry-run` previews which worktrees would be removed

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

---

## 3. Auto-Copy Strategies

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

## 4. Project-Type Configuration Patterns

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
  "autoCopyFiles": [
    ".env",
    ".env.local",
    ".env.development",
    ".vercel/",
    "public/uploads/",
    "components/ui/.vercel/"
  ]
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
  "autoCopyFiles": [
    ".env",
    "ssl/",
    "keys/",
    "secrets/",
    "config/local.json"
  ]
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
  "autoCopyFiles": [
    ".env",
    ".env.local",
    "public/config.json"
  ]
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
  "autoCopyFiles": [
    ".env",
    "packages/api/.env",
    "packages/web/.env",
    "packages/shared/config.local.json",
    ".vercel/"
  ]
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
  "autoCopyFiles": [
    ".env.backend",
    ".env.frontend",
    "backend/ssl/",
    "backend/secrets/",
    "frontend/.vercel/"
  ]
}
```

---

## 5. Team Configuration Management

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
  "autoCopyFiles": [
    ".env.template",
    "ssl/development-cert.pem",
    "config/shared.json"
  ]
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

## 6. Advanced Configuration Techniques

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

## 7. Troubleshooting Configuration

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
    "secrets/api-key.json"  // ✓ Relative to root
  ]
}
```

Not:

```json
{
  "autoCopyFiles": [
    "/Users/you/projects/myapp/secrets/api-key.json"  // ✗ Absolute path
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
3. Explore [advanced parallel development](../multi-worktree-dev/)

---

*Part of the [gw-tools skills collection](../README.md)*
