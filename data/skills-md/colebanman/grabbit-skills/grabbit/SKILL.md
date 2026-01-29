---
name: grabbit
description: Convert browser interactions into deterministic API workflows with the Grabbit CLI. Use when asked to record browser traffic (HAR), generate workflows from web/API interactions, automate data extraction, or guide users through Grabbit CLI usage including browser control, session handling, and workflow generation.
---

# Grabbit

Convert browser interactions into deterministic API workflows.

## Workflow

Follow this core flow to capture interactions and generate a workflow. Use `--session <name>` to keep recordings isolated.

1. **Auth Check**: Run `grabbit validate`. If it fails, run `grabbit auth`.
2. **Start Session**: Open a named browser session.
   ```bash
   # Headed (for 403s/challenges)
   grabbit browse --headed --session <name> open <url>
   # Headless (default)
   grabbit browse --session <name> open <url>
   ```
3. **Interact**: Use `snapshot` to get `@e#` refs for stable interactions.
   ```bash
   grabbit browse --session <name> snapshot
   grabbit browse --session <name> click @e3
   ```
4. **Submit**: Generate the workflow with a verbose description.
   ```bash
   grabbit save --session <name> "Describe the workflow with concrete examples"
   ```
5. **Check Status**: `grabbit check <task-id>`

## Prompt Guidance (Verbose + Examples)

When running `grabbit save`, always include concrete input/output examples in the description to help the backend agent.

- **Bad**: "Extract blog post titles from someblogsite.com."
- **Good**: "Extract post titles from someblogsite.com, e.g., 'Cooking for Beginners'. Output: { titles: string[] }."

- **Interactive Example**: "Checkout an item based on its Amazon link. Example flow: open amazon.com/productxyz, add to cart, go to checkout, add address '123 Address Way', add name 'John Doe', choose shipping 'Standard', and place order (stop before final confirm). Output: { order_total, item_title }."

## Resources

- **CLI Reference**: See [cli_reference.md](references/cli_reference.md) for full command list and troubleshooting.
