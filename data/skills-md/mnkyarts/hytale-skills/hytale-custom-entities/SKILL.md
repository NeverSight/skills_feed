---
name: hytale-custom-entities
description: Create custom entities and NPCs for Hytale with AI behaviors, components, spawning, and animations. Use when asked to "create a custom entity", "add an NPC", "make a mob", "design AI behavior", or "configure entity spawning".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Creating Custom Hytale Entities

Complete guide for defining custom entities with AI, components, spawning, and animations.

## When to use this skill

Use this skill when:
- Creating new entity types (mobs, NPCs, creatures)
- Designing AI behaviors with sensors and actions
- Setting up entity spawning rules
- Adding custom entity components
- Configuring entity animations and models
- Creating interactive NPCs

## Entity Architecture Overview

Hytale uses an ECS (Entity Component System) architecture:

- **Entity**: Container with unique ID
- **Components**: Data attached to entities
- **Systems**: Logic that processes components

### Entity Hierarchy

```
Entity
├── LivingEntity (has health, inventory, stats)
│   ├── Player
│   └── NPCEntity (has AI role, pathfinding)
├── BlockEntity (block-attached entities)
├── ProjectileEntity
└── ItemEntity (dropped items)
```

## Entity Asset Structure

```
my-plugin/
└── assets/
    └── Server/
        └── Content/
            ├── Entities/
            │   └── my_creature.entity
            ├── Roles/
            │   └── my_creature_role.role
            └── Spawns/
                └── my_creature_spawn.spawn
```

## Basic Entity Definition

**File**: `my_creature.entity`

```json
{
  "DisplayName": {
    "en-US": "Custom Creature"
  },
  "Model": "MyPlugin/Models/custom_creature",
  "Health": 20,
  "MovementSpeed": 1.0,
  "Role": "MyPlugin:CustomCreatureRole",
  "Tags": {
    "Type": ["Monster", "Hostile"]
  }
}
```

## Entity Properties Reference

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `DisplayName` | LocalizedString | Entity name |
| `Model` | String | Model asset reference |
| `Health` | Float | Maximum health |
| `Role` | String | AI role reference |
| `Team` | String | Team/faction ID |
| `Tags` | Object | Classification tags |

### Physical Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `MovementSpeed` | Float | 1.0 | Base move speed |
| `BoundingBox` | Object | auto | Collision box |
| `Mass` | Float | 1.0 | Physics mass |
| `Gravity` | Float | 1.0 | Gravity multiplier |
| `CanSwim` | Boolean | false | Can swim in water |
| `CanFly` | Boolean | false | Can fly |
| `StepHeight` | Float | 0.5 | Max step-up height |

### Combat Properties

| Property | Type | Description |
|----------|------|-------------|
| `AttackDamage` | Float | Base attack damage |
| `AttackSpeed` | Float | Attacks per second |
| `AttackRange` | Float | Melee attack range |
| `Armor` | Float | Damage reduction |
| `KnockbackResistance` | Float | Knockback reduction |

### Visual Properties

| Property | Type | Description |
|----------|------|-------------|
| `Scale` | Float | Model scale |
| `RenderDistance` | Float | Max render distance |
| `ShadowSize` | Float | Shadow radius |
| `GlowColor` | Color | Outline glow color |
| `Particles` | String | Ambient particles |

## AI Role System

NPCs are controlled by **Roles** containing **Instructions** with:
- **Sensors**: Conditions for activation
- **BodyMotion**: Movement behavior
- **HeadMotion**: Look behavior
- **Actions**: Effects to execute

### Basic Role Definition

**File**: `my_creature_role.role`

```json
{
  "MotionController": "Walk",
  "DefaultInstruction": {
    "Sensor": {
      "Type": "Always"
    },
    "BodyMotion": {
      "Type": "Wander",
      "Speed": 0.5,
      "Radius": 10
    },
    "HeadMotion": {
      "Type": "Nothing"
    }
  },
  "Instructions": [
    {
      "Priority": 10,
      "Sensor": {
        "Type": "SensorPlayer",
        "Range": 15,
        "Condition": "Visible"
      },
      "BodyMotion": {
        "Type": "Pursue",
        "Target": "Player",
        "Speed": 1.0
      },
      "HeadMotion": {
        "Type": "Watch",
        "Target": "Player"
      },
      "Actions": [
        {
          "Type": "Attack",
          "Range": 2.0,
          "Damage": 5,
          "Cooldown": 1.0
        }
      ]
    }
  ]
}
```

### Motion Controllers

| Controller | Description |
|------------|-------------|
| `Walk` | Ground-based movement |
| `Fly` | Aerial movement |
| `Dive` | Swimming movement |
| `Hover` | Stationary flight |

### Sensor Types

| Sensor | Description | Parameters |
|--------|-------------|------------|
| `Always` | Always true | - |
| `Never` | Always false | - |
| `Random` | Random chance | `Chance` |
| `SensorPlayer` | Detect players | `Range`, `Condition` |
| `SensorEntity` | Detect entities | `Range`, `EntityType`, `Tags` |
| `SensorDamage` | When damaged | `Threshold` |
| `SensorHealth` | Health check | `Below`, `Above` |
| `SensorTime` | Time of day | `DayTime`, `NightTime` |
| `SensorNav` | Navigation state | `HasPath`, `AtDestination` |
| `SensorDistance` | Distance check | `Target`, `Min`, `Max` |

### Body Motion Types

| Motion | Description | Parameters |
|--------|-------------|------------|
| `Wander` | Random wandering | `Speed`, `Radius`, `IdleTime` |
| `Pursue` | Chase target | `Target`, `Speed`, `StopDistance` |
| `Flee` | Run from target | `Target`, `Speed`, `SafeDistance` |
| `MoveTo` | Go to position | `Position`, `Speed` |
| `MoveAway` | Move away | `Target`, `Distance` |
| `Patrol` | Follow path | `Waypoints`, `Speed` |
| `Circle` | Circle target | `Target`, `Radius`, `Speed` |
| `Stay` | Don't move | - |
| `TakeOff` | Start flying | - |
| `Land` | Stop flying | - |
| `Teleport` | Instant move | `Position` |

### Head Motion Types

| Motion | Description | Parameters |
|--------|-------------|------------|
| `Watch` | Look at target | `Target` |
| `Aim` | Aim at target | `Target`, `Offset` |
| `Look` | Look direction | `Direction` |
| `Nothing` | Don't control head | - |

### Action Types

| Action | Description | Parameters |
|--------|-------------|------------|
| `Attack` | Melee attack | `Damage`, `Range`, `Cooldown` |
| `RangedAttack` | Projectile attack | `Projectile`, `Speed`, `Cooldown` |
| `ApplyEntityEffect` | Apply effect | `Effect`, `Duration`, `Target` |
| `PlaySound` | Play sound | `Sound`, `Volume` |
| `SpawnEntity` | Spawn entity | `Entity`, `Count` |
| `SetStat` | Modify stat | `Stat`, `Value` |
| `SetFlag` | Set flag | `Flag`, `Value` |
| `Notify` | Trigger event | `Event`, `Data` |
| `Wait` | Delay | `Duration` |

## Complex AI Example

**Aggressive mob with multiple behaviors**:

```json
{
  "MotionController": "Walk",
  "CombatRange": 2.0,
  "AggroRange": 20,
  "LeashRange": 40,
  
  "DefaultInstruction": {
    "Sensor": { "Type": "Always" },
    "BodyMotion": {
      "Type": "Wander",
      "Speed": 0.4,
      "Radius": 15,
      "IdleTime": { "Min": 2, "Max": 5 }
    },
    "HeadMotion": { "Type": "Nothing" }
  },
  
  "Instructions": [
    {
      "Name": "ReturnToLeash",
      "Priority": 100,
      "Sensor": {
        "Type": "SensorDistance",
        "Target": "LeashPosition",
        "Min": 40
      },
      "BodyMotion": {
        "Type": "MoveTo",
        "Target": "LeashPosition",
        "Speed": 1.5
      }
    },
    {
      "Name": "AttackPlayer",
      "Priority": 50,
      "Sensor": {
        "Type": "And",
        "Sensors": [
          {
            "Type": "SensorPlayer",
            "Range": 2.5,
            "Condition": "Visible"
          },
          {
            "Type": "SensorCooldown",
            "Cooldown": "AttackCooldown",
            "Ready": true
          }
        ]
      },
      "BodyMotion": { "Type": "Stay" },
      "HeadMotion": {
        "Type": "Aim",
        "Target": "Player"
      },
      "Actions": [
        {
          "Type": "Attack",
          "Damage": 8,
          "Animation": "attack_swing"
        },
        {
          "Type": "SetCooldown",
          "Cooldown": "AttackCooldown",
          "Duration": 1.5
        }
      ]
    },
    {
      "Name": "ChasePlayer",
      "Priority": 40,
      "Sensor": {
        "Type": "SensorPlayer",
        "Range": 20,
        "Condition": "Visible"
      },
      "BodyMotion": {
        "Type": "Pursue",
        "Target": "Player",
        "Speed": 1.0,
        "StopDistance": 1.5
      },
      "HeadMotion": {
        "Type": "Watch",
        "Target": "Player"
      }
    },
    {
      "Name": "FleeWhenLow",
      "Priority": 60,
      "Sensor": {
        "Type": "And",
        "Sensors": [
          { "Type": "SensorHealth", "Below": 0.25 },
          { "Type": "SensorPlayer", "Range": 15 }
        ]
      },
      "BodyMotion": {
        "Type": "Flee",
        "Target": "Player",
        "Speed": 1.3,
        "SafeDistance": 25
      }
    }
  ]
}
```

## Entity Spawning

Define where and when entities spawn:

### Spawn Point Configuration

**File**: `my_creature_spawn.spawn`

```json
{
  "Entity": "MyPlugin:CustomCreature",
  "SpawnWeight": 10,
  "GroupSize": { "Min": 1, "Max": 3 },
  "SpawnConditions": {
    "Biomes": ["Plains", "Forest"],
    "TimeOfDay": {
      "Start": 0.75,
      "End": 0.25
    },
    "LightLevel": { "Max": 7 },
    "MoonPhase": ["Full", "Waning"],
    "Weather": ["Clear", "Cloudy"],
    "Surface": true
  },
  "SpawnCooldown": 300,
  "MaxNearby": 4,
  "NearbyCheckRadius": 32
}
```

### Spawn Beacon (Block-based spawning)

```json
{
  "Type": "Beacon",
  "Entity": "MyPlugin:CustomCreature",
  "SpawnRadius": 10,
  "SpawnInterval": 100,
  "MaxSpawns": 5,
  "DespawnDistance": 64,
  "RequiredBlock": "MyPlugin:SpawnerBlock"
}
```

## Custom Entity Components

Create custom data components:

### Component Definition

```java
public class MyEntityData implements Component<EntityStore> {
    public static final BuilderCodec<MyEntityData> CODEC = BuilderCodec.builder(
        Codec.INT.required().fieldOf("Level"),
        Codec.STRING.optionalFieldOf("CustomName", ""),
        Codec.BOOL.optionalFieldOf("IsEnraged", false)
    ).constructor(MyEntityData::new);
    
    private int level;
    private String customName;
    private boolean isEnraged;
    
    public MyEntityData() {
        this(1, "", false);
    }
    
    public MyEntityData(int level, String customName, boolean isEnraged) {
        this.level = level;
        this.customName = customName;
        this.isEnraged = isEnraged;
    }
    
    // Getters and setters
    public int getLevel() { return level; }
    public void setLevel(int level) { this.level = level; }
    public String getCustomName() { return customName; }
    public void setCustomName(String name) { this.customName = name; }
    public boolean isEnraged() { return isEnraged; }
    public void setEnraged(boolean enraged) { this.isEnraged = enraged; }
}
```

### Component Registration

```java
@Override
protected void setup() {
    ComponentType<EntityStore, MyEntityData> myDataType = 
        getEntityStoreRegistry().registerComponent(
            MyEntityData.class,
            "myPluginEntityData",
            MyEntityData.CODEC
        );
}
```

## Custom Entity Systems

Process entities with matching components:

### Tick System

```java
public class EnrageSystem extends TickSystem<EntityStore> {
    private ComponentAccess<EntityStore, MyEntityData> myData;
    private ComponentAccess<EntityStore, HealthComponent> health;
    
    @Override
    protected void register(Store<EntityStore> store) {
        myData = registerComponent(MyEntityData.class);
        health = registerComponent(HealthComponent.class);
    }
    
    @Override
    public void tick(
        int index,
        ArchetypeChunk<EntityStore> chunk,
        Store<EntityStore> store,
        CommandBuffer<EntityStore> buffer
    ) {
        MyEntityData data = myData.get(chunk, index);
        HealthComponent hp = health.getOptional(chunk, index);
        
        if (hp != null && hp.getPercent() < 0.25f && !data.isEnraged()) {
            data.setEnraged(true);
            // Apply enrage buff
        }
    }
}
```

### Event System

```java
public class MyDamageHandler extends EntityEventSystem<EntityStore, Damage> {
    private ComponentAccess<EntityStore, MyEntityData> myData;
    
    public MyDamageHandler() {
        super(Damage.class);
    }
    
    @Override
    protected void register(Store<EntityStore> store) {
        myData = registerComponent(MyEntityData.class);
    }
    
    @Override
    public void handle(
        int index,
        ArchetypeChunk<EntityStore> chunk,
        Store<EntityStore> store,
        CommandBuffer<EntityStore> buffer,
        Damage damage
    ) {
        MyEntityData data = myData.getOptional(chunk, index);
        if (data != null && data.isEnraged()) {
            // Reduce damage when enraged
            damage.setAmount(damage.getAmount() * 0.5f);
        }
    }
}
```

## Entity Registration in Plugin

```java
@Override
protected void setup() {
    // Register components
    ComponentType<EntityStore, MyEntityData> dataType = 
        getEntityStoreRegistry().registerComponent(
            MyEntityData.class,
            "myEntityData", 
            MyEntityData.CODEC
        );
    
    // Register systems
    getEntityStoreRegistry().registerSystem(new EnrageSystem());
    getEntityStoreRegistry().registerSystem(new MyDamageHandler());
    
    // Register custom sensors
    getCodecRegistry(Sensor.CODEC).register(
        "MySensor", MySensor.class, MySensor.CODEC
    );
    
    // Register custom actions
    getCodecRegistry(Action.CODEC).register(
        "MyAction", MyAction.class, MyAction.CODEC
    );
}
```

## NPC Interactions

Create interactive NPCs:

```json
{
  "DisplayName": { "en-US": "Village Merchant" },
  "Model": "MyPlugin/Models/merchant",
  "Role": "MyPlugin:MerchantRole",
  "IsInteractable": true,
  "Interactions": {
    "Use": "MyPlugin:OpenShop"
  },
  "DialogueTree": "MyPlugin:MerchantDialogue",
  "Schedule": {
    "06:00-18:00": "WorkAtShop",
    "18:00-22:00": "Wander",
    "22:00-06:00": "Sleep"
  }
}
```

## Complete Example: Boss Entity

```json
{
  "DisplayName": {
    "en-US": "Shadow Guardian"
  },
  "Description": {
    "en-US": "Ancient protector of the dark temple"
  },
  "Model": "MyPlugin/Models/shadow_guardian",
  "Scale": 2.0,
  "Health": 500,
  "Armor": 10,
  "AttackDamage": 20,
  "MovementSpeed": 0.8,
  "KnockbackResistance": 0.8,
  "Role": "MyPlugin:ShadowGuardianRole",
  "BossBar": {
    "Enabled": true,
    "Color": "Purple",
    "Style": "Notched"
  },
  "Loot": "MyPlugin:ShadowGuardianLoot",
  "DeathSound": "MyPlugin/Sounds/boss_death",
  "AmbientSound": {
    "Sound": "MyPlugin/Sounds/dark_ambient",
    "Interval": 5
  },
  "Particles": "MyPlugin/Particles/shadow_aura",
  "GlowColor": { "R": 0.5, "G": 0.0, "B": 0.8 },
  "Tags": {
    "Type": ["Boss", "Undead", "Hostile"]
  }
}
```

## Troubleshooting

### Entity Not Spawning

1. Check spawn conditions match environment
2. Verify spawn weight is > 0
3. Check MaxNearby limit
4. Ensure biome/time conditions are met

### AI Not Working

1. Verify Role reference is correct
2. Check sensor conditions are achievable
3. Ensure instruction priorities are ordered
4. Debug with `/npc debug` command

### Components Not Saving

1. Ensure CODEC is defined correctly
2. Register with unique string ID
3. Check serialization in logs

See `references/entity-components.md` for built-in components.
See `references/ai-sensors.md` for all sensor types.
See `references/ai-actions.md` for all action types.
