---
name: research-synthesis
description: Research best practices and synthesize into design decisions for artifact creation. Invoke BEFORE any creator skill to ensure research-backed decisions.
version: 1.0.0
model: claude-sonnet-4-5
invoked_by: both
user_invocable: true
tools:
  - mcp__Exa__web_search_exa
  - mcp__Exa__get_code_context_exa
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Glob
  - Grep
skills:
  - task-management-protocol
triggers:
  - 'research for'
  - 'best practices for'
  - 'before creating'
best_practices:
  - Execute minimum 3 research queries before synthesizing
  - Consult at least 3 external sources
  - Document existing codebase patterns
  - Provide rationale for every design decision
  - Include risk assessment with mitigations
error_handling: graceful
streaming: supported
output_location: .claude/context/artifacts/research-reports/
---

# Research Synthesis Skill

## Purpose

Gather and synthesize research BEFORE creating any new artifact (agent, skill, workflow, hook, schema, template). This skill ensures all design decisions are backed by:

1. **Current best practices** from authoritative sources
2. **Implementation patterns** from real-world examples
3. **Existing codebase conventions** to maintain consistency
4. **Risk assessment** to anticipate problems

## When to Invoke This Skill

**MANDATORY BEFORE:**

- `agent-creator` - Research agent patterns and domain expertise
- `skill-creator` - Research skill implementation best practices
- `workflow-creator` - Research orchestration patterns
- `hook-creator` - Research validation and safety patterns
- `schema-creator` - Research JSON Schema patterns
- `template-creator` - Research code scaffolding patterns

**RECOMMENDED FOR:**

- New feature design
- Architecture decisions
- Technology selection
- Integration planning

## The Iron Law

```
NO ARTIFACT CREATION WITHOUT RESEARCH FIRST
```

If you haven't executed the research protocol, you cannot proceed with artifact creation.

## MANDATORY Research Protocol

### Step 1: Define Research Scope

Before executing queries, clearly define:

```markdown
## Research Scope Definition

**Artifact Type**: [agent | skill | workflow | hook | schema | template]
**Domain/Capability**: [What this artifact will do]
**Key Questions**:

1. What are the best practices for this domain?
2. What implementation patterns exist?
3. What tools/frameworks should be used?
4. What are the common pitfalls?

**Existing Patterns to Examine**:

- .claude/[category]/ - Similar artifacts
- .claude/templates/ - Relevant templates
- .claude/schemas/ - Validation patterns
```

### Step 2: Execute Research Queries (Minimum 3)

Execute at least 3 research queries using available tools.

**Query 1: Best Practices**

```javascript
// Using Exa (preferred for technical content)
mcp__Exa__web_search_exa({
  query: '{artifact_type} {domain} best practices 2024 2025',
  numResults: 5,
});

// Or using WebSearch (fallback)
WebSearch({
  query: '{domain} best practices implementation guide',
});
```

**Query 2: Implementation Patterns**

```javascript
// Code-focused search
mcp__Exa__get_code_context_exa({
  query: '{domain} implementation patterns examples github',
  tokensNum: 5000,
});

// Or fetch from authoritative sources
WebFetch({
  url: 'https://[authoritative-source]/docs/{topic}',
});
```

**Query 3: Claude/AI Agent Specific**

```javascript
// Framework-specific patterns
mcp__Exa__web_search_exa({
  query: 'Claude AI agent {domain} {artifact_type} patterns',
  numResults: 5,
});

// Or search for MCP patterns
WebSearch({
  query: 'Model Context Protocol {domain} integration',
});
```

**Additional Queries (As Needed)**

```javascript
// Security considerations
WebSearch({ query: '{domain} security vulnerabilities mitigations' });

// Performance patterns
WebSearch({ query: '{domain} performance optimization techniques' });

// Error handling
WebSearch({ query: '{domain} error handling best practices' });
```

### Step 3: Analyze Existing Codebase

Before synthesizing, examine existing patterns in the codebase:

```javascript
// Find similar artifacts
Glob({ pattern: '.claude/{artifact_category}/**/*.md' });

// Search for related implementations
Grep({ pattern: '{related_keyword}', path: '.claude/' });

// Read existing examples
Read({ file_path: '.claude/{category}/{similar_artifact}' });
```

**What to Extract:**

1. **Naming conventions** - How are similar artifacts named?
2. **Structure patterns** - What sections do they include?
3. **Tool usage** - What tools do similar artifacts use?
4. **Skill dependencies** - What skills are commonly assigned?
5. **Output locations** - Where do artifacts save their outputs?

### Step 4: Synthesize Findings

Output a structured research report in the following format:

```markdown
## Research Report: {Artifact Name}

**Date**: {YYYY-MM-DD}
**Researcher**: research-synthesis skill
**Artifact Type**: {type}
**Domain**: {domain}

---

### Research Queries Executed

| #   | Query       | Tool      | Sources Found | Key Finding     |
| --- | ----------- | --------- | ------------- | --------------- |
| 1   | "{query_1}" | Exa       | 5             | {brief_finding} |
| 2   | "{query_2}" | WebSearch | 3             | {brief_finding} |
| 3   | "{query_3}" | Exa Code  | 4             | {brief_finding} |

---

### Existing Codebase Patterns

**Similar Artifacts Found:**

- `{path_1}` - {what it does, what patterns it uses}
- `{path_2}` - {what it does, what patterns it uses}

**Conventions Identified:**

- Naming: {convention}
- Structure: {convention}
- Tools: {convention}
- Output: {convention}

---

### Best Practices Identified

| #   | Practice   | Source               | Confidence | Rationale        |
| --- | ---------- | -------------------- | ---------- | ---------------- |
| 1   | {practice} | {source_url_or_name} | High       | {why_applicable} |
| 2   | {practice} | {source_url_or_name} | Medium     | {why_applicable} |
| 3   | {practice} | {source_url_or_name} | High       | {why_applicable} |

**Confidence Levels:**

- **High**: Multiple authoritative sources agree
- **Medium**: Single authoritative source or multiple secondary sources
- **Low**: Limited evidence, requires validation

---

### Design Decisions

| Decision     | Rationale | Source   | Alternatives Considered    |
| ------------ | --------- | -------- | -------------------------- |
| {decision_1} | {why}     | {source} | {what_else_was_considered} |
| {decision_2} | {why}     | {source} | {what_else_was_considered} |
| {decision_3} | {why}     | {source} | {what_else_was_considered} |

---

### Recommended Implementation

**File Location**: `.claude/{category}/{name}/`

**Template to Use**: `.claude/templates/{template}.md`

**Skills to Invoke**:

- `{skill_1}` - {why}
- `{skill_2}` - {why}

**Hooks Needed**:

- `{hook_type}` - {purpose}

**Dependencies**:

- Existing artifacts: {list}
- External tools: {list}

---

### Risk Assessment

| Risk     | Likelihood | Impact | Mitigation       |
| -------- | ---------- | ------ | ---------------- |
| {risk_1} | Medium     | High   | {how_to_prevent} |
| {risk_2} | Low        | Medium | {how_to_prevent} |
| {risk_3} | High       | Low    | {how_to_prevent} |

---

### Quality Gate Checklist

Before proceeding to artifact creation, verify:

- [ ] Minimum 3 research queries executed
- [ ] At least 3 external sources consulted
- [ ] Existing codebase patterns documented
- [ ] All design decisions have rationale and source
- [ ] Risk assessment completed with mitigations
- [ ] Recommended implementation path documented

---

### Next Steps

1. **Invoke creator skill**: `Skill({ skill: "{creator_skill}" })`
2. **Use this report as input**: Reference decisions above
3. **Validate against checklist**: Before marking complete
```

## Integration with Creator Skills

### Pre-Creation Workflow

```text
[AGENT] User requests: "Create a Slack notification skill"

[AGENT] Step 1: Research first
Skill({ skill: "research-synthesis" })

[RESEARCH-SYNTHESIS] Executing research protocol...
- Query 1: "Slack API best practices 2025"
- Query 2: "Slack MCP server integration patterns"
- Query 3: "Claude AI Slack notification skill"
- Analyzing: .claude/skills/*/SKILL.md for patterns
- Output: Research Report saved

[AGENT] Step 2: Create with research backing
Skill({ skill: "skill-creator" })

[SKILL-CREATOR] Using research report...
- Following design decisions from report
- Applying identified best practices
- Mitigating documented risks
```

### Handoff Format

After completing research, provide this handoff to the creator skill:

```markdown
## Research Handoff to: {creator_skill}

**Report Location**: `.claude/context/artifacts/research-reports/{artifact_name}-research.md`

**Summary**:
{2-3 sentence summary of key findings}

**Critical Decisions**:

1. {decision_1}
2. {decision_2}
3. {decision_3}

**Proceed with creation**: YES/NO
**Confidence Level**: High/Medium/Low
```

## Quality Gate

Research is complete when ALL items pass:

```
[ ] Minimum 3 research queries executed
[ ] At least 3 external sources consulted (URLs or authoritative names)
[ ] Existing codebase patterns documented (at least 2 similar artifacts)
[ ] ALL design decisions have rationale AND source
[ ] Risk assessment completed (at least 3 risks with mitigations)
[ ] Recommended implementation path documented
[ ] Report saved to output location
```

**BLOCKING**: If any item fails, research is INCOMPLETE. Do not proceed to artifact creation.

## Output Locations

- Research reports: `.claude/context/artifacts/research-reports/`
- Temporary notes: `.claude/context/tmp/research/`
- Memory updates: `.claude/context/memory/learnings.md`

## Examples

### Example 1: Research Before Creating Slack Skill

```javascript
// Step 1: Define scope
// Artifact: skill, Domain: Slack notifications

// Step 2: Execute queries
mcp__Exa__web_search_exa({
  query: 'Slack API webhook best practices 2025',
  numResults: 5,
});

mcp__Exa__get_code_context_exa({
  query: 'Slack notification system implementation Node.js',
  tokensNum: 5000,
});

WebSearch({
  query: 'Claude AI MCP Slack server integration',
});

// Step 3: Analyze codebase
Glob({ pattern: '.claude/skills/*notification*/SKILL.md' });
Glob({ pattern: '.claude/skills/*slack*/SKILL.md' });
Read({ file_path: '.claude/skills/skill-creator/SKILL.md' });

// Step 4: Synthesize and output report
Write({
  file_path: '.claude/context/artifacts/research-reports/slack-notifications-research.md',
  content: '## Research Report: Slack Notifications Skill...',
});
```

### Example 2: Research Before Creating Database Agent

```javascript
// Research queries for database-architect agent
mcp__Exa__web_search_exa({
  query: 'database design architecture best practices 2025',
  numResults: 5,
});

WebFetch({
  url: 'https://docs.postgresql.org/current/ddl.html',
});

mcp__Exa__web_search_exa({
  query: 'AI agent database schema design automation',
  numResults: 5,
});

// Analyze existing agents
Glob({ pattern: '.claude/agents/domain/*data*.md' });
Read({ file_path: '.claude/agents/core/developer.md' });
```

## Common Research Domains

| Domain          | Key Queries                                      | Authoritative Sources       |
| --------------- | ------------------------------------------------ | --------------------------- |
| API Integration | "REST API design", "GraphQL patterns"            | OpenAPI spec, GraphQL spec  |
| Security        | "OWASP top 10", "security best practices"        | OWASP, NIST                 |
| Database        | "database design patterns", "SQL optimization"   | PostgreSQL docs, MySQL docs |
| Frontend        | "React patterns", "accessibility WCAG"           | React docs, W3C             |
| DevOps          | "CI/CD best practices", "IaC patterns"           | GitLab docs, Terraform docs |
| Testing         | "TDD patterns", "test automation"                | Testing Library, Jest docs  |
| AI/ML           | "LLM integration patterns", "prompt engineering" | Anthropic docs, OpenAI docs |

## File Placement & Standards

### Output Location Rules

This skill outputs to: `.claude/context/artifacts/research-reports/`

### Mandatory References

- **File Placement**: See `.claude/docs/FILE_PLACEMENT_RULES.md`
- **Developer Workflow**: See `.claude/docs/DEVELOPER_WORKFLOW.md`
- **Artifact Naming**: See `.claude/docs/ARTIFACT_NAMING.md`

### Enforcement

File placement is enforced by `file-placement-guard.cjs` hook.
Invalid placements will be blocked in production mode.

---

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

Check for:

- Previous research on similar domains
- Known patterns and conventions
- Documented decisions

**After completing:**

- New research findings -> Append to `.claude/context/memory/learnings.md`
- Important decisions -> Append to `.claude/context/memory/decisions.md`
- Issues found -> Append to `.claude/context/memory/issues.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

## Workflow Integration

This skill integrates with the Creator Ecosystem:

| Creator            | Research Focus                                       |
| ------------------ | ---------------------------------------------------- |
| `agent-creator`    | Domain expertise, agent patterns, skill dependencies |
| `skill-creator`    | Tool integration, MCP patterns, validation hooks     |
| `workflow-creator` | Orchestration patterns, multi-agent coordination     |
| `hook-creator`     | Validation patterns, security checks, safety gates   |
| `schema-creator`   | JSON Schema patterns, validation strategies          |
| `template-creator` | Code scaffolding, project structure patterns         |

**Full lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

---

## Iron Laws of Research Synthesis

```
1. NO CREATION WITHOUT RESEARCH FIRST
   - Skip research = uninformed decisions = bugs and rework
   - Research ALWAYS precedes creation

2. NO RESEARCH WITHOUT QUERIES
   - Minimum 3 queries from different angles
   - Thinking != research. Execute the queries.

3. NO SYNTHESIS WITHOUT CODEBASE ANALYSIS
   - External research is necessary but not sufficient
   - MUST examine existing patterns for consistency

4. NO DECISIONS WITHOUT RATIONALE
   - Every decision needs a source
   - "I think" is not a source. Link to evidence.

5. NO PROCEEDING WITHOUT QUALITY GATE
   - All checklist items must pass
   - BLOCKING: Incomplete research = no creation
```
