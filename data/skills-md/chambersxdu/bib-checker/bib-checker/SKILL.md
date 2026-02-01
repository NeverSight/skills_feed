---
name: bib-checker
description: "Verify BibTeX references for authenticity and correctness. Use when users ask to: (1) check if references in .bib files are real and accurate, (2) verify paper citations exist, (3) update arXiv preprints to published versions, (4) validate bibliography entries, (5) check for outdated or incorrect citation information, (6) audit references in academic papers."
---

# BibTeX Reference Checker

Verify authenticity and correctness of references in BibTeX files using web search.

## Workflow

1. Parse `.bib` file and extract all entries
2. For each entry, verify using web search tools
3. Check authenticity (does the paper exist?)
4. Check correctness (is the citation info accurate and up-to-date?)
5. Report issues and suggest fixes

## Verification Process

### Step 1: Parse BibTeX Entry

Extract key fields:
- `title` - Paper title
- `author` - Author names
- `year` - Publication year
- `booktitle` / `journal` - Venue
- `doi` - Digital Object Identifier
- `url` - Link to paper
- `eprint` / `arxivId` - arXiv identifier

### Step 2: Web Search Verification

Use `fetch_webpage` tool to query these sources:

1. **Google Scholar**: Search title + first author
2. **DBLP** (`dblp.org`): Authoritative CS bibliography
3. **Semantic Scholar** (`semanticscholar.org`): Academic search
4. **arXiv** (`arxiv.org`): For preprint verification
5. **DOI resolver** (`doi.org`): Verify DOI links

Search query construction:
```
"[exact paper title]" [first author last name] [year]
```

### Step 3: Authenticity Checks

| Check | Issue | Action |
|-------|-------|--------|
| Title not found anywhere | Paper may not exist | Flag as potentially fake |
| Authors don't match | Wrong attribution | Report discrepancy |
| Year mismatch | Incorrect year | Suggest correction |
| Venue doesn't exist | Fake conference/journal | Flag as suspicious |

**Red flags for fake references:**
- No search results for exact title
- Conference/journal has no web presence
- Author has no other publications
- DOI doesn't resolve

### Step 4: Correctness Checks

| Issue | Detection | Fix |
|-------|-----------|-----|
| arXiv → Published | Found in conference/journal proceedings | Update entry type, add venue |
| Wrong venue | DBLP shows different venue | Correct booktitle/journal |
| Missing DOI | DOI exists but not in entry | Add DOI field |
| Outdated info | Newer version available | Update fields |
| Wrong entry type | @article should be @inproceedings | Change entry type |

## Common Update Patterns

### arXiv to Conference
```bibtex
% Before (incorrect)
@article{smith2023,
  title = {Some Paper},
  author = {Smith, John},
  journal = {arXiv preprint arXiv:2301.12345},
  year = {2023}
}

% After (correct)
@inproceedings{smith2023,
  title = {Some Paper},
  author = {Smith, John},
  booktitle = {Proceedings of NeurIPS},
  year = {2023},
  doi = {10.xxxx/xxxxx}
}
```

### arXiv to Journal
```bibtex
% Before
@misc{doe2022,
  title = {Another Paper},
  author = {Doe, Jane},
  eprint = {2201.00001},
  archivePrefix = {arXiv}
}

% After
@article{doe2022,
  title = {Another Paper},
  author = {Doe, Jane},
  journal = {Nature Machine Intelligence},
  volume = {4},
  pages = {123--135},
  year = {2022},
  doi = {10.1038/s42256-022-00001-1}
}
```

## Output Report Format

```
=== BibTeX Verification Report ===

[✓] smith2023: "Deep Learning Methods" - Verified (NeurIPS 2023)

[!] jones2024: "Neural Networks Study"
    Issue: arXiv preprint has been published
    Current: @article with journal = {arXiv preprint arXiv:2401.xxxxx}
    Found: Published at ICML 2024
    Suggested fix: Update to @inproceedings with booktitle = {ICML}

[✗] fake2023: "Amazing Results Paper"
    Issue: Paper not found in any database
    Action: Verify this reference manually - may not exist

[!] wang2022: "Transformer Architecture"
    Issue: Author name mismatch
    Current: author = {Wang, John}
    Found: author = {Wang, Jun}

Summary:
- Total entries: 25
- Verified: 20
- Needs update: 3
- Suspicious: 2
```

## Verification Priority

Check in this order (most reliable first):
1. **DOI** - If present, resolve and verify
2. **DBLP** - Authoritative for CS papers
3. **Semantic Scholar** - Good coverage across fields
4. **Google Scholar** - Broadest coverage
5. **arXiv** - For preprints

## Handling Edge Cases

- **Workshop papers**: May not appear in DBLP, verify via conference website
- **Thesis citations**: Search university repository
- **Technical reports**: Search organization website
- **Non-English papers**: Search with original language title
- **Very recent papers**: May only be on arXiv, note as "preprint - check later"

## Interactive Fixing

When updating entries:
1. Show current entry
2. Show verified information from web
3. Display proposed changes as diff
4. Apply fixes while preserving BibTeX key and custom fields
