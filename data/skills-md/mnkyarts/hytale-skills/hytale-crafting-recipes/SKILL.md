---
name: hytale-crafting-recipes
description: Create custom crafting recipes for Hytale plugins including shaped, shapeless, processing, and blueprint recipes. Use when asked to "add crafting recipe", "create recipe", "make craftable item", "add smelting recipe", or "custom crafting".
metadata:
  author: hytale-modding
  version: "1.0.0"
---

# Hytale Crafting Recipes

Complete guide for creating custom crafting recipes including standard crafting, processing (furnace), blueprint, and structural recipes.

## When to use this skill

Use this skill when:
- Adding new crafting recipes for custom items
- Creating processing/smelting recipes
- Implementing blueprint-based crafting
- Setting up recipe requirements and knowledge
- Registering recipes through plugins
- Managing recipe learning/unlocking

## Recipe Architecture Overview

Hytale uses a JSON-based recipe system with multiple bench types. Recipes are defined in asset files and registered through the CraftingPlugin.

### Bench Types

| BenchType | Description | Example |
|-----------|-------------|---------|
| `Crafting` | Standard grid-based crafting | Crafting Table |
| `Processing` | Time-based conversion with fuel | Furnace, Smelter |
| `DiagramCrafting` | Blueprint/schematic crafting | Advanced Workbench |
| `StructuralCrafting` | Multi-block construction | Building Bench |
| `Fieldcraft` | Pocket crafting (no bench) | Player inventory |

### Recipe Flow

```
Recipe JSON → CraftingPlugin → BenchRecipeRegistry → Available in Bench UI
```

## Recipe JSON Format

### Basic Structure

```json
{
  "Input": [...],
  "Output": [...],
  "PrimaryOutput": "hytale:iron_sword",
  "BenchRequirement": [...],
  "TimeSeconds": 0,
  "KnowledgeRequired": false
}
```

### Fields Reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `Input` | Yes | Array | Required materials |
| `Output` | Yes | Array | Resulting items |
| `PrimaryOutput` | No | String | Main output item ID |
| `BenchRequirement` | No | Array | Required bench types |
| `TimeSeconds` | No | Number | Processing time (for Processing type) |
| `KnowledgeRequired` | No | Boolean | Must be learned first |
| `Category` | No | String | Recipe category for UI |

## Material Quantity Format

Materials can be specified in three ways:

### By Item ID

```json
{
  "ItemId": "hytale:iron_ingot",
  "Quantity": 3
}
```

### By Resource Type

```json
{
  "ResourceTypeId": "hytale:ore",
  "Quantity": 2
}
```

### By Item Tag

```json
{
  "ItemTag": "wood_planks",
  "Quantity": 4
}
```

## Standard Crafting Recipes

### Shapeless Recipe

Items can be placed anywhere in the grid:

```json
{
  "Input": [
    { "ItemId": "hytale:iron_ingot", "Quantity": 2 },
    { "ItemId": "hytale:stick", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:iron_sword", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

### Shaped Recipe

Pattern-based placement:

```json
{
  "Pattern": [
    " I ",
    " I ",
    " S "
  ],
  "Key": {
    "I": { "ItemId": "hytale:iron_ingot" },
    "S": { "ItemId": "hytale:stick" }
  },
  "Output": [
    { "ItemId": "hytale:iron_sword", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

### With Categories

```json
{
  "Input": [
    { "ItemId": "hytale:diamond", "Quantity": 2 },
    { "ItemId": "hytale:stick", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:diamond_sword", "Quantity": 1 }
  ],
  "Category": "Weapons",
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

## Fieldcraft (Pocket Crafting)

Recipes available without a bench (2x2 grid):

```json
{
  "Input": [
    { "ItemTag": "log", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:wooden_planks", "Quantity": 4 }
  ],
  "BenchRequirement": [
    { "BenchType": "Fieldcraft" }
  ]
}
```

Fieldcraft recipes are limited to 2x2 grid and simple combinations.

## Processing Recipes (Furnace)

Time-based conversion with fuel requirement:

```json
{
  "Input": [
    { "ItemId": "hytale:iron_ore", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:iron_ingot", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Processing" }
  ],
  "TimeSeconds": 10
}
```

### Processing with Multiple Outputs

```json
{
  "Input": [
    { "ItemId": "hytale:raw_meat", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:cooked_meat", "Quantity": 1 },
    { "ItemId": "hytale:bone", "Quantity": 1, "Chance": 0.25 }
  ],
  "BenchRequirement": [
    { "BenchType": "Processing" }
  ],
  "TimeSeconds": 8
}
```

### Fuel Configuration

Fuel values are defined separately in bench configuration:

```json
{
  "FuelItems": [
    { "ItemId": "hytale:coal", "BurnTime": 1600 },
    { "ItemId": "hytale:wood", "BurnTime": 300 },
    { "ItemTag": "planks", "BurnTime": 200 }
  ]
}
```

## Diagram Crafting (Blueprints)

Complex recipes that require learning:

```json
{
  "Input": [
    { "ItemId": "hytale:refined_iron", "Quantity": 5 },
    { "ItemId": "hytale:leather", "Quantity": 3 },
    { "ItemId": "hytale:ruby", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:enhanced_armor", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "DiagramCrafting" }
  ],
  "KnowledgeRequired": true,
  "DiagramId": "hytale:enhanced_armor_blueprint"
}
```

### Learning Blueprints

Players must learn diagrams before crafting:

```java
// Grant blueprint knowledge
player.getKnowledgeManager().learn("hytale:enhanced_armor_blueprint");

// Check if player knows recipe
boolean knows = player.getKnowledgeManager().hasKnowledge("hytale:enhanced_armor_blueprint");

// Remove knowledge
player.getKnowledgeManager().forget("hytale:enhanced_armor_blueprint");
```

## Structural Crafting

Multi-block construction recipes:

```json
{
  "Input": [
    { "ItemId": "hytale:stone_brick", "Quantity": 20 },
    { "ItemId": "hytale:iron_ingot", "Quantity": 4 },
    { "ItemId": "hytale:wooden_door", "Quantity": 1 }
  ],
  "Output": [
    { "StructureId": "hytale:small_house" }
  ],
  "BenchRequirement": [
    { "BenchType": "StructuralCrafting" }
  ],
  "Preview": "structures/small_house_preview.json"
}
```

## Bench Requirements

Specify which benches can craft the recipe:

### Single Bench Type

```json
"BenchRequirement": [
  { "BenchType": "Crafting" }
]
```

### Multiple Bench Options

```json
"BenchRequirement": [
  { "BenchType": "Crafting" },
  { "BenchType": "DiagramCrafting" }
]
```

### Specific Bench Block

```json
"BenchRequirement": [
  { 
    "BenchType": "Processing",
    "BlockId": "hytale:blast_furnace"
  }
]
```

### Tiered Benches

```json
"BenchRequirement": [
  { 
    "BenchType": "Crafting",
    "MinTier": 2
  }
]
```

## Recipe Registration

### Via JSON Assets

Place recipe files in your plugin's asset pack:

```
assets/
└── Server/
    └── Content/
        └── Recipes/
            ├── crafting/
            │   ├── iron_sword.json
            │   └── iron_pickaxe.json
            ├── processing/
            │   └── iron_smelting.json
            └── diagrams/
                └── enhanced_armor.json
```

### Via Plugin Code

```java
public class MyPlugin extends JavaPlugin {
    
    public MyPlugin(JavaPluginInit init) {
        super(init);
    }
    
    @Override
    protected void setup() {
        // Get the crafting registry
        CraftingRecipeRegistry registry = getCraftingRecipeRegistry();
        
        // Register a recipe programmatically
        CraftingRecipe recipe = CraftingRecipe.builder()
            .input(ItemId.of("hytale:diamond"), 2)
            .input(ItemId.of("hytale:stick"), 1)
            .output(ItemId.of("hytale:diamond_sword"), 1)
            .benchType(BenchType.Crafting)
            .category("Weapons")
            .build();
        
        registry.register(recipe);
    }
}
```

### Recipe Builder API

```java
CraftingRecipe recipe = CraftingRecipe.builder()
    // Input materials
    .input(ItemId.of("hytale:iron_ingot"), 5)
    .input(ItemTag.of("gems"), 2)
    .input(ResourceTypeId.of("hytale:magic_essence"), 1)
    
    // Output items
    .output(ItemId.of("hytale:magic_sword"), 1)
    .secondaryOutput(ItemId.of("hytale:magic_dust"), 1, 0.5f) // 50% chance
    
    // Requirements
    .benchType(BenchType.DiagramCrafting)
    .requiresKnowledge(true)
    .category("Magic Weapons")
    
    // Processing-specific
    .processingTime(Duration.ofSeconds(15))
    
    .build();
```

## Knowledge System

Recipes can require learning before use:

### Recipe with Knowledge Requirement

```json
{
  "Input": [...],
  "Output": [...],
  "KnowledgeRequired": true,
  "KnowledgeId": "mymod:secret_recipe"
}
```

### Managing Player Knowledge

```java
public class KnowledgeManager {
    
    // Teach recipe from item (like recipe book)
    public void teachFromItem(Player player, ItemStack recipeItem) {
        if (recipeItem.is(Items.RECIPE_SCROLL)) {
            String recipeId = recipeItem.getTag().getString("RecipeId");
            player.getKnowledgeManager().learn(recipeId);
            player.sendMessage("Learned: " + recipeId);
            recipeItem.shrink(1);
        }
    }
    
    // Teach recipe from NPC
    public void teachFromNPC(Player player, String recipeId, int cost) {
        if (player.getCurrency() >= cost) {
            player.removeCurrency(cost);
            player.getKnowledgeManager().learn(recipeId);
            player.sendMessage("Purchased recipe knowledge!");
        }
    }
    
    // Check available recipes for player
    public List<CraftingRecipe> getAvailableRecipes(Player player, BenchType bench) {
        return CraftingRecipeRegistry.getRecipes(bench).stream()
            .filter(r -> !r.requiresKnowledge() || 
                        player.getKnowledgeManager().hasKnowledge(r.getKnowledgeId()))
            .toList();
    }
}
```

## Recipe Categories

Organize recipes into categories for UI display:

### Standard Categories

| Category | Description |
|----------|-------------|
| `Tools` | Pickaxes, axes, shovels |
| `Weapons` | Swords, bows, staffs |
| `Armor` | Helmets, chestplates, etc. |
| `Building` | Blocks, decorations |
| `Food` | Consumables, cooking |
| `Materials` | Intermediate crafting materials |
| `Magic` | Enchanted items, potions |
| `Misc` | Everything else |

### Custom Categories

```json
{
  "Input": [...],
  "Output": [...],
  "Category": "MyMod:SpecialItems"
}
```

## Complete Recipe Examples

### Tiered Armor Set

```json
// Iron Helmet
{
  "Pattern": [
    "III",
    "I I"
  ],
  "Key": {
    "I": { "ItemId": "hytale:iron_ingot" }
  },
  "Output": [
    { "ItemId": "hytale:iron_helmet", "Quantity": 1 }
  ],
  "Category": "Armor",
  "BenchRequirement": [
    { "BenchType": "Crafting" }
  ]
}
```

### Processing Chain

```json
// Step 1: Ore to Raw Metal
{
  "Input": [
    { "ItemId": "hytale:iron_ore", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:raw_iron", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Processing", "BlockId": "hytale:crusher" }
  ],
  "TimeSeconds": 5
}

// Step 2: Raw Metal to Ingot
{
  "Input": [
    { "ItemId": "hytale:raw_iron", "Quantity": 2 }
  ],
  "Output": [
    { "ItemId": "hytale:iron_ingot", "Quantity": 1 }
  ],
  "BenchRequirement": [
    { "BenchType": "Processing", "BlockId": "hytale:furnace" }
  ],
  "TimeSeconds": 10
}
```

### Recipe with Chance Outputs

```json
{
  "Input": [
    { "ItemId": "hytale:mysterious_ore", "Quantity": 1 }
  ],
  "Output": [
    { "ItemId": "hytale:iron_ingot", "Quantity": 1 },
    { "ItemId": "hytale:gold_nugget", "Quantity": 1, "Chance": 0.3 },
    { "ItemId": "hytale:diamond", "Quantity": 1, "Chance": 0.05 }
  ],
  "BenchRequirement": [
    { "BenchType": "Processing" }
  ],
  "TimeSeconds": 15
}
```

## Runtime Recipe API

```java
// Get all recipes for a bench type
List<CraftingRecipe> recipes = CraftingRecipeRegistry.getRecipes(BenchType.Crafting);

// Find recipe by output
Optional<CraftingRecipe> recipe = CraftingRecipeRegistry.findByOutput(
    ItemId.of("hytale:diamond_sword")
);

// Check if player can craft
boolean canCraft = recipe.map(r -> r.canCraft(player)).orElse(false);

// Execute craft
if (canCraft) {
    CraftResult result = recipe.get().craft(player);
    if (result.isSuccess()) {
        player.getInventory().addItem(result.getOutput());
    }
}

// Get recipes by category
List<CraftingRecipe> weapons = CraftingRecipeRegistry.getByCategory("Weapons");

// Check materials
boolean hasMaterials = recipe.get().hasRequiredMaterials(player.getInventory());
```

## Best Practices

### Recipe Naming

Use consistent, descriptive IDs:

```
{namespace}:{material}_{item_type}
Examples:
- mymod:iron_sword
- mymod:diamond_pickaxe
- mymod:enchanted_bow
```

### Balance Considerations

- Scale input costs with output power
- Consider processing time for valuable items
- Use knowledge requirements for powerful recipes
- Provide recipe progression (basic → advanced)

### Testing Recipes

```java
// Debug command to test recipes
public class RecipeDebugCommand extends CommandBase {
    
    public RecipeDebugCommand() {
        super("recipedebug", "Debug recipe information");
    }
    
    @Override
    protected void execute(CommandContext ctx) {
        String recipeId = ctx.get(RECIPE_ID);
        Optional<CraftingRecipe> recipe = CraftingRecipeRegistry.get(recipeId);
        
        if (recipe.isEmpty()) {
            ctx.sendError("Recipe not found: " + recipeId);
            return;
        }
        
        CraftingRecipe r = recipe.get();
        ctx.sendMessage("Recipe: " + r.getId());
        ctx.sendMessage("Bench: " + r.getBenchType());
        ctx.sendMessage("Inputs: " + r.getInputs().size());
        ctx.sendMessage("Knowledge Required: " + r.requiresKnowledge());
    }
}
```

## Troubleshooting

### Recipe Not Appearing

1. Check JSON syntax is valid
2. Verify file is in correct asset path
3. Ensure BenchType matches the bench being used
4. Check if KnowledgeRequired and player has knowledge

### Crafting Fails

1. Verify player has all input materials
2. Check material quantities match exactly
3. Ensure item tags are registered
4. Verify bench tier requirements

### Processing Not Starting

1. Check furnace has fuel
2. Verify processing time is set
3. Ensure input slot has correct item
4. Check output slot has space

## Detailed References

For comprehensive documentation:

- `references/recipe-format.md` - Complete JSON schema for all recipe types
- `references/bench-configs.md` - Bench configuration and fuel settings
