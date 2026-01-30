---
name: vibereps
description: Exercise tracker for Claude Code. Setup, test, add exercises, tune detection. Launches pose-detection UI when Claude edits files.
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash, Glob, Grep
---

# Vibereps

Exercise tracker for Claude Code. Determine what the user needs based on context:

| User Intent | Action |
|-------------|--------|
| First time / "setup" / "install" | → Setup Flow |
| "test" / "launch" / "run" | → Test Tracker |
| "add exercise" / "custom" / "new exercise" | → Add Exercise |
| "not counting" / "sensitivity" / "threshold" / "tune" | → Tune Detection |
| General question | → Overview |

---

## Overview

Movement breaks while you code. When Claude edits files, vibereps launches a pose-detection exercise UI. Do a few squats or stretches while Claude works, then get notified when it's ready.

**Supported exercises:**
- Standing: squats, jumping_jacks, calf_raises, push_ups, high_knees, standing_crunches, side_stretches, torso_twists, arm_circles
- Seated: shoulder_shrugs, neck_tilts, neck_rotations

All pose detection happens locally via MediaPipe. No video data transmitted.

---

## Setup Flow

### Step 1: Choose Installation Method

Use AskUserQuestion:
```
Question: "How would you like to set up vibereps?"
Header: "Install"
Options:
- "Run installer (Recommended)": "Downloads files, installs menubar app, configures hooks automatically"
- "Manual configuration": "I already have vibereps files, just configure my hooks"
```

**If "Run installer":**
```bash
curl -fsSL https://raw.githubusercontent.com/Flow-Club/vibereps/main/install.sh | bash
```
Then show summary and done.

**If "Manual configuration":** Continue below.

### Step 2: Ask Exercise Mode

```
Question: "What type of exercises would you like?"
Header: "Mode"
Options:
- "Standing & Seated (Recommended)": "Full variety - squats, jumping jacks, plus desk-friendly neck stretches"
- "Standing only": "Active exercises - squats, jumping jacks, push-ups, calf raises"
- "Seated only": "Desk-friendly - shoulder shrugs, neck stretches"
```

### Step 3: Select Exercises

Use AskUserQuestion with MultiSelect: true. Show exercises based on mode:

**Standing:** squats, jumping_jacks, calf_raises, standing_crunches, side_stretches, pushups, high_knees, torso_twists, arm_circles

**Seated:** shoulder_shrugs, neck_tilts, neck_rotations

### Step 4: Find Install Location

```bash
if [[ -f "$HOME/.vibereps/exercise_tracker.py" ]]; then
    echo "$HOME/.vibereps"
else
    echo "$(pwd)"
fi
```

### Step 5: Configure Hooks

Update `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "VIBEREPS_EXERCISES={exercises} {vibereps_dir}/exercise_tracker.py post_tool_use '{}'",
        "async": true
      }]
    }],
    "Notification": [{
      "matcher": "idle_prompt|permission_prompt",
      "hooks": [{
        "type": "command",
        "command": "{vibereps_dir}/notify_complete.py '{}'",
        "async": true
      }]
    }]
  }
}
```

Replace `{vibereps_dir}` with full path (not ~) and `{exercises}` with comma-separated list.

### Step 6: Summary

```
Setup complete!

How it works:
1. Claude edits a file → Exercise tracker launches
2. Do a quick exercise while Claude works
3. Get notified when Claude is ready!
```

---

## Test Tracker

**Launch in quick mode** (exercises while Claude works):
```bash
pkill -f "exercise_tracker.py" 2>/dev/null
~/.vibereps/exercise_tracker.py user_prompt_submit '{}'
```

**Launch in normal mode** (after task complete):
```bash
pkill -f "exercise_tracker.py" 2>/dev/null
~/.vibereps/exercise_tracker.py task_complete '{}'
```

**With specific exercises:**
```bash
VIBEREPS_EXERCISES=squats,jumping_jacks ~/.vibereps/exercise_tracker.py user_prompt_submit '{}'
```

**Kill tracker:**
```bash
pkill -f "exercise_tracker.py"
```

**Check if running:**
```bash
lsof -i :8765
```

---

## Add Exercise

### 1. Choose detection type

| Type | Use For | Example |
|------|---------|---------|
| `angle` | Joint angle changes | squats, pushups |
| `height_baseline` | Vertical movement from baseline | calf raises |
| `height_relative` | Position relative to reference | jumping jacks |
| `tilt` | Torso lean | side stretches |
| `distance` | Body parts approaching | standing crunches |
| `width_ratio` | Shoulder/hip width ratio | torso twists |
| `quadrant_tracking` | Circular motion | arm circles |

### 2. MediaPipe Landmark IDs

- Shoulders: 11 (left), 12 (right)
- Elbows: 13 (left), 14 (right)
- Wrists: 15 (left), 16 (right)
- Hips: 23 (left), 24 (right)
- Knees: 25 (left), 26 (right)
- Ankles: 27 (left), 28 (right)

### 3. Create JSON config

Create `exercises/{exercise_name}.json`:

```json
{
  "id": "squats",
  "name": "Squats",
  "description": "Strengthens legs",
  "category": "strength",
  "reps": { "normal": 10, "quick": 5 },
  "detection": {
    "type": "angle",
    "landmarks": {
      "joint": [23, 25, 27],
      "joint_alt": [24, 26, 28]
    },
    "thresholds": { "down": 120, "up": 150 }
  },
  "instructions": {
    "ready": "Squat down below {down}°",
    "down": "Good! Now stand up"
  }
}
```

### 4. Test

```bash
~/.vibereps/exercise_tracker.py user_prompt_submit '{}'
```

---

## Tune Detection

### Common Issues

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Not counting reps | Thresholds too strict | Lower `down` threshold or raise `up` threshold |
| Double counting | Thresholds too loose | Tighten thresholds, add hysteresis |
| Counts on wrong motion | Wrong landmarks | Check landmark IDs match exercise |
| Works for some people | Fixed thresholds | Use body-relative thresholds |

### Threshold Locations

**JSON configs** (preferred): `exercises/*.json` → `detection.thresholds`

**Legacy functions** in `exercise_ui.html`:
- `detectLegacySquat`, `detectLegacyPushup`, etc.

### Testing Changes

1. Edit threshold in JSON
2. Restart tracker: `~/.vibereps/exercise_tracker.py user_prompt_submit '{}'`
3. Watch status text for live angle/distance values
4. Adjust based on state transitions

### Both-sides Averaging

For angle-based exercises, use `joint_alt` to average both sides:
```json
"landmarks": {
  "joint": [23, 25, 27],
  "joint_alt": [24, 26, 28]
}
```

---

## Links

- [GitHub](https://github.com/Flow-Club/vibereps)
- [Documentation](https://github.com/Flow-Club/vibereps/tree/main/docs)
