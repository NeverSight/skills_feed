---
name: docker-test
description: Test voxtype in Docker containers. Use for testing builds, verifying packages work on different distros, or isolating test environments.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Docker Test

Test voxtype builds and packages in isolated Docker containers.

## Build Testing

### Build AVX2 Binary (Clean Toolchain)

Uses Ubuntu 22.04 to avoid AVX-512 instruction contamination:

```bash
./scripts/build-docker.sh
```

Output: `releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx2`

### Build Vulkan Binary

Uses remote Docker context (pre-AVX-512 CPU) for clean build:

```bash
./scripts/build-docker-vulkan.sh
```

Output: `releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-vulkan`

### Full Docker Compose Build

```bash
VERSION=0.4.14 docker compose -f docker-compose.build.yml build --no-cache avx2 vulkan
VERSION=0.4.14 docker compose -f docker-compose.build.yml up avx2 vulkan
```

## Package Testing

### Test Debian Package

```bash
# Build test container
docker run -it --rm -v $(pwd)/releases:/releases ubuntu:22.04 bash

# Inside container:
apt update && apt install -y /releases/0.4.14/voxtype_0.4.14-1_amd64.deb
voxtype --version
voxtype --help
```

### Test RPM Package

```bash
# Fedora
docker run -it --rm -v $(pwd)/releases:/releases fedora:latest bash

# Inside container:
dnf install -y /releases/0.4.14/voxtype-0.4.14-1.x86_64.rpm
voxtype --version
```

## Distro-Specific Testing

### Ubuntu/Debian

```bash
docker run -it --rm ubuntu:22.04 bash -c "
  apt update &&
  apt install -y curl libasound2 &&
  curl -L https://github.com/peteonrails/voxtype/releases/download/v0.4.14/voxtype-0.4.14-linux-x86_64-avx2 -o /usr/bin/voxtype &&
  chmod +x /usr/bin/voxtype &&
  voxtype --version
"
```

### Fedora

```bash
docker run -it --rm fedora:latest bash -c "
  dnf install -y alsa-lib curl &&
  curl -L https://github.com/peteonrails/voxtype/releases/download/v0.4.14/voxtype-0.4.14-linux-x86_64-avx2 -o /usr/bin/voxtype &&
  chmod +x /usr/bin/voxtype &&
  voxtype --version
"
```

### Arch Linux

```bash
docker run -it --rm archlinux:latest bash -c "
  pacman -Sy --noconfirm base-devel git &&
  # Test AUR package build
  git clone https://aur.archlinux.org/voxtype-bin.git &&
  cd voxtype-bin &&
  makepkg -si --noconfirm
"
```

## Docker Context Management

For builds requiring a pre-AVX-512 CPU:

```bash
# List contexts
docker context ls

# Switch to remote build server
docker context use truenas

# Build clean binaries
docker compose -f docker-compose.build.yml up avx2 vulkan

# Switch back to local
docker context use default
```

## Troubleshooting

**Build cache issues:**
```bash
docker compose -f docker-compose.build.yml build --no-cache
```

**Container won't start:**
Check if audio devices are needed - voxtype requires ALSA/PipeWire which may not be available in containers.

**Version mismatch after build:**
Docker cached old layers. Always use `--no-cache` for release builds.
