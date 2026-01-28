---
name: roblox-ts
description: Write Roblox games in TypeScript. Use for roblox-ts setup, configuration, type-safe Roblox API usage, project structure, package management, compiling TypeScript to Luau, debugging, and working with roblox-ts packages and best practices.
version: 1.0.0
---

# Roblox-TS - Claude Code Skill

A comprehensive skill for developing Roblox games with TypeScript using roblox-ts.

## Overview

Roblox-TS is a TypeScript-to-Luau compiler that allows you to write Roblox games using TypeScript's type safety, modern syntax, and tooling while compiling to performant Luau code.

**What This Skill Covers:**
- **Setup & Configuration**: Project initialization, tsconfig.json, Rojo integration
- **Type-Safe Roblox API**: Working with Roblox services, instances, and datatypes
- **TypeScript Features**: Using modern TypeScript with Roblox limitations
- **Package Management**: Installing and using @rbxts packages from npm
- **Build & Deployment**: Compilation, optimization, and publishing workflow
- **Best Practices**: Type safety, performance, project structure, and debugging

**Documentation Sources:** 
- Official roblox-ts docs (https://roblox-ts.com/)
- TypeScript handbook (adapted for Roblox)
- Roblox Creator documentation

## Quick Start

### Installation

```bash
# Install roblox-ts globally
npm install -g roblox-ts

# Create new project
npx rbxtsc init

# Or initialize in existing directory
cd my-game
npx rbxtsc init

# Install packages
npm install
```

### Basic Script Structure

**Server Script (src/server/main.server.ts):**
```typescript
import { Players, Workspace } from "@rbxts/services";

Players.PlayerAdded.Connect((player) => {
    print(`${player.Name} joined the game!`);
});
```

**Client Script (src/client/main.client.ts):**
```typescript
import { Players, UserInputService } from "@rbxts/services";

const player = Players.LocalPlayer;

UserInputService.InputBegan.Connect((input) => {
    if (input.KeyCode === Enum.KeyCode.Space) {
        print("Space pressed!");
    }
});
```

### Compilation

```bash
# Build once
npx rbxtsc

# Watch mode (rebuild on file change)
npx rbxtsc -w

# Build with verbose output
npx rbxtsc -w --verbose
```

## Core Concepts

### Type-Safe Roblox API

All Roblox services and APIs are fully typed:

```typescript
import { Workspace, Players, ReplicatedStorage } from "@rbxts/services";

// Type-safe instance access
const part = Workspace.FindFirstChild("MyPart") as Part | undefined;
if (part) {
    part.BrickColor = BrickColor.Red();
    part.Anchored = true;
}

// Service usage with intellisense
Players.PlayerAdded.Connect((player) => {
    const character = player.Character || player.CharacterAdded.Wait()[0];
    const humanoid = character.FindFirstChildOfClass("Humanoid");
});
```

### TypeScript to Luau Mapping

**Arrays:**
```typescript
const array = [1, 2, 3, 4, 5];
array.push(6);
const filtered = array.filter(x => x > 3);
```

**Maps (instead of objects for dictionaries):**
```typescript
// Use Map for key-value pairs
const playerData = new Map<Player, number>();
playerData.set(player, 100);
const health = playerData.get(player);
```

**Sets:**
```typescript
const uniqueIds = new Set<string>();
uniqueIds.add("id1");
uniqueIds.add("id2");
```

**Promises (for async operations):**
```typescript
import { HttpService } from "@rbxts/services";

async function fetchData(url: string) {
    const response = await HttpService.GetAsync(url);
    return response;
}
```

### Roact (React for Roblox)

```typescript
import Roact from "@rbxts/roact";

interface Props {
    text: string;
    onClick: () => void;
}

function Button({ text, onClick }: Props) {
    return (
        <textbutton
            Size={new UDim2(0, 200, 0, 50)}
            Text={text}
            Event={{ MouseButton1Click: onClick }}
        />
    );
}
```

## When to Use This Skill

- Setting up new roblox-ts projects
- Configuring tsconfig.json or Rojo projects
- Converting Lua code to TypeScript
- Working with type-safe Roblox APIs
- Installing and using @rbxts packages
- Understanding TypeScript/Luau differences
- Debugging compilation or type errors
- Structuring roblox-ts projects
- Using modern TypeScript features with Roblox

## Detailed Documentation

This skill uses progressive disclosure for efficient context usage:
- **SKILL.md** (this file): Quick reference and common patterns (always loaded)
- **Reference files**: Detailed documentation (loaded only when needed)

**Available Reference Files:**
- [SETUP.md](SETUP.md) - Installation, project structure, configuration
- [TYPESCRIPT.md](TYPESCRIPT.md) - TypeScript features, limitations, and idioms
- [ROBLOX_API.md](ROBLOX_API.md) - Type-safe Roblox API usage and patterns
- [PACKAGES.md](PACKAGES.md) - Popular @rbxts packages and package management
- [BUILD.md](BUILD.md) - Compilation, optimization, and deployment
- [MIGRATION.md](MIGRATION.md) - Converting Lua to TypeScript
- [BEST_PRACTICES.md](BEST_PRACTICES.md) - Project structure, performance, debugging

## Usage Tips

**This skill activates when you mention roblox-ts concepts:**
- "Set up a new roblox-ts project"
- "Convert this Lua code to TypeScript"
- "Use RemoteEvents with type safety"
- "Install Roact for my roblox-ts game"
- "Fix roblox-ts compilation error"
- "Structure my TypeScript Roblox project"

**For best results:**
1. Specify if you're working on server or client scripts
2. Mention specific Roblox services or APIs you're using
3. Share error messages for compilation issues
4. Ask about TypeScript equivalents for Lua patterns
5. Request complete examples for new concepts

## Common Patterns

### Remote Events with Type Safety

```typescript
// shared/remotes.ts
import { createRemotes, remote } from "@rbxts/remo";

const remotes = createRemotes({
    playerDamaged: remote<Server, [targetId: string, damage: number]>(),
    updateHealth: remote<Client, [health: number]>(),
});

export = remotes;

// server/combat.server.ts
import remotes from "shared/remotes";

remotes.Server.playerDamaged.connect((player, targetId, damage) => {
    // Type-safe parameters
    print(`${player.Name} damaged ${targetId} for ${damage}`);
});

// Fire to client
remotes.Server.updateHealth.fire(player, 75);

// client/ui.client.ts
import remotes from "shared/remotes";

remotes.Client.updateHealth.connect((health) => {
    print(`Health updated: ${health}`);
});

// Fire to server
remotes.Client.playerDamaged.fire("enemy-123", 25);
```

### Data Stores with Type Safety

```typescript
import { DataStoreService } from "@rbxts/services";

interface PlayerData {
    coins: number;
    level: number;
    inventory: string[];
}

const dataStore = DataStoreService.GetDataStore("PlayerData");

function savePlayerData(userId: string, data: PlayerData) {
    const success = pcall(() => {
        dataStore.SetAsync(userId, data);
    })[0];
    
    return success;
}

function loadPlayerData(userId: string): PlayerData | undefined {
    const [success, data] = pcall(() => {
        return dataStore.GetAsync(userId) as PlayerData | undefined;
    });
    
    return success ? data : undefined;
}
```

### Character Management

```typescript
import { Players } from "@rbxts/services";

function setupCharacter(player: Player) {
    const character = player.Character || player.CharacterAdded.Wait()[0];
    const humanoid = character.WaitForChild("Humanoid") as Humanoid;
    const rootPart = character.WaitForChild("HumanoidRootPart") as Part;
    
    humanoid.Died.Connect(() => {
        print(`${player.Name} died`);
    });
    
    return { character, humanoid, rootPart };
}

Players.PlayerAdded.Connect((player) => {
    player.CharacterAdded.Connect(() => {
        setupCharacter(player);
    });
});
```

### GUI with Roact

```typescript
import Roact from "@rbxts/roact";
import { Players } from "@rbxts/services";

interface State {
    health: number;
}

class HealthBar extends Roact.Component<{}, State> {
    state: State = { health: 100 };
    
    render() {
        return (
            <screengui>
                <frame
                    Size={new UDim2(0, 200, 0, 30)}
                    Position={new UDim2(0.5, -100, 0, 10)}
                    BackgroundColor3={Color3.fromRGB(50, 50, 50)}
                >
                    <frame
                        Size={new UDim2(this.state.health / 100, 0, 1, 0)}
                        BackgroundColor3={Color3.fromRGB(0, 255, 0)}
                    />
                </frame>
            </screengui>
        );
    }
}

const playerGui = Players.LocalPlayer.WaitForChild("PlayerGui");
Roact.mount(<HealthBar />, playerGui);
```

## Configuration Quick Reference

**tsconfig.json essentials:**
```json
{
  "compilerOptions": {
    "outDir": "out",
    "rootDir": "src",
    "module": "commonjs",
    "strict": true,
    "noLib": true,
    "downlevelIteration": true,
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "types": ["@rbxts/types"]
  }
}
```

**default.project.json (Rojo):**
```json
{
  "name": "my-game",
  "tree": {
    "$className": "DataModel",
    "ReplicatedStorage": {
      "$className": "ReplicatedStorage",
      "rbxts_include": {
        "$path": "include",
        "node_modules": { "$path": "node_modules/@rbxts" }
      }
    },
    "ServerScriptService": {
      "$className": "ServerScriptService",
      "TS": { "$path": "out/server" }
    }
  }
}
```

## Best Practices

1. **Use strict type checking** - Enable `strict: true` in tsconfig.json
2. **Prefer Maps over objects** - For dictionaries with dynamic keys
3. **Use proper exports** - `export =` for modules, named exports for utilities
4. **Leverage type guards** - Use `typeIs` and `classIs` for runtime checks
5. **Structure by feature** - Group related server/client/shared code
6. **Use @rbxts packages** - Don't reinvent the wheel (Roact, t, remo, etc.)
7. **Handle promises properly** - Always catch rejections
8. **Avoid `any` type** - Use `unknown` and type guards instead

## TypeScript vs Lua Key Differences

**Arrays start at 0 (not 1):**
```typescript
const arr = [1, 2, 3];
print(arr[0]); // 1 (TypeScript)
// In Lua: arr[1] is 1
```

**Use === for equality:**
```typescript
if (value === undefined) { }  // TypeScript
// Not: if value == nil then (Lua)
```

**No `self` keyword:**
```typescript
class MyClass {
    value = 10;
    
    method() {
        print(this.value);  // TypeScript uses 'this'
    }
}
```

**Destructuring:**
```typescript
const { Name, Health } = player;
const [first, second] = array;
```

## Troubleshooting

**"Cannot find module '@rbxts/services'"** - Run `npm install @rbxts/services @rbxts/types`

**Compilation errors** - Check tsconfig.json has correct settings, ensure TypeScript version is compatible

**Type errors with Roblox API** - Update `@rbxts/types` package for latest API types

**"Expected 'this' in method"** - Use arrow functions for callbacks: `() => this.method()`

**Import errors** - Use correct export style (`export =` for modules, `export default` not supported)

For detailed troubleshooting, see BUILD.md and BEST_PRACTICES.md reference files.

## Skill Coverage

**Complete roblox-ts Feature Set:**
✅ Project setup and configuration  
✅ TypeScript compilation to Luau  
✅ Full Roblox API type definitions  
✅ Package management (@rbxts ecosystem)  
✅ Roact/React for UI  
✅ Remote communication patterns  
✅ Data storage patterns  
✅ Build and deployment workflow  
✅ Migration from Lua  
✅ Performance optimization  

**Best Practices Emphasized:**
- Strict type safety for reliability
- Map/Set over objects for collections
- Proper async handling with Promises
- Feature-based project structure
- Leveraging @rbxts package ecosystem
- Type guards for runtime safety
