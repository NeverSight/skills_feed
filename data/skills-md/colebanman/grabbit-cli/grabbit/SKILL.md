---
name: grabbit
description: "Control the Grabbit CLI to record browser interactions (HAR) and generate API workflows. Use when the user wants to: (1) Automate browser actions, (2) Capture web traffic for API analysis, (3) Create deterministic workflows from browsing sessions, or (4) Learn how to use the Grabbit CLI commands."
---

# Grabbit CLI

Grabbit turns browser actions into reusable API workflows: you browse a site, capture what you do, and Grabbit generates stable cURL-ready workflows for automation, extraction, and integrations.

**Always run `grabbit save` after browsing.** Do not parse snapshot output manually or treat it as the final result. Snapshot is for inspection during capture; the real output is the workflow from `save` → `check`. Skipping `save` leaves the session incomplete and produces no reusable workflow.

## Before You Start

**Install** (requires Node.js):
```bash
npm i -g @cole-labs/grabbit
```

**Sessions**: Always use `--session <name>` so captures stay isolated. Without it, multiple runs can mix requests.

## Core Workflow

1.  **Authenticate** (one-time):
    ```bash
    grabbit validate || grabbit auth
    ```
    `grabbit auth` opens your browser to a pairing page. Sign in, then enter the code shown there into your terminal.

2.  **Capture**:
    ```bash
    # Open a page (add --headed to see the browser; default is headless/invisible)
    grabbit browse --session <name> open <url>
    # Or with visible browser: grabbit browse --headed --session <name> open <url>

    # Inspect the page — snapshot prints @e1, @e2, etc. Use these for clicks/fills
    grabbit browse --session <name> snapshot

    # Interact using the refs from snapshot
    grabbit browse --session <name> click @e1
    grabbit browse --session <name> fill @e2 "data"

    # Optional: screenshot to verify
    grabbit browse --session <name> screenshot
    ```

3.  **Generate** (required — do not skip): Always run `save` when done browsing. Submit with a **verbose, example-rich prompt**. The command prints a task ID — use it in the next step.
    ```bash
    grabbit save --session <name> "Detailed description. Example Input: 'X'. Example Output: { id: '123' }"
    ```

4.  **Poll**: Use the task ID from `save`. When status is `completed`, the output includes a workflow ID for `grabbit add`.
    ```bash
    grabbit check <task-id>
    ```

5.  **Integrate**: After completion, use the workflow ID from the `check` output.
    ```bash
    grabbit add <workflow-id>
    grabbit skill install
    grabbit keys list
    grabbit keys show
    ```
    For tools/agents: `export GRABBIT_API_KEY="<token>"` — use the token from `grabbit keys show`.

6.  **List Workflows**:
    ```bash
    grabbit workflows
    ```

## Critical Best Practices

*   **Always save**: Never finish a browsing session without `grabbit save`. Do not parse snapshot text with grep/sed/awk — that is not the workflow. Grabbit generates the workflow from the HAR; you must run `save` then `check` to get it.
*   **Headed mode**: Add `--headed` to see the browser. Use it for bot protection (Cloudflare, 403s) or when debugging. Default is headless (no visible window).
*   **Snapshots**: Run `snapshot` for element refs (`@e1`, `@e2`, …) and to guide interactions. Do not use it as the source of extracted data — use `save` to produce the workflow that does the extraction.
*   **Prompting**: Include concrete examples (strings you saw, JSON shape). *Bad*: "Get prices." *Good*: "Extract prices. Example: '$19.99'. Output: { price: number }."

## Common Errors

*   **Unauthorized**: Run `grabbit auth`, then retry.
*   **No active browser session**: Run `grabbit browse --session <name> open <url>` before `grabbit save`.
*   **No requests recorded**: Interact with the page (click, type, navigate), then run `snapshot` and `save` again.

## Reference

For the full command list (cookies, storage, network, locators), see [cli_reference.md](references/cli_reference.md).
