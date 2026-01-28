---
name: turborepo
description: Turborepo monorepo management. Use when working with workspaces, build pipelines, caching, or monorepo-wide operations.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(pnpm:*), Bash(turbo:*)
---

# Turborepo Monorepo Guide

## Project Structure

```
projectx/
├── apps/                   # Applications
│   ├── auth/              # NestJS auth service
│   ├── order/             # NestJS order service
│   ├── product/           # NestJS product service
│   ├── storybook/         # Component documentation
│   └── web/               # React Router frontend
├── packages/              # Shared packages
│   ├── core/              # @projectx/core - NestJS shared modules
│   ├── db/                # @projectx/db - Prisma client
│   ├── email/             # @projectx/email - Email templates
│   ├── models/            # @projectx/models - TypeScript types
│   ├── payment/           # @projectx/payment - Stripe
│   ├── ui/                # @projectx/ui - React components
│   └── workflows/         # @projectx/workflows - Temporal
├── turbo.json             # Turborepo config
├── pnpm-workspace.yaml    # Workspace definition
└── package.json           # Root package
```

## Turbo Configuration

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "test/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    }
  }
}
```

## Common Commands

### Development

```bash
# Run all apps in development
pnpm dev

# Run specific app
pnpm dev:web
pnpm dev:auth
pnpm dev:order
pnpm dev:product

# Run Storybook
pnpm storybook
```

### Building

```bash
# Build all packages and apps
pnpm build

# Build specific targets
pnpm build:web
pnpm build:ui
pnpm build:auth

# Build with turbo filter
turbo run build --filter=web
turbo run build --filter=@projectx/ui
```

### Testing

```bash
# Run all tests
pnpm test

# Test specific package
pnpm --filter web test
pnpm --filter @projectx/ui test
```

### Filtering

```bash
# Build a package and its dependencies
turbo run build --filter=web...

# Build dependents of a package
turbo run build --filter=...@projectx/ui

# Build everything except one package
turbo run build --filter=!storybook

# Build changed packages since main
turbo run build --filter=[main]
```

## Package Dependencies

### Internal Package References

In `package.json`:

```json
{
  "dependencies": {
    "@projectx/ui": "workspace:*",
    "@projectx/db": "workspace:*",
    "@projectx/models": "workspace:*"
  }
}
```

### Creating a New Package

1. Create directory:
```bash
mkdir -p packages/new-package/src
```

2. Initialize package.json:
```json
{
  "name": "@projectx/new-package",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm --dts",
    "dev": "tsup src/index.ts --format esm --dts --watch"
  }
}
```

3. Add to workspace consumer:
```json
{
  "dependencies": {
    "@projectx/new-package": "workspace:*"
  }
}
```

### Creating a New App

1. Create directory:
```bash
mkdir -p apps/new-app/src
```

2. Initialize with NestJS or React Router template

3. Add to turbo.json if needed for custom pipelines

## Caching

### Local Caching

Turbo caches build outputs locally in `node_modules/.cache/turbo`.

```bash
# Clear local cache
turbo run build --force

# View cache status
turbo run build --dry-run
```

### Remote Caching (Optional)

```bash
# Login to Vercel for remote caching
turbo login

# Link to project
turbo link
```

## Task Graph

View the task dependency graph:

```bash
turbo run build --graph
```

## Environment Variables

### Global Environment

```json
// turbo.json
{
  "globalEnv": ["DATABASE_URL", "STRIPE_SECRET_KEY"],
  "globalDependencies": [".env"]
}
```

### Task-Specific Environment

```json
{
  "tasks": {
    "build": {
      "env": ["NODE_ENV"]
    }
  }
}
```

## Best Practices

1. **Use workspace protocol** - Always use `workspace:*` for internal deps
2. **Keep packages focused** - Each package should have a single responsibility
3. **Minimize dependencies** - Don't create unnecessary inter-package dependencies
4. **Use turbo filters** - Run commands only where needed
5. **Cache outputs** - Configure outputs correctly in turbo.json
6. **Share configs** - Use shared tsconfig, eslint configs
7. **Consistent naming** - Use `@projectx/` scope for all packages

## Troubleshooting

### Dependency Issues

```bash
# Clean and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Build Order Issues

```bash
# See what turbo will build
turbo run build --dry-run

# Force rebuild without cache
turbo run build --force
```

### Type Issues

```bash
# Regenerate TypeScript build info
pnpm build:core
pnpm build:ui
pnpm build
```
