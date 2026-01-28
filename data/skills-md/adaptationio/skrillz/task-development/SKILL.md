---
name: task-development
description: Break down skill development into concrete tasks with time estimates, dependencies, and validation criteria. Creates actionable task lists, identifies blockers, estimates effort, and sequences work optimally. Use when planning skill implementation, managing complex builds, or coordinating parallel work.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Task Development

## Overview

task-development transforms skill plans into actionable task lists with time estimates, dependencies, and optimal sequencing. It bridges the gap between high-level planning (from planning-architect) and actual implementation.

**Purpose**: Convert skill plans into concrete, executable tasks that can be tracked and completed systematically.

**Value**: Prevents missed work, ensures realistic scheduling, identifies blockers early, and enables efficient parallel work.

**When to Use**:
- After completing skill plan with planning-architect
- When breaking down complex skill implementations
- When coordinating work across multiple developers
- When estimating detailed implementation timelines
- When identifying critical path and parallel opportunities

## Prerequisites

Before breaking down tasks, you need:

1. **Completed Skill Plan**: Full skill plan from planning-architect with:
   - Requirements analysis
   - Pattern selection
   - File structure plan
   - Complexity estimate
   - Dependencies identified
   - Validation criteria

2. **Understanding of Skill Pattern**: Know which organizational pattern was chosen

3. **Familiarity with Skill-Builder**: Understanding of skill development process

## Task Development Workflow

### Step 1: Analyze Skill Plan

**Objective**: Thoroughly understand the skill plan before breaking it down

**Process**:

1. **Read Complete Plan**
   - Review all 6 sections from planning-architect
   - Understand requirements and scope
   - Note pattern selection and justification
   - Review file structure plan
   - Check dependency requirements

2. **Identify High-Level Phases**
   - Initialization phase (directory setup)
   - Content development phase (SKILL.md + references)
   - Automation phase (scripts/templates)
   - Validation phase (testing)
   - Documentation phase (README, finalization)

3. **Note Critical Constraints**
   - Hard dependencies (must-have prerequisites)
   - Sequencing requirements (what must come first)
   - Resource constraints (tools, knowledge, time)
   - Validation requirements (how to verify)

4. **Understand Success Criteria**
   - What does "done" look like?
   - What are validation gates?
   - What's the minimum viable version?

**Output**: Clear understanding of entire scope

**Example**:
```
Analyzing task-development plan:
- Pattern: Workflow-based (6 sequential steps)
- Files: SKILL.md + 3 references + 1 script
- Estimate: 12-15 hours
- Critical: Depends on planning-architect being complete
- Success: Can break down skill plans into tasks
```

---

### Step 2: Identify Major Components

**Objective**: Break skill into major building blocks

**Process**:

1. **Extract Components from Structure Plan**

   From the file structure plan, identify:
   - SKILL.md (always a component)
   - Each reference file (separate component)
   - Each script (separate component)
   - Each template (separate component)
   - README/documentation (component)
   - Validation (component)

2. **Group Related Work**

   Combine when appropriate:
   - Multiple small references → single "references" component
   - Related scripts → grouped component
   - Setup tasks → "initialization" component

3. **Identify Cross-Cutting Concerns**

   Tasks that span components:
   - Research (may inform multiple components)
   - Design decisions (impact multiple files)
   - Integration work (connecting pieces)
   - Testing (validates multiple components)

4. **List All Components**

   Create comprehensive list:
   ```
   Major Components:
   1. Initialization & Setup
   2. SKILL.md Development
   3. Reference Files Development
   4. Script Development
   5. Template Development (if applicable)
   6. Documentation (README)
   7. Validation & Testing
   ```

**Output**: Complete list of major components (typically 5-10)

**Example** (for task-development itself):
```
Major Components:
1. Initialization (directory setup)
2. SKILL.md (6-step workflow)
3. references/task-breakdown-patterns.md
4. references/estimation-techniques.md
5. references/dependency-management.md
6. scripts/break-down-tasks.py
7. README.md
8. Validation & Testing
```

**See Also**: [references/task-breakdown-patterns.md](references/task-breakdown-patterns.md) for component identification patterns by skill type

---

### Step 3: Break Down Components into Tasks

**Objective**: Decompose each component into concrete, actionable tasks

**Granularity Guidelines**:

**Task Size**: Each task should be:
- Completable in 30 minutes to 4 hours
- Have clear start and end points
- Produce tangible output
- Be independently testable

**Too Large**: "Build all references" (break down further)
**Good**: "Write task-breakdown-patterns.md sections 1-3"
**Too Small**: "Write one paragraph" (combine with others)

**Process**:

For each major component:

1. **SKILL.md Breakdown**
   ```
   Component: SKILL.md

   Tasks:
   - Create SKILL.md with YAML frontmatter (30 min)
   - Write Overview section (1 hour)
   - Write Prerequisites section (30 min)
   - Write Step 1: [Action] (1-2 hours)
   - Write Step 2: [Action] (1-2 hours)
   - Write Step 3: [Action] (1-2 hours)
   - Write Step 4: [Action] (1-2 hours)
   - Write Step 5: [Action] (1-2 hours)
   - Write Step 6: [Action] (1-2 hours)
   - Write Quick Start section (1 hour)
   - Write Examples section (1-2 hours)
   - Add references links (30 min)
   ```

2. **Reference Files Breakdown**
   ```
   Component: references/file-name.md

   Tasks:
   - Research topic (if needed) (1-3 hours)
   - Create file with structure (30 min)
   - Write main sections (2-4 hours per reference)
   - Add examples (1-2 hours)
   - Add cross-references (30 min)
   ```

3. **Script Breakdown**
   ```
   Component: scripts/script-name.py

   Tasks:
   - Design script architecture (1 hour)
   - Implement core functionality (2-4 hours)
   - Add error handling (1 hour)
   - Add --help documentation (30 min)
   - Test script with examples (1 hour)
   - Make executable (5 min)
   ```

4. **Documentation Breakdown**
   ```
   Component: README.md

   Tasks:
   - Write overview and purpose (30 min)
   - Document file structure (30 min)
   - Add usage examples (30 min)
   - Document dependencies (30 min)
   ```

5. **Validation Breakdown**
   ```
   Component: Validation

   Tasks:
   - Run structure validation (10 min)
   - Review content for completeness (30 min)
   - Test all examples (1 hour)
   - Fix any issues found (variable)
   ```

**Task Template**:
```
Task: [Action verb] [specific output]
Estimated Time: [X hours/minutes]
Prerequisites: [What must be done first]
Output: [What gets produced]
Validation: [How to verify complete]
```

**Output**: Complete task list with 15-40 tasks (depending on skill size)

**Example** (sample from task-development):
```
Tasks:
1. Create task-development directory structure (15 min)
2. Create SKILL.md with YAML frontmatter (30 min)
3. Write SKILL.md Overview section (1h)
4. Write SKILL.md Prerequisites section (30 min)
5. Write SKILL.md Step 1: Analyze Skill Plan (1.5h)
6. Write SKILL.md Step 2: Identify Major Components (1h)
7. Write SKILL.md Step 3: Break Down Components (2h)
8. Write SKILL.md Step 4: Estimate Each Task (1.5h)
9. Write SKILL.md Step 5: Identify Dependencies (1h)
10. Write SKILL.md Step 6: Sequence Tasks (1h)
11. Write SKILL.md Quick Start section (1h)
12. Write SKILL.md Examples section (1.5h)
13. Create references/task-breakdown-patterns.md (3h)
14. Create references/estimation-techniques.md (2.5h)
15. Create references/dependency-management.md (2h)
16. Create scripts/break-down-tasks.py (3h)
17. Create README.md (1h)
18. Validate with validate-skill.py (15 min)
19. Test with real skill plan (1h)
```

**See Also**: [references/task-breakdown-patterns.md](references/task-breakdown-patterns.md) for pattern-specific breakdown strategies

---

### Step 4: Estimate Each Task

**Objective**: Assign realistic time estimates to each task

**Estimation Techniques**:

#### Technique 1: Historical Data

Use actual time from similar tasks:

```
Previous: "Write SKILL.md Overview" took 45 min
Current: "Write SKILL.md Overview" → estimate 45 min
```

**When to Use**: When you have historical data
**Accuracy**: High (if similar context)

---

#### Technique 2: Comparison

Compare to known reference points:

```
"Write Step 1" is similar to "Write Overview" but 2x longer
Overview = 1h → Step 1 = 2h
```

**When to Use**: When similar tasks exist
**Accuracy**: Medium-High

---

#### Technique 3: Bottom-Up

Break task further and sum:

```
"Write Step 3: Break Down Components"
- Write process description: 30 min
- Write granularity guidelines: 30 min
- Write breakdown by component: 45 min
- Add examples: 30 min
- Add templates: 15 min
Total: 2h 30min
```

**When to Use**: For complex or uncertain tasks
**Accuracy**: High (but time-consuming)

---

#### Technique 4: Three-Point Estimation

Estimate optimistic, most likely, pessimistic:

```
"Create script"
Optimistic: 2h (everything goes smoothly)
Most Likely: 3h (typical case)
Pessimistic: 5h (debugging issues)

Formula: (O + 4M + P) / 6
Estimate: (2 + 12 + 5) / 6 = 3.2h
```

**When to Use**: For uncertain or risky tasks
**Accuracy**: Good for risky tasks

---

#### Technique 5: Expert Judgment

Use experience and intuition:

```
"This feels like a 2-hour task based on my experience"
```

**When to Use**: When other methods not applicable
**Accuracy**: Variable (improves with experience)

---

**Estimation Guidelines**:

1. **Start with Raw Estimate**
   - Use one of the techniques above
   - Don't add buffer yet

2. **Consider Complexity Factors**
   - Familiar work: 1.0x
   - Some learning: 1.3x
   - Significant new concepts: 1.5-2.0x

3. **Add Task-Level Buffer**
   - Simple task: 10% buffer
   - Medium complexity: 15% buffer
   - Complex/uncertain: 25% buffer

4. **Round to Reasonable Increments**
   - Under 1 hour: 15-min increments
   - 1-4 hours: 30-min increments
   - Over 4 hours: 1-hour increments

5. **Validate Total**
   - Sum all task estimates
   - Compare to planning-architect estimate
   - Should be within 10-20% of plan estimate
   - If significantly different, review

**Output**: Each task has time estimate

**Example**:
```
1. Create directory structure: 15 min
2. Create SKILL.md frontmatter: 30 min
3. Write Overview: 1h
4. Write Prerequisites: 30 min
5. Write Step 1: 1.5h
6. Write Step 2: 1h
7. Write Step 3: 2h
...
Total: 14.5 hours (within 12-15h plan estimate ✓)
```

**See Also**: [references/estimation-techniques.md](references/estimation-techniques.md) for comprehensive estimation methods

---

### Step 5: Identify Dependencies

**Objective**: Determine which tasks must be completed before others can start

**Dependency Types**:

#### Type 1: Hard Dependencies (Blocking)

Task B cannot start until Task A is complete:

```
Task A: Create SKILL.md structure
Task B: Write Step 1 in SKILL.md
Dependency: B depends on A (hard)
```

**Indicators**:
- Task B needs output from Task A
- Task B operates on files created by Task A
- Task B builds on concepts from Task A

---

#### Type 2: Soft Dependencies (Helpful)

Task B is easier if Task A is done, but not required:

```
Task A: Write SKILL.md workflow
Task B: Write reference guides
Dependency: B benefits from A (soft)
Reason: Seeing SKILL.md helps write consistent references
```

**Indicators**:
- Task B references Task A's output
- Task B is easier with Task A's context
- Task B may need minor updates after Task A

---

#### Type 3: No Dependency (Parallel)

Tasks can be done in any order:

```
Task A: Write reference-1.md
Task B: Write reference-2.md
Dependency: None (parallel)
```

**Indicators**:
- Tasks operate on different files
- Tasks have no shared dependencies
- Tasks don't reference each other

---

**Process**:

For each task, ask:

1. **What must exist before I start this task?**
   - Files: Which files must be created first?
   - Content: What content must be written first?
   - Decisions: What must be decided first?

2. **What tasks produce those prerequisites?**
   - Identify the tasks that create needed inputs

3. **Are dependencies hard or soft?**
   - Hard: Cannot start without it
   - Soft: Easier with it, but can proceed

4. **Can this task be parallelized?**
   - If no dependencies, can be done anytime
   - Enables parallel work

**Dependency Notation**:

```
Task ID | Task Name | Dependencies
--------|-----------|-------------
1       | Create dir| (none)
2       | SKILL.md  | 1
3       | Overview  | 2
4       | Step 1    | 2, 3
5       | Ref-1     | 2 (soft)
6       | Ref-2     | 2 (soft)
7       | Script    | 2, 5, 6
8       | README    | 2-7
9       | Validate  | 8
```

**Output**: Dependency map showing task relationships

**Example** (task-development):
```
Dependencies:
- Tasks 1-2: Sequential (create → scaffold)
- Tasks 3-12: Sequential (SKILL.md sections in order)
- Tasks 13-15: Parallel (references independent)
- Task 16: Depends on 13-15 (script uses reference patterns)
- Task 17: Depends on 2-16 (README describes everything)
- Task 18-19: Depends on 17 (validate complete skill)
```

**Critical Path**: Longest chain of dependent tasks
```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 17 → 18 → 19
(14.5 hours on critical path)
```

**Parallel Opportunities**:
```
Tasks 13, 14, 15 can be done in parallel (7.5h total)
If serial: 7.5h
If parallel: 3h (taking longest reference)
Savings: 4.5h with parallel work!
```

**See Also**: [references/dependency-management.md](references/dependency-management.md) for advanced dependency analysis

---

### Step 6: Sequence Tasks Optimally

**Objective**: Arrange tasks in optimal execution order

**Sequencing Strategies**:

#### Strategy 1: Dependency-Driven (Primary)

**Rule**: Always complete dependencies before dependent tasks

```
If Task B depends on Task A:
  Sequence: A → B (not B → A)

If Task C depends on A and B:
  Sequence: A → B → C (both A and B before C)
```

---

#### Strategy 2: Parallel Optimization

**Rule**: Execute independent tasks in parallel when possible

```
Tasks with no dependencies:
  Execute: Simultaneously (if resources available)

Example:
  Task A: Write reference-1.md (3h)
  Task B: Write reference-2.md (2.5h)
  Task C: Write reference-3.md (2h)

Serial: 7.5h
Parallel: 3h (longest task duration)
```

---

#### Strategy 3: Risk-First

**Rule**: Handle high-risk tasks early

```
High-risk tasks:
- New technology/unfamiliar domain
- Complex algorithms
- External dependencies
- Uncertain estimates

Sequence: Do these first to:
- Identify blockers early
- Adjust plan if needed
- Reduce late-stage surprises
```

---

#### Strategy 4: Quick Wins

**Rule**: Include some easy wins early

```
Benefits:
- Build momentum
- Provide early progress
- Boost confidence

Balance with risk-first approach
```

---

#### Strategy 5: Logical Grouping

**Rule**: Group related tasks together

```
Group by:
- Component (all SKILL.md tasks together)
- Type (all writing together, all coding together)
- Context (related functionality)

Benefits:
- Reduced context switching
- Better flow
- More efficient work
```

---

**Sequencing Process**:

1. **Create Phases**
   ```
   Phase 1: Initialization (setup tasks)
   Phase 2: Core Development (main content)
   Phase 3: Enhancement (references, scripts)
   Phase 4: Finalization (docs, validation)
   ```

2. **Within Each Phase, Order by**:
   - Dependencies (must-do-first)
   - Risk (high-risk early)
   - Logic (related tasks together)
   - Parallelization (independent tasks marked)

3. **Mark Parallel Opportunities**
   ```
   Task 13 ║ Write reference-1.md (3h)
   Task 14 ║ Write reference-2.md (2.5h)  } Parallel
   Task 15 ║ Write reference-3.md (2h)
   ```

4. **Identify Milestones**
   ```
   Milestone 1: SKILL.md complete
   Milestone 2: All references complete
   Milestone 3: Scripts complete
   Milestone 4: Validated and ready
   ```

**Output**: Sequenced task list with phases and parallel markers

**Example** (task-development sequenced):

```
PHASE 1: INITIALIZATION (15 min)
1. Create task-development directory structure [15 min]

PHASE 2: SKILL.MD CORE (9.5h)
2. Create SKILL.md with YAML frontmatter [30 min] → depends on 1
3. Write Overview section [1h] → depends on 2
4. Write Prerequisites section [30 min] → depends on 2
5. Write Step 1: Analyze Skill Plan [1.5h] → depends on 2
6. Write Step 2: Identify Components [1h] → depends on 5
7. Write Step 3: Break Down Tasks [2h] → depends on 6
8. Write Step 4: Estimate Tasks [1.5h] → depends on 7
9. Write Step 5: Identify Dependencies [1h] → depends on 8
10. Write Step 6: Sequence Tasks [1h] → depends on 9

MILESTONE: Core workflow complete

11. Write Quick Start section [1h] → depends on 2-10
12. Write Examples section [1.5h] → depends on 2-10

PHASE 3: REFERENCES (Parallel: 3h if parallel, 7.5h if serial)
13. ║ Create task-breakdown-patterns.md [3h] → depends on 2
14. ║ Create estimation-techniques.md [2.5h] → depends on 2
15. ║ Create dependency-management.md [2h] → depends on 2

MILESTONE: Documentation complete

PHASE 4: AUTOMATION (3h)
16. Create break-down-tasks.py [3h] → depends on 2, 13-15

PHASE 5: FINALIZATION (2.25h)
17. Create README.md [1h] → depends on all above
18. Validate with validate-skill.py [15 min] → depends on 17
19. Test with real skill plan [1h] → depends on 18

MILESTONE: Skill complete and validated

TOTAL TIME:
  Serial: 14.5 hours
  Optimal (with parallel refs): 11.5 hours
  Savings: 3 hours (21%)
```

---

## Quick Start: Break Down a Skill in 30 Minutes

### Prerequisites
- Completed skill plan from planning-architect
- 30 minutes available

### Rapid Breakdown Process

**10 minutes: Analyze & Identify**
1. Read skill plan quickly (5 min)
2. List major components from structure plan (5 min)

**15 minutes: Break Down & Estimate**
3. For each component, list 2-5 tasks (10 min)
4. Add rough time estimates (5 min)

**5 minutes: Dependencies & Sequence**
5. Mark obvious dependencies (3 min)
6. Put tasks in logical order (2 min)

**Result**: Actionable task list ready for implementation

### Example: 30-Minute Breakdown

**Skill**: simple-calculator

**Components** (2 min):
- SKILL.md
- README.md
- Validation

**Tasks** (10 min):
1. Create directory [10 min]
2. SKILL.md: Frontmatter + overview [30 min]
3. SKILL.md: Operations section [1h]
4. SKILL.md: Examples [30 min]
5. README.md [30 min]
6. Validate [15 min]

**Dependencies** (3 min):
- 2 depends on 1
- 3-4 depend on 2
- 5 depends on 2-4
- 6 depends on 5

**Sequence** (2 min):
1 → 2 → 3 → 4 → 5 → 6
Total: ~3 hours

**Done!** Ready to implement.

---

## Examples

### Example 1: Simple Skill Breakdown

**Skill**: troubleshooting-guide (task-based, 8 errors)

**Plan Summary**:
- Pattern: Task-based
- Files: SKILL.md + 1 reference
- Estimate: 8 hours

**Components**:
1. SKILL.md (task-based format)
2. references/advanced-troubleshooting.md
3. README.md
4. Validation

**Tasks** (18 total):
```
PHASE 1: SETUP (15 min)
1. Create directory structure [15 min]

PHASE 2: SKILL.MD (4.5h)
2. Create SKILL.md frontmatter [30 min]
3. Write Overview [30 min]
4. Write Error 1: [Name] [30 min]
5. Write Error 2: [Name] [30 min]
6. Write Error 3: [Name] [30 min]
7. Write Error 4: [Name] [30 min]
8. Write Error 5: [Name] [30 min]
9. Write Error 6: [Name] [30 min]
10. Write Error 7: [Name] [30 min]
11. Write Error 8: [Name] [30 min]
12. Write Quick Start [30 min]

PHASE 3: REFERENCES (2h)
13. Create advanced-troubleshooting.md [2h]

PHASE 4: FINALIZATION (1.25h)
14. Create README.md [45 min]
15. Validate structure [15 min]
16. Test all error cases [30 min]

Total: 8 hours ✓ (matches estimate)
```

**Dependencies**:
- Sequential: 1 → 2 → 3-12 → 13 → 14 → 15 → 16
- Parallel: Tasks 4-11 (8 error sections) could be parallel

---

### Example 2: Medium Skill Breakdown

**Skill**: api-integration (workflow-based)

**Plan Summary**:
- Pattern: Workflow-based (4 steps)
- Files: SKILL.md + 3 references + 1 script
- Estimate: 15 hours

**Components**:
1. SKILL.md (4-step workflow)
2. references/authentication-guide.md
3. references/endpoints-guide.md
4. references/error-handling-guide.md
5. scripts/test-api.py
6. README.md
7. Validation

**Tasks** (22 total):
```
PHASE 1: SETUP (15 min)
1. Create directory structure [15 min]

PHASE 2: SKILL.MD (6h)
2. Create frontmatter + overview [1h]
3. Write Prerequisites [30 min]
4. Write Step 1: Authentication [1.5h]
5. Write Step 2: Fetch Data [1h]
6. Write Step 3: Process Response [1h]
7. Write Step 4: Error Handling [1h]
8. Write Quick Start [1h]
9. Write Examples [1.5h]

MILESTONE: Core workflow done

PHASE 3: REFERENCES (5h - can be parallel)
10. ║ Create authentication-guide.md [2h]
11. ║ Create endpoints-guide.md [1.5h]
12. ║ Create error-handling-guide.md [1.5h]

PHASE 4: AUTOMATION (2h)
13. Design test-api.py [30 min]
14. Implement core functionality [1h]
15. Add error handling [30 min]
16. Make executable + test [15 min]

PHASE 5: FINALIZATION (1.75h)
17. Create README.md [1h]
18. Validate structure [15 min]
19. Test workflow with real API [1h]
20. Fix any issues [variable]

Total: 15 hours ✓
With parallel refs: 12.5 hours (2.5h savings)
```

---

### Example 3: Complex Skill Breakdown

**Skill**: testing-framework (capabilities-based)

**Plan Summary**:
- Pattern: Capabilities-based (3 capabilities)
- Files: SKILL.md + 5 references + 3 scripts
- Estimate: 28 hours

**Components**:
1. SKILL.md (capabilities structure)
2. references/unit-testing-guide.md
3. references/integration-testing-guide.md
4. references/e2e-testing-guide.md
5. references/test-data-guide.md
6. references/ci-integration-guide.md
7. scripts/init-tests.py
8. scripts/run-tests.py
9. scripts/generate-report.py
10. README.md
11. Validation

**Tasks** (35+ total):
```
PHASE 1: SETUP (20 min)
1. Create directory structure [20 min]

PHASE 2: SKILL.MD (10h)
2. Create frontmatter + overview [1.5h]
3. Write Capability 1: Unit Testing [2h]
4. Write Capability 2: Integration Testing [2h]
5. Write Capability 3: E2E Testing [2h]
6. Write Integration Patterns [1.5h]
7. Write Quick Start [1h]
8. Write Examples [2h]

PHASE 3: REFERENCES (10h - parallel)
9.  ║ unit-testing-guide.md [2.5h]
10. ║ integration-testing-guide.md [2.5h]
11. ║ e2e-testing-guide.md [3h]
12. ║ test-data-guide.md [1.5h]
13. ║ ci-integration-guide.md [1.5h]

PHASE 4: SCRIPTS (7h - can be parallel)
14. ║ init-tests.py [2h]
15. ║ run-tests.py [3h]
16. ║ generate-report.py [2h]

PHASE 5: FINALIZATION (2h)
17. Create README.md [1h]
18. Validate structure [15 min]
19. Integration testing [1.5h]
20. Fix issues [variable]

Total: 29 hours
With optimal parallelization: 20 hours (9h savings!)
```

---

## Task List Output Format

### Recommended Format

```markdown
# Task List: [skill-name]

**Generated**: [date]
**Based on**: [skill-name]-plan.md
**Total Estimate**: [X-Y hours]

---

## Summary

- **Total Tasks**: [N]
- **Serial Time**: [X hours]
- **Parallel Time**: [Y hours] (if applicable)
- **Estimated Savings**: [Z hours] with parallelization

---

## Task List

### Phase 1: [Phase Name]

**Duration**: [X hours]

| # | Task | Time | Dependencies | Status |
|---|------|------|--------------|--------|
| 1 | [Task description] | [Xh] | (none) | ⬜ |
| 2 | [Task description] | [Xh] | 1 | ⬜ |

### Phase 2: [Phase Name]

**Duration**: [X hours]

| # | Task | Time | Dependencies | Status |
|---|------|------|--------------|--------|
| 3 | [Task description] | [Xh] | 2 | ⬜ |
| 4 ║ [Task description] | [Xh] | 2 | ⬜ |
| 5 ║ [Task description] | [Xh] | 2 | ⬜ |

**Note**: Tasks 4-5 can be done in parallel (║ marker)

[Continue for all phases...]

---

## Milestones

- [ ] Milestone 1: [Description] (after task X)
- [ ] Milestone 2: [Description] (after task Y)
- [ ] Milestone 3: [Description] (after task Z)

---

## Critical Path

Tasks that must be done sequentially (longest chain):
```
1 → 2 → 3 → 6 → 9 → 12 → 15
Duration: [X hours]
```

---

## Parallel Opportunities

**Opportunity 1**: Tasks 4-5 (Phase 2)
- Serial: [X hours]
- Parallel: [Y hours]
- Savings: [Z hours]

**Opportunity 2**: Tasks 10-12 (Phase 3)
- Serial: [X hours]
- Parallel: [Y hours]
- Savings: [Z hours]

**Total Parallelization Savings**: [Z hours] ([N%])

---

## Notes

[Any special notes, risks, or considerations]
```

---

## Best Practices

### Task Breakdown Best Practices

1. **Right Granularity**
   - Tasks should be 30 min to 4 hours
   - Too large = hard to estimate and track
   - Too small = overhead and micro-management

2. **Clear Outputs**
   - Each task produces tangible output
   - Output should be verifiable
   - "Done" should be unambiguous

3. **Realistic Estimates**
   - Use historical data when available
   - Add appropriate buffers
   - Sum should match plan estimate (±20%)

4. **Dependencies Matter**
   - Identify all hard dependencies
   - Note soft dependencies for context
   - Enable parallelization opportunities

5. **Sequencing for Success**
   - Dependencies first (always)
   - High-risk tasks early (de-risk)
   - Quick wins included (momentum)
   - Logical grouping (efficiency)

### Common Mistakes

1. **Too Granular**
   - Problem: 100+ micro-tasks
   - Fix: Combine related tasks

2. **Too Coarse**
   - Problem: "Build entire skill" (1 task)
   - Fix: Break down to component level

3. **Ignoring Dependencies**
   - Problem: Parallel schedule for sequential work
   - Fix: Careful dependency analysis

4. **Optimistic Estimates**
   - Problem: No buffers, ideal-case thinking
   - Fix: Use buffers, three-point estimation

5. **No Validation Tasks**
   - Problem: "Done" but untested
   - Fix: Include validation tasks explicitly

---

## References

Comprehensive guides for each task development step:

- **[Task Breakdown Patterns](references/task-breakdown-patterns.md)** - Component identification patterns for each skill pattern type, granularity guidelines, breakdown templates, and common patterns by domain.

- **[Estimation Techniques](references/estimation-techniques.md)** - Detailed estimation methods (historical, comparison, bottom-up, three-point, expert judgment), calibration techniques, accuracy improvement, and estimation worksheets.

- **[Dependency Management](references/dependency-management.md)** - Dependency type identification, critical path analysis, parallel optimization strategies, circular dependency resolution, and dependency visualization techniques.

---

## Automation

Use the task breakdown automation script:

```bash
# Break down skill from plan file
python scripts/break-down-tasks.py skill-plan.md

# Interactive mode
python scripts/break-down-tasks.py --interactive

# Specify output file
python scripts/break-down-tasks.py skill-plan.md --output tasks.md
```

See script help:
```bash
python scripts/break-down-tasks.py --help
```

---

## Success Criteria

A successful task breakdown includes:

✅ **Complete Task List**
- All components from plan broken down
- 15-40 tasks (typical range)
- Tasks are right granularity (30min-4h)

✅ **Accurate Estimates**
- Each task has time estimate
- Total matches plan estimate (±20%)
- Buffers included appropriately

✅ **Clear Dependencies**
- All hard dependencies identified
- Dependencies enable sequencing
- Parallel opportunities noted

✅ **Optimal Sequence**
- Dependencies respected
- Logical phases defined
- Milestones identified
- Critical path clear

✅ **Actionable Output**
- Task list ready for todo-management
- Each task is concrete and clear
- Verification criteria defined

---

## Next Steps

After completing task breakdown:

1. **Review Task List**
   - Validate completeness
   - Check estimates seem reasonable
   - Verify dependencies are correct

2. **Feed to todo-management**
   - Use task list to create todos
   - Track progress as you work
   - Update estimates based on actuals

3. **Begin Implementation**
   - Start with Phase 1
   - Complete tasks in sequence
   - Mark tasks complete as you go

4. **Track & Adjust**
   - Compare actual vs estimated time
   - Adjust remaining estimates if needed
   - Learn for better estimation next time

---

## Quick Reference

### The 5-Step Task Breakdown Process

| Step | Focus | Key Output | Time |
|------|-------|------------|------|
| 1. Analyze Plan | Understand structure, complexity, scope | Component understanding | 15-30m |
| 2. Identify Components | List all deliverables from plan | Component list | 20-40m |
| 3. Break Into Tasks | Granular tasks (30min-4h each) | Task list with estimates | 45-90m |
| 4. Sequence & Dependencies | Order tasks, identify parallel work | Sequenced task list | 30-45m |
| 5. Create Task Document | Consolidated breakdown | Complete task document | 20-30m |

**Total Task Breakdown Time**: 2-4 hours

### Task Granularity Guidelines

| Too Small | Just Right | Too Large |
|-----------|------------|-----------|
| <30 min | 30min - 4h | >4 hours |
| Micro-tasks | Focused work | Needs breakdown |
| High overhead | Trackable | Hard to estimate |

**Sweet Spot**: 1-2 hour tasks (most trackable and estimable)

### Phase Organization Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **By File** | Many independent files | Phase 1: SKILL.md, Phase 2: References, Phase 3: Scripts |
| **By Layer** | Architectural layers | Phase 1: Foundation, Phase 2: Core, Phase 3: Advanced |
| **By Feature** | Feature-based development | Phase 1: Auth, Phase 2: Data, Phase 3: UI |
| **Sequential** | Strong dependencies | Phase 1→2→3 (each builds on previous) |

### Dependency Types

| Type | Meaning | Example | Impact |
|------|---------|---------|--------|
| **Hard** | B cannot start until A done | Structure before content | Serial work |
| **Soft** | B easier if A done first | Having plan helps writing | Preference |
| **Parallel** | A and B independent | Separate files | Time savings |

### Estimation Quick Tips

- **Historical**: Use past similar tasks for estimates
- **Bottom-up**: Sum component estimates (detailed but time-consuming)
- **Comparison**: Compare to known reference tasks
- **Buffer**: Add 15-20% for unknowns
- **Three-Point**: (Optimistic + 4×Likely + Pessimistic) / 6

### Common Task Patterns

**Foundation Phase** (Always first):
- Create directory structure
- Write YAML frontmatter
- Set up skeleton

**Core Content Phase** (Main work):
- Write each section/step/operation
- Build references
- Create examples

**Enhancement Phase** (Polish):
- Add best practices
- Write troubleshooting
- Create quick reference

**Finalization Phase** (Always last):
- Validation
- Testing
- Documentation

### Complexity Indicators

**Simple** (15-25 tasks, 8-12h):
- Single SKILL.md or 1-2 references
- Few dependencies
- Clear requirements

**Medium** (25-35 tasks, 15-25h):
- Multiple references
- Some automation scripts
- Moderate complexity

**Complex** (35-50+ tasks, 30-50h):
- Extensive references (5-10 files)
- Multiple automation scripts
- High complexity, many dependencies

### Quick Breakdown Checklist

- [ ] All plan components identified
- [ ] Tasks 30min-4h each (right granularity)
- [ ] 15-50 tasks total (typical range)
- [ ] Each task has estimate
- [ ] Total estimate ±20% of plan estimate
- [ ] All dependencies identified
- [ ] Sequence respects dependencies
- [ ] Parallel opportunities noted
- [ ] Phases logically organized
- [ ] Validation tasks included

### For More Information

- **Breakdown patterns**: references/task-breakdown-patterns.md
- **Estimation techniques**: references/estimation-techniques.md
- **Dependency management**: references/dependency-management.md
- **Automation**: scripts/break-down-tasks.py --help

---

**task-development** is the bridge between planning and implementation. Use it to transform skill plans into concrete, executable tasks that lead to successful skill development.