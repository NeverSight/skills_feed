---
name: skill-creator
description: Guide for creating effective agent skills. Use PROACTIVELY when creating new skills or refactoring bloated ones. Teaches progressive disclosure, 200-line rule, and 3-tier loading system.
tools: Read, Write, Glob, Grep
model: opus
---

# Skill Creator

Create effective agent skills using progressive disclosure. Skills are **workflow capabilities**, not documentation dumps. The goal is loading the right information at the right time.

## Core Principle

**Skills ≠ Documentation**

- `devops` isn't "Cloudflare docs" → it's the ability to deploy infrastructure
- `ui-styling` isn't "Tailwind docs" → it's the ability to design interfaces
- Each skill teaches *how to perform a task*, not *what a tool does*

## 3-Tier Architecture

```
Tier 1: Metadata (always loaded)
├── YAML frontmatter only (~100 words)
└── Enough for Claude to decide relevance

Tier 2: SKILL.md entry point (loaded on activation)
├── ~200 lines MAX
├── Overview, quick start, navigation
└── Points to references (doesn't include them)

Tier 3: references/ (loaded on-demand)
├── 200-300 lines each
├── Detailed documentation
└── Focused on single topics
```

## The 200-Line Rule

Entry point MUST be under 200 lines. This enables:
- Fast relevance scanning
- Quick reference selection
- 400-700 lines of relevant context vs 1,000+ of mixed relevance

**If you can't fit core instructions in 200 lines, you're putting too much in the entry point.**

## Skill Structure

```
skills/my-skill/
├── SKILL.md              # Entry point (<200 lines)
├── references/           # Detailed content
│   ├── guide-a.md        # 200-300 lines each
│   ├── guide-b.md
│   └── examples.md
├── scripts/              # Optional executable code
└── assets/               # Optional templates
```

## SKILL.md Template

```markdown
---
name: skill-name
description: One-line description. When to use this skill.
tools: Read, Write, Edit, Bash  # Optional
model: opus                      # Optional
---

# Skill Name

Brief description (2-3 sentences max).

## Quick Start

\`\`\`bash
# Essential commands only
\`\`\`

## Workflow

### 1. First Step
- Key points only
- No lengthy explanations

### 2. Second Step
- Action-oriented
- Link to references for details

## References

| Reference | Purpose |
|-----------|---------|
| `references/detailed-guide.md` | Full implementation details |
| `references/examples.md` | Code examples |
```

## Writing Guidelines

1. **Imperative tone**: "Run the build" not "You should run the build"
2. **Action-oriented**: What to do, not what things are
3. **Progressive detail**: Overview → Reference → Implementation
4. **No redundancy**: Say it once, in the right place

## When to Create vs Reference

**Create a skill when:**
- Task requires specific workflow knowledge
- Multiple steps with decision points
- Reusable across projects

**Use references when:**
- Detailed implementation specifics
- Code examples
- Edge cases and troubleshooting

## Refactoring Bloated Skills

Signs you need to refactor:
- SKILL.md over 200 lines
- Loading 5+ skills causes context issues
- 90% of loaded content isn't used

Process:
1. Extract detailed sections to `references/`
2. Keep only overview in SKILL.md
3. Add navigation table to references
4. Test cold start (should load <500 lines)

## References

| Reference | Purpose |
|-----------|---------|
| `references/architecture.md` | 3-tier system deep dive |
| `references/frontmatter.md` | YAML frontmatter spec |
| `references/writing-guide.md` | Content writing best practices |
| `references/refactoring.md` | How to split bloated skills |
| `references/anti-patterns.md` | What NOT to do |
| `references/examples.md` | Complete skill examples |

## Metrics

After creating/refactoring a skill:
- Entry point: <200 lines ✓
- Each reference: 200-300 lines ✓
- Cold start load: <500 lines ✓
- Relevant info ratio: >80% ✓
