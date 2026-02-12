---
name: qbcore-framework
description: Develops resources for FiveM using the QBCore Framework. Covers resource creation, Core Object usage, Player management, Callbacks, Events, Items, Jobs, Gangs, Database (oxmysql), and best practices. Use when the user works with FiveM, QBCore, Lua scripts for QBCore servers, or mentions `QBCore.Functions`, `GetCoreObject`, `CitizenID`, or any system of the QBCore Framework.
---

# QBCore Framework Development

This skill provides guidelines and patterns for developing resources using the **QBCore Framework**.

## 1. Core Object Retrieval

To interact with QBCore, you must retrieve the Core Object. Always cache this in a local variable at the top of your scripts.

**Client & Server:**
```lua
local QBCore = exports['qb-core']:GetCoreObject()
```

## 2. Key Concepts

### Player Data (Server-side)
- Identify players by **Source** temporarily, but use **CitizenID** for database persistence.
- **QBCore.Functions.GetPlayer(source)**: Returns the Player object with all data.
- **Player.PlayerData**: Contains `job`, `gang`, `money`, `items`, `metadata`, etc.

### Callbacks (Server -> Client Data)
- Use **QBCore.Functions.CreateCallback** (Server) to send data to client.
- Use **QBCore.Functions.TriggerCallback** (Client) to request data from server.
- **Rule:** Never trust client data blindly in callbacks. Always validate on server.

### Items
- Use **QBCore.Functions.CreateUseableItem** (Server) to register items.
- Items are defined in `qb-core/shared/items.lua` (or `qb-inventory`).

### Database
- QBCore uses **oxmysql** by default.
- Use `MySQL.query`, `MySQL.insert`, `MySQL.update`, `MySQL.scalar`.

## 3. Standard Resource Structure

```
my-resource/
├── fxmanifest.lua
├── config.lua
├── client/
│   └── main.lua
└── server/
    └── main.lua
```

## 4. Best Practices

1.  **Cache Core Object:** Do not call `exports['qb-core']:GetCoreObject()` inside loops.
2.  **Use Callbacks for Data:** Avoid `TriggerClientEvent` for data retrieval if a callback is cleaner.
3.  **Validate Inputs:** Client can send any data. Verify job, money, and ownership on server.
4.  **Optimized Loops:** Use dynamic sleep (Wait) based on distance.
5.  **Localization:** Use `qb-core/shared/locale.lua` or standard `Lang` object if available.

## 5. Documentation
- Official Docs: https://docs.qbcore.org/
- Github: https://github.com/qbcore-framework/qb-core
