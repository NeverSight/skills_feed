---
name: jira-transitions
description: Move Jira issues through workflow states. Use when transitioning issues (To Do, In Progress, Done) or setting resolutions.
---

# Jira Transitions Skill

## Purpose
Move issues through workflow states. Get available transitions and execute status changes.

## When to Use
- Moving issues to different statuses (To Do → In Progress → Done)
- Getting available transitions for an issue
- Bulk transitioning issues
- Setting resolution when closing issues

## Prerequisites
- Authenticated JiraClient (see jira-auth skill)
- Issue transition permissions
- Knowledge of workflow structure

## Important Notes

**Transition IDs are NOT standardized** - they vary by:
- Jira instance
- Project
- Workflow configuration

**Always query available transitions first** before attempting to transition.

## Implementation Pattern

### Step 1: Define Types

```typescript
interface Transition {
  id: string;
  name: string;
  to: {
    id: string;
    name: string;
    statusCategory: {
      id: number;
      key: string;
      name: string;
    };
  };
  fields?: Record<string, {
    required: boolean;
    name: string;
    allowedValues?: Array<{ id: string; name: string }>;
  }>;
}

interface TransitionsResponse {
  transitions: Transition[];
}
```

### Step 2: Get Available Transitions

```typescript
async function getTransitions(
  client: JiraClient,
  issueKeyOrId: string
): Promise<Transition[]> {
  const response = await client.request<TransitionsResponse>(
    `/issue/${issueKeyOrId}/transitions?expand=transitions.fields`
  );
  return response.transitions;
}
```

### Step 3: Find Transition by Name

```typescript
async function findTransitionByName(
  client: JiraClient,
  issueKeyOrId: string,
  targetStatusName: string
): Promise<Transition | null> {
  const transitions = await getTransitions(client, issueKeyOrId);
  return transitions.find(
    t => t.name.toLowerCase() === targetStatusName.toLowerCase() ||
         t.to.name.toLowerCase() === targetStatusName.toLowerCase()
  ) || null;
}
```

### Step 4: Execute Transition

```typescript
interface TransitionOptions {
  resolution?: { name: string } | { id: string };
  comment?: string;
  fields?: Record<string, any>;
}

async function transitionIssue(
  client: JiraClient,
  issueKeyOrId: string,
  transitionId: string,
  options: TransitionOptions = {}
): Promise<void> {
  const body: any = {
    transition: { id: transitionId },
  };

  if (options.resolution || options.fields) {
    body.fields = { ...options.fields };
    if (options.resolution) {
      body.fields.resolution = options.resolution;
    }
  }

  if (options.comment) {
    body.update = {
      comment: [
        {
          add: {
            body: {
              type: 'doc',
              version: 1,
              content: [
                {
                  type: 'paragraph',
                  content: [{ type: 'text', text: options.comment }],
                },
              ],
            },
          },
        },
      ],
    };
  }

  await client.request(`/issue/${issueKeyOrId}/transitions`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
```

### Step 5: High-Level Transition Helper

```typescript
async function moveIssueTo(
  client: JiraClient,
  issueKeyOrId: string,
  targetStatus: string,
  options: TransitionOptions = {}
): Promise<boolean> {
  const transition = await findTransitionByName(client, issueKeyOrId, targetStatus);

  if (!transition) {
    console.error(`No transition found to status: ${targetStatus}`);
    return false;
  }

  // Check if resolution is required
  if (transition.fields?.resolution?.required && !options.resolution) {
    // Default to "Done" resolution
    options.resolution = { name: 'Done' };
  }

  await transitionIssue(client, issueKeyOrId, transition.id, options);
  return true;
}
```

### Step 6: Bulk Transition

```typescript
async function bulkTransition(
  client: JiraClient,
  issueKeys: string[],
  targetStatus: string,
  options: TransitionOptions = {}
): Promise<{ success: string[]; failed: string[] }> {
  const results = { success: [] as string[], failed: [] as string[] };

  for (const issueKey of issueKeys) {
    try {
      const success = await moveIssueTo(client, issueKey, targetStatus, options);
      if (success) {
        results.success.push(issueKey);
      } else {
        results.failed.push(issueKey);
      }
    } catch (error) {
      results.failed.push(issueKey);
    }
  }

  return results;
}
```

## Common Transitions

Most Jira projects have these standard transitions:

| From Status | Transition Name | To Status |
|-------------|-----------------|-----------|
| To Do | Start Progress | In Progress |
| In Progress | Done | Done |
| In Progress | Stop Progress | To Do |
| Done | Reopen | To Do |

**Note**: These names vary by workflow configuration.

## Resolution Values

When transitioning to "Done", you often need a resolution:

| Resolution | Description |
|------------|-------------|
| Done | Work completed |
| Won't Do | Not planning to do |
| Duplicate | Already exists |
| Cannot Reproduce | Cannot reproduce issue |

## curl Examples

### Get Available Transitions
```bash
curl -X GET "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123/transitions?expand=transitions.fields" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Accept: application/json"
```

### Execute Transition (Simple)
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123/transitions" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": { "id": "21" }
  }'
```

### Transition with Resolution (for Done)
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123/transitions" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": { "id": "31" },
    "fields": {
      "resolution": { "name": "Done" }
    }
  }'
```

### Transition with Comment
```bash
curl -X POST "$JIRA_BASE_URL/rest/api/3/issue/SCRUM-123/transitions" \
  -H "Authorization: Basic $(echo -n 'email:token' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": { "id": "21" },
    "update": {
      "comment": [
        {
          "add": {
            "body": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [{ "type": "text", "text": "Moving to In Progress" }]
                }
              ]
            }
          }
        }
      ]
    }
  }'
```

## API Response (204 No Content)

A successful transition returns **204 No Content** with an empty body.

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Invalid transition ID | Query transitions first |
| 400 Bad Request | Missing required resolution | Add resolution field |
| 403 Forbidden | No permission to transition | Check workflow permissions |
| 404 Not Found | Issue doesn't exist | Verify issue key |

### Error Response Example
```json
{
  "errorMessages": [
    "You must specify a resolution when transitioning issues to the 'Done' status."
  ],
  "errors": {
    "resolution": "Resolution is required."
  }
}
```

## Workflow Discovery Pattern

```typescript
async function discoverWorkflow(
  client: JiraClient,
  issueKeyOrId: string
): Promise<Map<string, Transition[]>> {
  // Get transitions from current state
  const transitions = await getTransitions(client, issueKeyOrId);

  console.log(`Available transitions from current state:`);
  for (const t of transitions) {
    console.log(`  ${t.id}: ${t.name} → ${t.to.name}`);
    if (t.fields?.resolution?.required) {
      console.log(`    (requires resolution)`);
    }
  }

  return new Map([
    ['current', transitions]
  ]);
}
```

## Common Mistakes
- Using transition ID without querying first
- Forgetting resolution when moving to Done
- Assuming transition IDs are same across projects
- Not handling 204 response (empty body is success)

## References
- [Transitions API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-transitions-get)

## Version History
- 2025-12-10: Created
