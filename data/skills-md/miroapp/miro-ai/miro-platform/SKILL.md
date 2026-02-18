---
name: miro-platform
description: >-
  Comprehensive guide to Miro as a visual collaboration platform. Covers canvas
  features, content types, AI capabilities, and enterprise use cases. For MCP
  tool documentation, see the miro plugin's skill (miro-mcp).
---

# Miro Platform Guide

## What is Miro?

Miro is the visual collaboration platform for every team. With an infinite canvas, 100M+ users across 250K+ organizations use Miro for brainstorming, planning, design, and cross-functional collaboration.

In 2025, Miro became the "AI Innovation Workspace" - an AI-first platform where teams work together with AI on one shared canvas.

## Platform Capabilities

- **Infinite Canvas** - Unlimited workspace that scales from quick sketches to enterprise documentation
- **Real-time Collaboration** - Cursor tracking, video chat, comments, voting, timers
- **300+ Templates** - Pre-built frameworks for common workflows
- **160+ Integrations** - Connects to Jira, Figma, Slack, Teams, and more

## What's on a Miro Board?

Miro boards contain diverse content types for different purposes:

| Type | Purpose |
|------|---------|
| Sticky Notes | Quick brainstorming, idea capture |
| Cards | Structured work items with metadata |
| Frames | Containers to organize sections |
| Shapes | Flowchart symbols, UML, AWS/Azure icons |
| Tables | Structured data, matrices |
| Documents | Long-form rich text content |
| Wireframes | UI mockups and prototypes |
| Mind Maps | Hierarchical brainstorming |

See [Content Types](references/content-types.md) for detailed descriptions and business value.

## Miro AI

Miro is an AI-first platform with several AI capabilities:

- **Flows** - Visual AI workflows that automate multi-step processes
- **Sidekicks** - Conversational AI agents with task expertise
- **AI Diagram Generation** - Create diagrams from natural language
- **Model Selection** - Enterprise customers choose from OpenAI, Anthropic, Gemini

See [AI Capabilities](references/ai-capabilities.md) for details.

## Design-to-Code with Miro

Miro Specs converts team context (user stories, wireframes, architecture) into technical specifications that AI coding tools can consume:

- Capture PRDs, wireframes, and technical diagrams
- Send specs to GitHub Copilot, Cursor, Claude Code, Windsurf, Lovable
- External AI agents read board context via MCP integration

See [Design-to-Code](references/design-to-code.md) for workflows.

## Enterprise Use Cases

Common patterns for enterprise Miro adoption:

1. **Design Handoff** - Wireframes to code via AI tools
2. **Sprint Planning** - Visual planning with Jira/Linear sync
3. **Architecture Documentation** - Living technical diagrams
4. **Workshop Facilitation** - Remote workshops on canvas
5. **Knowledge Base** - Visual and written documentation hub

See [Enterprise Use Cases](references/enterprise-use-cases.md) for implementation patterns.

## MCP Tools

For Miro MCP tool documentation (how to read/write to boards programmatically), see the `miro` plugin's skill (`miro-mcp`) which is installed separately. The MCP tools enable:

- Creating diagrams, documents, and tables
- Reading board content and extracting documentation
- Syncing external data to Miro tables
- Browsing and filtering board items
