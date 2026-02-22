---
name: learn
description: Teach Claude ANY topic - code libraries, APIs, concepts, tools, methodologies, or domains. Researches via web and docs, then retains knowledge as a permanent skill. Use when user says "/learn <topic>", "learn about X", "teach yourself Y", "become an expert on Z". Examples - "/learn stripe" for payments, "/learn GTD" for productivity, "/learn israeli-tax-law" for domain knowledge.
version: "1.1.0"
author: aviz85
tags:
  - learning
  - knowledge
  - research
  - meta
argument-hint: "<topic> [--update] [--project]"
---

# Learn: Teach Claude Any Topic

Research and learn any topic, then retain the knowledge as a permanent skill. Works for:
- **Code libraries**: React, Stripe, Supabase (uses Context7 when available)
- **APIs & Services**: Twilio, OpenAI, Google APIs
- **Concepts & Methodologies**: GTD, Agile, Design Patterns
- **Domain Knowledge**: Tax law, medical terminology, industry practices
- **Tools**: Docker, Kubernetes, FFmpeg

After learning, Claude becomes an expert on that topic in all future conversations.

## Usage

```
/learn <topic>           # Create new skill from docs
/learn <topic> --update  # Update existing skill with latest docs
/learn <topic> --project # Save to project (.claude/skills/) instead of global
```

## Process

### 1. Research the Topic

**For code libraries/APIs** - try Context7 first:
```
mcp__plugin_context7_context7__resolve-library-id
  query: "user's task/question"
  libraryName: "<topic>"
```

**For any topic** (or if Context7 doesn't have it) - use WebSearch:
```
WebSearch: "<topic>" guide tutorial best practices
WebSearch: "<topic>" official documentation
WebSearch: "<topic>" examples patterns
```

**For domain knowledge** - broader research:
```
WebSearch: "<topic>" comprehensive guide
WebSearch: "<topic>" key concepts terminology
WebSearch: "<topic>" common mistakes pitfalls
```

Use WebFetch to read the most relevant pages found.

### 2. Extract Knowledge

Query the documentation for key information:

```
mcp__plugin_context7_context7__query-docs
  libraryId: "<resolved-id>"
  query: "getting started setup authentication common patterns"
```

Extract:
- **Setup/Installation**: How to get started
- **Core concepts**: Key abstractions and terminology
- **Common patterns**: Typical usage examples
- **API reference**: Essential methods/functions
- **Gotchas**: Non-obvious pitfalls mentioned in docs
- **Best practices**: Recommended approaches

If docs are large, make multiple targeted queries:
1. "installation setup quickstart"
2. "authentication API keys configuration"
3. "common patterns examples"
4. "error handling troubleshooting"

### 3. Consult Claude Code Guide

Before creating the skill, use the `claude-code-guide` agent to verify current skill conventions:

```
Task tool with subagent_type: claude-code-guide
prompt: "What are the current conventions for writing Claude Code skills?
        I need to know: required/optional frontmatter fields,
        description best practices, and recommended structure."
```

This ensures the generated skill follows the latest Claude Code patterns.

### 4. Generate Skill Structure

Create skill at appropriate location:
- Default: `~/.claude/skills/<topic>/skill.md`
- With `--project`: `.claude/skills/<topic>/skill.md`

**Skill template:**

```markdown
---
name: <topic>
description: <What the library does>. Use when <specific triggers>. Covers: <main capabilities>.
---

# <Topic> Quick Reference

## Setup

[Installation commands and initial config]

## Core Concepts

[Key abstractions - 2-3 sentences each]

## Common Patterns

### [Pattern 1 Name]
[Code example with brief explanation]

### [Pattern 2 Name]
[Code example with brief explanation]

## API Quick Reference

| Method | Purpose | Example |
|--------|---------|---------|
| ... | ... | ... |

## Gotchas

- [Non-obvious issue 1]
- [Non-obvious issue 2]

## Links

- [Official Docs](url)
- [API Reference](url)
```

### 5. Verify and Announce

After creating the skill:
1. Confirm the skill was created
2. Show the description (what triggers it)
3. Show 2-3 example prompts that would activate it

## Quality Guidelines

**Do:**
- Focus on practical, actionable information
- Include real code examples from docs
- Capture version-specific details if relevant
- Add the official docs URL for reference

**Don't:**
- Copy entire documentation (copyright)
- Include marketing/promotional content
- Add information Claude already knows generally
- Make the skill too long (under 500 lines)

## Update Mode (--update)

When updating an existing skill:
1. Read current skill content
2. Query docs for latest/new information
3. Merge new content, preserving existing structure
4. Note version changes if applicable

## Example

```
User: /learn stripe-payments

Claude:
1. Resolves "stripe" via Context7 → /stripe/stripe-node
2. Queries: setup, authentication, common patterns, webhooks
3. Consults claude-code-guide for current skill conventions
4. Creates ~/.claude/skills/stripe-payments/skill.md with:
   - API key setup
   - Payment intent flow
   - Webhook verification
   - Error handling patterns
5. Reports: "Created stripe-payments skill. Triggers on: 'Stripe payment', 'charge card', 'payment intent'"
```

## Requirements

- Context7 MCP plugin (recommended) - for accessing library documentation
- OR WebSearch/WebFetch tools - as fallback for any documentation
