---
name: create-voltagent
# prettier-ignore
description: Skill for creating AI agent projects using the VoltAgent framework. Guide for CLI setup and manual bootstrapping.
license: MIT
metadata:
  author: VoltAgent
  version: "1.0.0"
  repository: https://github.com/VoltAgent/skills
---

# Create VoltAgent Skill

Complete guide for creating new VoltAgent projects. Includes the CLI flow and a full manual setup.

Official documentation: https://voltagent.dev/docs/

---

## Start Here

When a user wants to create a VoltAgent project, ask:

"How would you like to create your VoltAgent project?"

1. Automatic Setup - run `npm create voltagent-app@latest` and handle prompts
2. Interactive Guide - walk through each step and confirm choices
3. Manual Installation - set up dependencies and a full working example

Based on their choice:
- Option 1: run the CLI, capture server and provider choices, and finish setup
- Option 2: gather server, provider, and API key, then run the CLI
- Option 3: follow the manual steps below

---

## Before You Start

- Node.js 20+ (>= 20.19.0 recommended)
- Git (optional, for auto git init)
- An API key for your model provider (not needed for Ollama)

---

## Fast Path

Create a new VoltAgent project with one command:

```bash
npm create voltagent-app@latest
```

Other package managers:

```bash
pnpm create voltagent-app@latest
yarn create voltagent-app@latest
bun create voltagent-app@latest
```

---

## CLI Flow

The create-voltagent-app command:
1. Asks for a project name (default: `my-voltagent-app`)
2. Prompts for a server framework (Hono or Elysia)
3. Prompts for an AI provider (OpenAI, Anthropic, Google, Groq, Mistral, Ollama)
4. Prompts for an API key when required
5. Installs dependencies and scaffolds the project
6. Writes `.env`, `README.md`, `tsconfig.json`, `tsdown.config.ts`, and Docker files
7. Initializes a git repo when available

---

## CLI Walkthrough

1. Run:
   ```bash
   npm create voltagent-app@latest
   ```

2. When prompted:
   - Choose a server (Hono recommended or Elysia)
   - Choose an AI provider
   - Enter your API key (skip if using Ollama)

3. Start the dev server:
   ```bash
   cd <your-project-directory>
   npm run dev
   ```

4. If you chose Ollama:
   ```bash
   ollama pull llama3.2
   ```

---

## CLI Flags and Examples

Create in a specific directory:

```bash
npm create voltagent-app@latest my-voltagent-app
```

Download an example from the VoltAgent repo:

```bash
npm create voltagent-app@latest -- --example with-workflow
```

pnpm / yarn / bun equivalents:

```bash
pnpm create voltagent-app@latest -- --example with-workflow
yarn create voltagent-app@latest -- --example with-workflow
bun create voltagent-app@latest -- --example with-workflow
```

Notes:
- Examples are pulled from https://github.com/voltagent/voltagent/tree/main/examples
- Some package managers require `--` before `--example`.
- After an example download, run `npm install` and `npm run dev`.

---

## Generated Layout

```
my-voltagent-app/
|-- src/
|   |-- index.ts
|   |-- tools/
|   |   |-- index.ts
|   |   `-- weather.ts
|   `-- workflows/
|       `-- index.ts
|-- .env
|-- .voltagent/
|-- Dockerfile
|-- .dockerignore
|-- .gitignore
|-- README.md
|-- package.json
|-- tsconfig.json
`-- tsdown.config.ts
```

If you run the docs sync script in this repo, you may also see `packages/core/docs` generated.

---

## Env Keys

The CLI writes `.env` with your provider key (or a placeholder). Common keys:

```env
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_GENERATIVE_AI_API_KEY=...
GROQ_API_KEY=...
MISTRAL_API_KEY=...
OLLAMA_HOST=http://localhost:11434

VOLTAGENT_PUBLIC_KEY=...
VOLTAGENT_SECRET_KEY=...
```

---

## Manual Setup (Full)

If you prefer not to use the CLI, follow these steps:

### Step 1: Create the project directory

```bash
mkdir my-voltagent-app && cd my-voltagent-app
npm init -y
mkdir -p src/tools src/workflows .voltagent
```

### Step 2: Install dependencies

Choose one server package:

```bash
npm install @voltagent/core @voltagent/libsql @voltagent/logger @voltagent/server-hono @voltagent/cli ai zod dotenv
```

or

```bash
npm install @voltagent/core @voltagent/libsql @voltagent/logger @voltagent/server-elysia @voltagent/cli ai zod dotenv
```

Dev dependencies:

```bash
npm install -D typescript tsx tsdown @types/node @biomejs/biome
```

### Step 3: Add scripts to package.json

```json
{
  "scripts": {
    "dev": "tsx watch --env-file=.env ./src",
    "build": "tsdown",
    "start": "node dist/index.js",
    "lint": "biome check ./src",
    "lint:fix": "biome check --write ./src",
    "typecheck": "tsc --noEmit",
    "volt": "volt"
  }
}
```

`volt` is the VoltAgent CLI. Use it for project utilities (for example `init`, `deploy`, `eval`, `prompts`, `tunnel`, `update`).

### Step 4: Configure TypeScript

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "outDir": "dist",
    "skipLibCheck": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Step 5: Add tsdown config

Create `tsdown.config.ts`:

```typescript
import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["./src/index.ts"],
  sourcemap: true,
  outDir: "dist",
});
```

### Step 6: Create .env

```env
OPENAI_API_KEY=your-api-key-here
VOLTAGENT_PUBLIC_KEY=your-public-key
VOLTAGENT_SECRET_KEY=your-secret-key
NODE_ENV=development
```

For Ollama:

```env
OLLAMA_HOST=http://localhost:11434
```

### Step 7: Create a tool

Create `src/tools/weather.ts`:

```typescript
import { createTool } from "@voltagent/core";
import { z } from "zod";

export const weatherTool = createTool({
  name: "getWeather",
  description: "Get the current weather for a specific location",
  parameters: z.object({
    location: z.string().describe("City or location to get weather for"),
  }),
  execute: async ({ location }) => {
    return {
      weather: {
        location,
        temperature: 21,
        condition: "Sunny",
        humidity: 45,
        windSpeed: 8,
      },
      message: `Current weather in ${location}: 21 C and sunny.`,
    };
  },
});
```

Create `src/tools/index.ts`:

```typescript
export { weatherTool } from "./weather";
```

### Step 8: Create a workflow

Create `src/workflows/index.ts`:

```typescript
import { createWorkflowChain } from "@voltagent/core";
import { z } from "zod";

export const expenseApprovalWorkflow = createWorkflowChain({
  id: "expense-approval",
  name: "Expense Approval Workflow",
  purpose: "Process expense reports with manager approval for high amounts",
  input: z.object({
    employeeId: z.string(),
    amount: z.number(),
    category: z.string(),
    description: z.string(),
  }),
  result: z.object({
    status: z.enum(["approved", "rejected"]),
    approvedBy: z.string(),
    finalAmount: z.number(),
  }),
})
  .andThen({
    id: "check-approval-needed",
    resumeSchema: z.object({
      approved: z.boolean(),
      managerId: z.string(),
      comments: z.string().optional(),
      adjustedAmount: z.number().optional(),
    }),
    execute: async ({ data, suspend, resumeData }) => {
      if (resumeData) {
        return {
          ...data,
          approved: resumeData.approved,
          approvedBy: resumeData.managerId,
          finalAmount: resumeData.adjustedAmount || data.amount,
          managerComments: resumeData.comments,
        };
      }

      if (data.amount > 500) {
        await suspend("Manager approval required", {
          employeeId: data.employeeId,
          requestedAmount: data.amount,
          category: data.category,
        });
      }

      return {
        ...data,
        approved: true,
        approvedBy: "system",
        finalAmount: data.amount,
      };
    },
  })
  .andThen({
    id: "process-decision",
    execute: async ({ data }) => {
      return {
        status: data.approved ? "approved" : "rejected",
        approvedBy: data.approvedBy,
        finalAmount: data.finalAmount,
      };
    },
  });
```

### Step 9: Create the entry point

Create `src/index.ts`:

```typescript
import "dotenv/config";
import {
  Agent,
  Memory,
  VoltAgent,
  VoltAgentObservability,
  VoltOpsClient,
} from "@voltagent/core";
import { LibSQLMemoryAdapter, LibSQLObservabilityAdapter } from "@voltagent/libsql";
import { createPinoLogger } from "@voltagent/logger";
import { honoServer } from "@voltagent/server-hono";
import { expenseApprovalWorkflow } from "./workflows";
import { weatherTool } from "./tools";

const logger = createPinoLogger({ name: "my-voltagent-app", level: "info" });

const memory = new Memory({
  storage: new LibSQLMemoryAdapter({
    url: "file:./.voltagent/memory.db",
    logger: logger.child({ component: "libsql" }),
  }),
});

const observability = new VoltAgentObservability({
  storage: new LibSQLObservabilityAdapter({
    url: "file:./.voltagent/observability.db",
  }),
});

const agent = new Agent({
  name: "my-voltagent-app",
  instructions: "A helpful assistant that can check weather and help with various tasks",
  model: "openai/gpt-4o-mini",
  tools: [weatherTool],
  memory,
});

new VoltAgent({
  agents: { agent },
  workflows: { expenseApprovalWorkflow },
  server: honoServer(),
  logger,
  observability,
  voltOpsClient: new VoltOpsClient({
    publicKey: process.env.VOLTAGENT_PUBLIC_KEY || "",
    secretKey: process.env.VOLTAGENT_SECRET_KEY || "",
  }),
});
```

Model format is `provider/model`. Examples:
- `openai/gpt-4o-mini`
- `anthropic/claude-3-5-sonnet`
- `google/gemini-2.0-flash`
- `groq/llama-3.3-70b-versatile`
- `mistral/mistral-large-latest`
- `ollama/llama3.2`

If you chose Elysia, replace `honoServer` with `elysiaServer` and update the import.

### Step 10: Run the dev server

```bash
npm run dev
```
