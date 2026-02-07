---
name: fivem-development
description: Develops resources for FiveM using vRP Creative Network with Lua. Covers resource creation, Proxy/Tunnel system, inventory, money, groups, identity, NUI, database (oxmysql), security, and performance. Use when the user works with FiveM, vRP, Lua scripts for GTA V servers, or mentions resources, client/server scripts, natives, NUI, or any system of the vRP Creative Network framework.
---

# FiveM Development — vRP

## Framework Architecture

vRP Creative Network is based on **Lua 5.4** with communication via **Proxy** (server-to-server) and **Tunnel** (client-server).

## FiveM Natives — Official Source

Official source for natives:

- Docs: https://docs.fivem.net/natives/
- Official Repository (mirror): https://github.com/proelias7/fivem-natives

## Support for Creative v5 and vRPEX (older variations)

Older versions maintain the same logic and best practices but change function and file names.

- **Creative v5:** core in `camelCase`, `modules/group.lua`, configs in `config/*.lua`.
- **vRPEX:** classic core (`getUserId`, `getUserSource`, `getUsers`, etc.) and configs in `cfg/*.lua`.

See the full mapping in [reference.md](reference.md).

### Key Concepts

| Concept | Description |
|---|---|
| **Passport** | Unique character ID (equivalent to `user_id` in other vRPs) |
| **Source** | Player connection ID on the server (changes on every reconnection) |
| **Datatable** | In-memory table with character data (inventory, position, skin, etc.) |
| **Characters** | Global server-side table indexed by `source` with character data |
| **Sources** | Global table `Sources[Passport] = source` for reverse lookup |

### Identification Flow

```lua
-- Server-side: get Passport from source
local Passport = vRP.Passport(source)

-- Server-side: get source from Passport
local source = vRP.Source(Passport)

-- Server-side: get character Datatable
local Datatable = vRP.Datatable(Passport)

-- Server-side: get inventory
local Inventory = vRP.Inventory(Passport)
```

### Proxy/Tunnel System

```lua
-- In any SERVER-SIDE resource, get access to vRP:
local Proxy = module("vrp", "lib/Proxy")
vRP = Proxy.getInterface("vRP")

-- In any CLIENT-SIDE resource:
local Tunnel = module("vrp", "lib/Tunnel")
local Proxy = module("vrp", "lib/Proxy")
vRPS = Tunnel.getInterface("vRP")  -- call server functions

-- Expose your resource functions (server):
myResource = {}
Proxy.addInterface("myResource", myResource)
Tunnel.bindInterface("myResource", myResource)
```

### Fire-and-forget Rule

Prefix Tunnel calls with `_` to not wait for a response:

```lua
-- Await response (blocking)
local result = vRP.Generateitem(Passport,"water",1)

-- Fire-and-forget (non-blocking)
vRP._Generateitem(Passport,"water",1)
```

## Main API (Server-side)

### Player/Identity

| Function | Parameters | Return | Description |
|--------|------------|---------|-----------|
| `vRP.Passport(source)` | source | Passport\|false | Gets player Passport |
| `vRP.Source(Passport)` | Passport | source\|nil | Gets source from Passport |
| `vRP.Datatable(Passport)` | Passport | table\|false | Character in-memory data |
| `vRP.Inventory(Passport)` | Passport | table | Character inventory |
| `vRP.Identity(Passport)` | Passport | table\|false | Character data (name, name2, bank, phone, etc.) |
| `vRP.FullName(source)` | source | string\|false | Character full name |
| `vRP.Players()` | — | table | Returns `Sources` (Passport→source) |
| `vRP.Kick(source, Reason)` | source, string | — | Kicks the player |
| `vRP.Teleport(source, x, y, z)` | source, coords | — | Teleports the player |
| `vRP.GetEntityCoords(source)` | source | vector3 | Player coordinates |
| `vRP.ModelPlayer(source)` | source | string | Ped model (mp_m/mp_f) |

### Money

| Function | Parameters | Return | Description |
|--------|------------|---------|-----------|
| `vRP.GetBank(source)` | source | number | Bank balance |
| `vRP.GiveBank(Passport, Amount)` | Passport, number | — | Adds money to bank |
| `vRP.RemoveBank(Passport, Amount)` | Passport, number | — | Removes money from bank |
| `vRP.PaymentBank(Passport, Amount)` | Passport, number | bool | Pays with bank (checks balance) |
| `vRP.PaymentMoney(Passport, Amount)` | Passport, number | bool | Pays with cash |
| `vRP.PaymentFull(Passport, Amount)` | Passport, number | bool | Tries cash, then bank |
| `vRP.PaymentDirty(Passport, Amount)` | Passport, number | bool | Pays with dirty money |
| `vRP.WithdrawCash(Passport, Amount)` | Passport, number | bool | Bank withdrawal |
| `vRP.PaymentGems(Passport, Amount)` | Passport, number | bool | Pays with gems |
| `vRP.GetCoins(Passport)` | Passport | number | Gets coins |
| `vRP.AddCoins(Passport, Amount)` | Passport, number | bool | Adds coins |
| `vRP.RemCoins(Passport, Amount)` | Passport, number | bool | Removes coins |

### Inventory

| Function | Parameters | Return | Description |
|--------|------------|---------|-----------|
| `vRP.GiveItem(Passport, Item, Amount, Notify, Slot)` | ... | — | Gives item (no durability) |
| `vRP.GenerateItem(Passport, Item, Amount, Notify, Slot)` | ... | — | Gives item (with durability/charges) |
| `vRP.TakeItem(Passport, Item, Amount, Notify, Slot)` | ... | bool | Removes item (returns success) |
| `vRP.RemoveItem(Passport, Item, Amount, Notify)` | ... | — | Removes item (no return) |
| `vRP.ItemAmount(Passport, Item)` | Passport, string | number | Item amount |
| `vRP.ConsultItem(Passport, Item, Amount)` | ... | bool | Checks if has amount |
| `vRP.InventoryWeight(Passport)` | Passport | number | Current weight |
| `vRP.GetWeight(Passport)` | Passport | number | Max weight |
| `vRP.SetWeight(Passport, Amount)` | Passport, number | — | Adds to max weight |
| `vRP.MaxItens(Passport, Item, Amount)` | ... | bool | Checks item max limit |
| `vRP.ClearInventory(Passport)` | Passport | — | Clears inventory |

### Groups/Permissions

| Function | Parameters | Return | Description |
|--------|------------|---------|-----------|
| `vRP.HasPermission(Passport, Permission, Level)` | ... | bool | Checks direct permission |
| `vRP.HasGroup(Passport, Permission, Level)` | ... | bool | Checks group (includes parents) |
| `vRP.HasService(Passport, Permission)` | ... | bool | Checks if in service |
| `vRP.SetPermission(Passport, Permission, Level, Mode)` | ... | — | Sets permission |
| `vRP.RemovePermission(Passport, Permission)` | ... | — | Removes permission |
| `vRP.ServiceToggle(Source, Passport, Permission, Silenced)` | ... | — | Toggles service |
| `vRP.NumPermission(Permission, Level)` | ... | table, number | Players in service |
| `vRP.CheckGroup(Passport, Type)` | ... | bool | Checks group by type |
| `vRP.HasAction(Passport)` | Passport | bool | Checks police action |
| `vRP.SetAction(Passport, Status)` | ... | — | Sets action status |

### Survival

| Function | Parameters | Description |
|--------|------------|-----------|
| `vRP.UpgradeHunger(Passport, Amount)` | ... | Increases hunger |
| `vRP.DowngradeHunger(Passport, Amount)` | ... | Decreases hunger |
| `vRP.UpgradeThirst(Passport, Amount)` | ... | Increases thirst |
| `vRP.DowngradeThirst(Passport, Amount)` | ... | Decreases thirst |
| `vRP.UpgradeInfection(Passport, Amount)` | ... | Increases infection |
| `vRP.DowngradeInfection(Passport, Amount)` | ... | Decreases infection |
| `vRP.Revive(source, Health)` | ... | Revives player |

### Database

```lua
-- Register prepared query
vRP.Prepare("name/query", "SELECT * FROM table WHERE id = @id")

-- Execute query
local result = vRP.Query("name/query", { id = 123 })
```

Uses **oxmysql** internally. Parameters with `@name`.

### Persistent Data

```lua
-- Server Data (entitydata — global data)
local data = vRP.GetSrvData("UniqueKey")
vRP.SetSrvData("UniqueKey", { field = "value" })

-- Player Data (playerdata — data per player)
local data = vRP.UserData(Passport, "key")
vRP.setUData(Passport, "key", json.encode(data))
```

### Global Utilities

| Function | Description |
|--------|-----------|
| `parseInt(value)` | Converts to integer (min. 0) |
| `parseFormat(value)` | Formats number with thousand separator |
| `splitString(str, symbol)` | Splits string by separator |
| `SplitOne(name)` | First element of split |
| `sanitizeString(str, chars, allow)` | Filters characters |
| `CompleteTimers(seconds)` | Formats full time in HTML |
| `MinimalTimers(seconds)` | Formats summarized time |
| `CountTable(table)` | Counts items in table |
| `async(func)` | Executes asynchronous function |

## Client-Server Communication

### Notification Events

```lua
-- Server-side: simple notification
TriggerClientEvent("Notify", source, "success", "Message.", false, 5000)
-- Types: "success", "important", "negado" (denied)

-- Server-side: item notification
TriggerClientEvent("NotifyItens", source, { "+", "itemIndex", "amount", "Item Name" })
-- "+" for gain, "-" for loss
```

### Important Events

| Event | Side | Description |
|--------|------|-----------|
| `"Connect"` | Server | Player chose character `(Passport, Source)` |
| `"Disconnect"` | Server | Player disconnected `(Passport, Source)` |
| `"CharacterChosen"` | Server | Character chosen `(Passport, source)` |
| `"vRP:Active"` | Client | Player activated `(source, Passport, Name)` |

## Critical Performance Rules (Summary)

ALWAYS follow these rules when writing code:

1. **Tunnel vs Event:** Use `TriggerServerEvent`/`TriggerClientEvent` when you do NOT need a return. Use Tunnel only when you NEED a return.
2. **Dynamic Sleep:** NEVER fixed `Wait(0)`. Adjust based on state (dist < 20 = `0`, dist < 50 = `500`, else = `1000`+).
3. **Calls in same environment:** Call functions directly. NEVER use `TriggerEvent()` to call on the same side.
4. **No remote calls in loops:** Do not use Tunnel/Events in loops < 5 seconds. Prefer batch or delta.
5. **Small Payloads:** Send only the change, not full data. Limit of ~8KB per event.
6. **Cache:** Use `exports.cacheaside:Get()` for repeated database queries. Never query the database in a loop.
7. **SafeEvent (server):** Every event that gives money/item/advantage MUST pass through `exports["cerberus"]:SafeEvent(source, "eventName", { time = N })`.
8. **SetCooldown (client):** Repetitive actions on client (open menu, use item) must use `exports["cerberus"]:SetCooldown("name", ms)`.
9. **Tables > if/else:** For 3+ conditions, use lookup table (O(1)) instead of if/elseif chains.
10. **Protect nil:** Always check variables before concatenating. Use `or ""` as fallback.

## UI Construction (React + Vite)

Stack: React 18 + TypeScript + Vite + Tailwind CSS + Zustand.

**Fundamental Rules:**
- `base: "./"` in vite.config.ts (MANDATORY for FiveM)
- Use `rem` for ALL sizes — NEVER `px` for layout
- Media queries in `html` font-size to scale with player resolution
- **Tailwind v4 uses OKLCH** and FiveM CEF does not support it. **Use Tailwind v3.4.17**.
- FORBIDDEN: `backdrop-filter: blur()`, `filter: blur()`, `filter: drop-shadow()` — cause FPS drop
- FORBIDDEN: framer-motion, GSAP, react-spring — heavy animation libs
- Use pure CSS transitions/keyframes for animations
- Independent modules (Notify, Progress) outside VisibilityProvider
- Main interface inside VisibilityProvider with NuiFocus
- Global `overflow: hidden` and `user-select: none`
- `isEnvBrowser()` for data mocking in dev
- Communication: `observe()` to listen to NUI, `Post.create()` to send callbacks

For complete UI guide: [ui-guide.md](ui-guide.md)

## Additional References

- For UI construction guide (React + Vite + FiveM): [ui-guide.md](ui-guide.md)
- For detailed best practices (performance, security, cache): [best-practices.md](best-practices.md)
- For complete and detailed API: [reference.md](reference.md)
- For code examples: [examples.md](examples.md)
- For resource templates: [templates.md](templates.md)
- For patterns and conventions: [patterns.md](patterns.md)

## External Resources (Download)

Use these official repositories when the project mentions dependencies:

- `cacheaside` (in-memory cache): `git@github.com:proelias7/cacheaside.git`
- `cerberus` (anti-exploit + cooldowns): `git@github.com:proelias7/cerberus.git`

## vRPex Compatibility

The vRP Creative Network has compatibility aliases with classic vRP:

| vRPex (old) | Creative Network (current) |
|----------------|--------------------------|
| `getUserId` | `Passport` |
| `getUserSource` | `Source` |
| `getUserIdentity` | `Identity` |
| `getUserDataTable` | `Datatable` |
| `hasGroup` | `HasGroup` |
| `hasPermission` | `HasPermission` |
| `giveInventoryItem` | `GiveItem` |
| `tryGetInventoryItem` | `TakeItem` |
| `getInventoryItemAmount` | `ItemAmount` |
| `giveMoney` | `GiveBank` |
| `tryFullPayment` | `PaymentFull` |
| `getBankMoney` | `GetBank` |
| `query` / `execute` | `Query` |
| `prepare` | `Prepare` |

**ALWAYS use the native Creative Network names** (right column), not the aliases.
