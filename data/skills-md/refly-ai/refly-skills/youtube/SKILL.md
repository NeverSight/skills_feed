---
name: youtube
description: "Integrate with YouTube for video management. Use when you need to: (1) upload videos to YouTube, (2) manage channel content, or (3) retrieve video analytics and insights."
version: 1.0.0
skillId: skp-z40t25bhzfl8riuieuy5sy37
workflowId: c-i7p2l6i0ceoa8urcbtk06rbi
installationId: skpi-jdgmfvnvnx0fxm3npchfuqwg
category: action
---

# Youtube

Integrate with YouTube for video management. Use when you need to: (1) upload videos to YouTube, (2) manage channel content, or (3) retrieve video analytics and insights.

## Input

Provide input as JSON:

```json
{
  "video_file": "<file-reference>",
  "video_title": "Title for your YouTube video",
  "video_description": "Description for your YouTube video",
  "video_tags": "Tags for your video (comma-separated)",
  "privacy_status": "Privacy status: public, private, or unlisted"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-jdgmfvnvnx0fxm3npchfuqwg --input '{
  "video_id": "dQw4w9WgXcQ",
  "action": "get_details"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-i7p2l6i0ceoa8urcbtk06rbi"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm action completed
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON video/channel data
- **Action**: Confirm video uploaded or details retrieved

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
