---
name: reflect
description: >
  Self-improving skill that analyzes conversations for corrections and preferences, then persists 
  them to skill files with optional Git versioning. Use when: (1) User runs "/reflect" or 
  "/reflect [skill-name]" to manually extract learnings, (2) User says "reflect on" or "reflect off" 
  to toggle automatic reflection, (3) User says "reflect status" to check mode, (4) User wants 
  Claude to remember corrections for future sessions. Supports manual and automatic (hook-based) modes.
---

# Reflect Skill

Analyze conversations to extract corrections, preferences, and best practices, then persist them to skill files. Supports manual triggering, automatic hooks, and Git versioning.

## Commands

| Command | Description |
|---------|-------------|
| `/reflect` | Analyze current session and propose skill updates |
| `/reflect [skill-name]` | Reflect and update a specific skill |
| `reflect on` | Enable automatic reflection via stop hook |
| `reflect off` | Disable automatic reflection |
| `reflect status` | Show current reflection mode |

## Manual Reflection Flow

### 1. Analyze Session for Signals

Scan the conversation and categorize by confidence:

**HIGH Confidence** - Explicit corrections
- "No, use X instead of Y"
- "Never [action] in this project"  
- "Always check for [condition]"

**MEDIUM Confidence** - Success patterns
- Approaches that worked after iteration
- Patterns user approved or praised

**LOW Confidence** - Observations
- Implied preferences
- Patterns to review later

### 2. Present Review & Approval

```
📊 Signals Detected:

HIGH CONFIDENCE:
- "Never generate button styles - reference existing components"
- "Always check for SQL injections"

MEDIUM CONFIDENCE:
- Arrow functions preferred for callbacks

LOW CONFIDENCE:
- Prefers concise explanations

📝 Proposed Changes to [skill-name].md:

+ ## Security
+ - Always validate database queries for SQL injection
+
+ ## Code Style  
+ - Never generate UI components; reference existing library

💬 Commit message: "Add SQL injection and UI component rules"

Accept changes? [Y/n/edit with natural language]
```

User options:
- `Y` - Accept all changes
- `n` - Reject
- Natural language: "Remove the arrow function one" or "Change the wording to..."

### 3. Update Skill & Commit

1. Locate target skill file (project or `~/.claude/skills/`)
2. Merge new learnings (newer rules override conflicts)
3. If Git repo: stage, commit with message, push

## Automatic Reflection

### Toggle Commands

```bash
reflect on      # Enable auto-reflection on session end
reflect off     # Disable auto-reflection
reflect status  # Check current mode
```

### How It Works

When enabled, the stop hook triggers automatic learning:

1. Session ends → stop hook fires
2. Analyzes conversation for learnings
3. Updates skill file (shows notification: "Learned from session: [skill-name]")
4. Commits to Git if configured

### Hook Configuration

The session-end hook is **auto-registered** when you install this plugin. No manual configuration needed.

State stored in `~/.claude/.reflect-state` (enabled/disabled).

## Git Integration

Version your skills to track evolution over time:

```bash
cd ~/.claude/skills
git init
git remote add origin <your-repo>
```

Benefits:
- See how skills evolve with each learning
- Rollback if a learning causes regressions  
- Track system improvement over time

## Learning Categories

| Category | Examples |
|----------|----------|
| Code Style | Naming conventions, formatting |
| Security | Input validation, SQL injection |
| Testing | Coverage requirements, edge cases |
| API Design | Endpoint conventions, responses |
| UI/UX | Component usage, accessibility |
| Workflow | PR process, commit format |

## Example

```
You: Review the auth module
Claude: [Reviews, misses SQL injection]
You: You missed SQL injection - always check for that

You: /reflect

Claude: 📊 HIGH: "Always check for SQL injections"
        
        📝 Proposed for security-review.md:
        + - Validate all database queries for SQL injection
        
        Accept? [Y/n]

You: Y

Claude: ✅ Updated security-review.md
        📤 Committed: "Add SQL injection validation rule"
```

Next session: Claude automatically checks for SQL injection.

## Goal

**Correct once, never again.** Build a self-improving system where learnings persist and compound over time.
