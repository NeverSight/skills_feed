---
name: cairo-security
description: Use when reviewing Cairo contracts for security — common vulnerabilities, audit patterns, production hardening, Cairo-specific pitfalls, L1/L2 bridging safety, session key security, precision/rounding bugs, static analysis tooling. Sourced from 50+ public audits and the Cairo Book.
license: Apache-2.0
metadata: {"author":"omarespejel","version":"3.2.0","last_updated":"2026-02-11","org":"keep-starknet-strange","github":"https://github.com/omarespejel","x":"https://x.com/omarespejel"}
keywords: [cairo, security, audit, vulnerabilities, access-control, reentrancy, starknet, production, hardening, l1-l2, session-keys, precision, rounding, static-analysis, snip-12, snip-9, outside-execution, governance, pausable, paymaster, account-abstraction, storage-node, vec, map, felt252, erc4626, erc20-permit]
allowed-tools: [Bash, Read, Write, Glob, Grep, Task]
user-invocable: true
---

# Cairo Security

Security patterns and common vulnerabilities for Cairo smart contracts on Starknet. Sourced from 50+ public audit reports including Nethermind, ConsenSys Diligence, Code4rena, ChainSecurity, Cairo Security Clan, Zellic, and Nethermind AuditAgent, plus the [Cairo Book security chapter](https://book.cairo-lang.org/ch104-01-general-recommendations.html), [Crytic's Not So Smart Contracts](https://github.com/crytic/building-secure-contracts/tree/master/not-so-smart-contracts/cairo), [Oxor.io Cairo Security Flaws](https://oxor.io/blog/2024-08-16-cairo-security-flaws/), and [FuzzingLabs Top 4 Vulnerabilities](https://fuzzinglabs.com/top-4-vulnerability-cairo-starknet-smart-contract/).

> **Versions:** This skill targets **Cairo 2.12.4** (latest stable tagged on GitHub; v2.15.0 exists but 2.12.4 carries the "Latest" tag), **Scarb 2.15.1**, **Starknet Foundry 0.56.0**, **OpenZeppelin Contracts for Cairo 3.0.0** (v4.0.0-alpha.0 is pre-release, uses Scarb 2.15.1 / snforge 0.55.0), and **Starknet v0.14.1** (mainnet Dec 2025). All code examples and import paths are verified against these versions.

> **Cairo Editions:** Cairo v2.15.0 introduced `edition 2025_12`, which changes snapshot/member access syntax (e.g., `(@a).b` returns desnapped value). If your `Scarb.toml` specifies this edition, test code that accesses struct members through snapshots — the number of `@` levels needed may differ from pre-2025_12 behavior.

> **Workflow:** Use this skill as a review pass after your contract compiles and tests pass. Not a replacement for a professional audit.

## When to Use

- Reviewing a contract before audit or deployment
- Checking for common Cairo/Starknet vulnerabilities
- Hardening a contract for production
- Implementing access control, upgrade safety, input validation
- Writing session key or delegated execution contracts
- Reviewing L1/L2 bridge handlers

**Not for:** Writing contracts (use cairo-contracts), testing (use cairo-testing), gas optimization (use cairo-optimization)

## Critical Patterns — Read These First

These are the highest-impact Cairo/Starknet security patterns. Each has caused real losses or was flagged in multiple audits. If you read nothing else, read these.

1. **`felt252` division is modular inverse, not floor division.** `felt252_div(10, 3)` does NOT return 3. It returns a huge field element. Never use `felt252` for financial math — use `u256` or `u128`. (Section 7)

2. **`Map.read()` returns zero on missing keys — no panic.** An attacker bypassed oracle validation by reading a non-existent key that returned zero, then signed over zeroed data. Always assert non-zero/non-default after reading from storage Maps. (Section 4, Section 16 C4 Perpetual H-01)

3. **`felt252` arithmetic wraps silently.** `balance - amount` where `amount > balance` wraps to a huge number with no error. Use `u256`/`u128` for all balances, amounts, prices. (Section 7)

4. **Floor division always favors the actor.** When burning/withdrawing, round UP against the user. When minting/depositing, round DOWN against the user. The zkLend $10M exploit chained precision loss with accumulator manipulation. (Section 3)

5. **Empty market initialization + flash loan = catastrophic.** First depositor controls the exchange rate. Lock minimum liquidity on first deposit. Applies to lending pools and ERC-4626 vaults. (Section 3)

6. **OZ embedded impls leak privileged selectors to session keys.** Every OZ version exposes new selectors (`set_public_key`, `setPublicKey`, `upgrade`). Block self-calls from session keys: `assert(call.to != get_contract_address())`. (Section 13)

7. **SNIP-9 `execute_from_outside` needs nonce + caller + time bounds.** Missing any one enables replay attacks. Signature must be validated via SNIP-12 over the full `OutsideExecution` struct. (Section 14)

8. **Starknet v0.14.0 killed v0/v1/v2 transactions and cut blocks to ~6s.** Time-dependent logic calibrated for 30s blocks is now wrong by 5x. STRK-only fees. (Section 15)

9. **`__validate__` in custom accounts must be lightweight.** No storage writes (except nonce), no external calls, bounded gas. Expensive validation griefs the sequencer. (Section 12)

10. **Checks-effects-interactions is not optional.** C4 Starknet Perpetual H-02: state diff applied before validation caused double-application. C4 Opus H-01: `charge()` called after computing withdrawal amount overwrote the result. (Section 2, Section 16)

---

## Pre-Deployment Checklist

Before any mainnet deployment:

- [ ] All tests pass (`snforge test`) including fuzz tests for arithmetic-heavy logic
- [ ] Fuzz tests written for arithmetic-heavy and state-transition logic (`snforge test --fuzzer-runs 500`)
- [ ] No `unwrap()` on user-controlled inputs — use `expect()` or pattern match
- [ ] Access control on all state-changing functions
- [ ] Zero-address checks on constructor arguments
- [ ] Initializer can only be called once (use OZ `InitializableComponent`)
- [ ] Events emitted for all state changes (upgrades, config, pausing, privileged actions)
- [ ] No storage collisions between components
- [ ] Upgrade function protected by owner/admin check
- [ ] Checks-effects-interactions pattern on all external calls
- [ ] ReentrancyGuard on functions that make external calls before state updates
- [ ] No unbounded loops on user-controlled data
- [ ] L1 handler validates `from_address` against trusted L1 contract
- [ ] Boolean returns from ERC20 `transfer`/`transfer_from` checked
- [ ] Operator precedence verified in complex boolean expressions
- [ ] Bit-packing does not exceed 251 bits for felt252
- [ ] Precision/rounding in division reviewed — truncation can be exploited (see Section 3)
- [ ] Nonces used for all signature-gated operations (see Section 5)
- [ ] No sensitive data stored in plaintext on-chain (see Section 6)
- [ ] Market initialization protected against empty-state manipulation
- [ ] Contract verified on block explorer
- [ ] `LegacyMap` migrated to `Map` (Cairo 2.7+)
- [ ] Storage `Map.read()` results validated when absence should be an error (returns zero, not panic)
- [ ] `felt252` not used for balances, amounts, prices, or counters (use `u256`/`u128`)
- [ ] SNIP-12 used for all off-chain signature verification (not raw Pedersen hashing)
- [ ] SNIP-9 `execute_from_outside` validates nonce, caller, and time bounds
- [ ] `__validate__` in custom accounts is lightweight and makes no external calls
- [ ] Liquidation/risk-management functions NOT blocked by pause mechanism
- [ ] Paymaster interactions rate-limited and allowlisted
- [ ] `NoncesComponent` from OZ used for replay protection (not hand-rolled nonces)
- [ ] V3 transaction resource bounds handled (STRK-only fees since v0.14.0)
- [ ] ERC-4626 vault first-depositor protection applied (minimum liquidity lock or virtual shares/assets) if applicable
- [ ] `PausableComponent` integrated with exclusions for liquidation/risk functions
- [ ] Public key inputs validated to lie on the STARK curve
- [ ] No legacy v0/v1/v2 transaction assumptions (deprecated since v0.14.0)
- [ ] Time-dependent logic recalibrated for ~6s block time (v0.14.0)
- [ ] Global validation functions scoped correctly — no cross-contamination where unrelated state failures block valid operations
- [ ] Per-asset risk parameters (not one-size-fits-all) for price staleness, funding caps, collateral factors
- [ ] `AccessControlDefaultAdminRulesComponent` used for admin role transfer delay

---

## 1. Access Control, Upgrades & Initializers

*Source: [Cairo Book ch104](https://book.cairo-lang.org/ch104-01-general-recommendations.html), [Code4rena Starknet Perpetual H-02](https://code4rena.com/reports/2025-03-starknet-perpetual)*

The most common critical findings in Starknet audits are "who can call this?" and "can this be re-initialized?"

### Missing Access Control

```cairo
// BAD — anyone can mint
fn mint(ref self: ContractState, to: ContractAddress, amount: u256) {
    self.erc20.mint(to, amount);
}

// GOOD — only minter role
fn mint(ref self: ContractState, to: ContractAddress, amount: u256) {
    self.access_control.assert_only_role(MINTER_ROLE);
    self.erc20.mint(to, amount);
}
```

### Unprotected Upgrade (Full Contract Takeover)

If a non-authorized user can upgrade, they replace the class with anything and get full control.

```cairo
// BAD — anyone can upgrade
fn upgrade(ref self: ContractState, new_class_hash: ClassHash) {
    self.upgradeable.upgrade(new_class_hash);
}

// GOOD — owner-only, with event
fn upgrade(ref self: ContractState, new_class_hash: ClassHash) {
    self.ownable.assert_only_owner();
    self.upgradeable.upgrade(new_class_hash);
    self.emit(Upgraded { new_class_hash });
}
```

### Re-Initializable Initializer

A publicly exposed initializer that can be called post-deploy is a frequent vulnerability.

```cairo
// BAD — can be called multiple times
fn initializer(ref self: ContractState, owner: ContractAddress) {
    self.ownable.initializer(owner);
}

// GOOD — one-shot guard
#[storage]
struct Storage {
    initialized: bool,
}

fn initializer(ref self: ContractState, owner: ContractAddress) {
    assert!(!self.initialized.read(), "ALREADY_INIT");
    self.initialized.write(true);
    self.ownable.initializer(owner);
}
```

**Rule:** If it must be external during deployment, make sure it can only be called once. If it doesn't need to be external, keep it internal.

---

## 2. Checks-Effects-Interactions (Reentrancy)

*Source: [0xEniotna/Starknet-contracts-vulnerabilities](https://github.com/0xEniotna/Starknet-contracts-vulnerabilities), Code4rena Starknet Perpetual H-02*

Code4rena's H-02 finding on Starknet Perpetual: `_execute_transfer` applied state diffs *before* performing checks. Always: check, then update state, then call external contracts.

```cairo
// BAD — state update after external call (reentrancy window)
fn withdraw(ref self: ContractState, amount: u256) {
    let caller = get_caller_address();
    let balance = self.balances.read(caller);
    assert(balance >= amount, 'Insufficient balance');

    IERC20Dispatcher { contract_address: self.token.read() }
        .transfer(caller, amount);       // external call FIRST

    self.balances.write(caller, balance - amount);  // state update AFTER
}

// GOOD — checks-effects-interactions
fn withdraw(ref self: ContractState, amount: u256) {
    let caller = get_caller_address();
    let balance = self.balances.read(caller);
    assert(balance >= amount, 'Insufficient balance');

    self.balances.write(caller, balance - amount);  // state update FIRST

    IERC20Dispatcher { contract_address: self.token.read() }
        .transfer(caller, amount);       // external call LAST
}
```

---

## 3. Precision, Rounding & Accumulator Manipulation

*Source: [BlockSec — zkLend Exploit Post-Mortem (Feb 2025)](https://blocksec.com/blog/zklend-exploit-post-mortem), [FuzzingLabs zkLend Analysis](https://fuzzinglabs.com/rediscovery-zklend-hack/)*

The zkLend exploit ($10M, Feb 12, 2025) is the largest Cairo-specific exploit to date. Root cause: precision loss through truncation in division, combined with accumulator manipulation via flash loan donations in an empty market.

### The Attack Pattern

1. **Empty market initialization** — attacker deposits 1 wei into an empty lending pool. Both `reserve_balance` and `ztoken_supply` start at 0 with `lending_accumulator = 1`.
2. **Accumulator inflation via flash loan donations** — attacker takes flash loans of 1 wei, repays 1000 wei. Excess is treated as a "donation" that inflates `lending_accumulator`. After 10 flash loans: accumulator reaches ~4.069 × 10^18.
3. **Rounding exploitation** — with a huge accumulator, `scaled_down_amount = amount / lending_accumulator` uses floor division (truncation). Burning tokens decreases `raw_balance` by only 1 unit despite burning large token amounts. Repeated deposit/withdraw cycles increment `raw_balance` by 1 each cycle.
4. **Profit extraction** — `raw_balance` reaches 1,724 → collateral value of 7,015 wstETH → borrow other assets from the market.

### Defense Patterns

```cairo
// PATTERN 1: Minimum liquidity lock (prevent empty-market manipulation)
// On first deposit, lock a minimum amount permanently
fn first_deposit(ref self: ContractState, amount: u256) {
    let MIN_LIQUIDITY: u256 = 1000;  // dead shares
    assert(amount > MIN_LIQUIDITY, 'BELOW_MIN_LIQUIDITY');
    // Mint MIN_LIQUIDITY shares to zero address (locked forever)
    self._mint(Zeroable::zero(), MIN_LIQUIDITY);
    // Mint remainder to depositor
    self._mint(get_caller_address(), amount - MIN_LIQUIDITY);
}

// PATTERN 2: Guard accumulator changes per transaction
fn settle_extra_reserve(ref self: ContractState) {
    let new_acc = self._compute_accumulator();
    let old_acc = self.lending_accumulator.read();
    let MAX_ACC_CHANGE: u256 = old_acc / 10; // max 10% change per tx
    assert(new_acc - old_acc <= MAX_ACC_CHANGE, 'ACC_CHANGE_TOO_LARGE');
    self.lending_accumulator.write(new_acc);
}

// PATTERN 3: Round UP when burning shares (penalize withdrawer, not pool)
fn burn_scaled(amount: u256, accumulator: u256) -> u256 {
    // Round up: (amount + accumulator - 1) / accumulator
    (amount + accumulator - 1) / accumulator
}
```

### Key Takeaway

Floor division in share/token math always favors the actor performing the operation. **When burning/withdrawing, round UP (against the user). When minting/depositing, round DOWN (against the user).** This ensures the pool never loses value through rounding.

### Fuzz Testing for Precision Bugs

```cairo
#[test]
#[fuzzer(runs: 1000)]
fn test_deposit_withdraw_invariant(deposit_amount: u256) {
    // After deposit + immediate full withdraw, user should get back <= deposit_amount
    // (never more, due to rounding favoring the pool)
    let shares = pool.deposit(deposit_amount);
    let withdrawn = pool.withdraw(shares);
    assert(withdrawn <= deposit_amount, 'ROUNDING_EXPLOIT');
}
```

### ERC-4626 Vault Share Manipulation

The same accumulator/precision attack from the zkLend exploit applies directly to ERC-4626 tokenized vaults (`ERC4626Component` in OZ Cairo 3.x). The first depositor can manipulate the share price by donating assets to inflate the exchange rate, causing subsequent depositors to receive fewer shares than expected.

**Two defense approaches:**

1. **Minimum liquidity lock** (described above) — the first depositor burns a small amount of shares to a dead address, establishing a baseline exchange rate that cannot be trivially inflated.
2. **Virtual shares/assets** — add 1 (or a small constant) to both the numerator and denominator in share calculations: `shares = (assets + 1) / (totalAssets + 1) * totalShares`. This eliminates the zero-denominator edge case and makes share price manipulation economically infeasible without requiring a liquidity lock. This is the approach used by OpenZeppelin's Solidity ERC-4626 implementation.

Both are valid; choose based on your protocol's constraints. Minimum liquidity lock is simpler but requires a one-time setup cost. Virtual shares are more elegant but require modifying the conversion math throughout.

### Wad Precision Truncation for Low-Decimal Tokens

*Source: [Code4rena Opus H-02 (Jan 2024)](https://code4rena.com/reports/2024-01-opus)*

Cairo's fixed-point `Wad` type (18 decimals) silently truncates when multiplied with tokens that have fewer decimals. In the Opus audit, `convert_to_yang_helper()` computed `(asset_amt * total_yang) / total_assets` — but because `Wad` multiplication divides by 1e18 internally, tokens with 8 decimals (like BTC) lost precision. A deposit of 0.0009 BTC ($36 at BTC=40K) resulted in **zero** shares.

**Rule:** When doing fixed-point math with tokens that have < 18 decimals, compute the numerator fully as `u256` before dividing. Never let intermediate `Wad` multiplication truncate low-decimal amounts to zero.

---

## 4. Cairo-Specific Pitfalls

*Source: [Cairo Book ch104](https://book.cairo-lang.org/ch104-01-general-recommendations.html)*

These are unique to Cairo and not found in Solidity auditing guides.

### Operator Precedence Bug

In Cairo, `&&` has higher precedence than `||`. Combined boolean expressions must be parenthesized.

```cairo
// BAD — && binds tighter than ||, so this means:
// mode == None || (mode == Recovery && coll_ok && debt_ok)
assert!(
    mode == Mode::None || mode == Mode::Recovery && ctx.coll_ok && ctx.debt_ok,
    "EMERGENCY_MODE"
);

// GOOD — explicit parentheses
assert!(
    (mode == Mode::None || mode == Mode::Recovery) && (ctx.coll_ok && ctx.debt_ok),
    "EMERGENCY_MODE"
);
```

### Unsigned Loop Underflow

Decrementing a `u32` counter past 0 panics. Use signed integers or explicit break.

```cairo
// BAD — panics when i decrements below 0
let mut i: u32 = n - 1;
while i >= 0 {  // always true for unsigned, then underflow panic
    process(i);
    i -= 1;
}

// GOOD — signed counter
let mut i: i32 = (n.try_into().unwrap()) - 1;
while i >= 0 {
    process(i.try_into().unwrap());
    i -= 1;
}
```

### Bit-Packing Overflow into felt252

Packing multiple fields into one `felt252` is common for gas optimization, but the sum of field sizes must not exceed 251 bits.

```cairo
// GOOD — explicit width checks before packing
fn pack_order(book_id: u256, tick_u24: u256, index_u40: u256) -> felt252 {
    assert!(book_id < (1_u256 * POW_2_187), "BOOK_OVER");
    assert!(tick_u24 < (1_u256 * POW_2_24), "TICK_OVER");
    assert!(index_u40 < (1_u256 * POW_2_40), "INDEX_OVER");
    let packed: u256 = (book_id * POW_2_64) + (tick_u24 * POW_2_40) + index_u40;
    packed.try_into().expect("PACK_OVERFLOW")
}
```

### `deploy_syscall(deploy_from_zero=true)` Collisions

Deterministic deployment from zero can collide if two contracts deploy with the same calldata. Set `deploy_from_zero` to `false` unless you specifically need deterministic addresses.

### Storage `Map.read()` Returns Zero for Non-Existent Keys (No Panic)

*Source: [Code4rena Starknet Perpetual H-01](https://code4rena.com/reports/2025-03-starknet-perpetual)*

Unlike languages that throw on missing keys, Cairo's `Map.read(key)` returns the type's default value (zero) when the key doesn't exist. This caused the H-01 finding in the Starknet Perpetual audit — an attacker used an arbitrary public key that mapped to empty storage, getting a zero value that bypassed oracle validation.

```cairo
// BAD — doesn't check if oracle exists, zero passes silently
let oracle_data = self.oracles.entry(asset_id).entry(public_key).read();
// oracle_data is 0 for non-existent keys — attacker signs over zeroed values

// GOOD — explicitly check for existence
let oracle_data = self.oracles.entry(asset_id).entry(public_key).read();
assert(oracle_data.is_non_zero(), 'ORACLE_NOT_REGISTERED');
```

**Rule:** Always validate that storage reads return non-default values when absence should be an error. This applies to all `Map` reads, not just oracle lookups.

### `get_caller_address().is_zero()` Is Useless

On Starknet, `get_caller_address()` is never the zero address (unlike Solidity's `msg.sender` for contract creation). Zero-address checks on caller are dead code.

### Unsafe `unwrap()` on User Input

*Source: [chipi-pay Nethermind AuditAgent finding #9](https://github.com/chipi-pay/sessions-smart-contract) — DoS via unsafe unwrap*

```cairo
// BAD — panics if conversion fails, exploitable DoS
let value: u64 = input.try_into().unwrap();

// GOOD — safe conversion
let value: u64 = match input.try_into() {
    Option::Some(v) => v,
    Option::None => { return 0; }  // safe failure, no panic
};
```

---

## 5. Signature Replay & Nonce Protection

*Source: [Oxor.io — Cairo Security Flaws (Aug 2024)](https://oxor.io/blog/2024-08-16-cairo-security-flaws/)*

Any signature-gated function without a nonce is replayable. An attacker can resubmit the same valid signature to execute the action multiple times.

### The Problem

```cairo
// BAD — no nonce, signature is replayable forever
fn claim_reward(
    ref self: ContractState, amount: felt252, r: felt252, s: felt252
) {
    let caller = get_caller_address();
    let msg = pedersen::pedersen(amount, caller.into());
    verify_ecdsa_signature(msg, self.signer.read(), r, s);
    // Transfer reward — attacker replays this with same (r, s) infinitely
    self._transfer_reward(caller, amount);
}
```

### The Fix — Always Include Nonce

```cairo
// GOOD — nonce prevents replay
fn claim_reward(
    ref self: ContractState, amount: felt252, r: felt252, s: felt252
) {
    let caller = get_caller_address();
    let nonce = self.nonces.read(caller);
    // Increment nonce BEFORE use (checks-effects-interactions)
    self.nonces.write(caller, nonce + 1);
    let msg = pedersen::pedersen(amount, caller.into());
    let msg_with_nonce = pedersen::pedersen(msg, nonce);
    verify_ecdsa_signature(msg_with_nonce, self.signer.read(), r, s);
    self._transfer_reward(caller, amount);
}
```

**Rule:** Every signature-verified operation must include (1) a nonce, (2) a chain_id, and (3) the contract address in the signed message to prevent cross-chain and cross-contract replay.

### Production Approach: OZ NoncesComponent

Don't roll your own nonce logic. Use OZ's `NoncesComponent`:

```cairo
use openzeppelin_utils::cryptography::nonces::NoncesComponent;

component!(path: NoncesComponent, storage: nonces, event: NoncesEvent);

#[abi(embed_v0)]
impl NoncesImpl = NoncesComponent::NoncesImpl<ContractState>;
impl NoncesInternalImpl = NoncesComponent::InternalImpl<ContractState>;

fn claim_reward(ref self: ContractState, amount: u256, nonce: felt252, signature: Span<felt252>) {
    let caller = get_caller_address();
    // Validates nonce is the next expected value AND increments it atomically
    self.nonces.use_checked_nonce(caller, nonce);
    // ... verify signature over (amount, nonce, chain_id, contract_address) ...
    self._transfer_reward(caller, amount);
}
```

`use_checked_nonce(owner, nonce)` verifies the nonce matches the expected next value and increments it in one step. `use_nonce(owner)` consumes and returns the current nonce without checking.

### SNIP-12: Typed Structured Data Signing

*Source: [OZ SNIP-12 Guide](https://docs.openzeppelin.com/contracts-cairo/3.x/guides/snip12), [SNIP-12 Spec](https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-12.md)*

SNIP-12 is Starknet's equivalent of EIP-712 — typed structured data signing that prevents signature reuse across contracts, chains, and message types. **Use SNIP-12 for all off-chain signature verification.**

```cairo
use openzeppelin_utils::cryptography::snip12;

// 1. Define your message struct
#[derive(Copy, Drop, Hash)]
struct Transfer {
    recipient: ContractAddress,
    amount: u256,
    nonce: felt252,
    expiry: u128,  // SNIP-12 has no u64, use u128 in type hash
}

// 2. Compute type hash offline and hardcode it
// starknet_keccak("Transfer(recipient:ContractAddress,amount:u256,nonce:felt,expiry:u128)")
const TRANSFER_TYPE_HASH: felt252 = 0x...; // Compute offline, don't do on-chain

// 3. Implement StructHash for your message type
// 4. Use OZ's OffchainMessageHash to compute the full hash including domain separator
```

**Key SNIP-12 security rules:**
- Domain separator MUST include `name`, `version`, `chain_id`, and `revision`
- **Breaking change:** Older revisions used `StarkNetDomain` (capital N), current uses `StarknetDomain` — mixing them produces different hashes
- Compute type hashes offline and hardcode them — on-chain computation is expensive and error-prone
- Always include a nonce and expiry in the message struct

---

## 6. Private Data in Storage

*Source: [FuzzingLabs — Top 4 Vulnerabilities (Nov 2024)](https://fuzzinglabs.com/top-4-vulnerability-cairo-starknet-smart-contract/)*

No data stored on Starknet is private. Any value written to contract storage is readable by anyone via RPC calls (`starknet_getStorageAt`). This includes "private" fields, passwords, API keys, and secrets.

```cairo
// BAD — secret is readable by anyone via RPC
#[storage]
struct Storage {
    secret: felt252,        // Anyone can read this
    admin_password: felt252, // This too
}

// GOOD — store hash, not plaintext
#[storage]
struct Storage {
    secret_hash: felt252,  // Store pedersen(secret) or poseidon(secret)
}

fn verify_secret(self: @ContractState, secret: felt252) -> bool {
    let hash = pedersen::pedersen(secret, 0);
    hash == self.secret_hash.read()
}
```

**Rule:** If your contract needs to verify a secret, store its hash on-chain and verify the preimage. Never store plaintext secrets, encryption keys, or passwords in contract storage.

---

## 7. felt252 Arithmetic & Safe Integer Types

*Source: [Oxor.io — Overflow and Underflow in Cairo](https://oxor.io/blog/2024-08-16-overflow-and-underflow-vulnerabilities-in-cairo/), [FuzzingLabs — Top 4 Vulnerabilities](https://fuzzinglabs.com/top-4-vulnerability-cairo-starknet-smart-contract/), [Crytic — Not So Smart Contracts](https://github.com/crytic/building-secure-contracts/tree/master/not-so-smart-contracts/cairo)*

The `felt252` type is a field element (0 to P-1, where P = 2^251 + 17*2^192 + 1). Arithmetic on `felt252` wraps modulo P silently — there is no overflow/underflow panic. This is the single most Cairo-specific footgun.

### The Problem

```cairo
// BAD — felt252 arithmetic wraps silently
fn vulnerable_subtract(balance: felt252, amount: felt252) -> felt252 {
    balance - amount  // If amount > balance, result wraps to a huge number (no panic!)
}

fn vulnerable_overflow(input: felt252) -> felt252 {
    let max_felt: felt252 = 0x800000000000000000000000000000000000000000000000000000000000000
        + 17 * 0x1000000000000000000000000000000000000000000000000;
    max_felt + input  // If input > 0, wraps to 0 (no panic!)
}
```

### The Fix — Use Safe Integer Types

Cairo's unsigned integer types (`u8`, `u16`, `u32`, `u64`, `u128`, `u256`) and signed types (`i8`, `i16`, `i32`, `i64`, `i128`) have built-in overflow/underflow protection. They panic on overflow, which is what you want.

```cairo
// GOOD — u256 panics on overflow/underflow
fn safe_subtract(balance: u256, amount: u256) -> u256 {
    assert(balance >= amount, 'INSUFFICIENT_BALANCE');
    balance - amount  // Would panic on underflow even without assert
}

// NOTE: In Cairo 2.x, plain a + b on integer types ALREADY panics on overflow.
// For non-panicking alternatives, use:
use core::num::traits::SaturatingAdd;
fn safe_add_saturating(a: u128, b: u128) -> u128 {
    a.saturating_add(b)  // Returns u128::MAX on overflow instead of panicking
}

// Or use overflowing_add for explicit overflow detection:
use core::integer::u128_overflowing_add;
fn safe_add_overflowing(a: u128, b: u128) -> (u128, bool) {
    match u128_overflowing_add(a, b) {
        Result::Ok(sum) => (sum, false),
        Result::Err(sum) => (sum, true),  // Overflow occurred
    }
}

// Or use wrapping_add for modular arithmetic (no panic, wraps):
use core::num::traits::WrappingAdd;
fn wrapping_add(a: u128, b: u128) -> u128 {
    a.wrapping_add(b)
}
```

### CRITICAL: `felt252` Division Is Field Division, NOT Floor Division

`felt252_div(a, b)` computes the **modular inverse**: it returns `n` such that `n * b ≡ a (mod P)`. This is NOT integer floor division. `felt252_div(10, 3)` does NOT return `3` — it returns a huge field element that, multiplied by 3 modulo P, equals 10.

```cairo
// BAD — gives completely wrong result for financial math
let price_per_unit: felt252 = felt252_div(total_cost, quantity);
// This is modular inverse, NOT 10/3 = 3

// GOOD — use integer division
let price_per_unit: u256 = total_cost / quantity;  // Floor division, panics on zero
```

**Rule:** NEVER use `felt252` for any division in financial calculations. Always use `u128`, `u256`, or `u64` which perform actual integer floor division. `felt252` division is only correct for cryptographic operations where you explicitly need modular arithmetic.

### When felt252 Is Acceptable

- **Hash computations** (pedersen, poseidon) — these are inherently modular arithmetic
- **Selectors and class hashes** — these are field elements by design
- **Storage keys** — addresses are felt252
- **Cryptographic operations** — signature verification, curve arithmetic

### When felt252 Is Dangerous

- **Balances, amounts, prices, fees** — always use `u256` or `u128`
- **Counters, indices, timestamps** — use `u64` or `u32`
- **Any user-controlled arithmetic** — never use felt252
- **Division** — `felt252_div` is modular inverse, not floor division
- **Comparisons** (`<`, `>`, `>=`) — felt252 comparisons work but can produce unexpected results near the field boundary

### Detecting felt252 Issues

Write targeted fuzz tests for functions that use felt252 arithmetic:

```cairo
#[test]
#[fuzzer(runs: 1000)]
fn fuzz_no_felt_underflow(a: felt252, b: felt252) {
    // If your function does a - b, test that the result is meaningful
    // Use u256 instead to get automatic underflow protection
    let safe_a: u256 = a.into();
    let safe_b: u256 = b.into();
    if safe_a >= safe_b {
        let result = safe_a - safe_b;
        assert(result <= safe_a, 'UNDERFLOW');
    }
}
```

> **Note:** FuzzingLabs' `sierra-analyzer` had a `felt_overflow` detector but the repo is no longer maintained. Until a replacement ships, fuzz testing is the primary detection method.

---

## 8. Storage Layout Security

*Source: [Starknet Docs — Storage](https://docs.starknet.io/build/starknet-by-example/basic/storage), [Cairo Book — Security (ch104)](https://book.cairo-lang.org/ch104-00-starknet-smart-contracts-security.html)*

Starknet storage is a flat key-value space of 2^251 slots, each holding one `felt252`. Understanding this model is critical for upgrade safety and collision avoidance.

### Storage Address Derivation

```
// Simple variables: base = sn_keccak("variable_name")
// Map entries: address = pedersen(sn_keccak("map_name"), key)
// Nested maps: address = pedersen(pedersen(sn_keccak("map_name"), key1), key2)
// Component storage: base = sn_keccak("component_name") (with substorage(v0))
```

### `LegacyMap` → `Map` Migration (Cairo 2.7+)

Cairo 2.7.0 introduced `Map<K, V>` (from `core::starknet::storage::Map`) to replace `LegacyMap<K, V>`. The storage layout is identical, so migration is safe for upgradeable contracts. `LegacyMap` is deprecated but still compiles on current Cairo versions — it emits a deprecation warning, not an error. Projects on older Scarb versions that cannot upgrade immediately can defer this migration, but should plan for it: `LegacyMap` may be removed in a future Cairo edition.

```cairo
// DEPRECATED — LegacyMap (Cairo < 2.7)
#[storage]
struct Storage {
    balances: LegacyMap<ContractAddress, u256>,
}
// Access: self.balances.read(addr), self.balances.write(addr, val)

// CURRENT — Map (Cairo 2.7+)
use core::starknet::storage::Map;
#[storage]
struct Storage {
    balances: Map<ContractAddress, u256>,
}
// Access: self.balances.entry(addr).read(), self.balances.entry(addr).write(val)
```

### Storage Nodes and `Vec` (Cairo 2.7+)

Cairo 2.7+ introduced `#[starknet::storage_node]` for composable nested storage and `Vec` for dynamic-length storage arrays:

```cairo
use core::starknet::storage::Vec;

// Storage Node — structured nested storage
#[starknet::storage_node]
struct UserData {
    balance: u256,
    last_active: u64,
}

#[storage]
struct Storage {
    users: Map<ContractAddress, UserData>,   // Nested: users.entry(addr).balance.read()
    pending_items: Vec<u256>,                 // Dynamic array in storage
}
```

**Security note for Vec:** `Vec` has no built-in length cap. User-growable Vecs can be used for DoS via unbounded storage growth. Always cap Vec length in user-facing functions.

### Storage Collision Between Components

If two components use the same storage variable name, their base addresses will collide. OZ's `#[substorage(v0)]` pattern avoids this for components, but custom storage vars can still collide.

```cairo
// BAD — two components both define a storage var named "balance"
// They will write to the same slot and corrupt each other's data

// GOOD — use unique prefixed names or rely on OZ component patterns
#[storage]
struct Storage {
    #[substorage(v0)]
    erc20: ERC20Component::Storage,       // OZ handles namespacing
    #[substorage(v0)]
    ownable: OwnableComponent::Storage,   // No collision with erc20
    my_custom_balance: u256,              // Explicit, unique name
}
```

**Storage Node collision note:** Storage nodes hash member names with `selector!("name")`. Two unrelated storage nodes with the same member name in different contexts won't collide because the parent path differs. However, custom `Store` implementations that pack data into raw slots bypass this namespacing.

### Upgrade Storage Layout Rules

When upgrading a contract (replacing the class hash), storage persists but layout must be compatible:

```
SAFE:
  - Add new storage variables (new base addresses)
  - Append new fields to the end of packed structs
  - Add new component substorages
  - Migrate LegacyMap to Map (same layout)

UNSAFE (will corrupt existing data):
  - Remove or reorder existing storage variables
  - Change the type of an existing variable (e.g., u128 -> u256)
  - Rename a storage variable (changes base address)
  - Change a component's substorage name
  - Change Map key types
```

### Multi-Slot Values

Types larger than 252 bits (e.g., `u256`) span consecutive slots. A `u256` uses slot `base + 0` for the low 128 bits and `base + 1` for the high 128 bits. Packing multiple small values into one `felt252` is a gas optimization but must respect the 251-bit limit (see Section 4, Bit-Packing).

---

## 9. Token Integration Pitfalls

*Source: [Cairo Book ch104](https://book.cairo-lang.org/ch104-01-general-recommendations.html)*

### Always Check Boolean Returns

While OpenZeppelin's ERC20 reverts on failure, not all ERC-20 implementations do. Some return `false` without panicking.

```cairo
// BAD — ignores return value
IERC20Dispatcher { contract_address: token }.transfer(to, amount);

// GOOD — check the return
let success = IERC20Dispatcher { contract_address: token }.transfer(to, amount);
assert(success, 'Transfer failed');
```

### CamelCase / snake_case Dual Interfaces

Most ERC20 tokens on Starknet use `snake_case`. Legacy tokens may have `camelCase` entrypoints (`transferFrom` vs `transfer_from`). If your contract interacts with arbitrary tokens, handle both or verify the tokens you'll integrate with.

### ERC20Permit — Off-Chain Approval Attack Surface

OZ Cairo 3.x added `ERC20Permit`, enabling token `approve` via off-chain SNIP-12 signatures. This is a new attack surface:

- **Front-running:** Permit signatures can be front-run — someone sees the permit in the mempool and submits it first. The standard handles this gracefully (the approve succeeds if allowance matches), but protocols should not assume permit calls are exclusive.
- **Expired permits:** Always check the deadline/expiry. A signed permit with a far-future expiry is a long-lived approval.
- **Nonce correctness:** Permit uses the owner's nonce from `NoncesComponent`. A consumed nonce invalidates the permit.
- **Integration rule:** When integrating with permit-enabled tokens, accept that `permit` + `transferFrom` may happen atomically in one call or separately. Don't rely on the approval being set in a previous transaction.

---

## 10. L1/L2 Bridging Safety

*Source: [Crytic/building-secure-contracts](https://github.com/crytic/building-secure-contracts/tree/master/not-so-smart-contracts/cairo)*

### L1 Handler Must Validate Caller

The `#[l1_handler]` attribute marks an entrypoint as callable from L1. Always validate that `from_address` is the trusted L1 contract.

> **Type note:** `from_address` in `#[l1_handler]` is `felt252`, NOT `ContractAddress`. This is a common source of bugs — you cannot use `ContractAddress` comparison directly. Compare as `felt252` or convert explicitly.

```cairo
// BAD — anyone on L1 can call this
#[l1_handler]
fn handle_deposit(
    ref self: ContractState,
    from_address: felt252,
    account: ContractAddress,
    amount: u256
) {
    self.balances.write(account, self.balances.read(account) + amount);
}

// GOOD — validate L1 caller
// NOTE: from_address is felt252, NOT ContractAddress.
// Store your L1 bridge address as felt252 to match, or convert explicitly.
#[l1_handler]
fn handle_deposit(
    ref self: ContractState,
    from_address: felt252,  // felt252 — not ContractAddress!
    account: ContractAddress,
    amount: u256
) {
    let l1_bridge: felt252 = self.l1_bridge.read(); // stored as felt252
    assert!(!l1_bridge.is_zero(), "UNINIT_BRIDGE");
    assert!(from_address == l1_bridge, "ONLY_L1_BRIDGE");
    self.balances.write(account, self.balances.read(account) + amount);
}
```

### L1-to-L2 Message Failure

L1->L2 messages can fail silently if the L2 handler reverts. The message stays in a "pending" state and can be retried, but the L1 side may have already updated its state. Design for idempotent handlers or include replay protection.

### L1/L2 Address Conversion

L1 (Ethereum) addresses are 20 bytes. Starknet addresses are felt252. Incorrect conversion or comparison between the two is a common bug. Always use explicit conversion functions and never compare raw values across domains.

### Replay Protection

Cross-chain messages need nonces or unique identifiers to prevent replay. If a message can be re-consumed, an attacker can double-credit.

### Bridge Withdrawal Limits (StarkGate Pattern)

*Source: [StarkGate 2.0 `token_bridge.cairo`](https://github.com/starknet-io/starkgate-contracts), [Starknet Docs — StarkGate](https://docs.starknet.io/learn/protocol/starkgate)*

StarkGate implements a daily withdrawal limit of 5% TVL per token (`DEFAULT_DAILY_WITHDRAW_LIMIT_PCT = 5`). A `SECURITY_AGENT` role can freeze withdrawals; lifting the freeze requires a quorum of `SECURITY_ADMIN` signers. This pattern limits damage from exploits to a single day's quota.

**Rule:** Any bridge or high-TVL vault should implement per-token daily withdrawal caps, a security freeze role (single key, fast response), and a multi-sig requirement to unfreeze. Do not let a single key both freeze and unfreeze.

### Unprotected Escrow Funds (MakerDAO DAI Bridge)

*Source: [ChainSecurity — MakerDAO StarkNet-DAI-Bridge Audit (2021)](https://chainsecurity.com/wp-content/uploads/2021/12/ChainSecurity_MakerDAO_StarkNet-DAI-Bridge_audit.pdf)*

ChainSecurity found a Critical finding in the MakerDAO StarkNet-DAI-Bridge: escrow funds on L1 were unprotected, allowing unauthorized access. The audit covered both Solidity L1 contracts and the Cairo L2 `dai.cairo` contract. Additional findings included 1 High, 5 Medium, and 5 Low — all fixed.

**Pattern:** L1/L2 bridges must protect escrowed funds on both sides. The L1 escrow is only as safe as the L2 handler validation, and vice versa.

---

## 11. Economic / DoS Patterns

*Source: [Cairo Book ch104](https://book.cairo-lang.org/ch104-01-general-recommendations.html)*

### Unbounded Loops

User-controlled iterations can exceed the Starknet steps limit, bricking the contract permanently — no one can interact with it anymore.

```cairo
// BAD — unbounded loop, attacker grows the list to exceed step limit
fn process_all(ref self: ContractState) {
    let mut i = 0;
    let count = self.pending_count.read();
    while i < count {
        self._process(i);
        i += 1;
    }
}

// GOOD — pagination pattern with bounded iterations
fn process_batch(ref self: ContractState, start: u64, max: u64) -> u64 {
    let mut i = start;
    let end = core::cmp::min(self.pending_count.read(), start + max);
    while i < end {
        self._process(i);
        i += 1;
    }
    end  // return next cursor
}
```

### Bad Randomness

Never use `block_timestamp`, `block_number`, or transaction hashes as randomness sources. They are known to validators/sequencers before execution. Use Pragma VRF or similar oracle-based randomness.

### Pause Mechanism — Don't Pause Liquidations

*Source: [Code4rena Starknet Perpetual L-05](https://code4rena.com/reports/2025-03-starknet-perpetual)*

When implementing `PausableComponent`, do NOT apply `assert_not_paused()` to liquidation or risk-management functions. Blocking liquidations during an emergency pause compounds the crisis — insolvent positions can't be closed, leading to bad debt accumulation.

```cairo
// BAD — pause blocks liquidation
fn liquidate(ref self: ContractState, position_id: u64) {
    self.pausable.assert_not_paused(); // Blocks during emergency!
    self._liquidate(position_id);
}

// GOOD — liquidation always available, other functions paused
fn open_position(ref self: ContractState, ...) {
    self.pausable.assert_not_paused(); // Paused during emergency
    // ...
}

fn liquidate(ref self: ContractState, position_id: u64) {
    // No pause check — must always be available
    self._liquidate(position_id);
}
```

---

## 12. Account Abstraction Security

*Source: [Starknet Docs — Account Abstraction](https://docs.starknet.io/build/starknet-by-example/advanced/account-abstraction)*

Starknet's native account abstraction means every account is a smart contract with `__validate__` and `__execute__` entry points. This is a unique attack surface.

### `__validate__` Constraints

`__validate__` runs before `__execute__` and has strict constraints:
- **Limited gas** — cannot perform expensive computation
- **Cannot modify storage** (except the nonce)
- **If `__validate__` fails, the sequencer loses gas** — no fee is charged to the account, but the sequencer still consumed resources for the validation attempt. This is a practical gotcha when testing custom accounts: failed validations cost the network real gas but produce no state changes or receipts.
- Must return `VALID` (felt252 value of `'VALID'`) or the transaction is rejected

### Sequencer DoS via `__validate__`

A malicious account can implement `__validate__` to always succeed initially but fail on re-execution (after the sequencer has committed gas). This griefs sequencers. Mitigation is sequencer-side (reputation systems, deposit requirements), but be aware when deploying custom account contracts.

### Custom Account Security Rules

```cairo
// Required entrypoints for an account contract
#[abi(embed_v0)]
fn __validate__(ref self: ContractState, calls: Array<Call>) -> felt252 {
    // 1. Verify signature (MUST be fast and cheap)
    // 2. Validate nonce (handled by protocol, but check custom logic)
    // 3. Do NOT make external calls
    // 4. Do NOT write to storage (except nonce)
    starknet::VALIDATED  // Return 'VALID'
}

#[abi(embed_v0)]
fn __execute__(ref self: ContractState, calls: Array<Call>) -> Array<Span<felt252>> {
    // 1. Assert caller is the protocol (assert_only_protocol)
    // 2. Verify correct tx version
    // 3. Execute calls
    // 4. Emit TransactionExecuted event
    execute_multicall(calls.span())
}
```

---

## 13. Session Key Security

*Source: [chipi-pay SNIP draft and Nethermind AuditAgent findings](https://github.com/chipi-pay/sessions-smart-contract) — 18 findings across 4 scans*

For contracts implementing session key delegation (relevant to AI agents):

### Admin Selector Blocklist

Session keys MUST NOT be able to call privileged functions. Each of these was discovered in a separate Nethermind audit scan:

```cairo
const BLOCKED_SELECTORS: [felt252; 7] = [
    selector!("upgrade"),                   // scan 1: contract replacement
    selector!("add_or_update_session_key"), // scan 1: create unrestricted sessions
    selector!("revoke_session_key"),        // scan 1: revoke other sessions
    selector!("__execute__"),               // scan 2: nested execution privilege escalation
    selector!("set_public_key"),            // scan 3: owner key rotation (OZ PublicKeyImpl)
    selector!("setPublicKey"),              // scan 3: owner key rotation (OZ PublicKeyCamelImpl)
    selector!("execute_from_outside_v2"),   // scan 3: nested SNIP-9 double-consumption
];
```

**Key lesson:** The denylist approach is inherently fragile — each audit scan found new selectors. Prefer the self-call block (below) as the primary defense.

### Self-Call Block (Primary Defense)

Block ALL calls where `call.to == get_contract_address()` when the session has no explicit whitelist. This eliminates the entire class of privilege escalation via self-calls, protecting against any future OZ embedded impl exposing new privileged selectors.

```cairo
// In validation, when allowed_entrypoints_len == 0:
for call in calls {
    assert(call.to != get_contract_address(), 'SESSION_NO_SELF_CALL');
}
```

> **OZ version note:** OZ 3.x `AccountComponent` has evolved its embedded impls and selectors compared to earlier versions. The exact set of privileged selectors exposed may differ between OZ v0.x, v2.x, and v3.x. The self-call block pattern above remains the primary defense regardless of OZ version, because it protects against the entire class of privilege escalation without enumerating specific selectors.

### Spending Limits (Value Control)

Selector whitelists control *which functions* a session can call, but not *how much value* each call moves. A session authorized to call `transfer` can transfer the entire balance.

```cairo
struct SpendingPolicy {
    token_address: ContractAddress,
    max_amount_per_call: u256,
    max_amount_per_window: u256,    // rolling window cap
    window_seconds: u64,             // e.g., 86400 = 24h
    amount_spent_in_window: u256,
    window_start: u64,
}
```

**Why rolling window instead of total cap?** A total cap (`max = 100 USDC`) doesn't protect against burst attacks — the attacker drains it in one call. A rolling window (`max 10 USDC per 24h`) limits damage even if the key is compromised for days.

### Call Consumption Ordering

*Source: chipi-pay Nethermind scan 2, finding #3*

Increment `calls_used` AFTER signature verification, not before. Otherwise a session with `max_calls = 1` fails on its first valid use because the counter was incremented before the limit check runs.

### `is_valid_signature` Has No Call Context

*Source: chipi-pay Nethermind scan 1, finding #5*

`is_valid_signature(hash, signature)` receives only hash and signature — no calls. It cannot enforce selector whitelists. Enforce whitelists in `__validate__` and `execute_from_outside_v2` where calls are available. This is an inherent ERC-1271 limitation, not a bug.

---

## 14. SNIP-9 Outside Execution Security

*Source: [SNIP-9 Spec](https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-9.md), [Starknet.js Outside Execution Guide](https://starknetjs.com/docs/guides/outsideExecution)*

SNIP-9 enables meta-transactions: a third party submits transactions on behalf of an account using the account's signature. This is a major attack surface.

### How It Works

An `OutsideExecution` object contains:
- `caller` — who is allowed to submit (or `'ANY_CALLER'` for anyone)
- `execute_after` / `execute_before` — time window
- `nonce` — dedicated outside-execution nonce (separate from tx nonce)
- `calls` — the actual calls to execute

The account signs this typed data (SNIP-12 format), and any permitted caller can submit it within the time window.

### Security Rules

```cairo
// 1. ALWAYS validate and consume the outside-execution nonce
// The nonce is separate from the normal transaction nonce.
// If not consumed, the same signed payload can be replayed.
assert(!self.outside_nonces.read(nonce), 'NONCE_ALREADY_USED');
self.outside_nonces.write(nonce, true);

// 2. Validate caller
let outside_caller = outside_execution.caller;
if outside_caller != 'ANY_CALLER'.try_into().unwrap() {
    assert(get_caller_address() == outside_caller, 'INVALID_CALLER');
}

// 3. Validate time bounds
let now = get_block_timestamp();
assert(now > outside_execution.execute_after, 'TOO_EARLY');
assert(now < outside_execution.execute_before, 'TOO_LATE');
```

### Common Vulnerabilities

- **Missing nonce consumption** — allows unlimited replay of a signed outside execution within the time window
- **Overly permissive `ANY_CALLER`** — anyone can submit the transaction, not just the intended relayer
- **Wide time windows** — `execute_before` set too far in the future gives attackers more time to replay
- **Nested reentrancy** — `execute_from_outside` calling `__execute__` calling `execute_from_outside` again. Block this with ReentrancyGuard or explicit nesting checks
- **Missing SNIP-12 domain binding** — signatures must include `chain_id` and contract version to prevent cross-chain replay

### Interaction with Session Keys

When combining SNIP-9 with session keys (Section 13), the session key's `execute_from_outside_v2` selector should be in the blocklist to prevent a session key from creating nested outside executions that bypass call limits.

---

## 15. Starknet Protocol Security Considerations

*Source: [Starknet Version Notes](https://docs.starknet.io/learn/cheatsheets/version-notes), [Starknet v0.14.0 "Grinta" Announcement](https://starknet.io/blog/starknet-grinta-the-architecture-of-a-more-decentralized-future)*

### Starknet v0.14.0 "Grinta" (Sep 1, 2025) — Breaking Changes

Grinta introduced multi-sequencer architecture (three independent sequencers with Tendermint consensus), a mempool, fee market, and subsecond pre-confirmations.

**Breaking changes that affect deployed contracts:**

- **v0, v1, v2 transactions are no longer supported.** Any contracts or tooling relying on legacy transaction types will fail. Accounts that lack `__validate__` must be called via the new `meta_tx_v0` syscall through v3 transactions. This is a hard break.
- **Block time shortened from ~30s to ~6s.** All time-dependent logic (funding rate calculations, price staleness windows, oracle freshness checks, time-locked operations) must be recalibrated. A 10-block window went from ~5 minutes to ~1 minute.
- **L2 gas fee market (EIP-1559 style).** L2 gas now has a dynamic base price. Contracts that estimate or hardcode gas costs will be wrong. Use current pricing from `get_execution_info`.
- **Transactions with internal calls to `__execute__` are reverted.** If your contract makes calls to an entry point literally named `__execute__`, those transactions will revert under v0.14.0.

**Security implications:**

- **MEV risk** — with a mempool and multiple sequencers, transaction ordering is no longer deterministic. Contracts sensitive to execution ordering (DEXes, liquidations) must implement slippage protection and deadline checks
- **Sequencer reorgs** — the Sep 2, 2025 incident showed reorgs are possible when sequencers diverge. Design for idempotent operations where possible
- **L1 handler failures** — failed L1 handlers are now included as `REVERTED` in blocks (bounded execution resources). Contracts relying on L1 handlers must handle reverts gracefully

### Sequencer-Prover Inconsistency (Zellic/Starknet OS Audit)

*Source: [Starknet Community Forum — Remediating a potential sequencer-prover inconsistency](https://community.starknet.io/t/remediating-a-potential-sequencer-prover-inconsistency-in-the-cairo-vm/115313)*

Zellic auditor @fcremo discovered an opcode with different validation logic between the RustVM (sequencer) and the Cairo AIR (prover). A transaction that passed sequencer validation could fail proof verification, or vice versa. StarkWare patched this as an immediate fix in v0.13.3. LambdaClass confirmed the impact on their VM implementation.

**This is a novel vulnerability class unique to STARK-based systems.** Contracts themselves cannot cause or prevent it, but developers should know: the trust model assumes sequencer and prover agree on all execution semantics. If they diverge, valid-looking transactions can fail at proof time, or invalid ones could pass sequencing. This is why Cairo VM formal verification (see Sources) matters.

### Starknet v0.14.1 (Dec 2025) — BLAKE Hash Migration

v0.14.1 migrated from Poseidon to BLAKE hash functions for `compiled_class_hash` computation. If your contract or tooling computes or verifies class hashes, ensure you use the correct hash function for the target Starknet version.

### V3 Transaction Resource Bounds

Since v0.13.0, V3 transactions use separate `L1_GAS` and `L2_GAS` resource bounds instead of a single `max_fee`. Contracts that validate or limit fees (e.g., account contracts during escapes) must check both resource types. See the ConsenSys Argent finding in Section 16 for a real example of this bug.

### Paymaster Security Considerations

Starknet's fee abstraction (via AVNU paymaster, Cartridge paymaster, etc.) allows third parties to pay gas on behalf of users. Security considerations:

- **Griefing:** A malicious account can pass `__validate__` but intentionally fail `__execute__`, wasting the paymaster's gas. Paymasters should implement reputation systems or require pre-deposits.
- **Token-based paymasters** must lock the user's payment tokens (e.g., ERC20) BEFORE paying gas, or the user can drain the paymaster by failing after gas is consumed.
- **Allowlists:** Production paymasters should maintain a whitelist of approved contracts/entrypoints to prevent abuse.
- **Rate limiting:** Per-account or per-session rate limits prevent a single agent from exhausting the paymaster's gas budget.

---

## 16. Real Audit Findings Reference

### zkLend Exploit — $10M Loss (February 12, 2025)

*Source: [BlockSec Post-Mortem](https://blocksec.com/blog/zklend-exploit-post-mortem), [SolidityScan Analysis](https://blog.solidityscan.com/zklend-hack-analysis), [FuzzingLabs](https://fuzzinglabs.com/rediscovery-zklend-hack/)*

- **Root cause:** Precision loss through truncation in `safe_decimal_math` division, combined with accumulator manipulation via flash loan donation mechanism in an empty market.
- **Impact:** Attacker inflated collateral from 1 wei to 7,015 wstETH, then borrowed other assets. Stolen funds bridged to Ethereum and attempted laundering via Railgun.
- **Recovery:** Railgun's compliance policies partially blocked the laundering attempt. The attacker later sent an on-chain message to zkLend and partial fund recovery negotiations followed. Not all funds were recovered.
- **Key lesson:** Empty market initialization + flash loan donation + floor division = catastrophic precision exploit. Detectable with fuzz tests targeting deposit/withdraw invariants.
- **Mitigation:** Minimum liquidity lock on first deposit, accumulator change caps, round-up on burns. (See Section 3 above.)

### CVE-2024-45304 — OpenZeppelin Cairo Ownership Bug

OZ Cairo Contracts before v0.16.0: `renounce_ownership` could be used to transfer ownership unintentionally. Fixed in v0.16.0.

### ConsenSys Diligence — Argent Account Starknet V3 (Jan 2024)

*Source: [ConsenSys Diligence Report](https://diligence.consensys.io/audits/2024/01/argent-account-argent-multisig-starknet-transaction-v3-updates/)*

- **Major — Lack of Fee Limits for V3 Transactions:** V3 transactions introduced separate L1_GAS and L2_GAS resource bounds, but only the `tip` was capped for escape transactions. A malicious Guardian could set excessive `max_price_per_unit` on L1_GAS or L2_GAS to drain the account. Fixed by introducing `MAX_ESCAPE_MAX_FEE_STRK = 50 STRK` and `MAX_ESCAPE_TIP_STRK = 1 STRK`.
- **Minor — `__validate_deploy__` reused `assert_correct_invoke_version`:** Deploy transactions should have their own version check for better maintainability and correctness.
- **Minor — `OUTSIDE_EXECUTION_TYPE_HASH` comment mismatch:** Hardcoded hash constant was correct but comments described the wrong preimage string.
- **Minor — Self-written `get_execution_info`:** Duplicate implementations of stdlib functions. Use `starknet::info` module directly.

**Pattern:** When Starknet introduces new transaction versions, all fee-limiting logic must be reviewed. Fee caps that work for V1 may not cover V3 resource bounds.

### Code4rena Starknet Perpetual (Mar–Apr 2025) — 2 High, 3 Medium, 14 Low

*Source: [Code4rena Report](https://code4rena.com/reports/2025-03-starknet-perpetual), 39 Cairo contracts, 3,846 lines*

- **H-01 — Malicious signed price injection:** `_validate_oracle_signature` reads `asset_oracle` storage for a public key but doesn't panic on non-existent key (returns zero). Attacker generates signature over zeroed-out packed values and injects arbitrary price. Fix: panic if `packed_asset_oracle` is zero.
- **H-02 — `_execute_transfer` wrong order of operations:** State diff applied before health check, so the check re-applies the diff and rejects valid transfers. Classic checks-effects-interactions violation.
- **M-01 — Deleveragable positions can't be fully liquidated:** When a position is fully liquidated (`TR == 0`), the `assert_healthy_or_healthier` check panics on `total_risk.is_zero()`, blocking liquidation of insolvent positions.
- **M-02 — Liquidatable positions forced into opposite:** Long positions can be forced into short during liquidation and vice versa.
- **M-03 — Stale prices in `funding_tick()`:** Inactive price data used for funding calculations.
- **L-03 — Owner account overwrite:** Missing validation allows owner to be overwritten without proper authorization flow.
- **L-04 — Missing curve validation for public keys:** Public keys in `new_position` not validated against the Stark curve. Always verify that public keys lie on the STARK curve; an invalid key creates permanently unusable state.
- **L-05 — Liquidation blocked by pause:** Applying `assert_not_paused()` to liquidation blocked risk management during emergencies. Liquidation must always be available. (See Section 11, "Pause Mechanism — Don't Pause Liquidations.")
- **L-06 — Global validation DoS:** `validate_assets_integrity()` checks ALL active assets, blocking operations on unrelated assets when one has stale data. (See Section 18, "DeFi Protocol Security Patterns.")
- **L-07 — Stale prices for inactive assets:** Inactive assets can't have prices updated but their last price is still used for settlement with no freshness check.
- **L-08 — Collateral-only users blocked:** Users with zero synthetic exposure blocked from withdrawing collateral because global validation ran unconditionally.

**Pattern:** Storage reads that return default values (zero) on missing keys are a Cairo-specific footgun. Always explicitly check that a storage read returned a non-default value.

### Code4rena Opus (Jan 2024) — 4 High, 9 Medium

*Source: [Code4rena Opus Report](https://code4rena.com/reports/2024-01-opus), 15 Cairo contracts, 4,056 lines*

The first major Cairo DeFi competitive audit on Code4rena. Key findings:

- **H-02 — Wad precision truncation for low-decimal tokens:** `convert_to_yang_helper()` lost precision for tokens with < 18 decimals due to intermediate Wad multiplication truncating to zero. A BTC deposit worth $36 resulted in 0 shares. (See Section 3, "Wad Precision Truncation.")
- **H-03 — Redistribution array index mismatch:** `redistribute_helper` maintained two arrays (`updated_trove_yang_balances` and `new_yang_totals`) but a `continue` statement caused them to go out of sync. Attacker could keep collateral while having debt redistributed away — debt zeroed, yangs kept.
- **H-04 — Recovery mode manipulation within single transaction:** Attacker opens a large enough position to push the system into recovery mode, which lowers liquidation thresholds, then liquidates healthy troves — all in one tx. Flash-loan amplifiable.
- **M-03 — ERC-4626 inflate mitigation insufficient:** The first-depositor share inflation attack was not fully mitigated, reinforcing the need for minimum liquidity locks.

**Pattern:** DeFi protocols using custom fixed-point types (Wad, Ray) must test with tokens of varying decimals. Array synchronization bugs in loop-with-continue are a Cairo-specific code smell. Recovery mode / global state changes must not be triggerable and exploitable within a single transaction.

### ChainSecurity — Starknet Perpetual (2025)

*Source: [ChainSecurity Report](https://www.chainsecurity.com/security-audit/starkware-starknet-perpetual)*

Independent audit alongside Code4rena. Key findings:

- **Rounding Is Not Always in Favor of the System:** Arithmetic rounding in settlement/funding calculations sometimes favored the user instead of the protocol, allowing slow value extraction over many transactions.
- **Insurance Fund Cannot Always Be the Deleverager:** Edge cases where the insurance fund could not fulfill its role as deleverager for insolvent positions.
- **Loosely Restricted Liquidations:** Operator had more latitude than documented to execute liquidations.

**Pattern:** Always round in favor of the protocol/pool/system, never the user. Verify this direction for every division in financial math. Insurance fund/backstop logic must handle edge cases (zero balance, concurrent liquidations).

### chipi-pay Session Contract — 18 Findings, 4 Nethermind Scans

*Source: [chipi-pay/sessions-smart-contract](https://github.com/chipi-pay/sessions-smart-contract)*

- Scan 1: 10 findings (3 High — unrestricted `__execute__` caller, whitelist bypass in `is_valid_signature`, call-limit bypass via `calls_used` reset)
- Scan 2: 3 findings (1 High — nested `__execute__` privilege escalation)
- Scan 3: 5 findings (2 High — `set_public_key`/`setPublicKey` not in blocklist)
- Scan 4: 0 findings — clean report after self-call block + expanded blocklist

**Pattern:** Every scan found new privileged selectors exposed by OZ embedded implementations. The self-call block (scan 4) eliminated the entire vulnerability class.

### Nethermind Public Cairo/Starknet Audit Catalogue

*Source: [NethermindEth/PublicAuditReports](https://github.com/NethermindEth/PublicAuditReports)*

Nethermind has published 25+ Cairo/Starknet-specific audit reports covering core ecosystem protocols:

| Report | Protocol | Focus |
|--------|----------|-------|
| NM0050, NM0064 | StarkGate | L1/L2 token bridge |
| NM0052 | Argent Account | Starknet smart wallet |
| NM0054 | Aave L2 | Lending protocol on Starknet |
| NM0056, NM0120 | ZKX | Perpetual DEX |
| NM0058, NM0097, NM0161, NM0392, NM0462 | zkLend | Lending, zkToken, liquid staking, recovery |
| NM0060 | MySwap / Braavos | AMM / wallet |
| NM0061 | Cartridge | Gaming account |
| NM0135 | Starknet ID | Identity / naming |
| NM0141, NM0578 | AVNU | DEX aggregator, forwarder |
| NM0147 | Pragma | Oracle network |
| NM0153 | Carmine | Options protocol |
| NM0159 | Dojo | Gaming engine |
| NM0180 | JediSwap | AMM |
| NM0194 | Starknet Token Distributor | STRK distribution |
| NM0237 | LayerAkira | Order book DEX |
| NM0259 | Starknet Nova | Core protocol |
| NM0337 | StakeStark | STRK staking |
| NM0544A, NM0544B | Piltover, Token Bridge | Core Starknet bridge |

**Use these as reference when building similar protocol types.** Each report PDF is available at the Nethermind repo.

### Code4rena LayerZero Starknet Endpoint (Oct–Nov 2025) — 0 High, 0 Medium, 6 Low

*Source: [Code4rena Report](https://code4rena.com/reports/2025-10-layerzero-starknet-endpoint), 46 Cairo files*

Cross-chain messaging endpoint in Cairo. No H/M findings, but Low findings contain useful patterns:

- **L-02 — Allowance-sweeping refund DoS:** `_refund_native()` tried to refund `allowance - fee` instead of `min(allowance - fee, balance)`. Users with standard large ERC20 approvals couldn't send messages. **Pattern:** When refunding excess tokens via `transferFrom`, cap the refund to `min(excess, sender_balance)`. Never assume `balance >= allowance`.
- **L-03 — Nilified messages re-committable:** `commit()` could overwrite `NIL_PAYLOAD_HASH` because `_has_payload_hash()` only checked `!= EMPTY_PAYLOAD_HASH`. **Pattern:** State invalidation (nilification/burning/blacklisting) must be checked explicitly before any state overwrite. Don't rely on "not empty" as a proxy for "valid."

### Cairo Security Clan — 30+ Cairo Audit Reports

*Source: [Cairo-Security-Clan/Audit-Portfolio](https://github.com/Cairo-Security-Clan/Audit-Portfolio)*

Starknet-native audit firm with 30+ public Cairo audit PDFs covering major ecosystem protocols:

| Protocol | Report |
|----------|--------|
| Ekubo | `Ekubo_Audit_Report.pdf` |
| Vesu | 7 reports (Core, Extensions, Liquidate, Multiply, Periphery, Updates) |
| Opus | `Opus_Audit_Report.pdf` |
| Paradex | `Paradex_Audit_Report.pdf` |
| Hyperlane | `Hyperlane_Audit_Report.pdf` + update |
| Clober | `Clober_Audit_Report.pdf` |
| Layer Akira | `Layer_Akira_Audit_Report.pdf` |
| Nimbora | `Nimbora Audit Report.pdf` |
| Nostra Pools | `Nostra Pools Security Review by 0xerim.pdf` |
| AVNU DCA | `Avnu_DCA_Audit_Report.pdf` |
| Argent Gifting | `Argent_Gifting_Audit_Report.pdf` |
| Starknet ID | `Starknet_ID_Audit_Report.pdf` |

**Use these as reference when building similar protocol types.** All PDFs are in the GitHub repo.

### ChainSecurity — Vesu Protocol (2024)

*Source: [ChainSecurity Report](https://www.chainsecurity.com/security-audit/vesu-protocol-smart-contracts)*

Permissionless DeFi lending protocol audit. All issues were fixed, but ChainSecurity noted **elevated residual risk** due to project complexity and limited internal QA (single developer). Key covered areas: pool isolation, asset solvency, oracle security, access control.

**Pattern:** For complex DeFi protocols, a single audit is not sufficient. ChainSecurity explicitly flagged that novel issues and regressions appeared during the last review cycle despite earlier fixes. Budget for multiple audit cycles and invest in internal security-focused QA (thorough unit/regression testing).

---

## 17. OpenZeppelin Cairo Security Components

*Source: [OZ Cairo 3.0 Security Docs](https://docs.openzeppelin.com/contracts-cairo/3.0.0-alpha.1/security)*

OZ Cairo provides core security components. Use them instead of rolling your own.

> **OZ v3.0.0 Import Path Migration (breaking):** In v3.0.0, `execute_single_call`, `execute_calls`, and `assert_valid_signature` moved from `openzeppelin_account::utils` to `openzeppelin_utils::execution`. If you're upgrading from v2.x, update these imports or compilation will fail. The `openzeppelin_interfaces` package versioning is now decoupled from the main umbrella package.

**Exact import paths (OZ Cairo 3.0.0):**
```cairo
use openzeppelin_security::InitializableComponent;
use openzeppelin_security::PausableComponent;
use openzeppelin_security::ReentrancyGuardComponent;
use openzeppelin_access::ownable::OwnableComponent;
use openzeppelin_access::accesscontrol::AccessControlComponent;
use openzeppelin_access::accesscontrol::default_admin_rules::AccessControlDefaultAdminRulesComponent;
use openzeppelin_upgrades::UpgradeableComponent;
use openzeppelin_utils::execution::{execute_single_call, execute_calls, assert_valid_signature};
```

### Initializable — One-Shot Constructor

For contracts where initialization must happen post-deploy (upgradeable patterns):

```cairo
use openzeppelin_security::InitializableComponent;

component!(path: InitializableComponent, storage: initializable, event: InitializableEvent);
impl InternalImpl = InitializableComponent::InternalImpl<ContractState>;

fn initializer(ref self: ContractState, owner: ContractAddress) {
    self.initializable.initialize(); // Panics on second call
    self.ownable.initializer(owner);
}
```

**Rule:** Only use `initialize()` in ONE function. If multiple init steps are needed, put them all in one initializer.

### Pausable — Emergency Stop

```cairo
use openzeppelin_security::PausableComponent;
use openzeppelin_access::ownable::OwnableComponent;

// Embed both components
#[abi(embed_v0)]
impl PausableImpl = PausableComponent::PausableImpl<ContractState>;
impl PausableInternalImpl = PausableComponent::InternalImpl<ContractState>;

#[external(v0)]
fn pause(ref self: ContractState) {
    self.ownable.assert_only_owner();
    self.pausable.pause();   // Emits Paused(account)
}

#[external(v0)]
fn unpause(ref self: ContractState) {
    self.ownable.assert_only_owner();
    self.pausable.unpause(); // Emits Unpaused(account)
}

// In protected functions:
fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) {
    self.pausable.assert_not_paused(); // Blocks when paused
    // ... transfer logic
}
```

### ReentrancyGuard — Cross-Function Protection

Unlike Solidity modifiers, Cairo uses explicit `start()`/`end()` calls:

```cairo
use openzeppelin_security::ReentrancyGuardComponent;

component!(path: ReentrancyGuardComponent, storage: reentrancy_guard, event: ReentrancyGuardEvent);
impl InternalImpl = ReentrancyGuardComponent::InternalImpl<ContractState>;

#[external(v0)]
fn withdraw(ref self: ContractState, amount: u256) {
    self.reentrancy_guard.start();  // Panics if already entered

    let caller = get_caller_address();
    let balance = self.balances.read(caller);
    assert(balance >= amount, 'Insufficient');
    self.balances.write(caller, balance - amount);
    IERC20Dispatcher { contract_address: self.token.read() }.transfer(caller, amount);

    self.reentrancy_guard.end();    // Reset guard
}
```

**Rule:** `start()` must be the first statement, `end()` must be before `return`. The guard protects across ALL functions that use it — if `withdraw` is entered, `swap` (also guarded) cannot be called by the same tx.

### Pausable — Critical Note on Liquidations

Do NOT apply `assert_not_paused()` to liquidation or risk-management functions (see Section 11 "Pause Mechanism — Don't Pause Liquidations"). Emergency pause must still allow insolvent positions to be closed.

### OZ Governance Components

OZ Cairo 3.x includes a full governance suite. Key security patterns:

- **`GovernorComponent`** — on-chain voting with timelock executor. The executor address must be carefully controlled (set to the Timelock, not an EOA).
- **`TimelockControllerComponent`** — enforces delay between proposal and execution. PROPOSER / CANCELLER / EXECUTOR roles must be granted carefully. Set a meaningful minimum delay (gives users time to exit before governance changes take effect).
- **`MultisigComponent`** — multi-signature operations. Quorum must be set carefully (too low = insecure, too high = governance deadlock). OZ fixed a quorum-related bug in v0.18.0.
- **`VotesComponent`** — ERC20/ERC721 token voting with delegation and checkpoints.

**Governance security rules:**
1. `DEFAULT_ADMIN_ROLE` should be **renounced** after initial role setup (otherwise the admin can bypass governance).
2. Timelock minimum delay should be non-trivial (24-48h minimum) to give users time to react.
3. Governor executor must be the Timelock contract, NOT an arbitrary address.
4. For upgradeable contracts, the upgrade function should be behind the Timelock, not a single owner.
5. `GovernorComponent` proposal state at snapshot timepoint changed from Active to **Pending** in v3.0.0 — verify your governance UIs match this.
6. `VotesComponent` now supports customizable clock mechanisms via `ERC6372Clock` — ensure your voting token implements the correct clock source.

### AccessControlDefaultAdminRulesComponent (OZ v3.0.0)

*Source: [OZ v3.0.0 Release](https://github.com/OpenZeppelin/cairo-contracts/releases/tag/v3.0.0)*

New in v3.0.0. Enforces a **transfer delay** on `DEFAULT_ADMIN_ROLE`, preventing instant admin transfers that could be exploited in governance attacks. This is the recommended way to handle admin roles in production.

```cairo
use openzeppelin_access::accesscontrol::default_admin_rules::AccessControlDefaultAdminRulesComponent;

// Key features:
// - Admin transfer requires a two-step process with a configurable delay
// - MAXIMUM_DEFAULT_ADMIN_TRANSFER_DELAY exposed in ImmutableConfig
// - Prevents social engineering attacks where admin is transferred in a single tx
```

**Rule:** For any contract with `AccessControlComponent`, prefer `AccessControlDefaultAdminRulesComponent` for the admin role to enforce transfer delays.

### MetaTransactionV0 Preset (OZ v3.0.0)

New in v3.0.0. Provides a meta-transaction preset with built-in replay protection. Relevant for relayer architectures and paymaster integrations. Uses SNIP-12 for signature validation. If you're building a meta-transaction relay, use this instead of rolling your own.

---

## 18. DeFi Protocol Security Patterns

*Source: [Code4rena Starknet Perpetual (2025)](https://code4rena.com/reports/2025-03-starknet-perpetual)*

These patterns are specific to DeFi protocols (DEXes, lending, perpetuals, vaults) and emerge from the largest Cairo-specific competitive audit to date.

### Global Validation DoS (C4 L-06, L-08)

**Pattern:** A global validation function that checks ALL state (all asset prices, all funding rates) blocks operations that only involve a subset of state. If one unrelated asset has stale data, ALL operations fail — including unrelated withdrawals.

```cairo
// BAD — global validation blocks unrelated operations
fn reduce_position(ref self: ContractState, asset_id: felt252) {
    self._validate_all_assets_integrity(); // Checks ALL assets, fails if ANY is stale
    // User can't reduce their position because an unrelated asset has stale data
}

// GOOD — scope validation to affected assets only
fn reduce_position(ref self: ContractState, asset_id: felt252) {
    self._validate_asset_integrity(asset_id); // Only checks the relevant asset
    // User can proceed even if unrelated assets are stale
}
```

**Also from L-08:** Users with zero synthetic exposure were blocked from withdrawing collateral because validation ran unconditionally. **Rule:** Scope validation to the user's actual exposure — don't gate collateral-only operations on synthetic asset health.

### Stale Prices for Inactive Assets (C4 L-07)

When deactivating assets, ensure settlement/wind-down functions either: (a) allow governance to update inactive prices, or (b) validate price freshness explicitly. In the C4 finding, inactive assets couldn't have prices updated (the setter rejected them), but their last price was still used for settlement calculations with no freshness check.

### Liquidation Must Not Flip Position Direction (C4 M-02)

A liquidator can purchase more synthetic than the liquidated user holds, forcing them from long to short (or vice versa) without consent. **Rule:** Cap liquidation amounts at the existing synthetic balance. Use the same `_validate_imposed_reduction_trade()` pattern as deleverage to prevent direction flips.

### Per-Asset Parameterization (C4 L-01, L-02)

Using a single global `max_price_interval` or `max_funding_rate` for all synthetic assets is a design anti-pattern. Different asset classes have different volatility profiles. BTC and a long-tail memecoin should not share the same staleness threshold.

**Rule:** All risk parameters (price staleness windows, funding rate caps, collateral factors, liquidation thresholds) must be configurable per asset.

---

## 19. Security Tooling

*Source: [Caracal](https://github.com/crytic/caracal), [FuzzingLabs](https://github.com/FuzzingLabs), [Cairo Book ch104-03](https://book.cairo-lang.org/ch104-03-static-analysis-tools.html)*

### Primary Tool: snforge Fuzz Testing (Starknet Foundry)

**This is the only actively maintained, Cairo-2.12+-compatible security testing tool.** Use `snforge test` with fuzz testing as your primary automated security tool.

```bash
# Run all tests with fuzzing (default 256 runs)
snforge test

# Increase fuzz iterations for security-sensitive functions
snforge test --fuzzer-runs 1000

# Run specific test
snforge test test_deposit_withdraw_invariant
```

Write property-based fuzz tests for all arithmetic and state-transition logic:

```cairo
#[test]
#[fuzzer(runs: 500, seed: 42)]
fn fuzz_transfer_preserves_total_supply(amount: u128) {
    // Setup
    let initial_supply = token.total_supply();
    // Act
    token.transfer(recipient, amount.into());
    // Assert: total supply never changes
    assert(token.total_supply() == initial_supply, 'SUPPLY_CHANGED');
}
```

### Caracal — Static Analyzer (Trail of Bits / Crytic)

> **WARNING: Caracal v0.2.3 (released Jan 2024) only supports Cairo up to 2.5.0 and is effectively unusable for any project on Cairo 2.7+, which includes essentially every Starknet project since mid-2024.** Check the [releases page](https://github.com/crytic/caracal/releases) for updates. Until a new release ships, use `snforge` fuzz testing as your primary automated security tool.

If you are on Cairo ≤ 2.5.0 (legacy projects):

```bash
cargo install caracal
cd my_project && caracal .
caracal . --detectors reentrancy,unchecked_return
```

### FuzzingLabs Tools (Archived / No Longer Maintained)

> **WARNING:** All three FuzzingLabs tools — `cairo-fuzzer`, `sierra-analyzer`, and `Thoth` — are explicitly marked **"This repository is no longer maintained"** by FuzzingLabs. Additionally, `cairo-fuzzer` does not support Cairo 2.0+ contracts. **Do not rely on any of these for current projects.**

These tools made important contributions to the Cairo security ecosystem and their research remains valuable for understanding vulnerability classes, but they should not be part of your active toolchain:

- **sierra-analyzer** — Sierra decompiler with felt252 overflow detectors. [Archived](https://github.com/FuzzingLabs/sierra-analyzer)
- **cairo-fuzzer** — Smart contract fuzzer (Cairo 0.x only). [Archived](https://github.com/FuzzingLabs/cairo-fuzzer)
- **Thoth** — Bytecode disassembler, decompiler, symbolic execution. [Archived](https://github.com/FuzzingLabs/thoth)

### Recommended CI Pipeline

```yaml
# In .github/workflows/security.yml
- name: Build
  run: scarb build
- name: Test (with fuzzing)
  run: snforge test --fuzzer-runs 500
# Note: no static analyzer is currently compatible with Cairo 2.12+
# Monitor Caracal releases for updates
```

---

## 20. Upgrade Safety

### Before Upgrading

1. New class hash should be declared and verified on explorer
2. Test upgrade on Sepolia first
3. Verify storage layout compatibility
4. Have a rollback plan (old class hash declared, ready to re-upgrade)

### Storage Layout Rules

- Never remove or reorder existing storage fields
- Only append new fields at the end
- Component substorage names must stay the same
- Map key types must not change

---

## 21. Audit Preparation

### What Auditors Look For

1. **Access control completeness** — every external `ref self` function has authorization
2. **Input validation** — all user inputs checked before use
3. **State consistency** — no paths where state becomes inconsistent
4. **Economic invariants** — total supply == sum of balances, etc.
5. **Upgrade governance** — who can upgrade, timelocks
6. **Event completeness** — all state changes emit events
7. **Error messages** — all asserts have descriptive messages
8. **L1/L2 message safety** — from_address validated, replay protected
9. **Unbounded iteration** — no user-growable loops
10. **Boolean return checks** — ERC20 transfer/approve returns checked

### Documentation for Auditors

Provide:
- Architecture diagram (contracts + interactions)
- Invariants the system should maintain
- Known trust assumptions
- Admin capabilities and their risks
- Expected call flows for each user type
- L1/L2 message flow diagrams (if applicable)

---

## 22. Production Operations

### Monitoring

- Watch for unexpected `upgrade` calls
- Monitor admin role grants/revocations
- Track session key creation and revocation patterns
- Alert on large transfers or unusual call patterns
- Monitor L1/L2 message consumption (stuck messages)

### Incident Response

1. **Kill switch** — ability to pause the contract
2. **Session revocation** — revoke all active sessions immediately
3. **Upgrade path** — deploy fix, declare, upgrade
4. **Communication** — notify users via events and off-chain channels

---

## Sources

### Official Documentation
- [Cairo Book — General Recommendations (ch104)](https://book.cairo-lang.org/ch104-01-general-recommendations.html)
- [Cairo Book — Static Analysis Tools (ch104-03)](https://book.cairo-lang.org/ch104-03-static-analysis-tools.html)
- [OpenZeppelin Cairo Security Docs (3.0)](https://docs.openzeppelin.com/contracts-cairo/3.0.0-alpha.1/security)
- [OpenZeppelin Cairo Contracts Advisories](https://advisories.gitlab.com/pkg/pypi/openzeppelin-cairo-contracts)

### Audit Reports
- [Code4rena — Starknet Perpetual (2025), 2H/3M/14L](https://code4rena.com/reports/2025-03-starknet-perpetual)
- [Code4rena — Opus (Jan 2024), 4H/9M — first major Cairo DeFi audit](https://code4rena.com/reports/2024-01-opus)
- [ChainSecurity — Starknet Perpetual (2025)](https://www.chainsecurity.com/security-audit/starkware-starknet-perpetual)
- [ChainSecurity — MakerDAO StarkNet-DAI-Bridge (2021), 1 Critical](https://chainsecurity.com/wp-content/uploads/2021/12/ChainSecurity_MakerDAO_StarkNet-DAI-Bridge_audit.pdf)
- [ConsenSys Diligence — Argent Account V3 (Jan 2024)](https://diligence.consensys.io/audits/2024/01/argent-account-argent-multisig-starknet-transaction-v3-updates/)
- [Nethermind — 25+ Cairo/Starknet Audit Reports](https://github.com/NethermindEth/PublicAuditReports)
- [chipi-pay — Session Key Contract + SNIP Draft + 4 Nethermind AuditAgent scans](https://github.com/chipi-pay/sessions-smart-contract)
- [Code4rena — LayerZero Starknet Endpoint (Oct 2025), 0H/0M/6L](https://code4rena.com/reports/2025-10-layerzero-starknet-endpoint)
- [Cairo Security Clan — 30+ Cairo Audit Reports (Ekubo, Vesu, Opus, Paradex, etc.)](https://github.com/Cairo-Security-Clan/Audit-Portfolio)
- [ChainSecurity — Vesu Protocol Smart Contracts](https://www.chainsecurity.com/security-audit/vesu-protocol-smart-contracts)

### Exploit Post-Mortems
- [BlockSec — zkLend $10M Exploit Post-Mortem (Feb 2025)](https://blocksec.com/blog/zklend-exploit-post-mortem)
- [SolidityScan — zkLend Hack Analysis](https://blog.solidityscan.com/zklend-hack-analysis)
- [FuzzingLabs — Rediscovery of the zkLend Hack](https://fuzzinglabs.com/rediscovery-zklend-hack/)

### Vulnerability Research
- [Crytic — Not So Smart Contracts (Cairo)](https://github.com/crytic/building-secure-contracts/tree/master/not-so-smart-contracts/cairo)
- [0xEniotna — Starknet Contract Vulnerabilities](https://github.com/0xEniotna/Starknet-contracts-vulnerabilities)
- [Oxor.io — Cairo Security Flaws (Aug 2024)](https://oxor.io/blog/2024-08-16-cairo-security-flaws/)
- [Oxor.io — Overflow and Underflow Vulnerabilities in Cairo](https://oxor.io/blog/2024-08-16-overflow-and-underflow-vulnerabilities-in-cairo/)
- [FuzzingLabs — Top 4 Vulnerabilities in Cairo/Starknet (Nov 2024)](https://fuzzinglabs.com/top-4-vulnerability-cairo-starknet-smart-contract/)
- [amanusk — Awesome Starknet Security](https://github.com/amanusk/awesome-starknet-security)

### Standards & Specifications
- [SNIP-9 — Outside Execution (meta-transactions)](https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-9.md)
- [SNIP-12 — Typed Structured Data Signing](https://github.com/starknet-io/SNIPs/blob/main/SNIPS/snip-12.md)
- [OZ SNIP-12 Guide](https://docs.openzeppelin.com/contracts-cairo/3.x/guides/snip12)

### OpenZeppelin Components
- [OZ Cairo Governance Docs (3.x)](https://docs.openzeppelin.com/contracts-cairo/3.x/api/governance)
- [OZ Cairo ERC20Permit](https://docs.openzeppelin.com/contracts-cairo/3.x/api/erc20#ERC20Permit)
- [OZ Cairo NoncesComponent](https://docs.openzeppelin.com/contracts-cairo/3.x/api/utilities#NoncesComponent)

### Account Abstraction & Paymasters
- [Starknet Docs — Account Abstraction](https://docs.starknet.io/build/starknet-by-example/advanced/account-abstraction)
- [Starknet Docs — Paymaster](https://docs.starknet.io/build/applications/paymaster)

### Protocol Security Disclosures
- [Zellic — Sequencer-Prover Inconsistency in Cairo VM (Starknet Community Forum)](https://community.starknet.io/t/remediating-a-potential-sequencer-prover-inconsistency-in-the-cairo-vm/115313)

### Formal Verification
- [StarkWare — Cairo VM Formal Proofs (Lean)](https://github.com/starkware-libs/formal-proofs) — formal verification of Cairo VM semantics, AIR encoding correctness, and elliptic curve operations (secp256k1/r1)

### Protocol Changes
- [Starknet Version Notes (official, all versions)](https://docs.starknet.io/learn/cheatsheets/version-notes)
- [Starknet v0.14.0 "Grinta" — Decentralized Sequencer](https://starknet.io/blog/starknet-grinta-the-architecture-of-a-more-decentralized-future)
- [Starknet Version Releases](https://www.starknet.io/developers/version-releases/)
- [Starknet Fees Documentation](https://docs.starknet.io/learn/protocol/fees)
- [Starknet Compatibility Tables](https://docs.starknet.io/learn/cheatsheets/compatibility)
- [Cairo v2.15.0 Release (edition 2025_12)](https://github.com/starkware-libs/cairo/releases/tag/v2.15.0)

### Cairo Core Library
- [Cairo Core Integer Module (overflow/wrapping/saturating)](https://docs.cairo-lang.org/core/core-integer.html)
- [Cairo SaturatingAdd Trait](https://docs.cairo-lang.org/core/core-num-traits-ops-saturating-SaturatingAdd.html)

### Security Tooling
- [snforge — Starknet Foundry Testing & Fuzzing (primary tool)](https://foundry-rs.github.io/starknet-foundry/)
- [Caracal — Static Analyzer (Cairo ≤ 2.5.0 only, last release Jan 2024)](https://github.com/crytic/caracal)
- [FuzzingLabs — sierra-analyzer (ARCHIVED, no longer maintained)](https://github.com/FuzzingLabs/sierra-analyzer)
- [FuzzingLabs — cairo-fuzzer (ARCHIVED, no longer maintained, Cairo 0.x only)](https://github.com/FuzzingLabs/cairo-fuzzer)
- [FuzzingLabs — Thoth (ARCHIVED, no longer maintained)](https://github.com/FuzzingLabs/thoth)
- [sqrlfirst — Cairo Security Checklist](https://github.com/sqrlfirst/cairo-checklist)
