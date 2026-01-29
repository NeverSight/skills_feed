---
name: plan-refiner
description: Generate and iteratively refine implementation plans from an initial spec/prompt. Takes a specification as input, generates an initial plan, then refines it through multiple review passes (minimum 3) with fresh agent context. User can continue beyond 3 passes until satisfied. Use when turning requirements into polished implementation plans.
license: MIT
metadata:
  author: dreambound
  version: "1.0.0"
---

# Plan Refiner Skill

This skill implements an iterative plan refinement process that transforms an initial specification into a polished implementation plan through multiple review passes with fresh agent perspective.

## Workflow Overview

```
Input: initial_spec.md (starting prompt/requirements)
         ↓
Step 1: Generate Initial Plan (plan.md v0)
         ↓
Step 2: Review Loop (minimum 3 passes)
  - Spawn fresh review agent with spec + clarifications + plan
  - Agent provides feedback + identifies critical assumptions
  - Agent verifies versions/APIs against live docs via Context7
  - Surface identified issues and assumptions to user
  - Prompt user for optional additional feedback
  - Apply all feedback to plan
  - After pass 3+, ask user to continue or finalize
         ↓
Output: Final plan.md + clarifications.md + audit trail
```

**Note:** Review agents use Context7 (`mcp__context7__resolve-library-id` → `mcp__context7__query-docs`) to verify that any package versions, GitHub Actions, APIs, or framework versions mentioned in the plan are current. This prevents recommending outdated versions based on training data.

**Fallback:** If Context7 MCP tools are unavailable, install the [context7 skill](https://skills.sh/intellectronica/agent-skills/context7) which provides equivalent functionality via HTTP API.

## Input Requirements

The user must provide an initial specification or prompt. This can be:
- A file path to an existing spec document
- Text content to save as `initial_spec.md`
- A description of what they want to plan

## Working Directory Structure

Create a namespaced directory under Claude's plan directory:

```
~/.claude/plans/plan-refiner/{spec-slug}/
├── initial_spec.md           # The starting requirements (immutable)
├── plan.md                   # Current plan (updated each pass)
├── clarifications.md         # Accumulated Q&A and user feedback
├── config.json               # Run configuration (includes custom_reviewer settings)
├── audit/
│   ├── plan_v0.md            # Initial plan from spec
│   ├── plan_v1.md            # After pass 1
│   ├── plan_v2.md            # After pass 2
│   └── plan_v3.md            # After pass 3, etc.
├── pass_N_feedback.md        # Default review feedback for each pass
└── pass_N_custom_feedback.md # Custom review feedback (if custom reviewer enabled)
```

### Global Preferences

```
~/.claude/plans/plan-refiner/
└── preferences.json          # Global preferences across all runs
```

**Spec Slug Generation:**
- From file path: Use filename without extension (e.g., `my-feature.md` → `my-feature`)
- From content: Slugify first heading or first line (e.g., "Auth Feature Spec" → `auth-feature-spec`)
- Add timestamp suffix if directory exists: `my-feature-20260128`

## Context Preservation Strategy

To preserve orchestrator context across multiple passes, this skill uses **file-based delegation**:

1. **Subagents read from files** - Don't embed full content in prompts; tell subagents which files to read
2. **Subagents write to files** - Feedback and plan updates go directly to disk
3. **Summaries only returned** - Subagents return brief summaries, not full content
4. **Orchestrator stays thin** - Main agent manages paths and workflow, not content

### Drift Mitigation: Spec-Always-Included

To prevent drift from the original specification:
- **All subagents always re-read `initial_spec.md`** before performing their task
- **Review agents explicitly check spec alignment** and flag drift in their feedback
- **Update agents verify changes align with spec** before writing
- **Summaries include alignment status** (e.g., "Aligned" or "Warning: divergence detected")

## Startup Configuration

Before beginning refinement, ask about optional custom review.

### Startup Questions

**Question 1: Custom Reviewer**

Check for `~/.claude/plans/plan-refiner/preferences.json`:

If `preferences.json` exists and has a previous `custom_reviewer`:
- Ask: "Last time you used '{skill-name}' as additional reviewer. Use it again?"
- Options: Yes / No / Different skill

Otherwise:
- Ask: "Add a custom review agent for specialized feedback? (e.g., security, performance)"
- Options: No (default only) / Yes, specify skill

**Question 2: Skill Specification** (if yes to custom reviewer)

Ask: "Specify the custom review skill:"
- Skill name (e.g., 'security-reviewer')
- Skill path (absolute path)
- Skip (use default only)

Also ask for the focus description (e.g., "security considerations", "performance optimization", "accessibility compliance").

### Preferences Persistence

Store in `~/.claude/plans/plan-refiner/preferences.json`:

```json
{
  "custom_reviewer": {
    "enabled": true,
    "type": "skill_name",
    "value": "security-reviewer",
    "focus": "security considerations"
  },
  "custom_reviewer_history": ["security-reviewer", "performance-reviewer"],
  "updated_at": "2026-01-28T..."
}
```

- `custom_reviewer`: Current configuration (or null if disabled)
- `custom_reviewer_history`: Previously used skills (for suggestions)
- `updated_at`: Last modification timestamp

---

## Execution Steps

### Step 1: Setup and Initial Plan Generation

1. **Generate spec slug** from input (filename or content title)
2. **Create namespaced directory** at `~/.claude/plans/plan-refiner/{spec-slug}/`
   - If directory exists, append timestamp suffix (e.g., `-20260128`)
3. **Save or verify initial_spec.md** from user input
4. **Create clarifications.md** (empty initially)
5. **Create audit/ directory**
6. **Create config.json** with run configuration:
   ```json
   {
     "created_at": "2026-01-28T...",
     "custom_reviewer": {
       "enabled": true,
       "type": "skill_name",
       "value": "security-reviewer",
       "focus": "security considerations"
     },
     "current_pass": 0,
     "status": "in_progress"
   }
   ```
   - Set `custom_reviewer` to null if not configured
7. **Spawn Plan Generation Agent** to create initial plan:
   - Use Task tool with `subagent_type: general-purpose`
   - Provide file paths (not contents): `initial_spec.md`, `plan.md`, `audit/plan_v0.md`
   - Agent reads spec, writes plan to both locations
   - Agent returns: brief summary of plan structure (not full content)
   - See `references/generation-prompt.md` for the prompt template

### Step 2: Review Loop (Minimum 3 Passes)

For each pass (1, 2, 3, ...):

#### 2a. Spawn Default Review Agent

Use the Task tool with `subagent_type: general-purpose` to create a fresh agent context.

**Important:** Do NOT use `subagent_type: Plan` as it triggers plan mode behavior and will prompt to execute instead of returning feedback.

**Prompt the agent with file paths, not contents:**
- Path to `initial_spec.md` (agent reads it - source of truth)
- Path to `clarifications.md` (agent reads it)
- Path to `plan.md` (agent reads it)
- Current pass number
- Path to write feedback: `pass_N_feedback.md`
- Review instructions from `references/review-prompt.md`

**Agent responsibilities:**
1. Read all input files (always starting with spec)
2. Verify plan alignment with original spec
3. Perform review
4. Write detailed feedback to `pass_N_feedback.md`
5. Return ONLY: alignment status + summary of issues + critical assumption questions

#### 2a-bis. Spawn Custom Review Agent (if configured)

If `config.json` has `custom_reviewer.enabled: true`:

1. **Spawn Custom Review Sub-Agent** via Task tool:
   - `subagent_type: general-purpose`
   - Provide file paths:
     - Spec path: `initial_spec.md`
     - Plan path: `plan.md`
     - Default feedback path: `pass_N_feedback.md`
   - Output path: `pass_N_custom_feedback.md`
   - Use prompt template from `references/custom-review-prompt.md`
   - Inject the custom focus from config (e.g., "security considerations")

2. **Process Custom Review Summary**:
   - Custom agent returns: focus area + additional issue count + additional questions + assessment
   - Additional issues are written to `pass_N_custom_feedback.md`

3. **Merge Feedback for Processing**:
   - Default feedback: `pass_N_feedback.md`
   - Custom feedback: `pass_N_custom_feedback.md`
   - Both files remain separate for audit purposes
   - Combined questions from both reviews are surfaced to user in step 2c
   - Update total issue count in summaries

**If custom reviewer skill not found:** Log warning and continue with default review only.

#### 2b. Process Agent Summary

The review agent returns a brief summary (not full feedback):
1. **Alignment Status**: "Aligned" or "Warning: [drift description]"
2. **Issue Count**: Number of issues found
3. **Critical Assumptions**: Questions requiring user input

Full feedback is already saved to `pass_N_feedback.md` by the agent.

**If alignment warning received:** Surface to user via AskUserQuestion before proceeding.

#### 2b-bis. Surface Issues to User

After processing the agent summary, read feedback file(s) and display identified issues:

1. **Read feedback files**:
   - Read `pass_N_feedback.md` for default review issues
   - If custom reviewer enabled, also read `pass_N_custom_feedback.md`

2. **Extract issues** from the "Plan Feedback" section:
   - Parse each `### Issue N:` block (or `#### Issue N:` for custom feedback)
   - Extract: title, location, problem, suggestion

3. **Display issues to the user** before asking questions:

```
## Pass {N} Review Findings

### Issues Identified ({count} total)

**Issue 1: {title}**
- Location: {location}
- Problem: {description}
- Suggestion: {recommendation}

**Issue 2: {title}**
...

[If custom reviewer enabled:]
### Additional Issues from {custom_focus} Review ({count})

**Issue 1: {title}**
...
```

If no issues found, display: "No issues identified in this pass."

#### 2c. Surface Questions to User

If the agent identified critical assumptions:
- Use AskUserQuestion to present each question
- Append user answers to `clarifications.md` with format:

```markdown
## Pass N Clarifications

**Q: [Question from agent]**
A: [User's answer]
```

#### 2d. Prompt for Additional User Feedback

After answering questions, ask the user:
"Do you have any additional feedback on the current plan? (You can skip this)"

If user provides feedback:
- Append to `clarifications.md`:

```markdown
### User Feedback (Pass N)
[User's feedback]
```

#### 2e. Apply Feedback via Subagent

Spawn a **Plan Update Agent** (`subagent_type: general-purpose`):

**Provide file paths:**
- Path to `initial_spec.md` (source of truth)
- Path to `plan.md` (current version)
- Path to `pass_N_feedback.md` (agent feedback)
- Path to `clarifications.md` (includes user answers)
- Path to write: `audit/plan_v{pass}.md` (backup) and updated `plan.md`
- Update instructions from `references/update-prompt.md`

**Agent responsibilities:**
1. Read spec, current plan, feedback, and clarifications
2. Verify changes align with original spec
3. Incorporate all feedback and user clarifications
4. Write updated plan to `plan.md`
5. Copy to `audit/plan_v{pass}.md`
6. Return ONLY: alignment status + 2-3 sentence summary of changes

**If alignment warning received:** Surface to user via AskUserQuestion:
"The update agent detected potential drift: [warning]. Continue with changes or revert?"

#### 2f. Continuation Check (After Pass 3+)

After pass 3 and each subsequent pass, ask the user:
"Would you like to continue refining the plan, or is it ready?"

Options:
- **Continue**: Proceed to next pass
- **Finalize**: Exit loop with current plan

### Step 3: Finalization

Present the user with:
- Final `plan.md` location
- Summary of changes across all passes
- Location of audit trail

## Subagent Prompt Templates

See the following templates in `references/`:
- `generation-prompt.md` - Initial plan generation agent
- `review-prompt.md` - Default review agents for each pass
- `custom-review-prompt.md` - Custom review agents (supplementary, specialized feedback)
- `update-prompt.md` - Plan update agent after feedback

## Pass Focus Areas

Each pass has a primary focus while still reviewing the full plan:

| Pass | Primary Focus |
|------|---------------|
| 1 | Alignment with spec, surface major assumptions |
| 2 | Completeness and feasibility, clarify remaining gaps, **version verification via Context7** |
| 3+ | Final polish, coherence, edge cases |

## Example Invocation

User: "Run /plan-refiner on my feature spec"

1. Agent asks for spec location or content
2. Agent generates spec slug (e.g., `my-feature` from `my-feature.md`)
3. Agent creates directory at `~/.claude/plans/plan-refiner/my-feature/` and saves spec
4. Agent generates initial plan (v0)
5. Agent runs 3 review passes with fresh context
6. After pass 3, agent asks to continue or finalize
7. Agent presents final plan location and audit trail

## Key Principles

1. **Fresh Perspective**: Each review pass uses a new agent with no accumulated context bias
2. **User in the Loop**: Critical assumptions require user clarification before proceeding
3. **Audit Trail**: Every plan version is preserved for reference
4. **Accumulated Context**: Clarifications (Q&A + feedback) persist across all passes
5. **Flexible Iteration**: Minimum 3 passes, but user controls when to stop
