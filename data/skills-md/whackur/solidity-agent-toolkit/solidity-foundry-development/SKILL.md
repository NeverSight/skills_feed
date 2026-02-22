---
name: solidity-foundry-development
description: Foundry development workflow for Solidity smart contracts. Use when building, testing, or deploying with Foundry (forge, cast, anvil). Covers project setup, foundry.toml configuration, testing patterns, fuzz testing, invariant testing, fork testing, cheatcodes, deployment scripts, and debugging. Triggers on tasks involving forge build, forge test, forge script, cast, anvil, or Foundry-based Solidity development.
license: MIT
metadata:
  author: whackur
  version: "0.5.3"
---

# Foundry Development Guide

## When to Apply

Apply this skill when working on Solidity projects using the Foundry toolkit. This includes setting up new projects, writing unit and integration tests, performing fuzz and invariant testing, simulating mainnet conditions via fork testing, and managing deployments using Solidity scripts.

## Project Setup

Initialize a project with `forge init`. Manage dependencies using `forge install <author>/<repo>`. Configure `foundry.toml` for remappings, optimizer settings, and EVM versions. Use `remappings.txt` to simplify imports (e.g., `@openzeppelin/=lib/openzeppelin-contracts/contracts/`).

## Testing Best Practices

### Test Structure

Tests should inherit from `forge-std/Test.sol`. Use `setUp()` for state initialization.

- `test_Xxx`: Standard test case.
- `testFuzz_Xxx`: Fuzz test case.
- `testFail_Xxx`: Test expected to fail (prefer `vm.expectRevert`).

### Fuzz Testing

Foundry automatically provides random inputs for function arguments in `testFuzz` functions. Use `vm.assume()` to filter inputs or `bound(uint256 x, uint256 min, uint256 max)` to constrain values.

### Invariant Testing

Stateful fuzzing that ensures properties hold across multiple transactions.

- `targetContract(address)`: Define the contract to test.
- `handler`: Use a dedicated contract to manage complex call sequences and state transitions.

### Fork Testing

Simulate mainnet state by providing a RPC URL.

- `vm.createFork(url)`: Create a fork.
- `vm.selectFork(id)`: Switch to a fork.
- `vm.rollFork(blockNumber)`: Pin the fork to a specific block.

## Essential Cheatcodes

| Cheatcode                            | Description                                                   |
| ------------------------------------ | ------------------------------------------------------------- |
| `vm.prank(addr)`                     | Sets `msg.sender` for the next call.                          |
| `vm.startPrank(addr)`                | Sets `msg.sender` for all subsequent calls until `stopPrank`. |
| `vm.deal(addr, amt)`                 | Sets the balance of an address.                               |
| `vm.expectRevert(bytes)`             | Expects the next call to revert with a specific error.        |
| `vm.expectEmit(bool,bool,bool,bool)` | Expects the next call to emit a specific event.               |
| `vm.warp(timestamp)`                 | Sets the block timestamp.                                     |
| `vm.roll(blockNumber)`               | Sets the block number.                                        |
| `vm.sign(pk, digest)`                | Generates an ECDSA signature.                                 |
| `vm.label(addr, name)`               | Labels an address for better trace readability.               |
| `vm.record()`                        | Starts recording all storage reads and writes.                |
| `vm.getCode(path)`                   | Returns the creation bytecode of a contract.                  |

## Deployment Workflow

Use `forge script` for Solidity-based deployments.

- Dry-run: `forge script script/Deploy.s.sol --rpc-url $RPC_URL`
- Broadcast: `forge script script/Deploy.s.sol --rpc-url $RPC_URL --broadcast --verify`
- Use `--verify` with `--etherscan-api-key` for automatic source verification.

## Debugging

- Verbosity: `-v` (logs), `-vv` (traces for failed tests), `-vvv` (traces for all tests), `-vvvv` (setup traces), `-vvvvv` (full stack traces).
- `forge debug`: Interactive debugger for a specific transaction.
- `console.log`: Use `forge-std/console.sol` for print debugging.

## Configuration Profiles

Use profiles in `foundry.toml` to manage different build configurations.

```toml
[profile.via_ir]
via_ir = true
test = 'src'
out = 'via_ir-out'

[profile.deterministic]
block_number = 17722462
block_timestamp = 1689711647
bytecode_hash = 'none'
cbor_metadata = false
```

## Enhanced with MCP

When the `solidity-agent-toolkit` is available, leverage these tools in your Foundry workflow:

**Build & Test:**

- `compile_contract`: Compile contracts and get artifact output (ABI, bytecode, errors)
- `run_tests`: Execute the full Foundry test suite with verbosity control
- `run_single_test`: Target specific test functions for fast iteration

**Artifacts & Inspection:**

- `get_abi`: Extract ABI from compiled contracts
- `get_bytecode`: Get deployment or runtime bytecode
- `inspect_storage`: Inspect storage layout for optimization or debugging
- `gas_snapshot`: Generate and compare gas reports across test runs
- `estimate_gas`: Estimate gas for specific function calls

**Deployment:**

- `dry_run_deploy`: Simulate deployment to catch errors before broadcasting
- `check_deployment_status`: Verify deployment transaction status

**Security (Pre-commit):**

- `run_slither`: Static analysis before pushing code
- `run_aderyn`: Fast Rust-based vulnerability scan
- `match_vulnerability_patterns`: Quick pattern check on changed files

## References

Detailed command references and patterns can be found in [Foundry Cheatsheet](./references/foundry-cheatsheet.md).
