---
name: skill-improver
description: This skill should be used at natural checkpoints (after completing complex tasks, at session end, or when friction occurs) to reflect on skill and process execution and identify targeted improvements. Use when experiencing confusion, repeated failures, or discovering new patterns that should be codified into skills for smoother future operation.
---

# Skill Improver

## Overview

This skill guides reflective improvement of skills and processes through structured analysis. Rather than automatically suggesting changes, it provides a framework for mindful reflection to identify high-impact improvements without creating bloat.

The philosophy follows Buddhist "skillful means" (upaya) - developing concrete, practical wisdom through iteration. The goal is harmonious operation between Claude and the user by refining skills to be clearer, more complete, and more efficient.

## When to Use This Skill

**Use this skill:**
- At the end of a session when significant work has been completed
- After completing a complex task that involved multiple skills or tools
- When experiencing repeated friction, confusion, or failures during execution
- When discovering a workaround or novel pattern that should be captured
- When the user expresses frustration with a process or skill
- After successfully navigating a challenging workflow that could be easier next time

**Do not use this skill:**
- After every tiny task (reflection should be purposeful, not reflexive)
- When there's nothing substantial to improve
- During active work (finish first, then reflect)

## Reflection Workflow

### 1. Identify the Context

Clearly establish what process or skill is being reflected upon:
- What was the original goal or request?
- Which skills were used?
- What tools and resources were involved?
- How did the process unfold?

### 2. Apply the Reflection Framework

Use `references/reflection_framework.md` to systematically analyze the experience. The framework provides structured questions across five dimensions:

1. **Process Execution** - What happened? What worked? What didn't?
2. **Skill Content Analysis** - Was the skill clear, complete, efficient, accurate?
3. **Tool and Resource Analysis** - Were the right tools available? Did they work well?
4. **Pattern Recognition** - Is this a one-time issue or recurring pattern?
5. **Improvement Identification** - What specific changes would help?

Load and review the framework:

```
Read references/reflection_framework.md and work through the relevant questions
```

### 3. Identify Improvement Patterns

Consult `references/improvement_patterns.md` to recognize common issues:
- Clarity issues (ambiguous descriptions, jargon, vague steps)
- Completeness issues (missing prerequisites, edge cases, error handling)
- Efficiency issues (redundant instructions, missing scripts, context bloat)
- Usability issues (poor discoverability, overwhelming complexity)
- Structural issues (wrong abstraction level, missing decision trees)

Load and cross-reference patterns:

```
Read references/improvement_patterns.md to identify which patterns match the observed issues
```

### 4. Formulate Specific Improvements

Based on reflection, create concrete, actionable improvement proposals. Each improvement should include:

- **Skill/Process**: Name of what's being improved
- **Issue Observed**: Concrete description of the problem
- **Root Cause**: Why this happened (what's missing or wrong)
- **Proposed Change**: Specific, actionable improvement
- **Impact**: High/Medium/Low priority
- **Implementation**: Exact files and changes needed

### 5. Apply Improvement Principles

Before finalizing recommendations, verify they follow skillful means:

**Do:**
- Be specific and concrete
- Show evidence from actual experience
- Consider cost/benefit ratio
- Prefer simplification over addition
- Document principles and "why", not just "what"

**Don't:**
- Pile on multiple vague changes
- Over-engineer solutions
- Duplicate existing information
- Spam the user with minor tweaks

### 6. Execute Improvements (if appropriate)

For high-impact improvements:
- If editing an existing skill, use the skill-creator skill to make changes
- If creating a new skill is warranted, use the skill-creator skill
- For process improvements, document the new approach

For lower-impact improvements:
- Present findings to the user for future consideration
- Ask if they'd like to implement changes now or later

## Decision Tree: Improve vs Create

Sometimes the best improvement is creating a new skill. Use this decision tree:

**Create a new skill when:**
- Distinct domain sufficiently different from existing skills
- Recurring multi-step workflow that happens repeatedly
- Requires unique scripts, templates, or reference documentation
- Clear trigger that distinguishes it from other skills

**Improve existing skill when:**
- Issue is with clarity, completeness, or organization
- Missing resources (scripts, references, assets) for existing workflow
- Same domain, just needs better documentation or tools
- Edge cases or error handling need addressing

**Do nothing when:**
- Issue was a one-time environmental problem
- Adding documentation would create bloat without value
- Change would over-engineer a simple process
- Proposed improvement won't actually be used

## Resources

This skill includes reference documentation to guide the reflection process:

### references/reflection_framework.md

Structured framework with questions across five dimensions:
1. Process Execution
2. Skill Content Analysis
3. Tool and Resource Analysis
4. Pattern Recognition
5. Improvement Identification

Use this to systematically analyze what happened and identify specific improvement opportunities.

### references/improvement_patterns.md

Catalog of common skill issues and their solutions:
- Clarity issues (ambiguous descriptions, jargon, vague workflows)
- Completeness issues (missing prerequisites, edge cases, error handling)
- Efficiency issues (redundancy, missing scripts, context bloat, missing templates)
- Usability issues (discoverability, complexity, inconsistent terminology)
- Structural issues (abstraction level, decision trees, undocumented scripts)

Use this to recognize patterns and find proven solutions.

## Example Usage

### Example 1: Missing Scripts

**Scenario**: After using the `pdf-editor` skill to rotate several PDFs, Claude had to rewrite rotation code multiple times due to varying file permissions.

**Reflection**:
1. **Context**: Used pdf-editor skill to rotate PDFs, encountered permission issues
2. **Framework application**: Process execution had friction - repetitive code writing, unexpected errors
3. **Pattern recognition**: Matches "Missing scripts for repetitive tasks" and "Incomplete error handling"
4. **Improvement formulation**:
   - **Skill/Process**: pdf-editor
   - **Issue**: Rewrote PyPDF2 rotation code 3 times; permission errors not handled
   - **Root Cause**: No rotation script; permission handling undocumented
   - **Proposed Change**: Create `scripts/rotate_pdf.py` with permission handling; add troubleshooting section
   - **Impact**: High - eliminates code rewriting, prevents permission errors
   - **Implementation**: Create script, update SKILL.md to reference it
5. **Execution**: Use skill-creator to add script and update documentation

### Example 2: Missing Reference Documentation

**Scenario**: After creating a Lorn/Clams Casino inspired beat using the `strudel` skill, user feedback revealed bass tone missed the mark. User corrected: "don't need to encode every iteration" and "bass tone not reminding me of references."

**Reflection**:
1. **Context**: Used strudel skill for dark ambient hip-hop, encountered two issues
2. **Framework application**:
   - Process execution: URL encoding was inefficient during iterations
   - Skill content: No guidance for translating artist references into techniques
3. **Pattern recognition**: Matches "Vague workflow steps" and "Missing reference documentation"
4. **Improvement formulation**:
   - **Skill/Process**: strudel
   - **Issue #1**: Encoded URL after every iteration; user said only needed on initial creation
   - **Root Cause**: Skill said "Always encode after modifications" - too broad
   - **Proposed Change**: Clarify when to encode (initial only, skip iterations, final if requested)
   - **Impact**: Medium - prevents unnecessary work
   - **Implementation**: Update SKILL.md section "Providing Output to the User"

   - **Issue #2**: No systematic guide for artist characteristics (Lorn, Clams Casino)
   - **Root Cause**: No reference for common genre/artist styles
   - **Proposed Change**: Create `references/genre-styles.md` with artist characteristics and Strudel techniques
   - **Impact**: High - translates user references into concrete implementation
   - **Implementation**: Create reference file, update SKILL.md to reference it
5. **Execution**: Used skill-creator to implement both improvements; user approved both

## Philosophy: Skillful Means

The goal is harmonious operation through continuous refinement:

- **Concrete over abstract**: Prefer working examples to theoretical descriptions
- **Simplicity over completeness**: Handle 80% of cases well rather than 100% poorly
- **Clarity over cleverness**: Straightforward instructions beat elegant complexity
- **Practical over perfect**: Ship useful improvements, iterate continuously
- **Harmonious over comprehensive**: Reduce friction, don't add features

Each improvement should make Claude's and the user's life tangibly easier. If it doesn't pass this test, don't recommend it.
