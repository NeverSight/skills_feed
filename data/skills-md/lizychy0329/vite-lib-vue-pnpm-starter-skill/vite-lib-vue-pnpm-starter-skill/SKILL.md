---
name: vite-lib-vue-pnpm-starter-skill
description: Create a minimal Vite Vue 3 library starter with pnpm workspace, direct file generation. Use when developers need to bootstrap a Vue 3 component library with TypeScript support using pnpm as the package manager.
---

# Vite Lib Vue 3 PNPM Starter Skill

This skill creates a minimal Vite + Vue 3 library project template using pnpm workspace for dependency management. It directly generates all necessary files without using Vite's official initialization commands.

## Core Features

- Directly generate all configuration files without manual intervention
- pnpm workspace for monorepo structure management
- Vue 3 + TypeScript support
- Minimal configuration approach
- pnpm package manager only

## Usage Workflow

### 1. Create Project Directory Structure

```bash
mkdir -p src/components
mkdir -p playground/src
mkdir -p playground/public
```

### 2. Generate Configuration Files

Generate the following essential files:

- Root `package.json` with workspace configuration and build scripts
- `pnpm-workspace.yaml` for monorepo setup
- `vite.config.ts` with library build configuration
- TypeScript configuration files (`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`)
- Library entry files (`index.ts`, `src/index.ts`, `src/components/index.ts`)
- Example component (`src/components/Counter.vue`)
- Playground files (`playground/package.json`, `playground/vite.config.ts`, `playground/index.html`, etc.)
- `.gitignore` file

### 3. Install Dependencies

```bash
pnpm install
```

### 4. Validate Setup

#### Build Validation

```bash
pnpm build
```

**Expected Result:**

- Successful build with no errors
- Generated `dist/` directory
- Files: `index.es.js`, `index.umd.js`, `index.d.ts`

#### Development Validation

```bash
cd playground && pnpm dev
```

**Expected Result:**

- Development server starts successfully
- No compilation errors
- No TypeScript errors
- Accessible development page

## Project Structure

```
project-root/
├── .gitignore
├── index.ts
├── package.json
├── pnpm-workspace.yaml
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
├── src/
│   ├── index.ts
│   ├── components/
│   │   ├── index.ts
│   │   └── Counter.vue
│   └── style.css
├── playground/
│   ├── .gitignore
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── public/
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── style.css
│       └── assets/
└── dist/ (generated after build)
```

## Key Implementation Details

### Library Configuration

- Set `vue` as external dependency in `vite.config.ts`
- Use `vite-plugin-dts` for TypeScript declaration generation
- Configure proper exports in `package.json` for different module systems

### TypeScript Setup

- Use TypeScript Project References for better compilation performance
- Strict TypeScript settings for improved code quality

### Playground Setup

- Reference main library via `workspace:*` for local development
- Separate configuration for isolated testing environment

## When to Use This Skill

- Creating a new Vue 3 component library
- Using Vite as the build tool
- Preferring pnpm for package management
- Needing a playground for local testing
- Requiring TypeScript type declarations

## Important Notes

- **pnpm Only:** Project is configured exclusively for pnpm
- **Minimal Configuration:** Keep settings lean and focused
- **Direct File Generation:** No Vite official commands used
- **Workspace Dependency:** Playground uses `workspace:*` for latest code
- **Type Checking:** `vue-tsc -b` runs before build
- **External Vue:** Vue is not bundled into the library
- **TypeScript References:** For optimal compilation

## Troubleshooting

### Q: Why pnpm instead of npm?

A: Faster installation, stricter dependency management, and better monorepo support.

### Q: Why separate package.json for playground?

A: Isolated environment with its own dependencies, referencing main library via workspace.

### Q: Why externalize Vue in build?

A: Avoids duplicate bundling and version conflicts, follows library best practices.

### Q: Why use TypeScript References?

A: Enables independent compilation of subprojects for faster builds and more accurate type checking.
