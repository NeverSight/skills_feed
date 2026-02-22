---
name: quickstart
description: "Set up Databricks agent development environment. Use when: (1) First time setup, (2) Configuring Databricks authentication, (3) User says 'quickstart', 'set up', 'authenticate', or 'configure databricks', (4) No .env file exists."
---

# Quickstart & Authentication

## Prerequisites

- **uv** (Python package manager)
- **nvm** with Node 20 (for frontend)
- **Databricks CLI v0.283.0+**

Check CLI version:
```bash
databricks -v  # Must be v0.283.0 or above
brew upgrade databricks  # If version is too old
```

## Run Quickstart

```bash
uv run quickstart
```

**Options:**
- `--profile NAME`: Use specified profile (non-interactive)
- `--host URL`: Workspace URL for initial setup
- `-h, --help`: Show help

**Examples:**
```bash
# Interactive (prompts for profile selection)
uv run quickstart

# Non-interactive with existing profile
uv run quickstart --profile DEFAULT

# New workspace setup
uv run quickstart --host https://your-workspace.cloud.databricks.com
```

## What Quickstart Configures

Creates/updates `.env` with:
- `DATABRICKS_CONFIG_PROFILE` - Selected CLI profile
- `MLFLOW_TRACKING_URI` - Set to `databricks://<profile-name>` for local auth
- `MLFLOW_EXPERIMENT_ID` - Auto-created experiment ID

## Manual Authentication (Fallback)

If quickstart fails:

```bash
# Create new profile
databricks auth login --host https://your-workspace.cloud.databricks.com

# Verify
databricks auth profiles
```

Then manually create `.env` (copy from `.env.example`):
```bash
# Authentication (choose one method)
DATABRICKS_CONFIG_PROFILE=DEFAULT
# DATABRICKS_HOST=https://<your-workspace-here>.databricks.com
# DATABRICKS_TOKEN=dapi....

# MLflow configuration
MLFLOW_EXPERIMENT_ID=<your-experiment-id>
MLFLOW_TRACKING_URI="databricks://DEFAULT"
MLFLOW_REGISTRY_URI="databricks-uc"

# Frontend proxy settings
CHAT_APP_PORT=3000
CHAT_PROXY_TIMEOUT_SECONDS=300
```

## Next Steps

After quickstart completes:
1. Run `uv run discover-tools` to find available workspace resources (see **discover-tools** skill)
2. Run `uv run start-app` to test locally (see **run-locally** skill)
