---
name: uniswap-v4-hooks
description: |
  Secure Uniswap v4 hook development assistant. Activates when:
  - Working with Uniswap v4 hooks, PoolManager, or hook contracts
  - Keywords: uniswap, v4, hook, hooks, beforeSwap, afterSwap, PoolManager, IHooks, BaseHook
  - Creating, reviewing, or auditing hook contracts
  - Implementing custom AMM logic, dynamic fees, or swap modifications
  - User says "uniswap hooks" or invokes "/uniswap-v4-hooks"
---

This skill guides secure development of Uniswap v4 hooks. Hooks are external smart contracts that intercept pool operations at specific lifecycle points. Security is paramount—hook vulnerabilities can drain user funds.

## Security Thinking

Before writing ANY hook code, assess the threat model:

**Who calls your hook?**
- Only `PoolManager` should call hook functions
- `msg.sender` in a hook is ALWAYS `PoolManager`, never the user
- The `sender` parameter is the router, not the end user

**What state is exposed?**
- Hooks execute mid-transaction—state can be manipulated between callbacks
- Reentrancy is possible through external calls
- Shared storage across pools using the same hook can break unexpectedly

**What can go wrong with deltas?**
- Every token in MUST equal tokens out (delta accounting)
- Rounding errors accumulate in iterative operations
- BeforeSwapDelta can bypass normal swap logic entirely

## CRITICAL: The NoOp Rug Pull Vector

Hooks with `BEFORE_SWAP_RETURNS_DELTA_FLAG` can **steal user funds**. This is the most dangerous hook permission.

```solidity
// MALICIOUS EXAMPLE - DO NOT USE
// This hook takes user tokens and returns nothing
function beforeSwap(...) external returns (bytes4, BeforeSwapDelta, uint24) {
    Currency input = params.zeroForOne ? key.currency0 : key.currency1;

    // Take all user funds
    input.take(poolManager, address(this), uint256(-params.amountSpecified), false);

    // Return delta saying we took everything, returning zero
    return (
        BaseHook.beforeSwap.selector,
        toBeforeSwapDelta(int128(-params.amountSpecified), 0), // THEFT
        0
    );
}
```

**When `beforeSwapReturnDelta: true`:**
- The hook can completely replace swap logic
- Pool math is SKIPPED if delta equals amountSpecified
- User funds flow to the hook, not through the AMM curve

**Defense:** NEVER enable `beforeSwapReturnDelta` unless implementing a legitimate custom AMM. Users should verify hook permissions before swapping.

## Permission Flags (Address Encoding)

Hook permissions are encoded in the contract address. The address must have specific bits set:

| Bit | Permission | Risk Level |
|-----|------------|------------|
| 0 | beforeInitialize | Low |
| 1 | afterInitialize | Low |
| 2 | beforeAddLiquidity | Medium |
| 3 | afterAddLiquidity | Medium |
| 4 | beforeRemoveLiquidity | Medium |
| 5 | afterRemoveLiquidity | Medium |
| 6 | beforeSwap | High |
| 7 | afterSwap | Medium |
| 8 | beforeDonate | Low |
| 9 | afterDonate | Low |
| 10 | beforeSwapReturnDelta | **CRITICAL** |
| 11 | afterSwapReturnDelta | High |
| 12 | afterAddLiquidityReturnDelta | Medium |
| 13 | afterRemoveLiquidityReturnDelta | Medium |

**Address Mining:** Use CREATE2 with salt grinding to deploy at an address with correct permission bits. Tools: `hook-mine-and-sinker`, `v4-hook-address-miner`.

## Access Control Pattern

```solidity
// REQUIRED: Verify caller is PoolManager
modifier onlyPoolManager() {
    require(msg.sender == address(poolManager), "Not PoolManager");
    _;
}

function beforeSwap(
    address sender,      // This is the ROUTER, not the user
    PoolKey calldata key,
    IPoolManager.SwapParams calldata params,
    bytes calldata hookData
) external onlyPoolManager returns (bytes4, BeforeSwapDelta, uint24) {
    // ...
}
```

## Identifying the Actual User (msg.sender Problem)

The `sender` parameter is the router contract, NOT the end user. To get the actual user:

```solidity
// 1. Define interface for trusted routers
interface IMsgSender {
    function msgSender() external view returns (address);
}

// 2. Maintain allowlist of trusted routers
mapping(address => bool) public trustedRouters;

// 3. Query router safely in hook
function afterSwap(
    address sender,  // This is the router
    PoolKey calldata key,
    IPoolManager.SwapParams calldata params,
    BalanceDelta delta,
    bytes calldata hookData
) external override returns (bytes4, int128) {
    // CRITICAL: Only trust verified routers
    if (!trustedRouters[sender]) {
        revert UntrustedRouter(sender);
    }

    // Safe to query actual user
    try IMsgSender(sender).msgSender() returns (address user) {
        // Use `user` for rewards, tracking, etc.
    } catch {
        revert RouterDoesNotImplementMsgSender();
    }

    return (this.afterSwap.selector, 0);
}
```

**NEVER trust `tx.origin`** for authentication (only acceptable for anti-gaming checks like self-referral prevention).

## Delta Accounting Rules

Deltas track what the hook owes or is owed. They MUST net to zero.

```solidity
// Taking tokens FROM PoolManager (hook receives tokens)
currency.take(poolManager, address(this), amount, false);

// Settling tokens TO PoolManager (hook sends tokens)
currency.settle(poolManager, address(this), amount, false);

// INVARIANT: All deltas must balance before unlock completes
```

**Common Delta Bugs:**
- Forgetting to settle after taking
- Rounding in wrong direction (always round against the user/hook)
- Not handling both swap directions (zeroForOne true AND false)

## Hook Implementation Checklist

Before ANY hook implementation:

- [ ] **Access Control**: Only PoolManager can call hook functions
- [ ] **Delta Balance**: Every take has a corresponding settle
- [ ] **Router Verification**: Never trust sender without allowlist check
- [ ] **Overflow Protection**: Use `mulDiv` for price math, never raw multiplication
- [ ] **Reentrancy Guards**: Add if making external calls
- [ ] **Token Type Handling**: Document unsupported tokens (rebasing, fee-on-transfer)
- [ ] **Permission Flags**: Minimal permissions needed for functionality

## Base Hook Template

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {BaseHook} from "v4-periphery/src/base/hooks/BaseHook.sol";
import {IPoolManager} from "v4-core/interfaces/IPoolManager.sol";
import {PoolKey} from "v4-core/types/PoolKey.sol";
import {BalanceDelta} from "v4-core/types/BalanceDelta.sol";
import {Hooks} from "v4-core/libraries/Hooks.sol";

contract MyHook is BaseHook {
    constructor(IPoolManager _manager) BaseHook(_manager) {}

    function getHookPermissions() public pure override returns (Hooks.Permissions memory) {
        return Hooks.Permissions({
            beforeInitialize: false,
            afterInitialize: false,
            beforeAddLiquidity: false,
            afterAddLiquidity: false,
            beforeRemoveLiquidity: false,
            afterRemoveLiquidity: false,
            beforeSwap: false,
            afterSwap: true,  // Enable only what you need
            beforeDonate: false,
            afterDonate: false,
            beforeSwapReturnDelta: false,  // DANGEROUS - enable with caution
            afterSwapReturnDelta: false,
            afterAddLiquidityReturnDelta: false,
            afterRemoveLiquidityReturnDelta: false
        });
    }

    function _afterSwap(
        address sender,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        BalanceDelta delta,
        bytes calldata hookData
    ) internal override returns (bytes4, int128) {
        // Your logic here
        return (this.afterSwap.selector, 0);
    }
}
```

## Common Vulnerability Patterns

### 1. Overflow in Price Calculations
```solidity
// BAD: Can overflow
uint256 price = uint256(sqrtPriceX96) ** 2;

// GOOD: Use mulDiv
uint256 price = FullMath.mulDiv(uint256(sqrtPriceX96), uint256(sqrtPriceX96), 1 << 96);
```

### 2. Incorrect Fee Calculation
```solidity
// BAD: Simple addition is wrong
uint256 totalFee = protocolFee + lpFee;

// GOOD: Protocol fee taken first, then LP fee from remainder
// protocolFee + lpFee * (1_000_000 - protocolFee) / 1_000_000
```

### 3. Missing Timestamp Validation
```solidity
// BAD: No future check
function submitOrder(uint256 expiration) external {
    orders[msg.sender] = Order(expiration, ...);
}

// GOOD: Validate expiration is in future
function submitOrder(uint256 expiration) external {
    require(expiration > block.timestamp, "Expiration must be in future");
    require(expiration % interval == 0, "Must align to interval");
    orders[msg.sender] = Order(expiration, ...);
}
```

### 4. Trusting Sender Without Verification
```solidity
// BAD: sender could be malicious contract
address user = sender;

// GOOD: Verify router and query actual user
require(trustedRouters[sender], "Untrusted router");
address user = IMsgSender(sender).msgSender();
```

## Token Handling Hazards

**Unsupported token types** (document explicitly if your hook doesn't handle):
- **Fee-on-transfer**: Actual received amount differs from transfer amount
- **Rebasing**: Balance changes without transfers
- **ERC-777**: Reentrancy via transfer hooks
- **Pausable**: Transfers can revert unexpectedly
- **Blocklist**: Some addresses may be blocked

```solidity
// If handling non-standard tokens, validate actual balances
uint256 balanceBefore = token.balanceOf(address(this));
token.transferFrom(user, address(this), amount);
uint256 actualReceived = token.balanceOf(address(this)) - balanceBefore;
```

## Testing Requirements

Use Foundry for comprehensive testing:

```solidity
// Invariant test: Deltas always balance
function invariant_deltasBalance() public {
    assertEq(poolManager.currencyDelta(address(hook), currency0), 0);
    assertEq(poolManager.currencyDelta(address(hook), currency1), 0);
}

// Fuzz test: No overflow in price calculations
function testFuzz_priceCalculation(uint160 sqrtPriceX96) public {
    vm.assume(sqrtPriceX96 >= TickMath.MIN_SQRT_PRICE);
    vm.assume(sqrtPriceX96 <= TickMath.MAX_SQRT_PRICE);
    // Should not revert
    hook.calculatePrice(sqrtPriceX96);
}

// Test both swap directions
function test_swapZeroForOne() public { ... }
function test_swapOneForZero() public { ... }
```

## Risk Assessment (Self-Score)

Before deployment, score your hook (0-33 scale):

| Dimension | Score Range | Your Hook |
|-----------|-------------|-----------|
| Code Complexity | 0-5 | |
| Custom Math | 0-5 | |
| External Dependencies | 0-3 | |
| External Liquidity | 0-3 | |
| TVL Potential | 0-5 | |
| Team Maturity | 0-3 | |
| Upgradeability | 0-3 | |
| Autonomous Updates | 0-3 | |
| Price-Impacting | 0-3 | |

**Risk Tiers:**
- **Low (0-6)**: 1 audit + AI static analysis
- **Medium (7-17)**: 1-2 audits + bug bounty recommended
- **High (18-33)**: 2 audits (1 math specialist) + mandatory bug bounty + monitoring

## Production Hooks Reference

Allowlisted hooks on Uniswap (as of Jan 2025):
- Flaunch (meme coin launchpad, 100% fees to creators)
- EulerSwap (lending-powered DEX)
- Zaha Studios TWAMM (time-weighted orders)
- Coinbase Verified Pools
- Panoptic Oracle Hook
- AEGIS Dynamic Fee Mechanism

Study these for patterns: https://raw.githubusercontent.com/fewwwww/awesome-uniswap-hooks/refs/heads/main/README.md

## NEVER Do This

- NEVER enable `beforeSwapReturnDelta` without understanding the rug pull risk
- NEVER trust `sender` parameter without router verification
- NEVER use `unchecked` blocks for price/amount math
- NEVER assume ERC20 standard behavior for all tokens
- NEVER skip delta settlement
- NEVER deploy without address permission verification
- NEVER store sensitive state readable mid-swap
- NEVER use `tx.origin` for authentication

## Resources

- **v4-core**: https://github.com/Uniswap/v4-core
- **v4-periphery**: https://github.com/Uniswap/v4-periphery
- **Security Framework**: https://docs.uniswap.org/contracts/v4/security
- **Hook Examples**: https://github.com/fewwwww/awesome-uniswap-hooks
- **Address Mining**: https://github.com/hensha256/hook-mine-and-sinker
- **v4 by Example**: https://v4-by-example.org

## Audit Checklist (Pre-Deployment)

- [ ] All hook functions check `msg.sender == poolManager`
- [ ] Deltas verified to net zero in all paths
- [ ] No overflow possible in math operations
- [ ] Router allowlist implemented if identifying users
- [ ] Token types explicitly documented
- [ ] Reentrancy guards on external calls
- [ ] Timestamp validations in place
- [ ] Permission flags minimal and correct
- [ ] Fuzz tests pass for edge cases
- [ ] Invariant tests for delta accounting
- [ ] Both swap directions tested
- [ ] Fee calculations match Uniswap's formula
