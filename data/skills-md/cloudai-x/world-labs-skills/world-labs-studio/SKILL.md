---
name: world-labs-studio
description: World Labs Studio - Compose multiple worlds, record camera animations, and expand boundaries
allowed-tools:
  - Bash
  - WebFetch
---

# World Labs Studio

Studio is where you compose, animate, and enhance your generated worlds. Connect multiple worlds, create camera paths, and export final videos.

## Accessing Studio

1. Go to <https://marble.worldlabs.ai>
2. Open a generated world
3. Click **Continue Creating** (paintbrush icon) to access Studio tools
4. Or access from your worlds tab

**Documentation**: <https://docs.worldlabs.ai/marble/create/studio-tools/>

## Three Core Features

| Feature     | Purpose                                  |
| ----------- | ---------------------------------------- |
| **Compose** | Connect and arrange multiple worlds      |
| **Record**  | Create camera animations with keyframes  |
| **Expand**  | Extend worlds beyond original boundaries |

## Compose Mode

### Overview

Compose allows you to:

- Connect multiple generated worlds into larger environments
- Position, rotate, and scale worlds
- Remove splat artifacts at boundaries
- Create seamless transitions

### Interface

```
┌─────────────────────────────────────────┐
│  [World 1]  ←→  [World 2]  ←→  [World 3]│
│     ↕                             ↕     │
│  [World 4]                   [World 5]  │
└─────────────────────────────────────────┘
         Compose Canvas View
```

### Adding and Positioning Worlds

1. **Add Scene**: Click to browse your worlds
2. **Choose World**: Select from saved worlds or community
3. **Position**: World appears with positioning handles
4. **Repeat**: Add more worlds to build larger environment

### Controls Panel

| Property   | Description                          |
| ---------- | ------------------------------------ |
| Position   | Adjust X, Y, Z coordinates           |
| Rotation   | Orient worlds to align correctly     |
| Scale      | Resize worlds proportionally         |
| Move Speed | Navigation speed (default: 3)        |
| FOV        | Field of view (default: 92)          |
| Grid       | Toggle grid visibility for alignment |
| Bounding   | Show world boundary corners          |

### Splat Removal

Clean Gaussian splat artifacts at world edges:

1. Select **Splat Eraser** tool
2. Choose brush shape (circle/square)
3. Adjust brush size
4. Paint over artifacts
5. Preview result in real-time

**Splat Count**: Monitor usage against your account limit (e.g., 500,000 / 2,000,000)

### Fine-Tuning Connections

1. Check overlapping areas where worlds meet
2. Align ground levels—ensure floor heights match
3. Match lighting for natural blending
4. Test transitions by navigating between worlds
5. Use consistent background color across scenes

## Record Mode

### Overview

Create cinematic camera animations:

- Define camera path with keyframes
- Control timing and easing
- Add AI enhancement pass
- Export high-quality video

### Keyframe System

| Key      | Action                           |
| -------- | -------------------------------- |
| `F`      | Add keyframe at current position |
| `U`      | Update current keyframe          |
| `Delete` | Remove selected keyframe         |
| `Space`  | Play/pause animation             |

### Creating Camera Paths

**Step 1: Position camera**

```
Navigate to starting view using:
- WASD: Move
- Mouse: Look
- Q/E: Up/Down
- Shift: Sprint
```

**Step 2: Add keyframe**

```
Press F to create keyframe at current position
```

**Step 3: Move to next position**

```
Navigate to next camera position
```

**Step 4: Repeat**

```
Continue adding keyframes along desired path
```

### Timeline Interface

```
0s      2s      4s      6s      8s      10s
├───●───┼───●───┼───────┼───●───┼───●───┤
    KF1     KF2             KF3     KF4
```

### Keyframe Properties

| Property | Description                                     |
| -------- | ----------------------------------------------- |
| Position | Camera XYZ location                             |
| Rotation | Camera orientation (pitch, yaw, roll)           |
| FOV      | Field of view                                   |
| Duration | Time to reach this keyframe                     |
| Easing   | Interpolation curve (linear, ease-in/out, etc.) |

### Easing Options

| Easing      | Effect               |
| ----------- | -------------------- |
| Linear      | Constant speed       |
| Ease-In     | Slow start, fast end |
| Ease-Out    | Fast start, slow end |
| Ease-In-Out | Slow start and end   |
| Bezier      | Custom curve control |

### Enhance Feature

After recording, apply AI enhancement:

1. **Temporal consistency**: Smooth flickering artifacts
2. **Detail enhancement**: Sharpen and improve quality
3. **Color grading**: Apply cinematic color profiles

```
[Record] → [Preview] → [Enhance] → [Export]
```

## Expand Mode

### Overview

Extend world boundaries beyond the original generation:

1. Navigate to world edge
2. Look for areas where world meets unexplored space
3. Position yourself at good viewpoint
4. Click **Expand** button
5. AI generates new content matching existing style

### Accessing Expand

- Click **Continue Creating** (paintbrush icon) on any generated world
- Available in the viewer or from your worlds tab

### Expand Controls

| Control       | Action                     |
| ------------- | -------------------------- |
| Click edge    | Select expansion direction |
| Drag boundary | Define expansion area      |
| Generate      | Create new world section   |

### Expansion Scenarios

**Indoor Extensions:**

- Expand bedrooms into en-suite bathrooms
- Extend kitchens into dining areas
- Add hallways connecting rooms
- Create balconies from indoor spaces

**Outdoor Growth:**

- Expand gardens into larger landscapes
- Extend courtyards into street views
- Add pathways to new zones

### Best Practices

✅ Expand in directions with good context
✅ Generate small sections, check quality
✅ Consider flow and logical navigation
✅ Think about how areas connect spatially

❌ Don't expand into empty void areas
❌ Avoid expanding where geometry is ambiguous
❌ **Note**: Vertical expansion (up/down) not currently supported

### Limitations

- Cannot expand upward or downward (horizontal only)
- "Not within recommended area" warning indicates expansion limit
- Trajectories don't persist across page navigation
- Multiple expansions require Studio Compose to stitch together

## Keyboard Shortcuts

### Navigation

| Key      | Action           |
| -------- | ---------------- |
| `W`      | Forward          |
| `S`      | Backward         |
| `A`      | Left             |
| `D`      | Right            |
| `Q`      | Down             |
| `E`      | Up               |
| `Shift`  | Sprint           |
| `Mouse`  | Look around      |
| `Scroll` | Adjust speed     |
| `[`      | Decrease FOV     |
| `]`      | Increase FOV     |
| `0`      | Return to origin |

### Recording

| Key       | Action                 |
| --------- | ---------------------- |
| `F`       | Add keyframe           |
| `U`       | Update keyframe        |
| `Delete`  | Remove keyframe        |
| `Space`   | Play/Pause             |
| `[` / `]` | Previous/Next keyframe |
| `Home`    | Go to start            |
| `End`     | Go to end              |

### General

| Key      | Action           |
| -------- | ---------------- |
| `Ctrl+Z` | Undo             |
| `Ctrl+Y` | Redo             |
| `Ctrl+S` | Save             |
| `Escape` | Cancel/Exit mode |
| `Tab`    | Toggle UI        |

## Workflow Example

### Creating a Walkthrough Video

1. **Generate worlds**: Create 3 connected room worlds
2. **Compose**: Connect rooms with aligned doorways
3. **Clean edges**: Remove splat artifacts at transitions
4. **Plan path**: Decide camera movement through spaces
5. **Record**:
   - Start at entrance
   - Add keyframes every 2-3 seconds
   - Include pauses at interesting features
   - End at final destination
6. **Preview**: Check timing and smoothness
7. **Adjust**: Update keyframes as needed
8. **Enhance**: Apply AI enhancement pass
9. **Export**: Render final video

## Export Settings

| Setting    | Options                   |
| ---------- | ------------------------- |
| Resolution | 1080p, 2K, 4K             |
| Frame rate | 24, 30, 60 fps            |
| Format     | MP4 (H.264), MOV (ProRes) |
| Quality    | Draft, Standard, High     |

## Related Skills

- `world-labs-api` - API integration
- `world-labs-chisel` - Block out geometry before generation
- `world-labs-export` - Export formats and integrations
