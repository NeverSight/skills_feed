---
name: luau-best-practices
description: |
  Luau best practices and clean code patterns for Roblox development. Use this skill when:
  - Writing new Luau modules, services, or controllers
  - Reviewing code for quality and maintainability
  - Setting up project structure and organization
  - Implementing error handling and validation
  - Managing memory and preventing leaks
  - Writing secure server-authoritative code
  - Following Roblox-specific conventions
  - Refactoring or improving existing code
  Triggers: "best practices", "clean code", "code review", "refactor", "code quality", "naming convention", "code style", "module pattern", "service pattern", "memory leak", "error handling", "pcall", "security", "server authority", "validation", "code organization"
---

# Luau Best Practices

Production-quality patterns for Roblox game development.

## Core Principles

1. **Server Authority** - Server owns game state; client is for presentation
2. **Fail Fast** - Validate early, error loudly in development
3. **Explicit > Implicit** - Clear intent beats clever code
4. **Minimal Surface Area** - Expose only what's needed

## Code Style

### Naming Conventions

```lua
-- PascalCase: Types, Classes, Services, Modules
type PlayerData = { ... }
local ShopService = {}
local PlayerController = require(...)

-- camelCase: Variables, functions, methods
local playerCount = 0
local function getPlayerData() end
function ShopService:purchaseItem() end

-- SCREAMING_SNAKE_CASE: Constants
local MAX_PLAYERS = 50
local DEFAULT_HEALTH = 100

-- Private with underscore prefix
local function _validateInput() end
local _cache = {}
```

### File Organization

```lua
--!strict

-- 1. Services/imports at top
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Signal = require(ReplicatedStorage.Packages.Signal)
local Types = require(script.Parent.Types)

-- 2. Constants
local MAX_RETRIES = 3
local TIMEOUT = 5

-- 3. Types
type Config = {
    enabled: boolean,
    maxItems: number,
}

-- 4. Module table
local MyModule = {}

-- 5. Private state
local _initialized = false
local _cache: { [string]: any } = {}

-- 6. Private functions
local function _helperFunction()
end

-- 7. Public API
function MyModule.init()
end

function MyModule.doSomething()
end

-- 8. Return
return MyModule
```

## Module Patterns

### Service Pattern (Server)

```lua
--!strict
local MyService = {}

local _started = false

function MyService:Start()
    assert(not _started, "MyService already started")
    _started = true
    -- Initialize connections, load data
end

function MyService:Stop()
    -- Cleanup for hot-reloading
end

return MyService
```

### Controller Pattern (Client)

```lua
--!strict
local MyController = {}

local _player = game:GetService("Players").LocalPlayer

function MyController:Init()
    -- Setup without yielding
end

function MyController:Start()
    -- Connect events, start loops
end

return MyController
```

### Lazy Initialization

```lua
local _data: PlayerData? = nil

local function getData(): PlayerData
    if not _data then
        _data = loadExpensiveData()
    end
    return _data
end
```

## Error Handling

### Use pcall for External Calls

```lua
-- DataStore, HTTP, any Roblox API that can fail
local success, result = pcall(function()
    return dataStore:GetAsync(key)
end)

if not success then
    warn("DataStore failed:", result)
    return nil
end

return result
```

### Result Pattern

```lua
type Result<T> =
    { ok: true, value: T } |
    { ok: false, error: string }

local function fetchData(id: string): Result<Data>
    local success, data = pcall(function()
        return dataStore:GetAsync(id)
    end)

    if not success then
        return { ok = false, error = tostring(data) }
    end

    return { ok = true, value = data }
end
```

### Assert for Programming Errors

```lua
-- Use assert for things that should never happen
function processPlayer(player: Player)
    assert(player, "player is required")
    assert(player:IsA("Player"), "expected Player instance")
    -- ...
end
```

See [references/error-handling.md](references/error-handling.md) for comprehensive patterns.

## Memory Management

### Always Disconnect

```lua
local connection: RBXScriptConnection

connection = event:Connect(function()
    -- handler
end)

-- Later, cleanup:
connection:Disconnect()
```

### Use Maids/Janitors

```lua
local Maid = require(Packages.Maid)

local maid = Maid.new()

maid:GiveTask(event:Connect(handler))
maid:GiveTask(instance)
maid:GiveTask(function()
    -- Custom cleanup
end)

-- Cleanup everything at once
maid:Destroy()
```

### Weak References for Caches

```lua
local cache = setmetatable({}, { __mode = "v" })

-- Values are garbage collected when no other references exist
cache[key] = expensiveObject
```

See [references/memory.md](references/memory.md) for leak prevention patterns.

## Security Best Practices

### Server Authority

```lua
-- BAD: Client tells server what happened
RemoteEvent.OnServerEvent:Connect(function(player, damage)
    target.Health -= damage  -- Client controls damage!
end)

-- GOOD: Server calculates everything
RemoteEvent.OnServerEvent:Connect(function(player, targetId)
    local target = getValidTarget(player, targetId)
    if not target then return end

    local damage = calculateDamage(player)  -- Server calculates
    target.Health -= damage
end)
```

### Validate All Input

```lua
RemoteFunction.OnServerInvoke = function(player, itemId, quantity)
    -- Type validation
    if typeof(itemId) ~= "string" then return end
    if typeof(quantity) ~= "number" then return end

    -- Range validation
    if quantity < 1 or quantity > 99 then return end
    if quantity ~= math.floor(quantity) then return end

    -- Business logic validation
    if not Items[itemId] then return end
    if not canAfford(player, itemId, quantity) then return end

    -- Now safe to process
    return purchaseItem(player, itemId, quantity)
end
```

### Rate Limiting

```lua
local lastAction: { [Player]: number } = {}
local COOLDOWN = 0.5

local function isRateLimited(player: Player): boolean
    local now = os.clock()
    local last = lastAction[player] or 0

    if now - last < COOLDOWN then
        return true
    end

    lastAction[player] = now
    return false
end
```

See [references/security.md](references/security.md) for comprehensive security patterns.

## Common Anti-Patterns

### Avoid

```lua
-- Using wait() - use task.wait()
wait(1)  -- BAD
task.wait(1)  -- GOOD

-- spawn() - use task.spawn()
spawn(fn)  -- BAD
task.spawn(fn)  -- GOOD

-- delay() - use task.delay()
delay(1, fn)  -- BAD
task.delay(1, fn)  -- GOOD

-- Polling when events exist
while true do
    if something then break end
    task.wait()
end
-- GOOD: Use events/signals instead

-- String concatenation in loops
local s = ""
for i = 1, 1000 do
    s = s .. tostring(i)  -- O(n²)
end
-- GOOD: Use table.concat

-- FindFirstChild chains
workspace.Folder.SubFolder.Part  -- Errors if missing
-- GOOD: Safe navigation
local folder = workspace:FindFirstChild("Folder")
local part = folder and folder:FindFirstChild("SubFolder")
    and folder.SubFolder:FindFirstChild("Part")
```

### Prefer

```lua
-- Generalized iteration
for _, v in ipairs(array) do end  -- OLD
for _, v in array do end  -- MODERN (Luau)

-- If expressions
local x = if condition then a else b  -- Clean ternary

-- Continue in loops
for _, item in items do
    if not item.valid then continue end
    process(item)
end

-- Optional chaining with and
local name = player and player.Character and player.Character.Name
```

## Project Structure

```
src/
├── Server/
│   ├── init.server.luau      # Bootstrap
│   ├── Services/             # Game services
│   │   ├── DataService.luau
│   │   └── CombatService.luau
│   └── Components/           # Server components
├── Client/
│   ├── init.client.luau      # Bootstrap
│   ├── Controllers/          # Client controllers
│   └── UI/                   # UI components
├── Shared/
│   ├── Types.luau            # Shared type definitions
│   ├── Constants.luau        # Shared constants
│   └── Util/                 # Shared utilities
└── Packages/                 # Wally packages
```

## Quick Reference

| Do | Don't |
|----|-------|
| `task.wait()` | `wait()` |
| `task.spawn()` | `spawn()` |
| `task.delay()` | `delay()` |
| `for _, v in t` | `for _, v in pairs(t)` |
| Validate on server | Trust client data |
| Use types | Use `any` everywhere |
| Disconnect events | Leave connections dangling |
| Use constants | Magic numbers/strings |
| Early return | Deep nesting |
| Small functions | 200+ line functions |

## References

- [Code Style Guide](references/code-style.md) - Naming, formatting, organization
- [Common Patterns](references/patterns.md) - Services, signals, state management
- [Error Handling](references/error-handling.md) - pcall, Result types, retries
- [Memory Management](references/memory.md) - Cleanup, leaks, weak tables
- [Security](references/security.md) - Server authority, validation, anti-exploit
