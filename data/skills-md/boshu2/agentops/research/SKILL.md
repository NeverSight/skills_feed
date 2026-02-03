---
name: research
description: 'Deep codebase exploration. Triggers: research, explore, investigate, understand, deep dive, current state.'
---

# Research Skill

> **Quick Ref:** Deep codebase exploration with multi-angle analysis. Output: `.agents/research/*.md`

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Execution Steps

Given `/research <topic>`:

### Step 1: Create Output Directory
```bash
mkdir -p .agents/research
```

### Step 2: Check Prior Art

**First, search and inject existing knowledge (if ao available):**

```bash
# Search knowledge base for relevant learnings, patterns, and prior research
ao search "<topic>" 2>/dev/null || echo "ao not available, skipping knowledge search"

# Inject relevant context into this session
ao inject "<topic>" 2>/dev/null || echo "ao not available, skipping knowledge injection"
```

**Review ao search results:** If ao returns relevant learnings or patterns, incorporate them into your research strategy. Look for:
- Prior research on this topic or related topics
- Known patterns or anti-patterns
- Lessons learned from similar investigations

**Search local research artifacts:**
```bash
ls -la .agents/research/ 2>/dev/null | grep -i "<topic>" || echo "No prior research found"
```

Also use Grep to search `.agents/` for related content. Check TEMPERED learnings:
```bash
ls -la .agents/learnings/ .agents/patterns/ 2>/dev/null | head -10
```

### Step 3: Launch Explore Agent

**YOU MUST USE THE TASK TOOL NOW.** Call it with these exact parameters:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Research: <topic>"
  prompt: |
    Thoroughly investigate: <topic>

    Search strategy:
    1. Glob for relevant files (*.md, *.py, *.ts, *.go, etc.)
    2. Grep for keywords related to <topic>
    3. Read key files and understand the architecture
    4. Check docs/ and .agents/ for existing documentation

    Return a detailed report with:
    - Key files found (with paths)
    - How the system works
    - Important patterns or conventions
    - Any issues or concerns

    Cite specific file:line references for all claims.
```

### Step 4: Dispatch Research Quality Swarm (Optional)

**For thorough research, launch parallel quality validation agents:**

```
Launch ALL FOUR agents in parallel (single message, 4 Task tool calls):

Tool: Task
Parameters:
  subagent_type: "agentops:coverage-expert"
  model: "haiku"
  description: "Coverage validation"
  prompt: |
    Validate research breadth for: <topic>
    Research artifact: .agents/research/YYYY-MM-DD-<topic-slug>.md

    Check: Did we look everywhere we should? Any unexplored areas?
    Return: Coverage score and gaps found.

Tool: Task
Parameters:
  subagent_type: "agentops:depth-expert"
  model: "haiku"
  description: "Depth validation"
  prompt: |
    Validate research depth for: <topic>
    Research artifact: .agents/research/YYYY-MM-DD-<topic-slug>.md

    Check: Do we UNDERSTAND the critical parts? HOW and WHY, not just WHAT?
    Return: Depth scores (0-4) for critical areas.

Tool: Task
Parameters:
  subagent_type: "agentops:gap-identifier"
  model: "haiku"
  description: "Gap identification"
  prompt: |
    Find missing information for: <topic>
    Research artifact: .agents/research/YYYY-MM-DD-<topic-slug>.md

    Check: What DON'T we know that we SHOULD know?
    Return: Critical gaps that must be filled before proceeding.

Tool: Task
Parameters:
  subagent_type: "agentops:assumption-challenger"
  model: "haiku"
  description: "Assumption challenge"
  prompt: |
    Challenge assumptions in research for: <topic>
    Research artifact: .agents/research/YYYY-MM-DD-<topic-slug>.md

    Check: What assumptions are we building on? Are they verified?
    Return: High-risk assumptions that need verification.
```

**Wait for all 4 agents, then synthesize their findings.**

### Step 5: Synthesize Findings

After the Explore agent and validation swarm return, write findings to:
`.agents/research/YYYY-MM-DD-<topic-slug>.md`

Use this format:
```markdown
# Research: <Topic>

**Date:** YYYY-MM-DD
**Scope:** <what was investigated>

## Summary
<2-3 sentence overview>

## Key Files
| File | Purpose |
|------|---------|
| path/to/file.py | Description |

## Findings
<detailed findings with file:line citations>

## Recommendations
<next steps or actions>
```

### Step 6: Request Human Approval (Gate 1)

**USE AskUserQuestion tool:**

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Research complete. Approve to proceed to planning?"
      header: "Gate 1"
      options:
        - label: "Approve"
          description: "Research is sufficient, proceed to /plan"
        - label: "Revise"
          description: "Need deeper research on specific areas"
        - label: "Abandon"
          description: "Stop this line of investigation"
      multiSelect: false
```

**Wait for approval before reporting completion.**

### Step 7: Report to User

Tell the user:
1. What you found
2. Where the research doc is saved
3. Gate 1 approval status
4. Next step: `/plan` to create implementation plan

## Key Rules

- **Actually dispatch the Explore agent** - don't just describe doing it
- **Scope searches** - use the topic to narrow file patterns
- **Cite evidence** - every claim needs `file:line`
- **Write output** - research must produce a `.agents/research/` artifact

## Thoroughness Levels

Include in your Explore agent prompt:
- "quick" - for simple questions
- "medium" - for feature exploration
- "very thorough" - for architecture/cross-cutting concerns
