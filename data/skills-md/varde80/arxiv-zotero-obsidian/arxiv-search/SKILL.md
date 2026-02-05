---
name: arxiv-search
description: Search arXiv for academic papers. Use when users want to find research papers, preprints, or academic articles on any topic. Supports filtering by date, category, and author.
allowed-tools: Read,Bash,Write
---

# arXiv Paper Search Skill

Search the arXiv repository for academic papers and preprints.

## Usage

When the user asks to search for papers, use the search script:

```bash
cd /Users/varde/code/arxiv-zotero-obsidian && python3 .claude/skills/arxiv-search/scripts/search_arxiv.py --query "SEARCH_TERMS" --max-results 10
```

## Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--query` | Search query (required) | - |
| `--max-results` | Maximum results | 10 |
| `--sort-by` | Sort: relevance, submitted_date, last_updated | relevance |
| `--category` | arXiv category (e.g., cs.AI, physics.cond-mat) | - |
| `--date-from` | Filter from date (YYYY-MM-DD) | - |
| `--date-to` | Filter until date (YYYY-MM-DD) | - |
| `--output` | Output format: text, json | text |

## Query Syntax

arXiv supports field-specific searches:

- `ti:keyword` - Search in title
- `au:name` - Search by author
- `abs:keyword` - Search in abstract
- `cat:category` - Filter by category

### Examples

```bash
# General topic search
python3 .claude/skills/arxiv-search/scripts/search_arxiv.py --query "quantum machine learning"

# Search by author
python3 .claude/skills/arxiv-search/scripts/search_arxiv.py --query "au:Hinton"

# Search with category filter
python3 .claude/skills/arxiv-search/scripts/search_arxiv.py --query "deep learning" --category "cs.LG"

# Combined query
python3 .claude/skills/arxiv-search/scripts/search_arxiv.py --query "ti:transformer AND abs:attention"

# Recent papers only
python3 .claude/skills/arxiv-search/scripts/search_arxiv.py --query "large language models" --date-from "2024-01-01"
```

## Output Format

The script outputs paper details including:
- **arxiv_id**: Unique identifier (use this for downloading)
- **title**: Paper title
- **authors**: Author names
- **abstract**: Paper abstract (truncated in text mode)
- **published**: Publication date
- **pdf_url**: Direct PDF download link
- **categories**: Subject categories

## Workflow

1. Run the search with user's query
2. Display results in a numbered list
3. Ask user which paper(s) they want to download/add to Zotero
4. Note the arxiv_id for use with zotero-add skill
