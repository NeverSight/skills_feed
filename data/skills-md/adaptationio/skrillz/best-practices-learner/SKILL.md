---
name: best-practices-learner
description: Extract learnings and best practices from skill development experience, review findings, and pattern analysis. Task-based operations for pattern extraction, learning documentation, guideline updates, knowledge sharing, and continuous improvement. Use when extracting learnings from completed skills, updating best practices, improving development process, or feeding continuous improvement cycle.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Best Practices Learner

## Overview

best-practices-learner systematically extracts learnings from skill development experience and feeds them back into the ecosystem. It transforms individual experiences into documented best practices that improve all future work.

**Purpose**: Capture and propagate learnings for continuous ecosystem improvement

**The 5 Learning Operations**:
1. **Extract Patterns** - Identify successful patterns from completed skills
2. **Document Learnings** - Capture what worked and what didn't
3. **Update Guidelines** - Feed learnings into common-patterns.md and templates
4. **Track Evolution** - Document how standards and practices evolved
5. **Share Knowledge** - Propagate learnings across ecosystem

**Key Principle**: Every skill built teaches us something - capture those lessons

**Continuous Improvement Loop**:
```
Build Skills → Review/Analyze → Extract Learnings →
Update Guidelines → Apply to Future Skills → Build Better Skills → Repeat
```

## When to Use

Use best-practices-learner when:

1. **After Completing Skills** - Extract learnings from successful builds
2. **After Reviews** - Capture insights from review-multi findings
3. **Pattern Discovery** - Document patterns identified through analysis
4. **Process Improvement** - Update development process based on experience
5. **Standards Evolution** - Document how best practices emerged and changed
6. **Knowledge Capture** - Before insights are forgotten, document them
7. **Ecosystem Enhancement** - Continuously improve toolkit quality

## Operations

### Operation 1: Extract Patterns

**Purpose**: Identify successful patterns from completed skills that should be repeated

**When to Use**:
- After completing skill successfully
- When reviewing multiple skills
- During retrospectives
- When patterns emerge

**Process**:

1. **Review Completed Work**
   - What worked well in this skill?
   - What made it easier/faster?
   - What would you repeat?
   - What was particularly effective?

2. **Identify Patterns**
   - Structural patterns (file organization, naming)
   - Content patterns (section types, documentation styles)
   - Process patterns (workflow steps, techniques)
   - Quality patterns (validation approaches, examples)

3. **Validate Pattern**
   - Is this truly a pattern (recurring, repeatable)?
   - Does it appear in 2+ instances?
   - Is it generalizable (not one-off)?
   - Does it have clear benefit?

4. **Document Pattern**
   - Pattern name
   - Description (what it is)
   - Context (when to use)
   - Example (concrete instance)
   - Benefit (why it works)

5. **Categorize Pattern**
   - Architecture pattern
   - Documentation pattern
   - Process pattern
   - Quality pattern
   - Integration pattern

**Example**:
```
Pattern Extracted: Quick Reference Section

Discovered During: Skills 4-5 (prompt-builder, skill-researcher)

Description: Add Quick Reference section as final section in SKILL.md
with high-density summary tables, commands, cheat sheets

Context: Use in all skills for rapid lookup and memory refresh

Benefit:
- Users can refresh memory without re-reading entire skill
- High-density information (tables, lists)
- Improves user experience
- Easy to find (always last section)

Evidence:
- Skills 4-8 have Quick Reference → received positive implicit feedback
- Skills 1-3 lacked it → identified as improvement in review
- Adding to skills 1-3 brought consistency to 100%

Recommendation: Make Quick Reference mandatory for all future skills

Category: Documentation Pattern
```

---

### Operation 2: Document Learnings

**Purpose**: Capture what worked, what didn't, and insights for future improvement

**When to Use**:
- End of each skill build
- After reviews or retrospectives
- When insights emerge
- Before forgetting context

**Process**:

1. **Capture What Worked**
   - Techniques that were effective
   - Approaches that saved time
   - Decisions that paid off
   - Tools/skills that helped

2. **Document What Didn't Work**
   - Mistakes made
   - Approaches that failed
   - Time wasted on wrong paths
   - What to avoid next time

3. **Extract Insights**
   - Why did X work well?
   - Why did Y fail?
   - What was the key factor?
   - What would you do differently?

4. **Quantify Impact** (when possible)
   - Time saved/lost
   - Quality improvement
   - Efficiency gain
   - Measurable benefits

5. **Make Actionable**
   - What should we do next time?
   - What should we stop doing?
   - What should we start doing?
   - Specific recommendations

**Example**:
```
Learning Documented: High-Quality Prompts Save Implementation Time

Context: Skills 4-9 development

What Worked:
- Investing 1.5-2h in prompt-builder to create detailed prompts
- Prompts with specific validation criteria, examples, constraints
- Targeting ≥4.5/5.0 prompt quality

Impact:
- Implementation 30-40% faster when following high-quality prompts
- Less rework (prompts were accurate first time)
- Clearer direction (no ambiguity)

What Didn't Work (Early Skills):
- Skills 1-3: Informal prompts or no prompts
- Result: More time spent figuring out what to write
- More iterations to get content right

Insight: Time invested in prompts pays 3-5x return in implementation

Quantified:
- 2h prompt investment → 6-10h implementation savings
- ROI: 300-500%

Recommendation: Always use prompt-builder for all future skills
Make this mandatory step in development-workflow

Category: Process Learning
```

---

### Operation 3: Update Guidelines

**Purpose**: Feed learnings into common-patterns.md, templates, and development guidelines

**When to Use**:
- After extracting patterns (Operation 1)
- After documenting learnings (Operation 2)
- When patterns validated (appear in 3+ skills)
- Periodic updates (after completing multiple skills)

**Process**:

1. **Identify Update Targets**
   - common-patterns.md (pattern library)
   - Templates (skill templates for patterns)
   - development-workflow (process improvements)
   - Guidelines in skill-builder-generic

2. **Prepare Updates**
   - Format patterns for documentation
   - Create examples
   - Write clear guidance
   - Show before/after if helpful

3. **Apply Updates**
   - Add new patterns to common-patterns.md
   - Update templates with new patterns
   - Enhance workflow documentation
   - Update guidelines

4. **Validate Updates**
   - Are updates clear and actionable?
   - Do they improve guidance quality?
   - Are examples helpful?

5. **Communicate Changes**
   - Document what changed and why
   - Note version/date of updates
   - Explain impact on future work

**Example**:
```
Guideline Update: Add Quick Reference Standard

Target: common-patterns.md

Update Content:
Added to "Documentation Patterns" section:

### Pattern: Quick Reference Section

**Description**: Final section in SKILL.md with high-density summary

**Structure**:
- Tables (operations, commands, metrics)
- Checklists (quick validation)
- Formulas (calculations)
- Decision trees (quick guides)

**Benefits**:
- Rapid lookup without re-reading
- Memory refresh
- Improved UX

**Mandatory**: All future skills must include Quick Reference

**Examples**: See skills 4-10 (all have this pattern)

Impact: Future skills will include Quick Reference by default

Version: Updated 2025-11-07 after Skills 1-10 analysis
```

---

### Operation 4: Track Evolution

**Purpose**: Document how standards, patterns, and practices evolved over time

**When to Use**:
- Significant standard changes (like Quick Reference adoption)
- After completing milestone (Layer 2, Layer 3, etc.)
- Periodic review (every 5-10 skills)
- Before major updates

**Process**:

1. **Identify Changes**
   - What standards emerged?
   - What practices changed?
   - What was added/removed?
   - When did changes occur?

2. **Document Evolution**
   - What was the original state?
   - What changed and when?
   - Why did it change?
   - What triggered the change?

3. **Capture Lessons**
   - What does this evolution teach us?
   - Why did standards emerge this way?
   - What does this mean for future?

4. **Track Metrics**
   - Quality trends over time
   - Efficiency trends
   - Complexity trends
   - Adoption rates

5. **Create Evolution Log**
   - Chronological documentation
   - Change descriptions
   - Rationale for changes
   - Impact assessment

**Example**:
```
Evolution Tracker: Quick Reference Pattern

Timeline:
- Skills 1-3 (Oct-Nov): No Quick Reference section
- Skill 4 (Nov): First Quick Reference added (prompt-builder)
- Skill 5 (Nov): Pattern repeated (skill-researcher)
- Skills 6-10: All included Quick Reference
- Nov 7: Retroactively added to Skills 1-3 (100% coverage)

Evolution:
Phase 1 (Skills 1-3): No standard for final reference section
Phase 2 (Skills 4-5): Quick Reference emerged organically
Phase 3 (Skills 6-10): Became standard practice
Phase 4 (Retroactive): Applied to early skills for consistency

Trigger: User experience feedback (implicit) - users wanted quick lookup

Impact:
- 100% of skills now have Quick Reference
- Improved user experience
- Standard documented in common-patterns.md
- Mandatory for future skills

Learning: Standards can emerge organically during development,
then be formalized and applied retroactively

Pattern: Emergent standards → Validation through usage →
Formalization → Retroactive application → Universal adoption
```

---

### Operation 5: Share Knowledge

**Purpose**: Propagate learnings across ecosystem and to broader community

**When to Use**:
- After guidelines updated
- When significant learnings captured
- Milestone completions
- Knowledge worth sharing

**Process**:

1. **Identify Valuable Knowledge**
   - What insights are most valuable?
   - What would help others?
   - What's novel or non-obvious?
   - What has evidence of effectiveness?

2. **Format for Sharing**
   - Document clearly with examples
   - Provide evidence (metrics, outcomes)
   - Make actionable
   - Include context

3. **Share Internally** (Ecosystem)
   - Update common-patterns.md
   - Update skill-builder-generic
   - Update development-workflow documentation
   - Incorporate into templates

4. **Share Externally** (If appropriate)
   - Community contributions
   - Blog posts or articles
   - GitHub discussions
   - Pattern sharing

5. **Enable Application**
   - Make learnings accessible
   - Provide templates or tools
   - Document in Quick References
   - Train on application

**Example**:
```
Knowledge Sharing: Bootstrap Strategy Effectiveness

Learning: Building skills in dependency order creates compound efficiency

Evidence:
- Skills 1-6: Each 75-90% faster than baseline
- Total time savings: 159 hours (72% reduction)
- Quality maintained: 100% pass rate (5/5 structure)

Application: Document in development-workflow, skill-builder-generic

Share Internally:
✅ Updated development-workflow/references/workflow-examples.md
✅ Added efficiency progression to common-patterns.md
✅ Documented in BUILD-ROADMAP.md

Share Externally: (If ecosystem open-sourced)
- Pattern: Dependency-ordered skill building
- Evidence: 72% efficiency gain demonstrated
- Recommendation: Build foundational skills first, leverage for later skills
```

---

## Best Practices

### 1. Capture Immediately
**Practice**: Document learnings right after discovering them

**Rationale**: Context fresh, details remembered, insights clear

**Application**: End of each skill build, add to learning log

### 2. Require Evidence
**Practice**: Support learnings with data and examples

**Rationale**: Evidence-based > opinion-based

**Application**: For each learning, note: evidence, metrics, examples

### 3. Make Actionable
**Practice**: Every learning should lead to specific action

**Rationale**: Learnings without application don't improve anything

**Application**: For each learning: "Therefore, we should [specific action]"

### 4. Update Guidelines Promptly
**Practice**: Apply learnings to guidelines quickly (within 1-2 skills)

**Rationale**: Fresh learnings applied promptly prevent forgetting

**Application**: After 2-3 instances of pattern, update guidelines

### 5. Track Evolution Explicitly
**Practice**: Document how and why standards changed

**Rationale**: Understanding evolution helps predict future changes

**Application**: Maintain evolution log in common-patterns or separate doc

---

## Quick Reference

### The 5 Learning Operations

| Operation | Focus | Output | When |
|-----------|-------|--------|------|
| Extract Patterns | Successful patterns | Documented patterns | After skills, reviews |
| Document Learnings | What worked/didn't | Learning log | End of each skill |
| Update Guidelines | Feed into docs | Updated common-patterns | After 2-3 pattern instances |
| Track Evolution | How standards changed | Evolution log | Milestones, periodic |
| Share Knowledge | Propagate learnings | Updated ecosystem docs | After updates |

### Learning Categories

- **Process Learnings**: Workflow improvements, efficiency gains
- **Quality Learnings**: What produces better quality
- **Pattern Learnings**: Recurring successful patterns
- **Tool Learnings**: Which tools/skills most valuable
- **Efficiency Learnings**: What saves time

### Integration with Ecosystem

```
analysis (identify patterns) →
best-practices-learner (extract and document) →
Update common-patterns.md →
development-workflow (apply in future skills)
```

---

**best-practices-learner captures and propagates learnings, enabling the ecosystem to improve itself continuously.**
