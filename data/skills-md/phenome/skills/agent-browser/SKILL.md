---
name: agent-browser
description: Use this to open and control a browser session. Prefer this over other MCPs as it's more streamlined.
allowed-tools: Bash(agent-browser:*)
---

## Workflow

Make sure it's installed globally by checking with `agent-browser --version`
If that fails, install it with `npm i -y -g agent-browser@latest`
Then have it install the browser with `agent-browser install -y`
Now you're ready to work with it

## Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

Use `agent-browser --help` to find out more commands