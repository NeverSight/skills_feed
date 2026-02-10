---
name: kernel-cli
description: Complete guide to Kernel CLI - cloud browser platform with automation, deployment, and management
---

# Kernel CLI

The Kernel CLI provides command-line access to Kernel's cloud browser platform for browser automation, serverless app deployment, and infrastructure management.

## Installation

- Homebrew: `brew install kernel/tap/kernel` (>=v0.13.4)
- npm: `npm install -g @onkernel/cli` (>=v0.13.4)

## Authentication

- **Preferred:** Set `KERNEL_API_KEY` environment variable
- **Fallback:** Run `kernel login` for interactive OAuth

## Quick Start

```bash
# Authenticate
export KERNEL_API_KEY=your_api_key

# Create a browser session
kernel browsers create

# Run Playwright automation
kernel browsers playwright execute <session_id> 'await page.goto("https://example.com")'

# Take a screenshot
kernel browsers computer screenshot <session_id> --to screenshot.png

# Cleanup
kernel browsers delete <session_id> --yes
```

## References

- [Browser Management](./references/browser-management.md) - Create, list, view, and delete browser sessions
- [App Deployment](./references/app-deployment.md) - Deploy TypeScript/Python apps and invoke actions
- [Computer Controls](./references/computer-controls.md) - OS-level mouse, keyboard, and screenshot capabilities
- [Process Execution](./references/process-execution.md) - Execute and manage processes in browser VMs
- [Profiles](./references/profiles.md) - Manage persistent browser profiles
- [Proxies](./references/proxies.md) - Create and manage datacenter, ISP, residential, and mobile proxies
- [Browser Pools](./references/browser-pools.md) - Manage pre-warmed browser pools
- [Extensions](./references/extensions.md) - Upload and manage Chrome extensions
- [Replays](./references/replays.md) - Record and download video replays
- [Filesystem Operations](./references/filesystem-ops.md) - Read, write, upload, and download files
