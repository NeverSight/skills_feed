---
name: doc-update
description: Update and clean up project documentation files (primarily .ai/features/, but also README.md, PROGRESS_TRACKER.md, CLAUDE.md, and other .md files). Use when user requests documentation cleanup, organization, or updates for any feature, module, or project documentation (e.g., 'update photo viewer docs', 'clean up README', 'organize documentation'). Removes code snippets, outdated details, and redundant information while preserving essential architectural decisions and technical context.
---

# Documentation Update Skill

## Overview

This skill provides a systematic workflow for updating and cleaning up project documentation files. While primarily designed for feature documentation in `.ai/features/`, it works with any markdown documentation in the project including README.md, PROGRESS_TRACKER.md, CLAUDE.md, or documentation within code modules.

The skill removes verbose implementation details, code snippets, outdated information, and redundant content while preserving essential architectural decisions and technical context needed for future development.

It is particularly valuable for maintaining a lean, focused documentation set that provides maximum value without information overload.

## When to Use This Skill

Use this skill when the user requests documentation cleanup, updates, or organization for:
- **Feature documentation** in `.ai/features/` (primary use case)
- **Core documentation** (README.md, PROGRESS_TRACKER.md, CLAUDE.md)
- **Any markdown file** in the project that needs cleanup
- **Module or component documentation** that has become outdated

**Trigger phrases:**
- "update docs for X" / "zaktualizuj dokumentację X"
- "clean up X documentation" / "posprzątaj dokumentację X"
- "organize documentation" / "uporządkuj dokumentację"
- "condense X documentation" / "wyczyść dokumentację X"
- "remove outdated details from X"
- "update README" / "clean up PROGRESS_TRACKER"

## Documentation Update Workflow

Follow this 7-step workflow when updating feature documentation:

### Step 1: Identify the Documentation File

Extract the documentation target from the user's request and locate the corresponding file.

**Actions:**
- Identify target from user request:
  - Feature name → `.ai/features/feature-*.md` (e.g., "photo viewer" → `feature-photo-viewer.md`)
  - Core docs → `README.md`, `PROGRESS_TRACKER.md`, `CLAUDE.md`
  - Other files → Any `.md` file mentioned by user
- Locate file in project structure
- Confirm file exists, if not, ask user for clarification

**Examples:**
```
User: "Update photo viewer documentation"
→ Target: .ai/features/feature-photo-viewer.md

User: "Clean up README"
→ Target: README.md

User: "Posprzątaj PROGRESS_TRACKER"
→ Target: PROGRESS_TRACKER.md
```

### Step 2: Gather Context from Multiple Sources

Before making changes, gather comprehensive context about the feature's current state from multiple sources.

**Required Context Sources:**

1. **Feature File**: Read the target `.ai/features/feature-*.md` file
   - Current status markers
   - Implementation details
   - Completion dates

2. **PROGRESS_TRACKER.md**: Check feature status in project tracker
   - Is it in "Last Completed"?
   - Is it in "Currently Working On"?
   - Is it in "Opcjonalne Fazy (Post-MVP)"?

3. **Git History**: Check implementation progress
   ```bash
   # Find commits related to this feature
   git log --all --oneline --grep="feature-name"
   git log --all --oneline --grep="photo-viewer"

   # Check if feature branch exists or was merged
   git branch -a | grep -i feature-name
   ```

4. **Codebase**: Systematically search and analyze implementation

   **CRITICAL: This is NOT optional - you MUST perform thorough code search before updating docs!**

   a) **Search by keywords** (use Grep tool with multiple patterns):
   ```bash
   # Example for "photo-viewer" feature:
   grep -r "photo.?viewer" --ignore-case    # Find all variants
   grep -r "photoViewer"                     # camelCase
   grep -r "PhotoViewer"                     # PascalCase
   grep -r "photo_viewer"                    # snake_case
   ```

   b) **Identify key files** (use Glob tool to find all related files):
   - **Backend:** `*Controller.java`, `*Service.java`, `*Repository.java`, `*Entity.java`, `*DTO.java`
   - **Frontend:** `*.component.ts`, `*.service.ts`, `*.guard.ts`, `*.model.ts`, `*.html`
   - **Tests:** `*Test.java`, `*.spec.ts`, `*.e2e.ts`

   c) **Read key files** (use Read tool - NOT just "check if exists"):
   - Read main service/component implementation files
   - Check method signatures, class structure, dependencies
   - Identify integration points with other features
   - Note important fields, interfaces, DTOs

   d) **Create component inventory** (make a list while reading):
   - Backend: Package + Class names (e.g., `com.photomap.service.PhotoViewerService`)
   - Frontend: File paths + Component/Service names (e.g., `src/app/photo-viewer/photo-viewer.component.ts`)
   - Key interfaces/DTOs (e.g., `PhotoViewerDTO`, `PhotoMetadata`)
   - Important public methods (e.g., `extractExifData()`, `generateThumbnail()`)

   **Do not proceed to Step 3 until you have:**
   - ✅ Searched code with multiple grep patterns
   - ✅ Found all related files with Glob
   - ✅ Read (not just checked) key implementation files
   - ✅ Created inventory of file paths/packages/classes

5. **CLAUDE.md**: Review project conventions
   - Language preferences (Polish/English)
   - Documentation standards
   - Technical stack info

**Do not proceed until all context is gathered.**

### Step 3: Determine Implementation Status

Based on gathered context, classify the feature into one of these statuses:

- **✅ COMPLETED**: Fully implemented, tested, merged to main
- **⏳ IN-PROGRESS**: Actively being developed, mixed completion status
- **🔜 PLANNED**: Designed but not yet started
- **⏸️ PAUSED**: Started but temporarily on hold
- **🗑️ DEPRECATED**: No longer relevant or replaced

**Decision Matrix:**

| Indicator | Status |
|-----------|--------|
| Branch merged + all phases complete + in PROGRESS_TRACKER "Last Completed" | ✅ COMPLETED |
| Branch active + some phases complete + in "Currently Working On" | ⏳ IN-PROGRESS |
| No code + in "Post-MVP" section + only planning details | 🔜 PLANNED |
| Some code + explicit "paused" marker + in waiting state | ⏸️ PAUSED |
| Explicit deprecation notice or code removed | 🗑️ DEPRECATED |

**Reference:** See `references/feature-status-levels.md` for detailed status definitions.

### Step 4: Apply Appropriate Cleanup Level

Based on status determined in Step 3, apply the corresponding cleanup strategy.

#### For ✅ COMPLETED Features: Aggressive Cleanup

**Remove:**
- All code snippets and examples
- Detailed step-by-step implementation instructions
- Granular task checklists (convert to phase summaries)
- Time tracking and progress tables
- Verbose testing procedures
- Development history and commit logs
- "Currently Working On" sections
- Outdated "Next Steps"

**Keep:**
- Status section with completion date
- Architecture overview (high-level components)
- Key technical decisions with rationale
- Component/service names and responsibilities
- Integration points with other features
- API endpoints or public interfaces
- Important constraints or limitations
- Future enhancement considerations

**Target reduction:** 60-85% file size reduction

#### For ⏳ IN-PROGRESS Features: Moderate Cleanup

**Remove:**
- Outdated code snippets
- Completed phase details (summarize instead)
- Resolved blockers
- Obsolete implementation attempts
- Redundant information

**Keep:**
- Current phase details and tasks
- Next steps and planned work
- Active blockers or decisions needed
- Recent implementation notes
- Testing approach for current work
- All items from COMPLETED list

**Target reduction:** 40-60% file size reduction

#### For 🔜 PLANNED Features: Light Cleanup

**Remove:**
- Speculative code examples
- Over-detailed implementation plans
- Premature technical decisions
- Excessive alternative approaches (keep top 2-3)

**Keep:**
- Requirements and user stories
- High-level architecture proposals
- Technology evaluation (brief)
- Dependencies and prerequisites
- Estimated effort/complexity
- Integration points

**Target reduction:** 30-50% file size reduction

**Reference:** See `references/cleanup-guidelines.md` for detailed guidelines.

### Step 5: Update Status Section

Ensure the feature file has a clear, prominent status section at the top.

**Required Format:**

```markdown
# [Feature Name]

**Status:** [✅/⏳/🔜/⏸️/🗑️] [Description]
**Branch:** [branch-name] ([merged to main] or [active])
**Completed:** [YYYY-MM-DD] (for completed features)
**Last Updated:** [YYYY-MM-DD] (for in-progress features)

## Overview
[Brief 1-2 paragraph summary]
```

**Examples:**
```markdown
**Status:** ✅ Completed (2025-10-25)
**Branch:** `feature/photo-viewer` (merged to master)

**Status:** ⏳ In Progress - Phase 2 of 4
**Branch:** `feature/email-system`
**Last Updated:** 2025-11-03

**Status:** 🔜 Planned (Post-MVP)
**Estimated Effort:** 2-3 weeks
```

### Ensure "Key Components" Section Exists

**CRITICAL: Every feature documentation MUST include a "Key Components" section with file paths/package references.**

This section should be added immediately after the **Overview** section, containing ONLY references to code (NOT code snippets or implementation details).

**Required Format:**

```markdown
## Key Components

### Backend
| Path/Package | Description |
|--------------|-------------|
| `com.photomap.service.PhotoService` | Main service for photo CRUD operations, EXIF extraction |
| `com.photomap.controller.PhotoController` | REST endpoints: POST /api/photos, GET /api/photos/{id} |
| `com.photomap.entity.Photo` | JPA entity with geolocation fields (latitude, longitude) |
| `com.photomap.repository.PhotoRepository` | Spring Data JPA repository for Photo entity |

### Frontend
| Path/Component | Description |
|----------------|-------------|
| `src/app/photo-viewer/photo-viewer.component.ts` | Main component displaying photo with map integration |
| `src/app/services/photo.service.ts` | Manages photo state via BehaviorSubject, handles API calls |
| `src/app/models/photo.model.ts` | TypeScript interface for Photo with metadata |
```

**Rules for "Key Components" section:**

1. **Content Rules:**
   - ✅ Include file paths (e.g., `src/app/service/photo.service.ts`)
   - ✅ Include package names (e.g., `com.photomap.service.PhotoService`)
   - ✅ Include one-sentence description (5-15 words) explaining purpose
   - ✅ Optionally mention key public methods/endpoints
   - ❌ **NO code snippets or implementation details**
   - ❌ **NO method bodies or class internals**
   - ❌ **NO examples of usage**

2. **Source of Information:**
   - Use the component inventory created in Step 2.4 (Codebase search)
   - All components listed here MUST come from actual code found via Grep/Glob/Read
   - Do NOT guess or assume components - only list what was found in code

3. **Status-Specific Guidelines:**

   **For ✅ COMPLETED features:**
   - Keep full component list (this is the MAIN architectural reference!)
   - Remove code snippets from other sections, but KEEP this component list
   - This section is gold for future work - never remove it

   **For ⏳ IN-PROGRESS features:**
   - List implemented components (found in code)
   - List planned components with `(planned)` suffix
   - Example: `PhotoExportService (planned)` - Export photos to ZIP

   **For 🔜 PLANNED features:**
   - List proposed architecture components with `(proposed)` suffix
   - Example: `com.photomap.service.NotificationService (proposed)` - Email notifications

4. **Grouping:**
   - Group by Backend/Frontend (for full-stack features)
   - For backend-only: use `### Backend` section only
   - For frontend-only: use `### Frontend` section only

**Purpose of this section:**
- Enable Claude Code to quickly find related files when working on this feature
- Provide architectural overview without code clutter
- Serve as navigation reference for future development

### Step 6: Apply Project Language Policy

**CRITICAL: Check project's language policy in CLAUDE.md FIRST before deciding on documentation language.**

**Step-by-step process:**

1. **Check CLAUDE.md for language policy:**
   - Read CLAUDE.md in project root
   - Look for section about "Language and Communication" or "Documentation"
   - Check if there's explicit policy about documentation language

2. **Apply appropriate rule:**

   **A) If CLAUDE.md specifies documentation language:**
   - ✅ Use the language specified in CLAUDE.md
   - Example: `Documentation: English (all .md files)` → Convert to English
   - Example: `Dokumentacja: Polski` → Convert to Polish
   - **This overrides the original document language**

   **B) If NO language policy in CLAUDE.md:**
   - ✅ Preserve the original language of the document
   - Polish document → Keep in Polish
   - English document → Keep in English
   - Mixed document → Ask user which to standardize to

   **C) If user explicitly requests translation:**
   - ✅ Use the language user requested
   - **This overrides CLAUDE.md and original language**

**Priority order:**
1. User's explicit request (highest)
2. CLAUDE.md language policy
3. Original document language (lowest)

**Example workflows:**

```
Scenario 1: Project with English policy
- CLAUDE.md says: "Documentation: English (all .md files)"
- Current doc: Polish
- Action: Convert to English

Scenario 2: Project without policy
- CLAUDE.md: No language policy specified
- Current doc: Polish
- Action: Keep in Polish

Scenario 3: User explicit request
- User says: "Update docs and translate to Polish"
- CLAUDE.md says: "Documentation: English"
- Action: Translate to Polish (user request overrides policy)

Scenario 4: No policy, mixed language doc
- CLAUDE.md: No language policy
- Current doc: Mixed Polish/English
- Action: Ask user which language to standardize to
```

### Step 7: Review with User Before Committing

**NEVER make documentation changes without user review.**

**Review Process:**
1. Make all changes to the file
2. Show user a summary of changes:
   - Original file size vs new file size
   - Key sections removed
   - Key sections kept
   - Status classification used
3. Optionally show git diff for detailed review
4. Ask: "Czy zatwierdzić te zmiany w dokumentacji?"
5. Wait for explicit confirmation
6. Only after YES → stage and commit changes

**Review Checklist - verify BEFORE showing summary to user:**

Before presenting the review summary, verify that all required steps were completed:

✅ **Code verification performed (Step 2.4):**
   - [ ] Grep search executed with multiple patterns (camelCase, PascalCase, snake_case)
   - [ ] Key files identified with Glob tool
   - [ ] Key files **read** with Read tool (not just checked for existence)
   - [ ] Component inventory created (file paths, packages, class names)

✅ **Documentation completeness:**
   - [ ] "Key Components" section exists in the updated documentation
   - [ ] All components from Step 2.4 inventory are listed in "Key Components"
   - [ ] Full file paths used (frontend) and package names (backend)
   - [ ] Descriptions are concise (5-15 words) and accurate
   - [ ] Section contains ONLY references (no code snippets or implementation details)

✅ **Status accuracy:**
   - [ ] Status classification matches git history + PROGRESS_TRACKER
   - [ ] Completion date accurate (for ✅ COMPLETED features)
   - [ ] Branch status verified (merged/active)

✅ **Cleanup level appropriate:**
   - [ ] COMPLETED: Removed 60-85% (kept architecture + decisions + Key Components)
   - [ ] IN-PROGRESS: Removed 40-60% (kept current work + Key Components)
   - [ ] PLANNED: Removed 30-50% (kept requirements + Key Components)

**⚠️ If ANY checklist item is NOT checked - DO NOT proceed to user review. Go back and complete missing steps first.**

**Example Review Summary:**
```
Zaktualizowałem dokumentację feature-photo-viewer.md:

Zmiany:
- Usunięto szczegółowe checklisty zadań (150 linii)
- Usunięto fragmenty kodu (80 linii)
- Usunięto verbose testing procedures (60 linii)
- Zachowano architekturę i kluczowe decyzje techniczne
- Zachowano Future Considerations

Status: ✅ COMPLETED
Rozmiar: 478 linii → 85 linii (82% redukcja)

Czy zatwierdzić te zmiany w dokumentacji?
```

## Resources

This skill includes reference documentation in the `references/` directory:

### references/cleanup-guidelines.md
Detailed guidelines for what to keep and remove for each implementation status. Includes specific examples and strategies for condensing different types of content.

**Read this when:** You need specific guidance on what to remove or keep for a particular status level.

### references/feature-status-levels.md
Comprehensive definitions of all implementation statuses (COMPLETED, IN-PROGRESS, PLANNED, etc.) with indicators and classification criteria.

**Read this when:** You're unsure how to classify a feature's status or need to understand status transitions.

### references/examples.md
Before/after examples of documentation transformations for different statuses, showing actual file size reductions and specific changes made.

**Read this when:** You want to see concrete examples of the cleanup process or validate your approach.

## Important Reminders

1. **Always gather full context** - Don't rely on the feature file alone
2. **Systematically search codebase** - Use Grep/Glob/Read tools to find all related components
3. **Include Key Components section** - Always add file paths/packages for quick reference
4. **Be aggressive with COMPLETED features** - Remove 60-85% of content
5. **Preserve technical decisions** - These are gold for future work
6. **Apply project language policy** - Check CLAUDE.md first, then user request, then preserve original
7. **Always review with user** - Never auto-commit documentation changes
8. **Use references liberally** - Refer to cleanup-guidelines.md for specific guidance

## Quick Reference

| Status | Cleanup Level | Target Reduction | Key Focus |
|--------|---------------|------------------|-----------|
| ✅ COMPLETED | Aggressive | 60-85% | Architecture + decisions |
| ⏳ IN-PROGRESS | Moderate | 40-60% | Current work + context |
| 🔜 PLANNED | Light | 30-50% | Requirements + why |
| ⏸️ PAUSED | Moderate | 40-60% | Context for resume |
| 🗑️ DEPRECATED | Minimal | Archive | Historical reference |

## Common Pitfalls to Avoid

- ❌ Removing all technical decisions (these are crucial!)
- ❌ Deleting integration points (needed for related work)
- ❌ Auto-translating without user request
- ❌ Committing without user review
- ❌ Being too conservative with COMPLETED features
- ❌ Removing current context from IN-PROGRESS features
- ❌ Keeping speculative code in PLANNED features
