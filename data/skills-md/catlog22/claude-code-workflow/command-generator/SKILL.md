---
name: command-generator
description: Command file generator - 5 phase workflow for creating Claude Code command files with YAML frontmatter. Generates .md command files for project or user scope. Triggers on "create command", "new command", "command generator".
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Command Generator

CLI-based command file generator producing Claude Code command .md files through a structured 5-phase workflow. Supports both project-level (`.claude/commands/`) and user-level (`~/.claude/commands/`) command locations.

## Architecture Overview

```
+-----------------------------------------------------------+
|                    Command Generator                        |
|                                                            |
|  Input: skillName, description, location, [group], [hint]  |
|                         |                                  |
|  +-------------------------------------------------+      |
|  |  Phase 1-5: Sequential Pipeline                 |      |
|  |                                                 |      |
|  |  [P1] --> [P2] --> [P3] --> [P4] --> [P5]      |      |
|  |  Param   Target   Template  Content   File     |      |
|  |  Valid   Path     Loading   Format    Gen      |      |
|  +-------------------------------------------------+      |
|                         |                                  |
|  Output: {scope}/.claude/commands/{group}/{name}.md       |
|                                                            |
+-----------------------------------------------------------+
```

## Key Design Principles

1. **Single Responsibility**: Generates one command file per invocation
2. **Scope Awareness**: Supports project and user-level command locations
3. **Template-Driven**: Uses consistent template for all generated commands
4. **Validation First**: Validates all required parameters before file operations
5. **Non-Destructive**: Warns if command file already exists

---

## Execution Flow

```
Phase 1: Parameter Validation
   - Ref: phases/01-parameter-validation.md
   - Validate: skillName (required), description (required), location (required)
   - Optional: group, argumentHint
   - Output: validated params object

Phase 2: Target Path Resolution
   - Ref: phases/02-target-path-resolution.md
   - Resolve: location -> target commands directory
   - Support: project (.claude/commands/) vs user (~/.claude/commands/)
   - Handle: group subdirectory if provided
   - Output: targetPath string

Phase 3: Template Loading
   - Ref: phases/03-template-loading.md
   - Load: templates/command-md.md
   - Template contains YAML frontmatter with placeholders
   - Output: templateContent string

Phase 4: Content Formatting
   - Ref: phases/04-content-formatting.md
   - Substitute: {{name}}, {{description}}, {{group}}, {{argumentHint}}
   - Handle: optional fields (group, argumentHint)
   - Output: formattedContent string

Phase 5: File Generation
   - Ref: phases/05-file-generation.md
   - Check: file existence (warn if exists)
   - Write: formatted content to target path
   - Output: success confirmation with file path
```

## Usage Examples

### Basic Command (Project Scope)
```javascript
Skill(skill="command-generator", args={
  skillName: "deploy",
  description: "Deploy application to production environment",
  location: "project"
})
// Output: .claude/commands/deploy.md
```

### Grouped Command with Argument Hint
```javascript
Skill(skill="command-generator", args={
  skillName: "create",
  description: "Create new issue from GitHub URL or text",
  location: "project",
  group: "issue",
  argumentHint: "[-y|--yes] <github-url | text-description> [--priority 1-5]"
})
// Output: .claude/commands/issue/create.md
```

### User-Level Command
```javascript
Skill(skill="command-generator", args={
  skillName: "global-status",
  description: "Show global Claude Code status",
  location: "user"
})
// Output: ~/.claude/commands/global-status.md
```

---

## Reference Documents by Phase

### Phase 1: Parameter Validation
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/01-parameter-validation.md](phases/01-parameter-validation.md) | Validate required parameters | Phase 1 execution |

### Phase 2: Target Path Resolution
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/02-target-path-resolution.md](phases/02-target-path-resolution.md) | Resolve target directory | Phase 2 execution |

### Phase 3: Template Loading
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/03-template-loading.md](phases/03-template-loading.md) | Load command template | Phase 3 execution |
| [templates/command-md.md](templates/command-md.md) | Command file template | Template reference |

### Phase 4: Content Formatting
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/04-content-formatting.md](phases/04-content-formatting.md) | Format content with params | Phase 4 execution |

### Phase 5: File Generation
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [phases/05-file-generation.md](phases/05-file-generation.md) | Write final file | Phase 5 execution |

### Design Specifications
| Document | Purpose | When to Use |
|----------|---------|-------------|
| [specs/command-design-spec.md](specs/command-design-spec.md) | Command design guidelines | Understanding best practices |

---

## Output Structure

### Generated Command File

```markdown
---
name: {skillName}
description: {description}
{group} {argumentHint}
---

# {skillName} Command

## Overview
{Auto-generated placeholder for command overview}

## Usage
{Auto-generated placeholder for usage examples}

## Execution Flow
{Auto-generated placeholder for execution steps}
```

---

## Error Handling

| Error | Stage | Action |
|-------|-------|--------|
| Missing skillName | Phase 1 | Error: "skillName is required" |
| Missing description | Phase 1 | Error: "description is required" |
| Missing location | Phase 1 | Error: "location is required (project or user)" |
| Invalid location | Phase 2 | Error: "location must be 'project' or 'user'" |
| Template not found | Phase 3 | Error: "Command template not found" |
| File exists | Phase 5 | Warning: "Command file already exists, will overwrite" |
| Write failure | Phase 5 | Error: "Failed to write command file" |

---

## Related Skills

- **skill-generator**: Create complete skills with phases, templates, and specs
- **flow-coordinator**: Orchestrate multi-step command workflows
