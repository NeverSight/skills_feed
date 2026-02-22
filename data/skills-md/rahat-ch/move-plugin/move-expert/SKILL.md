---
name: move-expert
description: Move language expert for Movement blockchain. Automatically triggered when working with .move files, discussing Move/Movement/Aptos concepts, debugging Move compiler errors, or building smart contracts.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, mcp__move__scaffold_module, mcp__move__run_cli, mcp__move__search_framework, mcp__move__query_rpc, mcp__move__setup_cli
---

# Move Expert for Movement Blockchain

You are an expert Move developer specializing in Movement blockchain development. You help users write, debug, and deploy Move smart contracts.

## Critical: Move Version Compatibility

**Movement supports Move 2.1 ONLY.** Do NOT use or suggest:
- `&mut Resource[addr]` syntax (Move 2.2+)
- `#[randomness]` attribute (Move 2.2+)
- Any Move 2.2/2.3 features

Use these Move 2.1 patterns instead:
- `borrow_global_mut<Resource>(addr)` for mutable borrows
- External randomness via oracle or VRF

## Movement Network Endpoints

**Mainnet (Chain ID: 126)**
- RPC: `https://mainnet.movementnetwork.xyz/v1`
- Explorer: `https://explorer.movementnetwork.xyz/?network=mainnet`

**Bardock Testnet (Chain ID: 250)**
- RPC: `https://testnet.movementnetwork.xyz/v1`
- Faucet: `https://faucet.movementnetwork.xyz/`
- Explorer: `https://explorer.movementnetwork.xyz/?network=bardock+testnet`

---

## Core Move Concepts

### Module Structure
```move
module my_addr::my_module {
    use std::signer;
    use aptos_framework::object;

    // Error codes (const)
    const E_NOT_OWNER: u64 = 1;

    // Resources (structs with abilities)
    struct MyResource has key, store {
        value: u64,
    }

    // Init function (called on publish)
    fun init_module(sender: &signer) {
        // Setup code
    }

    // Entry functions (callable from transactions)
    public entry fun do_something(sender: &signer) {
        // Implementation
    }

    // View functions (read-only, no gas)
    #[view]
    public fun get_value(addr: address): u64 acquires MyResource {
        borrow_global<MyResource>(addr).value
    }
}
```

### Abilities
| Ability | Meaning |
|---------|---------|
| `key` | Can be stored as top-level resource |
| `store` | Can be stored inside other structs |
| `copy` | Can be copied (duplicated) |
| `drop` | Can be discarded/destroyed |

Common patterns:
- `has key` - Top-level resource
- `has key, store` - Resource that can also be nested
- `has store, drop, copy` - Value type (like Token info)
- `has drop` - Event structs

### Global Storage Operations
```move
// Store resource at signer's address
move_to(signer, resource);

// Check if resource exists
exists<MyResource>(addr);

// Borrow immutable reference
let ref = borrow_global<MyResource>(addr);

// Borrow mutable reference
let ref = borrow_global_mut<MyResource>(addr);

// Remove and return resource
let resource = move_from<MyResource>(addr);
```

### Signer Operations
```move
use std::signer;

// Get address from signer
let addr = signer::address_of(signer);

// Signer is proof of account ownership
// Cannot be forged or transferred
```

---

## Object Model (Aptos Objects)

Objects are the modern way to create composable, transferable resources.

### Creating Objects
```move
use aptos_framework::object::{Self, Object, ConstructorRef};

// Create a named object (deterministic address)
let constructor_ref = object::create_named_object(
    creator,
    b"my_seed"
);

// Create a random object (unique address)
let constructor_ref = object::create_object(creator_addr);

// Create sticky object (non-deletable, at module address)
let constructor_ref = object::create_sticky_object(@my_addr);

// Get the object signer to store resources
let obj_signer = object::generate_signer(&constructor_ref);

// Store resource at object address
move_to(&obj_signer, MyData { value: 100 });

// Get object from constructor
let obj: Object<MyData> = object::object_from_constructor_ref(&constructor_ref);
```

### Object References
```move
// Generate refs from constructor (must be done at creation time)
let extend_ref = object::generate_extend_ref(&constructor_ref);
let transfer_ref = object::generate_transfer_ref(&constructor_ref);
let delete_ref = object::generate_delete_ref(&constructor_ref);

// Store refs for later use
struct MyController has key {
    extend_ref: ExtendRef,
    transfer_ref: TransferRef,
}
```

### Working with Objects
```move
// Get object address
let obj_addr = object::object_address(&obj);

// Check ownership
let is_owner = object::is_owner(obj, addr);
let owner = object::owner(obj);

// Transfer object
object::transfer(owner_signer, obj, recipient);

// Calculate deterministic address
let obj_addr = object::create_object_address(&creator, seed);
```

---

## Fungible Assets (FA)

Modern token standard replacing legacy Coin module.

### Creating a Fungible Asset
```move
use aptos_framework::fungible_asset::{Self, MintRef, BurnRef, TransferRef, Metadata};
use aptos_framework::primary_fungible_store;
use aptos_framework::object;

struct FAController has key {
    mint_ref: MintRef,
    burn_ref: BurnRef,
    transfer_ref: TransferRef,
}

fun create_fa(creator: &signer) {
    // Create object to hold FA metadata
    let constructor_ref = object::create_sticky_object(@my_addr);

    // Initialize as fungible asset with primary store
    primary_fungible_store::create_primary_store_enabled_fungible_asset(
        &constructor_ref,
        option::some(1000000000), // max_supply (optional)
        string::utf8(b"My Token"),
        string::utf8(b"MTK"),
        8, // decimals
        string::utf8(b"https://example.com/icon.png"),
        string::utf8(b"https://example.com"),
    );

    // Generate refs for mint/burn/transfer control
    let mint_ref = fungible_asset::generate_mint_ref(&constructor_ref);
    let burn_ref = fungible_asset::generate_burn_ref(&constructor_ref);
    let transfer_ref = fungible_asset::generate_transfer_ref(&constructor_ref);

    // Store refs
    let obj_signer = object::generate_signer(&constructor_ref);
    move_to(&obj_signer, FAController { mint_ref, burn_ref, transfer_ref });
}
```

### Minting Tokens
```move
fun mint(recipient: address, amount: u64) acquires FAController {
    let controller = borrow_global<FAController>(@my_addr);
    let fa = fungible_asset::mint(&controller.mint_ref, amount);
    primary_fungible_store::deposit(recipient, fa);
}
```

### Burning Tokens
```move
fun burn(from: address, amount: u64) acquires FAController {
    let controller = borrow_global<FAController>(@my_addr);
    let fa = primary_fungible_store::withdraw(from_signer, metadata, amount);
    fungible_asset::burn(&controller.burn_ref, fa);
}
```

### Checking Balance
```move
#[view]
public fun balance(owner: address, metadata: Object<Metadata>): u64 {
    primary_fungible_store::balance(owner, metadata)
}
```

### Transferring Tokens
```move
// User-initiated transfer
public entry fun transfer(
    sender: &signer,
    metadata: Object<Metadata>,
    recipient: address,
    amount: u64
) {
    primary_fungible_store::transfer(sender, metadata, recipient, amount);
}

// Admin transfer (using transfer_ref)
fun admin_transfer(
    from: address,
    to: address,
    amount: u64
) acquires FAController {
    let controller = borrow_global<FAController>(@my_addr);
    let from_store = primary_fungible_store::ensure_primary_store_exists(from, metadata);
    let to_store = primary_fungible_store::ensure_primary_store_exists(to, metadata);
    fungible_asset::transfer_with_ref(
        &controller.transfer_ref,
        from_store,
        to_store,
        amount
    );
}
```

---

## Token Objects (NFTs)

Modern NFT standard using objects.

### Creating a Collection
```move
use aptos_token_objects::collection;
use aptos_token_objects::token;

fun create_collection(creator: &signer) {
    collection::create_unlimited_collection(
        creator,
        string::utf8(b"My Collection Description"),
        string::utf8(b"My Collection"),
        option::none(), // royalty
        string::utf8(b"https://example.com/collection"),
    );
}

// Or with fixed supply
fun create_fixed_collection(creator: &signer) {
    collection::create_fixed_collection(
        creator,
        string::utf8(b"Description"),
        1000, // max_supply
        string::utf8(b"Collection Name"),
        option::none(),
        string::utf8(b"https://example.com"),
    );
}
```

### Minting NFTs
```move
fun mint_nft(creator: &signer, recipient: address) {
    let constructor_ref = token::create_named_token(
        creator,
        string::utf8(b"Collection Name"),
        string::utf8(b"Token description"),
        string::utf8(b"Token #1"),
        option::none(), // royalty
        string::utf8(b"https://example.com/token/1"),
    );

    // Transfer to recipient
    let transfer_ref = object::generate_transfer_ref(&constructor_ref);
    let token_obj = object::object_from_constructor_ref(&constructor_ref);
    object::transfer_with_ref(
        object::generate_linear_transfer_ref(&transfer_ref),
        recipient
    );
}
```

### Token with Custom Data
```move
struct MyTokenData has key {
    power: u64,
    rarity: String,
}

fun mint_with_data(creator: &signer) {
    let constructor_ref = token::create(
        creator,
        string::utf8(b"Collection"),
        string::utf8(b"Description"),
        string::utf8(b"Token Name"),
        option::none(),
        string::utf8(b"https://example.com/token"),
    );

    let token_signer = object::generate_signer(&constructor_ref);
    move_to(&token_signer, MyTokenData {
        power: 100,
        rarity: string::utf8(b"Legendary"),
    });
}
```

---

## Events

```move
use aptos_framework::event;

#[event]
struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

fun emit_transfer(from: address, to: address, amount: u64) {
    event::emit(TransferEvent { from, to, amount });
}
```

---

## Common Patterns

### Access Control
```move
const E_NOT_ADMIN: u64 = 1;

struct AdminConfig has key {
    admin: address,
}

fun only_admin(sender: &signer) acquires AdminConfig {
    let config = borrow_global<AdminConfig>(@my_addr);
    assert!(
        signer::address_of(sender) == config.admin,
        E_NOT_ADMIN
    );
}
```

### Pausable
```move
const E_PAUSED: u64 = 2;

struct PauseState has key {
    paused: bool,
}

fun when_not_paused() acquires PauseState {
    let state = borrow_global<PauseState>(@my_addr);
    assert!(!state.paused, E_PAUSED);
}
```

### Counter Pattern
```move
struct Counter has key {
    value: u64,
}

fun increment() acquires Counter {
    let counter = borrow_global_mut<Counter>(@my_addr);
    counter.value = counter.value + 1;
}
```

---

## Move.toml Configuration

```toml
[package]
name = "my_project"
version = "1.0.0"
authors = []

[addresses]
my_addr = "_"

[dependencies.AptosFramework]
git = "https://github.com/movementlabsxyz/aptos-core.git"
rev = "m1"
subdir = "aptos-move/framework/aptos-framework"

[dependencies.AptosStdlib]
git = "https://github.com/movementlabsxyz/aptos-core.git"
rev = "m1"
subdir = "aptos-move/framework/aptos-stdlib"

[dependencies.AptosTokenObjects]
git = "https://github.com/movementlabsxyz/aptos-core.git"
rev = "m1"
subdir = "aptos-move/framework/aptos-token-objects"
```

---

## Common Compiler Errors & Fixes

### Ability Errors
```
Error: "type does not have the 'key' ability"
Fix: Add `has key` to struct definition
```

```
Error: "cannot copy value"
Fix: Add `has copy` or use reference `&`
```

```
Error: "cannot drop value"
Fix: Add `has drop` or explicitly handle the value
```

### Borrow Errors
```
Error: "cannot borrow global mutably"
Fix: Use `borrow_global_mut` and add `acquires` annotation
```

```
Error: "value still borrowed"
Fix: Ensure previous borrow ends before new borrow
```

### Type Errors
```
Error: "expected type X, found Y"
Fix: Check function signatures, ensure types match
```

```
Error: "missing acquires annotation"
Fix: Add `acquires ResourceName` to function signature
```

### Access Errors
```
Error: "function is not public"
Fix: Add `public` or `public entry` to function
```

```
Error: "module not found"
Fix: Check Move.toml dependencies, ensure correct import path
```

---

## CLI Installation

Install the Movement CLI via Homebrew (macOS/Linux):
```bash
brew install movementlabsxyz/tap/movement
movement --version
```

Fallback: Aptos CLI v7.4.0 is supported if Movement CLI is unavailable:
```bash
brew install aptos
aptos --version  # must be exactly 7.4.0
```

Use the `setup_cli` MCP tool to check installation status, get install instructions, or initialize an account.

## CLI Commands

Movement CLI is recommended. Aptos CLI v7.4.0 is supported as a fallback only.

```bash
# Compile
movement move compile

# Test
movement move test

# Publish
movement move publish --named-addresses my_addr=default

# Initialize account
movement init --network testnet

# Check account
movement account list

# Run script
movement move run --function-id 'my_addr::module::function'
```

---

## Best Practices

1. **Use objects over legacy resources** - More flexible, composable
2. **Use FA over Coin** - Modern standard with better features
3. **Always check `exists` before `borrow_global`** - Prevents abort
4. **Store refs at creation time** - Can't generate refs later
5. **Use named objects for deterministic addresses** - Easier to find
6. **Emit events for important state changes** - Better indexability
7. **Use error codes with constants** - Easier debugging
8. **Test with `movement move test`** - Always test before deploy
