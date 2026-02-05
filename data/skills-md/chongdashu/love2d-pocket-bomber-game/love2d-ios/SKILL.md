---
name: love2d-ios
description: >
  Build and deploy Love2D games to iOS devices. Covers Xcode project setup,
  game bundling, touch controls, and common build issues. Trigger when users
  want to build Love2D games for iOS, add mobile touch controls, or fix
  iOS deployment issues.
---

# Love2D iOS Development

Build games with Love2D and deploy them to iOS devices—from first prototype to App Store.

## Philosophy: Mobile-First Game Development

Love2D was born on desktop, but mobile is where players are. The challenge isn't just "making it run on iOS"—it's **rethinking the game for touch**.

**Before building for iOS, ask**:
- How will players interact without a keyboard?
- What screen sizes and orientations should be supported?
- Is the game's pacing appropriate for mobile sessions?
- What gestures feel natural for this game's actions?

**Core principles**:

1. **Touch is not a keyboard substitute**: Design touch controls that feel native, not bolted-on. A virtual d-pad is a last resort, not a first choice.

2. **Screen size is a variable, not a constant**: Hard-coded coordinates break on different devices. Think in percentages and relative positions.

3. **The build pipeline is fragile**: Xcode projects, code signing, and bundle resources have many failure points. Understand the system, don't just copy commands.

4. **Iterate on device early**: The simulator lies. Test on real hardware as soon as possible.

---

## Development Workflow

### Desktop Development First

Develop and test on desktop before touching iOS:

```bash
# macOS: Love2D isn't in PATH by default
/Applications/love.app/Contents/MacOS/love /path/to/game

# Or create an alias in ~/.zshrc
alias love="/Applications/love.app/Contents/MacOS/love"
```

### Project Structure

```
my-game/
├── conf.lua          # Window size, Love2D version
├── main.lua          # Entry point
├── touch.lua         # Mobile touch controls (optional on desktop)
└── [game modules]    # Player, enemies, etc.
```

### iOS Build Pipeline

See references/ios-setup.md for detailed setup steps.

**Quick overview**:
1. Download Love2D iOS source + Apple libraries
2. Copy libraries to Xcode project
3. Create `game.love` (zip of Lua files)
4. Add `game.love` to Xcode bundle resources
5. Configure signing and deploy

### Update Workflow

Every code change requires rebuilding:

```bash
# From game directory
rm -f game.love
zip -9 -r game.love *.lua [assets/]
cp game.love /path/to/xcode/ios/
# Then build in Xcode (Cmd+R)
```

---

## Touch Control Patterns

See references/touch-controls.md for implementation details.

### Choosing the Right Pattern

| Game Type | Recommended Control |
|-----------|---------------------|
| Platformer | Virtual joystick + action buttons |
| Puzzle | Direct touch/drag on game objects |
| Endless runner | Tap/swipe gestures |
| Turn-based | Tap to select, tap to confirm |
| Twin-stick | Dual virtual joysticks |

### Touch Event Basics

```lua
function love.touchpressed(id, x, y, dx, dy, pressure)
    -- id: unique per finger (for multitouch)
    -- x, y: screen coordinates
end

function love.touchmoved(id, x, y, dx, dy, pressure)
    -- Track finger movement
end

function love.touchreleased(id, x, y, dx, dy, pressure)
    -- Clean up touch state
end
```

### Platform Detection

```lua
local function isMobile()
    local os = love.system.getOS()
    return os == "iOS" or os == "Android"
end

-- Use this to conditionally show touch controls
if isMobile() then
    touchControls = require("touch")
end
```

---

## Screen Adaptation

### Dynamic Sizing

Never hard-code 800x600. Always query dimensions:

```lua
local screenW, screenH

function love.load()
    screenW, screenH = love.graphics.getDimensions()
end

function love.resize(w, h)
    screenW, screenH = w, h
    -- Reposition UI, regenerate layouts
end
```

### Positioning Strategies

**Percentage-based**:
```lua
local buttonX = screenW * 0.85  -- 85% from left
local buttonY = screenH * 0.9   -- 90% from top
```

**Anchor-based**:
```lua
local margin = 20
local rightEdge = screenW - margin
local bottomEdge = screenH - margin
```

**Aspect-ratio aware**:
```lua
local targetAspect = 16/9
local currentAspect = screenW / screenH
-- Add letterboxing or adjust game area
```

---

## Anti-Patterns to Avoid

❌ **Hard-coded coordinates**
```lua
-- BAD: Breaks on different screens
player.x = 400
button.y = 550
```
Why bad: iPhone SE and iPad Pro have very different dimensions.
Better: Use percentages or anchor points relative to screen size.

❌ **Ignoring the "No-game screen"**
Why bad: Your game.love wasn't bundled—the app is working, your game isn't loaded.
Better: Verify game.love is in "Copy Bundle Resources" build phase.

❌ **Testing only on simulator**
Why bad: Simulator has different performance, touch behavior, and screen characteristics.
Better: Deploy to a real device early and often.

❌ **Giant virtual joysticks**
Why bad: Obscures gameplay, feels clunky.
Better: Semi-transparent, appropriately sized (60-80px radius), positioned in thumb-reach zones.

❌ **Copying Xcode project changes blindly**
Why bad: You won't know how to fix it when it breaks differently.
Better: Understand the project.pbxproj structure—PBXBuildFile, PBXFileReference, build phases.

❌ **Forgetting to rebuild game.love**
Why bad: You're testing old code and wondering why changes don't work.
Better: Script the rebuild process. Make it one command.

---

## Common Issues and Solutions

### Deployment Target Errors

**Error**: `IPHONEOS_DEPLOYMENT_TARGET is set to 8.0, but range is 12.0 to X.X`

**Fix**:
```bash
find . -name "*.pbxproj" -exec sed -i '' \
  's/IPHONEOS_DEPLOYMENT_TARGET = 8.0/IPHONEOS_DEPLOYMENT_TARGET = 15.0/g' {} \;
```

### "No-game screen" on Device

**Cause**: game.love not in bundle resources.

**Fix**: Add game.love to Xcode project:
1. Right-click ios folder → Add Files
2. Select game.love
3. Ensure "Add to targets: love-ios" is checked

If that fails, see references/xcode-project-structure.md for manual pbxproj editing.

### Signing Errors

**Fix**: In Xcode:
1. Select love-ios target
2. Signing & Capabilities → Select your Team
3. Change Bundle Identifier to something unique

### Touch Not Responding

**Causes**:
- Not implementing touch callbacks
- Touch area too small (minimum 44x44 points recommended)
- Touch being consumed by wrong element

---

## Variation Guidance

**Touch control layouts should vary based on**:
- Game genre (platformer vs puzzle vs action)
- Screen size (phone vs tablet)
- Player handedness (consider offering options)
- Game complexity (fewer buttons for simpler games)

**Avoid converging on**:
- Always using virtual joystick (sometimes gestures are better)
- Always putting fire button bottom-right (context matters)
- Fixed button sizes (adapt to screen)

---

## File Locations Reference

| Purpose | Path |
|---------|------|
| Xcode project | `love-X.X-ios-source/platform/xcode/love.xcodeproj` |
| iOS libraries | `love-X.X-ios-source/platform/xcode/ios/libraries/` |
| game.love destination | `love-X.X-ios-source/platform/xcode/ios/game.love` |
| Project config | `love.xcodeproj/project.pbxproj` |

---

## Remember

Love2D makes game development joyful. iOS deployment adds friction, but understanding the pipeline—not just following steps—makes you resilient when things break.

**The goal isn't "run on iOS." The goal is "feel great on iOS."**

Touch controls that feel native, layouts that adapt gracefully, and a build process you understand—that's the standard.

Claude is capable of building complete, polished mobile games. These guidelines illuminate the path from desktop prototype to iOS deployment.
