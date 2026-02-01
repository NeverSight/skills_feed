---
name: bittensor
description: Query Bittensor network using the Python SDK. Get metagraph data, subnet info, validator stats, and more. Use when user asks about TAO, subnets, validators, emissions, or staking.
---

# Bittensor SDK

Query the Bittensor decentralized AI network with structured JSON output.

## SDK Scripts

Run scripts with Python (assumes bittensor installed):

```bash
# Top validators on a subnet
python scripts/metagraph.py --netuid 8 --top 5

# List all subnets  
python scripts/subnets.py

# Specify network
python scripts/metagraph.py --netuid 1 --network test
```

## Available Scripts

| Script | Purpose | Args |
|--------|---------|------|
| `metagraph.py` | Subnet validators sorted by emission | `--netuid`, `--top`, `--network` |
| `subnets.py` | List all subnets | `--network` |

## Output Format

All scripts return JSON:

```json
{
  "netuid": 8,
  "name": "Vanta",
  "n_neurons": 256,
  "top_validators": [
    {"rank": 1, "name": "τaoshi validator", "emission": 147.67, "stake": 11859.70}
  ]
}
```

## Common Queries

**"Who are the top validators on subnet X?"**
```bash
python scripts/metagraph.py --netuid X --top 10
```

**"List all subnets"**
```bash
python scripts/subnets.py
```

**"What's the emission on SN8?"**
Run metagraph.py and sum the emissions from top_validators.

## CLI Fallback

For queries without SDK scripts, use `btcli`:

```bash
btcli wallet balance --wallet.name default
btcli stake list --wallet.name default
btcli subnets register --netuid 8 --wallet.name default
```

## Networks

- `finney` — Mainnet (default)
- `test` — Testnet
