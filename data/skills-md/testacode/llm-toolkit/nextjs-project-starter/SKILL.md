---
name: nextjs-project-starter
description: Crea proyectos Next.js con stack configurable (Mantine, Supabase, Zustand). Usa cuando el usuario diga "crear proyecto Next.js", "nuevo proyecto web", "empezar app fullstack", "bootstrap Next.js", o quiera iniciar un proyecto personal.
---

# Next.js Project Starter

Create new Next.js projects with a configurable stack, always using latest stable versions with documentation verification.

## When to Use

- Creating a new personal project
- Starting a fullstack Next.js application
- Bootstrapping a project with Mantine + Supabase stack
- User says "create new project", "start new app", "nuevo proyecto"

## Core Principles

1. **Always ask before acting** - Never assume, always confirm
2. **Latest versions** - Search npm/docs for current stable versions
3. **Show breaking changes** - Warn about major version changes
4. **Configurable** - Let user choose what to include

## Workflow

### Phase 1: Project Basics

Ask user for:

```
1. Project name (kebab-case)
2. Project description (one line)
3. Target domain (carlosmonti.com / xmontc.xyz / custom / none)
```

### Phase 2: Node Version Setup

```bash
# Check current node version
nvm current

# Search for Next.js recommended Node version
# (use WebSearch to find latest compatibility)
```

Present options:
```
Node.js version for this project:
☐ Use current (vX.X.X)
☐ Use Next.js recommended LTS (vX.X.X)
☐ Specify custom version
```

Generate:
- `.nvmrc` with selected version
- `package.json` with `"engines": { "node": ">=X.X.X" }`

### Phase 3: Feature Selection

Present configurable features:

```
Core Features (select all that apply):
☐ Mantine UI + Tabler Icons
☐ Supabase (auth + database)
☐ Zustand (state management)
☐ Zod (validation)
☐ SWR (data fetching)
☐ TanStack Query (alternative to SWR)
☐ Vercel Analytics + Speed Insights
☐ Testing setup (Vitest + Testing Library)
```

### Phase 4: Version & Docs Verification

For EACH selected feature, execute this process:

```bash
# 1. Get latest version
npm view @mantine/core version

# 2. Search for documentation and breaking changes
# Use WebSearch or Exa to find:
# - Official docs
# - Migration guides
# - Known issues
```

Present to user:
```
📦 @mantine/core
   Version: ^7.15.0 (latest stable)
   Docs: https://mantine.dev/getting-started
   ⚠️ Note: v7 requires PostCSS preset (breaking from v6)

   Install this version? [Y/n]
```

**IMPORTANT**: Do this for EACH dependency before installing. Never batch install without verification.

### Phase 5: Integration Questions

After features are confirmed, ask about integrations:

```
Project Integrations (confirm each):

1. GitHub Repository
   ☐ Create private repo on GitHub?
   → Will use: gh repo create {name} --private

2. Vercel Deployment
   ☐ Link to Vercel for auto-deploy?
   → Will use: vercel link

3. Supabase Project (if Supabase selected)
   ☐ Create new Supabase project?
   → Will guide through supabase.com setup

4. CLAUDE.md
   ☐ Generate CLAUDE.md for this project?
   → Will create based on selected stack
```

### Phase 6: Project Creation

Execute in order:

```bash
# 1. Create Next.js project
npx create-next-app@latest {project-name} \
  --typescript \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

# 2. Navigate to project
cd {project-name}

# 3. Create .nvmrc
echo "{node-version}" > .nvmrc

# 4. Install selected dependencies (with verified versions)
npm install @mantine/core@^{version} @mantine/hooks@^{version} ...
```

### Phase 7: Structure Generation

Create preferred folder structure:

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   ├── (auth)/            # Auth route group
│   └── (main)/            # Main app routes
├── components/            # React components
│   ├── ui/               # Base UI components
│   └── features/         # Feature-specific components
├── hooks/                 # Custom React hooks
├── lib/                   # Core utilities
├── providers/             # React context providers
├── stores/                # Zustand stores
├── types/                 # TypeScript types
├── utils/                 # Utility functions
│   └── supabase/         # Supabase client (if selected)
└── test/                  # Test setup & mocks
    ├── mocks/
    └── setup/
```

### Phase 8: Configuration Files

Generate based on selections:

#### If Mantine selected:
```javascript
// postcss.config.mjs
export default {
  plugins: {
    'postcss-preset-mantine': {},
    'postcss-simple-vars': {
      variables: {
        'mantine-breakpoint-xs': '36em',
        'mantine-breakpoint-sm': '48em',
        'mantine-breakpoint-md': '62em',
        'mantine-breakpoint-lg': '75em',
        'mantine-breakpoint-xl': '88em',
      },
    },
  },
};
```

#### If Supabase selected:
```typescript
// src/utils/supabase/client.ts
// src/utils/supabase/server.ts
// src/utils/supabase/middleware.ts
```

#### Environment template:
```bash
# .env.example
# Supabase (if selected)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Analytics (if selected)
NEXT_PUBLIC_VERCEL_ANALYTICS_ID=
```

### Phase 9: CLAUDE.md Generation

If user confirmed, generate CLAUDE.md with:

```markdown
# {Project Name}

{Description}

## Stack

- **Framework**: Next.js {version} (App Router)
- **UI**: Mantine {version}
- **Database**: Supabase
- **State**: Zustand
- **Validation**: Zod

## Commands

```bash
npm run dev      # Start development server
npm run build    # Production build
npm run test     # Run tests
npm run lint     # Run ESLint
```

## Project Structure

{Generated structure tree}

## Key Patterns

- Server Components by default
- Client Components marked with 'use client'
- API routes in src/app/api/
- Zustand stores in src/stores/
```

### Phase 10: Final Summary

Present summary to user:

```
✅ Project created: {name}

📁 Location: ~/Projects/github/{name}
🔧 Node: {version} (via .nvmrc)

📦 Installed:
   - next@{version}
   - @mantine/core@{version}
   - @supabase/ssr@{version}
   - zustand@{version}
   - zod@{version}

🔗 Integrations:
   - GitHub: https://github.com/testacode/{name}
   - Vercel: Linked (auto-deploy on push)
   - Supabase: {project-url}

📝 Next steps:
   1. cd {name}
   2. cp .env.example .env.local
   3. Configure Supabase credentials
   4. npm run dev
```

## Dependencies Reference

When searching for versions, use these as baseline:

| Package | Purpose | Docs URL |
|---------|---------|----------|
| next | Framework | https://nextjs.org/docs |
| @mantine/core | UI Components | https://mantine.dev |
| @mantine/hooks | React Hooks | https://mantine.dev/hooks |
| @tabler/icons-react | Icons | https://tabler.io/icons |
| @supabase/ssr | Supabase SSR | https://supabase.com/docs |
| zustand | State | https://zustand-demo.pmnd.rs |
| zod | Validation | https://zod.dev |
| swr | Data Fetching | https://swr.vercel.app |
| @tanstack/react-query | Data Fetching | https://tanstack.com/query |
| vitest | Testing | https://vitest.dev |

## Error Handling

If any step fails:

1. **npm install fails**: Check Node version, try with `--legacy-peer-deps`
2. **gh repo create fails**: Verify `gh auth status`
3. **vercel link fails**: Run `vercel login` first
4. **Supabase setup fails**: Guide user to manual setup at supabase.com

Always ask user how to proceed on errors, never assume.
