---
name: facebook
description: "Integrate with Facebook for social media management. Use when you need to: (1) post updates to Facebook pages, (2) share content and media, or (3) automate Facebook page workflows."
version: 1.0.0
skillId: skp-ary4qi0tx153f8ms8iwsxsmr
workflowId: c-opg0f8e7j3m1fmjhjakmhpfk
installationId: skpi-nyozn1z7255wdo122km3efhb
category: action
---

# Facebook

Integrate with Facebook for social media management. Use when you need to: (1) post updates to Facebook pages, (2) share content and media, or (3) automate Facebook page workflows.

## Input

Provide input as JSON:

```json
{
  "post_content": "The content text for your Facebook post",
  "page_id": "Your Facebook Page ID (optional, leave empty to post to personal timeline)",
  "post_type": "Type of post: status, photo, video, or link"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-nyozn1z7255wdo122km3efhb --input '{
  "page_id": "your-page-id",
  "message": "Check out our latest product update!"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-opg0f8e7j3m1fmjhjakmhpfk"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm post published
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON post confirmation (post ID, link)
- **Action**: Confirm post published successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
