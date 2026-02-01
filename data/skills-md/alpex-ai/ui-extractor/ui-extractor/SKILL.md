---
name: ui-extractor
description: Analyze screen recordings and websites to extract implementation specs, design systems, and UI patterns.
license: MIT
compatibility: Requires ffmpeg and ffprobe for video processing. Install with "brew install ffmpeg" on macOS.
allowed-tools: Bash(ffmpeg:*) Bash(ffprobe:*) Bash(jq:*) Bash(node:*) Bash(npm:*) Bash(./scripts/*) Read Write
metadata:
  author: alpex-ai
  version: "1.0.0"
  repository: https://github.com/alpex-ai/ui-extractor
---

# UI Extractor

Extract implementation specs, design systems, and component catalogs from any UI source.

## What It Does

**Input:** A URL, screen recording, or authenticated browser tab
**Output:** Implementation spec with components, design tokens, user flows, and Figma export

### Use Cases

- **Reverse engineer a competitor's UI** → Get their exact colors, typography, spacing, components
- **Document an existing app** → Auto-generate component inventory and design tokens
- **Match a reference design** → Compare your app against a target and get prioritized changes
- **Extract from authenticated sites** → Analyze internal dashboards, Figma files, or logged-in apps

## Supported Inputs

| Input Type | How to Use | What Happens |
|------------|------------|--------------|
| **URL** | `Analyze stripe.com` | Records the site with Playwright, extracts frames, analyzes |
| **Local Recording** | `Analyze ./recording.mov` | Extracts frames from your file, analyzes |
| **Browser Tab** | `Analyze my open Chrome tab` | Records your authenticated tab via Chrome MCP, analyzes |

## Example Commands

```
# Analyze any website (auto-records it)
Analyze linear.app

# Mobile or dark mode
Analyze stripe.com in mobile dark mode

# Just get the design system
Extract the design system from notion.com and export to Figma

# Compare your app to a reference
Compare ./my-app.mov with stripe.com

# Analyze an authenticated page you have open
Analyze my open Chrome tab
```

## Output

### Implementation Spec
- Screen inventory with frame references
- Component catalog (buttons, cards, modals, etc.)
- Design system tokens (colors, typography, spacing, shadows)
- User flows with triggers and transitions
- Implementation recommendations

### Design System (JSON)
```json
{
  "colors": { "primary": { "value": "#007AFF", "usage": "Primary actions" } },
  "typography": { "heading": { "size": "24px", "weight": "600" } },
  "spacing": { "sm": "8px", "md": "16px", "lg": "24px" }
}
```

### Export Formats
- CSS custom properties
- Tailwind config
- Figma Variables (JSON)
- Direct Figma push via MCP

---

# Agent Instructions

## Workflow Overview

1. **Resolve input** → URL, local file, or browser tab
2. **Capture frames** → Record (if URL/tab) or extract from video
3. **Analyze frames** → Identify components, colors, typography, flows
4. **Generate output** → Implementation spec, design system, or comparison

## Step 1: Resolve Input

**URL detected** (contains `.com`, `.io`, `.app`, `www.`, or `http`):
```bash
./scripts/record-website.sh "https://example.com" --analyze --quality default
```

Options: `--mobile`, `--dark-mode`, `--duration <secs>`

**Local file provided:**
Validate exists, check extension (`.mov`, `.mp4`, `.webm`)

**Browser tab requested** (mentions "tab", "browser", "Chrome", "open"):
Use Chrome MCP to record the tab:
1. Get tab context
2. Start GIF recording
3. Scroll/hover while recording
4. Export to `./recordings/tab-recording.gif`
5. Extract frames: `./scripts/extract-frames.sh ./recordings/tab-recording.gif ./frames`

**No path provided:**
Run `./scripts/detect-recording.sh` to find recent recordings

## Step 2: Validate Duration

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_PATH"
```

- **> 5 min**: Error, ask user to trim
- **> 1 min**: Warn about token usage
- **≤ 1 min**: Proceed

## Step 3: Extract Frames

```bash
# Standard extraction
./scripts/extract-frames.sh "$VIDEO_PATH" "./frames" --quality default

# High quality for short videos (<15s)
./scripts/extract-frames.sh "$VIDEO_PATH" "./frames" --quality high

# With motion analysis
./scripts/extract-frames.sh "$VIDEO_PATH" "./frames" --include-metadata
```

Quality levels:
- `low` (0.5fps): Videos >60s
- `default` (1fps): Most recordings
- `high` (2fps): Short/complex videos

## Step 4: Analyze Frames

Load frames and analyze using `references/frame-analysis-prompt.md`:

1. **Screens**: Identify distinct screens/states
2. **Components**: Catalog reusable UI elements
3. **Design System**: Colors, typography, spacing, shadows
4. **User Flows**: Screen transitions and triggers
5. **Implementation**: Component hierarchy, state hints

## Step 5: Generate Output

**Full Analysis** (default):
Output markdown implementation spec with all sections.

**Design System Only**:
Output JSON following `references/design-system-schema.md`.

Export to Figma:
```bash
./scripts/figma-export.sh --design-system ./output/design-system.json --format figma-tokens
```

**Comparison Mode**:
1. Analyze reference first
2. Analyze user's app
3. Output gap analysis with prioritized changes

## Error Handling

**File access denied (macOS security):**
```
I can't access ~/Desktop directly. Run this to copy your recording:
cp ~/Desktop/Screen\ Recording*.mov ./recording.mov
Then: "Analyze ./recording.mov"
```

**FFmpeg missing:**
```
Install ffmpeg: brew install ffmpeg
```

**Video too long:**
```
This video is X minutes. Please trim to under 5 minutes.
```

## Trigger Phrases

| Intent | Phrases |
|--------|---------|
| URL | "Analyze stripe.com", "Record linear.app", "Extract from example.com" |
| Browser Tab | "Analyze my open tab", "Record my Chrome tab", "Extract from this authenticated page" |
| Local File | "Analyze ./recording.mov", "Extract from this video" |
| Design System | "Extract the design system", "Get colors and typography", "Export to Figma" |
| Comparison | "Compare my app with...", "What's different from...", "Match this reference" |

## Dependencies

Required:
- `ffmpeg` / `ffprobe` - Video processing
- `node` ≥18 - Website recording

Optional:
- `jq` - Figma export
- Chrome MCP - Browser tab recording
- Figma MCP or `FIGMA_ACCESS_TOKEN` - Direct Figma push

## Reference Documents

- `references/frame-analysis-prompt.md` - Analysis prompt structure
- `references/design-system-schema.md` - Design system JSON schema
- `references/comparison-guide.md` - Comparison workflow
- `references/figma-integration.md` - Figma export details
