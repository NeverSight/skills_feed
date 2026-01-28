---
name: artifact-janitor
id: artifact-janitor
version: 1.1.0
description: "Senior Build Cleanup & System Optimization Specialist. Expert in reclaiming disk space and resolving build corruption in 2026 ecosystems."
---

# 🧹 Skill: artifact-janitor (v1.1.0)

## Executive Summary
The `artifact-janitor` is a tactical skill designed to maintain a clean, efficient, and healthy development environment. In 2026, where monorepos can easily exceed 5GB in dependencies and build caches (Turborepo, Next.js), proactive management of build artifacts is no longer optional—it is a performance requirement.

---

## 📋 Table of Contents
1. [Core Capabilities](#core-capabilities)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Quick Start: Simple Cleanup](#quick-start-simple-cleanup)
4. [Standard Production Patterns](#standard-production-patterns)
5. [Monorepo Deep Cleaning](#monorepo-deep-cleaning)
6. [Safety & Verification Protocols](#safety--verification-protocols)
7. [Automation with deep-clean.sh](#automation-with-deep-cleansh)
8. [Troubleshooting Build Corruption](#troubleshooting-build-corruption)
9. [Reference Library](#reference-library)

---

## 🚀 Core Capabilities
- **Artifact Discovery**: Identifying multi-gigabyte build caches and redundant dependencies.
- **Deep Cleanup**: Removing recursive `node_modules` and hidden cache directories (`.next`, `.turbo`).
- **Build Health Restoration**: Resolving "ghost errors" caused by corrupted build artifacts or stale TS build info.
- **Space Optimization**: Drastically reducing project size for archiving or sharing.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Manual `rm -rf`** | Prone to typos (e.g., `rm -rf / node_modules`). | Use the **`deep-clean.sh`** script or specific tool commands. |
| **Deleting `.git`** | Destroys repository history and identity. | **NEVER** delete `.git` unless detaching a repo. |
| **Deleting `.env`** | Loss of critical local secrets/keys. | Add `.env` to a "Protected" list. |
| **Blind Deletion in CI** | Can break incremental build performance. | Use targeted cache invalidation rather than total wipes. |
| **Ignoring `.cache`** | Many modern tools store GBs in hidden user-level caches. | Include `~/.cache` and framework-specific caches in discovery. |

---

## ⚡ Quick Start: Simple Cleanup

If you just need to free up some quick space or fix a minor build glitch:

```bash
# 1. Analyze space
du -sh node_modules .next

# 2. Targeted removal
rm -rf .next/
rm -rf node_modules/

# 3. Restore
bun install
```

---

## 🛠 Standard Production Patterns

### Pattern A: The "Ghost in the Machine" Fix
Use this when your code is correct but the build is failing with strange errors.

```bash
# Clean all caches and build info
rm -rf .next tsconfig.tsbuildinfo .turbo
# Re-generate everything
bun run build
```

### Pattern B: The Pre-Archive Scrub
Use this before zipping a project or pushing a massive refactor to ensure no local artifacts interfere.

```bash
# Using the janitor script in dry-run first
./skills/artifact-janitor/scripts/deep-clean.sh --dry-run
# Execute if safe
./skills/artifact-janitor/scripts/deep-clean.sh
```

---

## 📦 Monorepo Deep Cleaning

In 2026, monorepos are the norm. Standard `rm` doesn't scale.

### pnpm Workspace Cleanup
```bash
# Remove all node_modules in every package
pnpm -r exec rm -rf node_modules
# Clean pnpm global store (use with caution)
pnpm store prune
```

### Bun Workspace Cleanup
```bash
# Bun is fast, but its cache can grow
bun pm cache rm
```

---

## 🛡 Safety & Verification Protocols

1.  **Dry Run First**: Always visualize the deletion path.
2.  **Size Check**: `du -sh` is your best friend.
3.  **Process Check**: Ensure no `node`, `bun`, or `vite` processes are locking the files.
4.  **Verification**: After cleaning, run `bun x tsc --noEmit` to ensure the project structure is still valid.

*See [References: Safety Protocols](./references/safety-protocols.md) for more.*

---

## 🤖 Automation with `deep-clean.sh`

We provide a robust script in `skills/artifact-janitor/scripts/deep-clean.sh`.

**Features:**
- Recursive discovery of 20+ artifact types.
- Automatic sizing of reclaimed space.
- Safety-first `--dry-run` mode.

```bash
# Usage
./skills/artifact-janitor/scripts/deep-clean.sh [options]

# Options:
# --dry-run : Only show what would be deleted.
# --force   : Skip confirmation (use with caution).
```

---

## 🔍 Troubleshooting Build Corruption

### "Property X does not exist on type Y" (but it does)
**Cause**: Stale `tsconfig.tsbuildinfo` or `.next/types`.
**Fix**: `rm tsconfig.tsbuildinfo && rm -rf .next`.

### "Module not found" (after changing branches)
**Cause**: Stale `node_modules` or symlink breakage.
**Fix**: `rm -rf node_modules && bun install`.

---

## 📖 Reference Library

Detailed deep-dives into artifact management:

- [**Target Discovery Guide**](./references/target-discovery.md): How to find what's eating your disk.
- [**Safety Protocols**](./references/safety-protocols.md): Protecting your data during cleanup.
- [**CI/CD Optimization**](./references/cicd-cleanup.md): Best practices for automated pipelines.

---

*Updated: January 22, 2026 - 16:50*
