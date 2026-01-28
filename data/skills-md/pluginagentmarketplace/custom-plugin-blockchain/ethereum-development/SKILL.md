---
name: ethereum-development
description: Master Ethereum development including EVM, gas optimization, and client interactions
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 02-ethereum-development
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: ethereum_development

# Parameter Validation
parameters:
  topic:
    type: string
    required: true
    enum: [evm, gas, transactions, clients, debugging]
  network:
    type: string
    default: mainnet
    enum: [mainnet, sepolia, holesky, local]

# Retry & Error Handling
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

# Logging & Observability
logging:
  level: info
  include_timestamps: true
  track_usage: true
---

# Ethereum Development Skill

> Master Ethereum development including EVM internals, gas optimization, transaction mechanics, and client interactions.

## Quick Start

```python
# Invoke this skill for Ethereum development
Skill("ethereum-development", topic="gas", network="mainnet")
```

## Topics Covered

### 1. EVM (Ethereum Virtual Machine)
Understand the execution environment:
- **Stack Machine**: 256-bit words, 1024 depth
- **Memory**: Linear byte array, expansion costs
- **Storage**: Persistent key-value, 32-byte slots
- **Opcodes**: Costs, effects, gas consumption

### 2. Gas Optimization
Reduce transaction costs:
- **Storage Packing**: Fit multiple values in one slot
- **Calldata vs Memory**: Choose efficiently
- **Loop Optimization**: Cache storage reads
- **Custom Errors**: Save gas on reverts

### 3. Transaction Mechanics
Master transaction lifecycle:
- **Types**: Legacy (0), Access List (1), EIP-1559 (2)
- **Fee Estimation**: Base fee, priority fee, max fee
- **Nonce Management**: Sequential ordering
- **Receipts**: Status, logs, gas used

### 4. Client Interactions
Work with Ethereum nodes:
- **RPC Methods**: eth_, debug_, trace_
- **State Queries**: Storage slots, code, balance
- **Event Subscriptions**: Filter logs, topics

## Code Examples

### Gas-Efficient Storage
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Optimized {
    // Pack into single slot (32 bytes)
    struct User {
        uint128 balance;    // 16 bytes
        uint64 lastUpdate;  // 8 bytes
        uint32 nonce;       // 4 bytes
        bool active;        // 1 byte
        // 3 bytes padding
    }

    mapping(address => User) public users;
}
```

### Read Storage Slot
```typescript
import { createPublicClient, http, keccak256, encodePacked, pad } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({ chain: mainnet, transport: http() });

// Read mapping value: balances[address]
async function getBalance(contract: `0x${string}`, user: `0x${string}`) {
  const slot = keccak256(encodePacked(['address', 'uint256'], [user, 0n]));
  return await client.getStorageAt({ address: contract, slot });
}
```

### EIP-1559 Transaction
```typescript
import { createWalletClient, http, parseEther } from 'viem';

const client = createWalletClient({ transport: http() });

const hash = await client.sendTransaction({
  to: '0x...',
  value: parseEther('0.1'),
  type: 'eip1559',
  maxFeePerGas: parseGwei('30'),
  maxPriorityFeePerGas: parseGwei('2'),
});
```

## Gas Optimization Cheatsheet

| Technique | Savings | Example |
|-----------|---------|---------|
| Storage packing | ~20k/slot | `uint128 + uint128` in one slot |
| Calldata vs memory | ~3/byte | Use `calldata` for read-only |
| Unchecked math | ~80/op | `unchecked { i++; }` |
| Custom errors | ~200+ | `error Unauthorized()` |
| Short-circuit | Variable | Cheap checks first |

## Common Pitfalls

| Pitfall | Issue | Solution |
|---------|-------|----------|
| Storage in loops | Expensive reads | Cache in memory first |
| String storage | Uses multiple slots | Use bytes32 when possible |
| Zero value storage | Full refund gone | Don't rely on SSTORE refunds |

## Troubleshooting

### "Transaction underpriced"
```bash
# Check current gas prices
cast gas-price --rpc-url $RPC
cast basefee --rpc-url $RPC
```
Set `maxFeePerGas` to at least 2x current base fee.

### "Out of gas"
```bash
# Trace transaction to find issue
cast run --trace $TX_HASH --rpc-url $RPC
```

### "Nonce too low"
```bash
# Get current nonce
cast nonce $ADDRESS --rpc-url $RPC
```

## CLI Commands

```bash
# Foundry essentials
forge build --sizes          # Contract sizes
forge test --gas-report      # Gas consumption
forge snapshot               # Gas snapshots
cast storage $ADDR $SLOT     # Read storage
cast call $ADDR "fn()"       # Simulate call
```

## Test Template

```solidity
contract GasTest is Test {
    function test_GasOptimization() public {
        uint256 gasBefore = gasleft();
        target.optimizedFunction();
        uint256 gasUsed = gasBefore - gasleft();

        assertLt(gasUsed, 50000, "Too much gas used");
    }
}
```

## Cross-References

- **Bonded Agent**: `02-ethereum-development`
- **Related Skills**: `solidity-development`, `web3-frontend`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with viem, gas optimization |
| 1.0.0 | 2024-12 | Initial release |
