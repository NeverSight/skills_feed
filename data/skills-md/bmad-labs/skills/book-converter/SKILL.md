---
name: book-converter
description: Convert EPUB books to high-quality formatted Markdown using pandoc and AI-assisted formatting. Use when the user provides an EPUB file path and wants to convert it to professionally formatted Markdown, similar to the Clean Code Collection formatting. This skill handles the complete workflow from EPUB extraction through AI-driven content formatting, including fixing PDF conversion artifacts, joining split paragraphs, correcting code blocks, standardizing headers, and creating proper Table of Contents.
---

# Book Converter Skill

Convert EPUB books into professionally formatted Markdown books with AI-assisted quality improvements.

## Overview

This skill converts EPUB files into high-quality Markdown documents by:

1. Using pandoc to extract raw Markdown from EPUB
2. Creating a structured project directory
3. Planning and executing AI-driven formatting fixes
4. Producing chapter-by-chapter formatted output
5. Generating merged book file with Table of Contents

## Quick Start

User provides an EPUB file path:

```
/Users/username/Downloads/Book.Name.2024.epub
```

Execute the conversion workflow:

```bash
python3 scripts/convert_book.py "/path/to/book.epub"
```

This initiates the complete conversion process.

## Workflow

**CRITICAL: Use subagents for all formatting work to avoid polluting main context.**

### Phase 1: Setup and Extraction (Main Agent)

Run the conversion script:

```bash
python3 scripts/convert_book.py "/path/to/book.epub"
```

This script:
1. Verifies EPUB file exists
2. Creates project structure:
   - `books/book-name/` - Main directory
   - `books/book-name/raw/` - Pandoc output
   - `books/book-name/chapters/` - Formatted chapters
   - `books/book-name/images/` - Extracted images
3. Runs pandoc to extract Markdown
4. Copies formatting standards to project directory

**Output**: Raw Markdown in `books/book-name/raw/book-parsed.md`

### Phase 2: Analysis and Planning (Script + Subagent)

**Step 1**: Run the structure analysis script (Main Agent):

```bash
python3 books/book-name/analyze_structure.py books/book-name
```

This script:
- Extracts all headers with line numbers
- Detects formatting issues by sampling
- Suggests chapter boundaries
- Creates `STRUCTURE_ANALYSIS.md` report (~5-10 KB instead of 35k+ lines)

**Step 2**: Launch a **general** subagent to create mapping files:

```python
Task(
  subagent_type="general",
  description="Create chapter map and formatting plan",
  prompt="""Create CHAPTER_MAP.md and FORMATTING_PLAN.md:

1. Read books/book-name/STRUCTURE_ANALYSIS.md (concise report with headers and issues)
2. Read books/book-name/references/chapter-map-template.md for format
3. Read books/book-name/references/formatting-plan-template.md for format
4. Create books/book-name/CHAPTER_MAP.md:
   - Use suggested chapter boundaries from analysis
   - Verify line ranges make sense
   - Create proper slugged filenames
5. Create books/book-name/FORMATTING_PLAN.md:
   - Document issues found in analysis
   - Add severity and priority
   - Note book-specific patterns
6. Update books/book-name/progress.md to mark Phase 2 complete

Return: Summary of chapters found and major issues identified."""
)
```

**Output**: `CHAPTER_MAP.md`, `FORMATTING_PLAN.md`, and updated `progress.md`

### Phase 3: Chapter Formatting (Use Subagents)

For EACH chapter, launch a separate **general** subagent:

```python
# Example for Chapter 1
Task(
  subagent_type="general",
  description="Format Chapter 1",
  prompt="""Format Chapter 1 following the chapter formatting workflow.

**Critical Instructions:**
1. Read and follow ALL steps in books/book-name/references/chapter-workflow.md
2. Apply formatting rules from books/book-name/references/formatting-standards.md
3. Use books/book-name/CHAPTER_MAP.md to find line ranges for Chapter 1
4. Read books/book-name/FORMATTING_PLAN.md for known issues to watch for

**Workflow Summary (see chapter-workflow.md for complete details):**

Step 1: Read Standards and Chapter Map
- Read references/formatting-standards.md
- Read CHAPTER_MAP.md for your chapter's line ranges
- Read FORMATTING_PLAN.md for known issues

Step 2: Extract Chapter Content
- Extract Chapter 1 from raw/book-parsed.md using line ranges

Step 3: Identify Issues follow the standards
- Headers using bold instead of #
- Shattered code blocks
- Split paragraphs
- Missing code language identifiers
- Emphasis artifacts [word]
- Corrupted footnotes
- Missing image alt text
- Broken links

Step 4: Apply Formatting Fixes
- Follow the three-pass approach in chapter-workflow.md:
  * First pass: Structure (headers, code blocks)
  * Second pass: Content (paragraphs, emphasis)
  * Third pass: Details (footnotes, images, links)

Step 5: Create Output File
- Write to books/book-name/chapters/chapter-01-title.md
- Use structure from chapter-workflow.md

Step 6: Update Progress
- Update books/book-name/progress.md with completion status
- Document fixes applied

**Quality Checklist (from chapter-workflow.md):**
- [ ] All headers use proper # syntax
- [ ] All code blocks have language identifiers
- [ ] No shattered code blocks remain
- [ ] Text flows naturally without mid-sentence breaks
- [ ] All footnotes have [^N] format with definitions
- [ ] Images have descriptive alt text

Return: Confirmation with summary of fixes applied."""
)
```

**Important**: 
- Launch subagents in parallel batches (3-5 at a time) for efficiency
- Each subagent must read chapter-workflow.md and formatting-standards.md
- Follow the systematic workflow to ensure consistent quality

**Output**: Formatted chapters in `books/book-name/chapters/`

### Phase 4: Book Assembly (Main Agent)

The `merge_book.py` script is already copied to your project directory. Simply run it:

```bash
python3 books/book-name/merge_book.py books/book-name
```

The script will:
1. Read `CHAPTER_MAP.md` for chapter order
2. Load all formatted chapters from `chapters/`
3. Extract headers for Table of Contents
4. Fix image paths (relative to final location)
5. Combine all chapters in order
6. Generate comprehensive TOC
7. Output to `books/book-name-book.md`

**Output**: `books/book-name-book.md` with complete formatted book

**Note**: The merge script is reusable - no need to create it per book!

## Critical: Chapter Formatting Requirements

**Every subagent in Phase 3 MUST:**

1. **Read chapter-workflow.md first** - Contains the complete step-by-step process
2. **Read formatting-standards.md** - Contains all formatting rules (678 lines)
3. **Follow the workflow systematically** - Don't skip steps
4. **Use the three-pass approach**:
   - First pass: Fix structure (headers, code blocks)
   - Second pass: Fix content (paragraphs, emphasis)
   - Third pass: Fix details (footnotes, images, links)
5. **Complete the quality checklist** - Verify all items before finishing

**Why this matters:**
- Ensures consistent quality across all chapters
- Prevents common mistakes (skipped issues, inconsistent style)
- Proven process from Clean Code Collection (35k+ lines)
- Each chapter is only formatted once - must be thorough

**The workflow documents are your complete instructions - trust them!**

## Subagent Usage Principles

**Never process book content in main context.** Always use subagents to:

1. **Keep main context clean**: Book content is large and pollutes context
2. **Enable parallelization**: Format multiple chapters simultaneously
3. **Isolate formatting work**: Each chapter gets fresh context
4. **Avoid token limits**: Raw content can exceed context windows

**Subagent Selection**: Always use `subagent_type="general"` for all book processing tasks.

## Progress Tracking

Create and maintain `books/book-name/progress.md`:

```markdown
# Book Name - Conversion Progress

## Phase 1: Setup ✓
- [x] EPUB extracted
- [x] Project structure created

## Phase 2: Planning ✓
- [x] Chapter map created (15 chapters identified)
- [x] Formatting plan documented

## Phase 3: Chapter Formatting (5/15 complete)
- [x] Front Matter
- [x] Chapter 1: Introduction
- [x] Chapter 2: Getting Started
- [x] Chapter 3: Advanced Topics
- [x] Chapter 4: Best Practices
- [ ] Chapter 5: Performance
- [ ] ...

## Phase 4: Assembly
- [ ] Merge script created
- [ ] Final book generated
```

Update after each subagent completes.

## Quality Standards

All formatted output must meet these criteria:

- **Headers**: Use proper `#` syntax, not bold text
- **Code Blocks**: Include language identifiers, merge shattered blocks
- **Text Flow**: Join split sentences into natural paragraphs
- **Emphasis**: Use `*italic*` and `**bold**`, not `[brackets]`
- **Footnotes**: Standard `[^1]` format with definitions
- **Images**: Descriptive alt text, not generic filenames
- **Links**: Clean anchors, no PDF conversion artifacts

Complete standards reference: [references/formatting-standards.md](references/formatting-standards.md)

## Example Usage

**User Request:**
> "Convert this EPUB to Markdown: /Users/john/Downloads/Effective.Java.3rd.Edition.epub"

**Skill Execution:**

1. Run conversion script to extract content
2. Analyze structure and create chapter map
3. Format each chapter using AI subagents
4. Merge into final book with TOC
5. Provide user with `books/effective-java-final.md`

## Scripts

- **convert_book.py**: Main conversion script (Phase 1) - Extracts EPUB and sets up project
- **analyze_structure.py**: Structure analyzer (Phase 2) - Extracts headers and detects issues efficiently
- **merge_book.py**: Reusable merge script (Phase 4) - Combines all chapters into final book

## References

- **formatting-standards.md**: Complete formatting rules (loaded as needed during formatting)
- **chapter-workflow.md**: Detailed chapter formatting workflow (loaded as needed)
- **progress-template.md**: Template for progress tracking file
- **chapter-map-template.md**: Template for chapter mapping
- **formatting-plan-template.md**: Template for formatting issue documentation

## Notes

- **High Quality Focus**: Manual AI-driven formatting ensures prose flows naturally
- **No Automated Scripts**: Formatting requires human-like judgment for line joining
- **Preserve Content**: Never alter meaning or remove content
- **Code Accuracy**: Ensure code blocks are syntactically complete
