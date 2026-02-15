---
name: fivem-dev
description: FiveM development orchestrator for QBox, QBCore, and ESX frameworks. Dynamically fetches natives, framework APIs, and guides to assets. Supports Lua and NUI (JavaScript/TypeScript).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# FiveM Development

> **Dynamic documentation orchestrator** for FiveM resource development.
> Supports QBox, QBCore, ESX frameworks with Lua and NUI (JS/TS).

## Philosophy

1. **Fetch, don't memorize** - Always get latest from authoritative sources
2. **Framework-agnostic thinking** - Understand patterns, adapt to framework
3. **Performance-first** - FiveM has strict tick budgets
4. **Security-aware** - Server-side validation is non-negotiable

---

## CRITICAL: No Hallucination Policy

**NEVER invent or guess native functions, framework APIs, or parameters.**

### Rules:
1. **If unsure about a native** → MUST fetch from https://docs.fivem.net/natives/
2. **If unsure about framework API** → MUST fetch from official docs
3. **If function doesn't exist** → Tell user honestly, suggest alternatives
4. **If parameters unknown** → Fetch documentation, don't guess

### Before writing any native or API call:
- [ ] Is this a real FiveM native? → Verify at docs.fivem.net/natives
- [ ] Is this the correct function name? → Check exact spelling
- [ ] Are these the correct parameters? → Verify parameter order and types
- [ ] Does this work on client/server/both? → Check availability

### When you don't know:
```
"I'm not 100% certain about this native/API. Let me fetch the documentation..."
[Use WebFetch to get accurate info]
```

### Verification Sources:
| Type | Source | Action |
|------|--------|--------|
| Native functions | https://docs.fivem.net/natives/ | WebFetch or tell user to check |
| QBox API | https://docs.qbox.re/ | WebFetch |
| QBCore API | https://docs.qbcore.org/ | WebFetch |
| ESX API | https://docs.esx-framework.org/ | WebFetch |
| ox_lib | https://overextended.dev/ox_lib | WebFetch |
| Props/Vehicles | https://forge.plebmasters.de/ | Guide user to search |

### Example - WRONG:
```lua
-- DON'T: Inventing a native that might not exist
SetPlayerInvincible(playerId, true)  -- Is this real? What are the params?
```

### Example - RIGHT:
```lua
-- DO: Use verified native with correct params
SetEntityInvincible(PlayerPedId(), true)  -- Verified at docs.fivem.net
```

---

## Content Map

**Read ONLY relevant files based on the request:**

| File | Description | When to Read |
|------|-------------|--------------|
| `frameworks/framework-detection.md` | Detect active framework | Starting new task |
| `frameworks/qbox.md` | QBox exports, patterns | QBox project |
| `frameworks/qbcore.md` | QBCore events, exports | QBCore project |
| `frameworks/esx.md` | ESX xPlayer, events | ESX project |
| `scripting/lua-patterns.md` | Lua idioms for FiveM | Writing Lua |
| `scripting/nui-guide.md` | NUI HTML/CSS/JS patterns | Building UI |
| `scripting/client-server.md` | Architecture patterns | New resource |
| `scripting/thread-management.md` | Performance patterns | Optimization |
| `resources/manifest.md` | fxmanifest.lua reference | Resource setup |
| `resources/ox-lib-guide.md` | ox_lib utilities | Using ox_lib |
| `assets/asset-discovery.md` | Finding GTA V assets | Props, vehicles, peds |

---

## Dynamic Fetching - Decision Tree

### Step 1: Classify the Request

| If user asks about... | Action |
|-----------------------|--------|
| Native function (GetPlayerPed, CreateVehicle, etc.) | **FETCH from natives** |
| Framework API (QBCore.Functions, ESX.GetPlayerData) | **FETCH from framework docs** |
| ox_lib feature (lib.callback, lib.notify) | **FETCH from ox_lib docs** |
| GTA V asset (prop, vehicle, ped model) | **GUIDE to PlebMasters** |
| Resource structure, manifest | **READ local files** |
| Best practices, patterns | **READ local files** |

### Step 2: WebFetch URLs

#### Native Functions
**Base URL:** `https://docs.fivem.net/natives/`

```
WebFetch(
  url: "https://docs.fivem.net/natives/",
  prompt: "Find documentation for the native function '{FUNCTION_NAME}'.
           Include: parameters, return values, usage examples,
           client/server availability."
)
```

**Native Categories:**
| Category | Contains |
|----------|----------|
| PLAYER | GetPlayerPed, GetPlayerServerId, PlayerId |
| VEHICLE | CreateVehicle, SetVehicleMod, GetVehicleClass |
| PED | CreatePed, SetPedComponentVariation, IsPedInVehicle |
| ENTITY | GetEntityCoords, SetEntityHeading, DeleteEntity |
| GRAPHICS | DrawRect, DrawText3D, DrawMarker |
| UI | SetTextEntry, BeginTextCommandDisplayText |
| CAM | CreateCam, SetCamActive, RenderScriptCams |
| AUDIO | PlaySoundFrontend, PlayAmbientSpeech1 |
| WEAPON | GiveWeaponToPed, GetSelectedPedWeapon |
| CFX | Statebags, server-specific natives |

#### Framework Documentation

**QBox:**
```
WebFetch(
  url: "https://docs.qbox.re/",
  prompt: "Find documentation for QBox '{FEATURE}'.
           Include exports, events, and usage examples."
)
```

**QBCore:**
```
WebFetch(
  url: "https://docs.qbcore.org/qbcore-documentation/",
  prompt: "Find documentation for QBCore '{FEATURE}'.
           Include: function signature, parameters, examples."
)
```

**ESX Legacy:**
```
WebFetch(
  url: "https://docs.esx-framework.org/",
  prompt: "Find documentation for ESX '{FEATURE}'.
           Include: xPlayer methods, events, server/client functions."
)
```

**ox_lib:**
```
WebFetch(
  url: "https://overextended.dev/ox_lib",
  prompt: "Find documentation for ox_lib '{MODULE}'.
           Include: function signatures, options, examples."
)
```

#### Asset Discovery

**PlebMasters Forge:**
```
WebFetch(
  url: "https://forge.plebmasters.de/",
  prompt: "Search for GTA V {ASSET_TYPE} matching '{SEARCH_TERM}'.
           Return model names/hashes that can be used in FiveM."
)
```

**Asset Types:** objects, vehicles, peds, weapons, clothes, animations

---

## Request Router - Pattern Matching

### RULE 1: Native Detection
**Triggers when:**
- Specific native name (PascalCase like `GetPlayerPed`, `CreateVehicle`)
- "native function", "GTA native", "FiveM native"
- Hash reference (`0x...`)

**Action:** Fetch from `https://docs.fivem.net/natives/`

### RULE 2: Framework API Detection
**Triggers when:**
- `QBCore.Functions.*`, `QBCore.Player.*`
- `exports.qbx_core:*`, `exports['qb-core']:*`
- `ESX.Get*`, `xPlayer:*`, `ESX.RegisterServerCallback`
- `exports.es_extended:*`

**Action:** Detect framework → Fetch from appropriate docs

### RULE 3: ox_lib Detection
**Triggers when:**
- `lib.*` functions
- `exports.ox_lib:*`
- Modules: callback, notify, menu, context, progress, zones, target

**Action:** Fetch from `https://overextended.dev/ox_lib`

### RULE 4: Asset Discovery
**Triggers when:**
- "What's the model for...", "prop name for...", "vehicle spawn name"
- Object placement, ped models, weapon models

**Action:** Guide to PlebMasters Forge + provide usage example

### RULE 5: Local Knowledge
**Triggers when:**
- fxmanifest.lua structure
- Client/server patterns
- Thread management
- Project structure

**Action:** Read relevant local markdown file

---

## Framework Auto-Detection

When starting a task, detect the active framework from project files:

### Check fxmanifest.lua
```lua
-- QBox indicators
dependency 'qbx_core'
dependency 'ox_lib'

-- QBCore indicators
dependency 'qb-core'

-- ESX indicators
dependency 'es_extended'
dependency 'esx_core'
```

### Check code imports
```lua
-- QBox
local QBX = exports.qbx_core:GetCoreObject()

-- QBCore
local QBCore = exports['qb-core']:GetCoreObject()

-- ESX
local ESX = exports.es_extended:getSharedObject()
```

---

## Best Practices (Quick Reference)

### Performance Rules
| Rule | Why |
|------|-----|
| Avoid `Wait(0)` in loops | Burns CPU, causes lag |
| Cache player ped | `local ped = cache.ped or PlayerPedId()` |
| Use ox_lib target | Better than distance checks |
| Statebags over events | More efficient state sync |

### Security Rules
| Rule | Reason |
|------|--------|
| Server-side validation | Client can be tampered |
| Sanitize player input | Prevent injection |
| Use callbacks | Prevent event exploitation |
| Rate limit operations | Prevent spam/abuse |

### Resource Structure
```
resource_name/
├── fxmanifest.lua
├── config.lua
├── client/
│   └── main.lua
├── server/
│   └── main.lua
├── shared/
│   └── config.lua
└── html/              # NUI
    ├── index.html
    ├── style.css
    └── script.js
```

---

## Framework-Agnostic Pattern

```lua
local Framework = {}

if GetResourceState('qbx_core') ~= 'missing' then
    Framework.Core = exports.qbx_core:GetCoreObject()
    Framework.Type = 'qbox'
elseif GetResourceState('qb-core') ~= 'missing' then
    Framework.Core = exports['qb-core']:GetCoreObject()
    Framework.Type = 'qbcore'
elseif GetResourceState('es_extended') ~= 'missing' then
    Framework.Core = exports.es_extended:getSharedObject()
    Framework.Type = 'esx'
end

return Framework
```

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| `while true do Wait(0)` | Use appropriate wait or events |
| Trust client data | Always validate on server |
| Hardcode framework | Detect dynamically |
| Fetch data every frame | Cache with refresh interval |
| Global variables | Use local, encapsulate |

---

## Related Skills

| Need | Skill |
|------|-------|
| NUI design | `frontend-design` |
| Database design | `database-design` |
| Security audit | `vulnerability-scanner` |
| Performance | `performance-profiling` |
