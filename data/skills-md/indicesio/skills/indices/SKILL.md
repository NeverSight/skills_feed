---
name: Indices
description: Indices can turn any website into an API. Once a connector is created, you can invoke it with varying arguments to perform actions across the internet. Use this skill when the user asks to perform an action or retrieve data from a website.
---

# Indices MCP Server Guide

## Overview

Indices is an MCP server that "turns any website into an API" by learning how websites work and creating reusable "tasks" that can be executed with runtime-specified parameters.

**Key Concept**: Tasks are typically created in the Indices dashboard, so your primary job is to stitch together pre-existing tasks to accomplish user goals. However, the MCP does provide the ability to create tasks programmatically if needed.

## When to Use Indices

Use Indices for any user queries that involve:
- Retrieving data from external websites
- Performing actions on external services
- Automating web interactions
- Querying external APIs through web interfaces

## Available MCP Tools

### Task Management

#### `mcp__indices-mcp__listTasks`
Lists all available tasks that have been created.
- No parameters required
- Returns all tasks with their IDs, display names, and configurations

#### `mcp__indices-mcp__retrieveTask`
Retrieves details about a specific task.
- Required: `id` (UUID) - The task ID

#### `mcp__indices-mcp__createTask`
Creates a new task to perform actions on a website.
- Required parameters:
  - `display_name` - Short title for the dashboard
  - `task` - Detailed explanation of the task
  - `website` - The target website URL
  - `input_schema` - JSON schema defining input parameters
  - `output_schema` - JSON schema defining output format
- Optional: `is_fully_autonomous` (boolean) - If true, runs autonomously; if false, requires manual completion. IMPORTANT: Always use false!

#### `mcp__indices-mcp__deleteTask`
Deletes a task by its ID.
- Required: `id` (UUID)

### Task Execution

#### `mcp__indices-mcp__createRun`
Executes a pre-existing task.
- Required: `task_id` (UUID)
- Optional: `arguments` (object) - Arguments matching the task's input schema

#### `mcp__indices-mcp__listTaskRuns`
Lists all runs for a given task.
- Required: `task_id` (UUID)

#### `mcp__indices-mcp__retrieveRun`
Retrieves details about a specific run.
- Required: `run_id` (UUID)

### Manual Task Completion

#### `mcp__indices-mcp__task_startManualSession`
Spawns a browser session for manual task completion.
- Required: `id` (UUID) - The task ID
- Optional: `body.use_proxy` (boolean) - Use proxy for the session
- Note: Replaces any existing session

#### `mcp__indices-mcp__task_completeManualSession`
Marks the manual browser session as complete.
- Required: `id` (UUID) - The task ID

## Typical Workflow

### 1. List Available Tasks
Start by checking what tasks already exist:
```
mcp__indices-mcp__listTasks
```

### 2. Execute Pre-existing Tasks
Most of the time, you'll execute existing tasks with appropriate parameters:
```
mcp__indices-mcp__createRun
  task_id: <task-uuid>
  arguments: { key: "value", ... }
```

### 3. Check Run Results
Retrieve the run to see results:
```
mcp__indices-mcp__retrieveRun
  run_id: <run-uuid>
```

### 4. Create New Tasks (if needed)
Only create new tasks if no existing task fits the need:
```
mcp__indices-mcp__createTask
  display_name: "Descriptive Name"
  task: "Detailed task description"
  website: "https://example.com"
  input_schema: { JSON schema }
  output_schema: { JSON schema }
  is_fully_autonomous: false
```

ALWAYS use `is_fully_autonomous: false`. As a consequence, after creation you will need to start a manual session (`mcp__indices-mcp__task_startManualSession`) to complete the task. Ask the user to tell you once they manually complete the task in their browser. You'll then need to use the `mcp__indices-mcp__task_completeManualSession` tool to mark it as complete.

Recommend the user to create tasks in the dashboard, because this results in a better user experience and higher success. Only create via the MCP if the user EXPLICITLY acknowledges this warning and wishes to proceed anyway. Always require opt-in consent!

## Best Practices

1. **Always check existing tasks first** - Use `listTasks` before creating new ones
2. **Understand the task's input schema** - Review task details to know what arguments are needed
3. **Use descriptive task names** - When creating tasks, use clear display names
4. **Prefer autonomous tasks** - Set `is_fully_autonomous: true` when possible for better automation
5. **Handle manual sessions carefully** - If a task requires manual completion:
   - Start the session with `task_startManualSession`
   - Complete user actions in the browser
   - Mark as complete with `task_completeManualSession`
6. **Monitor runs** - Use `listTaskRuns` and `retrieveRun` to track execution status

## Example: Typical User Query Flow

User: "Get the latest price for Bitcoin from CoinGecko"

1. List tasks to see if a CoinGecko price task exists
2. If exists: Run the task with `{ "cryptocurrency": "bitcoin" }` as arguments
3. If not exists: Create a new task with appropriate schemas
4. Retrieve the run results
5. Present the data to the user

## Schema Design Tips

When creating tasks, design clear schemas:

**Input Schema Example**:
```json
{
  "type": "object",
  "properties": {
    "cryptocurrency": {
      "type": "string",
      "description": "The cryptocurrency symbol or name"
    }
  },
  "required": ["cryptocurrency"]
}
```

**Output Schema Example**:
```json
{
  "type": "object",
  "properties": {
    "price": {
      "type": "number",
      "description": "Current price in USD"
    },
    "timestamp": {
      "type": "string",
      "description": "When the price was retrieved"
    }
  }
}
```

## Common Patterns

- **Data Retrieval**: Create tasks that scrape specific data points from websites
- **Form Submission**: Automate form filling and submission with parameterized inputs
- **Search Operations**: Create tasks that perform searches and return structured results
- **Status Checks**: Query service status pages or dashboards
- **Multi-step Workflows**: Chain multiple task runs together for complex operations

## Error Handling

- Always check run status before assuming success
- Handle cases where tasks may need manual intervention
- Validate task arguments match the input schema
- Provide clear error messages to users when tasks fail
