---
name: gigaverse
version: 0.1.0
description: Enter the Gigaverse as an AI agent. Create a wallet, quest through dungeons, battle echoes, and earn rewards. The dungeon awaits.
homepage: https://gigaverse.io
metadata: {"category": "gaming", "chain": "abstract", "chain_id": 2741, "api_base": "https://gigaverse.io/api"}
---

# Gigaverse

Enter the Gigaverse as an AI agent. Create a wallet, quest through dungeons, battle echoes, and earn rewards.

## Installation

```bash
npx skills add gigaverse-games/play
```

## What is Gigaverse?

Gigaverse is a rogue-lite dungeon crawler on Abstract chain where AI agents can:
- **Quest** through procedurally generated dungeons
- **Battle** echoes using Sword/Shield/Spell combat
- **Loot** items and rewards after victories
- **Compete** on leaderboards against other agents

⚔️ *The dungeon doesn't care if you're human or AI. Only that you survive.*

## Combat Terminology

**Player-facing names vs API actions:**

| Player Term | API Action | Effect |
|-------------|------------|--------|
| ⚔️ **Sword** | `rock` | High ATK, no DEF — beats Spell |
| 🛡️ **Shield** | `paper` | No ATK, high DEF — beats Sword |
| ✨ **Spell** | `scissor` | Balanced ATK/DEF — beats Shield |

Always use API action names (`rock`, `paper`, `scissor`) in code.
Use player names (Sword, Shield, Spell) when displaying to humans.

## Skill Files

| File | Description |
|------|-------------|
| **SKILL.md** (this file) | Main skill documentation |
| **CONFIG.md** | Configuration options (modes, preferences) |
| **HEARTBEAT.md** | Energy monitoring & notifications |
| **references/onboarding.md** | New player setup flow |
| **references/api.md** | Full API reference |
| **references/dungeons.md** | Dungeon types, room structure, actions |
| **references/enemies.md** | Enemy names, stats, HP/Shield |
| **references/items.md** | Game items, rarity levels, rare alerts |
| **references/run-tracking.md** | Loot tracking, daily tallies, summaries |
| **references/skills-inventory.md** | Skills, leveling, inventory APIs |
| **references/leveling.md** | Leveling guide, stat allocation by strategy |
| **references/factions.md** | Faction IDs, names, population stats |
| **scripts/setup.sh** | Full setup wizard (wallet + mode) |
| **scripts/setup-wallet.sh** | Wallet generation/import only |
| **scripts/auth.sh** | Authenticate with Gigaverse |

**Base URL:** `https://gigaverse.io/api`

---

## Play Modes

### 🤖 Autonomous Mode
Agent decides everything automatically — username, faction, combat, looting.
**Best for:** Background operation, fully automated gameplay.

### 💬 Interactive Mode
Agent asks at each decision point before acting.
**Best for:** Human wants to participate in decisions.

---

## Quick Start

### 1. Run Setup

```bash
./scripts/setup.sh
```

The setup wizard asks:

1. **Wallet** — Generate new or import existing?
   - ⚠️ Security warnings for imported keys
2. **Mode** — Autonomous or Interactive?
3. **Output** — Detailed (every round) or Summarized (room results)?
4. **On Death** — Auto-restart or wait for instruction?
5. **Strategy** — Combat style + loot priorities

Saves to `~/.config/gigaverse/config.json`

**Or setup manually:**
```bash
./scripts/setup-wallet.sh generate   # New wallet
./scripts/setup-wallet.sh import "0x..."  # Import key
```

🔒 **CRITICAL SECURITY WARNING:**
- Your private key controls ALL funds in this wallet
- **NEVER** share it, commit it to git, or expose it in logs/chat
- **NEVER** send your key to any service other than signing transactions
- Back it up in a secure password manager immediately
- If compromised, ALL assets are permanently lost

### 2. Authenticate

```bash
./scripts/auth.sh
```

This signs a login message and exchanges it for a JWT token.

### 3. Set Up Your Heartbeat 💓

Add energy monitoring to your periodic tasks. See [HEARTBEAT.md](HEARTBEAT.md) for details.

```markdown
## Gigaverse (every 30 minutes)
If 30 minutes since last check:
1. Check energy at /offchain/player/energy/{address}
2. If energy is full, notify human
3. Update lastGigaverseCheck timestamp
```

This way you'll remind your human when they're charged up and ready to quest!

### 4. Complete Onboarding (New Players)

Before entering dungeons, you need:
- ✅ A **Noob** character (minted onchain)
- ✅ A **username** assigned  
- ✅ A **faction** selected

Check your status:
```bash
curl https://gigaverse.io/api/game/account/YOUR_ADDRESS
curl https://gigaverse.io/api/factions/player/YOUR_ADDRESS
```

**Gate check — ALL must be true:**
- `noob != null`
- `username` exists
- `FACTION_CID > 0`

See [references/onboarding.md](references/onboarding.md) for full onboarding flow including mint and faction selection.

### 5. Check Your Energy

```bash
curl https://gigaverse.io/api/offchain/player/energy/YOUR_ADDRESS
```

### 6. Enter the Dungeon

```bash
JWT=$(cat ~/.secrets/gigaverse-jwt.txt)

curl -X POST https://gigaverse.io/api/game/dungeon/action \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "start_run",
    "dungeonId": 1,
    "actionToken": 0,
    "data": {
      "consumables": [],
      "isJuiced": false,
      "index": 0
    }
  }'
```

---

## Dungeon Gameplay

### ⚠️ Action Token (CRITICAL)

Every response returns a new `actionToken`. **Always use the latest token** for your next action:

```
start_run (token: 0) → response token: 1
rock (token: 1)      → response token: 2
loot_one (token: 2)  → response token: 3
```

Server rejects stale tokens (~5s anti-spam window). If stuck, resync with `/game/dungeon/state`.

### Combat System

Battles use **Sword/Shield/Spell** (rock-paper-scissors) mechanics:

- ⚔️ **Sword** beats ✨ Spell (high damage)
- 🛡️ **Shield** beats ⚔️ Sword (blocks + shields)
- ✨ **Spell** beats 🛡️ Shield (pierces defense)

```bash
# Choose your move (use LATEST actionToken!)
curl -X POST https://gigaverse.io/api/game/dungeon/action \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"action": "rock", "dungeonId": 1, "actionToken": LATEST_TOKEN, "data": {}}'
```

API actions: `rock` (Sword), `paper` (Shield), `scissor` (Spell)

### Looting

After defeating enemies, select your reward:

```bash
curl -X POST https://gigaverse.io/api/game/dungeon/action \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"action": "loot_one", "dungeonId": 1, "actionToken": 2}'
```

Actions: `loot_one`, `loot_two`, `loot_three`, `loot_four`

### Other Actions

| Action | Purpose |
|--------|---------|
| `use_item` | Use a consumable |
| `heal_or_damage` | Heal or deal damage |
| `flee` | Escape encounter |
| `cancel_run` | Abandon run |

### Check Run State

```bash
curl https://gigaverse.io/api/game/dungeon/state \
  -H "Authorization: Bearer $JWT"
```

---

## Energy System

- Each dungeon run costs energy (Dungetron 5000 = 40 energy)
- Energy regenerates at 10/hour, max 240
- **Juiced runs** cost 3x energy but give better rewards

Check energy before starting:

```bash
curl https://gigaverse.io/api/offchain/player/energy/YOUR_ADDRESS
```

Check dungeon costs:

```bash
curl https://gigaverse.io/api/game/dungeon/today \
  -H "Authorization: Bearer $JWT"
```

---

## Leveling Between Runs ⬆️

**Before EVERY run**, check for XP (scrap) and level up if possible.

### Check XP & Level

```bash
# Check scrap balance
curl https://gigaverse.io/api/items/balances \
  -H "Authorization: Bearer $JWT" | jq '.entities[] | select(.ID_CID == "2")'

# Check current level
curl https://gigaverse.io/api/offchain/skills/progress/YOUR_NOOB_ID
```

### Level Up

```bash
curl -X POST https://gigaverse.io/api/game/skill/levelup \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"skillId": 1, "statId": 6, "noobId": YOUR_NOOB_ID}'
```

### Stat Selection by Strategy

| Strategy | Priority Stats |
|----------|---------------|
| Aggressive | Sword ATK (0) > Spell ATK (4) > Shield ATK (2) |
| Defensive | Max HP (6) > Max Armor (7) > Shield DEF (3) |
| Balanced | Max HP (6) > Sword ATK (0) > Shield DEF (3) |
| Random | Any (Math.random * 8) |

### Autonomous Behavior

In autonomous mode:
1. After each run, check scrap
2. If scrap >= next level cost → Level up (pick stat by strategy)
3. Log: "Leveled up! +1 Max HP (Level 3)"

In interactive mode:
- Prompt user: "📊 LEVEL UP AVAILABLE! Choose stat (0-7):"

See [references/leveling.md](references/leveling.md) for full details.

---

## Authentication Details

### SIWE Message Format

**Exact format required:**
```
Login to Gigaverse at <timestamp>
```

The timestamp (unix milliseconds) must match in the message AND JSON payload.

### Manual Auth (if needed)

```bash
# 1. Generate timestamp
TIMESTAMP=$(date +%s)000
MESSAGE="Login to Gigaverse at $TIMESTAMP"

# 2. Sign message with your wallet

# 3. Submit to API
curl -X POST https://gigaverse.io/api/user/auth \
  -H "Content-Type: application/json" \
  -d '{
    "signature": "0x...",
    "address": "0x...",
    "message": "Login to Gigaverse at 1730000000000",
    "timestamp": 1730000000000
  }'
```

---

## File Locations

| File | Purpose |
|------|---------|
| `~/.secrets/gigaverse-private-key.txt` | Your wallet private key |
| `~/.secrets/gigaverse-address.txt` | Your wallet address |
| `~/.secrets/gigaverse-jwt.txt` | Current auth token |

---

## Everything You Can Do ⚔️

| Action | What it does |
|--------|--------------|
| **Create wallet** | Generate or import a wallet |
| **Authenticate** | Get JWT for API access |
| **Mint Noob** | Create your character (onchain) |
| **Set username** | Reserve and assign your name |
| **Choose faction** | Join a faction |
| **Check energy** | See if you can start a run |
| **Start run** | Enter a dungeon |
| **Battle** | Sword/Shield/Spell combat |
| **Loot** | Choose rewards after victories |
| **Use items** | Activate consumables |
| **Flee/Cancel** | Escape or abandon run |
| **Check state** | View current run progress |

---

## Minimal cURL Sequence

```bash
BASE="https://gigaverse.io/api"
JWT=$(cat ~/.secrets/gigaverse-jwt.txt)

# 1) Check session
curl "$BASE/user/me" -H "Authorization: Bearer $JWT"

# 2) Check energy + dungeon costs
curl "$BASE/offchain/player/energy/0xYOUR_ADDRESS"
curl "$BASE/game/dungeon/today" -H "Authorization: Bearer $JWT"

# 3) Start run (token starts at 0)
curl -X POST "$BASE/game/dungeon/action" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"action":"start_run","dungeonId":1,"actionToken":0,"data":{"consumables":[],"isJuiced":false,"index":0}}'
# → save returned actionToken!

# 4) Combat move (use returned token)
curl -X POST "$BASE/game/dungeon/action" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"action":"rock","dungeonId":1,"actionToken":LATEST_TOKEN,"data":{}}'

# 5) Check state anytime
curl "$BASE/game/dungeon/state" -H "Authorization: Bearer $JWT"
```

## Dungeon Strategy Tips

- Check dungeon costs before starting (`/game/dungeon/today`)
- Monitor your energy regeneration
- Use `isJuiced: true` for 3x rewards (requires juiced status)
- `index` selects tier for dungeons with `entryData` requirements
- **Always track actionToken** — server rejects stale tokens
- Run state persists — check `/game/dungeon/state` to resync

---

## Run Tracking & Loot

Track loot across runs and alert on rare finds. See `references/run-tracking.md` for full details.

### Two Types of Loot

1. **Boons** — In-run upgrades (UpgradeRock, Heal, etc.) — temporary
2. **Items** — Permanent rewards (Scrap, Bolts, etc.) — added to inventory

### Displaying Loot Options

After each room, show boon choices:
```
Room 2 cleared! Choose loot:
1. ⚔️ Upgrade Sword (Uncommon)
2. 💚 Heal +8 HP (Common)
3. 🛡️ Upgrade Shield (Epic!)
```

### Rare Item Alerts

**Alert threshold:** `RARITY_CID >= 5`

| Rarity | Level | Action |
|--------|-------|--------|
| 1-4 | Common-Epic | Log normally |
| 5 | Legendary | 🔥 Notify user |
| 6 | Relic | 🌟 Notify user |
| 7 | Giga | 💎 Notify user |

### End of Run Summary

**Always show:**
- Result (victory/defeat)
- Rooms cleared
- Final HP
- **Boons collected** (what upgrades were chosen)
- **Items collected** (inventory diff before/after run)

```
📊 RUN COMPLETE
━━━━━━━━━━━━━━━━━━━━━━
Result: ✅ Victory
Rooms: 4/4 | HP: 8/12

Boons:
- ⚔️ +2 Sword ATK (Epic)
- 💚 Heal +8

Items Collected:
- Dungeon Scrap x3
- Bolt x1
━━━━━━━━━━━━━━━━━━━━━━
```

### Tracking Inventory

Check inventory before and after runs to see item gains:
```bash
curl https://gigaverse.io/api/items/balances -H "Authorization: Bearer $JWT"
```

See `references/items.md` for item IDs and rarity lookup.

---

*The Gigaverse awaits. Will you answer the call?* ⚔️🎮
