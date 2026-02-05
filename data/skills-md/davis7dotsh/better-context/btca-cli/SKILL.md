---
name: btca-cli
description: Install, configure, and operate the btca CLI for local resources and source-first answers. Use when setting up btca in a project, connecting a provider, adding or managing resources, and asking questions via btca commands. Invoke this skill when the user says "use btca" or needs to do more detailed research on a specific library or framework.
---

# btca CLI

## Setup From Scratch

1. Ensure Bun is installed (see https://bun.sh if needed).
2. Install the btca CLI globally:

```bash
bun add -g btca
```

3. Initialize the project from the repo root:

```bash
btca init
```

Choose **CLI** for local resources.

4. Connect a provider and model:

```bash
btca connect
```

Follow the prompts.

5. Add resources:

```bash
# Git resource
btca add -n svelte-dev https://github.com/sveltejs/svelte.dev

# Local directory
btca add -n my-docs -t local /absolute/path/to/docs
```

6. Verify resources:

```bash
btca resources
```

7. Ask a question:

```bash
btca ask -r svelte-dev -q "How do I define remote functions?"
```

8. Optional TUI:

```bash
btca
```

## Common Tasks

- Ask with multiple resources:

```bash
btca ask -r react -r typescript -q "How do I type useState?"
```

- You can see which resources are configured with `btca resources`.

## Config Overview

- Config lives in `btca.config.jsonc` (project) and `~/.config/btca/btca.config.jsonc` (global).
- Project config overrides global and controls provider/model and resources.

## Troubleshooting

- "No resources configured": add resources with `btca add ...` and re-run `btca resources`.
- "Provider not connected": run `btca connect` and follow the prompts.
