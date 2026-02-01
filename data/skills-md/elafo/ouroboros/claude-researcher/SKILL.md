---
name: claude-researcher
description: Research, fetch, analyze, investigate, explain, and clarify official Claude Code documentation from code.claude.com. Retrieve and consult authoritative information about subagents, hooks, skills, commands, plugins, output styles, MCP servers, and best practices using WebFetch. Cross-reference multiple documentation pages to provide comprehensive answers with citations. Use when users ask about Claude Code features, capabilities, specifications, official documentation, how-to guides, implementation details, configuration options, or need clarification on Claude Code behavior. Triggers include questions about "how does X work", "Claude Code docs", "official documentation", "best practices for", "how to create", code.claude.com references, or requests for authoritative guidance on Claude Code artifacts and features.
allowed-tools: WebFetch, Read, Grep, Glob
---

# Claude Researcher Skill

## Overview

The Claude Researcher skill provides authoritative answers about Claude Code by fetching and analyzing official documentation from code.claude.com. Instead of relying on potentially outdated knowledge or assumptions, this skill retrieves current, accurate information directly from the source.

## Core Capabilities

1. **Fetch Official Documentation** - Retrieve content from code.claude.com documentation pages using WebFetch
2. **Multi-Page Analysis** - Cross-reference multiple documentation pages for comprehensive understanding
3. **Authoritative Answers** - Provide accurate information with source citations
4. **Feature Explanation** - Explain Claude Code features, configurations, and best practices
5. **Code Examples** - Extract and present official code examples from documentation
6. **Specification Details** - Retrieve technical specifications, YAML formats, and API details
7. **Best Practices** - Share recommended approaches from official guides
8. **Discovery** - Find relevant documentation pages based on user queries

## Key Documentation Resources

The skill primarily accesses these official documentation sections:

- **Skills:** `https://code.claude.com/docs/en/skills`
- **Commands:** `https://code.claude.com/docs/en/commands`
- **Slash Commands:** `https://code.claude.com/docs/en/slash-commands`
- **Subagents:** `https://code.claude.com/docs/en/sub-agents`
- **Hooks:** `https://code.claude.com/docs/en/hooks`
- **Hooks Guide:** `https://code.claude.com/docs/en/hooks-guide`
- **Plugins:** `https://code.claude.com/docs/en/plugins`
- **Plugins Reference:** `https://code.claude.com/docs/en/plugins-reference`
- **Plugin Marketplaces:** `https://code.claude.com/docs/en/plugin-marketplaces`
- **Output Styles:** `https://code.claude.com/docs/en/output-styles`
- **Documentation Map:** `https://docs.claude.com/en/docs/claude-code/claude_code_docs_map.md`

Additional pages are discovered and accessed as needed based on the query.

## Methodology

### Step 1: Query Analysis
Identify what the user is asking about:
- Feature type (skill, command, subagent, hook, plugin)
- Specific aspect (creation, configuration, best practices, examples)
- Level of detail needed (overview, specification, troubleshooting)

### Step 2: Documentation URL Selection
Determine which documentation page(s) to fetch:
- Start with the most relevant primary page
- Identify related pages for cross-referencing
- Consider the docs map for discovery if unsure

### Step 3: Content Retrieval
Use WebFetch to retrieve documentation:
```
WebFetch: {
  url: "https://code.claude.com/docs/en/[topic]",
  prompt: "Extract information about [specific query aspect]"
}
```

### Step 4: Information Synthesis
Analyze fetched content:
- Extract relevant sections
- Identify key specifications and requirements
- Find code examples and patterns
- Note best practices and warnings

### Step 5: Response Formation
Provide comprehensive answer:
- Direct answer to the user's question
- Relevant specifications or configurations
- Code examples when applicable
- Source citations (URLs)
- Related information or warnings

### Step 6: Verification
If information seems incomplete:
- Fetch additional related pages
- Cross-reference specifications
- Check for updates or additional details

## Examples

### Example 1: Understanding Subagents

**User Query:** "How do subagents work in Claude Code?"

**Skill Action:**
1. Fetch `https://code.claude.com/docs/en/sub-agents`
2. Extract key information about:
   - What subagents are
   - When to use them
   - YAML frontmatter format
   - System prompt structure
   - Tool inheritance
3. Provide comprehensive answer with citations

**Expected Response Pattern:**
```
Subagents in Claude Code are specialized agents that handle delegated sub-tasks
with isolated context windows. Here's how they work:

[Key information from docs]

YAML Format:
---
name: agent-identifier
description: When and why to delegate
tools: Read, Grep, Bash
model: sonnet|opus|haiku
---

[Additional details and examples]

Source: https://code.claude.com/docs/en/sub-agents
```

### Example 2: Hook Configuration

**User Query:** "What are the best practices for creating hooks?"

**Skill Action:**
1. Fetch `https://code.claude.com/docs/en/hooks-guide`
2. Extract security requirements and best practices
3. Provide practical guidance with examples

### Example 3: Skill Creation

**User Query:** "Show me how to create a skill with the correct YAML format"

**Skill Action:**
1. Fetch `https://code.claude.com/docs/en/skills`
2. Extract YAML specification
3. Provide complete format with field explanations
4. Include description best practices

### Example 4: Plugin Structure

**User Query:** "How do I package commands in a Claude Code plugin?"

**Skill Action:**
1. Fetch `https://code.claude.com/docs/en/plugins`
2. Extract plugin structure information
3. Provide directory layout and registration details

### Example 5: Multi-Page Research

**User Query:** "What's the difference between skills, commands, and subagents?"

**Skill Action:**
1. Fetch all three documentation pages
2. Extract key differentiators
3. Create comparison with citations
4. Provide decision guidance

## Common Patterns

### Pattern 1: Always Cite Sources
Every answer should include the source URL(s):
```
According to the official documentation:
[Information]

Source: https://code.claude.com/docs/en/[page]
```

### Pattern 2: Fetch Before Answering
Never guess or rely on outdated knowledge when documentation is available:
```
Let me check the official documentation...
[WebFetch call]
Based on the official docs: [answer]
```

### Pattern 3: Cross-Reference for Completeness
For complex questions, fetch multiple pages:
```
Let me check both the skills and subagents documentation...
[Multiple WebFetch calls]
Here's the complete picture: [synthesized answer]
```

### Pattern 4: Extract Code Examples
When docs include examples, extract and present them:
```
Here's the official example from the documentation:

[Code block from docs]

This shows [explanation].
```

### Pattern 5: Identify Updates
If documentation seems different from known patterns:
```
Note: The official documentation shows [current approach], which may differ
from older patterns.
```

## Troubleshooting

### Issue 1: Documentation Page Not Found
**Symptom:** 404 error or redirect
**Solution:**
- Try the docs map page to find correct URL
- Check for alternative page names
- Search for related pages

### Issue 2: Information Seems Outdated
**Symptom:** Conflicts with known behavior
**Solution:**
- Fetch documentation anyway (it may be updated)
- Note discrepancies in response
- Suggest testing/verification

### Issue 3: Too Much Information
**Symptom:** Documentation page is very long
**Solution:**
- Use specific prompts in WebFetch to focus extraction
- Fetch multiple times with different prompts
- Summarize key points relevant to query

### Issue 4: Missing Specific Details
**Symptom:** Docs don't cover exact scenario
**Solution:**
- Fetch related pages for additional context
- Combine information from multiple sources
- Provide best interpretation with caveats

## Best Practices

1. **Fetch First, Answer Second** - Always retrieve current documentation before responding
2. **Cite All Sources** - Include URLs for transparency and user follow-up
3. **Use Specific Prompts** - Target WebFetch prompts to extract relevant information efficiently
4. **Cross-Reference** - Fetch multiple pages for comprehensive answers
5. **Extract Examples** - Code examples from docs are highly valuable
6. **Note Discrepancies** - If docs conflict with known patterns, mention it
7. **Stay Current** - Documentation is the source of truth for current behavior
8. **Provide Context** - Explain not just "what" but "why" and "when"
9. **Link Related Topics** - Help users discover related documentation
10. **Verify Understanding** - If docs are unclear, fetch additional pages or ask clarifying questions

## When to Activate

This skill should activate for queries like:

- "How do I create a [skill/command/subagent/hook/plugin]?"
- "What's the YAML format for [artifact]?"
- "Show me the official documentation for [feature]"
- "What are best practices for [Claude Code feature]?"
- "How does [feature] work in Claude Code?"
- "What tools can [artifact] access?"
- "Check the Claude Code docs for [topic]"
- "What does the official documentation say about [feature]?"
- "code.claude.com says [something] - explain this"
- "I need the specification for [artifact]"
- "What's the difference between [feature A] and [feature B]?"

## Integration with Other Skills

This skill complements existing plugin skills:

- **artifact-advisor** - Provides decision framework, this provides specifications
- **artifact-validator** - Validates against patterns, this retrieves official specs
- **skill-builder** - Guides creation, this provides official requirements
- **claude-expert** - Has curated knowledge, this fetches current docs

Use claude-researcher when official, current documentation is needed to augment or verify the guidance from other skills.
