---
name: lessons-learned
description: Helps AI agents learn from mistakes by capturing lessons in a structured format and syncing them to AGENTS.md or CLAUDE.md. Use when errors occur, tasks fail repeatedly, or complex tasks complete. AI suggests creating lessons; user confirms before writing.
license: MIT
metadata:
  author: shihyuho
  version: "1.1.0"
---

# Lessons Learned

A skill for AI agents to capture and learn from mistakes, preventing repeated errors through structured documentation and knowledge base integration.

## Overview

This skill enables AI agents to:
- Recognize situations where lessons should be captured
- Suggest creating lesson entries at appropriate moments
- Maintain a structured knowledge base of past mistakes and solutions
- Automatically review relevant lessons before starting similar tasks

**Key principle**: Learn once, avoid forever.

## When to Trigger

AI should suggest creating a lesson-learned entry in these situations:

### 1. After Task Failure or Error
When an error occurs that could have been prevented with prior knowledge.

**Example triggers**:
- Type errors or runtime exceptions
- Configuration mistakes
- API integration issues
- Logic errors discovered during testing

### 2. After Multiple Retry Attempts
When the same issue requires 2+ attempts to resolve.

**Example triggers**:
- Repeated failures on the same operation
- Multiple iterations to get syntax correct
- Back-and-forth on approach or implementation

### 3. After Unexpectedly Complex Tasks
When a task that seemed simple turns out to be more complex than anticipated.

**Example triggers**:
- Simple feature requires significant refactoring
- Edge cases emerge that weren't obvious upfront
- Dependencies or side effects were underestimated

### 4. User Explicit Request
When the user directly asks to document a lesson.

**Example**:
- "Let's document this for next time"
- "Create a lesson-learned entry"
- "We should remember this"

## Workflow

### Step 1: Detect Trigger Condition

Monitor for the trigger situations listed above during task execution.

### Step 2: Suggest Creating Lesson

When a trigger is detected, **ask the user for confirmation** before proceeding:

**Template**:
```
I noticed [specific situation that triggered this].
This could be valuable to document as a lesson-learned entry.

Would you like me to create a lesson file and update the lessons index file?
```

**Examples**:
```
I noticed we hit the same async/await issue twice in this session.
This could be valuable to document as a lesson-learned entry.

Would you like me to create a lesson file and update the lessons index file?
```

```
I noticed this type safety issue required multiple attempts to resolve.
This could be valuable to document as a lesson-learned entry.

Would you like me to create a lesson file and update the lessons index file?
```

### Step 3: Wait for User Confirmation

**Do not proceed without explicit user confirmation.**

Valid confirmations:
- "Yes"
- "Sure"
- "Go ahead"
- "Please do"
- Any affirmative response

If user declines or doesn't respond clearly, do not create the lesson.

### Step 4: Create Lesson File

If user confirms, create a new lesson file following these specifications:

**Location**: `docs/lessons/YYYY-MM-DD-topic-slug.md` (in the project root)

- If `docs/lessons/` does not exist, create it first.

**Naming convention**:
- Use current date: `YYYY-MM-DD`
- Use lowercase kebab-case for topic slug
- Keep slug concise (2-4 words)
- Examples:
  - `docs/lessons/2026-02-06-async-await-loops.md`
  - `docs/lessons/2026-02-08-type-guard-usage.md`
  - `docs/lessons/2026-02-10-state-mutation.md`

**Content format**: Use the template from `references/LESSON_TEMPLATE.md`

**Word limit**: Keep total content between 200-300 words. Be concise and actionable.

### Step 5: Update Lessons Index File

**Immediately after creating or updating a lesson file**, update the project's lessons index file.

**Index file selection rules** (required order):
1. If `AGENTS.md` exists, use `AGENTS.md`.
2. Else if `CLAUDE.md` exists, use `CLAUDE.md`.
3. Else ask the user which file to use (`AGENTS.md` or `CLAUDE.md`) and wait for an explicit choice.

**Location in the selected index file**:
- If the selected file does not exist yet, create it.
- Find or create a `## Lessons Learned` section.

**Format** (required order):
```markdown
## Lessons Learned

Quick reference to past mistakes and how to avoid them. For any similar task, the AI MUST read the relevant linked lesson file(s) before proceeding.

- [One-line summary of the lesson](docs/lessons/YYYY-MM-DD-topic-slug.md)
```

**Mandatory formatting rule**:
- The policy sentence above is required and must appear directly under `## Lessons Learned`.
- If the section already exists with only list items, insert this policy sentence before the first list item.
- If an entry for the same lesson path already exists, update that line instead of adding a duplicate.
- Do not update both files unless the user explicitly requests it.
- Do not treat the sentence as optional prose.

**Example**:
```markdown
## Lessons Learned

Quick reference to past mistakes and how to avoid them. For any similar task, the AI MUST read the relevant linked lesson file(s) before proceeding.

- [Avoid await in loops - use Promise.all for parallel async operations](docs/lessons/2026-02-06-async-await-loops.md)
- [Use type guards instead of type assertions for runtime safety](docs/lessons/2026-02-08-type-guard-usage.md)
- [Never mutate state directly - always create new objects](docs/lessons/2026-02-10-state-mutation.md)
```

The same structure applies if the selected file is `CLAUDE.md`.

**Summary guidelines**:
- One sentence, up to 30 words.
- Include both the mistake and the solution
- Use imperative mood (command form)
- Focus on actionable guidance

### Step 6: Confirm Completion

After creating both files, inform the user:

```
✓ Created lesson: docs/lessons/YYYY-MM-DD-topic-slug.md
✓ Updated <AGENTS.md|CLAUDE.md> with lesson reference

The lesson is now part of the project knowledge base.
```

## Mandatory Lesson Review

Before starting any task, AI **must**:

1. Determine the lessons index file using the same selection rules as Step 5
2. Check whether the selected file contains a `## Lessons Learned` section
3. If yes, scan the lesson summaries
4. Identify lessons relevant to the current task domain
5. Read the full content of relevant lessons
6. Apply the guidance from those lessons

**Relevance criteria**:
- Same technology/framework mentioned
- Similar operation or pattern (async, state management, API calls, etc.)
- Same category of issue (type safety, performance, error handling, etc.)

**Example**:
```
Task: Implement data fetching in React component
Relevant lessons to review:
- docs/lessons/2026-02-06-async-await-loops.md (async operations)
- docs/lessons/2026-02-15-react-useeffect-deps.md (React data fetching)

[AI reads these lessons before proceeding with implementation]
```

## File Structure

### Project-Level Files (Created in User's Project)

```
project/
├── AGENTS.md or CLAUDE.md             # Lessons index file (selected by rules)
└── docs/lessons/                      # Lessons directory
    ├── 2026-02-06-async-await-loops.md
    ├── 2026-02-08-type-guard-usage.md
    └── ...
```

### Lesson File Template

See `references/LESSON_TEMPLATE.md` for the complete template.

**Structure**:
```markdown
# [Brief Title]

**Date**: YYYY-MM-DD
**Context**: [One-line description]

## What Went Wrong

[Description of the mistake or issue]

## How to Avoid

[Concrete steps to prevent this in the future]
```

## Best Practices

### For AI Agents

1. **Be proactive but not intrusive** - Suggest lessons when valuable, but don't over-suggest
2. **Wait for confirmation** - Never create files without user approval
3. **Keep it concise** - Respect the 200-300 word limit
4. **Make it actionable** - Focus on "how to avoid" rather than lengthy explanations
5. **Review before acting** - Always check existing lessons before similar tasks

### For Users

1. **Be selective** - Not every mistake needs a lesson, focus on recurring issues
2. **Review periodically** - Scan the selected index file's `## Lessons Learned` section occasionally
3. **Update when needed** - If a lesson becomes outdated, update or remove it
4. **Share with team** - Commit lessons to version control for team benefit

## Examples

### Example 1: Async/Await in Loops

**Trigger**: Task required 3 attempts to fix performance issue

**AI Suggestion**:
```
I noticed we had to refactor this code multiple times due to async/await 
performance issues in loops. This could be valuable to document.

Would you like me to create a lesson-learned entry?
```

**Created Files**:
- `docs/lessons/2026-02-06-async-await-loops.md`
- Updated `<AGENTS.md|CLAUDE.md>` with: `[Avoid await in loops - use Promise.all for parallel async operations](docs/lessons/2026-02-06-async-await-loops.md)`

### Example 2: Type Safety Issue

**Trigger**: Type error caused runtime exception

**AI Suggestion**:
```
I noticed this type assertion caused a runtime error that could have been 
caught with proper type guards. Worth documenting?

Would you like me to create a lesson-learned entry?
```

**Created Files**:
- `docs/lessons/2026-02-08-type-guard-usage.md`
- Updated `<AGENTS.md|CLAUDE.md>` with: `[Use type guards instead of type assertions for runtime safety](docs/lessons/2026-02-08-type-guard-usage.md)`

## Integration with AGENTS.md / CLAUDE.md

The selected index file (`AGENTS.md` or `CLAUDE.md`) serves as the central knowledge base for lessons. The `## Lessons Learned` section acts as an index and quick reference.

**Structure within the selected index file**:

```markdown
# Project Name

[Other sections: Overview, Architecture, etc.]

## Lessons Learned

Quick reference to past mistakes and how to avoid them. For any similar task, the AI MUST read the relevant linked lesson file(s) before proceeding.

- [Lesson summary with actionable guidance](docs/lessons/file-name.md)
- [Another lesson summary](docs/lessons/another-file.md)

[Rest of selected index file content]
```

**Maintenance**:
- Keep this section near the top or bottom of the selected index file for easy access
- Lessons are listed in chronological order (newest first recommended)
- Remove outdated lessons or consolidate related ones over time

## Limitations

1. **Not a replacement for proper documentation** - Lessons are for mistakes and learnings, not comprehensive guides
2. **Requires discipline** - AI can suggest, but quality depends on thoughtful content
3. **Can accumulate noise** - Be selective about what qualifies as a lesson
4. **Manual cleanup needed** - Periodically review and prune outdated lessons

## See Also

- [LESSON_TEMPLATE.md](references/LESSON_TEMPLATE.md) - Complete lesson file template
