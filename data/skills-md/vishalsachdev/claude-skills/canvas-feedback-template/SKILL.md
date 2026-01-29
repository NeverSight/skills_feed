---
name: canvas-feedback-template
description: Generate learning science-backed feedback templates for Canvas assignments. Use when educators need feedback templates for grading, want to create rubric comments, need encouraging feedback language aligned with Pillar 3 principles (targeted, encouraging, immediate), or want to set up SpeedGrader comment libraries. Works with canvas-mcp for bulk grading.
---

# Canvas Feedback Template Generator

Generate learning science-backed feedback templates for Canvas assignments.

## Skill Purpose

This skill creates feedback templates that apply the Four Learning Design Pillars, specifically focusing on Pillar 3: Continuous Practice & Feedback. It generates targeted, encouraging feedback that helps students improve while maintaining a positive tone.

## Usage

```bash
/canvas-feedback-template
```

Or with specific context:
```bash
/canvas-feedback-template "peer review assignment" --rubric
```

## Workflow

### Step 1: Gather Context

Ask the user for:
1. **Assignment type** (essay, project, quiz, discussion, peer review)
2. **Learning objectives** being assessed
3. **Common issues** seen in submissions (optional)
4. **Rubric criteria** if available

### Step 2: Generate Templates

Create feedback templates organized by:

#### Performance Levels
- **Exceeds Expectations** - Celebrate mastery, suggest stretch goals
- **Meets Expectations** - Acknowledge success, highlight one improvement area
- **Approaching Expectations** - Specific improvements with encouragement
- **Needs Improvement** - Clear next steps with support resources

#### Feedback Components (per Principle 3.2.1 - Targeted Feedback)
Each template should include:
1. **Strength acknowledgment** (Principle 3.2.2 - Encouraging)
2. **Specific observation** with evidence from submission
3. **Actionable improvement** with concrete next step
4. **Forward-looking connection** to future learning

### Step 3: Apply Learning Principles

Ensure all templates follow these principles:

| Principle | Application in Feedback |
|-----------|------------------------|
| 3.2.1 Targeted | Focus on specific, goal-oriented actions |
| 3.2.2 Encouraging | Start with positives, maintain supportive tone |
| 3.2.3 Immediate | Design for quick delivery via SpeedGrader |
| 3.3.2 Generating explanations | Ask questions that prompt reflection |
| 3.3.3 Reflection | Include prompts for self-assessment |

### Step 4: Canvas Integration

If canvas-mcp is available:
1. **Rubric Comments**: Generate comment options for each rubric criterion
2. **Comment Library**: Format for Canvas SpeedGrader comment library
3. **Bulk Feedback**: Create templates suitable for `bulk_grade_submissions`

## Template Examples

### Essay Assignment - Meets Expectations

```markdown
**What's Working Well:**
Your thesis statement in paragraph 1 clearly establishes your argument about [topic].
The evidence in paragraphs 2-3 effectively supports your main claim.

**One Area to Strengthen:**
Your conclusion summarizes your points but could be more impactful. Try connecting
back to your opening hook or suggesting implications of your argument.

**Next Step:**
For your next essay, experiment with a "so what?" statement in your conclusion
that explains why your argument matters to the reader.
```

### Peer Review Assignment - Approaching Expectations

```markdown
**Strengths in Your Review:**
You identified the key strengths in your peer's draft and provided specific examples.

**Area for Growth:**
Your suggestions for improvement are general ("make it clearer"). More effective
peer feedback includes specific, actionable recommendations.

**How to Improve:**
Instead of "the introduction needs work," try: "Consider opening with a specific
example of [topic] to immediately engage readers. For instance, you could describe..."

**Reflection Question:**
What specific change would have the biggest impact on your peer's draft?
```

### Quiz/Assessment - Needs Improvement

```markdown
**Current Standing:**
You've demonstrated understanding of [specific topics]. Some foundational concepts
need more practice before moving forward.

**Focus Areas:**
- [Concept 1]: Review [specific resource or module]
- [Concept 2]: Complete practice problems in [location]

**Support Available:**
- Office hours: [times]
- Tutoring center: [link]
- Practice quiz: [link] (unlimited attempts)

**Encouragement:**
Many students find these concepts challenging at first. With targeted practice,
you can build mastery. Let's connect if you'd like to discuss a study plan.
```

## Rubric Comment Generation

When `--rubric` flag is used, generate comments for each criterion:

```yaml
criterion: "Thesis Statement"
levels:
  excellent:
    points: 20
    comment: "Your thesis is clear, specific, and arguable. It effectively previews your main arguments and sets up the essay structure."
  proficient:
    points: 16
    comment: "Your thesis establishes a clear position. To strengthen it, make your main argument more specific by identifying [the key factor/the primary cause/etc.]."
  developing:
    points: 12
    comment: "Your thesis identifies a topic but needs a clearer argumentative claim. Try completing this sentence: 'This essay argues that [specific claim] because [key reasons].'"
  beginning:
    points: 8
    comment: "I don't see a clear thesis statement. Let's meet to discuss how to craft a thesis that makes a specific, arguable claim about your topic."
```

## Canvas MCP Integration

### Using with SpeedGrader

```python
# After generating templates, user can apply via canvas-mcp
# Example workflow:
# 1. Generate templates with this skill
# 2. Copy to SpeedGrader comment library
# 3. Use bulk_grade_submissions for consistent feedback
```

### Bulk Grading Template

For `bulk_grade_submissions`, generate CSV-compatible format:

```csv
student_id,grade,comment
12345,85,"[Generated feedback based on rubric scores]"
12346,72,"[Generated feedback based on rubric scores]"
```

## Feedback Quality Checklist

Before finalizing templates, verify:

- [ ] **Specific**: References actual work, not generic statements
- [ ] **Actionable**: Includes concrete next step
- [ ] **Encouraging**: Leads with strengths, maintains supportive tone
- [ ] **Forward-looking**: Connects to future assignments/learning
- [ ] **Proportionate**: Length matches assignment weight
- [ ] **Accessible**: Uses clear language appropriate to course level

## Related Skills

- `/canvas-assignment-design` - Design assignments with feedback in mind
- `/canvas-course-audit` - Audit feedback practices across a course
- `/learning-design-review` - Review feedback quality against principles
