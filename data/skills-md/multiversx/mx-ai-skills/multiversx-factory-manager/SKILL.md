---
name: multiversx-factory-manager
description: Factory pattern for deploying and managing child contracts from a parent manager. Use when building marketplaces, launchpads, multi-tenant systems, or any protocol that deploys child contracts from a template.
---

# MultiversX Factory/Manager Pattern

Deploy, track, and upgrade child contracts from a template — the three core operations of a factory manager.

## What Problem Does This Solve?

When a protocol needs to deploy multiple instances of the same contract (e.g., one per user, per market, per pool), a factory manager handles the deployment lifecycle: deploy from a template, track all instances, and upgrade them when the template changes.

## When to Use

| Scenario | Use Factory? |
|---|---|
| Multiple instances of same contract needed | Yes |
| Each user/entity gets their own contract | Yes |
| Single contract serves all users | No |
| Different contract types per deployment | No — use separate deploy logic |

## Core Concept

```
Manager Contract
├── Stores template address (code to clone)
├── Deploy: creates child from template via from_source()
├── Track: registry of all deployed children
└── Upgrade: applies new template to existing children
```

## Operation 1: Deploy

Deploy a new child contract using `from_source()` to clone the template:

```rust
#[endpoint(deployChild)]
fn deploy_child(
    &self,
    child_id: ManagedBuffer,
    init_arg_a: BigUint,
    init_arg_b: ManagedAddress,
) -> ManagedAddress {
    let caller = self.blockchain().get_caller();
    let template = self.template_address().get();

    let metadata = CodeMetadata::UPGRADEABLE
        | CodeMetadata::READABLE
        | CodeMetadata::PAYABLE;

    // Deploy from template
    let new_address = self.tx()
        .typed(child_proxy::ChildProxy) // ChildProxy generated from child contract's #[multiversx_sc::proxy]
        .init(init_arg_a, init_arg_b)
        .from_source(template)
        .code_metadata(metadata)
        .returns(ReturnsNewManagedAddress)
        .sync_call();

    // Register in tracking
    self.child_addresses().insert(new_address.clone());
    self.child_by_id(&child_id).set(new_address.clone());

    self.deploy_event(&caller, &child_id, &new_address);
    new_address
}
```

### CodeMetadata Explained

| Flag | Effect | When to Use |
|---|---|---|
| `UPGRADEABLE` | Child can be upgraded later | Almost always — needed for Operation 3 |
| `READABLE` | Other contracts can read child's storage | When using cross-contract storage reads |
| `PAYABLE` | Child can receive EGLD directly | When child needs to accept payments |
| `PAYABLE_BY_SC` | Only other SCs can pay child | When child should only interact with contracts |

## Operation 2: Track (Registry)

```rust
#[multiversx_sc::module]
pub trait RegistryModule {
    // Template to clone from
    #[storage_mapper("templateAddress")]
    fn template_address(&self) -> SingleValueMapper<ManagedAddress>;

    // Set of all deployed child addresses
    #[storage_mapper("childAddresses")]
    fn child_addresses(&self) -> SetMapper<ManagedAddress>;

    // Lookup: ID → child address
    #[storage_mapper("childById")]
    fn child_by_id(&self, id: &ManagedBuffer) -> SingleValueMapper<ManagedAddress>;

    // Admin set (who can deploy/upgrade)
    #[storage_mapper("admins")]
    fn admins(&self) -> UnorderedSetMapper<ManagedAddress>;

    // Helper: verify address is a managed child
    fn require_managed_child(&self, address: &ManagedAddress) {
        require!(
            self.child_addresses().contains(address),
            "Not a managed child contract"
        );
    }
}
```

**Pattern**: `SetMapper` for the full set (iteration + contains check) + `SingleValueMapper` for ID-based lookup. This gives you both O(1) lookup by ID and iteration over all children.

## Operation 3: Upgrade

Upgrade a single child to the current template:

```rust
#[endpoint(upgradeChild)]
fn upgrade_child(&self, child_id: ManagedBuffer) {
    self.require_admin();

    let child_address = self.child_by_id(&child_id).get();
    self.require_managed_child(&child_address);

    let metadata = CodeMetadata::UPGRADEABLE
        | CodeMetadata::READABLE
        | CodeMetadata::PAYABLE;

    self.tx()
        .to(child_address)
        .typed(child_proxy::ChildProxy) // ChildProxy generated from child contract's #[multiversx_sc::proxy]
        .upgrade()
        .code_metadata(metadata)
        .from_source(self.template_address().get())
        .upgrade_async_call_and_exit();
}
```

> **Note**: When the child contract proxy is not available (e.g., template-based deployment from external code), use `raw_deploy()` instead of `typed()` for deployment.

## Template Management

```rust
#[only_owner]
#[endpoint(setTemplate)]
fn set_template(&self, template_address: ManagedAddress) {
    require!(
        self.blockchain().is_smart_contract(&template_address),
        "Address is not a smart contract"
    );
    self.template_address().set(template_address);
}
```

## Admin Hierarchy

```
Owner (deployer of manager)
  └── Admins (can deploy/upgrade children)
       └── Users (interact with their own child)
```

```rust
fn require_admin(&self) {
    let caller = self.blockchain().get_caller();
    require!(
        self.admins().contains(&caller)
            || caller == self.blockchain().get_owner_address(),
        "Not authorized"
    );
}
```

## Anti-Patterns

### 1. No Registry Tracking
```rust
// WRONG — deploying without tracking makes upgrades impossible
let addr = self.tx().typed(ChildProxy).init().from_source(template).sync_call();
// addr is lost after this transaction!
```

### 2. Missing UPGRADEABLE Flag
```rust
// WRONG — child can never be upgraded
let metadata = CodeMetadata::READABLE | CodeMetadata::PAYABLE;
// Should include CodeMetadata::UPGRADEABLE
```

### 3. Upgrading Without Validation
```rust
// WRONG — no check that address is actually a managed child
fn upgrade(&self, address: ManagedAddress) {
    self.tx().to(address).typed(ChildProxy).upgrade()
        .from_source(self.template_address().get())
        .upgrade_async_call_and_exit();
}
```

## Template

```rust
#[multiversx_sc::module]
pub trait FactoryModule {
    #[storage_mapper("templateAddress")]
    fn template_address(&self) -> SingleValueMapper<ManagedAddress>;

    #[storage_mapper("childAddresses")]
    fn child_addresses(&self) -> SetMapper<ManagedAddress>;

    #[storage_mapper("childById")]
    fn child_by_id(&self, id: &ManagedBuffer) -> SingleValueMapper<ManagedAddress>;

    #[storage_mapper("admins")]
    fn admins(&self) -> UnorderedSetMapper<ManagedAddress>;
}
```
