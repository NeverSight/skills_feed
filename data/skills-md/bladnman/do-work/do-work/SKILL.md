---
name: do-work
description: Task queue - add requests or process pending work
argument-hint: run | task to capture
---

# Do-Work Skill

A unified entry point for task capture and processing.

**Actions:**
- **do**: Capture new tasks/requests → writes to do-work/ folder
- **work**: Process pending requests → executes the queue

## Routing Decision

### Step 1: Parse the Input

Examine what follows "do work":

| Pattern | Example | Route |
|---------|---------|-------|
| Empty or bare invocation | `do work` | → Ask: "Start the work loop?" |
| Action verbs only | `do work run`, `do work go`, `do work start` | → work |
| Descriptive content | `do work add dark mode`, `do work [meeting notes]` | → do |

### Step 2: Preserve Payload

**Critical rule**: Never lose the user's content.

If routing is unclear BUT content was provided:
- Default to **do** (adding a task)
- Hold onto $ARGUMENTS
- If truly ambiguous, ask: "Add this as a request, or start the work loop?"
- User replies with just "add" or "work" → proceed with original content

### Action Verbs (→ Work)

These signal "process the queue":
run, go, start, begin, work, process, execute, build, continue, resume

### Content Signals (→ Do)

These signal "add a new task":
- Descriptive text beyond a single verb
- Feature requests, bug reports, ideas
- Screenshots or context
- "add", "create", "I need", "we should"

## Examples

### Routes to Work
- `do work` → "Ready to process the queue?" (confirmation)
- `do work run` → Starts work action immediately
- `do work go` → Starts work action immediately

### Routes to Do
- `do work add dark mode` → Creates REQ file
- `do work the button is broken` → Creates REQ file
- `do work [400 words]` → Creates REQ/CONTEXT files

## Payload Preservation Rules

When clarification is needed but content was provided:

1. **Do not lose $ARGUMENTS** - keep the full payload in context
2. **Ask a simple question**: "Add this as a request, or start the work loop?"
3. **Accept minimal replies**: User says just "add" or "work"
4. **Proceed with original content**: Apply the chosen action to the stored arguments
5. **Never ask the user to re-paste content**

This enables a two-phase commit pattern:
1. Capture intent payload
2. Confirm action

## Action References

Follow the detailed instructions in:
- [do action](./actions/do.md) - Request capture
- [work action](./actions/work.md) - Queue processing
