---
name: aptos-agent
description: Interact with Aptos blockchain - check balances, transfer APT, swap tokens, stake, and execute Move view functions. Features game-theoretic decision analysis with Nash equilibrium detection. All transactions require explicit approval.
version: 1.0.0
---


# Aptos Claude Agent

Aptos blockchain interaction with game-theoretic decision analysis.

## When to Use

- Check APT wallet balances
- Transfer APT tokens
- Swap tokens on DEX (Liquidswap, etc.)
- Stake APT
- Call Move view functions
- Process natural language blockchain intents
- Query NFT/token collections
- Interact with multisig accounts

## Setup

MCP server configured in `~/.mcp.json`:
```json
{
  "aptos": {
    "command": "node",
    "args": ["/path/to/aptos-claude-agent/dist/mcp/server.js"],
    "env": {
      "APTOS_NETWORK": "mainnet",
      "APTOS_PRIVATE_KEY": "${APTOS_PRIVATE_KEY}"
    }
  }
}
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `aptos_balance` | Get wallet balance |
| `aptos_transfer` | Transfer APT (requires approval) |
| `aptos_swap` | Swap tokens on DEX (requires approval) |
| `aptos_stake` | Stake APT (requires approval) |
| `aptos_view` | Read-only view function call |
| `aptos_intent` | Process natural language intent |
| `aptos_approve` | Approve/reject pending decision |
| `aptos_pending` | List pending decisions |

## Security Model

1. **Simulation First**: All transactions simulated before execution
2. **Approval Required**: Every state-changing operation needs explicit approval
3. **Game-Theoretic Analysis**: Transactions modeled as open games
4. **Wallet Validation**: ALWAYS validate key→address before funding

## CRITICAL: Wallet Derivation Safety

**NEVER use `derive-resource-account-address` for wallet creation.**

### Correct Workflow
```bash
# 1. Generate key
aptos key generate --output-file my_key

# 2. Derive address FROM PRIVATE KEY
aptos init --private-key-file my_key --network mainnet --profile my_wallet

# 3. VALIDATE before funding
just aptos-validate "PRIVATE_KEY" "EXPECTED_ADDRESS"

# 4. Only fund AFTER validation passes
```

### What Can Go Wrong
- Using `derive-resource-account-address` with pubkey = **PERMANENT FUND LOSS**
- Resource accounts need signer capabilities from source account
- If key doesn't match address, funds are unrecoverable

### Validation
Run `just aptos-validate-all` to verify all configured wallets before any funding operation.

---

## Aptos Framework Reference (0x1)

### Core Modules

| Module | Purpose |
|--------|---------|
| `0x1::coin` | Legacy fungible token standard |
| `0x1::fungible_asset` | New FA standard (object-based) |
| `0x1::aptos_coin` | Native APT token |
| `0x1::account` | Account creation/management |
| `0x1::object` | Object model foundation |
| `0x1::stake` | Validator staking |
| `0x1::delegation_pool` | Delegated staking |
| `0x1::multisig_account` | Multi-signature accounts |
| `0x1::aptos_governance` | On-chain governance |
| `0x1::code` | Module deployment |

### 0x1::coin Module

**Key Structs:**
- `Coin<CoinType>` - Fungible token container
- `CoinStore<CoinType>` - Account balance storage
- `CoinInfo<CoinType>` - Token metadata
- `MintCapability<CoinType>` - Minting rights
- `BurnCapability<CoinType>` - Burning rights
- `FreezeCapability<CoinType>` - Freeze rights

**View Functions:**
```move
0x1::coin::balance<CoinType>(owner: address): u64
0x1::coin::is_account_registered<CoinType>(account: address): bool
0x1::coin::name<CoinType>(): vector<u8>
0x1::coin::symbol<CoinType>(): vector<u8>
0x1::coin::decimals<CoinType>(): u8
0x1::coin::supply<CoinType>(): Option<u128>
```

**Entry Functions:**
```move
0x1::coin::transfer<CoinType>(from: &signer, to: address, amount: u64)
0x1::coin::register<CoinType>(account: &signer)
```

### 0x1::fungible_asset Module

**Key Structs:**
- `Metadata` - Asset metadata object
- `FungibleStore` - Balance storage
- `FungibleAsset` - Asset container
- `MintRef`, `BurnRef`, `TransferRef` - Capabilities

**View Functions:**
```move
0x1::fungible_asset::balance<T>(store: Object<T>): u64
0x1::primary_fungible_store::balance(account: address, metadata: Object<Metadata>): u64
```

### 0x1::stake Module

**Key Structs:**
- `StakePool` - Validator stake pool
- `ValidatorConfig` - Validator configuration
- `OwnerCapability` - Pool ownership

**View Functions:**
```move
0x1::stake::get_validator_state(pool_address: address): u64
0x1::stake::get_stake(pool_address: address): (u64, u64, u64, u64)
```

### 0x1::delegation_pool Module

**View Functions:**
```move
0x1::delegation_pool::get_stake(pool_address: address, delegator: address): (u64, u64, u64)
0x1::delegation_pool::calculate_and_update_voter_total_voting_power(pool_address: address): u64
```

### 0x1::multisig_account Module

**Key Functions:**
```move
0x1::multisig_account::create(owner: &signer, num_signatures_required: u64, owners: vector<address>)
0x1::multisig_account::create_transaction(multisig: address, payload: vector<u8>)
0x1::multisig_account::approve_transaction(owner: &signer, multisig: address, sequence_number: u64)
0x1::multisig_account::execute_transaction(multisig: address, sequence_number: u64)
```

---

## Token Standards Reference

### Legacy Token (0x3::token)

**Key Structs:**
- `Token` - Token instance with id, amount, properties
- `TokenId` - Global unique identifier (creator + collection + name + version)
- `TokenData` - Shared metadata (max supply, uri, royalty)
- `TokenStore` - Account's token holdings
- `CollectionData` - Collection metadata
- `Royalty` - Royalty configuration

**Entry Functions:**
```move
0x3::token::create_collection_script(creator: &signer, name: String, description: String, uri: String, maximum: u64)
0x3::token::create_token_script(creator: &signer, collection: String, name: String, description: String, ...)
0x3::token::mint_script(creator: &signer, token_data_address: address, collection: String, name: String, amount: u64)
0x3::token::direct_transfer_script(sender: &signer, receiver: &signer, creators_address: address, ...)
```

**View Functions:**
```move
0x3::token::balance_of(owner: address, id: TokenId): u64
0x3::token::get_royalty(token_data_id: TokenDataId): Royalty
0x3::token::get_token_supply(creator: address, collection: String, name: String): Option<u64>
```

### Digital Asset (0x4::token + 0x4::aptos_token)

**Key Structs (0x4::token):**
- `Token` - Object-based token with collection, index, description, name
- `BurnRef` - Burning capability
- `MutatorRef` - Mutation capability

**Key Structs (0x4::aptos_token):**
- `AptosCollection` - No-code collection with mutability settings
- `AptosToken` - Minimally viable token

**Entry Functions:**
```move
0x4::aptos_token::create_collection(creator: &signer, description: String, name: String, uri: String, ...)
0x4::aptos_token::mint(creator: &signer, collection: String, description: String, name: String, uri: String, ...)
0x4::aptos_token::mint_token_object(creator: &signer, collection: String, ...) -> Object<AptosToken>
0x4::aptos_token::burn(owner: &signer, token: Object<AptosToken>)
0x4::aptos_token::freeze_transfer(creator: &signer, token: Object<AptosToken>)
0x4::aptos_token::set_description(creator: &signer, token: Object<AptosToken>, description: String)
```

**View Functions:**
```move
0x4::token::creator(token: Object<Token>): address
0x4::token::collection_name(token: Object<Token>): String
0x4::aptos_token::are_properties_mutable(token: Object<AptosToken>): bool
0x4::aptos_token::is_burnable(token: Object<AptosToken>): bool
```

### Supporting Modules

**0x4::collection:**
```move
0x4::collection::count(collection: Object<Collection>): Option<u64>
0x4::collection::creator(collection: Object<Collection>): address
0x4::collection::name(collection: Object<Collection>): String
```

**0x4::royalty:**
```move
0x4::royalty::get(token: Object<Token>): Option<Royalty>
0x4::royalty::payee_address(royalty: &Royalty): address
0x4::royalty::numerator(royalty: &Royalty): u64
0x4::royalty::denominator(royalty: &Royalty): u64
```

**0x4::property_map:**
```move
0x4::property_map::read_string(object: &Object<T>, key: &String): String
0x4::property_map::read_u64(object: &Object<T>, key: &String): u64
0x4::property_map::read_bool(object: &Object<T>, key: &String): bool
```

---

## Common View Function Patterns

### Check APT Balance
```
aptos_view(
  functionId: "0x1::coin::balance",
  typeArgs: ["0x1::aptos_coin::AptosCoin"],
  args: ["0xADDRESS"]
)
```

### Check Token Balance (Legacy)
```
aptos_view(
  functionId: "0x3::token::balance_of",
  typeArgs: [],
  args: ["0xOWNER", { token_data_id: {...}, property_version: 0 }]
)
```

### Check Stake
```
aptos_view(
  functionId: "0x1::stake::get_stake",
  typeArgs: [],
  args: ["0xVALIDATOR_POOL"]
)
```

### Check Delegation
```
aptos_view(
  functionId: "0x1::delegation_pool::get_stake",
  typeArgs: [],
  args: ["0xPOOL", "0xDELEGATOR"]
)
```

---

## Game-Theoretic Features

### Nashator Analysis
Computes deviation incentives for transactions:
- **LAX monoidal** (`fire`): Actual execution
- **STRONG monoidal** (`exec`): Simulation only

### Bisimulation Self-Play
Explores alternatives via attacker/defender games. Equilibrium detected when `|utility - quality| < 0.15`.

### Risk Visualization
Decisions map to colors via deterministic LCG:
- **HOT ZONE [160-220]**: High-risk indices

---

## DeFi Protocols on Aptos

| Protocol | Category | Key Functions |
|----------|----------|---------------|
| **Liquidswap** | DEX | Swap, add/remove liquidity |
| **Thala** | DEX + Stablecoin | MOD stablecoin, LP farming |
| **Amnis Finance** | Liquid Staking | stAPT, 7-8% APY |
| **Aries Markets** | Lending | Supply, borrow, liquidate |
| **Cellana** | DEX | ve(3,3) model |
| **Echo Protocol** | BTC Bridge | Cross-chain BTC |

---

## Related Skills

- `aptos-trading` - Alpha executor trading scripts
- `acsets-algebraic-databases` - ACSet schemas for Aptos data
- `asi-integrated` - Unified ASI skill orchestration



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
aptos-agent (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch7: Propagators
- Ch3: Variations on an Arithmetic Theme
- Ch6: Layering
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.