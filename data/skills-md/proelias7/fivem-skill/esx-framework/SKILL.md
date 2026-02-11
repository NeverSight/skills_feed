---
name: esx-framework
description: Develops resources for FiveM using the ESX Framework (Legacy). Covers resource creation, Core Object (ESX), xPlayer functions, Events, Callbacks, Items, Jobs, Database (oxmysql), and best practices. Use when the user works with FiveM, ESX, ESX Legacy, or mentions `ESX.GetCoreObject`, `xPlayer`, `ESX.GetPlayerFromId`, or `esx:`.
---

# ESX Framework Development

This skill provides guidelines and patterns for developing resources using the **ESX Framework (Legacy)**.

## 1. Core Object Retrieval

**ESX Legacy (New Way):**
```lua
local ESX = exports["es_extended"]:getSharedObject()
```

**Legacy / Backwards Compatible:**
```lua
local ESX = nil
TriggerEvent('esx:getSharedObject', function(obj) ESX = obj end)
```

## 2. Key Concepts

### Player Data (Server-side)
- **xPlayer**: The main object for player interaction server-side.
- **ESX.GetPlayerFromId(source)**: Retrieves the xPlayer object.
- **xPlayer Methods**: `xPlayer.addMoney`, `xPlayer.setJob`, `xPlayer.addInventoryItem`.

### Callbacks (Server -> Client Data)
- **ESX.RegisterServerCallback** (Server): Respond to client requests.
- **ESX.TriggerServerCallback** (Client): Request data from server.

### Items & Database
- Items are defined in the database (`items` table) or `ox_inventory`.
- Database typically uses **oxmysql**.

## 3. Standard Resource Structure

```
my-resource/
├── fxmanifest.lua
├── config.lua
├── client/
│   └── main.lua
├── server/
│   └── main.lua
└── locales/
    └── en.lua
```

## 4. Best Practices

1.  **Use New Exports**: Prefer `exports["es_extended"]:getSharedObject()` over the event trigger.
2.  **Validate xPlayer**: Always check `if xPlayer then` before using it.
3.  **Secure Events**: Use `ESX.SecureNetEvent` (if available) or manual checks.
4.  **OneSync**: Develop with OneSync Infinity in mind (server-side entity creation).

## 5. Documentation
- Official Docs: https://documentation.esx-framework.org/
- Github: https://github.com/esx-framework/esx_core
