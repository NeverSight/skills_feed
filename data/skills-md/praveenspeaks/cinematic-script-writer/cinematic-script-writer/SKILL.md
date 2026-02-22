---
name: cinematic-script-writer
version: 1.4.0
description: "Create professional cinematic scripts for AI video generation with character consistency and cinematography knowledge. Use when the user wants to write a cinematic script, create story contexts with characters, generate image prompts for AI video tools (Midjourney, Sora, Veo), or needs cinematography guidance (camera angles, lighting, color grading). Also use for character consistency sheets, voice profiles, anachronism detection, and saving scripts to Google Drive."
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - node
    install:
      - id: npm-install
        kind: npm
        package: "cinematic-script-writer"
        bins:
          - cinematic-script
tags:
  - creative
  - video
  - script
  - cinematography
  - youtube
  - camera
  - lighting
  - consistency
  - character-design
  - voice
  - era-accurate
  - storage
  - google-drive
---

# Cinematic Script Writer

Create professional cinematic scripts for AI video generation with character consistency and cinematography knowledge.

## Installation

```bash
# Install via npm
npm install -g cinematic-script-writer

# Or install via OpenClaw CLI
openclaw skills install cinematic-script-writer
```

## CLI Usage

### Context Management

Create and manage story contexts with characters, era, and settings:

```bash
# Create a new story context
cinematic-script create-context --name "My Story" --era "Ancient India" --period "Ramayana Era"

# List all saved contexts
cinematic-script list-contexts

# Get a specific context
cinematic-script get-context --id <context-id>

# Delete a context
cinematic-script delete-context --id <context-id>
```

### Story Generation

Generate story ideas and create cinematic scripts:

```bash
# Generate story ideas for a context
cinematic-script generate-ideas --context-id <context-id> --count 3

# Create a full cinematic script from an idea
cinematic-script create-script --context-id <context-id> --idea-id <idea-id>

# Generate YouTube metadata for a script
cinematic-script generate-metadata --script-id <script-id>
```

### Cinematography Reference

Access camera angles, lighting, and shot type databases:

```bash
# List all camera angles
cinematic-script list-angles

# List all camera movements
cinematic-script list-movements

# List all shot types
cinematic-script list-shots

# Get camera setup recommendation
cinematic-script suggest-camera --scene-type "dialogue" --mood "dramatic"

# Get lighting suggestions
cinematic-script suggest-lighting --scene-type "interior" --mood "mysterious"

# Get color grading suggestions
cinematic-script suggest-grading --genre "action"

# Search cinematography database
cinematic-script search --query "low angle lighting"
```

### Character Consistency

Create character references and validate prompts:

```bash
# Create a character reference sheet
cinematic-script create-character-ref --character-id "char1" --name "Kutil" --visual "Purple rakshasa with golden eyes" --era "Ancient" --style "Pixar 3D"

# Create a voice profile for dialogue consistency
cinematic-script create-voice --character-id "char1" --name "Kutil" --personality "Mischievous, witty" --age "adult" --role "protagonist"

# Validate a prompt for anachronisms
cinematic-script validate-prompt --prompt "Your prompt here" --character-ids "char1,char2" --context-id <context-id>
```

### Storage

Save projects to Google Drive or local storage:

```bash
# Connect to Google Drive
cinematic-script connect-drive

# Connect to local storage
cinematic-script connect-local

# Check storage connection status
cinematic-script storage-status

# Save project to storage
cinematic-script save --title "My Story" --context-id <context-id> --script-id <script-id>
```

Storage implementation details:
- **Google Drive**: Uses Google OAuth2 for authentication. Credentials are stored securely in memory.
- **Local Storage**: Saves to the user's downloads folder as fallback.
- **Library**: Uses `googleapis` for Google Drive integration.

### Export

Export scripts in various formats:

```bash
# Export as Markdown (default)
cinematic-script export --script-id <script-id> --format markdown

# Export as JSON
cinematic-script export --script-id <script-id> --format json

# Export as plain text
cinematic-script export --script-id <script-id> --format text
```

## Features

- **Story Context Management**: Create and manage story settings, characters, and eras
- **Story Idea Generation**: Generate multiple story concepts with hooks and twists
- **Cinematic Script Writing**: Full scripts with camera angles, lighting, and shot types
- **Character Consistency**: Reference sheets and voice profiles for consistent characters
- **Environment Consistency**: Era-appropriate style guides and anachronism detection
- **YouTube Metadata**: Generate titles, descriptions, and SEO tags
- **Storage Integration**: Save to Google Drive or local storage
- **Export Options**: JSON, Markdown, or plain text formats

## When to Use

- Writing cinematic scripts or screenplays
- Creating stories with characters for animation/video
- Generating image/video prompts for AI tools (Midjourney, Sora, Veo, Runway)
- Getting cinematography guidance (camera angles, lighting, color grading)
- Maintaining character consistency across scenes
- Saving script projects to Google Drive

## Cinematography Reference

### Camera Angles

| Angle | Emotional Impact | Best For |
|-------|-----------------|----------|
| Eye-level | Connection, equality, neutrality | Dialogue, emotional moments |
| Low-angle | Power, dominance, heroism | Villain reveals, hero moments |
| High-angle | Vulnerability, weakness, overview | Defeat, establishing scale |
| Bird-eye | Insignificance, detachment, patterns | Epic scale, isolation |
| Worm-eye | Awe, grandeur, overwhelming presence | Monuments, giants, deities |
| Dutch angle | Unease, disorientation, tension | Chaos, dreams, horror |
| Overhead | Omniscience, surveillance | Table scenes, fight choreography |
| Shoulder-level | Intimate, casual, documentary feel | Walking conversations |
| Hip-level | Cowboy feel, casual tension | Westerns, standoffs |
| Knee-level | Childlike perspective, grounding | Children's stories, humility |

### Camera Movements

| Movement | Effect | Use For |
|----------|--------|---------|
| Static | Stability, observation | Contemplation, portraits |
| Pan | Revealing space | Following action horizontally |
| Tilt | Revealing height | Following vertical action |
| Dolly | Immersion, intimacy | Moving toward/away from subject |
| Truck | Following action | Side-to-side parallel movement |
| Crane | Epic scale, drama | Sweeping reveals, transitions |
| Handheld | Urgency, realism | Documentary, action, chaos |
| Steadicam | Smooth floating | Following through space, dreams |
| Zoom | Sudden focus, surprise | Dramatic emphasis, comedy |
| Rack-focus | Revealing connections | Shifting attention between subjects |

### Shot Types

| Shot | Framing | Emotional Impact |
|------|---------|-----------------|
| Establishing | Wide location | Sets scene, geography, time |
| Wide/Full | Subject + surroundings | Context, environment, scale |
| Medium | Waist up | Dialogue, body language |
| Close-up | Head/shoulders | Emotion, reaction, intimacy |
| Extreme close-up | Detail only (eyes, hands) | Intense emotion, symbolism |
| Over-shoulder | Past one subject to another | Conversation, perspective |
| POV | Character's view | Immersion, subjectivity |
| Insert | Object detail | Plot info, symbolism |
| Two-shot | Two subjects together | Relationship, tension |

### Lighting Techniques

| Technique | Mood | Best For |
|-----------|------|----------|
| Three-point | Professional, balanced | Dialogue, interviews |
| High-key | Happy, optimistic, bright | Comedy, commercials |
| Low-key | Dramatic, mysterious | Drama, horror, noir |
| Golden-hour | Romantic, nostalgic, magical | Romance, emotional moments |
| Blue-hour | Melancholic, mysterious | Urban, cityscapes |
| Chiaroscuro | Dramatic contrast | Art films, period pieces |
| Rim/backlight | Separation, ethereal | Silhouettes, divine presence |
| Practical | Realistic, natural | Candles, fires, lamps |
| God-rays | Divine, revelation | Spiritual moments, forests |
| Neon | Urban, futuristic | Cyberpunk, nightlife |

### Color Grading

| Style | Look | Genre |
|-------|------|-------|
| Teal-orange | Blockbuster cinematic | Action, sci-fi |
| Noir | High-contrast desaturated | Crime, mystery |
| Vintage/sepia | Warm, nostalgic | Period pieces, memory |
| Pastel | Soft, dreamy | Romance, coming-of-age |
| Bleach bypass | Desaturated, gritty | War, thriller |
| Cross-process | Surreal colors | Music videos, dreams |

## Image Prompt Format

When generating image prompts for AI tools:

```
[Shot type] [camera angle] of [subject doing action], [visual style] style,
[lighting technique], [composition rule], [color grading],
[era-appropriate details], [mood keywords], highly detailed, cinematic
```

Example:
```
Low-angle close-up of Kutil the purple rakshasa with mischievous golden eyes,
Pixar 3D style, dramatic underlighting with rim light, rule-of-thirds composition,
warm golden color grading, ancient Lanka palace background with ornate pillars,
playful yet mysterious mood, highly detailed, cinematic, 8k
```

## Output Structure

When saving a project, the following files are generated:

```
Story Title/
├── 00_INDEX.md           # Navigation
├── 01_SCRIPT_README.md   # Human-readable script
├── 02_IMAGE_PROMPTS.md   # All AI generation prompts
├── 03_CHARACTER_REFS.md  # Character design guides
├── 04_VOICE_GUIDES.md    # Dialogue consistency guides
├── 05_YOUTUBE_META.md    # Title, description, tags
└── 99_CONTEXT_INFO.md    # Story context and background
```

## Important Rules

1. **Always maintain character consistency** - include character's full visual description in every image prompt
2. **Never include anachronisms** - validate props, clothing, objects against the era
3. **Match cinematography to emotion** - use low angles for power, high angles for vulnerability
4. **Include both image and video prompts** - image prompts are static, video prompts describe motion
5. **Production-ready output** - every script should include enough detail for a team to produce it
6. **Respect the tone** - comedy needs comedic timing; drama needs longer holds on reactions

## License

MIT

## Author

Praveen Kumar
