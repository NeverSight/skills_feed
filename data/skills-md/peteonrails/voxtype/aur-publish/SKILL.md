---
name: aur-publish
description: Publish voxtype to AUR. Updates PKGBUILD, generates checksums, and pushes to AUR. Use after a GitHub release is published.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
---

# AUR Publish

Update and publish voxtype packages to the Arch User Repository.

## Packages

| Package | Type | Location |
|---------|------|----------|
| `voxtype` | Source build | `packaging/arch/` |
| `voxtype-bin` | Pre-built binaries | `packaging/arch-bin/` |

## Prerequisites

- GitHub release already published with binaries
- GPG key configured: `E79F5BAF8CD51A806AA27DBB7DA2709247D75BC6`

## Workflow for voxtype-bin

### 1. Generate SHA256 checksums

Download binaries from GitHub release and generate checksums:

```bash
VERSION=0.4.14
cd releases/${VERSION}

sha256sum voxtype-${VERSION}-linux-x86_64-avx2
sha256sum voxtype-${VERSION}-linux-x86_64-avx512
sha256sum voxtype-${VERSION}-linux-x86_64-vulkan
```

### 2. Update PKGBUILD

Edit `packaging/arch-bin/PKGBUILD`:
- Update `pkgver` to new version
- Reset `pkgrel` to 1
- Update `sha256sums` array with new checksums

### 3. Generate .SRCINFO

```bash
cd packaging/arch-bin
makepkg --printsrcinfo > .SRCINFO
```

### 4. Test locally

```bash
makepkg -si
```

### 5. Commit and push to AUR

```bash
cd packaging/arch-bin
git add PKGBUILD .SRCINFO
git commit -S -m "Update to ${VERSION}"
git push
```

## Important Rules

**Always bump `pkgver`, never just `pkgrel` when binaries change.**

The download URLs include `pkgver`:
```
https://github.com/peteonrails/voxtype/releases/download/v$pkgver/voxtype-$pkgver-linux-x86_64-avx2
```

If only `pkgrel` changes, the URL stays the same and AUR helpers cache the old file.

**Never re-upload different binaries to an existing GitHub release.**

This causes checksum mismatches for users with cached PKGBUILDs.

## Checklist

- [ ] GitHub release exists with correct binaries
- [ ] Binaries verified (version check, instruction validation)
- [ ] `pkgver` updated in PKGBUILD
- [ ] `pkgrel` reset to 1
- [ ] SHA256 checksums updated
- [ ] `.SRCINFO` regenerated
- [ ] Local `makepkg -si` succeeds
- [ ] Committed with signed commit
- [ ] Pushed to AUR
