---
name: package-release
description: Package voxtype for release. Creates deb and rpm packages from binaries. Use when building distribution packages.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Package Release

Build distribution packages (deb, rpm) for voxtype releases.

## Prerequisites

- `fpm` - Install with `gem install fpm`
- `rpmbuild` - Install with `sudo dnf install rpm-build` or `sudo pacman -S rpm-tools`
- Pre-built binaries in `releases/${VERSION}/`

## Quick Package

If binaries already exist:

```bash
./scripts/package.sh --skip-build ${VERSION}
```

## Full Build + Package

Build binaries and create packages:

```bash
./scripts/package.sh ${VERSION}
```

## Options

| Flag | Description |
|------|-------------|
| `--skip-build` | Use existing binaries, don't rebuild |
| `--deb-only` | Build only Debian package |
| `--rpm-only` | Build only RPM package |
| `--no-validate` | Skip package validation |
| `--release N` | Set package release number (default: 1) |
| `--arch ARCH` | Target architecture: x86_64 or aarch64 |

## Output

Packages are created in `releases/${VERSION}/`:
- `voxtype_${VERSION}-1_amd64.deb`
- `voxtype-${VERSION}-1.x86_64.rpm`

## Validation

The script automatically:
1. Validates binaries for CPU instruction contamination
2. Checks deb package structure for duplicate fields
3. Verifies required control file fields

## Workflow

1. Build binaries (Docker for AVX2/Vulkan, local for AVX-512)
2. Verify binary versions match expected version
3. Run `./scripts/package.sh --skip-build ${VERSION}`
4. Test package installation in a VM or container

## Common Issues

**Binary not found:**
```
Error: Binary not found: releases/0.4.14/voxtype-0.4.14-linux-x86_64-avx2
```
Build binaries first or check the version number.

**fpm not found:**
```bash
gem install fpm
```

**Validation failed:**
Check the specific error. Usually means Docker cache is stale.
