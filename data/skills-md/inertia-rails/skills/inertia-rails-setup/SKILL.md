---
name: inertia-rails-setup
description: >-
  One-time project initializer for Inertia Rails skills. Detects stack and frontend framework
  (React/Vue/Svelte) from Gemfile and package.json, offers to install recommended deps
  (alba-inertia, js-routes, pagy, shadcn), and generates a CLAUDE.md section that configures
  which skill patterns apply. Use when first installing these skills, bootstrapping a new
  Inertia Rails project, or when the stack changes.
---

# Inertia Rails Project Setup

Detect stack, offer recommended deps, generate CLAUDE.md configuration.

**Run once per project.** Re-run when the stack changes.

**NEVER:**
- Run setup without `inertia_rails` gem in Gemfile — all skills assume it exists. If missing, tell the user to install it first.
- Overwrite existing `## Inertia Rails Stack` in CLAUDE.md without reading it — the user may have manual customizations. Replace only the auto-generated block.
- Add `@/` resolve aliases to `vite.config.ts` — `vite-plugin-ruby` already provides them. Only add to `tsconfig.json`.
- Recommend `alba-inertia` if the project uses `jbuilder` AND the user hasn't expressed interest in switching — suggest it, but don't push. You CAN still suggest it if the project has `blueprinter` (alba is a direct upgrade path).
- Generate CLAUDE.md blocks for skills the user doesn't have installed — saying "alba-inertia skill does NOT apply" is correct; saying "use alba-inertia" when the gem is absent is wrong.

## Step 1: Detect Current Stack

Read `Gemfile` (NOT `Gemfile.lock`) and `package.json` and check for:

| Look for | Means |
|----------|-------|
| `inertia_rails` gem | Inertia Rails installed (required) |
| `@inertiajs/react` in package.json | React frontend |
| `@inertiajs/vue3` in package.json | Vue 3 frontend |
| `@inertiajs/svelte` in package.json | Svelte frontend |
| `alba-inertia` gem | Convention-based rendering active |
| `alba` + `typelizer` gems (no `alba-inertia`) | Alba serialization without convention rendering |
| `pagy` gem | Pagy pagination |
| `kaminari` gem | Kaminari pagination |
| `rspec-rails` gem | RSpec testing |
| `js-routes` gem | Typed frontend path helpers |
| `devise` gem | Devise authentication |
| `pundit` gem | Pundit authorization |
| `action_policy` gem | Action Policy authorization |
| `components.json` in root exists | shadcn installed (React: shadcn/ui, Vue: shadcn-vue, Svelte: shadcn-svelte) |

## Step 2: Recommend Missing Deps

Present detected stack, then offer deps that unlock skill features but aren't
installed yet. Use AskUserQuestion with multiSelect for the recommendations.

**Only recommend what's missing.** Skip anything already detected in Step 1.

| Dep | Type | Install command | What it unlocks |
|-----|------|-----------------|-----------------|
| `alba` + `typelizer` + `alba-inertia` | gems | `bundle add alba typelizer alba-inertia` | Convention-based rendering, auto-generated TypeScript types from Ruby. Eliminates `render inertia: { ... }` boilerplate and manual TS interfaces. Unlocks `alba-inertia` skill. |
| `js-routes` | gem | `bundle add js-routes` | Typed path helpers (`usersPath()`, `userPath(id)`) in React — no more hardcoded URL strings. |
| `pagy` | gem | `bundle add pagy` | Lightweight pagination with Inertia-friendly metadata. |
| shadcn/ui (React) | npx | `npx shadcn@latest init` | Pre-built React components adapted for Inertia. Unlocks `shadcn-inertia` skill. |
| shadcn-vue (Vue) | npx | `npx shadcn-vue@latest init` | Pre-built Vue components adapted for Inertia. Unlocks `shadcn-vue-inertia` skill. |
| shadcn-svelte (Svelte) | npx | `npx shadcn-svelte@latest init` | Pre-built Svelte components (bits-ui) adapted for Inertia. Unlocks `shadcn-svelte-inertia` skill. |

**Do NOT recommend** gems the user clearly chose alternatives for (e.g., don't suggest Pagy if Kaminari is present, you can still suggest alba if the project has `jbuilder` or `blueprinter`).

## Step 3: Install Opted-In Deps

Post-install scaffolding per dep:

1. **alba-inertia** — also scaffold `ApplicationResource`:
   ```ruby
   # app/resources/application_resource.rb
   class ApplicationResource
     include Alba::Resource
     helper Typelizer::DSL
     helper Alba::Inertia::Resource
     include Rails.application.routes.url_helpers
   end
   ```
   And add Typelizer initializer:
   ```ruby
   # config/initializers/typelizer.rb
   Typelizer.configure do |config|
     config.output_dir = Rails.root.join("app/frontend/types/generated")
   end
   ```
2. **js-routes** — run `rails generate js_routes` if the generator exists
3. **shadcn** — framework-specific init:
   - React: `npx shadcn@latest init`
   - Vue: `npx shadcn-vue@latest init`
   - Svelte: `npx shadcn-svelte@latest init`
   After init, add `@/` resolve aliases to `tsconfig.json` if not present

## Step 4: Generate CLAUDE.md

Find or create `CLAUDE.md` in the project root. If `## Inertia Rails Stack`
exists, replace it (up to next `##` or EOF). Otherwise, append.

**MANDATORY — READ ENTIRE FILE** before assembling the CLAUDE.md block:
[`references/claude-md-templates.md`](references/claude-md-templates.md) (~90 lines) — all
template blocks for each stack variant (serialization, UI, pagination, testing, routing,
authorization). Pick one block per category based on the detected stack.

**Do NOT load** the templates file until Step 4 — Steps 1-3 determine which blocks to use.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `npx shadcn@latest init` fails with "No framework detected" | Missing or misconfigured `vite.config.ts` | Ensure `vite-plugin-ruby` is configured and `tailwindcss` is in `package.json` before running init |
| Typelizer generates types in wrong directory | Missing or wrong `output_dir` in initializer | Add `config/initializers/typelizer.rb` with `config.output_dir = Rails.root.join("app/frontend/types/generated")` |
| `@/` imports not resolving | Aliases added to `vite.config.ts` instead of `tsconfig.json` | `vite-plugin-ruby` handles Vite aliases — only `tsconfig.json` needs `@/` paths for TypeScript |
| CLAUDE.md has conflicting instructions | Multiple `## Inertia Rails Stack` sections | Delete duplicates — only one auto-generated block should exist |
| Skills reference `alba-inertia` but it's not installed | Setup wasn't run, or alba wasn't selected | Re-run setup; CLAUDE.md should say "alba-inertia skill does NOT apply" if gem is absent |
| `js_routes:generate` fails | `js-routes` gem installed but generator not yet run | Run `rails generate js_routes` first to create the config file, then `rails js_routes:generate` |

## Step 5: Summary

Tell the user:
1. What was installed
2. Which skills are relevant to their stack (and which to ignore)
3. Review `## Inertia Rails Stack` in CLAUDE.md — it takes precedence over
   generic examples in individual skills
