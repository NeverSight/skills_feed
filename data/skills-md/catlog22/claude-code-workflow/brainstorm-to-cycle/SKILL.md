---
name: brainstorm-to-cycle
description: Convert brainstorm session output to parallel-dev-cycle input with idea selection and context enrichment. Unified parameter format.
argument-hint: "--session=<id> [--idea=<index>] [--auto] [--launch]"
---

# Brainstorm to Cycle Adapter

## Overview

Bridge workflow that converts **brainstorm-with-file** output to **parallel-dev-cycle** input. Reads synthesis.json, allows user to select an idea, and formats it as an enriched TASK description.

**Core workflow**: Load Session → Select Idea → Format Task → Launch Cycle

## Inputs

| Argument | Required | Description |
|----------|----------|-------------|
| --session | Yes | Brainstorm session ID (e.g., `BS-rate-limiting-2025-01-28`) |
| --idea | No | Pre-select idea by index (0-based, from top_ideas) |
| --auto | No | Auto-select top-scored idea without confirmation |
| --launch | No | Auto-launch parallel-dev-cycle without preview |

## Output

Launches `/parallel-dev-cycle` with enriched TASK containing:
- Primary recommendation or selected idea
- Key strengths and challenges
- Suggested implementation steps
- Alternative approaches for reference

## Execution Process

```
Phase 1: Session Loading
   ├─ Validate session folder exists
   ├─ Read synthesis.json
   ├─ Parse top_ideas and recommendations
   └─ Validate data structure

Phase 2: Idea Selection
   ├─ --auto mode → Select highest scored idea
   ├─ --idea=N → Select specified index
   └─ Interactive → Present options, await selection

Phase 3: Task Formatting
   ├─ Build enriched task description
   ├─ Include context from brainstorm
   └─ Generate parallel-dev-cycle command

Phase 4: Cycle Launch
   ├─ Confirm with user (unless --auto)
   └─ Execute parallel-dev-cycle
```

## Implementation

### Phase 1: Session Loading

##### Step 0: Determine Project Root

检测项目根目录，确保 `.workflow/` 产物位置正确：

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

优先通过 git 获取仓库根目录；非 git 项目回退到 `pwd` 取当前绝对路径。
存储为 `{projectRoot}`，后续所有 `.workflow/` 路径必须以此为前缀。

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()
const projectRoot = bash('git rev-parse --show-toplevel 2>/dev/null || pwd').trim()

// Parse arguments
const args = "$ARGUMENTS"
const sessionId = "$SESSION"
const ideaIndexMatch = args.match(/--idea=(\d+)/)
const preSelectedIdea = ideaIndexMatch ? parseInt(ideaIndexMatch[1]) : null
const isAutoMode = args.includes('--auto')

// Validate session
const sessionFolder = `${projectRoot}/.workflow/.brainstorm/${sessionId}`
const synthesisPath = `${sessionFolder}/synthesis.json`
const brainstormPath = `${sessionFolder}/brainstorm.md`

function fileExists(p) {
  try { return bash(`test -f "${p}" && echo "yes"`).includes('yes') } catch { return false }
}

if (!fileExists(synthesisPath)) {
  console.error(`
## Error: Session Not Found

Session ID: ${sessionId}
Expected path: ${synthesisPath}

**Available sessions**:
`)
  bash(`ls -1 ${projectRoot}/.workflow/.brainstorm/ 2>/dev/null | head -10`)
  return { status: 'error', message: 'Session not found' }
}

// Load synthesis
const synthesis = JSON.parse(Read(synthesisPath))

// Validate structure
if (!synthesis.top_ideas || synthesis.top_ideas.length === 0) {
  console.error(`
## Error: No Ideas Found

The brainstorm session has no top_ideas.
Please complete the brainstorm workflow first.
`)
  return { status: 'error', message: 'No ideas in synthesis' }
}

console.log(`
## Brainstorm Session Loaded

**Session**: ${sessionId}
**Topic**: ${synthesis.topic}
**Completed**: ${synthesis.completed}
**Ideas Found**: ${synthesis.top_ideas.length}
`)
```

---

### Phase 2: Idea Selection

```javascript
let selectedIdea = null
let selectionSource = ''

// Auto mode: select highest scored
if (isAutoMode) {
  selectedIdea = synthesis.top_ideas.reduce((best, idea) =>
    idea.score > best.score ? idea : best
  )
  selectionSource = 'auto (highest score)'

  console.log(`
**Auto-selected**: ${selectedIdea.title} (Score: ${selectedIdea.score}/10)
`)
}

// Pre-selected by index
else if (preSelectedIdea !== null) {
  if (preSelectedIdea >= synthesis.top_ideas.length) {
    console.error(`
## Error: Invalid Idea Index

Requested: --idea=${preSelectedIdea}
Available: 0 to ${synthesis.top_ideas.length - 1}
`)
    return { status: 'error', message: 'Invalid idea index' }
  }

  selectedIdea = synthesis.top_ideas[preSelectedIdea]
  selectionSource = `index ${preSelectedIdea}`

  console.log(`
**Pre-selected**: ${selectedIdea.title} (Index: ${preSelectedIdea})
`)
}

// Interactive selection
else {
  // Display options
  console.log(`
## Select Idea for Development

| # | Title | Score | Feasibility |
|---|-------|-------|-------------|
${synthesis.top_ideas.map((idea, i) =>
  `| ${i} | ${idea.title.substring(0, 40)} | ${idea.score}/10 | ${idea.feasibility || 'N/A'} |`
).join('\n')}

**Primary Recommendation**: ${synthesis.recommendations?.primary?.substring(0, 60) || 'N/A'}
`)

  // Build options for AskUser
  const ideaOptions = synthesis.top_ideas.slice(0, 4).map((idea, i) => ({
    label: `#${i}: ${idea.title.substring(0, 30)}`,
    description: `Score: ${idea.score}/10 - ${idea.description?.substring(0, 50) || ''}`
  }))

  // Add primary recommendation option if different
  if (synthesis.recommendations?.primary) {
    ideaOptions.unshift({
      label: "Primary Recommendation",
      description: synthesis.recommendations.primary.substring(0, 60)
    })
  }

  const selection = ASK_USER([{
    id: "idea", type: "select",
    prompt: "Which idea should be developed?",
    options: ideaOptions
  }])  // BLOCKS (wait for user response)

  // Parse selection
  if (selection.idea === "Primary Recommendation") {
    // Use primary recommendation as task
    selectedIdea = {
      title: "Primary Recommendation",
      description: synthesis.recommendations.primary,
      key_strengths: synthesis.key_insights || [],
      main_challenges: [],
      next_steps: synthesis.follow_up?.filter(f => f.type === 'implementation').map(f => f.summary) || []
    }
    selectionSource = 'primary recommendation'
  } else {
    const match = selection.idea.match(/^#(\d+):/)
    const idx = match ? parseInt(match[1]) : 0
    selectedIdea = synthesis.top_ideas[idx]
    selectionSource = `user selected #${idx}`
  }
}

console.log(`
### Selected Idea

**Title**: ${selectedIdea.title}
**Source**: ${selectionSource}
**Description**: ${selectedIdea.description?.substring(0, 200) || 'N/A'}
`)
```

---

### Phase 3: Task Formatting

```javascript
// Build enriched task description
function formatTask(idea, synthesis) {
  const sections = []

  // Main objective
  sections.push(`# Main Objective\n\n${idea.title}`)

  // Description
  if (idea.description) {
    sections.push(`# Description\n\n${idea.description}`)
  }

  // Key strengths
  if (idea.key_strengths?.length > 0) {
    sections.push(`# Key Strengths\n\n${idea.key_strengths.map(s => `- ${s}`).join('\n')}`)
  }

  // Main challenges (important for RA agent)
  if (idea.main_challenges?.length > 0) {
    sections.push(`# Main Challenges to Address\n\n${idea.main_challenges.map(c => `- ${c}`).join('\n')}`)
  }

  // Recommended steps
  if (idea.next_steps?.length > 0) {
    sections.push(`# Recommended Implementation Steps\n\n${idea.next_steps.map((s, i) => `${i + 1}. ${s}`).join('\n')}`)
  }

  // Alternative approaches (for RA consideration)
  if (synthesis.recommendations?.alternatives?.length > 0) {
    sections.push(`# Alternative Approaches (for reference)\n\n${synthesis.recommendations.alternatives.map(a => `- ${a}`).join('\n')}`)
  }

  // Key insights from brainstorm
  if (synthesis.key_insights?.length > 0) {
    const relevantInsights = synthesis.key_insights.slice(0, 3)
    sections.push(`# Key Insights from Brainstorm\n\n${relevantInsights.map(i => `- ${i}`).join('\n')}`)
  }

  // Source reference
  sections.push(`# Source\n\nBrainstorm Session: ${synthesis.session_id}\nTopic: ${synthesis.topic}`)

  return sections.join('\n\n')
}

const enrichedTask = formatTask(selectedIdea, synthesis)

// Display formatted task
console.log(`
## Formatted Task for parallel-dev-cycle

\`\`\`markdown
${enrichedTask}
\`\`\`
`)

// Save task to session folder for reference
Write(`${sessionFolder}/cycle-task.md`, `# Generated Task\n\n**Generated**: ${getUtc8ISOString()}\n**Idea**: ${selectedIdea.title}\n**Selection**: ${selectionSource}\n\n---\n\n${enrichedTask}`)
```

---

### Phase 4: Cycle Launch

```javascript
// Confirm launch (unless auto mode)
let shouldLaunch = isAutoMode

if (!isAutoMode) {
  const confirmation = ASK_USER([{
    id: "launch", type: "select",
    prompt: "Launch parallel-dev-cycle with this task?",
    options: [
      { label: "Yes, launch cycle (Recommended)", description: "Start parallel-dev-cycle with enriched task" },
      { label: "No, just save task", description: "Save formatted task for manual use" }
    ]
  }])  // BLOCKS (wait for user response)

  shouldLaunch = confirmation.launch.includes("Yes")
}

if (shouldLaunch) {
  console.log(`
## Launching parallel-dev-cycle

**Task**: ${selectedIdea.title}
**Source Session**: ${sessionId}
`)

  // Escape task for command line
  const escapedTask = enrichedTask
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/\$/g, '\\$')
    .replace(/`/g, '\\`')

  // Launch parallel-dev-cycle
  // Note: In actual execution, this would invoke the skill
  console.log(`
### Cycle Command

\`\`\`bash
/parallel-dev-cycle TASK="${escapedTask.substring(0, 100)}..."
\`\`\`

**Full task saved to**: ${sessionFolder}/cycle-task.md
`)

  // Return success with cycle trigger
  return {
    status: 'success',
    action: 'launch_cycle',
    session_id: sessionId,
    idea: selectedIdea.title,
    task_file: `${sessionFolder}/cycle-task.md`,
    cycle_command: `/parallel-dev-cycle TASK="${enrichedTask}"`
  }

} else {
  console.log(`
## Task Saved (Not Launched)

**Task file**: ${sessionFolder}/cycle-task.md

To launch manually:
\`\`\`bash
/parallel-dev-cycle TASK="$(cat ${sessionFolder}/cycle-task.md)"
\`\`\`
`)

  return {
    status: 'success',
    action: 'saved_only',
    session_id: sessionId,
    task_file: `${sessionFolder}/cycle-task.md`
  }
}
```

---

## Session Files

After execution:

```
{projectRoot}/.workflow/.brainstorm/{session-id}/
├── brainstorm.md        # Original brainstorm
├── synthesis.json       # Synthesis data (input)
├── perspectives.json    # Perspectives data
├── ideas/               # Idea deep-dives
└── cycle-task.md        # ⭐ Generated task (output)
```

## Task Format

The generated task includes:

| Section | Purpose | Used By |
|---------|---------|---------|
| Main Objective | Clear goal statement | RA: Primary requirement |
| Description | Detailed explanation | RA: Requirement context |
| Key Strengths | Why this approach | RA: Design decisions |
| Main Challenges | Known issues to address | RA: Edge cases, risks |
| Implementation Steps | Suggested approach | EP: Planning guidance |
| Alternatives | Other valid approaches | RA: Fallback options |
| Key Insights | Learnings from brainstorm | RA: Domain context |

## Error Handling

| Situation | Action |
|-----------|--------|
| Session not found | List available sessions, abort |
| synthesis.json missing | Suggest completing brainstorm first |
| No top_ideas | Report error, abort |
| Invalid --idea index | Show valid range, abort |
| Task too long | Truncate with reference to file |

## Examples

### Auto Mode (Quick Launch)

```bash
/brainstorm-to-cycle SESSION="BS-rate-limiting-2025-01-28" --auto
# → Selects highest-scored idea
# → Launches parallel-dev-cycle immediately
```

### Pre-Selected Idea

```bash
/brainstorm-to-cycle SESSION="BS-auth-system-2025-01-28" --idea=2
# → Selects top_ideas[2]
# → Confirms before launch
```

### Interactive Selection

```bash
/brainstorm-to-cycle SESSION="BS-caching-2025-01-28"
# → Displays all ideas with scores
# → User selects from options
# → Confirms and launches
```

## Integration Flow

```
brainstorm-with-file
        │
        ▼
   synthesis.json
        │
        ▼
 brainstorm-to-cycle  ◄─── This command
        │
        ▼
   enriched TASK
        │
        ▼
 parallel-dev-cycle
        │
        ▼
   RA → EP → CD → VAS
```

---

**Now execute brainstorm-to-cycle** with session: $SESSION
