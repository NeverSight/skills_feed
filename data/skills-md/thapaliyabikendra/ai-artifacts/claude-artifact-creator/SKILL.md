---
name: claude-artifact-creator
description: "Creates, improves, and validates Claude Code artifacts (skills, agents, commands, hooks). Use when creating domain expertise skills, specialized task agents, user-invoked commands, extending Claude Code capabilities, improving existing artifacts, reviewing artifact quality, analyzing code for automation opportunities, or consolidating duplicate artifacts."
layer: 4
tech_stack: [agnostic, markdown, yaml]
topics: [skills, agents, commands, hooks, claude-code, artifacts, meta]
depends_on: []
complements: []
keywords: [Skill, Agent, Command, Hook, SKILL.md, frontmatter, YAML, prompt-engineering]
---

# Claude Artifact Creator

Creates, improves, and maintains Claude Code extensions following official best practices.

## FIRST: Read Meta-Knowledge

**Before creating any artifact, READ `.claude/GUIDELINES.md`** for:
- Decision framework (Skill vs Agent vs Command vs Hook)
- Tool permissions strategy by role
- Hook events and configuration
- Agent/Skill/Command file formats
- Quality checklists and anti-patterns

This skill provides quick patterns; GUIDELINES.md provides authoritative rules.

## When to Use This Skill

- Creating a new skill for domain expertise or file processing
- Creating an agent for specialized tasks with context isolation
- Creating a command for user-invoked shortcuts
- Improving or refactoring existing artifacts
- Reviewing artifacts against quality standards
- Analyzing staged changes for automation opportunities
- Consolidating duplicate or overlapping artifacts

## Core Principle: Concise is Key

The context window is a shared resource. Before adding content, ask:
- "Does Claude really need this?" - Claude is already smart
- "Can this be in a reference file?" - Progressive disclosure
- "Does this justify its token cost?" - Every line has a cost

## Core Capabilities

1. **Create** - Generate artifacts from templates with proper structure
2. **Improve** - Enhance based on official best practices and patterns
3. **Review** - Audit against quality checklist and anti-patterns
4. **Consolidate** - Merge duplicate artifacts into focused ones

---

## Three-Layer Knowledge Architecture

**CRITICAL**: Before creating any knowledge artifact, determine the correct layer.

See [GUIDELINES.md § Three-Layer Knowledge Architecture](../../GUIDELINES.md#three-layer-knowledge-architecture) for full details.

### Quick Decision Flow

```
Is it a design principle that applies to ANY language?
│
├── YES → Create CONCEPT (knowledge/concepts/)
│         NO CODE, just principles
│
└── NO → Is it specific to a language/framework?
         │
         ├── YES → Create IMPLEMENTATION (knowledge/implementations/{lang}/)
         │         CODE EXAMPLES, links to concept
         │
         └── NO → Create SKILL (skills/)
                  ORCHESTRATION, references both
```

### Creating Concepts

**Location**: `knowledge/concepts/{topic}/{concept}.md`

**Rules**:
- ✅ Framework-independent principles only
- ✅ Why it matters (rationale)
- ✅ How to detect violations (criteria, not code)
- ❌ NO code examples
- ❌ NO language-specific syntax

**Template**:
```yaml
---
name: {Concept Name}
category: {topic}
implementations:
  dotnet: ../implementations/dotnet/{file}.md#{anchor}
  react: ../implementations/react/{file}.md#{anchor}
used_by_skills: []
---

# {Concept Name}

> "{Quote or one-liner definition}"

## The Principle

{Framework-independent explanation}

## Why It Matters

{Business/technical rationale}

## How to Detect Violations

- {Detection criteria - NO code}
- {Observable symptoms}

## Related Concepts

- [{Related Concept}](../{related}/concept.md)

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [Link](../../implementations/dotnet/{file}.md) |
| React | [Link](../../implementations/react/{file}.md) |
```

### Creating Implementations

**Location**: `knowledge/implementations/{lang}/{file}.md`

**Rules**:
- ✅ Links to concept(s) it implements
- ✅ ❌ Bad / ✅ Good code examples
- ✅ Framework-specific notes
- ❌ NO principle definitions (link instead)
- ❌ NO "why" explanations (concept layer)

**Template**:
```yaml
---
implements_concepts:
  - concepts/{topic}/{concept}
language: {csharp|typescript|python}
framework: [{dotnet|react|abp}]
---

# {Concept Name} in {Language}

## {Concept} {#anchor}

> **Concept**: [{Concept Name}](../../concepts/{topic}/{concept}.md)

### ❌ Violation

```{lang}
// Code showing anti-pattern
```

### ✅ Correct

```{lang}
// Code showing correct implementation
```

## Framework-Specific Notes

{Any framework-specific considerations}
```

### Updating Skills for Three-Layer

When creating or updating skills, add these front matter fields:

```yaml
---
name: skill-name
applies_concepts:
  - knowledge/concepts/{topic}/{concept}
uses_implementations:
  - knowledge/implementations/{lang}/{file}
---
```

### Governance Checklist

Before creating ANY knowledge artifact:

- [ ] **Concept exists?** If creating implementation, verify concept exists first
- [ ] **No code in concept?** Concepts must be code-free
- [ ] **Links bidirectional?** Concept → Implementation, Implementation → Concept
- [ ] **INDEX updated?** Add to `knowledge/concepts/INDEX.md` or `knowledge/implementations/INDEX.md`

---

## Quick Start

**Create a skill:**
```bash
python scripts/init_skill.py pdf-processor --path .claude/skills --template tool
```

**Create an agent:**
```bash
python scripts/init_agent.py abp-code-reviewer --path .claude/agents --template reviewer --category reviewers
```

**Create a command:**
```bash
python scripts/init_command.py run-tests --path .claude/commands --template workflow --category tdd
```

## Key Patterns

### 1. Decision Pattern
```
User triggers explicitly → COMMAND
Claude auto-detects → SKILL (no isolation) or AGENT (with isolation)
Deterministic on events → HOOK
```

### 2. Progressive Disclosure
```
Level 1: description (~100 tokens) → Trigger matching
Level 2: SKILL.md body (<5k tokens) → When activated
Level 3: references/ → On-demand deep dives
```

### 3. Artifact Limits

See [GUIDELINES.md § Size Limits](../../GUIDELINES.md#size-limits) for authoritative limits.

**Quick reference**: Skills <500, Agents <150, References one level deep.

### 4. Description Pattern
```yaml
# Good: Third-person with triggers
description: Processes PDF files for text extraction and form filling.
  Use when working with PDFs, extracting text, or filling forms.

# Bad: First-person or vague
description: I can help you with documents
```

## YAML Validation Rules

| Field | Requirements |
|-------|--------------|
| `name` | Max 64 chars, lowercase, hyphens only, no reserved words (anthropic, claude) |
| `description` | Max 1024 chars, third-person voice, 3+ trigger scenarios, no XML tags |
| `tools` | Comma-separated; omitting grants ALL tools (including MCP) |
| `model` | `haiku` (fast), `sonnet` (balanced), `opus` (powerful) |
| `permissionMode` | `default`, `acceptEdits`, `bypassPermissions` |

## Decision Flowchart

See [GUIDELINES.md § Choosing the Right Tool](../../GUIDELINES.md#choosing-the-right-tool) for the full decision matrix.

**Quick reference**: Command (user triggers) → Skill (auto, no isolation) → Agent (auto, isolated) → Hook (deterministic events)

## Creation Workflow

### Step 1: Identify Type

```
Type Decision Checklist:
- [ ] User invokes with /command? → Command
- [ ] Needs separate context window? → Agent
- [ ] Auto-triggered domain knowledge? → Skill
- [ ] Shell action on tool events? → Hook
```

### Step 2: Gather Requirements

**Skills**: Trigger scenarios (3+), resources needed, primary workflow
**Agents**: Team role, tools needed (least privilege), permission mode
**Commands**: Arguments, phases, expected output

### Step 3: Initialize

| Type | Command |
|------|---------|
| Skill | `python scripts/init_skill.py <name> --template <type>` |
| Agent | `python scripts/init_agent.py <name> --template <type> --category <cat>` |
| Command | `python scripts/init_command.py <name> --template <type> --category <cat>` |

**Templates:**
- Skills: `default`, `tool`, `workflow`, `domain`, `analysis`, `integration`, `generator`, `pattern`
- Agents: `architect`, `reviewer`, `developer`, `coordinator`, `specialist`
- Commands: `review`, `generate`, `debug`, `workflow`, `git`, `refactor`

### Step 4: Test

```
Testing Checklist:
- [ ] Customize all placeholders ([DOMAIN], [TARGET])
- [ ] Test with Haiku - enough guidance?
- [ ] Test with Sonnet - clear and efficient?
- [ ] Test with Opus - not over-explained?
- [ ] Verify triggers activate correctly
```

## Built-in Subagents

Claude Code includes built-in agents (cannot be modified):

| Agent | Purpose | Mode |
|-------|---------|------|
| **Plan** | Research before presenting plan | Read-only, plan mode |
| **Explore** | Fast codebase search | Read-only (`ls`, `find`, `cat`, `head`, `tail`) |

**Note**: Subagents cannot spawn other subagents.

## Tool Permissions & Hook Events

⚠️ **Warning**: Omitting `tools` grants ALL tools including MCP. Always whitelist explicitly.

**Full reference**: See [GUIDELINES.md § Agents](../../GUIDELINES.md#agents-agents) for tool permissions by role, and [GUIDELINES.md § Hooks](../../GUIDELINES.md#hooks) for hook events.

## Best Practices

1. **Concise over comprehensive** - Claude is smart; add only what it doesn't know
2. **Show, don't tell** - Examples beat descriptions
3. **Third-person descriptions** - Required for system prompt injection
4. **3+ trigger scenarios** - Specific scenarios in description ensure activation
5. **Least privilege tools** - Only grant necessary tools
6. **One level deep references** - No nested references (causes partial reads)
7. **Test all models** - What works for Opus may need more detail for Haiku
8. **Validate before shipping** - Run `scripts/validate.py --strict`

## Common Pitfalls

| Pitfall | Detection | Fix |
|---------|-----------|-----|
| Vague triggers | Description <100 chars | Add 3+ specific scenarios |
| Abstract only | No code blocks | Add before/after examples |
| Monolithic | >500 lines | Move to references/ |
| Kitchen sink | Lists 5+ domains | Create specialized artifacts |
| Embedded code in agent | Code blocks in agent | Extract to skill |
| First-person description | "I can help" | Use third-person |

See [references/anti-patterns.md](references/anti-patterns.md) for comprehensive list.

## Agent Refactoring

When agents grow >150 lines, extract embedded content to skills, commands, or docs.

**Full guide**: See [agent-refactoring-guide.md](references/agent-refactoring-guide.md)

## Agent Optimization Patterns

For comprehensive agent optimization, see [agent-optimization-patterns.md](references/agent-optimization-patterns.md).

**Key techniques:**

| Technique | Purpose |
|-----------|---------|
| **Semantic skill categorization** | Organize skills by METHODOLOGY, DOMAIN, LENS, OUTPUT |
| **Explicit workflow pipeline** | Declarative `GATHER → ANALYZE → REPORT` in frontmatter |
| **Skill invocation guidance** | Phase-to-skill mapping with fallback checks |
| **Project-agnostic design** | Dynamic context loading from docs/ |
| **Output externalization** | Dedicated format skill for report templates |

**Quick optimization checklist:**
```
- [ ] Skills categorized semantically (not alphabetically)
- [ ] Workflow defined as pipeline with phase-to-skill mapping
- [ ] Fallback checks provided for skill failures
- [ ] No hardcoded project names/paths
- [ ] Output template in dedicated skill
- [ ] Quality self-check categorized by concern
- [ ] Agent size <150 lines
```

## Agent Knowledge Profiles

Agents declare their knowledge profile in YAML front matter to enable validation and discoverability.

See [GUIDELINES.md § Artifact Knowledge Rules](../../GUIDELINES.md#artifact-knowledge-rules) for full governance.

### Required Front Matter Fields

| Field | Purpose | Format |
|-------|---------|--------|
| `understands` | Concepts agent knows | List of paths relative to `knowledge/concepts/` |
| `applies` | Implementations agent uses | List of paths relative to `knowledge/implementations/` |

### Example

```yaml
---
name: abp-developer
understands:
  - solid/srp
  - solid/dip
  - clean-code/naming
  - clean-architecture/layers
applies:
  - dotnet/solid
  - dotnet/clean-code
---
```

### Validation Rules

1. **Path validation**: All `understands` paths must exist in `knowledge/concepts/INDEX.md`
2. **Path validation**: All `applies` paths must exist in `knowledge/implementations/INDEX.md`
3. **Wildcard support**: Use `solid/*` to include all concepts in a category
4. **Role requirements**: Agents must meet minimum counts for their category

### Role Requirements

| Role (folder) | `understands` (min) | `applies` (min) |
|---------------|---------------------|-----------------|
| `reviewers/` | 3 | 1 |
| `engineers/` | 2 | 2 |
| `architects/` | 3 | 0 |
| `specialists/` | 1 | 0 |

### Validation Checklist

When creating or updating agents:

- [ ] All `understands` paths exist in concepts INDEX
- [ ] All `applies` paths exist in implementations INDEX
- [ ] Agent meets minimum requirements for its role category
- [ ] Skills align with knowledge profile (related domains)

**Cross-reference**: See [ARTIFACT-KNOWLEDGE-MATRIX.md](../../ARTIFACT-KNOWLEDGE-MATRIX.md) for full coverage.

## Success Metrics

Track these for artifact quality:

| Metric | Target |
|--------|--------|
| Trigger accuracy | Activates on relevant requests |
| Output consistency | Same quality across similar inputs |
| Model compatibility | Works with Haiku, Sonnet, Opus |
| Line count | Skills <500, Agents <150 |
| Description length | 100-1024 chars with triggers |

## Quality Checklist

See [GUIDELINES.md § Quality Checklists](../../GUIDELINES.md#quality-checklists) for authoritative checklists.

**Quick validation**:
- [ ] Description: third-person, 100-1024 chars, 3+ triggers
- [ ] Name: lowercase, hyphens, max 64 chars
- [ ] Under line limits (per GUIDELINES.md)
- [ ] Tested with Haiku, Sonnet, and Opus

## Integration Patterns

### Command → Agent → Skill

```
/add-feature (command)
  └─ Uses backend-architect (agent)
       └─ Applies api-design-principles (skill)
```

### Skill as Knowledge, Command as Action

```
Rule: "Knowing" = Skill, "Doing" = Command
      "Doing with Knowledge" = Command referencing Skills
```

## References

**Primary (READ FIRST):**
- [`.claude/GUIDELINES.md`](../../GUIDELINES.md) - **Authoritative meta-knowledge** for all artifact creation

**Skill-Specific:**
- [references/skills/skill-types.md](references/skills/skill-types.md) - Archetypes
- [references/agents/agent-categories.md](references/agents/agent-categories.md) - Role definitions
- [references/commands/command-patterns.md](references/commands/command-patterns.md) - Patterns
- [references/anti-patterns.md](references/anti-patterns.md) - What to avoid
- [references/agent-refactoring-guide.md](references/agent-refactoring-guide.md) - Extract from agents
- [references/agent-optimization-patterns.md](references/agent-optimization-patterns.md) - **Advanced optimization techniques** (skill categorization, workflow pipelines, fallback patterns)

**Project Context:**
- `CLAUDE.md` - Project-specific values and quick references
