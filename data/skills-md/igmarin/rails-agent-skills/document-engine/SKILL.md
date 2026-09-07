---
name: document-engine
type: atomic
license: MIT
description: >
  Use when writing engine README, install, and configuration docs.
  Trigger words: engine README, install guide, engine docs.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Document Engine

Use this skill when writing or maintaining documentation for Rails engines.

## Core Process & Constraints

| Step | Section | Focus |
|------|---------|-------|
| 1 | Installation | gem add, bundle, run install generator — **show minimum working path first** |
| 2 | Host Assumptions | Explicitly state any host model, job backend, or auth integration assumptions |
| 3 | Configuration | All options with defaults, required vs optional |
| 4 | Mounting | Explicit `mount MyEngine::Engine, at: '/path'` in routes — show once only |
| 5 | Usage | Copyable code for typical workflows |
| 6 | Migrations | Install generator, one-time setup, upgrade-impacting changes |

> **Hard gate:** All generated documentation MUST satisfy steps 1, 2, and 3 above before proceeding to optional sections.

**README snippet (install + mount):**

```markdown
## Installation

Add to your Gemfile:

    gem 'my_engine'

Run:

    bundle install
    rails generate my_engine:install

This creates `config/initializers/my_engine.rb`. Mount the engine in `config/routes.rb`:

    mount MyEngine::Engine, at: '/admin'
```

**Configuration section:**

```markdown
## Configuration

In `config/initializers/my_engine.rb`:

    MyEngine.configure do |config|
      config.user_class = "User"       # required: host model for current user
      config.widget_count = 10         # optional, default 10
    end
```

## Extended Resources

See [CHECKLIST.md](./CHECKLIST.md) for the full recommended README shape and documentation gap checklist. Critical gaps tracked there: installation steps, all config options with defaults, explicit mount path, migration timing, host model/auth assumptions.

- [assets/configuration.md](assets/configuration.md) — detailed config option catalog with type info, validation rules, and all supported defaults
- [assets/examples.md](assets/examples.md) — realistic end-to-end usage examples covering common host-app integration workflows
- [assets/installation.md](assets/installation.md) — step-by-step install and generator reference including post-install setup tasks

## Output Style

1. Keep sections short and task-oriented.
2. Validate against CHECKLIST.md: a checklist item **passes** when the docs contain a corresponding section with at least one copyable code example or explicit prose statement; it **fails** when absent, incomplete, or lacking a concrete example. Fix each failing item, then re-run from the top. Do not finalize until all critical items pass.
3. **Section Delineation**: Explicitly label mandatory "Hard-Gate" sections (Installation, Configuration, Host Assumptions) and "Optional" sections (Extension Points, Usage Examples).
4. **Upgrade Notes**: Include at least one copyable code example in any Upgrade Notes section.
5. Language — Must be in English unless explicitly requested otherwise.

**Common pitfalls to avoid:**
- Duplicate `mount MyEngine::Engine ...` across multiple sections — show it only once in the primary installation/mounting section.
- Syntax errors in Ruby/Rails code examples — double-check route mounting and authentication blocks (e.g., `authenticate :user, ->(u) { u.admin? } do`).

## Integration

| Skill | When to chain |
|-------|----------------|
| create-engine | Host-app contract, structure, extension points to document |
| create-engine-installer | Install generators, setup steps to document |
| release-engine | Changelog, upgrade notes, version documentation |
| generate-api-collection | When documenting or adding API endpoints (keep Postman collection in sync) |
