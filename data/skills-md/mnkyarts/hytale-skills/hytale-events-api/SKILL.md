---
name: hytale-events-api
description: Handle Hytale server events including player actions, world changes, entity interactions, and custom events. Use when asked to "listen for events", "handle player actions", "react to block changes", "create event handlers", or "implement event listeners".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Hytale Events API

Complete guide for handling server events and creating custom event systems.

## When to use this skill

Use this skill when:
- Listening for player actions (connect, chat, interact)
- Reacting to world changes (blocks, chunks)
- Handling entity events (damage, death, spawn)
- Creating custom events
- Managing event priorities and cancellation
- Implementing async event handlers

## Event System Architecture

Hytale has two event systems:

1. **General Event Bus** - Server-wide events (players, worlds, assets)
2. **ECS Event System** - Entity-specific events (damage, interactions)

## General Event Bus

### Event Registration

Register in plugin `setup()`:

```java
@Override
protected void setup() {
    // Global listener - receives ALL events of this type
    getEventRegistry().registerGlobal(
        PlayerConnectEvent.class, 
        this::onPlayerConnect
    );
    
    // Keyed listener - receives events with specific key
    getEventRegistry().register(
        AddPlayerToWorldEvent.class, 
        "world_name", 
        this::onPlayerAddToWorld
    );
    
    // Priority listener
    getEventRegistry().registerGlobal(
        EventPriority.FIRST, 
        SomeEvent.class, 
        this::onSomeEvent
    );
    
    // Unhandled listener - only if no keyed handler processed
    getEventRegistry().registerUnhandled(
        SomeEvent.class, 
        this::onUnhandledEvent
    );
}
```

### Event Priorities

```java
public enum EventPriority {
    FIRST((short)-21844),   // Runs first
    EARLY((short)-10922),
    NORMAL((short)0),       // Default
    LATE((short)10922),
    LAST((short)21844);     // Runs last
}
```

Handlers execute in priority order. Use custom short values for fine-grained control.

### Event Cancellation

For cancellable events:

```java
private void onPlayerInteract(PlayerInteractEvent event) {
    if (shouldBlock(event)) {
        event.setCancelled(true);
    }
}
```

Check cancellation:

```java
private void onEvent(SomeEvent event) {
    if (event instanceof ICancellable cancellable && cancellable.isCancelled()) {
        return; // Already cancelled by earlier handler
    }
    // Process event
}
```

## Player Events

### Connection Events

```java
// Player connecting (before entering world)
getEventRegistry().registerGlobal(PlayerConnectEvent.class, event -> {
    Player player = event.getPlayer();
    getLogger().atInfo().log("Player connecting: %s", player.getName());
});

// Player setup connect (cancellable)
getEventRegistry().registerGlobal(PlayerSetupConnectEvent.class, event -> {
    if (isBanned(event.getPlayer())) {
        event.setCancelled(true);
        event.setDisconnectReason("You are banned!");
    }
});

// Player disconnecting
getEventRegistry().registerGlobal(PlayerDisconnectEvent.class, event -> {
    Player player = event.getPlayer();
    savePlayerData(player);
});

// Player added to world
getEventRegistry().register(AddPlayerToWorldEvent.class, "main", event -> {
    event.getPlayer().sendMessage("Welcome to the main world!");
});

// Player ready (fully loaded)
getEventRegistry().registerGlobal(PlayerReadyEvent.class, event -> {
    Player player = event.getPlayer();
    showWelcomeScreen(player);
});
```

### Chat Event

```java
// Async event - returns CompletableFuture
getEventRegistry().registerAsyncGlobal(
    PlayerChatEvent.class,
    future -> future.thenApply(event -> {
        String message = event.getMessage();
        
        // Modify message
        event.setMessage("[Custom] " + message);
        
        // Or cancel
        if (containsBadWords(message)) {
            event.setCancelled(true);
        }
        
        return event;
    })
);
```

### Interaction Events

```java
getEventRegistry().registerGlobal(PlayerInteractEvent.class, event -> {
    Player player = event.getPlayer();
    InteractionType type = event.getInteractionType();
    
    switch (type) {
        case USE -> handleUse(event);
        case ATTACK -> handleAttack(event);
        case LOOK -> handleLook(event);
    }
});
```

## World Events

### World Lifecycle

```java
// World being added (cancellable)
getEventRegistry().register(AddWorldEvent.class, "new_world", event -> {
    World world = event.getWorld();
    initializeWorld(world);
});

// World being removed (cancellable except EXCEPTIONAL)
getEventRegistry().register(RemoveWorldEvent.class, "old_world", event -> {
    if (event.getReason() != RemoveWorldEvent.Reason.EXCEPTIONAL) {
        saveWorldData(event.getWorld());
    }
});

// World started
getEventRegistry().register(StartWorldEvent.class, "main", event -> {
    spawnInitialEntities(event.getWorld());
});

// All worlds loaded
getEventRegistry().registerGlobal(AllWorldsLoadedEvent.class, event -> {
    getLogger().atInfo().log("All worlds ready!");
});
```

### Chunk Events

```java
// Chunk pre-load processing
getEventRegistry().registerGlobal(
    EventPriority.FIRST, 
    ChunkPreLoadProcessEvent.class, 
    event -> {
        // Modify chunk before it's fully loaded
        Chunk chunk = event.getChunk();
    }
);
```

## Entity Events

### Entity Removal

```java
getEventRegistry().register(EntityRemoveEvent.class, "world_name", event -> {
    Entity entity = event.getEntity();
    if (entity instanceof NPCEntity npc) {
        logNPCRemoval(npc);
    }
});
```

### Inventory Events

```java
getEventRegistry().register(
    LivingEntityInventoryChangeEvent.class, 
    "world_name", 
    event -> {
        LivingEntity entity = event.getEntity();
        ItemStack oldItem = event.getOldItem();
        ItemStack newItem = event.getNewItem();
        int slot = event.getSlot();
    }
);
```

## ECS Events

For entity-specific events, use the ECS event system.

### Block Events

```java
@Override
protected void setup() {
    // Register event systems
    getEntityStoreRegistry().registerSystem(new BreakBlockHandler());
    getEntityStoreRegistry().registerSystem(new PlaceBlockHandler());
    getEntityStoreRegistry().registerSystem(new UseBlockHandler());
}

public class BreakBlockHandler extends EntityEventSystem<EntityStore, BreakBlockEvent> {
    public BreakBlockHandler() {
        super(BreakBlockEvent.class);
    }
    
    @Override
    public void handle(
        int index,
        ArchetypeChunk<EntityStore> chunk,
        Store<EntityStore> store,
        CommandBuffer<EntityStore> buffer,
        BreakBlockEvent event
    ) {
        BlockType blockType = event.getBlockType();
        Vector3i position = event.getPosition();
        Player player = event.getPlayer();
        
        // Cancel if protected
        if (isProtected(position)) {
            event.setCancelled(true);
            player.sendMessage("This area is protected!");
            return;
        }
        
        // Custom drops
        if (blockType.getId().equals("MyPlugin:CustomOre")) {
            event.setDrops(createCustomDrops());
        }
    }
}
```

### Place Block Event

```java
public class PlaceBlockHandler extends EntityEventSystem<EntityStore, PlaceBlockEvent> {
    public PlaceBlockHandler() {
        super(PlaceBlockEvent.class);
    }
    
    @Override
    public void handle(..., PlaceBlockEvent event) {
        BlockType blockType = event.getBlockType();
        Vector3i position = event.getPosition();
        
        // Prevent placing in certain areas
        if (isRestrictedArea(position)) {
            event.setCancelled(true);
        }
    }
}
```

### Use Block Event

```java
public class UseBlockHandler extends EntityEventSystem<EntityStore, UseBlockEvent.Pre> {
    public UseBlockHandler() {
        super(UseBlockEvent.Pre.class);
    }
    
    @Override
    public void handle(..., UseBlockEvent.Pre event) {
        BlockType blockType = event.getBlockType();
        Player player = event.getPlayer();
        
        // Custom interaction
        if (blockType.getId().equals("MyPlugin:TeleportBlock")) {
            teleportPlayer(player);
            event.setCancelled(true); // Prevent default behavior
        }
    }
}
```

### Damage Event

```java
public class DamageHandler extends EntityEventSystem<EntityStore, Damage> {
    private ComponentAccess<EntityStore, TransformComponent> transforms;
    
    public DamageHandler() {
        super(Damage.class);
    }
    
    @Override
    protected void register(Store<EntityStore> store) {
        transforms = registerComponent(TransformComponent.class);
    }
    
    @Override
    public void handle(..., Damage event) {
        float amount = event.getAmount();
        DamageCause cause = event.getCause();
        Entity source = event.getSource();
        
        // Modify damage
        if (isInSafeZone(transforms.get(chunk, index).getPosition())) {
            event.setAmount(0);
            event.setCancelled(true);
        }
        
        // Increase damage for critical
        if (event.isCritical()) {
            event.setAmount(amount * 1.5f);
        }
    }
}
```

### Item Events

```java
// Drop item
public class DropHandler extends EntityEventSystem<EntityStore, DropItemEvent> {
    public DropHandler() {
        super(DropItemEvent.class);
    }
    
    @Override
    public void handle(..., DropItemEvent event) {
        ItemStack item = event.getItemStack();
        
        if (isSoulbound(item)) {
            event.setCancelled(true);
        }
    }
}

// Pickup item
public class PickupHandler extends EntityEventSystem<EntityStore, InteractivelyPickupItemEvent> {
    public PickupHandler() {
        super(InteractivelyPickupItemEvent.class);
    }
    
    @Override
    public void handle(..., InteractivelyPickupItemEvent event) {
        ItemStack item = event.getItemStack();
        Entity entity = event.getEntity();
        
        if (!canPickup(entity, item)) {
            event.setCancelled(true);
        }
    }
}
```

### Craft Event

```java
public class CraftHandler extends EntityEventSystem<EntityStore, CraftRecipeEvent> {
    public CraftHandler() {
        super(CraftRecipeEvent.class);
    }
    
    @Override
    public void handle(..., CraftRecipeEvent event) {
        CraftingRecipe recipe = event.getRecipe();
        Player player = event.getPlayer();
        
        // Check permissions
        if (!hasRecipeUnlocked(player, recipe)) {
            event.setCancelled(true);
            player.sendMessage("Recipe not unlocked!");
        }
    }
}
```

## Asset Events

### Asset Loading

```java
getEventRegistry().register(
    LoadedAssetsEvent.class, 
    BlockType.class, 
    event -> {
        for (BlockType block : event.getLoadedAssets()) {
            processBlockType(block);
        }
    }
);

getEventRegistry().register(
    LoadedAssetsEvent.class, 
    Item.class, 
    event -> {
        for (Item item : event.getLoadedAssets()) {
            processItem(item);
        }
    }
);
```

### Asset Removal

```java
getEventRegistry().register(
    RemovedAssetsEvent.class, 
    BlockType.class, 
    event -> {
        for (String removedId : event.getRemovedIds()) {
            cleanupBlockType(removedId);
        }
    }
);
```

### Asset Pack Events

```java
getEventRegistry().registerGlobal(AssetPackRegisterEvent.class, event -> {
    AssetPack pack = event.getAssetPack();
    getLogger().atInfo().log("Asset pack registered: %s", pack.getName());
});

getEventRegistry().registerGlobal(AssetPackUnregisterEvent.class, event -> {
    AssetPack pack = event.getAssetPack();
    getLogger().atInfo().log("Asset pack unregistered: %s", pack.getName());
});
```

## Plugin Events

```java
// When another plugin completes setup
getEventRegistry().register(
    PluginSetupEvent.class, 
    OtherPlugin.class, 
    event -> {
        OtherPlugin plugin = (OtherPlugin) event.getPlugin();
        integrateWith(plugin);
    }
);
```

## Creating Custom Events

### Simple Event

```java
public class MyCustomEvent implements IEvent<Void> {
    private final Player player;
    private final String data;
    
    public MyCustomEvent(Player player, String data) {
        this.player = player;
        this.data = data;
    }
    
    public Player getPlayer() { return player; }
    public String getData() { return data; }
}

// Dispatch the event
HytaleServer.get().getEventBus()
    .dispatchFor(MyCustomEvent.class)
    .dispatch(new MyCustomEvent(player, "some data"));
```

### Keyed Event

```java
public class MyWorldEvent implements IEvent<String> {
    private final World world;
    
    public MyWorldEvent(World world) {
        this.world = world;
    }
    
    public World getWorld() { return world; }
}

// Dispatch with key
HytaleServer.get().getEventBus()
    .dispatchFor(MyWorldEvent.class, world.getName())
    .dispatch(new MyWorldEvent(world));
```

### Cancellable Event

```java
public class MyCancellableEvent implements IEvent<Void>, ICancellable {
    private boolean cancelled = false;
    private final Player player;
    
    public MyCancellableEvent(Player player) {
        this.player = player;
    }
    
    public Player getPlayer() { return player; }
    
    @Override
    public boolean isCancelled() { return cancelled; }
    
    @Override
    public void setCancelled(boolean cancelled) { 
        this.cancelled = cancelled; 
    }
}

// Dispatch and check
MyCancellableEvent event = HytaleServer.get().getEventBus()
    .dispatchFor(MyCancellableEvent.class)
    .dispatch(new MyCancellableEvent(player));

if (!event.isCancelled()) {
    // Proceed with action
}
```

### Async Event

```java
public class MyAsyncEvent implements IAsyncEvent<Void>, ICancellable {
    private boolean cancelled = false;
    private final Player player;
    private String result;
    
    public MyAsyncEvent(Player player) {
        this.player = player;
    }
    
    public Player getPlayer() { return player; }
    public String getResult() { return result; }
    public void setResult(String result) { this.result = result; }
    
    @Override
    public boolean isCancelled() { return cancelled; }
    
    @Override
    public void setCancelled(boolean cancelled) { 
        this.cancelled = cancelled; 
    }
}

// Dispatch async
HytaleServer.get().getEventBus()
    .dispatchForAsync(MyAsyncEvent.class)
    .dispatch(new MyAsyncEvent(player))
    .thenAccept(event -> {
        if (!event.isCancelled()) {
            processResult(event.getResult());
        }
    });
```

### Custom ECS Event

```java
public class MyEntityEvent extends CancellableEcsEvent {
    private final ItemStack item;
    private float modifier = 1.0f;
    
    public MyEntityEvent(ItemStack item) {
        this.item = item;
    }
    
    public ItemStack getItem() { return item; }
    public float getModifier() { return modifier; }
    public void setModifier(float modifier) { this.modifier = modifier; }
}

// Register event type
EntityEventType<EntityStore, MyEntityEvent> eventType = 
    getEntityStoreRegistry().registerEntityEventType(MyEntityEvent.class);

// Invoke on entity
store.invoke(entityRef, new MyEntityEvent(itemStack));
```

## Event Best Practices

### Performance

```java
// Check for listeners before creating event
IEventDispatcher dispatcher = HytaleServer.get().getEventBus()
    .dispatchFor(ExpensiveEvent.class);

if (dispatcher.hasListener()) {
    dispatcher.dispatch(new ExpensiveEvent(computeExpensiveData()));
}
```

### Cleanup

Event registrations are automatically cleaned up when plugin disables. For manual cleanup:

```java
private EventRegistration registration;

@Override
protected void setup() {
    registration = getEventRegistry().registerGlobal(
        SomeEvent.class, 
        this::handler
    );
}

public void disableFeature() {
    if (registration != null) {
        registration.unregister();
        registration = null;
    }
}
```

### Error Handling

```java
private void onPlayerConnect(PlayerConnectEvent event) {
    try {
        processPlayer(event.getPlayer());
    } catch (Exception e) {
        getLogger().atSevere().withCause(e).log("Error processing player connect");
        // Don't rethrow - let other handlers run
    }
}
```

## Troubleshooting

### Events Not Firing

1. Verify registration is in `setup()`
2. Check event class matches exactly
3. Verify key matches for keyed events
4. Ensure plugin is enabled

### Handler Not Called

1. Check priority vs other handlers
2. Verify event not cancelled by earlier handler
3. Check for exceptions in handler

### Async Events Hanging

1. Always complete the CompletableFuture
2. Add timeout handling
3. Check for deadlocks

See `references/event-list.md` for complete event catalog.
See `references/ecs-events.md` for ECS event patterns.
