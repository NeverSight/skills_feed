---
name: video-creator
description: Orchestrates end-to-end video generation through sequential workflow steps (audio, direction, assets, design, coding). Activates when user requests video creation from a script, wants to resume video generation, mentions "create video", "generate video", or "video workflow", requests running a specific step (audio, direction, assets, design, coding), asks to "create audio", "generate direction", "create assets", "generate design", or "code video components", or wants to resume a video. Manages workflow state tracking and parallel scene generation.
---

# Video Creator Skill

Manages the complete video creation pipeline from script input to final video components.

## Execution Modes

Determine which workflow to follow based on user input:

### Mode 1: Execute Video Step
**When:** Immediately read when user wants to execute a specific workflow step (audio, direction, assets, design, or coding).
**Workflow:** [execute-video-step.md](./execute-video-step.md)

### Mode 2: Execute Regenerate Scenes Step
**When:** Immediately read when user wants to regenerate specific scenes for a step (design or coding) with scenes parameter.
**Workflow:** [execute-regen-scenes-step.md](./execute-regen-scenes-step.md)

### Mode 3: Resume Video
**When:** Immediatly read when user wants to continue an existing video workflow from where it left off or check the status of an in-progress video
**Workflow:** [resume-video.md](./resume-video.md)

### Mode 4: Create Video
**When:** User wants to create a completely new video from scratch, starting with script input and style selection
**Workflow:** [create-video.md](./create-video.md)

## Step References

Individual step implementations (referenced by execution modes):

- [user-input-step.md](./steps/user-input-step.md) - Gather script and video style
- [audio-step.md](./steps/audio-step.md) - Generate audio from script
- [direction-step.md](./steps/direction-step.md) - Create video direction
- [assets-step.md](./steps/assets-step.md) - Generate SVG assets
- [design-step.md](./steps/design-step.md) - Generate design specifications
- [code-step.md](./steps/code-step.md) - Create video components
- [regenerate-design-step.md](./steps/regenerate-design-step.md) - Regenerate design for specific scenes
- [regenerate-code-step.md](./steps/regenerate-code-step.md) - Regenerate code for specific scenes

## Utility Scripts

**video-status.py**: Manages workflow state and step progression

Available actions:
- `create-video-status-file`: Initialize new video workflow and return first step
- `get-incomplete-step`: Get current pending step
- `complete-step`: Mark step done and advance to next

**Output Format:**

All actions output a single line

**list-topics.py**: Get all topics with video workflows

Usage:
```bash
python .claude/skills/video-creator/scripts/list-topics.py
```

When user doesn't specify a topic, use this script to get all available topics, display them to the user, and ask them to specify which topic they want to work with