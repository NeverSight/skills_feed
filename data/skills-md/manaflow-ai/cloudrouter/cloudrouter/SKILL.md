---
name: cloudrouter
description: Manage cloud development sandboxes with cloudrouter. Create, sync, and access remote VMs with GPU support, Docker, and browser automation. Use when asked to create a sandbox, spin up a dev environment, run code in the cloud, use GPUs, automate a browser, or interact with remote VMs.
license: MIT
metadata:
  author: manaflow-ai
  version: "0.0.3"
---

# cloudrouter - Cloud Sandboxes for Development

cloudrouter manages cloud sandboxes for development. Use these commands to create, manage, and access remote development environments with GPU support and browser automation.

## When this skill is invoked

When the user invokes `/cloudrouter` or `/cr` without a specific task, present the available modes:

```
cloudrouter - Cloud Development Sandboxes

  Modes:
    cloudrouter start .                    Sync current directory to a cloud sandbox
    cloudrouter start --size small .       Smaller sandbox (2 vCPU, 8 GB)
    cloudrouter start --gpu T4 .           Sandbox with T4 GPU (16GB VRAM)
    cloudrouter start --gpu A100 .         Sandbox with A100 GPU (40GB VRAM)
    cloudrouter start --gpu H100 .         Sandbox with H100 GPU (80GB VRAM)

  Manage:
    cloudrouter ls                         List all sandboxes
    cloudrouter code <id>                  Open VS Code in browser
    cloudrouter jupyter <id>               Open Jupyter Lab in browser
    cloudrouter pty <id>                   Open terminal session
    cloudrouter vnc <id>                   Open VNC desktop
    cloudrouter stop <id>                  Pause sandbox
    cloudrouter resume <id>                Resume paused sandbox

  Browser automation:
    cloudrouter browser snapshot -i <id>       Get interactive elements
    cloudrouter browser open <id> <url>        Navigate to URL
    cloudrouter browser screenshot <id>        Take screenshot

  Run "cloudrouter start --help" for all options.
```

## Setup

**Before doing anything else, always run this command at the start of any cloudrouter task.** Do not ask the user — just run it automatically:

```bash
npm install -g @manaflow-ai/cloudrouter   # Install/update CLI
```

This is idempotent — safe to run even if already up to date. This ensures the agent always has the latest CLI.

This installs both `cloudrouter` and `cr` (shorthand) as CLI commands.

Then authenticate:

```bash
cloudrouter login
```

If the user hasn't logged in yet, prompt them to run `cloudrouter login` first before using any other commands.

## Quick Start

```bash
cloudrouter login                        # Authenticate (opens browser)
cloudrouter start .                      # Create sandbox from current directory
cloudrouter start --gpu T4 .             # Create sandbox with GPU
cloudrouter start --size small .         # Create smaller sandbox
cloudrouter code <id>                    # Open VS Code
cloudrouter jupyter <id>                 # Open Jupyter Lab
cloudrouter pty <id>                     # Open terminal session
cloudrouter ls                           # List all sandboxes
```

> **Preferred:** Always use `cloudrouter start .` or `cloudrouter start <local-path>` to sync your local directory to a cloud sandbox. This is the recommended workflow over cloning from a git repo.

## Commands

### Authentication

```bash
cloudrouter login               # Login (opens browser)
cloudrouter logout              # Logout and clear credentials
cloudrouter whoami              # Show current user and team
```

### Creating Sandboxes

```bash
# Standard sandbox (syncs local directory) — DO NOT pass --size, default is large (8 vCPU, 32 GB)
cloudrouter start .                        # Create from current directory (recommended)
cloudrouter start ./my-project             # Create from a specific local directory
cloudrouter start -o .                     # Create and open VS Code immediately
cloudrouter start -n my-sandbox .          # Create with a custom name

# Size presets — only use if the user specifically requests a different size
cloudrouter start --size small .           # 2 vCPU, 8 GB RAM, 20 GB disk — only if user asks
cloudrouter start --size medium .          # 4 vCPU, 16 GB RAM, 40 GB disk — only if user asks
cloudrouter start --size large .           # 8 vCPU, 32 GB RAM, 80 GB disk (DEFAULT — no flag needed)
cloudrouter start --size xlarge .          # 16 vCPU, 64 GB RAM, 160 GB disk — only if user asks

# With GPU (auto-selects Modal provider)
cloudrouter start --gpu T4 .               # T4 GPU (16GB VRAM)
cloudrouter start --gpu L4 .               # L4 GPU (24GB VRAM)
cloudrouter start --gpu A10G .             # A10G GPU (24GB VRAM)
cloudrouter start --gpu A100 .             # A100 GPU (40GB VRAM) - requires approval
cloudrouter start --gpu H100 .             # H100 GPU (80GB VRAM) - requires approval
cloudrouter start --gpu H100:2 .           # Multi-GPU: 2x H100

# With custom resources (override --size values)
cloudrouter start --cpu 12 --memory 49152 .  # Custom CPU and memory
cloudrouter start --disk 100 .               # Custom disk size (GB)
cloudrouter start --image ubuntu:22.04 .     # Custom container image

# From git repo (URL as positional arg or --git flag)
cloudrouter start https://github.com/user/repo    # Clone git repo directly
cloudrouter start --git user/repo                  # Clone via shorthand
cloudrouter start --git user/repo -b main          # Clone specific branch

# Provider selection
cloudrouter start -p e2b .                 # Use E2B provider (default)
cloudrouter start -p modal .               # Use Modal provider

# Custom timeout
cloudrouter start --timeout 1800 .         # 30-minute timeout (default: 600s = 10 min)
```

### Size Presets

| Size | vCPU | RAM | Disk | Notes |
|------|------|-----|------|-------|
| small | 2 | 8 GB | 20 GB | Light tasks |
| medium | 4 | 16 GB | 40 GB | Standard development |
| large | 8 | 32 GB | 80 GB | **Default** |
| xlarge | 16 | 64 GB | 160 GB | Heavy workloads |

**Do NOT pass `--size` unless the user explicitly asks for a specific size.** The default is `large` (8 vCPU, 32 GB) which is appropriate for most tasks. Using `--size small` unnecessarily will make builds slower and may cause out-of-memory issues.

Individual resource flags (`--cpu`, `--memory`, `--disk`) override `--size` values.

### GPU Options

| GPU | VRAM | Best For | Availability |
|-----|------|----------|-------------|
| T4 | 16GB | Inference, fine-tuning small models | Self-serve |
| L4 | 24GB | Inference, image generation | Self-serve |
| A10G | 24GB | Training medium models | Self-serve |
| L40S | 48GB | Inference, video generation | Requires approval |
| A100 | 40GB | Training large models (7B-70B) | Requires approval |
| A100-80GB | 80GB | Very large models | Requires approval |
| H100 | 80GB | Fast training, research | Requires approval |
| H200 | 141GB | Maximum memory capacity | Requires approval |
| B200 | 192GB | Latest gen, frontier models | Requires approval |

GPUs requiring approval: contact founders@manaflow.ai.

Multi-GPU: append `:N` to the GPU type, e.g. `--gpu H100:2` for 2x H100.

### All `start` Flags

```
-n, --name <name>       Name for the sandbox
-o, --open              Open VS Code after creation
    --size <preset>     Machine size: small, medium, large (default), xlarge
    --gpu <type>        GPU type (T4, L4, A10G, L40S, A100, H100, H200, B200)
    --cpu <cores>       CPU cores (overrides --size)
    --memory <MiB>      Memory in MiB (overrides --size)
    --disk <GB>         Disk size in GB (overrides --size)
    --image <image>     Container image (e.g., ubuntu:22.04)
    --git <repo>        Git repository URL or user/repo shorthand
-b, --branch <branch>   Git branch to clone
-p, --provider <name>   Sandbox provider: e2b (default), modal
-T, --template <id>     Template ID — DO NOT use template names from `cloudrouter templates`; use --gpu flags instead
    --timeout <secs>    Sandbox timeout in seconds (default: 600 = 10 minutes)
```

> **Warning:** Do NOT pass template names (e.g. `cmux-devbox-base`) to the `-T` flag. These are display names, not valid template IDs.

> **Aliases:** `cloudrouter start`, `cloudrouter create`, `cloudrouter new` all do the same thing.

### Managing Sandboxes

```bash
cloudrouter ls                           # List all sandboxes
cloudrouter ls -p modal                  # List only GPU sandboxes
cloudrouter ls -p e2b                    # List only Docker sandboxes
cloudrouter status <id>                  # Show sandbox details and URLs
cloudrouter stop <id>                    # Pause sandbox (preserves state, can resume)
cloudrouter pause <id>                   # Same as stop — alias
cloudrouter resume <id>                  # Resume a paused sandbox
cloudrouter extend <id>                  # Extend sandbox timeout (default: +1 hour)
cloudrouter extend <id> --seconds 7200   # Extend by 2 hours
cloudrouter delete <id>                  # Delete sandbox permanently
cloudrouter templates                    # List available templates
```

> **Important:** `stop` and `pause` are the same command — they preserve sandbox state. Use `resume` to bring a paused sandbox back. Use `delete` (aliases: `rm`, `kill`) to permanently destroy a sandbox.

> **Do NOT use `--timeout`** with `extend` — the flag is `--seconds`.

### Access Sandbox

```bash
cloudrouter code <id>           # Open VS Code in browser
cloudrouter jupyter <id>        # Open Jupyter Lab in browser
cloudrouter vnc <id>            # Open VNC desktop in browser
cloudrouter pty <id>            # Interactive terminal session
```

### Work with Sandbox

```bash
cloudrouter pty <id>                       # Interactive terminal session (use for ongoing work)
cloudrouter ssh <id> <command>             # Execute a one-off command via SSH
cloudrouter ssh <id> "ls -la"              # Run a command (always quote the command string)
cloudrouter pty-list <id>                  # List active PTY sessions
```

> **Important:** Prefer `cloudrouter pty` for interactive work. Use `cloudrouter ssh` for quick one-off commands.
>
> **CRITICAL: Always quote the command string.** `cloudrouter ssh <id> ls -la` will FAIL because `-la` is parsed as a cloudrouter flag. Always wrap in quotes: `cloudrouter ssh <id> "ls -la"`.

#### IMPORTANT: Fix npm Permissions Before Any npm Command

**ALWAYS run this before `npm install` or any npm command in a new sandbox:**

```bash
cloudrouter ssh <id> "sudo chown -R 1000:1000 /home/user/.npm"
```

Without this, `npm install` will fail with EACCES/ENOENT errors on `.npm/_cacache`. This must be done **once per sandbox, before the first npm operation**. Do not skip this step.

### File Transfer

Upload and download files or directories between local machine and sandbox.

**Command signatures:**
- `cloudrouter upload <id> [local-path]` — accepts 1-2 positional args: sandbox ID and optional local path
- `cloudrouter download <id> [local-path]` — accepts 1-2 positional args: sandbox ID and optional local path
- Use `-r <remote-path>` flag to specify a non-default remote directory (default: `/home/user/workspace`)
- **Do NOT pass remote paths as positional arguments** — this will error. Always use the `-r` flag.

```bash
# Upload (local -> sandbox)
cloudrouter upload <id>                            # Upload current dir to /home/user/workspace
cloudrouter upload <id> ./my-project               # Upload directory to workspace
cloudrouter upload <id> ./config.json              # Upload single file to workspace
cloudrouter upload <id> . -r /home/user/app        # Upload to specific remote path
cloudrouter upload <id> . --watch                  # Watch and re-upload on changes
cloudrouter upload <id> . --delete                 # Delete remote files not present locally
cloudrouter upload <id> . -e "*.log"               # Exclude patterns
cloudrouter upload <id> . --dry-run                # Preview without making changes

# Download (sandbox -> local)
cloudrouter download <id>                          # Download workspace to current dir
cloudrouter download <id> ./output                 # Download workspace to ./output
cloudrouter download <id> ./output -r /home/user/app  # Download specific remote dir to ./output
```

> **Warning:** The `-r` flag expects a **directory** path, not a file path. To download a single file, download its parent directory and then access the file locally.
>
> **Common mistake:** `cloudrouter download <id> /remote/path /local/path` — this passes 3 positional args and will fail. Use `cloudrouter download <id> /local/path -r /remote/path` instead.

### Browser Automation (`cloudrouter browser`)

Control Chrome browser in the sandbox via agent-browser. The `cloudrouter browser` command wraps [agent-browser](https://github.com/vercel-labs/agent-browser) and runs commands inside the sandbox via SSH.

> **Startup delay:** The browser may not be ready immediately after sandbox creation. If a `browser` command fails right after `cloudrouter start`, wait a few seconds and retry.

#### Navigation

```bash
cloudrouter browser open <id> <url>        # Navigate to URL
cloudrouter browser back <id>              # Navigate back
cloudrouter browser forward <id>           # Navigate forward
cloudrouter browser reload <id>            # Reload page
cloudrouter browser url <id>               # Get current URL
cloudrouter browser title <id>             # Get page title
```

#### Inspect Page

```bash
cloudrouter browser snapshot -i <id>               # Interactive elements only (RECOMMENDED)
cloudrouter browser snapshot <id>                  # Full accessibility tree
cloudrouter browser snapshot -c <id>               # Compact output
cloudrouter browser screenshot <id>                # Take screenshot (base64 to stdout)
cloudrouter browser screenshot <id> out.png        # Save screenshot to file
cloudrouter browser screenshot <id> --full         # Full page screenshot
```

#### Interact with Elements

```bash
cloudrouter browser click <id> @e1                 # Click element by ref
cloudrouter browser click <id> "#submit"           # Click by CSS selector
cloudrouter browser dblclick <id> @e1              # Double-click element
cloudrouter browser fill <id> @e2 "user@email.com" # Clear input and fill value
cloudrouter browser type <id> @e3 "some text"      # Type without clearing (appends)
cloudrouter browser press <id> Enter               # Press key (Enter, Tab, Escape, etc.)
cloudrouter browser hover <id> @e4                 # Hover over element
cloudrouter browser focus <id> @e5                 # Focus element
cloudrouter browser scroll <id> down 500           # Scroll (up/down/left/right, optional px)
cloudrouter browser scrollintoview <id> "#element"  # Scroll element into view (CSS selector only, NOT @e refs)
cloudrouter browser select <id> @e7 "option-value" # Select dropdown option
cloudrouter browser check <id> @e8                 # Check checkbox
cloudrouter browser uncheck <id> @e9               # Uncheck checkbox
cloudrouter browser upload <id> @e10 /tmp/file.pdf # Upload file to file input
cloudrouter browser drag <id> @e1 @e2              # Drag and drop
```

#### Wait Commands

```bash
cloudrouter browser wait <id> @e1                  # Wait for element to appear
cloudrouter browser wait <id> 2000                 # Wait milliseconds
```

#### Get Information

```bash
cloudrouter browser get-text <id> @e1              # Get element text content
cloudrouter browser get-value <id> @e2             # Get input value
cloudrouter browser get-attr <id> @e3 href         # Get specific attribute
cloudrouter browser get-html <id> @e4              # Get innerHTML
cloudrouter browser get-count <id> ".item"         # Count matching elements
cloudrouter browser get-box <id> @e5               # Get bounding box
cloudrouter browser is-visible <id> @e1            # Check if element is visible
cloudrouter browser is-enabled <id> @e1            # Check if element is enabled
cloudrouter browser is-checked <id> @e1            # Check if checkbox is checked
```

#### Semantic Locators (alternative to refs)

When element refs are unreliable (dynamic pages), use semantic locators:

```bash
cloudrouter browser find <id> text "Sign In" click              # Find by visible text and click
cloudrouter browser find <id> label "Email" fill "user@test.com" # Find by label and fill
cloudrouter browser find <id> placeholder "Search" type "query"  # Find by placeholder
cloudrouter browser find <id> testid "submit-btn" click          # Find by data-testid
```

> **Note:** `find <id> role button click` finds the FIRST button on the page — it cannot filter by button name. Use `find <id> text "Button Name" click` to target a specific button by its visible text. There is no `--name` flag.

#### JavaScript & Console

```bash
cloudrouter browser eval <id> "document.title"                   # Evaluate JavaScript
cloudrouter browser console <id>                                 # View console messages
cloudrouter browser errors <id>                                  # View JavaScript errors
```

#### Tabs & Frames

```bash
cloudrouter browser tab-list <id>                  # List open tabs
cloudrouter browser tab-new <id> "https://..."     # Open new tab
cloudrouter browser tab-switch <id> 2              # Switch to tab by index
cloudrouter browser tab-close <id>                 # Close current tab
cloudrouter browser frame <id> "#iframe-selector"  # Switch to iframe
cloudrouter browser frame <id> main                # Switch back to main frame
```

#### Cookies & Storage

```bash
cloudrouter browser cookies <id>                   # List cookies
cloudrouter browser cookies-set <id> name value    # Set a cookie
cloudrouter browser cookies-clear <id>             # Clear all cookies
cloudrouter browser storage-local <id>             # Get all localStorage
cloudrouter browser storage-local <id> key         # Get specific key
cloudrouter browser storage-local-set <id> k v     # Set localStorage value
cloudrouter browser storage-local-clear <id>       # Clear localStorage
```

#### State Management

```bash
cloudrouter browser state-save <id> /tmp/auth.json   # Save cookies, storage, auth state
cloudrouter browser state-load <id> /tmp/auth.json   # Restore saved state
```

#### Browser Settings

```bash
cloudrouter browser set-viewport <id> 1920 1080    # Set viewport size
cloudrouter browser set-device <id> "iPhone 14"    # Emulate device
cloudrouter browser set-geo <id> 37.7749 -122.4194 # Set geolocation
cloudrouter browser set-offline <id> on            # Toggle offline mode
cloudrouter browser set-media <id> dark            # Emulate color scheme (dark/light)
```

#### Network Interception

```bash
cloudrouter browser network-route <id> "**/api/*"            # Intercept requests
cloudrouter browser network-route <id> "**/ads/*" --abort    # Block requests
cloudrouter browser network-unroute <id>                     # Remove all routes
cloudrouter browser network-requests <id>                    # List tracked requests
```

#### Dialogs

```bash
cloudrouter browser dialog-accept <id>             # Accept alert/confirm/prompt
cloudrouter browser dialog-accept <id> "answer"    # Accept prompt with text
cloudrouter browser dialog-dismiss <id>            # Dismiss dialog
```

#### Element Selectors

Two ways to select elements:
- **Element refs** from snapshot: `@e1`, `@e2`, `@e3`... (preferred — from `cloudrouter browser snapshot -i`)
- **CSS selectors**: `#id`, `.class`, `button[type="submit"]`

Snapshot output shows refs as `[ref=e1]`, but when using them in commands, prefix with `@`: e.g., `@e1`.

#### Tips for Effective Browser Automation

1. **Flags go BEFORE the sandbox ID.** This is critical. `cloudrouter browser snapshot -i <id>` works. `cloudrouter browser snapshot <id> -i` silently returns empty/wrong results. Always put flags like `-i`, `-c`, `--full` before the sandbox ID.

2. **Always snapshot before interacting.** Never use `@e1` without a preceding `cloudrouter browser snapshot -i <id>`. Refs don't exist until you snapshot.

3. **Always re-snapshot after DOM changes.** After any click that navigates, opens a dropdown, submits a form, or triggers dynamic content — snapshot again. Old refs may point to different elements.

4. **Don't mix snapshot modes.** Full `snapshot` and `snapshot -i` assign DIFFERENT ref numbers to the same elements. If you snapshot with `-i`, always interact using refs from that `-i` snapshot. Don't use refs from a full snapshot when you last ran `-i`, or vice versa.

5. **Use `snapshot -i` (interactive only).** The `-i` flag returns only actionable elements (buttons, inputs, links), which is far more efficient than the full accessibility tree. Stick to `-i` for all interactions.

6. **Use `fill` not `type` for form fields.** `fill` clears existing content first, which is almost always what you want. `type` appends to existing content.

7. **Wait after navigation.** After clicking a link or submitting a form, use `cloudrouter browser wait <id> 2000` or wait for a specific element before snapshotting to ensure the page has fully loaded.

8. **Verify navigation with `url` / `title`.** After clicking a link or submitting a form, confirm you landed on the expected page.

9. **Save auth state for reuse.** After logging in, use `cloudrouter browser state-save <id> /tmp/auth.json` to persist cookies/storage. Reload with `state-load` in future sessions.

10. **Fall back to semantic locators.** If a page is highly dynamic and refs keep going stale, use `cloudrouter browser find <id> text "Submit" click` instead of refs.

> **Note:** `cloudrouter browser` commands run agent-browser inside the sandbox via SSH. Always use `cloudrouter browser` commands for browser automation.

## Sandbox IDs

Sandbox IDs look like `cr_abc12345`. Use the full ID when running commands. Get IDs from `cloudrouter ls` or `cloudrouter start` output.

## Common Workflows

### Create and develop in a sandbox (preferred: local-to-cloud)

```bash
cloudrouter start ./my-project                                      # Creates sandbox, uploads files
cloudrouter ssh cr_abc123 "sudo chown -R 1000:1000 /home/user/.npm" # ⚠ MUST run before any npm command
cloudrouter ssh cr_abc123 "cd /home/user/workspace && npm install"   # Install dependencies
cloudrouter code cr_abc123                                          # Open VS Code
cloudrouter pty cr_abc123                                           # Open terminal (e.g. npm run dev)
```

### GPU workflow: ML training

```bash
cloudrouter start --gpu A100 ./ml-project    # Sandbox with A100 GPU
cloudrouter pty cr_abc123                    # Open terminal
# Inside: pip install -r requirements.txt && python train.py
cloudrouter download cr_abc123 ./checkpoints # Download trained model
```

### Jupyter workflow

```bash
cloudrouter start ./notebooks         # Create sandbox
cloudrouter jupyter cr_abc123         # Open Jupyter Lab in browser
```

### File transfer workflow

```bash
cloudrouter upload cr_abc123 ./my-project     # Push local files to sandbox
# ... do work in sandbox ...
cloudrouter download cr_abc123 ./output       # Pull files from sandbox to local
```

### Browser automation: Login to a website

```bash
cloudrouter browser open cr_abc123 "https://example.com/login"
cloudrouter browser snapshot -i cr_abc123
# Output: @e1 [input type="email"] placeholder="Email"
#         @e2 [input type="password"] placeholder="Password"
#         @e3 [button] "Sign In"

cloudrouter browser fill cr_abc123 @e1 "user@example.com"
cloudrouter browser fill cr_abc123 @e2 "password123"
cloudrouter browser click cr_abc123 @e3
cloudrouter browser wait cr_abc123 2000               # Wait for navigation
cloudrouter browser snapshot -i cr_abc123              # Re-snapshot after navigation!
cloudrouter browser screenshot cr_abc123 /tmp/result.png
```

### Browser automation: Scrape data

```bash
cloudrouter browser open cr_abc123 "https://example.com/data"
cloudrouter browser wait cr_abc123 2000
cloudrouter browser snapshot -i cr_abc123     # Get interactive elements
cloudrouter browser get-text cr_abc123 @e5    # Extract specific element text
cloudrouter browser screenshot cr_abc123      # Visual capture
```

### Pause and resume workflow

```bash
cloudrouter stop cr_abc123            # Pause (preserves state)
# ... later ...
cloudrouter resume cr_abc123          # Resume where you left off
```

### Sandbox Lifecycle & Cleanup

**Concurrency limit:** Users can have a maximum of **10 concurrently running sandboxes**. If the user is approaching this limit, alert them and suggest cleaning up unused sandboxes. If they need a higher limit, they should contact **founders@manaflow.ai** (the CLI will also display this message when the limit is hit).

**Cleanup rules — be careful and deliberate:**

1. **Only touch sandboxes you created in this session.** Never stop or delete sandboxes you didn't create or don't recognize. If you see unknown sandboxes in `cloudrouter ls`, leave them alone — they may belong to the user or another workflow.

2. **Extend before cleanup.** Before stopping or deleting a sandbox you created, consider whether the user might want to inspect it. If you built something the user should see (a running app, a trained model, browser automation results, etc.), **extend the sandbox** with `cloudrouter extend <id>` so the user has time to check it out. Share the relevant URL (VS Code, VNC, Jupyter, etc.) so they can access it.
   - Use `--seconds <N>` to set a custom duration (default is 3600 = 1 hour). **Do NOT use `--timeout`** — that flag does not exist on `extend`.
   - Example: `cloudrouter extend cr_abc123 --seconds 1800` extends by 30 minutes.

3. **Stop (pause), don't delete, by default.** Prefer `cloudrouter stop <id>` over `cloudrouter delete <id>` unless the sandbox is clearly disposable (e.g., a quick test that produced no artifacts). Stopped sandboxes can be resumed with `cloudrouter resume <id>`; deleted ones are gone forever. If `cloudrouter stop` fails (the VM may have died), the sandbox is likely already dead. You can use `cloudrouter delete <id>` to clean it up if the user needs sandbox slots freed, but don't delete proactively — only when the user needs more space or explicitly asks.

4. **Clean up when you're done.** When your task is complete and the user no longer needs the sandbox, stop it. Don't leave sandboxes running indefinitely — they count toward the concurrency limit.

5. **Monitor concurrency.** Before creating a new sandbox, run `cloudrouter ls` to check how many are running. If there are 8+ active sandboxes, warn the user and ask if any can be stopped before creating another. Never silently hit the limit.

6. **If the limit is reached:** Tell the user they've hit the 10-sandbox concurrency limit. Suggest stopping sandboxes they no longer need. If they need more capacity, direct them to contact **founders@manaflow.ai** to request a higher limit.

**Cleanup workflow:**

```bash
cloudrouter ls                                   # Check running sandboxes and count
cloudrouter extend cr_abc123                     # Extend by 1 hour (default)
cloudrouter extend cr_abc123 --seconds 3600      # Extend by custom duration
# ... share URLs, let user verify ...
cloudrouter stop cr_abc123                       # Pause when done (can resume later)
cloudrouter delete cr_abc123                     # Delete only if clearly disposable
```

## Surfacing URLs and Screenshots

Proactively share authenticated sandbox URLs and screenshots with the user when it helps build trust or verify progress. The user cannot see what's happening inside the sandbox — showing them evidence of your work is important.

**When to surface URLs:**
- After creating a sandbox or setting up an environment, share the VS Code URL (`cloudrouter code <id>`) so the user can inspect the workspace
- After deploying or starting a service, share the VNC URL (`cloudrouter vnc <id>`) so the user can see it running
- When Jupyter is running, share the Jupyter URL (`cloudrouter jupyter <id>`) so the user can verify notebooks
- Whenever the user might want to verify, inspect, or interact with the sandbox themselves

**When to take and share screenshots:**
- After completing a visual task (e.g., UI changes, web app deployment) — take a screenshot with `cloudrouter browser screenshot <id> /tmp/out.png` and show it
- When something looks wrong or unexpected — screenshot it for the user to confirm
- After browser automation steps that produce visible results (form submissions, page navigations, login flows)
- When the user asks you to check or verify something visually

**General rule:** If you think the user would benefit from seeing proof of what you did, surface the URL or screenshot. Err on the side of showing more rather than less — it builds trust and keeps the user in the loop.

## Security: Dev Server URLs

**CRITICAL: NEVER share or output raw E2B port-forwarded URLs.**

When a dev server runs in the sandbox (e.g., Vite on port 5173, Next.js on port 3000), E2B creates publicly accessible URLs like `https://5173-xxx.e2b.app`. These URLs have **NO authentication** — anyone with the link can access the running application.

**Rules:**
- **NEVER** output URLs like `https://5173-xxx.e2b.app`, `https://3000-xxx.e2b.app`, or any `https://<port>-xxx.e2b.app` URL
- **NEVER** construct or guess E2B port URLs from sandbox metadata
- **ALWAYS** tell the user to view dev servers through VNC: `cloudrouter vnc <id>`
- VNC is protected by token authentication (`?tkn=`) and is the only safe way to view dev server output
- **DO** share authenticated URLs: VS Code (`cloudrouter code <id>`), VNC (`cloudrouter vnc <id>`), Jupyter (`cloudrouter jupyter <id>`) — these have proper token auth and are safe to surface

**When a dev server is started:**
```
Dev server running on port 5173
  View it in your sandbox's VNC desktop: cloudrouter vnc <id>
  (The browser inside VNC can access http://localhost:5173)
```

**NEVER do this:**
```
Frontend: https://5173-xxx.e2b.app   <- WRONG: publicly accessible, no auth
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `npm install` fails with EACCES/ENOENT errors | **ALWAYS** run `cloudrouter ssh <id> "sudo chown -R 1000:1000 /home/user/.npm"` BEFORE any npm command in a new sandbox |
| `cloudrouter ssh <id> ls -la` fails with "unknown flag" | Always quote the command: `cloudrouter ssh <id> "ls -la"` |
| `snapshot <id> -i` returns empty/wrong results | Flags go BEFORE the ID: `snapshot -i <id>` |
| Browser commands fail right after `start` | Wait a few seconds — Chrome needs time to boot |
| `find ... role button click` clicks wrong button | Use `find ... text "Button Name" click` to target by visible text |
| `extend --timeout 300` fails | Use `--seconds`: `extend <id> --seconds 300` |
| Refs from `snapshot` don't match `snapshot -i` | Don't mix modes — stick to `snapshot -i` for interactions |
| Dev server running but can't access it | Use `cloudrouter browser open <id> "http://localhost:PORT"` — don't expose E2B port URLs |
| Long-running `ssh` command hangs | Use `cloudrouter pty` for interactive/long commands, `ssh` is for quick one-offs |
| `scrollintoview @e1` fails with "Unsupported token" | `scrollintoview` and `highlight` only accept CSS selectors (e.g. `"#id"`, `".class"`), NOT `@e` refs |
| `pkill -f` kills SSH session (exit 143/255) | `pkill -f` pattern may match the SSH session. Just run another `ssh` command to recover |
| `pdf` command saves to remote path | File saves inside the sandbox (e.g. `/tmp/page.pdf`). Use `cloudrouter download` to get it locally |
| `storage-local <id> key` shows "Done" not the value | Use `eval <id> "localStorage.getItem('key')"` to reliably get a specific localStorage value |
| Stale ref error after DOM change | Always re-snapshot after clicks/form submits. Error says "timed out" — means ref is stale |
| `cloudrouter stop` fails / sandbox unreachable | The VM likely died. Use `cloudrouter delete <id>` to clean it up if you need sandbox slots freed |
| `create-next-app` hangs via `ssh` | Interactive prompts don't work in `ssh`. Use `pty` for interactive installers, or pipe input |

## Global Flags

```
-t, --team <team>   Team slug (overrides default)
-v, --verbose       Verbose output
```
