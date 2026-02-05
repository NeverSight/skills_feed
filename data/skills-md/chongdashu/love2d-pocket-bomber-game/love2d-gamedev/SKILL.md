---
name: love2d-gamedev
description: >
  Complete Love2D game development from prototype to polished release.
  Covers core architecture, graphics, animation, tiles, collision, audio,
  and iOS deployment. Use when building Love2D games, implementing game
  mechanics, or deploying to mobile platforms.
---

# Love2D Game Development

Build polished 2D games with the Love2D framework—from first prototype to iOS release.

## Quick Reference

| Topic | When to Use |
|-------|-------------|
| [Core Architecture](references/core-architecture.md) | Understanding game loop, callbacks, modules |
| [Graphics & Drawing](references/graphics-drawing.md) | Images, colors, transforms, screen adaptation |
| [Animation](references/animation.md) | Sprite sheets, quads, frame timing |
| [Tiles & Maps](references/tiles-maps.md) | Tile-based levels, map loading |
| [Collision](references/collision.md) | AABB, circle, and separating axis collision |
| [Audio](references/audio.md) | Sound effects, music, volume control |
| [Project Structure](references/project-structure.md) | File organization, conf.lua, distribution |
| [Libraries](references/libraries.md) | Popular community libraries |
| [iOS Deployment](references/ios/overview.md) | Build, touch controls, App Store |

---

## The Love2D Game Loop

Every Love2D game follows this pattern:

```lua
function love.load()
    -- Called once at startup
    -- Load assets, initialize state
end

function love.update(dt)
    -- Called every frame
    -- dt = time since last frame (seconds)
    -- Update game logic here
end

function love.draw()
    -- Called every frame after update
    -- All rendering happens here
end
```

**Key insight**: `dt` (delta time) ensures consistent speed across frame rates.
```lua
-- WRONG: Speed varies with frame rate
player.x = player.x + 5

-- RIGHT: 200 pixels per second, regardless of FPS
player.x = player.x + 200 * dt
```

---

## Essential Patterns

### Loading and Drawing Images

```lua
function love.load()
    playerImage = love.graphics.newImage("player.png")
end

function love.draw()
    love.graphics.draw(playerImage, x, y)
    -- Full signature: draw(image, x, y, rotation, scaleX, scaleY, originX, originY)
end
```

### Input Handling

```lua
-- Polling (check every frame)
function love.update(dt)
    if love.keyboard.isDown("left") then
        player.x = player.x - 200 * dt
    end
end

-- Event-based (fires once per press)
function love.keypressed(key)
    if key == "space" then
        player:jump()
    end
end
```

### Screen-Adaptive Positioning

Never hard-code screen dimensions:

```lua
function love.load()
    screenW, screenH = love.graphics.getDimensions()
end

function love.resize(w, h)
    screenW, screenH = w, h
end

function love.draw()
    -- Position relative to screen
    local centerX = screenW / 2
    local bottomY = screenH - 50
end
```

---

## Core Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `love.graphics` | Rendering | `draw`, `rectangle`, `circle`, `print`, `setColor` |
| `love.audio` | Sound | `newSource`, `play`, `stop`, `setVolume` |
| `love.keyboard` | Keyboard input | `isDown`, `keypressed` callback |
| `love.mouse` | Mouse input | `getPosition`, `isDown`, callbacks |
| `love.touch` | Touch input | `touchpressed`, `touchmoved`, `touchreleased` |
| `love.filesystem` | File I/O | `read`, `write`, `getInfo` |
| `love.timer` | Timing | `getDelta`, `getTime`, `getFPS` |
| `love.window` | Window control | `setMode`, `getMode`, `setTitle` |
| `love.physics` | Box2D physics | `newWorld`, `newBody`, `newFixture` |

---

## Project Setup

### Minimal Project

```
my-game/
├── main.lua      # Entry point (required)
└── conf.lua      # Configuration (optional but recommended)
```

### conf.lua Template

```lua
function love.conf(t)
    t.window.title = "My Game"
    t.window.width = 800
    t.window.height = 600
    t.version = "11.5"              -- Love2D version
    t.console = true                -- Enable console on Windows

    -- Disable unused modules for faster startup
    t.modules.joystick = false
    t.modules.physics = false
end
```

### Running the Game

```bash
# macOS
/Applications/love.app/Contents/MacOS/love /path/to/game

# Create alias in ~/.zshrc
alias love="/Applications/love.app/Contents/MacOS/love"
```

---

## Common Patterns

### State Management

```lua
local gameState = "menu"  -- menu, playing, paused, gameover

function love.update(dt)
    if gameState == "playing" then
        updateGame(dt)
    end
end

function love.draw()
    if gameState == "menu" then
        drawMenu()
    elseif gameState == "playing" then
        drawGame()
    end
end
```

### Object-Oriented Entities

```lua
local Player = {}
Player.__index = Player

function Player:new(x, y)
    return setmetatable({
        x = x, y = y,
        speed = 200,
        image = love.graphics.newImage("player.png")
    }, Player)
end

function Player:update(dt)
    if love.keyboard.isDown("right") then
        self.x = self.x + self.speed * dt
    end
end

function Player:draw()
    love.graphics.draw(self.image, self.x, self.y)
end

return Player
```

### Camera/Viewport

```lua
local camera = { x = 0, y = 0 }

function love.draw()
    love.graphics.push()
    love.graphics.translate(-camera.x, -camera.y)

    -- Draw world objects here
    drawWorld()

    love.graphics.pop()

    -- Draw UI here (not affected by camera)
    drawUI()
end
```

---

## Anti-Patterns to Avoid

| Don't | Why | Do Instead |
|-------|-----|------------|
| Hard-code coordinates | Breaks on different screens | Use percentages or anchors |
| Forget `dt` in movement | Speed varies with frame rate | Multiply by `dt` |
| Load assets in `update`/`draw` | Loads every frame, kills performance | Load once in `love.load` |
| Use global variables everywhere | Hard to track, name collisions | Use local variables and modules |
| Test only on desktop | Touch behaves differently | Test on device early |

---

## iOS Development

For iOS deployment, see the [iOS Overview](references/ios/overview.md) which covers:

- [Build Setup](references/ios/setup.md) - Xcode project, libraries, signing
- [Touch Controls](references/ios/touch-controls.md) - Virtual joysticks, buttons, gestures
- [Xcode Project Structure](references/ios/xcode-project.md) - Manual pbxproj editing

**Quick iOS checklist**:
1. Download Love2D iOS source + Apple libraries
2. Copy libraries to Xcode project
3. Fix deployment target (8.0 → 15.0)
4. Create `game.love` (zip of Lua files)
5. Add `game.love` to Xcode bundle resources
6. Configure signing and deploy

---

## Philosophy

Love2D makes game development joyful through simplicity:

1. **Lua is approachable** - Dynamic typing, clean syntax, fast iteration
2. **The API is consistent** - Functions follow predictable patterns
3. **You own the game loop** - No hidden magic, full control
4. **Cross-platform by default** - Same code runs on Windows, macOS, Linux, iOS, Android

**The goal isn't just "make it work." The goal is "make it feel great."**

Smooth animations, responsive controls, adaptive layouts—that's the standard for polished games.
