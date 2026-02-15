---
name: linear-config
description: Configure linear-cli. Use for auth, API keys, workspaces, and diagnostics.
allowed-tools: Bash
---

# Configuration

```bash
# Set API key
linear-cli config set-key YOUR_API_KEY

# Show config
linear-cli config show

# Auth commands
linear-cli auth login                # Store API key
linear-cli auth status               # Check auth status
linear-cli auth logout               # Remove key

# Workspaces
linear-cli config workspace-add work KEY
linear-cli config workspace-list
linear-cli config workspace-switch work
linear-cli config workspace-current

# Profiles
linear-cli --profile work i list     # Use profile

# Diagnostics
linear-cli doctor                    # Check config and connectivity

# Shell completions
linear-cli config completions bash > ~/.bash_completion.d/linear-cli
linear-cli config completions zsh > ~/.zfunc/_linear-cli
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `LINEAR_API_KEY` | API key override |
| `LINEAR_CLI_PROFILE` | Profile override |
| `LINEAR_CLI_OUTPUT` | Default output format |
