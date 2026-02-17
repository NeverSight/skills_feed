---
name: slot-vrng
description: Integrate Cartridge's verifiable random number generator (vRNG) into onchain games.
---

# Slot vRNG

Cartridge's Verifiable Random Number Generator provides cheap, atomic, verifiable randomness for onchain games.
Randomness is generated and verified within a single transaction.

## Contract Addresses

| Network | Address |
|---------|---------|
| Mainnet | `0x051fea4450da9d6aee758bdeba88b2f665bcbf549d2c61421aa724e9ac0ced8f` |
| Sepolia | `0x051fea4450da9d6aee758bdeba88b2f665bcbf549d2c61421aa724e9ac0ced8f` |

## Cairo Interface

```rust
#[starknet::interface]
trait IVrfProvider<TContractState> {
    fn request_random(self: @TContractState, caller: ContractAddress, source: Source);
    fn consume_random(ref self: TContractState, source: Source) -> felt252;
}

#[derive(Drop, Copy, Clone, Serde)]
pub enum Source {
    Nonce: ContractAddress,
    Salt: felt252,
}
```

### Source Types

- `Source::Nonce(ContractAddress)`: Uses the address's internal nonce.
Each request generates a different seed.
- `Source::Salt(felt252)`: Uses a provided salt.
Same salt = same random value.

## Usage in Contracts

```rust
const VRF_PROVIDER_ADDRESS: starknet::ContractAddress =
    starknet::contract_address_const::<0x051fea4450da9d6aee758bdeba88b2f665bcbf549d2c61421aa724e9ac0ced8f>();

fn roll_dice(ref self: ContractState) {
    let vrf_provider = IVrfProviderDispatcher { contract_address: VRF_PROVIDER_ADDRESS };
    let player_id = get_caller_address();
    let random_value = vrf_provider.consume_random(Source::Nonce(player_id));
    // Use random_value in game logic
}
```

## Executing vRNG Transactions

`request_random` must be the first call in the multicall.
The Cartridge Paymaster wraps the multicall with `submit_random` and `assert_consumed`.

```js
const call = await account.execute([
  // First: request_random
  {
    contractAddress: VRF_PROVIDER_ADDRESS,
    entrypoint: 'request_random',
    calldata: CallData.compile({
      caller: GAME_CONTRACT,
      // Source::Nonce(address)
      source: { type: 0, address: account.address },
      // Or Source::Salt(felt252)
      // source: { type: 1, salt: 0x123 },
    }),
  },
  // Then: your game call
  {
    contractAddress: GAME_CONTRACT,
    entrypoint: 'roll_dice',
    // ...
  },
]);
```

The `source` in `request_random` must match the `source` in `consume_random`.

## Controller Policy

Add the vRNG contract to your Controller policies:

```typescript
const policies: Policy[] = [
  // ... your existing policies ...
  {
    target: VRF_PROVIDER_ADDRESS,
    method: "request_random",
    description: "Allows requesting random numbers from the VRF provider",
  },
];
```

## Security

Phase 0 assumes the Provider has not revealed the private key and does not collude with players.
Future plans include moving the Provider to a Trusted Execution Environment (TEE).
