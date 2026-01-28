---
name: intent-build-now
description: Start implementation from Intent. First validates Intent completeness, then launches idd-task-execution-master agent to plan and execute TDD-based development phases. Use when you have an Intent ready and want to start building.
---

# Intent Build Now

Start building from Intent with strict validation and TDD discipline.

## Workflow

```
/intent-build-now
       ↓
Locate Intent file
       ↓
Validate completeness ──→ Incomplete? ──→ Show gaps & how to fix
       ↓
Ready to build
       ↓
Launch idd-task-execution-master agent
       ↓
Phase-by-phase TDD execution
```

## Step 1: Locate Intent

Search for Intent file in order:
1. `intent/INTENT.md` (project root)
2. `INTENT.md` (current directory)
3. User-specified path

If not found, advise user to run `/intent-interview` first.

## Step 2: Validate Intent Completeness

### Required Sections

Check for these essential sections:

| Section | Purpose | How to Fix |
|---------|---------|------------|
| **Responsibilities** | What it does / doesn't do | Use `/intent-interview` to clarify scope |
| **Structure** | ASCII diagram of components | Add `## Structure` with ASCII diagram |
| **API** | Function signatures with params/returns | Define key interfaces in `## API` |

### Quality Checks

| Check | Criteria | If Missing |
|-------|----------|------------|
| **Clarity** | No ambiguous terms | Replace vague terms with specifics |
| **Testability** | Behaviors map to assertions | Add concrete examples with input → output |
| **Boundaries** | Clear scope limits | Add "What it doesn't do" list |
| **Dependencies** | External deps listed | Add `## Dependencies` section |

### Multi-Module Projects

For projects with multiple modules, also check:
- `intent/architecture/DEPENDENCIES.md` exists
- Module dependency graph is defined
- No circular dependencies

## Step 3: Report Readiness

### If Ready

```markdown
## Intent Validation: PASSED ✓

Your Intent is ready for implementation:
- ✓ Responsibilities defined
- ✓ Structure documented
- ✓ API signatures clear
- ✓ Examples provided

Launching idd-task-execution-master to plan phases...
```

Then use Task tool to launch `idd-task-execution-master` agent with the Intent content.

### If Not Ready

```markdown
## Intent Validation: NEEDS WORK

Your Intent is missing critical elements:

### Missing Sections

1. **Structure** - Add ASCII diagram showing component relationships
   ```
   ## Structure

   \```
   ComponentA ──→ ComponentB
        │
        ▼
   ComponentC
   \```
   ```

2. **API** - Define key function signatures
   ```
   ## API

   ### functionName(param1, param2)

   **Parameters:**
   - param1: type - description

   **Returns:** type - description
   ```

### Recommended Actions

1. Run `/intent-interview` to refine the Intent
2. Add missing sections manually
3. Run `/intent-build-now` again when ready

**Do not proceed with implementation until Intent is complete.**
```

## Step 4: Launch Execution

When Intent passes validation, use the Task tool:

```
Task: idd-task-execution-master

Prompt: "Here is the approved Intent for [project name].
Please create a phased execution plan following strict TDD:

[Full Intent content]

Requirements:
1. Break into logical phases
2. Each task: tests first, then implementation
3. Define completion criteria for each phase
4. Plan E2E verification gates"
```

## Integration

```
/intent-interview     # Create Intent from scratch
    ↓
/intent-critique      # Review for over-engineering
    ↓
/intent-review        # Section-by-section approval
    ↓
/intent-build-now     # THIS SKILL - Validate & start building
    ↓
[idd-task-execution-master plans phases]
    ↓
[idd-test-master designs tests]
    ↓
[idd-code-guru implements]
    ↓
[idd-e2e-test-queen validates]
    ↓
/intent-sync          # Sync confirmed details back
```

## Agent Coordination

This skill orchestrates the IDD agent team:

| Agent | Role | When Called |
|-------|------|-------------|
| `idd-task-execution-master` | Phase planning | After Intent validation passes |
| `idd-test-master` | Test design | Called by task-execution-master per task |
| `idd-code-guru` | Implementation | After tests are designed |
| `idd-e2e-test-queen` | E2E verification | After phase completion |

## Tips

1. **Don't rush validation** - An incomplete Intent leads to rework
2. **ASCII diagrams are mandatory** - They prevent misunderstandings
3. **Examples are tests** - Every example becomes a test case
4. **Boundaries prevent scope creep** - Be explicit about what's NOT included
