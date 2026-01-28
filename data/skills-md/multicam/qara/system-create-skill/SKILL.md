---
name: system-create-skill
context: fork
model: sonnet
description: |
  Skill creation and validation framework ensuring compliance with PAI architectural standards.

  USE WHEN user says "create skill", "create a skill", "new skill", "build skill",
  "make skill", "skill for X", "Create-A-Skill", or any request to create new PAI skills.
---

## Workflow Routing (SYSTEM PROMPT)

**CRITICAL: Every skill creation request MUST follow architectural compliance validation.**

**When user requests creating a new skill:**
Examples: "create skill", "create a skill", "new skill", "build skill", "make skill", "skill for X", "Create-A-Skill"
→ **READ:** ${PAI_DIR}/skills/CORE/skill-structure.md
→ **READ:** ${PAI_DIR}/skills/system-create-skill/workflows/create-skill.md
→ **EXECUTE:** Complete skill creation workflow with architectural validation

**When user requests validating existing skill:**
Examples: "validate skill", "check skill compliance", "audit skill", "verify skill structure"
→ **READ:** ${PAI_DIR}/skills/CORE/skill-structure.md
→ **READ:** ${PAI_DIR}/skills/system-create-skill/workflows/validate-skill.md
→ **EXECUTE:** Skill compliance audit workflow

**When user requests updating existing skill:**
Examples: "update skill", "refactor skill", "fix skill routing", "add workflow to skill"
→ **READ:** ${PAI_DIR}/skills/CORE/skill-structure.md
→ **READ:** ${PAI_DIR}/skills/system-create-skill/workflows/update-skill.md
→ **EXECUTE:** Skill update workflow with compliance checking

**When user requests canonicalizing a skill:**
Examples: "canonicalize skill", "canonicalize this skill", "canonicalize [skill-name]", "rebuild skill to standards", "refactor skill to canonical structure"
→ **READ:** ${PAI_DIR}/skills/CORE/skill-structure.md
→ **READ:** ${PAI_DIR}/skills/system-create-skill/workflows/canonicalize-skill.md
→ **EXECUTE:** Complete skill canonicalization workflow - analyze current skill structure and rebuild according to canonical architecture while preserving functionality

---

## When to Activate This Skill

### Direct Skill Creation Requests
- "create skill", "create a skill", "new skill for X"
- "build skill", "make skill", "add skill"
- "Create-A-Skill" (canonical name)
- "skill for [purpose]" or "need a skill that does X"

### Skill Validation Requests
- "validate skill", "check skill compliance", "audit skill structure"
- "verify skill follows standards", "is this skill compliant"
- "review skill architecture", "skill quality check"

### Skill Update Requests
- "update skill", "refactor skill", "fix skill routing"
- "add workflow to skill", "extend skill"
- "reorganize skill structure", "migrate skill"

### Skill Canonicalization Requests
- "canonicalize skill", "canonicalize this skill", "canonicalize [skill-name]"
- "rebuild skill to standards", "refactor skill to canonical structure"
- "fix skill compliance", "bring skill to canonical form"
- "standardize skill structure", "make skill compliant"

### Quality & Compliance Indicators
- User mentions "architectural standards" or "compliance"
- User references "skill-structure.md"
- User asks about "skill best practices" or "skill patterns"
- User needs to ensure skill follows "template" or "philosophy"

---

## Core Principles

### Architectural Compliance

**MANDATORY: Every skill MUST comply with the canonical architecture defined in:**
`${PAI_DIR}/skills/CORE/skill-structure.md`

This document defines:
- The 3 skill archetypes (Minimal, Standard, Complex)
- The 4-level routing hierarchy
- Mandatory structural requirements
- Workflow organization patterns
- Naming conventions
- Routing patterns

**NON-NEGOTIABLE Requirements:**

1. **Workflow Routing Section FIRST** - Immediately after YAML frontmatter
2. **Every Workflow Must Be Routed** - No orphaned workflow files
3. **Every Secondary File Must Be Linked** - From main SKILL.md body
4. **Canonical Structure Template** - Follow the exact structure
5. **Progressive Disclosure** - SKILL.md → workflows → documentation → references

### Template-Driven Philosophy

**Consistency over creativity** when it comes to structure:
- Use established archetypes (Minimal/Standard/Complex)
- Follow canonical naming conventions
- Implement proven routing patterns
- Maintain predictable organization

**Creativity where it matters:**
- Domain-specific workflows
- Custom capabilities
- Unique integrations
- Innovative approaches to problems

### Quality Gates

Every created/updated skill must pass:

1. **Structural Validation**
   - Correct archetype directory structure
   - Proper file naming conventions
   - Required files present

2. **Routing Validation**
   - Workflow Routing section present and FIRST
   - All workflows explicitly routed
   - Activation triggers comprehensive (8-category pattern)

3. **Documentation Validation**
   - All files referenced in SKILL.md
   - Clear purpose and when-to-use guidance
   - Examples provided

4. **Integration Validation**
   - No duplication of CORE context
   - Compatible with agent workflows

---

## Skill Creation Process

### Step 1: Define Skill Purpose

Ask user to clarify:
- **What does this skill do?** (Core capability)
- **When should it activate?** (Trigger patterns)
- **What workflows does it need?** (Count and categories)
- **What integrations?** (Agents, external services)

### Step 2: Choose Archetype

Based on workflow count and complexity:

**Minimal Skill (1-3 workflows)**
```
skill-name/
├── SKILL.md
└── workflows/ OR assets/
    └── *.md
```

**Standard Skill (3-15 workflows)**
```
skill-name/
├── SKILL.md
├── workflows/
│   └── *.md (flat or nested)
└── [optional: documentation/, tools/, references/]
```

**Complex Skill (15+ workflows)**
```
skill-name/
├── SKILL.md
├── CONSTITUTION.md (optional)
├── METHODOLOGY.md (optional)
├── documentation/
├── workflows/ (nested)
├── references/
├── state/
└── tools/
```

### Step 3: Read Architecture Document

**ALWAYS read the canonical architecture before creating:**
```bash
${PAI_DIR}/skills/CORE/skill-structure.md
```

This ensures:
- Latest architectural requirements
- Current best practices
- Proven routing patterns
- Quality standards

### Step 4: Create Skill Structure

Use the canonical template from skill-structure.md:

```markdown
---
name: skill-name
description: |
  What this skill does and when to use it.

  USE WHEN: user says "trigger phrase", "another trigger", or any related request.
---

## Workflow Routing (SYSTEM PROMPT)

**When user requests [action 1]:**
Examples: "actual user phrases", "variations", "synonyms"
→ **READ:** ${PAI_DIR}/skills/skill-name/workflows/workflow1.md
→ **EXECUTE:** What to do with this workflow

[Route EVERY workflow file]

---

## When to Activate This Skill

[Comprehensive activation triggers using 8-category pattern]

---

## Extended Context / Main Body

[Detailed information, file links, examples]
```

### Step 5: Validate Compliance

Run through quality gates:
- ✅ Workflow Routing section present and FIRST?
- ✅ All workflows explicitly routed?
- ✅ All files referenced in main body?
- ✅ Activation triggers comprehensive?
- ✅ Examples provided?
- ✅ Naming conventions followed?

### Step 6: Test Activation

Verify skill activates with natural language triggers from description.

---

## Reference Documentation

**Detailed pattern and quality references:**
- `references/skill-patterns-reference.md` - 8-category routing pattern, routing patterns, anti-patterns
- `references/quality-checklist.md` - Complete quality checklist and validation gates

---

## Extended Context

### Primary Reference Document

**${PAI_DIR}/skills/CORE/skill-structure.md**
- Canonical guide for all skill structure and routing
- Defines the 3 archetypes (Minimal, Standard, Complex)
- The 4-level routing hierarchy
- All structural requirements and naming conventions
- Routing pattern examples
- Complete skill ecosystem reference
- **ALWAYS read this before creating or updating skills**

### Workflow Files

**${PAI_DIR}/skills/system-create-skill/workflows/create-skill.md**
- Complete skill creation workflow
- Step-by-step process with validation gates
- Template generation
- Quality assurance checks

**${PAI_DIR}/skills/system-create-skill/workflows/validate-skill.md**
- Skill compliance audit workflow
- Structural validation
- Routing validation
- Documentation validation
- Integration validation

**${PAI_DIR}/skills/system-create-skill/workflows/update-skill.md**
- Skill update and refactoring workflow
- Adding workflows to existing skills
- Reorganizing skill structure
- Migration patterns

---

## Examples

### Example 1: Creating a Minimal Skill

**User:** "Create a skill for generating API documentation"

**System-create-skill Response:**
1. Read skill-structure.md
2. Determine archetype: Minimal (single workflow)
3. Create structure:
   ```
   api-docs/
   ├── SKILL.md
   └── workflows/
       └── generate-docs.md
   ```
4. Write SKILL.md with:
   - YAML: name, description with USE WHEN triggers
   - Workflow Routing section (FIRST)
   - When to Activate section (8-category pattern)
   - Main body with workflow description
5. Validate against quality checklist
6. Test activation: "generate API docs for my service"

### Example 2: Creating a Standard Skill

**User:** "Create a skill for database operations - migrations, backups, queries, optimization"

**System-create-skill Response:**
1. Read skill-structure.md
2. Determine archetype: Standard (4 workflows)
3. Create structure:
   ```
   database/
   ├── SKILL.md
   └── workflows/
       ├── run-migration.md
       ├── backup-database.md
       ├── optimize-queries.md
       └── execute-query.md
   ```
4. Write SKILL.md with semantic routing:
   - Route "run migration" → run-migration.md
   - Route "backup database" → backup-database.md
   - Route "optimize" → optimize-queries.md
   - Route "query" → execute-query.md
5. Comprehensive activation triggers covering all 4 workflows
6. Validate and register
7. Test each workflow activation

### Example 3: Validating Existing Skill

**User:** "Validate the research skill for compliance"

**System-create-skill Response:**
1. Read skill-structure.md
2. Read ${PAI_DIR}/skills/research/SKILL.md
3. Run validation:
   - ✅ Workflow Routing section present and FIRST
   - ✅ All 12 workflows explicitly routed
   - ✅ Activation triggers comprehensive
   - ✅ All files referenced
   - ✅ Standard archetype structure correct
4. Report: "research skill is COMPLIANT - no issues found"

---

## Summary

**system-create-skill ensures:**
- Every created skill follows architectural standards
- Compliance is validated automatically
- Templates drive consistency
- Quality gates prevent non-compliant skills
- Philosophy is embedded in process

**Three core operations:**
1. **Create** - New skills with architectural compliance
2. **Validate** - Existing skills against standards
3. **Update** - Modify skills while maintaining compliance

**One source of truth:**
`${PAI_DIR}/skills/CORE/skill-structure.md`

**Zero tolerance for:**
- Orphaned workflows (not routed)
- Invisible files (not linked)
- Vague triggers (not comprehensive)
- Structural violations (wrong archetype)

---

**Related Documentation:**
- `${PAI_DIR}/skills/CORE/skill-structure.md` - Canonical architecture guide (PRIMARY)
- `${PAI_DIR}/skills/CORE/CONSTITUTION.md` - Overall PAI philosophy

**Last Updated:** 2025-11-17
