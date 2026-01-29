---
name: canvas-course-audit
description: Audit an entire Canvas LMS course against the Four Learning Design Pillars (Clear Structure, Active Content, Continuous Practice, Intuitive UX). Use when users want to evaluate course quality, identify improvement areas, or prepare for course redesign. Requires canvas-mcp server for course data access. Triggers on "audit course", "course review", "evaluate my course", or Canvas course IDs/codes.
---

# Canvas Course Audit

Perform a comprehensive audit of a Canvas course against the Four Learning Design Pillars, generating actionable recommendations based on evidence-based instructional design principles.

## Skill Purpose

This skill systematically evaluates a Canvas course against 50+ learning design principles organized into four pillars:

1. **Clear, Purposeful Structure** - Organization, consistency, learning path clarity
2. **Active, Engaging Learning Content** - Multimedia, interactivity, relevance
3. **Continuous Practice & Feedback** - Assessment variety, feedback quality, metacognition
4. **Simple, Intuitive User Experience** - Navigation, accessibility, media controls

## Usage

```
/canvas-course-audit <course_id_or_code>
```

**Examples:**
- `/canvas-course-audit 12345`
- `/canvas-course-audit EDUC-101-F24`
- "Audit my Canvas course 67890"
- "Review course quality for PSY 200"

## Prerequisites

- **canvas-mcp** server must be configured and running
- User must have access to the target course (instructor/TA/admin role)
- Principles file at: `{SKILL_DIR}/../principles/learning-design-pillars.yaml`

## Workflow

### Step 1: Initialize Audit

1. Parse the course identifier from user input
2. Load the learning design pillars from the YAML file:
   ```
   {SKILL_DIR}/../principles/learning-design-pillars.yaml
   ```
3. Confirm course access with canvas-mcp

### Step 2: Fetch Course Data

Use canvas-mcp tools to gather comprehensive course data:

```
# Core course information
canvas_mcp.get_course_details(course_id)

# Content structure
canvas_mcp.list_modules(course_id)
canvas_mcp.list_pages(course_id)

# Assessments
canvas_mcp.list_assignments(course_id)
canvas_mcp.list_quizzes(course_id)

# Engagement elements
canvas_mcp.list_discussions(course_id)

# Files and media
canvas_mcp.list_files(course_id)
```

### Step 3: Analyze Against Each Pillar

For each pillar, evaluate the course against specific criteria:

#### Pillar 1: Clear, Purposeful Structure

| Category | Canvas Elements to Check | Principle IDs |
|----------|-------------------------|---------------|
| Content Organization | Module count, items per module, naming patterns | 1.1.1-1.1.5 |
| Design Consistency | Naming conventions, template usage, formatting | 1.2.1-1.2.3 |
| Learning Path Clarity | Objectives visibility, overview pages, rubrics | 1.3.1-1.3.5 |
| Adaptive Design | Prerequisites, optional content, pacing | 1.4.1-1.4.2 |

**Check:**
- [ ] Modules have 5-10 items each (not overloaded)
- [ ] Consistent naming pattern (e.g., "Week 1:", "Module 1:")
- [ ] Each module has overview/summary pages
- [ ] Learning objectives visible in module descriptions
- [ ] Prerequisite settings used appropriately
- [ ] Logical progression from foundational to advanced

#### Pillar 2: Active, Engaging Learning Content

| Category | Canvas Elements to Check | Principle IDs |
|----------|-------------------------|---------------|
| Content Design | Page word counts, heading usage, media ratio | 2.1.1-2.1.8 |
| Multimedia | Video count, embedded content, H5P elements | 2.2.1-2.2.6 |
| Engagement | Discussion prompts, relevance indicators | 2.3.1-2.3.9 |
| Quality | External links, date stamps, source citations | 2.4.1-2.4.4 |

**Check:**
- [ ] Videos embedded (not just linked)
- [ ] Video count > 0 per content module
- [ ] Pages use headings (H1, H2, H3 hierarchy)
- [ ] Images have alt text
- [ ] Content uses conversational tone
- [ ] Key terms are bolded/highlighted
- [ ] Discussions exist beyond announcements

#### Pillar 3: Continuous Practice & Feedback

| Category | Canvas Elements to Check | Principle IDs |
|----------|-------------------------|---------------|
| Practice Design | Quiz types, assignment variety, practice vs graded | 3.1.1-3.1.7 |
| Feedback | Rubric attachment, auto-grading, peer review | 3.2.1-3.2.5 |
| Metacognition | Reflection prompts, self-assessment tools | 3.3.1-3.3.4 |

**Check:**
- [ ] Practice quizzes exist (ungraded/unlimited attempts)
- [ ] Assignment types vary (papers, projects, presentations)
- [ ] Rubrics attached to assignments
- [ ] Peer review enabled on at least one assignment
- [ ] Discussions require substantive responses
- [ ] Feedback turnaround expectations stated

#### Pillar 4: Simple, Intuitive User Experience

| Category | Canvas Elements to Check | Principle IDs |
|----------|-------------------------|---------------|
| Navigation | Course navigation settings, hidden items | 4.1.1-4.1.5 |
| Accessibility | Alt text, captions, color contrast | 4.2.1-4.2.5 |
| Media Control | Video player features, time estimates | 4.3.1-4.3.2 |

**Check:**
- [ ] Unused navigation items hidden
- [ ] Home page provides clear starting point
- [ ] Module requirements enable progress tracking
- [ ] External links clearly marked
- [ ] Time estimates provided for activities
- [ ] Mobile-friendly content (responsive embeds)

### Step 4: Calculate Pillar Scores

Score each pillar on a 1-5 scale:

| Score | Description |
|-------|-------------|
| 5 | Exemplary - Meets nearly all criteria with excellence |
| 4 | Strong - Meets most criteria with minor gaps |
| 3 | Adequate - Meets core criteria but notable gaps exist |
| 2 | Developing - Several significant gaps identified |
| 1 | Needs Redesign - Fundamental issues across criteria |

**Scoring Formula:**
```
Pillar Score = (criteria_met / total_criteria) * 5
```

### Step 5: Generate Audit Report

Produce a structured report with these sections:

```markdown
# Canvas Course Audit Report

**Course:** [Course Name] ([Course Code])
**Audit Date:** [Date]
**Overall Score:** [Average of 4 pillars] / 5

## Executive Summary

[2-3 sentence overview of course strengths and primary improvement areas]

## Pillar Scores

| Pillar | Score | Status |
|--------|-------|--------|
| 1. Clear Structure | X.X/5 | [Emoji indicator] |
| 2. Active Content | X.X/5 | [Emoji indicator] |
| 3. Practice & Feedback | X.X/5 | [Emoji indicator] |
| 4. Intuitive UX | X.X/5 | [Emoji indicator] |

## Detailed Findings

### Pillar 1: Clear, Purposeful Structure

**Score: X.X/5**

**Strengths:**
- [Finding citing principle ID, e.g., "Consistent module naming (1.2.1)"]

**Gaps:**
- [Finding citing principle ID, e.g., "No learning objectives visible (1.3.1)"]

[Repeat for each pillar]

## Recommendations

### Quick Wins (< 1 hour each)
1. [Action] - Addresses [Principle ID]
2. [Action] - Addresses [Principle ID]

### Medium Effort (1-4 hours)
1. [Action] - Addresses [Principle IDs]

### Major Redesigns (Course revision needed)
1. [Action] - Addresses [Principle IDs]

## Appendix: Audit Checklist

[Full checklist with pass/fail for each item]
```

## Canvas MCP Integration

### Required MCP Tools

| Tool | Purpose | Data Extracted |
|------|---------|----------------|
| `get_course_details` | Course metadata | Name, code, term, syllabus |
| `list_modules` | Structure analysis | Module names, item counts, prerequisites |
| `list_assignments` | Assessment inventory | Types, rubrics, due dates, points |
| `list_quizzes` | Practice analysis | Quiz types, attempts, time limits |
| `list_discussions` | Engagement elements | Topics, requirements, reply counts |
| `list_pages` | Content analysis | Page content, headings, media |
| `list_files` | Media inventory | File types, organization |

### MCP Call Sequence

```javascript
// 1. Verify course access
course = await canvas_mcp.get_course_details(course_id);

// 2. Fetch structural elements
modules = await canvas_mcp.list_modules(course_id);

// 3. Fetch assessments
assignments = await canvas_mcp.list_assignments(course_id);
quizzes = await canvas_mcp.list_quizzes(course_id);

// 4. Fetch engagement elements
discussions = await canvas_mcp.list_discussions(course_id);

// 5. Fetch content
pages = await canvas_mcp.list_pages(course_id);

// 6. Fetch media inventory
files = await canvas_mcp.list_files(course_id);
```

### Handling MCP Limitations

- If a tool is unavailable, note it in the report and skip that analysis
- For large courses (>100 items), paginate requests
- Cache results for multi-pass analysis

## Audit Criteria

For complete audit criteria tables with Canvas-specific checks and weights for each pillar, see:
**[references/audit-criteria.md](references/audit-criteria.md)**

Key high-weight criteria to prioritize:
- **Pillar 1**: Learning objectives visible (1.3.1), rubrics attached (1.3.4), consistent naming (1.2.1)
- **Pillar 2**: Videos embedded (2.2.1), interactive elements (2.2.2), inclusivity (2.4.3)
- **Pillar 3**: Practice quizzes (3.1.6), varied practice (3.1.1), peer review (3.3.4)
- **Pillar 4**: Progress tracking (4.1.2), minimalist design (4.2.5), time estimates (4.3.2)

## Example Output

```markdown
# Canvas Course Audit Report

**Course:** Introduction to Psychology (PSY-101-F24)
**Audit Date:** 2024-12-27
**Overall Score:** 3.4 / 5

## Executive Summary

PSY-101 demonstrates strong content organization and navigation design but lacks sufficient practice opportunities and multimedia engagement. Priority improvements should focus on adding practice quizzes and embedding video content.

## Pillar Scores

| Pillar | Score | Status |
|--------|-------|--------|
| 1. Clear Structure | 4.2/5 | Strong |
| 2. Active Content | 2.8/5 | Developing |
| 3. Practice & Feedback | 2.5/5 | Developing |
| 4. Intuitive UX | 4.1/5 | Strong |

## Detailed Findings

### Pillar 1: Clear, Purposeful Structure

**Score: 4.2/5**

**Strengths:**
- Consistent "Week X: Topic" naming convention (1.2.1)
- Each module contains 5-8 items, well-segmented (1.1.1)
- Clear prerequisite chain for foundational modules (1.1.3)
- Comprehensive syllabus with course policies (1.3.5)

**Gaps:**
- Learning objectives not visible in module descriptions (1.3.1)
- No module overview/summary pages (1.3.2)
- Rubrics missing from 3 of 8 assignments (1.3.4)

### Pillar 2: Active, Engaging Learning Content

**Score: 2.8/5**

**Strengths:**
- Pages use heading hierarchy appropriately (1.1.4)
- Key terms bolded throughout (2.3.8)
- Additional reading resources provided (2.4.1)

**Gaps:**
- Only 2 videos across 15 modules (2.2.1)
- No interactive elements (H5P, embedded activities) (2.2.2)
- Most content is text-heavy without visuals (2.1.2)
- No discussion forums for engagement (2.2.2)

### Pillar 3: Continuous Practice & Feedback

**Score: 2.5/5**

**Strengths:**
- Varied assignment types: essays, short answers, projects (3.1.1)
- Clear instructions in assignment descriptions (3.2.5)

**Gaps:**
- Zero practice quizzes - all quizzes are graded (3.1.6)
- No peer review assignments (3.3.4)
- No reflection prompts (3.3.3)
- Feedback limited to letter grades, no rubric feedback (3.2.1)

### Pillar 4: Simple, Intuitive User Experience

**Score: 4.1/5**

**Strengths:**
- Unused nav items hidden (Home, Modules, Assignments, Grades only) (4.2.5)
- Module requirements enable progress tracking (4.1.2)
- Clean home page with welcome message (4.2.5)

**Gaps:**
- No time estimates for readings/videos (4.3.2)
- External links not clearly marked (4.1.4)

## Recommendations

### Quick Wins (< 1 hour each)
1. Add learning objectives to each module description - (1.3.1)
2. Enable peer review on one major assignment - (3.3.4)
3. Add time estimates to module headers - (4.3.2)
4. Mark external links with "[External]" label - (4.1.4)

### Medium Effort (1-4 hours)
1. Create practice quiz for each unit using question banks - (3.1.6)
2. Add module overview page template to each module - (1.3.2)
3. Attach detailed rubrics to all assignments - (1.3.4, 3.2.1)
4. Create one discussion forum per unit - (2.2.2, 3.3.4)

### Major Redesigns (Course revision needed)
1. Develop or curate 1-2 short videos per module - (2.2.1, 2.2.3)
2. Add interactive elements (H5P knowledge checks) - (2.2.2)
3. Redesign assessments to include reflection components - (3.3.3)
```

## Notes

- Some criteria require manual review (e.g., tone, video quality)
- Report indicates where automated checks were not possible
- Recommend running audit at start of semester for maximum improvement time
- Pair with instructional designer review for comprehensive evaluation
