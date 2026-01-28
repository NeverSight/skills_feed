---
name: productivity-integration
description: Orchestrates cross-system productivity workflows between Things3 and Notion, providing automation patterns, integration strategies, and unified productivity methodologies for personal systems.
---

# Productivity Integration & Cross-System Workflows

## Overview

This skill orchestrates workflows between Things3 and Notion, providing unified productivity patterns that leverage the strengths of both systems for comprehensive personal productivity management.

**Keywords**: productivity integration, cross-system workflows, things3 notion integration, task documentation, workflow automation, personal systems

## Integration Philosophy

### System Roles
- **Things3**: Task execution, scheduling, and action management
- **Notion**: Documentation, planning, and knowledge management
- **Combined**: Comprehensive productivity system with clear boundaries

### Data Flow Patterns
- **Capture**: Quick entry in Things3 inbox for speed
- **Process**: Elaborate and document in Notion for complex items
- **Execute**: Track progress and completion in Things3
- **Archive**: Long-term storage and reference in Notion

## Core Integration Workflows

### Inbox Processing Workflow
1. **Capture** tasks quickly in Things3 inbox
2. **Review** inbox items using `read_tasks(when="inbox")`
3. **Migrate** complex notes to Notion using `migrate_inbox_to_notion`
4. **Process** remaining tasks through Things3 organization
5. **Reference** detailed documentation in Notion as needed

### Project Planning Integration
1. **Plan** projects and create documentation in Notion
2. **Extract** actionable tasks and create in Things3
3. **Link** between systems using consistent naming
4. **Track** progress in Things3 with reference to Notion docs
5. **Update** documentation based on execution learnings

### Review Cycle Integration
- **Daily**: Focus on Things3 Today view for execution
- **Weekly**: Review Things3 Someday + update Notion planning docs
- **Monthly**: Comprehensive review across both systems
- **Quarterly**: Strategic planning in Notion with Things3 area updates

## Automation Patterns

### MCP Tool Coordination
Available tools work together for seamless integration:

```
# Morning planning workflow
read_tasks(when="today", tags=["work"])
# Review today's work tasks

migrate_inbox_to_notion(block_id="...", include_titled=false)
# Process captured notes

create_task(title="Follow up on project", area="Work")
# Add new tasks from Notion planning
```

### Personal Context Integration
Both systems reference `private-prefs/personal-taxonomy.json`:
- **Work identification**: Consistent tagging across systems
- **Priority levels**: Aligned priority scales
- **Area organization**: Parallel structure maintenance
- **Common patterns**: Shared organizational preferences

## Advanced Integration Strategies

### Content Synchronization
- Use Things3 for task status and scheduling
- Use Notion for detailed context and documentation
- Maintain cross-references using consistent naming
- Avoid duplicating task content between systems

### Workflow Triggering
- **Notion → Things3**: Extract actionable items from planning docs
- **Things3 → Notion**: Migrate complex inbox items for elaboration
- **Bidirectional**: Update both systems during review cycles

### Context Preservation
- Link Things3 areas to corresponding Notion databases
- Use tags to maintain context across systems
- Reference Notion pages in Things3 notes when appropriate
- Maintain project coherence across both platforms

## Integration Best Practices

### Avoiding Duplication
- Single source of truth for each type of information
- Clear boundaries between task management and documentation
- Regular cleanup of outdated cross-references
- Consistent naming conventions across systems

### Maintaining Coherence
- Align area and project structures between systems
- Use consistent tagging and categorization
- Regular synchronization of organizational changes
- Clear workflows for updating both systems

### Personal Adaptation
This skill automatically adapts to:
- Personal work areas and professional context
- Individual priority and organizational preferences
- Existing workflow patterns and tool usage
- Integration points with other productivity systems

## Troubleshooting Integration

### Common Issues
- **Context switching overhead**: Minimize by batching operations
- **Inconsistent organization**: Regular alignment reviews
- **Information scatter**: Clear workflows for cross-system updates
- **Automation complexity**: Start simple, evolve gradually

### Resolution Strategies
- Establish clear system boundaries and responsibilities
- Create routine workflows for cross-system synchronization
- Use MCP tools to automate repetitive integration tasks
- Maintain documentation of integration patterns and decisions

This skill works in coordination with `things3-productivity` and `notion-workflows` skills to provide comprehensive productivity system management.