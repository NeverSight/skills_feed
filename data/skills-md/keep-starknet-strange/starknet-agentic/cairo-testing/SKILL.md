---
name: cairo-testing
description: Use when writing tests for Cairo smart contracts — snforge test structure, contract deployment in tests, cheatcodes, event testing, fuzzing, fork testing.
license: Apache-2.0
metadata: {"author":"starknet-agentic","version":"1.0.0","org":"keep-starknet-strange"}
keywords: [cairo, testing, snforge, starknet-foundry, fuzzing, cheatcodes, integration-tests, unit-tests]
allowed-tools: [Bash, Read, Write, Glob, Grep, Task]
user-invocable: true
---

# Cairo Testing

Reference for testing Cairo smart contracts with Starknet Foundry (snforge).

## When to Use

- Writing unit tests for Cairo contract functions
- Writing integration tests that deploy and interact with contracts
- Using cheatcodes to manipulate block state, caller, timestamps
- Testing events are emitted correctly
- Fuzzing contract inputs
- Fork-testing against live Starknet state

**Not for:** Contract structure (use cairo-contracts), optimization (use cairo-optimization), deployment (use cairo-deploy)

## Setup

### Scarb.toml

```toml
[dev-dependencies]
snforge_std = "0.56.0"

[[target.starknet-contract]]
sierra = true
casm = true
```

> **Note:** snforge 0.56.0 requires Scarb >= 2.12.0. Check [scarbs.dev/packages/snforge_std](https://scarbs.dev/packages/snforge_std) for the latest version.

### Running Tests

```bash
# Run all tests
snforge test

# Run specific test by name
snforge test test_transfer

# Run tests matching a pattern
snforge test test_erc20

# Filter to a single test function (exact match)
snforge test --exact test_erc20_transfer

# Run with gas reporting
snforge test --detailed-resources
```

> **Tip:** Use `snforge test --filter <pattern>` or `snforge test <pattern>` to run a subset of tests during development. `--exact` matches the full test name when you need precision.

## Basic Test Structure

```cairo
#[cfg(test)]
mod tests {
    use super::MyContract;
    use starknet::ContractAddress;
    use starknet::contract_address_const;

    fn OWNER() -> ContractAddress {
        contract_address_const::<'OWNER'>()
    }

    fn USER() -> ContractAddress {
        contract_address_const::<'USER'>()
    }

    #[test]
    fn test_constructor() {
        let mut state = MyContract::contract_state_for_testing();
        MyContract::constructor(ref state, OWNER());
        assert(state.get_owner() == OWNER(), 'wrong owner');
    }
}
```

## Contract Deployment in Tests

For integration tests that need actual contract deployment:

```cairo
use snforge_std::{declare, ContractClassTrait, DeclareResultTrait};

fn deploy_contract() -> ContractAddress {
    let contract = declare("MyContract").unwrap().contract_class();
    let constructor_calldata = array![OWNER().into()];
    let (contract_address, _) = contract.deploy(@constructor_calldata).unwrap();
    contract_address
}

#[test]
fn test_deployed_contract() {
    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };
    assert(dispatcher.get_balance() == 0, 'initial balance should be 0');
}
```

## Cheatcodes

### Caller Address

```cairo
use snforge_std::{start_cheat_caller_address, stop_cheat_caller_address};

#[test]
fn test_only_owner() {
    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };

    // Impersonate OWNER
    start_cheat_caller_address(contract_address, OWNER());
    dispatcher.owner_only_function();  // should succeed
    stop_cheat_caller_address(contract_address);

    // Impersonate USER — should fail
    start_cheat_caller_address(contract_address, USER());
    // This should panic
}
```

### Block Timestamp

```cairo
use snforge_std::{start_cheat_block_timestamp, stop_cheat_block_timestamp};

#[test]
fn test_time_locked() {
    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };

    // Set block timestamp to future
    start_cheat_block_timestamp(contract_address, 1000000);
    dispatcher.time_sensitive_function();
    stop_cheat_block_timestamp(contract_address);
}
```

### Block Number

```cairo
use snforge_std::{start_cheat_block_number, stop_cheat_block_number};

start_cheat_block_number(contract_address, 500);
// ... test logic
stop_cheat_block_number(contract_address);
```

### Sequencer Address

```cairo
use snforge_std::{start_cheat_sequencer_address, stop_cheat_sequencer_address};

start_cheat_sequencer_address(contract_address, sequencer);
// ... test logic
stop_cheat_sequencer_address(contract_address);
```

## Expected Failures

### Expected Panic

```cairo
#[test]
#[should_panic(expected: 'Caller is not the owner')]
fn test_unauthorized_access() {
    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };

    start_cheat_caller_address(contract_address, USER());
    dispatcher.owner_only_function();  // should panic
}
```

### Expected Failure (any panic)

```cairo
#[test]
#[should_panic]
fn test_overflow() {
    let dispatcher = IMyContractDispatcher { contract_address: deploy_contract() };
    dispatcher.function_that_overflows();
}
```

## Event Testing

```cairo
use snforge_std::{spy_events, EventSpyAssertionsTrait, EventSpyTrait};

#[test]
fn test_transfer_emits_event() {
    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };

    let mut spy = spy_events();

    start_cheat_caller_address(contract_address, OWNER());
    dispatcher.transfer(USER(), 100);

    spy.assert_emitted(@array![
        (
            contract_address,
            MyContract::Event::Transfer(
                MyContract::Transfer {
                    from: OWNER(),
                    to: USER(),
                    amount: 100,
                }
            )
        )
    ]);
}
```

### Checking Event Count

```cairo
#[test]
fn test_event_count() {
    let mut spy = spy_events();

    // ... trigger events

    let events = spy.get_events();
    assert(events.events.len() == 2, 'expected 2 events');
}
```

## Fuzzing

```cairo
#[test]
#[fuzzer(runs: 256, seed: 12345)]
fn test_deposit_any_amount(amount: u256) {
    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };

    // Fund the user first (if needed)
    start_cheat_caller_address(contract_address, USER());
    dispatcher.deposit(amount);

    assert(dispatcher.get_balance(USER()) == amount, 'balance mismatch');
}
```

### Bounded Fuzzing

Use `assume` to constrain fuzz inputs:

```cairo
#[test]
#[fuzzer(runs: 100)]
fn test_transfer_bounded(amount: u256) {
    // Skip values that would overflow
    if amount == 0 || amount > 1000000 {
        return;
    }

    let contract_address = deploy_contract();
    let dispatcher = IMyContractDispatcher { contract_address };

    start_cheat_caller_address(contract_address, OWNER());
    dispatcher.transfer(USER(), amount);
}
```

## Fork Testing

Test against live Starknet state:

```cairo
use snforge_std::BlockTag;

#[test]
#[fork(url: "https://starknet-mainnet.g.alchemy.com/v2/YOUR_KEY", block_tag: latest)]
fn test_against_mainnet() {
    let usdc_address = contract_address_const::<0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8>();
    let dispatcher = IERC20Dispatcher { contract_address: usdc_address };

    let supply = dispatcher.total_supply();
    assert(supply > 0, 'USDC should have supply');
}
```

### Fork with Specific Block

```cairo
#[test]
#[fork(url: "https://starknet-mainnet.g.alchemy.com/v2/YOUR_KEY", block_number: 500000)]
fn test_at_specific_block() {
    // ... test against historical state
}
```

## Multi-Contract Tests

```cairo
fn setup() -> (ContractAddress, ContractAddress) {
    // Deploy token
    let token_class = declare("ERC20Token").unwrap().contract_class();
    let (token_addr, _) = token_class.deploy(@array![
        'MyToken'.into(), 'MTK'.into(), OWNER().into()
    ]).unwrap();

    // Deploy AMM that uses the token
    let amm_class = declare("AMM").unwrap().contract_class();
    let (amm_addr, _) = amm_class.deploy(@array![token_addr.into()]).unwrap();

    (token_addr, amm_addr)
}

#[test]
fn test_amm_swap() {
    let (token_addr, amm_addr) = setup();
    let token = IERC20Dispatcher { contract_address: token_addr };
    let amm = IAMMDispatcher { contract_address: amm_addr };

    // Approve AMM to spend tokens
    start_cheat_caller_address(token_addr, OWNER());
    token.approve(amm_addr, 1000);

    // Execute swap
    start_cheat_caller_address(amm_addr, OWNER());
    amm.swap(token_addr, 100);
}
```

## Test Organization

```
tests/
  test_unit.cairo        # unit tests (contract_state_for_testing)
  test_integration.cairo # integration tests (deploy + dispatch)
  test_fuzz.cairo        # fuzz tests
  helpers.cairo          # shared setup, deploy helpers, constants
```

### Shared Helpers Module

```cairo
// tests/helpers.cairo
use starknet::ContractAddress;
use starknet::contract_address_const;

fn OWNER() -> ContractAddress { contract_address_const::<'OWNER'>() }
fn USER() -> ContractAddress { contract_address_const::<'USER'>() }
fn ZERO() -> ContractAddress { contract_address_const::<0>() }

fn deploy_my_contract() -> ContractAddress {
    let contract = declare("MyContract").unwrap().contract_class();
    let (addr, _) = contract.deploy(@array![OWNER().into()]).unwrap();
    addr
}
```

## Gas Reporting

```bash
# Show gas usage per test
snforge test --detailed-resources

# Compare gas between runs (save output, diff manually)
snforge test --detailed-resources > gas-report.txt
```
