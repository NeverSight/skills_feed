---
name: md-translator
description: >
  This skill should be used when translating Docusaurus documentation files
  (Markdown, MDX, and i18n JSON) into other languages while preserving all
  syntax, structure, and formatting. Designed for the Agent Factory learn-app
  i18n workflow with state tracking via manifest.json to avoid duplicate work
  and resume interrupted translations. Use when the user says: "translate",
  "localize", "translate to Urdu/Spanish/French", "translation status",
  "what needs translating", "translate chapter", or "continue translating".
  Supports locales: en, fr, de, es, zh, ar, ur, hi.
---

# Markdown Translator for Docusaurus

Translate Docusaurus docs (MD/MDX and i18n JSON) to a target language while
preserving all syntax, structure, and Docusaurus-specific components.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Conversation** | Target locale, scope (file/chapter/all/JSON), resume vs fresh |
| **Manifest** | Read `apps/learn-app/translation-work/manifest.json` for current state |
| **Glossary** | Load `references/glossary-<locale>.md` for terminology |
| **Source files** | Read files to translate from `apps/learn-app/docs/` |
| **Rules** | Read `references/translation-rules.md` before first translation |

## Required Clarifications

1. **What locale?** (if not specified or inferrable from conversation)
2. **What scope?** Single file, chapter, all JSON files, or full locale

## Optional Clarifications

3. Resume from manifest or start fresh? (default: resume)
4. Specific files to prioritize? (default: by chapter order)

## Critical Rule: YOU Do the Translation

The extract/reassemble/validate scripts are helpers. **The actual translation
is YOUR job.** Read each segment's `original` field and write a real,
fluent, human-quality translation in the target language.

- Output MUST be actual text in the target script (Urdu = نستعلیق, Hindi = देवनागरी, Chinese = 中文)
- NEVER append language tags like `[UR]`, copy English unchanged, or write placeholders
- If you cannot translate well enough, STOP and tell the user
- Use the glossary for terminology consistency
- See `references/validation-guide.md` for correct vs wrong examples

## Prerequisites

```bash
pip install markdown-it-py
```

## Core Pipeline

Every MD/MDX file follows this pipeline:

```
Check Manifest → Extract (script) → Translate (YOU) → Reassemble (script) → Validate (script) → Update Manifest
```

### Step 1: Check Manifest

Read `apps/learn-app/translation-work/manifest.json`. Follow the decision tree
in `references/manifest-guide.md` to determine what work is needed.

### Step 2: Extract Segments

```bash
python scripts/translate_md.py extract <source.md> <segments.json> --lang <code>
```

Output to: `apps/learn-app/translation-work/<locale>/<name>_<locale>_segments.json`

`<name>` = source filename stem (e.g., `01-the-2025-inflection-point`).
See `references/docusaurus-i18n.md` for full naming conventions and path examples.

### Step 3: Translate Segments (YOUR JOB)

1. Read the segments JSON (`frontmatter_segments`, `body_segments`, and `admonition_segments`)
2. For EACH segment, translate `original` → `translated` in the target language
3. Preserve all inline Markdown formatting (see `references/translation-rules.md`)
4. Skip pure code, URLs, and numbers (copy as-is)
5. Translate `admonition_segments` titles (e.g., "Pro Tip" → target language)
6. Save to: `apps/learn-app/translation-work/<locale>/<name>_<locale>_translated.json`
7. **Run quality gate** from `references/validation-guide.md` before proceeding

### Step 4: Reassemble

```bash
python scripts/translate_md.py reassemble <source.md> <translated.json> <output.md>
```

Output to: `apps/learn-app/i18n/<locale>/docusaurus-plugin-content-docs/current/<path>/`

Create parent directories first: `mkdir -p <parent>`

### Step 5: Validate

```bash
python scripts/translate_md.py validate <source.md> <output.md>
```

### Step 6: Update Manifest

Update status and timestamps after each step. See `references/manifest-guide.md`.

## Workflow Modes

### Status Check (always start here)

Report current translation state for the requested locale from the manifest.

### Single File

Run the full pipeline (Steps 1-6) for one MD/MDX file.

### Chapter Batch

1. Discover path: `ls -d apps/learn-app/docs/*/<chapter-num>-*/`
2. List all `.md`/`.mdx` files in the chapter
3. Check manifest — skip files already completed with current MD5
4. Run the pipeline for each file needing work
5. Report: "Translated X new, skipped Y done, Z total"

### JSON Files

Translate the 4 Docusaurus i18n JSON files (`code.json`, `current.json`,
`navbar.json`, `footer.json`):

1. Read each source JSON
2. Translate `"message"` values (keep `"description"` in English)
3. Preserve all `{placeholder}` tokens and `|` pluralization separators
4. Urdu is NOT Arabic — use the correct language
5. Write to `apps/learn-app/i18n/<locale>/<path>`
6. Update manifest

### Resume / Continue

Read manifest, find incomplete files, resume from last completed step.

### New Content Sync

Scan `docs/` against manifest, mark new files as missing, changed files as
stale, then translate only what needs updating.

## Reference Files

| File | When to Read |
|------|-------------|
| `references/translation-rules.md` | Before first translation in a session |
| `references/docusaurus-i18n.md` | When unsure about output paths or folder structure |
| `references/manifest-guide.md` | When checking/updating translation state |
| `references/validation-guide.md` | Before marking any file as translated |
| `references/glossary-<locale>.md` | Before translating to that locale |
| `references/glossary-template.md` | When adding a new locale with no glossary |

## Error Recovery

| Problem | Action |
|---------|--------|
| Script fails on extract | Check file encoding, ensure markdown-it-py installed |
| Malformed JSON after translate | Validate JSON before saving, fix syntax errors |
| Validation fails | Read the specific failure, fix the translated output, re-validate |
| Wrong language in output | Mark `wrong_language` in manifest, re-translate |
| Source file changed | Mark `stale` in manifest, re-extract and re-translate |
| Cannot translate well | STOP, tell the user, suggest alternative approach |

## Output

- **Working files**: `apps/learn-app/translation-work/<locale>/`
- **Final MD**: `apps/learn-app/i18n/<locale>/docusaurus-plugin-content-docs/current/<path>/`
- **Final JSON**: `apps/learn-app/i18n/<locale>/<path>/`
- **Manifest**: Always update `apps/learn-app/translation-work/manifest.json`
