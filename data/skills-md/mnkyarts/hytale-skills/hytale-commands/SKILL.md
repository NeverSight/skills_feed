---
name: hytale-commands
description: Create custom commands for Hytale server plugins with arguments, permissions, and execution handling. Use when asked to "create a command", "add slash command", "make admin command", "register commands", or "command with arguments".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Hytale Custom Commands

Complete guide for creating custom server commands with arguments, permissions, tab completion, and execution handling.

## When to use this skill

Use this skill when:
- Creating new slash commands for players or admins
- Adding command arguments (required, optional, flags)
- Setting up command permissions
- Creating command collections/groups
- Implementing async commands for long-running operations
- Adding tab completion for arguments

## Command Architecture Overview

Hytale uses a command system based on abstract command classes with typed arguments. Commands are registered through the plugin's `CommandRegistry` and managed by the `CommandManager` singleton.

### Command Class Hierarchy

```
AbstractCommand
├── CommandBase              # Base for simple commands
├── AbstractAsyncCommand     # For async execution
├── AbstractPlayerCommand    # Requires player sender
├── AbstractWorldCommand     # Requires world context
├── AbstractTargetPlayerCommand    # Target another player
└── AbstractCommandCollection      # Group of subcommands
```

### Command Flow

```
Player Input -> CommandManager -> Parse Arguments -> Check Permissions -> Execute
```

## Basic Command Implementation

### Simple Command

```java
package com.example.myplugin.commands;

import com.hypixel.hytale.server.core.command.CommandBase;
import com.hypixel.hytale.server.core.command.CommandContext;

public class HelloCommand extends CommandBase {
    
    public HelloCommand() {
        super("hello", "Says hello to the world");
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        ctx.sendSuccess("Hello, World!");
    }
}
```

### Registration in Plugin

```java
@Override
protected void setup() {
    getCommandRegistry().registerCommand(new HelloCommand());
    getCommandRegistry().registerCommand(new SpawnCommand());
    getCommandRegistry().registerCommand(new TeleportCommand());
}
```

## Command Arguments

### Argument Types

| ArgType | Description | Example Value |
|---------|-------------|---------------|
| `STRING` | Text string | `"hello"` |
| `INTEGER` | Whole number | `42` |
| `FLOAT` | Decimal number | `3.14` |
| `BOOLEAN` | True/false | `true` |
| `PLAYER_REF` | Online player | `PlayerName` |
| `WORLD` | World name | `world_overworld` |
| `ITEM_ID` | Item identifier | `hytale:sword` |
| `BLOCK_ID` | Block identifier | `hytale:stone` |
| `ENTITY_TYPE_ID` | Entity type | `hytale:zombie` |
| `RELATIVE_INT_POSITION` | Block position | `~10 ~0 ~-5` |
| `RELATIVE_POSITION` | Precise position | `~10.5 ~0 ~-5.5` |
| `DIRECTION` | Direction vector | `north`, `up` |
| `DURATION` | Time duration | `10s`, `5m`, `1h` |
| `JSON` | JSON object | `{"key":"value"}` |
| `GREEDY_STRING` | Rest of input | `"hello world"` |

### Argument Kinds

```java
// Required argument - must be provided
RequiredArg<String> nameArg = new RequiredArg<>("name", ArgType.STRING);

// Optional argument - can be omitted
OptionalArg<Integer> countArg = new OptionalArg<>("count", ArgType.INTEGER);

// Default argument - uses default if omitted
DefaultArg<Integer> amountArg = new DefaultArg<>("amount", ArgType.INTEGER, 1);

// Flag argument - boolean switch
FlagArg silentFlag = new FlagArg("silent", "s");
```

### Command with Arguments

```java
public class GiveCommand extends CommandBase {
    
    private static final RequiredArg<PlayerRef> TARGET = 
        new RequiredArg<>("target", ArgType.PLAYER_REF);
    private static final RequiredArg<ItemId> ITEM = 
        new RequiredArg<>("item", ArgType.ITEM_ID);
    private static final DefaultArg<Integer> AMOUNT = 
        new DefaultArg<>("amount", ArgType.INTEGER, 1);
    private static final FlagArg SILENT = 
        new FlagArg("silent", "s");
    
    public GiveCommand() {
        super("give", "Give items to a player");
        addArg(TARGET);
        addArg(ITEM);
        addArg(AMOUNT);
        addArg(SILENT);
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        Player target = ctx.get(TARGET).resolve();
        ItemId item = ctx.get(ITEM);
        int amount = ctx.get(AMOUNT);
        boolean silent = ctx.has(SILENT);
        
        // Give the item
        target.getInventory().addItem(item, amount);
        
        if (!silent) {
            ctx.sendSuccess("Gave " + amount + "x " + item + " to " + target.getName());
        }
    }
}
```

## Specialized Command Classes

### Player-Only Command

Automatically checks that sender is a player. The `execute` method receives 5 parameters:

```java
import com.hypixel.hytale.component.Ref;
import com.hypixel.hytale.component.Store;
import com.hypixel.hytale.server.core.command.system.CommandContext;
import com.hypixel.hytale.server.core.command.system.basecommands.AbstractPlayerCommand;
import com.hypixel.hytale.server.core.universe.PlayerRef;
import com.hypixel.hytale.server.core.universe.world.World;
import com.hypixel.hytale.server.core.universe.world.storage.EntityStore;
import javax.annotation.Nonnull;

public class FlyCommand extends AbstractPlayerCommand {
    
    public FlyCommand() {
        super("fly", "Toggle flight mode");
    }
    
    @Override
    protected void execute(
        @Nonnull CommandContext context,
        @Nonnull Store<EntityStore> store,
        @Nonnull Ref<EntityStore> ref,
        @Nonnull PlayerRef playerRef,
        @Nonnull World world
    ) {
        // Access player data through PlayerRef
        String username = playerRef.getUsername();
        
        // Execute on world thread for world modifications
        world.execute(() -> {
            context.sendSuccess("Flight toggled for " + username);
        });
    }
}
```

### World Context Command

Requires a world context:

```java
public class TimeCommand extends AbstractWorldCommand {
    
    private static final RequiredArg<Integer> TIME = 
        new RequiredArg<>("time", ArgType.INTEGER);
    
    public TimeCommand() {
        super("time", "Set world time");
        addArg(TIME);
    }
    
    @Override
    protected void execute(CommandContext ctx, World world) {
        int time = ctx.get(TIME);
        world.setTime(time);
        ctx.sendSuccess("Set time to " + time + " in " + world.getName());
    }
}
```

### Target Player Command

For commands that target another player:

```java
public class HealCommand extends AbstractTargetPlayerCommand {
    
    public HealCommand() {
        super("heal", "Heal a player to full health");
    }
    
    @Override
    protected void execute(CommandContext ctx, Player target) {
        target.setHealth(target.getMaxHealth());
        ctx.sendSuccess("Healed " + target.getName());
    }
}
```

### Async Command

For long-running operations:

```java
public class BackupCommand extends AbstractAsyncCommand {
    
    public BackupCommand() {
        super("backup", "Create world backup");
    }
    
    @Override
    protected CompletableFuture<Void> executeAsync(CommandContext ctx) {
        return CompletableFuture.runAsync(() -> {
            ctx.sendMessage("Starting backup...");
            // Perform backup operation
            performBackup();
            ctx.sendSuccess("Backup complete!");
        });
    }
}
```

## Command Collections (Subcommands)

Group related commands together:

```java
public class AdminCommands extends AbstractCommandCollection {
    
    public AdminCommands() {
        super("admin", "Admin commands");
        
        // Register subcommands
        addSubCommand(new BanSubCommand());
        addSubCommand(new KickSubCommand());
        addSubCommand(new MuteSubCommand());
    }
    
    // Subcommand implementation
    private class BanSubCommand extends CommandBase {
        
        private static final RequiredArg<PlayerRef> TARGET = 
            new RequiredArg<>("target", ArgType.PLAYER_REF);
        private static final OptionalArg<String> REASON = 
            new OptionalArg<>("reason", ArgType.GREEDY_STRING);
        
        public BanSubCommand() {
            super("ban", "Ban a player");
            addArg(TARGET);
            addArg(REASON);
        }
        
        @Override
        protected void execute(CommandContext ctx) {
            Player target = ctx.get(TARGET).resolve();
            String reason = ctx.getOrDefault(REASON, "No reason provided");
            // Ban logic
            ctx.sendSuccess("Banned " + target.getName() + ": " + reason);
        }
    }
}
```

Usage: `/admin ban PlayerName Being naughty`

## Permissions

### Auto-Generated Permissions

Commands automatically get permissions based on plugin identity:

```
{plugin.group}.{plugin.name}.command.{commandName}
```

Example: `com.example.myplugin.command.give`

### Custom Permissions

```java
public class SecretCommand extends CommandBase {
    
    public SecretCommand() {
        super("secret", "A secret command");
        // Override default permission
        setPermission("admin.secret.access");
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        ctx.sendSuccess("You found the secret!");
    }
}
```

### Permission Checks in Execution

```java
@Override
protected void execute(CommandContext ctx) {
    if (!ctx.hasPermission("special.feature")) {
        ctx.sendError("You don't have permission for this feature!");
        return;
    }
    // Execute feature
}
```

## Command Context

The `CommandContext` provides access to sender info and utilities:

```java
@Override
protected void execute(CommandContext ctx) {
    // Get sender info
    CommandSender sender = ctx.getSender();
    boolean isPlayer = ctx.isPlayer();
    boolean isConsole = ctx.isConsole();
    
    // Get player if sender is player
    Optional<Player> player = ctx.getPlayerSender();
    
    // Get world context
    Optional<World> world = ctx.getWorld();
    
    // Send messages
    ctx.sendMessage("Plain message");
    ctx.sendSuccess("Success message");  // Green
    ctx.sendError("Error message");      // Red
    ctx.sendWarning("Warning message");  // Yellow
    
    // Get argument values
    String name = ctx.get(NAME_ARG);
    int count = ctx.getOrDefault(COUNT_ARG, 10);
    boolean hasFlag = ctx.has(SOME_FLAG);
    
    // Check permissions
    boolean canUse = ctx.hasPermission("some.permission");
}
```

## Tab Completion

Arguments provide automatic tab completion. Custom completion:

```java
public class CustomArg extends RequiredArg<String> {
    
    public CustomArg() {
        super("mode", ArgType.STRING);
    }
    
    @Override
    public List<String> getSuggestions(CommandContext ctx, String partial) {
        return List.of("easy", "medium", "hard")
            .stream()
            .filter(s -> s.startsWith(partial.toLowerCase()))
            .toList();
    }
}
```

## Complete Example Plugin

```java
package com.example.admintools;

import com.hypixel.hytale.server.core.plugin.JavaPlugin;
import com.hypixel.hytale.server.core.plugin.JavaPluginInit;
import javax.annotation.Nonnull;

public class AdminToolsPlugin extends JavaPlugin {
    
    public AdminToolsPlugin(@Nonnull JavaPluginInit init) {
        super(init);
    }
    
    @Override
    protected void setup() {
        // Register individual commands
        getCommandRegistry().registerCommand(new HealCommand());
        getCommandRegistry().registerCommand(new FlyCommand());
        getCommandRegistry().registerCommand(new TeleportCommand());
        
        // Register command collection
        getCommandRegistry().registerCommand(new AdminCommands());
        
        getLogger().atInfo().log("AdminTools commands registered!");
    }
}
```

## Best Practices

### Argument Validation

```java
@Override
protected void execute(CommandContext ctx) {
    int amount = ctx.get(AMOUNT);
    
    // Validate ranges
    if (amount < 1 || amount > 64) {
        ctx.sendError("Amount must be between 1 and 64");
        return;
    }
    
    // Continue execution
}
```

### Error Handling

```java
@Override
protected void execute(CommandContext ctx) {
    try {
        Player target = ctx.get(TARGET).resolve();
        if (target == null) {
            ctx.sendError("Player not found!");
            return;
        }
        // Execute command
    } catch (Exception e) {
        ctx.sendError("An error occurred: " + e.getMessage());
        getLogger().atSevere().withCause(e).log("Command error");
    }
}
```

### Feedback Messages

```java
@Override
protected void execute(CommandContext ctx) {
    // Always provide feedback
    ctx.sendMessage("Processing...");
    
    // Do work
    
    // Report result
    if (success) {
        ctx.sendSuccess("Operation completed!");
    } else {
        ctx.sendError("Operation failed: " + reason);
    }
}
```

## Troubleshooting

### Command Not Found

1. Verify command is registered in `setup()`
2. Check command name doesn't conflict with existing commands
3. Ensure plugin is loading correctly

### Permission Denied

1. Check player has the auto-generated permission
2. Verify custom permission is granted
3. Check permission node spelling

### Arguments Not Parsing

1. Verify argument order matches usage
2. Check ArgType matches expected input
3. Ensure required arguments are provided

### Tab Completion Not Working

1. Verify argument has suggestions defined
2. Check completion returns non-empty list
3. Ensure partial matching is implemented

## Detailed References

For comprehensive documentation:

- `references/argument-types.md` - Complete argument type reference with all ArgTypes, parsing, validation
- `references/command-patterns.md` - Advanced patterns: cooldowns, confirmations, pagination, wizards
