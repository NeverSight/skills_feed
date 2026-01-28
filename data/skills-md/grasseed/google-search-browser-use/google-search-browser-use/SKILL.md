---
name: google-search-browser-use
description: Use browser-use to perform Google searches, open results, and extract key information from live pages. Use when the user asks to "search Google", "look this up on Google", or needs current web results via a real browser session (often to avoid bot blocks).
---

# Google Search Browser Use

## Overview

Run Google searches with `browser-use` (prefer real browser mode), open results, and extract the relevant snippets or page content. This skill leverages the user's existing browser session to reduce CAPTCHAs.

## Prerequisites

Before running the search, ensure the environment is ready:

1.  **Check Installation**:
    Verify if `browser-use` is available in the current PATH.
    ```bash
    which browser-use
    ```

2.  **Install if Missing**:
    If not found, install it using pip.
    ```bash
    python3 -m pip install --user browser-use
    ```

3.  **Locate Binary**:
    If the command is still not found after installation, it is likely in the user's local bin directory. Retrieve the path dynamically:
    ```bash
    python3 -m site --user-base
    # The binary is typically at <USER_BASE>/bin/browser-use
    ```

## Workflow

### 1) Launch a Google search (Real Browser Mode)

Use the real browser to reuse the user’s logged-in session.

**Option A: Standard Execution**
```bash
browser-use --browser real open "https://www.google.com/search?q=YOUR+QUERY"
```

**Option B: Explicit Path Execution**
If Option A fails (command not found), use the full path found in Prerequisites:
```bash
# Example (adjust based on 'python3 -m site --user-base' output):
${HOME}/Library/Python/3.14/bin/browser-use --browser real open "https://www.google.com/search?q=YOUR+QUERY"
```
*(Note: Replace `3.14` with your current Python version if different)*

### 2) Inspect results and parse

Once the browser is open:

```bash
# Check current page state
browser-use --browser real state

# Click on a search result (use index from state output)
browser-use --browser real click <index>
```

### 3) Extract or Summarize

-   **Goal**: Provide a short summary (3-6 bullets) with source citations.
-   **Fallback**: If `browser-use` struggles with parsing, use `curl` with Jina AI for a text-friendly version:
    ```bash
    curl -L "https://r.jina.ai/https://example.com"
    ```

### 4) Close the Session

```bash
browser-use close
```

## Troubleshooting

-   **CAPTCHAs**: If encountered, solve them manually in the open browser window.
-   **Path Issues**: If `browser-use` cannot be called directly, always prefer finding the path via `python3 -m site --user-base` rather than guessing.
-   **Connection**: Ensure no VPN/Proxy is blocking Google results if timeouts occur.

