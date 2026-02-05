---
name: rehype
description: Operate, configure, test, and deploy Doppler's Rehype V4 hook whenever a task mentions Rehype, fee splits, buybacks, or Doppler hook troubleshooting.
metadata:
  owner: doppler
  version: "1.0"
---

> **Source References**: Code citations link to raw GitHub files pinned to commit `988dab4`. To fetch specific lines: `curl -s "<url>" | sed -n 'START,ENDp'`

# Rehype Doppler Hook

> Use this skill for anything involving Doppler's Rehype hook: configuring fee distributions, decoding swap flows, running invariant suites, or shipping deployments.

## When To Activate
- User references "rehype", Doppler hooks, fee distributions, buybacks, or beneficiary payouts
- Tasks touch `src/dopplerHooks/RehypeDopplerHook.sol`, `IRehypeHook.sol`, or related deployments/tests
- Need to explain hook-driven swap behavior, collect fees, or update pool configuration

## Prerequisites
- Doppler repo checked out and current (`whetstoneresearch/doppler`)
- Foundry toolchain installed for `forge`/`cast`
- Access to the Airlock + DopplerHookInitializer environment when mutating on-chain state
- Uniswap V4 Pool Manager RPC endpoint for simulations or deployments

## Quick Start
1. Identify the pool asset + numeraire by inspecting `DopplerHookInitializer.getState(asset)`.
2. Confirm Rehype is enabled for the pool (`ON_INITIALIZATION_FLAG | ON_SWAP_FLAG`).
3. Load current fee distribution with `RehypeDopplerHook.getFeeDistributionInfo(poolId)` to baseline percentages.
4. Move to the relevant workflow below (configuration, fee collection, testing, deployment).

## Core Workflows

### Configure / Tune Fee Distribution
1. Gather desired percentages (asset buyback, numeraire buyback, beneficiary, LP) that must sum to `WAD` (1e18).
2. Call `setFeeDistribution(poolId, ...)` from the `buybackDst` address (stored in `getPoolInfo[poolId].buybackDst`).
   - Only the `buybackDst` can update fee distribution; expect `SenderNotAuthorized` on mismatch.
3. Record reasoning + math (ideally in governance artifacts) because improper splits can stall swaps.
4. See [Configuration](references/CONFIGURATION.md) for calldata templates and sanity checks.

**Note**: The previous `setFeeDistributionByBeneficiary()` function has been removed. Fee distribution updates are now controlled exclusively by `buybackDst`.

### Collect Beneficiary Fees
1. Resolve the target asset (the Doppler token) and call `RehypeDopplerHook.collectFees(asset)`.
2. The hook transfers accumulated `beneficiaryFees0/1` to `buybackDst` and zeroes out the counters.
3. Confirm ERC20 balances + hook storage match expectations before/after collection.
4. Document tx hash for accounting.

### Collect Airlock Owner Fees (5% Protocol Fee)
1. The Rehype hook automatically splits 5% of all swap fees to the Airlock owner (stored separately as `airlockOwnerFees0/1`).
2. The Airlock owner calls `RehypeDopplerHook.claimAirlockOwnerFees(asset)` to claim accumulated fees.
3. Only the current `airlock.owner()` can call this function; expect `SenderNotAirlockOwner` on mismatch.
4. Returns `(fees0, fees1)` indicating amounts transferred.

### Understand Swap Flow / Debugging
1. `_onSwap` collects swap output fees, executes asset + numeraire buybacks, rebalances, and reinvests LP before crediting beneficiary balances.
2. Use `_collectSwapFees` math to estimate deductions: `fee = outputAmount * customFee / 1e6`.
3. **Fee Split**: 5% of collected fees go to `airlockOwnerFees`, remaining 95% go to `fees0/1` for distribution.
4. Inspect `getHookFees(poolId)` for:
   - `fees0/fees1` (distributable fees for buybacks/LP/beneficiary)
   - `beneficiaryFees0/1` (accumulated beneficiary share, claimable via `collectFees`)
   - `airlockOwnerFees0/1` (5% protocol fee, claimable via `claimAirlockOwnerFees`)
5. Troubleshoot common errors in the table below.

### Testing Changes
1. Run targeted unit tests: `forge test --match-contract RehypeDopplerHook -vv`.
2. Execute invariants from `test/invariant/rehype/` using `forge test --match-contract RehypeInvariants` (ERC20) and `RehypeInvariantsETH` (native path).
3. For fuzzing issues, consult handler design + risk matrix in [Testing](references/TESTING.md).
4. Capture seed(s) that reproduce failures; investigate `_rebalanceFees`, settlement paths, or `_collectSwapFees` underflows.

### Deploy / Upgrade Hook Instances
1. Edit `doppler/script/deployments.config.toml` with the target chain parameters (CreateX, initializer, pool manager).
2. Run `forge script script/DeployRehypeDopplerHook.s.sol --rpc-url <network> --broadcast --sig "run()"`.
3. Script enforces Create3 deterministic address parity; expect revert if mismatch.
4. After broadcasting, update `doppler/Deployments.md` with the new address + commit hash.
5. Details live in [Deployment](references/DEPLOYMENT.md).

## Troubleshooting Cheat Sheet
| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `FeeDistributionMustAddUpToWAD()` revert | Percentages do not sum to `1e18` | Normalize weights before calling setters |
| `SenderNotAuthorized()` revert | Caller is not the `buybackDst` for this pool | Query `getPoolInfo[poolId].buybackDst` and switch signer |
| `SenderNotAirlockOwner()` revert | Caller is not the airlock owner when claiming owner fees | Query `airlock.owner()` and switch signer |
| Swaps revert with `INSUFFICIENT_INPUT_AMOUNT` | Hook tried to rebalance more than held | Inspect `getHookFees` vs. ERC20 balances; rerun invariants |
| Hook stuck with large `fees0/fees1` but no beneficiary accrual | `_simulateSwap` failing or pool lacks liquidity | Verify Quoter path, pool balances, or temporarily disable LP reinvest via config |
| Deploy script exits early | `config.get("is_testnet")` false (prod guard) | Remove guard only when cleared for production |

## References
- [Configuration playbooks](references/CONFIGURATION.md)
- [Testing + invariants guide](references/TESTING.md)
- [Deployment runbook](references/DEPLOYMENT.md)
- Source of truth: `doppler/src/dopplerHooks/RehypeDopplerHook.sol`, `doppler/src/interfaces/IRehypeHook.sol`, `doppler/test/invariant/rehype/SPECIFICATION.md`
