---
name: nixomatic
description: >-
  Maintains development environment instructions in the project README.md
  using nixomatic. When the user asks to build, compile, test, lint,
  format, type-check, run, or set up a project, or when a command fails
  because a tool or runtime is not installed, analyze project files to
  determine required packages and use nix develop with a nixomatic.com URL.
  Ensure the README.md documents how to reproduce the environment with
  both nix develop and docker run nixos/nix.
---

# Nixomatic Skill

## Overview

[Nixomatic](https://nixomatic.com) is a Nix flake generator service that creates reproducible development environments on-the-fly from URL parameters. Instead of writing and maintaining `flake.nix` files, you construct a URL like `https://nixomatic.com/?p=nodejs,python3` and pass it directly to `nix develop`. The service generates and serves a Nix flake with the requested packages -- no local Nix configuration or flake authoring required.

Use this skill whenever the user asks to build, compile, test, lint, format, type-check, run, or set up a project, or when a command fails because a tool or runtime is missing.

## Detecting Nix vs Docker

Before running any environment command, determine which runtime is available:

1. Check if `nix` is on PATH (`which nix`). If found, use Nix directly.
2. If `nix` is not found, check if `docker` is on PATH (`which docker`). If found, use the Docker wrapper.
3. If neither is available, inform the user that one of Nix or Docker must be installed and provide links:
   - Nix: https://nixos.org/download/
   - Docker: https://docs.docker.com/get-docker/

## Analyzing the Project

**Important:** Never read or access files that may contain secrets (`.env`, `.env.*`, `credentials.json`, `*-credentials.*`, `*.pem`, `*.key`, private key files, or token files). Only inspect filenames to determine which packages are needed — do not read file contents unless they are project manifests (e.g., `package.json`, `Cargo.toml`, `go.mod`).

Determine what packages the project needs by scanning files in this order:

1. **Check for existing nixomatic URL in README.md**: Look for a `## Development Environment` section containing a `nixomatic.com` URL. If found, reuse that URL as the baseline (it represents the last known-good package set). Add packages only if something is missing.

2. **Check for `flake.nix`**: If the project root contains a `flake.nix`, prefer the project's own flake over nixomatic. Run commands with `nix develop --command -- <cmd>` using the local flake. Do not generate a nixomatic URL in this case.

3. **Detect languages and runtimes** from project files:
   - `package.json` -> `nodejs`
   - `Cargo.toml` -> `rustc,cargo`
   - `go.mod` -> `go`
   - `requirements.txt`, `setup.py`, `pyproject.toml` -> `python3`
   - `Gemfile` -> `ruby`
   - `build.gradle`, `build.gradle.kts`, `pom.xml` -> `jdk`
   - `mix.exs` -> `elixir`
   - `*.sln`, `*.csproj`, `*.fsproj` -> `dotnet-sdk`
   - `composer.json` -> `php`
   - `Package.swift` -> `swift`
   - `dune-project`, `*.opam` -> `ocaml`
   - `stack.yaml`, `*.cabal` -> `ghc,cabal-install`
   - `pubspec.yaml` -> `dart`
   - `zig.zon`, `build.zig` -> `zig`

4. **Detect build tools**:
   - `Makefile` -> `gnumake`
   - `CMakeLists.txt` -> `cmake`
   - `meson.build` -> `meson`
   - `Justfile` -> `just`
   - `Taskfile.yml` -> `go-task`
   - `Rakefile` (without Gemfile) -> `ruby`

5. **Detect additional tools** from config files:
   - `.eslintrc*`, `eslint.config.*` -> (already covered by nodejs)
   - `Dockerfile` -> `docker`
   - `.terraform*` -> `terraform`
   - `serverless.yml` -> `nodejs`
   - `Makefile` containing `protoc` -> `protobuf`

## Common Package Mappings

| Project file / indicator       | Nix packages          |
|-------------------------------|-----------------------|
| `package.json`                | `nodejs`              |
| `Cargo.toml`                  | `rustc`, `cargo`      |
| `go.mod`                      | `go`                  |
| `requirements.txt`            | `python3`             |
| `pyproject.toml`              | `python3`             |
| `Gemfile`                     | `ruby`                |
| `pom.xml` / `build.gradle`   | `jdk`                 |
| `mix.exs`                     | `elixir`              |
| `composer.json`               | `php`                 |
| `*.csproj` / `*.fsproj`      | `dotnet-sdk`          |
| `Package.swift`               | `swift`               |
| `stack.yaml` / `*.cabal`     | `ghc`, `cabal-install`|
| `pubspec.yaml`                | `dart`                |
| `build.zig` / `zig.zon`      | `zig`                 |
| `Makefile`                    | `gnumake`             |
| `CMakeLists.txt`              | `cmake`               |
| `meson.build`                 | `meson`               |
| `Justfile`                    | `just`                |
| `Taskfile.yml`                | `go-task`             |
| `curl` needed                 | `curl`                |
| `git` needed                  | `git`                 |
| `jq` needed                   | `jq`                  |
| `openssl` needed              | `openssl`             |
| `pkg-config` needed           | `pkg-config`          |
| `protobuf` needed             | `protobuf`            |

## Constructing the URL

Build the nixomatic URL from the detected packages:

```
https://nixomatic.com/?p=pkg1,pkg2,pkg3
```

Use the short `p` query parameter with comma-separated package names. For example, a Node.js project with a Makefile becomes:

```
https://nixomatic.com/?p=nodejs,gnumake
```

To pin a specific package version, use `@version` syntax:

```
https://nixomatic.com/?p=nodejs@20.11.1,python3
```

To pin to a specific nixpkgs revision, use `:revision` syntax:

```
https://nixomatic.com/?p=python3:3b93cf5
```

## Command Templates

### Nix (direct)

Run a command inside the environment:

```bash
nix \
    --extra-experimental-features 'nix-command flakes' \
    develop 'https://nixomatic.com/?p=<packages>' \
      --accept-flake-config \
      --command -- <cmd>
```

Enter an interactive shell:

```bash
nix \
    --extra-experimental-features 'nix-command flakes' \
    develop 'https://nixomatic.com/?p=<packages>' \
      --accept-flake-config
```

### Docker

Run a command inside the environment:

```bash
docker run -v nix-store:/nix -v "$PWD:/workspace" -w /workspace --rm nixos/nix nix \
    --extra-experimental-features 'nix-command flakes' \
    develop 'https://nixomatic.com/?p=<packages>' \
      --accept-flake-config \
      --command -- <cmd>
```

Enter an interactive shell:

```bash
docker run -v nix-store:/nix -v "$PWD:/workspace" -w /workspace --rm -it nixos/nix nix \
    --extra-experimental-features 'nix-command flakes' \
    develop 'https://nixomatic.com/?p=<packages>' \
      --accept-flake-config
```

**Note:** The Docker commands include `-v "$PWD:/workspace" -w /workspace` to mount the current project directory into the container. This is essential for real project work so that build tools can access project files.

## Agent Workflow

Follow these steps when the user asks to build, test, lint, format, or set up a project:

1. **Check for `flake.nix`**: If the project has its own `flake.nix`, use it directly with `nix develop --command -- <cmd>`. Skip the remaining steps.

2. **Check README.md for existing URL**: Look for a `## Development Environment` section containing a `nixomatic.com/?p=` URL. If found, use that URL as the starting point.

3. **Analyze project files**: Scan the project root for language files, build tool configs, and other indicators. Determine the required package set using the mappings above.

4. **Construct the URL**: Build `https://nixomatic.com/?p=pkg1,pkg2,...` from the detected packages. If reusing a README URL, merge any new packages into it.

5. **Detect runtime**: Check for `nix` on PATH, then `docker`. Select the appropriate command template.

6. **Execute the command**: Run the user's requested operation (build, test, lint, etc.) inside the nixomatic environment using the appropriate command template.

7. **Handle missing packages**: If a command fails because a tool is not found (e.g., `command not found: cmake`), add the missing package to the URL and retry the command.

8. **Update README.md**: After a successful command execution, ensure the project's README.md contains an up-to-date `## Development Environment` section with the working nixomatic URL. See the README.md Maintenance section below.

## README.md Maintenance

After successfully running commands in a nixomatic environment, ensure the project's README.md documents how to reproduce it. This is the primary artifact of this skill.

### Finding or creating the section

- Search README.md for a `## Development Environment` heading that contains a `nixomatic.com` URL.
- If found, update the URL if the package set has changed.
- If not found, append the section to the end of README.md (before any final sections like "License" or "Contributing" if they exist).

### Section template

Use this template for the Development Environment section. Replace `<packages>` with the actual comma-separated package list:

````markdown
## Development Environment

This project uses [nixomatic](https://nixomatic.com) for reproducible development environments.

### Using Nix

```bash
nix \
    --extra-experimental-features 'nix-command flakes' \
    develop 'https://nixomatic.com/?p=<packages>' \
      --accept-flake-config
```

### Using Docker

```bash
docker run -v nix-store:/nix -v "$PWD:/workspace" -w /workspace --rm -it nixos/nix nix \
    --extra-experimental-features 'nix-command flakes' \
    develop 'https://nixomatic.com/?p=<packages>' \
      --accept-flake-config
```
````

### Keeping the URL in sync

- When packages are added (e.g., a missing tool was discovered), update the URL in the README.md section.
- When packages are removed (e.g., a dependency was dropped), update the URL accordingly.
- Always use the same URL in both the Nix and Docker command blocks.

## Security Considerations

- **Nix sandbox:** Nix builds run inside a sandbox by default — build-time derivations have no network access and no filesystem access outside the Nix store. The `nix develop` command only makes packages available on `PATH`; it does not execute arbitrary scripts at evaluation time.
- **Deterministic flakes:** nixomatic.com serves deterministic Nix flakes generated from the requested package list. The flake only pulls packages from the official nixpkgs repository.
- **Docker isolation:** When using the Docker runtime, the container only has access to the mounted workspace directory and a persistent Nix store volume. No other host paths are exposed.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: <tool>` | Package missing from URL | Add the package to the `p=` parameter and retry |
| `error: unable to download` | Network issue or invalid URL | Check internet connectivity and verify the URL is well-formed |
| `error: flake has no attribute` | Unknown package name | Verify the package name exists in nixpkgs (search at https://search.nixos.org/packages) |
| `docker: command not found` | Docker not installed | Fall back to Nix, or ask user to install Docker |
| `nix: command not found` | Nix not installed | Fall back to Docker, or ask user to install Nix |
| `error: experimental Nix feature 'flakes' is disabled` | Old Nix without flakes flag | The `--extra-experimental-features 'nix-command flakes'` flag should handle this; if not, the user needs to update Nix |
| Permission denied on Docker socket | User not in docker group | The user must have permission to access the Docker daemon; ask them to verify their Docker setup |
