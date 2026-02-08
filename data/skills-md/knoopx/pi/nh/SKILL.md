---
name: nh
description: Switches NixOS/Home Manager configurations, cleans old generations, and performs system maintenance. Use when running os/home switch, pruning the Nix store, or managing system generations.
---

# nh (Nix Helper)

CLI tool that simplifies Nix operations with cleaner interface for builds, switches, and garbage collection.

## Core Commands

### System Updates (NixOS)

Use `nh os` for managing NixOS configurations. Prefix local paths with `path:`.

```bash
# Build and switch to a configuration (equivalent to nixos-rebuild switch)
nh os switch path:.

# Build and test a configuration (equivalent to nixos-rebuild test)
nh os test path:.

# Build a configuration without switching (equivalent to nixos-rebuild build)
nh os build path:.

# Make configuration the boot default without activating
nh os boot path:.

# Rollback to a previous generation
nh os rollback

# List available generations
nh os info

# Build a NixOS VM image
nh os build-vm path:.

# Load system configuration in a REPL (use tmux for interactive)
tmux new -d -s nh-repl 'nh os repl path:.'
```

### Home Manager Updates

Use `nh home` for managing Home Manager configurations.

```bash
# Build and switch Home Manager configuration
nh home switch path:.

# Build Home Manager configuration without switching
nh home build path:.

# Load Home Manager configuration in a REPL (use tmux for interactive)
tmux new -d -s hm-repl 'nh home repl path:.'
```

### Nix-Darwin (macOS)

Use `nh darwin` for managing nix-darwin configurations on macOS.

```bash
# Build and switch darwin configuration
nh darwin switch path:.

# Build darwin configuration without switching
nh darwin build path:.
```

### Package Search

Search for packages using search.nixos.org:

```bash
# Search for packages
nh search ripgrep
```

### Maintenance and Cleanup

`nh clean` provides a more intuitive way to manage the Nix store and generations.

```bash
# Clean all profiles (system + user)
nh clean all --keep-since 7d

# Clean only current user's profiles
nh clean user --keep 5

# Clean a specific profile
nh clean profile /nix/var/nix/profiles/system --keep 3

# Run garbage collection on the Nix store
nh clean all
```

## Common Options

- `--ask`: Ask for confirmation before performing actions (Avoid in headless/automated scripts).
- `--dry`: Show what would happen without making changes.
- `--update`: Update flake inputs before building.

## Best Practices

- **Headless Usage**: Avoid using the `--ask` flag in scripts or automated environments as it requires user interaction.
- **Path Inference**: `nh` automatically looks for a `flake.nix` in the current directory if no path is provided.
- **Visuals**: `nh` provides a more readable "Nom-like" output by default, which is helpful for monitoring build progress in a terminal.

## Related Skills

- **nix**: Use Nix for running applications without installation and evaluating Nix expressions.
- **nix-flakes**: Leverage Nix Flakes for reproducible builds and project isolation with nh.
