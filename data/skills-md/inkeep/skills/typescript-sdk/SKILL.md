---
name: typescript-sdk
description: Use when creating, modifying, or testing AI Agents built with the Inkeep TypeScript SDK (@inkeep/agents-sdk).
license: MIT
metadata:
  author: "inkeep"
  version: "1.0"
---


# Typescript Sdk

## Overview

The TypeScript SDK provides a declarative way to define agents, sub-agents, tools, and their relationships. 

## Rules (45)

Read individual rule files for detailed explanations and code examples on particular tasks or topics:

| Title | Topic | Description |
| --- | --- | --- |
| [Sub Agent Relationships Overview](./rules/agent-relationships-overview.md) | typescript-sdk/agent-relationships | Transfer and delegation relationships between Sub Agents |
| [When to Use Transfers vs Delegation](./rules/agent-relationships-when-to-use.md) | typescript-sdk/agent-relationships | Guidelines for choosing between transfer and delegation relationships |
| [Types of Delegation Relationships](./rules/delegation-types.md) | typescript-sdk/agent-relationships | Sub agent, external agent, and team agent delegation |
| [Configuring StopWhen](./rules/stop-when-config.md) | typescript-sdk/agent-settings | Control stopping conditions to prevent infinite loops in agents |
| [Sub Agent Parameters Reference](./rules/sub-agent-params.md) | typescript-sdk/agent-settings | Complete parameter reference for subAgent() configuration |
| [CLI inkeep add Command](./rules/cli-add-command.md) | typescript-sdk/cli-reference | Pull a template project or MCP from the Inkeep Agents Cookbook |
| [CLI inkeep config Command](./rules/cli-config-command.md) | typescript-sdk/cli-reference | Manage Inkeep configuration values |
| [CLI Configuration File Structure](./rules/cli-config-file-structure.md) | typescript-sdk/cli-reference | Structure of inkeep.config.ts and configuration priority |
| [CLI inkeep dev Command](./rules/cli-dev-command.md) | typescript-sdk/cli-reference | Start the Inkeep dashboard server for visual agents orchestration |
| [CLI Environment Variables](./rules/cli-environment-variables.md) | typescript-sdk/cli-reference | Environment variables respected by the CLI and SDK |
| [CLI inkeep init Command](./rules/cli-init-command.md) | typescript-sdk/cli-reference | Initialize a new Inkeep configuration file in your project |
| [CLI inkeep list-agents Command](./rules/cli-list-agents-command.md) | typescript-sdk/cli-reference | List all available agents for a specific project |
| [CLI inkeep profile Command](./rules/cli-profile-command.md) | typescript-sdk/cli-reference | Manage named CLI profiles for multiple remotes, credentials, and environments |
| [CLI inkeep pull Command](./rules/cli-pull-command.md) | typescript-sdk/cli-reference | Pull project configuration from server and update local TypeScript files |
| [CLI inkeep push Command](./rules/cli-push-command.md) | typescript-sdk/cli-reference | Push agent configurations to your server |
| [CLI inkeep update Command](./rules/cli-update-command.md) | typescript-sdk/cli-reference | Update the Inkeep CLI to the latest version |
| [Runtime Limits Configuration](./rules/runtime-limits-overview.md) | typescript-sdk/configure-runtime-limits | How to configure execution limits, timeouts, and constraints |
| [Runtime Configuration Variables](./rules/runtime-limits-variables.md) | typescript-sdk/configure-runtime-limits | All available environment variables for configuring runtime limits |
| [Context Fetchers Overview](./rules/context-fetchers-overview.md) | typescript-sdk/context-fetchers | How to use context fetchers to embed real-time data in agent prompts |
| [Credential Store Options](./rules/credential-store-options.md) | typescript-sdk/credentials/overview | Options for storing MCP server and external agent credentials |
| [Data Operation Types Reference](./rules/data-operation-types.md) | typescript-sdk/data-operations | All data operation event types and their payloads |
| [Data Operations Overview](./rules/data-operations-overview.md) | typescript-sdk/data-operations | How to enable and use data operations for debugging and monitoring |
| [External Agents Overview](./rules/external-agents-overview.md) | typescript-sdk/external-agents | How to configure and use external agents using the A2A protocol |
| [Passing Context via Headers](./rules/headers-passing-context.md) | typescript-sdk/headers | How to pass dynamic context to agents via HTTP headers |
| [Using Headers in Agents](./rules/headers-usage.md) | typescript-sdk/headers | How to use header values in prompts, context fetchers, and external tools |
| [Conversation Memory Overview](./rules/memory-overview.md) | typescript-sdk/memory | How conversation history is managed and included in context windows |
| [Model Types Reference](./rules/model-types.md) | typescript-sdk/models | When to use each model type in the configuration hierarchy |
| [Model Provider Options](./rules/provider-options.md) | typescript-sdk/models | Configuration options for different model providers |
| [Supported Models Reference](./rules/supported-models.md) | typescript-sdk/models | List of supported model providers and their API keys |
| [Defining Artifact Components](./rules/artifact-components-definition.md) | typescript-sdk/structured-outputs/artifact-components | How to define artifact components with preview fields for citations and sources |
| [Defining Data Components](./rules/data-components-definition.md) | typescript-sdk/structured-outputs/data-components | How to define data components using Zod schemas |
| [Status Updates Configuration](./rules/status-updates-config.md) | typescript-sdk/structured-outputs/status-updates | How to configure AI-powered status updates for agents |
| [Function Tools Execution Environment](./rules/function-tools-execution.md) | typescript-sdk/tools/function-tools | Sandbox providers, runtime configuration, and security guarantees |
| [Function Tools Overview](./rules/function-tools-overview.md) | typescript-sdk/tools/function-tools | Use cases and how to create function tools |
| [Environment-Aware MCP Servers](./rules/mcp-environment-aware.md) | typescript-sdk/tools/mcp-tools | Configure MCP tools to switch based on environment (dev vs production) |
| [MCP Tool Authentication](./rules/mcp-tool-auth.md) | typescript-sdk/tools/mcp-tools | Authentication methods for MCP servers including API keys, OAuth, and custom headers |
| [MCP Tool Overrides](./rules/mcp-tool-overrides.md) | typescript-sdk/tools/mcp-tools | Customize how individual MCP tools appear to agents |
| [Selecting MCP Tools](./rules/mcp-tool-selection.md) | typescript-sdk/tools/mcp-tools | How to selectively enable tools from MCP servers |
| [Registering MCP Servers as Tools](./rules/mcp-tools-registration.md) | typescript-sdk/tools/mcp-tools | How to register and configure MCP tools for your agents |
| [Tool Approvals Configuration](./rules/tool-approvals-config.md) | typescript-sdk/tools/tool-approvals | How to configure tools to require user approval before execution |
| [Responding to Tool Approval Requests](./rules/tool-approvals-response.md) | typescript-sdk/tools/tool-approvals | How to approve or deny tool execution requests |
| [Trigger Configuration Options](./rules/triggers-config-options.md) | typescript-sdk/triggers | Configuration options for triggers including authentication, schemas, and transforms |
| [Triggers Overview](./rules/triggers-overview.md) | typescript-sdk/triggers | Creating webhook endpoints to invoke agents from external services |
| [Configuration Priority Hierarchy](./rules/config-hierarchy.md) | typescript-sdk/workspace-configuration | How CLI flags, env vars, and config file values are resolved |
| [Workspace Configuration File](./rules/workspace-config-overview.md) | typescript-sdk/workspace-configuration | Structure and options for inkeep.config.ts |

## Other Resources
For additional information, see:
- Full Documentation: https://docs.inkeep.com/ (llms.txt and llms-full.txt available are available!)
- GitHub Repo (Open Source): https://github.com/inkeep/agents