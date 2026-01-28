---
name: testing-cicd-init
description: Add Vitest testing infrastructure and GitHub Actions CI/CD to any TypeScript project. Supports Next.js, NestJS, and React projects with 80% coverage thresholds. Use this skill when setting up tests for a new project or adding CI/CD pipelines.
---

# Testing & CI/CD Initialization

Automatically sets up comprehensive test infrastructure for TypeScript projects including Vitest, coverage thresholds, and GitHub Actions CI/CD.

## When to Use

This skill should be used when:

- Adding tests to a project without test coverage
- Setting up GitHub Actions CI/CD for the first time
- Configuring Vitest with coverage thresholds
- Initializing testing infrastructure for a new project
- Migrating from Jest to Vitest

## What It Does

1. **Detects project type** (Next.js, NestJS, React, Node.js)
2. **Adds Vitest configuration** with appropriate settings
3. **Creates test setup files** for the environment
4. **Adds GitHub Actions workflow** for CI/CD
5. **Configures 80% coverage thresholds**
6. **Adds test scripts** to package.json
7. **Installs required dependencies**

## Project Type Detection

The skill detects project type by scanning:

- `package.json` dependencies (next, @nestjs/core, react, etc.)
- Config files (next.config.*, nest-cli.json, etc.)
- Directory structure (app/, src/, pages/, etc.)

## Quick Start

Ask Claude to:

```
Add testing and CI/CD to this project
```

Or be specific:

```
Set up Vitest with 80% coverage and GitHub Actions for this Next.js project
```

## Configuration by Project Type

### Next.js Projects

**Dependencies installed:**

```bash
bun add -D vitest @vitest/coverage-v8 @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom
```

**Files created:**

- `vitest.config.ts` - Vitest with jsdom environment
- `src/test/setup.ts` - Test setup with RTL matchers
- `.github/workflows/ci.yml` - CI pipeline

**Test pattern:** `**/*.{test,spec}.{ts,tsx}`

### NestJS Projects

**Dependencies installed:**

```bash
bun add -D vitest @vitest/coverage-v8 supertest @types/supertest
```

**Files created:**

- `vitest.config.ts` - Vitest with node environment
- `test/setup.ts` - Test setup for NestJS
- `.github/workflows/ci.yml` - CI with MongoDB service

**Test pattern:** `src/**/*.spec.ts`

### React/Node.js Projects

Follows similar patterns based on detected framework.

## Coverage Configuration

Default thresholds (configurable):

- Lines: 80%
- Functions: 80%
- Branches: 75%
- Statements: 80%

Coverage is enforced:

1. In pre-commit hooks (via Husky)
2. In CI/CD pipeline (GitHub Actions)

## GitHub Actions Features

The generated CI workflow includes:

- Bun setup with caching
- Dependency installation
- Lint/format checking (Biome)
- TypeScript type checking
- Test execution with coverage
- Build verification
- MongoDB service (for NestJS projects)

## Templates

Templates are located in the `templates/` directory:

| Template | Purpose |
|----------|---------|
| `vitest.config.nextjs.ts` | Vitest config for Next.js |
| `vitest.config.nestjs.ts` | Vitest config for NestJS |
| `ci-nextjs.yml` | GitHub Actions for Next.js |
| `ci-nestjs.yml` | GitHub Actions for NestJS |
| `test-setup-react.ts` | Test setup with RTL |
| `test-setup-node.ts` | Test setup for Node.js |

## Monorepo Support

For monorepos (detected by workspaces in package.json):

1. Creates `vitest.workspace.ts` at root
2. Creates individual `vitest.config.ts` per package
3. Creates root-level GitHub Actions workflow
4. Uses `bun --filter '*' test` for orchestration

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `husky-test-coverage` | Adds pre-commit coverage enforcement |
| `linter-formatter-init` | Works alongside for code quality |
| `playwright-e2e-init` | Adds E2E testing after unit tests |
| `testing-expert` | Provides testing patterns guidance |

## Example Usage

### Adding tests to a Next.js project

```
User: Add testing to this project

Claude:
1. Detects Next.js from package.json
2. Installs vitest, @vitest/coverage-v8, @testing-library/react
3. Creates vitest.config.ts with jsdom environment
4. Creates src/test/setup.ts
5. Creates .github/workflows/ci.yml
6. Adds test scripts to package.json
```

### Adding tests to a NestJS API

```
User: Set up tests for this NestJS API

Claude:
1. Detects NestJS from @nestjs/core dependency
2. Installs vitest, @vitest/coverage-v8, supertest
3. Creates vitest.config.ts with node environment
4. Creates test/setup.ts
5. Creates .github/workflows/ci.yml with MongoDB service
6. Adds test scripts to package.json
```

## Troubleshooting

### Tests not finding modules

Ensure path aliases in `vitest.config.ts` match `tsconfig.json`:

```typescript
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
  },
},
```

### Coverage below threshold

1. Check coverage report: `bun test --coverage`
2. Identify uncovered lines
3. Add tests or adjust thresholds temporarily

### CI failing on type errors

Ensure `bunx tsc --noEmit` passes locally before pushing.

## Best Practices

1. **Start with unit tests** for utilities and services
2. **Add integration tests** for API endpoints
3. **Use E2E tests sparingly** for critical flows
4. **Run tests before commits** via Husky
5. **Monitor coverage trends** in CI

---

**When this skill is active**, Claude will:

1. Detect the project type automatically
2. Install appropriate testing dependencies
3. Create properly configured test files
4. Set up GitHub Actions CI/CD
5. Configure coverage thresholds
6. Add test scripts to package.json
