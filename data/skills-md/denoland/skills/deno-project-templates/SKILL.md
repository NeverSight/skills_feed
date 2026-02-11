---
name: deno-project-templates
description: Use when scaffolding new Deno projects. Provides templates for Fresh web apps, CLI tools, libraries, and API servers with modern best practices.
license: MIT
metadata:
  author: denoland
  version: "1.2"
---

# Deno Project Templates

This skill provides templates for creating new Deno projects with modern best practices.

## When to Use This Skill

- Creating a new Deno project from scratch
- Setting up project structure for different application types
- Scaffolding Fresh web apps, CLI tools, libraries, or API servers

## Scope Boundaries

This skill applies **only** when the user asks for a Deno project. Follow these rules:

- If the user asks for a **Node.js, Python, Go, Rust, or other non-Deno project**, answer using that technology's project setup directly. Do not suggest Deno templates.
- Only use these templates when the user explicitly asks for a Deno project or is working in a Deno environment.
- When mentioning deprecated patterns, describe them generically. Do not write out deprecated URLs or import syntax — only show the correct modern approach.

## Project Types

Choose the appropriate template based on what you want to build:

| Type | Use Case | Key Files |
|------|----------|-----------|
| **Fresh web app** | Full-stack web application with Fresh framework | `main.ts`, `routes/`, `islands/` |
| **CLI tool** | Command-line application | `main.ts` with arg parsing |
| **Library** | Reusable package to publish on JSR | `mod.ts`, `mod_test.ts` |
| **API server** | Backend API without frontend | `main.ts` with HTTP handlers |

## Fresh Web App

For full-stack web applications, use the Fresh initializer:

```bash
deno run -Ar jsr:@fresh/init my-project
cd my-project
```

This creates:
- `deno.json` - Project configuration and dependencies
- `main.ts` - Server entry point
- `client.ts` - Client entry point (CSS imports)
- `vite.config.ts` - Vite build configuration
- `routes/` - Pages and API routes (file-based routing)
- `islands/` - Interactive components that get JavaScript on the client
- `components/` - Server-only components (no JavaScript shipped)
- `static/` - Static assets like images, CSS

**Development:** Fresh uses Vite. The dev server runs at `http://localhost:5173` (not port 8000).

```bash
deno task dev
```

## CLI Tool

Create a command-line application with argument parsing.

**Template files:** See `assets/cli-tool/` directory.

### deno.json

```json
{
  "name": "my-cli",
  "version": "0.1.0",
  "exports": "./main.ts",
  "tasks": {
    "dev": "deno run --allow-all main.ts",
    "compile": "deno compile --allow-all -o my-cli main.ts"
  },
  "imports": {
    "@std/cli": "jsr:@std/cli@^1",
    "@std/fmt": "jsr:@std/fmt@^1"
  }
}
```

### main.ts

```typescript
import { parseArgs } from "@std/cli/parse-args";
import { bold, green } from "@std/fmt/colors";

const args = parseArgs(Deno.args, {
  boolean: ["help", "version"],
  alias: { h: "help", v: "version" },
});

if (args.help) {
  console.log(`
${bold("my-cli")} - A Deno CLI tool

${bold("USAGE:")}
  my-cli [OPTIONS]

${bold("OPTIONS:")}
  -h, --help     Show this help message
  -v, --version  Show version
`);
  Deno.exit(0);
}

if (args.version) {
  console.log("my-cli v0.1.0");
  Deno.exit(0);
}

console.log(green("Hello from my-cli"));
```

## Library

Create a reusable package for publishing to JSR.

**Template files:** See `assets/library/` directory.

### deno.json

```json
{
  "name": "@username/my-library",
  "version": "0.1.0",
  "exports": "./mod.ts",
  "tasks": {
    "test": "deno test",
    "check": "deno check mod.ts",
    "publish": "deno publish"
  }
}
```

### mod.ts

```typescript
/**
 * my-library - A Deno library
 *
 * @module
 */

/**
 * Example function - replace with your library's functionality
 *
 * @param name The name to greet
 * @returns A greeting message
 *
 * @example
 * ```ts
 * import { greet } from "@username/my-library";
 * console.log(greet("World")); // "Hello, World"
 * ```
 */
export function greet(name: string): string {
  return `Hello, ${name}`;
}
```

### mod_test.ts

```typescript
import { assertEquals } from "jsr:@std/assert";
import { greet } from "./mod.ts";

Deno.test("greet returns correct message", () => {
  assertEquals(greet("World"), "Hello, World");
});
```

**Remember:** Replace `@username` with your JSR username before publishing.

## API Server

Create a backend API without a frontend.

**Template files:** See `assets/api-server/` directory.

### deno.json

```json
{
  "tasks": {
    "dev": "deno run --watch --allow-net main.ts",
    "start": "deno run --allow-net main.ts"
  },
  "imports": {
    "@std/http": "jsr:@std/http@^1"
  }
}
```

### main.ts

```typescript
import { serve } from "@std/http";

const handler = (request: Request): Response => {
  const url = new URL(request.url);

  if (url.pathname === "/") {
    return new Response("Welcome to the API", {
      headers: { "Content-Type": "text/plain" },
    });
  }

  if (url.pathname === "/api/hello") {
    return Response.json({ message: "Hello from Deno" });
  }

  return new Response("Not Found", { status: 404 });
};

console.log("Server running at http://localhost:8000");
serve(handler, { port: 8000 });
```

## Post-Setup Steps

After creating project files:

```bash
cd my-project
deno install          # Install dependencies
deno fmt              # Format the code
deno lint             # Check for issues
```

## Development Commands by Project Type

| Project Type | Start Development | Build/Compile |
|--------------|-------------------|---------------|
| Fresh | `deno task dev` (port 5173) | `deno task build` |
| CLI | `deno task dev` | `deno task compile` |
| Library | `deno test` | N/A |
| API | `deno task dev` | N/A |

## Deployment

When ready to deploy:
- Fresh: `deno task build && deno deploy --prod`
- CLI: `deno task compile` (creates standalone binary)
- Library: `deno publish` (publishes to JSR)
- API: `deno deploy --prod`

## Best Practices

- Always use `jsr:` imports for Deno packages (the old URL-based imports are deprecated)
- Run `deno fmt` and `deno lint` regularly
- Projects are configured for Deno Deploy compatibility
