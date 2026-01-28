---
name: nixos-best-practices
description: Use when configuring NixOS with flakes, managing overlays with home-manager useGlobalPkgs, structuring NixOS configurations, or facing issues where configuration changes don't apply
license: MIT
metadata:
  author: chumeng
  version: "1.0.0"
---

# Configuring NixOS Systems with Flakes

Configure NixOS systems with flakes, manage overlays properly, and structure configurations for maintainability.

## Core Principle

**Understand the interaction between NixOS system configuration and Home Manager overlays.**

When `useGlobalPkgs = true`, overlays must be defined at the NixOS configuration level, not in Home Manager configuration files.

## When to Use

- Configuring NixOS with flakes and Home Manager
- Adding overlays that don't seem to apply
- Using `useGlobalPkgs = true` with custom overlays
- Structuring NixOS configurations across multiple hosts
- Package changes not appearing after rebuild
- Confused about where to define overlays

**Don't use for:**
- Packaging new software (use nix-packaging-best-practices)
- Simple package installation without overlays
- NixOS module development (see NixOS module documentation)

## Quick Reference

| Topic | Rule File |
|-------|-----------|
| Overlay scope and useGlobalPkgs | [overlay-scope](rules/overlay-scope.md) |
| Flakes configuration structure | [flakes-structure](rules/flakes-structure.md) |
| Host configuration organization | [host-organization](rules/host-organization.md) |
| Package installation best practices | [package-installation](rules/package-installation.md) |
| Common configuration mistakes | [common-mistakes](rules/common-mistakes.md) |
| Debugging configuration issues | [troubleshooting](rules/troubleshooting.md) |

## Essential Pattern: Overlay with useGlobalPkgs

```nix
# ❌ WRONG: Overlay in home.nix (doesn't apply)
# home-manager/home.nix
{
  nixpkgs.overlays = [ inputs.claude-code.overlays.default ];  # Ignored!
  home.packages = with pkgs; [ claude-code ];  # Not found!
}

# ✅ CORRECT: Overlay in NixOS home-manager block
# hosts/home/default.nix
{
  home-manager.useGlobalPkgs = true;
  home-manager.useUserPackages = true;
  home-manager.users.chumeng = import ./home.nix;
  home-manager.extraSpecialArgs = { inherit inputs pkgs-stable system; };
  # Overlay must be HERE when useGlobalPkgs = true
  nixpkgs.overlays = [ inputs.claude-code.overlays.default ];
}
```

## Common Tasks

| Task | Solution |
|------|----------|
| Add flake input | Add to `inputs` in flake.nix |
| Add overlay for system packages | Define in `nixpkgs.overlays` in system configuration |
| Add overlay for home-manager (useGlobalPkgs=true) | Define in `home-manager.nixpkgs.overlays` in host config |
| Add overlay for home-manager (useGlobalPkgs=false) | Define in `home.nix` with `nixpkgs.overlays` |
| Pass inputs to modules | Use `specialArgs` in nixosSystem or home-manager |
| Multiple host configurations | Create separate host files in `hosts/` |
| Shared configuration modules | Create modules in `modules/` and import in each host |
| Package not found after overlay | Check overlay scope vs useGlobalPkgs setting |

## Overlay Scope Decision Matrix

| useGlobalPkgs | Overlay Definition Location | Affects |
|---------------|---------------------------|---------|
| `true` | `home-manager.nixpkgs.overlays` | System + Home Manager packages |
| `true` | `home.nix` with `nixpkgs.overlays` | **Nothing** (ignored!) |
| `false` | `home.nix` with `nixpkgs.overlays` | Home Manager packages only |
| `false` | `home-manager.nixpkgs.overlays` | Home Manager packages only |
| Any | System `nixpkgs.overlays` | System packages only |

## Configuration Layers (Bottom to Top)

1. **System configuration** (`/etc/nixos/configuration.nix` or host files)
   - System-wide services
   - System packages
   - System overlays only affect this layer

2. **Home Manager (useGlobalPkgs=true)**
   - Uses system pkgs (includes system overlays)
   - Home Manager overlays affect both system and user packages
   - Most efficient for single-user systems

3. **Home Manager (useGlobalPkgs=false)**
   - Creates separate pkgs instance
   - Home Manager overlays affect user packages only
   - Useful for multi-user systems with different needs

## Red Flags - STOP

- "Overlay in home.nix isn't working" → Check if useGlobalPkgs=true, move to host config
- "I'll just add overlays everywhere" → Define once at appropriate scope
- "Package works in nix repl but not installed" → Check overlay scope
- "Changes don't apply after rebuild" → Verify overlay is in correct location
- "useGlobalPkgs=false for no reason" → Use true unless you need separate package sets

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/overlay-scope.md       # The core overlay scope issue
rules/flakes-structure.md    # How to organize flake.nix
rules/host-organization.md   # How to structure host configs
rules/common-mistakes.md     # Pitfalls and how to avoid them
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
