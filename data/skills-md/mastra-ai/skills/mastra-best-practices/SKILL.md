---
name: mastra-best-practices
description: Quick reference for Mastra conventions. When to use agents vs workflows, required TypeScript config, project structure, and common code patterns.
license: Apache-2.0
metadata:
  author: Mastra
  version: "1.0.0"
  repository: https://github.com/mastra-ai/skills
---

# Mastra Best Practices

Quick reference for Mastra conventions. **See [mastra.ai/docs](https://mastra.ai/docs) for details.**

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

## Key Conventions

1. Use `mastra.getAgent('name')` / `mastra.getWorkflow('name')` not direct imports
2. Always use env vars for API keys
3. ES2022 modules required (not CommonJS)
4. Test with Studio: `npm run dev` → http://localhost:4111

---

## Resources

- [Docs](https://mastra.ai/docs)
- [Agents](https://mastra.ai/docs/agents/overview)
- [Workflows](https://mastra.ai/docs/workflows/overview)
