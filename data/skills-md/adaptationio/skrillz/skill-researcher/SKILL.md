---
name: skill-researcher
description: Comprehensive research toolkit for discovering patterns, best practices, and technical knowledge across Web search, MCP servers, GitHub repositories, and documentation. Use when researching technologies, exploring codebases, finding examples, or gathering requirements for skill development.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Skill Researcher

## Overview

skill-researcher provides systematic research operations for gathering information from multiple sources. It enables comprehensive exploration of technologies, patterns, and best practices across Web search, MCP servers, GitHub repositories, and official documentation.

**Purpose**: Research and gather knowledge for informed skill development

**Pattern**: Task-based (5 independent research operations)

**Key Benefit**: Comprehensive, multi-source research that uncovers patterns, examples, and best practices

## When to Use

Use skill-researcher when:
- Starting a new skill (research domain, patterns, examples)
- Exploring unfamiliar technology or framework
- Looking for real-world examples and patterns
- Gathering requirements from multiple sources
- Validating approaches against community practices
- Discovering MCP servers for integration
- Finding official documentation and specifications

## Prerequisites

Before conducting research:
- **Clear research goal**: Know what you're trying to discover
- **Research questions**: Specific questions to answer
- **Source selection**: Which sources are most relevant
- **Synthesis plan**: How findings will be combined

## Research Operations

### Operation 1: Web Search Research

Conduct targeted web searches to discover current best practices, recent developments, and community knowledge.

**When to Use**:
- Researching current best practices (2024-2025)
- Finding recent blog posts and tutorials
- Discovering community discussions
- Locating official announcements
- Comparing different approaches

**Prerequisites**:
- Clear search query (specific, targeted)
- Knowledge of what you're looking for
- Ability to evaluate source credibility

**Steps**:

1. **Formulate Search Query**:
   - Use specific technical terms
   - Include year for recent results (2024, 2025)
   - Add qualifiers: "best practices", "tutorial", "guide", "documentation"
   - Combine terms strategically

   Example queries:
   ```
   "Claude Code skills" best practices 2025
   "MCP server" development guide
   "progressive disclosure" documentation pattern
   ```

2. **Execute Search**:
   - Use WebSearch tool with formulated query
   - Review returned results for relevance
   - Note source credibility (official docs > blog posts > forums)

3. **Extract Key Information**:
   - Identify patterns mentioned across multiple sources
   - Note specific techniques or approaches
   - Capture code examples
   - Record URLs for reference

4. **Evaluate Credibility**:
   - Official documentation: Highest credibility
   - Established tech blogs: High credibility
   - GitHub repos with activity: Medium-high credibility
   - Forums/discussions: Medium credibility (verify)
   - Personal blogs: Lower credibility (verify against other sources)

5. **Document Findings**:
   - Summarize key points
   - Note sources (URLs)
   - Highlight patterns across sources
   - Identify areas needing deeper research

**Example**:

```markdown
Research Goal: Best practices for Claude Code skill organization

Search Query: "Claude Code skills" progressive disclosure 2025

Findings:
1. Progressive disclosure pattern (from official Anthropic docs):
   - SKILL.md: Main entry, <5000 words
   - references/: Detailed guides, on-demand
   - scripts/: Automation utilities

2. YAML frontmatter requirements (from skill-creator):
   - name: hyphen-case
   - description: with "Use when" triggers

3. Community patterns (from 40+ skills analyzed):
   - Workflow-based: 45% of skills
   - Task-based: 30% of skills
   - Reference: 15% of skills
   - Capabilities: 10% of skills

Sources:
- https://docs.claude.com/en/docs/claude-code/...
- https://github.com/anthropics/anthropic-skills/...
```

**Expected Outcome**:
- Comprehensive findings document
- Multiple credible sources cited
- Patterns identified across sources
- Specific examples captured
- Areas for deeper research noted

**Validation**:
- [ ] Search query was specific and targeted
- [ ] Multiple sources consulted (minimum 3-5)
- [ ] Source credibility evaluated
- [ ] Key patterns identified and documented
- [ ] URLs/references captured for verification

**Common Issues**:
- **Issue**: Search too broad, overwhelming results
  - **Solution**: Add specific technical terms, year constraints
- **Issue**: Conflicting information across sources
  - **Solution**: Prioritize official docs, look for consensus patterns
- **Issue**: Outdated information
  - **Solution**: Filter by date, search for "2024" or "2025"

**Tips for Effective Web Search**:
- Start broad, then narrow based on initial findings
- Use quotes for exact phrases: "progressive disclosure"
- Combine terms: "Claude Code" + "best practices"
- Include current year for recent content
- Check multiple page results, not just first one

---

### Operation 2: MCP Server Research

Discover and research Model Context Protocol (MCP) servers for potential integration.

**When to Use**:
- Building skills that need external tool access
- Researching available MCP servers
- Evaluating MCP server capabilities
- Planning MCP server integration
- Discovering domain-specific MCP tools

**Prerequisites**:
- Understanding of MCP protocol basics
- Knowledge of integration requirements
- Capability requirements defined

**Steps**:

1. **Search for MCP Servers**:
   - Web search: "MCP server" + domain/capability
   - GitHub search: "MCP server" or "Model Context Protocol"
   - Anthropic official MCP server list
   - Community MCP server directories

   Example searches:
   ```
   "MCP server" database access
   "Model Context Protocol" file system
   GitHub: topic:mcp-server
   ```

2. **Evaluate Server Capabilities**:
   - Read server documentation
   - Review available tools/functions
   - Check supported platforms (Python, Node, etc.)
   - Verify installation requirements
   - Assess maturity (stars, commits, issues)

3. **Analyze Integration Requirements**:
   - Installation process complexity
   - Configuration needs
   - Authentication requirements
   - API surface (what tools does it expose?)
   - Dependencies and prerequisites

4. **Test Availability** (if applicable):
   - Check if server is installed in environment
   - Verify tools are accessible
   - Test basic operations
   - Note any limitations or quirks

5. **Document Capabilities**:
   - Server name and purpose
   - Available tools with descriptions
   - Installation/setup steps
   - Configuration requirements
   - Use case examples
   - Limitations or constraints

**Example**:

```markdown
Research Goal: Find MCP servers for file system operations

Servers Found:

1. **filesystem MCP Server** (Official Anthropic)
   - Tools: read_file, write_file, edit_file, list_directory, search_files
   - Platform: Python, Node
   - Installation: npm install @modelcontextprotocol/server-filesystem
   - Use Case: File operations in Claude Code skills
   - Maturity: Official, well-maintained
   - Limitations: Limited to local filesystem

2. **aws-s3 MCP Server** (Community)
   - Tools: s3_read, s3_write, s3_list, s3_delete
   - Platform: Python
   - Installation: pip install mcp-server-aws-s3
   - Use Case: Cloud storage integration
   - Maturity: 150 stars, active development
   - Limitations: Requires AWS credentials

Recommendation: Use official filesystem server for local operations,
consider aws-s3 for cloud storage needs.
```

**Expected Outcome**:
- List of relevant MCP servers
- Capability comparison
- Integration requirements documented
- Recommendation for usage
- Installation/setup instructions

**Validation**:
- [ ] Multiple MCP servers researched (3-5)
- [ ] Capabilities documented for each
- [ ] Installation requirements captured
- [ ] Integration complexity assessed
- [ ] Recommendations provided with rationale

**Common Issues**:
- **Issue**: Server not in official list
  - **Solution**: Search GitHub, check community directories
- **Issue**: Unclear capabilities
  - **Solution**: Read source code, check examples folder
- **Issue**: Installation fails
  - **Solution**: Check prerequisites, consult documentation

**Tips for MCP Research**:
- Start with official Anthropic MCP servers
- Check GitHub topics: "mcp-server", "model-context-protocol"
- Read server README thoroughly
- Look for examples/ directory in repo
- Check issue tracker for known problems

---

### Operation 3: GitHub Repository Research

Explore GitHub repositories to discover implementation patterns, code examples, and architectural approaches.

**When to Use**:
- Looking for real-world implementation examples
- Researching code patterns and structures
- Finding proven architectural approaches
- Discovering edge case handling
- Learning from production codebases

**Prerequisites**:
- GitHub access (for cloning, exploration)
- Clear research objective (what patterns to find)
- Ability to read and analyze code
- Understanding of relevant technologies

**Steps**:

1. **Find Relevant Repositories**:
   - Search GitHub by topic, language, keywords
   - Look for official repositories
   - Check stars, activity, recent commits
   - Review README for relevance

   Example searches:
   ```
   topic:claude-code language:markdown
   "Claude Code skill" in:readme
   anthropic/anthropic-skills
   ```

2. **Analyze Repository Structure**:
   - Examine directory organization
   - Review file naming conventions
   - Note configuration patterns
   - Identify architectural decisions

3. **Extract Code Patterns**:
   - Look for repeated patterns across files
   - Note error handling approaches
   - Examine state management
   - Study API usage patterns
   - Capture validation techniques

4. **Document Examples**:
   - Copy relevant code snippets
   - Note file locations (repo:path:lines)
   - Explain pattern purpose
   - Document context of usage

5. **Synthesize Learnings**:
   - Identify common patterns across repos
   - Note variations and reasons
   - Extract best practices
   - Document anti-patterns to avoid

**Example**:

```markdown
Research Goal: How to structure Claude Code skills with workflows

Repository: anthropic/anthropic-skills (example-skills)

Findings:

1. **Workflow Structure Pattern** (deployment-guide/SKILL.md):
   ```markdown
   ## Deployment Workflow

   ### Step 1: Prepare Application
   [Instructions]

   ### Step 2: Configure Railway
   [Instructions]

   ### Step 3: Deploy
   [Instructions]
   ```
   - Pattern: Sequential steps with clear headers
   - Each step is self-contained
   - Prerequisites stated upfront

2. **Reference Organization** (medirecords-integration/):
   ```
   medirecords-integration/
   ├── SKILL.md (overview + workflow)
   ├── references/
   │   ├── fhir-resources.md
   │   ├── api-endpoints.md
   │   └── error-handling.md
   ```
   - Pattern: Main file lean, details in references
   - Topic-based reference files
   - On-demand loading

3. **YAML Frontmatter Pattern** (all skills):
   ```yaml
   ---
   name: skill-name
   description: [What it does]. Use when [triggers].
   ---
   ```
   - Consistent across all skills
   - Description includes triggers
   - Hyphen-case naming

Patterns Identified:
- Sequential workflows use numbered steps
- Reference files for detailed content
- Examples in every major section
- Validation checklists common

Sources:
- https://github.com/anthropics/anthropic-skills/tree/main/examples/deployment-guide
- https://github.com/anthropics/anthropic-skills/tree/main/examples/medirecords-integration
```

**Expected Outcome**:
- Code patterns documented with examples
- File/directory structures captured
- Architectural approaches identified
- Best practices extracted
- Repository sources cited

**Validation**:
- [ ] Multiple repositories analyzed (3-5 minimum)
- [ ] Code snippets captured with location references
- [ ] Patterns identified across repositories
- [ ] Context of usage documented
- [ ] Best practices vs anti-patterns distinguished

**Common Issues**:
- **Issue**: Repository too large to analyze
  - **Solution**: Focus on specific directories relevant to research goal
- **Issue**: Code patterns unclear
  - **Solution**: Read tests, examples, documentation first
- **Issue**: Outdated repository
  - **Solution**: Check commit dates, look for active forks

**Tips for GitHub Research**:
- Use advanced search (stars:>100, language:python, etc.)
- Check examples/ or samples/ directories first
- Read CONTRIBUTING.md for patterns
- Look at tests/ for usage examples
- Check issues for edge cases and solutions

---

### Operation 4: Documentation Research

Analyze official documentation to understand specifications, APIs, and recommended practices.

**When to Use**:
- Learning official specifications
- Understanding API surface
- Finding authoritative guidance
- Validating approaches against official recommendations
- Discovering feature capabilities

**Prerequisites**:
- Link to official documentation
- Clear questions to answer
- Ability to navigate documentation structure
- Note-taking system

**Steps**:

1. **Locate Official Documentation**:
   - Find primary documentation site
   - Identify relevant sections
   - Check for API reference, guides, tutorials
   - Note documentation version/date

   Example sources:
   ```
   https://docs.claude.com/en/docs/claude-code/
   https://modelcontextprotocol.io/
   https://docs.anthropic.com/
   ```

2. **Navigate Documentation Structure**:
   - Start with overview/getting started
   - Read conceptual guides for understanding
   - Review API reference for specifics
   - Check examples/tutorials for patterns
   - Look for best practices section

3. **Extract Key Information**:
   - Core concepts and definitions
   - API functions and parameters
   - Configuration options
   - Limitations and constraints
   - Best practices and recommendations
   - Common patterns shown in examples

4. **Capture Specifics**:
   - Copy code examples exactly
   - Note parameter types and constraints
   - Document return values
   - Record error conditions
   - Capture configuration formats

5. **Create Reference Document**:
   - Organize by topic/feature
   - Include code examples
   - Note page URLs for verification
   - Highlight important warnings/notes
   - Document version information

**Example**:

```markdown
Research Goal: Claude Code skill structure requirements

Source: https://docs.claude.com/en/docs/claude-code/skills

Findings:

1. **Skill Structure Requirements**:
   - SKILL.md must have YAML frontmatter
   - Frontmatter fields: name, description
   - Progressive disclosure: SKILL.md < 15,000 words
   - Use references/ for detailed content
   - scripts/ for automation utilities

2. **YAML Frontmatter Specification**:
   ```yaml
   ---
   name: skill-name-in-hyphen-case
   description: Brief description. Use when [triggers].
   ---
   ```
   - name: Must match directory name
   - description: Should include discovery triggers

3. **Organizational Patterns**:
   - Workflow-based: Sequential steps (→)
   - Task-based: Independent operations (no order)
   - Reference/Guidelines: Standards and patterns
   - Capabilities-based: Multiple features

4. **Best Practices** (from docs):
   - Keep SKILL.md focused and scannable
   - Use examples liberally
   - Include validation criteria
   - Provide context for decisions
   - Test with real scenarios

5. **Limitations**:
   - SKILL.md size: recommended < 5,000 words for performance
   - No dynamic content (static markdown)
   - File paths must be relative

Source URLs:
- https://docs.claude.com/en/docs/claude-code/skills#structure
- https://docs.claude.com/en/docs/claude-code/skills#patterns
- https://docs.claude.com/en/docs/claude-code/skills#best-practices
```

**Expected Outcome**:
- Comprehensive documentation summary
- Specific requirements captured
- Code examples copied accurately
- URLs referenced for verification
- Version/date noted

**Validation**:
- [ ] Official documentation identified and verified
- [ ] Key concepts extracted and defined
- [ ] Code examples captured accurately
- [ ] Specifications documented precisely
- [ ] Page URLs recorded for reference
- [ ] Version/date information noted

**Common Issues**:
- **Issue**: Documentation unclear or incomplete
  - **Solution**: Check examples, search for supplementary guides
- **Issue**: Multiple documentation versions
  - **Solution**: Use most recent, note version explicitly
- **Issue**: Conflicting information
  - **Solution**: Reference official docs over community content

**Tips for Documentation Research**:
- Start with "Getting Started" or "Quickstart"
- Read conceptual guides before API reference
- Check changelog/releases for recent changes
- Look for "Best Practices" or "Recommendations" sections
- Copy examples exactly (don't paraphrase)
- Note warnings and "gotchas" prominently

---

### Operation 5: Synthesize Research Findings

Combine research from multiple sources into coherent, actionable insights.

**When to Use**:
- After completing research across multiple sources
- Before making architectural decisions
- When creating skill plans or specifications
- After gathering requirements
- To identify patterns and best practices

**Prerequisites**:
- Research completed from 2+ sources
- Findings documented from each source
- Research goal clearly defined
- Note-taking system used

**Steps**:

1. **Organize Findings by Theme**:
   - Group related findings together
   - Identify common topics across sources
   - Note unique findings from each source
   - Create topical categories

   Example themes:
   - Architecture/Structure
   - Best Practices
   - Common Patterns
   - Anti-Patterns
   - Requirements/Constraints
   - Examples

2. **Identify Patterns**:
   - What appears across multiple sources?
   - What's consistent vs. what varies?
   - Which sources agree/disagree?
   - What's the consensus approach?

3. **Evaluate Credibility**:
   - Official docs > established practices > individual opinions
   - Recent sources > older sources (for current practices)
   - Multiple confirmations > single source
   - Production examples > theoretical discussions

4. **Resolve Conflicts**:
   - If sources disagree, prioritize official documentation
   - Consider context differences
   - Look for evolution over time
   - Note when multiple valid approaches exist

5. **Create Synthesis Document**:

   **Template**:
   ```markdown
   # Research Synthesis: [Topic]

   ## Research Goal
   [What we set out to discover]

   ## Sources Consulted
   1. [Source 1]: [Type, date, credibility]
   2. [Source 2]: [Type, date, credibility]
   3. [Source 3]: [Type, date, credibility]

   ## Key Findings

   ### [Theme 1]
   **Pattern**: [What's consistent across sources]
   **Sources**: [Which sources confirm this]
   **Evidence**: [Specific examples or quotes]

   ### [Theme 2]
   [Same structure]

   ## Best Practices Identified
   1. [Practice 1] - from [sources]
   2. [Practice 2] - from [sources]

   ## Anti-Patterns to Avoid
   1. [Anti-pattern 1] - why to avoid
   2. [Anti-pattern 2] - why to avoid

   ## Conflicting Information
   [Any disagreements, with resolution]

   ## Recommendations
   1. [Actionable recommendation based on research]
   2. [Actionable recommendation based on research]

   ## Examples
   [Concrete code/structure examples from research]

   ## References
   - [URL 1]: [Description]
   - [URL 2]: [Description]
   ```

6. **Extract Actionable Insights**:
   - What decisions can be made?
   - What approaches should be used?
   - What should be avoided?
   - What needs further research?

**Example**:

```markdown
# Research Synthesis: Claude Code Skill Organization

## Research Goal
Determine best practices for organizing Claude Code skills with comprehensive workflows.

## Sources Consulted
1. Official Claude Code documentation (2025, official, highest credibility)
2. anthropic/anthropic-skills GitHub (2025, official examples, high credibility)
3. Web search results: "Claude Code skills" best practices (2024-2025, mixed credibility)

## Key Findings

### Progressive Disclosure Pattern
**Pattern**: Three-tier architecture (SKILL.md → references/ → scripts/)
**Sources**: Official docs, all official examples, community consensus
**Evidence**:
- Docs state: "SKILL.md recommended < 5,000 words"
- All 7 official examples use this pattern
- Community skills (40+ analyzed) overwhelmingly use this

### Workflow Organization
**Pattern**: Sequential steps with clear numbering and transitions
**Sources**: deployment-guide, medirecords-integration examples
**Evidence**:
```markdown
## Step 1: [Action]
[Content]
**Next**: Proceed to Step 2
```

### YAML Frontmatter
**Pattern**: Minimal (name + description only)
**Sources**: All official examples, documentation
**Evidence**: Consistent across 100% of examples

## Best Practices Identified
1. Keep SKILL.md under 5,000 words (from official docs + all examples)
2. Use numbered workflow steps with transitions (from 6/7 workflow examples)
3. Include validation checklists (from 5/7 examples)
4. Provide examples in every major section (from documentation + examples)
5. Use hyphen-case for naming (from all official skills)

## Anti-Patterns to Avoid
1. Monolithic SKILL.md files (>10,000 words) - hurts performance
2. Missing YAML frontmatter - skill won't be discovered
3. No examples - users can't visualize usage
4. Vague validation criteria - can't verify success

## Recommendations
1. Use three-tier progressive disclosure for all skills
2. Adopt numbered workflow steps with transitions
3. Include validation checklist in each step/operation
4. Provide 2-3 examples per major concept
5. Keep SKILL.md focused (<3,000 words ideal, <5,000 max)

## Examples
[From synthesis document, include actual code]

## References
- https://docs.claude.com/en/docs/claude-code/skills
- https://github.com/anthropics/anthropic-skills/
```

**Expected Outcome**:
- Comprehensive synthesis document
- Clear patterns identified
- Actionable recommendations
- Conflicts resolved
- Sources cited

**Validation**:
- [ ] Findings from all sources incorporated
- [ ] Patterns identified across multiple sources
- [ ] Recommendations are actionable
- [ ] Conflicts identified and resolved
- [ ] Sources properly cited
- [ ] Document organized clearly

**Common Issues**:
- **Issue**: Too much information, overwhelmed
  - **Solution**: Focus on research goal, organize by theme
- **Issue**: Contradictory findings
  - **Solution**: Prioritize official sources, note context differences
- **Issue**: Can't find patterns
  - **Solution**: Look for what appears 2-3+ times across sources

**Tips for Synthesis**:
- Use consistent format for all research findings
- Group similar findings before synthesizing
- Prioritize quality over quantity (3 good sources > 10 weak)
- Make recommendations specific and actionable
- Note what you still don't know (further research needed)

---

## Best Practices

### Research Process

**1. Define Clear Research Goals**:
- Specific questions to answer
- Success criteria for research
- Time constraints
- Sources to prioritize

**2. Multi-Source Validation**:
- Never rely on single source
- Cross-reference findings (3-5 sources)
- Prioritize official documentation
- Check recent dates (2024-2025)

**3. Document Thoroughly**:
- Capture URLs and dates
- Quote precisely (don't paraphrase)
- Note source credibility
- Include context

**4. Synthesize Systematically**:
- Organize by theme
- Identify patterns
- Resolve conflicts
- Create actionable insights

**5. Iterate and Refine**:
- Start broad, then narrow
- Deep dive promising areas
- Validate assumptions
- Fill gaps as discovered

### Source Credibility Hierarchy

1. **Official Documentation** (Highest)
   - Anthropic official docs
   - Technology official docs
   - Specifications and RFCs

2. **Official Examples** (Very High)
   - Anthropic example skills
   - Official GitHub repositories
   - Reference implementations

3. **Established Community** (High)
   - Well-maintained open source projects (1000+ stars)
   - Recognized experts' content
   - Production codebases

4. **Community Content** (Medium)
   - Blog posts from developers
   - GitHub repositories (100-1000 stars)
   - Technical forums (validated answers)

5. **Individual Opinions** (Lower - verify)
   - Personal blogs
   - Unverified forum posts
   - Small repositories

## Common Mistakes

### Mistake 1: Single Source Research

**Problem**: Relying on one source, missing broader context
- Only read one blog post
- Trust first search result
- Skip official documentation

**Fix**: Always consult 3-5 sources, prioritize official docs

### Mistake 2: No Source Documentation

**Problem**: Can't verify findings or provide references
- No URLs captured
- Can't remember where information came from
- Unable to validate later

**Fix**: Document source URL, date, and credibility for every finding

### Mistake 3: Accepting Outdated Information

**Problem**: Using old practices that have evolved
- 2020 blog post (pre-Claude Code)
- Deprecated APIs
- Old best practices

**Fix**: Filter by date, search for "2024" or "2025", check official docs

### Mistake 4: Skipping Synthesis

**Problem**: Have data but no insights
- Raw notes without organization
- Can't make decisions
- No actionable recommendations

**Fix**: Always synthesize findings into themes and recommendations

### Mistake 5: Ignoring Credibility

**Problem**: Treating all sources equally
- Personal blog = official docs
- Unverified forum post = production code
- Single example = standard pattern

**Fix**: Evaluate credibility, prioritize authoritative sources

## Integration with Other Skills

### With planning-architect

**Use skill-researcher** before planning to gather requirements and patterns
- Research informs planning decisions
- Examples guide structure choices
- Best practices shape approach

**Flow**: research → gather insights → plan skill → build

### With skill-builder-generic

**Use skill-researcher** to discover patterns for skill building
- Research skill examples
- Find organizational patterns
- Discover best practices

**Flow**: research skills → identify patterns → apply to new skill

### With prompt-builder

**Use skill-researcher** to find prompt examples and patterns
- Research effective prompts
- Discover prompt engineering techniques
- Find validation approaches

**Flow**: research prompts → apply principles → build better prompts

## Quick Reference

### The 5 Research Operations

1. **Web Search** - Current practices, tutorials, discussions (WebSearch tool)
2. **MCP Servers** - Discover and evaluate MCP servers for integration
3. **GitHub** - Code patterns, structures, implementations
4. **Documentation** - Official specs, APIs, authoritative guidance
5. **Synthesize** - Combine findings into actionable insights

### Research Quality Checklist

- [ ] Clear research goal defined
- [ ] Multiple sources consulted (3-5+)
- [ ] Source credibility evaluated
- [ ] Findings documented with URLs and dates
- [ ] Patterns identified across sources
- [ ] Conflicts resolved
- [ ] Synthesis document created
- [ ] Recommendations are actionable

### Source Selection Guide

**For current best practices**: Web search (2024-2025)
**For specifications**: Official documentation
**For code patterns**: GitHub repositories
**For integrations**: MCP server research
**For validation**: Multiple sources + synthesis

---

For detailed guides on each research type, see the references/ directory.

For research automation tools, use scripts/research-helper.py.
