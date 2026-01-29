---
name: claude-md-master
description: Master skill for CLAUDE.md lifecycle - create, update, improve with repo-verified content and multi-module support. Use when creating or updating CLAUDE.md files.
---

# CLAUDE.md Master (Create/Update/Improver)

## When to use
- User asks to create, improve, update, or standardize CLAUDE.md files.

## Core rules
- Only include info verified in repo or config.
- Never include secrets, tokens, credentials, or user data.
- Never include task-specific or temporary instructions.
- Keep concise: root <= 200 lines, module <= 120 lines.
- Use bullets; avoid long prose.
- Commands must be copy-pasteable and sourced from repo docs/scripts/CI.
- Skip empty sections; avoid filler.

## Mandatory inputs (analyze before generating)
- Build/package config relevant to detected stack (root + modules).
- Static analysis config used in repo (if present).
- Actual module structure and source patterns (scan real dirs/files).
- Representative source roots per module to extract:
  package/feature structure, key types, and annotations in use.

## Discovery (fast + targeted)
1. Locate existing CLAUDE.md variants: `CLAUDE.md`, `.claude.md`, `.claude.local.md`.
2. Identify stack and entry points via minimal reads:
   - `README.md`, relevant `docs/*`
   - Build/package files (see stack references)
   - Runtime/config: `Dockerfile`, `docker-compose.yml`, `.env.example`, `config/*`
   - CI: `.github/workflows/*`, `.gitlab-ci.yml`, `.circleci/*`
3. Extract commands only if they exist in repo scripts/config/docs.
4. Detect multi-module structure:
   - Android/Gradle: read `settings.gradle` or `settings.gradle.kts` includes.
   - iOS: detect multiple targets/workspaces in `*.xcodeproj`/`*.xcworkspace`.
   - If more than one module/target has `src/` or build config, plan module CLAUDE.md files.
5. For each module candidate, read its build file + minimal docs to capture
   module-specific purpose, entry points, and commands.
6. Scan source roots for:
   - Top-level package/feature folders and layer conventions.
   - Key annotations/types in use (per stack reference).
   - Naming conventions used in the codebase.
7. Capture non-obvious workflows/gotchas from docs or code patterns.

Performance:
- Prefer file listing + targeted reads.
- Avoid full-file reads when a section or symbol is enough.
- Skip large dirs: `node_modules`, `vendor`, `build`, `dist`.

## Stack-specific references (Pattern 2)
Read the relevant reference only when detection signals appear:
- Android/Gradle → `references/android.md`
- iOS/Xcode/Swift → `references/ios.md`
- PHP → `references/php.md`
- Go → `references/go.md`
- React (web) → `references/react-web.md`
- React Native → `references/react-native.md`
- Rust → `references/rust.md`
- Python → `references/python.md`
- Java/JVM → `references/java.md`
- Node tooling → `references/node.md`
- .NET/C# → `references/dotnet.md`
- Dart/Flutter → `references/flutter.md`
- Ruby/Rails → `references/ruby.md`
- Elixir/Erlang → `references/elixir.md`
- C/C++/CMake → `references/cpp.md`
- Other/Unknown → `references/generic.md` (fallback when no specific reference matches)

If multiple stacks are detected, read multiple references.
If no stack is recognized, use the generic reference.

## Multi-module output policy (mandatory when detected)
- Always create a root `CLAUDE.md`.
- Also create `CLAUDE.md` inside each meaningful module/target root.
  - "Meaningful" = has its own build config and `src/` (or equivalent).
  - Skip tooling-only dirs like `buildSrc`, `gradle`, `scripts`, `tools`.
- Module file must be module-specific and avoid duplication:
  - Include purpose, key paths, entry points, module tests, and module
    commands (if any).
  - Reference shared info via `@/CLAUDE.md`.

## Business module CLAUDE.md policy (all stacks)
For monorepo business logic directories (`src/`, `lib/`, `packages/`, `internal/`):
- Create `CLAUDE.md` for modules with >5 files OR own README
- Skip utility-only dirs: `Helper`, `Utils`, `Common`, `Shared`, `Exception`, `Trait`, `Constants`
- Layered structure not required; provide module info regardless of architecture
- Max 120 lines per module CLAUDE.md
- Reference root via `@/CLAUDE.md` for shared architecture/patterns
- Include: purpose, structure, key classes, dependencies, entry points

## Mandatory output sections (per module CLAUDE.md)
Include these sections if detected in codebase (skip only if not present):
- **Feature/component inventory**: list top-level dirs under source root
- **Core/shared modules**: utility, common, or shared code directories
- **Navigation/routing structure**: navigation graphs, routes, or routers
- **Network/API layer pattern**: API clients, endpoints, response wrappers
- **DI/injection pattern**: modules, containers, or injection setup
- **Build/config files**: module-specific configs (proguard, manifests, etc.)

See stack-specific references for exact patterns to detect and report.

## Update workflow (must follow)
1. Propose targeted additions only; show diffs per file.

2. Ask for approval before applying updates:

**Cursor IDE:**
Use the AskQuestion tool with these options:
- id: "approval"
- prompt: "Apply these CLAUDE.md updates?"
- options: [{"id": "yes", "label": "Yes, apply"}, {"id": "no", "label": "No, cancel"}]

**Claude Code (Terminal):**
Output the proposed changes and ask:
"Do you approve these updates? (yes/no)"
Stop and wait for user response before proceeding.

**Other Environments (Fallback):**
If no structured question tool is available:
1. Display proposed changes clearly
2. Ask: "Do you approve these updates? Reply 'yes' to apply or 'no' to cancel."
3. Wait for explicit user confirmation before proceeding

3. Apply updates, preserving custom content.

If no CLAUDE.md exists, propose a new file for approval.

## Content extraction rules (mandatory)
- From codebase only:
  - Extract: type/class/annotation names used, real path patterns,
    naming conventions.
  - Never: hardcoded values, secrets, API keys, business-specific logic.
  - Never: code snippets in Do/Do Not rules.

## Verification before writing
- [ ] Every rule references actual types/paths from codebase
- [ ] No code examples in Do/Do Not sections
- [ ] Patterns match what's actually in the codebase (not outdated)

## Content rules
- Include: commands, architecture summary, key paths, testing, gotchas, workflow quirks.
- Exclude: generic best practices, obvious info, unverified statements.
- Use `@path/to/file` imports to avoid duplication.
- Do/Do Not format is optional; keep only if already used in the file.
- Avoid code examples except short copy-paste commands.

## Existing file strategy
Detection:
- If `<!-- Generated by claude-md-editor skill -->` exists → subsequent run
- Else → first run

First run + existing file:
- Backup `CLAUDE.md` → `CLAUDE.md.bak`
- Use `.bak` as a source and extract only reusable, project-specific info
- Generate a new concise file and add the marker

Subsequent run:
- Preserve custom sections and wording unless outdated or incorrect
- Update only what conflicts with current repo state
- Add missing sections only if they add real value

Never modify `.claude.local.md`.

## Output
After updates, print a concise report:
```
## CLAUDE.md Update Report
- /CLAUDE.md [CREATED | BACKED_UP+CREATED | UPDATED]
- /<module>/CLAUDE.md [CREATED | UPDATED]
- Backups: list any `.bak` files
```

## Validation checklist
- Description is specific and includes trigger terms
- No placeholders remain
- No secrets included
- Commands are real and copy-pasteable
- Report-first rule respected
- References are one level deep
