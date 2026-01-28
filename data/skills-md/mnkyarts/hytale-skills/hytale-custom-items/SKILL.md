---
name: hytale-custom-items
description: Create custom items for Hytale including tools, weapons, armor, consumables, and special items. Use when asked to "add a custom item", "create a weapon", "make armor", "add a tool", or "create consumable items".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Creating Custom Hytale Items

Complete guide for defining custom items with tools, weapons, armor, and special abilities.

## When to use this skill

Use this skill when:
- Creating new item types
- Making custom weapons with stats
- Designing armor sets
- Creating tools for gathering
- Adding consumable items
- Defining item interactions
- Setting up item crafting recipes

## Item Asset Structure

Items are defined as JSON assets in your plugin's asset pack:

```
my-plugin/
└── assets/
    └── Server/
        └── Content/
            └── Items/
                ├── my_sword.item
                ├── my_armor.item
                └── my_tool.item
```

## Basic Item Definition

**File**: `my_item.item`

```json
{
  "DisplayName": {
    "en-US": "Custom Item"
  },
  "Description": {
    "en-US": "A mysterious custom item"
  },
  "Icon": "MyPlugin/Icons/custom_item",
  "MaxStack": 64,
  "Categories": ["MyPlugin:Miscellaneous"],
  "Tags": {
    "Type": ["Resource"]
  }
}
```

## Item Properties Reference

### Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `DisplayName` | LocalizedString | - | Localized item name |
| `Description` | LocalizedString | - | Localized description |
| `Parent` | String | - | Inherit from another item |
| `Icon` | String | - | Icon texture path |
| `Model` | String | - | 3D model for held item |
| `MaxStack` | Integer | 64 | Maximum stack size |
| `MaxDurability` | Integer | 0 | Durability (0 = infinite) |
| `Categories` | Array | [] | Item category references |
| `Tags` | Object | {} | Category tags |

### Visual Properties

| Property | Type | Description |
|----------|------|-------------|
| `Texture` | String | Item texture |
| `Scale` | Float | Model scale |
| `Animation` | String | Item animation set |
| `Particles` | String | Held particle effect |
| `Trail` | String | Swing trail effect |
| `Light` | Object | Light emission settings |

### Behavior Properties

| Property | Type | Description |
|----------|------|-------------|
| `Rarity` | Enum | `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary` |
| `BlockId` | String | Block to place (for placeable items) |
| `Interactions` | Object | Interaction type mappings |
| `CanDrop` | Boolean | Can be dropped |
| `DestroyOnDeath` | Boolean | Lost on player death |

## Tool Items

Create tools for gathering resources:

```json
{
  "DisplayName": { "en-US": "Mythril Pickaxe" },
  "Icon": "MyPlugin/Icons/mythril_pickaxe",
  "Model": "MyPlugin/Models/mythril_pickaxe",
  "MaxDurability": 1500,
  "Rarity": "Rare",
  "Tool": {
    "Specs": [
      {
        "GatherType": "Pickaxe",
        "Power": 5,
        "Quality": 4
      }
    ],
    "Speed": 1.5,
    "DurabilityLossPerUse": 1,
    "Efficiency": 1.2
  },
  "Tags": {
    "Type": ["Tool", "Pickaxe"]
  }
}
```

### Tool Spec Properties

| Property | Type | Description |
|----------|------|-------------|
| `GatherType` | Enum | `Pickaxe`, `Axe`, `Shovel`, `Hoe`, `Shears` |
| `Power` | Integer | Mining power level |
| `Quality` | Integer | Material quality level |

### Tool Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Speed` | Float | 1.0 | Mining speed multiplier |
| `DurabilityLossPerUse` | Integer | 1 | Durability cost per block |
| `Efficiency` | Float | 1.0 | Efficiency multiplier |
| `SilkTouch` | Boolean | false | Drop blocks directly |
| `Fortune` | Integer | 0 | Drop multiplier level |

## Weapon Items

Create melee and ranged weapons:

### Melee Weapon

```json
{
  "DisplayName": { "en-US": "Shadow Blade" },
  "Icon": "MyPlugin/Icons/shadow_blade",
  "Model": "MyPlugin/Models/shadow_blade",
  "MaxDurability": 500,
  "Rarity": "Epic",
  "Weapon": {
    "Type": "Sword",
    "AttackDamage": 12,
    "AttackSpeed": 1.6,
    "Knockback": 0.4,
    "CriticalChance": 0.15,
    "CriticalMultiplier": 1.5,
    "DurabilityLossOnHit": 1,
    "DualWield": false,
    "StatModifiers": {
      "Strength": 2,
      "Speed": 0.1
    },
    "DamageType": "Slashing",
    "Enchantable": true
  },
  "Trail": "MyPlugin/Trails/shadow_swing",
  "Animation": "MyPlugin/Animations/sword",
  "Tags": {
    "Type": ["Weapon", "Sword", "Melee"]
  }
}
```

### Ranged Weapon

```json
{
  "DisplayName": { "en-US": "Frost Bow" },
  "Icon": "MyPlugin/Icons/frost_bow",
  "Model": "MyPlugin/Models/frost_bow",
  "MaxDurability": 384,
  "Weapon": {
    "Type": "Bow",
    "AttackDamage": 8,
    "DrawTime": 1.0,
    "ProjectileSpeed": 3.0,
    "Projectile": "MyPlugin:FrostArrow",
    "Accuracy": 0.95,
    "AmmoType": "Hytale:Arrow",
    "InfiniteAmmo": false,
    "StatModifiers": {
      "Dexterity": 1
    }
  },
  "Animation": "MyPlugin/Animations/bow"
}
```

### Weapon Types

| Type | Description |
|------|-------------|
| `Sword` | Standard melee |
| `Axe` | Heavy melee |
| `Spear` | Long reach melee |
| `Dagger` | Fast melee |
| `Mace` | Blunt melee |
| `Bow` | Ranged, requires ammo |
| `Crossbow` | Ranged, slower |
| `Wand` | Magic ranged |
| `Staff` | Magic ranged |
| `Thrown` | Throwable weapon |

### Damage Types

| Type | Description |
|------|-------------|
| `Physical` | Default damage |
| `Slashing` | Cutting damage |
| `Piercing` | Stabbing damage |
| `Blunt` | Impact damage |
| `Fire` | Fire damage |
| `Ice` | Cold damage |
| `Lightning` | Electric damage |
| `Magic` | Arcane damage |
| `Poison` | Toxic damage |
| `True` | Ignores armor |

## Armor Items

Create armor with protection stats:

```json
{
  "DisplayName": { "en-US": "Dragon Scale Chestplate" },
  "Icon": "MyPlugin/Icons/dragon_chestplate",
  "Model": "MyPlugin/Models/dragon_chestplate",
  "MaxDurability": 528,
  "Rarity": "Legendary",
  "Armor": {
    "Slot": "Chest",
    "Defense": 8,
    "Toughness": 3,
    "DamageResistance": {
      "Fire": 0.5,
      "Physical": 0.2
    },
    "StatModifiers": {
      "Health": 20,
      "FireResistance": 50
    },
    "SetBonus": {
      "SetId": "MyPlugin:DragonScale",
      "RequiredPieces": 4,
      "Bonuses": {
        "FireImmunity": true,
        "FlyAbility": true
      }
    }
  },
  "Tags": {
    "Type": ["Armor", "Chest"]
  }
}
```

### Armor Slots

| Slot | Coverage |
|------|----------|
| `Head` | Helmet |
| `Chest` | Chestplate |
| `Legs` | Leggings |
| `Feet` | Boots |
| `Offhand` | Shield |
| `Accessory` | Ring, Amulet |

### Armor Properties

| Property | Type | Description |
|----------|------|-------------|
| `Defense` | Integer | Base armor points |
| `Toughness` | Float | Damage reduction scaling |
| `DamageResistance` | Object | Per-damage-type reduction |
| `StatModifiers` | Object | Stat bonuses when worn |
| `SetBonus` | Object | Multi-piece set bonuses |
| `EquipSound` | String | Sound on equip |
| `SpecialAbility` | String | Active ability reference |

## Consumable Items

Create food, potions, and usable items:

### Food Item

```json
{
  "DisplayName": { "en-US": "Healing Berries" },
  "Icon": "MyPlugin/Icons/healing_berries",
  "MaxStack": 32,
  "Utility": {
    "Type": "Food",
    "ConsumeTime": 1.0,
    "Nutrition": 4,
    "Saturation": 2.5,
    "Effects": [
      {
        "Effect": "Hytale:Regeneration",
        "Duration": 10,
        "Amplifier": 1
      }
    ],
    "ConsumeSound": "Hytale/Sounds/eat",
    "ConsumeParticle": "MyPlugin/Particles/heal"
  }
}
```

### Potion Item

```json
{
  "DisplayName": { "en-US": "Potion of Strength" },
  "Icon": "MyPlugin/Icons/strength_potion",
  "MaxStack": 16,
  "Utility": {
    "Type": "Potion",
    "ConsumeTime": 0.5,
    "Effects": [
      {
        "Effect": "Hytale:Strength",
        "Duration": 180,
        "Amplifier": 2
      }
    ],
    "RemoveOnUse": true,
    "ReturnItem": "Hytale:EmptyBottle"
  }
}
```

### Throwable Item

```json
{
  "DisplayName": { "en-US": "Fire Bomb" },
  "Icon": "MyPlugin/Icons/fire_bomb",
  "MaxStack": 16,
  "Utility": {
    "Type": "Thrown",
    "ThrowSpeed": 1.5,
    "Projectile": "MyPlugin:FireBombProjectile",
    "RemoveOnUse": true,
    "Cooldown": 0.5
  }
}
```

## Special Items

### Placeable Item

```json
{
  "DisplayName": { "en-US": "Torch" },
  "Icon": "MyPlugin/Icons/torch",
  "MaxStack": 64,
  "BlockId": "MyPlugin:TorchBlock",
  "PlaceSound": "Hytale/Sounds/place_torch"
}
```

### Container Item

```json
{
  "DisplayName": { "en-US": "Backpack" },
  "Icon": "MyPlugin/Icons/backpack",
  "MaxStack": 1,
  "Container": {
    "Slots": 27,
    "AllowNesting": false,
    "PickupOnBreak": true
  }
}
```

### Glider Item

```json
{
  "DisplayName": { "en-US": "Glider Wings" },
  "Icon": "MyPlugin/Icons/glider",
  "MaxDurability": 200,
  "Glider": {
    "GlideSpeed": 1.2,
    "FallSpeed": 0.08,
    "Maneuverability": 1.0,
    "Model": "MyPlugin/Models/glider_wings",
    "DurabilityLossPerSecond": 1
  }
}
```

## Item Interactions

Define custom use behaviors:

```json
{
  "Interactions": {
    "Use": "MyPlugin:MyItemUse",
    "UseOnBlock": "MyPlugin:MyItemUseOnBlock",
    "UseOnEntity": "MyPlugin:MyItemUseOnEntity",
    "Attack": "MyPlugin:MyItemAttack"
  }
}
```

### Interaction in Java

```java
public class MyItemInteraction extends Interaction {
    public static final BuilderCodec<MyItemInteraction> CODEC = BuilderCodec.builder(
        Codec.INT.optionalFieldOf("Power", 10)
    ).constructor(MyItemInteraction::new);
    
    private final int power;
    
    public MyItemInteraction(int power) {
        this.power = power;
    }
    
    @Override
    public InteractionResult interact(InteractionContext context) {
        // Custom interaction logic
        Player player = context.getPlayer();
        player.sendMessage("Used item with power: " + power);
        return InteractionResult.SUCCESS;
    }
}

// Register in plugin setup
@Override
protected void setup() {
    getCodecRegistry(Interaction.CODEC).register(
        "MyItemUse", 
        MyItemInteraction.class, 
        MyItemInteraction.CODEC
    );
}
```

## Crafting Recipes

### Shaped Recipe

```json
{
  "Type": "Shaped",
  "Pattern": [
    "MMM",
    " S ",
    " S "
  ],
  "Key": {
    "M": { "Item": "MyPlugin:MythrilIngot" },
    "S": { "Item": "Hytale:Stick" }
  },
  "Result": {
    "Item": "MyPlugin:MythrilPickaxe",
    "Quantity": 1
  },
  "Category": "MyPlugin:ToolCrafting",
  "RequiredBench": "MyPlugin:Forge"
}
```

### Shapeless Recipe

```json
{
  "Type": "Shapeless",
  "Ingredients": [
    { "Item": "Hytale:Coal", "Quantity": 1 },
    { "Item": "Hytale:Stick", "Quantity": 1 },
    { "Item": "Hytale:GunPowder", "Quantity": 1 }
  ],
  "Result": {
    "Item": "MyPlugin:FireBomb",
    "Quantity": 4
  },
  "Category": "MyPlugin:Alchemy"
}
```

### Smelting Recipe

```json
{
  "Type": "Smelting",
  "Input": { "Item": "MyPlugin:RawMythril" },
  "Result": { "Item": "MyPlugin:MythrilIngot" },
  "ProcessingTime": 200,
  "Experience": 1.0,
  "RequiredBench": "Hytale:Furnace"
}
```

## Complete Example: Magic Staff

```json
{
  "DisplayName": {
    "en-US": "Staff of Lightning"
  },
  "Description": {
    "en-US": "Channels the power of storms"
  },
  "Icon": "MyPlugin/Icons/lightning_staff",
  "Model": "MyPlugin/Models/lightning_staff",
  "MaxStack": 1,
  "MaxDurability": 250,
  "Rarity": "Epic",
  "Weapon": {
    "Type": "Staff",
    "AttackDamage": 5,
    "AttackSpeed": 0.8,
    "DamageType": "Lightning",
    "Projectile": "MyPlugin:LightningBolt",
    "ProjectileSpeed": 5.0,
    "ManaCost": 15,
    "Cooldown": 1.5,
    "StatModifiers": {
      "Intelligence": 5,
      "MagicDamage": 0.2
    }
  },
  "Particles": "MyPlugin/Particles/electric_aura",
  "Light": {
    "Level": 5,
    "Color": { "R": 0.8, "G": 0.9, "B": 1.0 }
  },
  "Animation": "MyPlugin/Animations/staff_cast",
  "Interactions": {
    "Use": "MyPlugin:CastLightning",
    "UseCharged": "MyPlugin:CastChainLightning"
  },
  "Tags": {
    "Type": ["Weapon", "Staff", "Magic"],
    "Element": ["Lightning"]
  }
}
```

## Item Events in Java

```java
@Override
protected void setup() {
    // Listen for item pickup
    getEntityStoreRegistry().registerSystem(new PickupItemHandler());
    
    // Listen for item drop
    getEventRegistry().registerGlobal(DropItemEvent.class, this::onItemDrop);
    
    // Listen for item crafting
    getEventRegistry().registerGlobal(CraftRecipeEvent.class, this::onCraft);
}

private void onItemDrop(DropItemEvent event) {
    ItemStack stack = event.getItemStack();
    if (stack.getItem().getId().equals("MyPlugin:CursedItem")) {
        event.setCancelled(true);
        event.getPlayer().sendMessage("You cannot drop this cursed item!");
    }
}

private void onCraft(CraftRecipeEvent event) {
    CraftingRecipe recipe = event.getRecipe();
    getLogger().atInfo().log("Player crafted: %s", recipe.getResult().getItem().getId());
}
```

## Troubleshooting

### Item Not Appearing

1. Check asset path is correct
2. Verify manifest includes asset pack
3. Check for JSON syntax errors
4. Ensure Icon texture exists

### Tool Not Working

1. Verify `Tool.Specs` is configured
2. Check `GatherType` matches block material
3. Ensure `Power` level is sufficient

### Durability Issues

1. Set `MaxDurability` > 0
2. Configure `DurabilityLossPerUse`
3. Check stack size is 1 for durability items

See `references/item-stats.md` for stat modifier details.
See `references/item-effects.md` for effect reference.
