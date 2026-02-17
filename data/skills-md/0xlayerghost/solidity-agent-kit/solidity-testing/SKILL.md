---
name: solidity-testing
description: "[AUTO-INVOKE] MUST be invoked BEFORE writing or modifying any test files (*.t.sol). Covers test structure, naming conventions, coverage requirements, fuzz testing, and Foundry cheatcodes. Trigger: any task involving creating, editing, or running Solidity tests."
---

# Testing Standards

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Test Organization

- **One test contract per source contract**: `MyToken.sol` → `MyToken.t.sol`
- **File location**: All tests in `test/` directory
- **Naming**: `test_<feature>_<scenario>` for passing tests, `testFail_<feature>_<scenario>` for expected reverts
  - Example: `test_transfer_revertsWhenInsufficientBalance`
  - Example: `test_stake_updatesBalanceCorrectly`
- **Independence**: Each test must run in isolation — use `setUp()` for shared state, no cross-test dependencies
- **Filtering**: Support `--match-test` and `--match-contract` for targeted runs

## Coverage Requirements

Every core function must have tests covering:

| Scenario | What to verify |
|----------|---------------|
| Happy path | Standard input → expected output, correct state changes |
| Permission checks | Unauthorized caller → `vm.expectRevert` with correct error |
| Boundary conditions | Zero values, max values (`type(uint256).max`), off-by-one |
| Failure scenarios | Every `require` / `revert` / custom error path |
| State changes | Storage updates, balance changes, event emissions (`vm.expectEmit`) |
| Edge cases | Empty arrays, duplicate calls, self-transfers |

## Foundry Cheatcodes Quick Reference

| Cheatcode | Usage |
|-----------|-------|
| `vm.prank(addr)` | Next call from `addr` |
| `vm.startPrank(addr)` | All calls from `addr` until `vm.stopPrank()` |
| `vm.warp(timestamp)` | Set `block.timestamp` |
| `vm.roll(blockNum)` | Set `block.number` |
| `vm.deal(addr, amount)` | Set ETH balance |
| `vm.expectRevert(error)` | Next call must revert with specific error |
| `vm.expectEmit(true,true,false,true)` | Verify event emission (topic checks) |
| `vm.record()` / `vm.accesses()` | Track storage reads/writes |
| `makeAddr("name")` | Create labeled address for readable traces |

## Fuzz Testing Rules

- All math-heavy and fund-flow functions must have fuzz tests
- Pattern: `function testFuzz_<name>(uint256 amount) public`
- Use `vm.assume()` to constrain inputs: `vm.assume(amount > 0 && amount < MAX_SUPPLY);`
- Default runs: 256 — increase to 10,000+ for critical functions: `forge test --fuzz-runs 10000`

## Common Commands

```bash
# Run all tests
forge test

# Run specific test function
forge test --match-test test_transfer

# Run specific test contract
forge test --match-contract MyTokenTest

# Verbose output with full trace
forge test -vvvv

# Gas report
forge test --gas-report

# Fuzz with more runs
forge test --fuzz-runs 10000

# Test coverage
forge coverage

# Coverage with report
forge coverage --report lcov
```
