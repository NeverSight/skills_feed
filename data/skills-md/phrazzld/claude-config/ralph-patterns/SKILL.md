---
name: ralph-patterns
description: |
  Patterns for Ralph loop tasks. Auto-loaded to provide guidance on
  completion signals, progress tracking, and iteration patterns.
  Ralph = autonomous issue-to-merged-PR loop.
user-invocable: false
effort: high
---

# Ralph Loop Patterns

You're running in a Ralph loop - an autonomous issue-to-merged-PR workflow.

## Completion Signals

Output these exact XML tags for the shell script to detect:

- `<promise>DONE</promise>` - Task complete, exit successfully
- `<promise>BLOCKED</promise>` - Cannot proceed, needs human intervention

Always include the exact XML tag. The shell script greps for it.

## Progress Tracking

Ralph monitors these for "no progress" circuit breaker:
- Git HEAD (commits)
- PR state (reviews, CI status)

**Make commits frequently to show progress.** Avoid long stretches without commits.

## Within a Ralph Loop

You have full access to:
- `/spec`, `/architect`, `/build`, `/refactor`, `/update-docs`, `/pr`
- Moonbridge MCP for Codex/Kimi delegation
- Sentry, PostHog, GitHub MCPs
- All configured hooks and skills

## Delegation Pattern

Use Moonbridge for implementation:
```
mcp__moonbridge__spawn_agent({
  "prompt": "Implement [feature]. Follow pattern in [ref file].",
  "adapter": "codex",
  "reasoning_effort": "high"
})
```

## Handling CI Failures

1. Get CI logs: `gh run view --log-failed`
2. Analyze failures
3. Fix and push
4. Wait for re-run (CI usually triggers automatically)

## Handling Review Feedback

1. Get PR comments: `gh pr view --comments`
2. Identify critical vs stylistic feedback
3. Address critical feedback first
4. Push changes
5. Respond to reviewers via commit message or PR comment

## When to Output BLOCKED

Output `<promise>BLOCKED</promise>` when:
- Missing required credentials or API keys
- Ambiguous requirements that need human clarification
- Conflicting constraints with no clear resolution
- External dependency is down/unavailable
- Permissions issues you can't resolve

Include a brief explanation after the tag:
```
<promise>BLOCKED</promise>
Reason: Need clarification on whether user auth should use JWT or session cookies.
```

## Anti-Patterns

- Don't loop infinitely on the same failing test
- Don't make empty commits just to show progress
- Don't ignore reviewer feedback hoping it goes away
- Don't skip /codify-learning at the end (Ralph does this automatically)
