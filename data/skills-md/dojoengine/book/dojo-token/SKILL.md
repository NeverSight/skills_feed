---
name: dojo-token
description: Implement ERC20 and ERC721 token standards in Dojo using Origami library. Use when adding fungible tokens, NFTs, or token-based game mechanics.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Dojo Token Standards

Implement ERC20 fungible tokens and ERC721 NFTs in your Dojo game using the Origami library.

## When to Use This Skill

- "Implement ERC20 token for game currency"
- "Create NFT items with ERC721"
- "Add token standard to my game"
- "Use Origami for tokens"

## What This Skill Does

Implements token standards:
- ERC20 fungible tokens (currency, resources)
- ERC721 non-fungible tokens (items, characters)
- Token minting and burning
- Transfer mechanics
- Balance tracking

## Token Standards

### ERC20 - Fungible Tokens

For interchangeable assets:
- Game currency (gold, gems)
- Resources (wood, stone)
- Experience points

**Properties:**
- Divisible (can have fractions)
- Interchangeable (any token = any other)
- Track balances per account

### ERC721 - Non-Fungible Tokens

For unique assets:
- Character NFTs
- Equipment/items
- Land plots
- Achievements

**Properties:**
- Unique (each has token ID)
- Indivisible (whole units only)
- Individual ownership tracking

## Using Origami Library

### Installation

Add to `Scarb.toml`:
```toml
[dependencies]
origami_token = { git = "https://github.com/dojoengine/origami", tag = "v1.0.0" }
```

Origami provides reusable token components following standard interfaces.
Refer to the [Origami documentation](https://github.com/dojoengine/origami) for the latest API.

## Simple Token Implementation

You can implement tokens using standard Dojo models without Origami:

### ERC20-like Currency

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Gold {
    #[key]
    pub player: ContractAddress,
    pub amount: u256,
}

#[starknet::interface]
trait IGoldToken<T> {
    fn mint(ref self: T, to: ContractAddress, amount: u256);
    fn transfer(ref self: T, to: ContractAddress, amount: u256);
    fn balance_of(self: @T, account: ContractAddress) -> u256;
}

#[dojo::contract]
mod gold_token {
    use super::{IGoldToken, Gold};
    use starknet::{ContractAddress, get_caller_address};
    use dojo::model::ModelStorage;

    #[abi(embed_v0)]
    impl GoldTokenImpl of IGoldToken<ContractState> {
        fn mint(ref self: ContractState, to: ContractAddress, amount: u256) {
            let mut world = self.world_default();

            let mut balance: Gold = world.read_model(to);
            balance.amount += amount;
            world.write_model(@balance);
        }

        fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) {
            let mut world = self.world_default();
            let from = get_caller_address();

            let mut from_balance: Gold = world.read_model(from);
            let mut to_balance: Gold = world.read_model(to);

            assert(from_balance.amount >= amount, 'insufficient balance');

            from_balance.amount -= amount;
            to_balance.amount += amount;

            world.write_model(@from_balance);
            world.write_model(@to_balance);
        }

        fn balance_of(self: @ContractState, account: ContractAddress) -> u256 {
            let world = self.world_default();
            let balance: Gold = world.read_model(account);
            balance.amount
        }
    }

    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
            self.world(@"my_game")
        }
    }
}
```

### ERC721-like NFT

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Weapon {
    #[key]
    pub token_id: u256,
    pub owner: ContractAddress,
    pub damage: u32,
    pub rarity: u8,
}

#[starknet::interface]
trait IWeaponNFT<T> {
    fn mint(ref self: T, to: ContractAddress, damage: u32) -> u256;
    fn transfer(ref self: T, to: ContractAddress, token_id: u256);
    fn owner_of(self: @T, token_id: u256) -> ContractAddress;
}

#[dojo::contract]
mod weapon_nft {
    use super::{IWeaponNFT, Weapon};
    use starknet::{ContractAddress, get_caller_address};
    use dojo::model::ModelStorage;

    #[abi(embed_v0)]
    impl WeaponNFTImpl of IWeaponNFT<ContractState> {
        fn mint(ref self: ContractState, to: ContractAddress, damage: u32) -> u256 {
            let mut world = self.world_default();

            let token_id: u256 = world.uuid().into();

            let weapon = Weapon {
                token_id,
                owner: to,
                damage,
                rarity: 1,
            };

            world.write_model(@weapon);
            token_id
        }

        fn transfer(ref self: ContractState, to: ContractAddress, token_id: u256) {
            let mut world = self.world_default();
            let from = get_caller_address();

            let mut weapon: Weapon = world.read_model(token_id);
            assert(weapon.owner == from, 'not owner');

            weapon.owner = to;
            world.write_model(@weapon);
        }

        fn owner_of(self: @ContractState, token_id: u256) -> ContractAddress {
            let world = self.world_default();
            let weapon: Weapon = world.read_model(token_id);
            weapon.owner
        }
    }

    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
            self.world(@"my_game")
        }
    }
}
```

## Game Patterns

### In-Game Currency

```cairo
// Award gold for completing quest
fn complete_quest(ref self: ContractState, quest_id: u32) {
    let mut world = self.world_default();
    let player = get_caller_address();

    // Check quest is completed
    // ...

    // Award gold
    let mut gold: Gold = world.read_model(player);
    gold.amount += 100;
    world.write_model(@gold);
}

// Spend gold to buy item
fn buy_item(ref self: ContractState, item_id: u32, price: u256) {
    let mut world = self.world_default();
    let player = get_caller_address();

    let mut gold: Gold = world.read_model(player);
    assert(gold.amount >= price, 'insufficient gold');

    gold.amount -= price;
    world.write_model(@gold);

    // Give item to player
    // ...
}
```

### Multiple Resource Types

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Resources {
    #[key]
    pub player: ContractAddress,
    pub wood: u256,
    pub stone: u256,
    pub iron: u256,
}
```

### Equipment NFTs

```cairo
fn equip_weapon(ref self: ContractState, token_id: u256) {
    let mut world = self.world_default();
    let player = get_caller_address();

    // Check ownership
    let weapon: Weapon = world.read_model(token_id);
    assert(weapon.owner == player, 'not owner');

    // Equip
    let mut equipment: Equipment = world.read_model(player);
    equipment.weapon_id = token_id;
    world.write_model(@equipment);
}
```

## Token Events

```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::event]
pub struct TokenTransferred {
    #[key]
    pub from: ContractAddress,
    #[key]
    pub to: ContractAddress,
    pub amount: u256,
}

#[derive(Copy, Drop, Serde)]
#[dojo::event]
pub struct NFTTransferred {
    #[key]
    pub token_id: u256,
    pub from: ContractAddress,
    pub to: ContractAddress,
}

// Emit in your functions
world.emit_event(@TokenTransferred { from, to, amount });
```

## Considerations

- **Balance checks**: Always verify sufficient balance before transfers
- **Ownership**: Always verify ownership before NFT operations
- **Overflow**: Use u256 for token amounts to avoid overflow
- **Events**: Emit events for all token operations for indexing
- **Permissions**: Grant writer permission to token contracts

## Next Steps

After implementing tokens:
1. Test thoroughly with `dojo-test` skill
2. Deploy with `dojo-deploy` skill
3. Integrate with client (`dojo-client` skill)
4. Set up permissions (`dojo-world` skill)

## Related Skills

- **dojo-model**: Token models extend Dojo models
- **dojo-system**: Token logic in systems
- **dojo-test**: Test token operations
- **dojo-review**: Audit token implementation
