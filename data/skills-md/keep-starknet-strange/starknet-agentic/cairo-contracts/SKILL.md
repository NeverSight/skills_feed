---
name: cairo-contracts
description: Use when writing Cairo smart contracts on Starknet — contract structure, storage, events, interfaces, components, OpenZeppelin v3 patterns, and common contract templates.
license: Apache-2.0
metadata: {"author":"starknet-agentic","version":"1.0.0","org":"keep-starknet-strange"}
keywords: [cairo, contracts, starknet, openzeppelin, components, storage, events, interfaces, erc20, erc721]
allowed-tools: [Bash, Read, Write, Glob, Grep, Task]
user-invocable: true
---

# Cairo Contracts

Reference for writing Cairo smart contracts on Starknet. Covers structure, storage, events, interfaces, components, and OpenZeppelin v3 patterns.

> **Optimization:** After your contract compiles and tests pass, use the [cairo-optimization](../cairo-optimization/) skill as a separate pass.

## When to Use

- Writing a new Starknet smart contract from scratch
- Adding storage, events, or interfaces to an existing contract
- Using OpenZeppelin components (Ownable, ERC20, ERC721, AccessControl, Upgradeable)
- Implementing the component pattern with `embeddable_as`
- Structuring a multi-contract project with Scarb

**Not for:** Gas optimization (use cairo-optimization), testing (use cairo-testing), deployment (use cairo-deploy)

## Contract Structure

Every Starknet contract follows this skeleton:

```cairo
#[starknet::contract]
mod MyContract {
    use starknet::ContractAddress;
    use starknet::storage::{StoragePointerReadAccess, StoragePointerWriteAccess};

    #[storage]
    struct Storage {
        owner: ContractAddress,
        balance: u256,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        Transfer: Transfer,
    }

    #[derive(Drop, starknet::Event)]
    struct Transfer {
        #[key]
        from: ContractAddress,
        #[key]
        to: ContractAddress,
        amount: u256,
    }

    #[constructor]
    fn constructor(ref self: ContractState, owner: ContractAddress) {
        self.owner.write(owner);
    }

    #[abi(embed_v0)]
    impl MyContractImpl of super::IMyContract<ContractState> {
        fn get_balance(self: @ContractState) -> u256 {
            self.balance.read()
        }

        fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) {
            // implementation
        }
    }
}
```

## Interfaces

Define interfaces outside the contract module. Use `#[starknet::interface]`:

```cairo
#[starknet::interface]
trait IMyContract<TContractState> {
    fn get_balance(self: @TContractState) -> u256;
    fn transfer(ref self: TContractState, to: ContractAddress, amount: u256);
}
```

- `self: @TContractState` — read-only (view function)
- `ref self: TContractState` — read-write (external function)

## Storage

### Basic Types

```cairo
#[storage]
struct Storage {
    value: felt252,           // single felt
    counter: u128,            // unsigned integer
    owner: ContractAddress,   // address
    is_active: bool,          // boolean
}
```

### Maps

```cairo
use starknet::storage::Map;

#[storage]
struct Storage {
    balances: Map<ContractAddress, u256>,
    allowances: Map<(ContractAddress, ContractAddress), u256>,
}

// Usage:
fn get_balance(self: @ContractState, account: ContractAddress) -> u256 {
    self.balances.read(account)
}

fn set_allowance(ref self: ContractState, owner: ContractAddress, spender: ContractAddress, amount: u256) {
    self.allowances.write((owner, spender), amount);
}
```

### Composite Key Maps (Nested Map Alternative)

Prefer composite key tuples over nested Maps:

```cairo
use starknet::storage::Map;

#[storage]
struct Storage {
    // Map<(owner, spender), amount> — preferred over nested Map
    allowances: Map<(ContractAddress, ContractAddress), u256>,
}

// Usage:
let amount = self.allowances.entry((owner, spender)).read();
self.allowances.entry((owner, spender)).write(new_amount);
```

## Events

```cairo
#[event]
#[derive(Drop, starknet::Event)]
enum Event {
    Transfer: Transfer,
    Approval: Approval,
}

#[derive(Drop, starknet::Event)]
struct Transfer {
    #[key]    // indexed — used for filtering
    from: ContractAddress,
    #[key]
    to: ContractAddress,
    amount: u256,  // not indexed — stored in data
}

// Emit:
self.emit(Transfer { from, to, amount });
```

## Components (OpenZeppelin v3 Pattern)

Components are reusable contract modules. This is the standard pattern in Cairo / OZ v3:

### Using a Component

The **Mixin pattern** is the most common approach in OZ v3 — it exposes all standard interface methods (e.g., `balance_of`, `transfer`, `approve`) in a single `impl` block:

```cairo
#[starknet::contract]
mod MyToken {
    use openzeppelin_access::ownable::OwnableComponent;
    use openzeppelin_token::erc20::{ERC20Component, ERC20HooksEmptyImpl};

    component!(path: OwnableComponent, storage: ownable, event: OwnableEvent);
    component!(path: ERC20Component, storage: erc20, event: ERC20Event);

    // Embed external implementations (makes functions callable from outside)
    #[abi(embed_v0)]
    impl OwnableMixinImpl = OwnableComponent::OwnableMixinImpl<ContractState>;
    #[abi(embed_v0)]
    impl ERC20MixinImpl = ERC20Component::ERC20MixinImpl<ContractState>;

    // Internal implementations (for use inside the contract)
    impl OwnableInternalImpl = OwnableComponent::InternalImpl<ContractState>;
    impl ERC20InternalImpl = ERC20Component::InternalImpl<ContractState>;

    #[storage]
    struct Storage {
        #[substorage(v0)]
        ownable: OwnableComponent::Storage,
        #[substorage(v0)]
        erc20: ERC20Component::Storage,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        #[flat]
        OwnableEvent: OwnableComponent::Event,
        #[flat]
        ERC20Event: ERC20Component::Event,
    }

    #[constructor]
    fn constructor(ref self: ContractState, owner: ContractAddress) {
        self.ownable.initializer(owner);
        self.erc20.initializer("MyToken", "MTK");
    }
}
```

### Writing a Component

```cairo
#[starknet::component]
mod MyComponent {
    use starknet::ContractAddress;
    use starknet::storage::{StoragePointerReadAccess, StoragePointerWriteAccess};

    #[storage]
    struct Storage {
        value: u256,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        ValueChanged: ValueChanged,
    }

    #[derive(Drop, starknet::Event)]
    struct ValueChanged {
        new_value: u256,
    }

    #[embeddable_as(MyComponentImpl)]
    impl MyComponent<
        TContractState, +HasComponent<TContractState>
    > of super::IMyComponent<ComponentState<TContractState>> {
        fn get_value(self: @ComponentState<TContractState>) -> u256 {
            self.value.read()
        }

        fn set_value(ref self: ComponentState<TContractState>, new_value: u256) {
            self.value.write(new_value);
            self.emit(ValueChanged { new_value });
        }
    }
}
```

## Common OpenZeppelin Components

### Scarb.toml Dependencies

```toml
[dependencies]
starknet = ">=2.12.0"
openzeppelin_access = "3.0.0"
openzeppelin_token = "3.0.0"
openzeppelin_upgrades = "3.0.0"
openzeppelin_introspection = "3.0.0"
openzeppelin_security = "3.0.0"
```

> **Note:** OZ packages are on the [Scarb registry](https://scarbs.dev). No git tags needed. Check `scarbs.dev` for the latest version.

### Ownable

```cairo
use openzeppelin_access::ownable::OwnableComponent;

component!(path: OwnableComponent, storage: ownable, event: OwnableEvent);

#[abi(embed_v0)]
impl OwnableMixinImpl = OwnableComponent::OwnableMixinImpl<ContractState>;
impl OwnableInternalImpl = OwnableComponent::InternalImpl<ContractState>;

// In constructor:
self.ownable.initializer(owner);

// In functions:
self.ownable.assert_only_owner();
```

### Upgradeable

```cairo
use openzeppelin_upgrades::UpgradeableComponent;
use openzeppelin_upgrades::interface::IUpgradeable;

component!(path: UpgradeableComponent, storage: upgradeable, event: UpgradeableEvent);

impl UpgradeableInternalImpl = UpgradeableComponent::InternalImpl<ContractState>;

#[abi(embed_v0)]
impl UpgradeableImpl of IUpgradeable<ContractState> {
    fn upgrade(ref self: ContractState, new_class_hash: ClassHash) {
        self.ownable.assert_only_owner();
        self.upgradeable.upgrade(new_class_hash);
    }
}
```

### ERC20

```cairo
use openzeppelin_token::erc20::{ERC20Component, ERC20HooksEmptyImpl};

component!(path: ERC20Component, storage: erc20, event: ERC20Event);

#[abi(embed_v0)]
impl ERC20MixinImpl = ERC20Component::ERC20MixinImpl<ContractState>;
impl ERC20InternalImpl = ERC20Component::InternalImpl<ContractState>;

// In constructor:
self.erc20.initializer("TokenName", "TKN");
self.erc20.mint(recipient, initial_supply);
```

### AccessControl

```cairo
use openzeppelin_access::accesscontrol::AccessControlComponent;
use openzeppelin_access::accesscontrol::DEFAULT_ADMIN_ROLE;

component!(path: AccessControlComponent, storage: access_control, event: AccessControlEvent);

#[abi(embed_v0)]
impl AccessControlMixinImpl = AccessControlComponent::AccessControlMixinImpl<ContractState>;
impl AccessControlInternalImpl = AccessControlComponent::InternalImpl<ContractState>;

const MINTER_ROLE: felt252 = selector!("MINTER_ROLE");

// In constructor:
self.access_control.initializer();
self.access_control._grant_role(DEFAULT_ADMIN_ROLE, admin);
self.access_control._grant_role(MINTER_ROLE, minter);

// In functions:
self.access_control.assert_only_role(MINTER_ROLE);
```

## Project Structure

```
my-project/
  Scarb.toml
  src/
    lib.cairo          # mod declarations
    contract.cairo     # main contract
    interfaces.cairo   # trait definitions
    components/
      mod.cairo
      my_component.cairo
  tests/
    test_contract.cairo
```

### lib.cairo

```cairo
mod contract;
mod interfaces;
mod components;
```

## Common Patterns

### Reentrancy Guard

```cairo
#[storage]
struct Storage {
    entered: bool,
}

fn _enter(ref self: ContractState) {
    assert(!self.entered.read(), 'ReentrancyGuard: reentrant');
    self.entered.write(true);
}

fn _exit(ref self: ContractState) {
    self.entered.write(false);
}
```

### Pausable

```cairo
use openzeppelin_security::pausable::PausableComponent;

component!(path: PausableComponent, storage: pausable, event: PausableEvent);

// In functions:
self.pausable.assert_not_paused();
```

### Constructor Validation

```cairo
#[constructor]
fn constructor(ref self: ContractState, owner: ContractAddress) {
    assert(!owner.is_zero(), 'Owner cannot be zero');
    self.ownable.initializer(owner);
}
```
