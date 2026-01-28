---
name: skill-router
description: Intelligently routes user requests to the most appropriate Claude Code skill. ALWAYS use this skill FIRST when user asks for help, mentions "skill", "which", "how to", or seems unsure about which approach to take. This is the default entry point for all skill-related requests.
allowed-tools: Read, AskUserQuestion, WebSearch, Grep
metadata:
  hooks:
    after_complete:
      - trigger: session-logger
        mode: auto
        reason: "Log skill routing decisions"
---

# Skill Router

An intelligent router that analyzes user requests and recommends the most appropriate Claude Code skill for the task.

## When This Skill Activates

This skill activates when you:
- Ask "which skill should I use?" or "what skill can help with...?"
- Say "use a skill" without specifying which one
- Express a need but aren't sure which skill fits
- Mention "skill router" or "help me find a skill"

## Available Skills Catalog

### Core Development

| Skill | Best For |
|-------|----------|
| `commit-helper` | Writing Git commit messages, formatting commits |
| `code-reviewer` | Reviewing PRs, code changes, quality checks |
| `debugger` | Diagnosing bugs, errors, unexpected behavior |
| `refactoring-specialist` | Improving code structure, reducing technical debt |

### Design & UX

| Skill | Best For |
|-------|----------|
| `figma-designer` | Analyzing Figma designs and producing implementation-ready visual specs/PRDs |

### Documentation & Testing

| Skill | Best For |
|-------|----------|
| `documentation-engineer` | Writing README, technical docs, code documentation |
| `api-documenter` | Creating OpenAPI/Swagger specifications |
| `test-automator` | Writing tests, setting up test frameworks |
| `qa-expert` | Test strategy, quality gates, QA processes |

### Architecture & DevOps

| Skill | Best For |
|-------|----------|
| `api-designer` | Designing REST/GraphQL APIs, API architecture |
| `security-auditor` | Security audits, vulnerability reviews, OWASP Top 10 |
| `performance-engineer` | Performance optimization, speed analysis |
| `deployment-engineer` | CI/CD pipelines, deployment automation |

### Planning & Analysis

| Skill | Best For |
|-------|----------|
| `architecting-solutions` | Creating PRDs, solution design, requirements analysis |
| `planning-with-files` | Multi-step task planning, persistent file-based organization |
| `self-improving-agent` | Universal self-improvement that learns from all skill experiences |

## Routing Process

### Step 1: Intent Analysis

Analyze the user's request to identify:
- **Task Type**: What does the user want to accomplish?
- **Context**: What is the working domain (web, mobile, data, etc.)?
- **Complexity**: Is this a simple task or complex workflow?

### Step 2: Skill Matching

Match the identified intent to the most relevant skill(s) using:
- **Keyword matching**: Compare request keywords with skill descriptions
- **Semantic similarity**: Understand the meaning behind the request
- **Context awareness**: Consider project state and previous actions

### Step 3: Interactive Clarification

If the request is ambiguous, guide the user with targeted questions:
- What is the primary goal?
- What type of output is expected?
- Are there specific constraints or preferences?

### Step 4: Recommendation & Execution

Present the recommended skill with:
- Skill name and brief description
- Why it fits the current request
- Option to proceed or ask for alternatives

## Routing Examples

### Example 1: Clear Intent

**User:** "I need to review this pull request"

**Router Analysis:**
- Keywords: "review", "pull request"
- Intent: Code review
- **Recommendation:** `code-reviewer`

### Example 2: Ambiguous Intent

**User:** "Use a skill to help with my project"

**Router Questions:**
1. What type of task are you working on?
2. Are you designing, coding, testing, or documenting?

Based on answers → Recommend appropriate skill

### Example 3: Multi-Skill Scenario

**User:** "I'm building a new API and need help with the full workflow"

**Router Recommendation:**
Consider using multiple skills in sequence:
1. `api-designer` - Design the API structure
2. `api-documenter` - Document endpoints with OpenAPI
3. `test-automator` - Set up API tests
4. `code-reviewer` - Review implementation

## Interactive Question Templates

When user intent is unclear, use these question patterns:

### Goal Clarification
- "What are you trying to accomplish with this task?"
- "What would the ideal outcome look like?"

### Domain Identification
- "What area does this relate to: development, testing, documentation, or deployment?"
- "Are you working on code, APIs, infrastructure, or something else?"

### Stage Assessment
- "What stage are you at: planning, implementing, testing, or maintaining?"

### Preference Confirmation
- "Do you want a quick solution or a comprehensive approach?"
- "Are there specific tools or frameworks you're using?"

## Best Practices

### 1. Start Broad, Then Narrow
- Begin with general category questions
- Drill down into specifics based on responses

### 2. Explain Your Reasoning
- Tell the user why a particular skill is recommended
- Build trust through transparency

### 3. Offer Alternatives
- Present the top recommendation
- Mention 1-2 alternatives if applicable

### 4. Handle Edge Cases
- If no skill fits perfectly, suggest the closest match
- Offer to help without a specific skill if better

### 5. Learn from Context
- Consider previous interactions
- Remember user preferences for future routing

## Advanced Routing Patterns

### Semantic Routing
Use semantic similarity when keywords don't match directly:
- "clean up my code" → `refactoring-specialist`
- "make my app faster" → `performance-engineer`
- "check for security issues" → `security-auditor`

### Multi-Skill Orchestrations
Suggest skill combinations for complex workflows:
- **New Feature**: `architecting-solutions` → `debugger` → `code-reviewer`
- **API Project**: `api-designer` → `api-documenter` → `test-automator`
- **Production Readiness**: `security-auditor` → `performance-engineer` → `deployment-engineer`

### Confidence Levels
Indicate confidence in recommendations:
- **High**: Direct keyword match, clear intent
- **Medium**: Semantic similarity, reasonable inference
- **Low**: Ambiguous request, clarification needed

## Error Recovery

If the recommended skill doesn't fit:
1. Acknowledge the mismatch
2. Ask follow-up questions to refine understanding
3. Provide alternative recommendations
4. Fall back to general assistance if needed

## Output Format

When recommending a skill, use this format:

```markdown
## Recommended Skill: {skill-name}

{brief description of why this skill fits}

**What it does:** {one-sentence skill description}

**Best for:** {specific use cases}

---

Would you like me to activate this skill, or would you prefer to see other options?
```

## References

- [AI Agent Routing: Tutorial & Best Practices](https://www.patronus.ai/ai-agent-development/ai-agent-routing)
- [Intent Recognition and Auto-Routing in Multi-Agent Systems](https://gist.github.com/mkbctrl/a35764e99fe0c8e8c00b2358f55cd7fa)
- [Multi-LLM Routing Strategies (AWS)](https://aws.amazon.com/blogs/machine-learning/multi-llm-routing-strategies-for-generative-ai-applications-on-aws/)
