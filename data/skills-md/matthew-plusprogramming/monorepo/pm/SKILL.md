---
name: pm
description: Product manager skill for interviewing users to gather requirements, clarify ambiguities, refine iterations, and gather feedback on features. Use at the start of any task requiring a spec, or when gathering user feedback on implementations.
allowed-tools: Read, Write, Task, Glob
user-invocable: true
---

# Product Manager Skill

## Purpose

Orchestrate product discovery by dispatching the product-manager subagent to conduct interviews, gather requirements, and produce structured outputs.

**Key Output**: Creates a spec group with `requirements.md` that feeds into `/spec` and `/atomize`.

## Usage

```
/pm                           # Start new discovery interview, create spec group
/pm <spec-group-id>           # Add requirements to existing spec group
/pm feedback <spec-group-id>  # Gather feedback on implementation
/pm refine <spec-group-id>    # Refine existing requirements based on new info
```

## When to Use This Skill

- **Initial discovery**: Starting a new task that needs a spec (creates spec group)
- **Clarification**: User request is vague or has multiple interpretations
- **Refinement**: Spec group exists but has open questions or ambiguities
- **Feedback collection**: Implementation complete, gathering user reactions
- **Iteration planning**: Deciding what to build next or how to improve existing features

## Process

### 1. Parse Invocation

Determine the mode from the command:

| Command                  | Mode        | Context                           |
| ------------------------ | ----------- | --------------------------------- |
| `/pm`                    | `discovery` | New spec group will be created    |
| `/pm sg-logout`          | `discovery` | Add to existing spec group        |
| `/pm feedback sg-logout` | `feedback`  | Gather feedback on implementation |
| `/pm refine sg-logout`   | `refine`    | Refine existing requirements      |

### 2. Load Context (if spec group exists)

For modes that reference an existing spec group:

```
Read: .claude/specs/groups/<spec-group-id>/manifest.json
Read: .claude/specs/groups/<spec-group-id>/requirements.md (if exists)
```

### 3. Dispatch Product Manager Subagent

Dispatch the product-manager subagent with appropriate context:

#### Discovery Mode (new)

```
Task: product-manager
Prompt: |
  <context>
  Mode: discovery
  User request: <original user request>
  </context>

  Conduct a discovery interview to gather requirements for a new feature.

  Interview the user to understand:
  - Problem being solved
  - Goals and success criteria
  - Constraints and boundaries
  - Edge cases and failure modes
  - Priorities (must-have vs nice-to-have)

  After interviewing, create a spec group directory and requirements.md:
  - Directory: .claude/specs/groups/sg-<feature-slug>/
  - Create manifest.json with review_state: DRAFT
  - Create requirements.md with all gathered requirements in EARS format

  Confirm understanding with user before finalizing.
```

#### Discovery Mode (existing spec group)

```
Task: product-manager
Prompt: |
  <context>
  Mode: discovery
  Spec group: <spec-group-id>
  Existing manifest: <manifest contents>
  Existing requirements: <requirements.md contents if exists>
  User request: <original user request>
  </context>

  Add requirements to existing spec group.

  Interview the user to understand additional requirements.
  Update requirements.md with new requirements.
  Maintain existing requirements unless explicitly superseded.

  Confirm understanding with user before finalizing.
```

#### Feedback Mode

```
Task: product-manager
Prompt: |
  <context>
  Mode: feedback
  Spec group: <spec-group-id>
  Existing requirements: <requirements.md contents>
  Implementation status: <from manifest>
  </context>

  Gather feedback on the implementation.

  Interview the user to understand:
  - What's working well
  - What needs improvement
  - What's missing
  - What should be built next

  Produce an iteration plan documenting:
  - Feedback summary
  - Proposed changes
  - Next steps

  Update requirements.md with feedback notes.
```

#### Refine Mode

```
Task: product-manager
Prompt: |
  <context>
  Mode: refine
  Spec group: <spec-group-id>
  Existing requirements: <requirements.md contents>
  Open questions: <extracted from requirements.md>
  </context>

  Refine existing requirements based on new information.

  Interview the user to:
  - Resolve open questions
  - Clarify ambiguities
  - Update priorities if needed

  Update requirements.md with refined requirements.
  Mark resolved questions as resolved with answers.
```

### 4. Synthesize Results

After subagent completes, report the outcome:

#### Discovery Complete

```markdown
## Requirements Gathered ✅

Spec group created: `sg-<feature-slug>`
Location: `.claude/specs/groups/sg-<feature-slug>/`

Files created:

- `manifest.json` — Spec group metadata (review_state: DRAFT)
- `requirements.md` — <N> requirements in EARS format

**Next Steps**:

1. Review requirements: `cat .claude/specs/groups/sg-<feature-slug>/requirements.md`
2. (Optional) Run `/prd draft sg-<feature-slug>` to write PRD to Google Docs
3. Run `/spec sg-<feature-slug>` to create spec.md
4. Run `/atomize sg-<feature-slug>` to decompose into atomic specs
5. Run `/enforce sg-<feature-slug>` to validate atomicity
6. User approves → implementation begins
```

#### Feedback Complete

```markdown
## Feedback Gathered ✅

Spec group: `<spec-group-id>`

**Feedback Summary**:

- Working well: <count> items
- Needs improvement: <count> items
- Missing: <count> items

Iteration plan added to requirements.md

**Next Steps**:

1. Review iteration plan
2. Run `/spec <spec-group-id>` to update spec with changes
3. Re-implement changed requirements
```

#### Refine Complete

```markdown
## Requirements Refined ✅

Spec group: `<spec-group-id>`

**Resolved**:

- <count> open questions resolved
- <count> requirements clarified

**Next Steps**:

1. Review updated requirements.md
2. Continue with `/spec` or `/atomize`
```

## State Transitions

After `/pm` completes:

| Mode                 | review_state | work_state | updated_by |
| -------------------- | ------------ | ---------- | ---------- |
| discovery (new)      | DRAFT        | PLAN_READY | agent      |
| discovery (existing) | DRAFT        | PLAN_READY | agent      |
| feedback             | DRAFT        | PLAN_READY | agent      |
| refine               | DRAFT        | PLAN_READY | agent      |

## Integration with Workflow

### In oneoff-spec Workflow

```
/route → /pm → requirements.md
              ↓
         /spec → spec.md
              ↓
         /atomize → atomic/*.md
              ↓
         /enforce → validation
```

### Linking to External PRD

After `/pm`, if requirements should link to a Google Doc PRD:

```
/prd link sg-<feature-slug> <google-doc-id>
```

## Error Handling

### Spec Group Not Found

```
Error: Spec group 'sg-unknown' not found

Available spec groups:
  - sg-logout-button
  - sg-auth-system

To create a new spec group, run:
  /pm
```

### Invalid Mode

```
Error: Invalid mode 'invalid'

Valid modes:
  - /pm                    (new discovery)
  - /pm <spec-group-id>    (add to existing)
  - /pm feedback <sg-id>   (gather feedback)
  - /pm refine <sg-id>     (refine requirements)
```

## Examples

### Example 1: New Discovery

```
User: /pm

→ Dispatch product-manager (discovery mode)
→ Subagent interviews user about the problem
→ Subagent creates sg-logout-button/ with manifest.json and requirements.md
→ Report: Requirements Gathered ✅
```

### Example 2: Add to Existing

```
User: /pm sg-auth-system

→ Load existing manifest and requirements
→ Dispatch product-manager (discovery mode with context)
→ Subagent interviews for additional requirements
→ Subagent updates requirements.md
→ Report: Requirements Updated ✅
```

### Example 3: Feedback Collection

```
User: /pm feedback sg-logout-button

→ Load existing manifest and requirements
→ Dispatch product-manager (feedback mode)
→ Subagent interviews about implementation
→ Subagent produces iteration plan
→ Report: Feedback Gathered ✅
```

### Example 4: Refine Requirements

```
User: /pm refine sg-auth-system

→ Load existing requirements and open questions
→ Dispatch product-manager (refine mode)
→ Subagent interviews to resolve questions
→ Subagent updates requirements.md
→ Report: Requirements Refined ✅
```
