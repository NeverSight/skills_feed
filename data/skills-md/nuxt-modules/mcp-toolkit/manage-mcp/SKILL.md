---
name: manage-mcp
description: Manage MCP servers in Nuxt - setup, create, customize with middleware, review, and troubleshoot
---

# Manage MCP

Complete skill for managing Model Context Protocol (MCP) servers in Nuxt applications. Setup, create, customize with middleware and handlers, review, and troubleshoot.

## When to Use

- **Setup**: "Setup an MCP server in my Nuxt app"
- **Create**: "Create a tool to calculate BMI" / "Add a resource to read the README"
- **Customize**: "Add authentication to my MCP server" / "Create middleware for rate limiting"
- **Review**: "Review my MCP implementation" / "Check for best practices"
- **Troubleshoot**: "My auto-imports aren't working" / "Cannot connect to endpoint"
- **Test**: "Create tests for my MCP tools"

---

## Setup MCP Server

### Installation

**Automatic (recommended):**
```bash
npx nuxt module add mcp-toolkit
```

**Manual:**
```bash
pnpm add -D @nuxtjs/mcp-toolkit zod
```

Add to `nuxt.config.ts`:
```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/mcp-toolkit'],
  mcp: {
    name: 'My MCP Server',
  },
})
```

### Directory Structure

```
server/mcp/
├── tools/       # Actions AI can perform
├── resources/   # Data AI can read
└── prompts/     # Message templates
```

### Verification

1. Start: `pnpm dev`
2. Check: `http://localhost:3000/mcp` (should redirect)
3. Open DevTools (Shift+Alt+D) → MCP tab

---

## Create Tools

Tools are functions AI assistants can call.

### Basic Structure

```typescript
import { z } from 'zod'

export default defineMcpTool({
  description: 'What the tool does',
  inputSchema: {
    param: z.string().describe('Parameter description'),
  },
  handler: async ({ param }) => {
    return {
      content: [{
        type: 'text',
        text: 'Result',
      }],
    }
  },
})
```

### Input Patterns

```typescript
// Required
name: z.string().describe('User name')

// Optional with default
limit: z.number().default(10).describe('Max results')

// Enum
format: z.enum(['json', 'xml']).describe('Format')

// Array
tags: z.array(z.string()).describe('Tags')
```

### Error Handling

```typescript
if (!param) {
  return {
    content: [{ type: 'text', text: 'Error: param required' }],
    isError: true,
  }
}
```

### Caching

```typescript
export default defineMcpTool({
  cache: '5m',  // 5 minutes
  // ...
})
```

See [detailed examples →](./references/tools.md)

---

## Create Resources

Resources expose read-only data.

### File Resource

```typescript
import { readFile } from 'node:fs/promises'

export default defineMcpResource({
  description: 'Read a file',
  uri: 'file:///README.md',
  mimeType: 'text/markdown',
  handler: async (uri: URL) => {
    const content = await readFile('README.md', 'utf-8')
    return {
      contents: [{
        uri: uri.toString(),
        text: content,
        mimeType: 'text/markdown',
      }],
    }
  },
})
```

### API Resource

```typescript
export default defineMcpResource({
  description: 'Fetch API data',
  uri: 'api:///users',
  mimeType: 'application/json',
  cache: '5m',
  handler: async (uri: URL) => {
    const data = await $fetch('https://api.example.com/users')
    return {
      contents: [{
        uri: uri.toString(),
        text: JSON.stringify(data, null, 2),
        mimeType: 'application/json',
      }],
    }
  },
})
```

### Dynamic Resource

```typescript
import { z } from 'zod'

export default defineMcpResource({
  description: 'Fetch by ID',
  uriTemplate: {
    uriTemplate: 'user:///{id}',
    arguments: {
      id: z.string().describe('User ID'),
    },
  },
  handler: async (uri: URL, args) => {
    const user = await fetchUser(args.id)
    return {
      contents: [{
        uri: uri.toString(),
        text: JSON.stringify(user),
        mimeType: 'application/json',
      }],
    }
  },
})
```

See [detailed examples →](./references/resources.md)

---

## Create Prompts

Prompts are reusable message templates.

### Static Prompt

```typescript
export default defineMcpPrompt({
  description: 'Code review',
  handler: async () => {
    return {
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: 'Review this code for best practices.',
        },
      }],
    }
  },
})
```

### Dynamic Prompt

```typescript
import { z } from 'zod'

export default defineMcpPrompt({
  description: 'Custom review',
  inputSchema: {
    language: z.string().describe('Language'),
    focus: z.array(z.string()).describe('Focus areas'),
  },
  handler: async ({ language, focus }) => {
    return {
      messages: [{
        role: 'user',
        content: {
          type: 'text',
          text: `Review my ${language} code: ${focus.join(', ')}`,
        },
      }],
    }
  },
})
```

See [detailed examples →](./references/prompts.md)

---

## Middleware & Handlers

Customize MCP behavior with middleware and handlers for authentication, logging, rate limiting, and more.

### Basic Middleware

```typescript
// server/mcp/middleware.ts
export default defineMcpMiddleware({
  handler: async (event, next) => {
    console.log('MCP Request:', event.path)

    // Check auth
    const token = event.headers.get('authorization')
    if (!token) {
      return createError({ statusCode: 401, message: 'Unauthorized' })
    }

    return next()
  },
})
```

### Custom Handler

```typescript
// server/mcp/handlers/custom.ts
export default defineMcpHandler({
  name: 'custom-mcp',
  route: '/mcp/custom',
  handler: async (event) => {
    return {
      tools: await loadCustomTools(),
      resources: [],
      prompts: [],
    }
  },
})
```

### Common Use Cases

- **Authentication**: API keys, JWT tokens
- **Rate limiting**: Per IP or per user
- **Logging**: Request/response tracking
- **CORS**: Cross-origin configuration
- **Multiple endpoints**: Public/admin separation

See [detailed middleware guide →](./references/middleware.md)

---

## Review & Best Practices

### Tool Checklist

✅ Use kebab-case filenames
✅ Add `.describe()` to all Zod fields
✅ Return `isError: true` for errors
✅ Add caching for expensive ops
✅ Clear, actionable descriptions
✅ Validate all inputs

❌ Generic descriptions
❌ Skip error handling
❌ Expose sensitive data
❌ No input validation

### Resource Checklist

✅ Descriptive URIs (`config:///app`)
✅ Set appropriate MIME types
✅ Enable caching when needed
✅ Handle errors gracefully
✅ Use URI templates for collections

❌ Unclear URI schemes
❌ Skip MIME types
❌ Expose sensitive data
❌ Return huge datasets without pagination

### Prompt Checklist

✅ Clear descriptions
✅ Meaningful parameters
✅ Default values where appropriate
✅ Single, focused purpose
✅ Reusable design

❌ Overly complex
❌ Skip descriptions
❌ Mix multiple concerns

---

## Troubleshooting

### Auto-imports Not Working

**Fix:**
1. Check `modules: ['@nuxtjs/mcp-toolkit']` in config
2. Restart dev server
3. Files in `server/mcp/` directory?
4. Run `pnpm nuxt prepare`

### Endpoint Not Accessible

**Fix:**
1. Dev server running?
2. Test: `curl http://localhost:3000/mcp`
3. Check `enabled: true` in config
4. Review server logs

### Validation Errors

**Fix:**
- Required fields provided?
- Types match schema?
- Use `.optional()` for optional fields
- Enum values exact match?

### Tool Not Discovered

**Fix:**
- File extension `.ts` or `.js`?
- Using `export default`?
- File in correct directory?
- Restart dev server

See [detailed troubleshooting →](./references/troubleshooting.md)

---

## Testing with Evals

### Setup

```bash
pnpm add -D evalite vitest @ai-sdk/mcp ai
```

Add to `package.json`:
```json
{
  "scripts": {
    "eval": "evalite",
    "eval:ui": "evalite watch"
  }
}
```

### Basic Test

Create `test/mcp.eval.ts`:
```typescript
import { experimental_createMCPClient as createMCPClient } from '@ai-sdk/mcp'
import { generateText } from 'ai'
import { evalite } from 'evalite'
import { toolCallAccuracy } from 'evalite/scorers'

evalite('MCP Tool Selection', {
  data: async () => [
    {
      input: 'Calculate BMI for 70kg 1.75m',
      expected: [{
        toolName: 'bmi-calculator',
        input: { weight: 70, height: 1.75 },
      }],
    },
  ],
  task: async (input) => {
    const mcp = await createMCPClient({
      transport: { type: 'http', url: 'http://localhost:3000/mcp' },
    })
    try {
      const result = await generateText({
        model: 'openai/gpt-4o',
        prompt: input,
        tools: await mcp.tools(),
      })
      return result.toolCalls ?? []
    }
    finally {
      await mcp.close()
    }
  },
  scorers: [
    ({ output, expected }) => toolCallAccuracy({
      actualCalls: output,
      expectedCalls: expected,
    }),
  ],
})
```

### Running

```bash
# Start server
pnpm dev

# Run tests (in another terminal)
pnpm eval

# Or with UI
pnpm eval:ui  # http://localhost:3006
```

See [detailed testing guide →](./references/testing.md)

---

## Quick Reference

### Common Commands

```bash
# Setup
npx nuxt module add mcp-toolkit

# Dev
pnpm dev

# Test endpoint
curl http://localhost:3000/mcp

# Regenerate types
pnpm nuxt prepare

# Run evals
pnpm eval
```

### Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  mcp: {
    name: 'My Server',
    route: '/mcp',
    enabled: true,
    dir: 'mcp',
  },
})
```

### Debug Tools

- **DevTools**: Shift+Alt+D → MCP tab
- **Logs**: Check terminal
- **curl**: Test endpoint

## Learn More

- [Documentation](https://mcp-toolkit.nuxt.dev/)
- [Tools Guide](https://mcp-toolkit.nuxt.dev/core-concepts/tools)
- [Resources Guide](https://mcp-toolkit.nuxt.dev/core-concepts/resources)
- [Prompts Guide](https://mcp-toolkit.nuxt.dev/core-concepts/prompts)
- [MCP Protocol](https://modelcontextprotocol.io/)
