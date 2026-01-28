---
name: bevy
description: This skill should be used when working on Bevy game engine projects. It provides specialized knowledge for Bevy's Entity Component System (ECS) architecture, component-driven design patterns, system ordering, UI development, build strategies, and common pitfalls. Use this skill when implementing game features, debugging Bevy code, designing component architectures, or working with Bevy's UI system.
---

# Bevy Game Development Skill

A specialized skill for developing games and applications using the Bevy game engine, based on real-world experience building complex Bevy projects.

## When to Use This Skill

Invoke this skill when:
- Implementing features in a Bevy game or application
- Designing component architectures for ECS
- Creating or debugging Bevy systems
- Working with Bevy's UI system
- Building and testing Bevy projects
- Troubleshooting common Bevy issues
- Organizing project structure for Bevy applications

## Before You Start: Essential Bevy Tips

### ⚠️ Bevy 0.17 Breaking Changes

**If working with Bevy 0.17**, be aware of significant API changes:
- Material handles now wrapped in `MeshMaterial3d<T>` (not `Handle<T>`)
- Event system replaced with observer pattern (`commands.trigger()`, `add_observer()`)
- Color arithmetic operations removed (use component extraction)

**See `references/bevy_specific_tips.md` for complete Bevy 0.17 migration guide and examples.**

### Consult Bevy Registry Examples First

**The registry examples are your bible.** Always check them before implementing new features.

**Location:**
```bash
~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/bevy-0.17.1/examples
```

There are MANY examples covering all aspects of Bevy development. Review relevant examples to understand best practices and working patterns.

### Use Plugin Structure

Break your app into discrete modules using plugins. This improves organization and makes code discoverable.

```rust
pub struct CombatPlugin;

impl Plugin for CombatPlugin {
    fn build(&self, app: &mut App) {
        app
            .add_event::<DamageEvent>()
            .add_systems(Update, (process_damage, check_death));
    }
}
```

See `references/bevy_specific_tips.md` for detailed plugin patterns and examples.

### Design Before Coding

**Pure ECS demands careful data modeling.** It's hard to search a massive list of systems in one file!

Before implementing:
1. Design the data model (entities, components, events, systems)
2. Check Bevy examples for similar patterns
3. Review docs and existing code
4. Create a plugin for the feature domain

See `references/bevy_specific_tips.md` for domain-driven design guidance.

## Core Development Principles

### Think in ECS Terms

Bevy is an Entity Component System (ECS) engine. Always think in terms of **data** (components) and **transformations** (systems), not objects and methods.

**Separation of Concerns:**
- **Components** = Pure data, no logic
- **Systems** = Pure logic, operate on components
- **Events** = Communication between systems
- **Resources** = Global state (use sparingly)

### Component-Driven Design

**Keep components focused:**
```rust
// ✅ GOOD: Small, focused components
#[derive(Component)]
pub struct Health { pub current: f32, pub max: f32 }

#[derive(Component)]
pub struct Armor { pub defense: f32 }

// ❌ BAD: Monolithic component
#[derive(Component)]
pub struct CombatStats {
    pub health: f32,
    pub armor: f32,
    pub strength: f32,
    // ... wastes memory for entities that only have some stats
}
```

**Add helper methods via impl blocks:**
```rust
impl Health {
    pub fn is_alive(&self) -> bool {
        self.current > 0.0
    }

    pub fn percentage(&self) -> f32 {
        self.current / self.max
    }
}
```

For detailed component patterns, see `references/ecs_patterns.md`.

### System Design and Ordering

**Order systems by dependencies:**
```rust
.add_systems(
    Update,
    (
        // 1. Input processing
        handle_input,

        // 2. State changes
        process_events,
        update_state,

        // 3. Derive properties from state
        calculate_derived_values,

        // 4. Visual updates
        update_materials,
        update_animations,

        // 5. UI updates (must run last)
        update_ui_displays,
    ),
)
```

**Use change detection to optimize:**
```rust
// Only process entities where Health changed
pub fn update_health_bar(
    query: Query<(&Health, &mut HealthBar), Changed<Health>>,
) {
    for (health, mut bar) in query.iter_mut() {
        bar.width = health.percentage() * 100.0;
    }
}
```

For detailed query patterns and system design, see `references/ecs_patterns.md`.

## Build and Testing Workflow

### Build Commands

**Development (faster iteration):**
```bash
cargo build --features bevy/dynamic_linking
```
- Uses dynamic linking for faster compile times
- 2-3x faster than release builds
- Only use during development
- **CRITICAL:** Always use this for development builds

**Quick Check:**
```bash
cargo check
```
- Fastest way to verify compilation
- Use after every significant change

**Release (production):**
```bash
cargo build --release
```
- Full optimization
- Use for final testing and distribution

### Build Management - CRITICAL

**DO NOT delete target binaries freely!** Bevy takes minutes to rebuild from scratch.

- Avoid `cargo clean` unless absolutely necessary
- Each clean rebuild costs valuable development time
- Be mindful of versions, targets, and crate dependencies getting tangled
- Bevy is under active development - stick to one version per project

See `references/bevy_specific_tips.md` for detailed build optimization and version management.

### Testing Workflow

1. **After component changes:** Run `cargo check`
2. **After system changes:** Run `cargo check` then `cargo build --features bevy/dynamic_linking`
3. **Manual testing:**
   - Does the game launch?
   - Do the new features work?
   - Are console logs showing expected output?
   - Do visual changes appear correctly?

**Validation points** - Let the user test at these milestones:
- New entity spawned
- New mechanic implemented
- Visual effects added
- Major system changes

## UI Development in Bevy

Bevy uses a flexbox-like layout system. Follow the marker component pattern:

**1. Create marker components:**
```rust
#[derive(Component)]
pub struct HealthBar;

#[derive(Component)]
pub struct ScoreDisplay;
```

**2. Setup in Startup:**
```rust
pub fn setup_ui(mut commands: Commands) {
    commands.spawn((
        HealthBar,
        Node {
            position_type: PositionType::Absolute,
            left: Val::Px(10.0),
            top: Val::Px(10.0),
            width: Val::Px(200.0),
            height: Val::Px(20.0),
            ..default()
        },
        BackgroundColor(Color::srgba(0.8, 0.2, 0.2, 0.9)),
    ));
}
```

**3. Update in Update:**
```rust
pub fn update_health_ui(
    health: Query<&Health, With<Player>>,
    mut ui: Query<&mut Node, With<HealthBar>>,
) {
    if let (Ok(health), Ok(mut node)) = (health.get_single(), ui.get_single_mut()) {
        node.width = Val::Px(health.percentage() * 200.0);
    }
}
```

For detailed UI patterns including positioning, styling, and text updates, see `references/ui_development.md`.

## Incremental Development Strategy

### Phase-Based Development

Break features into phases:

**Phase 1: Foundation** - Core components and basic systems
**Phase 2: Content** - Add entities and populate world
**Phase 3: Polish** - UI improvements and visual effects
**Phase 4: Advanced Features** - Complex mechanics and AI

### Iteration Pattern

```
1. Plan → 2. Implement → 3. Build → 4. Test → 5. Refine
     ↑                                           ↓
     ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

**Each phase should have:**
1. Clear success criteria (checklist of what works)
2. Manual test cases (step-by-step testing procedures)
3. User validation points (when to let user test)

## Performance Optimization

### When to Optimize

**For prototypes (7-100 entities):**
- No optimization needed
- Change detection is sufficient
- Focus on features, not performance

**For production (100+ entities):**
- Use spatial partitioning for proximity queries
- Batch material updates
- Consider Fixed timestep for physics
- Profile before optimizing

### Query Optimization Tips

1. **Use change detection:** `Query<&Component, Changed<Component>>`
2. **Filter early:** `Query<&A, (With<B>, Without<C>)>` instead of filtering in loops
3. **Check resource changes:** Return early if resource hasn't changed

## Common Pitfalls to Avoid

**Critical mistakes and their solutions are documented in `references/common_pitfalls.md`. Key pitfalls include:**

1. Forgetting to register systems in `main.rs`
2. Borrowing conflicts (use `get_many_mut` for multiple mutations)
3. Not using `Changed<T>` for expensive operations
4. Wrong system ordering (input → state → derived → visual → UI)
5. Entity queries after despawn (use `if let Ok()` pattern)
6. Material/asset handle confusion (store handles properly)

Review `references/common_pitfalls.md` before implementing complex features.

## Using Subagents for Complex Features

When implementing multi-step features, use the plan-implementer subagent with this structure:

```
Goal: [One sentence describing end state]

Current State: [What exists now]

Requirements: [Numbered list of what to build]

Implementation Steps: [Suggested approach]

Success Criteria: [How to verify it works]

Notes: [Important context, edge cases, design principles]
```

**Example:**
```
Implement Health System

Goal: Implement a health system with damage, healing, and death mechanics.

Current State:
- Player entity exists
- No health tracking yet

Requirements:
1. Create Health component with current/max values
2. Create DamageEvent for dealing damage
3. Create system to process damage events
4. Add death detection when health reaches 0
5. Add visual health bar UI

Implementation Steps:
1. Create Health component in src/components/properties.rs
2. Create DamageEvent in src/events.rs
3. Create process_damage system in src/systems/combat.rs
4. Create check_death system
5. Create health bar UI in src/systems/ui/health_bar.rs
6. Register all systems in main.rs in correct order

Success Criteria:
- Player spawns with Health component
- Damage events reduce health
- Health bar updates when health changes
- Entity despawns when health reaches 0
- Code compiles without errors
```

## Project Structure Reference

For details on recommended file organization, module structure, and component file patterns, see `references/project_structure.md`.

## References

This skill includes detailed reference documentation:

- `references/bevy_specific_tips.md` - **START HERE:** Registry examples, plugin structure, build optimization, version management, domain-driven design for ECS
- `references/ecs_patterns.md` - Component design patterns, query patterns, and common ECS design patterns (Derivation, State Machine, Threshold/Trigger, Event-Driven, Initialization)
- `references/ui_development.md` - Bevy UI hierarchy, component patterns, layout tips, positioning, styling, and text updates
- `references/common_pitfalls.md` - Common mistakes and their solutions (system registration, borrowing conflicts, change detection, system ordering, entity queries, asset handles)
- `references/project_structure.md` - Recommended file organization, module structure, component file patterns, and change detection

Load these references as needed to inform implementation decisions.

## Additional Resources

**Bevy Documentation:**
- Official Bevy Book: https://bevyengine.org/learn/book/
- Bevy Examples: https://github.com/bevyengine/bevy/tree/main/examples (also in `~/.cargo/registry/...`)
- Bevy Cheat Book: https://bevy-cheatbook.github.io/
- Plugin Guide: https://bevy.org/learn/quick-start/getting-started/plugins/
- System Sets: https://bevy-cheatbook.github.io/programming/system-sets.html
- Setup & Optimization: https://bevy.org/learn/quick-start/getting-started/setup/

**ECS Design Principles:**
- Prefer composition over inheritance
- One component = one concern
- Systems should be pure functions
- Use events to decouple systems
- **Design data model before coding**
- **Check registry examples first**

---

**Remember:** Think in terms of data (components) and transformations (systems), not objects and methods. Always consult registry examples and design your data model before diving into implementation. This is the key to effective Bevy development.
