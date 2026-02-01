---
name: accelint-skill-manager
description: Use when users say "create a skill", "make a new skill", "build a skill", "skill for X", "package this as a skill", or when refactoring/updating/auditing existing skills that extend agent capabilities with specialized knowledge, workflows, or tool integrations.
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0"
---

# Skill Manager

This skill provides guidance for creating and managing effective agent skills.

## NEVER Do When Creating Skills

- **NEVER write tutorials explaining basics** - Assume Claude knows standard concepts, libraries, and patterns. Focus on expert-only knowledge.
- **NEVER put triggering information in body** - "When to use" guidance belongs ONLY in the description field. The body is loaded after activation decision.
- **NEVER dump everything in SKILL.md** - Use progressive disclosure: core workflow in SKILL.md (<500 lines ideal), detailed content in references/, loaded on-demand.
- **NEVER use generic warnings** - "Be careful" and "avoid errors" are useless. Provide specific anti-patterns with concrete reasons.
- **NEVER use same freedom level for all tasks** - Creative domains (design, architecture) need high freedom with principles. Fragile operations (file formats, APIs) need low freedom with exact scripts.
- **NEVER explain standard operations** - Assume Claude knows how to read files, write code, use common libraries. Focus on non-obvious decisions and edge cases.
- **NEVER include obvious procedures** - "Step 1: Open file, Step 2: Edit, Step 3: Save" wastes tokens. Include only domain-specific workflows Claude wouldn't know.

## Before Creating a Skill, Ask

Apply these tests to ensure the skill provides genuine value:

### Knowledge Delta Test
- **Does this capture what takes experts years to learn?** If explaining basics or standard library usage, it's redundant.
- **Am I explaining TO Claude or arming Claude?** Skills should arm agents with expert knowledge, not teach them concepts.
- **Is every paragraph earning its context space?** Token economy matters - shared with system prompts, conversation history, and other skills.

### Activation Economics
- **Does the description answer WHAT, WHEN, and include KEYWORDS?** Vague descriptions mean the skill never gets activated.
- **Would an agent reading just the description know exactly when to use this?** If unclear, the skill is invisible.

### Freedom Calibration
- **What happens if the agent makes a mistake?** High consequence = low freedom (exact scripts). Low consequence = high freedom (principles).
- **Is there one correct way or multiple valid approaches?** One way = prescriptive. Multiple ways = guidance with examples.

### Token Efficiency
- **Can this be compressed without losing expert knowledge?** References loaded on-demand save context.
- **Are there repetitive procedures that could become scripts?** Reusable code belongs in scripts/, not repeated in instructions.

## Flowchart Usage

```
digraph when_flowchart {
  "Need to show information?" [shape=diamond];
  "Decision where I might go wrong?" [shape=diamond];
  "Use markdown" [shape=box];
  "Small inline flowchart" [shape=box];

  "Need to show information?" -> "Decision where I might go wrong?" [label="yes"];
  "Decision where I might go wrong?" -> "Small inline flowchart" [label="yes"];
  "Decision where I might go wrong?" -> "Use markdown" [label="no"];
}
```

**Use flowcharts ONLY for:**
- Non-obvious decision points
- Process loops where you might stop too early
- "When to use A vs B" decisions

**Never use flowcharts for:**
- Reference material → Tables, lists
- Code examples → Markdown blocks
- Linear instructions → Numbered lists
- Labels without semantic meaning (step1, helper2)

## How to Use

This skill uses **progressive disclosure** to minimize context usage:

### 1. Start with the Workflow (SKILL.md)
Follow the 4-step workflow below for skill creation or refactoring.

### 2. Reference Implementation Details (AGENTS.md)
Load [AGENTS.md](AGENTS.md) for file system conventions, naming patterns, and structural rules.

### 3. Load Specific Examples as Needed
When implementing specific rules, load corresponding reference files for ❌/✅ examples.

## Skill Creation Workflow

To create or refactor a skill, follow the "Skill Creation Workflow" in order, skipping steps only if there is a clear reason why they are not applicable.

**Copy this checklist to track progress:**

```
- [ ] Step 1: Understanding - Gather concrete examples of skill usage
- [ ] Step 2: Planning - Identify reusable scripts, references, assets
- [ ] Step 3: Initializing - Check existing skills, create directory structure
- [ ] Step 4: Editing - Write agent-focused content with procedural knowledge
```

Include what rules from this skill are being applied, and why, in your summary.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

Example: Building an image-editor skill, ask:
- "What functionality? Editing, rotating, other?"
- "Usage examples?"
- "Trigger phrases: 'Remove red-eye', 'Rotate image'—others?"

Avoid overwhelming users. Start with key questions, follow up as needed.

Conclude when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Examples:
- `pdf-editor` skill for "Rotate this PDF" → store `scripts/rotate-pdf.sh` to avoid rewriting code each time
- `frontend-app-builder` for "Build a todo app" → store `assets/hello-world/` boilerplate template
- `big-query` for "How many users logged in today?" → store `references/schema.md` with table schemas

Analyze each concrete example to create a list of reusable resources: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Check available skills to identify potentially relevant ones the user may have missed:

```bash
ls -la .claude/skills 2>/dev/null || echo "No project skills found"
ls -la ~/.claude/skills 2>/dev/null || echo "No global skills found"
```

Look for skills related to:
- File types the command will process (docx, pdf, xlsx, pptx)
- Domain expertise (frontend-design, product-self-knowledge)
- Workflows or patterns (skill-creator, mcp-builder)

Present relevant skills to the user:
- "I found these skills that might be relevant: [list]. Should any of these be included?"
- Be concise; only mention skills with clear relevance

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

For new skills, use the template in [assets/skill-template/](assets/skill-template/) as a starting point. Copy the template directory and customize it for your specific skill.

Follow the instructions and conventions outlined in the [AGENTS.md](AGENTS.md) outline as well as the references.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of an agent to use. Focus on including information that would be beneficial and non-obvious to an agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another agent instance execute these tasks more effectively.

**Calibrate freedom to task fragility:**

| Task Type | Freedom Level | Guidance Format | Example |
|-----------|---------------|-----------------|---------|
| **Creative/Design** | High freedom | Principles, thinking patterns, anti-patterns | "Commit to a bold aesthetic" |
| **Code Review** | Medium freedom | Guidelines with examples, decision frameworks | "Priority: security > logic > performance" |
| **File Operations** | Low freedom | Exact scripts, specific steps, no variation | "Use exact command: `pandoc --flag`" |

**The test:** "If the agent makes a mistake, what's the consequence?"
- High consequence (file corruption, data loss) → Low freedom with precise scripts
- Medium consequence (suboptimal code, style issues) → Medium freedom with examples
- Low consequence (aesthetic choices, multiple valid approaches) → High freedom with principles

If you are updating an existing skill you can use the templates in [assets/skill-template/](assets/skill-template/) as a reference for larger structural changes and alignment. Consistency is imperative so lean towards aggressive reformatting to achieve adherence.

When updating an existing skill, ensure that the frontmatter `metadata.version` value is bumped. If the scope of the change is substantial do a major change 1.0 to 2.0, otherwise minor 1.0 to 1.1.
