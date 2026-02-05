---
name: factory-droid
description: |
  Factory Droid - AI-native software development platform with CLI and desktop app.
  Use when working with Factory's Droid CLI, configuring AI agents, setting up AGENTS.md, 
  customizing models (BYOK), creating hooks, skills, or custom slash commands.
  Keywords: droid, factory-ai, cli, ai-agent, AGENTS.md, byok, custom-models, hooks, 
  skills, specification-mode, auto-run, enterprise, mcp, github-integration, code-review.
compatibility: Node.js, any terminal. Supports macOS, Linux, Windows.
metadata:
  source: https://docs.factory.ai/sitemap.xml
  total_docs: 98
  generated: 2026-01-13T19:04:00Z
---

# Factory Droid

> Factory is an AI-native software development platform that works everywhere you do. From IDE to CI/CD - delegate complete tasks like refactors, incident response, and migrations to Droids without changing your tools, models, or workflow.

## Quick Start

```bash
# Navigate to your project directory
cd your-project

# Start the droid CLI
droid

# Explore your codebase
> analyze this codebase and explain the overall architecture

# Make your first change
> add comprehensive logging to the main application startup
```

## Installation

Download and install from [factory.ai](https://factory.ai), then run `droid` in your terminal.

## Key Features

- **Model-agnostic**: OpenAI, Anthropic, Google, X AI, open-source or local models
- **Context-confidence**: Compresses incrementally with anchor points for near-perfect context
- **Specification mode**: Detailed implementation, technical details and mixed model support
- **Enterprise-ready**: SSO + SAML, dedicated compute, compliance & security

## Documentation

Full documentation in `docs/`. See `docs/000-index.md` for detailed navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Getting Started | 001-006, 011-019 | Introduction, quickstart, common use cases |
| Configuration | 041-050 | Settings, AGENTS.md, custom droids, hooks, MCP |
| Custom Models (BYOK) | 051-060 | OpenAI, Anthropic, Gemini, Groq, Ollama, etc. |
| Skills | 027, 061-068 | Reusable agent capabilities and domain expertise |
| User Features | 071-080 | Model selection, spec mode, auto-run, code review |
| Power User | 091-095 | Setup checklist, memory, conventions, token efficiency |
| Tutorials | 101-116 | Droid Exec, hooks automation, GitHub Actions |
| Enterprise | 121-128 | Security, deployment, SSO, compliance |
| API Reference | 136-143 | CLI reference, hooks, REST API |
| Changelog | 156-159 | Version history and release notes |

### By Keyword

| Keyword | File |
|---------|------|
| AGENTS.md | `042-cli-configuration-agents-md.md` |
| auto-run | `074-cli-user-guides-auto-run.md` |
| autonomy-level | `041-cli-configuration-settings.md` |
| BYOK | `051-cli-byok-overview.md` |
| CLI reference | `136-reference-cli-reference.md` |
| code-review | `076-cli-features-code-review.md` |
| custom-droids | `043-cli-configuration-custom-droids.md` |
| custom-models | `051-060` (BYOK section) |
| droid-exec | `080-cli-droid-exec-overview.md` |
| droid-shield | `078-cli-account-droid-shield.md` |
| enterprise | `121-enterprise.md` |
| gemini | `053-cli-byok-google-gemini.md` |
| github-actions | `104-guides-droid-exec-github-actions.md` |
| github-app | `016-integrations-github-app.md` |
| groq | `055-cli-byok-groq.md` |
| hooks | `045-cli-configuration-hooks-guide.md` |
| hooks-reference | `137-reference-hooks-reference.md` |
| ide-integration | `017-integrations-ide-integrations.md` |
| linear | `019-integrations-linear.md` |
| mcp | `046-cli-configuration-mcp.md` |
| memory | `092-guides-power-user-memory-management.md` |
| model-selection | `071-cli-user-guides-choosing-your-model.md` |
| ollama | `060-cli-byok-ollama.md` |
| openai | `052-cli-byok-openai-anthropic.md` |
| openrouter | `059-cli-byok-openrouter.md` |
| prompt-engineering | `094-guides-power-user-prompt-crafting.md` |
| quickstart-cli | `012-cli-getting-started-quickstart.md` |
| quickstart-web | `011-web-getting-started-quickstart.md` |
| readiness-report | `077-cli-features-readiness-report.md` |
| security | `026-cli-account-security.md` |
| settings | `041-cli-configuration-settings.md` |
| skills | `027-cli-configuration-skills.md` |
| slack | `018-integrations-slack.md` |
| slash-commands | `044-cli-configuration-custom-slash-commands.md` |
| specification-mode | `073-cli-user-guides-specification-mode.md` |
| sso | `123-enterprise-identity-sso-and-scim.md` |
| token-efficiency | `095-guides-power-user-token-efficiency.md` |

### Learning Path

**Level 1: Foundation**
- Files 001-010: Introduction to Factory platform
- Files 011-019: Quickstart and common use cases

**Level 2: Core Understanding**
- Files 026-029: Security, skills, IAM concepts
- Files 041-050: Settings, AGENTS.md, custom droids, hooks

**Level 3: Practical Application**
- Files 051-060: BYOK custom models configuration
- Files 061-068: Domain-specific skills
- Files 101-116: Automation tutorials

**Level 4: Advanced Usage**
- Files 071-080: User features and workflows
- Files 091-095: Power user optimization
- Files 121-128: Enterprise deployment

**Level 5: Reference**
- Files 136-143: API and CLI reference
- Files 156-159: Changelog and version history

## Common Tasks

### Configure AI Model
-> `docs/041-cli-configuration-settings.md` (model selection, reasoning effort)
-> `docs/051-cli-byok-overview.md` (custom models setup)

### Set Up AGENTS.md
-> `docs/042-cli-configuration-agents-md.md` (specification, templates, best practices)

### Create Custom Slash Commands
-> `docs/044-cli-configuration-custom-slash-commands.md` (Markdown templates, executable scripts)

### Configure Hooks
-> `docs/045-cli-configuration-hooks-guide.md` (lifecycle events, shell commands)
-> `docs/137-reference-hooks-reference.md` (full reference)

### Use Specification Mode
-> `docs/073-cli-user-guides-specification-mode.md` (planning, workflow, autonomy)

### Set Up Code Review
-> `docs/076-cli-features-code-review.md` (/review command, workflows)
-> `docs/103-guides-droid-exec-code-review.md` (automated PR reviews)

### Configure GitHub Integration
-> `docs/016-integrations-github-app.md` (GitHub App setup)
-> `docs/104-guides-droid-exec-github-actions.md` (CI/CD workflows)

### Run Headless/CI Mode
-> `docs/080-cli-droid-exec-overview.md` (droid exec, automation)
-> `docs/101-guides-building-droid-exec-tutorial.md` (tutorial)

### Optimize Token Usage
-> `docs/095-guides-power-user-token-efficiency.md` (strategies, model selection)

### Enterprise Deployment
-> `docs/121-enterprise.md` (overview, security, governance)
-> `docs/122-enterprise-network-and-deployment.md` (network, airgap, proxies)

## Settings Reference

Settings file location:
- macOS/Linux: `~/.factory/settings.json`
- Windows: `%USERPROFILE%\.factory\settings.json`

Key settings:
```json
{
  "model": "opus",
  "reasoningEffort": "low",
  "autonomyLevel": "normal",
  "diffMode": "github",
  "cloudSessionSync": true,
  "enableDroidShield": true
}
```

Available models: `opus`, `sonnet`, `haiku`, `gpt-5.1`, `gpt-5.1-codex`, `gpt-5.2`, `gemini-3-pro`, `droid-core`, `custom-model`

## Slash Commands

| Command | Description |
|---------|-------------|
| `/settings` | Configure droid behavior |
| `/model` | Switch AI models |
| `/review` | AI-powered code review |
| `/mcp` | Manage MCP servers |
| `/hooks` | Manage lifecycle hooks |
| `/help` | See all commands |
