---
name: google-maps
description: "Integrate with Google Maps for location services. Use when you need to: (1) geocode addresses to coordinates, (2) search for places, or (3) get directions and location data."
version: 1.0.0
skillId: skp-r598mda394rkxeplzlfiglle
workflowId: c-b6hhdfj7pt9c1yrowfbmx5vc
installationId: skpi-cvy0z7sx46moqd1w590mygq3
category: text-data
---

# Google Maps

Integrate with Google Maps for location services. Use when you need to: (1) geocode addresses to coordinates, (2) search for places, or (3) get directions and location data.

## Input

Provide input as JSON:

```json
{
  "search_query": "Location or place name to search for (e.g., 'Eiffel Tower', 'restaurants in New York', '1600 Amphitheatre Parkway')",
  "place_type": "Type of place to search for (e.g., 'restaurant', 'hotel', 'museum', 'cafe'). Leave empty for general search."
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-cvy0z7sx46moqd1w590mygq3 --input '{
  "address": "1600 Amphitheatre Parkway, Mountain View, CA",
  "action": "geocode"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-b6hhdfj7pt9c1yrowfbmx5vc"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get location data from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: JSON location/geocoding data
- **Action**: Display location information to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
