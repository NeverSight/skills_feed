---
name: '@gw-autonomous-workflow'
description: Autonomous feature development workflow using isolated worktrees. Use this skill to autonomously implement features from task description through tested PR delivery. Handles worktree creation, implementation, testing, iteration, documentation, and PR creation. Triggers on requests for autonomous feature development, end-to-end implementation, or "implement X feature autonomously."
license: MIT
metadata:
  author: mthines
  version: '1.0.0'
  workflow_type: 'autonomous'
  min_agent_capability: 'code_execution,file_editing,git_operations'
  phases:
    - 'validation_questions'
    - 'intake_planning'
    - 'worktree_setup'
    - 'implementation'
    - 'testing_iteration'
    - 'documentation'
    - 'pr_creation'
    - 'cleanup'
---

# Autonomous Workflow - Complete Feature Delivery

Execute complete feature development cycles autonomously—from task intake through tested PR delivery—using isolated Git worktrees.

## Table of Contents

1. [Workflow Overview](#1-workflow-overview)
2. [Phase 0: Validation & Questions (MANDATORY)](#2-phase-0-validation--questions-mandatory)
3. [Phase 1: Task Intake & Planning](#3-phase-1-task-intake--planning)
4. [Phase 2: Worktree Setup (🔴 MANDATORY)](#4-phase-2-worktree-setup--mandatory)
5. [Phase 3: Implementation](#5-phase-3-implementation)
6. [Phase 4: Testing & Iteration](#6-phase-4-testing--iteration)
7. [Phase 5: Documentation](#7-phase-5-documentation)
8. [Phase 6: PR Creation & Delivery](#8-phase-6-pr-creation--delivery)
9. [Phase 7: Cleanup (Optional)](#9-phase-7-cleanup-optional)
10. [Decision Framework](#10-decision-framework)
11. [Error Recovery Procedures](#11-error-recovery-procedures)
12. [Safety Guardrails](#12-safety-guardrails)

---

## 🔴 CRITICAL REQUIREMENT: Isolated Worktree Development

**This skill ALWAYS creates a new isolated worktree before any code changes.**

Every autonomous execution follows this sequence:

1. Phase 0: Ask questions and validate requirements
2. Phase 1: Analyze codebase and plan approach
3. **Phase 2: Create new worktree with `gw add <branch-name>` (MANDATORY)**
4. Phase 3-7: All work happens in the isolated worktree

**Never skip worktree creation unless user explicitly requests it.**

This ensures:

- User's current work remains untouched
- True parallel development capability
- Clean rollback if needed
- Best practices with gw-tools

---

## 1. Workflow Overview

### What This Skill Does

This skill enables **autonomous execution** of complete feature development workflows:

1. **Validates requirements** through upfront questions
2. **Plans implementation** based on deep codebase analysis
3. **🔴 ALWAYS creates isolated worktree** using `gw add` (MANDATORY - see note below)
4. **Implements features** following existing patterns in the isolated worktree
5. **Tests iteratively** until all tests pass
6. **Documents changes** in relevant files
7. **Delivers draft PR** ready for human review

### 🔴 CRITICAL: Worktree Isolation is MANDATORY

**This workflow ALWAYS creates a new isolated worktree using `gw add` before any code changes.**

- ✅ **ALWAYS create worktree** - Every autonomous execution starts with `gw add <branch-name>`
- ✅ **Work in isolation** - All implementation happens in the new worktree, never in user's current directory
- ✅ **Parallel development** - User can continue working while you implement in isolated environment
- ❌ **NEVER skip worktree creation** - This is non-negotiable unless user explicitly says "work in current directory"

**Why this matters:**

- Preserves user's working state
- Enables true parallel development
- Provides clean rollback (just remove worktree)
- Follows gw-tools best practices

### When to Use This Skill

**Use this skill when:**

- User requests autonomous feature implementation
- Task has clear deliverable (feature, fix, refactor)
- Project uses gw-tools for worktree management (REQUIRED)
- Tests are available to validate correctness
- User wants work done in parallel/isolation from their current work

**Do NOT use this skill when:**

- User wants to code alongside you (use interactive mode)
- Task is exploratory research without clear deliverable
- Project doesn't use Git or gw-tools
- Changes affect critical production code without tests
- User explicitly says "work in current directory" or "don't create worktree"

### Expected Outcomes

**Successful execution produces:**

- ✅ New isolated worktree created with `gw add <branch-name>`
- ✅ Complete implementation in isolated worktree (user's work untouched)
- ✅ All tests passing (existing + new if applicable)
- ✅ Documentation updated (README, CHANGELOG, API docs)
- ✅ Draft PR with comprehensive description
- ✅ Clean commit history with conventional commits
- ✅ User can continue working in parallel during implementation

**If unable to complete:**

- ⚠️ Partial implementation committed with notes
- ⚠️ Clear explanation of blockers encountered
- ⚠️ Recommendations for next steps

### Autonomy Model

This workflow operates with **high autonomy after validation**:

1. **Phase 0 (Validation)**: Interactive - ask clarifying questions
2. **Phase 1 (Planning)**: Autonomous - analyze and plan approach
3. **Phase 2 (Worktree Setup)**: 🔴 MANDATORY - Always create isolated worktree with `gw add`
4. **Phase 3-6**: Autonomous - execute with continuous self-validation in isolated worktree
5. **Decision points**: Use decision framework, iterate until correct
6. **Blockers**: Report and deliver partial work with notes

**Non-negotiable requirement:** Phase 2 (worktree creation) must ALWAYS happen before Phase 3 (implementation).

---

## 2. Phase 0: Validation & Questions (MANDATORY)

### 🔴 CRITICAL: ALWAYS START HERE

**This phase is MANDATORY.** Never skip directly to implementation.

### Objectives

1. **Understand requirements completely** - No assumptions
2. **Identify ambiguities** - Surface edge cases early
3. **Validate scope** - Confirm what's in/out of scope
4. **Clarify acceptance criteria** - Define "done"
5. **Get explicit confirmation** - User approves understanding

### Procedure

```markdown
## Step 1: Parse User Request

Read the user's request carefully. Identify:

- Primary feature/fix being requested
- Mentioned technologies, files, or patterns
- Implied requirements (what's assumed but not stated)
- Missing information (what's unclear)

## Step 2: Analyze Codebase Context

Before asking questions, understand the project:

- Project structure (monorepo? single app?)
- Technology stack (framework, language, tools)
- Testing setup (unit, integration, e2e?)
- Documentation patterns (where docs live)
- Existing similar features (patterns to follow)

Use tools: nx_workspace, nx_project_details, Read, Glob, Grep

## Step 3: Formulate Clarifying Questions

Ask about:

**Requirements clarity:**

- "Should X feature also handle Y scenario?"
- "What should happen when Z edge case occurs?"

**Scope boundaries:**

- "Should this include tests/docs/migrations?"
- "Are we updating existing feature or adding new?"

**Technical decisions:**

- "Prefer approach A (simpler) or B (more flexible)?"
- "Follow pattern X from file.ts or pattern Y from other.ts?"

**Acceptance criteria:**

- "How will we know this is complete?"
- "What tests should pass?"

## Step 4: Present Understanding for Validation

Summarize your understanding:

"Based on your request, I understand:

1. Goal: [primary objective]
2. Scope: [what's included/excluded]
3. Approach: [technical approach]
4. Tests: [validation strategy]
5. Docs: [documentation updates]

Questions before proceeding:

- [Question 1]
- [Question 2]
- [Question 3]

Does this match your intent?"

## Step 5: Get Explicit Confirmation

Wait for user response. Do NOT proceed until:

- ✅ All questions answered
- ✅ Understanding validated
- ✅ Scope confirmed
- ✅ User explicitly says "proceed" or equivalent

If user clarifies/corrects:

- Update your understanding
- Re-validate if significant changes
- Confirm again before proceeding
```

### Example: Validation in Action

```markdown
User: "Add dark mode toggle to the app"

Agent (Phase 0):
"Let me understand this requirement before implementation.

Current analysis:

- Project: Next.js app with Tailwind CSS
- Existing: Light theme only
- Location: No theme infrastructure found

Clarifying questions:

1. **Scope**: Should dark mode apply globally or per-page?
2. **Persistence**: Save user preference (localStorage/cookie)?
3. **Default**: System preference or manual toggle?
4. **Components**: All pages or specific sections?
5. **Approach**: Prefer Tailwind dark: classes or CSS variables?
6. **Toggle UI**: Where should the toggle appear (navbar/settings)?

My proposed approach:

- Add theme context provider
- Use Tailwind dark: classes
- Save preference to localStorage
- System preference as default
- Toggle in navbar

Does this match your vision? Any preferences on the questions above?"

[Wait for user confirmation before proceeding to Phase 1]
```

### Validation Checklist

Before leaving Phase 0:

- [ ] User request fully understood
- [ ] All ambiguities clarified
- [ ] Scope explicitly confirmed
- [ ] Acceptance criteria defined
- [ ] Technical approach validated
- [ ] User gave explicit "proceed" signal

**If any checkbox is unchecked, DO NOT proceed to Phase 1.**

---

## 3. Phase 1: Task Intake & Planning

### Objectives

1. **Deep codebase analysis** - Understand existing patterns thoroughly
2. **Implementation strategy** - Plan detailed approach
3. **File identification** - Know exactly what to change
4. **Self-validation** - Review plan against requirements

### Procedure

```markdown
## Step 1: Analyze Codebase (Deep Dive)

### Project Structure

- Identify relevant directories/modules
- Map dependencies between components
- Locate configuration files

Tools: nx_workspace, nx_project_details, Glob

### Existing Patterns

- Find similar features already implemented
- Study code style, naming conventions
- Understand error handling patterns
- Review testing patterns

Tools: Grep (search for patterns), Read (study implementations)

### Technology Stack

- Framework version and features
- Build tools and configuration
- Testing framework and conventions
- Documentation format

### Dependencies

- Required packages already installed?
- Need to add new dependencies?
- Version compatibility considerations

## Step 2: Create Implementation Plan

Document your plan:

**Changes Required:**

1. File: `path/to/file1.ts`
   - Add: [specific additions]
   - Modify: [specific changes]
   - Reason: [why this change]

2. File: `path/to/file2.ts`
   - Add: [specific additions]
   - Reason: [why this change]

3. New file: `path/to/file3.ts`
   - Purpose: [what this does]
   - Exports: [public API]

**Testing Strategy:**

- Unit tests: [what to test]
- Integration tests: [if applicable]
- Manual validation: [if applicable]

**Documentation Updates:**

- README.md: [what to add/change]
- API docs: [if applicable]
- CHANGELOG: [entry to add]

**Risks & Mitigations:**

- Risk: [potential issue]
  Mitigation: [how to handle]

## Step 3: Self-Validation (Review Your Plan)

Ask yourself:

**Completeness:**

- Does this plan achieve all requirements from Phase 0?
- Are edge cases from user questions addressed?
- Is anything missing?

**Correctness:**

- Does this follow existing project patterns?
- Are dependencies and imports correct?
- Will this integrate cleanly?

**Testability:**

- Can this be validated with tests?
- Are test cases comprehensive?

**Maintainability:**

- Is this approach simple enough?
- Does it follow project conventions?
- Will other developers understand this?

## Step 4: Iteration Checkpoint

If self-validation reveals issues:

1. Refine the plan
2. Re-validate
3. Iterate until plan is solid

**Do NOT proceed to Phase 2 until plan is validated.**

## Step 5: Present Plan Summary (Optional)

For complex tasks, briefly summarize plan:

"Implementation plan:

- Modifying 3 files: [list]
- Adding 1 file: [list]
- Tests: [strategy]
- Docs: [updates]

Proceeding with Phase 2: Worktree setup."
```

### Planning Checklist

- [ ] Codebase deeply analyzed
- [ ] All relevant files identified
- [ ] Implementation approach defined
- [ ] Testing strategy clear
- [ ] Documentation scope identified
- [ ] Plan self-validated
- [ ] Ready to execute

---

## 4. Phase 2: Worktree Setup (🔴 MANDATORY - ALWAYS DO THIS FIRST)

### 🔴 CRITICAL: This Phase is MANDATORY Before Any Code Changes

**ALWAYS create a new isolated worktree before implementation. NEVER work in the user's current directory.**

This phase MUST be completed before Phase 3 (Implementation). Working in an isolated worktree:

- ✅ Preserves user's working state
- ✅ Enables parallel development
- ✅ Provides clean rollback capability
- ✅ Follows gw-tools best practices

**Only skip worktree creation if:**

- User explicitly says "work in current directory"
- User explicitly says "don't create worktree"

**In all other cases: CREATE THE WORKTREE FIRST.**

### Objectives

1. **Generate appropriate branch name** - Follow conventions
2. **🔴 Create isolated worktree** - Execute `gw add <branch-name>` (MANDATORY)
3. **Navigate to worktree** - Execute `gw cd <branch-name>`
4. **Install dependencies** - Ensure environment ready
5. **Validate setup** - Confirm everything works

### Procedure

````markdown
## Step 1: Generate Branch Name

Use decision framework (see Section 10):

**Pattern:** `<type>/<short-description>`

Types:

- `feat/` - New feature
- `fix/` - Bug fix
- `refactor/` - Code restructuring
- `docs/` - Documentation only
- `chore/` - Tooling, dependencies
- `test/` - Adding/fixing tests

Example: `feat/dark-mode-toggle`

## Step 2: Create Worktree

Execute:

```bash
gw add <branch-name>
```
````

**Validation:**

- Command succeeded?
- Worktree appears in `gw list`?
- Files present in new directory?

If fails, see Error Recovery (Section 11).

## Step 3: Navigate to Worktree

```bash
gw cd <branch-name>
```

**Validation:**

- `pwd` shows correct directory?
- `.git` symlink points to correct location?

## Step 4: Install Dependencies

Check if dependencies need installation:

- Does `package.json` exist?
- Is post-add hook configured?

If manual install needed:

```bash
npm install
# or
pnpm install
# or
yarn install
```

**Validation:**

- `node_modules/` directory exists?
- Key dependencies present?
- No installation errors?

## Step 5: Verify Environment

Run basic checks:

```bash
# TypeScript project
npm run build  # or tsc --noEmit

# Linting
npm run lint

# Tests (quick smoke test)
npm test -- --listTests  # Just list, don't run yet
```

**Validation:**

- No immediate errors?
- Build system works?
- Test framework found?

## Step 6: Sync Configuration (If Needed)

If project uses autoCopyFiles:

```bash
gw sync <branch-name>
```

**Validation:**

- `.env` copied (if configured)?
- Other config files synced?

````

### Setup Checklist

- [ ] Branch name follows conventions
- [ ] 🔴 Worktree created successfully with `gw add`
- [ ] 🔴 Currently in new worktree directory (verified with `pwd`)
- [ ] Dependencies installed in worktree
- [ ] Environment builds/compiles
- [ ] Configuration files synced
- [ ] Ready to implement in isolated environment

**If any of the 🔴 marked items are not checked, STOP and complete Phase 2 before proceeding.**

---

## 5. Phase 3: Implementation

### ⚠️ PREREQUISITE: Phase 2 (Worktree Setup) MUST be complete

**Before starting this phase, verify:**
- ✅ New worktree created with `gw add <branch-name>`
- ✅ Currently in the new worktree directory (check with `pwd`)
- ✅ Dependencies installed in worktree
- ✅ Environment validated (builds/compiles)

**If worktree not created yet, STOP and return to Phase 2.**

### Objectives

1. **Follow existing patterns** - Consistency with codebase
2. **Implement incrementally** - Small, focused changes in isolated worktree
3. **Validate continuously** - Self-check at every step
4. **Commit logically** - Meaningful commit messages

### Procedure

```markdown
## Step 1: Start with Foundation

Implement in logical order:
1. Types/interfaces (if TypeScript)
2. Core logic/functions
3. UI components (if applicable)
4. Integration/glue code
5. Configuration updates

## Step 2: Implement One Change at a Time

For each file change:

### Before Editing:
- Read existing file completely
- Understand current structure
- Identify insertion points
- Note existing patterns

### During Editing:
- Make focused change (one concern)
- Follow existing code style
- Maintain consistent formatting
- Add comments only if logic non-obvious
- Don't over-engineer

### After Editing:
**Immediate validation:**
```bash
# Does it compile?
npm run build  # or tsc --noEmit

# Does it pass linting?
npm run lint -- <file-path>
````

**Self-review questions:**

- Does this match existing patterns?
- Is naming consistent with codebase?
- Are imports organized correctly?
- Did I introduce any obvious bugs?
- Is this the simplest solution?

### Iterate if needed:

- Validation failed? Fix immediately
- Code feels wrong? Refine before proceeding
- Don't accumulate technical debt

## Step 3: Commit Incrementally

After each logical unit of work:

```bash
git add <changed-files>
git commit -m "<type>(<scope>): <description>"
```

**Conventional commit format:**

- `feat(ui): add dark mode toggle button`
- `feat(theme): implement theme context provider`
- `test(theme): add theme toggle unit tests`
- `docs(readme): document dark mode feature`

**Commit guidelines:**

- One logical change per commit
- Clear, descriptive messages
- Reference issues if applicable
- Keep commits atomic (can be reverted independently)

## Step 4: Continuous Self-Validation

After every 2-3 files changed:

**Checkpoint validation:**

```bash
# Full build
npm run build

# All lint rules
npm run lint

# Quick test run (if fast)
npm test -- --coverage=false --maxWorkers=1
```

**Self-assessment:**

- Is implementation on track?
- Any deviations from plan?
- Need to adjust approach?

**Iteration decision:**
If validation reveals issues:

1. Stop and analyze root cause
2. Fix the underlying problem
3. Re-validate
4. Continue only when solid

## Step 5: Integration Check

After all implementation changes:

**Final integration validation:**

- All files compile together?
- No TypeScript/lint errors?
- Imports resolve correctly?
- No circular dependencies?

**Manual testing (if applicable):**

- Start dev server
- Test feature manually
- Try edge cases from Phase 0
- Verify user requirements met

## Step 6: Pre-Testing Commit

Commit all implementation work:

```bash
git add .
git commit -m "feat(scope): implement <feature-name>

- Detail 1
- Detail 2
- Detail 3"
```

Now ready for formal testing (Phase 4).

````

### Implementation Checklist

- [ ] All planned files modified
- [ ] Code follows existing patterns
- [ ] Builds/compiles successfully
- [ ] Linting passes
- [ ] Commits are logical and clear
- [ ] Self-reviewed all changes
- [ ] Ready for testing

---

## 6. Phase 4: Testing & Iteration

### Objectives

1. **Run comprehensive tests** - Validate correctness
2. **Iterate aggressively** - Fix failures until passing
3. **Add new tests** - Cover new functionality
4. **Validate thoroughly** - Ensure quality

### Procedure

```markdown
## Step 1: Determine Test Strategy

Based on changes:

**Code changes require:**
- Unit tests for new functions/components
- Integration tests if multiple modules interact
- Regression tests for bug fixes

**UI changes require:**
- Component tests
- Visual regression tests (if available)
- Manual browser testing

**API changes require:**
- Endpoint tests
- Contract tests
- Error case coverage

## Step 2: Run Existing Tests

```bash
# Run full test suite
npm test

# Or specific tests if large codebase
npm test -- --testPathPattern="relevant"
````

**Expected outcomes:**

- ✅ All existing tests pass (no regressions)
- ❌ Some tests fail (expected if changing behavior)

## Step 3: Analyze Test Failures

For each failure:

### Understand the Failure:

- Read error message completely
- Identify which assertion failed
- Understand what was expected vs actual
- Trace back to root cause

### Categorize:

1. **Expected failure** - Behavior intentionally changed
   → Update test to match new behavior
2. **Regression** - Broke existing functionality
   → Fix implementation to preserve behavior
3. **Test infrastructure** - Test setup issue
   → Fix test configuration

### Prioritize:

- Critical failures first (core functionality)
- Edge cases later
- Flaky tests last (may be test issue)

## Step 4: Iterate Until Tests Pass

**Iteration loop (no hard limit):**

### Iteration 1:

1. Fix most obvious issues
2. Re-run tests
3. Validate: Did failures decrease?

### Iteration 2:

If still failing:

1. Re-analyze root cause (was first fix superficial?)
2. Try different approach
3. Re-run tests
4. Validate: Getting closer?

### Iteration 3+:

Keep iterating:

1. Consider alternative implementation
2. Review original plan (was approach wrong?)
3. Simplify if over-complicated
4. Ask: What would make tests pass?

**Continue until:**

- ✅ All tests passing, OR
- ⚠️ Identified blocker requiring user input

**Self-validation questions:**

- Are tests actually validating requirements?
- Are we testing the right things?
- Do tests cover edge cases from Phase 0?

## Step 5: Add New Tests (If Applicable)

If new functionality added:

```typescript
// Example: Testing new feature
describe('DarkModeToggle', () => {
  it('should toggle theme when clicked', () => {
    // Test new functionality
  });

  it('should persist preference to localStorage', () => {
    // Test persistence
  });

  it('should respect system preference on first load', () => {
    // Test edge case
  });
});
```

**New test requirements:**

- Cover main functionality
- Cover edge cases discussed in Phase 0
- Follow existing test patterns
- Use same testing utilities

**Validate new tests:**

```bash
# Run only new tests
npm test -- --testPathPattern="DarkModeToggle"
```

**Self-check:**

- Do new tests pass?
- Do they actually validate the feature?
- Are they maintainable?

## Step 6: Manual Validation (If Applicable)

For UI changes, use agent-browser:

```markdown
Objective: Validate dark mode toggle works correctly

Steps:

1. Start dev server (npm run dev)
2. Navigate to app (http://localhost:3000)
3. Locate dark mode toggle
4. Click toggle → verify theme changes
5. Refresh page → verify preference persisted
6. Test edge cases:
   - Different pages
   - Different components
   - System preference changes
```

## Step 7: Final Validation

All tests passing?

**Final checkpoint:**

```bash
# Clean test run
npm run test -- --coverage

# Check coverage (if requirements specified)
# Ensure new code has adequate coverage
```

**Self-assessment:**

- All requirements from Phase 0 validated?
- Edge cases tested?
- No regressions introduced?
- Tests are reliable (not flaky)?

## Step 8: Commit Test Changes

```bash
git add <test-files>
git commit -m "test(scope): add comprehensive tests for <feature>

- Unit tests for X
- Integration tests for Y
- Edge case coverage for Z"
```

````

### Testing Checklist

- [ ] Test strategy determined
- [ ] All existing tests pass
- [ ] Test failures analyzed and fixed
- [ ] New tests added (if applicable)
- [ ] Manual validation completed (if UI)
- [ ] Coverage adequate
- [ ] All requirements validated
- [ ] Ready for documentation

---

## 7. Phase 5: Documentation

### Objectives

1. **Identify documentation scope** - What needs updating
2. **Update relevant docs** - README, API docs, CHANGELOG
3. **Self-validate clarity** - Read as new user would
4. **Maintain style consistency** - Follow existing patterns

### Procedure

```markdown
## Step 1: Identify Documentation Needs

Based on changes:

**User-facing features:**
- README.md (usage examples)
- User guides
- Screenshots/demos

**API changes:**
- API documentation
- JSDoc/TSDoc comments
- OpenAPI/Swagger specs

**Configuration changes:**
- Config file documentation
- Environment variable docs
- Setup instructions

**Breaking changes:**
- CHANGELOG.md (highlight breaking changes)
- Migration guide

**All changes:**
- CHANGELOG.md entry

## Step 2: Update README (If Applicable)

Add usage examples:

```markdown
### Dark Mode

The app now supports dark mode! Toggle between light and dark themes:

#### Using the UI
Click the theme toggle in the navigation bar.

#### Programmatically
\```typescript
import { useTheme } from '@/contexts/ThemeContext';

function MyComponent() {
  const { theme, setTheme } = useTheme();

  // Toggle theme
  setTheme(theme === 'light' ? 'dark' : 'light');
}
\```

#### Default Behavior
- Respects system preference on first load
- Persists user preference to localStorage
- Falls back to light mode if preference unavailable
````

**Validation:**

- Read example as new user
- Is it clear how to use the feature?
- Are code examples correct?
- Is it easy to find?

## Step 3: Update API Documentation (If Applicable)

Document new APIs:

````typescript
/**
 * Theme context providing theme state and controls.
 *
 * @example
 * \```tsx
 * import { useTheme } from '@/contexts/ThemeContext';
 *
 * function MyComponent() {
 *   const { theme, setTheme } = useTheme();
 *   return <button onClick={() => setTheme('dark')}>Dark Mode</button>;
 * }
 * \```
 */
export function useTheme(): ThemeContextValue {
  // ...
}
````

**Validation:**

- Are all public APIs documented?
- Are examples realistic?
- Is return type clear?

## Step 4: Update CHANGELOG

Add entry following project convention:

```markdown
## [Unreleased]

### Added

- Dark mode toggle in navigation bar (#123)
  - Respects system preference
  - Persists user choice to localStorage
  - Applies theme globally

### Changed

- Theme context now exported from `@/contexts/ThemeContext`

### Fixed

- N/A
```

**Validation:**

- Entry describes user-facing changes?
- Includes relevant issue/PR numbers?
- Follows existing CHANGELOG format?

## Step 5: Update Other Documentation

Check for other docs needing updates:

- Configuration guides
- Architecture docs
- Team runbooks
- Troubleshooting guides

## Step 6: Self-Validation (Read as New User)

**Critical:** Read your own documentation with fresh eyes:

**Clarity check:**

- Can I understand this without context?
- Are examples self-contained?
- Is technical jargon explained?

**Completeness check:**

- Are all new features documented?
- Are edge cases explained?
- Are limitations mentioned?

**Accuracy check:**

- Do code examples actually work?
- Are paths/names correct?
- Is version info accurate?

**Iteration if needed:**

- Something confusing? Rewrite it
- Example unclear? Add more context
- Important detail missing? Add it

## Step 7: Commit Documentation

```bash
git add README.md CHANGELOG.md docs/
git commit -m "docs(feature): document dark mode toggle

- Add usage examples to README
- Update CHANGELOG with new feature
- Document theme context API"
```

````

### Documentation Checklist

- [ ] Documentation scope identified
- [ ] README updated (if applicable)
- [ ] API docs updated (if applicable)
- [ ] CHANGELOG entry added
- [ ] Code examples tested
- [ ] Self-validated for clarity
- [ ] Style consistent with project
- [ ] Ready for PR creation

---

## 8. Phase 6: PR Creation & Delivery

### 🎯 Final Deliverable: DRAFT Pull Request

**This phase creates a DRAFT PR, not a ready-to-merge PR.**

The PR will be marked as draft to signal:
- ✅ Implementation complete and tested
- ✅ Ready for human review
- ⚠️ Requires user approval before marking "ready for review"
- ⚠️ Not auto-mergeable - user must review and approve

### Objectives

1. **Pre-flight validation** - Ensure everything ready
2. **Push to remote** - Backup work
3. **Generate PR description** - Comprehensive summary
4. **🔴 Create DRAFT PR** - Always use `--draft` flag (MANDATORY)
5. **Report completion** - Deliver results to user with PR link

### Procedure

```markdown
## Step 1: Pre-Flight Validation

Final checks before delivery:

**All changes committed?**
```bash
git status  # Should show "nothing to commit, working tree clean"
````

**All tests passing?**

```bash
npm test  # Full test suite
```

**Builds successfully?**

```bash
npm run build  # Production build
```

**Linting clean?**

```bash
npm run lint  # All lint rules
```

**Documentation complete?**

- README updated? ✓
- CHANGELOG updated? ✓
- API docs updated? ✓

If ANY check fails:

1. Stop immediately
2. Fix the issue
3. Re-validate
4. Only proceed when everything passes

## Step 2: Push to Remote

```bash
# Push branch to remote
git push -u origin <branch-name>
```

**Validation:**

- Push succeeded?
- Branch visible on GitHub/GitLab?

## Step 3: Generate PR Description

Create comprehensive description:

```markdown
## Summary

[High-level overview of what this PR does]

## Changes

- [User-facing change 1]
- [User-facing change 2]
- [Technical change 3]

## Implementation Details

- Modified `file1.ts`: [what and why]
- Added `file2.ts`: [purpose]
- Updated `docs/`: [documentation changes]

## Testing

- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing completed
- [x] Edge cases validated

## Test Coverage

[Coverage stats if available]

## Screenshots (if UI changes)

[Attach screenshots or request user to add]

## Breaking Changes

[None / List breaking changes and migration path]

## Related Issues

Closes #[issue-number]
```

**Self-review:**

- Does this explain the PR clearly?
- Would a reviewer understand the context?
- Are all changes justified?

## Step 4: Create Draft PR

Use GitHub CLI:

```bash
gh pr create \
  --draft \
  --title "<type>(<scope>): <description>" \
  --body "$(cat <<'EOF'
[PR description from Step 3]
EOF
)"
```

**Example:**

```bash
gh pr create \
  --draft \
  --title "feat(ui): add dark mode toggle" \
  --body "$(cat <<'EOF'
## Summary
Implements dark mode toggle with theme persistence and system preference support.

## Changes
- Added theme context provider
- Created dark mode toggle component
- Implemented localStorage persistence
- Added comprehensive tests
- Updated documentation

## Implementation Details
- `src/contexts/ThemeContext.tsx`: Theme state management
- `src/components/ThemeToggle.tsx`: Toggle UI component
- `tailwind.config.js`: Dark mode configuration
- Tests: Full coverage of theme logic

## Testing
- [x] 15 new unit tests (100% coverage)
- [x] Manual testing in Chrome, Firefox, Safari
- [x] System preference detection validated
- [x] Persistence across page reloads confirmed

## Screenshots
[Will add in PR review]
EOF
)"
```

**Validation:**

- PR created successfully?
- Shows as draft?
- Description rendered correctly?

## Step 5: Report Completion to User

Deliver results:

```markdown
✅ **Feature implementation complete!**

**Delivered:**

- Branch: `feat/dark-mode-toggle`
- Worktree: `/path/to/worktree`
- Draft PR: https://github.com/user/repo/pull/123

**Summary:**

- Implemented dark mode toggle with theme persistence
- All tests passing (15 new tests, 100% coverage)
- Documentation updated (README + CHANGELOG)
- Ready for your review

**Next steps:**

1. Review the draft PR
2. Add screenshots if desired
3. Mark as ready for review when satisfied
4. Merge when approved

**Worktree cleanup:**
Run `gw remove feat/dark-mode-toggle` after PR is merged.
```

## Step 6: Preserve Worktree

**Do NOT remove worktree yet** - user may want to:

- Review changes locally
- Make adjustments
- Test manually
- Add screenshots

Worktree cleanup happens in Phase 7 (optional).

````

### Delivery Checklist

- [ ] Pre-flight validation passed
- [ ] All tests passing
- [ ] Branch pushed to remote
- [ ] PR description comprehensive
- [ ] Draft PR created
- [ ] PR link delivered to user
- [ ] Worktree preserved for review
- [ ] Workflow complete!

---

## 9. Phase 7: Cleanup (Optional)

### When to Use This Phase

**Run cleanup when:**
- PR has been merged
- PR has been closed/abandoned
- User explicitly requests cleanup
- Need to reclaim disk space

**Do NOT cleanup if:**
- PR still under review
- User hasn't reviewed changes yet
- Might need to iterate on PR

### Procedure

```markdown
## Step 1: Check PR Status

```bash
gh pr view <pr-number> --json state,mergedAt
````

**Safe to cleanup if:**

- State: MERGED
- State: CLOSED (and user confirms)

**NOT safe if:**

- State: OPEN
- User hasn't reviewed yet

## Step 2: Confirm with User (If Uncertain)

"The PR for <feature> is <state>. Should I remove the worktree to clean up disk space?"

Wait for confirmation.

## Step 3: Remove Worktree

```bash
# Safe removal (ensures committed/pushed)
gw remove <branch-name>
```

**Validation:**

- Worktree removed from `gw list`?
- Directory deleted?
- Git administrative cleanup done?

## Step 4: Navigate to Main

```bash
gw cd main
```

**Validation:**

- In main worktree now?
- Can continue other work?

## Step 5: Report Cleanup

"✅ Worktree cleaned up. Disk space reclaimed: ~X MB"

```

### Cleanup Checklist

- [ ] PR status checked
- [ ] Safe to remove worktree
- [ ] Worktree removed successfully
- [ ] Navigated to main
- [ ] User notified

---

## 10. Decision Framework

### Branch Naming Decisions

**Decision tree:**

```

Is this a new feature?
├─ Yes → `feat/<feature-name>`
└─ No ↓

Is this fixing a bug?
├─ Yes → `fix/<bug-description>`
└─ No ↓

Is this refactoring existing code?
├─ Yes → `refactor/<scope>`
└─ No ↓

Is this documentation only?
├─ Yes → `docs/<doc-name>`
└─ No ↓

Is this testing only?
├─ Yes → `test/<test-scope>`
└─ No ↓

Is this tooling/dependencies?
└─ Yes → `chore/<tool-name>`

```

**Examples:**
- `feat/dark-mode-toggle`
- `fix/login-validation-error`
- `refactor/api-client-structure`
- `docs/api-reference-update`
- `test/user-service-coverage`
- `chore/upgrade-typescript-5`

### Test Strategy Selection

**Decision tree:**

```

What changed?

Pure functions/utilities?
→ Unit tests (Jest/Vitest)
→ Coverage target: >80%

React components?
→ Component tests (Testing Library)
→ Test: rendering, interactions, props

API endpoints?
→ Integration tests (supertest)
→ Test: request/response, errors

Database operations?
→ Integration tests with test DB
→ Test: CRUD, transactions, constraints

UI interactions?
→ E2E tests (Playwright/Cypress)
→ Test: user flows, critical paths

Multiple systems interacting?
→ Integration tests
→ Test: data flow, error propagation

```

### Documentation Scope Determination

**Decision tree:**

```

What's the change?

New user-facing feature?
├─ README: Usage example
├─ CHANGELOG: Feature entry
└─ User guide: Detailed walkthrough

New API/function?
├─ JSDoc/TSDoc: API documentation
├─ README: Quick example
└─ API reference: Full details

Configuration change?
├─ Config docs: New options
├─ README: Updated setup
└─ Migration guide (if breaking)

Bug fix?
├─ CHANGELOG: Fixed entry
└─ Tests: Regression coverage

Internal refactoring?
└─ CHANGELOG: Technical note (optional)

```

### Iteration vs Delivery Decision

**When to iterate:**

```

Tests failing?
└─ Iterate (fix and retest)

Feature incomplete?
└─ Iterate (finish implementation)

Requirements unclear after starting?
└─ STOP and ask user (return to Phase 0)

Code doesn't follow patterns?
└─ Iterate (refactor to match)

Documentation insufficient?
└─ Iterate (improve docs)

```

**When to deliver partial work:**

```

Blocker requires user input?
├─ Commit what's done
├─ Document blocker
├─ Create draft PR with notes
└─ Ask user for help

External dependency unavailable?
├─ Implement what's possible
├─ Document missing piece
└─ Deliver with action items

Fundamental approach wrong?
├─ Stop implementation
├─ Explain issue to user
└─ Request new direction

````

**Never stop for:**
- Test failures (iterate until passing)
- Lint errors (fix immediately)
- Unclear code (refactor until clear)
- Missing docs (write them)

---

## 11. Error Recovery Procedures

### Worktree Creation Failures

**Error:** `gw add` fails

**Diagnosis:**
```bash
# Check git status
git status

# Check worktree list
git worktree list

# Check if branch already exists
git branch --list <branch-name>
````

**Recovery:**

```
Branch already exists?
├─ Use different branch name
└─ Or: Use existing branch (gw cd <branch>)

Permission error?
├─ Check directory permissions
└─ Try with sudo (if appropriate)

Disk space issue?
├─ Run: df -h
├─ Clean up: gw prune --clean
└─ Retry after space freed

Git error?
├─ Read error message carefully
├─ Fix underlying git issue
└─ Retry worktree creation
```

### Dependency Installation Failures

**Error:** `npm install` fails

**Diagnosis:**

```bash
# Check node version
node --version

# Check package manager
which npm pnpm yarn

# Check network
ping registry.npmjs.org

# Read error output carefully
```

**Recovery:**

```
Network error?
├─ Check internet connection
├─ Try different registry
└─ Use cached dependencies

Version incompatibility?
├─ Check node version requirements
├─ Switch node version (nvm)
└─ Update package.json if needed

Lock file mismatch?
├─ Delete lock file
├─ Delete node_modules
└─ Reinstall fresh

Disk space?
├─ Clean npm cache: npm cache clean --force
└─ Free disk space
```

### Test Failures During Iteration

**Error:** Tests fail after implementation

**Diagnosis:**

```bash
# Run single failing test with verbose output
npm test -- --testPathPattern="failing-test" --verbose

# Check test coverage
npm test -- --coverage

# Read stack trace completely
```

**Recovery approach:**

```markdown
## Iteration 1: Fix Obvious Issues

1. Read error message completely
2. Identify assertion that failed
3. Fix most likely cause
4. Rerun tests
5. Assess: Better or worse?

## Iteration 2: Deep Analysis

If still failing:

1. Add console.logs to understand state
2. Check assumptions about data/types
3. Verify mocks/stubs are correct
4. Fix root cause (not symptom)
5. Rerun tests

## Iteration 3: Alternative Approach

If still failing:

1. Question implementation approach
2. Review similar code in codebase
3. Consider simpler solution
4. Refactor if necessary
5. Rerun tests

## Iteration 4+: Systematic Debugging

1. Isolate minimal reproduction
2. Test each component independently
3. Verify test itself is correct
4. Consider test environment issues
5. Keep iterating until passing

## If Truly Stuck (rare):

1. Commit working code with failing test
2. Document exact failure and attempts
3. Ask user for guidance
```

**Never give up after fixed iterations** - iterate until tests pass or blocker identified.

### Merge Conflicts

**Error:** Merge conflict when pushing/rebasing

**Diagnosis:**

```bash
# Check conflict files
git status

# View conflicts
git diff
```

**Recovery:**

````markdown
## Step 1: Understand Conflicts

- Read both versions (HEAD vs incoming)
- Understand intent of each change
- Determine correct resolution

## Step 2: Resolve Conflicts

```bash
# Open conflicted files
# Edit to resolve conflicts (remove markers)
# Keep both changes if both needed
# Choose one if mutually exclusive
```
````

## Step 3: Test After Resolution

```bash
# Ensure code still works
npm run build
npm test
```

## Step 4: Complete Resolution

```bash
git add <resolved-files>
git commit  # Or git rebase --continue
```

## Step 5: Validate

- All conflicts resolved?
- Tests still pass?
- Code makes sense?

````

### Build Failures

**Error:** `npm run build` fails

**Diagnosis:**
```bash
# Read build output completely
npm run build 2>&1 | tee build.log

# Check TypeScript errors
npx tsc --noEmit

# Check for missing files
````

**Recovery:**

```
TypeScript error?
├─ Fix type issues
├─ Add missing types
└─ Update imports

Missing dependency?
├─ Install missing package
└─ Update imports

Path/import error?
├─ Check file locations
├─ Fix import paths
└─ Verify tsconfig paths

Config error?
├─ Review build config
├─ Check recent changes
└─ Restore working config
```

---

## 12. Safety Guardrails

### Validation Checkpoints

**Phase 0:** Mandatory validation before any work

- ✓ Requirements understood
- ✓ User confirmed understanding

**Phase 1:** Plan validated before implementation

- ✓ Plan matches requirements
- ✓ Approach is sound

**Phase 2:** 🔴 Worktree creation validated before ANY coding (MANDATORY)

- ✓ New worktree created with `gw add <branch-name>`
- ✓ Currently in worktree directory (verified with `pwd`)
- ✓ Dependencies installed in worktree
- ✓ Environment builds/compiles

**Phase 3:** Code validated during implementation (ONLY in worktree)

- ✓ Working in isolated worktree, not user's directory
- ✓ Builds after each file
- ✓ Self-review before commit

**Phase 4:** Tests validated before delivery

- ✓ All tests pass
- ✓ Requirements verified

**Phase 5:** Documentation validated for clarity

- ✓ Read as new user
- ✓ Examples tested

**Phase 6:** Everything validated before PR

- ✓ All checks passing
- ✓ Complete and ready

### Rollback Procedures

**If need to undo work:**

```bash
# Undo uncommitted changes
git checkout .

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Return to starting point
git reset --hard origin/main

# Remove worktree entirely
gw remove <branch-name> --force
```

### When to Stop and Ask

**Stop autonomous execution and ask user when:**

1. **Requirements ambiguous mid-implementation**
   - User's request wasn't clear enough
   - Edge case discovered not covered in Phase 0
   - Multiple valid approaches, unclear which to use

2. **Fundamental blocker encountered**
   - Required external service/API unavailable
   - Missing credentials/access
   - Architectural decision needed

3. **Scope creep detected**
   - Implementation expanding beyond original scope
   - Additional features seem necessary
   - Breaking changes not originally discussed

4. **Tests reveal misunderstanding**
   - Tests passing but not actually testing requirement
   - Requirements seem contradictory
   - Expected behavior unclear

5. **Resource/time limits approaching**
   - Already spent excessive time (>2 hours)
   - Many iterations without progress
   - Complexity greater than initially assessed

**How to ask:**

```markdown
"⚠️ Pausing autonomous execution - need guidance.

**Situation:**
[Describe what happened]

**Issue:**
[Explain the blocker/ambiguity]

**Options I see:**

1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]
3. [Option C] - [pros/cons]

**My recommendation:**
[Which option and why]

**Question:**
[Specific question for user]

Should I proceed with [recommended option] or would you prefer [alternative]?"
```

### Resource Limits

**Soft limits (guidelines, not hard stops):**

- **Commits:** ~3-10 per feature (logical grouping)
- **Files changed:** ~20 files max (if more, consider splitting)
- **Time:** ~1-2 hours (if longer, reassess approach)
- **Iterations:** No limit (iterate until correct)
- **Tests added:** Proportional to complexity

**Hard limits (stop and ask):**

- **>50 files changed** - Scope too large, split into multiple PRs
- **>3 hours stuck** - Fundamental issue, need user input
- **>100 commits** - Something wrong with approach
- **Breaking existing tests** - Don't disable tests, fix code or ask

### Quality Gates

**Before moving to next phase:**

- [ ] Previous phase checklist complete
- [ ] Self-validation passed
- [ ] No blocking errors
- [ ] Clear to proceed

**🔴 Before Phase 3 (Implementation) - CRITICAL GATE:**

- [ ] Phase 2 complete - worktree created with `gw add`
- [ ] Currently in worktree directory (run `pwd` to verify)
- [ ] NOT in user's original directory
- [ ] Dependencies installed in worktree
- [ ] Build system works in worktree

**If this gate fails, you MUST return to Phase 2 and create the worktree.**

**Before final delivery (Phase 6):**

- [ ] ALL tests passing
- [ ] Build succeeds
- [ ] Linting clean
- [ ] Documentation complete
- [ ] Self-reviewed all changes
- [ ] Requirements from Phase 0 met

**If any gate fails:**

1. Stop immediately
2. Identify root cause
3. Fix the issue
4. Re-validate
5. Only proceed when gate passes

---

## Summary

This autonomous workflow enables complete feature delivery through:

1. **✅ Phase 0 (MANDATORY):** Validate understanding upfront through questions
2. **📋 Phase 1:** Deep analysis and planning
3. **🔧 Phase 2 (🔴 MANDATORY):** Create isolated worktree with `gw add` - ALWAYS DO THIS
4. **💻 Phase 3:** Incremental implementation with continuous validation in isolated worktree
5. **🧪 Phase 4:** Aggressive iteration until all tests pass
6. **📚 Phase 5:** Clear, validated documentation
7. **🚀 Phase 6:** Comprehensive PR delivery
8. **🧹 Phase 7:** Safe cleanup when appropriate

**Key principles:**

- 🔴 **ALWAYS create isolated worktree first** (Phase 2 is mandatory)
- Always ask clarifying questions first (Phase 0)
- Work in isolation - never affect user's current directory
- Validate continuously, not just at the end
- Iterate until correct, no artificial limits
- Self-review every change immediately
- Deliver quality, not just speed
- Stop and ask when truly blocked

**Success metrics:**

- ✅ Requirements fully met
- ✅ All tests passing
- ✅ Documentation complete
- ✅ Clean commit history
- ✅ Draft PR ready for review

---

## Additional Resources

- [Complete Workflow Example](./examples/autonomous-workflow-complete.md)
- [Error Recovery Scenarios](./examples/error-recovery-scenarios.md)
- [Iterative Refinement Example](./examples/iterative-refinement.md)

---

_Part of the [gw-tools skills collection](../README.md)_
