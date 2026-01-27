---
name: anthropic-expert
description: Comprehensive Anthropic product expertise covering Claude models, Claude API, Python SDK, Agent SDK, Claude Code, and Model Context Protocol. Six integrated capabilities with complete documentation, searchable references, code examples, and cross-product integration patterns. Use when working with Claude API, building agents, using SDKs, developing with Claude Code, integrating MCP servers, learning Anthropic products, optimizing costs, implementing Anthropic features, managing context, using Opus 4.5, or implementing advanced tool patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Anthropic Expert

## Overview

anthropic-expert provides comprehensive expertise on all Anthropic products, features, and integrations. It covers 6 major product areas with complete documentation, 100+ features, code examples, and cross-product integration patterns.

**Purpose**: One-stop knowledge base for all Anthropic products and capabilities

**Coverage** (100% of Anthropic ecosystem):
- **6 Products**: Claude Models, Claude API, Python SDK, Agent SDK, Claude Code, MCP
- **100+ Features**: All API features, SDK capabilities, Agent concepts, Claude Code topics
- **44 Claude Code Topics**: Complete CLI documentation
- **All SDKs**: Python + TypeScript SDKs for API and Agent development
- **All Tools**: 10+ built-in tools + custom tool creation
- **Administration**: Workspaces, usage tracking, costs, security, compliance

**What's Included**:
- Complete feature documentation with examples
- Code snippets for all major features (50+ examples)
- Cross-product integration patterns
- Best practices from official docs
- Searchable references (search-docs.py)
- Update tracking (maintained by anthropic-docs-updater)

## The 6 Capabilities

### Capability 1: Claude Models & API Expertise

**What It Covers**:
- All Claude models (Sonnet 4.5, Opus 4.1, Haiku 4.5, legacy models)
- Complete Messages API (endpoints, parameters, streaming)
- All API features: Prompt Caching, Extended Thinking, Citations, Memory, Vision, PDF, Context Editing
- Tools ecosystem: Bash, Code execution, Computer use, Web search, MCP connector, Memory tool
- Files API: Upload, manage, reference documents
- Skills API: Anthropic-managed skills (Office suite) + custom skills
- Message Batches: Async processing with 50% cost reduction
- Admin API: Organization, workspaces, members, API keys, usage, costs

**When to Use This Capability**:
- Building applications with Claude API
- Implementing API features (streaming, caching, tool use)
- Using advanced features (Extended Thinking, Citations, Memory)
- Processing images or PDFs
- Managing costs and usage
- Building RAG applications
- Integrating external tools

**Quick Navigation**:
- Models overview: See `references/claude-api-complete.md` - Models section
- Streaming: See `references/claude-api-complete.md` - Streaming section
- Prompt Caching: See `references/claude-api-complete.md` - Prompt Caching section
- Tools: See `references/claude-api-complete.md` - Tools section
- Admin API: See `references/claude-api-complete.md` - Admin API section

**Key Features Quick Reference**:

| Feature | What It Does | Benefit | Availability |
|---------|--------------|---------|--------------|
| **Prompt Caching** | Cache frequent prompts | 90% cost, 85% latency reduction | All models |
| **Extended Thinking** | Visible reasoning process | Better complex reasoning | Opus 4.1, Sonnet 4.5 |
| **Citations** | Ground in sources | Trustworthy responses | All models |
| **Memory** | Persistent context | Long-term task awareness | All models |
| **Vision** | Process images | Multimodal applications | All models |
| **PDF Support** | Parse PDFs | Document processing | All models |
| **Message Batches** | Async processing | 50% cost reduction | All models |
| **Files API** | Upload once, use multiple times | Efficient document handling | Beta |
| **Skills API** | Extend capabilities | Office docs, custom skills | Beta |

---

### Capability 2: Python SDK Usage

**What It Covers**:
- Installation and setup (`pip install anthropic`)
- Sync client usage (basic patterns)
- Async client usage (asyncio integration)
- Streaming responses (server-sent events)
- Tool use integration (function calling)
- Prompt caching SDK integration
- Batch processing (async requests)
- File management (Files API via SDK)
- Error handling (exceptions, retries, timeouts)
- Configuration (API keys, settings)
- Type safety (typing support)
- 30+ code examples

**When to Use This Capability**:
- Python application development
- Integrating Claude into Python projects
- Async/await patterns needed
- Type-safe Claude integration
- Production Python applications

**Quick Navigation**:
- Installation: `references/python-sdk-reference.md` - Installation section
- Basic usage: `references/python-sdk-reference.md` - Basic Usage
- Streaming: `references/python-sdk-reference.md` - Streaming section
- Tool use: `references/python-sdk-reference.md` - Tool Use section

**Quick Start Example**:
```python
import anthropic

# Initialize client
client = anthropic.Anthropic(api_key="your_api_key")

# Create message
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)

print(message.content)
```

---

### Capability 3: Agent SDK Expertise

**What It Covers**:
- Agent SDK overview (Python + TypeScript)
- Installation (claude-agent-sdk)
- Agents (creation, configuration, deployment)
- Subagents (.claude/agents/, composition patterns)
- Agent Skills (.claude/skills/, reusable capabilities)
- Tools (built-in ecosystem + custom tool creation)
- Sessions (multi-turn conversations, state management)
- Permissions (fine-grained access control)
- Streaming modes (single vs streaming)
- Hooks (.claude/settings.json, event-driven automation)
- Slash Commands (built-in + custom commands)
- Plugins (programmable extensions, Beta)
- System prompts (agent instructions)
- MCP integration (protocol support in agents)
- Cost tracking (expense monitoring)
- Hosting (deployment patterns)
- Use cases (coding agents, business agents)
- 25+ code examples

**When to Use This Capability**:
- Building AI agents
- Creating autonomous systems
- Agent composition (subagents)
- Reusable agent capabilities (skills)
- Production agent deployment
- Custom tool integration
- Session-based applications

**Quick Navigation**:
- Agents: `references/agent-sdk-complete.md` - Agents section
- Subagents: `references/agent-sdk-complete.md` - Subagents section
- Skills: `references/agent-sdk-complete.md` - Agent Skills section
- Tools: `references/agent-sdk-complete.md` - Tools section
- Deployment: `references/agent-sdk-complete.md` - Hosting section

**Key Concepts**:

| Concept | Description | Storage | Use Case |
|---------|-------------|---------|----------|
| **Agents** | Specialized AI for tasks | Code/config | Custom assistants |
| **Subagents** | Delegated specialists | .claude/agents/*.md | Task delegation |
| **Agent Skills** | Reusable capabilities | .claude/skills/* | Capability sharing |
| **Tools** | External integrations | Agent config | API/service calls |
| **Sessions** | Multi-turn conversations | Session state | Persistent interactions |
| **Hooks** | Event automation | .claude/settings.json | Validation, workflows |
| **Slash Commands** | Custom commands | .md files | Quick actions |
| **Plugins** | Programmable extensions | Plugin code | Custom functionality |

---

### Capability 4: Claude Code Mastery

**What It Covers** (All 44 Documentation Pages):

**GETTING STARTED**:
- Overview (capabilities, Unix philosophy)
- Quickstart (8-step setup guide)
- Common Workflows (codebase analysis, debugging, refactoring, testing, git integration)
- Claude Code on the Web (cloud execution)

**BUILD WITH CLAUDE CODE**:
- Sub-agents (specialized AI agents for delegated tasks)
- Plugins (extending functionality with custom code)
- Skills (creating reusable agent capabilities)
- Output Styles (customizing response formatting)
- Hooks Guide (event-driven automation and validation)
- Headless (API-based integration without terminal UI)
- GitHub Actions (CI/CD workflow automation)

**DEPLOYMENT & CI/CD**:
- GitLab CI/CD (pipeline integration)
- MCP (Model Context Protocol server setup)
- Migration Guide (version upgrade instructions)
- Troubleshooting (common issues and solutions)
- Third-party Integrations (enterprise provider strategies)
- Amazon Bedrock (AWS model access)
- Google Vertex AI (GCP model setup)
- Network Config (proxy, certificate management)

**ADMINISTRATION**:
- LLM Gateway (LiteLLM routing configuration)
- DevContainer (containerized development)
- Sandboxing (security isolation)
- Setup (cross-platform installation)
- IAM (authentication and permissions)
- Security (threat protection, best practices)
- Data Usage (privacy policies, telemetry)
- Monitoring Usage (metrics collection)
- Costs (expense tracking and optimization)

**CONFIGURATION**:
- Analytics (team usage metrics)
- Plugin Marketplaces (distributing and discovering plugins)
- Settings (configuration files and precedence)
- VS Code (extension setup)
- JetBrains (IntelliJ-based IDE plugin)
- Terminal Config (shell customization)
- Model Config (model selection and caching)
- Memory (persistent context management)

**REFERENCE**:
- Statusline (custom status line creation)
- CLI Reference (command syntax and flags)
- Interactive Mode (keyboard shortcuts, editing)
- Slash Commands (built-in and custom commands)
- Checkpointing (session state management)
- Hooks (advanced hook configuration)

**ADDITIONAL**:
- Plugins Reference (plugin schema and structure)
- Legal and Compliance (licensing, BAA)

**When to Use This Capability**:
- Developing with Claude Code CLI
- Creating custom skills
- Building sub-agents
- Developing plugins
- CI/CD integration
- Enterprise deployment
- Configuring Claude Code
- Troubleshooting issues

**Quick Navigation**:
- All topics: `references/claude-code-reference.md` (organized by category)
- Specific feature: Use search: `python scripts/search-docs.py "hooks"`

---

### Capability 5: MCP Integration

**What It Covers**:
- Model Context Protocol specification
- MCP server development (creating custom servers)
- MCP client integration (connecting to servers)
- Tool creation (building MCP tools)
- Security best practices (securing MCP integrations)
- Integration across products (API MCP connector, Agent SDK MCP, Claude Code MCP)
- Common MCP servers (Slack, GitHub, Google Drive, Jira, Asana)
- Custom MCP server examples

**When to Use This Capability**:
- Connecting Claude to external services
- Building custom MCP servers
- Integrating with enterprise tools (Slack, Jira, etc.)
- Creating custom tool ecosystems
- Extending Claude capabilities

**Quick Navigation**:
- MCP overview: `references/mcp-integration-guide.md` - Protocol Overview
- Server development: `references/mcp-integration-guide.md` - Server Development
- Examples: `references/mcp-integration-guide.md` - Examples section

**MCP in Products**:
- **Claude API**: MCP connector tool (Beta) - call MCP servers from API
- **Agent SDK**: Built-in MCP integration - agents can use MCP servers
- **Claude Code**: Native MCP support - connect to servers via config

---

### Capability 6: Administration & Enterprise

**What It Covers**:
- Workspaces (create, manage, organize projects)
- API Key management (create, rotate, secure)
- Organization members (add, remove, roles, permissions)
- Usage tracking (token counts, request metrics, analytics)
- Cost management (expense tracking, optimization, budgets)
- IAM (authentication methods, permission models)
- Security (threat protection, data encryption, compliance)
- Compliance (BAA for healthcare, legal requirements)
- Admin API (programmatic management)
- Code examples for all admin operations

**When to Use This Capability**:
- Enterprise deployment
- Team/organization management
- Cost tracking and optimization
- Security configuration
- Compliance requirements (healthcare, financial)
- Programmatic administration

**Quick Navigation**:
- Complete guide: `references/administration-reference.md`
- Specific topic: Search: `python scripts/search-docs.py "workspaces"`

**Admin API Quick Reference**:

| Operation | Endpoint | Use Case |
|-----------|----------|----------|
| Get Org Info | GET /v1/organization | Org details |
| List Members | GET /v1/organization/members | Team management |
| Create Workspace | POST /v1/organization/workspaces | Project organization |
| Get Usage | GET /v1/organization/usage | Token tracking |
| Get Costs | GET /v1/organization/costs | Expense monitoring |
| Manage Keys | POST /v1/organization/api_keys | Key creation |

---

## Integration Scenarios

### Scenario 1: API Development → Production Deployment

**Use Case**: Develop with API, deploy as agent

**Workflow**:
1. **Development** (Claude API + Python SDK):
   - Use Python SDK for development
   - Implement with API features (streaming, caching, tools)
   - Test locally with API client

2. **Agent Creation** (Agent SDK):
   - Convert API application to agent
   - Use Agent SDK for deployment
   - Add session management, permissions

3. **Production** (Agent hosting):
   - Deploy agent with hosting patterns
   - Monitor with cost tracking
   - Manage with Admin API

**Products Used**: Claude API → Python SDK → Agent SDK
**See**: `references/integration-patterns.md` - API to Agent Pattern

---

### Scenario 2: Local Development → Cloud Deployment

**Use Case**: Develop locally with Claude Code, deploy to production

**Workflow**:
1. **Local Development** (Claude Code):
   - Use Claude Code CLI for local development
   - Create skills, sub-agents, plugins
   - Test workflows locally

2. **Adaptation** (Agent SDK):
   - Convert Claude Code skills to Agent SDK skills
   - Adapt sub-agents for production
   - Add production tooling

3. **Deployment**:
   - Deploy agent with Agent SDK hosting
   - Use MCP for external integrations
   - Monitor with Admin API

**Products Used**: Claude Code → Agent SDK → MCP
**See**: `references/integration-patterns.md` - Claude Code to Production Pattern

---

### Scenario 3: RAG Application

**Use Case**: Build retrieval-augmented generation system

**Workflow**:
1. **Document Management** (Files API):
   - Upload documents via Files API
   - Manage document library

2. **Search Integration** (Search Results + Citations):
   - Provide search results to Claude
   - Enable citations for grounding

3. **Query Processing** (Messages API):
   - Send queries with document context
   - Get cited responses

**Products Used**: Files API + Search Results + Citations
**See**: `references/integration-patterns.md` - RAG Pipeline Pattern

---

### Scenario 4: MCP Everywhere

**Use Case**: Integrate external services across all products

**MCP in Claude API**:
- Use MCP connector tool (Beta)
- Call MCP servers from API requests
- Example: `{"type": "mcp_connector", "server": "slack"}`

**MCP in Agent SDK**:
- Built-in MCP integration
- Agents access MCP servers directly
- Configure in agent settings

**MCP in Claude Code**:
- Native MCP support
- Connect via .claude/mcp-servers config
- Auto-discovered tools

**Products Used**: MCP across API, Agent SDK, Claude Code
**See**: `references/mcp-integration-guide.md` - Integration Across Products

---

## Best Practices

### 1. Choose the Right Product

**Use Claude API when**:
- Direct API integration needed
- Custom application development
- Maximum flexibility required
- You manage infrastructure

**Use Python SDK when**:
- Python applications
- Type safety desired
- Async/await patterns needed
- Simplified API access

**Use Agent SDK when**:
- Building autonomous agents
- Session-based applications
- Need subagents or agent composition
- Production agent deployment

**Use Claude Code when**:
- Terminal-based development
- Local skill/agent creation
- Quick prototyping
- Developer productivity

### 2. Optimize Costs

**Prompt Caching** (90% cost reduction):
- Cache system prompts, long documents
- Standard: 5-min TTL (most use cases)
- Extended: 1-hour TTL (very frequent access)

**Message Batches** (50% cost reduction):
- Use for async/batch processing
- Ideal for background jobs, bulk operations

**Model Selection**:
- Haiku 4.5: Fast, cheap (simple tasks)
- Sonnet 4.5: Balanced (most use cases)
- Opus 4.1: Complex reasoning (when needed)

### 3. Leverage Progressive Features

Start simple, add features as needed:
1. Basic Messages API
2. Add Streaming (better UX)
3. Add Prompt Caching (cost savings)
4. Add Tool Use (external integration)
5. Add Extended Thinking (complex reasoning)
6. Add Citations (trustworthiness)
7. Add Memory (long-term context)

### 4. Integrate with MCP

**Why MCP**: Standardized integration to external services

**Use Across Products**:
- API: MCP connector tool
- Agent SDK: Built-in MCP integration
- Claude Code: Native MCP support

**Common MCP Servers**:
- Slack (team communication)
- GitHub (code management)
- Google Drive (documents)
- Jira (project management)
- Custom servers (your services)

### 5. Monitor Usage and Costs

**Admin API Tracking**:
- GET /v1/organization/usage (token metrics)
- GET /v1/organization/costs (expense data)
- Monitor by workspace for project tracking

**Cost Optimization**:
- Use caching aggressively
- Choose appropriate models
- Batch async work
- Monitor with Admin API

---

## See Also

For specialized deep-dives on advanced topics:

- **claude-opus-4-5-guide**: Comprehensive guide to Opus 4.5, effort parameter, model selection, and benchmark comparisons
- **claude-context-management**: Context editing strategies (server-side clearing, client-side compaction), memory tool integration for infinite conversations
- **claude-advanced-tool-use**: Tool search (10,000+ tools), programmatic calling, tool use examples for production systems
- **claude-cost-optimization**: Cost tracking, ROI measurement, optimization patterns (caching, batching, context editing, effort tuning)

---

## Quick Reference

### Product Navigator

**Need To** | **Use Product** | **See Reference** |
|-----------|-----------------|-------------------|
| Call Claude API directly | Claude API | claude-api-complete.md |
| Develop in Python | Python SDK | python-sdk-reference.md |
| Build autonomous agents | Agent SDK | agent-sdk-complete.md |
| Local CLI development | Claude Code | claude-code-reference.md |
| Connect external services | MCP | mcp-integration-guide.md |
| Manage organization | Admin API | administration-reference.md |
| Cross-product patterns | Integration | integration-patterns.md |

### Feature Finder

**Want Feature** | **Product** | **Reference Location** |
|----------------|-------------|------------------------|
| Streaming responses | API, SDKs | claude-api-complete.md - Streaming |
| Prompt Caching | API, SDKs | claude-api-complete.md - Caching |
| Extended Thinking | API, SDKs | claude-api-complete.md - Extended Thinking |
| Tool use / Function calling | API, SDKs, Agents | claude-api-complete.md - Tools |
| Advanced tool patterns | API, SDKs | claude-advanced-tool-use/SKILL.md |
| Context editing & compaction | API, SDKs | claude-context-management/SKILL.md |
| Vision / Image processing | API, SDKs | claude-api-complete.md - Vision |
| PDF processing | API, SDKs | claude-api-complete.md - PDF Support |
| Opus 4.5 & effort parameter | API, SDKs | claude-opus-4-5-guide/SKILL.md |
| Subagents | Agent SDK | agent-sdk-complete.md - Subagents |
| Agent Skills | Agent SDK, Claude Code | agent-sdk-complete.md - Skills |
| Hooks | Agent SDK, Claude Code | agent-sdk-complete.md - Hooks |
| Slash Commands | Agent SDK, Claude Code | agent-sdk-complete.md - Slash Commands |
| MCP integration | API, Agent SDK, Claude Code | mcp-integration-guide.md |
| Cost tracking & ROI | Admin API, Agent SDK | claude-cost-optimization/SKILL.md |
| Cost optimization strategies | All products | claude-cost-optimization/SKILL.md |

### Search Instructions

**Find Anything Quickly**:
```bash
# Search across all references
python scripts/search-docs.py "prompt caching"

# Search specific product
python scripts/search-docs.py "streaming" --product "Python SDK"

# Find code examples
python scripts/search-docs.py "example" --type code
```

**Search Returns**:
- Reference file name
- Section location
- Relevant excerpt
- Line numbers

### Latest Models (2025)

| Model | Best For | Context | Features |
|-------|----------|---------|----------|
| **Sonnet 4.5** | General purpose, balanced | 200k-1M | Extended Thinking, all features |
| **Opus 4.1** | Complex reasoning, analysis | 200k | Hybrid thinking, extended reasoning |
| **Haiku 4.5** | Speed, efficiency, cost | 200k | Fast responses, cost-effective |

### Common Workflows

**1. Simple API Call**:
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

**2. Streaming Response**:
```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your prompt"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**3. Tool Use**:
```python
tools = [{"name": "get_weather", "description": "Get weather for location", ...}]
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in SF?"}]
)
```

**4. Prompt Caching**:
```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "System prompt...",
             "cache_control": {"type": "ephemeral"}}
        ]
    }
]
```

### Documentation Structure

```
anthropic-expert/
├── SKILL.md - This file (overview, capabilities, quick ref)
├── references/
│   ├── claude-api-complete.md - Models, API, all features
│   ├── python-sdk-reference.md - Python SDK complete guide
│   ├── agent-sdk-complete.md - Agent SDK comprehensive
│   ├── claude-code-reference.md - All 44 Claude Code topics
│   ├── mcp-integration-guide.md - MCP across products
│   ├── administration-reference.md - Admin, costs, security
│   ├── integration-patterns.md - Cross-product usage
│   └── changelog.md - Version history, updates
├── scripts/
│   └── search-docs.py - Search all references
└── README.md - Quick start, navigation guide
```

**Total Coverage**: ~8,400 lines of comprehensive Anthropic expertise

### Update Tracking

**Last Updated**: 2025-11-07 (initial build)
**Next Update**: Use `anthropic-docs-updater` skill to check for and apply updates
**Changelog**: See `references/changelog.md` for version history

---

**anthropic-expert provides complete, searchable, up-to-date expertise on all Anthropic products, features, and integration patterns - your comprehensive guide to the Anthropic ecosystem.**
