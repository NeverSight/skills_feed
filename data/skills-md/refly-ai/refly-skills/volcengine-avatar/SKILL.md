---
name: volcengine-avatar
description: "Create AI digital humans using Volcengine Avatar. Use when you need to: (1) create AI avatar presenters, (2) generate avatar videos with speech, or (3) build virtual spokespersons for content."
version: 1.0.0
skillId: skp-yko91g1z2u9yy0ghcpupg5p5
workflowId: c-ucda40jk4sf3s27hr8e7s62d
installationId: skpi-ixed341d48t5k1sdp4g8c8n0
category: file-generation
---

# Volcengine Avatar

Create AI digital humans using Volcengine Avatar. Use when you need to: (1) create AI avatar presenters, (2) generate avatar videos with speech, or (3) build virtual spokespersons for content.

## Input

Provide input as JSON:

```json
{
  "avatar_image": "<file-reference>",
  "audio_file": "<file-reference>",
  "video_title": "Title for the generated avatar video",
  "avatar_name": "Name for the digital human avatar role"
}
```

## Execution (Pattern A: File Generation)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-ixed341d48t5k1sdp4g8c8n0 --input '{
  "script": "Welcome to our product demonstration video.",
  "avatar_id": "default"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-ucda40jk4sf3s27hr8e7s62d"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Download and Show Result

```bash
# Get files from this run
FILES=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.files[]')

# Download and open each file
echo "$FILES" | jq -c '.' | while read -r file; do
  FILE_ID=$(echo "$file" | jq -r '.fileId')
  FILE_NAME=$(echo "$file" | jq -r '.name')
  if [ -n "$FILE_ID" ] && [ "$FILE_ID" != "null" ]; then
    refly file download "$FILE_ID" -o "$HOME/Desktop/${FILE_NAME}"
    open "$HOME/Desktop/${FILE_NAME}"
  fi
done
```

## Expected Output

- **Type**: Video
- **Format**: .mp4 avatar video file
- **Location**: `~/Desktop/`
- **Action**: Opens automatically to show user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
