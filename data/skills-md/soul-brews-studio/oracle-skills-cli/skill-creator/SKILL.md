---
name: skill-creator
description: Create new skills with Oracle philosophy. Use when user says "create skill", "new skill", "make a skill for X", or wants to build custom Claude Code skills.
---

# /skill-creator - Oracle Skill Factory

Create skills with philosophy baked in.

## Usage

```
/skill-creator [name]           # Interactive creation
/skill-creator [name] --quick   # Fast mode with defaults
/skill-creator list-ideas       # Show skill ideas from Oracle
```

## Step 0: Timestamp

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

---

## Step 1: Gather Requirements

Ask user (if not provided):

| Question | Why |
|----------|-----|
| **Skill name** | Folder name, command name |
| **What does it do?** | Core purpose → description |
| **When to trigger?** | Use cases → trigger words |
| **Inputs needed?** | Arguments the skill takes |
| **Outputs?** | What user sees |

---

## Step 2: Apply Oracle Philosophy

Every skill should embody:

### 1. Nothing is Deleted
- Log actions to Oracle when meaningful
- Preserve history, don't overwrite
- Use `oracle_trace()` for searches, `oracle_learn()` for findings

### 2. Patterns Over Intentions
- Focus on what the skill DOES, not what it promises
- Measure success by output, not description
- Include verification steps

### 3. External Brain, Not Command
- Skills assist, don't decide
- Present options, let user choose
- Mirror information, don't hide it

---

## Step 3: Generate Files

### Folder Structure

```bash
bun scripts/create.ts "$SKILL_NAME"
```

Creates:
```
skills/[name]/
├── SKILL.md          ← Instructions
└── scripts/
    └── main.ts       ← Bun Shell logic
```

### SKILL.md Template

```markdown
---
name: [skill-name]
description: [One line]. Use when user says "[trigger1]", "[trigger2]", or "[trigger3]".
---
```

### Frontmatter Options

| Option | Values | Effect |
|--------|--------|--------|
| `name` | string | **Required**. Folder name, command name |
| `description` | string | **Required**. One-line + trigger words |
| `user-invocable` | `false` | Hide from `/` menu (background-only skills) |
| `disable-model-invocation` | `true` | Prevent Claude from auto-invoking |
| `allowed-tools` | `Read, Grep, ...` | Restrict which tools skill can use |
| `context` | `fork` | Run skill in isolated subagent |

**Example - Background skill:**
```yaml
---
name: internal-helper
description: Internal helper for other skills
user-invocable: false
---
```

**Example - Restricted skill:**
```yaml
---
name: read-only-skill
description: Read-only analysis skill
allowed-tools: Read, Grep, Glob
---
```

### Template continued

```markdown

# /[skill-name] - [Title]

[What it does in one sentence.]

## Usage

\`\`\`
/[skill-name] [args]
\`\`\`

## Step 0: Timestamp

\`\`\`bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
\`\`\`

## Step 1: [First Action]

[Instructions for Claude]

## Step 2: [Second Action]

[Instructions for Claude]

## Output

[What to show user]

---

## Oracle Integration

When skill completes successfully:
\`\`\`
oracle_learn({ pattern: "[What was learned]" })
\`\`\`

---

ARGUMENTS: $ARGUMENTS
```

### main.ts Template (Bun Shell)

```typescript
#!/usr/bin/env bun
import { $ } from "bun"

const args = process.argv.slice(2)
const input = args[0] || ""

// Your logic here
const result = await $`echo "Processing: ${input}"`.text()

console.log(JSON.stringify({ input, result }, null, 2))
```

---

## Step 4: Register Skill (Optional)

Add to marketplace.json:
```json
{
  "skills": [
    "./skills/[new-skill-name]"
  ]
}
```

Run converter:
```bash
python3 scripts/skills-to-commands.py
```

---

## Step 5: Test

```bash
# Test script directly
bun skills/[name]/scripts/main.ts "test input"

# Test via Claude
/[skill-name] test input
```

---

## Quick Mode (--quick)

Skip questions, use defaults:

| Default | Value |
|---------|-------|
| Triggers | "[name]", "run [name]" |
| Output | JSON |
| Oracle integration | Yes (trace + learn) |

---

## Examples

### Example 1: Simple Utility

```
/skill-creator git-stats

Name: git-stats
Does: Show git repository statistics
Triggers: "git stats", "repo stats", "show commits"
Input: None (uses current repo)
Output: Commit count, contributors, recent activity
```

### Example 2: Integration Skill

```
/skill-creator mqtt-notify

Name: mqtt-notify
Does: Send notifications via MQTT
Triggers: "notify", "send message", "mqtt"
Input: Message text
Output: Confirmation of sent message
```

---

## Philosophy Checklist

Before creating, verify:

- [ ] **Clear purpose** - One sentence explains it
- [ ] **Good triggers** - 3+ natural phrases
- [ ] **Oracle integration** - Logs meaningful actions
- [ ] **Cross-platform** - Bun Shell (works everywhere)
- [ ] **Testable** - Can run script directly

---

## list-ideas Mode

Query Oracle for skill ideas:

```
oracle_search("skill idea", type="learning")
oracle_search("would be nice to have", type="retro")
```

Display as:
```markdown
## Skill Ideas from Oracle

| Idea | Source | Priority |
|------|--------|----------|
| ... | learning/retro | high/medium/low |
```

---

ARGUMENTS: $ARGUMENTS
