---
name: assistant-architect
description: Create AI Studio Assistant Architect JSON import files from screenshots or descriptions. Use when users provide a screenshot of a form/UI to replicate, describe an assistant they want built, or need to generate multi-prompt workflow JSON for PSD AI Studio.
triggers:
  - "create assistant"
  - "build assistant"
  - "assistant architect"
  - "ai studio assistant"
  - "assistant json"
  - "new assistant"
  - "design assistant"
  - "make this into an assistant"
  - "turn this into an assistant"
allowed-tools: Read, Write, AskUserQuestion
version: 1.2.0
---

# Assistant Architect

Create valid JSON import files for PSD AI Studio's Assistant Architect system.

**Spec Reference:** See `references/json-spec.md` for complete field definitions and validation rules.

---

## Input Modes

### From Screenshot

When the user provides a screenshot, extract:

| Element | Maps To |
|---------|---------|
| Text input boxes | `short_text` (single line) or `long_text` (multi-line) |
| Dropdowns/select menus | `select` with choices from visible options |
| Checkboxes/multi-select | `multi_select` |
| File upload areas | `file_upload` |
| Field labels | `label` property |
| Placeholder text | `options.placeholder` |
| Visible instructions | `system_context` or prompt `content` |
| Step numbers/tabs | Multiple prompts in sequence |

Also infer:
- **Assistant name** from title/header
- **Description** from any visible purpose text
- **Prompt content** from visible instructions or "what this does" text

### Handling Collapsed Dropdowns

**CRITICAL:** When you see a dropdown in a screenshot but can't see its options (e.g., shows "Select subject" or has a dropdown arrow but options aren't expanded), you MUST resolve the options before generating JSON.

**Resolution order:**

1. **Check if it matches a Common Field Library** (see below)
   - "Grade", "Grade Level" → Use Grade Levels library
   - "Subject", "Content Area" → Use Subjects library
   - "State" → Use US States library
   - "Language" → Use Language library
   - "Tone", "Style" → Use Writing Tone library
   - "Format", "Output Format" → Use Output Format library

2. **If no library match, ASK the user:**
   ```
   I see a dropdown for "[Field Name]" but can't see the options.

   Options:
   a) Provide a screenshot with the dropdown expanded
   b) List the values that should appear (comma-separated)
   c) Describe the type of options (e.g., "departments in our district")
   ```

3. **Never leave a select field without choices** - this will cause import errors

**Visual indicators of dropdowns:**
- Dropdown arrow (▼ or chevron) on right side
- "Select..." placeholder text
- Bordered box that looks clickable but isn't a text input
- Different styling from text inputs (often lighter/grayed placeholder)

### From Description (Dictation/Rambling)

Parse unstructured input for:

| Look For | Maps To |
|----------|---------|
| "user provides/enters/types..." | Input field |
| "asks for/needs a..." | Input field |
| "choose from/select/pick..." | `select` field |
| "upload/attach file..." | `file_upload` field |
| "then/next/after that..." | Additional prompt (chained) |
| "analyze/summarize/write/create..." | Prompt purpose |
| "should be/must be/format as..." | System context or prompt instructions |

### Smart Defaults

When not specified, use:

| Decision | Default |
|----------|---------|
| Model | `gpt-4o` (complex tasks), `gpt-4o-mini` (simple Q&A) |
| Field type for text | `long_text` with 6 rows |
| Execution | Sequential (single prompt unless steps mentioned) |
| Timeouts | `null` (system default) |
| Required fields | `true` for primary input, `false` for options |

---

## Workflow

### 1. Gather Requirements

**If screenshot provided:** Extract all visible elements per the table above.

**If description provided:** Parse for inputs, outputs, and flow.

**If unclear or incomplete:** Ask targeted questions:
- What should the assistant do?
- What inputs does it need?
- Single or multi-step?

### 1.5 Resolve All Dropdown Options (REQUIRED)

**Before generating JSON, ensure every dropdown has defined options.**

For each dropdown/select field identified:

| If... | Then... |
|-------|---------|
| Options are visible in screenshot | Extract them exactly |
| Field matches a Common Field Library | Use the library options |
| Field is domain-specific (e.g., "Department", "Building", "Program") | **ASK the user for the list** |
| Unclear what options should be | **ASK the user** |

**Example question format:**
```
I found these dropdowns that need options defined:

1. **Department** - What departments should be listed?
2. **Building** - What buildings/schools should be included?
3. **Program Type** - What program types exist?

You can provide comma-separated values, or share a screenshot with dropdowns expanded.
```

**Do NOT proceed to JSON generation with unresolved dropdowns.**

### 2. Design the Assistant

Based on requirements, determine:

| Decision | Options |
|----------|---------|
| Execution pattern | Sequential (default) / Parallel / Chained |
| Model selection | `gpt-4o` (complex) / `gpt-4o-mini` (simple) / `claude-3-5-sonnet` |
| Input fields | `short_text`, `long_text`, `select`, `multi_select`, `file_upload` |
| Timeouts | Default null, max 900 seconds |

### 3. Generate JSON

Build the JSON structure:

```json
{
  "version": "1.0",
  "exported_at": "[ISO-8601 timestamp]",
  "export_source": "Geoffrey Assistant Architect",
  "assistants": [{
    "name": "[Assistant Name]",
    "description": "[Purpose]",
    "is_parallel": false,
    "prompts": [...],
    "input_fields": [...]
  }]
}
```

### 4. Write the File

Save to user's preferred location (default: `~/Downloads/[assistant-name].json`).

---

## Quick Patterns

### Simple Q&A Assistant

```json
{
  "version": "1.0",
  "export_source": "Geoffrey Assistant Architect",
  "assistants": [{
    "name": "Quick Helper",
    "description": "Answers questions clearly",
    "prompts": [{
      "name": "answer",
      "content": "Answer this question:\n\n{{question}}",
      "system_context": "You are a helpful expert.",
      "model_name": "gpt-4o-mini",
      "position": 0
    }],
    "input_fields": [{
      "name": "question",
      "label": "Your Question",
      "field_type": "long_text",
      "position": 0,
      "options": { "required": true, "rows": 6 }
    }]
  }]
}
```

### Document Analyzer (Chained)

```json
{
  "prompts": [
    {
      "name": "extract",
      "content": "Extract key points from:\n\n{{document}}",
      "model_name": "gpt-4o",
      "position": 0
    },
    {
      "name": "analyze",
      "content": "Analyze these points:\n\n{{prompt_0_output}}",
      "model_name": "gpt-4o",
      "position": 1
    }
  ]
}
```

### Transform with Options

```json
{
  "prompts": [{
    "name": "transform",
    "content": "Rewrite in {{style}} style:\n\n{{content}}",
    "model_name": "gpt-4o",
    "position": 0
  }],
  "input_fields": [
    {
      "name": "content",
      "label": "Content",
      "field_type": "long_text",
      "position": 0
    },
    {
      "name": "style",
      "label": "Writing Style",
      "field_type": "select",
      "position": 1,
      "options": {
        "choices": [
          { "value": "formal", "label": "Formal" },
          { "value": "casual", "label": "Casual" },
          { "value": "technical", "label": "Technical" }
        ],
        "default": "formal"
      }
    }
  ]
}
```

---

## Validation Checklist

Before writing the file, verify:

- [ ] `version` is `"1.0"`
- [ ] Each assistant has `name` (min 3 chars), `prompts`, `input_fields`
- [ ] Each prompt has `name`, `content`, `model_name`, `position`
- [ ] Each input field has `name`, `label`, `field_type`, `position`
- [ ] `position` values are sequential starting from 0
- [ ] All `{{variables}}` match input field names or `prompt_N_output`
- [ ] **CRITICAL: Every `select` and `multi_select` field has `options.choices` array with at least 2 items**
- [ ] No dropdown was left with placeholder options like "Option 1", "Option 2"
- [ ] Domain-specific dropdowns (departments, buildings, programs) have real values from user

---

## Common Models

| Use Case | Model |
|----------|-------|
| Complex analysis | `gpt-4o` |
| Simple tasks | `gpt-4o-mini` |
| Long context | `claude-3-5-sonnet` |
| Fast responses | `gemini-1.5-flash` |

---

## Common Field Libraries

**CRITICAL:** When a field represents a finite set of choices (grade levels, subjects, states, etc.), ALWAYS use `select` or `multi_select` with proper options—NEVER use `short_text` or `long_text`.

### Detecting Select Fields

If the screenshot or description contains ANY of these patterns, use a select field:

| Pattern | Field Type |
|---------|------------|
| "Select...", "Choose...", dropdown arrow | `select` |
| "Pick one", "Which...", finite list | `select` |
| "Check all that apply", multiple checkboxes | `multi_select` |
| Grade level, subject, state, language, format | `select` (use library below) |

### Grade Levels (K-12)

```json
{
  "name": "grade_level",
  "label": "Grade Level",
  "field_type": "select",
  "options": {
    "required": true,
    "choices": [
      { "value": "Pre-K", "label": "Pre-K" },
      { "value": "Kindergarten", "label": "Kindergarten" },
      { "value": "1st Grade", "label": "1st Grade" },
      { "value": "2nd Grade", "label": "2nd Grade" },
      { "value": "3rd Grade", "label": "3rd Grade" },
      { "value": "4th Grade", "label": "4th Grade" },
      { "value": "5th Grade", "label": "5th Grade" },
      { "value": "6th Grade", "label": "6th Grade" },
      { "value": "7th Grade", "label": "7th Grade" },
      { "value": "8th Grade", "label": "8th Grade" },
      { "value": "9th Grade", "label": "9th Grade" },
      { "value": "10th Grade", "label": "10th Grade" },
      { "value": "11th Grade", "label": "11th Grade" },
      { "value": "12th Grade", "label": "12th Grade" }
    ]
  }
}
```

### Subjects (K-12)

```json
{
  "name": "subject",
  "label": "Subject",
  "field_type": "select",
  "options": {
    "required": true,
    "choices": [
      { "value": "English Language Arts", "label": "English Language Arts" },
      { "value": "Mathematics", "label": "Mathematics" },
      { "value": "Science", "label": "Science" },
      { "value": "Social Studies", "label": "Social Studies" },
      { "value": "History", "label": "History" },
      { "value": "World Languages", "label": "World Languages" },
      { "value": "Physical Education", "label": "Physical Education" },
      { "value": "Health", "label": "Health" },
      { "value": "Visual Arts", "label": "Visual Arts" },
      { "value": "Music", "label": "Music" },
      { "value": "Theater/Drama", "label": "Theater/Drama" },
      { "value": "Computer Science", "label": "Computer Science" },
      { "value": "Career & Technical Education", "label": "Career & Technical Education" },
      { "value": "Special Education", "label": "Special Education" },
      { "value": "Library/Media", "label": "Library/Media" },
      { "value": "Counseling", "label": "Counseling" },
      { "value": "Other", "label": "Other" }
    ]
  }
}
```

### US States

```json
{
  "name": "state",
  "label": "State",
  "field_type": "select",
  "options": {
    "required": true,
    "default": "Washington",
    "choices": [
      { "value": "Alabama", "label": "Alabama" },
      { "value": "Alaska", "label": "Alaska" },
      { "value": "Arizona", "label": "Arizona" },
      { "value": "Arkansas", "label": "Arkansas" },
      { "value": "California", "label": "California" },
      { "value": "Colorado", "label": "Colorado" },
      { "value": "Connecticut", "label": "Connecticut" },
      { "value": "Delaware", "label": "Delaware" },
      { "value": "Florida", "label": "Florida" },
      { "value": "Georgia", "label": "Georgia" },
      { "value": "Hawaii", "label": "Hawaii" },
      { "value": "Idaho", "label": "Idaho" },
      { "value": "Illinois", "label": "Illinois" },
      { "value": "Indiana", "label": "Indiana" },
      { "value": "Iowa", "label": "Iowa" },
      { "value": "Kansas", "label": "Kansas" },
      { "value": "Kentucky", "label": "Kentucky" },
      { "value": "Louisiana", "label": "Louisiana" },
      { "value": "Maine", "label": "Maine" },
      { "value": "Maryland", "label": "Maryland" },
      { "value": "Massachusetts", "label": "Massachusetts" },
      { "value": "Michigan", "label": "Michigan" },
      { "value": "Minnesota", "label": "Minnesota" },
      { "value": "Mississippi", "label": "Mississippi" },
      { "value": "Missouri", "label": "Missouri" },
      { "value": "Montana", "label": "Montana" },
      { "value": "Nebraska", "label": "Nebraska" },
      { "value": "Nevada", "label": "Nevada" },
      { "value": "New Hampshire", "label": "New Hampshire" },
      { "value": "New Jersey", "label": "New Jersey" },
      { "value": "New Mexico", "label": "New Mexico" },
      { "value": "New York", "label": "New York" },
      { "value": "North Carolina", "label": "North Carolina" },
      { "value": "North Dakota", "label": "North Dakota" },
      { "value": "Ohio", "label": "Ohio" },
      { "value": "Oklahoma", "label": "Oklahoma" },
      { "value": "Oregon", "label": "Oregon" },
      { "value": "Pennsylvania", "label": "Pennsylvania" },
      { "value": "Rhode Island", "label": "Rhode Island" },
      { "value": "South Carolina", "label": "South Carolina" },
      { "value": "South Dakota", "label": "South Dakota" },
      { "value": "Tennessee", "label": "Tennessee" },
      { "value": "Texas", "label": "Texas" },
      { "value": "Utah", "label": "Utah" },
      { "value": "Vermont", "label": "Vermont" },
      { "value": "Virginia", "label": "Virginia" },
      { "value": "Washington", "label": "Washington" },
      { "value": "West Virginia", "label": "West Virginia" },
      { "value": "Wisconsin", "label": "Wisconsin" },
      { "value": "Wyoming", "label": "Wyoming" },
      { "value": "District of Columbia", "label": "District of Columbia" }
    ]
  }
}
```

### Learning Standards Frameworks

```json
{
  "name": "standards_framework",
  "label": "Standards Framework",
  "field_type": "select",
  "options": {
    "required": false,
    "choices": [
      { "value": "Common Core State Standards (CCSS)", "label": "Common Core State Standards (CCSS)" },
      { "value": "Next Generation Science Standards (NGSS)", "label": "Next Generation Science Standards (NGSS)" },
      { "value": "C3 Framework (Social Studies)", "label": "C3 Framework (Social Studies)" },
      { "value": "ISTE Standards", "label": "ISTE Standards (Technology)" },
      { "value": "National Core Arts Standards", "label": "National Core Arts Standards" },
      { "value": "SHAPE America Standards (PE/Health)", "label": "SHAPE America Standards (PE/Health)" },
      { "value": "ACTFL Standards (World Languages)", "label": "ACTFL Standards (World Languages)" },
      { "value": "State-Specific Standards", "label": "State-Specific Standards" },
      { "value": "Other", "label": "Other" }
    ]
  }
}
```

### Writing Tone/Style

```json
{
  "name": "tone",
  "label": "Tone",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "professional", "label": "Professional" },
      { "value": "friendly", "label": "Friendly" },
      { "value": "formal", "label": "Formal" },
      { "value": "casual", "label": "Casual" },
      { "value": "encouraging", "label": "Encouraging" },
      { "value": "academic", "label": "Academic" },
      { "value": "conversational", "label": "Conversational" }
    ],
    "default": "professional"
  }
}
```

### Output Format

```json
{
  "name": "output_format",
  "label": "Output Format",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "paragraph", "label": "Paragraph" },
      { "value": "bullet_points", "label": "Bullet Points" },
      { "value": "numbered_list", "label": "Numbered List" },
      { "value": "table", "label": "Table" },
      { "value": "outline", "label": "Outline" }
    ],
    "default": "paragraph"
  }
}
```

### Length/Detail Level

```json
{
  "name": "length",
  "label": "Length",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "brief", "label": "Brief (1-2 sentences)" },
      { "value": "short", "label": "Short (1 paragraph)" },
      { "value": "medium", "label": "Medium (2-3 paragraphs)" },
      { "value": "detailed", "label": "Detailed (comprehensive)" }
    ],
    "default": "medium"
  }
}
```

### Audience

```json
{
  "name": "audience",
  "label": "Audience",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "students", "label": "Students" },
      { "value": "parents", "label": "Parents/Guardians" },
      { "value": "teachers", "label": "Teachers" },
      { "value": "administrators", "label": "Administrators" },
      { "value": "school_board", "label": "School Board" },
      { "value": "community", "label": "Community Members" },
      { "value": "general", "label": "General Audience" }
    ]
  }
}
```

### Language (for multilingual support)

```json
{
  "name": "language",
  "label": "Output Language",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "English", "label": "English" },
      { "value": "Spanish", "label": "Spanish" },
      { "value": "Vietnamese", "label": "Vietnamese" },
      { "value": "Chinese (Simplified)", "label": "Chinese (Simplified)" },
      { "value": "Chinese (Traditional)", "label": "Chinese (Traditional)" },
      { "value": "Korean", "label": "Korean" },
      { "value": "Tagalog", "label": "Tagalog" },
      { "value": "Russian", "label": "Russian" },
      { "value": "Arabic", "label": "Arabic" },
      { "value": "Somali", "label": "Somali" },
      { "value": "Ukrainian", "label": "Ukrainian" }
    ],
    "default": "English"
  }
}
```

---

## K-12 District-Specific Field Libraries

**SCOPE:** Use these libraries ONLY when building AI Studio assistants for educational/instructional purposes (lesson plans, assessments, student feedback, curriculum tools, etc.).

**Pedagogical alignment:** For educational assistants, reference PSD's Instructional Essentials skill (`/psd-instructional-vision`) to ensure alignment with district beliefs about rigor, inclusion, data-driven decisions, and innovation.

### ELA Standards Domains

```json
{
  "name": "ela_domain",
  "label": "ELA Domain",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Reading Literature", "label": "Reading Literature" },
      { "value": "Reading Informational Text", "label": "Reading Informational Text" },
      { "value": "Reading Foundational Skills", "label": "Reading Foundational Skills" },
      { "value": "Writing", "label": "Writing" },
      { "value": "Speaking and Listening", "label": "Speaking and Listening" },
      { "value": "Language", "label": "Language" }
    ]
  }
}
```

### Math Standards Domains

```json
{
  "name": "math_domain",
  "label": "Math Domain",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Counting and Cardinality", "label": "Counting and Cardinality (K)" },
      { "value": "Operations and Algebraic Thinking", "label": "Operations and Algebraic Thinking" },
      { "value": "Number and Operations in Base Ten", "label": "Number and Operations in Base Ten" },
      { "value": "Number and Operations - Fractions", "label": "Number and Operations - Fractions" },
      { "value": "Measurement and Data", "label": "Measurement and Data" },
      { "value": "Geometry", "label": "Geometry" },
      { "value": "Ratios and Proportional Relationships", "label": "Ratios and Proportional Relationships" },
      { "value": "The Number System", "label": "The Number System" },
      { "value": "Expressions and Equations", "label": "Expressions and Equations" },
      { "value": "Functions", "label": "Functions" },
      { "value": "Statistics and Probability", "label": "Statistics and Probability" }
    ]
  }
}
```

### Science Standards Domains (NGSS)

```json
{
  "name": "science_domain",
  "label": "Science Domain",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Physical Science", "label": "Physical Science" },
      { "value": "Life Science", "label": "Life Science" },
      { "value": "Earth and Space Science", "label": "Earth and Space Science" },
      { "value": "Engineering Design", "label": "Engineering Design" }
    ]
  }
}
```

### Grade Bands

```json
{
  "name": "grade_band",
  "label": "Grade Band",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "K-2", "label": "K-2 (Primary)" },
      { "value": "3-5", "label": "3-5 (Intermediate)" },
      { "value": "6-8", "label": "6-8 (Middle School)" },
      { "value": "9-12", "label": "9-12 (High School)" }
    ]
  }
}
```

### Student Population / Learner Characteristics

```json
{
  "name": "student_population",
  "label": "Student Population",
  "field_type": "multi_select",
  "options": {
    "choices": [
      { "value": "General Education", "label": "General Education" },
      { "value": "English Learners (EL/MLL)", "label": "English Learners (EL/MLL)" },
      { "value": "Students with IEPs", "label": "Students with IEPs" },
      { "value": "Students with 504 Plans", "label": "Students with 504 Plans" },
      { "value": "Highly Capable", "label": "Highly Capable/Gifted" },
      { "value": "At-Risk", "label": "At-Risk/Tier 2-3" }
    ]
  }
}
```

### Instructional Model (aligned with PSD Tier 1 practices)

```json
{
  "name": "instructional_model",
  "label": "Instructional Model",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Whole Group", "label": "Whole Group Direct Instruction" },
      { "value": "Small Group", "label": "Small Group (Flexible Grouping)" },
      { "value": "Stations/Centers", "label": "Stations/Learning Centers" },
      { "value": "Workshop Model", "label": "Workshop Model (Mini-lesson → Work Time → Share)" },
      { "value": "Guided Practice", "label": "Gradual Release (I Do, We Do, You Do)" },
      { "value": "Inquiry-Based", "label": "Inquiry-Based/Project-Based" },
      { "value": "Flipped", "label": "Flipped Classroom" },
      { "value": "Co-Teaching", "label": "Co-Teaching" }
    ]
  }
}
```

### Assessment Type (aligned with Data-Driven Decisions essential)

```json
{
  "name": "assessment_type",
  "label": "Assessment Type",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Formative - Exit Ticket", "label": "Formative - Exit Ticket" },
      { "value": "Formative - Check for Understanding", "label": "Formative - Check for Understanding" },
      { "value": "Formative - Observation", "label": "Formative - Observation/Anecdotal" },
      { "value": "Formative - Student Self-Assessment", "label": "Formative - Student Self-Assessment" },
      { "value": "Summative - Unit Test", "label": "Summative - Unit Test" },
      { "value": "Summative - Project/Performance", "label": "Summative - Project/Performance Task" },
      { "value": "Summative - Portfolio", "label": "Summative - Portfolio" },
      { "value": "Benchmark/Interim", "label": "Benchmark/Interim Assessment" },
      { "value": "Diagnostic", "label": "Diagnostic/Pre-Assessment" }
    ]
  }
}
```

### Lesson Duration

```json
{
  "name": "lesson_duration",
  "label": "Lesson Duration",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "15-20 minutes", "label": "15-20 minutes (Mini-lesson)" },
      { "value": "30 minutes", "label": "30 minutes" },
      { "value": "45 minutes", "label": "45 minutes (Standard period)" },
      { "value": "60 minutes", "label": "60 minutes" },
      { "value": "90 minutes", "label": "90 minutes (Block)" },
      { "value": "Multi-day", "label": "Multi-day lesson" }
    ]
  }
}
```

### Bloom's Taxonomy Level (Depth of Knowledge)

```json
{
  "name": "cognitive_level",
  "label": "Cognitive Level",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Remember", "label": "Remember (Recall facts)" },
      { "value": "Understand", "label": "Understand (Explain ideas)" },
      { "value": "Apply", "label": "Apply (Use in new situations)" },
      { "value": "Analyze", "label": "Analyze (Draw connections)" },
      { "value": "Evaluate", "label": "Evaluate (Justify decisions)" },
      { "value": "Create", "label": "Create (Produce new work)" }
    ]
  }
}
```

### Depth of Knowledge (Webb's DOK)

```json
{
  "name": "dok_level",
  "label": "Depth of Knowledge",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "DOK 1", "label": "DOK 1 - Recall" },
      { "value": "DOK 2", "label": "DOK 2 - Skill/Concept" },
      { "value": "DOK 3", "label": "DOK 3 - Strategic Thinking" },
      { "value": "DOK 4", "label": "DOK 4 - Extended Thinking" }
    ]
  }
}
```

### Educator Role

```json
{
  "name": "role",
  "label": "Role",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Classroom Teacher", "label": "Classroom Teacher" },
      { "value": "Special Education Teacher", "label": "Special Education Teacher" },
      { "value": "EL/MLL Specialist", "label": "EL/MLL Specialist" },
      { "value": "Instructional Coach", "label": "Instructional Coach" },
      { "value": "Counselor", "label": "School Counselor" },
      { "value": "Librarian", "label": "Teacher-Librarian" },
      { "value": "Paraeducator", "label": "Paraeducator/IA" },
      { "value": "Principal", "label": "Principal" },
      { "value": "Assistant Principal", "label": "Assistant Principal" },
      { "value": "District Staff", "label": "District Staff" }
    ]
  }
}
```

### School Level

```json
{
  "name": "school_level",
  "label": "School Level",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Elementary", "label": "Elementary School" },
      { "value": "Middle", "label": "Middle School" },
      { "value": "High", "label": "High School" },
      { "value": "K-8", "label": "K-8 School" },
      { "value": "Alternative", "label": "Alternative School" },
      { "value": "District-Wide", "label": "District-Wide" }
    ]
  }
}
```

### Communication Type

```json
{
  "name": "communication_type",
  "label": "Communication Type",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Parent Newsletter", "label": "Parent Newsletter" },
      { "value": "Parent Email", "label": "Parent Email" },
      { "value": "Student Feedback", "label": "Student Feedback" },
      { "value": "IEP/504 Communication", "label": "IEP/504 Communication" },
      { "value": "Behavior Communication", "label": "Behavior Communication" },
      { "value": "Progress Report", "label": "Progress Report" },
      { "value": "Staff Communication", "label": "Staff Communication" },
      { "value": "Community Announcement", "label": "Community Announcement" }
    ]
  }
}
```

### Quarter/Trimester

```json
{
  "name": "grading_period",
  "label": "Grading Period",
  "field_type": "select",
  "options": {
    "choices": [
      { "value": "Q1", "label": "Quarter 1" },
      { "value": "Q2", "label": "Quarter 2" },
      { "value": "Q3", "label": "Quarter 3" },
      { "value": "Q4", "label": "Quarter 4" },
      { "value": "Semester 1", "label": "Semester 1" },
      { "value": "Semester 2", "label": "Semester 2" },
      { "value": "Full Year", "label": "Full Year" },
      { "value": "Summer", "label": "Summer" }
    ]
  }
}
```

---

## Making Reasonable Assumptions

**For general assistants:** Use the Common Field Libraries (grade, subject, state, tone, format, etc.).

**For educational/instructional assistants:** Use the K-12 District-Specific Field Libraries above AND invoke the PSD Instructional Vision skill (`/psd-instructional-vision`) for pedagogical alignment.

### Educational Assistant Decision Framework

When a dropdown's options aren't visible in a screenshot for an educational tool:

| Field Type | Assumption Strategy |
|------------|---------------------|
| Grade/Subject/State | Use Common Field Libraries |
| Standards | Use domain-level dropdowns (ELA, Math, Science domains) + text for specific codes |
| Roles/Positions | Use Educator Role library |
| Time/Duration | Use Lesson Duration or Grading Period library |
| Assessment | Use Assessment Type library |
| Instructional approach | Use Instructional Model library |
| Student groups | Use Student Population library |
| Cognitive rigor | Use Bloom's or DOK library |
| District-specific (buildings, departments) | **Ask user** - these vary by district |

### PSD Instructional Essentials Alignment

When building educational AI Studio assistants, ensure options align with PSD's four essentials:

- **Rigor & Inclusion** → Include scaffolding options, differentiation choices, support for all learners
- **Data-Driven Decisions** → Include assessment type options, formative check options
- **Continuous Growth** → Include reflection prompts, self-assessment, goal-setting options
- **Innovation** → Include technology integration, real-world connection, student voice options

---

## Output

Write the JSON file to the user's specified path or `~/Downloads/[kebab-case-name].json`.

Confirm:
- File path written
- Assistant name and purpose
- Number of prompts and input fields
- Next step: Import via AI Studio → Assistants → Import
