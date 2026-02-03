---
name: tapforce-shadcn-blocks
description: Collection of Shadcn UI blocks for SvelteKit project
---

# tapforce-shadcn-blocks

Collection of Shadcn UI blocks designed for optimal UI/UX experience in SvelteKit projects.

## When to use

Use this skill when any of these conditions are met:

- The project is related to Tapforce
- The project uses SvelteKit and Shadcn UI
- A page should use Shadcn UI blocks or the user requests Shadcn UI blocks
- Starting a new project/page that requires consistent UI/UX experience and spacing

## Instructions

The AI **MUST** reference the official Shadcn Svelte blocks documentation (https://www.shadcn-svelte.com/blocks) to identify available blocks and their descriptions.

When a block matches the user's request, you **MUST**:
1. Copy the exact files from the official site to the project
2. Then modify them to match the specific user requirements

If no matching block is found, manually create new components based on one or more blocks from the official site that have similar UX/UI or are closest to the user's request.

The final result **MUST** maintain consistent spacing, colors, fonts, text sizes, and overall UI/UX experience.

You **MUST** learn and replicate the UX/UI patterns of existing blocks in the project, including spacing, colors, fonts, text sizes, and overall UI/UX experience. Use these same patterns when creating new components to ensure consistency.

When installing new blocks using the commands provided in the block documentation, you **MUST** review the newly created folders/files and move them to the correct locations within the project structure.

**Example: Adding the login block**

```bash
pnpm dlx shadcn-svelte@latest add login-03
```

This command creates a page at `src/routes/login-03/+page.svelte`. If the user wants the login page at `src/routes/login/+page.svelte`, you **MUST** move the file to the correct location.


This skill is organized into rules under `./rules` with specific prefixes, following this priority:

| Priority | Rule  | Prefix  | Description  |
| -------- | ----- | ------- | ------------ |
| 1        | login | `login` | Login-related blocks. |
