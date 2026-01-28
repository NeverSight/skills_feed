---
name: hytale-networking
description: Handle Hytale network packets, create custom packets, and implement client-server communication. Use when asked to "create custom packets", "handle network messages", "send data to client", "receive client data", or "implement networking".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Hytale Networking API

Complete guide for handling network packets and client-server communication.

## When to use this skill

Use this skill when:
- Sending data to clients
- Receiving data from clients
- Creating custom packet types
- Implementing custom UI synchronization
- Handling real-time player input
- Syncing custom game state

## Network Architecture Overview

Hytale uses a packet-based networking system:

```
Client <---> Server
   |           |
   Packet      Packet
   Encoder     Decoder
   |           |
   ByteBuf <-> ByteBuf
```

### Protocol Components

| Component | Description |
|-----------|-------------|
| `Packet` | Data structure with serialization |
| `PacketRegistry` | Maps packet IDs to classes |
| `PacketHandler` | Processes incoming packets |
| `PacketEncoder` | Serializes packets to bytes |
| `PacketDecoder` | Deserializes bytes to packets |

## Packet Structure

### Packet Interface

All packets implement the `Packet` interface:

```java
public interface Packet {
    int getId();
    void serialize(ByteBuf buffer);
    int computeSize();
}
```

### Built-in Packet Categories

| Category | Direction | Examples |
|----------|-----------|----------|
| `auth` | Bidirectional | AuthToken, ConnectAccept |
| `connection` | Bidirectional | Connect, Disconnect, Ping |
| `setup` | S→C | WorldSettings, AssetInitialize |
| `player` | C→S | ClientMovement, MouseInteraction |
| `entities` | S→C | EntityUpdates, PlayAnimation |
| `world` | S→C | SetChunk, ServerSetBlock |
| `inventory` | Bidirectional | MoveItemStack, SetActiveSlot |
| `window` | Bidirectional | OpenWindow, CloseWindow |
| `interface` | S→C | ChatMessage, Notification |
| `interaction` | Bidirectional | SyncInteractionChains |
| `camera` | S→C | CameraShakeEffect |

## Registering Packet Handlers

### SubPacketHandler Pattern

Create modular packet handlers:

```java
public class MyPacketHandler implements SubPacketHandler {
    private final MyPlugin plugin;
    
    public MyPacketHandler(MyPlugin plugin) {
        this.plugin = plugin;
    }
    
    @Override
    public void registerHandlers(IPacketHandler handler) {
        // Register by packet ID
        handler.registerHandler(108, this::handleClientMovement);
        handler.registerHandler(111, this::handleMouseInteraction);
        
        // Or by packet class
        handler.registerHandler(CustomPacket.ID, this::handleCustomPacket);
    }
    
    private void handleClientMovement(Packet packet) {
        ClientMovement movement = (ClientMovement) packet;
        Vector3d position = movement.getPosition();
        // Process movement
    }
    
    private void handleMouseInteraction(Packet packet) {
        MouseInteraction interaction = (MouseInteraction) packet;
        // Process mouse input
    }
}
```

### Registering in Plugin

```java
@Override
protected void setup() {
    // Register packet handler with server manager
    ServerManager serverManager = HytaleServer.get().getServerManager();
    serverManager.registerSubPacketHandler(new MyPacketHandler(this));
}
```

## Sending Packets

### Send to Single Player

```java
public void sendToPlayer(Player player, Packet packet) {
    player.getConnection().send(packet);
}
```

### Send to Multiple Players

```java
public void sendToAll(Packet packet) {
    for (Player player : HytaleServer.get().getOnlinePlayers()) {
        player.getConnection().send(packet);
    }
}

public void sendToWorld(World world, Packet packet) {
    for (Player player : world.getPlayers()) {
        player.getConnection().send(packet);
    }
}

public void sendToNearby(Vector3d position, double radius, Packet packet) {
    for (Player player : HytaleServer.get().getOnlinePlayers()) {
        if (player.getPosition().distanceTo(position) <= radius) {
            player.getConnection().send(packet);
        }
    }
}
```

### Send with Callback

```java
player.getConnection().send(packet).thenAccept(result -> {
    if (result.isSuccess()) {
        getLogger().atInfo().log("Packet sent successfully");
    } else {
        getLogger().atWarning().log("Packet failed to send: %s", result.getError());
    }
});
```

## Built-in Packets Reference

### Chat Message

```java
// Send chat message to player
ChatMessage chatPacket = new ChatMessage(
    "Hello, World!",
    ChatMessage.Type.SYSTEM
);
player.getConnection().send(chatPacket);
```

### Notification

```java
// Send notification popup
Notification notification = new Notification(
    "Achievement Unlocked!",
    "You found the secret area",
    Notification.Type.SUCCESS,
    5000  // Duration in ms
);
player.getConnection().send(notification);
```

### Play Sound

```java
// Play sound at position
PlaySoundPacket sound = new PlaySoundPacket(
    "MyPlugin/Sounds/alert",
    position,
    1.0f,  // Volume
    1.0f   // Pitch
);
player.getConnection().send(sound);
```

### Entity Updates

```java
// Send entity state update
EntityUpdates updates = new EntityUpdates(
    entityId,
    new HashMap<>() {{
        put("health", health);
        put("position", position);
    }}
);
sendToNearby(position, 64, updates);
```

### Set Block

```java
// Update block on client
ServerSetBlock setBlock = new ServerSetBlock(
    position,
    blockTypeId,
    blockState
);
sendToWorld(world, setBlock);
```

## Creating Custom Packets

### Define Packet Class

```java
public class MyCustomPacket implements Packet {
    public static final int ID = 5000; // Custom ID (use high numbers)
    
    private final String message;
    private final int value;
    private final Vector3d position;
    
    // Deserialize constructor
    public MyCustomPacket(ByteBuf buffer) {
        this.message = PacketIO.readString(buffer);
        this.value = buffer.readInt();
        this.position = new Vector3d(
            buffer.readDouble(),
            buffer.readDouble(),
            buffer.readDouble()
        );
    }
    
    // Create constructor
    public MyCustomPacket(String message, int value, Vector3d position) {
        this.message = message;
        this.value = value;
        this.position = position;
    }
    
    @Override
    public int getId() {
        return ID;
    }
    
    @Override
    public void serialize(ByteBuf buffer) {
        PacketIO.writeString(buffer, message);
        buffer.writeInt(value);
        buffer.writeDouble(position.x());
        buffer.writeDouble(position.y());
        buffer.writeDouble(position.z());
    }
    
    @Override
    public int computeSize() {
        return PacketIO.stringSize(message) + 4 + 24; // int + 3 doubles
    }
    
    // Getters
    public String getMessage() { return message; }
    public int getValue() { return value; }
    public Vector3d getPosition() { return position; }
}
```

### Register Custom Packet

```java
@Override
protected void setup() {
    PacketRegistry.register(
        MyCustomPacket.ID,
        MyCustomPacket.class,
        MyCustomPacket::new,  // Deserializer
        MyCustomPacket::validate  // Optional validator
    );
}

// Optional validation
public static boolean validate(ByteBuf buffer) {
    // Quick validation without full parse
    return buffer.readableBytes() >= 28; // Minimum size
}
```

## PacketIO Utilities

### Writing Data

```java
// Primitives
buffer.writeByte(value);
buffer.writeShort(value);
buffer.writeInt(value);
buffer.writeLong(value);
buffer.writeFloat(value);
buffer.writeDouble(value);
buffer.writeBoolean(value);

// Strings
PacketIO.writeString(buffer, string);

// Variable-length integers
VarInt.write(buffer, value);

// Collections
PacketIO.writeArray(buffer, items, PacketIO::writeString);

// UUIDs
PacketIO.writeUUID(buffer, uuid);

// Vectors
PacketIO.writeVector3d(buffer, vector);
PacketIO.writeVector3i(buffer, blockPos);

// Optional values (nullable)
PacketIO.writeOptional(buffer, value, PacketIO::writeString);
```

### Reading Data

```java
// Primitives
byte b = buffer.readByte();
short s = buffer.readShort();
int i = buffer.readInt();
long l = buffer.readLong();
float f = buffer.readFloat();
double d = buffer.readDouble();
boolean bool = buffer.readBoolean();

// Strings
String str = PacketIO.readString(buffer);

// Variable-length integers
int var = VarInt.read(buffer);

// Collections
List<String> items = PacketIO.readArray(buffer, PacketIO::readString);

// UUIDs
UUID uuid = PacketIO.readUUID(buffer);

// Vectors
Vector3d pos = PacketIO.readVector3d(buffer);
Vector3i blockPos = PacketIO.readVector3i(buffer);

// Optional values
String optional = PacketIO.readOptional(buffer, PacketIO::readString);
```

## Compression

Large packets are automatically compressed using Zstd:

```java
public class LargeDataPacket implements Packet {
    public static final boolean IS_COMPRESSED = true;
    
    private final byte[] data;
    
    @Override
    public void serialize(ByteBuf buffer) {
        // Data will be automatically compressed if IS_COMPRESSED = true
        buffer.writeBytes(data);
    }
}
```

Manual compression:

```java
// Compress
byte[] compressed = PacketIO.compress(data);

// Decompress
byte[] decompressed = PacketIO.decompress(compressed);
```

## Client-Bound Custom UI

### Custom Page Packet

Send custom UI pages to clients:

```java
public void showCustomUI(Player player, String pageId, Map<String, Object> data) {
    CustomPage page = new CustomPage(
        pageId,
        serializeData(data)
    );
    player.getConnection().send(page);
}
```

### Window System

```java
// Open custom window
OpenWindow openWindow = new OpenWindow(
    windowId,
    "MyPlugin:CustomWindow",
    windowData
);
player.getConnection().send(openWindow);

// Handle window actions
handler.registerHandler(SendWindowAction.ID, packet -> {
    SendWindowAction action = (SendWindowAction) packet;
    int windowId = action.getWindowId();
    String actionType = action.getActionType();
    
    processWindowAction(player, windowId, actionType, action.getData());
});

// Close window
CloseWindow closeWindow = new CloseWindow(windowId);
player.getConnection().send(closeWindow);
```

## Handling Client Input

### Mouse Interaction

```java
handler.registerHandler(MouseInteraction.ID, packet -> {
    MouseInteraction interaction = (MouseInteraction) packet;
    
    MouseButton button = interaction.getButton();
    Vector3d hitPos = interaction.getHitPosition();
    Vector3i blockPos = interaction.getBlockPosition();
    int entityId = interaction.getEntityId();
    
    if (button == MouseButton.RIGHT) {
        handleRightClick(player, hitPos, blockPos, entityId);
    } else if (button == MouseButton.LEFT) {
        handleLeftClick(player, hitPos, blockPos, entityId);
    }
});
```

### Movement

```java
handler.registerHandler(ClientMovement.ID, packet -> {
    ClientMovement movement = (ClientMovement) packet;
    
    Vector3d position = movement.getPosition();
    Vector3f rotation = movement.getRotation();
    Vector3d velocity = movement.getVelocity();
    boolean onGround = movement.isOnGround();
    
    validateMovement(player, position, velocity);
});
```

### Key Input

```java
handler.registerHandler(KeyInputPacket.ID, packet -> {
    KeyInputPacket input = (KeyInputPacket) packet;
    
    int keyCode = input.getKeyCode();
    boolean pressed = input.isPressed();
    
    handleKeyInput(player, keyCode, pressed);
});
```

## Rate Limiting

Protect against packet spam:

```java
public class RateLimitedHandler implements SubPacketHandler {
    private final Map<UUID, RateLimiter> limiters = new ConcurrentHashMap<>();
    
    @Override
    public void registerHandlers(IPacketHandler handler) {
        handler.registerHandler(MyPacket.ID, this::handleWithRateLimit);
    }
    
    private void handleWithRateLimit(Packet packet) {
        Player player = getPacketSender();
        RateLimiter limiter = limiters.computeIfAbsent(
            player.getUUID(), 
            k -> new RateLimiter(10, 1000) // 10 per second
        );
        
        if (!limiter.tryAcquire()) {
            getLogger().atWarning().log("Rate limit exceeded for %s", player.getName());
            return;
        }
        
        processPacket(packet);
    }
}
```

## Error Handling

```java
handler.registerHandler(MyPacket.ID, packet -> {
    try {
        processPacket(packet);
    } catch (Exception e) {
        getLogger().atSevere().withCause(e).log("Error processing packet");
        
        // Optionally disconnect on critical errors
        if (e instanceof CriticalPacketError) {
            player.disconnect("Protocol error");
        }
    }
});
```

## Packet Validation

```java
public class ValidatedPacket implements Packet {
    @Override
    public void serialize(ByteBuf buffer) {
        // Add checksum
        int checksum = computeChecksum();
        buffer.writeInt(checksum);
        // Write data
    }
    
    public static ValidatedPacket deserialize(ByteBuf buffer) {
        int checksum = buffer.readInt();
        // Read data
        ValidatedPacket packet = new ValidatedPacket(...);
        
        if (packet.computeChecksum() != checksum) {
            throw new PacketValidationException("Checksum mismatch");
        }
        
        return packet;
    }
}
```

## Performance Tips

### Packet Batching

```java
public class PacketBatcher {
    private final List<Packet> pending = new ArrayList<>();
    private final Player player;
    
    public void queue(Packet packet) {
        pending.add(packet);
    }
    
    public void flush() {
        if (pending.isEmpty()) return;
        
        // Send as batch if supported
        BatchPacket batch = new BatchPacket(pending);
        player.getConnection().send(batch);
        pending.clear();
    }
}
```

### Delta Compression

Only send changes:

```java
public class EntityStateSync {
    private final Map<Integer, EntityState> lastSent = new HashMap<>();
    
    public void sync(Player player, List<Entity> entities) {
        List<EntityDelta> deltas = new ArrayList<>();
        
        for (Entity entity : entities) {
            EntityState current = captureState(entity);
            EntityState last = lastSent.get(entity.getId());
            
            if (last == null || !current.equals(last)) {
                deltas.add(computeDelta(last, current));
                lastSent.put(entity.getId(), current);
            }
        }
        
        if (!deltas.isEmpty()) {
            player.getConnection().send(new EntityDeltaPacket(deltas));
        }
    }
}
```

### Lazy Serialization

```java
public class LazyPacket implements Packet {
    private ByteBuf cached;
    
    @Override
    public void serialize(ByteBuf buffer) {
        if (cached == null) {
            cached = Unpooled.buffer();
            doSerialize(cached);
        }
        buffer.writeBytes(cached.duplicate());
    }
}
```

## Troubleshooting

### Packet Not Received

1. Verify packet ID is registered
2. Check handler is registered
3. Ensure packet is properly serialized
4. Check for exceptions in handler

### Deserialization Errors

1. Verify read order matches write order
2. Check data type sizes
3. Validate buffer has enough bytes
4. Add bounds checking

### Connection Drops

1. Check for unhandled exceptions
2. Verify packet size limits
3. Monitor bandwidth usage
4. Check ping/timeout settings

See `references/packet-list.md` for complete packet catalog.
See `references/serialization.md` for serialization patterns.
