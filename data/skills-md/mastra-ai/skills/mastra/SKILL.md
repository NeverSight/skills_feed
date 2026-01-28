---
name: mastra
description: Comprehensive guide for building AI applications with Mastra, the TypeScript AI framework for agents and workflows. Covers LLM agents with tools and memory, multi-step workflows with branching/parallel execution, storage backends (Postgres/LibSQL), RAG/vector search, and custom tool creation. Use when building conversational agents, automated workflows, RAG systems, or any Mastra TypeScript/JavaScript application. Includes 27+ production-ready code patterns, API verification guidance, troubleshooting, and best practices.
license: Apache-2.0
metadata:
  author: Mastra
  version: "1.0.0"
  repository: https://github.com/mastra-ai/skills
---

# Mastra Development Guide

Comprehensive guide for building AI applications with Mastra.

---

## Prerequisites

```bash
pnpm add @mastra/core zod
```

Install additional packages only when needed:
- Storage: `@mastra/pg`, `@mastra/libsql`, `@mastra/mongodb`
- RAG: `@mastra/rag`
- Memory: `@mastra/memory`

---

## Critical Knowledge

⚠️ **Always verify against current code**:
1. **Use `mastra-embedded-docs-look-up` skill** for current API signatures
2. **Check `node_modules/@mastra/*/dist/docs/`** for package-specific documentation
3. **Search source code**: `node_modules/@mastra/*/src/`
4. **Fallback to docs**: [mastra.ai/docs](https://mastra.ai/docs)

⚠️ **ES2022 Required** - CommonJS will fail. Must use `"target": "ES2022"`.

---

## Working Guidelines

1. **Minimal configuration**: Only specify options that differ from defaults
2. **Check embedded docs first**: Use `mastra-embedded-docs-look-up` skill
3. **Verify TypeScript config**: Must be ES2022, not CommonJS
4. **Test in Studio**: Run `npm run dev` → http://localhost:4111
5. **Model format**: Always use `provider/model` (e.g., `openai/gpt-4o`)
6. **Environment variables**: Load with `dotenv/config` or native `.env` support

---

## Agent vs Workflow

| Use | When |
|-----|------|
| **Agent** | Open-ended tasks (support, research) - reasons, decides tools, retains memory |
| **Workflow** | Defined sequences (pipelines, approvals) - orchestrates specific steps in order |

---

## TypeScript Config (Required)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler"
  }
}
```

**Critical:** CommonJS causes errors. Must use ES2022.

---

## Project Structure

```
src/mastra/
├── tools/       # Custom tools
├── agents/      # Agent configs
├── workflows/   # Workflows
└── index.ts     # Mastra instance
```

---

## Environment Variables

```env
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_GENERATIVE_AI_API_KEY=...
```

---

## Verifying Current APIs

**Before writing code**, verify the current API:

```bash
# Check what's exported from @mastra/core
ls node_modules/@mastra/core/dist/docs/

# View SOURCE_MAP.json for complete API surface
cat node_modules/@mastra/core/dist/docs/SOURCE_MAP.json

# Search for specific exports
grep -r "export.*Agent" node_modules/@mastra/core/src/
```

**Or use the skill**: `mastra-embedded-docs-look-up`

---

## Quick Reference

### Basic Agent
```typescript
new Agent({
  id: 'my-agent',
  name: 'My Agent',
  instructions: 'You are helpful',
  model: 'openai/gpt-4o',
  tools: { myTool }  // optional
})
```

### Basic Workflow
```typescript
createWorkflow({
  id: 'my-workflow',
  inputSchema: z.object({ input: z.string() }),
  outputSchema: z.object({ output: z.string() })
})
  .then(step1)
  .commit()
```

### Structured Output
```typescript
const response = await agent.generate('Extract: John, 30', {
  structuredOutput: {
    schema: z.object({
      name: z.string(),
      age: z.number()
    })
  }
})
console.log(response.object) // Access via .object property
```

### Streaming
```typescript
const stream = await agent.stream('Tell a story')
for await (const chunk of stream.fullStream) {
  console.log(chunk)
}
```

---

## Workflow Patterns

### Sequential Steps
```typescript
const workflow = createWorkflow({
  id: 'sequential',
  inputSchema: z.object({ data: z.string() }),
  outputSchema: z.object({ result: z.string() })
})
  .then(step1)
  .then(step2)
  .then(step3)
  .commit();
```

### Branching (Conditional)
```typescript
const workflow = createWorkflow({
  id: 'branching',
  inputSchema: z.object({ value: z.number() }),
  outputSchema: z.object({ result: z.string() })
})
  .branch([
    // [condition, workflow/step to execute]
    [async ({ inputData }) => inputData.value > 10, pathA],
    [async ({ inputData }) => inputData.value <= 10, pathB],
  ])
  .commit();
```

### Parallel Execution
```typescript
const workflow = createWorkflow({
  id: 'parallel',
  inputSchema: z.object({ items: z.array(z.string()) }),
  outputSchema: z.object({ results: z.array(z.any()) })
})
  .parallel([step1, step2, step3]) // All execute concurrently
  .commit();
```

### Foreach Loop
```typescript
const workflow = createWorkflow({
  id: 'foreach',
  inputSchema: z.object({ items: z.array(z.string()) }),
  outputSchema: z.object({ results: z.array(z.string()) })
})
  .foreach(processItemStep) // Iterates over input array
  .commit();
```

### Suspend/Resume (Human-in-the-loop)
```typescript
const approvalTool = createTool({
  id: 'approval',
  inputSchema: z.object({ request: z.string() }),
  outputSchema: z.object({ approved: z.boolean() }),
  suspendSchema: z.object({ requestId: z.string() }),
  resumeSchema: z.object({ approved: z.boolean() }),
  execute: async (input, context) => {
    if (!context.resumeData) {
      // First call - suspend execution
      context.suspend({ requestId: 'req-123' });
      return;
    }
    // Resumed - use resumeData
    return { approved: context.resumeData.approved };
  }
});

// Resume later
await run.resume({ resumeData: { approved: true } });
```

### Workflow State Management
```typescript
const workflow = createWorkflow({
  id: 'stateful',
  inputSchema: z.object({ data: z.string() }),
  outputSchema: z.object({ result: z.string() }),
  stateSchema: z.object({ counter: z.number() })
})
  .then(createStep({
    id: 'increment',
    execute: async ({ state, setState }) => {
      await setState({ counter: (state.counter || 0) + 1 });
      return { result: 'incremented' };
    }
  }))
  .commit();

// Execute with initial state
const run = await workflow.createRun();
const result = await run.start({
  inputData: { data: 'test' },
  initialState: { counter: 0 }
});
```

---

## Agent Patterns

### Agent with Tools
```typescript
// 1. Create tools
const weatherTool = createTool({
  id: 'get-weather',
  description: 'Get weather for a location',
  inputSchema: z.object({ location: z.string() }),
  outputSchema: z.object({ temp: z.number(), condition: z.string() }),
  execute: async ({ location }) => {
    // TODO: Fetch weather
    return { temp: 72, condition: 'sunny' };
  }
});

// 2. Create agent with tools
const agent = new Agent({
  id: 'weather-agent',
  name: 'Weather Assistant',
  instructions: 'You help users with weather information',
  model: 'openai/gpt-4o',
  tools: { weatherTool } // Assign tools
});
```

### Agent with Memory
```typescript
// 1. Configure storage
const storage = new PostgresStore({
  connectionString: process.env.DATABASE_URL
});
await storage.init();

// 2. Create memory
const memory = new Memory({
  id: 'chat-memory',
  storage,
  options: {
    lastMessages: 10 // Retrieve last 10 messages
  }
});

// 3. Create agent with memory
const agent = new Agent({
  id: 'chat-agent',
  instructions: 'You are a helpful assistant',
  model: 'openai/gpt-4o',
  memory
});

// 4. Use with consistent threadId
await agent.generate('Hello', {
  threadId: 'user-123-conversation',
  resourceId: 'user-123'
});
```

### Agent with Memory + Tools
```typescript
const agent = new Agent({
  id: 'full-agent',
  instructions: 'You are a helpful assistant with tools',
  model: 'openai/gpt-4o',
  tools: { weatherTool, searchTool },
  memory // Memory from previous example
});

await agent.generate('What\'s the weather in SF?', {
  threadId: 'user-123',
  resourceId: 'user-123'
});
```

### Agent with Semantic Recall
```typescript
// Requires vector store and embedder
const memory = new Memory({
  id: 'semantic-memory',
  storage: postgresStore,
  vector: chromaVectorStore, // Vector store for semantic search
  embedder: openaiEmbedder,  // Embedding model
  options: {
    lastMessages: 5,
    semanticRecall: true // Enable semantic search
  }
});

const agent = new Agent({
  id: 'semantic-agent',
  memory
});
```

### Agent with Structured Output
```typescript
const response = await agent.generate(
  'Extract user info: John Smith, age 30, lives in SF',
  {
    structuredOutput: {
      schema: z.object({
        name: z.string(),
        age: z.number(),
        location: z.string()
      })
    }
  }
);

console.log(response.object); // { name: 'John Smith', age: 30, location: 'SF' }
```

---

## Memory Patterns

### Basic Message History
```typescript
const memory = new Memory({
  id: 'basic-memory',
  storage: postgresStore,
  options: {
    lastMessages: 10 // Retrieve last 10 messages
  }
});
```

### Working Memory (Persistent State)
```typescript
const memory = new Memory({
  id: 'working-memory',
  storage: postgresStore,
  options: {
    lastMessages: 10,
    workingMemory: {
      enabled: true,
      scope: 'resource', // 'resource' or 'thread'
      template: `User preferences: {preferences}`
    }
  }
});
```

### Semantic Recall (Vector Search)
```typescript
const memory = new Memory({
  id: 'semantic-memory',
  storage: postgresStore,
  vector: chromaVectorStore, // REQUIRED
  embedder: openaiEmbedder,  // REQUIRED
  options: {
    lastMessages: 5,
    semanticRecall: true // REQUIRED
  }
});
```

---

## Tool Patterns

### Basic Tool
```typescript
const calculatorTool = createTool({
  id: 'calculator',
  description: 'Perform basic math operations',
  inputSchema: z.object({
    operation: z.enum(['add', 'subtract', 'multiply', 'divide']),
    a: z.number(),
    b: z.number()
  }),
  outputSchema: z.object({ result: z.number() }),
  execute: async ({ operation, a, b }) => {
    switch (operation) {
      case 'add': return { result: a + b };
      case 'subtract': return { result: a - b };
      case 'multiply': return { result: a * b };
      case 'divide': return { result: a / b };
    }
  }
});
```

### Tool with Context Access
```typescript
const toolWithContext = createTool({
  id: 'context-aware',
  inputSchema: z.object({ query: z.string() }),
  outputSchema: z.object({ result: z.string() }),
  execute: async (input, context) => {
    // Access mastra instance
    const agent = context.mastra.getAgent('other-agent');

    // Access memory
    const messages = await context.memory?.listMessages();

    // Access request context
    const userId = context.requestContext?.get('userId');

    return { result: 'done' };
  }
});
```

### Suspending Tool (Human-in-the-loop)
```typescript
const approvalTool = createTool({
  id: 'approval',
  inputSchema: z.object({ action: z.string() }),
  outputSchema: z.object({ approved: z.boolean() }),
  suspendSchema: z.object({ actionId: z.string() }),
  resumeSchema: z.object({ approved: z.boolean() }),
  execute: async (input, context) => {
    if (!context.agent?.resumeData) {
      // Suspend and wait for approval
      const actionId = generateId();
      context.agent.suspend({ actionId });
      return;
    }

    // Resumed with approval decision
    return { approved: context.agent.resumeData.approved };
  }
});
```

---

## Storage Patterns

### Postgres Storage
```typescript
import { PostgresStore } from '@mastra/pg';

const storage = new PostgresStore({
  connectionString: process.env.DATABASE_URL
});
await storage.init(); // Creates tables

const mastra = new Mastra({
  storage
});
```

### LibSQL Storage (SQLite-compatible)
```typescript
import { LibSQLStore } from '@mastra/libsql';

const storage = new LibSQLStore({
  id: 'my-db',
  url: 'file:./local.db' // or libsql://...
});
await storage.init();
```

### Agent-Specific Storage
```typescript
const mastra = new Mastra({
  storage: postgresStore, // Default storage
  agents: {
    chatAgent: new Agent({
      id: 'chat-agent',
      memory: new Memory({
        id: 'chat-memory',
        storage: libsqlStore // Different storage for this agent
      })
    })
  }
});
```

---

## RAG Patterns

### Vector Query Tool (Recommended)
```typescript
import { createVectorQueryTool } from '@mastra/rag';

// 1. Create vector query tool
const searchTool = createVectorQueryTool({
  vectorStoreName: 'my-vector-store',
  indexName: 'documents',
  vector: chromaVectorStore,
  embedder: openaiEmbedder,
  topK: 5
});

// 2. Use with agent
const agent = new Agent({
  id: 'rag-agent',
  instructions: 'You help users find information in our docs',
  tools: { searchTool }
});

// Agent can now query documents via the tool
await agent.generate('What is in the documentation about authentication?');
```

### Graph RAG (Advanced)
```typescript
import { GraphRAG } from '@mastra/rag';

// Create graph RAG with embedding dimension and similarity threshold
const graphRag = new GraphRAG(1536, 0.7); // OpenAI embedding dimension

// Add nodes with embeddings
graphRag.addNode({
  id: 'doc1',
  content: 'Document content about authentication',
  embedding: await embedder.embed('Document content...')
});

// Add relationships between documents
graphRag.addEdge({ source: 'doc1', target: 'doc2', weight: 0.8 });

// Query the graph
const nodes = graphRag.getNodes();
const edges = graphRag.getEdges();
```

---

## Key Conventions

1. Use `mastra.getAgent('name')` / `mastra.getWorkflow('name')` not direct imports
2. Always use env vars for API keys
3. ES2022 modules required (not CommonJS)
4. Test with Studio: `npm run dev` → http://localhost:4111

---

## Common Errors

### "Cannot find module" or "ES Module" errors
- **Cause**: CommonJS config
- **Fix**: Set `"target": "ES2022"`, `"module": "ES2022"` in tsconfig.json

### "Property X does not exist on type Y"
- **Cause**: Outdated API usage or incorrect type
- **Fix**: Use `mastra-embedded-docs-look-up` skill to check current API

### Agent not using assigned tools
- **Cause**: Tools not registered in Mastra instance or agent config
- **Fix**: Add tools to `new Mastra({ tools: { ... } })` and reference in agent

### Memory not persisting across conversations
- **Cause**: Missing storage configuration or threadId
- **Fix**: Configure storage backend and pass consistent `threadId` to agent.generate()

**See [references/common-errors.md](references/common-errors.md) for comprehensive troubleshooting.**

---

---

## Documentation Resources

**For API signatures and detailed types**:
- Use `mastra-embedded-docs-look-up` skill
- Check `node_modules/@mastra/core/dist/docs/`

**For project initialization**:
- Use `create-mastra` skill

**For detailed patterns**:
- See reference files in `references/patterns/` directory

---

## Resources

- [Docs](https://mastra.ai/docs)
- [Agents](https://mastra.ai/docs/agents/overview)
- [Workflows](https://mastra.ai/docs/workflows/overview)
- [Upgrade to v1 Guide](https://mastra.ai/guides/migrations/upgrade-to-v1/overview)
