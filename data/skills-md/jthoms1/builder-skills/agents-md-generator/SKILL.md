---
name: agents-md-generator
description: "Generate comprehensive agents.md files for Builder.io Fusion projects. Creates project-specific AI instruction files that establish conventions, build commands, testing procedures, design system rules, and coding standards. Use when setting up a new project, onboarding a repository to AI-assisted development, or improving AI code generation quality."
---

# agents.md Generator

You are a specialist in creating `agents.md` files—the configuration files that Builder.io Fusion uses to understand project conventions. A well-crafted agents.md dramatically improves code generation quality by teaching the AI your team's patterns, preferences, and requirements.

## Determine the Workflow

Use AskUserQuestion to clarify which workflow the user needs:

1. **Generate New** - Create agents.md for a project that doesn't have one
2. **Update Existing** - Improve or expand an existing agents.md
3. **Analyze Only** - Review the project and provide recommendations without generating

If the user's intent is clear from their message, proceed directly.

## Quick Start

1. **Check for existing file**: Look for `agents.md` at the repository root
2. **Analyze the repository**: Examine existing patterns, dependencies, and configuration
3. **Identify the project type**: Framework, language, styling approach, testing setup
4. **Read specialized template**: Use the appropriate template for the project type
5. **Generate the agents.md**: Create a comprehensive file at repository root
6. **Validate**: Verify all commands work and paths are correct

## Why agents.md Matters

Without clear instructions, AI assistants guess at conventions. With a good agents.md, generated code looks like your team wrote it. The file should:

- Establish coding standards and naming conventions
- Document build, test, and dev commands
- Specify design system components and usage rules
- Define approved/forbidden dependencies
- List common pitfalls to avoid

## Section Priority Guide

| Section | Purpose | Priority |
|---------|---------|----------|
| Project Overview | Context about the app/repo | Required |
| Dev Environment | Setup, install, run commands | Required |
| Code Style | Formatting, naming, patterns | Required |
| Design System | Components, tokens, usage rules | High |
| Testing | Test commands, coverage requirements | High |
| File Structure | Where things go | Medium |
| Dependencies | What to use, what to avoid | Medium |
| Common Pitfalls | Mistakes to avoid | Medium |
| Git Workflow | Branching, commits, PRs | Optional |

## Specialized Resources

Read the appropriate template based on project type:

| Project Type | Resource | When to Use |
|-------------|----------|-------------|
| Monorepo | `monorepo-template.md` | Turborepo, Nx, pnpm workspaces |
| Next.js App Router | `nextjs-app-router-template.md` | Next.js 13+ with app directory |
| Standard project | `assets/complete-example.md` | General reference for any project |

## Repository Analysis Workflow

Before generating an agents.md, analyze the codebase systematically:

### Step 1: Package Manager & Scripts

Examine `package.json` for:
- Package manager (npm, pnpm, yarn, bun)
- Scripts: dev, build, test, lint commands
- Key dependencies (framework, styling, testing)

### Step 2: Framework & Structure

Identify by checking for these directories and files:
- `src/`, `app/`, `pages/`, `components/` directories
- Config files: `.eslintrc*`, `.prettierrc*`, `tsconfig.json`, `tailwind.config.*`, `biome.json`
- Framework indicators: `next.config.*`, `vite.config.*`, `nuxt.config.*`

Look for:
- React, Vue, Svelte, or other framework
- App Router vs Pages Router (Next.js)
- TypeScript configuration
- Styling approach (Tailwind, CSS Modules, etc.)

### Step 3: Design System

Search for:
- Design system imports (patterns like `from '@company/ui'`)
- Component library references in package.json (shadcn, radix, mui, chakra, mantine)
- Design token files or CSS variables

### Step 4: Testing Setup

Identify by looking for:
- Test files: `*.test.*`, `*.spec.*`
- Test config: `jest.config.*`, `vitest.config.*`, `playwright.config.*`
- Test libraries in package.json (testing-library, jest, vitest, playwright)

### Step 5: Monorepo Detection

Check for monorepo indicators:
- `turbo.json`, `nx.json`, `pnpm-workspace.yaml`, `lerna.json`
- `packages/`, `apps/`, `libs/` directories
- Workspaces configuration in package.json

If monorepo detected, read `monorepo-template.md` for additional sections.

## agents.md Template Structure

Generate the file at the repository root as `agents.md` with these sections:

```markdown
# agents.md

## Project Overview

[Brief description of what this application does]

**Tech Stack:**
- Framework: [Next.js 14 / React 18 / Vue 3 / etc.]
- Language: [TypeScript / JavaScript]
- Styling: [Tailwind CSS / CSS Modules / etc.]
- Testing: [Jest / Vitest / Playwright / etc.]

---

## Dev Environment

### Setup
[Package manager] install
cp .env.example .env.local

### Common Commands
| Command | Purpose |
|---------|---------|
| `[pm] dev` | Start development server |
| `[pm] build` | Production build |
| `[pm] test` | Run test suite |
| `[pm] lint` | Run linter |

---

## Code Style

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase with use prefix | `useAuth.ts` |
| Utilities | camelCase | `formatDate.ts` |

### File Organization
[Directory structure]

---

## Design System

[If applicable - component library, usage rules, tokens]

---

## Testing

[Test patterns, requirements, file locations]

---

## Common Pitfalls

[Project-specific mistakes to avoid]
```

See `assets/complete-example.md` for a fully-fleshed example.

## Handling Existing agents.md

If the project already has an `agents.md`:

1. **Read and analyze** the existing file
2. **Identify gaps** - missing sections, outdated commands, vague rules
3. **Propose updates** - show what would be added or changed
4. **Ask before replacing** - confirm with user before overwriting

## Validation Checklist

Before finalizing an agents.md, verify:

- [ ] File is named `agents.md` (lowercase) at repository root
- [ ] Package manager commands match actual scripts in package.json
- [ ] Build and dev commands actually exist
- [ ] Design system package name is accurate (if referenced)
- [ ] File structure matches actual repository
- [ ] No references to non-existent packages or files
- [ ] Under 500 lines total

## Best Practices

### Do:
- Start simple, add detail based on actual AI behavior issues
- Use specific file paths and real examples from the codebase
- Include actual component names from the design system
- Reference real configuration files (tsconfig paths, etc.)
- Update when conventions change

### Don't:
- Write vague guidance ("write clean code")
- Create rules that conflict with each other
- Exceed 500 lines—keep it focused
- Include sensitive information (API keys, internal URLs)
- Duplicate information that's in other config files

## Iteration Pattern

After creating the initial agents.md:

1. Generate code using the AI
2. Note where AI deviates from conventions
3. Add specific rules to address deviations
4. Repeat until AI output matches expectations

## Resources

| Resource | When to Use |
|----------|-------------|
| `assets/complete-example.md` | Full reference example |
| `monorepo-template.md` | Turborepo/Nx/pnpm workspaces |
| `nextjs-app-router-template.md` | Next.js 13+ App Router |

## Output Format

When generating an agents.md, provide:

1. **Analysis Summary**: Key findings from repository analysis
2. **Generated agents.md**: The complete file content
3. **Validation Notes**: Any commands to verify or potential issues found
