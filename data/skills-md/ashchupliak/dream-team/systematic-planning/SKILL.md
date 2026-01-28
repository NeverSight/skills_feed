---
name: systematic-planning
description: Systematic feature planning workflow - use when starting complex features requiring structured approach
---

# Systematic Planning Skill

Transform complex feature requests into structured, executable plans.

## When to Use
- Complex features requiring multiple components
- Features touching backend + frontend + infrastructure
- Tasks requiring careful design before implementation

## Planning Phases

### Phase 1: Business Specification
Define what we're building and why:
```markdown
## Feature: [Name]

### Problem Statement
[What problem does this solve?]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

### Scope
**In Scope**: [what's included]
**Out of Scope**: [what's NOT included]

### Constraints
- [Technical constraints]
- [Business constraints]
```

### Phase 2: Technical Architecture
How we'll build it:
```markdown
## Technical Design

### Approach
[High-level approach in 2-3 sentences]

### Components
1. [Component 1] - [responsibility]
2. [Component 2] - [responsibility]

### Data Model
[Tables/entities needed]

### API Design
[Endpoints with methods]

### Dependencies
[External services/libraries needed]
```

### Phase 3: Implementation Tasks
Numbered steps for execution:
```markdown
## Implementation Tasks

### S001: [First task]
- Files: [files to create/modify]
- Acceptance: [how to verify]

### S002: [Second task]
- Files: [files to create/modify]
- Acceptance: [how to verify]

[Continue with S003, S004, etc.]
```

## Output Location
Save planning documents to: `.claude/plans/[feature-name].md`

## Integration with Team Workflow
1. Use this skill for Phase 0 (before analyst)
2. Output feeds into analyst requirements
3. Architect uses this as foundation for design

## Example Usage

User: "Add user notification preferences"

Response:
```markdown
# Feature: User Notification Preferences

## Phase 1: Business Spec
### Problem
Users cannot control which notifications they receive, leading to notification fatigue.

### Success Criteria
- [ ] Users can toggle email notifications
- [ ] Users can toggle in-app notifications
- [ ] Preferences persist across sessions

### Scope
**In**: Email, in-app notification toggles
**Out**: SMS, push notifications (future phase)

## Phase 2: Technical Design
### Approach
Add notification_preferences table linked to users, expose via REST API, update notification service to check preferences.

### Components
1. NotificationPreference entity
2. PreferenceService
3. PreferenceController
4. UI Settings panel

### API
GET/PUT /api/v1/users/{id}/notification-preferences

## Phase 3: Tasks
### S001: Database migration
- Files: V026__notification_preferences.sql
- Acceptance: Table exists with correct schema

### S002: Backend implementation
- Files: NotificationPreference.kt, PreferenceService.kt, PreferenceController.kt
- Acceptance: API returns/updates preferences

### S003: Frontend UI
- Files: settings/notifications.tsx
- Acceptance: User can toggle preferences
```

## Tips
- Keep tasks small (< 2 hours each)
- Each task should be independently verifiable
- Link tasks to specific files
- Include acceptance criteria for QA
