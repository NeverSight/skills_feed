---
name: learning-design-checklist
description: Generate a quick compliance checklist from the Four Learning Design Pillars. Use when users want a practical checklist for reviewing content, a quick audit tool, or verification questions for specific pillars.
---

# Learning Design Checklist Generator

Generate actionable verification checklists from the Four Learning Design Pillars.

## Skill Purpose

This skill creates practical checklists using the verification questions from the learning design framework. Unlike the full review skill, this produces quick, scannable checklists for rapid content verification.

## Usage

```bash
/learning-design-checklist                    # Full checklist (all pillars)
/learning-design-checklist --pillar 1         # Structure pillar only
/learning-design-checklist --pillar 3         # Practice & Feedback only
/learning-design-checklist --canvas           # Canvas LMS-specific checklist
```

## Workflow

### Step 1: Determine Scope

Ask user which checklist they need:
- **Full checklist**: All 4 pillars (~46 items)
- **Single pillar**: Focus on one area
- **Canvas-specific**: Tailored to Canvas LMS features

### Step 2: Load and Generate Checklist

Read from `{SKILL_DIR}/../principles/learning-design-pillars.json`

The JSON contains `checks` arrays for each principle - use these for checklist items.

### Step 3: Output Format

Generate checklist in markdown format:

```markdown
# Learning Design Checklist

## Pillar 1: Clear, Purposeful Structure

### 1.1 Content Organization
- [ ] Is content chunked into bite-sized units? (1.1.1)
- [ ] Does each screen/page have a single primary idea? (1.1.1)
- [ ] Can a learner understand each segment without hunting elsewhere? (1.1.2)
- [ ] Are prerequisites stated or embedded? (1.1.2)
- [ ] Do later concepts require earlier ones that are already taught? (1.1.3)
- [ ] Is complexity increasing gradually? (1.1.3)
- [ ] Can a learner scan and instantly see structure and priority? (1.1.4)
- [ ] Are learners guided on what to focus on and why? (1.1.5)

### 1.2 Design Consistency
- [ ] Do screens behave consistently across the course? (1.2.1)
- [ ] Are learners forced to jump between tools/screens unnecessarily? (1.2.2)
- [ ] Do later modules build on earlier ones with consistent expectations? (1.2.3)

### 1.3 Learning Path Clarity
- [ ] Can a learner tell what success looks like? (1.3.1)
- [ ] Does every unit begin with orientation and end with consolidation? (1.3.2)
- [ ] Is every activity clearly tied to an objective? (1.3.3)
- [ ] Are expectations explicit (time, quality, grading, outcomes)? (1.3.4)
- [ ] Are prerequisites and structure clearly communicated? (1.3.5)

### 1.4 Adaptive Learning Design
- [ ] Is there planned re-exposure later in the program? (1.4.1)
- [ ] Can experienced learners move faster without losing coherence? (1.4.2)

---

## Pillar 2: Active, Engaging Learning Content

### 2.1 Content Design & Presentation
- [ ] Is content succinct and focused on objectives? (2.1.1)
- [ ] Does content use both visual and verbal mediums? (2.1.2)
- [ ] Are graphics relevant, not purely decorative? (2.1.3)
- [ ] Are related text and visuals placed near each other? (2.1.4)
- [ ] Is text scannable with short paragraphs and headings? (2.1.5)
- [ ] Is additional detail revealed on demand? (2.1.6)
- [ ] Can users jump to content of interest? (2.1.7)
- [ ] Are fonts readable and audio audible? (2.1.8)

### 2.2 Multimedia & Interactive Elements
- [ ] Is multimedia used to increase engagement? (2.2.1)
- [ ] Does content prioritize doing over passive reading? (2.2.2)
- [ ] Are videos under 10 minutes? (2.2.3)
- [ ] Does video narration explain visuals? (2.2.4)
- [ ] Is on-screen text used sparingly in videos? (2.2.5)
- [ ] Are audio and visuals synchronized? (2.2.6)

### 2.3 Engagement & Relevance
- [ ] Is language conversational and relatable? (2.3.1)
- [ ] Is the purpose of features explained to learners? (2.3.2)
- [ ] Are prior knowledge connections activated? (2.3.3)
- [ ] Are storytelling elements used when appropriate? (2.3.4)
- [ ] Do lessons start concrete before moving to abstract? (2.3.5)
- [ ] Is difficulty appropriately calibrated? (2.3.6)
- [ ] Are examples relevant and interesting to learners? (2.3.7)
- [ ] Are key terms highlighted and defined? (2.3.8a)
- [ ] Are multiple perspectives and examples provided? (2.3.8b)

### 2.4 Quality and Accessibility
- [ ] Are supplementary resources available? (2.4.1)
- [ ] Is content current, accurate, and sourced? (2.4.2)
- [ ] Is content free from bias and discrimination? (2.4.3)
- [ ] Are credibility indicators present? (2.4.4)

---

## Pillar 3: Continuous Practice & Feedback

### 3.1 Practice Design & Variety
- [ ] Is practice varied across contexts? (3.1.1)
- [ ] Are skills/concepts interleaved in practice? (3.1.2)
- [ ] Does practice cycle back over time? (3.1.3)
- [ ] Are recall-heavy prompts used? (3.1.4)
- [ ] Does practice reflect real-world contexts? (3.1.5)
- [ ] Is low-stakes practice available? (3.1.6)
- [ ] Are prior skills practiced before new topics? (3.1.7)

### 3.2 Feedback & Assessment
- [ ] Is feedback specific and actionable? (3.2.1)
- [ ] Is feedback encouraging in tone? (3.2.2)
- [ ] Is feedback delivered immediately? (3.2.3)
- [ ] Are worked examples provided and faded? (3.2.4)
- [ ] Are rubrics and expectations clear? (3.2.5)

### 3.3 Metacognition & Deep Learning
- [ ] Can learners accurately assess their progress? (3.3.1)
- [ ] Are why/how/what-if questions used? (3.3.2)
- [ ] Are reflection prompts included? (3.3.3)
- [ ] Are collaboration opportunities provided? (3.3.4)

---

## Pillar 4: Simple, Intuitive UX

### 4.1 Navigation & Orientation
- [ ] Is navigation intuitive? (4.1.1)
- [ ] Are progress/location indicators visible? (4.1.2)
- [ ] Are interactive elements clearly distinguishable? (4.1.3)
- [ ] Is the system self-contained with external links labeled? (4.1.4)
- [ ] Can returning learners easily find their place? (4.1.5)

### 4.2 Accessibility & Optimization
- [ ] Is search functionality available? (4.2.1)
- [ ] Are annotation tools provided? (4.2.2)
- [ ] Is content viewable on different screen sizes? (4.2.3)
- [ ] Can display preferences be customized? (4.2.4)
- [ ] Is the design minimalist and clear? (4.2.5)

### 4.3 Media Control & Time
- [ ] Can learners control video pace? (4.3.1)
- [ ] Are time estimates provided? (4.3.2)
```

## Canvas-Specific Checklist Variant

When `--canvas` flag is used, generate Canvas LMS-tailored checklist:

```markdown
# Canvas Course Design Checklist

## Structure (Pillar 1)
- [ ] Modules named consistently (e.g., "Week 1: Topic")
- [ ] Module requirements set for sequencing
- [ ] Learning objectives in module descriptions
- [ ] Prerequisites configured where needed
- [ ] Welcome/orientation module exists
- [ ] Course home page provides clear navigation

## Content (Pillar 2)
- [ ] Pages use H1/H2/H3 hierarchy
- [ ] Images have alt text
- [ ] Videos under 10 minutes (or segmented)
- [ ] Canvas Studio used with captions
- [ ] Discussions encourage active participation
- [ ] External tools clearly labeled

## Practice & Feedback (Pillar 3)
- [ ] Practice quizzes with unlimited attempts
- [ ] Rubrics attached to all graded assignments
- [ ] Peer reviews configured where appropriate
- [ ] Quiz feedback shows correct answers
- [ ] Assignment feedback turnaround < 7 days
- [ ] Self-check opportunities in modules

## UX (Pillar 4)
- [ ] Unused navigation items hidden
- [ ] Modules view set as home page
- [ ] Content tested on mobile
- [ ] Module progress tracking enabled
- [ ] Assignment time estimates included
- [ ] Video durations displayed
```

## Related Skills

- `/learning-design-review` - Full analysis with scores and recommendations
- `/canvas-course-audit` - Automated Canvas course audit
