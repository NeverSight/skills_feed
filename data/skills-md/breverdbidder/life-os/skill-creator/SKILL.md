---
name: skill-creator
description: Guide for creating effective skills that extend Claude's capabilities
---

# Skill Creator

Build custom Claude skills for repetitive workflows.

## Process

### 1. Identify Use Cases
Collect 3-5 concrete examples when skill would be used.

### 2. Determine Contents
- **SKILL.md** (required): Instructions
- **scripts/** (optional): Python/bash executables
- **references/** (optional): Documentation
- **assets/** (optional): Templates, boilerplate

### 3. Write SKILL.md
```yaml
---
name: skill-name
description: Clear 1-2 sentence description
---

# Skill Name

## When to Use This Skill
- Use case 1
- Use case 2

## Instructions
Step-by-step guidance for Claude

## Examples
Concrete examples with inputs/outputs
```

### 4. Keep Minimal
Only include what Claude needs to execute.

## Usage
```
"Use skill creator to build Supabase integration skill"
```
