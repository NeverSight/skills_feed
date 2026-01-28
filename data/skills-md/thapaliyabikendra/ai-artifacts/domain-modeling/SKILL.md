---
name: domain-modeling
description: "Model business domains with entities, relationships, business rules, and permissions. Use when: (1) creating entity definitions, (2) defining business rules (BR-XXX), (3) designing permission structures, (4) analyzing domain impact, (5) maintaining domain documentation."
layer: 2
tech_stack: [agnostic, markdown]
topics: [entity-design, business-rules, relationships, permissions, aggregates, value-objects]
depends_on: []
complements: [requirements-engineering]
keywords: [Entity, Aggregate, ValueObject, BusinessRule, BR-, Relationship, Domain]
---

# Domain Modeling

Create and maintain business domain models with entities, relationships, business rules, and permission structures.

## When to Use

- Creating new entity definitions
- Defining business rules (BR-XXX format)
- Designing permission and role structures
- Analyzing impact of domain changes
- Maintaining `docs/domain/` documentation

## Entity Definition Template

```markdown
# {Entity} Entity

> **Aggregate Root**: Yes/No
> **Base Class**: `FullAuditedAggregateRoot<Guid>`
> **Table**: `{Entities}`

## Description
[Purpose of this entity in the domain]

## Properties
| Property | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `Id` | `Guid` | Yes | PK | Unique identifier |
| `Name` | `string` | Yes | MaxLength(100) | Display name |
| `Email` | `string` | Yes | Email format, Unique | Contact email |
| `Status` | `{Entity}Status` | Yes | Enum | Current state |
| `CreatedAt` | `DateTime` | Yes | Auto-set | Creation timestamp |

## Relationships
| Relationship | Type | Target Entity | FK Column | Description |
|--------------|------|---------------|-----------|-------------|
| Parent | N:1 | `{ParentEntity}` | `{Parent}Id` | Belongs to parent |
| Children | 1:N | `{ChildEntity}` | - | Has many children |

## Business Rules
| Rule ID | Rule | Validation Point |
|---------|------|------------------|
| BR-{CAT}-001 | [Rule description] | [When validated] |

## State Transitions
```
[Initial] → [State1] → [State2] → [Final]
              ↓
          [Cancelled]
```

## API Access
| Operation | Permission | Roles |
|-----------|------------|-------|
| List | `{Project}.{Entities}` | Admin, User |
| View | `{Project}.{Entities}` | Admin, User |
| Create | `{Project}.{Entities}.Create` | Admin |
| Update | `{Project}.{Entities}.Edit` | Admin |
| Delete | `{Project}.{Entities}.Delete` | Admin |

## Sample Data
| Id | Name | Status |
|----|------|--------|
| `{guid}` | Example 1 | Active |
```

## Business Rule Format

### Rule ID Convention
```
BR-{CATEGORY}-{NUMBER}

Categories:
- PAT: Patient rules
- DOC: Doctor rules
- APT: Appointment rules
- SCH: Schedule rules
- MED: Medical record rules
- SYS: System-wide rules
```

### Rule Documentation
```markdown
| ID | Rule | Enforcement | Impact |
|----|------|-------------|--------|
| BR-APT-001 | Appointments cannot overlap for same doctor | Create/Update | Reject with error |
| BR-APT-002 | Appointments must be within doctor schedule | Create | Reject with error |
| BR-PAT-001 | Patient email must be unique | Create/Update | Reject with error |
```

### Rule Template (Detailed)
```markdown
**BR-{CAT}-{NNN}: {Rule Name}**

**Description**: [What the rule enforces]
**Trigger**: [When this rule applies]
**Condition**: [The logic to evaluate]
**Action**: [What happens when condition is met/not met]
**Exception**: [Any exceptions to this rule]
**Related**: [Related rules or entities]
```

## Permission Structure

### Naming Convention
```
{ProjectName}.{Resource}.{Action}

Actions:
- (none) = Default/View
- Create
- Edit
- Delete
- {Custom} = Domain-specific actions
```

### Permission Table Template
```markdown
## {Resource} Permissions

| Permission | Description | Roles |
|------------|-------------|-------|
| `{Project}.{Resources}` | View {resources} | Admin, Manager, User |
| `{Project}.{Resources}.Create` | Create new {resource} | Admin, Manager |
| `{Project}.{Resources}.Edit` | Modify {resource} | Admin, Manager |
| `{Project}.{Resources}.Delete` | Delete {resource} | Admin |
| `{Project}.{Resources}.{Custom}` | [Custom action] | [Specific roles] |
```

## Role Definition Template

```markdown
## {Role}

**Description**: [Role purpose and scope]

### Capabilities
- [Capability 1]
- [Capability 2]
- [Capability 3]

### Permissions
| Resource | View | Create | Edit | Delete | Custom |
|----------|------|--------|------|--------|--------|
| Patients | ✓ | ✓ | ✓ | - | - |
| Doctors | ✓ | - | - | - | - |

### Restrictions
- [What this role cannot do]
- [Scope limitations]
```

## Impact Analysis Template

```markdown
# Impact Analysis: {Feature Name}

## Summary
| Metric | Count |
|--------|-------|
| New Entities | X |
| Modified Entities | Y |
| New Business Rules | Z |
| Modified Business Rules | W |
| New Permissions | N |
| Risk Level | Low/Medium/High |

## Entity Changes

### New Entities
| Entity | Reason | Relationships |
|--------|--------|---------------|
| {Entity} | [Why needed] | [Related to...] |

### Modified Entities
| Entity | Change | Before | After | Reason |
|--------|--------|--------|-------|--------|
| {Entity} | New property | - | `{Prop}: {Type}` | [Why] |
| {Entity} | New relationship | - | `{Nav}: {Target}` | [Why] |

## Business Rule Changes

### New Rules
| ID | Rule | Justification |
|----|------|---------------|
| BR-XXX-001 | [Rule] | [Why needed] |

### Modified Rules
| ID | Before | After | Reason | Risk |
|----|--------|-------|--------|------|
| BR-XXX-001 | [Old rule] | [New rule] | [Why] | Medium |

## Permission Changes
| Permission | Roles | Justification |
|------------|-------|---------------|
| `{Project}.{Resource}.{Action}` | [Roles] | [Why needed] |

## Affected Components
| Component | Impact | Action Required |
|-----------|--------|-----------------|
| `{Entity}AppService` | [Change type] | [Create/Modify] |

## Test Impact
| Existing Test | Impact | Action |
|---------------|--------|--------|
| `{Test}_Tests` | [Breaking/None] | [Update/None] |

## Risks & Concerns
| Concern | Severity | Mitigation |
|---------|----------|------------|
| [Issue] | Low/Medium/High | [How to address] |

## Stakeholder Sign-off Required
- [ ] Product Owner - [What needs approval]
- [ ] Tech Lead - [What needs approval]
- [ ] Security - [What needs approval]
```

## Relationship Patterns

### One-to-Many (1:N)
```
Parent Entity                Child Entity
┌─────────────┐             ┌─────────────┐
│ Doctor      │ 1 ────── N  │ Appointment │
│             │             │ DoctorId    │
└─────────────┘             └─────────────┘
```

### Many-to-Many (M:N via junction)
```
Entity A                    Junction                    Entity B
┌─────────────┐            ┌─────────────┐            ┌─────────────┐
│ Patient     │ 1 ──── N   │ PatientTag  │ N ──── 1  │ Tag         │
│             │            │ PatientId   │            │             │
│             │            │ TagId       │            │             │
└─────────────┘            └─────────────┘            └─────────────┘
```

## Quality Checklist

### Entity Definition
- [ ] All properties have type and constraints
- [ ] Relationships clearly defined with FK
- [ ] Business rules listed with BR-XXX IDs
- [ ] API access permissions mapped
- [ ] Sample data provided

### Business Rules
- [ ] Uses BR-{CAT}-{NNN} format
- [ ] Enforcement point specified
- [ ] Impact of violation documented
- [ ] Cross-referenced in entity files

### Permissions
- [ ] Follows naming convention
- [ ] Mapped to appropriate roles
- [ ] Custom actions documented

## References

- [references/entity-examples.md](references/entity-examples.md) - Real entity examples
- [references/rule-patterns.md](references/rule-patterns.md) - Common business rule patterns
