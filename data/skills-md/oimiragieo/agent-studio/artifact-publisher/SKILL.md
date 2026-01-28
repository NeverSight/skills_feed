---
name: artifact-publisher
description: Publish and share artifacts to the project. Use when a user wants to save, share, or finalize generated artifacts.
version: 2.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Version all artifacts
  - Include metadata (date, author, purpose)
  - Save to appropriate artifacts directory
  - Link related artifacts
error_handling: graceful
streaming: supported
---

# Artifact Publisher Skill

<identity>
Artifact Publisher - Handles the lifecycle of artifacts, ensuring they are properly versioned, saved, and documented.
</identity>

<capabilities>
- Saving artifacts to project directories
- Versioning artifact files
- Adding metadata to artifacts
- Linking related artifacts
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Artifact Type

Determine the artifact type and appropriate location:

| Type         | Location                     | Format                    |
| ------------ | ---------------------------- | ------------------------- |
| Plan         | `.claude/context/plans/`     | `plan-{id}.md`            |
| Report       | `.claude/context/reports/`   | `report-{type}-{date}.md` |
| Architecture | `.claude/context/artifacts/` | `architecture-{name}.md`  |
| Schema       | `.claude/context/artifacts/` | `schema-{name}.json`      |
| Config       | `.claude/context/artifacts/` | `config-{name}.yaml`      |

### Step 2: Add Metadata

Include standard metadata in the artifact:

```markdown
---
id: artifact-{timestamp}
type: plan|report|architecture|schema|config
title: Artifact Title
created: 2026-01-23T12:00:00Z
author: agent-name
workflow_id: workflow-123
status: draft|final
tags: [tag1, tag2]
---
```

### Step 3: Save Artifact

Write the artifact to the appropriate location:

```bash
# Example: Save a plan artifact
Write file_path=".claude/context/plans/plan-auth-2026-01-23.md" content="..."
```

### Step 4: Update References

If the artifact is part of a workflow, update the workflow documentation:

```markdown
## Artifacts

- Plan: `.claude/context/plans/plan-auth-2026-01-23.md`
- Architecture: `.claude/context/artifacts/architecture-auth.md`
```

### Step 5: Notify Completion

Report the artifact location:

```markdown
## Artifact Published

**Type**: Plan
**Location**: `.claude/context/plans/plan-auth-2026-01-23.md`
**Status**: Final
```

</execution_process>

<best_practices>

1. **Consistent Naming**: Use `{type}-{name}-{date}` format
2. **Include Metadata**: Always add creation date and author
3. **Version Important Artifacts**: Keep history of major changes
4. **Link Dependencies**: Reference related artifacts
5. **Use Appropriate Directory**: Follow project conventions

</best_practices>
</instructions>

<examples>
<usage_example>
**Publish Request**:

```
Save this architecture design as a final artifact
```

**Response**:

```markdown
## Artifact Published

**Type**: Architecture
**Title**: User Authentication System
**Location**: `.claude/context/artifacts/architecture-auth-2026-01-23.md`
**Status**: Final

### Metadata

- Created: 2026-01-23T12:00:00Z
- Author: architect
- Tags: authentication, security, jwt
```

</usage_example>
</examples>

## Rules

- Always include metadata in artifacts
- Use consistent naming conventions
- Save to appropriate project directories

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
