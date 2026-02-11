---
name: plugin-design
description: Master plugin user experience design, command workflows, and interaction patterns. Create intuitive, user-friendly plugin interfaces.
sasmp_version: "1.3.0"
bonded_agent: 03-plugin-designer
bond_type: PRIMARY_BOND
---

# Plugin Design

## Quick Start

Design commands users will love:

```markdown
# /create-plugin - Create new plugin

## What This Does
Creates a new plugin with guided setup.

## Usage
```
/create-plugin [name] [--type agent|command|skill]
```

## Example
```
$ /create-plugin my-plugin --type agent
Creating... ✅
Next: /design-plugin my-plugin
```
```

## Command Design Principles

### Clear & Discoverable

```
✅ /create-plugin          Clear action
✅ /design-plugin          Obvious purpose
✅ /test-plugin            Self-explanatory
✅ /optimize-plugin        What it does
```

### Consistent Naming

```
Verb-noun pattern:
├─ /create-X
├─ /design-X
├─ /test-X
└─ /optimize-X
```

## User Experience Patterns

### Interactive Workflow

```
User Input:
/create-plugin

System Response:
  1. What's your plugin name?
     > my-plugin

  2. Plugin type?
     [1] Agent-based
     [2] Command-based
     [3] Skill library
     > 1

  3. Number of agents?
     > 3

Output:
✅ Plugin created
Next: /design-plugin
```

### Progressive Disclosure

```
Beginner:
/create-plugin my-plugin
  (simple, guided)

Intermediate:
/create-plugin my-plugin --type agent --agents 3
  (more options)

Advanced:
/create-plugin --config config.json --skip-validation
  (all options)
```

## Error Message Design

### User-Friendly Errors

❌ Bad: `Invalid input`
✅ Good: `Plugin name must be 3-50 characters, lowercase, hyphens only`

❌ Bad: `Error 500`
✅ Good: `Plugin creation failed: skill-one not found in agents/`

❌ Bad: `Fatal error`
✅ Good: `Missing required field 'description' in plugin.json`

## Interface Patterns

### Success Feedback

```
✅ Task completed
├─ What was done
├─ Where to find it
└─ What's next
```

### Warnings

```
⚠️  Warning: Using old syntax
├─ Recommendation: Update to new syntax
└─ Link: /help/migration-guide
```

### Errors

```
❌ Error: Manifest invalid
├─ Issue: Missing "author" field
├─ Fix: Add "author": "Your Name"
└─ Help: /help/plugin-json
```

## Consistency Standards

### Visual Hierarchy

```
✅ Success (green)
⚠️  Warning (yellow)
❌ Error (red)
ℹ️  Info (blue)
→ Action (arrow)
```

### Message Format

```
[Icon] [Brief message]
├─ [Detail 1]
├─ [Detail 2]
└─ [Action or suggestion]
```

## Navigation Design

### Command Discovery

```
Help:
├─ /help                 Show all commands
├─ /help /create-plugin  Help for specific command
└─ /help --agents        List all agents

Related:
├─ Run: /create-plugin
├─ Then: /design-plugin
└─ Then: /test-plugin
```

### Intelligent Suggestions

```
After /create-plugin:
→ Suggestion: Run /design-plugin next
  (natural workflow progression)

After /test-plugin:
→ Suggestion: Run /optimize-plugin
  (next logical step)
```

## Accessibility Design

### Clear Language

```
✅ Simple words
✅ Short sentences
✅ Active voice
✅ No jargon

❌ "Facilitate optimization"
✅ "Make faster"
```

### Visual Clarity

```
✅ Good contrast
✅ Large text
✅ Clear structure
✅ Readable font
```

### Keyboard Navigation

```
✅ All commands accessible via keyboard
✅ No mouse required
✅ Clear keyboard shortcuts
```

## Feedback Mechanisms

### Immediate Feedback

```
User types: /create
System shows: Available commands starting with 'create'
  ├─ /create-plugin
  ├─ /create-agent
  └─ /create-skill
```

### Progress Indication

```
Creating plugin...
  ⠋ Creating folders
  ✅ Folders created
  ⠙ Writing files
  ✅ Files written
  ⠹ Validating structure
  ✅ Validation complete
✅ Done!
```

### Confirmation

```
Are you sure you want to delete my-plugin?
(This cannot be undone)

[Yes, delete]  [No, cancel]
```

## Workflow Patterns

### Simple Linear

```
/create → /design → /test → /deploy
```

### Branching

```
/test
  ├─ Tests pass → /deploy
  └─ Tests fail → Fix issues → /test again
```

### Exploratory

```
/explore-agents
  ├─ Agent details
  └─ Related agents
```

## Help System

### Context-Sensitive Help

```
After error:
❌ Skill name invalid
💡 Need help?
  ├─ Show format examples
  ├─ Visit docs
  └─ Ask @plugin-developer
```

### Progressive Complexity

```
Level 1: What does this command do?
Level 2: How do I use it?
Level 3: What options are available?
Level 4: Advanced use cases?
```

## User Feedback Integration

### Suggestions

```
Users often ask about:
├─ "How do I structure my plugin?"
  → /design-plugin command
└─ "How do I test it?"
  → /test-plugin command
```

### Common Issues

```
We notice users struggle with:
├─ JSON formatting
  → Add JSON validation
└─ Naming conventions
  → Add clear examples
```

---

**Use this skill when:**
- Designing commands
- Planning workflows
- Creating help systems
- Improving user experience
- Designing error messages

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 03-plugin-designer
