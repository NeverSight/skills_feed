---
name: mcp-development
description: Complete MCP development toolkit for creating, debugging, testing, and reviewing MCP servers. Use when setting up new MCP projects, creating tools, debugging connection issues, reviewing MCP code, or generating documentation.
---

# MCP Development Toolkit

Complete toolkit for MCP server development including project setup, tool creation, debugging, and code review.

## Project Setup

### Directory Structure
```
mcp-project/
├── src/
│   ├── index.ts          # Server entry point
│   ├── tools/            # Tool definitions
│   │   └── index.ts
│   ├── db/               # Database connections
│   │   └── connection.ts
│   └── utils/
│       └── index.ts
├── build/                # Compiled output
├── .env.example
├── package.json
├── tsconfig.json
└── README.md
```

### package.json
```json
{
  "name": "mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "build/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js",
    "dev": "tsc --watch",
    "inspector": "npx @modelcontextprotocol/inspector"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "build",
    "rootDir": "src",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
```

For detailed setup guide, see [SETUP.md](SETUP.md).

## Creating Tools

For tool creation templates and patterns, see [TOOLS.md](TOOLS.md).

## Debugging

For common issues and debugging techniques, see [DEBUG.md](DEBUG.md).

## Code Review

For review checklists, see [REVIEW.md](REVIEW.md).

## Quick Commands

```bash
# Initialize project
npm init -y && npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node && npx tsc --init

# Build and run
npm run build && node build/index.js

# Test with inspector
npx @modelcontextprotocol/inspector
```
