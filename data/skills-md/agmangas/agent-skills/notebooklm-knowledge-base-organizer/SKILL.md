---
name: notebooklm-knowledge-base-organizer
description: >
  Use when preparing files for NotebookLM, organizing documents into a
  knowledge base, converting formats for NotebookLM compatibility, or
  reducing a large document collection to fit NotebookLM's 50-source limit.
  Scores and prioritizes sources, performs strategic merging (time-series,
  topic-based, format consolidation), converts unsupported formats
  (PPTX to PDF, XLSX to CSV), applies flat structure with descriptive
  snake_case names, and optimizes for RAG retrieval performance.
---

# NotebookLM Knowledge Base Organizer

Prepares files for optimal use in NotebookLM by intelligently selecting and
consolidating sources, converting formats, organizing structure, and ensuring
compatibility. The primary constraint is NotebookLM's 50-source limit per
notebook. When collections exceed this limit, systematic scoring,
prioritization, and strategic merging reduce source count without losing
valuable information.

## When to Use This Skill

- You have 50+ files and need to optimize for NotebookLM's limit
- Preparing documents for a new NotebookLM notebook
- Converting a messy folder into NotebookLM-ready sources
- Files are in unsupported formats (PPTX, XLSX, complex PDFs)
- Documents exceed 500k words or 200MB per file
- Building a knowledge base for research, projects, or learning
- Large document collections (100-300 files) need intelligent prioritization

## What This Skill Does

1. **Scores and Prioritizes Sources** (when >50 detected) using Relevance, Recency, Uniqueness, and Information Density (0-40 scale)
2. **Strategic Merging** via time-series (daily to monthly), topic-based (related papers to comprehensive guides), and format consolidation (slides + transcript to unified PDF)
3. **Converts to Supported Formats** (PPTX to PDF, XLSX to CSV, scanned to OCR)
4. **Applies Flat Structure** with descriptive snake_case naming
5. **Removes Duplicates** across formats
6. **Splits Large Files** exceeding 500k words into parts
7. **Optimizes for RAG** with smaller, focused documents for better retrieval

## NotebookLM Supported Formats

**Supported:**
- PDF (text-selectable, not scanned images)
- Google Docs, Sheets (<100k tokens), Slides (<100 slides)
- Microsoft Word (.docx)
- Text files (.txt, .md)
- Images (PNG, JPEG, TIFF, WEBP)
- Audio (MP3, WAV, AAC, OGG with clear speech)
- URLs (websites, YouTube, Google Drive links)
- Copy-pasted text

**Convert These:**
- PPTX to PDF
- XLSX to CSV or Google Sheets
- Scanned PDFs to OCR text-selectable PDF
- Large Sheets to CSV (<100k tokens)

## File Limits

**Per Source:**
- 500,000 words max
- 200MB file size max
- No page limit (word limit matters)

**Per Notebook (Free):**
- 50 sources maximum -- HARD LIMIT
- 100 notebooks total

Prefer many smaller, focused documents over few large ones for better RAG retrieval. The 50-source limit is the primary optimization constraint.

IMPORTANT: Preserve original file timestamps during all operations. Timestamps
are essential for understanding latest additions, recent meeting minutes, and
key decisions. Use `touch -r original converted` after conversions. Include
dates in ISO format (YYYY-MM-DD) in all filenames.

## How to Use

```
Prepare these files for NotebookLM - convert formats and organize with descriptive names
```

```
Convert all PPTX and XLSX files to NotebookLM-compatible formats
```

```
Check if any files exceed NotebookLM's 500k word or 200MB limits
```

```
Organize this research folder for a NotebookLM knowledge base
```

```
Find duplicate content across different file formats
```

```
Split this large PDF into NotebookLM-compatible chunks
```

## Instructions

When a user requests NotebookLM organization, follow these steps.

### Step 1: Assess and Prioritize Sources

Count and evaluate before proceeding with any organization.

```bash
total_sources=$(find . -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.txt" -o -name "*.md" -o -name "*.csv" \) | wc -l)
echo "Total sources found: $total_sources"
```

If total exceeds 50:

1. **Score all sources** using the 4-dimension rubric (Relevance, Recency, Uniqueness, Density, each 0-10). See `references/scoring-system.md` for the full rubric, assessment commands, and batch scoring script.

2. **Rank and select top candidates** using the decision matrix. Target 35-40 auto-keep sources initially. See `references/prioritization-strategy.md` for the selection process and space-based adjustments.

3. **Identify merge candidates** -- find time-series patterns, topic clusters, and multi-format duplicates:
   ```bash
   # Time-series opportunities
   find . -name "*_20[0-9][0-9]_[0-9][0-9]_*" | \
     sed 's/_20[0-9][0-9]_[0-9][0-9]_[0-9][0-9]//' | sort | uniq -c | sort -rn

   # Topic clusters
   find . -type f -name "*.pdf" | xargs -I {} basename {} .pdf | \
     sed 's/_part_[0-9]*//;s/_[0-9][0-9]*$//' | sort | uniq -c | sort -rn | awk '$1 > 2'
   ```

4. **Execute strategic merges** using appropriate patterns. See `references/merging-strategies.md` for time-series, topic-based, and format consolidation scripts. Preserve timestamps on all merged outputs.

5. **Recount and validate** the final total is at or below 50 (ideally 48 to reserve slots for future additions).

### Step 2: Understand the Scope

Ask clarifying questions:
- What is the topic/purpose of this knowledge base?
- Which directory contains the source materials?
- Target: single notebook or multiple related notebooks?
- Any files that must stay in original format?
- Is this for research, learning, project documentation, or reference?

### Step 3: Analyze Current State

Review files for NotebookLM compatibility:

```bash
find . -type f -exec file {} \;
find . -type f -exec du -h {} \; | sort -rh
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
for f in *.pdf; do pdftotext "$f" - | wc -w; done
```

Categorize findings:
- **Compatible as-is**: PDF, DOCX, TXT, MD, images
- **Needs conversion**: PPTX, XLSX, XLS, PPT, scanned PDFs
- **Too large**: Files >500k words or >200MB
- **Duplicates**: Same content in different formats
- **Merge candidates**: Sources identified for consolidation in Step 1

### Step 4: Convert Unsupported Formats

**PowerPoint to PDF:**
```bash
soffice --headless --convert-to pdf *.pptx
touch -r original.pptx converted.pdf  # Preserve timestamp
```

**Excel to CSV:**
```bash
soffice --headless --convert-to csv:"Text - txt - csv (StarCalc)":44,34,UTF8 *.xlsx
touch -r original.xlsx converted.csv  # Preserve timestamp
```

**Scanned PDF to Searchable:**
```bash
ocrmypdf input.pdf output_searchable.pdf
touch -r input.pdf output_searchable.pdf  # Preserve timestamp
pdftotext output_searchable.pdf - | wc -w  # Verify text extraction
```

WARNING: Always run `touch -r original converted` after every conversion to preserve the original file timestamp.

### Step 5: Apply Naming

Use this pattern: `category_topic_descriptor_YYYY_MM_DD.ext`

Examples:
- `research_quantum_computing_basics_2025.pdf`
- `meeting_notes_project_kickoff_2026_01_15.txt`
- `client_proposal_acme_corp_final.docx`
- `reference_api_documentation_v2.md`
- `data_sales_figures_q4_2025.csv`

See `references/organization-scripts.md` for the automated naming script. Preserve timestamps when renaming: use `mv` (preserves by default) and verify with `stat`.

### Step 6: Split Large Documents

For files >500k words or >200MB:

```bash
pdftotext document.pdf - | wc -w  # Check word count
pdftk large.pdf cat 1-500 output large_part_1.pdf
pdftk large.pdf cat 501-1000 output large_part_2.pdf
touch -r large.pdf large_part_1.pdf large_part_2.pdf  # Preserve timestamps
```

Name parts by content, not arbitrary numbers:
- `annual_report_2025_part_1_executive_summary.pdf`
- `annual_report_2025_part_2_financials.pdf`
- `annual_report_2025_part_3_appendices.pdf`

### Step 7: Consolidation Pass

Perform strategic merging to optimize source count. This step is critical when merge candidates were identified in Step 1 or the collection is near the 50-source limit.

Merging is a primary optimization strategy, not a last resort. Three patterns apply:

- **Time-series**: Combine chronological documents into period summaries (daily to monthly, weekly to quarterly)
- **Topic-based**: Combine related papers/docs into comprehensive guides with chapter markers
- **Format consolidation**: Combine slides + transcript + notes for the same event into a single PDF

See `references/merging-strategies.md` for full merge patterns, scripts (time-series merger, topic-based PDF merger), decision trees, and quality checks.

IMPORTANT: Preserve chronological timestamps in merged content. Add clear date headers within merged files so temporal context is not lost.

Log all merge decisions for inclusion in the organization plan.

### Step 8: Implement Flat Structure

NotebookLM works best with flat source lists, no nested folders.

**Before:**
```
docs/
  project/
    planning/
      requirements.pdf
    research/
      background.pdf
  reference/
    api_docs.pdf
```

**After:**
```
notebooklm_sources/
  project_requirements_2026.pdf
  project_background_research.pdf
  reference_api_documentation.pdf
```

See `references/organization-scripts.md` for the implementation script. Preserve timestamps when copying: use `cp -p` to maintain original dates.

### Step 9: Find and Remove Duplicates

```bash
find . -type f -exec md5 {} \; | sort | uniq -d
find . -type f -printf '%f\n' | sed 's/\.[^.]*$//' | sort | uniq -d
for pdf in *.pdf; do echo "=== $pdf ==="; pdftotext "$pdf" - | md5; done | sort
```

Decision matrix:
- Same content, different formats: keep PDF (best for NotebookLM)
- Same content, different names: keep most descriptive name
- Slight variations: merge into single document if <500k words
- Truly duplicate: delete older version (check timestamps first)

### Step 10: Optimize for RAG

NotebookLM uses RAG, which works best with focused documents:

- Split 100-page documents into 3-5 topic-focused files
- Separate chapters/sections into individual sources
- Keep each source focused on one topic/subtopic
- Prefer 20-50 pages per PDF over 200+ page megadocs

```
Instead of:
  company_handbook_500_pages.pdf

Create:
  handbook_code_of_conduct.pdf
  handbook_benefits_overview.pdf
  handbook_time_off_policy.pdf
  handbook_remote_work_guidelines.pdf
  handbook_career_development.pdf
```

### Step 11: Propose Organization Plan

Present a plan to the user before making changes. The plan should cover current state, source selection strategy (if >50 sources), proposed structure, changes to make, and a compatibility check.

See `references/organization-plan-template.md` for the full template with sections for prioritization results, merge decisions, and final source count verification.

### Step 12: Execute Organization

After user approval, execute all conversions, merges, renames, and structural changes. Log all operations.

See `references/organization-scripts.md` for the complete execution script with logging and limit verification. Run `touch -r` after every file operation to preserve original timestamps.

### Step 13: Provide Upload Instructions

Provide the user with a summary of organized sources and upload instructions for NotebookLM (direct upload and Google Drive options).

See `references/upload-guide.md` for the full upload instructions template including maintenance guidance.

## Examples

### Example 1: Research Paper Collection

**User**: "Prepare my PhD research papers folder for NotebookLM"

**Process**:
1. Finds 35 PDFs, 12 DOCX, 8 PPTX across nested folders
2. Converts 8 PPTX to PDF (preserves timestamps)
3. Identifies 2 papers >500k words, splits into parts
4. Renames: `smith_2024.pdf` to `research_quantum_entanglement_smith_2024.pdf`
5. Creates flat structure in `phd_research_sources/`
6. Result: 48 sources ready for upload

### Example 2: Company Knowledge Base

**User**: "Convert our company wiki exports to NotebookLM format"

Split single 145-page PDF by section into 7 focused sources:
- `company_overview_history_mission.pdf` (8 pages)
- `company_policies_hr_guidelines.pdf` (28 pages)
- `company_product_documentation.pdf` (45 pages)
- (4 more topic-focused files)

Result: 7 focused sources instead of 1 large doc. Better RAG retrieval.

### Example 3: Excel Data

**User**: "I have 10 Excel files with research data"

Convert each sheet to separate CSV. Name descriptively: `data_survey_responses_2025.csv`. Create overview doc: `data_overview_methodology.txt`. Preserve timestamps on all conversions.

Result: 10 XLSX to 23 CSV files + 1 overview doc.

### Example 4: Conference Materials

**User**: "Organize my conference materials for a knowledge base"

Input: 12 MP3 recordings, 8 PPTX decks, 15 JPG notes, 5 PDFs. Keep MP3 as-is (NotebookLM transcribes on upload). Convert PPTX to PDF. Keep JPGs (NotebookLM reads handwriting via OCR). Apply naming: `conf_session_title_speaker_date.ext`. Preserve all timestamps.

Result: 40 sources in flat folder.

### Example 5: Large Collection (200+ Sources)

For a complete workflow handling 200+ sources (e.g., reducing 237 sources to 48 with strategic merging), see `references/large-collection-workflow.md`.

## Common Patterns

### Academic Research
```
research_[topic]_[author]_[year].pdf
notes_[course]_[topic]_[date].md
textbook_[subject]_chapter_[n]_[title].pdf
```

### Business Projects
```
project_[name]_requirements.pdf
project_[name]_timeline.csv
meeting_[project]_[date]_notes.txt
client_[name]_proposal_final.docx
```

### Learning/Courses
```
course_[name]_lecture_[n]_[topic].pdf
course_[name]_readings_week_[n].pdf
course_[name]_assignment_[n].docx
```

### Personal Knowledge Base
```
article_[topic]_[author]_[date].pdf
book_notes_[title]_[author].md
tutorial_[skill]_[topic].pdf
reference_[tool]_documentation.pdf
```

## Pro Tips

1. **Optimize for Search**: Use descriptive names with search keywords.
   Good: `tutorial_python_async_programming_advanced.pdf`.
   Bad: `tutorial_5.pdf`.

2. **Topic-Based Splitting**: Split large docs by topic, not arbitrary page count.
   Good: `handbook_benefits.pdf`, `handbook_policies.pdf`.
   Bad: `handbook_part_1.pdf`, `handbook_part_2.pdf`.

3. **Date Formatting**: Use ISO format (YYYY-MM-DD) for sortability.
   Good: `meeting_notes_2026_02_04.txt`.
   Bad: `meeting_notes_feb_4_2026.txt`.

4. **Preserve Source Timestamps**: Always maintain original file creation/modification dates. These enable accurate recency scoring and help NotebookLM's RAG weight recent meeting notes, decisions, and additions appropriately. Use `touch -r original converted` after every conversion.

5. **Extract Text from Scans**: Scanned PDFs do not work in NotebookLM. Test with `pdftotext test.pdf - | head`. If blank, run `ocrmypdf input.pdf output.pdf`.

6. **Use Prefixes for Ordering**: Add numeric prefixes for logical ordering: `01_project_overview.pdf`, `02_project_requirements.pdf`.

7. **Test Before Bulk Upload**: Upload 2-3 files first to verify processing, summaries, and search accuracy. Then upload the rest.

## Best Practices Summary

**Source Selection and Optimization:**
- Always assess total source count first before organizing
- Use scoring rubric for objective prioritization (>50 sources)
- Merge strategically as primary optimization, not last resort
- Prefer quality over quantity: 48 great sources over 50 mediocre ones
- Reserve 2-3 slots for future additions
- Do not merge high-value unique sources (score 35+)
- Do not combine unrelated topics just to hit limits

**File Naming:**
- Descriptive snake_case with searchable terms and ISO dates
- Keep under 100 characters, no spaces or special characters
- Use dates instead of version numbers

**Format Selection:**
- PDF for presentations and mixed content
- CSV for spreadsheet data
- DOCX/TXT/MD for text documents
- Always convert PPTX and XLSX before upload

**Timestamp Preservation:**
- Run `touch -r original converted` after every conversion
- Use `cp -p` when copying files to preserve modification dates
- Include ISO dates in filenames for explicit temporal context
- Timestamps drive recency scoring and RAG relevance weighting

**Organization Structure:**
- Flat structure (one folder, all files)
- Descriptive names include folder context
- Stay under 50 sources per notebook

## Implementation Checklist

**Phase 1: Assessment and Prioritization**
- [ ] Identify target notebook topic/purpose
- [ ] Locate all source files and count total
- [ ] If >50: run scoring rubric for all sources
- [ ] If >50: identify and execute strategic merges
- [ ] If >50: select top sources using decision matrix (target 48)
- [ ] Check file formats, note conversions needed
- [ ] Estimate word counts for large files

**Phase 2: Conversion and Organization**
- [ ] Convert unsupported formats (preserve timestamps)
- [ ] Apply descriptive snake_case naming
- [ ] Split large documents by topic
- [ ] Remove duplicates
- [ ] Create flat output directory
- [ ] Verify all files <200MB and <500k words
- [ ] Verify final source count is at or below 50
- [ ] Verify timestamps preserved on all converted/moved files

**Phase 3: Upload and Verification**
- [ ] Document selection strategy in organization plan
- [ ] Test upload 2-3 files
- [ ] Upload remaining sources
- [ ] Verify NotebookLM processing and summaries
- [ ] Test search functionality
- [ ] Confirm all key topics covered despite any source reduction
