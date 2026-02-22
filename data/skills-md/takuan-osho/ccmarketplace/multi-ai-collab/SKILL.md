---
name: multi-ai-collab
description: Orchestrate multiple AI agents with specialized personas for cross-review and collaborative development
---

# Multi-AI Collaboration Skill

## Overview

This skill enables the invoking AI agent to act as an **Orchestrator**, coordinating multiple AI agents (Codex CLI, Gemini CLI, Claude sub-agents) with assigned **Personas** (specialized expert roles) for collaborative software development tasks.

The primary use case is **Cross-Review**: having multiple AI agents independently analyze code from different expert perspectives, then synthesizing their findings to provide comprehensive, bias-reduced results.

## Prerequisites

Before using this skill, ensure the required CLI tools are installed:

```bash
# Check available agents
which codex && codex --version
which gemini && gemini --version
which claude && claude --version
```

### CLI Installation

- **Codex CLI**: See [OpenAI Codex Documentation](https://developers.openai.com/codex/cli/)
- **Gemini CLI**: `npm install -g @google/gemini-cli` or `brew install gemini-cli`
- **Claude Code**: See [Claude Code Documentation](https://code.claude.com/docs)

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Invoking AI)                       │
│                                                                     │
│  The AI agent that invokes this skill becomes the orchestrator.     │
│  It coordinates all sub-agents and synthesizes results.             │
└─────────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│   Codex CLI   │       │  Gemini CLI   │       │ Claude (sub)  │
│  latest       │       │  latest       │       │   latest      │
│               │       │               │       │               │
│   Persona:    │       │   Persona:    │       │   Persona:    │
│   Architect   │       │   Security    │       │  QA Engineer  │
└───────────────┘       └───────────────┘       └───────────────┘
```

### Phase 1: Task Analysis (Silent)

The orchestrator performs initial analysis using a **Parallel Fan-Out** pattern for efficiency:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Phase 1: Parallel Fan-Out                       │
│                                                                     │
│   ┌─────────────────────┐     ┌─────────────────────┐              │
│   │  Identify target    │     │  Detect available   │              │
│   │  files/code         │     │  AI agents          │   PARALLEL   │
│   └─────────┬───────────┘     └──────────┬──────────┘              │
│             │                            │                          │
│             └────────────┬───────────────┘                          │
│                          ▼                                          │
│             ┌─────────────────────┐                                 │
│             │  Analyze task       │                                 │
│             │  nature             │                     SEQUENTIAL  │
│             └──────────┬──────────┘                                 │
│                        ▼                                            │
│             ┌─────────────────────┐                                 │
│             │  Recommend          │                                 │
│             │  personas           │                                 │
│             └─────────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────┘
```

**Step 1 (Parallel):** Execute these tasks concurrently as they have no dependencies:
- **Identify target files/code** - Use Glob, Grep, Read tools to understand scope
- **Detect available AI agents** - Check which CLIs are installed (`which codex gemini claude`)

**Step 2 (Sequential):** After parallel tasks complete, execute in order:
- **Analyze task nature** - Determine if it's implementation, review, refactoring, investigation (requires file context from Step 1)
- **Recommend personas** - Suggest appropriate expert roles based on task nature and available agents

### Phase 2: Team Assembly (Interactive)

Use the **environment-appropriate user input tool** to configure the team:

#### Q1: Select Personas (Multiple Choice)

```
Which expert personas should participate in this task?

1. 🏗️ Architect - System design, modularity, dependencies
2. 🔒 Security Researcher - Vulnerabilities, OWASP, auth/authz
3. 🧪 QA Engineer - Test design, edge cases, coverage
4. 👁️ Code Reviewer - Code quality, readability, best practices
5. ⚡ Performance Engineer - Complexity, memory, caching
6. 🔍 Analyzer - Static analysis, bug patterns, type safety
7. 📝 Documentarian - API docs, comments, README
8. 🧠 Domain Expert - Business logic, requirements fit

Recommended based on task analysis: 1, 2, 4
```

#### Q2: Assign AI Agents to Personas

```
Assign an AI agent to each selected persona:

Architect:
  1. Codex CLI (latest default) - Recommended: deep reasoning
  2. Gemini CLI (latest default)
  3. Claude (sub-agent)

Security Researcher:
  1. Codex CLI (latest default)
  2. Gemini CLI (latest default) - Recommended: can search latest CVEs
  3. Claude (sub-agent)

Code Reviewer:
  1. Codex CLI (latest default)
  2. Gemini CLI (latest default)
  3. Claude (sub-agent) - Recommended: fast iteration
```

#### Q3: Select Workflow Mode

```
Select workflow mode:

1. Parallel - All agents work independently, synthesize at end (Recommended for cross-review)
2. Sequential - Each agent builds on previous results
3. Pipeline - Implementation → Test → Review flow
4. Adversarial - Agents critically challenge each other's findings
```

### Phase 3: Execution

The orchestrator executes the configured workflow.

#### Parallel Mode (Cross-Review)

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Agent A   │   │   Agent B   │   │   Agent C   │
│  (Codex)    │   │  (Gemini)   │   │  (Claude)   │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       ▼                 ▼                 ▼
   Result A          Result B          Result C
       │                 │                 │
       └────────────┬────┴────────────────┘
                    ▼
             ┌─────────────┐
             │  Synthesis  │
             └─────────────┘
```

**Execution Commands:**

```bash
# Codex CLI (Architect persona) - omit --model to use latest default
codex exec "You are a Senior Software Architect.
Analyze the following code for:
- Modularity and separation of concerns
- Dependency management
- Extensibility and maintainability
- Design pattern usage

[CODE_CONTENT]

Provide findings with severity (Critical/High/Medium/Low) and recommendations."

# Gemini CLI (Security persona) - omit -m to use latest default
gemini -p "You are a Security Researcher.
Analyze the following code for:
- OWASP Top 10 vulnerabilities
- Authentication/authorization issues
- Input validation and sanitization
- Data protection and encryption

[CODE_CONTENT]

Provide vulnerabilities with CVSS scores and remediation steps."

# Claude sub-agent (QA persona)
# Use the environment-appropriate subagent tool (Claude Code Task / Codex spawn_agent)
"You are a QA Engineer.
Based on the code, design:
- Required test cases (unit, integration, e2e)
- Edge cases and boundary conditions
- Security test scenarios
- Performance test considerations

[CODE_CONTENT]"
```

#### Sequential Mode

```
Agent A → Agent B → Agent C → Synthesis
   │          │          │
   └── Pass results to next agent
```

Each agent receives the previous agent's findings and builds upon them.

#### Pipeline Mode

```
Implementer → Tester → Reviewer
     │           │          │
   Code      Tests      Review
     │           │          │
     └───────────┴──────────┴──→ Quality-assured output
```

#### Adversarial Mode (Generator/Critic Pattern)

This mode implements the **Generator and Critic** pattern from Google ADK for iterative refinement:

```
┌─────────────────────────────────────────────────────────────────────┐
│              Generator/Critic Iteration Cycle                       │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │                    Iteration Loop                             │ │
│   │                                                               │ │
│   │   ┌─────────────┐                                             │ │
│   │   │  Generator  │──────────────┐                              │ │
│   │   │  (Agent A)  │   Proposal   │                              │ │
│   │   └─────────────┘              ▼                              │ │
│   │         ▲              ┌─────────────┐                        │ │
│   │         │              │   Critic    │                        │ │
│   │         │              │  (Agent B)  │                        │ │
│   │         │              └──────┬──────┘                        │ │
│   │         │                     │                               │ │
│   │         │   Feedback          ▼                               │ │
│   │         │              ┌─────────────┐                        │ │
│   │         └──────────────│  Evaluate   │                        │ │
│   │                        │  Quality    │                        │ │
│   │                        └──────┬──────┘                        │ │
│   │                               │                               │ │
│   │                 ┌─────────────┴─────────────┐                 │ │
│   │                 ▼                           ▼                 │ │
│   │         [Quality OK?]              [Max iterations?]          │ │
│   │              │ No                        │ Yes                │ │
│   │              └───── Continue ────────────┴── Exit ──────────▶ │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│                               ▼                                     │
│                    ┌─────────────────────┐                         │
│                    │   Final Decision    │                         │
│                    │  (User Input Tool)  │                         │
│                    └─────────────────────┘                         │
└─────────────────────────────────────────────────────────────────────┘
```

**Configuration Parameters:**
- `max_iterations`: Maximum number of generate-critique cycles (default: 3)
- `quality_threshold`: Criteria for acceptable output (e.g., no Critical issues)
- `escalate_on_deadlock`: Whether to involve user when agents cannot converge

**Iteration Cycle:**

1. **Generate Phase**: Generator agent produces a proposal/analysis
2. **Critique Phase**: Critic agent evaluates and challenges the proposal
3. **Evaluate Phase**: Check termination conditions:
   - Quality threshold met (no Critical/High severity issues remain)
   - Maximum iterations reached
   - Agents have converged on consensus
4. **Refine or Exit**: Either continue with refined proposal or exit to final decision

**Example Adversarial Flow:**
```
Iteration 1:
  Generator (Codex/Architect): "Propose microservices architecture"
  Critic (Gemini/Security): "Challenges: Service-to-service auth gaps, data consistency risks"
  Quality: Critical issues found → Continue

Iteration 2:
  Generator: "Refined proposal with OAuth2 service mesh, saga pattern for consistency"
  Critic: "Medium concerns: Observability gaps, no circuit breaker"
  Quality: No Critical issues → Continue (optional refinement)

Iteration 3:
  Generator: "Added distributed tracing, circuit breaker with fallbacks"
  Critic: "Low concerns: Consider rate limiting for external APIs"
  Quality: Acceptable → Exit

Final: Present converged proposal to user for approval
```

**Termination Conditions:**
| Condition | Action |
|-----------|--------|
| Quality threshold met | Exit with approved proposal |
| max_iterations reached | Exit with best proposal + unresolved concerns |
| Agents deadlocked | Escalate to user via User Input Tool |
| Critical regression | Revert to previous iteration's proposal |

### Phase 4: Synthesis

The orchestrator consolidates all results:

 1. **Collect results** from all agents
 2. **Identify consensus** - Points all agents agree on
 3. **Identify divergence** - Points where agents disagree
 4. **Prioritize actions** - Create actionable items with priority
 5. **Handle conflicts** - Use the environment-appropriate user input tool for unresolved disagreements

---

## Personas Reference

### 🏗️ Architect

**Focus Areas:**
- Modularity and separation of concerns
- Dependency direction and management
- Extensibility for future changes
- Design pattern appropriateness
- Public API/interface design

**Output Format:**
- Architecture assessment summary
- Issues (Critical/High/Medium/Low)
- Improvement recommendations
- Diagrams if needed

### 🔒 Security Researcher

**Focus Areas:**
- OWASP Top 10 compliance
- Authentication and authorization
- Input validation and sanitization
- Cryptography and data protection
- Error handling information leakage

**Output Format:**
- Vulnerability summary
- Findings with CVSS scores
- Attack scenarios
- Remediation steps

### 🧪 QA Engineer

**Focus Areas:**
- Test case design (unit/integration/e2e)
- Edge cases and boundary conditions
- Regression test needs
- Test coverage gaps
- Security testing requirements

**Output Format:**
- Test strategy overview
- Required test cases
- Edge cases identified
- Coverage recommendations

### 👁️ Code Reviewer

**Focus Areas:**
- Code readability and clarity
- Naming conventions
- Error handling patterns
- Code duplication
- Best practices adherence

**Output Format:**
- Review summary
- Issues by category
- Specific line-level feedback
- Improvement suggestions

### ⚡ Performance Engineer

**Focus Areas:**
- Time complexity analysis
- Memory usage patterns
- N+1 query problems
- Caching opportunities
- Resource management

**Output Format:**
- Performance assessment
- Bottleneck identification
- Optimization recommendations
- Benchmarking suggestions

### 🔍 Analyzer

**Focus Areas:**
- Bug patterns and anti-patterns
- Dead code detection
- Type safety issues
- Null/undefined handling
- Race conditions

**Output Format:**
- Static analysis results
- Bug risk assessment
- Code smell identification
- Refactoring suggestions

### 📝 Documentarian

**Focus Areas:**
- API documentation completeness
- Code comment quality
- README accuracy
- Type definitions
- Usage examples

**Output Format:**
- Documentation gaps
- Improvement areas
- Template suggestions
- Priority updates

### 🧠 Domain Expert

**Focus Areas:**
- Business logic correctness
- Requirements alignment
- Use case coverage
- Domain terminology
- Edge case handling

**Output Format:**
- Requirements fit analysis
- Business rule verification
- Missing functionality
- Domain-specific recommendations

---

## CLI Command Reference

### Codex CLI

```bash
# Basic invocation (latest default)
codex exec "prompt"

# With explicit model (if you must pin it)
codex exec --config model='"<latest-codex-model>"' "prompt"

# Reading from file (latest default)
codex exec "Review this code: $(cat src/file.ts)"
```

### Gemini CLI

```bash
# Basic invocation (latest default)
gemini -p "prompt"

# With JSON output (latest default)
gemini -p "prompt" --output-format json

# Non-interactive mode (required for scripting)
gemini -p "prompt"
```

### Claude Code (Sub-agent)

For Claude Code, use the Task tool with `subagent_type: general-purpose` (default/latest model):

```
Task tool parameters:
  subagent_type: general-purpose
  prompt: "[Persona prompt with task]"
  model: omit to use latest default, or specify if you must pin
```

For other AI agent CLIs invoking Claude:

```bash
# Non-interactive mode
claude -p "prompt" --output-format json

# With tool restrictions
claude -p "prompt" --allowedTools Read,Grep,Glob

# With turn limit
claude -p "prompt" --max-turns 5
```

---

## Output Template

```markdown
# 🎭 Multi-AI Collaboration Report

## Executive Summary
[1-2 sentence summary of findings]

## Team Configuration

| Persona | AI Agent | Model | Focus |
|---------|----------|-------|-------|
| 🏗️ Architect | Codex CLI | latest default | Design & Structure |
| 🔒 Security | Gemini CLI | latest default | Vulnerabilities |
| 🧪 QA | Claude (sub) | latest default | Test Design |

**Workflow:** Parallel (Cross-Review)
**Target:** [files/directories]

---

## Agent Results

### 🏗️ Architect (Codex CLI)

**Assessment:** [Overall status]

**Findings:**
1. [Finding] - Severity: [Level]
2. [Finding] - Severity: [Level]

**Recommendations:**
- [Recommendation]

---

### 🔒 Security Researcher (Gemini CLI)

**Assessment:** [Overall status]

**Vulnerabilities:**
| ID | Type | Severity | Location |
|----|------|----------|----------|
| SEC-001 | [Type] | [Severity] | [Location] |

**Remediation:**
- [Steps]

---

### 🧪 QA Engineer (Claude)

**Test Strategy:**
- [Strategy overview]

**Required Tests:**
- [ ] [Test case]

**Edge Cases:**
- [Edge case]

---

## Synthesis

### ✅ Consensus
- [Points all agents agree on]

### ⚠️ Divergence

| Topic | Architect | Security | QA | Resolution |
|-------|-----------|----------|-----|------------|
| [Topic] | [View] | [View] | [View] | [Status] |

### ❓ User Decisions Required

1. **[Decision item]**
   - Agent A recommends: [X]
   - Agent B recommends: [Y]

---

## Priority Actions

### 🔴 Critical (P0)
- [ ] [Action]

### 🟠 High (P1)
- [ ] [Action]

### 🟡 Medium (P2)
- [ ] [Action]

### 🟢 Low (P3)
- [ ] [Action]

---

## Next Steps
1. [Step]
2. [Step]
```

---

## Usage Examples

### Example 1: Cross-Review a Pull Request

```
User: Review the authentication module changes in this PR

Orchestrator:
1. Identifies target files (src/auth/*)
2. Detects available agents (codex, gemini, claude)
3. Recommends personas: Architect, Security, Code Reviewer

User Input Tool: "Select personas for this review"
User: 1, 2, 4 (Architect, Security, Code Reviewer)

User Input Tool: "Assign agents to personas"
User: Codex→Architect, Gemini→Security, Claude→Reviewer

User Input Tool: "Select workflow mode"
User: 1 (Parallel)

Execution:
- Codex analyzes architecture
- Gemini checks security
- Claude reviews code quality
- Orchestrator synthesizes results
```

### Example 2: Implementation with QA Split

```
User: Implement user profile feature with tests

Orchestrator:
1. Analyzes requirements
2. Recommends Pipeline mode: Implementer → QA → Reviewer

Execution:
- Orchestrator (Claude) implements feature
- Codex creates comprehensive tests
- Gemini reviews implementation and tests
```

### Example 3: Security Audit

```
User: Perform security audit on payment module

Orchestrator:
1. Identifies payment-related files
2. Recommends personas: Security, Analyzer, Performance

Execution:
- Gemini (Security): OWASP analysis, CVE search
- Codex (Analyzer): Static analysis, bug patterns
- Claude (Performance): DoS vulnerability, resource limits
```

---

## Best Practices

1. **Start with Parallel mode** for unbiased cross-review
2. **Use Codex for deep reasoning** tasks (architecture, complex bugs)
3. **Use Gemini for research** tasks (latest vulnerabilities, best practices)
4. **Use Claude sub-agents for speed** (quick iterations, implementation)
5. **Always synthesize divergent opinions** - don't just merge results
6. **Escalate to user** when agents fundamentally disagree
7. **Limit personas to 3-4** per task to avoid information overload

---

## Troubleshooting

### Agent CLI not found

```bash
# Check installation
which codex gemini claude

# Install missing CLIs
# Codex: Follow OpenAI instructions
# Gemini: npm install -g @google/gemini-cli
# Claude: Download from anthropic.com
```

### Agent timeout

- Reduce scope of analysis
- Split into smaller tasks
- Use simpler prompts

### Conflicting results

- Use Adversarial mode for deeper analysis
- Escalate to user via the environment-appropriate user input tool
- Document disagreement in report

---

## Environment-Specific Notes

### Codex CLI Environment

- Use `request_user_input` for persona selection and workflow mode
- Use `spawn_agent` for subagents (latest default model)
- Use `exec_command` to invoke external CLIs (gemini, claude)

### Claude Code Environment

- Use **AskUserTool** for user interactions
- Use **Task tool** with `subagent_type: general-purpose` for Claude sub-agents (latest default model)
- Use **Bash tool** to invoke external CLIs (codex, gemini)

### Gemini CLI Environment

- Use numbered prompt options for user selection (no tool calls)
- Use `gemini -p` directly for execution (latest default model)
- For subagents, invoke other CLIs directly (codex/claude) with latest defaults

### Other AI Agent Environments

- Use the platform's equivalent of: user input, subagent, and shell execution tools
- Default to each CLI's latest model unless explicitly pinned
