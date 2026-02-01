---
name: btca-lazy
description: Use btca only when the user explicitly requests it.
---

# btca (lazy)

## Purpose

Use btca only when the user explicitly says "use btca".

## When to Use

- The user explicitly requests btca for upstream information.
- The user asks for official source or documentation verification.

## When Not to Use

- The user did not request btca.
- The answer is available from local repository context.

## Workflow

- Read `btca.config.jsonc` from the current project root to discover available resources.
- If `btca.config.jsonc` is missing, read `~/.config/btca/btca.config.jsonc`.
- Only run btca after the user requests it explicitly.

## Usage

```bash
btca ask -r <resource> -q "<question>"
```

Use multiple resources when needed:

```bash
btca ask -r svelte -r sveltekit -q "How to lazy load a svelte component?"
```

## Available Resources

read `btca.config.jsonc` or if it is missing try reading `~/.config/btca/btca.config.jsonc` for the name field in the resources array.
