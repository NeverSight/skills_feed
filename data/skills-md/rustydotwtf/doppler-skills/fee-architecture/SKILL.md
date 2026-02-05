---
name: fee-architecture
description: Reference for Doppler fee collection, distribution, and configuration. Covers LP fees, protocol fees, integrator fees, beneficiary distribution, and dynamic fee modes.
metadata:
  author: doppler
  version: "1.0"
---

> **Source References**: Code citations link to raw GitHub files pinned to commit `988dab4`. To fetch specific lines: `curl -s "<url>" | sed -n 'START,ENDp'`

# Fee Architecture

Reference for Doppler fee collection, distribution, and configuration.

---

## Overview

Doppler implements a multi-layer fee system:

1. **LP Fees**: Trading fees collected during swaps (configurable per pool)
2. **Protocol Fees**: Whetstone's cut from LP fees (5% of fees or 0.1% of proceeds)
3. **Integrator Fees**: Front-end integrator's share (remainder of LP fees)
4. **Beneficiary Fees**: Distribution to locked pool beneficiaries

---

## Quick Facts

| Fee Type | Rate | Recipient | When Collected |
|----------|------|-----------|----------------|
| LP Fees | Configurable (0-100%) | Pool | Every swap |
| Protocol Fees | 5% of LP fees OR 0.1% of proceeds | Whetstone | Migration |
| Integrator Fees | Remainder of LP fees | Integrator | Migration |
| Beneficiary Fees | Share-based (WAD) | Beneficiaries | On demand |

---

## Fee Modes

| Mode | Description | Pool Type |
|------|-------------|-----------|
| **Standard** | Fixed fee set at pool creation | V3 pools, V4 without hook |
| **Dynamic** | Hook can modify fee per swap | V4 with Doppler hook |

---

## Key Contracts

| Contract | Purpose | Source |
|----------|---------|--------|
| `Airlock` | Protocol/integrator fee handling | `src/Airlock.sol` |
| `FeesManager` | Beneficiary fee tracking | `src/base/FeesManager.sol` |
| `StreamableFeesLocker` | Position-based fee streaming (V1) | `src/StreamableFeesLocker.sol` |
| `StreamableFeesLockerV2` | Pool-based fee streaming (V2) | `src/StreamableFeesLockerV2.sol` |

---

## Common Tasks

### Check protocol fees
```solidity
uint256 fees = airlock.getProtocolFees(tokenAddress);
```

### Check integrator fees
```solidity
uint256 fees = airlock.getIntegratorFees(integratorAddress, tokenAddress);
```

### Collect beneficiary fees
```solidity
// For FeesManager-based contracts
feesManager.collectFees(poolId);
```

---

## References

- [COLLECTION.md](references/COLLECTION.md) - FeesManager and beneficiary tracking
- [DISTRIBUTION.md](references/DISTRIBUTION.md) - Protocol/integrator fee split
- [DYNAMIC-FEES.md](references/DYNAMIC-FEES.md) - Dynamic vs standard fees

---

## Related Skills

- [v4-dynamic-auction](../v4-dynamic-auction/SKILL.md) - Dynamic fee hooks
- [v4-multicurve-auction](../v4-multicurve-auction/SKILL.md) - Locked pools with beneficiaries
- [token-lifecycle](../token-lifecycle/SKILL.md) - Token vesting and inflation
