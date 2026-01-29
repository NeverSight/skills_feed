---
name: linear-workflow-manager
description: This skill should be used when organizing daily work with Linear, starting the work day, reviewing priorities, triaging issues, or managing status updates. Use it for daily standup preparation, automated issue triage, workload planning, and status reporting. Integrates with Linear GraphQL API for seamless issue management.
---

# Linear Workflow Manager

## Overview

This skill helps organize your work day with Linear by automating daily planning, issue triage, and status updates. It leverages autonomous Claude agents to process issues, analyze workload, and generate reports, while providing structured workflows for common Linear tasks.

## Core Workflows

### 1. Daily Standup & Planning

**Trigger:** "Start my work day" or "Plan my day with Linear"

**Workflow:**

1. **Fetch high priority items** - Query Linear for issues assigned to you filtered by priority (Urgent, High)
2. **Analyze workload** - Review issue count, estimates, deadlines, and blockers
3. **Suggest daily priorities** - Recommend which issues to tackle first based on:
   - Priority level
   - Due dates
   - Dependencies and blockers
   - Project milestones
   - Team needs
4. **Create daily plan** - Present organized plan with time estimates and suggested ordering

**Agent Usage:** Launch a planning agent with Task tool (subagent_type: general-purpose) to:
- Analyze the full workload context
- Identify dependencies and blockers
- Generate prioritized task list
- Estimate time allocations

**Example interaction:**
```
User: "Start my work day"
Assistant: I'll help you plan your day with Linear.
[Executes: linear.sh query queries/planning/my-priorities.json]
[Analyzes output and creates prioritized plan]
```

### 2. Issue Triage

**Trigger:** "Triage new Linear issues" or "Process unassigned issues"

**Workflow:**

1. **Fetch untriaged issues** - Query Linear for new/unassigned issues or issues without labels/priority
2. **Categorize each issue** - For each issue, analyze:
   - Content and context
   - Urgency and impact
   - Appropriate team/assignee
   - Required labels and project
3. **Apply metadata** - Set priority, add labels, assign to team/person, link to projects
4. **Document decisions** - Add comment explaining triage decisions for transparency

**Agent Usage:** Launch a triage agent with Task tool (subagent_type: general-purpose) to:
- Process multiple issues in batch
- Apply consistent triage criteria
- Update Linear issues via GraphQL mutations
- Generate triage summary report

**Example interaction:**
```
User: "Triage new Linear issues"
Assistant: I'll process untriaged issues in your Linear workspace.
[Executes: linear.sh query queries/triage/untriaged-issues.json]
[Analyzes issues and updates via GraphQL mutations]
```

**Triage Criteria:** Load `references/triage_criteria.md` for team-specific guidelines on:
- Priority assignment rules
- Label taxonomy
- Assignment routing
- SLA expectations

### 3. Status Updates & Reporting

**Trigger:** "Generate status update" or "Create Linear progress report"

**Workflow:**

1. **Define scope** - Ask user what to report on:
   - Personal work (your issues)
   - Team work (team's issues)
   - Project work (specific project or milestone)
   - Custom filter
2. **Fetch relevant issues** - Query Linear with appropriate filters
3. **Generate report** - Create structured summary including:
   - Completed work (since last report)
   - In-progress work (current status)
   - Blocked items (with blockers identified)
   - Upcoming work (next priorities)
   - Key metrics (velocity, completion rate)
4. **Format for audience** - Adapt tone/detail for standup vs. stakeholder update

**Agent Usage:** Launch a reporting agent with Task tool (subagent_type: general-purpose) to:
- Aggregate issue data across time periods
- Identify trends and patterns
- Generate clear, concise summaries
- Format for different audiences

**Example interaction:**
```
User: "Generate my weekly status update"
Assistant: I'll create a status report for your Linear work this week.
[Executes: linear.sh query queries/reporting/completed-this-week.json]
[Analyzes data and generates formatted summary]
```

**Report Templates:** Load `references/report_templates.md` for standard formats like:
- Daily standup updates
- Weekly progress reports
- Sprint retrospectives
- Stakeholder summaries

## Linear GraphQL Integration

This skill uses direct Linear GraphQL API access for all Linear operations. No MCP required.

**Setup:** Ensure Linear API key is configured in `~/.claude/.env`:
```bash
LINEAR_API_KEY=lin_api_xxx
```

**Helper Script:** `scripts/linear.sh` provides command interface:
```bash
linear.sh query <query-file>           # Execute query template
linear.sh create-issue <title> <desc>  # Quick issue creation
linear.sh list-issues                  # List your issues
linear.sh my-day                       # Today's priorities
```

**Query Templates:** Pre-built GraphQL queries in `queries/` directory:
- `planning/` - Daily standup, workload, deadlines
- `triage/` - Untriaged issues, priority updates, assignments
- `reporting/` - Completed work, blockers, velocity
- `common/` - Teams, search, CRUD operations

**For Agents:**
- Start at `references/query-index.md` to find the right query
- Use `linear.sh query <template>` for simple execution
- Or construct custom GraphQL with curl for complex needs
- See `references/examples.md` for patterns and workflows

## Best Practices

### Daily Workflow
1. Start each work day with the planning workflow to set priorities
2. Use triage workflow for any new issues that come in during the day
3. End the day with a quick status update to track progress

### Agent Coordination
- Use agents for batch operations (triage multiple issues, generate reports)
- Keep user in the loop with progress updates
- Present agent findings for user review before bulk updates

### Customization
- Add team-specific triage criteria to `references/triage_criteria.md`
- Customize report templates in `references/report_templates.md`
- Adjust priority rules and workflows to match your team's process

## Quick Reference

**Start work day:**
"Start my work day" → Planning agent analyzes high priority items

**Triage issues:**
"Triage new issues" → Triage agent processes untriaged items

**Generate report:**
"Create status update" → Reporting agent summarizes work and progress

**Custom query:**
"Show me [specific filter]" → Query Linear directly with helper script or GraphQL