---
name: jira
description: Jira project management including issues, sprints, boards, and workflows. Activate for Jira tickets, sprint planning, backlog management, and Atlassian integration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Jira Skill

Provides comprehensive Jira project management capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Issue creation and management
- Sprint planning and execution
- Backlog grooming
- Jira API integration
- Workflow automation

## Jira API Quick Reference

### Authentication
\`\`\`python
from jira import JIRA

# Basic auth
jira = JIRA(
    server='https://your-domain.atlassian.net',
    basic_auth=('email@example.com', 'API_TOKEN')
)

# OAuth
jira = JIRA(
    server='https://your-domain.atlassian.net',
    oauth={
        'access_token': 'ACCESS_TOKEN',
        'access_token_secret': 'ACCESS_TOKEN_SECRET',
        'consumer_key': 'CONSUMER_KEY',
        'key_cert': 'KEY_CERT'
    }
)
\`\`\`

### Issue Operations

\`\`\`python
# Create issue
new_issue = jira.create_issue(
    project='GA',
    summary='Implement agent health monitoring',
    description='Add health check endpoints and monitoring dashboards',
    issuetype={'name': 'Story'},
    priority={'name': 'High'},
    labels=['backend', 'monitoring'],
    components=[{'name': 'Agent Platform'}]
)
print(f"Created: {new_issue.key}")

# Get issue
issue = jira.issue('GA-123')
print(f"Summary: {issue.fields.summary}")
print(f"Status: {issue.fields.status.name}")

# Update issue
issue.update(
    summary='Updated summary',
    description='Updated description',
    priority={'name': 'Critical'}
)

# Add comment
jira.add_comment(issue, 'This is a comment')

# Transition issue
jira.transition_issue(issue, 'In Progress')

# Assign issue
jira.assign_issue(issue, 'username')

# Link issues
jira.create_issue_link('Blocks', 'GA-123', 'GA-124')
\`\`\`

### Search (JQL)

\`\`\`python
# Basic search
issues = jira.search_issues('project = GA AND status = "In Progress"')

# With fields
issues = jira.search_issues(
    'project = GA',
    fields='summary,status,assignee',
    maxResults=50
)

# Common JQL queries
queries = {
    'my_open': 'assignee = currentUser() AND status != Done',
    'sprint_backlog': 'project = GA AND sprint in openSprints()',
    'high_priority': 'project = GA AND priority = High AND status != Done',
    'recently_updated': 'project = GA AND updated >= -7d ORDER BY updated DESC',
    'unassigned': 'project = GA AND assignee is EMPTY AND status != Done',
    'bugs': 'project = GA AND issuetype = Bug AND status != Done'
}

for name, jql in queries.items():
    results = jira.search_issues(jql)
    print(f"{name}: {len(results)} issues")
\`\`\`

### Sprint Management

\`\`\`python
# Get board
board = jira.boards(name='GA Board')[0]

# Get sprints
sprints = jira.sprints(board.id)
active_sprint = next(s for s in sprints if s.state == 'active')

# Get sprint issues
sprint_issues = jira.search_issues(f'sprint = {active_sprint.id}')

# Create sprint
new_sprint = jira.create_sprint(
    name='Sprint 15',
    board_id=board.id,
    startDate='2024-01-15',
    endDate='2024-01-29'
)

# Add issues to sprint
jira.add_issues_to_sprint(active_sprint.id, ['GA-123', 'GA-124'])

# Start/Complete sprint
jira.update_sprint(sprint.id, state='active')
jira.update_sprint(sprint.id, state='closed')
\`\`\`

### Bulk Operations

\`\`\`python
# Bulk create
issues_to_create = [
    {
        'project': {'key': 'GA'},
        'summary': f'Task {i}',
        'issuetype': {'name': 'Task'}
    }
    for i in range(1, 6)
]
created = jira.create_issues(issues_to_create)

# Bulk transition
issues = jira.search_issues('project = GA AND status = "To Do"')
for issue in issues:
    jira.transition_issue(issue, 'In Progress')
\`\`\`

## Issue Templates

### Story Template
\`\`\`markdown
## User Story
As a [type of user],
I want [goal]
So that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
- Implementation details
- Dependencies

## Definition of Done
- [ ] Code complete
- [ ] Tests written
- [ ] Documentation updated
- [ ] Code reviewed
\`\`\`

### Bug Template
\`\`\`markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS:
- Browser:
- Version:

## Screenshots/Logs
Attach relevant screenshots or logs
\`\`\`

## Workflow States

\`\`\`
┌──────────┐    ┌─────────────┐    ┌────────────┐    ┌────────┐
│  To Do   │ -> │ In Progress │ -> │ In Review  │ -> │  Done  │
└──────────┘    └─────────────┘    └────────────┘    └────────┘
     ^                                    │
     └────────────────────────────────────┘
                   (Rejected)
\`\`\`

## Golden Armada Jira Commands

\`\`\`bash
# Create issue from CLI
/jira-create --type story --summary "Implement feature X" --priority high

# Get sprint status
/jira-status --sprint current

# Transition issue
/jira-transition GA-123 --status "In Progress"

# Sync with development
/atlassian-sync --commits --branch main
\`\`\`
