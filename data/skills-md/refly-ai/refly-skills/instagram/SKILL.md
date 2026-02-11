---
name: instagram
description: "Integrate with Instagram for social media. Use when you need to: (1) post content to Instagram, (2) manage media and insights, or (3) automate Instagram publishing workflows."
version: 1.0.0
skillId: skp-egurs3nyo1s6488eccidxo3x
workflowId: c-z15u3sezyx46cvplswiukpel
installationId: skpi-ouiqydzmtpr5oeu9i6b6akfn
category: action
---

# Instagram

Integrate with Instagram for social media. Use when you need to: (1) post content to Instagram, (2) manage media and insights, or (3) automate Instagram publishing workflows.

## Input

Provide input as JSON:

```json
{
  "post_caption": "Caption text for your Instagram post",
  "post_image": "<file-reference>",
  "insights_period": "Time period for analytics insights (e.g., 'last 7 days', 'last 30 days')"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-ouiqydzmtpr5oeu9i6b6akfn --input '{
  "image_url": "https://example.com/image.jpg",
  "caption": "Check out our new product! #launch"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-z15u3sezyx46cvplswiukpel"
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
- **Format**: JSON post confirmation
- **Action**: Confirm post published successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
