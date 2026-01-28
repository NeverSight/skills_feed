---
name: new-project-scaffolding
description: Scaffold a new Nx monorepo project with backend, frontend, shared types library, justfile commands, and direnv setup. Use when starting a fresh project or asked to "create a new project", "scaffold a monorepo", or "set up a new workspace".
---

# New Project Scaffolding

This skill guides you through scaffolding a new Nx monorepo with a standard structure including backend API, frontend web app, shared types library, and essential tooling (Just, direnv).

## Project Structure Overview

```
{project-name}/
├── apps/
│   ├── backend/          # Node.js/Koa backend API
│   └── webapp/           # React frontend application
├── libs/
│   └── types/            # Shared TypeScript types (@{project}/types)
├── scripts/              # Utility TypeScript scripts (run with vite-node)
├── .envrc                # direnv configuration
├── .env.example          # Environment variable template
├── .env.local            # Local environment variables (gitignored)
├── justfile              # Task runner commands
├── nx.json               # Nx configuration
├── tsconfig.base.json    # Base TypeScript configuration
└── package.json          # Root package.json
```

## Scaffolding Steps

### Step 1: Create Nx Workspace

```bash
npx create-nx-workspace@latest {project-name} \
  --preset=ts \
  --packageManager=npm \
  --nxCloud=skip \
  --interactive=false
```

This creates a minimal TypeScript workspace. The `--preset=ts` gives us a clean slate to add exactly what we need.

### Step 2: Install Required Nx Plugins

```bash
cd {project-name}
npm install -D @nx/node @nx/react @nx/webpack @nx/jest @nx/eslint
```

### Step 3: Generate Backend Application

```bash
npx nx generate @nx/node:application \
  --name=backend \
  --directory=apps/backend \
  --framework=express \
  --projectNameAndRootFormat=as-provided \
  --e2eTestRunner=none \
  --unitTestRunner=jest
```

### Step 4: Generate Frontend Application

```bash
npx nx generate @nx/react:application \
  --name=webapp \
  --directory=apps/webapp \
  --projectNameAndRootFormat=as-provided \
  --bundler=webpack \
  --style=css \
  --routing=true \
  --e2eTestRunner=none \
  --unitTestRunner=jest
```

### Step 5: Generate Shared Types Library

```bash
npx nx generate @nx/js:library \
  --name=types \
  --directory=libs/types \
  --projectNameAndRootFormat=as-provided \
  --unitTestRunner=jest \
  --bundler=tsc \
  --strict
```

After generation, update `libs/types/package.json`:

```json
{
  "name": "@{project}/types",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    "./package.json": "./package.json",
    ".": {
      "types": "./src/index.ts",
      "import": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "dependencies": {
    "tslib": "^2.3.0"
  }
}
```

### Step 6: Configure TypeScript Path Aliases

Update `tsconfig.base.json` to include the types library path:

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "importHelpers": true,
    "isolatedModules": true,
    "lib": ["es2022"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "noEmitOnError": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "skipLibCheck": true,
    "strict": true,
    "target": "es2022",
    "baseUrl": ".",
    "paths": {
      "@{project}/types": ["libs/types/src/index.ts"]
    }
  }
}
```

### Step 7: Create Scripts Directory

```bash
mkdir -p scripts
```

Create `scripts/example-script.ts` as a template:

```typescript
/**
 * Example utility script
 * Run with: npx vite-node scripts/example-script.ts
 */

const run = async () => {
  console.log('Script executed successfully');
  process.exit(0);
};

run().catch((error) => {
  console.error('Error:', error);
  process.exit(1);
});
```

Install vite-node for running scripts:

```bash
npm install -D vite-node
```

### Step 8: Create justfile

Create `justfile` in the project root:

```just
# {Project Name} - Just Command Runner
# Run `just --list` to see all available commands

# Default recipe to display help
default:
  @just --list

# === Development ===

# Serve backend
serve-backend:
  echo "Starting backend..."
  npx nx serve backend

# Serve webapp
serve-webapp:
  echo "Starting webapp..."
  npx nx serve webapp

# Serve all projects in parallel (backend + webapp)
serve-all:
  echo "Starting all projects..."
  npx nx run-many --targets=serve --projects=backend,webapp --parallel=2

# Serve with debugger
serve-all-debug:
  echo "Starting all projects with debugger..."
  NODE_OPTIONS='--inspect' npx nx run-many --targets=serve --projects=backend,webapp --parallel=2

# === Building ===

# Build a specific project
build project:
  echo "Building {{project}}..."
  npx nx build {{project}}

# Build all projects
build-all:
  echo "Building all projects..."
  npx nx run-many --targets=build --all

# === Testing ===

# Run unit tests for a project
test project:
  echo "Running tests for {{project}}..."
  npx nx test {{project}}

# Run all tests
test-all:
  echo "Running all tests..."
  npx nx run-many --targets=test --all

# === Linting ===

# Lint a specific project
lint project:
  echo "Linting {{project}}..."
  npx nx lint {{project}} --fix

# Lint all projects
lint-all:
  echo "Linting all projects..."
  npx nx run-many --targets=lint --all --fix

# === Utilities ===

# Clean NX cache
clean:
  echo "Cleaning NX cache..."
  npx nx reset

# Show project details
show project:
  npx nx show project {{project}}

# View dependency graph
graph:
  npx nx graph

# Install dependencies
install:
  npm install

# Generate a new library
gen-lib name:
  npx nx generate @nx/js:library --name={{name}} --directory=libs/{{name}} --projectNameAndRootFormat=as-provided --unitTestRunner=jest --bundler=tsc --strict

# Run a TypeScript script
run-script script:
  npx vite-node scripts/{{script}}.ts
```

### Step 9: Set Up Environment Variables

Create `.env.example`:

```bash
# Database
MONGODB_URI=mongodb://localhost:27017/{project-name}

# Server
PORT=3005
NODE_ENV=development

# Frontend
VITE_API_URL=http://localhost:3005

# Add your environment variables here
```

Create `.envrc`:

```bash
# Use direnv to auto load environment variables upon entering this project directory
set -o allexport; source .env.local; set +o allexport
```

Copy to local:

```bash
cp .env.example .env.local
```

### Step 10: Update .gitignore

Add these entries to `.gitignore`:

```
# Environment
.env.local
.env*.local

# Nx
.nx/cache
dist/

# Dependencies
node_modules/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build outputs
*.tsbuildinfo
```

### Step 11: Configure nx.json

Update `nx.json` with recommended settings:

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "plugins": [
    {
      "plugin": "@nx/js/typescript",
      "options": {
        "typecheck": {
          "targetName": "typecheck"
        },
        "build": {
          "targetName": "build",
          "configName": "tsconfig.lib.json",
          "buildDepsName": "build-deps",
          "watchDepsName": "watch-deps"
        }
      }
    },
    {
      "plugin": "@nx/webpack/plugin",
      "options": {
        "buildTargetName": "build",
        "serveTargetName": "serve",
        "previewTargetName": "preview",
        "buildDepsTargetName": "build-deps",
        "watchDepsTargetName": "watch-deps",
        "serveStaticTargetName": "serve-static"
      }
    },
    {
      "plugin": "@nx/eslint/plugin",
      "options": {
        "targetName": "lint"
      }
    },
    {
      "plugin": "@nx/jest/plugin",
      "options": {
        "targetName": "test"
      }
    }
  ],
  "targetDefaults": {
    "test": {
      "dependsOn": ["^build"]
    }
  },
  "generators": {
    "@nx/react": {
      "application": {
        "babel": true,
        "style": "css",
        "linter": "eslint",
        "bundler": "webpack"
      },
      "component": {
        "style": "css"
      },
      "library": {
        "style": "css",
        "linter": "eslint"
      }
    }
  },
  "tui": {
    "enabled": false
  }
}
```

## Post-Scaffolding Checklist

After scaffolding, verify:

1. **Install dependencies**: `npm install`
2. **Allow direnv**: `direnv allow`
3. **Test backend**: `just serve-backend`
4. **Test frontend**: `just serve-webapp`
5. **Test both**: `just serve-all`
6. **View dependency graph**: `just graph`

## Using Shared Types

In the backend, import types:

```typescript
import { MyType } from '@{project}/types';
```

In the frontend, import types:

```typescript
import type { MyType } from '@{project}/types';
```

## Adding New Libraries

```bash
# Generate a new shared library
just gen-lib my-utils

# Or manually
npx nx generate @nx/js:library \
  --name=my-utils \
  --directory=libs/my-utils \
  --projectNameAndRootFormat=as-provided \
  --unitTestRunner=jest \
  --bundler=tsc \
  --strict
```

Then add the path alias to `tsconfig.base.json`:

```json
{
  "paths": {
    "@{project}/types": ["libs/types/src/index.ts"],
    "@{project}/my-utils": ["libs/my-utils/src/index.ts"]
  }
}
```

## Troubleshooting

### NX Cache Issues
```bash
just clean
# or
npx nx reset
rm -rf .nx/cache
```

### Port Already in Use
```bash
lsof -i :3005
kill -9 <PID>
```

### direnv Not Loading
```bash
direnv allow
direnv status
```

### TypeScript Path Not Resolving
Ensure:
1. Path is in `tsconfig.base.json`
2. Restart your IDE/editor
3. Run `npx nx reset` to clear cache
