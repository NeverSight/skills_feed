---
name: component
description: Generate syntactically correct Claude Code configuration components (commands, subagents, skills, output styles) with optimal cross-component integration. Triggers on requests to create slash commands, agents, subagents, skills, output styles, Claude Code plugins, agentic workflows, or multi-agent pipelines. Ensures parameter validity per component type and semantic coherence across component references.
---

# Component: Claude Code Configuration Generator

Generate integrated Claude Code configuration with syntactically valid YAML frontmatter and semantically coherent cross-references.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLAUDE CODE CONFIGURATION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   COMMANDS ─────────invoke────────► SUBAGENTS                               │
│   (.claude/commands/*.md)           (.claude/agents/*.md)                   │
│   • Entry points                    • Specialized personas                  │
│   • Tool orchestration              • Persistent identity                   │
│   • User-facing /slash              │                                       │
│                                     ▼ load                                  │
│                                   SKILLS                                    │
│                                   (.claude/skills/*/SKILL.md)               │
│                                   • Procedural knowledge                    │
│                                   • Domain expertise                        │
│                                                                             │
│   STYLES ─────────modulate────────► SESSION BEHAVIOR                        │
│   (.claude/styles/*.md)             • Autonomy level                        │
│   • Interaction patterns            • Output format                         │
│                                     • Checkpoint frequency                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Relationships**:
- Commands **invoke** Subagents (via `Agent` tool)
- Subagents **load** Skills (via `skills:` array)
- Styles **modulate** session behavior (parallel to commands, not hierarchical)

## Parameter Matrix

| Parameter | Commands | Subagents | Skills | Styles |
|-----------|:--------:|:---------:|:------:|:------:|
| `name` | ✗ (filename) | ✗ (filename) | ✓ (required) | ✓ (required) |
| `description` | ✓ (required) | ✓ (required) | ✓ (required) | ✓ (required) |
| `allowed-tools` | ✓ | ✓ | ✓ | ✗ |
| `disallowed-tools` | ✗ | ✓ | ✗ | ✗ |
| `model` | ✓ | ✓ | ✗ | ✗ |
| `argument-hint` | ✓ | ✗ | ✗ | ✗ |
| `disable-model-invocation` | ✓ | ✗ | ✗ | ✗ |
| `permissionMode` | ✗ | ✓ | ✗ | ✗ |
| `skills` | ✗ | ✓ | ✗ | ✗ |
| `keep-coding-instructions` | ✗ | ✗ | ✗ | ✓ |

### Parameter Dependencies

```
allowed-tools + Agent ──────► enables subagent spawning
skills ──────────────────────► requires skill directories exist
permissionMode: allow ───────► full autonomy (no prompts)
permissionMode: ask ─────────► checkpoint prompts (default)
permissionMode: deny ────────► read-only operations
```

## Component Specifications

### Commands (`.claude/commands/<name>.md`)

Filename becomes `/slash-command` (no `name` field).

```yaml
---
description: Execute [action] on [target]     # REQUIRED
allowed-tools: [Read, Write, Agent]           # Optional: tool access
model: sonnet                                 # Optional: sonnet|opus|haiku
argument-hint: <target>                       # Optional: CLI placeholder
---

## Implementation

[Procedural instructions for command execution]
[Can spawn subagents via Agent tool]
```

**Example** (`/review`):
```yaml
---
description: Review code changes for quality and correctness
allowed-tools: [Read, Grep, Glob, Agent]
model: opus
argument-hint: <path>
---

## Execution

1. Analyze target path for code changes
2. Spawn reviewer agent with file context
3. Synthesize findings into actionable feedback
```

### Subagents (`.claude/agents/<name>.md`)

Specialized personas with tool access and skill mastery.

```yaml
---
description: [Role] specializing in [domain]. [Key traits].  # REQUIRED
allowed-tools: [Read, Write]                                  # Permitted tools
disallowed-tools: [Bash]                                      # Explicit denials
model: sonnet                                                 # Reasoning model
permissionMode: ask                                           # ask|allow|deny
skills: [skill-a, skill-b]                                    # Loaded procedures
---

## Persona

[Identity, decision heuristics, communication style]
```

**Example** (`security-analyst.md`):
```yaml
---
description: Security analyst for vulnerability detection and threat modeling. Methodical, conservative.
allowed-tools: [Read, Grep, Glob]
disallowed-tools: [Write, Bash]
model: opus
permissionMode: ask
skills: [security-analysis, threat-modeling]
---

## Persona

Identify vulnerabilities with CVSS scoring. Prioritize by exploitability.
Flag sensitive data exposure. Never modify production code directly.
```

### Skills (`.claude/skills/<name>/SKILL.md`)

Procedural knowledge packages loaded by subagents.

```yaml
---
name: skill-name                              # REQUIRED: kebab-case, ≤64 chars
description: Procedures for [domain]. Trigger when [conditions].  # REQUIRED: ≤1024 chars
allowed-tools: [Read]                         # Optional: tool restrictions when active
---

## Procedures

[Step-by-step workflows, decision trees, domain knowledge]
```

**Example** (`security-analysis/SKILL.md`):
```yaml
---
name: security-analysis
description: Static security analysis procedures. Trigger when reviewing code for vulnerabilities, secrets, or injection risks.
---

## Detection Patterns

### Secret Detection
- API keys: `[A-Za-z0-9]{32,}`
- AWS keys: `AKIA[A-Z0-9]{16}`
- Private keys: `-----BEGIN.*PRIVATE KEY-----`

### Injection Risks
- SQL: Unparameterized queries with string concatenation
- XSS: Unescaped user input in HTML templates
- Command: Shell execution with user-controlled arguments
```

### Styles (`.claude/styles/<name>.md`)

Interaction mode modulators for session behavior.

```yaml
---
name: style-name                              # REQUIRED
description: [Interaction pattern] for [use case].  # REQUIRED
keep-coding-instructions: true                # Optional: preserve coding behavior
---

## Behavior Modifications

[Output format, checkpoint frequency, autonomy level]
```

**Supervision Gradient**:

| Style | Behavior | Use Case |
|-------|----------|----------|
| `autonomous` | Execute without prompting, log decisions | Trusted automation |
| `supervised` | Checkpoint at key decisions | Normal development |
| `collaborative` | Explain reasoning, seek approval | Learning, auditing |

## Tool Pattern Syntax

```yaml
allowed-tools:
  # Basic tools
  - Read                      # File reading
  - Write                     # File writing
  - Edit                      # File editing
  - Glob                      # Pattern matching
  - Grep                      # Text search
  - LS                        # Directory listing
  - Agent                     # Subagent spawning
  - WebFetch                  # URL fetching
  
  # Bash patterns
  - Bash(git status)          # Exact command
  - Bash(git:*)               # All git subcommands
  - Bash(npm run:*)           # All npm run scripts
  
  # MCP tools
  - mcp__server__tool         # Specific MCP tool
  - mcp__github__*            # All tools from MCP server
```

## Generation Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. ANALYZE                                                                  │
│    └─► Identify domain requirements, capabilities needed                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. DESIGN SKILLS                                                            │
│    └─► Package domain procedures (security-analysis, code-review, etc.)     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. CREATE SUBAGENTS                                                         │
│    └─► Define personas that load skills, set tool access                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. BUILD COMMANDS                                                           │
│    └─► Create /slash entry points that invoke agents                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. CONFIGURE STYLES                                                         │
│    └─► Set supervision levels for different workflows                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 6. VALIDATE                                                                 │
│    └─► Check syntax, cross-references, parameter validity                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Integration Patterns

### Pattern 1: Skill-Backed Agent

```
skill: code-analysis ──► agent: analyst ──► command: /analyze
                              │
                         skills: [code-analysis]
```

Agent loads procedural knowledge via skills, invoked by command.

### Pattern 2: Multi-Agent Pipeline

```
command: /ship
    │
    ├─► Agent[planner] ───► Plan
    ├─► Agent[implementer] ► Code  
    ├─► Agent[reviewer] ──► Review
    └─► Agent[deployer] ──► Deploy
```

Sequential agent stages for complex workflows.

### Pattern 3: Skill Composition

Agent loads multiple skills for comprehensive expertise:

```yaml
# .claude/agents/fullstack.md
---
description: Full-stack developer proficient across domains
skills:
  - frontend-development
  - backend-development
  - security-guidelines
---
```

### Pattern 4: Skill References Skill

Skills can reference procedures from other skills:

```yaml
# .claude/skills/advanced-security/SKILL.md
---
name: advanced-security
description: Advanced threat modeling. Extends security-analysis procedures.
---

## Foundation

Load base procedures from `security-analysis` skill, then apply:

### Extended Analysis
- Supply chain attack vectors
- Dependency confusion risks
- CI/CD pipeline vulnerabilities
```

## Validation Checklist

### Commands
- [ ] No `name` field (filename is command name)
- [ ] Has `description` (imperative verb + target)
- [ ] Tool patterns valid
- [ ] No forbidden params: `permissionMode`, `skills`, `keep-coding-instructions`

### Subagents
- [ ] Has `description` (role + domain + traits)
- [ ] `skills:` arrays reference existing skill directories
- [ ] `permissionMode` is `ask`, `allow`, or `deny`
- [ ] `model` is `sonnet`, `opus`, or `haiku`

### Skills  
- [ ] Has `name` (kebab-case, matches directory)
- [ ] Has `description` (max 1024 chars, includes trigger conditions)
- [ ] SKILL.md under 500 lines
- [ ] Directory contains SKILL.md at minimum

### Styles
- [ ] Has `name` and `description`
- [ ] `keep-coding-instructions` is boolean if present
- [ ] No tool or model parameters

### Cross-References
- [ ] All skills in `skills:` arrays exist as directories
- [ ] All agents referenced by commands exist
- [ ] No circular skill dependencies

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Command not appearing | Missing `.claude/commands/` path | Ensure file in correct directory |
| Agent can't access tool | `allowed-tools` missing tool | Add tool to agent's allowed-tools |
| Skill not loading | Skill name mismatch | Ensure `name:` matches directory name |
| Style not applying | Missing `name` field | Add required `name` parameter |

## Alternatives Considered

**JSON Configuration**: Single `.claude.json` file is simpler but lacks prose instructions and becomes unwieldy at scale. Markdown files support rich documentation alongside configuration.

**Flat Structure**: All components in one directory sacrifices organization but works for small projects. Current structure scales to dozens of components.

## References

Detailed documentation by topic:

- `references/syntax.md` — Complete YAML frontmatter schemas, all parameters
- `references/patterns.md` — Integration patterns, multi-agent pipelines  
- `references/examples.md` — Full plugin examples with all component types
