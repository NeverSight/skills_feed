---
name: microsim-standardization
description: This skill standardizes MicroSim directories by validating structure, metadata, documentation, and required components against a comprehensive quality checklist. Use this when auditing or upgrading a MicroSim to ensure it meets all documentation and structural standards, including index.md formatting, metadata.json validation, iframe embeds, and p5.js editor links.
---

# MicroSim Standardization

## Overview

This skill validates and standardizes MicroSim directories to ensure they meet quality and documentation standards. MicroSims are interactive educational simulations that may use various JavaScript libraries (p5.js, vis-network, Chart.js, etc.). This skill performs a comprehensive audit of a MicroSim directory, generates a TODO list of required upgrades, and optionally implements the standardization changes.  After this process runs, a quality_score will be added to the index.md metadata.
A rubric of how the quality score is provided and this score should be shown to the user before and after the changes.

## Note on Terminology

There are two types of metadata for a MicroSim.
1. **yml header metadata:** - this metadata is inserted into the top of the index.md file.  This is to support the social image previews.  The mkdocs social_preview extension uses these fields.  The quality_score is also stored here.
2. **:Dublin core metadata** - These metadata elements are ONLY stored in the `metadata.json` file.

Do not mix these up!  Never put Dublin Core metadata into the yml headers.

## Workflow

### Step 1: Receive MicroSim Directory Path

Receive the path to the MicroSim directory from the user. The directory should be located at:
- `docs/sims/[microsim-name]/`

Note that the `microsim-name` must be a string with only lowercase letters and dashes (kebab-case)

#### 2: Check for an Existing Quality Score

Check of a quality_score of 85 or above exists in the yml metadata of the index.md file like this:

```yml
---
quality_score: 86
---
```

If the score is 85 or above, suggest to the user to skip the rest of the steps.  Tell them that perhaps their tokens can be better used to create new MicroSims.

If the score is missing or lower than 85, proceed with the next steps.

Confirm the directory exists and contains at minimum a `main.html` file (the core simulation file).

### Step 3: Run Standardization Checklist

Run through the complete standardization checklist, documenting which items pass and which need work. Use the TodoWrite tool to create a comprehensive TODO list of all items that need to be addressed.  Store the TODO list in TODO.txt in the
MicroSim directory.

**Standardization Checklist:**

#### 1. Index.md File Existence
- Check if `index.md` file exists in the MicroSim directory
- If missing: Add TODO to create `index.md` file

#### 2. YAML metadata at the top of the index.md
- Verify `index.md` begins with YAML frontmatter (between `---` delimiters)
- Required YAML fields:
  - `title:` - MicroSim title
  - `description:` - Brief description for SEO and social previews
  - `quality_score:` - Integer 1-100 indicating completeness/quality
  - `image:` and `og:image` - Social media preview image path (optional but recommended)
- If missing or incomplete: Add TODO to add/fix YAML frontmatter

#### 3. Level 1 Header After Frontmatter
- Verify a level 1 header (`# Title`) appears immediately after YAML metadata
- The title should match or complement the YAML `title` field
- If missing: Add TODO to add level 1 header

#### 4. Iframe Embed After Title
- Check for iframe element after the level 1 title
- Iframe must reference `main.html`
- Standard format:
  ```html
  <iframe src="main.html" width="100%" height="600px"></iframe>
  ```
- If missing or incorrect: Add TODO to add/fix iframe embed

Note: Do not add the frameborder attribute to the iframe.  The site-wide CSS is responsible for styling all iframes with the site.

#### 5. Copy-Paste Iframe Example
- Check for a second iframe in an HTML code block with label "Copy this iframe to your website:"
- This allows users to embed the MicroSim in their own sites
- Standard format:
  ````markdown
  ```html
  <iframe src="https://your-domain.github.io/path/to/sims/microsim-name/main.html" width="100%" height="600px"></iframe>
  ```
  ````
- If missing: Add TODO to add copy-paste iframe example

#### 6. Metadata.json File Existence
- Check if `metadata.json` file exists in the MicroSim directory
- If missing: Add TODO to create `metadata.json` with Dublin Core metadata

#### 7. Metadata.json Schema Validation
- Validate `metadata.json` against the Dublin Core schema in `assets/metadata-schema.json`
- Required Dublin Core fields:
  - `title` - MicroSim name
  - `description` - Purpose and functionality
  - `creator` - Author name or organization
  - `date` - Creation date (ISO 8601: YYYY-MM-DD)
  - `subject` - Keywords or topics (string or array)
  - `type` - Resource type (e.g., "Interactive Simulation")
  - `format` - File format (e.g., "text/html")
  - `language` - Language code (e.g., "en" or "en-US")
  - `rights` - License information (e.g., "CC BY 4.0", "MIT License")
- If validation fails: Add TODO to fix metadata.json structure and content

#### 8. Fullscreen Link Button
- Check for fullscreen link button after the iframe example
- Standard format:
  ```markdown
  [Run MicroSim in Fullscreen](main.html){ .md-button .md-button--primary }
  ```
- If missing: Add TODO to add fullscreen link button

#### 9. P5.js Editor Link (P5.js MicroSims Only)
- Determine if the MicroSim uses p5.js by checking:
  - Import statements in `main.html` for p5.js CDN
  - Use of p5.js functions like `setup()`, `draw()`, `createCanvas()`
- If p5.js is used, check for p5.js editor link:
  ```markdown
  [Edit in the p5.js Editor](https://editor.p5js.org/username/sketches/SKETCH_ID)
  ```
- If link is missing or placeholder: Add TODO to prompt user for p5.js sketch path
- If not a p5.js MicroSim: Skip this check

#### 10. Description Section (Level 2 Header)
- Check for a level 2 header section (e.g., `## Description`, `## How to Use`, `## About This MicroSim`) after the frontmatter elements
- This section should describe the MicroSim's purpose, how to use it, and what concepts it demonstrates
- If missing: Add TODO to add description section

#### 11. Lesson Plan Section
- Check if a `## Lesson Plan` level 2 header exists
- This section should include:
  - Learning objectives
  - Target audience
  - Prerequisites
  - Activities or exercises
  - Assessment suggestions
- If missing: Add TODO to ask user whether to create a lesson plan section

#### 12. References Section
- Check if a `## References` level 2 header exists at the end of the document
- This section should include:
  - Links to relevant academic papers or articles
  - Links should be in the format `1. [Link Title](URL) - publication_date - publication_name - description and relevency`
  - Documentation for libraries used
  - Related educational resources
- If missing and appropriate for the content: Add TODO to add references section

### Step 4: Present TODO List to User

Present the comprehensive TODO list to the user, organized by priority:
1. Critical structural issues (missing index.md, invalid metadata.json)
2. Required documentation elements (frontmatter, headers, iframes)
3. Enhanced documentation (lesson plans, references)

Ask the user: **"Should I proceed with implementing these standardization changes? (y/n)"**

### Step 5: Implement Changes (If Approved)

If the user responds "y" or "yes":

1. Work through the TODO list systematically
2. Update the TodoWrite status as each item is completed
3. For items requiring user input (e.g., p5.js sketch URL, lesson plan content details), use AskUserQuestion to gather necessary information
4. Validate all changes as they're made
5. Re-run metadata.json validation after modifications

**Implementation Guidelines:**

- **Preserve existing content**: Never remove or overwrite user content without explicit confirmation
- **Maintain formatting consistency**: Use the same markdown style as existing content
- **Add blank lines before lists**: MkDocs requires blank lines before markdown lists
- **Use Title Case for headers**: Follow MkDocs Material theme conventions
- **Validate JSON syntax**: Ensure metadata.json is valid JSON before saving
- **Test iframe paths**: Verify `main.html` path is correct relative to `index.md`

### Step 6: Final Validation and Quality Report

After completing all changes:

1. Run final validation on metadata.json using the schema
2. Check that all TODO items are marked completed
3. Provide a summary report to the user:
   - Number of issues found and fixed
   - Any items that require follow-up
   - Suggested quality_score for the YAML frontmatter (based on completeness)

|Test Name|Description|Points|
|---------|-----------|------|
|Title|index.md file has a title in markdown level|2|
|main.html|The file main.html is present|10|
|Metadata 1|index.md has title and description metadata in yml|3|
|Metadata 2|index.md has image references for social preview|5|
|metadata.json present|A metadata.json file is present|10|
|metadata.json is valid|The microsim JSON schema had passed validation with no errors|20|
|iframe|A iframe that uses src="main.html" is present|10|
|Fullscreen Link Button|check if a button to view the MicroSim in fullscreen is present|5|
|iframe example|A iframe example in a HTML source block is present|5|
|image|An image of the microsim is present in the MicroSim directory and referenced by the header metadata|5|
|Overview Documentation|A description of the MicroSim and how to use it is present|5|
|Lesson Plan|A detailed lesson plan is present|10|
|References|A list of references in markdown format|5|
|MicroSim Type Specific Format|Varies on the type.  Example is a link to the p5.js editor.|5|

After the score is calculated, it must be written to the index.md metadata `quality_score` field

## Resources

### assets/metadata-schema.json

JSON Schema for validating MicroSim metadata.json files against Dublin Core standards. This schema defines:
- Required fields (9 core Dublin Core elements)
- Optional fields (extended metadata for educational resources)
- Field types and validation patterns
- Educational extensions (Bloom's levels, concepts, prerequisites)

Use this schema to validate metadata.json files programmatically or to guide manual validation.

### assets/index-template.md

Complete template showing the standard structure for a MicroSim index.md file, including:

- YAML frontmatter with all required fields
- Level 1 header
- Iframe embeds (both display and copy-paste versions)
- Fullscreen link button
- Description section with usage instructions
- Lesson Plan section with learning objectives, activities, and assessment
- References section

Use this template when creating new index.md files or when a MicroSim is missing critical documentation sections.

### assets/metadata-template.json

Complete template showing all Dublin Core metadata fields with example values, including:
- All 9 required core fields
- Optional contributor and identifier fields
- Educational extensions (Bloom's levels, concepts, prerequisites, library)

Use this template when creating new metadata.json files or when existing metadata is incomplete.

## Notes

- **Quality Score Guidance**: Assign quality scores based on completeness:
  - 90-100: All checklist items present, excellent documentation, lesson plan included
  - 70-89: Most items present, good documentation, may lack lesson plan
  - 50-69: Core items present, minimal documentation
  - Below 50: Missing critical components

- **Library Detection**: Detect JavaScript libraries by checking for:
  - p5.js: `p5.js` or `p5.min.js` in script tags
  - vis-network: `vis-network` in script tags or imports
  - Chart.js: `chart.js` or `Chart.min.js` in script tags
  - D3.js: `d3.js` or `d3.min.js` in script tags

- **Metadata Best Practices**:
  - Use ISO 8601 dates (YYYY-MM-DD)
  - Include multiple subject keywords for discoverability
  - Specify clear educational levels and prerequisites
  - List all contributors, not just the primary creator
  - Include version numbers for tracking iterations
