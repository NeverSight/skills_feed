---
name: citation-format
description: "Format citations and bibliographies in multiple academic styles (APA, IEEE, Chicago, Harvard, MLA, Nature, Science). Use when: (1) Converting between citation styles for different journals, (2) Cleaning and standardizing bibliography entries, (3) Validating citation formatting before submission, (4) Generating properly formatted reference lists, (5) Checking citation consistency across manuscripts."
allowed-tools: Read, Write
version: 1.0.0
---

# Citation Formatting Skill

## Purpose

Format academic citations according to standard style guides. Ensures proper citation formatting for journal submissions, dissertations, and academic publications.

## Supported Citation Styles

### 1. APA 7th Edition
**Use for:** Psychology, education, social sciences

**Journal Article:**
```
Smith, J., & Jones, M. (2023). Title of article. Journal Name, 15(2), 123-145. https://doi.org/10.1000/xyz123
```

**Book:**
```
Author, A. A. (2023). Title of book (2nd ed.). Publisher Name.
```

**Chapter:**
```
Author, A. A. (2023). Chapter title. In B. B. Editor (Ed.), Book title (pp. 45-67). Publisher.
```

### 2. IEEE
**Use for:** Engineering, computer science, technology

**Journal Article:**
```
[1] J. Smith and M. Jones, "Title of article," Journal Name, vol. 15, no. 2, pp. 123-145, 2023.
```

**Conference:**
```
[1] J. Smith, "Paper title," in Proc. Conference Name, City, Country, 2023, pp. 45-52.
```

### 3. Chicago (Author-Date)
**Use for:** History, arts, humanities

**Journal Article:**
```
Smith, John, and Mary Jones. 2023. "Title of Article." Journal Name 15 (2): 123-145.
```

**Book:**
```
Smith, John. 2023. Book Title. City: Publisher Name.
```

### 4. Chicago (Notes-Bibliography)
**Footnote:**
```
1. John Smith and Mary Jones, "Title of Article," Journal Name 15, no. 2 (2023): 123-145.
```

**Bibliography:**
```
Smith, John, and Mary Jones. "Title of Article." Journal Name 15, no. 2 (2023): 123-145.
```

### 5. Harvard
**Use for:** UK universities, various disciplines

```
Smith, J. and Jones, M. (2023) 'Title of article', Journal Name, 15(2), pp. 123-145.
```

### 6. MLA 9th Edition
**Use for:** Literature, languages, humanities

```
Smith, John, and Mary Jones. "Title of Article." Journal Name, vol. 15, no. 2, 2023, pp. 123-145.
```

### 7. Nature
**Use for:** Natural sciences

```
Smith, J. & Jones, M. Title of article. Journal Name 15, 123-145 (2023).
```

### 8. Science
**Use for:** Multidisciplinary sciences

```
J. Smith, M. Jones, Title of article. Journal Name 15, 123 (2023).
```

## When to Use This Skill

1. **Journal Submission** - Format references for target journal
2. **Style Conversion** - Convert between styles (APA → IEEE)
3. **Dissertation Formatting** - Ensure consistency across chapters
4. **Bibliography Cleaning** - Fix formatting errors in .bib files
5. **Citation Validation** - Verify proper formatting before submission
6. **Collaborative Writing** - Standardize citations from multiple authors

## Common Formatting Tasks

### Task 1: Convert Citation Style

**Input:**
```
Style: APA → IEEE
Citation: Smith, J., & Jones, M. (2023). Deep learning. AI Journal, 15(2), 123-145.
```

**Process:**
1. Extract metadata: authors, title, journal, volume, issue, pages, year
2. Apply IEEE template
3. Add numbering

**Output:**
```
[1] J. Smith and M. Jones, "Deep learning," AI Journal, vol. 15, no. 2, pp. 123-145, 2023.
```

### Task 2: Clean BibTeX Entry

**Input (messy):**
```bibtex
@article{smith2023,
  author={Smith, John and Jones, Mary and Johnson, Bob},
  title={A Really Long Title That Goes On And On},
  journal={Journal},
  year=2023,
  volume=15,
  pages={123--145},
  doi={10.1000/xyz}
}
```

**Output (cleaned):**
```bibtex
@article{smith2023deep,
  author = {Smith, John and Jones, Mary and Johnson, Bob},
  title = {A Really Long Title That Goes On and On},
  journal = {Journal Name},
  year = {2023},
  volume = {15},
  number = {2},
  pages = {123--145},
  doi = {10.1000/xyz123}
}
```

### Task 3: Generate Reference List

**Input:** List of DOIs or BibTeX entries  
**Output:** Formatted reference list in specified style

## Formatting Rules by Style

### APA 7th Edition Rules
- **Author names:** Last, F. M., & Last, F. M.
- **Year:** (2023)
- **Title:** Sentence case (only first word capitalized)
- **Journal:** Title Case, volume(issue), pages
- **DOI:** https://doi.org/10.xxxx/yyyy

### IEEE Rules
- **Numbering:** [1], [2], [3] in order of appearance
- **Author names:** F. M. Last and F. M. Last
- **Title:** "Title case with quotes"
- **Journal:** Italic Journal, vol. 15, no. 2, pp. 123-145, Month 2023
- **DOI:** doi: 10.xxxx/yyyy

### Chicago Rules
- **Author-Date:** Last, First, and First Last. Year.
- **Notes:** Superscript footnote numbers
- **Bibliography:** Alphabetical by last name
- **Title:** Title Case for Books, "Sentence case" for articles

## Integration with Other Components

### With Citation-Management MCP Server
```
Use citation-management MCP to:
1. Fetch metadata from DOI
2. Verify citations via Crossref
3. Check for retractions
4. Then apply formatting with this skill
```

### With Manuscript-Writer Agent
```
Agent workflow:
1. Collect citations during writing
2. Use citation-format skill to format
3. Generate bibliography
4. Validate all citations before submission
```

### With Bibliography Tools
- **BibTeX:** Parse and reformat .bib files
- **Zotero:** Export and format Zotero libraries
- **Mendeley:** Convert Mendeley exports

## Examples

### Example 1: Multi-Author APA Citation

**Input Data:**
```
Authors: Smith, J., Jones, M., Johnson, B., Williams, K., Brown, L., Davis, R., Miller, T., Wilson, P.
Year: 2023
Title: large-scale meta-analysis of intervention effects
Journal: Psychological Bulletin
Volume: 149
Issue: 3
Pages: 456-489
DOI: 10.1037/bul0000123
```

**APA Format (7+ authors):**
```
Smith, J., Jones, M., Johnson, B., Williams, K., Brown, L., Davis, R., Miller, T., & Wilson, P. (2023). Large-scale meta-analysis of intervention effects. Psychological Bulletin, 149(3), 456-489. https://doi.org/10.1037/bul0000123
```

### Example 2: Conference Proceedings (IEEE)

**Input Data:**
```
Authors: Zhang, L., Kumar, R.
Year: 2024
Title: Neural architecture search using reinforcement learning
Conference: International Conference on Machine Learning
Location: Vienna, Austria
Pages: 1234-1242
```

**IEEE Format:**
```
[1] L. Zhang and R. Kumar, "Neural architecture search using reinforcement learning," in Proc. Int. Conf. Mach. Learn., Vienna, Austria, 2024, pp. 1234-1242.
```

### Example 3: Book Chapter (Chicago)

**Input Data:**
```
Author: Thompson, S.
Year: 2023
Chapter: Qualitative research methods in education
Editors: Anderson, P., Baker, M.
Book: Handbook of Educational Research
Pages: 234-267
Publisher: Academic Press
Location: New York
```

**Chicago (Author-Date):**
```
Thompson, Sarah. 2023. "Qualitative Research Methods in Education." In Handbook of Educational Research, edited by Peter Anderson and Michelle Baker, 234-267. New York: Academic Press.
```

## Validation Checklist

Before finalizing citations, verify:

- [ ] **Author names** formatted correctly for style
- [ ] **Publication year** present and correct
- [ ] **Title** capitalization follows style rules
- [ ] **Journal names** spelled out or abbreviated per style
- [ ] **Volume and issue** numbers formatted correctly
- [ ] **Page ranges** use correct separator (–, --, or -)
- [ ] **DOIs** formatted correctly and functional
- [ ] **Punctuation** matches style guide exactly
- [ ] **Hanging indents** applied (APA, MLA, Chicago)
- [ ] **Numbering** sequential and correct (IEEE)
- [ ] **Alphabetical order** correct (most styles)

## Common Errors to Fix

### Error 1: Incorrect Capitalization
❌ "Deep Learning Applications in Medical Imaging"  (Title Case in APA)
✅ "Deep learning applications in medical imaging" (Sentence case)

### Error 2: Missing DOI
❌ Citation without DOI
✅ Add: https://doi.org/10.xxxx/yyyy

### Error 3: Inconsistent Formatting
❌ Mixed citation styles in one document
✅ All citations use same style

### Error 4: Incorrect Ampersand Usage
❌ "Smith and Jones" in APA in-text citation
✅ "Smith & Jones" in APA in-text citation

### Error 5: Page Range Separator
❌ "123-145" in Chicago (should be en-dash)
✅ "123–145" in Chicago

## Best Practices

1. **Choose Style Early** - Select citation style at project start
2. **Use Reference Manager** - Zotero, Mendeley, or EndNote
3. **Validate DOIs** - Ensure all DOIs resolve correctly
4. **Check Journal Requirements** - Some journals have specific rules
5. **Automate When Possible** - Use tools for consistent formatting
6. **Proofread Carefully** - Citation errors are common in rejections

## Resources

- **APA Style:** https://apastyle.apa.org/
- **IEEE Reference Guide:** https://ieee-dataport.org/sites/default/files/analysis/27/IEEE%20Citation%20Guidelines.pdf
- **Chicago Manual of Style:** https://www.chicagomanualofstyle.org/
- **MLA Handbook:** https://style.mla.org/
- **Purdue OWL:** https://owl.purdue.edu/owl/research_and_citation/

---

**Last Updated:** 2025-11-09
**Version:** 1.0.0
