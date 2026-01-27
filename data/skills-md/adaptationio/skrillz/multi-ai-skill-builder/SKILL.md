---
name: multi-ai-skill-builder
description: Meta-skill for building Claude Code skills using Multi-AI research, planning, and implementation. Coordinates Claude, Gemini, and Codex for comprehensive research, synthesizes findings, and generates production-ready skills. Use when creating new skills, enhancing existing skills, researching skill domains, or building skill families.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Skill Builder

## Overview

multi-ai-skill-builder is a meta-skill that systematizes the Multi-AI approach to building Claude Code skills. It coordinates multiple AI models (Claude, Gemini, Codex) through research, planning, and implementation phases to create comprehensive, production-ready skills.

**Purpose**: Build high-quality Claude Code skills using Multi-AI research and synthesis

**Pattern**: Workflow-based (5-step sequential process)

**Key Principles** (validated by tri-AI research):
1. **Multi-Source Research** - Claude for docs, Gemini for web, Codex for GitHub
2. **Synthesis Before Building** - Combine findings into coherent plan
3. **Progressive Disclosure** - SKILL.md + references/ + scripts/
4. **Pattern Compliance** - Follow established skill patterns
5. **Validation Loop** - Multi-AI review of generated skills
6. **Iterative Refinement** - Build → Review → Improve cycle

**Quality Targets**:
- Research coverage: 3+ sources (Claude + Gemini + Codex)
- Skill completeness: All required sections present
- Code examples: 5+ practical examples per skill
- Validation score: ≥85/100

---

## When to Use

Use multi-ai-skill-builder when:

- Creating new Claude Code skills from scratch
- Building skill families (related skills for a domain)
- Enhancing existing skills with new research
- Researching best practices for a technical domain
- Converting research into actionable skills
- Establishing skill development workflows

**When NOT to Use**:
- Simple skill updates (use direct editing)
- Trivial skills (<100 lines, single operation)
- Skills outside your domain expertise (research first)

---

## Prerequisites

### Required
- Skill topic/domain clearly defined
- Time for research (30-60 min) and building (60-120 min)
- Access to Claude (always available)

### Recommended
- Gemini CLI for web research
- Codex CLI for GitHub patterns
- Existing example skills to reference

### Understanding
- Claude Code skill structure
- YAML frontmatter format
- Progressive disclosure architecture

---

## Workflow

### Step 1: Research Phase (Multi-AI)

**Time**: 30-60 minutes
**Purpose**: Gather comprehensive knowledge from multiple sources

**1.1 Claude Documentation Research**

Launch Claude subagent for official documentation:
```
Research [TOPIC] for Claude Code skill creation:

Focus on:
1. Official documentation and best practices
2. Existing similar skills in the codebase
3. API patterns and SDK usage
4. Common workflows and use cases

Output structured findings with:
- Key concepts
- Recommended patterns
- Code examples
- Gotchas and anti-patterns
```

**1.2 Gemini Web Research**

Use Gemini CLI for current best practices:
```bash
gemini -p "Research [TOPIC] best practices 2024-2025:
1. Industry standard approaches
2. Common patterns and anti-patterns
3. Tool comparisons and recommendations
4. Recent developments and trends
5. Real-world implementation examples

Provide comprehensive findings with sources."
```

**1.3 Codex GitHub Research**

Use Codex for code patterns:
```bash
codex "Research GitHub patterns for [TOPIC]:
1. Popular library implementations
2. Production code examples
3. Testing patterns
4. Configuration approaches
5. Error handling patterns

Provide code examples and best practices."
```

**1.4 Create Research Directory**

```bash
mkdir -p .analysis/[topic]-research
```

Save all research to:
- `.analysis/[topic]-research/claude-docs-research.md`
- `.analysis/[topic]-research/gemini-web-research.md`
- `.analysis/[topic]-research/codex-github-research.md`

---

### Step 2: Synthesis Phase

**Time**: 15-30 minutes
**Purpose**: Combine research into actionable plan

**2.1 Synthesize Findings**

```
Synthesize findings from multi-AI research:

Claude findings: [SUMMARY]
Gemini findings: [SUMMARY]
Codex findings: [SUMMARY]

Create unified synthesis:
1. Key patterns to implement
2. Best practices to follow
3. Anti-patterns to avoid
4. Recommended skill structure
5. Operations/workflows to include
6. Code examples to provide
```

**2.2 Create Synthesis Document**

Save to `.analysis/[topic]-research/SYNTHESIS_AND_PLAN.md`:

```markdown
# [Topic] Skill Synthesis

## Research Sources
- Claude: Documentation analysis
- Gemini: Web best practices
- Codex: GitHub patterns

## Key Findings
1. [Finding 1]
2. [Finding 2]
...

## Recommended Structure
- Pattern: [workflow/task/reference/capabilities]
- Operations: [list]
- References: [list]

## Implementation Plan
1. Create SKILL.md with [structure]
2. Add references for [topics]
3. Include [N] code examples
4. Cover [operations/workflows]

## Quality Checklist
- [ ] YAML frontmatter complete
- [ ] Trigger keywords included
- [ ] 5+ code examples
- [ ] Error handling covered
- [ ] All patterns validated
```

---

### Step 3: Build Phase

**Time**: 60-90 minutes
**Purpose**: Create the skill files

**3.1 Create Directory Structure**

```bash
mkdir -p .claude/skills/[skill-name]/references
mkdir -p .claude/skills/[skill-name]/scripts  # if needed
```

**3.2 Build SKILL.md**

Follow the template structure:

```markdown
---
name: skill-name-in-hyphen-case
description: [Purpose]. [Pattern type]. Use when [triggers].
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Skill Name

## Overview
[Brief description]
**Purpose**: [One line]
**Pattern**: [Workflow/Task/Reference/Capabilities]
**Key Principles**: [3-6 numbered principles]
**Quality Targets**: [Measurable goals]

## When to Use
[Use cases and non-use cases]

## Prerequisites
### Required / ### Recommended / ### Understanding

## [Operations or Workflow Steps]
[Main content with code examples]

## Multi-AI Coordination
[How to use Claude/Gemini/Codex for this skill]

## Related Skills
[Links to related skills]

## References
[Links to reference files]
```

**3.3 Build Reference Files**

Create detailed guides in `references/`:
- Detailed how-to guides
- Configuration references
- Integration patterns
- Troubleshooting guides

**3.4 Add Code Examples**

Every skill needs:
- Quick start example
- Common use case examples
- Advanced/edge case examples
- Error handling examples
- Integration examples

---

### Step 4: Validation Phase

**Time**: 15-30 minutes
**Purpose**: Verify skill quality

**4.1 Structure Validation**

Check YAML frontmatter:
```bash
head -20 .claude/skills/[skill-name]/SKILL.md
```

Verify sections:
- [ ] YAML frontmatter with name, description
- [ ] Overview section
- [ ] When to Use section
- [ ] Prerequisites section
- [ ] Main content (operations/workflows)
- [ ] Related Skills section
- [ ] References section

**4.2 Multi-AI Review**

```
Review this skill for quality:

[PASTE SKILL.md]

Check:
1. YAML frontmatter complete and descriptive?
2. Trigger keywords in description?
3. Clear when to use / when not to use?
4. Prerequisites documented?
5. 5+ code examples?
6. Error handling covered?
7. Progressive disclosure followed?
8. Related skills linked?

Score (0-100) and improvement suggestions.
```

**4.3 Gemini Cross-Check**

```bash
gemini -p "Verify this skill against best practices:
[SKILL CONTENT]

Check for:
- Accuracy of technical information
- Missing important patterns
- Outdated recommendations"
```

---

### Step 5: Refinement Phase

**Time**: 15-30 minutes
**Purpose**: Apply improvements from validation

**5.1 Apply Feedback**

Address issues from validation:
- Fix any structural issues
- Add missing examples
- Clarify unclear sections
- Enhance descriptions

**5.2 Final Quality Check**

Ensure:
- [ ] Score ≥85/100
- [ ] All validation items pass
- [ ] Cross-check feedback addressed
- [ ] Ready for production use

**5.3 Create Delivery Summary**

Save to `.analysis/[topic]-research/DELIVERY_SUMMARY.md`:

```markdown
# [Skill Name] - Delivery Summary

**Date**: [Date]
**Status**: COMPLETE
**Total Lines**: [X] lines across [Y] files

## Research Phase
- Claude: [Summary]
- Gemini: [Summary]
- Codex: [Summary]

## Skills Delivered
### [skill-name]
**Files**:
- SKILL.md ([X] bytes)
- references/[file].md
...

**Coverage**:
- [Feature 1]
- [Feature 2]
...

## Quality Validation
- Structure: PASS
- Content: PASS
- Examples: [N] included
- Score: [X]/100

## Usage Examples
[Show example triggers]
```

---

## Multi-AI Coordination

### Agent Assignment for Skill Building

| Phase | Primary | Support | Purpose |
|-------|---------|---------|---------|
| Docs Research | Claude | - | Official documentation |
| Web Research | Gemini | Claude | Current best practices |
| Code Research | Codex | Claude | GitHub patterns |
| Synthesis | Claude | Gemini | Combine findings |
| Building | Claude | - | Write skill files |
| Validation | Claude | Gemini | Quality check |

### Research Commands

**Claude Subagent**:
```
Use Task tool with subagent_type=Explore
```

**Gemini CLI**:
```bash
gemini -p "Research [topic]: [specific questions]"
```

**Codex CLI**:
```bash
codex "Research GitHub patterns for [topic]"
```

---

## Templates

### SKILL.md Template

See `templates/SKILL_TEMPLATE.md`

### Reference File Template

See `templates/REFERENCE_TEMPLATE.md`

### Synthesis Template

See `templates/SYNTHESIS_TEMPLATE.md`

---

## Quality Checklist

### Structure (20 points)
- [ ] YAML frontmatter valid
- [ ] All required sections present
- [ ] Progressive disclosure followed
- [ ] File naming conventions

### Content (25 points)
- [ ] Clear descriptions
- [ ] Comprehensive coverage
- [ ] Accurate information
- [ ] Well-organized

### Examples (25 points)
- [ ] 5+ code examples
- [ ] Quick start example
- [ ] Common use cases
- [ ] Error handling
- [ ] Advanced scenarios

### Usability (15 points)
- [ ] Easy to navigate
- [ ] Clear when to use
- [ ] Prerequisites documented
- [ ] Related skills linked

### Validation (15 points)
- [ ] Multi-AI reviewed
- [ ] Cross-checked
- [ ] Feedback addressed
- [ ] Score ≥85/100

---

## Example: Building ECS Skills

This example shows how we built the ECS/Fargate skill family:

### Research Phase
```bash
# Claude subagent for AWS docs
# Gemini for 2024-2025 best practices
gemini -p "Research ECS/Fargate best practices 2024-2025..."

# Codex for GitHub patterns
codex "Research GitHub patterns for ECS/Terraform..."
```

### Synthesis Phase
- Combined findings into unified plan
- Identified 5 skills to build
- Mapped to existing EKS skill patterns

### Build Phase
- Created boto3-ecs (SDK patterns)
- Created terraform-ecs (IaC)
- Created ecs-fargate (Fargate specifics)
- Created ecs-deployment (strategies)
- Created ecs-troubleshooting (debugging)

### Result
- 2,209+ lines across 15 files
- All skills validated
- Progressive disclosure implemented
- Multi-AI researched and reviewed

---

## Related Skills

- **multi-ai-research**: Research phase patterns
- **multi-ai-planning**: Planning phase patterns
- **multi-ai-implementation**: Implementation patterns
- **multi-ai-verification**: Validation patterns
- **skill-builder-generic**: Universal skill patterns
- **review-multi**: Skill review framework

---

## References

- `templates/SKILL_TEMPLATE.md` - Skill file template
- `templates/REFERENCE_TEMPLATE.md` - Reference file template
- `templates/SYNTHESIS_TEMPLATE.md` - Research synthesis template
