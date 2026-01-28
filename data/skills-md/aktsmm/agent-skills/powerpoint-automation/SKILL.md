---
name: powerpoint-automation
description: Create professional PowerPoint presentations from various sources including web articles, blog posts, and existing PPTX files. Ideal for tech presentations, reports, and documentation.
license: Complete terms in LICENSE.txt
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# PowerPoint Automation

AI-powered PPTX generation pipeline using Orchestrator-Workers pattern. Automatically extracts content, translates, applies templates, and performs quality reviews.

## When to Use This Skill

Use this skill when the user wants to:

- Convert web articles or blog posts to PowerPoint presentations
- Translate English PPTX to Japanese (or other languages)
- Create presentations using custom templates
- Generate technical presentations with code blocks and diagrams
- Automate presentation creation with quality assurance

## Quick Start

### Prerequisites

Install dependencies:

```powershell
# Python dependencies
pip install -r scripts/requirements.txt

# Node.js dependencies (for diagram generation)
npm install --prefix scripts
```

### Basic Usage

**From Web Article:**

```
# Simply describe what you want with a URL
"Create a 15-slide presentation about Azure Copilot from this Zenn article:
https://zenn.dev/example/articles/pptx-guide"

# The system will automatically:
# 1. Extract content and images
# 2. Generate content.json
# 3. Create PPTX with template
# 4. Review quality
```

**From Existing PPTX:**

```
# Provide PPTX file path in your request
"Translate this English presentation to Japanese: input/presentation.pptx"

# System will:
# 1. Analyze structure
# 2. Extract content
# 3. Translate (if needed)
# 4. Apply new template
```

## Architecture

This skill uses the **Orchestrator-Workers** pattern with 6 specialized agents.
See [Agents](#agents) section for details.

## Workflow Phases

```
TRIAGE → PLAN → PREPARE_TEMPLATE → EXTRACT → TRANSLATE → BUILD → REVIEW → DONE
```

### Phase Details

| Phase                | Script                                         | Description                                    |
| -------------------- | ---------------------------------------------- | ---------------------------------------------- |
| **TRIAGE**           | Orchestrator                                   | Detect input type, determine workflow          |
| **PLAN**             | User Confirmation                              | Present options (slide count, template, style) |
| **PREPARE_TEMPLATE** | `diagnose_template.py`, `clean_template.py`    | Clean and analyze template                     |
| **EXTRACT**          | `extract_images.py`, `reconstruct_analyzer.py` | Extract content → content.json                 |
| **TRANSLATE**        | Localizer Agent                                | Translate content.json                         |
| **BUILD**            | `create_from_template.py`                      | Generate PPTX                                  |
| **REVIEW**           | PPTX Reviewer Agent                            | Quality check                                  |
| **DONE**             | -                                              | Open PowerPoint                                |

## Key Scripts

See `references/SCRIPTS.md` for complete script documentation.

**Most Common:**

- `create_from_template.py` - Generate PPTX from content.json (⭐ Recommended)
- `reconstruct_analyzer.py` - Convert PPTX → content.json
- `extract_images.py` - Extract images from PPTX or web
- `validate_content.py` - Validate content.json schema
- `validate_pptx.py` - Detect text overflow, missing notes

**Specialized:**

- `create_pptx.js` - Generate diagrams with pptxgenjs
- `merge_slides.py` - Combine diagram slides into template
- `summarize_content.py` - Reduce slide count with AI

## Intermediate Representation (IR)

All agents communicate via **content.json** (SSOT):

```json
{
  "slides": [
    {
      "type": "title",
      "title": "Presentation Title",
      "subtitle": "Subtitle"
    },
    {
      "type": "content",
      "title": "Main Topic",
      "items": ["Point 1", "Point 2"],
      "image": {
        "path": "images/diagram.png",
        "position": "right",
        "width_percent": 45
      }
    }
  ]
}
```

See `references/schemas/content.schema.json` for full specification.

## Design Principles

1. **SSOT (Single Source of Truth)**: content.json is the canonical representation
2. **SRP (Single Responsibility)**: Each agent/script has one clear purpose
3. **Fail Fast**: Errors detected early, automatic retry (max 3×)
4. **Human in the Loop**: User confirmation at PLAN phase
5. **Dynamic Context**: Adapt to any template size, not hardcoded

## Templates

Two templates are included:

| Template                    | Purpose                                 | Size                 | Layouts    |
| --------------------------- | --------------------------------------- | -------------------- | ---------- |
| `assets/base_template.pptx` | Full-featured template with all layouts | 16:9 (13.33" × 7.5") | 11 layouts |
| `assets/template.pptx`      | Legacy template (Japanese layout names) | 16:9 (13.33" × 7.5") | 4 layouts  |

### When to Use Each Template

- **`base_template.pptx`** (Recommended): Full-featured template with 11 standard English layouts. Use for most presentations including tech blogs, reports, and translations. Works best with `analyze_template.py` auto-detection.
- **`template.pptx`**: Legacy template with Japanese layout names. Use if you need specific Japanese layout naming or compatibility with older workflows.

To use custom templates:

```powershell
python scripts/analyze_template.py path/to/custom.pptx
```

## Error Handling

- **Retry Policy**: Max 3 attempts per phase
- **Escalation**: After 3 failures → human intervention
- **Recovery**: `scripts/resume_workflow.py` to resume from specific phase

## Advanced Features

### Diagram Generation (pptxgenjs)

```javascript
// Create architecture diagrams with shapes and arrows
node scripts/create_pptx.js
```

### Slide Merging

```powershell
# Merge diagram slides into template
python scripts/merge_slides.py template.pptx diagrams.pptx output.pptx
```

### Content Summarization

```powershell
# Reduce slide count with AI summarization
python scripts/summarize_content.py content.json --target-slides 15
```

## Agents

Detailed agent definitions in `references/agents/`:

| Agent         | File                     | Purpose                                              |
| ------------- | ------------------------ | ---------------------------------------------------- |
| Orchestrator  | `orchestrator.agent.md`  | Pipeline coordination, state management, retry logic |
| Brainstormer  | `brainstormer.agent.md`  | Interactive ideation → proposal.json                 |
| Localizer     | `localizer.agent.md`     | Translation (EN ↔ JA)                                |
| Summarizer    | `summarizer.agent.md`    | Content summarization, slide count reduction         |
| JSON Reviewer | `json-reviewer.agent.md` | content.json quality assurance                       |
| PPTX Reviewer | `pptx-reviewer.agent.md` | Final PPTX quality assurance                         |

## References

Detailed documentation in `references/`:

- **SCRIPTS.md**: Complete script reference and usage examples
- **USE_CASES.md**: Detailed workflows for common scenarios
- **Agents**: `references/agents/*.agent.md` - Agent definitions
- **Instructions**: `references/instructions/*.instructions.md` - Workflow rules
- **Schemas**: `references/schemas/*.schema.json` - JSON schemas
- **AGENTS.md**: Architecture overview and design principles

## Common Use Cases

- **Tech Blog → PPTX**: Convert Zenn/Qiita articles to presentations (15-20 slides, ~5 min)
- **English → Japanese**: Translate presentations maintaining design (~15 min for 120 slides)
- **Report Generation**: Create business reports from notes + charts (~10 min)
- **Technical Training**: Convert API docs to training material with code examples (~8 min)
- **Architecture Diagrams**: Generate custom diagrams and merge into templates (~5 min)

See `references/USE_CASES.md` for detailed workflows and examples.

## Limitations

- **Language Support**: Primarily English ↔ Japanese (extendable)
- **Image Formats**: PNG, JPG, JPEG (no SVG/GIF animation)
- **Code Blocks**: Best with pptxgenjs method
- **Template Compatibility**: Works with standard PowerPoint templates (16:9 recommended)

## Troubleshooting

Common issues documented in repository's `docs/TROUBLESHOOTING.md`.

**Quick checks:**

```powershell
# Validate content.json
python scripts/validate_content.py output_manifest/xxx_content.json

# Diagnose template
python scripts/diagnose_template.py templates/xxx.pptx

# Check PPTX quality
python scripts/validate_pptx.py output_ppt/xxx.pptx
```

## License

This skill is licensed under CC BY-NC-SA 4.0. See LICENSE.txt for full terms.

---

**Note**: This skill orchestrates a complex multi-agent pipeline. For best results, follow the PLAN phase confirmation process and use the Orchestrator agent as the entry point.
