---
name: forge-create-issue
description: Collaboratively plan and create well-structured GitHub issues through interactive discussion. Use when the user wants to create a GitHub issue, plan a feature, report a bug, or scope out work for implementation.
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Glob, WebSearch
---

# Create GitHub Issue

Collaboratively plan and create well-structured GitHub issues through interactive discussion.

## Input

The issue idea or problem description will be provided as: $ARGUMENTS

If no argument is provided, ask the user what they'd like to create an issue for.

## Process

### Step 1: Understand the Request

Parse the user's input to understand:
- What problem they're trying to solve
- What outcome they expect
- Any constraints or preferences mentioned

**Do NOT assume** you understand the full scope. Always ask clarifying questions.

### Step 2: Explore and Clarify

Use AskUserQuestion to gather information:

1. **Problem Context**
   - What triggered this need?
   - Who is affected (users, developers, ops)?
   - What's the current behavior vs. desired behavior?

2. **Success Criteria**
   - How will we know this is done?
   - Are there measurable outcomes?
   - What does "good enough" look like?

3. **Constraints & Dependencies**
   - Timeline considerations?
   - Technical constraints?
   - Dependencies on other work?

### Step 3: Research the Codebase

Before proposing solutions, explore the relevant parts of the codebase:
- Find related existing code
- Understand current patterns and conventions
- Identify potential integration points
- Look for similar past implementations

- **Verify external dependencies**: If the issue involves external services, APIs, or third-party tools, run a quick smoke test to confirm they're accessible and working. Flag any issues to the user before proceeding to solution design — building on broken dependencies wastes entire sessions.

Use this research to inform realistic implementation options.

### Step 4: Generate Alternative Approaches

**CRITICAL: Never present just one approach.** Always research and present 2-4 different ways to solve the problem:

For each approach, describe:
- **Summary**: One-line description
- **How it works**: Brief technical explanation
- **Pros**: Benefits of this approach
- **Cons**: Drawbacks or risks
- **Effort estimate**: Relative complexity (Low/Medium/High)
- **Files likely affected**: Key areas of the codebase

Present these options to the user and discuss trade-offs. Let them choose or combine approaches.

### Step 5: Assess Scope

Evaluate if this should be one issue or multiple:

**Signs it should be split:**
- Multiple distinct deliverables
- Different areas of the codebase with no overlap
- Work that could be done in parallel by different people
- Natural breaking points (e.g., "backend then frontend")
- Estimated effort exceeds 1-2 days of work

**Signs it should stay as one issue:**
- Tightly coupled changes
- Single logical unit of work
- Splitting would create coordination overhead
- Small enough to complete in a focused session

**If splitting makes sense, offer options:**
1. **Single issue**: Keep as-is, note it's larger
2. **Multiple issues**: Create separate, linked issues
3. **Epic with sub-issues**: Create a parent tracking issue with child tasks

Ask the user which structure they prefer and why.

### Step 6: Draft the Issue

**Issue titles MUST use conventional commit format:**
```
<type>(<scope>): <description>
```

**Types:**
- `feat` - New feature or capability
- `fix` - Bug fix
- `docs` - Documentation only
- `refactor` - Code restructuring without behavior change
- `test` - Adding or updating tests
- `chore` - Maintenance, dependencies, tooling
- `perf` - Performance improvement

**Scope** is optional but recommended - use the affected area (e.g., `auth`, `templates`, `api`, `frontend`).

**Labels - Apply appropriate labels to categorize the issue:**

| Category | Labels | When to Use |
|----------|--------|-------------|
| **Type** | `bug`, `feature`, `enhancement`, `refactor`, `performance`, `security`, `testing`, `documentation` | Every issue should have exactly one type label |
| **Area** | `area: backend`, `area: frontend`, or project-specific areas | Apply all areas the issue touches |
| **Workflow** | `epic`, `discovery`, `blocked`, `good first issue` | Use when applicable |
| **Priority** | `priority: high`, `priority: low` | Optional - use for triage |

**Label Selection Guidelines:**
- **Type label**: Match the conventional commit type (feat→feature, fix→bug, etc.)
- **Area labels**: Can apply multiple if issue spans areas (e.g., `area: backend` + `area: frontend`)
- **Discovery**: For research/spike work before implementation is clear
- **Epic**: For parent issues that track multiple sub-issues

**Examples:**
- `feat(auth): Add OAuth2 login with Google`
- `fix(templates): Resolve SVG conversion timeout on large files`
- `refactor(api): Migrate endpoints to new router structure`
- `docs: Update API reference for v2 endpoints`

Create a well-structured issue with these sections:

```markdown
## Summary
[1-2 sentence description of what this issue accomplishes]

## Problem / Motivation
[Why does this need to exist? What problem does it solve? Who benefits?]

## Proposed Solution
[Description of the chosen approach]

### Implementation Details
[Technical details, affected files, key considerations]

### Alternatives Considered
[Brief mention of other approaches and why they weren't chosen]

### Implementation Constraints
[Include when the issue involves choices between libraries, APIs, configuration approaches, or non-obvious patterns]
- Preferred libraries or tools: <what to use and what to avoid>
- Configuration location: <where settings should live>
- Patterns to follow: <reference existing patterns in the codebase>
- External dependencies: <services or APIs required, and how to verify they work>

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]
- [ ] Tests added/updated
- [ ] Documentation updated (if applicable)

## Additional Context
[Any other relevant information, links, screenshots, etc.]
```

### Step 7: Review with User

Present the draft issue to the user:
- Read through the full issue
- Ask if anything is missing or incorrect
- Offer to adjust scope, add details, or restructure

Iterate until the user is satisfied.

### Step 8: Create the Issue

```bash
# Create the issue with conventional commit title format and appropriate labels
gh issue create \
  --title "<type>(<scope>): <description>" \
  --body "$(cat <<'EOF'
<issue body from Step 6>
EOF
)" \
  --label "<type-label>" \
  --label "<area-label>"

# Examples:
# gh issue create --title "feat(auth): Add password reset flow" \
#   --label "feature" --label "area: backend" ...

# gh issue create --title "fix(templates): Handle empty prompt gracefully" \
#   --label "bug" --label "area: backend" ...

# gh issue create --title "perf(frontend): Add session caching" \
#   --label "performance" --label "area: frontend" ...

# gh issue create --title "feat(payments): Add annual billing" \
#   --label "feature" --label "area: payments" --label "area: frontend" ...
```

**Creating Epics with Sub-Issues:**

When creating an epic with sub-issues, use GitHub's built-in sub-issue feature for automatic linking:

```bash
# 1. Create the parent issue first with epic label
gh issue create \
  --title "feat(frontend): Add dark mode support" \
  --body "$(cat <<'EOF'
## Summary
Add dark mode support to the frontend application.

## Problem / Motivation
Users have requested dark mode for comfortable evening use.

## Acceptance Criteria
- [ ] Users can toggle between light and dark mode
- [ ] Preference persists across sessions
EOF
)" \
  --label "epic" \
  --label "feature" \
  --label "area: frontend"

# Note the parent issue number (e.g., #200)

# 2. Create sub-issues using --parent flag to link automatically
gh issue create \
  --title "feat(frontend): Add theme context and toggle component" \
  --body "Sub-task for dark mode implementation." \
  --label "feature" \
  --label "area: frontend" \
  --parent 200

gh issue create \
  --title "feat(ui): Update core UI components with dark variants" \
  --body "Sub-task for dark mode implementation." \
  --label "feature" \
  --label "area: frontend" \
  --parent 200

# Sub-issues are automatically linked in the parent's task list
```

**Benefits of using `--parent`:**
- Automatic bidirectional linking between parent and children
- Progress tracking visible on parent issue
- No need to manually update issue bodies with links

### Step 9: Confirm and Share

After creation:
- Share the issue URL with the user
- If multiple issues were created, list all of them
- Offer to assign the issue or add it to a project/milestone
- Suggest using `forge-implement-issue` to start implementation

## Guidelines

### Interaction Style

- **Be curious**: Ask "why" and "what if" questions
- **Challenge assumptions**: If something seems unclear, dig deeper
- **Offer perspective**: Share what you've seen work well in similar situations
- **Stay collaborative**: This is a dialogue, not a form to fill out

### Quality Checks

Before finalizing, verify:
- [ ] **Title uses conventional commit format** (`<type>(<scope>): <description>`)
- [ ] **Labels applied**: At least one type label + relevant area label(s)
- [ ] Problem is clearly articulated
- [ ] Solution approach is justified
- [ ] Acceptance criteria are testable
- [ ] Scope is appropriate (not too big, not too small)
- [ ] Implementation path is realistic
- [ ] No critical details are missing

### What NOT to Do

- Don't create the issue without user confirmation
- Don't assume technical approach without exploring options
- Don't skip the alternatives analysis
- Don't add attribution lines (Co-Authored-By, etc.)
- Don't include time estimates (per project guidelines)
- Don't create overly detailed implementation specs (leave room for implementer judgment)

## Examples

### Example Dialogue Flow

**User**: "We need email notifications for order updates"

**Assistant**: "Email notifications — great for keeping users informed. Before we scope this out, help me understand:

1. Which order events should trigger emails (placed, shipped, delivered, cancelled)?
2. Do we need to support email preferences (opt-in/opt-out per event type)?
3. Is there an existing email service or should we evaluate options?

Also, let me check how notifications are currently handled in the codebase..."

[After research and discussion]

**Assistant**: "Based on our discussion, I see three approaches:

**Option A: Transactional email service (SendGrid, Postmark)**
- Use a dedicated transactional email API
- Template management in the service
- Pros: Reliable delivery, analytics, easy templates
- Cons: External dependency, cost per email

**Option B: Self-hosted SMTP**
- Send via SMTP using nodemailer or similar
- Templates stored in the codebase
- Pros: Full control, no vendor lock-in
- Cons: Deliverability challenges, needs monitoring

**Option C: Event-driven with queue**
- Publish order events to a queue, consume asynchronously
- Decouple email sending from order processing
- Pros: Resilient, scalable, supports future notification channels
- Cons: More infrastructure, higher complexity

Given the project's current scale, Option A is the simplest starting point. What's your preference?"

### Example Issue Structure (Epic)

**Title:** `feat(notifications): Add email notifications for order updates`

```markdown
## Summary
Send email notifications to users when their order status changes.

## Problem / Motivation
Users currently have no way to know when their order ships or gets delivered without manually checking. Email notifications improve the user experience and reduce support inquiries.

## Proposed Solution
Integrate a transactional email service to send templated emails on key order events (placed, shipped, delivered).

## Acceptance Criteria
- [ ] Users receive email when order is placed
- [ ] Users receive email when order ships with tracking info
- [ ] Users can opt out of email notifications
- [ ] Emails render correctly across major email clients
```

**Note:** Sub-issues are created separately using `gh issue create --parent <ISSUE_NUMBER>` and will be automatically linked by GitHub. No need to manually list them in the body.

## Related Skills

**Before:** Use `forge-setup-project` to set up the project meta-structure (CLAUDE.md, docs/, etc.).
**Next step:** Use `forge-implement-issue` to implement the issue you just created.
**Full workflow:** `forge-setup-project` → `forge-create-issue` → `forge-implement-issue` → `forge-reflect-pr` → `forge-address-pr-feedback` → `forge-update-changelog`
