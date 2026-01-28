---
name: secret-sauce
description: Development best practices and project patterns. Use when starting projects, setting up CLAUDE.md, coding TypeScript/Next.js/React/Supabase, implementing AI flows, data fetching, testing, deployment, git workflows, browser automation, centralized configuration, or Tailwind CSS v4.
---

# Secret Sauce

Best practices, rules, and templates extracted from real production projects.

## Quick Reference

| Category | Reference File |
|----------|----------------|
| **Tech Stack** | `references/tech-stack.md` |
| **Project Setup** | `references/claude-md-template.md` |
| **Project Tracking** | `references/project-tracking.md` |
| **Coding Standards** | `references/coding-standards.md` |
| **Centralization** | `references/centralization-patterns.md` |
| **Tailwind v4** | `references/tailwind-v4.md` |
| **AI Development** | `references/ai-flow-patterns.md` |
| **Data Fetching** | `references/data-fetching.md` |
| **Git Workflow** | `references/git-workflows.md` |
| **Testing** | `references/testing-patterns.md` |
| **Supabase** | `references/supabase-patterns.md` |
| **Deployment** | `references/deployment-patterns.md` |
| **Browser Tools** | `references/browser-automation.md` |
| **Versioning** | `references/version-management.md` |

## Framework Rules

| Framework | Rule File |
|-----------|-----------|
| TypeScript | `rules/typescript.md` |
| Next.js | `rules/nextjs.md` |
| React | `rules/react.md` |
| Supabase | `rules/supabase.md` |
| Security | `rules/security.md` |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/CLAUDE.md.template` | Project configuration starter |
| `templates/settings.json.template` | Permission configuration |
| `templates/project-plan.md.template` | Project planning document |
| `templates/implementation-plan.md.template` | Technical implementation plan |
| `templates/code-review.md.template` | Code review summary |
| `templates/changelog.md.template` | Project changelog |

---

## Usage

### Starting a New Project

1. Copy `templates/CLAUDE.md.template` to your project root as `CLAUDE.md`
2. Customize sections for your stack
3. Reference specific rules: `~/.claude/skills/secret-sauce/rules/typescript.md`

### Setting Up Permissions

1. Copy `templates/settings.json.template` to `.claude/settings.json`
2. Adjust permissions for your workflow

### Project Documentation

Use templates for consistent project documentation:
- `project-plan.md.template` for planning
- `implementation-plan.md.template` for technical specs
- `code-review.md.template` for reviews

---

## Key Patterns

### CLAUDE.md Structure

Every project CLAUDE.md should include:
1. YAML frontmatter (title, status, owner, tags)
2. Quick Reference section with key commands
3. Active/Pending/Completed projects
4. Stack-specific guidelines
5. Development patterns

### Git Workflow

- Commit format: `<type>(<scope>): <description>`
- Never commit without confirmation
- Branch naming: `feature/<name>`, `fix/<name>`
- PR template with summary and test plan

### Centralization Pattern

All configuration in `@/config`:
```typescript
import { env, isProduction, getServiceUrl } from '@/config';
```

### Configuration Hierarchy

1. Database configuration (system_configuration table)
2. Environment variables (.env.local)
3. Hardcoded defaults

Secrets (API keys) → `.env.local` only
Configs (models, URLs) → Database with fallback

### Testing Standards

- Target: >90% coverage
- Use Jest with 30s timeout for ML operations
- Add new test directories to test runners
- Security tests required for auth/validation

### AI Flow Pattern

1. Zod schemas for input/output
2. Prompt builder functions
3. OpenAI SDK v6 with `zodResponseFormat()`
4. Error handling with Result types
5. Server action wrapper

### Data Fetching

- Always pass `signal` to fetch calls
- Use `isAbortError()` to handle cancellation
- Memoize fetch options to prevent refetches
- Use `usePolling` for dashboards with visibility-aware intervals

### Security Checklist

- Strict TypeScript (no `any`)
- Zod input validation
- Safe property access: `Object.prototype.hasOwnProperty.call()`
- XSS prevention on all user inputs
- Rate limiting in API routes
