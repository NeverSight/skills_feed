---
name: project-estimation
description: "Create detailed software project effort estimates with task breakdowns by engineer role. When users ask for project estimates, effort breakdown, man-hours, resource planning, or project costing. Analyzes project descriptions and requirements documents to produce structured estimates. Can push backlog to Jira."
license: MIT
---

# Project Estimation Guide

## Overview

This skill helps create accurate software development estimates by systematically breaking down projects into estimable tasks and assigning effort by role. Output can be delivered as Excel spreadsheets using the `xlsx` skill, and tasks can be pushed directly to Jira to create a project backlog.

## Estimation Workflow

### Step 1: Clarify Project Scope

**ALWAYS ask the user about project maturity level before estimating:**

| Level | Description | Multiplier |
|-------|-------------|------------|
| **PoC** | Proof of Concept - minimal viable functionality, no production concerns | 0.3-0.5x |
| **MVP** | Minimum Viable Product - core features, basic quality, limited scale | 0.6-0.8x |
| **Production** | Full production - complete features, security, scalability, monitoring | 1.0x |

**Key questions to ask:**
- Is this PoC, MVP, or production-ready system?
- What are the non-functional requirements (users, load, compliance)?
- Are there existing systems to integrate with?
- What is the team's familiarity with the tech stack?
- Are there hard deadlines or constraints?

### Step 2: Hierarchical Task Breakdown

Break down from high-level to lowest estimable units (1-3 days max per task).

```
Level 0: Project
└── Level 1: Epic/Module
    └── Level 2: Feature
        └── Level 3: Task
            └── Level 4: Subtask (if needed)
```

**Example breakdown:**
```
E-commerce Platform
├── User Management (Epic)
│   ├── Registration (Feature)
│   │   ├── Registration form UI (Task) - FE: 1.5d
│   │   ├── Email verification API (Task) - BE: 1d
│   │   ├── Email templates (Task) - BE: 0.5d
│   │   └── Registration tests (Task) - QA: 1d
│   ├── Authentication (Feature)
│   │   ├── Login/logout UI (Task) - FE: 1d
│   │   ├── JWT auth endpoints (Task) - BE: 1.5d
│   │   ├── Password reset flow (Task) - BE: 1.5d, FE: 1d
│   │   └── Auth tests (Task) - QA: 1.5d
│   └── User Profile (Feature)
│       └── ...
├── Product Catalog (Epic)
│   └── ...
└── Checkout (Epic)
    └── ...
```

### Step 3: Assign Effort by Role

**Standard roles and responsibilities:**

| Role | Code | Responsibilities |
|------|------|------------------|
| Backend Engineer | BE | APIs, business logic, database, integrations |
| Frontend Engineer | FE | UI components, state management, UX implementation |
| AI/ML Engineer | AI | Model development, training, inference pipelines |
| QA Engineer | QA | Test planning, automation, manual testing |
| DevOps Engineer | DevOps | Infrastructure, CI/CD, monitoring, deployment |
| Project Manager | PM | Coordination, documentation, stakeholder communication |
| Designer | Design | UI/UX design, prototypes, design system |
| Tech Lead | TL | Architecture, code review, technical decisions |

### Step 4: Apply Risk Factors

| Risk Factor | Multiplier |
|-------------|------------|
| New technology for team | 1.3-1.5x |
| Unclear requirements | 1.2-1.5x |
| External API dependencies | 1.2-1.4x |
| Legacy system integration | 1.3-1.6x |
| Tight deadline | 1.2-1.4x |
| Distributed team | 1.1-1.3x |

### Step 5: Add Contingency Buffer

| Confidence Level | Buffer |
|------------------|--------|
| High (clear scope, known tech) | 10-15% |
| Medium (some unknowns) | 20-30% |
| Low (many unknowns) | 30-50% |

## Baseline Estimates by Component

### Frontend Components

| Component | FE Effort | Notes |
|-----------|-----------|-------|
| Simple page | 0.5-1d | Static content |
| Form (simple) | 1-2d | 3-5 fields, basic validation |
| Form (complex) | 3-5d | Multi-step, conditional logic |
| Data table | 2-4d | Sort, filter, pagination |
| Dashboard | 3-5d | Multiple widgets |
| Admin panel | 5-10d | CRUD operations, filters |

### Backend Components

| Component | BE Effort | Notes |
|-----------|-----------|-------|
| CRUD endpoint | 0.5-1d | Standard operations |
| Complex endpoint | 1-3d | Business logic, validation |
| Third-party integration | 2-5d | Per API |
| Background job | 1-3d | With retry logic |
| Auth system | 3-5d | JWT, sessions, permissions |

### AI/ML Components

| Component | AI Effort | Notes |
|-----------|-----------|-------|
| LLM integration | 2-4d | Prompt engineering, API setup |
| RAG pipeline | 5-10d | Embeddings, vector DB, retrieval |
| Custom model training | 10-20d | Data prep, training, evaluation |
| ML inference API | 3-5d | Model serving, optimization |

### QA Effort Guidelines

| Coverage | QA Multiplier |
|----------|---------------|
| Minimal (smoke tests) | 0.1x of dev |
| Standard (core flows) | 0.2-0.3x of dev |
| Comprehensive | 0.4-0.5x of dev |
| Critical system | 0.5-0.7x of dev |

### PM/Coordination Overhead

| Project Size | PM Overhead |
|--------------|-------------|
| Small (<1 month) | 10-15% |
| Medium (1-3 months) | 15-20% |
| Large (3+ months) | 20-25% |

## Output Format

### Excel Spreadsheet (Recommended)

Use the `xlsx` skill to create estimates in Excel format with:

**Sheet 1: Summary**
| Role | Days | Rate | Cost |
|------|------|------|------|
| BE | 45 | $X | $Y |
| FE | 30 | $X | $Y |
| QA | 15 | $X | $Y |
| **Total** | **90** | | **$Z** |

**Sheet 2: Detailed Breakdown**
| Epic | Feature | Task | BE | FE | AI | QA | DevOps | PM | Total |
|------|---------|------|----|----|----|----|--------|-----|-------|
| User Mgmt | Registration | Form UI | - | 1.5 | - | - | - | - | 1.5 |
| User Mgmt | Registration | API | 1 | - | - | - | - | - | 1 |
| User Mgmt | Registration | Tests | - | - | - | 1 | - | - | 1 |

**Sheet 3: Assumptions & Risks**
- Document all assumptions made
- List identified risks with mitigation strategies
- Note excluded items

### Markdown Table (Quick Estimates)

```markdown
## Estimate Summary

| Phase | BE | FE | QA | DevOps | PM | Total |
|-------|----|----|----|----|-----|-------|
| Phase 1 | 20d | 15d | 8d | 5d | 5d | 53d |
| Phase 2 | 15d | 10d | 6d | 3d | 4d | 38d |
| Buffer (20%) | | | | | | 18d |
| **Total** | **35d** | **25d** | **14d** | **8d** | **9d** | **109d** |
```

## Common Pitfalls to Avoid

**Underestimation causes:**
- Forgetting testing, code review, deployment time
- Not accounting for meetings (add 10-20%)
- Missing error handling and edge cases
- Ignoring documentation needs
- Assuming ideal conditions

**Items often forgotten:**
- Authentication and authorization
- Error handling and logging
- Data migration
- Environment setup
- API documentation
- Security hardening
- Performance optimization
- Monitoring and alerting

## Quick Reference

### T-Shirt to Days Conversion

| Size | PoC | MVP | Production |
|------|-----|-----|------------|
| XS | 0.25d | 0.5d | 1d |
| S | 0.5d | 1d | 2d |
| M | 1d | 2-3d | 4-5d |
| L | 2d | 4-5d | 8-10d |
| XL | 3-5d | 8-10d | 15-20d |

### Story Points to Days (per developer)

| Points | Days |
|--------|------|
| 1 | 0.25-0.5 |
| 2 | 0.5-1 |
| 3 | 1-2 |
| 5 | 2-3 |
| 8 | 3-5 |
| 13 | 5-8 |

## Jira Integration

Push estimated tasks directly to Jira to create a project backlog.

### Prerequisites

Before pushing to Jira, gather from the user:
1. **Jira instance URL** (e.g., `https://company.atlassian.net`)
2. **Project key** (e.g., `PROJ`)
3. **API token** - user can generate at https://id.atlassian.com/manage-profile/security/api-tokens
4. **Email** associated with the Jira account

### Task to Jira Mapping

| Estimation Level | Jira Issue Type |
|------------------|-----------------|
| Epic | Epic |
| Feature | Story |
| Task | Task or Sub-task |
| Subtask | Sub-task |

### Field Mapping

| Estimate Field | Jira Field |
|----------------|------------|
| Epic name | Epic Name (custom field) |
| Feature/Task name | Summary |
| Description | Description |
| Total effort (days) | Original Estimate (convert to hours: days × 8) |
| Role assignments | Labels or custom field |
| Story points | Story Points (if using points) |

### Push to Jira Workflow

**Step 1: Confirm with user**
```
Before pushing to Jira, confirm:
- Jira URL: [user provides]
- Project key: [user provides]
- Create Epics? (yes/no)
- Estimate format: (days/hours/story points)
```

**Step 2: Create issues via API**

Use bash with curl to create issues. First, set up authentication:

```bash
# Store credentials (ask user for these values)
JIRA_URL="https://company.atlassian.net"
JIRA_EMAIL="user@company.com"
JIRA_TOKEN="your-api-token"
PROJECT_KEY="PROJ"
```

**Create an Epic:**
```bash
curl -X POST "$JIRA_URL/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -d '{
    "fields": {
      "project": {"key": "'"$PROJECT_KEY"'"},
      "summary": "User Management",
      "issuetype": {"name": "Epic"},
      "description": {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Epic for user management features"}]}]
      }
    }
  }'
```

**Create a Story linked to Epic:**
```bash
curl -X POST "$JIRA_URL/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -d '{
    "fields": {
      "project": {"key": "'"$PROJECT_KEY"'"},
      "summary": "User Registration",
      "issuetype": {"name": "Story"},
      "parent": {"key": "PROJ-1"},
      "description": {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Implement user registration flow"}]}]
      },
      "timetracking": {
        "originalEstimate": "24h"
      },
      "labels": ["BE", "FE", "QA"]
    }
  }'
```

**Create a Task/Sub-task:**
```bash
curl -X POST "$JIRA_URL/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -d '{
    "fields": {
      "project": {"key": "'"$PROJECT_KEY"'"},
      "summary": "Registration form UI",
      "issuetype": {"name": "Sub-task"},
      "parent": {"key": "PROJ-2"},
      "timetracking": {
        "originalEstimate": "12h"
      },
      "labels": ["FE"]
    }
  }'
```

### Batch Creation Script

For large estimates, generate a bash script that creates all issues:

```bash
#!/bin/bash
# Auto-generated Jira import script

JIRA_URL="https://company.atlassian.net"
JIRA_EMAIL="$JIRA_EMAIL"
JIRA_TOKEN="$JIRA_TOKEN"
PROJECT_KEY="PROJ"

create_issue() {
  local json="$1"
  response=$(curl -s -X POST "$JIRA_URL/rest/api/3/issue" \
    -H "Content-Type: application/json" \
    -u "$JIRA_EMAIL:$JIRA_TOKEN" \
    -d "$json")
  echo "$response" | grep -o '"key":"[^"]*"' | cut -d'"' -f4
}

# Create Epics first, capture keys
echo "Creating Epics..."
EPIC_USER_MGMT=$(create_issue '{"fields":{"project":{"key":"'"$PROJECT_KEY"'"},"summary":"User Management","issuetype":{"name":"Epic"}}}')
echo "Created: $EPIC_USER_MGMT"

# Create Stories under Epics
echo "Creating Stories..."
STORY_REGISTRATION=$(create_issue '{"fields":{"project":{"key":"'"$PROJECT_KEY"'"},"summary":"User Registration","issuetype":{"name":"Story"},"parent":{"key":"'"$EPIC_USER_MGMT"'"},"timetracking":{"originalEstimate":"24h"}}}')
echo "Created: $STORY_REGISTRATION"

# Create Sub-tasks under Stories
echo "Creating Tasks..."
create_issue '{"fields":{"project":{"key":"'"$PROJECT_KEY"'"},"summary":"Registration form UI","issuetype":{"name":"Sub-task"},"parent":{"key":"'"$STORY_REGISTRATION"'"},"timetracking":{"originalEstimate":"12h"},"labels":["FE"]}}'

echo "Done!"
```

### CSV Export for Jira Import

Alternatively, create a CSV file for Jira's CSV import feature:

```csv
Summary,Issue Type,Parent,Description,Original Estimate,Labels
User Management,Epic,,"Epic for user management features",,
User Registration,Story,User Management,"Implement user registration",24h,"BE,FE,QA"
Registration form UI,Sub-task,User Registration,"Build the registration form",12h,FE
Email verification API,Sub-task,User Registration,"API endpoint for email verification",8h,BE
Registration tests,Sub-task,User Registration,"Write tests for registration",8h,QA
```

**CSV Import Steps:**
1. Go to Jira > Project Settings > External System Import
2. Select "CSV"
3. Upload the CSV file
4. Map columns to Jira fields
5. Review and import

### Estimate to Hours Conversion

When pushing to Jira, convert days to hours:

| Days | Hours (8h/day) |
|------|----------------|
| 0.25 | 2h |
| 0.5 | 4h |
| 1 | 8h |
| 1.5 | 12h |
| 2 | 16h |
| 3 | 24h |
| 5 | 40h |

### Jira Custom Fields

Common custom fields that may need configuration:

| Field | API Field Name | Notes |
|-------|---------------|-------|
| Story Points | `customfield_10016` | ID varies by instance |
| Epic Link | `customfield_10014` | For older Jira versions |
| Sprint | `customfield_10020` | ID varies by instance |

To find custom field IDs for a project:
```bash
curl -s "$JIRA_URL/rest/api/3/field" \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" | jq '.[] | {name, id}'
```

### Error Handling

Common issues when pushing to Jira:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify email and API token |
| 400 Bad Request | Invalid field values | Check issue type names, project key |
| 403 Forbidden | Insufficient permissions | User needs project write access |
| Field not found | Custom field ID wrong | Look up correct field ID |

### Jira Cloud vs Server

The API examples above use Jira Cloud (Atlassian Document Format for descriptions). For Jira Server/Data Center:

```bash
# Jira Server uses plain text descriptions
curl -X POST "$JIRA_URL/rest/api/2/issue" \
  -H "Content-Type: application/json" \
  -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -d '{
    "fields": {
      "project": {"key": "'"$PROJECT_KEY"'"},
      "summary": "Task name",
      "issuetype": {"name": "Task"},
      "description": "Plain text description here"
    }
  }'
```
