---
name: diagram-reports-generator
description: This skill generates comprehensive diagram and MicroSim reports for the geometry course by analyzing chapter markdown files and creating table and detail reports. Use this skill when working with an intelligent textbook (specifically geometry-course) that needs updated visualization of all diagrams and MicroSims across chapters, including their status, difficulty, Bloom's Taxonomy levels, and UI complexity.
---

# Diagram Reports Generator

## Overview

This skill automatically generates comprehensive reports of all diagrams and MicroSims in the geometry course by analyzing chapter markdown files. It creates two report files: a table view for quick reference and a detailed view organized by chapter.

## When to Use This Skill

Use this skill when:

- Working with the geometry-course intelligent textbook project
- Needing to audit all diagrams and MicroSims across chapters
- Tracking implementation status of visual elements
- Analyzing complexity and Bloom's Taxonomy distribution
- Updating documentation after adding new diagrams or MicroSims
- Generating reports for instructors or content creators

## Workflow

### Step 1: Install the Diagram Report Generator Script

If the project does not already have the diagram report generator script, install it from the skill's bundled resources:

1. Check if `src/diagram-reports/diagram-report.py` exists in the project
2. If it doesn't exist:
   - Create the directory: `mkdir -p src/diagram-reports`
   - Copy the script from this skill's `scripts/diagram-report.py` to `src/diagram-reports/diagram-report.py`
3. If it already exists, verify it's up to date (optionally show the user a diff if there are differences)

Example installation:
```bash
# Create directory if needed
mkdir -p src/diagram-reports

# Copy script from skill (use Read tool to get script content, then Write tool to create file)
# The script is located in this skill's scripts/diagram-report.py
```

### Step 2: Verify Project Structure

Before running the report generator, verify the project structure:

1. Confirm the current working directory is the geometry-course root (or any intelligent textbook project)
2. Verify `docs/chapters/` contains chapter directories (format: `01-chapter-name`, `02-chapter-name`, etc.)
3. Ensure `docs/learning-graph/` directory exists for output

### Step 3: Run the Report Generator

Execute the Python script to generate the reports:

```bash
python src/diagram-reports/diagram-report.py
```

The script will:

- Scan all chapter directories in `docs/chapters/`
- Parse each chapter's `index.md` file
- Extract diagram and MicroSim specifications from `<details>` blocks with "#### Diagram:" headers
- Analyze each element for:
  - Type (diagram or MicroSim)
  - Status (implementation status if specified)
  - Bloom's Taxonomy levels
  - UI element count
  - Estimated difficulty (Easy, Medium, Hard, Very Hard)
  - Learning objectives

### Step 4: Verify Generated Reports

After running the script, verify two files were created in `docs/learning-graph/`:

1. **diagram-table.md** - A sortable table view with columns:
   - Chapter number
   - Element title (with links to chapter sections)
   - Status
   - Type (Diagram/MicroSim)
   - Bloom's Taxonomy levels
   - UI elements count
   - Difficulty rating

2. **diagram-details.md** - A detailed view organized by chapter with:
   - Chapter-level summaries
   - Full element descriptions
   - Learning objectives
   - Linked titles to source chapter sections

### Step 5: Review Navigation Configuration

The generated reports should already be linked in the MkDocs navigation. Verify the `mkdocs.yml` file contains these entries under the "Learning Graph" section:

```yaml
- Learning Graph:
    - Diagrams Table: learning-graph/diagram-table.md
    - Diagrams Details: learning-graph/diagram-details.md
```

If these entries are missing, add them to the navigation structure.

### Step 6: Preview the Reports

To view the generated reports:

1. Run `mkdocs serve` to start the local development server
2. Navigate to the "Learning Graph" section
3. Click on "Diagrams Table" or "Diagrams Details"
4. Verify all diagrams and MicroSims are properly listed with accurate information

## Understanding Report Output

### Difficulty Estimation

The script estimates difficulty based on:

- **Element Type**: MicroSims start with higher base difficulty
- **UI Complexity**: Number of sliders, buttons, dropdowns, and other controls
- **Features**: Animation, rotation, 3D/isometric views, real-time calculations
- **Canvas Size**: Larger canvases increase complexity

Difficulty levels:
- **Easy**: Static diagrams or simple visualizations
- **Medium**: Basic interactivity with 1-3 UI elements
- **Hard**: Moderate interactivity with 4-6 UI elements or complex features
- **Very Hard**: High interactivity with many UI elements or advanced features

### Bloom's Taxonomy Detection

The script automatically detects Bloom's Taxonomy levels mentioned in specifications:

- Remembering
- Understanding
- Applying
- Analyzing
- Evaluating
- Creating

## Troubleshooting

### No Elements Found

If the report shows zero elements:

- Verify chapter markdown files contain `#### Diagram:` headers followed by `<details>` blocks
- Check that `<details>` blocks include specification content
- Run with verbose flag: `python src/diagram-reports/diagram-report.py --verbose`

### Missing Information

If elements are missing type, status, or other fields:

- Review the `<details>` block format in chapter files
- Ensure specifications include `**Type:**`, `**Status:**`, and `**Learning Objective:**` fields
- The script will infer type from content if not explicitly specified

### Broken Links in Reports

If chapter links don't work:

- Verify chapter directory naming follows the pattern: `##-descriptive-name`
- Check that MkDocs anchor generation matches the script's anchor creation logic
- Test links by navigating in the served site

## Advanced Usage

### Custom Output Location

Specify a different output directory:

```bash
python src/diagram-reports/diagram-report.py --output-dir /path/to/output
```

### Generate CSV Format

For spreadsheet analysis:

```bash
python src/diagram-reports/diagram-report.py --format csv
```

### Generate HTML Format

For standalone HTML reports:

```bash
python src/diagram-reports/diagram-report.py --format html
```

### Verbose Output for Debugging

Enable detailed logging:

```bash
python src/diagram-reports/diagram-report.py --verbose
```

## Integration with Intelligent Textbook Workflow

This skill integrates with the broader intelligent textbook creation workflow:

1. **After content creation**: Run this skill after generating or updating chapter content
2. **Before review sessions**: Generate reports to identify gaps or inconsistencies
3. **During planning**: Use difficulty distribution to balance implementation effort
4. **For documentation**: Include reports in instructor guides or project documentation

## Bundled Resources

### scripts/diagram-report.py

This skill includes the complete Python script for generating diagram and MicroSim reports. The script will be installed into the user's project at `src/diagram-reports/diagram-report.py` when the skill is first used.

The script:
- Analyzes all chapter markdown files in `docs/chapters/`
- Extracts diagram and MicroSim specifications from `<details>` blocks
- Calculates difficulty estimates based on UI complexity and features
- Detects Bloom's Taxonomy levels from specification text
- Generates both table and detailed report formats
- Supports multiple output formats (markdown, CSV, HTML)
