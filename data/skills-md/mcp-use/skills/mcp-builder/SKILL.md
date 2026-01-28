---
name: mcp-builder
description: Build Model Context Protocol (MCP) servers with mcp-use framework. Use when creating MCP servers, defining tools/resources/prompts, working with mcp-use, bootstrapping MCP projects, deploying MCP servers, or when user mentions MCP development, MCP tools, MCP resources, or MCP prompts.
---

# MCP Server Builder

Build production-ready MCP servers with the mcp-use framework. This Skill provides quick-start instructions and best practices for creating MCP servers.

## Quick Start

**Always bootstrap with `npx create-mcp-use-app`:**

```bash
npx create-mcp-use-app my-mcp-server
cd my-mcp-server
```

**Choose template based on needs:**
- `--template starter` - Basic MCP server with simple tools and resources
- `--template apps-sdk` - MCP server with OpenAI Apps SDK widgets (recommended for interactive UIs)
- `--template mcp-ui` - MCP server with MCP-UI framework support

```bash
npx create-mcp-use-app my-server --template apps-sdk
cd my-server
yarn install
```

## Defining Tools

Tools are executable functions that AI models can call:

```typescript
import { MCPServer, text, object } from "mcp-use/server";
import { z } from "zod";

const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  description: "My MCP server"
});

// Simple tool
server.tool(
  {
    name: "greet-user",
    description: "Greet a user by name",
    schema: z.object({
      name: z.string().describe("The user's name"),
      formal: z.boolean().optional().describe("Use formal greeting")
    })
  },
  async ({ name, formal }) => {
    const greeting = formal ? `Good day, ${name}` : `Hey ${name}!`;
    return text(greeting);
  }
);
```

**Key points:**
- Use Zod for schema validation
- Add `.describe()` to all parameters
- Return appropriate response types (text, object, widget)

## Defining Resources

Resources expose data that clients can read:

```typescript
import { object, text, markdown } from "mcp-use/server";

// Static resource
server.resource(
  {
    uri: "config://settings",
    name: "Application Settings",
    description: "Current configuration",
    mimeType: "application/json"
  },
  async () => {
    return object({
      theme: "dark",
      version: "1.0.0"
    });
  }
);

// Dynamic resource
server.resource(
  {
    uri: "stats://current",
    name: "Current Stats",
    description: "Real-time statistics",
    mimeType: "application/json"
  },
  async () => {
    const stats = await getStats();
    return object(stats);
  }
);

// Markdown resource
server.resource(
  {
    uri: "docs://guide",
    name: "User Guide",
    description: "Documentation",
    mimeType: "text/markdown"
  },
  async () => {
    return markdown("# Guide\n\nWelcome!");
  }
);
```

**Response helpers available:**
- `text(string)` - Plain text
- `object(data)` - JSON objects
- `markdown(string)` - Markdown content
- `html(string)` - HTML content
- `image(buffer, mimeType)` - Binary images

## Defining Prompts

Prompts are reusable templates for AI interactions:

```typescript
server.prompt(
  {
    name: "code-review",
    description: "Generate a code review template",
    schema: z.object({
      language: z.string().describe("Programming language"),
      focusArea: z.string().optional().describe("Specific focus area")
    })
  },
  async ({ language, focusArea }) => {
    const focus = focusArea ? ` with focus on ${focusArea}` : "";
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please review this ${language} code${focus}.`
          }
        }
      ]
    };
  }
);
```

## Testing Locally

**Development mode (hot reload):**
```bash
yarn dev
```

**Production mode:**
```bash
yarn build
yarn start
```

**Inspector UI:**
Access at `http://localhost:3000/inspector` to test tools, view resources, and try prompts.

**Tunneling (test with ChatGPT before deploying):**

Option 1 - Auto-tunnel:
```bash
mcp-use start --port 3000 --tunnel
```

Option 2 - Separate tunnel:
```bash
yarn start  # Terminal 1
npx @mcp-use/tunnel 3000  # Terminal 2
```

You'll get a public URL like `https://happy-cat.local.mcp-use.run/mcp`

**Tunnel details:**
- Expires after 24 hours
- Closes after 1 hour of inactivity
- Rate limit: 10 creations/hour, max 5 active per IP

Learn more: https://mcp-use.com/docs/tunneling

## Deployment

**Deploy to mcp-use Cloud (recommended):**

```bash
# Login first (if not already)
npx mcp-use login

# Deploy
yarn deploy
```

**If authentication error:**
```bash
npx mcp-use login
yarn deploy
```

**After deployment:**
- Public URL provided (e.g., `https://your-server.mcp-use.com/mcp`)
- Auto-scaled and monitored
- HTTPS enabled
- Zero-downtime deployments

## Best Practices

**Tool Design:**
- ✅ One tool = one focused capability
- ✅ Descriptive names and descriptions
- ✅ Use `.describe()` on all Zod fields
- ✅ Handle errors gracefully
- ✅ Return helpful error messages

**Resource Design:**
- ✅ Use clear URI schemes (config://, docs://, stats://)
- ✅ Choose appropriate MIME types
- ✅ Use response helpers for cleaner code
- ✅ Make resources dynamic when needed

**Prompt Design:**
- ✅ Keep prompts reusable
- ✅ Use system messages for context
- ✅ Parameterize with Zod schemas
- ✅ Include clear instructions

**Testing:**
- ✅ Test with Inspector UI first
- ✅ Use tunneling to test with real clients before deploying
- ✅ Verify all tools, resources, and prompts work as expected

**Deployment:**
- ✅ Test locally and with tunneling first
- ✅ Run `npx mcp-use login` if deploy fails
- ✅ Version your server semantically
- ✅ Document breaking changes

## Widget Support (Apps SDK Template)

If using apps-sdk template, widgets auto-register:

```typescript
// resources/weather-widget.tsx
export const widgetMetadata = {
  description: "Display weather information",
  schema: z.object({
    city: z.string(),
    temperature: z.number()
  })
};

export default function WeatherWidget({ city, temperature }) {
  return (
    <div>
      <h2>{city}</h2>
      <p>{temperature}°C</p>
    </div>
  );
}
```

Widget automatically becomes available as tool and resource!

## Project Structure

```
my-mcp-server/
├── resources/           # React widgets (apps-sdk)
│   └── widget.tsx
├── public/             # Static assets
├── index.ts            # Server entry point
├── package.json
├── tsconfig.json
└── README.md
```

## Common Patterns

**Tool with widget:**
```typescript
server.tool(
  {
    name: "show-data",
    description: "Display data with visualization",
    schema: z.object({
      query: z.string()
    }),
    widget: {
      name: "data-display",
      invoking: "Loading...",
      invoked: "Data loaded"
    }
  },
  async ({ query }) => {
    const data = await fetchData(query);
    return widget({
      props: { data },
      output: text(`Found ${data.length} results`)
    });
  }
);
```

**Resource template (parameterized):**
```typescript
server.resourceTemplate(
  {
    uriTemplate: "user://{userId}/profile",
    name: "User Profile",
    description: "Get user by ID",
    mimeType: "application/json"
  },
  async ({ userId }) => {
    const user = await fetchUser(userId);
    return object(user);
  }
);
```

**Error handling:**
```typescript
server.tool(
  {
    name: "divide",
    schema: z.object({
      a: z.number(),
      b: z.number()
    })
  },
  async ({ a, b }) => {
    if (b === 0) {
      return text("Error: Cannot divide by zero");
    }
    return text(`Result: ${a / b}`);
  }
);
```

## Detailed Examples

For comprehensive examples and advanced patterns, connect to the **mcp-use MCP server** which provides:
- Complete example resources for all primitives
- Full working server examples
- Detailed documentation
- Interactive widgets showcase

## Learn More

- **Documentation**: https://docs.mcp-use.com
- **Examples**: https://github.com/mcp-use/mcp-use/tree/main/examples
- **Tunneling Guide**: https://mcp-use.com/docs/tunneling
- **Discord**: https://mcp-use.com/discord
- **GitHub**: https://github.com/mcp-use/mcp-use

## Quick Reference

**Commands:**
- `npx create-mcp-use-app my-server` - Bootstrap
- `yarn dev` - Development mode
- `yarn build` - Build for production
- `yarn start` - Run production server
- `mcp-use start --tunnel` - Start with tunnel
- `npx mcp-use login` - Authenticate
- `yarn deploy` - Deploy to cloud

**Response helpers:**
- `text(str)`, `object(data)`, `markdown(str)`, `html(str)`, `image(buf, mime)`

**Server methods:**
- `server.tool()` - Define executable tool
- `server.resource()` - Define static/dynamic resource
- `server.resourceTemplate()` - Define parameterized resource
- `server.prompt()` - Define prompt template
- `server.listen()` - Start server
