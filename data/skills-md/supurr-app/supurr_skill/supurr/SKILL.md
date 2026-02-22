---
name: supurr
description: Backtest, deploy, and monitor trading bots on Hyperliquid. Supports Grid, DCA, and Spot-Perp Arbitrage strategies across Native Perps, Spot markets (USDC/USDH), and HIP-3 sub-DEXes.
---

# Supurr CLI — Complete Command Reference

> **For LLMs**: This is the authoritative reference. Use exact syntax. Config files are in `~/.supurr/configs/`.

---

## Quick Reference

| Command                | Purpose                       |
| ---------------------- | ----------------------------- |
| `supurr init`          | Setup wallet credentials      |
| `supurr whoami`        | Show current wallet           |
| `supurr new grid`      | Generate grid strategy config |
| `supurr new arb`       | Generate spot-perp arb config |
| `supurr new dca`       | Generate DCA strategy config  |
| `supurr configs`       | List saved configs            |
| `supurr config <name>` | View config details           |
| `supurr backtest`      | Run historical simulation     |
| `supurr deploy`        | Deploy bot to production      |
| `supurr monitor`       | View active bots              |
| `supurr inspect <id>`  | Deep dive into a specific bot |
| `supurr account`       | Hyperliquid account dashboard |
| `supurr history`       | View historical bot sessions  |
| `supurr stop`          | Stop a running bot (signed)   |
| `supurr prices`        | Debug price data              |
| `supurr update`        | Update CLI to latest          |

---

## Global Options

```bash
supurr --help              # Show all commands
supurr --version, -V       # Show CLI version
supurr -d, --debug         # Enable debug logging (any command)
```

---

## 1. `supurr init` — Credential Setup

```bash
# Interactive
supurr init

# Non-interactive
supurr init --address 0x... --api-wallet 0x...

# Overwrite existing
supurr init --force
```

| Option                | Description                    |
| --------------------- | ------------------------------ |
| `-f, --force`         | Overwrite existing credentials |
| `--address <address>` | Wallet address (0x...)         |
| `--api-wallet <key>`  | API wallet private key         |

---

## 2. `supurr whoami` — Show Identity

```bash
supurr whoami    # Shows: Address + masked key
```

---

## 3. `supurr new <strategy>` — Config Generator

Supports three strategies: `grid`, `arb`, `dca`.

```bash
supurr new grid [options]   # Grid trading
supurr new arb [options]    # Spot-perp arbitrage
supurr new dca [options]    # Dollar-cost averaging
```

### Unified Asset Format

The `--asset` flag supports a **unified format** that auto-detects the market type from delimiters:

| Format      | Delimiter   | Type              | Example             |
| ----------- | ----------- | ----------------- | ------------------- |
| `BTC`       | none        | Perp              | `--asset BTC`       |
| `ETH-USDC`  | `-` (dash)  | Perp (with quote) | `--asset ETH-USDC`  |
| `HYPE/USDC` | `/` (slash) | Spot              | `--asset HYPE/USDC` |
| `HYPE/USDH` | `/` (slash) | Spot (non-USDC)   | `--asset HYPE/USDH` |
| `hyna:BTC`  | `:` (colon) | HIP-3             | `--asset hyna:BTC`  |

> The old flags (`--type`, `--quote`, `--dex`) **still work** and override the unified format when both are provided.

```bash
# These produce identical configs:
supurr new grid --asset HYPE/USDC
supurr new grid --asset HYPE --type spot --quote USDC
```

---

### 3a. `supurr new grid` — Grid Strategy

#### Market Types

| Type     | Quote    | Requires  | Example                                 |
| -------- | -------- | --------- | --------------------------------------- |
| `native` | USDC     | —         | `--asset BTC`                           |
| `spot`   | Variable | `--quote` | `--asset HYPE --type spot --quote USDC` |
| `hip3`   | Per-DEX  | `--dex`   | `--asset BTC --type hip3 --dex hyna`    |

#### Grid Options

| Option                  | Default       | Description                                    |
| ----------------------- | ------------- | ---------------------------------------------- |
| `-a, --asset <symbol>`  | `BTC`         | Base asset (BTC, ETH, HYPE, etc.)              |
| `-o, --output <file>`   | `config.json` | Output filename                                |
| `--type <type>`         | `native`      | Market type: native, spot, hip3                |
| `--dex <dex>`           | —             | **Required for hip3**: hyna, xyz, km, vntl     |
| `--quote <quote>`       | —             | **Required for spot**: USDC, USDE, USDT0, USDH |
| `--mode <mode>`         | `long`        | Grid mode: long, short, neutral                |
| `--levels <n>`          | `20`          | Number of grid levels                          |
| `--start-price <price>` | —             | Grid start price                               |
| `--end-price <price>`   | —             | Grid end price                                 |
| `--investment <amount>` | `1000`        | Max investment in quote currency               |
| `--leverage <n>`        | `2`           | Leverage (1 for spot)                          |
| `--testnet`             | false         | Use Hyperliquid testnet                        |

#### Grid Examples

```bash
# Native Perp (BTC-USDC)
supurr new grid --asset BTC --levels 4 --start-price 88000 --end-price 92000 --investment 100 --leverage 20

# USDC Spot (HYPE/USDC)
supurr new grid --asset HYPE --type spot --quote USDC --levels 3 --start-price 29 --end-price 32 --investment 100

# Non-USDC Spot (HYPE/USDH)
supurr new grid --asset HYPE --type spot --quote USDH --levels 3 --start-price 29 --end-price 32 --investment 100

# HIP-3 (hyna:BTC)
supurr new grid --asset BTC --type hip3 --dex hyna --levels 4 --start-price 88000 --end-price 92000 --investment 100 --leverage 20
```

#### HIP-3 DEXes

| DEX    | Quote | Assets                              |
| ------ | ----- | ----------------------------------- |
| `hyna` | USDE  | Crypto perps (BTC, ETH, HYPE, etc.) |
| `xyz`  | USDE  | Stocks (AAPL, TSLA, etc.)           |
| `km`   | USDT  | Kinetiq Markets                     |
| `vntl` | USDE  | AI/tech tokens                      |

---

### 3b. `supurr new arb` — Spot-Perp Arbitrage Strategy

Generates a config that simultaneously trades the **spot** and **perp** legs of the same asset, capturing spread differentials.

> **Market Constraint**: Only assets that have **both** a spot token AND a perp market on Hyperliquid are eligible. The CLI auto-resolves the spot counterpart.

#### Spot Resolution Logic

Hyperliquid spot tokens for major assets use a `U`-prefix naming convention:

| You pass `--asset` | CLI resolves spot token | Spot pair  | Perp pair  |
| ------------------ | ----------------------- | ---------- | ---------- |
| `BTC`              | `UBTC`                  | UBTC/USDC  | BTC perp   |
| `ETH`              | `UETH`                  | UETH/USDC  | ETH perp   |
| `SOL`              | `USOL`                  | USOL/USDC  | SOL perp   |
| `ENA`              | `UENA`                  | UENA/USDC  | ENA perp   |
| `WLD`              | `UWLD`                  | UWLD/USDC  | WLD perp   |
| `MON`              | `UMON`                  | UMON/USDC  | MON perp   |
| `MEGA`             | `UMEGA`                 | UMEGA/USDC | MEGA perp  |
| `ZEC`              | `UZEC`                  | UZEC/USDC  | ZEC perp   |
| `XPL`              | `UXPL`                  | UXPL/USDC  | XPL perp   |
| `PUMP`             | `UPUMP`                 | UPUMP/USDC | PUMP perp  |
| `HYPE`             | `HYPE` (exact name)     | HYPE/USDC  | HYPE perp  |
| `TRUMP`            | `TRUMP` (exact name)    | TRUMP/USDC | TRUMP perp |
| `PURR`             | `PURR` (exact name)     | PURR/USDC  | PURR perp  |
| `BERA`             | `BERA` (exact name)     | BERA/USDC  | BERA perp  |

Resolution order: try `U{ASSET}` first → fallback to exact name → fail if neither exists.

> **⚠️ U-prefix Hazard**: Do NOT pass asset names that already start with `U` (e.g., `UNIT`). The CLI will prepend another `U` and look for `UUNIT`, which doesn't exist. Always use the **perp ticker name** (e.g., `BTC`, not `UBTC`).

#### Arb Options

| Option                 | Default            | Description                                  |
| ---------------------- | ------------------ | -------------------------------------------- |
| `-a, --asset <symbol>` | `BTC`              | Perp asset name (BTC, ETH, HYPE, etc.)       |
| `--amount <usdc>`      | `100`              | Order amount in USDC per leg                 |
| `--leverage <n>`       | `1`                | Leverage for perp leg                        |
| `--open-spread <pct>`  | `0.003`            | Min opening spread (0.003 = 0.3%)            |
| `--close-spread <pct>` | `-0.001`           | Min closing spread (-0.001 = -0.1%)          |
| `--slippage <pct>`     | `0.001`            | Slippage buffer for both legs (0.001 = 0.1%) |
| `-o, --output <file>`  | `{asset}-arb.json` | Output filename                              |
| `--testnet`            | false              | Use Hyperliquid testnet                      |

#### Arb Examples

```bash
# BTC spot-perp arb (default $100/leg)
supurr new arb --asset BTC

# HYPE arb with $50 per leg, 2x leverage on perp
supurr new arb --asset HYPE --amount 50 --leverage 2

# ETH arb with tighter spreads
supurr new arb --asset ETH --open-spread 0.002 --close-spread -0.0005 --slippage 0.0005

# SOL arb on testnet
supurr new arb --asset SOL --testnet
```

> **Balance Requirement**: Arb bots require USDC balance in **both** Spot and Perps wallets on Hyperliquid, since the bot trades on both sides simultaneously.

---

### 3c. `supurr new dca` — DCA Strategy

Generates a Dollar-Cost Averaging config that opens positions in steps when price deviates, then takes profit on the averaged entry.

#### DCA Options

| Option                       | Default       | Description                                        |
| ---------------------------- | ------------- | -------------------------------------------------- |
| `-a, --asset <symbol>`       | `BTC`         | Base asset                                         |
| `--mode <mode>`              | `long`        | Direction: long or short                           |
| `--type <type>`              | `native`      | Market type: native, spot, hip3                    |
| `--trigger-price <price>`    | `100000`      | Price to trigger base order                        |
| `--base-order <size>`        | `0.001`       | Base order size in base asset                      |
| `--dca-order <size>`         | `0.001`       | DCA order size in base asset                       |
| `--max-orders <n>`           | `5`           | Max number of DCA orders                           |
| `--size-multiplier <x>`      | `2.0`         | Size multiplier per DCA step                       |
| `--deviation <pct>`          | `0.01`        | Price deviation % to trigger first DCA (0.01 = 1%) |
| `--deviation-multiplier <x>` | `1.0`         | Deviation multiplier for subsequent steps          |
| `--take-profit <pct>`        | `0.02`        | Take profit % from avg entry (0.02 = 2%)           |
| `--stop-loss <pnl>`          | —             | Optional stop loss as absolute PnL threshold       |
| `--leverage <n>`             | `2`           | Leverage (1 for spot)                              |
| `--restart`                  | false         | Restart cycle after take profit                    |
| `--cooldown <secs>`          | `60`          | Cooldown between cycles in seconds                 |
| `-o, --output <file>`        | `config.json` | Output filename                                    |
| `--testnet`                  | false         | Use Hyperliquid testnet                            |

#### DCA Examples

```bash
# BTC DCA long, trigger at $95k
supurr new dca --asset BTC --trigger-price 95000

# ETH DCA short with custom deviation
supurr new dca --asset ETH --mode short --deviation 0.02

# HYPE DCA with auto-restart
supurr new dca --asset HYPE --restart --cooldown 120 --take-profit 0.03

# DCA on spot market
supurr new dca --asset HYPE --type spot --quote USDC --trigger-price 25
```

---

## 4. `supurr configs` — List Saved Configs

```bash
supurr configs    # Lists all configs in ~/.supurr/configs/
```

**Output:**

```
📁 Configs (/Users/you/.supurr/configs):
  btc-grid.json         grid     BTC-USDC
  hype-usdc-spot.json   grid     HYPE-USDC
  hyna-btc.json         grid     BTC-USDE
```

---

## 5. `supurr config <name>` — View Config

```bash
supurr config btc-grid        # View btc-grid.json
supurr config btc-grid.json   # Same
```

---

## 6. `supurr backtest` — Run Backtest

### Syntax

```bash
supurr backtest -c <config> [options]
```

> **Supported strategies**: Grid and DCA only. Arb (spot-perp arbitrage) backtesting is **not supported** — arb requires simultaneous dual-market execution that cannot be accurately simulated from single-asset price feeds.

### Options

| Option                | Description                              |
| --------------------- | ---------------------------------------- |
| `-c, --config <file>` | **Required.** Config file (name or path) |
| `-s, --start <date>`  | Start date (YYYY-MM-DD)                  |
| `-e, --end <date>`    | End date (YYYY-MM-DD)                    |
| `-p, --prices <file>` | Use local prices file                    |
| `-o, --output <file>` | Save results to JSON                     |
| `--no-cache`          | Disable price caching                    |

### Examples

```bash
# By config name (looks in ~/.supurr/configs/)
supurr backtest -c btc-grid.json -s 2026-01-28 -e 2026-02-01

# By full path
supurr backtest -c ~/.supurr/configs/btc-grid.json -s 2026-01-28 -e 2026-02-01

# Save results
supurr backtest -c btc-grid.json -s 2026-01-28 -e 2026-02-01 -o results.json
```

### Archive Data Availability

| Dex           | Asset Format           | Example            |
| ------------- | ---------------------- | ------------------ |
| `hyperliquid` | `BTC`, `HYPE`          | Native perp + Spot |
| `hyna`        | `hyna:BTC`, `hyna:ETH` | HIP-3 DEX          |

> **Note**: Archive data available from 2026-01-28 onwards.
>
> **Important**: Backtests use Supurr's price archive (tick-level) or a user-provided prices file (`-p`). Do **not** use Hyperliquid Info API mids/candles for backtests; they don't provide tick-level historical data and will produce inaccurate results.

---

## 7. `supurr deploy` — Deploy Bot

```bash
supurr deploy -c <config> [-s <address> | -v <address>]
```

| Option                       | Description                                             |
| ---------------------------- | ------------------------------------------------------- |
| `-c, --config <file>`        | **Required.** Config file (name or path)                |
| `-s, --subaccount <address>` | Trade from a subaccount (validates master ownership)    |
| `-v, --vault <address>`      | Trade from a vault (validates you are the vault leader) |

> **Subaccount vs Vault:**
>
> - **Subaccount** = personal trading account under your master wallet. Verified via `subAccounts` API (checks `master` field).
> - **Vault** = shared investment pool you manage. Verified via `vaultDetails` API (checks `leader` field).
> - Both set `vault_address` in the bot config on success.
> - **Cannot use both** `--subaccount` and `--vault` simultaneously.

### Examples

```bash
# Deploy from main wallet
supurr deploy -c btc-grid.json

# Deploy from subaccount
supurr deploy -c btc-grid.json -s 0x804e57d7baeca937d4b30d3cbe017f8d73c21f1b

# Deploy from vault (you must be the vault leader)
supurr deploy -c config.json --vault 0xdc89f67e74098dd93a1476f7da79747f71ccb5d9

# HL: prefix is auto-stripped (copy-paste from Hyperliquid UI)
supurr deploy -c config.json -s HL:0x804e57d7baeca937d4b30d3cbe017f8d73c21f1b
```

**Output:**

```
✔ Loaded config for grid strategy
✔ Subaccount verified: 0x804e57d7...
✔ Bot deployed successfully!
📦 Deployment Details
  Bot ID:       217
  Pod Name:     bot-217
  Bot Type:     grid
  Market:       BTC-USDC
```

### Gotchas

| Issue                        | Solution                                                                   |
| ---------------------------- | -------------------------------------------------------------------------- |
| `HL:` prefix in address      | Auto-stripped — safe to paste from Hyperliquid explorer                    |
| "Subaccount not owned"       | Ensure the subaccount's `master` matches your `supurr whoami` address      |
| "Vault not found"            | Check the vault address exists on the correct network (mainnet vs testnet) |
| "Vault leader mismatch"      | Only the vault leader can deploy — check `vaultDetails` API                |
| `subAccounts` returns `null` | Normal — means no subaccounts exist for that address                       |

---

## 8. `supurr monitor` — View User's Bots

> **Updated in v0.3.0**: Now shows only the user's bots by default (requires `supurr init`). Use `--history` to include stopped bots.

### Syntax

```bash
supurr monitor [options]
```

### Options

| Option                   | Description                          |
| ------------------------ | ------------------------------------ |
| `-w, --wallet <address>` | Filter by wallet address             |
| `--watch`                | Live mode (refreshes every 2s)       |
| `--history`              | Show all bots including stopped ones |

### Examples

```bash
supurr monitor                 # Show only active bots for current user
supurr monitor --history       # Show all bots (active + stopped)
supurr monitor --watch         # Live monitoring (Ctrl+C to exit)
supurr monitor --watch --history  # Live monitoring with history
supurr monitor -w 0x1234...    # Filter by wallet
```

### Behavior

- **User-Specific**: Fetches bots for the address in `~/.supurr/credentials.json` (from `supurr init`)
- **Default**: Shows only active bots (status = "running" or "starting")
- **With `--history`**: Shows all bots including stopped ones
- **Header**: Displays user address and sync delay: `🤖 Active Bots  │  User: 0x0ecba...  │  Sync delay: 0s`
- **Trading Link**: Shows clickable visualization link at the end with correct market format:
  - **Spot**: `KNTQ_USDH` (underscore separator)
  - **Perp**: `BTC-USDC` (hyphen separator)
  - **HIP-3**: `vntl:ANTHROPIC` (dex:base format)

**Output Columns:**

- **ID** — Bot identifier
- **Type** — Strategy (grid, dca, mm, arb)
- **Market** — Trading pair (BTC-USDC, HYPE-USDH)
- **Position** — Size + direction (L=Long, S=Short)
- **PnL** — Total profit/loss

**Example Output:**

```
🤖 Active Bots  │  User: 0x0ecba...  │  Sync delay: 0s

ID   Type  Market       Position  PnL
299  grid  KNTQ-USDH    0.5 L     +12.34
300  arb   BTC-USDC     -         +5.67

📊 Visualize: https://trade.supurr.app/trade/KNTQ_USDH?user_address=0x0ecba...
```

---

## 8b. `supurr inspect <bot_id>` — Per-Bot Deep Dive

Fetches bot metadata from the Bot API and enriches with live Hyperliquid data (position, orders, fills).

### Syntax

```bash
supurr inspect <bot_id> [options]
```

### Options

| Option        | Description                     |
| ------------- | ------------------------------- |
| `<bot_id>`    | **Required.** Bot ID to inspect |
| `-w, --watch` | Live refresh every 3 seconds    |

### Examples

```bash
supurr inspect 302            # Detailed view of bot 302
supurr inspect 302 --watch    # Live refresh (Ctrl+C to exit)
```

### Output Sections

```
╔══════════════════════════════════════════════════════════════════╗
║  🤖 Bot #302  │  arb  │  UETH/USDC  │  Running (2h 14m)       ║
╚══════════════════════════════════════════════════════════════════╝

📊 Position — direction, size, entry/mark price, leverage, liq price
💰 PnL Breakdown — realized, unrealized, funding, total
📋 Active Orders — all resting orders for this bot's market
📜 Recent Fills — last trades with time, side, price, size, fee
⚙️ Config Snapshot — strategy params, spreads, investment
📊 Visualize — clickable trade.supurr.app link
```

### Data Sources

| Section            | Source  | Endpoint                              |
| ------------------ | ------- | ------------------------------------- |
| Bot metadata & PnL | Bot API | `user_bots/{address}` → filter by ID  |
| Position details   | HL Info | `clearinghouseState` → filter by coin |
| Active orders      | HL Info | `frontendOpenOrders` → filter by coin |
| Recent fills       | HL Info | `userFills` → filter by coin          |
| Config             | Bot API | Included in bot response              |

> **Sub-account awareness**: The bot's config stores the actual trading address. Inspect auto-uses this for HL queries.

---

## 8c. `supurr account` — Hyperliquid Account Dashboard

Displays perp margin, spot balances, positions, and optionally open orders, fills, and order history — all sourced directly from the Hyperliquid Info API.

### Syntax

```bash
supurr account [options]
```

### Options

| Option      | Description             |
| ----------- | ----------------------- |
| `--orders`  | Also show open orders   |
| `--fills`   | Also show recent fills  |
| `--history` | Also show order history |

### Examples

```bash
supurr account                     # Overview: margin + positions + spot
supurr account --orders            # Also show open orders
supurr account --fills             # Also show recent fills
supurr account --orders --fills    # Show orders and fills
supurr account --history           # Show order history
```

### Default Output

```
╔══════════════════════════════════════════════════════╗
║  💰 Account: 0x1234...abcd                           ║
╚══════════════════════════════════════════════════════╝

🏦 Perp Margin
  Account Value: 12,450.00 USDC
  Total Margin:   3,200.00 USDC
  Available:      9,250.00 USDC

📈 Positions (2)
  Asset   │ Side  │ Size     │ Entry    │ Mark     │ UPnL
  BTC     │ LONG  │ 0.0100   │ 97500.0  │ 98200.0  │ +7.00
  ETH     │ SHORT │ 0.5000   │ 3100.0   │ 3085.0   │ +7.50

💎 Spot Balances
  Token   │ Balance      │ Value (USD)
  USDC    │ 5,000.00     │ 5,000.00
  HYPE    │ 120.50       │ 2,410.00
```

### Data Source

All data comes directly from Hyperliquid Info API — no backend dependency:

| Feature                 | HL Endpoint              |
| ----------------------- | ------------------------ |
| Perp margin & positions | `clearinghouseState`     |
| Spot balances           | `spotClearinghouseState` |
| Open orders             | `frontendOpenOrders`     |
| Recent fills            | `userFills`              |
| Order history           | `historicalOrders`       |

## 9. `supurr history` — View Bot History

```bash
supurr history             # Show last 20 bot sessions
supurr history -n 50       # Show last 50 bot sessions
```

| Option                | Default | Description            |
| --------------------- | ------- | ---------------------- |
| `-n, --limit <count>` | `20`    | Number of bots to show |

**Output Columns:**

- **ID** — Bot identifier
- **Market** — Trading pair (from `config.markets[0]`)
- **Type** — Strategy (grid, dca, mm, arb)
- **PnL** — Total profit/loss (realized + unrealized)
- **Stop Reason** — Why the bot stopped (`shutdown:graceful` → "User stopped the bot Successfully")

---

## 10. `supurr stop` — Stop Bot (Signature Auth)

Signs `Stop <bot-id>` with your API wallet private key (EIP-191 personal_sign) and sends the signature to the bot API.

```bash
supurr stop              # Interactive - select from list
supurr stop --id 217     # Stop specific bot by ID
```

| Option          | Description                            |
| --------------- | -------------------------------------- |
| `--id <bot_id>` | Bot ID to stop (from `supurr monitor`) |

> **Crypto:** Uses `@noble/curves/secp256k1` + `@noble/hashes/sha3` (pure JS, no native deps). Signature format: `0x{r}{s}{v}` (65 bytes).

---

## 11. `supurr prices` — Debug Price Data

```bash
supurr prices -a BTC                     # Fetch BTC prices (7 days)
supurr prices -a hyna:BTC --dex hyna     # HIP-3 prices
supurr prices -a HYPE -s 2026-01-28      # From specific date
```

| Option                 | Description                     |
| ---------------------- | ------------------------------- |
| `-a, --asset <symbol>` | **Required.** Asset symbol      |
| `--dex <dex>`          | DEX name (default: hyperliquid) |
| `-s, --start <date>`   | Start date                      |
| `-e, --end <date>`     | End date                        |
| `--no-cache`           | Disable caching                 |

---

## 12. `supurr update` — Self-Update

```bash
supurr update    # Check and install latest version
```

---

## Complete Workflows

### Workflow 1: Grid — Backtest → Deploy → Monitor

```bash
# 1. Initialize (first time only)
supurr init --address 0x... --api-wallet 0x...

# 2. Create config
supurr new grid --asset BTC --levels 4 --start-price 88000 --end-price 92000 --investment 100 --leverage 20 --output btc-grid.json

# 3. Backtest
supurr backtest -c btc-grid.json -s 2026-01-28 -e 2026-02-01

# 4. Deploy
supurr deploy -c btc-grid.json

# 5. Monitor
supurr monitor --watch

# 6. Stop when done
supurr stop --id <bot_id>
```

### Workflow 2: Arb — Setup → Deploy → Monitor

```bash
# 1. Initialize
supurr init --address 0x... --api-wallet 0x...

# 2. Generate arb config (auto-resolves spot counterpart)
supurr new arb --asset BTC --amount 200 --leverage 1 --output btc-arb.json

# 3. Review the generated config
supurr config btc-arb

# 4. Ensure USDC balance in BOTH Spot and Perps wallets on Hyperliquid

# 5. Deploy
supurr deploy -c btc-arb.json

# 6. Monitor
supurr monitor --watch
```

### Workflow 3: DCA — Configure → Deploy

```bash
# 1. Create DCA config
supurr new dca --asset BTC --trigger-price 95000 --base-order 0.001 --max-orders 5 --take-profit 0.02 --output btc-dca.json

# 2. Deploy
supurr deploy -c btc-dca.json

# 3. Monitor
supurr monitor --watch
```

### Workflow 4: Test All Market Types

```bash
# Native Perp
supurr new grid --asset BTC --output native-btc.json
supurr backtest -c native-btc.json -s 2026-01-28 -e 2026-02-01

# USDC Spot
supurr new grid --asset HYPE --type spot --quote USDC --output hype-usdc.json
supurr backtest -c hype-usdc.json -s 2026-01-30 -e 2026-01-31

# Non-USDC Spot
supurr new grid --asset HYPE --type spot --quote USDH --output hype-usdh.json
supurr backtest -c hype-usdh.json -s 2026-01-30 -e 2026-01-31

# HIP-3
supurr new grid --asset BTC --type hip3 --dex hyna --output hyna-btc.json
supurr backtest -c hyna-btc.json -s 2026-01-28 -e 2026-02-01
```

---

## Config Storage

```
~/.supurr/
├── credentials.json      # { address, private_key }
├── configs/              # Saved bot configs
│   ├── btc-grid.json
│   ├── hype-usdc.json
│   └── ...
└── cache/                # Price data cache
    └── hyperliquid/
        ├── BTC/
        └── HYPE/
```

---

## Instrument Meta — Tick & Lot Size Formulas

The CLI auto-computes `instrument_meta` from Hyperliquid's `szDecimals` (quantity precision). These are the **verified** formulas matching HL docs:

| Market Type | `tick_decimals` formula  | `MAX_DECIMALS` | Example (BTC, szDec=5)     | Example (HYPE spot, szDec=2)    |
| ----------- | ------------------------ | -------------- | -------------------------- | ------------------------------- |
| **Perp**    | `max(6 - szDecimals, 0)` | 6              | `tick_size: "0.1"` (1 dec) | —                               |
| **HIP-3**   | `max(6 - szDecimals, 0)` | 6              | `tick_size: "0.1"` (1 dec) | —                               |
| **Spot**    | `max(8 - szDecimals, 0)` | 8              | —                          | `tick_size: "0.000001"` (6 dec) |

**Derivations:**

```
tick_decimals = max(MAX_DECIMALS - szDecimals, 0)
tick_size     = 10^(-tick_decimals)     # e.g., 10^(-1) = 0.1
lot_size      = 10^(-szDecimals)         # e.g., 10^(-5) = 0.00001
min_qty       = lot_size
min_notional  = "10"                     # fixed for all markets
```

> [!CAUTION]
> Spot uses `MAX_DECIMALS = 8`, not 6. Using the wrong constant will cause order rejections on low-priced spot tokens (e.g., KNTQ where szDecimals=0 → tick_decimals should be 8, not 6).

---

## API Endpoints Used

| Purpose       | Endpoint                                      | Auth              |
| ------------- | --------------------------------------------- | ----------------- |
| Bot Deploy    | `POST /bots/create/<wallet>`                  | —                 |
| Active Bots   | `GET /dashboard/active_bots`                  | —                 |
| Bot History   | `GET /dashboard/user_bots/<address>` (Python) | —                 |
| Stop Bot      | `POST /bots/<bot_id>/stop` (Node)             | EIP-191 signature |
| Price Data    | `GET /prices?dex=X&asset=Y&start_time=Z`      | —                 |
| Price Archive | `GET /{dex}/{asset}/{date}.json`              | —                 |

---

## Troubleshooting

| Issue                     | Solution                                                         |
| ------------------------- | ---------------------------------------------------------------- |
| "Config not found"        | Use `supurr configs` to list available configs                   |
| "No credentials"          | Run `supurr init` first                                          |
| "0 prices fetched"        | Check date range (data from 2026-01-28+)                         |
| "API wallet not valid"    | Register API wallet on Hyperliquid first                         |
| HIP-3 backtest fails      | Use format `--dex hyna --asset BTC`                              |
| "No spot market found"    | Asset has no spot counterpart — arb not available for this asset |
| Arb asset starts with `U` | Use the perp name (e.g., `BTC` not `UBTC`) — CLI adds `U` prefix |

---

# Appendix: Hyperliquid Info API

> **Backtesting note**: This appendix is for live metadata and user state lookups. It is **not** a source of tick-level historical data for `supurr backtest`.

> **Get address via**: `supurr whoami` — returns the configured wallet address.

All endpoints use `POST https://api.hyperliquid.xyz/info` with `Content-Type: application/json`.

## Market Data (No Address Required)

| Query            | Request Body                         |
| ---------------- | ------------------------------------ |
| All Mid Prices   | `{"type": "allMids"}`                |
| Sub-DEX Prices   | `{"type": "allMids", "dex": "hyna"}` |
| Perp Metadata    | `{"type": "metaAndAssetCtxs"}`       |
| Spot Metadata    | `{"type": "spotMeta"}`               |
| L2 Order Book    | `{"type": "l2Book", "coin": "BTC"}`  |
| List HIP-3 DEXes | `{"type": "perpDexs"}`               |

## User Data (Address Required)

| Query           | Request Body                                                                   |
| --------------- | ------------------------------------------------------------------------------ |
| Perp Positions  | `{"type": "clearinghouseState", "user": "0x..."}`                              |
| Spot Balances   | `{"type": "spotClearinghouseState", "user": "0x..."}`                          |
| Open Orders     | `{"type": "openOrders", "user": "0x..."}`                                      |
| Order History   | `{"type": "historicalOrders", "user": "0x..."}`                                |
| Trade Fills     | `{"type": "userFills", "user": "0x...", "aggregateByTime": true}`              |
| Funding History | `{"type": "userFunding", "user": "0x...", "startTime": <ts>, "endTime": <ts>}` |
| Sub-Accounts    | `{"type": "subAccounts", "user": "0x..."}`                                     |
| Vault Details   | `{"type": "vaultDetails", "vaultAddress": "0x..."}`                            |

## HIP-3 Sub-DEXes

| DEX    | Quote | Assets                        |
| ------ | ----- | ----------------------------- |
| `hyna` | USDE  | Crypto perps (BTC, ETH, HYPE) |
| `xyz`  | USDE  | Stocks (AAPL, TSLA, NVDA)     |
| `vntl` | USDE  | AI/tech tokens                |
| `km`   | USDT  | Kinetiq Markets               |
| `cash` | USDC  | Tech stocks                   |

## TypeScript Helper

```typescript
const HL = "https://api.hyperliquid.xyz/info";

async function query<T>(body: object): Promise<T> {
  const res = await fetch(HL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

// Examples
const mids = await query({ type: "allMids" });
const positions = await query({ type: "clearinghouseState", user: "0x..." });
const spotBal = await query({ type: "spotClearinghouseState", user: "0x..." });
const dexes = await query({ type: "perpDexs" });
```

## Common Hazards

| Issue                   | Solution                                                                          |
| ----------------------- | --------------------------------------------------------------------------------- |
| `szDecimals` truncation | **Truncate** (floor) qty to `szDecimals` before submit — never round up           |
| Spot tick_size ≠ perp   | Spot uses `MAX_DECIMALS=8`, perp/HIP-3 uses `6` — don't mix formulas              |
| HIP-3 price prefix      | Sub-DEX prices keyed as `hyna:BTC`, not `BTC`                                     |
| Sub-DEX asset index     | Use local index from DEX's `universe`, not global                                 |
| Fill limits             | `userFills` max 2000 — paginate with time ranges                                  |
| Slider/input precision  | Always floor (truncate) trade sizes, never round — rounding up can exceed balance |

---

## Tutorials

Step-by-step deployment guides with parameter selection advice and practical tips:

- [Grid Bot Tutorial](tutorials/grid.md) — Range trading with buy/sell grids
- [Arb Bot Tutorial](tutorials/arb.md) — Market-neutral spot-perp arbitrage
- [DCA Bot Tutorial](tutorials/dca.md) — Dollar-cost averaging with auto-restart
