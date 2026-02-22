---
name: cairo-deploy
description: Use when deploying Cairo contracts to Starknet — sncast commands, account setup, declare/deploy workflow, network configuration, contract verification.
license: Apache-2.0
metadata: {"author":"starknet-agentic","version":"1.0.0","org":"keep-starknet-strange"}
keywords: [cairo, deploy, sncast, starknet, devnet, sepolia, mainnet, declare, verification]
allowed-tools: [Bash, Read, Write, Glob, Grep, Task]
user-invocable: true
---

# Cairo Deploy

Reference for deploying Cairo smart contracts to Starknet using sncast (Starknet Foundry).

## When to Use

- Deploying contracts to Starknet devnet, Sepolia, or mainnet
- Declaring contract classes
- Setting up deployer accounts
- Configuring network endpoints
- Verifying deployed contracts
- Invoking/calling deployed contracts

**Not for:** Writing contracts (use cairo-contracts), testing (use cairo-testing), optimization (use cairo-optimization)

## Setup

### Install Starknet Foundry

```bash
# Install via asdf (recommended for version pinning)
asdf plugin add starknet-foundry
asdf install starknet-foundry 0.56.0
asdf global starknet-foundry 0.56.0

# Or install directly
curl -L https://raw.githubusercontent.com/foundry-rs/starknet-foundry/master/scripts/install.sh | sh
snfoundryup
```

### .tool-versions

Pin versions for reproducible builds:

```
scarb 2.15.1
starknet-foundry 0.56.0
```

> **Note:** snforge 0.56.0 requires Scarb >= 2.12.0. Check [github.com/foundry-rs/starknet-foundry/releases](https://github.com/foundry-rs/starknet-foundry/releases) for the latest.

## Build

```bash
# Build contracts (generates Sierra + CASM)
scarb build
```

Output goes to `target/dev/`:
- `myproject_MyContract.contract_class.json` (Sierra)
- `myproject_MyContract.compiled_contract_class.json` (CASM)

## Account Setup

### Create a New Account

```bash
# Generate account on Sepolia
sncast account create \
    --url https://starknet-sepolia.g.alchemy.com/v2/YOUR_KEY \
    --name my-deployer

# This outputs the account address — fund it with ETH/STRK before deploying

# Deploy the account contract
sncast account deploy \
    --url https://starknet-sepolia.g.alchemy.com/v2/YOUR_KEY \
    --name my-deployer
```

### Import Existing Account

```bash
sncast account add \
    --url https://starknet-sepolia.g.alchemy.com/v2/YOUR_KEY \
    --name my-deployer \
    --address 0x123... \
    --private-key 0xabc... \
    --type oz
```

Account types: `oz` (OpenZeppelin), `argent`, `braavos`

## sncast.toml

Configure defaults to avoid repeating flags:

```toml
[default]
url = "https://starknet-sepolia.g.alchemy.com/v2/YOUR_KEY"
account = "my-deployer"
accounts-file = "~/.starknet_accounts/starknet_open_zeppelin_accounts.json"
wait = true

[mainnet]
url = "https://starknet-mainnet.g.alchemy.com/v2/YOUR_KEY"
account = "mainnet-deployer"
```

Use profiles: `sncast --profile mainnet declare ...`

## Declare (Register Class)

Before deploying, declare the contract class on-chain:

```bash
# Declare contract
sncast declare \
    --contract-name MyContract

# Output:
# class_hash: 0x1234...
# transaction_hash: 0xabcd...
```

If the class is already declared, sncast will tell you — that's fine, use the existing class hash.

## Deploy (Create Instance)

```bash
# Deploy with constructor args
sncast deploy \
    --class-hash 0x1234... \
    --constructor-calldata 0xOWNER_ADDRESS

# Multiple constructor args (space-separated)
sncast deploy \
    --class-hash 0x1234... \
    --constructor-calldata 0xOWNER 0xTOKEN_ADDRESS 1000
```

### Constructor Calldata Encoding

Arguments are passed as felt252 values:
- `ContractAddress` — pass as hex `0x123...`
- `u256` — pass as TWO felts: `low high` (e.g., `1000 0` for 1000)
- `felt252` — pass directly
- `bool` — `1` for true, `0` for false
- `ByteArray` (strings) — use sncast's string encoding or pass raw

## Invoke (Write)

```bash
# Call a write function
sncast invoke \
    --contract-address 0xCONTRACT \
    --function "transfer" \
    --calldata 0xRECIPIENT 1000 0
```

## Call (Read)

```bash
# Call a view function (free, no tx)
sncast call \
    --contract-address 0xCONTRACT \
    --function "get_balance" \
    --calldata 0xACCOUNT
```

## Multicall

Execute multiple calls in a single transaction:

```bash
# Create a multicall file
cat > multicall.toml << 'EOF'
[[call]]
call_type = "deploy"
class_hash = "0x1234..."
inputs = ["0xOWNER"]

[[call]]
call_type = "invoke"
contract_address = "0xTOKEN"
function = "approve"
inputs = ["0xSPENDER", "1000", "0"]
EOF

sncast multicall run --path multicall.toml
```

## Deploy Script Pattern

For complex deployments, use a script:

```bash
#!/bin/bash
set -euo pipefail

RPC_URL="https://starknet-sepolia.g.alchemy.com/v2/YOUR_KEY"
ACCOUNT="my-deployer"

echo "Building..."
scarb build

echo "Declaring MyToken..."
TOKEN_CLASS=$(sncast declare --contract-name MyToken --url $RPC_URL --account $ACCOUNT | grep "class_hash" | awk '{print $2}')
echo "Token class: $TOKEN_CLASS"

echo "Deploying MyToken..."
TOKEN_ADDR=$(sncast deploy --class-hash $TOKEN_CLASS --constructor-calldata 0xOWNER --url $RPC_URL --account $ACCOUNT | grep "contract_address" | awk '{print $2}')
echo "Token deployed at: $TOKEN_ADDR"

echo "Declaring AMM..."
AMM_CLASS=$(sncast declare --contract-name AMM --url $RPC_URL --account $ACCOUNT | grep "class_hash" | awk '{print $2}')

echo "Deploying AMM..."
AMM_ADDR=$(sncast deploy --class-hash $AMM_CLASS --constructor-calldata $TOKEN_ADDR --url $RPC_URL --account $ACCOUNT | grep "contract_address" | awk '{print $2}')
echo "AMM deployed at: $AMM_ADDR"

echo "Done. Addresses:"
echo "  Token: $TOKEN_ADDR"
echo "  AMM:   $AMM_ADDR"
```

## Network Endpoints

| Network | RPC URL |
|---------|---------|
| Devnet (local) | `http://localhost:5050` |
| Sepolia (testnet) | `https://starknet-sepolia.g.alchemy.com/v2/KEY` |
| Mainnet | `https://starknet-mainnet.g.alchemy.com/v2/KEY` |

Alternative providers: Infura, Blast, Nethermind (free tier available).

### Local Devnet

```bash
# Install and run starknet-devnet-rs
cargo install starknet-devnet
starknet-devnet --seed 42

# Devnet provides pre-funded accounts — use them for testing
```

## Contract Verification

Verify source code on Voyager or Starkscan:

```bash
# Verify on Voyager (manual: upload Sierra JSON via web UI)
# https://sepolia.voyager.online/contract/0xADDRESS#code

# Or use Walnut for programmatic verification
# https://app.walnut.dev
```

> **Note:** `sncast verify` currently only supports the Walnut verification backend. Voyager and Starkscan verification must be done through their respective web UIs.

## Upgradeable Contracts

For contracts using OZ UpgradeableComponent:

```bash
# 1. Declare new class
sncast declare --contract-name MyContractV2

# 2. Call upgrade on existing contract
sncast invoke \
    --contract-address 0xEXISTING_CONTRACT \
    --function "upgrade" \
    --calldata 0xNEW_CLASS_HASH
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Contract not found` | Account not deployed | Run `sncast account deploy` |
| `Insufficient max fee` | Not enough ETH/STRK for gas | Fund the deployer account |
| `Class already declared` | Same class hash exists | Use the existing class hash for deploy |
| `Entry point not found` | Wrong function name | Check the contract ABI |
| `Invalid calldata` | Wrong number/type of args | Check constructor signature, remember u256 = 2 felts |
