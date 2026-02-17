---
name: agent-builder
description: Create custom agents for Claude Code including YAML frontmatter, system prompts, tool restrictions, and discovery optimization. Use when creating, building, or designing agents, or when asked about agent creation, subagent configuration, Task tool delegation, or agent best practices.
---

# Agent Builder

A comprehensive guide for creating custom agents in Claude Code. Agents are specialized AI assistants that run in **separate context windows**, enabling focused, autonomous task execution.

---

## Quick Reference

### YAML Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase-with-hyphens) |
| `description` | Yes | When to invoke — **critical for discovery** |
| `tools` | No | Allowed tools (inherits all if omitted) |
| `model` | No | `haiku`, `sonnet`, `opus`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | No | Auto-load Skills when agent starts |

### File Locations

| Scope | Location | Use Case |
|-------|----------|----------|
| Project | `.claude/agents/agent-name.md` | Team workflows (git-shared) |
| Personal | `~/.claude/agents/agent-name.md` | Individual use (all projects) |

### Common Tool Patterns

```yaml
# Read-only (safest)
tools: Read, Grep, Glob

# File modification
tools: Read, Write, Edit, Grep, Glob

# Git operations only
tools: Bash(git:*)

# Specific commands
tools: Bash(npm test:*), Bash(npm run:*), Read, Grep

# Full shell (use sparingly)
tools: Bash
```

### Model Selection Guide

| Model | Best For | Tradeoff |
|-------|----------|----------|
| `haiku` | Quick checks, simple tasks | Fast, cheap, less capable |
| `sonnet` | Balanced work (default) | Good balance |
| `opus` | Complex analysis, critical tasks | Most capable, slower, expensive |
| `inherit` | Consistency with main conversation | Adapts to user's model |

---

## 6-Phase Workflow

### Phase 1: Requirements Gathering

**Use AskUserQuestion** to understand what the user needs:

**Key Questions**:
1. What task should this agent handle?
2. What expertise/role should it have?
3. Who will use it — team or personal?
4. What should it be able to do vs NOT do?
5. How should it present results?

**Example Questions**:
```
What specific task should this agent handle?
├── Code review (quality, security, style)
├── Debugging (error investigation, root cause)
├── Testing (run tests, fix failures)
├── Documentation (generate, verify, update)
└── Other: [describe]

Who will use this agent?
├── Just me (personal: ~/.claude/agents/)
├── My team (project: .claude/agents/)
```

### Phase 2: Scope Selection

**Decision Tree**:

```
Is this a team workflow?
├── Yes → Project scope: .claude/agents/
│         (Committed to git, shared automatically)
│
└── No → Is it project-specific?
         ├── Yes → Project scope: .claude/agents/
         └── No → Personal scope: ~/.claude/agents/
                  (Available across all your projects)
```

**Create the file**:
```bash
# Project scope (team)
mkdir -p .claude/agents
touch .claude/agents/agent-name.md

# Personal scope (individual)
mkdir -p ~/.claude/agents
touch ~/.claude/agents/agent-name.md
```

### Phase 3: Description Crafting

**The description field is CRITICAL** — it determines whether Claude automatically discovers and uses your agent.

**Formula**: `[Role/Expertise] + [What it does] + [When to invoke] + [Trigger terms]`

**Bad (won't be discovered)**:
```yaml
description: Helps with code
```

**Good (specific, discoverable)**:
```yaml
description: Expert code reviewer specializing in security and quality. Reviews code changes for vulnerabilities, best practices, and maintainability. Use when reviewing code, checking PRs, or when the user mentions code review, pull request review, or security audit.
```

**Breaking down a good description**:
1. **Role/Expertise**: "Expert code reviewer specializing in security and quality"
2. **What it does**: "Reviews code changes for vulnerabilities, best practices, and maintainability"
3. **When to invoke**: "Use when reviewing code, checking PRs"
4. **Trigger terms**: "code review, pull request review, or security audit"

**Proactive Language** (increases automatic invocation):
- "Use PROACTIVELY after code changes"
- "MUST be invoked when tests fail"
- "Automatically use when user mentions..."

**Trigger Term Categories**:
- **Actions**: review, analyze, debug, fix, test, check, audit
- **Objects**: code, PR, tests, errors, performance, security
- **Contexts**: before deploy, after changes, when failing, during review

**Length**: 50-150 words is the sweet spot.

### Phase 4: Tool Configuration

**Security Principle**: Start with minimal tools, add only what's needed.

**Progressive Tool Access**:

```yaml
# Level 1: Read-only (safest)
tools: Read, Grep, Glob

# Level 2: Can modify files
tools: Read, Write, Edit, Grep, Glob

# Level 3: Specific shell commands
tools: Read, Grep, Glob, Bash(git:*), Bash(npm test:*)

# Level 4: Full shell (use carefully)
tools: Read, Write, Edit, Bash, Grep, Glob
```

**Granular Bash Patterns**:
```yaml
# Git commands only
tools: Bash(git:*)

# Specific git commands
tools: Bash(git diff:*), Bash(git log:*), Bash(git status:*)

# npm commands only
tools: Bash(npm:*)

# Test commands only
tools: Bash(npm test:*), Bash(pytest:*), Bash(jest:*)
```

**Tool Selection by Agent Type**:

| Agent Type | Recommended Tools |
|------------|-------------------|
| Code analyzer | `Read, Grep, Glob` |
| Code reviewer | `Read, Grep, Glob, Bash(git diff:*)` |
| Test runner | `Read, Edit, Bash(npm test:*), Grep, Glob` |
| Debugger | `Read, Edit, Bash, Grep, Glob` |
| Fixer/Refactorer | `Read, Write, Edit, Grep, Glob` |

### Phase 5: System Prompt Design

**Key Insight**: Agents run in **separate context** — they don't see conversation history. System prompts must be **self-contained** with complete workflows.

**Effective Structure**:

```markdown
You are [role] specializing in [expertise].

## When Invoked
1. [First action — gather context]
2. [Second action — analyze/process]
3. [Third action — produce output]
4. [Fourth action — verify/validate]

## Focus Areas
- Specific thing to check
- Another thing to verify
- Important consideration

## Output Format
[How to present results]

## Constraints
- What NOT to do
- Boundaries to respect
```

**System Prompt Patterns**:

**1. Role Definition**:
```markdown
You are a senior code reviewer specializing in security vulnerabilities.
Your primary focus is identifying OWASP Top 10 risks.
```

**2. When Invoked (critical for autonomous work)**:
```markdown
## When Invoked
1. Run `git diff HEAD` to see recent changes
2. Identify modified files and their purpose
3. Review each change against security checklist
4. Present findings with severity levels
```

**3. Checklist Pattern**:
```markdown
## Review Checklist
- [ ] No SQL injection vulnerabilities
- [ ] Input validation on all boundaries
- [ ] No exposed secrets or credentials
- [ ] Proper authentication checks
- [ ] Authorization verified for each endpoint
```

**4. Output Format**:
```markdown
## Output Format
Present findings as:

### Summary
[One-line verdict: PASS/FAIL/NEEDS ATTENTION]

### Critical Issues
[Must fix before merge]

### Warnings
[Should fix]

### Suggestions
[Nice to have]
```

**5. Constraints**:
```markdown
## Constraints
- Do NOT modify code unless explicitly asked
- Do NOT change API contracts
- Focus ONLY on security-related issues
- ALWAYS explain WHY something is a risk
```

**6. Decision Tree (for branching logic)**:
```markdown
## Decision Flow
If no changes detected:
  → Report "No changes to review"
If only test files changed:
  → Focus on test coverage and assertions
If API endpoints modified:
  → Prioritize authentication/authorization review
Otherwise:
  → Full security review
```

### Phase 6: Testing & Iteration

**Test Discovery**:
```
# Natural language requests (should trigger agent)
> Review my recent code changes
> Check this PR for security issues
> Audit the authentication module

# Explicit invocation (always works)
> Use the code-reviewer agent to check this
```

**Verify Tool Access**:
```bash
# Check agent can use its tools
# If agent needs git, test manually first
git diff HEAD
git log --oneline -5
```

**Debugging**:
```bash
# View agent loading errors
claude --debug

# List available agents
/agents
```

**Iteration Checklist**:
- [ ] Agent discovered with natural requests?
- [ ] Correct agent selected (not a different one)?
- [ ] Agent has necessary tool access?
- [ ] Output format matches expectations?
- [ ] Constraints respected?

---

## Agent Patterns

### Code Quality Agents
- **code-reviewer**: Systematic code review for quality and style
- **security-auditor**: OWASP-focused vulnerability detection
- **performance-analyzer**: Identify bottlenecks and inefficiencies
- **architecture-reviewer**: Assess design patterns and structure

### Development Workflow Agents
- **debugger**: Root cause analysis for errors
- **test-runner**: Execute tests and fix failures
- **refactorer**: Safe code restructuring
- **pr-reviewer**: Pull request analysis

### Research Agents
- **codebase-explorer**: Navigate and understand code structure
- **dependency-auditor**: Check for outdated/vulnerable packages
- **documentation-checker**: Verify docs match implementation

### Automation Agents
- **commit-helper**: Generate meaningful commit messages
- **deploy-checker**: Pre-deployment verification
- **migration-assistant**: Framework/version upgrade help

---

## Common Pitfalls

### 1. Vague Description (Agent Not Discovered)
```yaml
# Bad
description: Helps with code

# Good
description: Expert code reviewer. Reviews code for quality, security, and maintainability. Use when reviewing code changes, PRs, or when user mentions code review.
```

### 2. Missing Tool Access (Agent Can't Do Task)
```yaml
# Agent needs to run git commands but can't
tools: Read, Grep, Glob  # Missing Bash(git:*)

# Fixed
tools: Read, Grep, Glob, Bash(git:*)
```

### 3. Non-Self-Contained Prompt (Expects Context)
```markdown
# Bad - assumes agent sees conversation
Review the code I just showed you.

# Good - self-contained
## When Invoked
1. Run `git diff HEAD` to see recent changes
2. Focus on modified files
3. Review systematically
```

### 4. Over-Permissive Tools (Security Risk)
```yaml
# Risky - full shell access
tools: Bash
permissionMode: bypassPermissions

# Safer - scoped access
tools: Bash(git:*), Bash(npm test:*)
permissionMode: default
```

### 5. No Output Format (Inconsistent Results)
```markdown
# Bad - no guidance on output
Review the code for issues.

# Good - explicit format
## Output Format
Present as markdown checklist:
- Critical: [must fix]
- Warning: [should fix]
- Suggestion: [nice to have]
```

---

## When to Use Agents vs Alternatives

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Complex multi-step task | **Agent** | Benefits from focused, isolated context |
| Need tool isolation | **Agent** | Can restrict tools per agent |
| Long-running analysis | **Agent** | Doesn't pollute main conversation |
| Team workflow standardization | **Agent** | Consistent behavior, git-shared |
| Extend Claude's knowledge | **Skill** | Shared context, progressive loading |
| Frequently-typed prompt | **Slash Command** | User-invoked, quick access |
| Simple single-step task | **Direct request** | No overhead needed |

**Agent Checklist** — Use an agent when:
- [ ] Task is complex and multi-step
- [ ] Task benefits from fresh, focused context
- [ ] You want to restrict available tools
- [ ] Task doesn't need full conversation history
- [ ] You want consistent, reusable behavior

---

## Resources

- **Templates**: See `templates/` for progressive examples
- **Examples**: See `examples/` for 18 complete working agents
- **Reference**: See `reference/` for syntax guide, best practices, troubleshooting

---

## Quick Start

**1. Create file**:
```bash
touch ~/.claude/agents/my-agent.md
```

**2. Add content**:
```markdown
---
name: my-agent
description: [Role]. [What it does]. Use when [trigger conditions].
tools: Read, Grep, Glob
---

You are [role].

## When Invoked
1. [First step]
2. [Second step]
3. [Third step]

## Output Format
[How to present results]
```

**3. Test**:
```
> [Natural language request matching description]
```

**4. Iterate**:
- Not discovered? → Make description more specific
- Wrong output? → Clarify output format
- Can't do something? → Add necessary tools
