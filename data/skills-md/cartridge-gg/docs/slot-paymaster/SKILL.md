---
name: slot-paymaster
description: Set up and manage Slot paymasters to sponsor transaction fees for gasless user experiences.
---

# Slot Paymaster

Manage paymasters that sponsor transaction fees, enabling gasless experiences for users.
Zero integration required — when enabled, eligible transactions are automatically sponsored.

## Availability

- **Testnet**: Automatically enabled, no setup required
- **Mainnet**: Self-served via Slot CLI

## Creating a Paymaster

Requires an authenticated session (`slot auth login`) and a team with credits.

```sh
slot paymaster <name> create --team <team> --budget <amount> --unit CREDIT
```

The budget is deducted from the team's credit balance.
1 CREDIT = $0.01 USD.

## Budget Management

```sh
# Increase budget
slot paymaster <name> budget increase --amount <amount> --unit CREDIT

# Decrease budget
slot paymaster <name> budget decrease --amount <amount> --unit CREDIT
```

## Policy Management

Policies define which contracts and entrypoints the paymaster will sponsor.

### Add from preset (recommended)

Use verified contract presets from the Dojo ecosystem:

```sh
slot paymaster <name> policy add-from-preset --name <preset-name>
```

Presets are maintained at https://github.com/cartridge-gg/presets/tree/main/configs

### Add a single policy

```sh
slot paymaster <name> policy add --contract <address> --entrypoint <entry-point>
```

### Add from JSON

```sh
slot paymaster <name> policy add-from-json --file <path>
```

JSON format:

```json
[
  {
    "contractAddress": "0x1234...abcd",
    "entrypoint": "move_player"
  },
  {
    "contractAddress": "0x5678...efgh",
    "entrypoint": "attack",
    "predicate": {
      "address": "0x9abc...1234",
      "entrypoint": "check_attack_eligibility"
    }
  }
]
```

Predicates are optional.
When present, the predicate contract is called first — the transaction is only sponsored if it returns `true`.

### Remove policies

```sh
# Remove one
slot paymaster <name> policy remove --contract <address> --entrypoint <entry-point>

# Remove all (requires confirmation)
slot paymaster <name> policy remove-all

# List current policies
slot paymaster <name> policy list
```

## Info and Configuration

```sh
# View paymaster details, budget, and policy count
slot paymaster <name> info

# Rename
slot paymaster <name> update --name <new-name>

# Transfer to different team
slot paymaster <name> update --team <new-team>

# Enable/disable
slot paymaster <name> update --active false
slot paymaster <name> update --active true
```

## Monitoring

### Stats

```sh
slot paymaster <name> stats --last <period>
```

Period options: `1hr`, `2hr`, `24hr`, `1day`, `2day`, `7day`, `1week`.

### Transaction history

```sh
slot paymaster <name> transactions [OPTIONS]
```

Options:
- `--filter SUCCESS|REVERTED|ALL`
- `--last <period>`
- `--order-by FEES_ASC|FEES_DESC|EXECUTED_AT_DESC|EXECUTED_AT_ASC`
- `--limit <n>` (max 1000)

### Dune Analytics

Generate SQL queries for Dune dashboards:

```sh
# With actual timestamps
slot paymaster <name> dune --last 24hr

# With template parameters for Dune dashboards
slot paymaster <name> dune --dune-params
```

## Common Workflow: New Game Setup

```sh
# Create paymaster
slot paymaster my-game-pm create --team my-team --budget 1000 --unit CREDIT

# Add game contract policies
slot paymaster my-game-pm policy add --contract 0x123...abc --entrypoint move_player
slot paymaster my-game-pm policy add --contract 0x123...abc --entrypoint attack_enemy

# Verify setup
slot paymaster my-game-pm info
```
