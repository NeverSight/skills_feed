---
name: crunch-coordinate
description: Use when managing Crunch coordinators, competitions (crunches), rewards, checkpoints, staking, or cruncher accounts via the crunch-cli. Also use when working inside a coordinator node workspace (contains .agent/ folder, docker-compose.yml, runtime_definitions/, or CrunchConfig).
---

# Crunch Protocol CLI Skill

Translates natural language queries into `crunch-cli` commands. Supports profiles and output formatting for Slack, Telegram, Discord, or plain text.

## Prerequisites
- Node.js 18+ with `npm`
- Solana wallet keypair (for on-chain operations)

## Package Installation

This skill installs packages via npm (global):

| Package | Source | Purpose |
|---------|--------|---------|
| `@crunchdao/crunch-cli` | [npm](https://www.npmjs.com/package/@crunchdao/crunch-cli) | CrunchDAO protocol CLI (coordinators, competitions, staking) |

**Agent rules for package installation:**
- **Only install `@crunchdao/crunch-cli`** from the official npm registry
- **No custom registry URLs** — no `--registry` overrides
- **Ask the user before installing** if not already present

## Credentials

### Solana Wallet Keypair (required for on-chain operations)
- **What it is:** A JSON file containing a Solana private key, used to sign transactions
- **How it's configured:** Set via `crunch-cli config set wallet /path/to/wallet.json` or `-w` flag per command
- **Stored in:** User-managed file on disk; path referenced in `~/.crunch/config.json`

**Agent rules for wallets:**
- **Never create or generate wallet keypairs** unless the user explicitly asks and understands the security implications
- **Never read or display** the contents of wallet keypair files
- **Never commit wallet files** to git — always verify `.gitignore` covers them
- **Ask the user** for the wallet path — never assume or search for keypair files

### Profile Config (`~/.crunch/config.json`)
- Stores network, wallet path, and RPC URL per profile
- Managed via `crunch-cli config` commands — no need to edit manually
- **Never modify or delete existing profiles** unless explicitly asked

## Setup

```bash
npm install -g @crunchdao/crunch-cli
crunch-cli --version
```

## Profiles

The CLI has built-in profile management via `~/.crunch/config.json`:

```bash
crunch-cli config show                    # Show current config
crunch-cli config active                  # Show resolved active values
crunch-cli config list-profiles           # List available profiles
crunch-cli config save-profile <name>     # Save current config as profile
crunch-cli config use <profile>           # Switch profile
crunch-cli config set <key> <value>       # Set config value
```

Global flags can override config per-command:

| Flag | Description |
|------|-------------|
| `-n, --network` | Solana network: `mainnet-beta`, `devnet`, `localhost` |
| `-u, --url` | Custom RPC URL |
| `-w, --wallet` | Path to Solana keypair |
| `-o, --output` | Output format: `json`, `table`, `yaml` |

## Direct Phrase Mapping

| User Phrase | CLI Command |
|-------------|-------------|
| `get/show crunch <name>` | `crunch-cli crunch get "<name>"` |
| `list crunches` | `crunch-cli crunch list` |
| `get/show coordinator [address]` | `crunch-cli coordinator get [address]` |
| `list coordinators` | `crunch-cli coordinator list` |
| `get config` | `crunch-cli coordinator get-config` |
| `checkpoint for <name>` | `crunch-cli crunch checkpoint-get-current "<name>"` |
| `create checkpoint <name>` | `crunch-cli crunch checkpoint-create "<name>" prizes.json` |
| `deposit reward <name> <amount>` | `crunch-cli crunch deposit-reward "<name>" <amount>` |
| `drain <name>` | `crunch-cli crunch drain "<name>"` |
| `create/register cruncher` | `crunch-cli cruncher create` |
| `register for <name>` | `crunch-cli cruncher register "<name>"` |
| `claim rewards <name>` | `crunch-cli cruncher claim "<name>"` |
| `show staking positions` | `crunch-cli staking positions` |
| `stake/deposit <amount>` | `crunch-cli staking deposit <amount>` |
| `delegate to <coordinator>` | `crunch-cli staking delegate "<coordinator>" <amount>` |
| `show staking rewards` | `crunch-cli staking rewards` |
| `claim staking rewards` | `crunch-cli staking claim` |
| `undelegate from <coordinator>` | `crunch-cli staking undelegate "<coordinator>" <amount>` |
| `withdraw stake <amount>` | `crunch-cli staking withdraw <amount>` |
| `init workspace <name>` | `crunch-cli init-workspace "<name>"` |
| `list scenarios/simulations` | `crunch-cli model list` |
| `run simulation <scenario>` | `crunch-cli model run "<scenario>"` |
| `register coordinator <name>` | `crunch-cli coordinator register "<name>"` |
| `create crunch <name>` | `crunch-cli crunch create "<name>" <amount> [maxModels]` |
| `start/end crunch <name>` | `crunch-cli crunch start/end "<name>"` |

## Execution Pattern

1. **Parse** — Identify action, target, name/identifier, parameters
2. **Resolve profile** — If mentioned, switch profile or use flags
3. **Map** — Use phrase mapping table
4. **Execute** — Run command
5. **Format** — Output for requested medium (Slack/Telegram/Discord/plain)

## Output Formatting

Detect medium from user request ("for slack", "telegram format", etc.):

- **Slack:** `*bold*`, `•` bullets, `━` separators
- **Telegram:** `<b>bold</b>`, emoji prefixes
- **Discord:** `## headers`, `**bold**`
- **Plain:** Simple key: value pairs

## Error Handling

If command fails, suggest fixes:
- Wrong network? Add `-n mainnet-beta` or `-n devnet`
- Missing wallet? Add `-w /path/to/wallet.json`
- Not found? List available with `crunch-cli crunch list`

## Coordinator Node Setup

### Scaffolding rules

1. **Do not require cloning a template repo** — always use the CLI scaffold flow
2. **Always prefer CLI flow** (`crunch-cli init-workspace`)
3. Generated workspaces must be **standalone and runnable from their own folder**
4. Always validate after changes with `make deploy && make verify-e2e`

### Scaffold a new workspace

```bash
crunch-cli init-workspace my-challenge
```

This generates:
- `my-challenge/crunch-node-my-challenge/` — node deployment (workers, docker, config)
- `my-challenge/crunch-my-challenge/` — challenge package (tracker, scoring, examples)

### Design checklist (collect before coding)

For every new challenge, confirm these points before implementation:

1. **Model interface** — tracker class that participants implement
2. **Scoring function** — how predictions are scored against actuals
3. **Feed configuration** — source, subjects, kind, granularity
4. **Ground truth resolution** — how actuals are derived from feed data
5. **Emission config** — crunch pubkey, provider wallets, tier distribution

If any are missing, ask follow-up questions before proceeding.

### After scaffolding: customize and deploy

```bash
cd my-challenge/crunch-node-my-challenge
make deploy
make verify-e2e
```

Report API at http://localhost:8000

---

## Working in a Coordinator Workspace

When you detect you are inside a coordinator node workspace (look for `.agent/` folder, `docker-compose.yml`, `runtime_definitions/`, or `CrunchConfig`), load the project-specific agent context:

1. **Read `.agent/context.md`** — project architecture, extension points, do-not-edit zones
2. **Read `.agent/policy.md`** — rules, approval gates, output contracts
3. **Read the relevant playbook** from `.agent/playbooks/`:
   - `feature.md` — adding a new feature
   - `bugfix.md` — diagnosing and fixing a bug
   - `customize.md` — changing competition types, scoring, feeds, emission
   - `release.md` — deploying to production
4. **Read subfolder context** when working in a specific area:
   - `node/.agent/context.md` — workers, docker, config, API, edit boundaries
   - `challenge/.agent/context.md` — tracker, scoring, backtest, examples

These files are the source of truth for how to operate in that workspace. They contain approval gates, allowed operations, and validation requirements specific to the project. Follow them.

## Reference

For full CLI documentation: [references/cli-reference.md](references/cli-reference.md)
