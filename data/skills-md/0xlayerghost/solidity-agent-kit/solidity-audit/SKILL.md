---
name: solidity-audit
description: "Security audit and code review checklist. Covers 30+ vulnerability types with real-world exploit cases (2021-2026) and EVMbench Code4rena patterns. Use when conducting security audits, code reviews, or pre-deployment security assessments."
---

# Solidity Security Audit Checklist

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

> **Usage**: This skill is for security audits and code reviews. It is NOT auto-invoked — call `/solidity-audit` when reviewing contracts for vulnerabilities.

## Contract-Level Vulnerabilities

### 1. Reentrancy

| Variant | Description | Check |
|---------|-------------|-------|
| Same-function | Attacker re-enters the same function via fallback/receive | All external calls after state updates (CEI pattern)? |
| Cross-function | Attacker re-enters a different function sharing state | All functions touching shared state protected by `nonReentrant`? |
| Cross-contract | Attacker re-enters through a different contract that reads stale state | External contracts cannot read intermediate state? |
| Read-only | View function returns stale data during mid-execution state | No critical view functions used as oracle during state transitions? |

**Case**: [GMX v1 (Jul 2025, $42M)](https://www.halborn.com/blog/post/explained-the-gmx-hack-july-2025) — reentrancy in GLP pool on Arbitrum, attacker looped withdrawals to drain liquidity.

### 2. Access Control

| Check | Detail |
|-------|--------|
| Missing modifier | Every state-changing function has explicit access control? |
| Modifier logic | Modifier actually reverts on failure (not just empty check)? |
| State flag | Access-once patterns properly update storage after each user? |
| Admin privilege scope | Owner powers are minimal and time-limited? |

**Case**: [Bybit (Feb 2025, $1.4B)](https://www.halborn.com/blog/post/explained-the-bybit-hack-february-2025) — Safe{Wallet} UI injected with malicious JS, hijacked signing process. Not a contract flaw, but access control at the infrastructure layer.

### 3. Input Validation

| Check | Detail |
|-------|--------|
| Zero address | All address params reject `address(0)`? |
| Zero amount | Fund transfers reject zero amounts? |
| Array bounds | Paired arrays validated for matching length? |
| Arbitrary call | No unvalidated `address.call(data)` where attacker controls `data`? |
| Numeric bounds | Inputs bounded to prevent dust attacks or gas griefing? |

### 4. Flash Loan Attacks

| Variant | Mechanism | Defense |
|---------|-----------|---------|
| Price manipulation | Flash-borrow → swap to move price → exploit price-dependent logic → repay | TWAP oracle with min-liquidity check |
| Governance | Flash-borrow governance tokens → vote → repay in same block | Snapshot voting + minimum holding period + timelock ≥ 48h |
| Liquidation | Flash-borrow → manipulate collateral value → trigger liquidation | Multi-oracle price verification + circuit breaker |
| Combo (rounding) | Flash-borrow → manipulate pool → micro-withdrawals exploit rounding → repay | Minimum withdrawal amount + virtual shares |

**Cases**:
- [Cream Finance (Oct 2021, $130M)](https://rekt.news/cream-rekt-2/) — flash loan + yUSD oracle manipulation + missing reentrancy guard
- [Abracadabra (Mar 2025, $13M)](https://www.halborn.com/blog/post/explained-the-abracadabra-money-hack-march-2025) — state tracking error in cauldron, self-liquidation + bad loan
- [Bunni (Sep 2025, $8.4M)](https://www.theblock.co/post/369564/bunni-smart-contract-rounding-error) — flash loan + pool price manipulation + rounding error micro-withdrawals

### 5. Oracle & Price

| Check | Detail |
|-------|--------|
| Single oracle dependency | Using multiple independent price sources? |
| Stale price | Checking `updatedAt` timestamp and rejecting old data? |
| Spot price usage | Never using raw AMM reserves for pricing? |
| Minimum liquidity | Oracle reverts if pool reserves below threshold? |
| Price deviation | Circuit breaker if price moves beyond threshold vs last known? |
| Chainlink round completeness | Checking `answeredInRound >= roundId`? |

**Case**: [Cream Finance (Oct 2021, $130M)](https://rekt.news/cream-rekt-2/) — attacker manipulated yUSD vault price by reducing supply, then used inflated collateral to drain all lending pools.

### 6. Numerical Issues

| Type | Description | Defense |
|------|-------------|---------|
| Primitive overflow | `uint256 a = uint8(b) + 1` — reverts if b=255 on Solidity ≥0.8 | Use consistent types, avoid implicit narrowing |
| Truncation | `int8(int256Value)` — silently overflows even on ≥0.8 | Use `SafeCast` library for all type narrowing |
| Rounding / precision loss | `usdcAmount / 1e12` always rounds to 0 for small amounts | Multiply before divide; check for zero result |
| Division before multiplication | `(a / b) * c` loses precision | Always `(a * c) / b` |

**Case**: [Bunni (Sep 2025, $8.4M)](https://www.halborn.com/blog/post/explained-the-bunni-hack-september-2025) — rounding errors in micro-withdrawals exploited via flash loan.

### 7. Signature Issues

| Type | Description | Defense |
|------|-------------|---------|
| ecrecover returns address(0) | Invalid sig returns `address(0)`, not revert | Always check `recovered != address(0)` |
| Replay attack | Same signature reused across txs/chains | Include `chainId` + `nonce` + `deadline` in signed data |
| Signature malleability | ECDSA has two valid (s, v) pairs per signature | Use OpenZeppelin `ECDSA.recover` (enforces low-s) |
| Empty loop bypass | Signature verification in for-loop, attacker sends empty array | Check `signatures.length >= requiredCount` before loop |
| Missing msg.sender binding | Proof/signature not bound to caller | Always include `msg.sender` in signed/proven data |

### 8. ERC20 Compatibility

| Issue | Description | Defense |
|-------|-------------|---------|
| Fee-on-transfer | `transfer(100)` may deliver <100 tokens | Check balance before/after, use actual received amount |
| Rebase tokens | Token balances change without transfers | Never cache external balances; always read live |
| No bool return | Some tokens (USDT) don't return bool on transfer | Use `SafeERC20.safeTransfer` |
| ERC777 hooks | Transfer hooks can trigger reentrancy | Use `ReentrancyGuard` on all token-receiving functions |
| Zero-amount transfer | `transferFrom(A, B, 0)` — address poisoning | Reject zero-amount transfers |
| Approval race | Changing allowance from N to M allows spending N+M | Use `safeIncreaseAllowance` / `safeDecreaseAllowance` |

### 9. MEV / Front-Running

| Type | Description | Defense |
|------|-------------|---------|
| Sandwich attack | Attacker front-runs buy + back-runs sell around victim | Slippage protection + deadline parameter |
| ERC4626 inflation | First depositor donates to inflate share price, rounding out later depositors | Minimum first deposit or virtual shares (ERC4626 with offset) |
| Approval front-run | Attacker spends old allowance before new allowance tx confirms | Use `increaseAllowance` not `approve` |
| Unrestricted withdrawal | Attacker monitors mempool for withdraw tx, front-runs with own | Require commit-reveal or auth binding |

### 10. Storage & Low-Level

| Issue | Description |
|-------|-------------|
| Storage pointer | `Foo storage foo = arr[0]; foo = arr[1];` — does NOT update arr[0] |
| Nested delete | `delete structWithMapping` — inner mapping data persists |
| Private variables | All contract storage is publicly readable via `eth_getStorageAt` |
| Unsafe delegatecall | Delegatecall to untrusted contract can `selfdestruct` the caller |
| Proxy storage collision | Upgrade changes parent order → variables overwrite each other (use storage gaps) |
| msg.value in loop | msg.value doesn't decrease in loop — enables double-spend |

### 11. Contract Detection Bypass

| Method | How it works |
|--------|-------------|
| Constructor call | Attack from constructor — `extcodesize == 0` during deployment |
| CREATE2 pre-compute | Pre-calculate contract address, use as EOA before deploying |

### 12. Proxy & Upgrade Vulnerabilities

> Source: [EVMbench Paper §4.2, Appendix H](https://cdn.openai.com/evmbench/evmbench.pdf) / [Code4rena 2024-07-basin H-01](https://code4rena.com/reports/2024-07-basin)

| Check | Detail |
|-------|--------|
| `_authorizeUpgrade` access control | UUPS `_authorizeUpgrade` must have `onlyOwner` modifier? |
| Permissionless factory/registry | Can attacker use permissionless factory (e.g. Aquifer `boreWell`) to satisfy upgrade checks? |
| `upgradeTo` modifier | Overridden `upgradeTo`/`upgradeToAndCall` retains `onlyProxy` modifier? |
| Initializer protection | `initializer` modifier prevents re-initialization? Implementation calls `_disableInitializers()`? |
| Storage layout compatibility | Upgrade-safe storage layout (storage gaps or ERC-7201 namespace)? |

**Case**: [Code4rena 2024-07-basin H-01](https://code4rena.com/reports/2024-07-basin) (via [EVMbench Paper Fig.12, p.19](https://cdn.openai.com/evmbench/evmbench.pdf)) — `_authorizeUpgrade` only checked delegatecall and Aquifer registration but lacked `onlyOwner`, allowing anyone to upgrade a Well proxy to a malicious implementation and drain funds. Oracle patch: add a single `onlyOwner` modifier.

### 13. Trust Boundary & Protocol Composability

> Source: [EVMbench Paper §4.2.1, Fig.6](https://cdn.openai.com/evmbench/evmbench.pdf) / Code4rena [2024-04-noya H-08](https://code4rena.com/reports/2024-04-noya), [2024-07-benddao](https://code4rena.com/reports/2024-07-benddao)

| Check | Detail |
|-------|--------|
| Cross-vault trust isolation | Registry/Router relay calls verify vault-level authorization? |
| Trusted sender abuse | Functions like `sendTokensToTrustedAddress` verify source vault, not just router identity? |
| Flash loan + routing combo | Can attacker use flash loan callback to make router impersonate arbitrary vault? |
| Collateral ownership verification | Liquidation/staking operations verify actual NFT/collateral owner? |
| Cross-contract state dependency | Multi-contract interactions free from intermediate state dependencies? |

**Cases**:
- [Code4rena 2024-04-noya H-08](https://code4rena.com/reports/2024-04-noya) (via [EVMbench Paper §4.2.1, Fig.6, p.8-9](https://cdn.openai.com/evmbench/evmbench.pdf)) — PositionRegistry + BalancerFlashLoan pipeline lacked vault-level auth; keeper used flash loan to make router impersonate any vault, draining cross-vault funds via `sendTokensToTrustedAddress`
- [Code4rena 2024-07-benddao](https://code4rena.com/reports/2024-07-benddao) (via [EVMbench Paper Fig.13, p.19](https://cdn.openai.com/evmbench/evmbench.pdf)) — `isolateLiquidate` did not verify NFT ownership, allowing attacker to pass others' tokenIds for liquidation

### 14. State Ordering & Counter Manipulation

> Source: [EVMbench Paper Appendix H.1, Fig.19-21](https://cdn.openai.com/evmbench/evmbench.pdf) / [Code4rena 2024-08-phi H-06](https://code4rena.com/reports/2024-08-phi)

| Check | Detail |
|-------|--------|
| Counter/ID increment order | `credIdCounter++` or similar ID increments happen before external calls? |
| Auto-buy in create | `create()` functions with auto `buy()` calls execute only after ID/state fully initialized? |
| Refund timing | ETH refund (excess) happens after all state updates complete? |
| Bonding curve metadata overwrite | Can attacker reenter to modify bonding curve/pricing params — buy cheap, switch to expensive curve, sell high? |

**Case**: [Code4rena 2024-08-phi H-06](https://code4rena.com/reports/2024-08-phi) (via [EVMbench Paper Appendix H.1, p.25-28](https://cdn.openai.com/evmbench/evmbench.pdf)) — `_createCredInternal` called `buyShareCred` before incrementing `credIdCounter`; `_handleTrade` refunded excess ETH before updating `lastTradeTimestamp`. Attacker reentered to accumulate shares on cheap curve, overwrote metadata to expensive curve, sold to drain all contract ETH. Fix: add `nonReentrant` to `buyShareCred`/`sellShareCred`.

## Infrastructure-Level Vulnerabilities

### 15. Frontend / UI Injection

Attackers inject malicious code into the dApp frontend or signing interface.

**Defense**: Verify transaction calldata matches expected function selector and parameters before signing. Use hardware wallet with on-device transaction preview. Audit all frontend dependencies regularly.

**Case**: [Bybit (Feb 2025, $1.4B)](https://www.nccgroup.com/research-blog/in-depth-technical-analysis-of-the-bybit-hack/) — malicious JavaScript injected into Safe{Wallet} UI, tampered with transaction data during signing.

### 16. Private Key & Social Engineering

Compromised keys remain the #1 loss source in 2025-2026.

**Defense**: Store keys in HSM or hardware wallet. Use multisig (≥ 3/5) for all treasury and admin operations. Never share seed phrases with any "support" contact. Conduct regular social engineering awareness training.

**Case**: [Step Finance (Jan 2026, $30M)](https://www.halborn.com/blog/post/explained-the-step-finance-hack-january-2026) — treasury wallet private keys compromised via device breach.

### 17. Cross-Chain Bridge

| Check | Detail |
|-------|--------|
| Inherited code | Audit all bridge logic inherited from third-party frameworks |
| Message verification | Cross-chain messages validated with proper signatures and replay protection? |
| Liquidity isolation | Bridge funds separated from protocol treasury? |

**Case**: [SagaEVM (Jan 2026, $7M)](https://www.theblock.co/post/386638/sagaevm-suffers-exploit) — inherited vulnerable EVM precompile bridge logic from Ethermint.

### 18. Legacy / Deprecated Contracts

Old contracts with known bugs remain callable on-chain forever.

**Defense**: Permanently `pause` or migrate funds from deprecated contracts. Monitor old contract addresses for unexpected activity. Remove mint/admin functions before deprecation.

**Case**: [Truebit (Jan 2026, $26.4M)](https://www.coindesk.com/markets/2026/01/09/truebit-token-tru-crashes-99-9-after-usd26-6m-exploit-drains-8-535-eth) — Solidity 0.6.10 contract lacked overflow protection, attacker minted tokens at near-zero cost.

## Audit Execution Checklist

When conducting a security audit, check each item:

**Reentrancy:**
- [ ] All functions with external calls use `nonReentrant`
- [ ] CEI pattern followed — no state reads after external calls
- [ ] View functions not used as oracle during state transitions

**Access Control:**
- [ ] Every state-changing function has explicit access modifier
- [ ] Modifiers actually revert (not silently pass)
- [ ] Admin privileges are minimal and documented

**Input & Logic:**
- [ ] No unvalidated arbitrary `call` / `delegatecall`
- [ ] No `tx.origin` for authentication
- [ ] Array lengths validated for paired inputs
- [ ] No division-before-multiplication precision loss

**Token Handling:**
- [ ] All ERC20 ops use `SafeERC20`
- [ ] Fee-on-transfer tokens handled (balance diff check)
- [ ] Rebase token balances not cached
- [ ] Zero-amount transfers rejected

**Price & Oracle:**
- [ ] No raw spot price usage
- [ ] Stale price check (`updatedAt` / `answeredInRound`)
- [ ] Minimum liquidity threshold enforced
- [ ] Price deviation circuit breaker

**Signature & Crypto:**
- [ ] `ecrecover` result checked against `address(0)`
- [ ] Signed data includes `chainId`, `nonce`, `msg.sender`, `deadline`
- [ ] Using OZ `ECDSA` (low-s enforced)
- [ ] MerkleProof leaves bound to `msg.sender`

**Flash Loan Defense:**
- [ ] Governance: snapshot voting + holding period + timelock
- [ ] Price: TWAP or multi-oracle, not single-block spot
- [ ] Vault: minimum first deposit or virtual shares (ERC4626)

**Proxy & Upgrade ([EVMbench](https://cdn.openai.com/evmbench/evmbench.pdf)):**
- [ ] UUPS `_authorizeUpgrade` has `onlyOwner` — [EVMbench/basin H-01]
- [ ] `upgradeTo`/`upgradeToAndCall` retains `onlyProxy` — [EVMbench/basin H-01]
- [ ] Implementation constructor calls `_disableInitializers()` — [EVMbench/basin H-01]
- [ ] Storage layout upgrade-compatible (storage gaps or ERC-7201) — [EVMbench/basin H-01]

**Trust Boundary & Composability ([EVMbench](https://cdn.openai.com/evmbench/evmbench.pdf)):**
- [ ] Router/Registry relay calls verify source vault/contract authorization — [EVMbench/noya H-08]
- [ ] Liquidation operations verify actual collateral ownership — [EVMbench/benddao]
- [ ] Flash loan callback paths cannot be abused to penetrate trust boundaries — [EVMbench/noya H-08]
- [ ] No intermediate state dependencies in multi-contract interactions — [EVMbench/noya H-08]

**State Ordering ([EVMbench](https://cdn.openai.com/evmbench/evmbench.pdf)):**
- [ ] Counter/ID increments complete before external calls — [EVMbench/phi H-06]
- [ ] ETH refunds execute after all state updates — [EVMbench/phi H-06]
- [ ] Auto-operations in create functions (auto-buy etc.) execute after full initialization — [EVMbench/phi H-06]

**Infrastructure:**
- [ ] Third-party dependencies audited (bridge code, inherited contracts)
- [ ] No deprecated contracts still callable with admin/mint functions
- [ ] Multisig on all treasury and admin wallets
- [ ] Frontend transaction verification (calldata matches expected)

## AI Agent Audit Methodology

> Source: [EVMbench (OpenAI/Paradigm, Feb 2026)](https://cdn.openai.com/evmbench/evmbench.pdf) — evaluated AI agents on 120 high-severity vulnerabilities from 40 Code4rena audit repositories across Detect/Patch/Exploit modes.

### Audit Strategy

1. **Coverage over depth**: scan ALL in-scope files; do not stop after finding the first vulnerability [EVMbench §5, p.10]
2. **Three-phase audit**: Detect (identify vulnerabilities) -> Patch (write fix) -> Exploit (build PoC) [EVMbench §3.2, p.5]
3. **Incremental output**: write findings continuously during audit to preserve progress [EVMbench Appendix G, Fig.18, p.24]
4. **Systematic category scan**: check by vulnerability class (reentrancy, access control, numerical, oracle...) rather than intuition [EVMbench §3.1, p.4]
5. **Verify fixes**: after patching, confirm original tests still pass AND exploit is no longer viable [EVMbench §3.2.2, p.5]

### High-Frequency Vulnerability Patterns (Code4rena Data)

> Source: EVMbench Table 4 (p.17) — 40 audit repositories

- Missing access control (upgradeability, liquidation, admin functions) — basin H-01, munchables, benddao
- Reentrancy + state ordering errors (refund before state update) — phi H-06, noya H-08
- Flash loan trust boundary penetration (exploiting router/registry trust propagation) — noya H-08
- Signature replay / front-running (checkpoint bypass, session signature replay) — sequence H-01, H-02
- Numerical precision / rounding (bonding curve, micro-withdrawals) — abracadabra H-02, size H-02

### Key Findings

> Source: EVMbench Paper §4.1 (p.7), Fig.7 (p.10), Fig.10 (p.18), Fig.11 (p.19)

- With mechanism hints, Patch success rate jumps from ~40% to ~94% [Fig.7] — agents know how to fix but struggle to find vulnerabilities
- Most vulnerabilities require ≤5 lines of code to fix [Fig.10, p.18]
- Most exploits require only 1-3 transactions [Fig.11, p.19]
- Agents whose finding count is closest to actual vulnerability count score highest (quality > quantity) [Fig.5, p.8]

## 2021-2026 Incident Quick Reference

| Date | Project | Loss | Attack Type | Root Cause | Source |
|------|---------|------|-------------|------------|--------|
| Oct 2021 | Cream Finance | $130M | Flash loan + oracle | yUSD vault price manipulation via supply reduction | [rekt.news](https://rekt.news/cream-rekt-2/) |
| Feb 2025 | Bybit | $1.4B | UI injection / supply chain | Safe{Wallet} JS tampered via compromised dev machine | [NCC Group](https://www.nccgroup.com/research-blog/in-depth-technical-analysis-of-the-bybit-hack/) |
| Mar 2025 | Abracadabra | $13M | Logic flaw | State tracking error in cauldron liquidation | [Halborn](https://www.halborn.com/blog/post/explained-the-abracadabra-money-hack-march-2025) |
| Jul 2025 | GMX v1 | $42M | Reentrancy | GLP pool cross-contract reentrancy on Arbitrum | [Halborn](https://www.halborn.com/blog/post/explained-the-gmx-hack-july-2025) |
| Sep 2025 | Bunni | $8.4M | Flash loan + rounding | Rounding direction error in withdraw, 44 micro-withdrawals | [The Block](https://www.theblock.co/post/369564/bunni-smart-contract-rounding-error) |
| Oct 2025 | Abracadabra #2 | $1.8M | Logic flaw | cook() validation flag reset, uncollateralized MIM borrow | [Halborn](https://www.halborn.com/blog/post/explained-the-abracadabra-hack-october-2025) |
| Jan 2026 | Step Finance | $30M | Key compromise | Treasury wallet private keys stolen via device breach | [Halborn](https://www.halborn.com/blog/post/explained-the-step-finance-hack-january-2026) |
| Jan 2026 | Truebit | $26.4M | Legacy contract | Solidity 0.6.10 integer overflow in mint pricing | [CoinDesk](https://www.coindesk.com/markets/2026/01/09/truebit-token-tru-crashes-99-9-after-usd26-6m-exploit-drains-8-535-eth) |
| Jan 2026 | SagaEVM | $7M | Supply chain / bridge | Inherited Ethermint precompile bridge vulnerability | [The Block](https://www.theblock.co/post/386638/sagaevm-suffers-exploit) |
