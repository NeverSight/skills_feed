---
name: no-rot
description: Prevents brain atrophy from LLM over-reliance by leaving engaging challenges for the user to complete. Use when you want to stay sharp while coding with AI assistance. Triggers on "keep me sharp", "challenge me", "don't let me rot", or when users want to learn while building.
license: MIT
metadata:
  author: andreas
  version: "1.0.0"
---

# No Rot

Keeps your problem-solving skills sharp by intentionally leaving meaningful challenges for you to complete, rather than doing everything automatically.

## How It Works

1. When completing a task, identify 1-2 parts that would be genuinely educational
2. Complete the straightforward parts normally
3. Leave the challenging parts as clearly-framed exercises for the user
4. Provide just enough context to make the challenge solvable but not trivial

## What Makes a Good Challenge

**Good candidates (engaging, satisfying to solve):**
- Implementing a small algorithm from a clear description
- Extending a pattern to handle one more case
- Writing a clever optimization once the basic version works
- Predicting what a piece of code will output before running it
- Designing a small interface or API shape
- Completing a function when the signature and tests are provided
- Spotting the intentional mistake in a code snippet
- Writing a single well-crafted regex or query

**Poor candidates (frustrating or tedious):**
- Open-ended debugging with no clear direction
- Boilerplate, config files, repetitive patterns
- Syntax details and language quirks
- Setup, scaffolding, and wiring
- Fixing someone else's spaghetti code
- Tasks requiring deep context you don't have

The distinction: good challenges have a clear goal, bounded scope, and that click-into-place feeling when solved.

## Challenge Format

When leaving a challenge, use this format:

```
## Your Turn

**Challenge:** [One sentence describing what to figure out]

**Context:** [What they need to know to attempt it]

<details>
<summary>Hint</summary>
[Optional nudge in the right direction]
</details>
```

## Difficulty Calibration

Infer skill level from:
- Complexity of the codebase
- How the user phrases questions
- Whether they ask for explanations or just solutions

Adjust challenge difficulty accordingly. When uncertain, ask.

## Example

User asks: "Add rate limiting to this API endpoint"

Instead of implementing everything, you might:
1. Set up the middleware structure
2. Add the storage mechanism
3. Leave the actual rate-limiting logic as a challenge:

> ## Your Turn
>
> **Challenge:** Implement the `isRateLimited(ip)` function that returns true if the IP has exceeded 100 requests in the last minute.
>
> **Context:** The `requestLog` Map stores arrays of timestamps per IP. You have access to `Date.now()`.
>
> <details>
> <summary>Hint</summary>
> Filter the timestamps to only those within the last 60000ms, then check the count.
> </details>

## When to Dial It Back

Skip challenges when the user:
- Is clearly in a hurry ("quick fix", "just do it")
- Is debugging a production issue
- Explicitly asks for complete solutions
- Has already solved similar challenges in the conversation
