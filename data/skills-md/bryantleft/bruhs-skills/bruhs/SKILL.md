---
name: bruhs
description: Opinionated development lifecycle - spawn projects, cook features, yeet to ship
---

# bruhs - Complete Development Lifecycle

When invoked, ask the user which command to run:

```
What do you want to do?
○ spawn - Create new project or add to monorepo
○ claim - Claim existing project for bruhs
○ cook - Plan + Build a feature end-to-end
○ yeet - Ship: Linear ticket → Branch → Commit → PR
○ peep - Address PR review comments and merge
○ dip - Clean up after merge and switch to base branch
○ slop - Clean up AI slop (senior engineer code review)
```

Present these options interactively, then follow the corresponding command file:
- **spawn** → Read and follow `commands/spawn.md`
- **claim** → Read and follow `commands/claim.md`
- **cook** → Read and follow `commands/cook.md`
- **yeet** → Read and follow `commands/yeet.md`
- **peep** → Read and follow `commands/peep.md`
- **dip** → Read and follow `commands/dip.md`
- **slop** → Read and follow `commands/slop.md`

## Quick Access

Users can also specify directly:
- `/bruhs spawn` or `/bruhs spawn <name>`
- `/bruhs claim`
- `/bruhs cook` or `/bruhs cook <feature>`
- `/bruhs yeet`
- `/bruhs peep` or `/bruhs peep <PR#>` or `/bruhs peep <TICKET-ID>`
- `/bruhs dip`
- `/bruhs slop` or `/bruhs slop <path>` or `/bruhs slop --fix`

If an argument is provided, skip the selection and go directly to that command.
