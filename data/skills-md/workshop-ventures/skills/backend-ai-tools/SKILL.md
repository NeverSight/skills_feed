---
name: backend-ai-tools
description: Create AI tools for use with Vercel AI SDK agents. Use when asked to "create AI tools", "add agent tools", "create tool for AI", or "add tools to agent".
---

# Backend AI Tools Creation

Create tools for AI agents using the Vercel AI SDK `tool()` function with Zod schemas.

## Overview

Tools allow AI agents to:
- Query databases
- Create/update records
- Call external APIs
- Perform calculations
- Validate data

## File Structure

```
apps/backend/src/ai/tools/
├── workflow.ts       # Workflow-related tools
├── workflowRun.ts    # Workflow run tools
└── {resource}.ts     # New resource tools
```

## Creating Tools

### Basic Tool Pattern

```typescript
import { tool } from 'ai';
import { z } from 'zod';
import { ResourceStatusOptions } from '@{project}/types';
import Resource from '../../models/Resource';

const createResourceSchema = z.object({
  name: z.string().describe('Name of the resource'),
  description: z.string().optional().describe('Optional description'),
  status: z.enum(ResourceStatusOptions).optional().describe('Initial status'),
});

export const createResourceTool = tool({
  description: `Create a new resource in the database.
    Returns the resourceId for use in subsequent operations.`,
  inputSchema: createResourceSchema,
  execute: async (input) => {
    const resource = new Resource({
      name: input.name,
      description: input.description,
      status: input.status || 'active',
    });
    await resource.save();
    return {
      success: true,
      resourceId: resource.id,
      message: `Created resource "${input.name}" with ID: ${resource.id}`,
    };
  },
});
```

### Tool with Context

When tools need user context or other dependencies:

```typescript
export interface ToolContext {
  userId: string;
  accountId: string;
}

// Tool factory that accepts context
export const createListUserTasksTool = (context: ToolContext) => tool({
  description: 'List tasks for the current user',
  inputSchema: z.object({
    status: z.enum(['pending', 'completed', 'all']).optional().describe('Filter tasks by status'),
    limit: z.number().optional().default(10).describe('Maximum number of tasks to return'),
  }),
  execute: async (input) => {
    const query: Record<string, unknown> = { userId: context.userId };
    if (input.status && input.status !== 'all') query.status = input.status;

    const tasks = await Task.find(query).limit(input.limit || 10).sort({ createdAt: -1 });
    return { success: true, count: tasks.length, tasks: tasks.map(t => ({ id: t.id, title: t.title, status: t.status })) };
  },
});
```

## Schema Design

### Descriptive Field Descriptions

The `.describe()` method is crucial - it tells the AI what each field means:

```typescript
const addNodeSchema = z.object({
  workflowId: z.string().describe('The workflowId of the workflow to add the node to'),
  id: z.string().describe('Unique identifier for the node (use format: node-1, node-2, etc.)'),
  type: z.enum(NodeTypeOptions).describe('The type of node based on its purpose'),
  title: z.string().describe('Short title for the step (max 50 characters)'),
  content: z.string().describe('Detailed instructions for this step'),
});
```

### Enum Fields

Import enum options from `@{project}/types`:

```typescript
import { StatusOptions, PriorityOptions } from '@{project}/types';

const updateSchema = z.object({
  status: z.enum(StatusOptions).describe('New status: active, inactive, or archived'),
  priority: z.enum(PriorityOptions).optional().describe('Priority level if changing'),
});
```

## Tool Description Best Practices

### Be Specific About Purpose

```typescript
export const addNodeTool = tool({
  description: `Add a new node (step) to an existing workflow.
    Node types:
    - 'action': Steps that require doing something
    - 'inspection': Steps that require checking
    - 'decision': Yes/No branching points
    - 'warning': Safety-critical steps`,
  inputSchema: addNodeSchema,
  execute: async (input) => { /* ... */ },
});
```

### Explain Return Values

```typescript
export const createWorkflowTool = tool({
  description: `Create a new workflow in the database.
    Call this first before adding nodes and edges.
    Returns the workflowId which you'll need for subsequent addNode and addEdge calls.`,
  inputSchema: createWorkflowSchema,
  execute: async (input) => { /* ... */ },
});
```

## Return Value Patterns

```typescript
// Success
return { success: true, resourceId: resource.id, message: `Created resource "${input.name}"` };

// Success with count
return { success: true, message: `Added node`, nodeCount: result.nodes.length };

// Error
return { success: false, message: `Workflow with ID "${workflowId}" not found` };

// List response
return { success: true, count: items.length, items: items.map(item => ({ id: item.id, name: item.name })) };
```

## Using Tools with Agents

```typescript
// Direct export
import { projectTools } from '../tools/project';
const agent = new MyAgent(context, projectTools);

// Combining multiple tool sets
const allTools = { ...workflowTools, ...projectTools };
const agent = new MyAgent(context, allTools);

// Context-aware tools
const tools = createProjectTools({ userId: user.uid, accountId: user.accountId });
```

## Complete Example

See [references/complete-example.md](references/complete-example.md) for a full project tools implementation with CRUD operations.

## Checklist

1. **Create tool file** in `apps/backend/src/ai/tools/{resource}.ts`
2. **Define Zod schemas** with descriptive `.describe()` on each field
3. **Create tools** using `tool()` from 'ai' package
4. **Write clear descriptions** explaining purpose and return values
5. **Handle errors** with `success: false` responses
6. **Export tool collection** as named object
7. **Import in agent** and pass to agent constructor
