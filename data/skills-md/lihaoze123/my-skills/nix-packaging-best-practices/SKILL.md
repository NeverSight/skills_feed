---
name: nix-packaging-best-practices
description: Best practices for packaging pre-compiled binaries (.deb, .rpm, .tar.gz, AppImage) for NixOS, handling library dependencies, or facing "library not found" errors with binary distributions
license: MIT
metadata:
  author: chumeng
  version: "1.0.0"
---

# Packaging Binary Distributions for Nix

Extract and patch binary packages within Nix builds for reproducibility.

## Core Principle

**Source from original archive directly, never from pre-extracted directories.**

## When to Use

- Converting binary packages (.deb, .rpm, .tar.gz, .zip) to Nix derivations
- Packaging proprietary/closed-source software distributed as binaries
- Electron/GUI apps show "library not found" errors
- User provides pre-extracted binary contents
- Binary distributions need library path fixes

**Don't use for:**
- Software available in nixpkgs
- Source-based packages (use standard derivation)
- AppImages (use appimage-run or extract and patch)

## Quick Reference

| Topic | Rule File |
|-------|-----------|
| Core pattern for .deb packages | [essential-pattern](rules/essential-pattern.md) |
| .rpm, .tar.gz, .zip extraction | [archive-formats](rules/archive-formats.md) |
| nativeBuildInputs vs buildInputs | [dependencies](rules/dependencies.md) |
| Local vs remote source files | [source-files](rules/source-files.md) |
| Common pitfalls and fixes | [common-mistakes](rules/common-mistakes.md) |
| Finding missing libraries with ldd | [finding-libraries](rules/finding-libraries.md) |
| Quick testing with steam-run | [quick-testing](rules/quick-testing.md) |
| Troubleshooting autoPatchelf errors | [troubleshooting-autoPatchelf](rules/troubleshooting-autoPatchelf.md) |
| Version variable in filename | [version-management](rules/version-management.md) |
| Electron app dependencies | [electron-apps](rules/electron-apps.md) |
| FHS env for resistant binaries | [advanced-fhs-env](rules/advanced-fhs-env.md) |
| Build phases and hooks | [build-phases](rules/build-phases.md) |
| Wrapper scripts with makeWrapper | [wrapper-programs](rules/wrapper-programs.md) |

## Essential Pattern (.deb)

```nix
{ pkgs }:

pkgs.stdenv.mkDerivation rec {
  pname = "appname";
  version = "1.0.0";

  src = ./AppName-${version}-linux-amd64.deb;

  nativeBuildInputs = with pkgs; [
    autoPatchelfHook  # Fixes library paths
    dpkg              # Extracts .deb
  ];

  buildInputs = with pkgs; [
    stdenv.cc.cc.lib
    glib
    gtk3
  ];

  unpackPhase = ''
    ar x $src
    tar xf data.tar.xz
  '';

  installPhase = ''
    mkdir -p $out
    cp -r opt/AppName/* $out/
  '';
}
```

## Common Tasks

| Task | Solution |
|------|----------|
| Local archive | `src = ./package-${version}.tar.gz` |
| Remote archive | `src = fetchurl { url = "..."; hash = "sha256-..."; }` |
| Extract .deb | `ar x $src && tar xf data.tar.xz` + dpkg |
| Extract .rpm | `rpm2cpio $src \| cpio -idmv` + rpm, cpio |
| Extract .tar.gz | Auto-detected by stdenv |
| Extract .zip | Add `unzip` to nativeBuildInputs |
| Fix libraries | Add `autoPatchelfHook` to nativeBuildInputs |
| Find missing libs | Run `ldd result/bin/app` for "not found" |
| Quick test binary | `nix-shell -p steam-run; steam-run ./binary` |
| Debug autoPatchelf | `nix log /nix/store/...-drv` |
| Search libraries | `nix-locate libX11.so.6` |
| Wrapper scripts | Add `makeWrapper` to nativeBuildInputs |
| Version sync | Use `src = ./app-${version}.tar.gz` |

## Dependency Categories

**nativeBuildInputs**: Build-time tools (dpkg, autoPatchelfHook, makeWrapper)
**buildInputs**: Runtime libraries (gtk3, glib, libpulseaudio)
**propagatedBuildInputs**: Rarely needed for binary packaging

## Common Library Mappings

| Missing Library | Nix Package |
|-----------------|-------------|
| `libgtk-3.so.0` | `gtk3` |
| `libglib-2.0.so.0` | `glib` |
| `libpulse.so.0` | `libpulseaudio` |
| `libGL.so.1` | `mesa` or `libglvnd` |
| `libxkbcommon.so.0` | `libxkbcommon` (NOT xorg.libxkbcommon) |
| `libstdc++.so.6` | `stdenv.cc.cc.lib` |

## Red Flags - STOP

- "User already extracted it, use that directory" → NO, source from original archive
- "Absolute path works for me locally" → Breaks for others, use relative
- "Just add more libraries until it works" → Find actual dependencies with `ldd`

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/essential-pattern.md
rules/archive-formats.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
