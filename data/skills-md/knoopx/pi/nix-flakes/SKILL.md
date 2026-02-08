---
name: nix-flakes
description: Creates reproducible builds, manages flake inputs, defines devShells, and builds packages with flake.nix. Use when initializing Nix projects, locking dependencies, or running nix build/develop commands.
---

# Nix Flakes

Modern Nix project management with hermeticity and reproducibility through flake.lock.

## Core Commands

### Project Management

```bash
# Initialize a new flake in the current directory
nix flake init

# Create a new flake from template
nix flake new hello -t templates#hello

# Update flake.lock (updates all inputs)
nix flake update

# Update specific input only
nix flake update nixpkgs

# Lock without updating (create missing entries)
nix flake lock

# Check flake for syntax and common errors
nix flake check

# Show flake outputs
nix flake show

# Show flake metadata (inputs, revisions)
nix flake metadata path:.
nix flake info path:.  # Alias for metadata

# Prefetch flake and inputs into store
nix flake prefetch github:NixOS/nixpkgs
nix flake prefetch-inputs path:.

# Clone flake repository
nix flake clone nixpkgs --dest ./nixpkgs
```

### Running and Building

Always prefix local flake paths with `path:` (e.g., `path:.`) to ensure Nix uses all files in the directory without requiring them to be staged in Git.

```bash
# Build the default package
nix build path:.

# Build a specific output
nix build path:.#packageName

# Run the default app
nix run path:.

# Run a specific app from a flake
nix run path:.#appName

# Run an app from a remote flake
nix run github:numtide/treefmt
```

### Development Environments

In a headless environment, use `nix develop` with `--command` to run tasks within the environment.

```bash
# Run a command inside the devShell
nix develop path:. --command make build

# Check if current environment matches devShell
nix develop path:. --command env
```

## Flake Structure (`flake.nix`)

A basic `flake.nix` pattern:

```nix
{
  description = "A basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      packages.${system}.default = pkgs.hello;

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [ pkgs.git pkgs.vim ];
      };
    };
}
```

## Best Practices

- **Locking**: Manage the `flake.lock` file to ensure reproducibility.
- **Purity**: Flakes are "pure" by default. They cannot access files outside the flake directory unless they are tracked (e.g. in the git tree if using git).
- **Non-Interactive**: When using `nix develop`, always use the `--command` flag to ensure scripts remain non-interactive.

## Debugging Flakes

```bash
# Inspect inputs
nix flake metadata path:.

# Evaluate a specific output
nix eval path:.#packages.x86_64-linux.default.name
```

## Related Skills

- **nix**: Run applications without installation and create development environments using Nix.
- **nh**: Manage NixOS and Home Manager operations with improved output using nh.

## Related Tools

- **search-nix-packages**: Search for packages available in the NixOS package repository when working with flakes.
- **search-nix-options**: Find configuration options available in NixOS for flake configurations.
- **search-home-manager-options**: Find configuration options for Home Manager in flake setups.
