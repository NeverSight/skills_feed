---
name: unreal-engine
description: >
  Comprehensive Unreal Engine C++ and Blueprint development assistant with deep project structure understanding.
  Use when helping with Unreal Engine projects, including: C++ gameplay programming, Blueprint development,
  input system configuration (Enhanced Input), Gameplay Ability System (GAS), project structure navigation,
  asset discovery and referencing, plugin integration (experimental/beta), API lookups for underdocumented features,
  and debugging. Triggers on any Unreal Engine development question, especially when working within a .uproject directory.
---

# Unreal Engine Development Assistant

## Core Philosophy: Zero Assumptions

**CRITICAL**: Never make assumptions about the user's project. Every Unreal project is unique in structure, assets, and configuration. Always verify before suggesting code or assets.

## Pre-Flight Discovery Protocol

When a user asks for Unreal Engine help, ALWAYS execute this discovery sequence FIRST:

### 1. Locate the .uproject File

```bash
find . -maxdepth 2 -name "*.uproject" -type f
```

**If found**: Read it to extract:
- Engine version from `"EngineAssociation"` field
- Project name from filename
- Enabled plugins from `"Plugins"` array
- Module dependencies from `"Modules"` array

**Example .uproject structure**:
```json
{
  "FileVersion": 3,
  "EngineAssociation": "5.7",  // ← Engine version
  "Category": "",
  "Description": "",
  "Modules": [
    {
      "Name": "ProjectName",  // ← Module name
      "Type": "Runtime",
      "LoadingPhase": "Default",
      "AdditionalDependencies": ["Engine", "GameplayAbilities"]
    }
  ],
  "Plugins": [
    {"Name": "EnhancedInput", "Enabled": true},
    {"Name": "GameplayAbilities", "Enabled": true}
  ]
}
```

### 2. Map the Project Structure

**Standard Unreal project layout**:
```
ProjectRoot/
├── ProjectName.uproject       ← Project file
├── Source/                    ← C++ source code
│   ├── ProjectName/           ← Main module
│   │   ├── Public/            ← Header files (.h)
│   │   ├── Private/           ← Implementation files (.cpp)
│   │   └── ProjectName.Build.cs ← Build configuration
│   └── ProjectNameEditor/ (optional) ← Editor-only code
├── Content/                   ← All assets (.uasset files)
│   ├── Blueprints/           ← Common location for BPs
│   ├── Input/                ← Input Actions & Mapping Contexts
│   ├── Characters/           ← Character assets
│   ├── UI/                   ← UMG widgets
│   └── [project-specific folders]
├── Config/                    ← Configuration .ini files
│   ├── DefaultEngine.ini     ← Engine settings
│   ├── DefaultInput.ini      ← Legacy input config
│   └── DefaultGame.ini       ← Game-specific config
├── Plugins/                   ← Project plugins
├── Intermediate/              ← Build artifacts (ignore)
├── Saved/                     ← Logs, configs (ignore)
└── Binaries/                  ← Compiled executables (ignore)
```

Execute these discovery commands:

```bash
# Find C++ classes
view Source/*/Public
view Source/*/Private

# Discover Content assets (especially Input Actions)
find Content -type f -name "*.uasset" | head -50

# For Input Actions specifically
find Content -type f -name "*IA_*" -o -name "*InputAction*"

# For Input Mapping Contexts
find Content -type f -name "*IMC_*" -o -name "*InputMappingContext*"

# Find Blueprint classes
find Content -type f -name "BP_*.uasset"
```

### 3. Understand Existing Code

**Before suggesting ANY code**:
- Read existing character/controller classes to understand patterns
- Check what components are already added
- Identify naming conventions (e.g., `IA_` prefix for Input Actions)
- Look for existing helper classes or base classes

```bash
# Example: Find character class
find Source -name "*Character.h" -o -name "*Character.cpp"
```

## Input System Handling

### Enhanced Input System (UE5+)

**NEVER assume input action names**. Always discover them first:

```bash
# Find Input Actions in Content
find Content -type f \( -name "IA_*.uasset" -o -name "*InputAction*.uasset" \)

# Find Input Mapping Contexts
find Content -type f \( -name "IMC_*.uasset" -o -name "*MappingContext*.uasset" \)
```

**Common Input Action patterns**:
- `IA_Move` or `IA_Movement` (Axis2D)
- `IA_Look` (Axis2D)
- `IA_Jump` (Boolean)
- `IA_Interact` (Boolean)

But ALWAYS verify - projects use different naming conventions.

### Binding Input Actions in C++

**Template for Enhanced Input binding**:

```cpp
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputAction.h"

// In SetupPlayerInputComponent
void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    
    // Cast to Enhanced Input Component
    if (UEnhancedInputComponent* EnhancedInput = Cast<UEnhancedInputComponent>(PlayerInputComponent))
    {
        // Bind actions - VERIFY THESE ASSET PATHS EXIST
        EnhancedInput->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AMyCharacter::Move);
        EnhancedInput->BindAction(LookAction, ETriggerEvent::Triggered, this, &AMyCharacter::Look);
        EnhancedInput->BindAction(JumpAction, ETriggerEvent::Started, this, &AMyCharacter::Jump);
    }
}
```

**Header declarations**:

```cpp
UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
UInputAction* MoveAction;

UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
UInputAction* LookAction;
```

### .uasset Files and Blueprint Reading

**.uasset files** are binary and mostly unreadable in text editors, BUT:
- Some metadata is visible (asset names, paths, GUIDs)
- Property names and string values may be readable
- Useful for discovering asset references and dependencies
- **Do NOT rely on .uasset contents for implementation details**

**Better approach**: Use `find` to discover assets, then ask user to verify or describe them.

## Gameplay Ability System (GAS)

When working with GAS projects (check `.uproject` for `"GameplayAbilities"` plugin):

### Critical GAS Setup Requirements

**1. Build.cs dependencies**:
```csharp
PublicDependencyModuleNames.AddRange(new string[] { 
    "Core", "CoreUObject", "Engine", "InputCore",
    "GameplayAbilities",
    "GameplayTags", 
    "GameplayTasks"
});
```

**2. Ability System Component placement**:
- **For single-player or listen-server**: Can be on Character
- **For dedicated server**: Usually on PlayerState (for player-owned actors)
- **For AI/NPCs**: Can be on Character or custom actor

**3. Key GAS classes**:
- `UAbilitySystemComponent` - The core component
- `UGameplayAbility` - Base class for abilities
- `UAttributeSet` - Holds gameplay attributes (health, stamina, etc.)
- `UGameplayEffect` - Modifies attributes
- `FGameplayTag` - Tags for ability system

### Common GAS Patterns

**Granting abilities**:
```cpp
// In C++
AbilitySystemComponent->GiveAbility(
    FGameplayAbilitySpec(AbilityClass, 1, INDEX_NONE, this)
);
```

**Activating abilities**:
```cpp
// By class
AbilitySystemComponent->TryActivateAbilityByClass(AbilityClass);

// By tag
FGameplayTagContainer TagContainer;
TagContainer.AddTag(FGameplayTag::RequestGameplayTag(FName("Ability.Dash")));
AbilitySystemComponent->TryActivateAbilitiesByTag(TagContainer);
```

## Plugin-Specific Guidance

### Unknown or Experimental Plugins

**When encountering unfamiliar plugins** (e.g., Mutable, MutableClothing, RelativeIKOp):

1. **Search for official documentation**:
```
web_search: "Unreal Engine [PluginName] documentation API"
web_search: "Unreal Engine [PluginName] usage examples"
```

2. **Check source code** (if accessible):
```bash
# Engine plugins location (if user has source build)
find /path/to/UE5/Engine/Plugins -name "PluginName"
```

3. **Be transparent**: "This plugin is experimental/underdocumented. Let me search for the latest information..."

## API Knowledge Gaps

**When uncertain about API usage**:

1. **Search Epic's documentation**:
```
web_search: "Unreal Engine [ClassName] API [EngineVersion]"
```

2. **Search community resources**:
```
web_search: "Unreal Engine [feature] example code C++"
```

3. **Check Epic Developer Community forums**
4. **Look for example projects** (Lyra, Valley of the Ancient, ActionRPG)

## Common Pitfalls to Avoid

### ❌ WRONG: Making Assumptions

```cpp
// DON'T assume this exists
EnhancedInput->BindAction(IA_Jump, ETriggerEvent::Started, this, &AMyCharacter::Jump);
```

### ✓ CORRECT: Discovery First

```bash
# Find what Input Actions actually exist
find Content -name "*IA_*"
# Then ask user or use discovered names
```

### ❌ WRONG: Generic Action Names

```cpp
// Too generic - what if they use IA_PlayerJump?
UPROPERTY(EditAnywhere, Category = "Input")
UInputAction* JumpAction;
```

### ✓ CORRECT: Verify Asset Names

```bash
# Discover actual naming convention
find Content/Input -name "*.uasset"
# Results might show: IA_Jump, IA_PlayerJump, InputAction_Jump, etc.
```

## Version-Specific Considerations

### Engine Version Detection

Always check `.uproject` for `"EngineAssociation"`:
- **5.0-5.4**: Stable Enhanced Input, Experimental GAS improvements
- **5.5+**: Mutable/Customization systems, new input features
- **4.27**: Legacy input system, requires manual Enhanced Input setup

### Version-Specific Features

When suggesting code, CHECK if features exist in that version:
```
web_search: "Unreal Engine [feature] [version] availability"
```

## Workflow Decision Tree

```
User asks for Unreal help
    │
    ├─> Find .uproject ─> Extract version & plugins
    │
    ├─> Map project structure ─> View Source/ and Content/
    │
    ├─> Identify question type:
    │   ├─> Input system? ─> Discover Input Actions/Contexts
    │   ├─> GAS-related? ─> Check GAS setup, discover abilities
    │   ├─> Plugin-specific? ─> Search documentation
    │   └─> General C++? ─> Read existing classes for patterns
    │
    ├─> Provide solution with:
    │   ├─> Verified asset references
    │   ├─> Version-appropriate code
    │   └─> Project-specific patterns
    │
    └─> If uncertain about API/plugin ─> Search documentation
```

## Best Practices Checklist

Before providing ANY code suggestion:

- [ ] Found and read .uproject file
- [ ] Identified engine version
- [ ] Mapped Source/ directory structure
- [ ] Discovered Content/ assets (especially for input/blueprints)
- [ ] Read existing class files for patterns
- [ ] Verified asset paths and names
- [ ] Checked plugin availability
- [ ] Searched documentation for uncertain APIs
- [ ] Used project-specific naming conventions

## Quick Reference Commands

```bash
# Engine version
grep "EngineAssociation" *.uproject

# Find C++ classes
find Source -name "*.h" -o -name "*.cpp" | head -20

# Find Input Actions
find Content -name "IA_*.uasset" -o -name "*InputAction*.uasset"

# Find Blueprints
find Content -name "BP_*.uasset" | head -20

# Find config files
ls -la Config/

# Check for GAS
grep -i "GameplayAbilities" *.uproject
```

## Detailed References

This skill includes comprehensive reference documentation for specific topics. Load these when needed:

### references/enhanced_input.md
Load when working with Enhanced Input System:
- Detailed API reference for Input Actions, Mapping Contexts, Triggers
- Complete binding examples and patterns
- Value type handling (Digital, Axis1D, Axis2D, Axis3D)
- Console commands and debugging tips
- Migration from legacy input system

### references/gameplay_ability_system.md
Load when working with GAS:
- Complete setup guide (ASC, AttributeSet, Abilities, Effects)
- Replication strategies (PlayerState vs Character placement)
- Granting and activating abilities
- Gameplay Tags usage
- Attribute modification patterns
- Common GAS patterns (damage, cooldowns, costs)
- Debugging and best practices

### references/common_pitfalls.md
Load when troubleshooting or encountering errors:
- Input system issues and solutions
- GAS activation problems
- Build and compilation errors
- Blueprint/C++ integration issues
- Asset reference problems
- Plugin troubleshooting
- Performance debugging
- Emergency recovery procedures
