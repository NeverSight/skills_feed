---
name: claude-expert
description: Essential reference for ALL Claude Code artifact work (Skills, Commands, Subagents, Hooks, Plugins). Automatically activates when creating, updating, validating, or discussing any Claude Code artifact. Provides complete specifications, YAML schemas, field definitions, creation workflows, decision frameworks, comparison matrices, validation rules, common mistakes, and best practices. Always consult for artifact specifications, technical requirements, workflow guidance, quality standards, or troubleshooting. Works alongside claude-researcher skill for documentation verification.
allowed-tools: Read, Skill
---

# Claude Code Expert: Technical Reference

Complete technical reference for all Claude Code artifacts (Skills, Commands, Subagents, Hooks) including specifications, workflows, decision frameworks, and best practices.

## Purpose

This Skill serves as the **knowledge repository** for the Ouroboros plugin. It contains all the detailed technical information that other Skills reference when guiding users through artifact creation and management.

**This Skill automatically activates when:**
- Creating any Claude Code artifact (Skill, Command, Subagent, Hook, Plugin)
- Updating or modifying existing artifacts
- Validating artifact quality or structure
- Discussing artifact specifications or requirements
- Troubleshooting artifact issues
- Choosing between artifact types
- Needing YAML schema or field definitions
- Asking about workflows or best practices
- Reviewing common mistakes or anti-patterns

**Integration with claude-researcher:**
This Skill works alongside the `claude-researcher` skill for documentation verification:
- **claude-expert** provides curated specifications, workflows, and best practices
- **claude-researcher** fetches and verifies official documentation from code.claude.com
- Use claude-researcher via: `Skill` tool to verify latest specifications
- Together they ensure both comprehensive knowledge and current accuracy

## Knowledge Areas

### 1. Artifact Specifications
Complete technical specifications for all artifact types:
- **Skills:** YAML schema, description formula, activation mechanism
- **Commands:** Frontmatter options, argument patterns, tool access
- **Subagents:** System prompts, delegation patterns, model selection
- **Hooks:** Event types, security requirements, configuration format

**See:** `specifications.md` for complete details

### 2. Creation Workflows
Step-by-step workflows for creating each artifact type:
- **Skill Creation:** 8-step workflow emphasizing description crafting and activation testing
- **Command Creation:** Argument handling, frontmatter configuration
- **Subagent Creation:** System prompt design, scope definition
- **Hook Creation:** Security review, threat modeling (MANDATORY)

**See:** `workflows.md` for complete workflows

### 3. Decision Frameworks
Frameworks for choosing the right artifact type:
- **Comparison Matrix:** Skills vs Commands vs Subagents vs Hooks
- **Decision Trees:** Invocation model, reasoning requirements, context needs
- **Use Case Patterns:** Common scenarios and recommended artifact types
- **Anti-Patterns:** What NOT to use and why

**See:** `comparison-matrix.md` for decision frameworks

### 4. Common Mistakes
Historical patterns of errors and how to prevent them:
- **Skill Mistakes:** Poor descriptions, missing triggers, YAML errors
- **Command Mistakes:** Argument handling, tool access issues
- **Subagent Mistakes:** Scope creep, delegation patterns
- **Hook Mistakes:** Security vulnerabilities, unquoted variables

**See:** `common-mistakes.md` for anti-patterns and prevention

## How This Skill Works

### Progressive Disclosure

This Skill uses **progressive disclosure** - Claude reads the knowledge files only when needed:

1. **SKILL.md** (this file) - Overview and index
2. **Supporting files** - Detailed knowledge loaded on demand:
   - `specifications.md` - When detailed specs needed
   - `workflows.md` - When step-by-step guidance needed
   - `comparison-matrix.md` - When decision support needed
   - `common-mistakes.md` - When troubleshooting or prevention needed

### Multi-Skill Activation

Claude can activate **multiple Skills simultaneously**. The claude-expert skill is designed to work alongside other skills:

**Example 1: Creation with claude-expert**
```
User: "I want to create a Skill for PDF processing"

Skills activated:
- claude-expert (provides specifications and best practices)
- skill-builder (guides creation workflow)
```

**Example 2: Decision-making with claude-expert**
```
User: "Should I use a Skill or Command for deployment?"

Skills activated:
- claude-expert (provides comparison framework)
- artifact-advisor (guides decision)
```

**Example 3: Validation with claude-expert**
```
User: "Validate this Skill and fix any issues"

Skills activated:
- claude-expert (provides specifications to validate against)
- artifact-validator (runs validation)
```

**Example 4: Documentation verification with claude-researcher**
```
User: "Create a new Command and verify it follows latest specs"

Skills activated:
- claude-expert (provides specifications and workflows)
- claude-researcher (fetches latest official documentation)
- command-builder (guides creation)
```

### Invoking claude-researcher

When current official documentation is needed, invoke claude-researcher:

```
Use the Skill tool to activate claude-researcher:
Skill(skill: "ouroboros:claude-researcher")

Then the researcher will fetch official docs from code.claude.com
and provide authoritative, current information.
```

## Knowledge Organization

### Specifications Structure

For each artifact type, specifications include:
- **Purpose & Use Cases:** When to use this artifact type
- **File Structure:** Directory layout and required files
- **YAML Schema:** Complete field definitions
- **Configuration Options:** All available settings
- **Tool Access Patterns:** Tool restriction patterns
- **Best Practices:** Quality guidelines
- **Examples:** Complete working examples

### Workflows Structure

For each artifact type, workflows include:
- **Step-by-Step Process:** Complete creation workflow
- **Time Estimates:** Expected duration for each step
- **Decision Points:** Key choices to make
- **Validation Checkpoints:** Quality checks throughout
- **Testing Procedures:** How to verify it works
- **Troubleshooting:** Common issues and fixes

### Decision Framework Structure

- **Decision Questions:** Key questions to ask
- **Scoring System:** Objective evaluation criteria
- **Recommendation Logic:** When to use each artifact type
- **Trade-offs:** Pros and cons of each choice
- **Edge Cases:** Unusual scenarios and guidance

### Common Mistakes Structure

- **Categorized by Artifact Type:** Organized for quick lookup
- **Severity Levels:** Critical, High, Medium, Low
- **Prevention Guidance:** How to avoid each mistake
- **Detection Methods:** How to identify the issue
- **Remediation Steps:** How to fix it

## Using This Knowledge

### For Users

**Direct questions:**
- "What are the required fields for a Skill?"
- "Show me the YAML schema for Commands"
- "What's the complete workflow for creating a Hook?"
- "What are common mistakes when creating Skills?"

Claude will activate this Skill and retrieve the relevant knowledge.

### For Other Skills

Other Skills in the Centauro plugin reference this knowledge:

**artifact-advisor** references:
- Comparison matrix for decision-making
- Use case patterns for recommendations
- Anti-patterns to warn users about

**skill-builder** references:
- Skill specification for YAML generation
- Creation workflow for step-by-step guidance
- Common mistakes for prevention tips

**artifact-validator** references:
- Specifications for validation rules
- YAML schemas for syntax checking
- Common mistakes for error detection

**hook-security-reviewer** (when built) will reference:
- Hook specification security section
- Hook creation workflow security steps
- Security-related common mistakes

## Quality Framework

All knowledge in this Skill follows the **Centauro Quality Framework:**

**Q = 0.40·Relevance + 0.30·Completeness + 0.20·Consistency + 0.10·Efficiency**

**Target grades:**
- Specifications: A (≥0.90)
- Workflows: A (≥0.90)
- Decision frameworks: A (≥0.90)
- Common mistakes: B+ (≥0.85)

## Maintenance

### Updating Knowledge

When Claude Code specifications change:
1. Update the relevant file (specifications.md, workflows.md, etc.)
2. Maintain consistency across all files
3. Update version in SKILL.md
4. Test that Skills still work correctly

### Version Tracking

Current knowledge version: **1.0.0**

**Coverage:**
- ✅ Skills: Complete specification and workflow
- ✅ Commands: Complete specification and workflow
- ✅ Subagents: Complete specification and workflow
- ✅ Hooks: Complete specification and workflow
- ✅ Comparison matrix: Complete decision framework
- ✅ Common mistakes: 50+ documented patterns

**Based on:**
- Claude Code official documentation (2024-2025)
- Real-world usage patterns
- Security best practices
- Community feedback

## Related Skills

**Documentation Skills:**
- **claude-researcher:** Fetches official Claude Code documentation from code.claude.com
  - Use when needing to verify current specifications
  - Use when official docs needed for latest features
  - Complements claude-expert's curated knowledge

**Workflow Skills (use claude-expert for knowledge):**
- **artifact-advisor:** Recommends which artifact type to use
- **skill-builder:** Guides Skill creation
- **command-builder:** Guides Command creation
- **subagent-builder:** Guides Subagent creation
- **hook-builder:** Guides Hook creation with security review
- **artifact-validator:** Validates artifact quality

**Troubleshooting Skills (use claude-expert for diagnosis):**
- **artifact-migrator:** Updates artifacts to new specifications
- **artifact-troubleshooter:** Diagnoses artifact issues (future)

## Quick Reference

### Most Common Queries

**"What are the required YAML fields for a Skill?"**
→ See specifications.md, Skill Specification section

**"What's the step-by-step process for creating a Skill?"**
→ See workflows.md, Skill Creation Workflow section

**"Should I use a Skill or a Command?"**
→ See comparison-matrix.md, Decision Framework section

**"Why isn't my Skill activating?"**
→ See common-mistakes.md, Skill Activation Issues section

**"How do I write a secure Hook?"**
→ See workflows.md, Hook Creation Workflow, Security Review section

**"What tools can a Skill use?"**
→ See specifications.md, Skill Specification, Tool Access section

## File Index

Navigate to detailed knowledge:

1. **specifications.md** - Complete technical specifications
   - Skill Specification (YAML, activation, examples)
   - Command Specification (arguments, frontmatter)
   - Subagent Specification (system prompts, delegation)
   - Hook Specification (events, security, configuration)

2. **workflows.md** - Step-by-step creation workflows
   - Skill Creation Workflow (8 steps, 60-120 min)
   - Command Creation Workflow (6 steps, 45-60 min)
   - Subagent Creation Workflow (7 steps, 60-90 min)
   - Hook Creation Workflow (9 steps with security, 90-120 min)

3. **comparison-matrix.md** - Decision frameworks
   - Artifact Comparison Matrix
   - Decision Trees (invocation, reasoning, context)
   - Use Case Patterns
   - Anti-Patterns

4. **common-mistakes.md** - Error patterns and prevention
   - Skill Mistakes (activation, YAML, descriptions)
   - Command Mistakes (arguments, tool access)
   - Subagent Mistakes (scope, delegation)
   - Hook Mistakes (SECURITY, validation)

---

## Best Practices for Using This Skill

### Always Active for Artifact Work
This skill should **automatically activate** whenever working with Claude Code artifacts. The enhanced description ensures it activates for:
- Any mention of Skills, Commands, Subagents, Hooks, or Plugins
- Creating, updating, or validating artifacts
- Questions about specifications or requirements
- Troubleshooting artifact issues

### Combining with claude-researcher
For the most accurate and current information:
1. **Start with claude-expert** for curated knowledge and workflows
2. **Verify with claude-researcher** when latest specifications needed
3. **Cross-reference** both sources for complete understanding

### Working with Other Skills
claude-expert is designed to be a **supporting skill** that provides knowledge to:
- artifact-advisor (for decision frameworks)
- skill-builder, command-builder, subagent-builder, hook-builder (for workflows)
- artifact-validator (for validation rules)
- artifact-migrator (for specification updates)

It should activate automatically alongside these skills without explicit invocation.

---

**This Skill serves as the foundation knowledge for all artifact creation and management in the Ouroboros plugin.**
