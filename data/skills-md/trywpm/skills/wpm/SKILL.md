---
name: wpm
description: Manages WordPress plugins, themes, and mu-plugins using wpm, a package manager for the WordPress ecosystem. Use when the user wants to install, update, remove, or publish WordPress packages, initialize a WordPress project with wpm, manage wpm.json dependencies, or work with the wpm registry.
---

# wpm - Package Manager for WordPress

## Installation

```bash
# Check if installed
wpm --version

# Install (Unix)
curl -fsSL https://wpm.so/install | bash

# Install (Windows PowerShell)
irm wpm.so/install.ps1 | iex
```

## Quick start

Initialize a project:

```bash
wpm init
```

Install a package:

```bash
wpm install wordpress-seo@26.9.0
```

## wpm.json overview

Two modes based on context:

| | Project (site) | Publishable package |
|---|---|---|
| `private` | `true` (recommended) | `false` or omitted |
| `type` | optional | **required** (`plugin`/`theme`/`mu-plugin`) |
| `version` | optional | **required** (SemVer) |
| `config.runtime` | recommended | — |
| `requires` | — | recommended |

### Critical version rules

- `dependencies`, `devDependencies`, `config.runtime.wp`, `config.runtime.php` → **exact versions only** (no `^`, `~`, `>=`)
- `requires.wp`, `requires.php` → version ranges allowed (`>=6.0.0`)

**Schema**: Read [reference/schema.json](reference/schema.json) for the full JSON schema.

## Commands

**CLI reference**: See [reference/commands.md](reference/commands.md) for all commands and workflows.

Common commands:

```bash
wpm init                          # New project
wpm init --existing               # Existing plugin/theme
wpm install <pkg>@<version>       # Install package
wpm ls                            # List dependencies
wpm outdated                      # Check for updates
wpm uninstall <pkg>               # Remove (⚠️ confirm first)
```

If unsure about a command or flag, run `wpm <command> --help`.

## Publishing

**Publishing guide**: See [reference/publishing.md](reference/publishing.md) for auth, CI, and publish workflow.

## Lockfile

- `wpm.lock` is auto-generated. Commit it. Never edit manually.

## Common pitfalls

- Do NOT use version ranges in `dependencies` or `devDependencies`
- Do NOT use ranges in `config.runtime`
- Do NOT publish when `"private": true`
- Always run `wpm outdated` before updating; re-install specific versions explicitly
