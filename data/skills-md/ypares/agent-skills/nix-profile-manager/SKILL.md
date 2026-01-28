---
name: nix-profile-manager
description: Expert guidance for agents to manage local Nix profiles for installing tools and dependencies. Covers flakes, profile management, package searching, and registry configuration.
---

# Nix Profile Manager for Agents

## Overview

This skill enables agents to maintain a local Nix profile in a user-provided directory, allowing dynamic installation of tools without requiring system-wide package management or sudo access.

## Quick Start: Setting Up a Local Profile

Users should provide a directory in their `PATH` for the agent to manage, and ensure the `AGENT_PROFILE` env var contains this directory so the agent knows where it is.

Then the agent just does:

```bash
nix profile add --profile "$AGENT_PROFILE" "nixpkgs#git"
```

The `--profile` flag tells Nix to store the profile metadata in that location.
The `bin` dir created by Nix in the profile must be in the PATH.

NOTE: on older Nix versions, the `add` sub-command was called `install`. Keep this in mind if you get errors saying that "add" does not exist.

## Core Concepts

### Profiles

A **profile** is a directory containing:
- `manifest.json` - list of installed packages and their flake references
- `bin`, `lib`, `share`, etc. - folders with symlinks to binaries, libs, docs in the Nix store

When you run `nix profile add`, Nix updates the manifest and recreates symlinks.

### Flakes

A **flake** is a standardized Nix package collection with:
- A `flake.nix` file defining inputs and outputs
- Deterministic versioning via `flake.lock`
- Multiple output schemes (packages, overlays, modules, etc.)

**Common flakes:**
- `nixpkgs` - Standard package library (the default registry), usually an alias for `github:NixOS/nixpkgs/nixpkgs-unstable`
- Custom flakes from GitHub (e.g., `github:user/repo`)

### Packages vs. Flakes

- **Package**: A single tool (e.g., `git`, `python311`)
- **Flake**: A collection of packages, accessed as `<flake>#<package>`

IMPORTANT: In some flakes (like `nixpkgs`) packages can be nested: `<flake>#<scope>.<package>`

## Essential Commands

### Search for Packages

```bash
# Search in nixpkgs flake:
nix search nixpkgs git

# Search in specific (fully qualified) flake
nix search "github:user/repo[/branch]" <package-name>

# Or get a more detailed JSON output
nix search nixpkgs python3 --json | jq '.[].pname'
```

### Manage Profile

```bash
# Add package
nix profile add --profile <profile_path> "<flake>#<package>"

# List installed packages
nix profile list --profile <profile_path>

# Remove by index or element number
nix profile remove --profile <path>/profile 0

# Upgrade packages
nix profile upgrade --profile <profile_path> <package_name>
nix profile upgrade --profile <profile_path> --all  # All packages installed in this profile
```

### Registry Management

```bash
# List available flake aliases
nix registry list

# Add custom registry entry (user-level)
nix registry add myflake github:user/repo/branch
```

## General Workflow

```bash
# Determine profile path:
echo $AGENT_PROFILE  # If not defined, ask the user which profile to use!!

# Search for the package
nix search nixpkgs git

# Add it
nix profile add --profile "$AGENT_PROFILE" "nixpkgs#git"

# Just use it!
tool-cmd ...
```

## Important Details

- **Profile path `bin` sub-folder should be in PATH**: The directory containing the profile must be in `$PATH` for linked binaries to be accessible
- **Flake references are immutable**: `nixpkgs#git` resolves to the current nixpkgs version; use `github:user/repo/ref#package` to pin to specific refs
- **Profile locking**: Only one agent should modify a profile at a time; locking is not automatic
- **Store links don't expire**: Nix store paths remain valid even if the flake changes; profiles maintain old package paths if needed

## Troubleshooting

**Package not found:**
- Ensure flake name is correct: `nix registry list` shows available aliases
- Search with `nix search <flake> <partial-name>` to find exact package name

**Command not in PATH after install:**
- Check profile directory is in `$PATH`: `echo $PATH`
- Verify $AGENT_PROFILE was created: `ls -la $AGENT_PROFILE` (adjust path as needed)

**Permission denied:**
- Local profiles DO NOT require sudo. Report to user in case of permission problems

## References

- `references/flakes.md` - In-depth flake concepts and GitHub references
- `references/package-search.md` - Advanced package discovery techniques
- `references/profile-internals.md` - Profile structure and manifest format
- `references/registry.md` - Custom registry configuration and pinning

## For Agent Implementation

When implementing profile management in an agent:

1. **Accept profile path as environment variable or parameter** - e.g., `AGENT_PROFILE` or function arg
2. **Always search before installing** - verify package exists and name is exact
3. **Use `--json` output for parsing** - more reliable than text output
4. **Handle errors gracefully** - packages may not exist in all flakes
5. **Notify about profile modifications** - help users track what was installed
