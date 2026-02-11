---
name: pygame-patterns
description: Codify reusable pygame patterns for entities, projectiles, movement, and sprite handling. Use when implementing pygame entities or systems that need frame-independent physics, collision detection, or sprite management. References verified patterns from project implementation.
allowed-tools: Read, Grep, Glob
---

# Pygame Patterns Skill

Provides tested, verified pygame patterns from this project. Use when implementing new entities or systems to ensure consistency and correctness.

## Core Principles

1. **Frame-Independent Movement**: All movement uses delta_time for consistent speed regardless of framerate
2. **Verified Patterns Only**: All patterns come from working code in this project
3. **Config-Driven**: Use centralized config.py dataclasses, never hardcode values
4. **Angle Conventions**: 0° = right, 90° = up, 180° = left, 270° = down (pygame Y-axis is inverted)

## Available Patterns

### Projectiles
See [patterns/projectiles.md](patterns/projectiles.md) for:
- Spawning projectiles at entity position with direction
- Frame-independent projectile movement (velocity vectors)
- Circle collision detection
- Lifetime management and despawning
- Converting angles to velocity vectors (accounting for pygame Y-axis)

## Instructions

### Step 1: Identify the Pattern Needed

Determine which pattern matches your implementation:
- **Projectile system**: spawning, movement, collision → Use projectiles.md
- **Entity movement**: WASD, smooth rotation → See player.py:129-155
- **Sprite loading**: error handling, fallbacks → See utils.py:10-27
- **Collision detection**: circle-based → See game.py collision logic

### Step 2: Reference the Pattern

Read the pattern documentation:
```bash
Read .claude/skills/pygame-patterns/patterns/<pattern>.md
```

Or examine the existing implementation:
```bash
Read src/entities/<entity>.py
```

### Step 3: Verify with Documentation

**CRITICAL**: Before implementing, verify pygame APIs with ref.tools:
- Check pyproject.toml for pygame version
- Use ref_search_documentation for API verification
- Confirm function signatures and parameters

### Step 4: Apply the Pattern

Follow the pattern structure:
1. Add config dataclass to src/config.py (no hardcoded values)
2. Import necessary pygame modules
3. Use delta_time for frame-independent calculations
4. Add logging for entity lifecycle events
5. Follow angle conventions (0° = right, pygame Y-inverted)

## Pattern Verification Checklist

Before using a pattern:
- [ ] Read the pattern documentation
- [ ] Verify pygame APIs with ref.tools if using new functions
- [ ] Check that config values are in config.py
- [ ] Understand coordinate system (pygame Y-axis inverted)
- [ ] Test frame-independence (should work at any FPS)

## Example Usage

When implementing a projectile entity:

1. **Read the pattern**:
   ```
   Read .claude/skills/pygame-patterns/patterns/projectiles.md
   ```

2. **Follow the structure**:
   - Create ProjectileConfig in config.py
   - Spawn at entity position with angle
   - Convert angle → velocity (cos/sin, negative Y)
   - Update position with delta_time
   - Check lifetime and collisions

3. **Verify angle math**:
   ```python
   # 0° = right, 90° = up (pygame Y is inverted)
   angle_rad = math.radians(angle)
   velocity_x = math.cos(angle_rad) * speed
   velocity_y = -math.sin(angle_rad) * speed  # negative for pygame
   ```

## Integration with Other Skills

- **python-testing**: Use to generate tests for entity movement and collision
- **entity-builder**: Use this skill to inform entity generation patterns
- **game-artist**: Use patterns for sprite loading and rotation

## Current Project Patterns

Verified patterns from implemented code:
- **Player rotation**: src/entities/player.py:129-155 (smooth rotation, angle wrap)
- **Sprite loading**: src/utils.py:10-27 (error handling, fallbacks)
- **Collision detection**: Circle-based (used in player-zombie and player-powerup)
- **Frame-independent movement**: All entities use delta_time * speed

## Quality Standards

All patterns must:
- Be frame-independent (use delta_time)
- Use centralized config (no magic numbers)
- Include logging for entity events
- Handle pygame Y-axis inversion correctly
- Be verified from working code
