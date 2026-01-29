---
name: work-on-linear-issue
description: Fetches a Linear issue and creates a comprehensive plan for implementation.
---

# Work on Linear Issue

Fetches issue details from Linear and guides you through creating a comprehensive implementation plan.

## When to Use

- When starting work on a Linear issue
- When you need to analyze and plan implementation for an issue
- When onboarding to a new task from Linear

## Prerequisites

- `LINEAR_API_KEY` environment variable must be set (can also be in `.env` file)
- `curl` and `jq` must be installed

## Usage

```bash
builtin:///skills/scripts/work-on-linear-issue <issue-abbreviation>
```

Examples:

```bash
builtin:///skills/scripts/work-on-linear-issue MC-123
builtin:///skills/scripts/work-on-linear-issue https://linear.app/abc/issue/MC-123/issue-title
```

## Workflow

"AI models are geniuses who start from scratch on every task." — Noam Brown

Onboard yourself to the current task:
• Use ultrathink.
• Explore the codebase.
• Ask questions if needed.

Goal: Be fully prepared to start working on the task.

Take as long as you need to prepare. Over-preparation is better than under-preparation.

## Planning Tasks

1. Review the issue details fetched from Linear
2. Examine relevant parts of the codebase
3. Analyze existing patterns and potential issues
4. Create a comprehensive plan considering:
   - Required code changes
   - Potential impacts on other parts of the system
   - Necessary tests to be written or updated
   - Documentation updates
   - Performance considerations
   - Security implications
   - Backwards compatibility (if applicable)
   - Reference links to featurebase or user request sources

5. Think deeply about edge cases, potential challenges, and best practices
6. **ASK FOR EXPLICIT APPROVAL** before starting on the TODO list

Remember: Your task is to create a plan, not to implement changes. Focus on providing a thorough, well-thought-out strategy, then ASK FOR APPROVAL BEFORE STARTING WORK.
