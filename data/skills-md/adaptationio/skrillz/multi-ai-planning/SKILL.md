---
name: multi-ai-planning
description: Create production-ready, agent-executable plans using verification-first approach, hierarchical decomposition, dependency mapping, and quality gates. Optional multi-AI research integration (Claude + Gemini + Codex). Use when planning complex features, migrations, refactorings, security implementations, or any multi-step agentic workflows requiring rigorous verification and parallel execution coordination.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Planning

## Overview

multi-ai-planning creates comprehensive, agent-executable plans for complex objectives using verification-first approach, hierarchical task decomposition, and rigorous quality validation.

**Purpose**: Transform objectives into structured, validated plans that agents can execute reliably

**Pattern**: Workflow-based (6-step sequential process)

**Key Innovation**: Plans are schema-validated, quality-scored (≥90/100), and designed for multi-agent parallel execution with built-in verification and checkpoint systems.

**Core Principles** (validated by Claude + Gemini + Codex):
1. **Verification-First**: Define success criteria before implementation
2. **Hierarchical Decomposition**: Break down to atomic, executable steps
3. **Explicit Dependencies**: Map all dependencies, identify parallel opportunities
4. **Quality Gates**: Multi-layer validation before execution
5. **Safe Checkpoints**: Git tags + patches for resumption and rollback

---

## When to Use

Use multi-ai-planning when:

- Planning complex features (>8 tasks, multiple components)
- Multi-step migrations or refactorings
- Security implementations requiring verification
- System integrations with many touch points
- Projects requiring multi-agent coordination
- When parallel execution optimization is important
- Quality and verification are critical

**When NOT to Use**:
- Simple tasks (<3 steps)
- Ad-hoc exploratory work
- Quick prototyping without formal structure

---

## Prerequisites

### Required
- Clear objective (know what you want to accomplish)
- Time for planning (1-3 hours depending on complexity)

### Optional (for enhanced planning)
- **multi-ai-research skill** (for research phase)
- **Gemini CLI** (`npm install -g @google/gemini-cli`) - web research
- **Codex CLI** (`npm install -g @openai/codex`) - code pattern research

### Understanding
- Familiarity with the objective domain
- Basic understanding of agent coordination (see references/task-tool-coordination.md)

---

## Planning Workflow

### Step 1: Objective Analysis & Research

Analyze the objective and optionally research best practices, patterns, and approaches before creating the plan.

**Purpose**: Ground plan in proven patterns and understand problem space

**When to Use**: Always (research optional but recommended for unfamiliar domains)

**Inputs**:
- Clear objective statement
- Context about current system (if applicable)
- Success criteria (what "done" looks like)

**Process**:

1. **Clarify Objective**:
   ```markdown
   Objective: [Specific statement of what needs to be accomplished]

   Context:
   - Current state: [What exists now]
   - Desired state: [What should exist]
   - Constraints: [Time, resources, compatibility]

   Success Criteria:
   1. [Specific, measurable criterion]
   2. [Criterion 2]
   3. [Criterion 3]
   ```

2. **Determine Plan Type**:
   - Feature development (new functionality)
   - Refactoring (improve existing code)
   - Migration (move to new technology/pattern)
   - Security implementation (add security features)
   - Integration (connect systems)
   - Research project (investigate and document)

3. **Optional: Research Domain** (recommended for complex/unfamiliar):

   **If using multi-ai-research skill**:
   ```
   Use multi-ai-research for "Research [domain] best practices and implementation patterns"
   ```

   This will provide:
   - Official documentation insights (Claude)
   - Latest web best practices (Gemini)
   - GitHub implementation patterns (Codex)
   - Multi-source validation

   **Manual research** (if multi-ai-research not available):
   - Search web for "[domain] best practices 2024-2025"
   - Review official documentation
   - Find 3-5 example implementations
   - Document findings in research-notes.md

4. **Analyze Approach Options**:
   Based on research (if done), identify 2-3 possible approaches:
   ```markdown
   ## Approach Options

   ### Option A: [Approach name]
   - **Description**: [How it works]
   - **Pros**: [Benefits]
   - **Cons**: [Drawbacks]
   - **Complexity**: Low/Medium/High
   - **Risk**: Low/Medium/High

   ### Option B: [Alternative]
   [Same format]

   ### Recommended: [Choice] because [rationale]
   ```

5. **Define Initial Scope**:
   ```markdown
   ## Scope Definition

   **Included**:
   - [Component/area in scope]
   - [Component 2]

   **Excluded**:
   - [What we're NOT doing]
   - [Out of scope item 2]

   **Rationale**: [Why this scope is appropriate]
   ```

**Outputs**:
- Objective clarification document
- Plan type identified
- Research findings (if research conducted)
- Approach recommendation with rationale
- Initial scope definition

**Validation**:
- [ ] Objective is specific and clear
- [ ] Success criteria are measurable
- [ ] Plan type identified
- [ ] Approach chosen with rationale
- [ ] Scope defined (in/out)
- [ ] Research conducted (if needed)

**Time Estimate**: 30-60 minutes (research adds 30-60 min if used)

**Next**: Proceed to Step 2

---

### Step 2: Hierarchical Task Decomposition

Break down the objective into hierarchical tasks using recursive decomposition until reaching atomic, executable steps.

**Purpose**: Create complete task tree with appropriate granularity

**Inputs**:
- Objective and scope (from Step 1)
- Chosen approach
- Research findings (if available)

**Process**:

1. **Identify Large Tasks** (8-15 tasks):

   Break objective into major phases or components:
   ```markdown
   ## Large Task Breakdown

   1. **Database Schema** - Create data models and migrations
   2. **OAuth Integration** - Implement OAuth provider
   3. **API Endpoints** - Create authentication endpoints
   4. **Frontend Components** - Build UI for auth
   5. **Testing Suite** - Comprehensive tests
   6. **Documentation** - User and technical docs
   7. **Security Audit** - Verify security best practices
   8. **Deployment** - Production deployment

   Total large tasks: 8 (target: 8-15)
   ```

   **Granularity Check**:
   - Too few (<5): Tasks are too big, decompose more
   - Just right (8-15): Good granularity
   - Too many (>15): Tasks too small, group related tasks

2. **Decompose Large → Medium** (3-8 tasks each):

   For each large task, break into medium-sized tasks:
   ```markdown
   ### Large Task 2: OAuth Integration

   Medium tasks:
   2.1. Provider Configuration (setup OAuth provider)
   2.2. Token Management (generate, refresh, validate tokens)
   2.3. User Profile Sync (fetch and store user data)
   2.4. Error Handling (handle OAuth failures)
   2.5. Integration Tests (verify OAuth flow)

   Total: 5 medium tasks (target: 3-8)
   ```

   **For Complex Projects**: Can use Task tool to parallelize decomposition:
   ```typescript
   // Spawn parallel decomposition agents
   const decompositions = await Promise.all([
     task({
       description: "Decompose database schema task",
       prompt: `Break down "Database Schema" large task into 3-8 medium tasks.
       For each: description, dependencies, estimate.
       Write to decomp-task1.json`
     }),
     task({
       description: "Decompose OAuth task",
       prompt: `Break down "OAuth Integration"...
       Write to decomp-task2.json`
     })
   ]);
   // Integrate results into plan
   ```

3. **Decompose Medium → Small/Atomic** (for complex medium tasks):

   Continue breaking down until tasks are atomic (cannot be meaningfully subdivided):
   ```markdown
   ### Medium Task 2.2: Token Management

   Small/Atomic tasks:
   2.2.1. Create token schema (database)
   2.2.2. Implement token generation function
   2.2.3. Implement token refresh logic
   2.2.4. Add token validation middleware

   Total: 4 atomic tasks (can't break down further)
   ```

4. **Granularity Validation**:

   Check each task level:
   ```markdown
   ## Granularity Check

   **Huge** (if objective is massive): 15-25 large tasks
   **Large**: 8-15 medium tasks each
   **Medium**: 3-8 small tasks each
   **Small**: Atomic (single focused operation)

   ✅ All tasks at appropriate granularity
   ✅ No task is too big (>15 subtasks)
   ✅ No unnecessary subdivision
   ```

**Outputs**:
- Complete hierarchical task tree
- All tasks with clear descriptions
- Appropriate granularity at each level
- Task IDs in hierarchical format (1, 1.2, 1.2.3)

**Validation**:
- [ ] Large tasks (8-15) identified
- [ ] Complex large tasks decomposed to medium (3-8 each)
- [ ] Complex medium tasks decomposed to small/atomic
- [ ] All tasks have clear, actionable descriptions
- [ ] No task is too vague or too big
- [ ] Granularity appropriate at each level

**Time Estimate**: 45-90 minutes (varies with complexity)

**Next**: Proceed to Step 3

---

### Step 3: Dependency Mapping & Parallel Identification

Map dependencies between all tasks and identify opportunities for parallel execution.

**Purpose**: Enable optimal execution order and parallel agent coordination

**Inputs**:
- Complete task tree (from Step 2)

**Process**:

1. **Identify Dependencies**:

   For each task, ask:
   - What must be complete before this can start?
   - What information/artifacts does this task need?
   - What can this task be done in parallel with?

   ```markdown
   ## Dependency Analysis

   ### Task 1: Database Schema
   - **Depends on**: None (can start immediately)
   - **Provides for**: Tasks 2, 3, 4 (need schema to exist)

   ### Task 2: OAuth Integration
   - **Depends on**: Task 1 (needs user table schema)
   - **Provides for**: Task 3 (API needs OAuth)

   ### Task 3: API Endpoints
   - **Depends on**: Task 1 (schema), Task 2 (OAuth)
   - **Can parallel with**: Task 4 (frontend independent)

   ### Task 4: Frontend Components
   - **Depends on**: None initially (can mock API)
   - **Integration depends on**: Task 3 (real API)
   ```

2. **Build Dependency Graph**:

   Create visual or structured representation:
   ```markdown
   ## Dependency Graph

   ```mermaid
   graph TD
     T1[Task 1: Schema]
     T2[Task 2: OAuth]
     T3[Task 3: API]
     T4[Task 4: Frontend]
     T5[Task 5: Tests]

     T1 --> T2
     T1 --> T3
     T2 --> T3
     T3 --> T5
     T4 --> T5
   ```

   **JSON Format** (for schema):
   ```json
   {
     "dependencies": {
       "2": ["1"],
       "3": ["1", "2"],
       "5": ["3", "4"]
     }
   }
   ```

3. **Validate No Circular Dependencies**:

   Check for cycles:
   - Task A depends on Task B
   - Task B depends on Task C
   - Task C depends on Task A ❌ CIRCULAR!

   **Validation Method**:
   ```bash
   # Use scripts/visualize-deps.sh to generate graph
   # Visual inspection will show cycles
   # Or use topological sort algorithm
   ```

4. **Identify Parallel Execution Groups**:

   Group tasks that can run simultaneously:
   ```markdown
   ## Parallel Execution Opportunities

   ### Phase 1 (Immediate Start)
   - Task 1: Database Schema
   **Agents**: 1
   **Estimated**: 3h

   ### Phase 2 (After Task 1)
   - Task 2: OAuth Integration
   - Task 4: Frontend (can start with mocks)
   **Agents**: 2 parallel
   **Estimated**: 5h (max of the two)

   ### Phase 3 (After Tasks 2, 3)
   - Task 3: API Endpoints
   **Agents**: 1
   **Estimated**: 4h

   ### Phase 4 (After Tasks 3, 4)
   - Task 5: Tests (integration)
   **Agents**: 1
   **Estimated**: 3h

   **Total Sequential**: 15h
   **With Parallelization**: 12h (20% savings)
   ```

5. **Calculate Critical Path**:

   Find longest chain of dependent tasks:
   ```markdown
   ## Critical Path Analysis

   **Critical Path**: Task 1 → Task 2 → Task 3 → Task 5
   **Duration**: 3h + 5h + 4h + 3h = 15h

   **Optimization**: Task 4 can run in parallel, not on critical path

   **Focus**: Critical path tasks are priority for on-time completion
   ```

**Outputs**:
- Dependency map (JSON format)
- Dependency graph (visual/mermaid)
- Parallel execution groups identified
- Critical path calculated
- Optimized execution phases

**Validation**:
- [ ] All task dependencies documented
- [ ] No circular dependencies
- [ ] Dependency graph validates
- [ ] Parallel groups identified
- [ ] Critical path calculated
- [ ] Execution phases defined

**Time Estimate**: 30-45 minutes

**Next**: Proceed to Step 4

---

### Step 4: Verification Planning

For each task, define verification-first: specify how to verify it's done correctly BEFORE planning implementation.

**Purpose**: Ensure every task is testable and has clear success criteria

**Inputs**:
- Complete task tree with dependencies (from Steps 2-3)

**Process**:

1. **For Each Task, Define Success Criteria**:

   Use SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound):
   ```markdown
   ### Task 2.2.2: Implement Token Generation

   **Success Criteria** (defined FIRST):
   - [ ] Function `generateToken(user)` exists in src/auth/tokens.ts
   - [ ] Function returns JWT string (format: xxx.yyy.zzz)
   - [ ] Token includes userId claim in payload
   - [ ] Token expires in 24 hours (exp claim)
   - [ ] Token signed with process.env.JWT_SECRET
   - [ ] Function throws error for invalid user
   - [ ] Function handles missing user gracefully

   **NOT** vague criteria like:
   ❌ "Token generation works"
   ❌ "Function is implemented"
   ```

2. **Choose Verification Method**:

   Select appropriate verification for each task:
   - **automated_test**: Unit/integration tests (preferred)
   - **manual_check**: Manual verification (when automation not feasible)
   - **visual_inspection**: UI/UX verification (screenshots)
   - **integration_test**: End-to-end workflow tests
   - **code_review**: Review for quality/security

3. **Define Verification Commands** (for automated):

   ```markdown
   ### Verification Method: automated_test

   **Commands**:
   ```bash
   # Run specific test file
   npm test -- src/auth/tokens.test.ts

   # Verify function exists
   grep -q "function generateToken" src/auth/tokens.ts || exit 1

   # Check test coverage
   npm run coverage -- --file=src/auth/tokens.ts
   ```

   **Expected**: All tests pass, coverage ≥80%
   **Timeout**: 30 seconds
   ```

4. **Plan Quality Gates**:

   Define gates at major milestones:
   ```markdown
   ## Quality Gates

   ### Gate 1: Foundation Complete (after Tasks 1-2)
   - [ ] Database schema created and migrated
   - [ ] OAuth provider configured
   - [ ] All tests pass
   - [ ] No linting errors

   ### Gate 2: Core Features Complete (after Tasks 3-4)
   - [ ] API endpoints functional
   - [ ] Frontend integrated
   - [ ] Integration tests pass
   - [ ] Manual testing complete

   ### Gate 3: Production Ready (after all tasks)
   - [ ] All functionality verified
   - [ ] Security audit passed
   - [ ] Documentation complete
   - [ ] Deployment tested
   ```

5. **Add to Task Definitions**:

   Update each task with verification:
   ```json
   {
     "id": "2.2.2",
     "description": "Implement token generation function",
     "verification": {
       "success_criteria": [
         "Function generateToken(user) exists",
         "Returns JWT string format xxx.yyy.zzz",
         "Includes userId claim",
         "Expires in 24 hours",
         "Throws on invalid user"
       ],
       "method": "automated_test",
       "commands": [
         "npm test -- src/auth/tokens.test.ts",
         "npm run coverage -- --file=src/auth/tokens.ts"
       ],
       "timeout_seconds": 30
     }
   }
   ```

**Outputs**:
- All tasks have success criteria (minimum 1, target 3-5)
- All tasks have verification method
- Automated verification commands (where applicable)
- Quality gates defined at milestones

**Validation**:
- [ ] Every task has specific success criteria
- [ ] Success criteria are measurable
- [ ] Verification method appropriate for task
- [ ] Automated commands provided (where feasible)
- [ ] Quality gates defined
- [ ] No vague criteria ("it works", "done")

**Time Estimate**: 45-75 minutes

**Next**: Proceed to Step 5

---

### Step 5: Quality Verification & Scoring

Validate the plan for completeness, feasibility, clarity, and executability. Score 0-100 with ≥90 threshold for approval.

**Purpose**: Ensure plan quality before execution begins

**Inputs**:
- Complete plan with tasks, dependencies, verification (from Steps 1-4)

**Process**:

1. **Run Schema Validation**:

   ```bash
   # Validate plan structure
   bash .claude/skills/multi-ai-planning/scripts/validate-schema.sh plan.json

   # Expected output:
   # ✅ plan.json validates against plan.schema.json
   # ✅ All tasks validate
   # ✅ All checkpoints validate
   ```

2. **Check Completeness** (scored /20):

   ```markdown
   ### Completeness Assessment

   - All requirements mapped to tasks: [X]/5
     - Check: Every requirement from Step 1 has task(s)
     - Missing: [List any unmapped requirements]

   - All tasks have success criteria: [X]/5
     - Check: Every task has ≥1 criterion
     - Missing: [List tasks without criteria]

   - All dependencies documented: [X]/5
     - Check: All task dependencies in dependency graph
     - Missing: [Any undocumented dependencies]

   - Resource requirements clear: [X]/5
     - Check: Agents, tools, permissions documented
     - Missing: [Any unclear requirements]

   **Completeness Score**: [X]/20
   ```

3. **Assess Feasibility** (scored /20):

   ```markdown
   ### Feasibility Assessment

   - Resources available: [X]/5
     - Required agents: Available ✅ / Missing ❌
     - Required tools: Available ✅ / Missing ❌

   - Timeline realistic: [X]/5
     - Estimated: [X] hours
     - Available time: [Y] hours
     - Realistic ✅ / Optimistic ⚠️ / Unrealistic ❌

   - No blocking constraints: [X]/5
     - API access: ✅
     - Permissions: ✅
     - External dependencies: ✅

   - Dependencies manageable: [X]/5
     - Critical path length: Reasonable ✅ / Too long ❌
     - Parallel opportunities: Identified ✅

   **Feasibility Score**: [X]/20
   ```

4. **Evaluate Clarity** (scored /20):

   ```markdown
   ### Clarity Assessment

   - All steps unambiguous: [X]/5
     - Check each task description
     - Vague tasks: [List]

   - Terms defined: [X]/5
     - Technical terms explained ✅
     - Acronyms defined ✅

   - Examples provided: [X]/5
     - Complex tasks have examples ✅
     - Verification examples present ✅

   - Agent assignments clear: [X]/5
     - Each task suggests agent type ✅
     - Coordination documented ✅

   **Clarity Score**: [X]/20
   ```

5. **Score Executability** (scored /20):

   ```markdown
   ### Executability Assessment

   - Success criteria measurable: [X]/5
     - All criteria are objective ✅
     - Can determine pass/fail ✅

   - Verification methods defined: [X]/5
     - All tasks have method ✅
     - Methods appropriate ✅

   - Failure handling planned: [X]/5
     - Failure scenarios documented ✅
     - Rollback procedures defined ✅

   - Rollback procedures clear: [X]/5
     - Checkpoints defined ✅
     - Recovery steps documented ✅

   **Executability Score**: [X]/20
   ```

6. **Assess Integration** (scored /20):

   ```markdown
   ### Integration Assessment

   - Integration points identified: [X]/5
     - All system touch points mapped ✅
     - APIs, databases, services documented ✅

   - Backward compatibility checked: [X]/5
     - Compatibility plan exists ✅
     - Migration strategy defined ✅

   - Testing strategy defined: [X]/5
     - Unit tests planned ✅
     - Integration tests planned ✅
     - E2E tests planned ✅

   - Documentation plan clear: [X]/5
     - User docs planned ✅
     - Technical docs planned ✅
     - API docs planned ✅

   **Integration Score**: [X]/20
   ```

7. **Calculate Total Quality Score**:

   ```markdown
   ## Quality Score Summary

   - Comprehensiveness: [X]/20
   - Feasibility: [X]/20
   - Clarity: [X]/20
   - Executability: [X]/20
   - Integration: [X]/20

   **Total Score**: [X]/100

   **Threshold**: ≥90 for approval

   **Result**:
   - ≥90: ✅ APPROVED (proceed to execution)
   - 80-89: ⚠️ NEEDS MINOR REVISION (address gaps)
   - 70-79: ❌ NEEDS MAJOR REVISION (significant issues)
   - <70: ❌ REJECTED (fundamental problems, re-plan)
   ```

8. **If Score <90, Identify Gaps**:

   ```markdown
   ## Gap Analysis

   ### Critical Gaps (Blocking Approval)
   1. [Gap description]
      - **Impact**: Why this matters
      - **Fix**: Specific action to address
      - **Effort**: [time to fix]

   ### Medium Gaps (Should Fix)
   1. [Gap]

   **Estimated Effort to Reach ≥90**: [X] hours
   **Recommendation**: [Apply fixes and re-verify / Re-plan from scratch]
   ```

9. **Generate Verification Report**:

   Use templates/VERIFICATION_TEMPLATE.md to create detailed report.

**Outputs**:
- Quality score (0-100) with dimension breakdown
- Verification report with gap analysis
- Approval decision (approved / needs revision / rejected)
- If needs revision: specific fixes required

**Validation**:
- [ ] All 5 quality dimensions scored
- [ ] Total score calculated correctly
- [ ] Threshold check performed (≥90)
- [ ] Gaps identified if score <90
- [ ] Verification report generated

**Time Estimate**: 30-45 minutes

**Decision Point**:
- If ≥90: Proceed to Step 6 (Finalization)
- If <90: Apply fixes, return to relevant step, re-verify

**Next**: If approved, proceed to Step 6

---

### Step 6: Finalization & Output Generation

Generate final plan outputs in both machine-readable (JSON) and human-readable (Markdown) formats.

**Purpose**: Create production-ready plan artifacts ready for agent execution

**Inputs**:
- Approved plan (quality score ≥90 from Step 5)

**Process**:

1. **Generate plan.json** (machine-readable):

   Compile all plan data into schema-validated JSON:
   ```bash
   # Use templates and gathered data to create plan.json
   # Validate against schema
   bash scripts/validate-schema.sh plan.json

   # Expected output:
   # ✅ Valid JSON
   # ✅ Validates against plan.schema.json
   # ✅ All required fields present
   ```

2. **Generate PLAN.md** (human-readable):

   Create markdown version from plan.json or use template:
   ```bash
   # Generate markdown from JSON
   bash scripts/generate-plan-md.sh plan.json > PLAN.md

   # Or use template and fill in manually
   cp templates/PLAN_TEMPLATE.md PLAN.md
   # Fill in all sections with plan data
   ```

   Ensures:
   - All information from JSON present
   - Formatted for human readability
   - Includes visual dependency graph
   - Quality score displayed
   - Clear next steps

3. **Generate COORDINATION.md** (agent execution guide):

   Document how agents should execute this plan:
   ```markdown
   # Execution Coordination Guide

   ## Phase 1: Immediate Start
   **Task 1**: Database Schema
   **Agent**: Use Task tool to spawn code-writer agent
   **Prompt**:
   ```
   Create database schema for user authentication.

   Requirements:
   - Users table with id, email, password_hash
   - OAuth_tokens table with user_id, provider, tokens
   - Migrations using [framework]

   Success criteria:
   - Migration runs successfully
   - Tables created with correct schema
   - Indexes added for performance

   Write migrations to: migrations/001_auth_schema.sql
   ```

   **Verification**: Run migration, check tables exist
   **Next**: Task 2 (after verification passes)

   ## Phase 2: Parallel Execution
   [Similar format for parallel tasks]
   ```

4. **Create Checkpoint Plan**:

   ```markdown
   ## Checkpoint Strategy

   ### CP-001: After Tasks 1-2
   - Foundation complete
   - Safe rollback point
   ```bash
   git commit -m "Checkpoint 1: Foundation"
   git tag -a cp-001 -m "Schema and OAuth"
   ```

   ### CP-002: After Tasks 3-4
   - Core features complete
   - Integration point
   ```bash
   git commit -m "Checkpoint 2: Core"
   git tag -a cp-002 -m "API and Frontend"
   ```
   ```

5. **Generate Verification Summary**:

   Include verification report in final package:
   ```markdown
   ## Plan Quality Verification

   - Schema Validation: ✅ PASS
   - Quality Score: 94/100 ✅
   - Completeness: 95% ✅
   - All Quality Gates: ✅ PASS

   **Status**: APPROVED FOR EXECUTION
   ```

6. **Package Complete Plan**:

   Create plan package with all artifacts:
   ```
   plans/[plan-id]/
   ├── plan.json (machine-readable)
   ├── PLAN.md (human-readable)
   ├── COORDINATION.md (execution guide)
   ├── VERIFICATION.md (quality report)
   ├── dependencies.mermaid (visual graph)
   └── checkpoints/ (checkpoint data)
   ```

**Outputs**:
- plan.json (validated against schema)
- PLAN.md (human-readable version)
- COORDINATION.md (agent execution guide)
- VERIFICATION.md (quality assurance report)
- Visual dependency graph
- Complete plan package

**Validation**:
- [ ] plan.json validates against schema
- [ ] PLAN.md is comprehensive and clear
- [ ] COORDINATION.md provides clear agent instructions
- [ ] VERIFICATION.md shows quality ≥90
- [ ] All artifacts in plan package
- [ ] Ready for execution

**Time Estimate**: 20-30 minutes

**Result**: Production-ready plan, approved and ready for agent execution

---

## Post-Workflow: Plan Execution

After completing the 6-step workflow, you have a production-ready plan. Now execute it:

### Execution Pattern

**Using the Plan**:
1. Read COORDINATION.md for execution guidance
2. Follow tasks in dependency order
3. Execute parallel groups simultaneously where possible
4. Verify each task before proceeding
5. Create checkpoints at specified points
6. Update progress.json in real-time

**Task Execution Template**:
```typescript
// For each task in execution order:

// 1. Read task from plan.json
const task = plan.tasks.find(t => t.id === currentTaskId);

// 2. Check dependencies satisfied
const depsSatisfied = task.dependencies.every(dep =>
  plan.tasks.find(t => t.id === dep).status === 'complete'
);

// 3. If dependencies met, execute
if (depsSatisfied) {
  // Execute via Task tool or direct implementation
  const result = await executeTask(task);

  // 4. Verify
  const verified = await verifyTask(task);

  // 5. Update status
  task.status = verified ? 'complete' : 'failed';
  updateProgress(task);

  // 6. Create checkpoint if specified
  if (isCheckpointAfterTask(task.id)) {
    createCheckpoint(task.id);
  }
}
```

**Monitoring Progress**:
```bash
# Check current status
cat plans/[plan-id]/progress.json

# View execution log
cat plans/[plan-id]/execution-log.md

# See what's next
grep "pending" plans/[plan-id]/plan.json
```

---

## Integration with Multi-AI Research (Optional)

For enhanced planning with multi-perspective research:

### Step 1 Enhancement: Research Phase

**Instead of manual research**, use multi-ai-research:

```bash
# Invoke multi-ai-research skill
Use multi-ai-research for "Research [domain] implementation patterns and best practices"
```

This provides:
- **Claude research**: Official docs, codebase patterns
- **Gemini research**: Web best practices, latest trends
- **Codex research**: GitHub patterns, code examples
- **Cross-validated**: All findings verified across sources
- **Quality**: ≥95/100 with 100% citations

**Outputs**:
- `.analysis/ANALYSIS_FINAL.md` - Comprehensive research
- Patterns identified
- Best practices extracted
- Implementation recommendations

**Use in Planning**:
- Informs approach selection (Step 1)
- Guides task breakdown (Step 2)
- Suggests verification methods (Step 4)
- Improves plan quality

**Time Added**: +30-60 minutes
**Quality Improvement**: +5-10 points on plan quality score

---

## Best Practices

### 1. Research Before Planning (Step 1)
**Practice**: Invest time in research for unfamiliar domains

**Rationale**: Grounded plans based on proven patterns

### 2. Decompose to Atomic (Step 2)
**Practice**: Break down until tasks cannot be meaningfully subdivided

**Rationale**: Atomic tasks are executable and verifiable

### 3. Map Dependencies Explicitly (Step 3)
**Practice**: Document all dependencies, even obvious ones

**Rationale**: Prevents execution errors, enables parallelization

### 4. Verification Before Implementation (Step 4)
**Practice**: Define how to verify BEFORE defining how to implement

**Rationale**: Prevents ambiguity, enables test-driven development

### 5. Quality Threshold (Step 5)
**Practice**: Require ≥90 quality score before approval

**Rationale**: High-quality plans have higher execution success rates

### 6. Use Checkpoints (Execution)
**Practice**: Create checkpoints at major milestones

**Rationale**: Enables safe rollback and resumption

---

## Common Mistakes

### Mistake 1: Skipping Research
**Problem**: Plans based on assumptions, not proven patterns
**Fix**: Always research unfamiliar domains (use multi-ai-research)

### Mistake 2: Tasks Too Big
**Problem**: Tasks with >15 subtasks, vague descriptions
**Fix**: Decompose until 8-15 tasks per level, atomic at bottom

### Mistake 3: Missing Dependencies
**Problem**: Parallel execution fails due to undocumented dependencies
**Fix**: Explicitly map all dependencies, even obvious ones

### Mistake 4: Vague Success Criteria
**Problem**: "Feature works", "Looks good" - not measurable
**Fix**: SMART criteria - specific, measurable, testable

### Mistake 5: No Quality Verification
**Problem**: Executing low-quality plans leads to failures
**Fix**: Always score quality, require ≥90 before execution

### Mistake 6: Unsafe Rollback
**Problem**: Using git reset or destructive operations
**Fix**: Git tags + patch bundles, safe checkpoint procedures

---

## Quick Reference

### The 6-Step Planning Workflow

| Step | Purpose | Time | Key Output |
|------|---------|------|------------|
| 1 | Objective Analysis & Research | 30-120m | Approach, scope, research findings |
| 2 | Hierarchical Decomposition | 45-90m | Complete task tree |
| 3 | Dependency Mapping | 30-45m | Dependency graph, parallel groups |
| 4 | Verification Planning | 45-75m | Success criteria, verification methods |
| 5 | Quality Verification | 30-45m | Quality score (≥90), approval |
| 6 | Finalization | 20-30m | plan.json, PLAN.md, COORDINATION.md |

**Total Time**: 3.5-6.5 hours (varies by complexity)

### Plan Quality Rubric

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Excellent | ✅ Approve and execute |
| 80-89 | Good | ⚠️ Minor revisions recommended |
| 70-79 | Needs Work | ❌ Major revisions required |
| <70 | Poor | ❌ Re-plan from scratch |

### Task Granularity Guide

| Level | Subtasks | Example |
|-------|----------|---------|
| **Huge** | 15-25 | "Build complete authentication system" |
| **Large** | 8-15 | "Implement OAuth integration" |
| **Medium** | 3-8 | "Add token management" |
| **Small** | 1-3 | "Create token generation function" |
| **Atomic** | 1 | "Add userId to JWT payload" |

### Schemas

- **plan.schema.json**: Overall plan structure
- **task.schema.json**: Individual task definition
- **checkpoint.schema.json**: Checkpoint metadata

All plans must validate against schemas before execution.

---

**multi-ai-planning creates rigorous, agent-executable plans with hierarchical decomposition, dependency mapping, verification-first approach, and quality gates - ensuring reliable multi-agent execution.**

For detailed patterns, see references/. For examples, see examples/.
