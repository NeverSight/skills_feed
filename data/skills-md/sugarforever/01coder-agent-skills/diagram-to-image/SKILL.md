---
name: diagram-to-image
description: Convert Mermaid diagrams and Markdown tables to images (PNG/SVG) for platforms that don't support rich formatting. Use when user asks to "convert to image", "export as PNG", "make this an image", or has content for X/Twitter that needs visual exports.
---

# Diagram to Image

Convert Mermaid diagrams and Markdown tables to images (PNG/SVG) for use in platforms that don't support rich formatting, like X (Twitter).

## When to Use

Use this skill when:
- User has a Mermaid diagram that needs to be converted to an image
- User has a Markdown table that needs to be converted to an image
- User is writing content for X/Twitter and needs visual exports
- User asks to "convert to image", "export as PNG", "make this an image", or similar

## Prerequisites

Ensure dependencies are installed:

```bash
# Check if mermaid-cli is installed
which mmdc || npm install -g @mermaid-js/mermaid-cli
```

## Smart Output Location

**IMPORTANT:** Determine the best output location based on context. Follow this decision tree:

### 1. User Specifies Path
If user explicitly mentions a path or filename, use that.

### 2. Project Context Detection
Check for common image/asset directories in the current project:

```bash
# Check for existing image directories (in order of preference)
ls -d ./images ./assets ./img ./static ./public/images ./assets/images 2>/dev/null | head -1
```

Use the first existing directory found. Common patterns:
- `./images/` - General projects
- `./assets/` - Web projects
- `./assets/images/` - Structured web projects
- `./public/images/` - Next.js, React projects
- `./static/` - Hugo, other static site generators
- `./img/` - Short form convention

### 3. Article/Document Context
If user is writing an article or document:
- Look for the document's directory
- Create `images/` subdirectory if appropriate
- Name the image based on the document name + descriptor

### 4. Conversation Context
Analyze the conversation to determine:
- **What the diagram represents** → Use for filename (e.g., `auth-flow.png`, `user-journey.png`)
- **Related file being discussed** → Place image near that file
- **Topic being discussed** → Use for naming

### 5. Default Fallback
If no context clues:
- Use current working directory
- Generate descriptive filename from diagram content

## Filename Generation

Create meaningful filenames based on content analysis:

| Content Pattern | Example Filename |
|----------------|------------------|
| `flowchart` with auth/login | `auth-flow.png` |
| `sequenceDiagram` with API | `api-sequence.png` |
| `erDiagram` | `entity-relationship.png` |
| `pie` chart about X | `x-distribution.png` |
| `gantt` chart | `project-timeline.png` |
| Table with comparison | `comparison-table.png` |
| Table with data | `data-table.png` |

**Rules:**
- Use kebab-case (lowercase with hyphens)
- Keep names concise but descriptive (2-4 words)
- Avoid generic names like `diagram.png` or `image.png`
- Include topic/subject when identifiable

## Conversion Process

### Step 1: Analyze Context

Before converting, gather context:
1. Check current working directory
2. Look for existing image directories
3. Analyze diagram/table content for naming
4. Consider any files or topics mentioned in conversation

### Step 2: Determine Output Path

```bash
# Example logic (implement mentally, not as literal script)
if user_specified_path:
    output_path = user_specified_path
elif exists("./images"):
    output_path = "./images/{generated_name}.png"
elif exists("./assets"):
    output_path = "./assets/{generated_name}.png"
elif exists("./public/images"):
    output_path = "./public/images/{generated_name}.png"
else:
    output_path = "./{generated_name}.png"
```

### Step 3: Create Temporary Input File

```bash
# For Mermaid
cat > /tmp/diagram.mmd << 'DIAGRAM_EOF'
<mermaid content>
DIAGRAM_EOF

# For Markdown table
cat > /tmp/table.md << 'TABLE_EOF'
<table content>
TABLE_EOF
```

### Step 4: Convert

**Mermaid to PNG:**
```bash
mmdc -i /tmp/diagram.mmd -o <output_path>.png -b white -s 2
```

**Mermaid to SVG:**
```bash
mmdc -i /tmp/diagram.mmd -o <output_path>.svg -b transparent
```

**Table to PNG:**
```bash
python3 ~/.claude/skills/diagram-to-image/scripts/table_to_image.py /tmp/table.md <output_path>.png
```

### Step 5: Report Result

After conversion, tell the user:
1. **Full path** where image was saved
2. **Why** that location was chosen (briefly)
3. **Image dimensions** or file size
4. Suggest they can specify a different location if needed

## Examples

### Example 1: Project with images/ directory

**Context:** User is in a project that has `./images/` directory, discussing authentication.

**User:** "Convert this to an image"
```
flowchart TD
    A[Login] --> B{Valid?}
    B -->|Yes| C[Dashboard]
    B -->|No| D[Error]
```

**Action:**
1. Detect `./images/` exists
2. Analyze content → authentication flow
3. Generate filename: `login-flow.png`
4. Output: `./images/login-flow.png`

---

### Example 2: Writing X article about AI

**Context:** User mentioned writing an article about AI agents for X.

**User:** "Make this a PNG"
```
flowchart LR
    User --> Agent --> Tools --> Response
```

**Action:**
1. No standard image directory found
2. Context: AI agents article for X
3. Generate filename: `ai-agent-flow.png`
4. Output: `./ai-agent-flow.png`

---

### Example 3: Data comparison table

**User:** "Export this table as image"
```
| Model | Speed | Accuracy |
|-------|-------|----------|
| GPT-4 | Slow | High |
| Claude | Fast | High |
```

**Action:**
1. Check for image directories
2. Analyze content → model comparison
3. Generate filename: `model-comparison.png`
4. Output to appropriate location

---

### Example 4: User specifies location

**User:** "Save this diagram to ~/Desktop/my-chart.png"

**Action:** Use exactly `~/Desktop/my-chart.png` as specified.

## Error Handling

- If output directory doesn't exist, create it (with user confirmation for new directories)
- If file already exists, append number: `auth-flow-2.png`
- If mmdc not installed: `npm install -g @mermaid-js/mermaid-cli`
- If Pillow not installed: `pip install pillow`
