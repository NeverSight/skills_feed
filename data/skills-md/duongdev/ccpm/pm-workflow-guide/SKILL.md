---
name: pm-workflow-guide
description: Provides intelligent context-aware PM workflow guidance with automatic phase detection. Prioritizes 6 natural workflow commands (plan, work, sync, commit, verify, done) for streamlined project management. Auto-activates when user mentions planning, implementation, verification, spec management, or asks "what command should I use". Detects workflow phase and suggests optimal command path. Provides learning mode for new users. Prevents common mistakes and offers error prevention. Works with pm-workflow state machine (IDEA → PLANNED → IMPLEMENTING → VERIFYING → VERIFIED → COMPLETE).
---

# PM Workflow Guide

This skill helps you navigate CCPM's 49+ commands by automatically detecting your current workflow phase and suggesting the most appropriate commands.

## Natural Workflow Commands (RECOMMENDED)

**Start here!** CCPM provides 6 simple, chainable commands that cover the complete workflow:

### Quick Reference Card

```
Planning      → /ccpm:plan "title"              Create & plan a new task
Working       → /ccpm:work                       Start/resume implementation
Progressing   → /ccpm:sync "summary"             Save progress to Linear
Committing    → /ccpm:commit                     Create git commit (conventional)
Verifying     → /ccpm:verify                     Run quality checks
Finalizing    → /ccpm:done                       Create PR & finalize
```

### Complete Workflow Examples

**Example 1: New feature from scratch**
```
/ccpm:plan "Add two-factor authentication" my-app
/ccpm:work                                # Start implementation
/ccpm:sync "Implemented authenticator logic"
/ccpm:commit                              # Auto-formats: feat(auth): implement 2FA
/ccpm:verify                              # Run tests, linting, build
/ccpm:done                                # Create PR and finalize
```

**Example 2: Fixing a bug**
```
/ccpm:plan BUG-456                        # Plan existing bug ticket
/ccpm:work                                # Resume where you left off
/ccpm:sync "Fixed race condition"
/ccpm:commit                              # Auto-formats: fix(cache): prevent race condition
/ccpm:verify                              # Ensure fix doesn't break tests
/ccpm:done                                # Ship the fix
```

**Example 3: Documentation update**
```
/ccpm:plan "Update API documentation" my-app
/ccpm:work
/ccpm:sync "Added deployment guide"
/ccpm:commit                              # Auto-formats: docs(api): add deployment guide
/ccpm:verify
/ccpm:done
```

### Command Details

1. **`/ccpm:plan`** - Smart planning
   - Create new task: `/ccpm:plan "title" <project>`
   - Plan existing issue: `/ccpm:plan <issue-id>`
   - Update plan: `/ccpm:plan <issue-id> "changes"`

2. **`/ccpm:work`** - Smart work
   - Auto-detects: Not started → start, In progress → resume
   - Auto-detects issue from git branch name

3. **`/ccpm:sync`** - Save progress
   - Auto-detects issue from git branch
   - Shows git changes summary
   - Updates Linear with findings

4. **`/ccpm:commit`** - Git integration
   - Conventional commits format (feat/fix/docs/refactor/etc)
   - Links commits to Linear issues automatically
   - Example: `fix(auth): handle token expiration`

5. **`/ccpm:verify`** - Quality checks
   - Auto-detects issue from branch
   - Runs tests, linting, build checks sequentially
   - Fails fast if checks don't pass

6. **`/ccpm:done`** - Finalize
   - Pre-flight safety checks
   - Creates PR with auto-generated description
   - Syncs Linear status to Jira
   - Requires confirmation for external writes (safety)

### When to Use Project Configuration Commands

The 6 natural commands cover 90% of workflows. Use project configuration commands for:
- **Project setup**: `/ccpm:project:add` (add new project)
- **Project management**: `/ccpm:project:list`, `/ccpm:project:show` (view projects)
- **Project switching**: `/ccpm:project:set` (switch active project)
- **Design refresh**: `/ccpm:figma-refresh` (refresh Figma design cache)

## Instructions

### Automatic Phase Detection

This skill activates when user mentions workflow-related keywords and provides context-aware command suggestions.

### Planning Phase

**Trigger phrases**:
- "plan this task"
- "create new task/epic/feature"
- "write a spec"
- "gather requirements"
- "need to understand..."
- "starting a new project"

**Recommended commands**:

1. **Natural command** → `/ccpm:plan "Task title" <project>`
   - Simple, chainable planning
   - Creates Linear issue
   - Gathers context from Jira/Confluence/Slack
   - Analyzes codebase
   - Generates comprehensive plan

2. **Plan existing issue** → `/ccpm:plan <issue-id>`
   - Plans an existing Linear issue
   - Gathers context and generates checklist
   - Use when issue already exists

3. **Update existing plan** → `/ccpm:plan <issue-id> "changes"`
   - Requirements changed during implementation
   - Interactive clarification
   - Impact analysis
   - Updates plan with changes

**Example conversation**:
```
User: "I need to plan the new user authentication feature"

Claude: [pm-workflow-guide activates]

I'll help you plan this. Here's what to use:

1. NEW TASK → /ccpm:plan "User authentication" my-app
2. EXISTING ISSUE → /ccpm:plan <issue-id>
3. QUICK INTERNAL → /ccpm:plan "task" my-app

The first option is recommended - it's simple and chainable!

Which applies to your situation?
```

### Spec Management Phase

**Trigger phrases**:
- "write a spec"
- "need architecture document"
- "document this feature"
- "create epic/feature"
- "requirements doc"

**Recommended commands**:

1. **Plan the work** → `/ccpm:plan "Task title" <project>`
   - Creates Linear issue with comprehensive plan
   - Gathers context from Jira/Confluence/Slack
   - Analyzes codebase
   - Generates implementation checklist

2. **Update plan with details** → `/ccpm:plan <issue-id> "additional requirements"`
   - Add architecture details
   - Specify API design requirements
   - Document data model needs
   - Add testing and security considerations

**Example conversation**:
```
User: "Let's implement the payment gateway integration"

Claude: [pm-workflow-guide activates]

⚠️ This sounds like a complex feature that needs planning first.

Recommended workflow:
1. /ccpm:plan "Payment Gateway Integration" my-app
2. Review the plan (architecture, security, API design)
3. Update plan if needed: /ccpm:plan <issue-id> "additional details"
4. Then start implementation: /ccpm:work

Would you like to start with planning?
```

### Implementation Phase

**Trigger phrases**:
- "start coding"
- "begin implementation"
- "let's build this"
- "what should I work on"
- "ready to code"
- "save my progress"
- "commit this code"

**Recommended commands**:

1. **Natural command** → `/ccpm:work`
   - Start or resume implementation
   - Auto-detects issue from git branch
   - Fetches full task context
   - Lists available agents
   - Coordinates parallel work

2. **Save progress** → `/ccpm:sync "summary"`
   - Save work-in-progress to Linear
   - Auto-detects issue from git branch
   - Documents changes made
   - Updates Linear context
   - Maintains full history

3. **Commit code** → `/ccpm:commit`
   - Create conventional git commit
   - Auto-formats commit message
   - Links to Linear issue
   - Example: `feat(auth): add 2FA support`

**Example conversation**:
```
User: "Let's start working on AUTH-123"

Claude: [pm-workflow-guide activates]

Perfect! Use the natural workflow:

/ccpm:work                    # Start implementation (auto-detects AUTH-123)
/ccpm:sync "progress note"    # Save progress as you work
/ccpm:commit                  # Create conventional commits
/ccpm:verify                  # Check quality when done
/ccpm:done                    # Create PR and finalize

Start with: /ccpm:work
Ready to proceed?
```

### Verification Phase

**Trigger phrases**:
- "ready to test"
- "done coding"
- "check my work"
- "run quality checks"
- "verify implementation"

**Recommended commands**:

1. **Natural command** → `/ccpm:verify`
   - Run all quality checks
   - Auto-detects issue from git branch
   - Runs tests, linting, build checks
   - Comprehensive code review
   - Final approval when passing

**Example conversation**:
```
User: "I'm done implementing, ready to test"

Claude: [pm-workflow-guide activates]

Perfect! Let's verify your work:

/ccpm:verify

This will:
✓ Run all automated checks (tests, linting, build)
✓ Perform comprehensive code review
✓ Security audit
✓ Performance check
✓ Final approval when passing

Ready to proceed?
```

### Completion Phase

**Trigger phrases**:
- "ready to merge"
- "ship it"
- "create PR"
- "deploy this"
- "mark as complete"

**Recommended commands**:

1. **Natural command** → `/ccpm:done`
   - Auto-detects issue from git branch
   - Creates PR with auto-generated description
   - Syncs Linear status to Jira
   - Sends Slack notification
   - Marks Linear issue complete
   - Requires confirmation for external writes (safety)

**Example conversation**:
```
User: "Everything looks good, ready to ship!"

Claude: [pm-workflow-guide + external-system-safety activate]

Perfect! Let's finalize:

/ccpm:done

This will:
1. Create BitBucket PR with auto-description
2. Update Linear status to "Complete"
3. Sync Jira status to "Done"
4. Send Slack notification to team

⚠️ Note: External system writes require your confirmation

Ready to proceed?
```

### Utility Commands (Context-Aware)

**When user asks "what's the status"** → `/ccpm:work <linear-issue-id>`
- Shows current Linear status
- Formatted display
- Progress indicators

**When user asks "load this task"** → `/ccpm:work <linear-issue-id>`
- Quick context loading
- Fetches issue details
- Identifies related files
- Sets up environment

**When user asks "what's available"** → `/ccpm:work`
- Lists all available agents
- Shows capabilities
- From CLAUDE.md

**When user asks "how complex"** → `/ccpm:work <linear-issue-id>`
- AI-powered analysis
- Complexity assessment
- Risk identification
- Timeline estimation

**When user asks "what depends on what"** → `/ccpm:work <linear-issue-id>`
- Visualizes dependencies
- Shows execution order
- Identifies blockers

**When user asks "show progress"** → `/ccpm:sync <project>`
- Progress across all tasks
- Team velocity
- Burndown charts

**When user asks "search tasks"** → `/ccpm:work <project> "<query>"`
- Text search in Linear
- Lists matching tasks
- Quick access

**When user is stuck** → `/ccpm:work [issue-id]`
- Context-aware help
- Command suggestions
- Workflow guidance

### Workflow State Machine

```
┌─────────────┐
│   IDEA      │ "I need to..."
└──────┬──────┘
       │ /ccpm:plan (for epics/features)
       │ /ccpm:plan (for tasks)
       ▼
┌─────────────┐
│  PLANNED    │ "Plan is ready"
└──────┬──────┘
       │ /ccpm:work
       ▼
┌─────────────┐
│IMPLEMENTING │ "Working on it"
└──────┬──────┘
       │ /ccpm:verify
       ▼
┌─────────────┐
│  VERIFYING  │ "Testing & reviewing"
└──────┬──────┘
       │ /ccpm:verify
       ▼
┌─────────────┐
│  VERIFIED   │ "All checks passed"
└──────┬──────┘
       │ /ccpm:done
       ▼
┌─────────────┐
│  COMPLETE   │ "Shipped! 🚀"
└─────────────┘
```

### Special Workflows

#### Repeat Project (BitBucket PR Review)

**Trigger phrases**:
- "check this PR"
- "review PR 123"
- "analyze pull request"
- "Repeat project PR"

**Command**: `/ccpm:repeat:check-pr <pr-number-or-url>`
- Uses Playwright browser automation
- Navigates BitBucket
- Analyzes PR changes
- Reviews code quality
- Provides feedback

#### UI Design Workflow

**Trigger phrases**:
- "design the UI"
- "create mockups"
- "need wireframes"

**Commands**:
1. `/ccpm:plan <issue-id>` - Generate multiple design options
2. `/ccpm:plan <issue-id> <option-number> "<feedback>"` - Iterate on design
3. `/ccpm:plan <issue-id> <option-number>` - Finalize and generate specs

### Smart Suggestions Based on Context

**If user mentions issue ID directly**:
```
User: "What's the status of AUTH-123?"
Claude: Let me check: /ccpm:work AUTH-123
```

**If user seems lost**:
```
User: "I don't know what to do next with this task"
Claude: Let me help: /ccpm:work <issue-id>
```

**If user mentions external ticket**:
```
User: "I need to plan JIRA-456"
Claude: I'll create a Linear issue and plan it: /ccpm:plan
```

**If user asks about agents**:
```
User: "What agents can help with backend work?"
Claude: Let me show you: /ccpm:work
```

### Integration with Other Skills

This skill works alongside:

1. **external-system-safety**: Reminds user about confirmation requirements
   ```
   Claude: Note: /ccpm:done will require confirmation for:
   - Jira status update
   - Slack notification
   ```

2. **spec-first-development**: Encourages spec creation before implementation
   ```
   Claude: Before using /ccpm:work, consider:
   - Does this task have a spec?
   - For complex features, use /ccpm:plan first
   ```

3. **tdd-practices**: Reminds about TDD workflow
   ```
   Claude: Remember: Write tests first!
   The tdd-enforcer hook will block production code without tests.
   ```

### Error Prevention

**Prevent common mistakes**:

❌ User: "/ccpm:plan without JIRA ticket"
✅ Claude: "You'll need a Jira ticket ID. Do you have one, or should we use /ccpm:plan?"

❌ User: "/ccpm:work without planning"
✅ Claude: "I don't see a plan for this issue yet. Run /ccpm:plan first."

❌ User: "/ccpm:done before verification"
✅ Claude: "Run /ccpm:verify first to ensure quality checks pass."

### Natural Workflow Activation Triggers

This skill activates with high priority when users ask about the natural workflow:

**Planning triggers**:
- "how do I plan"
- "start a new task"
- "create a task"
- "plan something"

**Implementation triggers**:
- "start work" / "start working"
- "save my progress"
- "commit this" / "create a commit"
- "how do I commit"

**Verification triggers**:
- "how do I test"
- "verify my work"
- "run checks"
- "before I ship"

**Completion triggers**:
- "ready to ship"
- "create a PR"
- "finalize this"
- "mark complete"

When these triggers appear, recommend the natural 6-command workflow first.

### Learning Mode

For new users, provide extra context:

```
User: "How do I plan a task?"

Claude: [pm-workflow-guide activates - detects new user]

CCPM has a simple 6-command workflow:

1. /ccpm:plan "task title" <project>   - Create & plan
2. /ccpm:work                           - Start coding
3. /ccpm:sync "summary"                 - Save progress
4. /ccpm:commit                         - Git commit
5. /ccpm:verify                         - Quality checks
6. /ccpm:done                           - Create PR

These commands are chainable and auto-detect your issue from git branch!

For more control, extended commands like /ccpm:plan also available.

Which matches your situation?

(Tip: For complex features, consider /ccpm:plan first)
```

## Examples

### Example 1: New Feature from Scratch

```
User: "I need to implement a new export feature for reports"

Claude: [pm-workflow-guide + spec-first-development activate]

Perfect! Let's use the natural workflow:

/ccpm:plan "Export reports feature" my-app

This will:
✓ Create Linear issue
✓ Gather context from Jira/Slack/Confluence
✓ Analyze codebase
✓ Generate comprehensive plan

Then continue with:
/ccpm:work           # Start coding
/ccpm:sync "notes"   # Save progress
/ccpm:commit         # Git commit
/ccpm:verify         # Quality checks
/ccpm:done           # Create PR & ship

For complex features, add /ccpm:plan before /ccpm:work

Shall I start planning?
```

### Example 2: Mid-Implementation Questions

```
User: "I'm stuck on this auth task, not sure what to do next"

Claude: [pm-workflow-guide activates]

Let me help! Continue with the natural workflow:

/ccpm:sync "stuck on session management"    # Save progress with note

Then I can help debug and suggest next steps.

What's your issue ID or branch name?
```

### Example 3: Ready to Ship

```
User: "I think I'm done, how do I finish this?"

Claude: [pm-workflow-guide activates]

Great! Use the natural workflow:

/ccpm:verify          # Run all quality checks

Once passing, continue:

/ccpm:done            # Create PR, sync Jira, ship

That's it! The natural workflow handles everything.

Ready to verify?
```

## Command Reference Quick Access

**Full command list**: `/ccpm:work`
**Visual workflow**: `/ccpm:work`
**Search commands**: Ask "what command should I use for..."

## Summary

This skill helps you:
- ✅ **Use 6 simple commands** for the complete workflow (plan, work, sync, commit, verify, done)
- ✅ **Chain commands naturally** - they auto-detect context from git branch
- ✅ **Never worry about options** - natural commands make the best choice
- ✅ **Follow optimal workflows** - each phase has a clear recommended path
- ✅ **Avoid common mistakes** - skill prevents implementing without planning, shipping without verification
- ✅ **Explore 49+ commands** when you need more control (extended options always available)

### Quick Start: The 6-Command Workflow

```
/ccpm:plan "title" <project>   →  Create and plan a task
/ccpm:work                     →  Start or resume coding
/ccpm:sync "summary"           →  Save progress
/ccpm:commit                   →  Create conventional git commit
/ccpm:verify                   →  Run quality checks
/ccpm:done                     →  Create PR and finalize
```

**That's it!** These 6 commands cover 90% of all CCPM workflows. The skill activates automatically when you mention planning, implementation, verification, or completion—providing intelligent suggestions based on your exact context.

For advanced workflows (specs, UI design, multi-agent projects), extended commands are always available.
