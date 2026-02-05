---
name: wendy-contributing
description: 'Expert guidance on contributing to WendyOS: Yocto builds, agent internals, E2E testing, and system architecture. Use when developers mention: (1) building WendyOS images, (2) meta-wendyos layers or bitbake, (3) wendy-agent development or internals, (4) containerd or nerdctl on WendyOS, (5) E2E tests for wendy-agent, (6) Yocto recipes or bbappend files, (7) mDNS/Avahi service configuration, (8) device identity or UUID generation.'
references:
  - yocto-meta-layers.md
  - system-internals.md
  - raspberry-pi.md
---

# WendyOS Contributing

This skill covers internal development and contribution to WendyOS itself, including building OS images, understanding agent architecture, and running E2E tests.

## Overview

WendyOS is an Embedded Linux operating system for edge computing built with Yocto. It supports:
- NVIDIA Jetson devices (production with OTA updates)
- Raspberry Pi 4/5 (edge devices)
- ARM64 VMs (development)

## Agent Architecture

The `wendy-agent` is a container daemon (similar to `dockerd`/`containerd`):
- Manages container lifecycle via gRPC on port 50051
- Images are pushed via `wendy run`, not pulled from Docker Hub
- There's no `docker pull` equivalent - apps are deployed from source

## Building WendyOS (Yocto)

WendyOS images are built with Yocto. Three meta layers exist:

| Layer | Target | Image |
|-------|--------|-------|
| `meta-wendyos-jetson` | NVIDIA Jetson | `edgeos-image` |
| `meta-wendyos-virtual` | ARM64 VM | `edgeos-vm-image` |
| `meta-wendyos-rpi` | Raspberry Pi 4/5 | `edgeos-rpi-image` |

Quick build (any layer):
```bash
cd meta-wendyos-<target>
./bootstrap.sh
source ./repos/poky/oe-init-build-env build
bitbake <image-name>
```

For macOS, use the Docker build environment:
```bash
cd docker && ./docker-util.sh shell
```

See `references/yocto-meta-layers.md` for detailed Yocto configuration.

## E2E Testing

The `wendy-agent` repository includes an E2E test suite in `E2ETests/`.

### Running E2E Tests
```bash
# Start the VM
cd meta-wendyos-virtual
./scripts/setup-dev-vm.sh create && ./scripts/setup-dev-vm.sh start

# Deploy a test app first (required for container tests)
cd wendy-agent/Examples/HelloWorld
wendy run --json --device localhost:50051  # --json for non-interactive output

# Run E2E tests with fast path (CRITICAL for performance)
cd wendy-agent/E2ETests
E2E_USE_EXISTING_VM=true E2E_VM_PATH=/path/to/meta-wendyos-virtual swift test
```

**Important**: Always set `E2E_USE_EXISTING_VM=true` when the VM is already running. This skips shell script checks and reduces test time from ~5s/test to ~0.01s/test.

**Tip**: Use `--json` flag on all wendy commands for quick JSON responses without interactive polling.

### Test Performance Tips
- Use `.serialized` trait on test suites to avoid VM race conditions
- Set `E2E_USE_EXISTING_VM=true` to skip redundant VM status checks
- mDNS discovery tests take ~5s each (inherent to protocol)
- Container state change tests can be slow - disable for quick runs
- Don't use `Issue.record()` for expected failures (like WiFi in VM) - it counts as failure

### CI Limitations
GitHub-hosted runners don't support nested virtualization. Use self-hosted runners or run E2E tests locally.

### Test Suites
| Suite | Tests | Time | Notes |
|-------|-------|------|-------|
| Device Connection | 7 | ~0.07s | gRPC connectivity |
| Container Deployment | 6 | ~0.06s | Container lifecycle |
| WiFi Operations | 4 | ~0.04s | Graceful failures in VM |
| Hardware Capabilities | 4 | ~0.07s | Device enumeration |
| Device Discovery | 4 | ~21s | mDNS (slow by design) |

## System Internals

For debugging, container runtime details (containerd/nerdctl), mDNS discovery, device identity, and common pitfalls, see `references/system-internals.md`.

For Raspberry Pi specific configuration (serial console, flashing, partition layout), see `references/raspberry-pi.md`.

## Reference Files

Load these files as needed for specific topics:

- **`references/yocto-meta-layers.md`** - Yocto layer structure, build configuration, partition layouts, Docker build environment, common issues
- **`references/system-internals.md`** - containerd runtime, containerd-registry, device identity, mDNS configuration, Lima VM development, offline image bundling
- **`references/raspberry-pi.md`** - RPi machine configuration, serial console, flashing images, partition layout
