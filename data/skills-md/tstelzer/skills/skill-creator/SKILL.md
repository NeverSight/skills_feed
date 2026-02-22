---
name: skill-creator
description: Guide for creating or updating simple, standalone skills with a single SKILL.md file
---

# Skill Creator

## What a Skill Is

A skill is a concise, task-focused guide that tells Claude how to perform a specific job consistently.

## SKILL.md Format

Frontmatter:

```yaml
name: skill-name
description: What the skill does and when to use it.
```

Body:

- Use imperative instructions.
- Keep it short and procedural.
- Include only information Claude needs to execute the task.

## Creation Checklist

1. Identify target tasks and example user prompts.
2. Write the frontmatter description to cover when the skill should trigger.
3. Draft a minimal workflow in the body.
4. Add 1–3 concise examples if they clarify steps.
5. Remove anything not essential to the workflow.

## Rules

- Do not overexplain the "why" (unless explicitly prompted), only show the "how" of skills.
- Prefer compact code snippets over long explanations.
- Do not strictly follow the structure reference pages, simplify and group.
- Keep the main SKILL.md compact and to the point. For more specialized information, co-locate `*.md` files (sub-skills) next to the `SKILL.md`. These should not include frontmatter. Reference them like this in the `SKILL.md` top-level:

```md
[For deriving http clients](./effect-derive-http-client.md)
[For creating middlewares](./effect-http-middleware.md)
[For deriving swagger UIs](./effect-http-swagger.md)
[For multipart uploads](./effect-http-multipart.md)
[For streaming](./effect-http-streaming.md)
```

## Minimal Template

```markdown
---
name: skill-name
description: One sentence describing what it does and when to use it.
---

# Skill Name

## Workflow

1. Step one.
2. Step two.
3. Step three.

## Examples

- "Example user prompt"
```
