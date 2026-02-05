---
name: codex
description: |
  OpenAI Codex - AI-powered coding agent for CLI, IDE, and cloud automation.
  Use when working with Codex CLI, IDE extension, cloud environments, configuration, security, MCP integration, skills, or automation workflows.
  Keywords: codex, openai, ai-coding-agent, cli, ide-extension, vs-code, cloud-automation, mcp, agent-skills, configuration, security, sandbox, github-integration, slash-commands, code-review, automation.
compatibility: Node.js (for CLI install via npm), macOS/Linux (Windows via WSL2)
metadata:
  source: https://developers.openai.com/llms.txt
  total_docs: 44
  generated: 2026-01-13T19:30:00Z
---

# OpenAI Codex

> OpenAI's coding agent for software development. Reads, edits, and runs code locally or in the cloud. Included with ChatGPT Plus, Pro, Business, Edu, and Enterprise plans.

## Quick Start

```bash
# Install CLI with npm
npm install -g @openai/codex

# Or with Homebrew
brew install codex

# Start interactive session
codex
```

For IDE: Install extension from VS Code Marketplace (`openai.chatgpt`) or download for:
- Visual Studio Code: `vscode:extension/openai.chatgpt`
- Cursor: `cursor:extension/openai.chatgpt`
- Windsurf: `windsurf:extension/openai.chatgpt`

For Cloud: Go to [chatgpt.com/codex](https://chatgpt.com/codex)

## Installation

### CLI
```bash
npm install -g @openai/codex
# or
brew install codex
```

### IDE Extension
Install from VS Code Marketplace: [openai.chatgpt](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)

### Cloud
Access at [chatgpt.com/codex](https://chatgpt.com/codex)

## Documentation

Full documentation in `docs/`. See `docs/000-index.md` for navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| **Getting Started** | 001-003 | Overview, quickstart, and installation |
| **Security** | 004-006 | Authentication, security architecture, and access control |
| **Configuration** | 007-016 | Basic and advanced configuration for all platforms |
| **CLI** | 017-020 | Command-line interface usage and commands |
| **IDE** | 011-012, 021-023 | VS Code extension features and commands |
| **Cloud** | 024-025 | Cloud environments and web interface |
| **Integrations** | 016, 026-027 | GitHub, Linear, and Slack integrations |
| **Usage** | 028-031 | Prompting, workflows, and platform-specific guides |
| **Advanced** | 032-037 | Skills, automation, CI/CD, and MCP |
| **Reference** | 038-041 | Models, pricing, SDK, and open-source |
| **Enterprise** | 042-043 | Enterprise administration and team building |

### By Keyword

| Keyword | File |
|---------|------|
| authentication | `docs/004-codex-auth.md` |
| api-key | `docs/004-codex-auth.md` |
| mfa | `docs/004-codex-auth.md` |
| security | `docs/005-codex-security.md` |
| sandbox | `docs/005-codex-security.md`, `docs/015-codex-rules.md` |
| internet-access | `docs/006-codex-cloud-internet-access.md` |
| config.toml | `docs/007-codex-config-basic.md`, `docs/009-codex-config-reference.md` |
| configuration | `docs/007-codex-config-basic.md`, `docs/010-codex-config-advanced.md` |
| sample-config | `docs/008-codex-config-sample.md` |
| ide-settings | `docs/011-codex-ide-settings.md` |
| vs-code | `docs/012-codex-ide.md` |
| agents-md | `docs/013-codex-guides-agents-md.md` |
| mcp | `docs/014-codex-mcp.md` |
| rules | `docs/015-codex-rules.md` |
| starlark | `docs/015-codex-rules.md` |
| slack | `docs/016-codex-integrations-slack.md` |
| cli | `docs/017-codex-cli.md` |
| cli-reference | `docs/018-codex-cli-reference.md` |
| cli-features | `docs/019-codex-cli-features.md` |
| slash-commands | `docs/020-codex-cli-slash-commands.md`, `docs/023-codex-ide-slash-commands.md` |
| ide-commands | `docs/021-codex-ide-commands.md` |
| ide-features | `docs/022-codex-ide-features.md` |
| cloud | `docs/024-codex-cloud.md` |
| environments | `docs/025-codex-cloud-environments.md` |
| github | `docs/026-codex-integrations-github.md` |
| linear | `docs/027-codex-integrations-linear.md` |
| prompting | `docs/028-codex-prompting.md` |
| custom-prompts | `docs/029-codex-custom-prompts.md` |
| workflows | `docs/030-codex-workflows.md` |
| windows | `docs/031-codex-windows.md` |
| wsl | `docs/031-codex-windows.md` |
| skills | `docs/032-codex-skills.md` |
| create-skill | `docs/033-codex-skills-create-skill.md` |
| feature-maturity | `docs/034-codex-feature-maturity.md` |
| non-interactive | `docs/035-codex-noninteractive.md` |
| ci-cd | `docs/035-codex-noninteractive.md`, `docs/036-codex-github-action.md` |
| github-action | `docs/036-codex-github-action.md` |
| agents-sdk | `docs/037-codex-guides-agents-sdk.md` |
| models | `docs/038-codex-models.md` |
| pricing | `docs/039-codex-pricing.md` |
| sdk | `docs/040-codex-sdk.md` |
| typescript-sdk | `docs/040-codex-sdk.md` |
| open-source | `docs/041-codex-open-source.md` |
| enterprise | `docs/042-codex-enterprise.md` |
| ai-native-team | `docs/043-codex-guides-build-ai-native-engineering-team.md` |

### Learning Path

1. **Foundation**: Start with `docs/001-003` for intro and setup
2. **Core**: Security (`docs/004-006`), Configuration (`docs/007-016`)
3. **Practical**: CLI (`docs/017-020`), IDE (`docs/021-023`), Workflows (`docs/028-030`)
4. **Advanced**: Skills (`docs/032-033`), Automation (`docs/035-037`), MCP (`docs/014`)
5. **Reference**: Models (`docs/038`), Pricing (`docs/039`), SDK (`docs/040`)

## Common Tasks

### Install and Authenticate
-> `docs/003-codex-quickstart.md` (Installation across all platforms)
-> `docs/004-codex-auth.md` (Authentication methods)

### Configure Codex
-> `docs/007-codex-config-basic.md` (Basic config.toml setup)
-> `docs/009-codex-config-reference.md` (Complete configuration reference)
-> `docs/008-codex-config-sample.md` (Sample configuration file)

### Use CLI
-> `docs/017-codex-cli.md` (CLI overview)
-> `docs/018-codex-cli-reference.md` (Command line options)
-> `docs/020-codex-cli-slash-commands.md` (Slash commands)

### Use IDE Extension
-> `docs/012-codex-ide.md` (Setup and overview)
-> `docs/021-codex-ide-commands.md` (Commands and keybindings)
-> `docs/022-codex-ide-features.md` (Features)

### Set Up Security and Rules
-> `docs/005-codex-security.md` (Security architecture)
-> `docs/015-codex-rules.md` (Command rules with Starlark)

### Integrate with MCP
-> `docs/014-codex-mcp.md` (Model Context Protocol setup)

### Create Custom Skills
-> `docs/032-codex-skills.md` (Skills overview)
-> `docs/033-codex-skills-create-skill.md` (Create custom skills)

### Run in CI/CD
-> `docs/035-codex-noninteractive.md` (Non-interactive mode)
-> `docs/036-codex-github-action.md` (GitHub Action)

### Use AGENTS.md
-> `docs/013-codex-guides-agents-md.md` (Custom instructions)

### Integrate with GitHub/Linear/Slack
-> `docs/026-codex-integrations-github.md` (GitHub integration)
-> `docs/027-codex-integrations-linear.md` (Linear integration)
-> `docs/016-codex-integrations-slack.md` (Slack integration)
