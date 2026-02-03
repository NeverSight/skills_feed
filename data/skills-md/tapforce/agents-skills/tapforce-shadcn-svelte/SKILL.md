---
name: tapforce-shadcn-svelte
description: Comprehensive guide for using Shadcn UI with SvelteKit
---

# tapforce-shadcn-svelte

Use Shadcn UI version svelte to co-op with SvelteKit project. The target is replace manual svelte components with shadcn ui components if possible.

## When to use

Use this skill when project mention about tapforce, using Shadcn UI, or you think project need to use Shadcn UI.

## Instructions

**IMPORTANT: When using this skill, always fetch the latest LLMs content from https://www.shadcn-svelte.com/llms.txt to ensure you have the most up-to-date information and best practices.**

Skill separated to rules under `./rules` with prefix, following priority:

| Priority | Rule    | prefix | Description                                              |
| -------- | ------- | ------ | -------------------------------------------------------- |
| 1        | prepare | `pr`   | Steps and practices to prepare project to use Shadcn UI. |
| 2        | policy  | `pl`   | Practices to follow when use Shadcn UI.                  |

Each rules have own name, description, and tags.
Rule can include **Incorrect**, **Correct**, or **Example** code block.

Full version of skill and rules represent with file AGENTS.md.

## Reference

- [Install with sveltekit](https://www.shadcn-svelte.com/docs/installation/sveltekit)
- [Theming](https://www.shadcn-svelte.com/docs/theming)
- [Dark mode](https://www.shadcn-svelte.com/docs/dark-mode/svelte)
- [CLI](https://www.shadcn-svelte.com/docs/cli)
- [Components](https://www.shadcn-svelte.com/docs/components)
- [LLMs](https://www.shadcn-svelte.com/llms.txt)
