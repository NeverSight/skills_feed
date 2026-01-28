---
name: pulumi-neo
description: Pulumi Neo AI-powered infrastructure automation agent. Use when working with Pulumi Neo for conversational infrastructure management, creating Neo tasks, monitoring task progress, infrastructure analysis, maintenance operations, or automating multi-step cloud workflows through natural language.
---

# Pulumi Neo Skill

Pulumi Neo is an AI agent for platform engineers that enables conversational infrastructure management through natural language.

## Prerequisites

- **Pulumi Cloud account** with Neo access
- **PULUMI_ACCESS_TOKEN** environment variable set with your Personal Access Token
- **Organization**: Required for all Neo API calls

## Detecting Organization

```bash
# Get current Pulumi organization from CLI
pulumi org get-default

# If no default org or using self-managed backend, ask user for organization name
```

If `pulumi org get-default` returns an error or shows a non-cloud backend, prompt the user for their Pulumi Cloud organization name.

## Claude Code Integration

**RECOMMENDED: Use MCP tools directly** - they work natively with Claude Code:
```
mcp__pulumi__neo-bridge      # Create and interact with Neo tasks
mcp__pulumi__neo-get-tasks   # List existing tasks
mcp__pulumi__neo-continue-task # Continue polling a task
```

**If using the Python script, ALWAYS add `--no-poll`:**
```bash
# REQUIRED: --no-poll prevents blocking (script will hang without it)
python scripts/neo_task.py --org <org> --message "Your message" --no-poll

# Check events separately
python scripts/neo_task.py --org <org> --task-id <task-id> --get-events
```

**WARNING:** Never run the script without `--no-poll` in Claude Code - the polling loop will block indefinitely.

## Using the Python Script

The script handles Neo task creation, polling, and management:

```bash
# Create a task and poll for updates (interactive/terminal use)
python scripts/neo_task.py --org <org-name> --message "Help me optimize my Pulumi stack"

# Create task without polling (CI/CD or programmatic use)
python scripts/neo_task.py --org <org-name> --message "Analyze this" --no-poll

# Create task with stack context
python scripts/neo_task.py --org <org-name> \
  --message "Analyze this stack" \
  --stack-name prod --stack-project my-infra --no-poll

# Create task with repository context
python scripts/neo_task.py --org <org-name> \
  --message "Review this infrastructure code" \
  --repo-name my-repo --repo-org my-github-org --no-poll

# List existing tasks
python scripts/neo_task.py --org <org-name> --list

# Fetch current events (single request, no polling)
python scripts/neo_task.py --org <org-name> --task-id <task-id> --get-events

# Poll an existing task for updates (interactive)
python scripts/neo_task.py --org <org-name> --task-id <task-id>

# Send approval for a pending request
python scripts/neo_task.py --org <org-name> --task-id <task-id> --approve

# Cancel a pending request
python scripts/neo_task.py --org <org-name> --task-id <task-id> --cancel
```

## Neo Task Workflow

### 1. Creating Tasks

Tasks are created with a natural language message describing what you want Neo to do:

- **Infrastructure analysis**: "Analyze my production stack for security issues"
- **Maintenance operations**: "Help me upgrade my Kubernetes cluster"
- **Configuration changes**: "Add monitoring to my Lambda functions"
- **Multi-step workflows**: "Set up a complete CI/CD pipeline for this project"

### 2. Entity Context

Provide context to Neo by attaching entities:

| Entity Type | Use Case |
|-------------|----------|
| `stack` | Reference a Pulumi stack (name + project) |
| `repository` | Reference a code repository (name + org + forge) |
| `pull_request` | Reference a PR (number + merged status + repository) |
| `policy_issue` | Reference a governance policy issue (id) |

### 3. Task Status

| Status | Description |
|--------|-------------|
| `pending` | Task is queued |
| `running` | Neo is processing the task |
| `waiting_for_approval` | Neo needs user confirmation to proceed |
| `completed` | Task finished successfully |
| `failed` | Task encountered an error |

### 4. Approval Flow

When Neo requires confirmation for an operation:

1. Task status changes to `waiting_for_approval`
2. Event contains `approval_request_id`
3. User reviews the proposed changes
4. Send approval or cancellation via the API

## Common Workflows

### Analyze Infrastructure

```bash
python scripts/neo_task.py --org myorg \
  --message "What security improvements can I make to my AWS infrastructure?" \
  --stack-name prod --stack-project aws-infra
```

### Fix Policy Violations

```bash
python scripts/neo_task.py --org myorg \
  --message "Help me fix the policy violations in my production stack"
```

### Generate Pulumi Code

```bash
python scripts/neo_task.py --org myorg \
  --message "Create a new Pulumi TypeScript project for a containerized web app on AWS ECS"
```

### Review Pull Request

```bash
python scripts/neo_task.py --org myorg \
  --message "Review the infrastructure changes in this PR" \
  --repo-name infra --repo-org myorg --repo-forge github
```

## Best Practices

### Clear Instructions
- Be specific about what you want Neo to do
- Include relevant context (stack names, regions, requirements)
- Specify constraints (budget, compliance requirements)

### Entity Context
- Always attach relevant stack or repository entities
- This helps Neo understand the scope of your request

### Approval Workflow
- Review Neo's proposed changes carefully before approving
- Neo generates pull requests for infrastructure changes
- Use the preview feature to understand impact before deployment

## Troubleshooting

### Authentication Errors (401)
```bash
# Verify token is set
echo $PULUMI_ACCESS_TOKEN

# Test authentication
curl -H "Authorization: token $PULUMI_ACCESS_TOKEN" \
  https://api.pulumi.com/api/user
```

### Organization Not Found (404)
- Verify organization name with `pulumi org get-default`
- Ensure your token has access to the organization

### Cannot Respond While Request Pending (409)
- Wait for Neo to finish processing before sending new messages
- Poll for status updates before responding

## References

- [references/pulumi-neo-api.md](references/pulumi-neo-api.md) - Complete API documentation
