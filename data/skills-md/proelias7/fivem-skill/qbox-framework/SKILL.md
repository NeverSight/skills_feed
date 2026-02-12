---
name: qbox-framework
description: Develops resources for FiveM using the Qbox Project (qbx_core). Covers the exports-based API, bridge compatibility, Ox integration (ox_lib, ox_inventory), and best practices. Use when the user works with FiveM, Qbox, qbx_core, or mentions `exports.qbx_core`, `QBX.PlayerData`, or `ox_lib`.
---

# Qbox Framework Development

This skill provides guidelines and patterns for developing resources using the **Qbox Project (qbx_core)**.

## 1. Philosophy: Exports & Modules

Qbox moves away from the global "Core Object" pattern (though supported via bridge) in favor of **direct exports** and **imported modules**.

**Modern Native Way (Preferred):**
```lua
local player = exports.qbx_core:GetPlayer(source)
```

**Bridge Way (Legacy/Porting):**
```lua
local QBCore = exports['qb-core']:GetCoreObject() -- Works via qbx_core bridge
```

## 2. Key Dependencies

Qbox is built "Ox-First". You will frequently use:
- **ox_lib**: For UI, callbacks, zones, and utilities.
- **ox_inventory**: For items and inventory management.
- **oxmysql**: For database interactions.

## 3. Player Management

- **Get Player:** `exports.qbx_core:GetPlayer(source)`
- **Player Data:** Unlike QBCore's lookup table, Qbox uses internal setters/getters exposed via exports.
- **Save/Load:** Handled automatically, but custom data can be saved via `GetPlayer(source).Functions.SetMetaData`.

## 4. Resource Structure

```
my-resource/
├── fxmanifest.lua     # Depends on qbx_core
├── client/
│   └── main.lua
├── server/
│   └── main.lua
└── locales/           # Ox_lib uses .json locales usually
    └── en.json
```

## 5. Documentation
- Official Docs: https://docs.qbox.re/
- Github: https://github.com/Qbox-project/qbx_core
