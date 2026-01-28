---
name: vm0-cli
description: VM0 CLI for building and running AI agents in secure sandboxes. Use this skill when users need to install vm0, create agent projects, deploy agents, run agents, manage volumes/artifacts, or schedule agent runs.
vm0_secrets:
  - VM0_TOKEN
---

# VM0 CLI

Build and run AI agents in secure sandboxed environments using the VM0 command-line interface.

> Official docs: https://docs.vm0.ai

---

## When to Use

Use this skill when you need to:

- Install and set up the VM0 CLI
- Create and configure AI agent projects
- Deploy agents to the VM0 platform
- Run agents with prompts and inputs
- Manage input files (volumes) and output files (artifacts)
- Schedule recurring agent runs
- View logs and usage statistics

---

## Prerequisites

### Installation

Install the VM0 CLI globally via npm:

```bash
npm install -g @vm0/cli
```

Verify installation:

```bash
vm0 --version
```

### Authentication

Log in to your VM0 account:

```bash
vm0 auth login
```

This opens a browser for authentication. After login, verify status:

```bash
vm0 auth status
```

For CI/CD environments, get your API token:

```bash
vm0 auth setup-token
```

Then set the environment variable:

```bash
export VM0_TOKEN=vm0_live_your-api-key
```

---

## Quick Start

### 1. Initialize a Project

Create a new VM0 project in the current directory:

```bash
vm0 init
```

This creates a `vm0.yaml` configuration file interactively. For non-interactive mode:

```bash
vm0 init --name my-agent
```

### 2. Configure the Agent

Edit `vm0.yaml` to define your agent:

```yaml
version: "1.0"

agents:
  my-agent:
    framework: claude-code
    instructions: AGENTS.md
    skills:
      - https://github.com/vm0-ai/vm0-skills/tree/main/github
    environment:
      DEBUG: "${{ vars.DEBUG }}"
      API_KEY: "${{ secrets.API_KEY }}"
```

### 3. Deploy the Agent

Deploy your agent configuration:

```bash
vm0 compose vm0.yaml
```

Skip confirmation prompts with `-y`:

```bash
vm0 compose vm0.yaml -y
```

### 4. Run the Agent

Execute the agent with a prompt:

```bash
vm0 run my-agent "Please analyze the codebase and suggest improvements"
```

Or use `cook` for one-click execution from `vm0.yaml`:

```bash
vm0 cook "Analyze the code"
```

---

## Core Operations

### Running Agents

**Basic run:**

```bash
vm0 run my-agent "Your prompt here"
```

**Run with variables and secrets:**

```bash
vm0 run my-agent "Process data" --vars DEBUG=true --secrets API_KEY=xxx
```

**Run with artifact storage:**

```bash
vm0 run my-agent "Generate report" --artifact-name my-output
```

**Run with input volumes:**

```bash
vm0 run my-agent "Process files" --volume-version input-data=latest
```

**Enable verbose output:**

```bash
vm0 run my-agent "Hello" -v
```

**Resume from checkpoint:**

```bash
vm0 run resume <checkpoint-id> "Continue the task"
```

**Continue from session:**

```bash
vm0 run continue <session-id> "Next step"
```

### One-Click Execution (cook)

Run directly from `vm0.yaml` in current directory:

```bash
vm0 cook "Your prompt"
```

Skip confirmation:

```bash
vm0 cook -y "Your prompt"
```

Continue last session:

```bash
vm0 cook continue "Follow up"
```

Resume from last checkpoint:

```bash
vm0 cook resume "Continue"
```

View logs from last cook run:

```bash
vm0 cook logs
```

### Viewing Logs

**View agent events (default):**

```bash
vm0 logs <run-id>
```

**View system logs:**

```bash
vm0 logs <run-id> --system
```

**View metrics:**

```bash
vm0 logs <run-id> --metrics
```

**View network logs:**

```bash
vm0 logs <run-id> --network
```

**Filter by time:**

```bash
vm0 logs <run-id> --since 5m
vm0 logs <run-id> --since 2h
vm0 logs <run-id> --since 2024-01-15T10:30:00Z
```

**Show last N entries:**

```bash
vm0 logs <run-id> --tail 20
```

---

## Storage Management

### Volumes (Input Files)

Volumes store input files that agents can read.

**Initialize a volume (interactive):**

```bash
cd my-data-directory
vm0 volume init
```

**Initialize a volume (non-interactive):**

```bash
cd my-data-directory
vm0 volume init --name my-data
```

**Push local files to cloud:**

```bash
vm0 volume push
```

**Pull cloud files to local:**

```bash
vm0 volume pull
```

**Pull specific version:**

```bash
vm0 volume pull abc123de
```

**Check volume status:**

```bash
vm0 volume status
```

**List all volumes:**

```bash
vm0 volume list
```

**Clone a remote volume:**

```bash
vm0 volume clone my-volume ./local-dir
```

### Artifacts (Output Files)

Artifacts store output files created by agents.

**Initialize an artifact (interactive):**

```bash
cd my-output-directory
vm0 artifact init
```

**Initialize an artifact (non-interactive):**

```bash
cd my-output-directory
vm0 artifact init --name my-output
```

**Push local files to cloud:**

```bash
vm0 artifact push
```

**Pull cloud files to local:**

```bash
vm0 artifact pull
```

**Pull specific version:**

```bash
vm0 artifact pull abc123de
```

**Check artifact status:**

```bash
vm0 artifact status
```

**List all artifacts:**

```bash
vm0 artifact list
```

**Clone a remote artifact:**

```bash
vm0 artifact clone my-artifact ./local-dir
```

---

## Agent Management

### List Agents

```bash
vm0 agent list
```

With details:

```bash
vm0 agent list --verbose
```

### Inspect Agent

View agent configuration:

```bash
vm0 agent inspect my-agent
```

View specific version:

```bash
vm0 agent inspect my-agent:abc123
```

---

## Scheduling

Create scheduled agent runs with cron expressions.

### Initialize Schedule

**Interactive mode:**

```bash
vm0 schedule init
```

**Non-interactive mode:**

```bash
vm0 schedule init --name my-schedule --frequency daily --time 09:00 --prompt "Run daily task"
```

### Deploy Schedule

```bash
vm0 schedule deploy schedule.yaml
```

Or deploy from default file:

```bash
vm0 schedule deploy
```

### Manage Schedules

**List all schedules:**

```bash
vm0 schedule list
```

**View schedule status:**

```bash
vm0 schedule status my-schedule
```

**Enable a schedule:**

```bash
vm0 schedule enable my-schedule
```

**Disable a schedule:**

```bash
vm0 schedule disable my-schedule
```

**Delete a schedule (with confirmation):**

```bash
vm0 schedule delete my-schedule
```

**Delete a schedule (non-interactive):**

```bash
vm0 schedule delete my-schedule --force
```

---

## Scope Management

Scopes are namespaces for organizing your agents and resources.

**View current scope:**

```bash
vm0 scope status
```

**Set scope:**

```bash
vm0 scope set my-team
```

---

## Usage Statistics

View your usage statistics:

```bash
vm0 usage
```

**Filter by date range:**

```bash
vm0 usage --since 7d
vm0 usage --since 30d
vm0 usage --since 2024-01-01 --until 2024-01-31
```

---

## Model Provider Configuration

Manage LLM model providers for agent runs.

**List providers:**

```bash
vm0 model-provider list
```

**Setup a provider (interactive):**

```bash
vm0 model-provider setup
```

**Setup a provider (non-interactive):**

```bash
vm0 model-provider setup --type anthropic-api-key --credential "sk-ant-xxx"
```

**Set default provider:**

```bash
vm0 model-provider set-default anthropic-api-key
```

**Delete a provider:**

```bash
vm0 model-provider delete anthropic-api-key
```

---

## Credential Management (Experimental)

Store credentials for agent runs.

**List credentials:**

```bash
vm0 experimental-credential list
```

**Set a credential:**

```bash
vm0 experimental-credential set MY_API_KEY "secret-value"
```

**Delete a credential:**

```bash
vm0 experimental-credential delete MY_API_KEY
```

---

## vm0.yaml Reference

### Basic Structure

```yaml
version: "1.0"

agents:
  agent-name:
    framework: claude-code
    instructions: AGENTS.md
    skills:
      - https://github.com/vm0-ai/vm0-skills/tree/main/github
      - https://github.com/vm0-ai/vm0-skills/tree/main/slack
    environment:
      VAR_NAME: "value"
      SECRET_VAR: "${{ secrets.SECRET_NAME }}"
      CONFIG_VAR: "${{ vars.CONFIG_NAME }}"
```

### Fields

| Field | Description |
|-------|-------------|
| `version` | Configuration version (currently "1.0") |
| `agents` | Map of agent definitions |
| `framework` | Agent framework (e.g., `claude-code`) |
| `instructions` | Path to instructions file |
| `skills` | List of skill URLs to include |
| `environment` | Environment variables for the agent |

### Variable Syntax

- `${{ secrets.NAME }}` - Sensitive values stored securely
- `${{ vars.NAME }}` - Non-sensitive configuration values
- Direct values - Plain text values

---

## Environment Information

View system and environment details:

```bash
vm0 info
```

---

## Non-Interactive Mode (CI/CD)

All commands support non-interactive mode for use in CI/CD pipelines, scripts, and automated environments. The CLI detects non-TTY environments (`process.stdout.isTTY === false`) and requires explicit flags for all inputs.

### Authentication

Set the `VM0_TOKEN` environment variable instead of interactive login:

```bash
export VM0_TOKEN=vm0_live_your-api-key
```

### Command Reference

| Command | Non-Interactive Flags | Notes |
|---------|----------------------|-------|
| `vm0 init` | `--name <name>` | Required in non-TTY |
| `vm0 compose` | `-y, --yes` | Skip new secrets confirmation |
| `vm0 cook` | `-y, --yes` | Skip all confirmation prompts |
| `vm0 volume init` | `--name <name>` | Required in non-TTY |
| `vm0 artifact init` | `--name <name>` | Required in non-TTY |
| `vm0 schedule init` | `--name`, `--frequency`, `--time`, `--prompt` | All required; `--day` for weekly/monthly |
| `vm0 schedule delete` | `-f, --force` | Skip deletion confirmation |
| `vm0 model-provider setup` | `--type <type> --credential <value>` | Both required together |

### CI/CD Example

```bash
# Set authentication
export VM0_TOKEN=${{ secrets.VM0_TOKEN }}

# Initialize project (non-interactive)
vm0 init --name my-agent --force

# Initialize storage (non-interactive)
cd input-data && vm0 volume init --name input-data && cd ..
cd artifact && vm0 artifact init --name artifact && cd ..

# Deploy agent (skip confirmation)
vm0 compose vm0.yaml -y

# Run agent
vm0 run my-agent --artifact-name artifact "Execute the task"
```

### GitHub Actions Example

```yaml
jobs:
  run-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install VM0 CLI
        run: npm install -g @vm0/cli

      - name: Run Agent
        env:
          VM0_TOKEN: ${{ secrets.VM0_TOKEN }}
        run: |
          vm0 compose vm0.yaml -y
          vm0 run my-agent --artifact-name output "Generate daily report"
```

### Schedule Init (Non-Interactive)

Create schedules without prompts:

```bash
# Daily schedule
vm0 schedule init \
  --name daily-report \
  --frequency daily \
  --time 09:00 \
  --timezone America/New_York \
  --prompt "Generate daily report" \
  --force

# Weekly schedule (Monday)
vm0 schedule init \
  --name weekly-summary \
  --frequency weekly \
  --day mon \
  --time 09:00 \
  --timezone UTC \
  --prompt "Generate weekly summary" \
  --force

# Monthly schedule (1st of month)
vm0 schedule init \
  --name monthly-report \
  --frequency monthly \
  --day 1 \
  --time 09:00 \
  --timezone UTC \
  --prompt "Generate monthly report" \
  --force
```

### Model Provider Setup (Non-Interactive)

```bash
vm0 model-provider setup --type anthropic-api-key --credential "sk-ant-xxx"
```

---

## Guidelines

1. **Always authenticate first** - Run `vm0 auth login` before using other commands
2. **Use `vm0 init` for new projects** - Creates proper project structure
3. **Deploy before running** - Run `vm0 compose` after modifying `vm0.yaml`
4. **Use volumes for input data** - Push data files as volumes before running agents
5. **Check logs for debugging** - Use `vm0 logs` to troubleshoot failed runs
6. **Use scopes for organization** - Set appropriate scope for team collaboration

---

## Common Workflows

### Deploy and Run Agent

```bash
# 1. Initialize project
vm0 init --name my-agent

# 2. Edit vm0.yaml and AGENTS.md

# 3. Deploy configuration
vm0 compose vm0.yaml

# 4. Run the agent
vm0 run my-agent "Execute the task"

# 5. Check logs if needed
vm0 logs <run-id>
```

### Provide Input Files to Agent

```bash
# 1. Create and navigate to data directory
mkdir input-data && cd input-data

# 2. Add your files
cp ~/documents/*.pdf .

# 3. Initialize and push volume (use --name for non-interactive)
vm0 volume init --name input-data
vm0 volume push

# 4. Run agent with volume
cd ..
vm0 run my-agent "Process the documents" --volume-version input-data=latest
```

### Download Agent Output

```bash
# 1. List artifacts
vm0 artifact list

# 2. Clone the artifact locally
vm0 artifact clone my-output ./results

# 3. Or pull to existing directory
cd my-output-dir
vm0 artifact pull
```

---

## Troubleshooting

### Authentication Issues

```bash
# Check auth status
vm0 auth status

# Re-login if needed
vm0 auth logout
vm0 auth login
```

### Agent Not Found

```bash
# List available agents
vm0 agent list

# Check if deployed
vm0 compose vm0.yaml
```

### View Detailed Errors

```bash
# Use verbose mode
vm0 run my-agent "prompt" -v

# Check system logs
vm0 logs <run-id> --system
```
