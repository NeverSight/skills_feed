---
name: flamework-roblox-ts
description: Build Roblox games with Flamework, a TypeScript framework. Use when creating services, controllers, components, networking (RemoteEvents/RemoteFunctions), dependency injection, lifecycle events, or working with Flamework decorators, macros, and configuration.
version: 1.0.0
---

# Flamework for Roblox-TS - Claude Code Skill

A comprehensive skill for working with Flamework, the TypeScript game framework for Roblox.

## Overview

Flamework is an extensible TypeScript game framework for Roblox that provides singletons, dependency injection, networking, and a component system with minimal boilerplate.

**What This Skill Covers:**
- **Core Framework**: Services, controllers, dependency injection, lifecycle events
- **Networking**: Type-safe RemoteEvents and RemoteFunctions with automatic guard generation
- **Components**: Entity-component system with attributes and lifecycle support
- **Configuration**: Complete project setup, tsconfig.json, and runtime configuration
- **Macros**: Compile-time utilities like Flamework.id, createGuard, and hash
- **Modding**: Creating custom decorators, metadata system, and extending Flamework

**Documentation Source:** Based on official Flamework documentation (https://flamework.fireboltofdeath.dev/) - current as of Flamework v1.0+

## Quick Start

### Basic Service/Controller

```typescript
import { Service, OnStart } from "@flamework/core";

@Service()
export class MyService implements OnStart {
    onStart() {
        print("Service started!");
    }
}
```

### Dependency Injection

```typescript
import { Service } from "@flamework/core";
import { OtherService } from "./other-service";

@Service()
export class MyService {
    // Dependencies injected via constructor
    constructor(private otherService: OtherService) {}
    
    method() {
        this.otherService.doSomething();
    }
}
```

### Runtime Initialization

```typescript
// runtime.server.ts or runtime.client.ts
import { Flamework } from "@flamework/core";

// Preload paths (services, controllers, components)
Flamework.addPaths("src/server/services/");
Flamework.addPaths("src/server/components/");

// Start the framework
Flamework.ignite();
```

## Core Concepts

### Singletons
Services (@Service) run on server, Controllers (@Controller) run on client. Only one instance created per class. Load order determined automatically by dependencies or via `loadOrder` option.

### Lifecycle Events
Implement interfaces to hook into lifecycle: `OnStart`, `OnInit`, `OnTick`, `OnPhysics`, `OnRender` (client only). Prefer `OnStart` over `OnInit` (OnInit blocks sequential execution).

### Dependency Resolution
Use constructor DI (preferred) or `Dependency<T>()` macro. Framework automatically determines load order from constructor dependencies.

## When to Use This Skill

- Setting up Flamework project structure
- Creating services, controllers, or components
- Implementing networking with type-safe RemoteEvents/RemoteFunctions
- Using dependency injection patterns
- Working with lifecycle events
- Configuring Flamework (tsconfig.json, flamework.json)
- Using Flamework macros (Flamework.id, Flamework.createGuard, etc.)
- Extending Flamework with custom decorators

## Detailed Documentation

This skill uses progressive disclosure for efficient context usage:
- **SKILL.md** (this file): Quick reference and common patterns (always loaded)
- **Reference files**: Detailed documentation (loaded only when needed)

**Available Reference Files:**
- [QUICKSTART.md](QUICKSTART.md) - Complete setup guide for new projects
- [CORE.md](CORE.md) - Services, controllers, dependency injection, lifecycle events
- [NETWORKING.md](NETWORKING.md) - RemoteEvents, RemoteFunctions, middleware, type guards
- [COMPONENTS.md](COMPONENTS.md) - Component system, attributes, configuration
- [CONFIGURATION.md](CONFIGURATION.md) - tsconfig.json, flamework.json, project setup
- [MACROS.md](MACROS.md) - Utility macros and compile-time features
- [MODDING.md](MODDING.md) - Creating custom decorators, metadata system

## Usage Tips

**This skill activates when you mention Flamework-related concepts:**
- "Create a Flamework service with dependency injection"
- "Set up RemoteEvents for combat system"
- "Make a health component with regeneration"
- "Configure Flamework for production"
- "Use Flamework.createGuard to validate data"
- "Create a custom decorator"

**For best results:**
1. Be specific about what you're building (service, component, networking, etc.)
2. Mention Flamework explicitly to trigger the skill
3. Ask for complete examples when learning new concepts
4. Request configuration help when setting up projects
5. Use progressive queries - start general, then ask for specific details

## Common Patterns

### Service with Dependencies
```typescript
@Service()
export class PlayerService implements OnStart {
    constructor(
        private dataService: DataService,
        private components: Components
    ) {}
    
    onStart() {
        // Initialize after dependencies ready
    }
}
```

### RemoteEvent Communication
```typescript
// shared/networking.ts
import { Networking } from "@flamework/networking";

interface ClientToServer {
    requestData(id: string): void;
}

interface ServerToClient {
    updateData(id: string, data: unknown): void;
}

export const GlobalEvents = Networking.createEvent<ClientToServer, ServerToClient>();

// server/networking.ts
export const Events = GlobalEvents.createServer();

// client/networking.ts
export const Events = GlobalEvents.createClient();
```

### Component with Attributes
```typescript
import { Component, BaseComponent } from "@flamework/components";

interface Attributes {
    health: number;
    maxHealth: number;
}

@Component({ tag: "Health" })
export class HealthComponent extends BaseComponent<Attributes> implements OnStart {
    onStart() {
        print(`Health: ${this.attributes.health}/${this.attributes.maxHealth}`);
    }
}
```

## Installation Quick Reference

```bash
# Install Flamework
npm i -D rbxts-transformer-flamework
npm i @flamework/core

# Optional modules
npm i @flamework/networking
npm i @flamework/components
```

**tsconfig.json** requirements:
```json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "plugins": [{ "transform": "rbxts-transformer-flamework" }],
    "typeRoots": ["node_modules/@rbxts", "node_modules/@flamework"]
  }
}
```

**default.project.json** requirements:
```json
{
  "node_modules": {
    "@rbxts": { "$path": "node_modules/@rbxts" },
    "@flamework": { "$path": "node_modules/@flamework" }
  }
}
```

## Best Practices

1. **Use constructor DI** over `Dependency<T>()` macro when possible
2. **Prefer OnStart** over OnInit for lifecycle events
3. **Split networking** into separate server/client files to hide server config from client
4. **Use progressive disclosure** - Split large codebases with clear separation
5. **Leverage type guards** - Flamework auto-generates guards for networking and components
6. **Structure by feature** not by type (group related services/controllers/components together)

## Troubleshooting

**"Dependency called before ignition"** - Use constructor DI or move Dependency<T>() call after Flamework.ignite()

**Components not loading** - Check ancestorBlacklist/Whitelist, ensure CollectionService tag is set, verify instanceGuard passes

**Network type guard failures** - Ensure types are supported by guard generation, check middleware configuration

**Load order issues** - Let automatic resolution handle it, or specify `loadOrder` in decorator options

For detailed troubleshooting and advanced topics, see the reference documentation files.

## Skill Coverage

**Complete Flamework v1.0+ Feature Set:**
✅ Core singletons and DI  
✅ Lifecycle events (OnStart, OnTick, OnPhysics, OnRender)  
✅ Full networking module with middleware  
✅ Complete component system with attributes  
✅ Configuration and setup (tsconfig, flamework.json)  
✅ All utility macros (id, implements, createGuard, hash)  
✅ Modding and extension API  

**Best Practices Emphasized:**
- Constructor DI over Dependency<T>() macro
- OnStart over OnInit for initialization
- Type safety with automatic guard generation
- Separate server/client networking files for security
- Feature-based code organization
- Progressive disclosure in large codebases