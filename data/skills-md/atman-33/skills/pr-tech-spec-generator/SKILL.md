---
name: pr-tech-spec-generator
description: Generate comprehensive technical specifications from GitHub Pull Requests. Use when users provide a GitHub PR URL and request documentation, technical specs, or change analysis. Analyzes PR commits and diffs using gh CLI and git commands to produce structured documentation covering folder structure, DB schema changes, API definitions, test changes, and dependency updates.
---

# PR Tech Spec Generator

Generate comprehensive technical specifications from GitHub Pull Requests.

## Overview

This skill analyzes GitHub PRs and generates structured technical documentation. It fetches PR information via `gh` CLI, analyzes git diffs from local repositories, and produces a detailed specification document covering all aspects of the changes.

## Quick Start

**Basic usage:**

```bash
python scripts/generate_spec.py <pr-url>
```

**With custom repository path:**

```bash
python scripts/generate_spec.py <pr-url> --repo-path /path/to/repo
```

**With custom output directory:**

```bash
python scripts/generate_spec.py <pr-url> --output-dir /path/to/output
```

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth login`)
- Local git repository (branches will be automatically fetched if not present)
- Python 3.6+

**Note**: The script automatically handles cases where:
- Remote branches don't exist locally (will attempt to fetch them)
- Only local branches exist (will use local references)
- Branches are specified as commit hashes

## Workflow

1. **Parse PR URL** - Extract owner, repo, and PR number
2. **Fetch PR info** - Use `gh pr view` to get PR metadata
3. **Resolve branch references** - Find branches (remote, local, or commit hash)
4. **Analyze git diff** - Use git commands to get detailed changes
5. **Detect patterns** - Identify DB, API, test, and dependency changes
6. **Generate document** - Create structured Markdown specification
7. **Save output** - Write to `outputs/` directory with timestamp

## Generated Specification Structure

The generated technical specification includes:

1. **Overview** - PR metadata (number, URL, date, branches, description)
2. **Change Summary** - Statistics (files changed, lines added/removed, commits)
3. **Folder Structure** - Tree view of changed files with status indicators
4. **Commit History** - Chronological table of all commits
5. **DB Schema Changes** - Detected migration and schema modifications
6. **API Definition** - Detected endpoint changes and affected API files
7. **Major Changes** - Key code modifications (functions, classes, exports)
8. **Tests** - Changed test files and coverage
9. **Dependencies** - Package/library version updates
10. **Generation Info** - Metadata about the generated document

## Detection Capabilities

The script automatically detects:

- **DB Changes**: Migrations, schema files (Prisma, TypeORM, SQL, etc.)
- **API Changes**: Route definitions across frameworks (NestJS, Express, FastAPI, Flask, Spring)
- **Test Changes**: Test files across frameworks (Jest, Mocha, pytest, RSpec, JUnit)
- **Dependencies**: Package managers (npm, pip, bundler, maven, gradle, cargo, go modules)
- **Code Changes**: Functions, classes, constants, exports

See [detection-patterns.md](references/detection-patterns.md) for detailed pattern information.

## Customization

To customize detection patterns or output format:

1. **Detection patterns**: Edit the pattern lists in `scripts/generate_spec.py`
2. **Output structure**: Modify the `generate_spec_document()` function
3. **Template**: Reference [spec-template.md](references/spec-template.md) for standard structure

## Example Usage

```bash
# Generate spec for a PR
python scripts/generate_spec.py https://github.com/owner/repo/pull/123

# Output: outputs/tech-spec-pr123-20260110-143052.md
```

## Limitations

- Detection patterns are regex-based and may have false positives
- Very large PRs may generate lengthy documents
- Language/framework-agnostic detection may miss project-specific patterns
- If both base and head branches don't exist in the repository, the script will attempt to fetch them automatically

## Resources

- **scripts/generate_spec.py** - Main specification generator
- **references/spec-template.md** - Document structure template
- **references/detection-patterns.md** - Detection pattern documentation

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
