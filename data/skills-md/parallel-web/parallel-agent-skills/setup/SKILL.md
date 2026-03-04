---
name: setup
description: Set up the Parallel plugin (install CLI)
user-invocable: true
allowed-tools: Bash(curl:*), Bash(pipx:*), Bash(parallel-cli:*)
metadata:
  author: parallel
---

# Parallel Plugin Setup

## Install CLI

Try the install script first:

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

If unable to install that way, install via pip instead:

```bash
pipx install "parallel-web-tools[cli]"
pipx ensurepath
```

## Authenticate

```bash
parallel-cli login
```

## Verify

```bash
parallel-cli auth
```

If `parallel-cli` not found, add `~/.local/bin` to PATH.
