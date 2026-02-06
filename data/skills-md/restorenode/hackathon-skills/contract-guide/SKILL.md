---
name: contract-guide
description: 'Expert guide for writing smart contracts on Initia. It helps identify the correct libraries, naming conventions, and deployment patterns for Move, Wasm, and EVM.'
---

# Contract Guide Skill

This skill provides expert guidance for writing smart contracts on Initia. It helps identify the correct libraries, naming conventions, and deployment patterns for Move, Wasm, and EVM.

## MoveVM

### Project Structure

A typical MoveVM project on Initia has the following structure:

```
.
├── Move.toml
└── sources
    └── *.move
```

-   `Move.toml`: The manifest file that defines the project's metadata, dependencies, and addresses.
-   `sources/`: The directory containing the Move source code files.

### Key Libraries and Dependencies

-   **InitiaStdlib**: The standard library for Initia Move modules. It is typically included as a dependency in `Move.toml`:
    ```toml
    [dependencies]
    InitiaStdlib = { git = "https://github.com/initia-labs/movevm.git", subdir = "precompile/modules/initia_stdlib", rev = "main" }
    ```

### Naming Conventions

-   **Modules and Functions:** `snake_case` (e.g., `module my_module`, `fun my_function`).

### Example: Oracle Integration

Here is an example of a Move module that interacts with an oracle:

```move
module example::oracle_example {
    use std::string::String;
    use initia_std::oracle::get_price;

    #[view]
    public fun get_price_example(pair_id: String): (u256, u64, u64) {
        let (price, timestamp, decimals) = get_price(pair_id);
        (price, timestamp, decimals)
    }

    #[test]
    public fun test_get_price_example(): (u256, u64, u64) {
        let btc_usd_pair_id = string::utf8(b"BITCOIN/USD");
        let (price, timestamp, decimals) = get_price_example(btc_usd_pair_id);
        (price, timestamp, decimals)
    }
}
```

## WasmVM (CosmWasm)

### Project Structure

A typical WasmVM project on Initia follows the standard CosmWasm project structure:

```
.
├── Cargo.toml
└── src
    ├── lib.rs
    ├── contract.rs
    ├── msg.rs
    ├── state.rs
    └── error.rs
```

### Key Libraries and Dependencies

-   **cosmwasm-std**: The standard library for CosmWasm contracts.
-   **cw-storage-plus**: A library for managing contract storage.
-   **slinky_wasm**: A specific library for interacting with Initia's oracle.

Example `Cargo.toml` dependencies:

```toml
[dependencies]
cosmwasm-schema = "2.0.1"
cosmwasm-std = { version = "2.0.1", features = ["cosmwasm_1_3"] }
cw-storage-plus = "2.0.0"
cw2 = "2.0.0"
schemars = "0.8.16"
serde = { version = "1.0.197", default-features = false, features = ["derive"] }
thiserror = { version = "1.0.58" }
slinky_wasm = { path = "packages/slinky_wasm" }
```

### Coding Patterns

-   **Entry Points:** Use the standard `#[entry_point]` macro for `instantiate`, `execute`, and `query` functions.
-   **Oracle Integration:** Use the `slinky_wasm` library to query the oracle. Queries are made using `QueryRequest::Wasm(WasmQuery::Smart { ... })`.

### Example: Oracle Query

```rust
pub mod query {
    use cosmwasm_std::{QueryRequest, WasmQuery};
    use slinky_wasm::oracle::GetAllCurrencyPairsResponse;

    // ...

    pub fn example_get_price(deps: Deps) -> StdResult<GetPriceResponse> {
        let state = STATE.load(deps.storage)?;
        let slinky_addr = state.slinky;

        let base_asset = "BTC";
        let quote_asset = "USD";

        deps.querier.query(&QueryRequest::Wasm(WasmQuery::Smart {
            contract_addr: slinky_addr.to_string(),
            msg: to_json_binary(&slinky_wasm::oracle::QueryMsg::GetPrice {
                base: base_asset.to_string(),
                quote: quote_asset.to_string(),
            })?,
        }))
    }
}
```

## EVM (Solidity)

### Project Structure

A typical EVM project on Initia uses the Foundry toolchain:

```
.
├── foundry.toml
├── src
│   └── *.sol
├── lib
└── script
```

### Key Libraries and Dependencies

-   **initia-evm-contracts**: The key library for Initia EVM development. It is usually included as a git submodule in the `lib` directory.

### Coding Patterns

-   **Oracle Integration:** Use the `ISlinky` interface from `initia-evm-contracts` to interact with the oracle.

### Naming Conventions

-   **Functions:** `snake_case`
-   **Variables:** `camelCase`

### Example: Oracle Integration

```solidity
pragma solidity ^0.8.24;

import "initia-evm-contracts/src/interfaces/ISlinky.sol";

contract Oracle {

    ISlinky immutable public slinky;

    constructor (address _slinky) {
        slinky = ISlinky(_slinky);
    }

    function oracle_get_price() external {
        string memory base = "BTC";
        string memory quote = "USD";
        price = slinky.get_price(base, quote);
    }
}
```
