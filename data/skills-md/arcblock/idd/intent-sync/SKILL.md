---
name: intent-sync
description: After implementation is complete and tests pass, sync confirmed details back to Intent. Captures finalized interfaces, data structures, naming conventions, and architecture decisions. Use after development is done and user confirms the implementation.
---

# Intent Sync

Synchronize implementation details back to Intent after development is complete. This makes Intent the true single source of truth.

## When to Use

Use `/intent-sync` when:
- Implementation is complete
- All tests pass
- User has confirmed the implementation works
- You want to capture the finalized design in Intent

## What Gets Synced Back

During implementation, many details get finalized that weren't specified in the original Intent:

| Category | Examples |
|----------|----------|
| **Interfaces** | API endpoints, function signatures, protocol definitions |
| **Data Structures** | Schema definitions, type definitions, model structures |
| **Naming** | Final class names, function names, variable conventions |
| **Architecture** | Module boundaries, dependency directions, layer structure |
| **Configuration** | Environment variables, config file formats, defaults |
| **Error Handling** | Error codes, error message formats, recovery strategies |

## Workflow

```
User confirms implementation is done
    ↓
Read original Intent file
    ↓
Scan implemented code for:
    - Public interfaces
    - Data structures
    - Key naming conventions
    - Architecture patterns
    ↓
Compare with Intent
    ↓
Identify gaps/differences
    ↓
Present changes for approval
    ↓
Update Intent with confirmed details
    ↓
Mark synced sections with timestamp
```

## Sync Process

### Step 1: Gather Implementation Facts

Scan the codebase for finalized details:

```
Code Analysis:
├── Public APIs
│   ├── Endpoints (REST/GraphQL/RPC)
│   ├── Function signatures
│   └── Event definitions
├── Data Models
│   ├── Database schemas
│   ├── Type definitions
│   └── Config structures
├── Architecture
│   ├── Module structure
│   ├── Dependency graph
│   └── Layer boundaries
└── Conventions
    ├── Naming patterns
    ├── Error formats
    └── Logging standards
```

### Step 2: Compare with Intent

Identify what's new or different:

| Status | Meaning | Action |
|--------|---------|--------|
| **New** | Not in original Intent | Add to Intent |
| **Changed** | Different from Intent | Update Intent |
| **Confirmed** | Matches Intent | Mark as implemented |
| **Removed** | In Intent but not implemented | Remove or mark deferred |

### Step 3: Present for Approval

Use `AskUserQuestion` to confirm changes:

```
"The following details were finalized during implementation.
Should I sync them back to Intent?"

Interfaces:
- [x] POST /api/users - Create user (new)
- [x] UserSchema: added 'createdAt' field (changed)

Data Structures:
- [x] Config now uses YAML instead of JSON (changed)

Naming:
- [x] Service class renamed to UserService (changed)
```

### Step 4: Update Intent

Add a new section or update existing sections:

```markdown
## Finalized Implementation Details

> Synced on: YYYY-MM-DD
> From: [commit hash or version]

### API Interfaces

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| /api/users | POST | `{name, email}` | `{id, name, email, createdAt}` |
| /api/users/:id | GET | - | `{id, name, email, createdAt}` |

### Data Structures

\`\`\`typescript
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}
\`\`\`

### Module Structure

\`\`\`
src/
├── api/
│   └── users.ts       # User endpoints
├── services/
│   └── UserService.ts # Business logic
├── models/
│   └── User.ts        # Data model
└── config/
    └── config.yaml    # Configuration
\`\`\`

### Key Decisions Confirmed

| Decision | Final Choice | Rationale |
|----------|--------------|-----------|
| Config format | YAML | Better readability for nested config |
| ID generation | UUID v4 | Standard, no coordination needed |
```

## Output Format

The sync adds or updates these Intent sections:

### New Section: `## Finalized Implementation Details`

Contains:
- Sync timestamp
- Source reference (commit/version)
- Concrete interfaces
- Concrete data structures
- Final module structure
- Confirmed decisions

### Updated Existing Sections

- Architecture diagrams updated to reflect reality
- Data contracts updated with actual schemas
- API specifications updated with real endpoints

## Sync Markers

Use markers to indicate sync status:

```markdown
## API Design

> [!SYNCED] Last synced: 2024-01-15 from commit abc123

### Endpoints
...
```

Or in tables:

| Component | Status | Last Synced |
|-----------|--------|-------------|
| User API | SYNCED | 2024-01-15 |
| Auth API | DRAFT | - |

## Integration with Other Skills

```
/intent-interview     # Create Intent (initial)
    ↓
/intent-review        # Approve Intent
    ↓
/intent-plan          # Generate execution plan
    ↓
[Execute: TDD cycles]
    ↓
/intent-sync          # Write back confirmed details (THIS SKILL)
    ↓
/intent-check         # Verify consistency
```

## Best Practices

1. **Sync after stability**: Don't sync during active development; wait for confirmation
2. **Preserve original intent**: Keep original design rationale, add implementation details
3. **Be specific**: Include actual types, actual endpoints, actual names
4. **Version reference**: Always note which code version was synced
5. **Incremental sync**: Can sync multiple times as features stabilize

## Example Session

```
User: Implementation is done, tests pass. Please sync back to Intent.