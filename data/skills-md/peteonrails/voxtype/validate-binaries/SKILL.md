---
name: validate-binaries
description: Validate voxtype binaries for CPU instruction contamination. Use when checking release binaries for AVX-512 or GFNI instruction leaks that would crash on older CPUs.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Validate Binaries

Verify that voxtype binaries don't contain forbidden CPU instructions that would cause crashes on older CPUs.

## What This Checks

| Binary | Must NOT have | Must have |
|--------|---------------|-----------|
| AVX2 | zmm registers, AVX-512 EVEX, GFNI | - |
| Vulkan | zmm registers, AVX-512 EVEX, GFNI | - |
| AVX-512 | - | zmm registers (confirms optimization) |

## Forbidden Instructions

- `zmm` registers - 512-bit AVX-512 registers
- `vpternlog`, `vpermt2`, `vpblendm` - AVX-512 specific
- `{1to4}`, `{1to8}`, `{1to16}` - AVX-512 broadcast syntax
- `vgf2p8`, `gf2p8` - GFNI instructions (not on Zen 3)

## Usage

When asked to validate binaries:

1. Determine the version from context or ask
2. Find binaries in `releases/${VERSION}/`
3. Run objdump checks on each binary
4. Report pass/fail for each

## Validation Commands

```bash
# Set version
VERSION=0.4.14

# Check AVX2 binary (should be 0 for all)
echo "=== AVX2 Binary ==="
objdump -d releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx2 | grep -c zmm || echo "zmm: 0"
objdump -d releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx2 | grep -cE 'vpternlog|vpermt2|vpblendm' || echo "AVX-512 ops: 0"
objdump -d releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx2 | grep -cE 'vgf2p8|gf2p8' || echo "GFNI: 0"

# Check Vulkan binary (should be 0 for all)
echo "=== Vulkan Binary ==="
objdump -d releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-vulkan | grep -c zmm || echo "zmm: 0"
objdump -d releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-vulkan | grep -cE 'vgf2p8|gf2p8' || echo "GFNI: 0"

# Check AVX-512 binary (should be > 0)
echo "=== AVX-512 Binary ==="
objdump -d releases/${VERSION}/voxtype-${VERSION}-linux-x86_64-avx512 | grep -c zmm
```

## Interpreting Results

**PASS conditions:**
- AVX2: All counts are 0
- Vulkan: All counts are 0
- AVX-512: zmm count > 0

**FAIL conditions:**
- AVX2 or Vulkan has any zmm/GFNI instructions
- AVX-512 has 0 zmm instructions (not optimized)

If validation fails, the Docker build cache is likely stale. Recommend:
```bash
docker compose -f docker-compose.build.yml build --no-cache avx2 vulkan
```
