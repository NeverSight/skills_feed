---
name: slides-generator
description: Create Hummingbot-branded PDF slides from markdown with Mermaid diagram support. Use for presentations, decks, and technical documentation with professional diagrams.
metadata:
  author: hummingbot
---

# slides-generator

Create Hummingbot-branded presentation slides in PDF format from markdown content. Features two-column layouts and Mermaid diagram rendering for technical architecture and flowcharts.

## Workflow

### Step 1: Get Markdown Content

Ask the user to provide a markdown file or paste markdown content. The content should follow this format:

```markdown
# Presentation Title

## 1. First Slide Title

Content for the first slide. Can include:
- Bullet points
- **Bold text** and *italic text*
- Code blocks

## 2. Second Slide Title

More content here.

## 3. Third Slide Title

And so on...
```

**Format Rules:**
- `# Title` = Presentation title (optional, becomes title slide)
- `## N. Slide Title` = New slide (N is slide number)
- Content under each `##` heading becomes slide content
- Supports markdown formatting: lists, bold, italic, code blocks, links

### Step 2: Parse and Confirm

Before generating the PDF, parse the markdown and show the user a summary:

```
📊 Slide Outline:

1. First Slide Title
2. Second Slide Title
3. Third Slide Title
...

Total: X slides

Please confirm to proceed with PDF generation, or provide edits.
```

Wait for user confirmation before proceeding.

### Step 3: Generate PDF

Run the generation script:

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/slides-generator/scripts/generate_slides.sh) \
  --input "<markdown_file_or_content>" \
  --output "<output_pdf_path>"
```

Or if the user provided inline content, save it to a temp file first:

```bash
# Save content to temp file
cat > /tmp/slides_content.md << 'SLIDES_EOF'
<markdown_content_here>
SLIDES_EOF

# Generate PDF
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/slides-generator/scripts/generate_slides.sh) \
  --input /tmp/slides_content.md \
  --output ~/slides_output.pdf
```

### Step 4: Deliver Result

After generation, tell the user:
- The PDF file location
- How many slides were generated
- Offer to open/view the PDF if desired

## Editing Existing Slides

If the user wants to edit slides from a previously generated PDF:

1. **Read the original markdown** (if available) or **view the PDF** to understand current content
2. Ask the user what changes they want:
   - Edit specific slide content
   - Add new slides
   - Remove slides
   - Reorder slides
3. Apply changes to the markdown
4. Regenerate the PDF

Use the `--edit` flag to update specific slides without regenerating all:

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/slides-generator/scripts/generate_slides.sh) \
  --input "<updated_markdown>" \
  --output "<same_pdf_path>" \
  --edit
```

## Diagrams

Users can describe diagrams in natural language using `mermaid:` syntax. **You must translate these descriptions to Mermaid code** before generating the PDF.

### User Input Format

Users write descriptions like:
```markdown
mermaid: A flowchart showing User Interface connecting to Condor and MCP Agents,
both connecting to Hummingbot API (highlighted), then to Client, then to Gateway
```

### Translation to Mermaid

Convert the description to proper Mermaid syntax:
```markdown
\`\`\`mermaid
flowchart TB
    A[User Interface] --> B[Condor]
    A --> C[MCP Agents]
    B --> D[Hummingbot API]
    C --> D
    D --> E[Hummingbot Client]
    E --> F[Gateway]
    style D fill:#00D084,color:#fff
\`\`\`
```

### Diagram Types

- `flowchart TD` - Top-down flowchart
- `flowchart LR` - Left-right flowchart
- `sequenceDiagram` - API and interaction flows
- `classDiagram` - Object-oriented design
- `erDiagram` - Database schemas

### Highlighting

Use `style NodeName fill:#00D084,color:#fff` for Hummingbot green highlighting.

### Requirements

Mermaid diagrams require the Mermaid CLI:
```bash
npm install -g @mermaid-js/mermaid-cli
```

## Code Blocks

Use regular `\`\`\`` code blocks for ASCII art, code snippets, or preformatted text:

```markdown
\`\`\`
Price
  ^
  |  [BUY] --- Level 3
  |  [BUY] --- Level 2
  |  [BUY] --- Level 1
  +-------------------> Time
\`\`\`
```

Code blocks render with monospace font on a gray background.

## Two-Column Layout

When a slide has both bullet points AND a diagram, it automatically renders in two columns:
- Left column: Text content
- Right column: Diagram

```markdown
## 4. How It Works

Key features:
- Automated order placement
- Dynamic position management
- Risk-controlled execution
- Real-time monitoring

mermaid: flowchart showing Market Data to Strategy to Orders
```

After translation:
```markdown
## 4. How It Works

Key features:
- Automated order placement
- Dynamic position management
- Risk-controlled execution
- Real-time monitoring

\`\`\`mermaid
flowchart TD
    A[Market Data] --> B[Strategy]
    B --> C[Orders]
    style B fill:#00D084,color:#fff
\`\`\`
```

## Example Markdown

```markdown
# Q4 Product Update

## 1. Overview

Today we'll cover:
- Product milestones
- Key metrics
- Roadmap preview

## 2. Architecture

Our system components:
- User-facing interfaces
- Core API layer
- Exchange connectivity

mermaid: flowchart showing UI to API (highlighted) to Gateway

## 3. Key Metrics

| Metric | Q3 | Q4 | Change |
|--------|----|----|--------|
| Users | 10K | 15K | +50% |
| Revenue | $100K | $150K | +50% |

## 4. Q1 Roadmap

1. Mobile app launch
2. Enterprise tier
3. International expansion

## 5. Questions?

Thank you!

Contact: team@example.com
```

After translating `mermaid:` descriptions:

```markdown
## 2. Architecture

Our system components:
- User-facing interfaces
- Core API layer
- Exchange connectivity

\`\`\`mermaid
flowchart TD
    A[UI] --> B[API]
    B --> C[Gateway]
    style B fill:#00D084,color:#fff
\`\`\`
```

## Dependencies

The script will check for and install if needed:
- Python 3
- `fpdf2` Python package (for PDF generation)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python 3: `brew install python3` (macOS) or `apt install python3` (Linux) |
| "fpdf2 not installed" | Run: `pip3 install fpdf2` |
| "Permission denied" | Check write permissions for output directory |
| "Empty PDF" | Verify markdown format follows the `## N. Title` pattern |

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_slides.sh` | Main PDF generation script |
