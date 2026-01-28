---
name: component-architect
description: |
  Enforces official Claude Code component standards. Use when creating skills,
  agents, commands, or hooks. Validates existing components and offers remediation.
  Implements the "one skill = one specialized agent" architecture pattern.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: sonnet
context: fork
agent: component-architect-agent
user-invocable: true
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "$HOME/.claude/skills/component-architect/scripts/validate-component.sh"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "$HOME/.claude/skills/component-architect/scripts/log-component.sh"
---

# Component Architect

## Core Responsibilities

1. **Pre-Creation Validation**: Check official docs before generating any component
2. **Existing Component Audit**: Scan ~/.claude for non-compliant components
3. **Remediation Orchestration**: Spawn subagents to fix non-compliant files
4. **Architecture Enforcement**: Apply "one skill = one specialized agent" pattern

## Official Frontmatter Reference

| Component | Required | Optional |
|-----------|----------|----------|
| SKILL.md | name, description | allowed-tools, model, context, agent, hooks, user-invocable |
| Agent .md | name, description | tools, disallowedTools, model, permissionMode, skills, hooks |
| Command .md | (none) | description, allowed-tools, model, argument-hint |
| plugin.json | name, description | author |
| hooks.json | hooks object | description |

## Validation Commands

### Validate All Components
```bash
/component-architect validate
```

### Validate Specific Type
```bash
/component-architect validate --type skills
/component-architect validate --type agents
/component-architect validate --type hooks
```

### Apply Architecture Pattern
```bash
/component-architect apply-pattern --skill skill-name
```

## Architecture Pattern: One Skill = One Agent

For every active skill:
1. Set `context: fork` in SKILL.md
2. Create designated agent with matching name pattern
3. Configure agent with:
   - Intelligent `model` selection based on task complexity
   - Appropriate `permissionMode` for the workflow
   - Complementary `skills` that enhance the primary skill
   - Scoped `hooks` for lifecycle management
   - Restricted `tools` appropriate to the domain

### Model Selection Matrix

| Complexity | Model | Indicators |
|------------|-------|------------|
| High | opus | Architecture, debugging, multi-domain reasoning |
| Medium | sonnet | Implementation, refactoring, moderate analysis |
| Low | haiku | Searches, simple transforms, quick lookups |
| Inherited | inherit | When parent context model is appropriate |

### Permission Mode Selection Matrix

| Scenario | Mode | Use When |
|----------|------|----------|
| Complex multi-step | plan | High complexity requiring human feedback before implementation |
| Edge case handling | acceptEdits | Potential edge cases need user confirmation on edits |
| Routine execution | bypassPermissions | Clear requirements, preplanned, or promise completion |
| Standard workflow | default | Normal permission checking with prompts |
| Deny risky ops | dontAsk | Auto-deny prompts (explicitly allowed tools still work) |

## Remediation Workflow

1. Scan component directories for non-compliant files
2. Generate remediation plan per file
3. Spawn parallel subagents for batch updates
4. Verify all changes post-remediation

## Integration References

- [scripts/validate-component.sh](scripts/validate-component.sh) - PreToolUse validation
- [scripts/log-component.sh](scripts/log-component.sh) - PostToolUse logging
- [scripts/audit-components.py](scripts/audit-components.py) - Full audit script
- [references/official-spec.md](references/official-spec.md) - Cached official docs
