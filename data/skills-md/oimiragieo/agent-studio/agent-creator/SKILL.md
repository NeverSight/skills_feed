---
name: agent-creator
description: Creates specialized AI agents on-demand when no existing agent matches a request. Use when the Router cannot find a suitable agent for a task. Enables self-evolution by generating persistent agents.
version: 2.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash, Task]
best_practices:
  - Verify no existing agent matches first
  - Research domain before creating agent
  - Assign relevant skills to new agents
error_handling: graceful
streaming: supported
output_location: .claude/agents/
---

# Agent Creator Skill

Creates specialized AI agents on-demand for capabilities that don't have existing agents.

## ROUTER UPDATE REQUIRED (CRITICAL - DO NOT SKIP)

**After creating ANY agent, you MUST update CLAUDE.md Section 3 "AGENT ROUTING TABLE":**

```markdown
| Request Type | agent-name | `.claude/agents/<category>/<name>.md` |
```

**Verification:**

```bash
grep "<agent-name>" .claude/CLAUDE.md || echo "ERROR: CLAUDE.md ROUTING TABLE NOT UPDATED!"
```

**WHY**: Agents not in the routing table will NEVER be spawned by the Router.

---

## When This Skill Is Triggered

1. **Router finds no matching agent** for a user request
2. **User explicitly requests** creating a new agent
3. **Specialized expertise needed** that existing agents don't cover

## Quick Reference

| Operation             | Method                                         |
| --------------------- | ---------------------------------------------- |
| Check existing agents | `Glob: .claude/agents/**/*.md`                 |
| Research domain       | `WebSearch: "<topic> best practices 2026"`     |
| Find relevant skills  | `Glob: .claude/skills/*/SKILL.md`              |
| Create agent          | Write to `.claude/agents/<category>/<name>.md` |
| Spawn agent           | `Task` tool with new `subagent_type`           |
| Run in terminal       | `claude -p "prompt" --allowedTools "..."`      |

## Agent Creation Process

### Step 1: Verify No Existing Agent

```bash
# Search for relevant agents
Glob: .claude/agents/**/*.md
Grep: "<topic>" in .claude/agents/
```

If a suitable agent exists, use it instead. Check:

- Core agents: `.claude/agents/core/`
- Specialized agents: `.claude/agents/specialized/`
- Orchestrators: `.claude/agents/orchestrators/`

### Step 2: Research the Domain

**Use web search to gather current information:**

```
WebSearch: "<topic> expert techniques best practices 2026"
WebSearch: "<topic> tools frameworks methodologies"
```

**Research goals:**

- Current best practices and industry standards
- Popular tools, frameworks, and methodologies
- Expert techniques and evaluation criteria
- Common workflows and deliverables

### Step 2.5: Research Keywords (MANDATORY - DO NOT SKIP)

Before designing the agent, you MUST research keywords that users will use to invoke this agent.

#### Required Actions

1. **Execute Exa Searches** (minimum 3 queries):

   ```javascript
   // Query 1: Role-specific tasks
   mcp__Exa__web_search_exa({ query: '[agent-role] common tasks responsibilities' });

   // Query 2: Industry terminology
   mcp__Exa__web_search_exa({ query: '[agent-role] terminology keywords phrases' });

   // Query 3: Problem types
   mcp__Exa__web_search_exa({ query: '[agent-role] problem types use cases' });
   ```

2. **Document Keywords** (save to research report):
   - High-Confidence Keywords: Unique to this agent
   - Medium-Confidence Keywords: May overlap with other agents
   - Action Verbs: Common verbs for this role
   - Problem Indicators: Phrases users say when needing this agent

3. **Save Research Report**:
   Save to: `.claude/context/artifacts/research-reports/agent-keywords-[agent-name].md`

#### Validation Gate

- [ ] Minimum 3 Exa searches executed
- [ ] Keywords documented with confidence levels
- [ ] Research report saved

**BLOCKING**: Agent creation CANNOT proceed without completing keyword research.

### Step 3: Find Relevant Skills to Assign (CRITICAL)

**Every agent MUST have relevant skills assigned and include skill loading in their workflow.**

**Search existing skills the agent should use:**

```bash
Glob: .claude/skills/*/SKILL.md
Grep: "<related-term>" in .claude/skills/
```

**Skill categories available:**
| Domain | Skills |
|--------|--------|
| Documentation | doc-generator, diagram-generator |
| Testing | test-generator, tdd |
| DevOps | docker-compose, kubernetes-flux, terraform-infra |
| Cloud | aws-cloud-ops, gcloud-cli |
| Code Quality | code-analyzer, code-style-validator |
| Project Management | linear-pm, jira-pm, github-ops |
| Debugging | debugging, smart-debug |
| Communication | slack-notifications |
| Data | text-to-sql, repo-rag |
| Task Management | task-management-protocol |

**Skill Discovery Process:**

1. **Scan all skills**: `Glob: .claude/skills/*/SKILL.md`
2. **Read each SKILL.md** to understand what it does
3. **Match skills to agent domain**:
   - If agent does code → consider: tdd, debugging, git-expert, code-analyzer
   - If agent does planning → consider: plan-generator, sequential-thinking, diagram-generator
   - If agent does security → consider: security-related skills
   - If agent does documentation → consider: doc-generator, diagram-generator
   - **ALL agents** should include: task-management-protocol (for task tracking)
4. **Include ALL relevant skills** in the agent's frontmatter

### Step 4: Determine Agent Configuration

| Agent Type | Use When                       | Model  | Temperature |
| ---------- | ------------------------------ | ------ | ----------- |
| Worker     | Executes tasks directly        | sonnet | 0.3         |
| Analyst    | Research, review, evaluation   | sonnet | 0.4         |
| Specialist | Deep domain expertise          | opus   | 0.4         |
| Advisor    | Strategic guidance, consulting | opus   | 0.5         |

| Category      | Directory                       | Examples                      |
| ------------- | ------------------------------- | ----------------------------- |
| Core          | `.claude/agents/core/`          | developer, planner, architect |
| Specialized   | `.claude/agents/specialized/`   | security-architect, devops    |
| Domain Expert | `.claude/agents/domain/`        | ux-reviewer, data-scientist   |
| Orchestrator  | `.claude/agents/orchestrators/` | master-orchestrator           |

### Step 5: Generate Agent Definition (WITH SKILL LOADING)

**CRITICAL**: The generated agent MUST include:

1. Skills listed in frontmatter `skills:` array
2. "Step 0: Load Skills" in the Workflow section with ACTUAL skill paths

Write to `.claude/agents/<category>/<agent-name>.md`:

````yaml
---
name: <agent-name>
description: <One sentence: what it does AND when to use it. Be specific about trigger conditions.>
tools: [Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, TaskUpdate, TaskList, TaskCreate, TaskGet, Skill]
model: sonnet
temperature: 0.4
context_strategy: lazy_load  # REQUIRED: minimal, lazy_load, or full
priority: medium
skills:
  - <skill-1>
  - <skill-2>
  - task-management-protocol
context_files:
  - .claude/context/memory/learnings.md
---

# <Agent Title>

## Core Persona
**Identity**: <Role title>
**Style**: <Working style adjectives>
**Approach**: <Methodology>
**Values**: <Core principles>

## Responsibilities
1. **<Area 1>**: Description
2. **<Area 2>**: Description
3. **<Area 3>**: Description

## Capabilities
Based on current best practices:
- <Capability from web research>
- <Capability from web research>
- <Capability from web research>

## Tools & Frameworks
- <Tool/Framework from research>
- <Tool/Framework from research>
- <Pattern/Practice from research>

## Workflow

### Step 0: Load Skills (FIRST)

Invoke your assigned skills using the Skill tool:

```javascript
Skill({ skill: 'doc-generator' });
Skill({ skill: 'diagram-generator' });
````

> **CRITICAL**: Do NOT just read SKILL.md files. Use the `Skill()` tool to invoke skill workflows.
> Reading a skill file does not apply it. Invoking with `Skill()` loads AND applies the workflow.
>
> **NOTE FOR AGENT-CREATOR**: Replace these skill names with the ACTUAL skills
> you assigned in the frontmatter. Every skill in `skills:` must have
> its invocation listed here.

### Step 1-5: Execute Task

1. **Analyze**: Understand the request and context
2. **Research**: Gather relevant information
3. **Execute**: Perform the task using available tools AND skill workflows
4. **Deliver**: Produce deliverables in appropriate format
5. **Document**: Record findings to memory

> **Skill Protocol**: Your skills define specialized workflows.
> Apply them throughout your task execution.

## Response Approach

When executing tasks, follow this 8-step approach:

1. **Acknowledge**: Confirm understanding of the task
2. **Discover**: Read memory files, check task list
3. **Analyze**: Understand requirements and constraints
4. **Plan**: Determine approach and tools needed
5. **Execute**: Perform the work using tools and skills
6. **Verify**: Check output quality and completeness
7. **Document**: Update memory with learnings
8. **Report**: Summarize what was done and results

## Behavioral Traits

- <Trait 1: Domain-specific behavior>
- <Trait 2: Quality focus>
- <Trait 3: Communication style>
- <Trait 4: Error handling approach>
- <Trait 5: Testing philosophy>
- <Trait 6: Documentation practices>
- <Trait 7: Collaboration style>
- <Trait 8: Performance consideration>
- <Trait 9: Security awareness>
- <Trait 10: Continuous improvement>

> **NOTE FOR AGENT-CREATOR**: Replace these with ACTUAL behavioral traits
> specific to the agent's domain. Reference python-pro.md for examples.
> Minimum 10 traits required.

## Example Interactions

| User Request          | Agent Action         |
| --------------------- | -------------------- |
| "<example request 1>" | <how agent responds> |
| "<example request 2>" | <how agent responds> |
| "<example request 3>" | <how agent responds> |
| "<example request 4>" | <how agent responds> |
| "<example request 5>" | <how agent responds> |
| "<example request 6>" | <how agent responds> |
| "<example request 7>" | <how agent responds> |
| "<example request 8>" | <how agent responds> |

> **NOTE FOR AGENT-CREATOR**: Replace these with ACTUAL example interactions
> specific to the agent's domain. Reference python-pro.md for examples.
> Minimum 8 examples required.

## Output Locations

- Deliverables: `.claude/context/artifacts/`
- Reports: `.claude/context/reports/`
- Temporary files: `.claude/context/tmp/`

## Task Progress Protocol (MANDATORY)

**When assigned a task, use TaskUpdate to track progress:**

```javascript
// 1. Check available tasks
TaskList();

// 2. Claim your task (mark as in_progress)
TaskUpdate({
  taskId: '<your-task-id>',
  status: 'in_progress',
});

// 3. Do the work...

// 4. Mark complete when done
TaskUpdate({
  taskId: '<your-task-id>',
  status: 'completed',
  metadata: {
    summary: 'Brief description of what was done',
    filesModified: ['list', 'of', 'files'],
  },
});

// 5. Check for next available task
TaskList();
```

**The Three Iron Laws of Task Tracking:**

1. **LAW 1**: ALWAYS call TaskUpdate({ status: "in_progress" }) when starting
2. **LAW 2**: ALWAYS call TaskUpdate({ status: "completed", metadata: {...} }) when done
3. **LAW 3**: ALWAYS call TaskList() after completion to find next work

**Why This Matters:**

- Progress is visible to Router and other agents
- Work survives context resets
- No duplicate work (tasks have owners)
- Dependencies are respected (blocked tasks can't start)

## Memory Protocol (MANDATORY)

**Before starting any task:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing work, record findings:**

- New pattern/solution -> Append to `.claude/context/memory/learnings.md`
- Roadblock/issue -> Append to `.claude/context/memory/issues.md`
- Decision made -> Append to `.claude/context/memory/decisions.md`

**During long tasks:** Use `.claude/context/memory/active_context.md` as scratchpad.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

```

### Reference Agent (MANDATORY COMPARISON)

**Use `.claude/agents/domain/python-pro.md` as the canonical reference agent.**

Before finalizing any agent, compare against python-pro.md structure:

```

[ ] Has all sections python-pro has (Core Persona, Capabilities, Workflow, Response Approach, Behavioral Traits, Example Interactions, Skill Invocation Protocol, Memory Protocol)
[ ] Section order matches python-pro
[ ] Level of detail is comparable
[ ] Behavioral Traits has 10+ items (domain-specific)
[ ] Example Interactions has 8+ items (domain-specific)
[ ] Response Approach has 8 numbered steps
[ ] Skill Invocation Protocol includes Automatic and Contextual skills tables

```

**Why python-pro is the reference:**
- Most complete implementation of all required sections
- Demonstrates proper skill invocation protocol
- Shows appropriate level of detail for capabilities
- Has proper Response Approach structure

**BLOCKING**: Do not proceed if agent is missing sections that python-pro has.

### Step 6: Validate Required Fields (BLOCKING)

**Before writing agent file, verify ALL required fields are present.**

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `name` | YES | - | lowercase-with-hyphens |
| `description` | YES | - | Single line, include trigger conditions |
| `model` | YES | sonnet | sonnet, opus, or haiku |
| `context_strategy` | YES | lazy_load | minimal, lazy_load, or full |
| `tools` | YES | [] | At least [Read] required |
| `skills` | YES | [] | List relevant skills |
| `context_files` | YES | [learnings.md] | Memory files to load |
| `temperature` | NO | 0.4 | 0.0-1.0 |
| `priority` | NO | medium | low, medium, high |

**BLOCKING**: Do not write agent file if any required field is missing.

**Validation checklist before writing:**
```

[ ] name: defined and kebab-case
[ ] description: single line, describes trigger conditions
[ ] model: one of sonnet/opus/haiku
[ ] context_strategy: one of minimal/lazy_load/full
[ ] tools: array with at least Read
[ ] skills: array (can be empty but must exist)
[ ] context_files: array with at least learnings.md
[ ] Response Approach section present with 8 steps
[ ] Behavioral Traits section present with 10+ traits
[ ] Example Interactions section present with 8+ examples

````

**Model Validation (CRITICAL):**
- model field MUST be base name only: `haiku`, `sonnet`, or `opus`
- DO NOT use dated versions like `claude-opus-4-5-20251101`
- DO NOT use full version strings like `claude-3-sonnet-20240229`
- The orchestration layer handles model resolution automatically

**Extended Thinking (NOT STANDARD):**
- `extended_thinking: true` is NOT documented in CLAUDE.md
- DO NOT add this field unless explicitly documented and requested
- If used, must have documented justification in the agent definition
- This field may cause unexpected behavior in agent spawning

**Tools Array Validation:**
- Standard tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, TaskUpdate, TaskList, TaskCreate, TaskGet, Skill
- DO NOT add MCP tools (mcp__*) unless whitelisted in router-enforcer.cjs
- MCP tools (mcp__Exa__*, mcp__GitHub__*, etc.) cause router enforcement failures
- If MCP integration is needed, document it explicitly and verify hook compatibility

After writing, validate file was saved:

1. **YAML frontmatter is valid** - No syntax errors
2. **Required fields present** - All fields from checklist above
3. **Skills exist** - All referenced skills are in `.claude/skills/`
4. **File saved correctly** - Glob to verify file exists

### Step 7: Update CLAUDE.md Routing Table (MANDATORY - BLOCKING)

**This step is AUTOMATIC and BLOCKING. Do not skip.**

After agent file is written, you MUST update the CLAUDE.md routing table:

1. **Parse CLAUDE.md Section 3** ("AGENT ROUTING TABLE")
2. **Generate routing entry**:
   ```markdown
   | {request_type} | `{agent_name}` | `.claude/agents/{category}/{agent_name}.md` |
````

3. **Find correct insertion point** (alphabetical within category, or at end of relevant section)
4. **Insert using Edit tool**
5. **Verify with**:
   ```bash
   grep "{agent-name}" .claude/CLAUDE.md || echo "ERROR: CLAUDE.md ROUTING TABLE NOT UPDATED!"
   ```

**BLOCKING**: If routing table update fails, agent creation is INCOMPLETE. Do NOT proceed to spawning the agent.

**Why this is mandatory**: Agents not in the routing table will NEVER be spawned by the Router. An agent without a routing entry is effectively invisible to the system.

### Step 7.5: Update Router-Enforcer (MANDATORY - BLOCKING)

**This step is MANDATORY and BLOCKING. Without it, the Router cannot discover the agent.**

After updating CLAUDE.md, you MUST register the agent in router-enforcer.cjs:

#### Required Updates

1. **Add to `intentKeywords` object** with keywords from Step 2.5:

   ```javascript
   // In router-enforcer.cjs intentKeywords section
   '<agent-name>': [
     // High-confidence keywords (unique to this agent)
     'keyword1', 'keyword2',
     // Action verbs
     'review', 'analyze',
     // Problem indicators
     'need help with X'
   ],
   ```

2. **Add to `ROUTING_TABLE` object**:

   ```javascript
   // In router-enforcer.cjs ROUTING_TABLE section
   '<agent-name>': {
     path: '.claude/agents/<category>/<agent-name>.md',
     primaryKeywords: ['keyword1', 'keyword2'],  // High-confidence from Step 2.5
     secondaryKeywords: ['keyword3', 'keyword4']  // Medium-confidence from Step 2.5
   },
   ```

3. **Add to `SCORING_BOOSTS` if needed** (for high-priority agents):
   ```javascript
   // In router-enforcer.cjs SCORING_BOOSTS section
   '<agent-name>': { boost: 5, condition: 'specific_intent_type' },
   ```

#### Verification

```bash
grep "<agent-name>" .claude/hooks/routing/router-enforcer.cjs || echo "ERROR: Agent not in router-enforcer.cjs - AGENT CREATION INCOMPLETE"
```

**BLOCKING**: If router-enforcer update fails, agent creation is INCOMPLETE. The agent will never be discovered by the Router.

**Why this is mandatory**: The router-enforcer.cjs uses keyword matching to select agents. Without keyword registration, the Router's scoring algorithm cannot consider this agent for any request.

### Step 8: Create Workflow & Update Memory

The CLI tool automatically:

1. **Creates a workflow example** in `.claude/workflows/<agent-name>-workflow.md`
2. **Updates memory** in `.claude/context/memory/learnings.md` with routing hints

```bash
# Create agent with full self-evolution
node .claude/tools/agent-creator/create-agent.mjs \
  --name "ux-reviewer" \
  --description "Reviews mobile app UX and accessibility" \
  --original-request "Review the UX of my iOS app"
```

This outputs a spawn command for the Task tool to immediately execute the original request.

### Step 9: Execute the Agent

**Option A: Use output spawn command (recommended for self-evolution)**
The CLI outputs a Task spawn command when `--original-request` is provided:

```javascript
Task({
  subagent_type: 'general-purpose',
  description: 'ux-reviewer executing original task',
  prompt: 'You are the UX-REVIEWER agent...',
});
```

**Option B: Spawn via Task tool manually**

```javascript
Task({
  subagent_type: 'general-purpose',
  description: 'Execute task with new agent',
  prompt: 'You are <AGENT>. Read .claude/agents/domain/<name>.md and complete: <task>',
});
```

**Option C: Run in separate terminal (new session)**

```bash
node .claude/tools/agent-creator/spawn-agent.mjs --agent "<name>" --prompt "<task>"
```

## Agent Naming Conventions

- **Format**: `lowercase-with-hyphens`
- **Pattern**: `<domain>-<role>` (e.g., `ux-reviewer`, `data-analyst`)
- **Avoid**: Generic names like `helper`, `assistant`, `agent`

## Examples

### Example 1: UX Reviewer for Mobile Apps (Complete Flow)

**User**: "I need a UX review of an Apple mobile app"

1. **Check**: No `ux-reviewer*.md` or `mobile*.md` agent exists
2. **Research**:
   - `WebSearch: "mobile UX review best practices 2026 iOS"`
   - `WebSearch: "Apple Human Interface Guidelines evaluation criteria"`
3. **Find skills**: Scan `.claude/skills/*/SKILL.md`:
   - `diagram-generator` for wireframes
   - `doc-generator` for reports
   - `task-management-protocol` for task tracking
4. **Create** `.claude/agents/domain/mobile-ux-reviewer.md`:

````yaml
---
name: mobile-ux-reviewer
description: Reviews mobile app UX against Apple HIG and accessibility standards. Use for UX audits and accessibility compliance checks.
tools: [Read, WebSearch, WebFetch, TaskUpdate, TaskList, TaskCreate, TaskGet, Skill]
model: sonnet
temperature: 0.4
context_strategy: lazy_load
skills:
  - diagram-generator
  - doc-generator
  - task-management-protocol
context_files:
  - .claude/context/memory/learnings.md
---

# Mobile UX Reviewer

## Core Persona
**Identity**: UX/Accessibility Specialist
...

## Workflow

### Step 0: Load Skills (FIRST)

Invoke your assigned skills using the Skill tool:

```javascript
Skill({ skill: 'diagram-generator' });
Skill({ skill: 'doc-generator' });
````

> **CRITICAL**: Use `Skill()` tool, not `Read()`. Skill() loads AND applies the workflow.

### Step 1-5: Execute Task

...

````

5. **Execute**: Spawn via Task tool

### Example 2: Data Scientist Agent

**User**: "Analyze this dataset and build a prediction model"

1. **Check**: No `data-scientist*.md` agent exists
2. **Research**:
   - `WebSearch: "data science workflow best practices 2026"`
   - `WebSearch: "machine learning model evaluation techniques"`
3. **Find skills**: `text-to-sql`, `diagram-generator`, `doc-generator`, `task-management-protocol`
4. **Create**: `.claude/agents/domain/data-scientist.md`
5. **Execute**: Task tool with new agent

### Example 3: API Integration Specialist

**User**: "Help me integrate with the Stripe API"

1. **Check**: No `stripe*.md` or `api-integration*.md` agent exists
2. **Research**:
   - `WebSearch: "Stripe API integration best practices 2026"`
   - `WebFetch: "https://stripe.com/docs"` (extract key patterns)
3. **Find skills**: `github-ops`, `test-generator`, `doc-generator`, `task-management-protocol`
4. **Create**: `.claude/agents/domain/api-integrator.md`
5. **Execute**: Spawn agent to complete integration

## Integration with Router

The Router should output this when no agent matches:

```json
{
  "intent": "specialized_task",
  "complexity": "medium",
  "target_agent": "agent-creator",
  "reasoning": "No existing agent matches UX review for mobile apps. Creating specialized agent.",
  "original_request": "<user's original request>"
}
````

## Persistence

- Agents saved to `.claude/agents/` persist across sessions
- Next session automatically discovers new agents via `/agents` command
- Skills assigned in frontmatter are available to the agent

## File Placement & Standards

### Output Location Rules

This skill outputs to: `.claude/agents/<category>/`

Categories:

- `core/` - fundamental agents (developer, planner, architect, etc.)
- `domain/` - language/framework specialists (python-pro, etc.)
- `specialized/` - task-specific agents (security-architect, etc.)
- `orchestrators/` - multi-agent coordinators

### Mandatory References

- **File Placement**: See `.claude/docs/FILE_PLACEMENT_RULES.md`
- **Developer Workflow**: See `.claude/docs/DEVELOPER_WORKFLOW.md`
- **Artifact Naming**: See `.claude/docs/ARTIFACT_NAMING.md`

### Enforcement

File placement is enforced by `file-placement-guard.cjs` hook.
Invalid placements will be blocked in production mode.

---

## Memory Protocol (MANDATORY)

**Before creating an agent:**

```bash
cat .claude/context/memory/learnings.md
```

Check for patterns in previous agent creations.

**After creating an agent:**

- Record the new agent pattern to `.claude/context/memory/learnings.md`
- If the domain is new, add to `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

## Iron Laws of Agent Creation

These rules are INVIOLABLE. Breaking them causes silent failures.

```
1. NO AGENT WITHOUT TOOLS FIELD
   - Every agent MUST have tools: [Read, ...] in frontmatter
   - Agents without tools cannot perform actions

2. NO AGENT WITHOUT SKILLS FIELD
   - Every agent SHOULD have skills: [...] in frontmatter
   - Skills provide specialized workflows

3. NO MULTI-LINE YAML DESCRIPTIONS
   - description: | causes parsing failures
   - Always use single-line description

4. NO SKILLS THAT DON'T EXIST
   - Every skill in skills: array must exist at .claude/skills/<skill>/SKILL.md
   - Run: node .claude/tools/validate-agents.mjs to catch broken pointers

5. NO AGENT WITHOUT MEMORY PROTOCOL
   - Every agent MUST have Memory Protocol section in body
   - Without it, learnings are lost

6. NO AGENT WITHOUT ROUTING TABLE ENTRY
   - After creating agent, add to CLAUDE.md routing table
   - Unrouted agents are never spawned

7. NO CREATION WITHOUT SYSTEM IMPACT ANALYSIS
   - Update CLAUDE.md routing table (MANDATORY)
   - Update router.md agent tables (MANDATORY)
   - Check if new workflows are needed
   - Check if related agents need skill updates
   - Document all system changes made

8. NO AGENT WITHOUT TASK TRACKING
   - Every agent MUST include Task Progress Protocol section
   - Every agent MUST have task tools in tools: array
   - Without task tracking, work is invisible to Router

9. NO AGENT WITHOUT ROUTER KEYWORDS
   - Every agent MUST have researched keywords (Step 2.5)
   - Keywords must be documented in research report
   - Agent must be registered in router-enforcer.cjs with keywords
   - Without router keywords, agent will never be discovered by Router

10. NO AGENT WITHOUT RESPONSE APPROACH
    - Every agent MUST have Response Approach section with 8 numbered steps
    - Every agent MUST have Behavioral Traits section with 10+ domain-specific traits
    - Every agent MUST have Example Interactions section with 8+ examples
    - Without these sections, execution strategy is undefined
    - Reference python-pro.md for canonical structure
```

## System Impact Analysis (MANDATORY)

**After creating ANY agent, you MUST analyze and update system-wide impacts.**

### Impact Checklist

Run this analysis after every agent creation:

```
[AGENT-CREATOR] System Impact Analysis for: <agent-name>

1. ROUTING TABLE UPDATE (MANDATORY)
   - Add entry to CLAUDE.md routing table
   - Format: | Request Type | agent-name | .claude/agents/<category>/<name>.md |
   - Choose appropriate request type keywords

2. ROUTER AGENT UPDATE (MANDATORY)
   - Update router.md Core/Specialized/Domain agent tables
   - Add to Planning Orchestration Matrix if applicable
   - Add example spawn pattern if complex

3. SKILL ASSIGNMENT CHECK
   - Are all assigned skills valid? (validate-agents.mjs checks this)
   - Should any existing skills be assigned to this agent?
   - Scan .claude/skills/ for relevant unassigned skills

4. WORKFLOW CHECK
   - Does this agent need a dedicated workflow?
   - Should it be added to existing enterprise workflows?
   - Create/update .claude/workflows/ as needed

5. RELATED AGENT CHECK
   - Does this agent overlap with existing agents?
   - Should existing agents reference this one?
   - Update Planning Orchestration Matrix for multi-agent patterns
```

### Example: Creating a "technical-writer" Agent

```
[AGENT-CREATOR] Created: .claude/agents/core/technical-writer.md

[AGENT-CREATOR] System Impact Analysis...

1. ROUTING TABLE UPDATE
   Added to CLAUDE.md:
   | Documentation, docs | technical-writer | .claude/agents/core/technical-writer.md |

2. ROUTER AGENT UPDATE
   Added to router.md Core Agents table
   Added to Planning Orchestration Matrix:
   | Documentation (new/update) | technical-writer | - | Single |

3. SKILL ASSIGNMENT CHECK
   Assigned skills: writing, doc-generator, writing-skills, task-management-protocol
   All skills exist and validated

4. WORKFLOW CHECK
   Consider creating: .claude/workflows/documentation-workflow.md

5. RELATED AGENT CHECK
   No overlap with existing agents
   Planner may delegate doc tasks to this agent
```

### System Update Commands

```bash
# Add to CLAUDE.md routing table (edit manually)
# Look for "## 3. AGENT ROUTING TABLE" section

# Update router.md agent tables (edit manually)
# Look for "Core Agents:" or "Specialized Agents:" sections

# Verify routing table entry exists
grep "<agent-name>" .claude/CLAUDE.md || echo "ERROR: Not in routing table!"

# Verify router.md entry exists
grep "<agent-name>" .claude/agents/core/router.md || echo "ERROR: Not in router!"

# Full validation
node .claude/tools/validate-agents.mjs
```

### Validation Checklist (Run After Every Creation) - BLOCKING

**This checklist is BLOCKING. All items must pass before agent creation is complete.**

```bash
# Verify keyword research report exists (Step 2.5) - MANDATORY
[ -f ".claude/context/artifacts/research-reports/agent-keywords-<agent-name>.md" ] || echo "ERROR: Keyword research report missing - AGENT CREATION INCOMPLETE"

# Validate the new agent
node .claude/tools/validate-agents.mjs 2>&1 | grep "<agent-name>"

# Verify skills exist
for skill in $(grep -A10 "^skills:" .claude/agents/<category>/<agent>.md | grep "  - " | sed 's/  - //'); do
  [ -f ".claude/skills/$skill/SKILL.md" ] || echo "BROKEN: $skill"
done

# Check CLAUDE.md routing table - MANDATORY
grep "<agent-name>" .claude/CLAUDE.md || echo "ERROR: Not in routing table - AGENT CREATION INCOMPLETE"

# Check router-enforcer.cjs keywords registration (Step 7.5) - MANDATORY
grep "<agent-name>" .claude/hooks/routing/router-enforcer.cjs || echo "ERROR: Agent not in router-enforcer.cjs - AGENT CREATION INCOMPLETE"
```

**Completion Checklist** (all must be checked):

```
[ ] Step 2.5 keyword research completed (3+ Exa searches)
[ ] Keyword research report saved to .claude/context/artifacts/research-reports/agent-keywords-<name>.md
[ ] Agent file created at .claude/agents/<category>/<name>.md
[ ] All required YAML fields present (name, description, model, context_strategy, tools, skills, context_files)
[ ] model field is base name only (sonnet/opus/haiku) - NO dated versions
[ ] NO extended_thinking field unless explicitly documented
[ ] NO MCP tools (mcp__*) unless whitelisted
[ ] All assigned skills exist in .claude/skills/
[ ] CLAUDE.md routing table updated
[ ] Routing table entry verified with grep
[ ] validate-agents.mjs passes for new agent
[ ] Task Progress Protocol section included in agent body
[ ] Task tools included in tools: array
[ ] Router keywords registered in router-enforcer.cjs (Iron Law #9)
[ ] Response Approach section present with 8 numbered steps (Iron Law #10)
[ ] Behavioral Traits section present with 10+ domain-specific traits (Iron Law #10)
[ ] Example Interactions section present with 8+ examples (Iron Law #10)
[ ] Compared against python-pro.md reference agent structure
```

**BLOCKING**: If ANY item fails, agent creation is INCOMPLETE. Fix all issues before proceeding.

---

## Workflow Integration

This skill is part of the unified artifact lifecycle. For complete multi-agent orchestration:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- How the Router discovers and invokes this skill's artifacts

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Discovery, creation, update, deprecation phases
- Version management and registry updates
- CLAUDE.md integration requirements

**External Integration:** `.claude/workflows/core/external-integration.md`

- Safe integration of external artifacts
- Security review and validation phases

---

## Cross-Reference: Creator Ecosystem

This skill is part of the **Creator Ecosystem**. After creating an agent, consider whether companion creators are needed:

| Creator              | When to Use                                     | Invocation                             |
| -------------------- | ----------------------------------------------- | -------------------------------------- |
| **skill-creator**    | Agent needs new skills not in `.claude/skills/` | `Skill({ skill: 'skill-creator' })`    |
| **workflow-creator** | Agent needs orchestration workflow              | `Skill({ skill: 'workflow-creator' })` |
| **template-creator** | Agent needs code templates                      | `Skill({ skill: 'template-creator' })` |
| **schema-creator**   | Agent needs input/output validation schemas     | `Skill({ skill: 'schema-creator' })`   |
| **hook-creator**     | Agent needs pre/post execution hooks            | `Skill({ skill: 'hook-creator' })`     |

### Integration Workflow

After creating an agent that needs additional capabilities:

```javascript
// 1. Agent created but needs new skill
Skill({ skill: 'skill-creator' });
// Create the skill, then update agent's skills: array

// 2. Agent needs MCP server integration
// Use skill-creator to convert MCP server to skill
// node .claude/skills/skill-creator/scripts/convert.cjs --server "@modelcontextprotocol/server-xyz"

// 3. Agent needs workflow
// Create workflow in .claude/workflows/<agent-name>-workflow.md
// Update CLAUDE.md Section 8.6 if enterprise workflow
```

### Post-Creation Checklist for Ecosystem Integration

After agent is fully created and validated:

```
[ ] Does agent need skills that don't exist? -> Use skill-creator
[ ] Does agent need multi-phase orchestration? -> Create workflow
[ ] Does agent need code scaffolding? -> Create templates
[ ] Does agent interact with external services? -> Consider MCP integration
[ ] Should agent be part of enterprise workflows? -> Update Section 8.6
```
