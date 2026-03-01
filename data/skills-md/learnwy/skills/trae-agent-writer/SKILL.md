---
name: trae-agent-writer
description: "Create subagent definitions (agent.md files) for independent AI workers. Use when user wants to: create an agent, build a grader/evaluator, make an A/B comparator, spawn independent workers, or create something that runs in isolation. Triggers on: '创建 agent', 'subagent', 'grade outputs independently', 'blind comparison', 'run this in parallel'. Do NOT use for skills (use trae-skill-writer) or rules (use trae-rules-writer)."
license: "MIT"
compatibility: "Requires Trae IDE"
metadata:
  author: "learnwy"
  version: "1.1"
---

# Trae Agent Writer

Create agent definitions for tasks that need independent, isolated execution.

## What is an Agent?

A **focused, autonomous instruction set** for a subagent to execute independently:
- **Spawned as subagents** - Run with isolated context
- **Single-purpose** - One agent, one job
- **Stateless** - No memory between invocations
- **Composable** - Orchestrated by parent agents/skills

## Workflow

```
0. SIZE CHECK   → Is project too large? Ask user to specify context
1. ANALYZE      → What independent task needs an agent?
2. READ CODE    → Study existing patterns/agents if any
3. DEFINE       → Role, inputs, process, outputs
4. CREATE       → Write agent.md following the pattern
5. VERIFY       → Test agent invocation
```

## Naming Convention (CRITICAL)

**Every agent MUST use a descriptive, action-oriented name.**

| Good ✅ | Bad ❌ |
|---------|--------|
| `review-grader.md` | `agent.md` |
| `code-comparator.md` | `helper.md` |
| `project-scanner.md` | `scanner.md` (too vague) |

**For project-specific agents, consider prefix:**
- `app-analyzer.md` for your-app project
- `fe-validator.md` for frontend agents

## Language Consistency (CRITICAL)

**All content within an agent MUST be in ONE language.**

- Role, steps, guidelines - ALL same language
- Prefer English for code projects
- Do NOT mix Chinese and English in the same agent file

```markdown
# Good - all English
## Process
### Step 1: Read Input
Read the input file and extract claims.

# Bad - mixed languages
## Process 流程
### Step 1: Read Input 读取输入
Read the input file 读取文件.
```

## Code-First Approach

**Before writing an agent, study existing patterns.**

```
1. Check if similar agents exist in the project
2. Read 1-2 existing agents for patterns
3. Understand how agents are invoked in this codebase
4. Follow established conventions
```

## Agent Format

```markdown
# {Agent Name} Agent

{One-sentence role}

## Role

{What this agent does and why}

## Inputs

- **param_name**: Description
- **output_path**: Where to save results

## Process

### Step 1: {Action}
1. Do this
2. Then this

### Step N: Write Results
Save to `{output_path}`.

## Output Format

```json
{
  "field": "value"
}
```

## Guidelines

- **Be objective**: Avoid bias
- **Cite evidence**: Quote specific text
```

## Agent Locations

| Location | Use Case |
|----------|----------|
| `skill-name/agents/` | Inside orchestrating skills |
| `.trae/agents/` | Project-level agents |
| `~/.trae/agents/` | Global agents |

## Path Conventions

**NEVER use absolute paths.** Use relative paths or placeholders:

| Bad ❌ | Good ✅ |
|--------|---------|
| `/Users/john/project/` | `{project_root}/` |
| `/home/dev/output/` | `{output_path}` (as input) |

Placeholders: `{project_root}`, `{git_root}`, `{skill_dir}`, `{output_path}`

## Good Agent Candidates

| Pattern | Why Agent? | Example |
|---------|------------|---------|
| Grader | Needs objectivity | Output evaluator |
| Comparator | Blind comparison | A/B tester |
| Analyzer | Deep dive, isolated | Performance analyzer |
| Transformer | Parallel processing | File converter |
| Researcher | Independent investigation | Doc researcher |

**Don't make agents for:** Simple inline tasks, tasks needing conversation history, single-step operations.

## Quality Checklist

Before creating agents, verify:

- [ ] **Naming**: Descriptive, action-oriented, optionally prefixed
- [ ] **Language**: 100% consistent language
- [ ] **Role**: Clear single purpose
- [ ] **Inputs**: All parameters documented
- [ ] **Process**: Step-by-step instructions
- [ ] **Output**: Structured format defined
- [ ] **Paths**: Uses placeholders, no absolute paths

## Example

```
User: "I need an agent to grade code review outputs"

ANALYZE:
- Purpose: Evaluate code reviews objectively
- Needs isolation to prevent bias

CREATE: review-grader.md

# Review Grader Agent

Grade code reviews against quality expectations.

## Role

Assess reviews for completeness, accuracy, helpfulness.
Operates blindly to prevent bias.

## Inputs

- **review_path**: Path to review file
- **expectations**: List of expected findings
- **output_path**: Where to save grading.json

## Process

### Step 1: Read Review
1. Read review file
2. Extract all claims and findings

### Step 2: Check Expectations
For each expectation:
1. Search for evidence in review
2. Mark PASS/FAIL
3. Cite specific evidence

### Step 3: Write Results
Save to `{output_path}/grading.json`

## Output Format

```json
{
  "expectations": [
    {"text": "...", "passed": true, "evidence": "..."}
  ],
  "summary": {"passed": 4, "failed": 1, "pass_rate": 0.80}
}
```

## Guidelines

- **Be objective**: Don't favor verbose or brief reviews
- **Cite evidence**: Quote specific text from review
- **Be thorough**: Check all expectations
```

## References

- [Trae Agent Documentation](assets/trae-agent-docs.md) - Official docs
- [Agent Patterns](references/agent-patterns.md) - Common archetypes
- [Agent Template](assets/agent.md.template) - Starter template
- [Grader Agent Example](examples/grader-agent.md) - Complete example
