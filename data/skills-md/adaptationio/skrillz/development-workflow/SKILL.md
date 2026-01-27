---
name: development-workflow
description: Complete end-to-end skill development workflow orchestrating research, planning, task breakdown, prompt design, and progress tracking. Use when building new Claude Code skills, creating workflow skills, or following systematic development process from concept to validated skill.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Development Workflow

## Overview

development-workflow provides a complete end-to-end process for developing Claude Code skills from concept to production. It orchestrates five component skills (skill-researcher, planning-architect, task-development, prompt-builder, todo-management) into a cohesive workflow that ensures systematic, research-driven, high-quality skill development.

**Purpose**: Systematic skill development using proven best practices

**Pattern**: Workflow-based (5-step sequential process with one optional step)

**Key Benefit**: Transforms ad-hoc skill building into a repeatable, quality-assured process

**Component Skills**:
1. skill-researcher: Multi-source research (Web, GitHub, MCP, docs)
2. planning-architect: Skill architecture and structure design
3. task-development: Detailed task breakdown with estimates (optional)
4. prompt-builder: High-quality prompt creation for operations
5. todo-management: Real-time progress tracking

## When to Use

Use development-workflow when:
- Building a new Claude Code skill from scratch
- Want systematic, research-driven approach
- Need to ensure quality through structured process
- Building complex skills (workflow-based, many operations)
- Want to leverage the complete skill toolkit
- Following bootstrap strategy for efficiency

## Prerequisites

Before starting this workflow:
- **Clear objective**: Know what skill you want to build and why
- **Component skills available**: All 5 skills installed and accessible
- **Time allocated**: 4-8 hours for workflow (research through task list)
- **Implementation time**: Additional time to actually build the skill (varies by complexity)
- **Research goal**: Specific domain or problem to research

## Skill Development Workflow

### Step 1: Research Domain & Patterns

Research the domain comprehensively to discover patterns, best practices, examples, and validate approaches before designing the skill.

**Purpose**: Ground skill in proven patterns and community knowledge

**Component Skill**: skill-researcher

**Integration Method**: Guided execution (user invokes skill-researcher with specific goals)

**When to Use**: Always (never skip research)

**Inputs**:
- Skill objective: [What the skill should accomplish]
- Research questions:
  - What patterns exist for this type of skill?
  - What are community best practices?
  - What examples are available?
  - What MCP servers exist (if integration needed)?
  - What official documentation exists?

**Process**:

1. **Define Research Scope**:
   ```markdown
   Research Goal: [Skill domain/topic]

   Questions to Answer:
   - What organizational patterns are used?
   - What are best practices for [domain]?
   - What code/structure examples exist?
   - What official specifications exist?
   - What MCP integrations are available?
   ```

2. **Execute Research Operations**:

   Invoke skill-researcher and execute all relevant operations:

   **Operation 1: Web Search Research**
   - Query: "[domain] best practices 2025"
   - Query: "Claude Code [skill type] patterns"
   - Sources: Minimum 3-5 credible sources
   - Document findings: web-research.md

   **Operation 2: GitHub Repository Research** (if code patterns needed)
   - Search: [domain] examples, official repositories
   - Analyze: 3-5 repositories for patterns
   - Extract: Code structures, organizational patterns
   - Document findings: github-patterns.md

   **Operation 3: Documentation Research**
   - Find: Official Claude Code documentation
   - Find: Domain-specific official docs
   - Extract: Specifications, requirements, best practices
   - Document findings: official-docs.md

   **Operation 4: MCP Server Research** (if integration needed)
   - Search: MCP servers for [domain]
   - Evaluate: Capabilities, maturity, integration complexity
   - Document findings: mcp-options.md

   **Operation 5: Synthesize Research Findings**
   - Organize: All findings by theme
   - Identify: Patterns appearing across 3+ sources
   - Resolve: Any conflicts between sources
   - Create: research-synthesis.md with actionable insights

3. **Review Synthesis**:
   - Read complete synthesis document
   - Note key patterns identified
   - Note best practices found
   - Note examples to reference
   - Identify any gaps requiring additional research

4. **Extract Key Insights**:
   ```markdown
   # Key Insights from Research

   ## Patterns Identified:
   1. [Pattern 1]: Appears in [X] sources
   2. [Pattern 2]: Appears in [Y] sources

   ## Best Practices:
   1. [Practice 1] - from [sources]
   2. [Practice 2] - from [sources]

   ## Examples to Reference:
   - [Example 1]: [Source and what it demonstrates]
   - [Example 2]: [Source and what it demonstrates]

   ## Recommendations:
   1. [Actionable recommendation based on research]
   2. [Actionable recommendation based on research]
   ```

**Outputs**:
- research-synthesis.md: Complete multi-source synthesis
- Key patterns identified (minimum 2)
- Best practices extracted (minimum 3)
- Examples captured (minimum 3)
- Actionable recommendations (minimum 2)

**Validation**:
- [ ] Minimum 3-5 sources consulted
- [ ] Patterns identified across multiple sources
- [ ] Best practices documented with sources
- [ ] Examples captured with references
- [ ] Synthesis document complete
- [ ] Recommendations are specific and actionable

**Time Estimate**: 1-2 hours

**Common Issues**:
- **Issue**: Insufficient sources found
  - **Solution**: Broaden search terms, try related domains, check official docs
- **Issue**: No clear patterns emerge
  - **Solution**: Look at higher-level patterns (workflow vs task-based), check similar skills
- **Issue**: Conflicting information
  - **Solution**: Prioritize official docs, look for consensus (3+ sources agreeing)

**Next**: Proceed to Step 2 with research findings

---

### Step 2: Plan Skill Architecture

Design the skill's structure, scope, and approach based on research findings. Define what goes where and how the skill will be organized.

**Purpose**: Create clear architectural plan before implementation

**Component Skill**: planning-architect

**Integration Method**: Guided execution

**When to Use**: Always (planning is essential)

**Inputs**:
- research-synthesis.md (from Step 1)
- Skill objective (what it should accomplish)
- Target users (who will use it)
- Success criteria (what "done" looks like)

**Process**:

1. **Prepare Planning Inputs**:
   ```markdown
   Skill Objective: [Clear statement of what skill does]
   Target Users: [Who will use this - developers, domain experts, etc.]
   Success Criteria: [What makes this skill successful]
   Research Findings: [Key patterns and practices from Step 1]
   ```

2. **Invoke planning-architect Workflow**:

   Execute all 5 steps of planning-architect:

   **Step 1: Understand Requirements**
   - Review research findings
   - Clarify skill objective
   - Identify target users and their needs
   - Define success criteria
   - Note constraints (time, complexity, dependencies)

   **Step 2: Choose Organizational Pattern**
   - Evaluate patterns: Workflow vs Task-based vs Reference vs Capabilities
   - Consider research findings (what patterns did you see?)
   - Choose pattern with rationale
   - Document decision

   Example decision:
   ```markdown
   Pattern: Workflow-based
   Rationale: Sequential steps with clear dependencies (research found 80% of similar skills use workflow pattern)
   ```

   **Step 3: Design Structure**
   - Design SKILL.md sections (Overview, When to Use, Steps/Operations)
   - Plan references/ directory (what detailed guides needed?)
   - Plan scripts/ directory (what automation needed?)
   - Create file structure outline

   **Step 4: Plan Content**
   - For each workflow step or task operation:
     - Define purpose
     - List inputs needed
     - Describe process
     - Specify outputs
     - Define validation criteria
   - Plan reference file contents
   - Plan script functionality

   **Step 5: Validate Plan**
   - Check completeness (all sections planned?)
   - Check coherence (does structure make sense?)
   - Check feasibility (can it be built?)
   - Review against research findings
   - Confirm success criteria addressed

3. **Create Planning Documents**:

   Generate these artifacts:

   **skill-plan.md**: Complete architecture
   ```markdown
   # Skill Plan: [Name]

   ## Pattern: [Chosen pattern]
   Rationale: [Why this pattern]

   ## Structure:
   - SKILL.md: [Sections planned]
   - references/: [Files planned]
   - scripts/: [Scripts planned]

   ## Content Plan:
   [For each section, what it contains]

   ## Validation: [Plan review results]
   ```

   **structure-outline.md**: Visual file structure
   ```
   [skill-name]/
   ├── SKILL.md
   ├── references/
   │   ├── [reference-1].md
   │   └── [reference-2].md
   ├── scripts/
   │   └── [script-1].py
   └── README.md
   ```

4. **Review and Adjust**:
   - Read complete plan
   - Verify against research findings
   - Check for gaps or inconsistencies
   - Adjust as needed before proceeding

**Outputs**:
- skill-plan.md: Complete skill architecture and approach
- structure-outline.md: File structure with all planned files
- content-specifications.md: What each section/file will contain
- Pattern choice documented with rationale

**Validation**:
- [ ] Pattern chosen (workflow/task/reference/capabilities) with rationale
- [ ] File structure designed (SKILL.md + references + scripts)
- [ ] All sections planned with content specifications
- [ ] Plan aligns with research findings
- [ ] Plan addresses success criteria
- [ ] Plan validated for completeness and feasibility

**Time Estimate**: 1-1.5 hours

**Common Issues**:
- **Issue**: Can't decide between patterns
  - **Solution**: Check research - what pattern did similar skills use? Default to workflow for sequential processes, task-based for independent operations
- **Issue**: Uncertain about what references to create
  - **Solution**: References for any topic needing >500 words of detail
- **Issue**: Not sure if scripts needed
  - **Solution**: Scripts for automation, validation, or user convenience - often optional

**Next**: Proceed to Step 3 (optional) or Step 4

---

### Step 3: Design Task Breakdown (Optional)

Break down skill implementation into detailed tasks with estimates, dependencies, and optimal sequencing. This step is optional but recommended for complex skills.

**Purpose**: Create detailed, actionable task list for systematic implementation

**Component Skill**: task-development

**Integration Method**: Guided execution

**When to Use**:
- Complex skills (>20 tasks estimated)
- Team coordination needed
- Tight timeline/budget
- Want detailed planning

**When to Skip**:
- Simple skills (<10 tasks estimated)
- Solo development with flexible timeline
- Prefer lightweight planning

**Decision Criteria**:
```
Use task-development if ANY of:
- Workflow-based skill with 5+ steps
- Each step needs 500+ words of content
- Multiple reference files (3+)
- Scripts with significant logic
- Unfamiliar domain (learning curve)

Skip task-development if ALL of:
- Task-based skill with <8 operations
- Familiar domain
- Solo developer
- Flexible timeline
```

**Inputs**:
- skill-plan.md (from Step 2)
- Complexity assessment (simple/medium/complex)

**Process**:

1. **Assess Complexity**:
   ```markdown
   Skill: [Name]
   Pattern: [workflow/task/etc]

   Estimated Components:
   - SKILL.md sections: [count]
   - Reference files: [count]
   - Scripts: [count]
   - Total estimated tasks: [rough guess]

   Decision: [Use task-development: YES/NO]
   Rationale: [Why]
   ```

2. **If Using task-development, Execute Workflow**:

   Invoke task-development and execute all 6 steps:

   **Step 1: Analyze Skill Plan**
   - Review complete skill plan
   - Identify major components (SKILL.md, each reference, each script)
   - Note complexity areas
   - Consider dependencies

   **Step 2: Identify Major Components**
   - List all deliverables:
     - SKILL.md with all sections
     - Each reference file
     - Each script file
     - README.md
     - Any examples or templates

   **Step 3: Break Down Components into Tasks**
   - For each component, create specific tasks
   - Example for SKILL.md:
     - Task 1: YAML frontmatter (15 min)
     - Task 2: Overview section (30 min)
     - Task 3: Step 1 detailed instructions (1h)
     - Task 4: Step 2 detailed instructions (1h)
     - ... etc
   - Be specific: "Write X" not "Work on X"

   **Step 4: Estimate Each Task**
   - Use historical data if available (how long similar tasks took)
   - Use comparison (similar to Task X which took Y)
   - Use three-point: (optimistic + 4×most-likely + pessimistic) / 6
   - Document estimates with method used

   **Step 5: Identify Dependencies**
   - For each task, what must complete first?
   - Hard dependencies (blocking): "Task 5 MUST wait for Task 2"
   - Soft dependencies (preferred): "Task 7 easier after Task 4"
   - Document rationale for each dependency

   **Step 6: Sequence Tasks Optimally**
   - Create execution sequence
   - Identify critical path (longest chain of dependencies)
   - Note parallel opportunities (tasks that can run simultaneously)
   - Optimize schedule

3. **Create Task List Document**:
   ```markdown
   # Task List: [Skill Name]

   Total Tasks: [count]
   Estimated Time: [range]
   Critical Path: [time]

   ## Tasks:

   1. Create directory structure (15 min) - No dependencies
   2. SKILL.md: YAML frontmatter (15 min) - Depends on: 1
   3. SKILL.md: Overview (30 min) - Depends on: 2
   ...

   ## Dependencies:
   [Detailed dependency list with rationale]

   ## Critical Path:
   [Tasks on critical path]

   ## Parallel Opportunities:
   [Tasks that can run simultaneously]
   ```

4. **Validate Task List**:
   - Check: All components from plan have tasks
   - Check: Estimates sum to reasonable total
   - Check: Dependencies make sense
   - Check: Critical path identified

**Outputs** (if used):
- task-list.md: Complete task breakdown with estimates
- dependencies.md: Task dependencies and critical path
- schedule.md: Optimal task sequence

**Validation** (if used):
- [ ] All components broken into specific tasks
- [ ] Each task has time estimate
- [ ] Dependencies identified with rationale
- [ ] Critical path calculated
- [ ] Parallel opportunities noted
- [ ] Total time estimate reasonable

**Time Estimate**: 30-60 minutes (if used)

**Alternative** (if skipped):
Create simple task checklist:
```markdown
## Simple Task List:

- [ ] Create directory structure
- [ ] Build SKILL.md
- [ ] Build reference files (X files)
- [ ] Build scripts (if needed)
- [ ] Build README.md
- [ ] Validate skill
```

**Next**: Proceed to Step 4

---

### Step 4: Create High-Quality Prompts

Build effective prompts for each workflow step or task operation in the skill. Use prompt-builder to ensure quality, clarity, and consistency.

**Purpose**: Create prompts that produce reliable, high-quality results

**Component Skill**: prompt-builder

**Integration Method**: Guided execution (invoke for each prompt needed)

**When to Use**: Always (quality prompts are critical)

**Inputs**:
- skill-plan.md (workflow steps or operations defined)
- task-list.md (if available, shows what needs prompts)
- Number of prompts needed: [One per workflow step or task operation]

**Process**:

1. **Identify Prompts Needed**:

   From skill plan, list each workflow step or task operation:
   ```markdown
   Prompts Needed:

   Workflow-based skill:
   - Prompt 1: Step 1 instructions
   - Prompt 2: Step 2 instructions
   - Prompt 3: Step 3 instructions
   ...

   Task-based skill:
   - Prompt 1: Operation 1 instructions
   - Prompt 2: Operation 2 instructions
   ...
   ```

2. **For Each Prompt, Execute prompt-builder Workflow**:

   Invoke prompt-builder for each prompt (can do multiple in sequence):

   **Step 1: Understand Context**
   - Goal: What should this prompt accomplish?
   - Audience: Claude executing the skill
   - Situation: Position in workflow/skill
   - Constraints: Format, length, style
   - Success: What does good execution look like?

   **Step 2: Define Task Clearly**
   - Action verb: Specific action (Invoke, Execute, Analyze, Create...)
   - Object: What's being acted on
   - Constraints: Explicit requirements (format, length, inclusions)
   - Quality criteria: Measurable success indicators
   - Context references: What information to use

   **Step 3: Structure Prompt**
   - Choose template (workflow step vs task operation)
   - Organize sections:
     - Purpose statement
     - Component skill used (if any)
     - Inputs
     - Process (numbered steps)
     - Outputs
     - Validation checklist
   - Format consistently

   **Step 4: Add Context & Examples**
   - Background: Why this step exists
   - Examples: Good output examples
   - Boundaries: What NOT to do
   - Success patterns: What quality looks like

   **Step 5: Refine & Validate**
   - Check clarity (unambiguous?)
   - Check specificity (precise requirements?)
   - Check completeness (all info provided?)
   - Score quality dimensions (target: all ≥4)
   - Iterate if needed

3. **Collect and Review All Prompts**:
   ```markdown
   # Prompt Collection: [Skill Name]

   ## Step 1 Prompt:
   [Complete prompt text]
   Quality Score: [Clarity: 4.5, Specificity: 4.0, ...]

   ## Step 2 Prompt:
   [Complete prompt text]
   Quality Score: [Clarity: 5.0, Specificity: 4.5, ...]

   ...
   ```

4. **Check Consistency**:
   - Review all prompts together
   - Check consistent terminology
   - Check consistent style
   - Check logical flow between prompts
   - Adjust for consistency

**Outputs**:
- prompts-collection.md: All prompts for workflow steps/operations
- quality-scores.md: Validation scores for each prompt (all should be ≥4)
- Prompts ready to integrate into SKILL.md

**Validation**:
- [ ] One prompt per workflow step/operation
- [ ] All prompts score ≥4 on quality dimensions (clarity, specificity, completeness, actionability, reliability)
- [ ] Prompts use consistent terminology
- [ ] Prompts use consistent style and format
- [ ] Examples provided where helpful
- [ ] Validation criteria included in each prompt

**Time Estimate**: 1-2 hours (depends on number of prompts)

**Common Issues**:
- **Issue**: Prompt too vague
  - **Solution**: Add specific numbers, formats, examples
- **Issue**: Prompt validation scores <4
  - **Solution**: Add context, examples, specific criteria - iterate with prompt-builder
- **Issue**: Inconsistent terminology across prompts
  - **Solution**: Define key terms once, use consistently

**Next**: Proceed to Step 5

---

### Step 5: Track Implementation Progress

Monitor task completion, identify blockers, maintain momentum throughout skill implementation. Use todo-management continuously from start to completion.

**Purpose**: Systematic progress tracking ensures completion and identifies issues early

**Component Skill**: todo-management

**Integration Method**: Continuous execution (used throughout implementation phase)

**When to Use**: Always (throughout implementation)

**Inputs**:
- task-list.md (from Step 3) OR
- Simple task list (if Step 3 skipped)

**Process**:

1. **Initialize Todo List**:

   **If task-list.md exists** (from Step 3):
   ```bash
   python task-development/scripts/break-down-tasks.py --input task-list.md --output todos.md
   # Or use todo-management script:
   python todo-management/scripts/update-todos.py --init task-list.md [skill-name]
   ```

   **If simple task list** (Step 3 skipped):
   Create todos.md manually:
   ```markdown
   # Todo List: [Skill Name]

   Started: [date]
   Estimate: [time range]

   ⬜ 1. Create directory structure (15 min)
   ⬜ 2. Build SKILL.md: YAML frontmatter (15 min)
   ⬜ 3. Build SKILL.md: Overview (30 min)
   ⬜ 4. Build SKILL.md: Step 1 (1h)
   ...

   Progress: 0/X tasks (0%)
   ```

2. **Throughout Implementation, Use Todo Management Operations**:

   **Operation 1: Start Task**
   - When beginning work: Mark task as in_progress (🔄)
   - RULE: Only ONE task in_progress at a time
   - Add start timestamp
   ```bash
   python todo-management/scripts/update-todos.py --start [task-number]
   ```

   **Operation 2: Complete Task**
   - When task finished and verified: Mark as completed (✅)
   - Add completion timestamp
   - Record actual time (compare to estimate)
   ```bash
   python todo-management/scripts/update-todos.py --complete [task-number] --actual "[time]"
   ```

   **Operation 3: Report Progress**
   - Generate status report (end of session, before meetings)
   ```bash
   python todo-management/scripts/update-todos.py --report
   ```

   **Operation 4: Identify Blockers**
   - If task blocked: Mark as blocked (🚫) with reason
   - Address blocker within 1 day
   ```bash
   python todo-management/scripts/update-todos.py --block [task-number] --reason "[specific blocker]"
   ```

   **Operation 5: Update Estimates**
   - As you work: Note actual times vs estimates
   - Learn for future estimates
   - Adjust remaining task estimates if needed

   **Operation 6: Handle Task Changes**
   - Add new tasks discovered during implementation
   - Mark obsolete tasks as obsolete (⊗)
   - Update task descriptions if needed

   **Operation 7: Maintain Momentum**
   - Ensure progress every session (≥1 task completed)
   - Address blockers quickly
   - Celebrate completions

3. **Monitor Progress Continuously**:
   ```markdown
   # Progress Check (daily/per session)

   ✅ Completed: [count]
   🔄 In Progress: [count] (should be 1)
   ⬜ Pending: [count]
   🚫 Blocked: [count] (should be 0 or addressing)

   Percentage: [completed/total × 100]%
   Velocity: [tasks per day/session]
   Blockers: [list any, with resolution plan]
   Next Session: [next task to start]
   ```

4. **Continue Until All Tasks Complete**:
   - Work through task list systematically
   - Mark tasks complete immediately (don't batch)
   - Keep only ONE task in_progress
   - Address blockers same-day
   - Generate final completion summary

**Outputs**:
- todos.md: Real-time task tracking (updated continuously)
- progress-reports/: Status reports generated
- completion-summary.md: Final summary with actual times vs estimates

**Validation**:
- [ ] Todo list initialized from task list
- [ ] Tasks updated in real-time (not batched)
- [ ] Only ONE task in_progress at any time
- [ ] Blockers identified and addressed
- [ ] Progress reports generated regularly
- [ ] Actual times recorded vs estimates
- [ ] All tasks eventually completed

**Time Estimate**: Continuous (throughout implementation, which varies by skill complexity)

**Common Issues**:
- **Issue**: Multiple tasks in_progress
  - **Solution**: Complete current task before starting next (focus)
- **Issue**: Blocker sitting for days
  - **Solution**: Address within 1 day, escalate if can't resolve
- **Issue**: Estimates wildly off
  - **Solution**: Learning opportunity - note for future, adjust remaining estimates
- **Issue**: Losing momentum (no completions)
  - **Solution**: Break large tasks smaller, find quick wins, identify blockers

**Next**: Implementation complete when all tasks done

---

## Post-Workflow: Implementation Phase

After completing the 5-step workflow, you have:
- ✅ Research findings with patterns and best practices
- ✅ Complete skill plan with structure
- ✅ Task list with estimates (or simple checklist)
- ✅ High-quality prompts for all steps/operations
- ✅ Progress tracking system initialized

**Now**: Implement the skill using the plan, prompts, and task list

**During Implementation**:
- Follow the task list order
- Use prompts created in Step 4
- Track progress with Step 5 (todo-management)
- Reference research findings (Step 1) as needed
- Refer to skill plan (Step 2) for structure

**After Implementation**:
- Validate skill structure (YAML, files, format)
- Test skill execution (dry run, actual use)
- Review against research best practices
- Iterate and refine as needed

## Best Practices

### Research-Driven Development

**1. Never Skip Research** (Step 1)
- Research grounds skill in proven patterns
- Prevents reinventing solutions
- Validates approach early
- Discovers existing MCP integrations

**2. Multi-Source Validation**
- Minimum 3-5 sources
- Cross-reference findings
- Look for consensus (3+ sources agreeing)
- Prioritize official documentation

**3. Pattern Recognition**
- Note what appears multiple times
- This is consensus pattern
- Document source consensus
- Apply to your skill

### Planning Before Building

**1. Complete Planning Before Implementation** (Step 2)
- Prevents mid-implementation rework
- Ensures coherent structure
- Identifies gaps early
- Provides roadmap

**2. Choose Pattern Deliberately**
- Workflow: Sequential dependencies
- Task-based: Independent operations
- Reference: Standards/guidelines
- Capabilities: Multiple integrated features
- Document rationale

**3. Plan Content, Not Just Structure**
- Don't just list sections
- Specify what each contains
- Identify examples needed
- Note validation criteria

### Task Management

**1. Use Task Breakdown for Complex Skills** (Step 3)
- If >20 tasks: Use task-development
- If <10 tasks: Simple checklist fine
- When in doubt: Use full task breakdown

**2. Estimate Realistically**
- Use historical data when available
- Three-point estimation for uncertainty
- Track actuals to improve future estimates

**3. Manage Dependencies**
- Identify critical path
- Find parallel opportunities
- Don't let dependencies block unnecessarily

### Prompt Quality

**1. Invest Time in Prompts** (Step 4)
- Quality prompts = quality skill
- All prompts should score ≥4
- Consistency across prompts matters
- Examples clarify intent

**2. Validate Each Prompt**
- Use prompt-builder validation
- Check all 5 dimensions
- Iterate until quality threshold met
- Don't skip this step

**3. Include Validation Criteria**
- Every prompt needs validation
- Checkboxes for verification
- Measurable, objective criteria
- Enables self-assessment

### Progress Tracking

**1. Track Continuously** (Step 5)
- Update immediately (don't batch)
- One task in_progress rule
- Complete before moving to next
- Address blockers same-day

**2. Maintain Momentum**
- ≥1 task completed per session
- Celebrate completions
- Break large tasks if stuck
- Keep progressing

**3. Learn from Actuals**
- Record actual time vs estimate
- Note what took longer/shorter
- Improve future estimates
- Identify efficiency opportunities

## Common Mistakes

### Mistake 1: Skipping Research

**Problem**: Building without understanding existing patterns
- Reinvents solutions
- Misses best practices
- Lower quality result

**Fix**: Always complete Step 1, minimum 3-5 sources

### Mistake 2: Starting Implementation Without Plan

**Problem**: Ad-hoc structure, rework needed
- Incoherent organization
- Missing components discovered late
- Wasted effort

**Fix**: Complete Step 2 planning before writing any code/content

### Mistake 3: Poor Quality Prompts

**Problem**: First-draft prompts without validation
- Vague instructions
- Inconsistent results
- Users confused

**Fix**: Use Step 4 prompt-builder, ensure all ≥4 quality score

### Mistake 4: No Progress Tracking

**Problem**: Losing momentum, incomplete tasks
- Work feels endless
- Blockers unaddressed
- Don't know when done

**Fix**: Use Step 5 todo-management from start to finish

### Mistake 5: Skipping Optional Step When Needed

**Problem**: Complex skill without task breakdown
- Overwhelmed by complexity
- Missing dependencies
- Inefficient execution

**Fix**: Use Step 3 for complex skills (>20 tasks, unfamiliar domain, team coordination)

### Mistake 6: Multiple Tasks In Progress

**Problem**: Context switching, nothing completing
- Divided attention
- Tasks incomplete
- Momentum lost

**Fix**: ONE task in_progress rule, complete before next

## Integration Notes

### Component Skills Used

**skill-researcher** (Step 1):
- Used once at workflow start
- Provides foundation for everything after
- Essential, never skip
- Time: 1-2 hours

**planning-architect** (Step 2):
- Used once after research
- Depends on research findings
- Produces plan for Steps 3-4
- Time: 1-1.5 hours

**task-development** (Step 3):
- Optional, used for complex skills
- Depends on plan from Step 2
- Produces task list for Step 5
- Time: 30-60 minutes (if used)

**prompt-builder** (Step 4):
- Used multiple times (once per prompt)
- Depends on plan (knows what prompts needed)
- Produces prompts for implementation
- Time: 1-2 hours

**todo-management** (Step 5):
- Used continuously during implementation
- Depends on task list (from Step 3 or simple list)
- Tracks progress until complete
- Time: Ongoing throughout implementation

### Using Skills Individually

All component skills work independently outside this workflow:
- skill-researcher: Any research need
- planning-architect: Planning any project
- task-development: Breaking down any work
- prompt-builder: Creating any prompt
- todo-management: Tracking any task list

This workflow orchestrates them for complete skill development.

### Workflow Variations

**Fast Track** (simple skills):
- Step 1: Research (required)
- Step 2: Planning (required)
- Step 3: Skip task-development, use simple checklist
- Step 4: Prompt building (required)
- Step 5: Progress tracking (required)
- Time: ~3-4 hours + implementation

**Full Process** (complex skills):
- All 5 steps
- Detailed task breakdown
- Comprehensive planning
- Time: ~5-8 hours + implementation

## Quick Reference

### The 5-Step Process

1. **Research Domain**: skill-researcher (1-2h) - Always required
2. **Plan Architecture**: planning-architect (1-1.5h) - Always required
3. **Task Breakdown**: task-development (30-60m) - Optional for complex
4. **Build Prompts**: prompt-builder (1-2h) - Always required
5. **Track Progress**: todo-management (ongoing) - Always required

### Decision Points

**Use task-development?**
- Yes: Complex (>20 tasks), team work, tight timeline
- No: Simple (<10 tasks), solo, flexible timeline

### Time Budget

- **Workflow Phase**: 4-8 hours (research through task list)
- **Implementation Phase**: Varies by skill (simple: 2-3h, complex: 8-12h)
- **Total**: Simple skill ~6-10 hours, Complex skill ~15-20 hours

### Success Criteria

✅ Research complete (3+ sources, patterns identified)
✅ Plan created (structure, content, validation)
✅ Tasks defined (breakdown or checklist)
✅ Prompts built (all ≥4 quality)
✅ Progress tracked (todos updated continuously)
✅ Implementation complete (all tasks done)
✅ Skill validated (structure, function, quality)

---

For workflow examples and common patterns, see references/workflow-examples.md.

For patterns used in official skills, see references/common-patterns.md.
