---
name: micro-commit
description: Split git changes into context-based micro-commits
user-invocable: true
---

This approach is inspired by **Lucas Rocha's micro-commit** methodology, which emphasizes breaking down changes into small, logical, and independently meaningful commits.

## Core Guidelines

Before starting any task, read and follow `/key-guidelines`

---

Commits unstaged changes by grouping them into logical micro-commits using the git-operations-specialist skill.

## Dependencies

- use git-operations-specialist skill

## Instructions

**IMPORTANT: Use the git-operations-specialist skill (via Skill tool) for ALL git-related operations in this command.**

Analyze all unstaged changes and execute multiple micro-commits, grouping related changes together.

### Required Execution Items

1. **Check Current Status**: Run `git status` to identify all unstaged changes

2. **Group Changes by Context**: Analyze the changes and group them logically:
   - **By File Type**: Group similar file types (e.g., all TypeScript files, all config files)
   - **By Feature**: Group files that implement the same feature
   - **By Layer**: Group by architectural layer (e.g., API changes, frontend changes, database changes)
   - **By Purpose**: Group by purpose (e.g., new features, bug fixes, refactoring, configuration)

3. **Create Micro-Commits**: For each logical group:
   - Stage only the files in that group using `git add`
   - Create a focused commit with a clear message
   - Verify the commit was successful

4. **Commit Message Guidelines**:
   - Follow the `.gitmessage` template format
   - Use appropriate commit type prefixes: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`
   - Each commit should describe ONE logical change

5. **Final Verification**: After all commits, run `git status` to confirm no changes remain unstaged

### ⚠️ Important Constraints
- **Stage files explicitly** - Use `git add <file>` for each group before committing
- **Use HEREDOC** - Maintain proper formatting of commit messages
- **One Context Per Commit** - Each commit should represent a single logical change
- **Sequential Processing** - Process one group at a time, verifying each commit before moving to the next

### Example Grouping Strategy

If you have changes to:
- `apps/api/src/routes/timeline.ts` (API logic)
- `apps/dashboard/src/types/api.ts` (Type definitions)
- `apps/dashboard/src/components/TimelineVisjs.tsx` (UI component)
- `apps/api/tsconfig.json` (Configuration)

Group them as:
1. **Commit 1**: API logic changes (`apps/api/src/routes/timeline.ts`)
2. **Commit 2**: Type definitions (`apps/dashboard/src/types/api.ts`)
3. **Commit 3**: UI component changes (`apps/dashboard/src/components/TimelineVisjs.tsx`)
4. **Commit 4**: Configuration changes (`apps/api/tsconfig.json`)
