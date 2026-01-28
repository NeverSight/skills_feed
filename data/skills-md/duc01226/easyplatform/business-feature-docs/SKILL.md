---
name: business-feature-docs
description: Generate enterprise module documentation with 26-section structure and folder hierarchy. Use for module docs, enterprise features, detailed specs in docs/business-features/{Module}/. Includes README, INDEX, API-REFERENCE, detailed-features/. Triggers on "module docs", "enterprise feature docs", "business module", "26-section docs", "detailed feature specs". For single-file quick docs, use feature-docs instead.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

# EasyPlatform Business Feature Documentation

Generate comprehensive business feature documentation following the **GOLD STANDARD** template.

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **⚠️ MUST READ** `.claude/skills/shared/business-docs-26-sections.md` — 26-section template structure
- **⚠️ MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` — BDD/Gherkin scenario templates
- **⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — validation checkpoints, confidence levels
- **⚠️ MUST READ** `docs/features/README.ExampleFeature1.md` — gold standard example
- **⚠️ MUST READ** `docs/templates/detailed-feature-docs-template.md` — full template
- **⚠️ MUST READ** `docs/templates/detailed-feature-docs-template.ai.md` — AI companion template

## Phase 1: Module Detection & Context Gathering

### Step 1.1: Identify Target Module

1. User explicitly specifies module name
2. Feature name/domain implies module
3. Search codebase for feature-related entities/commands

### Step 1.2: Read Existing Documentation

```
1. Read docs/BUSINESS-FEATURES.md (master index)
2. Read docs/business-features/{Module}/INDEX.md (if exists)
3. Read docs/business-features/{Module}/README.md (if exists)
4. Identify what already exists vs what needs creation/update
```

### Step 1.3: Codebase Analysis

Gather evidence from source code:
- **Entities**: `src/Backend/*.Domain/Entities/`
- **Commands**: `src/Backend/*.Application/UseCaseCommands/`
- **Queries**: `src/Backend/*.Application/UseCaseQueries/`
- **Controllers**: `src/Backend/*.Api/Controllers/`
- **Frontend**: `src/Frontend/apps/` or `src/Frontend/libs/apps-domains/`

## Phase 2: Documentation Generation

**⚠️ MUST READ** `.claude/skills/shared/business-docs-26-sections.md` for the full 26-section structure, format templates, and quality checklist.

Key requirements:
- All 26 mandatory sections in correct order
- Quick Navigation by Role table
- FR-{MOD}-XX format for business requirements
- TC-{MOD}-XXX format with GIVEN/WHEN/THEN for test cases
- Evidence with `{FilePath}:{LineRange}` format

## Phase 2.5: AI Companion Generation

**Output**: `docs/business-features/{Module}/detailed-features/README.{Feature}.ai.md`

10 sections (~300 lines): Context, File Locations, Domain Model, API Contracts, Business Rules, Patterns, Integration, Security, Test Scenarios, Quick Reference.

Compression rules: Tables over prose, paths over descriptions, signatures over examples, decisions over explanations.

## Phase 3: Master Index Update

After creating/updating module docs, update `docs/BUSINESS-FEATURES.md`:
1. Read current content
2. Verify module is listed
3. Add link if missing

## Anti-Hallucination Protocol

- Every feature claim MUST have code reference with file path and line numbers
- Read actual source files before documenting
- Never assume behavior without code evidence
- Checkpoint: "Have I read the actual code? Are my references accurate?"

## Quality Checklist

- [ ] All 26 mandatory sections present in correct order
- [ ] Quick Navigation by Role included
- [ ] Test cases use TC-{MOD}-XXX with GIVEN/WHEN/THEN
- [ ] All code references verified with actual files
- [ ] Master index (BUSINESS-FEATURES.md) updated
- [ ] AI companion file created (<= 300 lines)


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
