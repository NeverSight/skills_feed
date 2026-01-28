---
name: research
description: Start a research project with intelligent agent orchestration
metadata:
  short-description: Intelligent Research Orchestration
---

# /research - Intelligent Research Orchestration

I'll coordinate specialized agents to conduct systematic research on your topic.

## Research Topic
**Query**: $ARGUMENTS

## 🤖 Orchestration Mode

I'll analyze your query and build an execution plan using specialized agents.

**Agent Registry**:
- `literature-reviewer`: Academic source search, citation chains
- `critical-analyzer`: Fallacy detection, bias identification
- `hypothesis-explorer`: Hypothesis formulation, variable mapping
- `lateral-thinker`: Cross-domain analogies, creative thinking
- `qual-researcher`: Thematic analysis, coding strategies
- `quant-analyst`: Statistical methods, effect sizes
- `peer-reviewer`: Manuscript evaluation
- `ethics-expert`: IRB compliance, privacy risks
- `grant-writer`: Grant proposal development, funding strategy

**Orchestration Process**:
1. **Classify Query**: Determine research type
2. **Select Agents**: Choose optimal agent sequence
3. **Generate Plan**: Build execution DAG
4. **Present Plan**: Show workflow to user
5. **Execute**: Run agents sequentially, save outputs
6. **Synthesize**: Integrate outputs, save final report

I'm analyzing your research topic to determine the optimal workflow...

**Proposed Plan**:
[I will generate this based on your query]

**Proceed?** (yes/no/modify)

---

## File Writing Protocol

**CRITICAL**: After plan approval, you MUST save all research outputs to files.

### Step 1: Create Output Directory
After user approves the plan, immediately:
1. Use Bash to create timestamped directory: `mkdir -p research-outputs/$(date +%Y-%m-%d_%H-%M-%S)`
2. Store the full path in a variable for subsequent file writes
3. Confirm directory creation to user

### Step 2: Write Research Plan
Use Write tool to create `00-research-plan.md` in the output directory:
```markdown
# Research Plan: [Query]

**Created**: [Timestamp]
**Query**: [User's research query]

## Selected Agents
1. [agent-name] - [purpose]
2. [agent-name] - [purpose]
...

## Execution Plan
[Full plan as presented to user]
```

### Step 3: Write Agent Outputs
After EACH agent completes execution:
1. Use Write tool to save output to `{NN}-{agent-name}.md`
   - NN = sequential number (01, 02, 03, etc.)
   - Example: `01-literature-reviewer.md`, `02-critical-analyzer.md`
2. Format:
```markdown
# {Agent Name} Output

**Agent**: {agent-name}
**Executed**: [Timestamp]

---

[Full agent output - preserve all markdown formatting]
```

### Step 4: Write Final Synthesis
After synthesis completes:
1. Use Write tool to save to `final-synthesis.md`
2. Include complete synthesis with all sections
3. Add metadata header with timestamp and agents used

### Error Handling
- If directory creation fails: warn user and continue with conversation-only output
- If Write fails: log error, notify user, continue execution
- Partial results are acceptable if execution is interrupted

---

**Modes Supported**:
- Default: Interactive
- `--auto`: Automatic execution
- `--plan-only`: Show plan only
- `--manual`: Traditional guided mode

**Templates**: `--template=quick|rigorous|comprehensive`
