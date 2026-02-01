---
name: agentform
description: |
  Create and debug Agentform AI agent configurations (.af files). Use when:
  (1) Creating new agentform projects or workflows
  (2) Debugging agentform syntax errors
  (3) Adding MCP server integrations
  (4) Configuring agents, models, policies, or capabilities
  (5) Writing workflow steps with routing and human approval
  Agentform is "Infrastructure as Code for AI agents" - declarative .af files define agents, workflows, and policies.
---

# Agentform Skill

Create declarative AI agent configurations using Agentform's `.af` syntax.

## File Structure

Number files for alphabetical processing order:

```
project/
├── 00-project.af      # Project metadata
├── 01-variables.af    # API keys, secrets
├── 02-providers.af    # LLM providers + models
├── 03-servers.af      # MCP servers (optional)
├── 04-capabilities.af # Server capabilities (optional)
├── 05-policies.af     # Cost/timeout limits
├── 06-agents.af       # Agent definitions
├── 07-workflows.af    # Workflow definitions
└── input.yaml         # Example inputs
```

## Block Types Quick Reference

### agentform (required)

```hcl
agentform {
  version = "0.1"
  project = "my-project"
}
```

### variable

```hcl
variable "api_key" {
  type        = string
  description = "API key"
  sensitive   = true
}
```

Reference: `var.api_key`

### provider

Format: `provider "type.vendor" "name" { ... }`

```hcl
provider "llm.anthropic" "default" {
  api_key = var.anthropic_api_key
}

provider "llm.openai" "default" {
  api_key = var.openai_api_key
  default_params {
    temperature = 0.7
    max_tokens  = 2000
  }
}
```

Reference: `provider.llm.anthropic.default`

### model

```hcl
model "claude_sonnet" {
  provider = provider.llm.anthropic.default
  id       = "claude-sonnet-4-5-20250929"
}

model "gpt4o" {
  provider = provider.llm.openai.default
  id       = "gpt-4o"
  params {
    temperature = 0.5
  }
}
```

Reference: `model.claude_sonnet`

### Model IDs

**Do not hardcode model IDs.** Always fetch current model names from the provider's API documentation:

- **Anthropic**: https://docs.anthropic.com/en/docs/about-claude/models
- **OpenAI**: https://platform.openai.com/docs/models

Model IDs change with new releases. Example workflow:
1. Check provider docs for current model ID
2. Use exact ID string in your config
3. Test with `agentform validate`

### server (MCP integration)

```hcl
server "github" {
  type      = "mcp"
  transport = "stdio"
  command   = ["npx", "-y", "@modelcontextprotocol/server-github"]

  auth {
    token = var.github_token
  }
}
```

Reference: `server.github`

### capability

```hcl
capability "get_pr" {
  server      = server.github
  method      = "get_pull_request"
  side_effect = "read"
}

capability "create_review" {
  server            = server.github
  method            = "create_pull_request_review"
  side_effect       = "write"
  requires_approval = true
}
```

Reference: `capability.get_pr`

### policy

Each budget needs its own `budgets {}` block:

```hcl
policy "review_policy" {
  budgets { max_cost_usd_per_run = 0.50 }
  budgets { max_capability_calls = 15 }
  budgets { timeout_seconds = 300 }
}
```

Reference: `policy.review_policy`

### agent

```hcl
agent "reviewer" {
  model           = model.claude_sonnet
  fallback_models = [model.gpt4o]
  policy          = policy.review_policy
  allow           = [capability.get_pr, capability.create_review]

  instructions = <<EOF
You are a code reviewer.
Focus on security and performance.
EOF
}
```

Reference: `agent.reviewer`

## Heredoc Syntax (CRITICAL)

Multi-line strings use heredoc. **The closing marker MUST be at column 0** (no indentation):

```hcl
instructions = <<EOF
Line 1
Line 2
EOF
```

WRONG (will fail validation):
```hcl
  instructions = <<EOF
    Line 1
  EOF
```
The `EOF` has leading spaces - this breaks parsing.

## Expression Syntax

### References

| Type | Syntax | Example |
|------|--------|---------|
| Variable | `var.name` | `var.api_key` |
| Provider | `provider.type.name` | `provider.llm.openai.default` |
| Model | `model.name` | `model.gpt4o` |
| Agent | `agent.name` | `agent.reviewer` |
| Capability | `capability.name` | `capability.get_pr` |
| Server | `server.name` | `server.github` |
| Policy | `policy.name` | `policy.default` |
| Step | `step.name` | `step.fetch_pr` |

### State References (in workflows)

| Context | Syntax |
|---------|--------|
| Workflow input | `input.field` |
| Step output | `state.step_output` |
| Nested field | `state.review.response` |
| Result in step | `result.text`, `result.data` |

### Operators

```hcl
// Comparison
condition = state.value == "expected"
condition = state.count > 10

// Logical
condition = state.a && state.b
condition = !state.flag

// Ternary
value = state.premium ? "gold" : "standard"
```

**NO FUNCTION CALLS** - `contains()`, `length()` etc. are NOT supported.

## Workflow Reference

See [references/workflows.md](references/workflows.md) for complete workflow patterns.

## CLI Commands

```bash
# Validate
agentform validate --var api_key=$API_KEY

# Run workflow
agentform run workflow_name \
  --var api_key=$API_KEY \
  --input '{"field": "value"}'

# Verbose
agentform run workflow_name --verbose
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| Unexpected token `<` | Heredoc `EOF` indented | Move `EOF` to column 0 |
| Unexpected token `(` | Function call used | Use comparison operators |
| Variable has no value | Missing runtime var | Add `--var name=value` |
| MCP server not found | Wrong package name | Check npm package exists |

## Common MCP Servers

- `@modelcontextprotocol/server-github`
- `@modelcontextprotocol/server-filesystem`

## Templates

Copy these pre-validated templates as starting points:

### Simple Agent (no MCP)
```bash
cp -r ~/.claude/skills/agentform/assets/templates/simple-agent ./my-agent
```

### MCP Agent (GitHub PR reviewer)
```bash
cp -r ~/.claude/skills/agentform/assets/templates/mcp-agent ./my-pr-reviewer
```
