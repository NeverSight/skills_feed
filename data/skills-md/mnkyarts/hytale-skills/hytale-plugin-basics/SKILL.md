---
name: hytale-plugin-basics
description: Create and structure Hytale server plugins with proper lifecycle, manifest, dependencies, and registries. Use when asked to "create a Hytale plugin", "make a Hytale mod", "start a new Hytale plugin", "setup plugin structure", or "write plugin boilerplate".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Hytale Plugin Development Basics

Complete guide for creating Hytale server plugins following the official architecture patterns.

## When to use this skill

Use this skill when:
- Creating a new Hytale plugin from scratch
- Setting up plugin project structure
- Configuring plugin manifest (manifest.json)
- Understanding plugin lifecycle hooks
- Registering commands, events, or components
- Managing plugin dependencies

## Plugin Architecture Overview

Hytale plugins are Java-based extensions that run on the server. They follow an ECS (Entity Component System) architecture with lifecycle management.

### Plugin Types

| Type | Location | Description |
|------|----------|-------------|
| Core Plugins | Registered programmatically | Built-in server functionality |
| Builtin Plugins | `server.jar/../builtin/` | Shipped with server |
| External Plugins | `mods/` directory | User-installed plugins |
| Early Plugins | `earlyplugins/` | Bytecode transformers (advanced) |

### Plugin Lifecycle States

```
NONE -> SETUP -> START -> ENABLED -> SHUTDOWN -> DISABLED
```

## Project Structure

```
my-plugin/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/example/myplugin/
│       │       ├── MyPlugin.java
│       │       ├── commands/
│       │       ├── events/
│       │       ├── components/
│       │       └── systems/
│       └── resources/
│           ├── manifest.json
│           └── assets/           # Optional asset pack
│               └── Server/
│                   └── Content/
├── build.gradle
└── settings.gradle
```

## Plugin Manifest (manifest.json)

**Required** file in JAR root defining plugin metadata:

```json
{
  "Group": "com.example",
  "Name": "MyPlugin",
  "Version": "1.0.0",
  "Description": "My awesome Hytale plugin",
  "Authors": [
    {
      "Name": "Author Name",
      "Email": "author@example.com",
      "Url": "https://example.com"
    }
  ],
  "Website": "https://example.com/myplugin",
  "Main": "com.example.myplugin.MyPlugin",
  "ServerVersion": ">=1.0.0",
  "Dependencies": {
    "Hytale:NPCPlugin": ">=1.0.0"
  },
  "OptionalDependencies": {
    "Hytale:TeleportPlugin": "*"
  },
  "LoadBefore": {
    "Hytale:SomeOtherPlugin": "*"
  },
  "DisabledByDefault": false,
  "IncludesAssetPack": true
}
```

### Manifest Fields

| Field | Required | Description |
|-------|----------|-------------|
| `Group` | No | Organization/namespace identifier |
| `Name` | Yes | Plugin name (1-64 chars) |
| `Version` | No | Semantic version string |
| `Description` | No | Human-readable description |
| `Authors` | No | Array of author info objects |
| `Main` | Yes | Fully qualified main class name |
| `ServerVersion` | No | Required server version constraint |
| `Dependencies` | No | Required plugins with version constraints |
| `OptionalDependencies` | No | Optional plugins with version constraints |
| `LoadBefore` | No | Plugins this should load before |
| `DisabledByDefault` | No | Start disabled (default: false) |
| `IncludesAssetPack` | No | Has embedded assets (default: false) |

## Main Plugin Class

Extend `JavaPlugin` and implement lifecycle methods:

```java
package com.example.myplugin;

import com.hypixel.hytale.server.core.plugin.JavaPlugin;
import com.hypixel.hytale.server.core.plugin.JavaPluginInit;
import javax.annotation.Nonnull;

public class MyPlugin extends JavaPlugin {
    
    // Required constructor
    public MyPlugin(@Nonnull JavaPluginInit init) {
        super(init);
    }
    
    @Override
    protected void setup() {
        // Called after config load
        // Register: commands, events, components, systems, codecs
        getLogger().atInfo().log("MyPlugin setup complete!");
    }
    
    @Override
    protected void start() {
        // Called after all plugins complete setup
        // Safe to interact with other plugins
        getLogger().atInfo().log("MyPlugin started!");
    }
    
    @Override
    protected void shutdown() {
        // Called before disable (in reverse load order)
        // Cleanup resources
        getLogger().atInfo().log("MyPlugin shutting down!");
    }
}
```

## Available Registries

Access through `PluginBase` methods:

| Registry | Method | Purpose |
|----------|--------|---------|
| Commands | `getCommandRegistry()` | Register slash commands |
| Events | `getEventRegistry()` | Register event listeners |
| Tasks | `getTaskRegistry()` | Register async tasks |
| Block States | `getBlockStateRegistry()` | Register block state types |
| Entities | `getEntityRegistry()` | Register entity types |
| Client Features | `getClientFeatureRegistry()` | Register client features |
| Assets | `getAssetRegistry()` | Register asset stores |
| Entity Components | `getEntityStoreRegistry()` | Register ECS components/systems |
| Chunk Components | `getChunkStoreRegistry()` | Register chunk components/systems |
| Codecs | `getCodecRegistry(codec)` | Register serializable types |

### Command Registration

```java
@Override
protected void setup() {
    getCommandRegistry().registerCommand(new MyCommand());
}

// Command class
public class MyCommand extends Command {
    public MyCommand() {
        super("mycommand", "My command description");
        
        // Add arguments
        addArg(EntityArg.player("target"));
        addArg(IntArg.number("amount", 1, 100));
    }
    
    @Override
    public void execute(CommandContext ctx) {
        Player target = ctx.get("target");
        int amount = ctx.get("amount");
        ctx.sendMessage("Executed on " + target.getName() + " with " + amount);
    }
}
```

### Event Registration

```java
@Override
protected void setup() {
    // Global listener (all events of this type)
    getEventRegistry().registerGlobal(PlayerConnectEvent.class, this::onPlayerConnect);
    
    // Keyed listener (specific world/key)
    getEventRegistry().register(AddPlayerToWorldEvent.class, "world_name", this::onPlayerAddToWorld);
    
    // Priority listener
    getEventRegistry().registerGlobal(EventPriority.FIRST, SomeEvent.class, this::onSomeEvent);
}

private void onPlayerConnect(PlayerConnectEvent event) {
    getLogger().atInfo().log("Player connected: %s", event.getPlayer().getName());
}
```

### Component Registration (ECS)

```java
@Override
protected void setup() {
    // Register a component type
    ComponentType<EntityStore, MyComponent> myComponentType = 
        getEntityStoreRegistry().registerComponent(
            MyComponent.class, 
            MyComponent::new
        );
    
    // Register with serialization codec
    ComponentType<EntityStore, MyComponent> myComponentType = 
        getEntityStoreRegistry().registerComponent(
            MyComponent.class, 
            "myComponentName", 
            MyComponent.CODEC
        );
    
    // Register a system
    getEntityStoreRegistry().registerSystem(new MySystem());
}
```

### Codec Registration

```java
@Override
protected void setup() {
    // Register custom interaction type
    getCodecRegistry(Interaction.CODEC)
        .register("MyInteraction", MyInteraction.class, MyInteraction.CODEC);
    
    // Register custom action type
    getCodecRegistry(Action.CODEC)
        .register("MyAction", MyAction.class, MyAction.CODEC);
}
```

## Plugin Configuration

Use `withConfig()` for typed configuration:

```java
public class MyPlugin extends JavaPlugin {
    private final Config<MyConfig> config;
    
    public MyPlugin(@Nonnull JavaPluginInit init) {
        super(init);
        this.config = withConfig(MyConfig.CODEC);
    }
    
    @Override
    protected void setup() {
        MyConfig cfg = config.get();
        getLogger().atInfo().log("Config value: %s", cfg.someValue());
    }
}

// Config class
public record MyConfig(
    String someValue,
    int maxPlayers,
    boolean enableFeature
) {
    public static final BuilderCodec<MyConfig> CODEC = BuilderCodec.builder(
        Codec.STRING.required().fieldOf("SomeValue"),
        Codec.INT.required().fieldOf("MaxPlayers"),
        Codec.BOOL.optionalFieldOf("EnableFeature", true)
    ).constructor(MyConfig::new);
}
```

Config files are stored in `config/{PluginGroup}.{PluginName}/config.json`.

## Accessing Server Resources

```java
// Get the server instance
HytaleServer server = HytaleServer.get();

// Get the universe (world container)
Universe universe = server.getUniverse();

// Get a specific world
World world = universe.getWorld("world_name");

// Get the event bus
IEventBus eventBus = server.getEventBus();

// Get player by name
Optional<Player> player = server.getPlayerByName("PlayerName");

// Get asset registry
AssetRegistry assetRegistry = server.getAssetRegistry();
```

## Dependency Injection Pattern

Access other plugins safely:

```java
@Override
protected void start() {
    // Get optional dependency
    PluginBase teleportPlugin = getPluginManager()
        .getPlugin(PluginIdentifier.of("Hytale", "TeleportPlugin"))
        .orElse(null);
    
    if (teleportPlugin != null) {
        // Use teleport plugin features
    }
}
```

## Gradle Build Configuration

```groovy
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0.0'

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
    // Add Hytale repository if available
}

dependencies {
    compileOnly 'com.hypixel.hytale:hytale-server-api:1.0.0'
}

jar {
    from('src/main/resources') {
        include 'manifest.json'
        include 'assets/**'
    }
}
```

## Best Practices

### Lifecycle Management

1. **setup()**: Register all components, never interact with game state
2. **start()**: Safe to interact with world, players, other plugins
3. **shutdown()**: Clean up resources, save data, cancel tasks

### Error Handling

```java
@Override
protected void setup() {
    try {
        getCommandRegistry().registerCommand(new MyCommand());
    } catch (Exception e) {
        getLogger().atSevere().withCause(e).log("Failed to register command");
    }
}
```

### Logging

The Hytale server uses a fluent logging API:

```java
// Use the built-in logger with fluent API
getLogger().atInfo().log("Information message");
getLogger().atWarning().log("Warning message");
getLogger().atSevere().log("Error message");  // or atSevere().withCause(exception).log("Error message")
getLogger().atFine().log("Debug message");

// With string formatting
getLogger().atInfo().log("Player %s connected", playerName);

// With exception
getLogger().atSevere().withCause(exception).log("Failed to process request");
```

**Note:** The logger does NOT use `.info()`, `.warn()`, `.error()` methods directly. Always use the fluent pattern: `.atLevel().log("message")`.

### Resource Cleanup

All registrations through plugin registries are automatically cleaned up when the plugin is disabled. For custom resources:

```java
private ScheduledFuture<?> task;

@Override
protected void start() {
    task = scheduler.scheduleAtFixedRate(this::doWork, 0, 1, TimeUnit.SECONDS);
}

@Override
protected void shutdown() {
    if (task != null) {
        task.cancel(false);
    }
}
```

## Troubleshooting

### Plugin Not Loading

1. Check `manifest.json` is in JAR root
2. Verify `Main` class path is correct
3. Check for dependency version mismatches
4. Look for exceptions in server logs

### Class Not Found

1. Ensure dependencies are marked `compileOnly`
2. Check plugin load order via `Dependencies`/`LoadBefore`
3. Verify JAR contains all required classes

### Events Not Firing

1. Confirm registration happens in `setup()`
2. Check event key matches (for keyed events)
3. Verify event priority order
4. Ensure event isn't being cancelled

## Scaffolding Scripts

Use the provided scripts to quickly create a new plugin project with the complete directory structure and boilerplate code.

### Linux/macOS

```bash
# Interactive mode (prompts for all values)
./scripts/create-plugin.sh

# With arguments
./scripts/create-plugin.sh <PluginName> [Group] [Version] [Author] [Description]

# Example
./scripts/create-plugin.sh MyAwesomePlugin com.mycompany 1.0.0 "John Doe" "A cool plugin"
```

### Windows

```batch
:: Interactive mode (prompts for all values)
scripts\create-plugin.bat

:: With arguments
scripts\create-plugin.bat <PluginName> [Group] [Version] [Author] [Description]

:: Example
scripts\create-plugin.bat MyAwesomePlugin com.mycompany 1.0.0 "John Doe" "A cool plugin"
```

### Generated Structure

The scripts create the following project structure:

```
my-plugin/
├── src/main/java/com/example/myplugin/
│   ├── MyPlugin.java              # Main plugin class with lifecycle methods
│   ├── commands/
│   │   └── ExampleCommand.java    # Example command implementation
│   ├── events/
│   │   └── PlayerEventHandler.java # Example event handler
│   ├── components/                 # Directory for ECS components
│   └── systems/                    # Directory for ECS systems
├── src/main/resources/
│   ├── manifest.json              # Plugin manifest with metadata
│   └── assets/Server/Content/     # Asset pack directory (optional)
├── build.gradle                   # Gradle build configuration (Java 21)
├── settings.gradle                # Gradle project settings
└── .gitignore                     # Git ignore rules
```

### Script Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| PluginName | Yes | - | Name of the plugin (1-64 alphanumeric chars, starts with letter) |
| Group | No | `com.example` | Maven group/Java package prefix |
| Version | No | `1.0.0` | Semantic version string |
| Author | No | `Author` | Plugin author name |
| Description | No | *(empty)* | Human-readable plugin description |

See `references/plugin-lifecycle.md` for detailed lifecycle documentation.
See `references/registry-patterns.md` for advanced registration patterns.
