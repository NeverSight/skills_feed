---
name: flipside
description: |
  Query blockchain data across 40+ chains, create AI agents for crypto analytics,
  and build automated data pipelines. Use when working with blockchain data,
  crypto wallets, DeFi protocols, NFTs, token transfers, or on-chain analytics.
  Requires the Flipside CLI (https://docs.flipsidecrypto.xyz/get-started/cli).
compatibility: Requires flipside CLI installed and authenticated (flipside login)
allowed-tools: Bash(flipside:*) Read Write
metadata:
  author: flipside
  version: "1.1"
  homepage: https://flipsidecrypto.xyz
---

# Flipside CLI

Query blockchain data, create AI agents, and build automated data pipelines.

## First Steps

**Always start by checking what's available in the user's organization:**

```bash
# 1. Verify authentication and see the current org
flipside whoami

# 2. List available agents (names vary by org)
flipside agents list

# 3. List available skills
flipside skills list
```

Agent and skill names are organization-specific. Always run `flipside agents list` to discover what agents are available before trying to use them.

## Golden Rule

**Use Flipside agents for SQL queries.** Don't write SQL from scratch—let the agents generate correct queries against Flipside's data warehouse.

```bash
# One-shot query (no session memory)
flipside agents run <org>/<agent_name> --message "Get the top 10 DEX swaps on Ethereum today"

# Multi-turn conversation (maintains context between messages)
flipside chat create  # get session ID
flipside chat send-message --session-id <id> "Get top DEX swaps on Ethereum"
flipside chat send-message --session-id <id> "Now filter to only Uniswap"

# Always use --title when testing (makes sessions easier to find)
flipside agents run <org>/<agent_name> --message "test query" --title "Testing from Claude Code"
```

## Primary Workflows

### One-Shot Queries (agents run)

For single queries without session memory, use `flipside agents run`:

```bash
# First, list available agents to find the right one
flipside agents list

# Run a chat agent with a message
flipside agents run <org>/<agent_name> --message "Show me the largest ETH transfers today"

# Run a sub agent with structured JSON input
flipside agents run <org>/<agent_name> --data-json '{"chain": "ethereum", "limit": 10}'

# Add a title for easier session tracking
flipside agents run <org>/<agent_name> --message "Query request" --title "My analysis"
```

**IMPORTANT:** Agent names MUST use the `org/agent_name` format. Get the exact names from `flipside agents list`.

### Multi-Turn Conversations (chat)

For conversations that need session memory (follow-up questions, context from previous messages), use chat:

```bash
# Create a new chat session
flipside chat create
# Returns: Session ID: abc123...

# Send messages to the session (maintains context)
flipside chat send-message --session-id <session-id> "What were the top DEX swaps on Ethereum yesterday?"

# Follow up (the session remembers previous context)
flipside chat send-message --session-id <session-id> "Now show me the same for Arbitrum"

# List your sessions
flipside chat list

# Resume an existing session interactively
flipside chat resume
```

Use chat when you need:
- Follow-up questions that reference previous answers
- Multi-step analysis where context matters
- Building on previous query results

### Running SQL Directly

For known queries, you can run SQL directly:

```bash
# Create and execute a query
flipside query create "SELECT * FROM ethereum.core.fact_blocks LIMIT 10"

# Execute an existing saved query
flipside query execute <query-id>

# Get results from a query run
flipside query-run result <run-id>
```

## Command Reference

### Agents

```bash
flipside agents list                              # List available agents
flipside agents init my_agent                     # Create agent YAML template
flipside agents validate my_agent.agent.yaml      # Validate before deploy
flipside agents push my_agent.agent.yaml          # Deploy agent
flipside agents run <org>/<agent> --message "..." # Run chat agent
flipside agents run <org>/<agent> --data-json '{}' # Run sub agent
flipside agents describe <org>/<agent>            # Show agent details
flipside agents pull <org>/<agent>                # Download agent YAML
flipside agents delete <org>/<agent>              # Delete an agent
```

### Chat

```bash
flipside chat                                     # Start interactive chat
flipside chat --run <run-id>                      # Chat about an automation run
flipside chat resume                              # Resume previous chat
flipside chat list                                # List chat sessions
flipside chat send-message --session-id <id> "x" # Programmatic message
```

### Queries

```bash
flipside query create "SELECT ..."                # Create saved query
flipside query list                               # List saved queries
flipside query get <query-id>                     # Get query details
flipside query execute <query-id>                 # Execute query (creates run)
flipside query runs <query-id>                    # List runs for a query
flipside query-run result <run-id>                # Get query results
flipside query-run status <run-id>                # Check run status
flipside query-run poll <run-id>                  # Poll until complete
```

### Automations

```bash
flipside automations list                         # List automations
flipside automations init my_pipeline             # Create automation YAML
flipside automations validate <file>              # Validate before deploy
flipside automations push <file>                  # Deploy automation
flipside automations run <id>                     # Trigger automation
flipside automations run <id> -i '{"key":"val"}'  # Run with inputs
flipside automations runs list <id>               # List runs
flipside automations runs result <run-id>         # Get run results
```

### Skills

```bash
flipside skills list                              # List available skills
flipside skills init my_skill                     # Create skill YAML
flipside skills push my_skill.skill.yaml          # Deploy skill
```

### Utilities

```bash
flipside whoami                                   # Show current user/org
flipside --help                                   # Full command help
flipside <command> --help                         # Help for specific command
flipside update                                   # Update CLI to latest version
```

## When to Load References

Load the detailed reference files when you need:

- **[AGENTS.md](references/AGENTS.md)** - Agent YAML schema, chat vs sub agents, deployment
- **[AUTOMATIONS.md](references/AUTOMATIONS.md)** - Pipeline steps, DAG edges, scheduling
- **[SKILLS.md](references/SKILLS.md)** - Creating reusable tool bundles
- **[TABLES.md](references/TABLES.md)** - Common tables by chain (Ethereum, Solana, etc.)
- **[QUERIES.md](references/QUERIES.md)** - SQL patterns, result handling

## Creating New Agents

```bash
# 1. Create a template
flipside agents init my_agent

# 2. Edit the generated YAML file
# my_agent.agent.yaml

# 3. Validate before deploying
flipside agents validate my_agent.agent.yaml

# 4. Deploy
flipside agents push my_agent.agent.yaml
```

## Templates

Starter templates are available in `assets/`:

- `assets/agent.template.yaml` - Basic agent config
- `assets/automation.template.yaml` - Basic automation config
- `assets/skill.template.yaml` - Basic skill config

Copy and customize these for new projects.

## Troubleshooting

If a command fails:

1. Check authentication: `flipside whoami`
2. Check CLI version: `flipside --version` and `flipside update`
3. Use verbose mode: `flipside --verbose <command>`
4. Check JSON output for details: `flipside --json <command>`
