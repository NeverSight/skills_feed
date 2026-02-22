---
name: conventional-comments
description: Format review comments following the Conventional Comments standard. Use when writing code review comments, PR feedback, RFC reviews, peer reviews, or when the user asks for help with review comments.
---

# Conventional Comments

Based on the [Conventional Comments](https://conventionalcomments.org/) standard. Comments that are easy to grok and grep.

## Comment Format

```
<label> [decorations]: <subject>

[discussion]
```

- **label** (required) — a single word signifying the kind of comment
- **subject** (required) — the main message of the comment
- **decorations** (optional) — extra classifiers in parentheses, comma-separated, placed after the label
- **discussion** (optional) — supporting statements, context, reasoning, and next steps

## Labels

Use these labels to prefix every comment:

| Label | Purpose |
|-------|---------|
| `praise` | Highlight something positive. Leave at least one per review. Must be sincere — false praise is damaging. |
| `nitpick` | Trivial, preference-based request. Non-blocking by nature. |
| `suggestion` | Propose an improvement. Be explicit about *what* and *why*. |
| `issue` | Highlight a specific problem (user-facing or internal). Pair with a suggestion when possible. |
| `todo` | Small, trivial, but necessary change. Simpler than an issue or suggestion. |
| `question` | Potential concern you're not sure about. Ask for clarification or investigation. |
| `thought` | An idea that emerged from reviewing. Non-blocking, but valuable for mentoring and focused initiatives. |
| `chore` | Task that must be done before acceptance. Link to the process description when possible. |
| `note` | Always non-blocking. Highlights something the reader should be aware of. |

Optional expressive labels:

| Label | Purpose |
|-------|---------|
| `typo` | Like `todo`, but the issue is a misspelling. |
| `polish` | Like `suggestion`, but nothing is wrong — just immediate quality improvements. |
| `quibble` | Like `nitpick`, without the imagery. |

## Decorations

Decorations add context inside parentheses after the label:

| Decoration | Meaning |
|------------|---------|
| `(non-blocking)` | Should NOT prevent acceptance. Useful when comments are blocking by default. |
| `(blocking)` | MUST be resolved before acceptance. Useful when comments are non-blocking by default. |
| `(if-minor)` | Resolve only if the fix is minor or trivial. |

Custom decorations (e.g., `security`, `ux`, `test`, `performance`) MAY be added to further classify comments. Keep them minimal — too many decorations hurt readability.

## Code Review Formatting

All comment output MUST be valid GitHub-flavored markdown — assume it will be copy-pasted into a PR comment.

### Code references

Only include explicit file paths or line references when pointing the reader to a **different** location than where the comment is placed (e.g., related code in another file, a shared utility, a test that needs updating), otherwise the localisation is handeled by GitHub's review UI.

### Code in comments

- Wrap inline code (variable names, function calls, values) in single backticks: `` `myFunction()` ``
- Use fenced code blocks with a language tag for multi-line code snippets:

````markdown
```python
def example():
    return True
```
````

- When suggesting a replacement, show both the current and proposed code in fenced blocks

## Communication Best Practices

### Be curious

Assume you don't have all the context. Ask questions instead of stating conclusions as facts.

- Bad: "This bug could be solved in the `Main` component. That will probably take a lot less code."
- Good: **question:** "Could we solve this in the `Main` component? I wonder if that would be a more straightforward fix and require less code."

### Replace "you" with "we"

Written reviews lack vocal tone. "You should" feels pointed; "we should" feels collaborative.

- Bad: **issue:** "You should write tests for this."
- Good: **todo:** "We should write tests for this."

### Leave actionable comments

Make it clear how a comment should be resolved. If there's no obvious path forward, make that obvious too.

### Combine similar comments

Batch similar issues into one comment rather than many small ones. Include a patch or example when helpful.

### Patient mentoring

Knowledge shared with patience and kindness lands more deeply and ripples out to future reviews.

## Examples

**Praise:**

> **praise:** Beautiful test coverage — the edge cases are well thought out.

**Suggestion with code:**

> **suggestion (security):** I'm a bit concerned that we are implementing our own DOM purifying function here.
>
> Could we consider using the framework's built-in sanitizer instead?
>
> ```typescript
> // Instead of
> function sanitize(input: string) { ... }
>
> // Use
> import { sanitize } from '@angular/core';
> ```

**Issue with decoration:**

> **issue (ux, non-blocking):** These buttons should be red, but let's handle this in a follow-up.

**Question with decoration:**

> **question (non-blocking):** At this point, does it matter which thread has won?
>
> Maybe to prevent a race condition we should keep looping until they've all won?

**Nitpick:**

> **nitpick:** `little star` => `little bat`
>
> Can we update the other references as well?

**Cross-file reference (when pointing to a different location):**

> **suggestion:** This validation duplicates the logic in `src/utils/validate.ts#L30-L45`. Could we reuse `validateInput()` here instead?

**Chore:**

> **chore:** Let's run the `lint-check` CI job to make sure this doesn't break any known references.
>
> Here are the [docs for running this job](#). Feel free to reach out if you need any help!

**Combined suggestion (batching similar feedback):**

> **polish:** Could we rename all `m_X` variables to just `X`? Hungarian Notation isn't followed in this project.
>
> For example:
>
> ```typescript
> // Instead of
> interface Wizard { m_foo: string; }
>
> // Use
> interface Wizard { foo: string; }
> ```
