---
name: document
description: |
  Generate documentation for your codebase — reference docs for a file, feature guides, or a full documentation site.
  Use when asked to "document this", "generate docs", "write documentation", "create API reference",
  or when you need thorough documentation for a module, feature, or entire project.
  Framework-aware: detects Fumadocs, Nextra, Docusaurus, etc. and generates in the right format.
license: MIT
argument-hint: "[path-or-description]"
metadata:
  author: howells
website:
  order: 18
  desc: Generate docs
  summary: Generate documentation for your codebase — from a single file reference to a full documentation site.
  what: |
    Document reads your code and generates thorough documentation. Point it at a file for a reference doc, describe a feature for an end-to-end guide, or ask it to document the whole project. It detects your docs framework (Fumadocs, Nextra, etc.) and generates in the right format. For full-site docs, it spawns parallel agents to write sections simultaneously.
  why: |
    Code without documentation is a liability. Document turns your codebase into something a new developer (or user) can understand without reading every file. It asks who the docs are for — developers or users — and adjusts depth and tone accordingly.
  decisions:
    - Conversation-driven. No flags. Detects intent from what you give it.
    - Asks audience first. Developer docs and user docs are fundamentally different.
    - Framework-aware, not framework-coupled. Detects Fumadocs/Nextra/etc. and adapts format. Recommends a framework if none exists, but doesn't install it.
  agents:
    - docs-writer
---

<tool_restrictions>
# Tool Restrictions

**Do NOT use the `EnterPlanMode` tool.** This skill has its own documentation generation process. Claude's built-in plan mode would bypass it.

**Do NOT use the `ExitPlanMode` tool.** This skill is never in plan mode.

**ALWAYS use the `AskUserQuestion` tool for questions.** Never ask questions as plain text in your response. Every question to the user — whether clarifying scope, choosing audience, or validating content — MUST use the `AskUserQuestion` tool. This enforces one question at a time and prevents walls of text with multiple questions. If you need to provide context before asking, keep it to 2-3 sentences max, then use the tool.
</tool_restrictions>

<key_principles>
# Key Principles

- **One question at a time via AskUserQuestion tool** — Every question MUST use the `AskUserQuestion` tool. Never write questions as plain text. Never ask more than one question per message.
- **Substance before meta-decisions** — Scan the codebase and show what you found BEFORE asking about audience, format, or location. Users decide better with concrete context.
- **Framework-aware, not framework-coupled** — Detect existing docs frameworks and generate in their format. If none exists, generate plain markdown and recommend one. Never install or scaffold frameworks.
- **Incremental validation** — Generate a sample section first. Get approval on style and depth before generating the rest.
- **Respect existing docs** — When docs already exist, offer to add to the existing structure rather than replacing everything.
- **Code examples from source** — Every code example in generated docs must come from actual source code, never fabricated.
</key_principles>

<tasklist_context>
**Use TaskList tool** to check for existing tasks related to documentation work.

If a related task exists, note its ID and mark it `in_progress` with TaskUpdate when starting.
</tasklist_context>

<required_reading>
**Read these reference files NOW:**
1. ${CLAUDE_PLUGIN_ROOT}/references/documentation-guide.md
2. ${CLAUDE_PLUGIN_ROOT}/templates/doc-templates.md
</required_reading>

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check for recent documentation work or related changes.
</progress_context>

<process>
# Documentation Generation

## Phase 1: Detect Intent & Context

**Silently gather context (don't dump findings on the user):**

1. Read `package.json` — identify stack, dependencies, project name
2. Scan directory structure — `app/`, `pages/`, `src/`, `packages/`
3. Check for existing docs — Glob `docs/**/*.md`, `docs/**/*.mdx`, `content/**/*.md`, `content/**/*.mdx`
4. Check for existing docs framework (see Framework Detection below)

**Then determine intent from the user's input:**

**If user provided a file/directory path** (e.g., `/arc:document src/lib/auth.ts`):
- Read the target file/directory
- Analyze: exports, types, dependencies, usage patterns
- Use AskUserQuestion:
  ```
  Question: "I see [file] exports [N] functions and [N] types. Should I..."
  Header: "Scope"
  Options:
    - label: "Document just this file"
      description: "Reference doc: exports, types, usage examples"
    - label: "Document the broader feature"
      description: "Feature guide: all related files, end-to-end"
  ```
- Route to Reference or Feature flow based on answer

**If user provided a description** (e.g., "document the auth feature"):
- Route to Feature flow

**If user provided no args:**
- Use AskUserQuestion:
  ```
  Question: "What would you like to document?"
  Header: "Scope"
  Options:
    - label: "A specific file or module"
      description: "I'll point you at a file and generate a reference doc"
    - label: "A feature"
      description: "End-to-end documentation for a feature across all its files"
    - label: "The entire project"
      description: "Full documentation site — I'll scan the codebase and generate everything"
  ```
- Route based on answer

## Phase 2: Scope & Audience

### Reference Flow

1. Read the target file completely
2. Analyze exports, types, interfaces, dependencies, imported-by relationships
3. Present findings: "[File] exports [list]. It depends on [list] and is used by [list]."
4. Ask audience via AskUserQuestion:
   ```
   Question: "Who is this documentation for?"
   Header: "Audience"
   Options:
     - label: "Developers"
       description: "How the code works: architecture, types, patterns, dependencies"
     - label: "Users"
       description: "How to use it: getting started, configuration, examples"
     - label: "Both"
       description: "Separate sections for developers and users"
   ```

### Feature Flow

1. Identify all files that comprise the feature:
   - Routes/pages related to it
   - API endpoints
   - Components
   - Types/interfaces
   - Utilities/helpers
   - Tests
   - Configuration
2. Present: "The [feature] spans [N] files: [list key files]"
3. If existing docs directory found, ask via AskUserQuestion:
   ```
   Question: "I see existing docs at [path]. Should I..."
   Header: "Existing docs"
   Options:
     - label: "Add to existing structure"
       description: "Create new doc files in the existing docs directory"
     - label: "Create standalone"
       description: "Generate docs in a new location"
   ```
4. Ask audience (same as Reference flow)

### Full-Site Flow

1. **Scan the codebase.** Identify documentable units:

   | What | Detection |
   |------|-----------|
   | Routes/Pages | Glob `app/`, `pages/`, `src/app/` |
   | API endpoints | Glob `api/` routes, server actions, tRPC routers |
   | Components | Exported components with props/interfaces |
   | Packages | `packages/*/package.json` in monorepos |
   | Configuration | `.env.example`, config files, environment variables |
   | Database schema | Drizzle schema files, Prisma schema |
   | Authentication | Auth providers, middleware, protected routes |
   | CLI commands | `bin/` or command definitions |

2. **Generate an outline.** Present it to the user:
   ```
   I found [N] routes, [N] API endpoints, [N] packages, and a [database] schema.

   Proposed documentation outline:
   1. Getting Started
   2. Features
      - Auth (5 files)
      - Billing (3 files)
      - Notifications (4 files)
   3. API Reference
      - Users endpoint
      - Orders endpoint
   4. Architecture
      - Overview
   5. Reference
      - Components (12)
      - Utilities (8)
   ```

3. **Ask for approval** via AskUserQuestion:
   ```
   Question: "Does this outline look right?"
   Header: "Outline"
   Options:
     - label: "Yes, proceed"
       description: "Generate docs for all these sections"
     - label: "Remove some sections"
       description: "I'll tell you what to skip"
     - label: "Add something missing"
       description: "There's something I want documented that's not listed"
   ```

4. **Ask audience** (same question as Reference/Feature flow)

## Phase 3: Framework Detection

Check `package.json` dependencies and project files:

| Framework | Detection | Content Format |
|-----------|-----------|---------------|
| Fumadocs | `fumadocs-core` in deps, `source.config.ts` exists | `.mdx` with `meta.json` sidebar configs |
| Nextra | `nextra` in deps, `_meta.json` files exist | `.mdx` with `_meta.json` sidebar configs |
| Docusaurus | `@docusaurus/core` in deps | `.mdx` with `sidebars.js` |
| Starlight | `@astrojs/starlight` in deps | `.mdx` with Astro sidebar config |
| VitePress | `vitepress` in deps | `.md` with `.vitepress/config` sidebar |
| None | No framework detected | `.md` with README index |

**If framework detected:**
- Note the format silently
- Generate content in that format
- Detect existing content directory (e.g., `content/docs/` for Fumadocs)

**If no framework detected:**
- Will generate plain markdown
- After sample validation, recommend a framework based on stack:
  - Next.js project → "Fumadocs would give you search, navigation, and a polished UI. Set it up with `/arc:implement`?"
  - Astro project → "Starlight is built for Astro and gives you great docs out of the box."
  - General → "Plain markdown works everywhere. If you want a docs site later, Fumadocs or VitePress are good options."
- Use AskUserQuestion:
  ```
  Question: "No docs framework detected. Want to..."
  Header: "Format"
  Options:
    - label: "Plain markdown"
      description: "Simple .md files with a README index. Works everywhere."
    - label: "Set up a framework first"
      description: "I'll recommend one for your stack. Use /arc:implement to scaffold it, then come back."
  ```

## Phase 4: Sample & Validation

**Before generating all docs, produce one sample section.**

Pick the most representative section from the outline (or the target for Reference/Feature flow). Generate it fully.

Show the sample to the user, then ask via AskUserQuestion:
```
Question: "Here's the [section name] documentation. Is the depth and style right?"
Header: "Style check"
Options:
  - label: "Yes, generate the rest"
    description: "This depth and tone is what I want"
  - label: "More detailed"
    description: "Include more technical depth, more examples"
  - label: "Less detailed"
    description: "Keep it higher-level, less verbose"
  - label: "Different tone"
    description: "I'll describe what I want changed"
```

**If user wants changes:** adjust and regenerate the sample. Repeat until approved.

This validated sample becomes the **style reference** for all subsequent generation (and for docs-writer agents in full-site mode).

## Phase 5: Location

**Determine where docs should live.**

If existing docs directory was found in Phase 1, propose using it.

Otherwise, ask via AskUserQuestion:
```
Question: "Where should the docs live?"
Header: "Location"
Options:
  - label: "docs/"
    description: "Standard convention at the repo root"
  - label: "apps/docs/content/"
    description: "Monorepo convention — docs as a separate app"
```

For Fumadocs projects, check `source.config.ts` for the configured content directory and use that.

## Phase 6: Generation

### Reference & Feature (small scope)

Single-pass generation. No agents needed.

1. Use the templates from `${CLAUDE_PLUGIN_ROOT}/templates/doc-templates.md`
2. Read all source files identified in Phase 2
3. Generate documentation matching the validated style sample
4. Write files to the chosen location
5. If framework detected, generate sidebar config (meta.json, _meta.json, etc.)

### Full-Site (large scope)

**Spawn docs-writer agents in batches following `${CLAUDE_PLUGIN_ROOT}/disciplines/dispatching-parallel-agents.md`.**

1. **Prepare agent assignments.** Each outline section = one agent. Each agent gets:
   - Section name and description
   - List of source files to read (exact paths)
   - Audience: developer, user, or both
   - The validated style sample from Phase 4
   - Output format: `.md` or `.mdx`
   - Framework-specific instructions (sidebar config format, frontmatter requirements)
   - Output location

2. **Dispatch in batches of 2-3.**
   ```
   Batch 1: Agent → Features/Auth, Agent → Features/Billing
   Batch 2: Agent → API Reference, Agent → Architecture
   Batch 3: Agent → Components Reference, Agent → Getting Started
   ```

3. **Collect results.** Each agent returns file contents in delimiter format.

4. **Write files.** Create the directory structure and write each file.

## Phase 7: Consolidation (full-site only)

After all agents return:

1. **Terminology check** — Scan all generated docs for the same concept called different names. Standardize.
2. **Cross-reference check** — Verify all internal links (`[see auth](../features/auth.md)`) point to real files.
3. **Gap check** — Compare generated docs against the outline. Flag any missing sections.
4. **Fix issues** — Rewrite affected sections. Don't rewrite everything.

## Phase 8: Supporting Files

Generate supporting infrastructure:

**For plain markdown:**
- `README.md` — Index with links to all sections, using the full-site index template
- `getting-started.md` — Quick start guide (if full-site mode)

**For Fumadocs:**
- `meta.json` in each directory — sidebar ordering
- Root `index.mdx` — Landing page
- `getting-started.mdx` — Quick start guide (if full-site mode)

**For Nextra:**
- `_meta.json` in each directory

**For other frameworks:**
- Appropriate sidebar/navigation config

## Completion

Present what was generated:

```
Documentation generated:

Files: [N] docs written
Location: [path]
Format: [markdown / Fumadocs MDX / etc.]
Audience: [developer / user / both]

Sections:
- Getting Started
- Features: Auth, Billing, Notifications
- API Reference: Users, Orders
- Architecture: Overview
- Reference: Components, Utilities
```

Then offer next steps via AskUserQuestion:
```
Question: "What's next?"
Header: "Next step"
Options:
  - label: "Review the docs"
    description: "I'll walk through each section for your approval"
  - label: "Add more sections"
    description: "Document additional features or modules"
  - label: "Set up a docs framework"
    description: "Scaffold a docs site with /arc:implement to host these"
  - label: "Done"
    description: "Documentation is complete"
```
</process>

<integration>
## Integration with Other Skills

**Doc staleness detection:** `/arc:implement` checks for stale docs after completing work. If changed files have associated documentation, they prompt the user to update inline.

**Production readiness:** `/arc:letsgo` includes documentation coverage as a checklist item.

**Design context:** `/arc:ideate` reads existing docs to understand the current feature set.

**Framework scaffolding:** If the user wants a docs site (Fumadocs, etc.), route them to `/arc:implement` for the infrastructure. `/arc:document` generates content, not apps.
</integration>

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:document — [scope] ([audience]) [N files]`

Examples:
- `/arc:document — auth.ts reference (developer) 1 file`
- `/arc:document — auth feature guide (user) 3 files`
- `/arc:document — full site (both) 24 files`
</arc_log>

<success_criteria>
Documentation is complete when:
- [ ] Intent detected from user input (reference, feature, or full-site)
- [ ] Codebase scanned and findings shown to user
- [ ] Audience selected (developer, user, both)
- [ ] Framework detected (or plain markdown chosen)
- [ ] Sample section generated and style approved by user
- [ ] All documentation files written to chosen location
- [ ] Sidebar/navigation config generated (if framework detected)
- [ ] Index/README generated with links to all sections
- [ ] Cross-references verified (full-site only)
- [ ] User presented with completion summary and next steps
</success_criteria>
