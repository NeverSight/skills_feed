---
name: minecraft-server-scriptapi
description: Guidance for working with the Minecraft Bedrock Script API @minecraft/server module. Use when answering questions about server-side scripting, world/system APIs, events, entities, components, or module versions for Minecraft Creator ScriptAPI.
---

# Minecraft Server ScriptAPI

## Workflow

1. **Scope**: Identify task (events, entities, components, commands, timing). Default to latest stable version unless beta/preview requested.
2. **Docs**: Navigate from module index to specific class/interface/event. Use Microsoft Learn as source of truth. Search via MCP when details missing.
3. **Output**: Quote exact API names. Provide minimal working example with required imports. Verify no official equivalent exists before creating custom helpers.
   - For enums like `CustomCommandParamType`, always check Microsoft Learn to confirm availability.
   - `@minecraft/vanilla-data` is not on Microsoft Learn, so skip MCP searches for those enums.

## Common patterns

### Events
- Subscribe/unsubscribe on `world`/`system` events. Guard logic for performance.

### Dimensions
- Use `world.getDimension(MinecraftDimensionTypes.<Dimension>)` and pick the appropriate dimension for the task.

### Components
- Check existence before access.
- Use typed IDs: `EntityComponentTypes`, `BlockComponentTypes`, `ItemComponentTypes`.

### Scheduling
- Use `system.run`, `system.runTimeout`, `system.runInterval`, `system.runJob`.

### Identifiers
- **MUST use `@minecraft/vanilla-data` enums**: `MinecraftBlockTypes`, `MinecraftEntityTypes`, `MinecraftItemTypes`, `MinecraftDimensionTypes`, `MinecraftEffectTypes`, `potionEffect`, `potionDelivery`, `feature`, `enchantment`, `cooldownCategory`, `cameraPresets`, `biome`.
- **Custom IDs**: Must include namespace prefix (e.g., `example:cmd`). One consistent prefix per addon.

Example:

```ts
import { world, system } from "@minecraft/server";
import { MinecraftDimensionTypes, MinecraftBlockTypes } from "@minecraft/vanilla-data";

system.runInterval(() => {
  const dimensions = [MinecraftDimensionTypes.Overworld, MinecraftDimensionTypes.Nether];
  const blocks = [MinecraftBlockTypes.Stone, MinecraftBlockTypes.Sand, MinecraftBlockTypes.GrassBlock];
  for (const dimension of dimensions) {
    for (const block of blocks) {
      world.getDimension(dimension).setBlockType({ x: 0, y: 0, z: 0 }, block);
    }
  }
});
```

## Permission modes

### Read-only
- Before simulation/events/tick start. No world mutations.
- Fix: defer to `system.run`/`runTimeout`/`runJob`.

### Doc verification
- When using any method/property, always check Microsoft Learn to confirm whether it is read-only safe or early-execution safe.
- Look for explicit notes in the API reference (read-only / early-execution) and follow them strictly.
- For arrow-function callbacks only, also check for restricted-execution notes like:
  - "This closure is called with restricted-execution privilege."
  - "This function can't be called in restricted-execution mode."
- If a restricted-execution note applies, review the arrow-function body to ensure no read-only or early-execution violations; defer with `system.run` if needed.

Example (read-only deferral):

```ts
world.beforeEvents.playerInteractWithBlock.subscribe((event) => {
  const player = event.player;
  system.run(() => {
    player.runCommand("say ok");
  });
});
```

### Early-execution
- Before world loads. Many APIs unavailable.
- Fix: defer to `world.afterEvents.worldLoad` or `system.run`.
- Subscribe at root to avoid missing events.

**Safe in early-execution**:
- Event subscriptions (`world`/`system` `beforeEvents`/`afterEvents`)
- `system.clearJob`, `clearRun`, `run`, `runInterval`, `runJob`, `runTimeout`, `waitTicks`
- `BlockComponentRegistry.registerCustomComponent`, `ItemComponentRegistry.registerCustomComponent`

## Custom commands

- Interface: `CustomCommand` (`name`, `description`, `permissionLevel`, `mandatoryParameters`, `optionalParameters`).
- Parameters: `CustomCommandParameter` (`name`, `type`, optional `enumName`).
- Param types and arrow-function argument types:
  - `String` -> `String`
  - `PlayerSelector` -> `Player`
  - `Location` -> `Vector3`
  - `ItemType` -> `ItemType`
  - `Integer` -> `Number`
  - `Float` -> `Number`
  - `Enum` -> `String`
  - `EntityType` -> `EntityType`
  - `EntitySelector` -> `Entity`
  - `Boolean` -> `Bool`
  - `BlockType` -> `BlockType`
- Register enums: `CustomCommandRegistry.registerEnum(name, values)`.
- Register cmd: `CustomCommandRegistry.registerCommand(customCommand, callback)`.
- Callback: `(origin, ...args) => CustomCommandResult`.
- Custom command callbacks run with restricted-execution privileges, so do not call read-only-restricted methods directly; defer with `system.run` if needed.
- When using an arrow function, align parameter names and order with the `CustomCommandParameter.name` list; avoid mismatched names or generic `args` when parameters are defined.

Example:

```ts
import {
  system,
  StartupEvent,
  CommandPermissionLevel,
  CustomCommandParamType,
  CustomCommandStatus,
} from "@minecraft/server";

system.beforeEvents.startup.subscribe((init: StartupEvent) => {
  init.customCommandRegistry.registerEnum("example:mode", ["on", "off"]);

  init.customCommandRegistry.registerCommand(
    {
      name: "example:demo",
      description: "Command demo",
      permissionLevel: CommandPermissionLevel.GameDirectors,
      cheatsRequired: true,
      mandatoryParameters: [
        {  type: CustomCommandParamType.String, name: "msg", },
        {  type: CustomCommandParamType.Enum, name: "example:mode"},
      ],
      optionalParameters: [
        { type: CustomCommandParamType.Boolean, name: "silent" },
        { type: CustomCommandParamType.Integer, name: "count" },
      ],
    },
    (origin, msg, mode, silent, count) => {
      const msgValue = String(msg ?? "ok");
      const modeValue = String(mode ?? "off");
      const silentValue = Boolean(silent ?? false);
      const countValue = Number(count ?? 1);

      return {
        status: CustomCommandStatus.Success,
        message: silentValue
          ? undefined
          : `[${origin.sourceType}] ${msgValue} mode=${modeValue} count=${countValue}`,
      };
    }
  );
});
```

## Script events

- Send: `system.sendScriptEvent(id, message)` (namespaced ID, payload string).
- Receive: `system.afterEvents.scriptEventReceive.subscribe(callback, options?)`.
- Event: `ScriptEventCommandMessageAfterEvent` (`id`, `message`, `sourceType`, optional `sourceEntity`/`sourceBlock`/`initiator`).
- Filter: `ScriptEventMessageFilterOptions.namespaces`.

Example:

```ts
import { system, world, ScriptEventSource } from "@minecraft/server";

system.afterEvents.scriptEventReceive.subscribe((event) => {
  const { id, message, sourceType, initiator, sourceEntity, sourceBlock } = event;
  if (id !== "example:say") return;

  switch (sourceType) {
    case ScriptEventSource.Block:
      world.sendMessage(`sendBy:${sourceBlock?.typeId ?? "unknown"} ${message}`);
      break;
    case ScriptEventSource.Entity:
      world.sendMessage(`sendBy:${sourceEntity?.typeId ?? "unknown"} ${message}`);
      break;
    case ScriptEventSource.NPCDialogue:
      world.sendMessage(`sendBy:${initiator?.typeId ?? "unknown"} ${message}`);
      break;
    case ScriptEventSource.Server:
      world.sendMessage(`sendBy:server ${message}`);
      break;
  }
});

```

## Performance

- Expensive work in events: use `system.runJob(generator)` to spread across ticks.
- Short-circuit before iterating large sets.

## system.run variants

- `run`: next tick.
- `runTimeout(cb, ticks)`: delay N ticks. `0` can cause tight loops if misused.
- `runInterval(cb, ticks)`: repeat every N ticks until `clearRun`.
- `runJob(generator)`: long-running work. Keep iterations small.

## Type safety

- Use `typeId` checks and verify component existence.
- `instanceof` only for documented `@minecraft/server` classes.



## Minimal templates

Event subscription:

```ts
world.afterEvents.playerJoin.subscribe((event) => {
  const player = event.player;
});
```

Tick loop:

```ts
system.runInterval(() => {
  // tick logic
}, 1);
```

Get dimension:

```ts
const overworld = world.getDimension(MinecraftDimensionTypes.Overworld);
```

Spawn entity:

```ts
const overworld = world.getDimension(MinecraftDimensionTypes.Overworld);
overworld.spawnEntity(MinecraftEntityTypes.Zombie, { x: 0, y: 80, z: 0 });
```

Give item:

```ts
const item = new ItemStack(MinecraftItemTypes.Diamond, 1);
player.getComponent("inventory")?.container?.addItem(item);
```

Apply effect:

```ts
player.addEffect(MinecraftEffectTypes.Speed, 200, { amplifier: 1 });
```

Get component (typed):

```ts
const health = entity.getComponent(EntityComponentTypes.Health);
```

## Pitfalls

- **Null components**: Check existence before access.
- **Heavy events**: Use `system.runJob`.
- **Permissions**: Avoid read-only/early-execution violations.
- **Raw IDs**: Use typed enums.
- **Namespaces**: One consistent prefix per addon.

## MCP tools

- Endpoint: https://learn.microsoft.com/api/mcp
- Search: `microsoft_docs_search` (module + class + task).
- Fetch: `microsoft_docs_fetch` (full signatures/details).
