---
name: luau-type-expert
description: |
  Professional Luau type-checking and clean code specialist for Roblox development. Use this skill when:
  - Writing or reviewing Luau code that needs proper type annotations
  - Fixing type errors from luau-lsp or luau-analyze
  - Converting untyped Lua/Luau to strictly typed code
  - Designing type-safe APIs, modules, or data structures
  - Understanding Luau type system features (generics, unions, intersections, refinements)
  - Optimizing code for luau-lsp compatibility
  - Setting up --!strict mode compliance
  - Creating type definitions (.d.luau files)
  - Debugging "Type X is not compatible with Y" errors
  - Writing metatables with proper type support
  Triggers: "type error", "type annotation", "luau types", "strict mode", "--!strict", "type checking", "luau-lsp", "type mismatch", "generic type", "union type", "type narrowing", "type refinement", "type cast", "export type", "typeof"
---

# Luau Type Expert

Expert guidance for writing type-safe, clean Luau code that passes strict type checking.

## Type Modes

Always use `--!strict` at file top. Three modes exist:

| Mode | Behavior |
|------|----------|
| `--!nocheck` | Disables type checking entirely |
| `--!nonstrict` | Unknown types become `any` (default) |
| `--!strict` | Full type tracking, catches mismatches |

## Type Annotation Syntax

```lua
--!strict

-- Variables
local count: number = 0
local name: string = "Player"
local active: boolean = true

-- Functions
local function add(a: number, b: number): number
    return a + b
end

-- Optional parameters
local function greet(name: string, title: string?): string
    return (title or "") .. name
end

-- Multiple returns
local function divmod(a: number, b: number): (number, number)
    return math.floor(a / b), a % b
end

-- Variadic
local function sum(...: number): number
    local total = 0
    for _, v in {...} do total += v end
    return total
end
```

## Type Aliases

```lua
-- Simple alias
type UserId = number

-- Table types
type PlayerData = {
    coins: number,
    level: number,
    inventory: { string },
}

-- Export for cross-module use
export type ItemRecord = {
    id: string,
    quantity: number,
    createdAt: number,
}

-- Function type
type Callback = (player: Player, data: any) -> boolean

-- Generic types
type Result<T, E> = { ok: true, value: T } | { ok: false, error: E }
type Array<T> = { T }
type Map<K, V> = { [K]: V }
```

## Union and Intersection Types

```lua
-- Union: value is one of these types
type StringOrNumber = string | number
type OptionalString = string | nil  -- same as string?

-- Literal unions (discriminated)
type Status = "pending" | "active" | "completed"
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE"

-- Intersection: value has all these properties
type Named = { name: string }
type Aged = { age: number }
type Person = Named & Aged  -- has both name and age

-- Function intersection (overloads)
type Stringify = ((n: number) -> string) & ((b: boolean) -> string)
```

## Type Narrowing (Refinements)

Luau automatically narrows types in conditional blocks:

```lua
local function process(value: string | number)
    if type(value) == "string" then
        -- value: string here
        print(value:upper())
    else
        -- value: number here
        print(value + 1)
    end
end

-- typeof() for Roblox instances
local function handlePart(obj: Instance)
    if typeof(obj) == "BasePart" then
        -- obj: BasePart here
        obj.Anchored = true
    end
end

-- Truthy narrowing
local function safePrint(msg: string?)
    if msg then
        -- msg: string (not nil)
        print(msg)
    end
end

-- Equality narrowing
local function handleStatus(status: "pending" | "done")
    if status == "pending" then
        -- status: "pending"
    else
        -- status: "done"
    end
end
```

**Early return preserves refinements:**

```lua
local function requirePlayer(player: Player?): Player
    if not player then
        error("Player required")
    end
    -- player: Player (narrowed after early return)
    return player
end
```

## Type Casts

Use `::` to override inferred types:

```lua
-- Cast to specific type
local data = {} :: { string }
table.insert(data, "hello")  -- OK
table.insert(data, 123)      -- Error: number not string

-- Cast result of expression
local id = tostring(123) :: string

-- Cast for API returns
local part = workspace:FindFirstChild("Part") :: Part?
```

**Cast rules:** One operand must be subtype of the other, or `any`.

## Generics

```lua
-- Generic function
local function first<T>(arr: { T }): T?
    return arr[1]
end

-- Generic with constraint
local function clone<T>(obj: T & {}): T
    local copy = {}
    for k, v in obj :: any do
        copy[k] = v
    end
    return copy :: T
end

-- Generic type alias
type Container<T> = {
    value: T,
    set: (self: Container<T>, value: T) -> (),
    get: (self: Container<T>) -> T,
}

-- Multiple type parameters
type Pair<K, V> = { key: K, value: V }
```

## Table Types

```lua
-- Array (sequential integer keys)
type StringArray = { string }
type NumberList = { number }

-- Dictionary (string keys)
type Config = { [string]: any }
type Scores = { [string]: number }

-- Mixed table
type Player = {
    name: string,           -- required field
    score: number,
    items: { string },      -- array field
    metadata: { [string]: any }?,  -- optional dictionary
}

-- Exact table (no extra keys allowed in strict)
type Point = { x: number, y: number }
```

## Metatables and OOP

```lua
--!strict

export type Vector2 = {
    x: number,
    y: number,
}

type Vector2Impl = {
    __index: Vector2Impl,
    new: (x: number, y: number) -> Vector2,
    add: (self: Vector2, other: Vector2) -> Vector2,
    magnitude: (self: Vector2) -> number,
}

local Vector2: Vector2Impl = {} :: Vector2Impl
Vector2.__index = Vector2

function Vector2.new(x: number, y: number): Vector2
    return setmetatable({ x = x, y = y }, Vector2) :: Vector2
end

function Vector2:add(other: Vector2): Vector2
    return Vector2.new(self.x + other.x, self.y + other.y)
end

function Vector2:magnitude(): number
    return math.sqrt(self.x^2 + self.y^2)
end

return Vector2
```

## Common Type Errors and Fixes

See [references/common-errors.md](references/common-errors.md) for detailed error solutions.

**Quick fixes:**

| Error | Fix |
|-------|-----|
| `Type 'X' could not be converted into 'Y'` | Add explicit cast `:: Y` or fix the type |
| `Unknown global 'X'` | Import module or declare global type |
| `Property 'X' is not compatible` | Match property types exactly |
| `W_001: Unknown require` | Use proper require path aliases |

## luau-lsp CLI Usage

```bash
# Basic analysis
luau-lsp analyze src/

# With sourcemap for Roblox
luau-lsp analyze --sourcemap=sourcemap.json src/

# With definitions
luau-lsp analyze --definitions:@roblox=globalTypes.d.luau src/

# Disable all FFlags
luau-lsp analyze --no-flags-enabled src/
```

## .luaurc Configuration

```json
{
    "languageMode": "strict",
    "lint": {
        "LocalShadow": "disabled",
        "ImportUnused": "enabled"
    },
    "aliases": {
        "@shared": "src/Shared",
        "@server": "src/Server"
    }
}
```

## Performance-Aware Typing

See [references/performance.md](references/performance.md) for performance patterns.

**Key points:**
- Use `table.field` not `table["field"]`
- Keep metatables shallow (direct `__index` to table)
- Localize builtins: `local max = math.max`
- Avoid `getfenv`/`setfenv` (deoptimizes)
- Use `table.create(n)` for known sizes

## Lint Rules Reference

See [references/lint-rules.md](references/lint-rules.md) for all 28 lint rules.

**Critical rules:**
- `UnknownGlobal` - Catches typos
- `LocalUnused` - Dead code
- `ImplicitReturn` - Inconsistent returns
- `UninitializedLocal` - Use before assign
