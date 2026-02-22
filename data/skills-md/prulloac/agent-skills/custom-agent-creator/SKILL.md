---
name: custom-agent-creator
description: Skill to create custom agents for VS Code Copilot or OpenCode, helping users configure and generate agent files with proper formatting and configurations. Use when users want to create specialized AI assistants for VS Code Copilot (.agent.md files) or OpenCode (JSON/markdown agent configs) with specific tools, prompts, models, and behaviors. If the user is not specific about the target platform, ask them to specify Copilot or OpenCode.
---

# Custom Agent Creator

## Overview

This skill guides the creation of custom agents for either VS Code Copilot or OpenCode. It helps users define agent properties like name, description, tools, models, and permissions, then generates the appropriate configuration file in the correct format.

## Workflow

### Step 1: Determine Target Platform
If the user hasn't specified, ask whether they want to create an agent for:
- **VS Code Copilot** (.agent.md files)
- **OpenCode** (JSON/markdown configs)

### Step 2: Gather Agent Specifications
Collect detailed information about the agent:
- **Agent Name**: Clear, descriptive identifier (e.g., "code-reviewer", "planner")
- **Description**: Brief explanation of what the agent does and when to use it
- **Role/Purpose**: Specific task the agent is designed for (e.g., "security auditing", "documentation writing")
- **Tools & Permissions**: Which capabilities are needed
- **Model Preference**: Specific AI model if needed (otherwise use default)
- **Additional Config**: Temperature, steps limit, handoffs, etc.

### Step 3: Validate Requirements
Ensure all required fields are provided:
- Copilot: name, description, tools list
- OpenCode: description, mode (primary/subagent), tool permissions

### Step 4: Generate Configuration File
Create the appropriate file based on platform:
- **Copilot**: Generate `.agent.md` with YAML frontmatter + markdown body
- **OpenCode**: Generate markdown config file with YAML frontmatter

### Step 5: Add Specialized Instructions
Write clear, actionable instructions in the file body:
- Define the agent's role and expertise
- Specify key behaviors and guidelines
- Include workflow steps if applicable
- Provide tool usage guidance

### Step 6: Configure Tools & Permissions
Set appropriate tool access levels:
- **Copilot**: Specify tool names in `tools` array
- **OpenCode**: Set individual tool permissions (true/false/"ask")

## Copilot Agents

Custom agents for VS Code Copilot are defined in `.agent.md` files with YAML frontmatter.

**File Structure**:
- Frontmatter: YAML with fields like `description`, `name`, `tools`, `model`, `handoffs`
- Body: Markdown instructions for the agent

**Common Fields**:
- `description`: Brief description shown in chat input
- `tools`: List of available tools
- `model`: AI model to use
- `handoffs`: Suggested next steps for workflow transitions

See [references/copilot-agents.md](references/copilot-agents.md) for complete documentation.

## OpenCode Agents

Agents for OpenCode can be defined in JSON config or Markdown files.

**Configuration Options**:
- `description`: Required description
- `mode`: "primary" or "subagent"
- `model`: Model identifier
- `tools`: Tool permissions (true/false)
- `permissions`: Granular control over actions
- `temperature`: Response creativity (0.0-1.0)

See [references/opencode-agents.md](references/opencode-agents.md) for complete documentation.

## Validation & Verification Steps

After generating the agent configuration, verify the following:

### 1. File Structure Validation
- ✅ File exists in correct location (`.github/agents/` for Copilot, `.opencode/agents/` for OpenCode)
- ✅ File has correct extension (`.agent.md` for Copilot, `.md` for OpenCode)
- ✅ File name matches agent identifier (e.g., `code-reviewer.agent.md`)

### 2. Frontmatter Validation
- ✅ YAML frontmatter is syntactically valid
- ✅ Required fields present: `description`, `name` (Copilot) or `mode` (OpenCode)
- ✅ No invalid field values (e.g., tools exist, models are supported, temperature is 0.0-1.0)

### 3. Instructions Validation
- ✅ Agent body contains clear, actionable instructions
- ✅ Instructions are specific to the agent's role
- ✅ Tool references are correct (use `#tool:toolName` format for Copilot)

### 4. Platform-Specific Validation

**For Copilot agents:**
- ✅ Tools list contains valid Copilot tools
- ✅ Model names are valid (check Copilot's supported models)
- ✅ Handoffs reference existing agents (if configured)
- ✅ File can be loaded in VS Code without errors

**For OpenCode agents:**
- ✅ Mode is either "primary" or "subagent"
- ✅ Tool permissions are boolean or "ask"/"allow"/"deny" (for permissions)
- ✅ Temperature value is between 0.0 and 1.0
- ✅ File can be loaded by OpenCode config parser

### 5. Functionality Verification
- ✅ Agent can be invoked/selected in the UI
- ✅ Tools specified are actually available and functional
- ✅ Instructions are followed when the agent is used
- ✅ No errors in agent logs when activated

## Concrete Examples

### Example 1: VS Code Copilot Security Reviewer Agent

**File: `.github/agents/security-reviewer.agent.md`**

```markdown
---
description: Reviews code for security vulnerabilities and best practices
name: Security Reviewer
tools: ['fetch', 'search', 'usages']
model: ['Claude Opus 4.5', 'GPT-5.2']
handoffs:
  - label: Fix Issues
    agent: agent
    prompt: Now implement fixes for the security issues identified above.
    send: false
---
# Security Code Reviewer

You are a security expert reviewing code for vulnerabilities. Focus on:

## Security Focus Areas
- Input validation vulnerabilities
- Authentication and authorization flaws
- SQL injection and command injection risks
- Data exposure and sensitive information handling
- Insecure deserialization
- Dependency vulnerabilities
- CORS and CSRF protection

## Analysis Guidelines
1. Examine the code structure and data flow
2. Identify potential attack vectors
3. Check for missing input validation
4. Verify secure defaults are used
5. Look for hardcoded secrets or credentials

## Output Format
- List each security finding with severity (Critical/High/Medium/Low)
- Provide specific recommendations for each issue
- Reference relevant security standards (OWASP, CWE)
- Suggest code examples when applicable

## Tools Available
Use #tool:fetch to examine relevant files and #tool:search to find similar patterns.
```

### Example 2: OpenCode Code Review Agent

**File: `.opencode/agents/code-reviewer.md`**

```markdown
---
description: Reviews code for quality, best practices, and potential issues
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash:
    "git diff": allow
    "grep *": allow
tools:
  write: false
  edit: false
  bash: true
---
You are a code reviewer focused on quality, maintainability, and best practices.

## Review Checklist
- Code readability and naming conventions
- Test coverage and edge cases
- Performance implications
- Security concerns
- Adherence to project standards
- Error handling and logging

## Analysis Process
1. Read the relevant code files
2. Check test coverage
3. Look for performance issues
4. Verify error handling
5. Compare against project patterns

## Feedback Style
- Be constructive and specific
- Suggest improvements with examples
- Ask questions if intent is unclear
- Acknowledge good practices

## Tools Usage
Use bash to run git diff and grep for pattern analysis.
Use read-only access only - make no changes.
```

### Example 3: OpenCode Documentation Writer Agent

**File: `.opencode/agents/docs-writer.md`**

```markdown
---
description: Writes and maintains project documentation
mode: subagent
temperature: 0.3
tools:
  bash: false
  edit: true
---
You are a technical documentation writer specializing in clear, comprehensive documentation.

## Documentation Standards
- Clear, concise language suitable for developers
- Proper markdown formatting with appropriate headings
- Code examples that are tested and functional
- Consistent terminology throughout
- Links to related documentation

## Writing Process
1. Understand the feature or concept deeply
2. Structure documentation logically
3. Add relevant code examples
4. Review for clarity and completeness
5. Check links and cross-references

## Output Guidelines
- Use proper heading hierarchy (H1, H2, H3)
- Include practical examples
- Document edge cases and limitations
- Provide both getting started and advanced sections
```

### Example 4: VS Code Copilot Planning Agent

**File: `.github/agents/planner.agent.md`**

```markdown
---
description: Generates detailed implementation plans for new features or refactoring
name: Planner
tools: ['fetch', 'search', 'githubRepo']
model: 'Claude Opus 4.5'
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Now implement the plan outlined above, following the implementation steps.
    send: false
---
# Implementation Planner

You are an expert at creating comprehensive implementation plans.

## Planning Methodology
1. **Analysis Phase**: Understand requirements and constraints
2. **Design Phase**: Propose architecture and approach
3. **Breakdown Phase**: Create detailed implementation steps
4. **Testing Phase**: Define verification strategy
5. **Review Phase**: Identify risks and dependencies

## Output Structure
- Executive Summary (1-2 paragraphs)
- Requirements Analysis
- Proposed Architecture
- Implementation Steps (ordered and detailed)
- Testing Strategy
- Risk Assessment
- Dependencies and Prerequisites

## Key Principles
- Plans should be actionable and specific
- Each step should have clear success criteria
- Include estimated complexity (low/medium/high)
- Reference existing code patterns
- Account for backward compatibility
```

## Resources

### references/
- `copilot-agents.md`: Full documentation for Copilot custom agents
- `opencode-agents.md`: Full documentation for OpenCode agents

### assets/
- `copilot-template.agent.md`: Template for Copilot agent files
- `opencode-template.md`: Template for OpenCode agent files
