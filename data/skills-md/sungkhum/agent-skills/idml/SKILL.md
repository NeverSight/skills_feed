---
name: idml
description: "Comprehensive Adobe InDesign IDML creation, editing, and analysis. Use when working with .idml files to unpack, inspect, modify stories or spreads, preserve layout structure, validate packages, or generate IDML from InDesign exports."
metadata:
  tags: "idml,indesign,xml,zip,layout,translation,localization"
---

# IDML creation, editing, and analysis

## Overview

An IDML file is a ZIP package containing XML component files (stories, spreads, resources) and a root `designmap.xml`. Use component-level edits for minimal, safe changes; use full-package workflows for repacking and validation.

**Where scripts live**
- All helper scripts are in `scripts/`. If a model says “no python scripts,” have it list the directory to confirm:
  - `ls scripts`
  - `ls skills/idml/scripts` (if running from repo root)

**Reference files:**
- IDML package structure: `references/idml-structure.md`
- IDML XML overview: `references/idml-xml.md`
- IDML document library: `references/idml-document.md`
- IDML translation workflow: `references/idml-translation.md`
- Track changes guidance: `references/idml-track-changes.md`
- Schemas and validation: `references/idml-schemas.md`
- Tooling: `references/tools.md`

## Example prompts
- "Extract all story text from this IDML and prepare it for translation."
- "Apply translated text back into Stories/*.xml without changing layout."
- "Map stories to spreads and pages for review."
- "Validate this IDML package and run a roundtrip smoke test."
- "Generate an observed schema and report unknown elements."

## Workflow decision tree

### Reading/analyzing content
- Unpack and inspect `designmap.xml`, story files, and spreads.
- Use the XML reference to understand component boundaries.

### Creating a new document
- Preferred: create in InDesign and export to IDML.
- If generating from scratch, follow the IDML specification and component schemas.

### Editing an existing document
- **Text-only edits**: edit `Stories/*.xml`.
- **Layout edits**: edit `Spreads/*.xml` or `MasterSpreads/*.xml`.
- **Styles/resources**: edit `Resources/*.xml` and keep references consistent.

## Reading and analyzing content

### Unpacking
```bash
python scripts/unpack_idml.py file.idml unpacked
```

### Key files
See `references/idml-structure.md` for the required files and folders.

## Editing workflows

### Library-based edits (recommended)
Use `scripts/idml_document.py` for component discovery and XML edits. See `references/idml-document.md` for usage.

### Raw XML edits (advanced)
1. **MANDATORY - READ ENTIRE FILE**: Read `references/idml-xml.md` before editing XML directly.
2. Unpack the file: `python scripts/unpack_idml.py file.idml unpacked`
3. Edit the specific component XML (stories/spreads/resources).
4. Repack: `python scripts/pack_idml.py unpacked out.idml`
5. Validate: `python scripts/validate_idml.py unpacked --original out.idml`

## Translation workflow

Use `references/idml-translation.md` to extract, translate, and reapply story text.

## Track changes
Disable Track Changes before exporting IDML from InDesign. See `references/idml-track-changes.md`.

## Validation and smoke tests
- Package validation: `python scripts/validate_idml.py <unpacked_dir> --original <file.idml>`
- Full roundtrip smoke test: `python scripts/smoke_test.py <file.idml> <work_dir>`
- Translation extract: `python scripts/extract_story_text.py <unpacked_dir> translations.jsonl`
- Prepare translation JSONL: `python scripts/prepare_translation_jsonl.py translations.jsonl translations_for_translation.jsonl`
- Translation apply: `python scripts/apply_story_text.py <unpacked_dir> translations.jsonl`
- Story count report: `python scripts/compare_story_counts.py english.jsonl khmer.jsonl --out story_counts.json`
- Alignment file: `python scripts/align_story_text.py english.jsonl khmer.jsonl --out alignment.jsonl`
- Story/spread map: `python scripts/map_story_spreads.py <unpacked_dir> --out story_spreads.json`
- Resource report: `python scripts/check_resources.py <unpacked_dir> --out resources_report.json`
- Content-only validation: `python scripts/validate_content_only_changes.py <original_unpacked> <modified_unpacked>`
- Observed schema report: `python scripts/observe_idml_schema.py <idml_or_unpacked> --out idml_observed_schema.json`
- Observed schema validation: `python scripts/validate_observed_schema.py <schema.json> <idml_or_unpacked> --out idml_schema_report.json`
- Observed schema coverage: `python scripts/observed_schema_report.py <schema.json> --out idml_schema_coverage.json`
- Observed schema delta: `python scripts/schema_delta_report.py <base_schema.json> <new_schema.json> --out idml_schema_delta.json`
- Coverage checklist: `python scripts/coverage_checklist.py <schema_delta.json> --out idml_schema_checklist.md`
- Combined coverage plan: `python scripts/coverage_plan.py Label=delta.json ... --out idml_schema_plan.md`

## Code style guidelines
- Write concise code.
- Avoid verbose variable names and redundant operations.
- Avoid unnecessary print statements.

## Dependencies
**Required**
- **defusedxml**: `pip install defusedxml` (safe XML parsing)

**Optional**
- **InDesign**: export IDML from source documents
- **jing**: Relax NG validator for strict schema checks
