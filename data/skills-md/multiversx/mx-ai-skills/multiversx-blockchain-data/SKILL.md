---
name: multiversx-blockchain-data
description: Read on-chain state in MultiversX smart contracts. Use when accessing caller info, account balances, block timestamps, ESDT token metadata, local roles, code metadata, or any data from self.blockchain().
---

# MultiversX Blockchain Data — `self.blockchain()` API Reference

Complete reference for reading on-chain state in MultiversX smart contracts (SDK v0.64+).

## Caller & Account Info

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_caller()` | `ManagedAddress` | Address that initiated the current call |
| `.get_sc_address()` | `ManagedAddress` | This contract's own address |
| `.get_owner_address()` | `ManagedAddress` | Contract owner address |
| `.check_caller_is_owner()` | `()` | Panics if caller != owner. Equivalent to `#[only_owner]`. |
| `.check_caller_is_user_account()` | `()` | Panics if caller is a smart contract (not an EOA). |
| `.is_smart_contract(address)` | `bool` | Check if an address is a smart contract |
| `.get_shard_of_address(address)` | `u32` | Get shard ID for an address |

```rust
// Owner-only guard (manual alternative to #[only_owner])
self.blockchain().check_caller_is_owner();

// Prevent contract-to-contract calls (anti-flash-loan)
self.blockchain().check_caller_is_user_account();

// Check if target is a SC before sending
let is_sc = self.blockchain().is_smart_contract(&target);
```

## Balances

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_balance(address)` | `BigUint` | EGLD balance of any address |
| `.get_sc_balance(token_id, nonce)` | `BigUint` | This contract's balance of any token (EGLD or ESDT). `token_id` is `impl AsRef<TokenId>`. |
| `.get_esdt_balance(address, token_id, nonce)` | `BigUint` | ESDT balance of any address. `token_id` is `&EsdtTokenIdentifier`. |

```rust
// Check own EGLD balance
let egld = self.blockchain().get_balance(&self.blockchain().get_sc_address());

// Check own ESDT balance (simpler via get_sc_balance)
let balance = self.blockchain().get_sc_balance(&my_token_id, 0u64);
```

## Block Info

### Current Block

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_block_timestamp_seconds()` | `TimestampSeconds` | Block timestamp in seconds (v0.63+) |
| `.get_block_timestamp_millis()` | `TimestampMillis` | Block timestamp in milliseconds (v0.63+) |
| `.get_block_nonce()` | `u64` | Block nonce (height) |
| `.get_block_round()` | `u64` | Block round |
| `.get_block_epoch()` | `u64` | Current epoch |
| `.get_block_round_time_millis()` | `DurationMillis` | Round duration in ms (v0.63+) |
| `.get_block_random_seed()` | `ManagedByteArray<48>` | 48-byte random seed |

### Previous Block

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_prev_block_timestamp_seconds()` | `TimestampSeconds` | Previous block timestamp (seconds) |
| `.get_prev_block_timestamp_millis()` | `TimestampMillis` | Previous block timestamp (ms) |
| `.get_prev_block_nonce()` | `u64` | Previous block nonce |
| `.get_prev_block_round()` | `u64` | Previous block round |
| `.get_prev_block_epoch()` | `u64` | Previous epoch |
| `.get_prev_block_random_seed()` | `ManagedByteArray<48>` | Previous block random seed |

### Epoch Start Info

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_epoch_start_block_timestamp_millis()` | `TimestampMillis` | When current epoch started |
| `.get_epoch_start_block_nonce()` | `u64` | Block nonce at epoch start |
| `.get_epoch_start_block_round()` | `u64` | Block round at epoch start |

### Deprecated Timestamp Methods (Do NOT Use)

| Deprecated | Replacement | Since |
|-----------|-------------|-------|
| `.get_block_timestamp()` | `.get_block_timestamp_seconds()` | v0.63 |
| `.get_block_timestamp_ms()` | `.get_block_timestamp_millis()` | v0.63 |
| `.get_prev_block_timestamp()` | `.get_prev_block_timestamp_seconds()` | v0.63 |
| `.get_prev_block_timestamp_ms()` | `.get_prev_block_timestamp_millis()` | v0.63 |
| `.get_block_round_time_ms()` | `.get_block_round_time_millis()` | v0.63 |
| `.epoch_start_block_timestamp_ms()` | `.get_epoch_start_block_timestamp_millis()` | v0.63 |
| `.epoch_start_block_timestamp_millis()` | `.get_epoch_start_block_timestamp_millis()` | v0.63.1 |
| `.epoch_start_block_nonce()` | `.get_epoch_start_block_nonce()` | v0.63.1 |
| `.epoch_start_block_round()` | `.get_epoch_start_block_round()` | v0.63.1 |

## Transaction Info

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_tx_hash()` | `ManagedByteArray<32>` | Current transaction hash |
| `.get_gas_left()` | `u64` | Remaining gas |
| `.get_state_root_hash()` | `ManagedByteArray<32>` | State root hash |

## ESDT Token Metadata

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_esdt_token_data(address, token_id, nonce)` | `EsdtTokenData` | Full token data (amount, attributes, creator, royalties, URIs, etc.) |
| `.get_esdt_token_type(address, token_id, nonce)` | `EsdtTokenType` | Token type enum (Fungible, NonFungible, SemiFungible, Meta) |
| `.get_token_attributes::<T>(token_id, nonce)` | `T: TopDecode` | Deserialized NFT/SFT attributes from this contract's account |
| `.get_current_esdt_nft_nonce(address, token_id)` | `u64` | Last minted nonce for a token on an address |

```rust
// EsdtTokenData fields:
pub struct EsdtTokenData<M: ManagedTypeApi> {
    pub token_type: EsdtTokenType,
    pub amount: BigUint<M>,
    pub frozen: bool,
    pub hash: ManagedBuffer<M>,
    pub name: ManagedBuffer<M>,
    pub attributes: ManagedBuffer<M>,  // raw bytes — use get_token_attributes for typed
    pub creator: ManagedAddress<M>,
    pub royalties: BigUint<M>,         // 0-10000 (basis points)
    pub uris: ManagedVec<M, ManagedBuffer<M>>,
}
```

```rust
// Read NFT attributes as a typed struct
#[derive(TopDecode)]
struct MyNftAttributes {
    level: u8,
    power: u64,
}

let attrs: MyNftAttributes = self.blockchain()
    .get_token_attributes::<MyNftAttributes>(&nft_token_id, nft_nonce);
```

## ESDT Status & Roles

| Method | Returns | Description |
|--------|---------|-------------|
| `.is_esdt_frozen(address, token_id, nonce)` | `bool` | Whether token is frozen for this address |
| `.is_esdt_paused(token_id)` | `bool` | Whether token transfers are globally paused |
| `.is_esdt_limited_transfer(token_id)` | `bool` | Whether token has limited transfer enabled |
| `.get_esdt_local_roles(token_id)` | `EsdtLocalRoleFlags` | Bitmask of roles this contract has for the token |

```rust
// Check roles before minting
let roles = self.blockchain().get_esdt_local_roles(&token_id);
require!(
    roles.has_role(&EsdtLocalRole::NftCreate),
    "Contract lacks NftCreate role"
);
```

## Code Inspection

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_code_metadata(address)` | `CodeMetadata` | Contract code metadata (upgradeable, readable, payable flags) |
| `.get_code_hash(address)` | `ManagedBuffer` | Hash of contract WASM code |
| `.is_builtin_function(name)` | `bool` | Whether a function name is a protocol built-in |

## Native Token

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_native_token()` | `ManagedRef<TokenId>` | Returns `EGLD-000000` as a `TokenId` |
| `.is_native_token(token_id)` | `bool` | Checks if a `TokenId` is `EGLD-000000` |

## Validators

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_cumulated_validator_rewards()` | `BigUint` | Validator rewards accrued to this contract |

## Back-Transfers (After Cross-Contract Calls)

| Method | Returns | Description |
|--------|---------|-------------|
| `.get_back_transfers()` | `BackTransfers` | All tokens returned from a sync/async call |
| `.reset_back_transfers()` | `()` | Clears current back-transfers (prevents double-reading) |

See the `multiversx-cross-contract-calls` skill for full back-transfer patterns.

## Common Patterns

### Time-Based Logic
```rust
let now = self.blockchain().get_block_timestamp_seconds();
let deadline = self.deadline().get();
require!(now < deadline, "Deadline passed");
```

### Shard-Aware Operations
```rust
let caller_shard = self.blockchain().get_shard_of_address(
    &self.blockchain().get_caller()
);
let sc_shard = self.blockchain().get_shard_of_address(
    &self.blockchain().get_sc_address()
);
let same_shard = caller_shard == sc_shard;
// If same shard, can use sync calls; otherwise need async
```

### Token Property Validation
```rust
fn validate_nft(&self, token_id: &EsdtTokenIdentifier, nonce: u64) {
    let sc_addr = self.blockchain().get_sc_address();
    let data = self.blockchain().get_esdt_token_data(&sc_addr, token_id, nonce);
    require!(data.amount > 0u64, "NFT not owned");
    require!(!data.frozen, "Token is frozen");
}
```

### Balance Check Before Transfer
```rust
let sc_balance = self.blockchain().get_sc_balance(&token_id, 0u64);
require!(sc_balance >= amount, "Insufficient contract balance");
self.tx().to(&recipient).esdt((token_id, 0u64, amount)).transfer();
```

## Anti-Patterns

```rust
// BAD: Using deprecated get_block_timestamp() — returns raw u64
let ts = self.blockchain().get_block_timestamp();

// GOOD: Use typed timestamp (v0.63+)
let ts = self.blockchain().get_block_timestamp_seconds();

// BAD: Storing raw u64 timestamps, mixing seconds/millis
self.last_action().set(self.blockchain().get_block_timestamp_millis().as_u64_millis());

// GOOD: Store typed timestamps
self.last_action().set(self.blockchain().get_block_timestamp_seconds());

// BAD: get_balance to check own EGLD — requires passing own address
let bal = self.blockchain().get_balance(&self.blockchain().get_sc_address());

// GOOD: Use get_sc_balance which handles EGLD via native token detection
let bal = self.blockchain().get_sc_balance(&self.blockchain().get_native_token(), 0u64);
```
