---
name: siebel-development
description: >
  Comprehensive Siebel CRM development skill for configuration, scripting, workflow, 
  and integration requirements. Use when: (1) Creating/modifying Siebel workflows,
  (2) Writing eScript or Business Services, (3) Configuring BCs, Applets, MVGs, Links,
  or Picklists, (4) Building REST/SOAP integrations, (5) Setting up Runtime Events,
  (6) Troubleshooting Siebel issues, or (7) Any Siebel CRM development task.
---

# Siebel Development

## Development Workflow

For any Siebel requirement, follow this approach. To start, use the **[New Requirement Workflow](commands/new-requirement.md)**.

1. **Understand** - Clarify the business requirement and identify affected objects
2. **Design** - Choose the right approach (Configuration vs Scripting vs Workflow)
3. **Implement** - Build using appropriate Siebel tools
4. **Test** - Validate in Siebel client
5. **Document** - Create implementation notes

## Skill-Building Framework (Mentorship Mode)

For complex requirements, create a `skill_building.md` using this 8-section framework:

### 1. Requirement Breakdown
- Rewrite in simple technical terms
- Categorize: UI / Data / Workflow / Integration / Security
- List assumptions & questions for BA

### 2. Impact Analysis
- Identify ALL impacted objects (BC, Applet, View, WF, LOV, Scripts)
- Explain WHY each is needed
- Highlight missed dependencies (e.g., Manifest registration)

### 3. Implementation Strategy
- Step-by-step in correct Siebel sequence
- Naming conventions
- Why this approach over alternatives

### 4. Skill Upgrade
- Concepts this requirement strengthens
- Advanced topic to study next
- Common mistakes to avoid

### 5. Edge Cases & Performance
- Possible edge cases
- Data integrity concerns
- Production issue prevention

### 6. Testing Strategy
- Unit test scenarios
- Negative tests
- Regression areas

### 7. Deployment Checklist
- Pre-deployment checks
- Migration steps
- Post-deployment validation

### 8. Interview Angle
- How to explain in an interview
- Senior-level talking points

## Documentation Organization Framework

When organizing raw requirements or messy notes into clean documentation, use this structure:

### Standard Sections
1. **Problem Statement** - Business need in 1-2 sentences
2. **Constraints & Assumptions** - Known limits, clarifications needed
3. **Solution Overview** - High-level approach
4. **Impacted Siebel Objects** - Table of BC, Applet, WF, LOV, etc.
5. **Implementation Steps** - Ordered, actionable steps
6. **Data Flow / Logic** - Pseudo-code or flowchart
7. **Risks & Edge Cases** - What could go wrong
8. **Testing Scenarios** - Unit, Negative, Regression
9. **Deployment Notes** - Pre/Post checks
10. **Key Learnings** - What you learned from this

### Naming & Filing
| Type | File Pattern | Folder |
|------|--------------|--------|
| New Feature | `YYYY-MM-DD-feature-name.md` | `requirements/` |
| Bug Fix | `YYYY-MM-DD-bug-description.md` | `requirements/` |
| Integration | `integration-<system>.md` | `requirements/` |
| Interview Prep | `topic-name.md` | `quick-reference/` |

### One-Glance Summary Template
End each document with 5-6 bullets for quick future reference:
```
## Quick Summary
- **What:** [Brief description]
- **Why:** [Business reason]
- **How:** [Key technical approach]
- **Objects:** [Main BCs/Applets]
- **Risk:** [Main concern]
- **Tags:** [searchable keywords]
```

## Repository Organization (Knowledge Architecture)

Use this framework when organizing raw content, migrating old files, or maintaining long-term structure.

### Folder Categories
| Category | Purpose | Example |
|----------|---------|--------|
| `development/requirements/` | Business requirements | `ai-leads-new-fields/` |
| `core-concepts/` | Fundamentals & Theory | `fundamentals/`, `workflows/` |
| `integration/` | Inbound/Outbound integration guides | `guides/`, `labs/` |
| `open-ui/` | PM, PR, Manifest notes | `presentation-model.md` |
| `quick-reference/` | Cheat sheets, one-pagers | `imp-workflow.md` |
| `rules/` | Non-negotiable standards | `naming.md` |
| `commands/` | Human workflow entry points | `new-requirement.md` |
| `code-snippets/` | Reusable patterns | `common-patterns.md` |

### Requirement Folder Structure
Each requirement should be a folder in `development/requirements/`.
For the mandatory structure and required files, see **[Requirement Structure Rule](rules/requirement-structure.md)**.

```
domain-name/
├── README.md           # Analysis, decision, interview guide (REQUIRED)
├── implementation.md   # Implementation steps & code (REQUIRED)
├── testing.md          # Verification steps (RECOMMENDED)
└── assets/             # Screenshots, diagrams
```

### Naming Conventions
For comprehensive naming rules (Files, Folders, and Siebel Objects), see **[Naming Conventions](rules/naming.md)**.

| Type | Pattern | Example |
|------|---------|--------|
| Requirement Folder | `domain-short-desc` | `mvg-multiselect-ui` |
| Completed Req | `completed-domain-short-desc` | `completed-mvg-multiselect-ui` |
| Guide File | `topic-name.md` | `workflows.md` |
| Lab File | `Lab-NN-short-desc.md` | `Lab-01-Outbound-REST.md` |

### Governance Files
| File | Purpose |
|------|---------|
| `DECISIONS.md` | Log architectural choices (Why we chose X) |
| `PATTERNS.md` | Extract reusable patterns from requirements |
| `LEARNING_LOG.md` | Track personal skill growth monthly |
| `CHANGELOG.md` | Repository history |

### Quality Checklist
- [ ] README has "How to Explain in Interview" section
- [ ] Key decisions logged in `DECISIONS.md`
- [ ] Reusable patterns added to `PATTERNS.md`
- [ ] Personal learnings added to `LEARNING_LOG.md`
- [ ] Folder renamed to `completed-*` upon finish

## Decision Guide


| Requirement Type | Primary Approach | Reference |
|------------------|------------------|-----------|
| Data automation on save/create | Runtime Event + Workflow | [workflows.md](references/workflows.md) |
| Field calculations/validations | BC Script or Calculated Field | [scripting.md](references/scripting.md) |
| External API calls | EAI HTTP Transport + BS | [integration.md](references/integration.md) |
| UI behavior changes | Applet Script or User Property | [configuration.md](references/configuration.md) |
| Scheduled/batch processing | Workflow Policy | [workflows.md](references/workflows.md) |
| Multi-step business process | Service Flow Workflow | [workflows.md](references/workflows.md) |

## Quick Patterns

### Trigger Workflow on Record Save
```
1. Create Workflow (Business Object = target BO)
2. Create Runtime Event:
   - Object Type: BusComp
   - Event: WriteRecord
   - Condition: [Field] = 'Value'
3. Create Action Set:
   - Service: Workflow Process Manager
   - Method: RunProcess
```

### Call REST API from Siebel
```
1. Create Business Service with eScript
2. Use EAI HTTP Transport:
   - Method: SendReceive
   - Set: HTTPRequestURLTemplate, HTTPRequestMethod, HTTPContentType
3. Parse response with Siebel XSL To XML Convertor (jsontops)
```

### Update Related Records in Workflow
```
1. Use Siebel Operation step:
   - Operation: Update
   - Business Component: [Target BC]
   - Search Spec: [Id] = &ProcessProperty
2. Set Field Input Arguments for fields to update
```

### Show/Hide Field Based on Another Field Value (Open UI)
```
1. Create Physical Renderer (PR) for the applet
2. Override ShowUI: Check field value, toggle visibility
3. Override FieldChange: Trigger toggle on field change
4. Use jQuery: $("[name='Field']").closest(".siebui-ctrl-wrap").show()/hide()
```

## Reference Files

Read the appropriate reference when working on specific domains:

| Domain | Reference | When to Read |
|--------|-----------|--------------|
| Workflows | [workflows.md](references/workflows.md) | Creating or modifying workflow processes, Runtime Events, or policies |
| Integration | [integration.md](references/integration.md) | REST/SOAP calls, EAI, Integration Objects |
| Scripting | [scripting.md](references/scripting.md) | eScript, Business Services, BC events |
| Configuration | [configuration.md](references/configuration.md) | BC, Applet, BO, Links, Picklists, MVGs |
| Runtime Events | [runtime-events.md](references/runtime-events.md) | Setting up triggers and action sets |
| Open UI | [open-ui.md](references/open-ui.md) | PM, PR, Plugin Wrappers, Manifest |
| Troubleshooting | [troubleshooting.md](references/troubleshooting.md) | Debugging issues, common errors |

## Key Siebel Objects Hierarchy

```
Application
└── Business Object (BO)
    └── Business Component (BC) ──► Table
        ├── Fields ──► Columns
        ├── Links ──► Parent-Child relationships
        └── Applet ──► UI display
```

## Common Business Services

| Service | Purpose |
|---------|---------|
| `EAI HTTP Transport` | REST/HTTP calls |
| `EAI Siebel Adapter` | Query/Insert/Update/Delete Siebel data |
| `Workflow Process Manager` | Run workflows programmatically |
| `Server Requests` | Async workflow execution |
| `Outbound Communications Manager` | Send emails |

## Best Practices Summary

1. **Configuration over Scripting:** Always prefer User Properties, Calculated Fields, and Workflows before writing eScript.
2. **Naming Convention:** Use `X_` prefix for custom columns, `_LBL` suffix for Symbolic Strings.
3. **Open UI:** Use Plugin Wrappers for field-level changes; Physical Renderers only for layout overhaul.
4. **Testing:** Always test in all supported locales before deployment.
5. **Manifest:** Double-check `manifest.xml` registration—silent failures are common.

