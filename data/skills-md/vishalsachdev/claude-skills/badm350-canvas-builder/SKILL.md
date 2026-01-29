---
name: badm350-canvas-builder
description: Generate Canvas-ready HTML pages and assignments for BADM 350 Technology & AI Strategy course. Use when building weekly module content from markdown lesson plans, creating "Start Here" pages with Tuesday/Thursday session structure, or generating assignment HTML with rubrics. Triggers on requests to "build Canvas content", "create week X page", or "generate assignment for BADM 350".
---

# BADM 350 Canvas Content Builder

Converts BADM 350 week markdown files into Canvas-ready HTML following the Gies College course style guide.

## Workflow

### 1. Identify Source Files

Week content lives in:
```
/Users/vishal/teaching/badm350/modules/unit-X-*/week-NN-topic.md
```

Style guide at:
```
/Users/vishal/teaching/badm350/canvas-style-guide.md
```

### 2. Generate Start Here Page

Read the week markdown and extract:
- Learning objectives (with L-C-E tier)
- Session agendas (Tuesday/Thursday, 75 min each)
- Before/During/After Class tasks
- Readings and resources
- Lab deliverable info

Apply the Start Here template from `references/start-here-template.md`.

Output to: `/Users/vishal/teaching/badm350/canvas-html/week-NN-start-here.html`

### 3. Generate Assignment HTML

Identify assignment type from lab deliverable section:
- **Lab**: Hands-on practice, 10 pts, completion-based rubric
- **Discussion**: Article analysis + peer replies, 10-15 pts
- **Position Paper**: Debate prep + evidence, 15-20 pts
- **Essay**: Framework application + research, 15 pts

Apply appropriate template from `references/assignment-templates.md`.

Output to: `/Users/vishal/teaching/badm350/canvas-html/week-NN-[assignment-name].html`

### 4. Upload to Canvas

Use Canvas MCP tools:

**Create page:**
```
mcp__canvas-api__create_page(course_identifier="67619", title="Week N Start Here", body=<html>, published=true)
```

**Create module:**
```
mcp__canvas-api__create_module(course_identifier="67619", name="Week N: Topic", position=N, published=true)
```

**Add item to module:**
```
mcp__canvas-api__add_module_item(course_identifier="67619", module_id=<id>, item_type="Page", page_url="week-n-start-here")
```

**Create assignment:**
```
mcp__canvas-api__create_assignment(
  course_identifier="67619",
  name="Assignment Name",
  description=<generated_html>,
  points_possible=10,
  submission_types="online_text_entry",
  due_at="2026-01-26T05:59:00Z"
)
```

### 5. Generate Setup Instructions

Create `/Users/vishal/teaching/badm350/canvas-html/week-NN-canvas-setup.md` with:
- Canvas assignment settings (name, points, due date, submission type)
- Rubric configuration table
- Module item order

## Key Style Elements

| Element | Value |
|---------|-------|
| Icons | Orange `#ff5f05` |
| Footer | Navy `#12284c` |
| CSS | `https://instructure-uploads.s3.amazonaws.com/account_145590000000000001/attachments/9675811/dp_app.css` |
| JS | `https://instructure-uploads.s3.amazonaws.com/account_145590000000000001/attachments/9675810/dp_app.js` |
| Banner | `https://files.ciditools.com/illinoisedu/UIUC_banner_Creative_1.png` |

## Session Structure (Tuesday/Thursday)

Each session has three phases:
- **Before Class**: Checklist of prep tasks with time estimates
- **During Class**: Table with Time | Activity | Purpose columns
- **After Class**: Tasks and upcoming deliverables

## Reference Files

- `references/start-here-template.md` - Full HTML template for Start Here pages
- `references/assignment-templates.md` - Templates for Lab, Discussion, Position Paper, Essay
- `references/rubric-patterns.md` - Standard rubric configurations

## Canvas Course Info

- **Course ID**: 67619 (Spring 2026)
- **Format**: On-campus, Tuesday/Thursday, 75 min each
- **Class Size**: ~19 students
