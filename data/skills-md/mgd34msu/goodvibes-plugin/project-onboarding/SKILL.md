---
name: project-onboarding
description: "Load PROACTIVELY when starting work on an unfamiliar codebase or setting up a new project. Use when user says \"help me understand this codebase\", \"onboard me\", \"what does this project do\", \"set up my environment\", or \"map the architecture\". Covers codebase structure analysis, architecture mapping, dependency auditing, convention and pattern detection, developer environment setup, and documentation of findings for rapid productive contribution."
metadata:
  version: 1.0.0
  category: quality
  tags: [onboarding, architecture, dependencies, conventions, environment, documentation]
---

## Resources
```
scripts/
  validate-onboarding.sh
references/
  onboarding-patterns.md
```

# Project Onboarding Quality Skill

This skill teaches you how to systematically onboard onto new projects using GoodVibes precision tools. A thorough onboarding process maps the architecture, identifies patterns, validates the environment, and generates documentation for rapid productive contribution.

## When to Use This Skill

Load this skill when:
- Joining a new project or team
- Understanding an unfamiliar codebase
- Documenting project architecture
- Setting up developer environments
- Creating onboarding guides
- Auditing project health and technical debt

Trigger phrases: "onboard to this project", "understand this codebase", "setup dev environment", "map the architecture", "generate project docs".

## Core Workflow

### Phase 1: Project Structure Analysis

Understand the directory layout, monorepo configuration, and entry points.

#### Step 1.1: Discover Directory Structure

Use `discover` to map the project's directory layout and identify key configuration files.

```yaml
discover:
  queries:
    - id: config_files
      type: glob
      patterns: 
        - "package.json"
        - "tsconfig*.json"
        - "*.config.{js,ts,mjs,cjs}"
        - ".env*"
        - "docker-compose*.yml"
        - "Dockerfile*"
    - id: src_structure
      type: glob
      patterns:
        - "src/**/*"
        - "app/**/*"
        - "pages/**/*"
        - "lib/**/*"
    - id: monorepo_indicators
      type: glob
      patterns:
        - "pnpm-workspace.yaml"
        - "lerna.json"
        - "nx.json"
        - "turbo.json"
        - "packages/*/package.json"
        - "apps/*/package.json"
  verbosity: files_only
```

**What this reveals:**
- Project type (monorepo vs single package)
- Framework/build tool (Next.js, Vite, Create React App, etc.)
- Configuration complexity
- Docker setup for containerized development

#### Step 1.2: Identify Entry Points

Find main application entry points, server files, and public APIs.

```yaml
discover:
  queries:
    - id: entry_points
      type: glob
      patterns:
        - "src/index.{ts,tsx,js,jsx}"
        - "src/main.{ts,tsx,js,jsx}"
        - "src/app.{ts,tsx,js,jsx}"
        - "app/layout.{ts,tsx,js,jsx}"
        - "pages/_app.{ts,tsx,js,jsx}"
        - "server.{ts,js}"
    - id: api_routes
      type: glob
      patterns:
        - "src/api/**/*"
        - "app/api/**/*"
        - "pages/api/**/*"
        - "routes/**/*"
    - id: public_assets
      type: glob
      patterns:
        - "public/**/*"
        - "static/**/*"
  verbosity: files_only
```

**What this reveals:**
- Application architecture (SPA, SSR, API-only, full-stack)
- Routing patterns
- Static asset organization

#### Step 1.3: Read Core Configuration

Use `precision_read` to examine package.json and key config files.

```yaml
precision_read:
  files:
    - path: "package.json"
      extract: content
    - path: "tsconfig.json"
      extract: content
  verbosity: standard
```

**What this reveals:**
- Dependencies and dev dependencies
- Scripts for build, dev, test, lint
- Node version requirements (engines field)
- Package manager (npm, yarn, pnpm)

### Phase 2: Dependency Audit

Analyze dependencies for version currency, security vulnerabilities, and bundle size.

#### Step 2.1: List All Dependencies

Extract dependencies from package.json files.

```yaml
precision_grep:
  queries:
    - id: dependencies
      pattern: '"dependencies":\s*\{[\s\S]*?\}'
      glob: "**/package.json"
      multiline: true
    - id: dev_dependencies
      pattern: '"devDependencies":\s*\{[\s\S]*?\}'
      glob: "**/package.json"
      multiline: true
    - id: peer_dependencies
      pattern: '"peerDependencies":\s*\{[\s\S]*?\}'
      glob: "**/package.json"
      multiline: true
  output:
    format: matches
  verbosity: standard
```

#### Step 2.2: Check for Outdated Dependencies

Run npm/yarn/pnpm commands to check for updates.

```yaml
precision_exec:
  commands:
    - cmd: "npm outdated --json"
    - cmd: "npm audit --json"
  verbosity: standard
```

**What this reveals:**
- Packages with available updates
- Security vulnerabilities
- Severity levels (critical, high, moderate, low)

#### Step 2.3: Analyze Bundle Size and Tree

Identify large dependencies and potential optimizations.

```yaml
precision_exec:
  commands:
    - cmd: "npx bundle-phobia-cli --json react react-dom next"
  verbosity: minimal
```

**What this reveals:**
- Download size and install size
- Gzipped size for production
- Heavy dependencies to watch

### Phase 3: Architecture Mapping

Map module boundaries, data flow, and API surface.

#### Step 3.1: Extract Module Structure

Use `precision_read` with outline extraction to map the codebase structure.

```yaml
# Note: path "src" works as a directory - precision_read will recursively extract outline
precision_read:
  files:
    - path: "src"
      extract: outline
  output:
    max_per_item: 100
  verbosity: standard
```

**What this reveals:**
- Directory organization patterns
- Module boundaries
- Code volume per module

#### Step 3.2: Identify Key Symbols

Use `precision_read` with symbol extraction to find exported functions, classes, and types.

```yaml
# First discover the files
discover:
  queries:
    - id: lib_files
      type: glob
      patterns: ["src/lib/**/*.{ts,tsx}"]
    - id: api_files
      type: glob
      patterns: ["src/api/**/*.{ts,tsx}"]
  verbosity: files_only

# Then read symbols from discovered files
precision_read:
  files:
    # Use file paths from discover results
    - path: "src/lib/index.ts"  # Example - use actual discovered paths
      extract: symbols
    - path: "src/api/index.ts"  # Example - use actual discovered paths
      extract: symbols
  symbol_filter: ["function", "class", "interface", "type"]
  verbosity: minimal
```

**What this reveals:**
- Public API surface
- Core abstractions and utilities
- Type definitions

#### Step 3.3: Map Data Flow

Trace imports and exports to understand module dependencies.

```yaml
discover:
  queries:
    - id: imports
      type: grep
      pattern: '^import .* from ["''].*["''];?$'
      glob: "src/**/*.{ts,tsx,js,jsx}"
    - id: exports
      type: grep
      pattern: '^export (default|const|function|class|interface|type|enum)'
      glob: "src/**/*.{ts,tsx,js,jsx}"
  verbosity: count_only
```

**What this reveals:**
- Module coupling
- Import patterns (barrel files, direct imports)
- Potential circular dependencies

### Phase 4: Convention Detection

Identify code style, naming patterns, and file organization rules.

#### Step 4.1: Detect Naming Conventions

Search for naming patterns in files and symbols.

```yaml
discover:
  queries:
    - id: component_naming
      type: grep
      pattern: 'export (default )?(function|const) [A-Z][a-zA-Z]*'
      glob: "src/components/**/*.{ts,tsx}"
    - id: hook_naming
      type: grep
      pattern: 'export (default )?(function|const) use[A-Z][a-zA-Z]*'
      glob: "src/**/*.{ts,tsx}"
    - id: util_naming
      type: grep
      pattern: 'export (default )?(function|const) [a-z][a-zA-Z]*'
      glob: "src/lib/**/*.{ts,tsx}"
  verbosity: count_only
```

**What this reveals:**
- PascalCase for components
- camelCase for utilities
- `use` prefix for hooks
- File naming patterns

#### Step 4.2: Detect File Organization Patterns

Analyze directory structure for organizational conventions.

```yaml
discover:
  queries:
    - id: index_files
      type: glob
      patterns: ["**/index.{ts,tsx,js,jsx}"]
    - id: type_files
      type: glob
      patterns: ["**/*.types.{ts,tsx}", "**/types.{ts,tsx}", "**/types/**/*"]
    - id: test_colocation
      type: glob
      patterns: 
        - "**/*.test.{ts,tsx}"
        - "**/__tests__/**/*"
  verbosity: count_only
```

**What this reveals:**
- Barrel exports (index.ts pattern)
- Type definition organization
- Test file placement (co-located vs dedicated folders)

#### Step 4.3: Check for Linting and Formatting Config

Find ESLint, Prettier, and other code quality configurations.

```yaml
discover:
  queries:
    - id: lint_config
      type: glob
      patterns:
        - ".eslintrc*"
        - "eslint.config.{js,mjs,cjs}"
        - ".prettierrc*"
        - "prettier.config.{js,mjs,cjs}"
    - id: editor_config
      type: glob
      patterns:
        - ".editorconfig"
        - ".vscode/settings.json"
  verbosity: files_only
```

**Read the configs:**

```yaml
precision_read:
  files:
    - path: ".eslintrc.json"
      extract: content
    - path: ".prettierrc"
      extract: content
  verbosity: standard
```

**What this reveals:**
- Code style rules (indentation, quotes, semicolons)
- Enabled/disabled linting rules
- Formatting preferences

### Phase 5: Environment Setup

Set up developer environment with required dependencies, config files, and database.

#### Step 5.1: Check Node Version Requirements

Read `.nvmrc`, `package.json engines`, or `.node-version`.

```yaml
precision_grep:
  queries:
    - id: node_version_nvmrc
      pattern: '.*'
      glob: ".nvmrc"
    - id: node_version_package
      pattern: '"engines":\s*\{[\s\S]*?"node":\s*"[^"]+"'
      glob: "package.json"
      multiline: true
  output:
    format: matches
  verbosity: standard
```

**What this reveals:**
- Required Node.js version
- Package manager version requirements

#### Step 5.2: Install Dependencies

Run the package manager install command.

```yaml
precision_exec:
  commands:
    - cmd: "npm install"
      timeout_ms: 300000
  verbosity: minimal
```

**For pnpm or yarn:**

```yaml
precision_exec:
  commands:
    - cmd: "pnpm install"
      timeout_ms: 300000
  verbosity: minimal
```

#### Step 5.3: Setup Environment Variables

Identify required environment variables from `.env.example` or code.

```yaml
precision_read:
  files:
    - path: ".env.example"
      extract: content
  verbosity: standard
```

**Search for env var usage in code:**

```yaml
precision_grep:
  queries:
    - id: env_usage
      pattern: 'process\.env\.[A-Z_]+'
      glob: "src/**/*.{ts,tsx,js,jsx}"
  output:
    format: matches
    max_per_item: 20
  verbosity: minimal
```

**What this reveals:**
- Required environment variables
- API keys, database URLs, secrets needed
- Third-party service integrations

#### Step 5.4: Database Setup

Check for database schema files, migrations, and seed scripts.

```yaml
discover:
  queries:
    - id: prisma_schema
      type: glob
      patterns: ["prisma/schema.prisma"]
    - id: migrations
      type: glob
      patterns:
        - "prisma/migrations/**/*"
        - "migrations/**/*"
        - "db/migrations/**/*"
    - id: seed_scripts
      type: glob
      patterns:
        - "prisma/seed.{ts,js}"
        - "db/seed.{ts,js}"
        - "scripts/seed.{ts,js}"
  verbosity: files_only
```

**Run database setup:**

```yaml
precision_exec:
  commands:
    - cmd: "npx prisma generate"
    - cmd: "npx prisma migrate dev"
    - cmd: "npx prisma db seed"
  verbosity: standard
```

**What this reveals:**
- Database schema and models
- Migration history
- Seed data for development

### Phase 6: Build & Dev Workflow

Understand build commands, dev server, hot reload, and test runners.

#### Step 6.1: Identify Build Scripts

Extract scripts from package.json.

```yaml
precision_grep:
  queries:
    - id: scripts
      pattern: '"scripts":\s*\{[\s\S]*?\}'
      glob: "package.json"
      multiline: true
  output:
    format: matches
  verbosity: standard
```

**What this reveals:**
- `dev` or `start` command for local development
- `build` command for production build
- `test` command for running tests
- `lint` command for linting
- Custom scripts for deployment, database, etc.

#### Step 6.2: Test Build Process

Run the build command to verify setup.

```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
      timeout_ms: 300000
  verbosity: standard
```

**What this reveals:**
- Build errors or warnings
- Build output location
- Build time and performance

#### Step 6.3: Start Dev Server

Run the dev command to verify hot reload works.

```yaml
precision_exec:
  commands:
    - cmd: "npm run dev"
      timeout_ms: 60000
      until:
        pattern: "(ready|compiled|listening|started)"
        kill_after: true  # Stops dev server after pattern matches
  verbosity: standard
```

**What this reveals:**
- Dev server port (usually :3000, :5173, :8080)
- Hot reload configuration
- Startup time

#### Step 6.4: Run Tests

Execute test suite to verify test setup.

```yaml
precision_exec:
  commands:
    - cmd: "npm test"
      timeout_ms: 120000
  verbosity: standard
```

**What this reveals:**
- Test framework (Jest, Vitest, Mocha, etc.)
- Test coverage
- Failing tests or setup issues

### Phase 7: Key Patterns

Identify recurring patterns for state management, error handling, authentication, and routing.

#### Step 7.1: State Management Patterns

Search for state management libraries and patterns.

```yaml
discover:
  queries:
    - id: react_state
      type: grep
      pattern: '(useState|useReducer|useContext)'
      glob: "src/**/*.{ts,tsx}"
    - id: zustand
      type: grep
      pattern: "(create|useStore).*from ['\"]zustand"
      glob: "src/**/*.{ts,tsx}"
    - id: redux
      type: grep
      pattern: "(useSelector|useDispatch|createSlice)"
      glob: "src/**/*.{ts,tsx}"
    - id: jotai
      type: grep
      pattern: "(atom|useAtom).*from ['\"]jotai"
      glob: "src/**/*.{ts,tsx}"
  verbosity: count_only
```

**What this reveals:**
- Primary state management approach
- Global vs local state patterns
- Store organization

#### Step 7.2: Error Handling Patterns

Find error boundaries, try-catch patterns, and error reporting.

```yaml
# Use precision_grep instead of discover for multiline patterns
precision_grep:
  queries:
    - id: error_boundaries
      pattern: "(class|extends) .*ErrorBoundary"
      glob: "src/**/*.{ts,tsx}"
    - id: try_catch
      pattern: "try \{[\s\S]*?\} catch"
      glob: "src/**/*.{ts,tsx,js,jsx}"
      multiline: true
    - id: error_reporting
      pattern: "(Sentry|Bugsnag|ErrorBoundary|reportError)"
      glob: "src/**/*.{ts,tsx,js,jsx}"
  output:
    format: count_only
  verbosity: minimal
```

**What this reveals:**
- Error boundary usage
- Error logging and reporting setup
- Exception handling conventions

#### Step 7.3: Authentication Patterns

Identify authentication library and patterns.

```yaml
discover:
  queries:
    - id: auth_providers
      type: grep
      pattern: "(NextAuth|Clerk|Auth0|Supabase|Lucia|useAuth)"
      glob: "src/**/*.{ts,tsx}"
    - id: protected_routes
      type: grep
      pattern: "(withAuth|requireAuth|ProtectedRoute|middleware)"
      glob: "src/**/*.{ts,tsx}"
    - id: session_usage
      type: grep
      pattern: "(getSession|useSession|getServerSession)"
      glob: "src/**/*.{ts,tsx}"
  verbosity: count_only
```

**What this reveals:**
- Authentication provider (Clerk, NextAuth, custom)
- Protected route patterns
- Session management approach

#### Step 7.4: Routing Patterns

Understand routing architecture.

```yaml
discover:
  queries:
    - id: app_router
      type: glob
      patterns: ["app/**/page.{ts,tsx}", "app/**/layout.{ts,tsx}"]
    - id: pages_router
      type: glob
      patterns: ["pages/**/*.{ts,tsx}"]
    - id: react_router
      type: grep
      pattern: "(BrowserRouter|Routes|Route|useNavigate)"
      glob: "src/**/*.{ts,tsx}"
  verbosity: count_only
```

**What this reveals:**
- Routing framework (Next.js App Router, Pages Router, React Router)
- Route organization
- Dynamic route patterns

### Phase 8: Documentation Generation

Generate CLAUDE.md, architecture docs, and onboarding guides.

#### Step 8.1: Create CLAUDE.md Project Instructions

Write a comprehensive CLAUDE.md with project context.

```yaml
precision_write:
  files:
    - path: ".claude/CLAUDE.md"
      mode: fail_if_exists
      content: |
        # Project Name

        ## Overview
        [Brief description of the project, its purpose, and key features]

        ## Architecture
        - **Framework**: [Next.js 14 App Router / Remix / etc.]
        - **Language**: [TypeScript]
        - **Database**: [PostgreSQL with Prisma]
        - **Authentication**: [Clerk / NextAuth]
        - **State Management**: [Zustand / Redux / etc.]

        ## Directory Structure
        ```
        src/
          app/          # Next.js App Router pages and layouts
          components/   # React components
          lib/          # Utility functions and shared logic
          api/          # API route handlers
          types/        # TypeScript type definitions
        ```

        ## Development Workflow
        1. Install dependencies: `pnpm install`
        2. Setup environment: Copy `.env.example` to `.env.local`
        3. Setup database: `npx prisma migrate dev`
        4. Start dev server: `pnpm dev`
        5. Run tests: `pnpm test`

        ## Key Patterns
        - Components use PascalCase naming
        - Utilities use camelCase naming
        - Hooks start with `use` prefix
        - Server components by default, use 'use client' directive for client components

        ## Testing
        - Unit tests: Vitest
        - E2E tests: Playwright
        - Run with: `pnpm test`

        ## Deployment
        - Platform: [Vercel / Netlify / etc.]
        - CI/CD: [GitHub Actions]
        - Deploy command: `pnpm build`
  verbosity: minimal
```

#### Step 8.2: Generate Architecture Diagram

Create a mermaid diagram of the architecture.

```yaml
precision_write:
  files:
    - path: "docs/ARCHITECTURE.md"
      mode: fail_if_exists
      content: |
        # Architecture

        ## System Overview
        ```mermaid
        graph TD
          A[Client Browser] --> B[Next.js App Router]
          B --> C[React Server Components]
          B --> D[API Routes]
          D --> E[Database - Prisma]
          D --> F[External APIs]
          C --> E
        ```

        ## Module Boundaries
        - `app/`: Page routes and layouts (Next.js App Router)
        - `components/`: Reusable UI components
        - `lib/`: Business logic and utilities
        - `api/`: Backend API handlers

        ## Data Flow
        1. User requests page -> Next.js App Router
        2. Server Component fetches data -> Prisma -> Database
        3. Server renders component with data
        4. Client receives HTML with hydration instructions
        5. Client-side interactions -> API routes -> Database

        ## External Dependencies
        - Authentication: Clerk
        - Email: Resend
        - Storage: Vercel Blob
  verbosity: minimal
```

#### Step 8.3: Create Onboarding Checklist

Generate a checklist for new developers.

```yaml
precision_write:
  files:
    - path: "docs/ONBOARDING.md"
      mode: fail_if_exists
      content: |
        # Onboarding Checklist

        ## Prerequisites
        - [ ] Node.js 18+ installed
        - [ ] pnpm installed (`npm install -g pnpm`)
        - [ ] Git configured
        - [ ] PostgreSQL installed locally (or Docker)

        ## Setup Steps
        1. [ ] Clone repository
        2. [ ] Install dependencies: `pnpm install`
        3. [ ] Copy `.env.example` to `.env.local`
        4. [ ] Fill in environment variables (get from team)
        5. [ ] Setup database: `npx prisma migrate dev`
        6. [ ] Seed database: `npx prisma db seed`
        7. [ ] Start dev server: `pnpm dev`
        8. [ ] Open http://localhost:3000
        9. [ ] Run tests: `pnpm test`
        10. [ ] Verify build: `pnpm build`

        ## Key Resources
        - Architecture: [docs/ARCHITECTURE.md](./ARCHITECTURE.md)
        - API Docs: [docs/API.md](./API.md)
        - Code Review: Use `/code-review` skill

        ## First Tasks
        1. Read through CLAUDE.md for project context
        2. Explore the codebase structure
        3. Review recent pull requests
        4. Pick a "good first issue" from GitHub
  verbosity: minimal
```

### Phase 9: Contribution Workflow

Understand Git branching strategy, PR process, and CI/CD pipeline.

#### Step 9.1: Check Git Configuration

Find branch protection rules and workflow files.

```yaml
discover:
  queries:
    - id: github_workflows
      type: glob
      patterns: [".github/workflows/**/*.yml", ".github/workflows/**/*.yaml"]
    - id: git_hooks
      type: glob
      patterns: [".husky/**/*", ".git/hooks/**/*"]
    - id: branch_config
      type: glob
      patterns: [".github/CODEOWNERS", ".github/pull_request_template.md"]
  verbosity: files_only
```

**Read GitHub Actions workflows:**

```yaml
precision_read:
  files:
    - path: ".github/workflows/ci.yml"
      extract: content
  verbosity: standard
```

**What this reveals:**
- CI/CD pipeline steps
- Required checks before merge
- Deploy process

#### Step 9.2: Understand PR Process

Read PR template and contributing guidelines.

```yaml
precision_read:
  files:
    - path: ".github/pull_request_template.md"
      extract: content
    - path: "CONTRIBUTING.md"
      extract: content
  verbosity: standard
```

**What this reveals:**
- PR description requirements
- Review process
- Testing expectations

#### Step 9.3: Check Commit Conventions

Search for commit message conventions.

```yaml
# Check for commitlint config
precision_grep:
  queries:
    - id: commitlint
      pattern: '.*'
      glob: ".commitlintrc*"
  output:
    format: matches
  verbosity: minimal

# Check commit convention from recent commits
precision_exec:
  commands:
    - cmd: "git log --oneline -20"
  verbosity: standard
```

**What this reveals:**
- Commit message format (Conventional Commits, custom)
- Scopes used in commits

### Phase 10: Validation & Verification

Verify environment works end-to-end.

#### Step 10.1: Run Full Test Suite

Execute all tests with coverage.

```yaml
precision_exec:
  commands:
    - cmd: "npm test -- --coverage"
      timeout_ms: 180000
  verbosity: standard
```

**What this reveals:**
- Test coverage percentage
- Uncovered files or lines
- Slow or flaky tests

#### Step 10.2: Verify Linting Passes

Run linting to ensure code quality.

```yaml
precision_exec:
  commands:
    - cmd: "npm run lint"
  verbosity: standard
```

**What this reveals:**
- Linting errors or warnings
- Code style violations

#### Step 10.3: Check Type Safety

Run TypeScript type checker.

```yaml
precision_exec:
  commands:
    - cmd: "npm run typecheck"
  verbosity: standard
```

**What this reveals:**
- Type errors
- Missing type definitions
- `any` usage

#### Step 10.4: Verify Production Build

Build for production and check bundle size.

```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
      timeout_ms: 300000
    - cmd: "ls -lh .next/static/chunks" # Next.js example
  verbosity: standard
```

**What this reveals:**
- Build warnings or errors
- Bundle size
- Optimization opportunities

## Best Practices

### 1. Start Small, Go Deep

Don't try to understand everything at once. Start with:
1. Project structure (Phase 1)
2. Environment setup (Phase 5)
3. Build workflow (Phase 6)

Then dive deeper into architecture, patterns, and contribution workflow.

### 2. Use Precision Tools Efficiently

- Use `discover` with `verbosity: count_only` first to gauge scope
- Use `verbosity: files_only` to build target lists
- Use `precision_read` with `extract: outline` before reading full content
- Use `precision_grep` with `output.format: count_only` for pattern prevalence checks

### 3. Document as You Learn

Create or update documentation during onboarding:
- CLAUDE.md with project context
- Architecture diagrams
- Setup guides
- Common pitfalls and solutions

### 4. Validate Early

Run builds, tests, and linting early in the onboarding process. This catches environment issues before you invest time in understanding the codebase.

### 5. Ask Questions

When you find:
- Undocumented patterns
- Complex abstractions
- Missing tests
- Inconsistent conventions

Document them as questions for the team.

## Common Pitfalls

### Pitfall 1: Skipping Dependency Installation

**Problem:** Jumping into code reading without installing dependencies.

**Solution:** Always run `npm install` first. Many tools (TypeScript, ESLint) need dependencies to function.

### Pitfall 2: Ignoring Environment Variables

**Problem:** Missing `.env.local` file causes runtime errors.

**Solution:** Copy `.env.example` to `.env.local` and fill in required values. Ask team for secrets.

### Pitfall 3: Not Testing the Build

**Problem:** Assuming the build works without verifying.

**Solution:** Run `npm run build` early to catch configuration issues, missing dependencies, or TypeScript errors.

### Pitfall 4: Overlooking Database Setup

**Problem:** Application fails at runtime due to missing database schema.

**Solution:** Run migrations (`npx prisma migrate dev`) and seed data before starting dev server.

### Pitfall 5: Not Reading Existing Documentation

**Problem:** Missing key context in README.md, CONTRIBUTING.md, or project docs.

**Solution:** Use `precision_read` to read all markdown files in the root and `docs/` folder first.

## Validation Script

Use the validation script to check your onboarding completeness:

```bash
bash plugins/goodvibes/skills/quality/project-onboarding/scripts/validate-onboarding.sh
```

This will verify:
- Dependencies installed
- Environment variables configured
- Database setup complete
- Tests passing
- Build successful

## References

For detailed patterns and examples, see:
- [Onboarding Patterns Reference](./references/onboarding-patterns.md)
- [Architecture Mapping Examples](./references/onboarding-patterns.md#architecture-mapping)
- [Convention Detection Patterns](./references/onboarding-patterns.md#convention-detection)

## Related Skills

- `quality/code-review` - Review code quality after understanding the codebase
- `architecture/system-design` - Design new features following existing patterns
- `testing/test-strategy` - Write tests matching project conventions
