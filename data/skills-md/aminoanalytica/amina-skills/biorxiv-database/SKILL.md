---
name: biorxiv-database
description: Search and retrieve preprints from bioRxiv. Use when asked to "search bioRxiv", "find preprints", "look up bioRxiv papers", or retrieve life sciences literature.
---

# bioRxiv Database

A Python toolkit for programmatic access to bioRxiv preprints. Supports comprehensive metadata retrieval with structured JSON output for integration into research workflows.

## Use Cases

- Query recent preprints by topic or research domain
- Monitor publications from specific researchers
- Perform systematic literature reviews
- Analyze publication trends across time periods
- Retrieve citation metadata and DOIs
- Download preprint PDFs for text analysis
- Filter results by subject category

## Quick Start

```bash
# Install dependencies
pip install requests

# Search by keywords
python scripts/biorxiv_client.py --terms "protein folding" --recent 30 --out results.json

# Search by author
python scripts/biorxiv_client.py --author "Chen" --recent 180

# Get specific paper by DOI
python scripts/biorxiv_client.py --doi "10.1101/2024.05.22.594321"

# Download PDF
python scripts/biorxiv_client.py --doi "10.1101/2024.05.22.594321" --fetch-pdf paper.pdf
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-t, --terms` | Search keywords (multiple allowed) |
| `-a, --author` | Author name to search |
| `--doi` | Specific DOI to retrieve |
| `--since` | Start date (YYYY-MM-DD) |
| `--until` | End date (YYYY-MM-DD) |
| `--recent` | Search last N days |
| `-s, --subject` | Subject category filter |
| `--fields` | Fields to search: title, abstract, authors |
| `-o, --out` | Output file (default: stdout) |
| `--max` | Maximum results to return |
| `--fetch-pdf` | Download PDF (requires --doi) |
| `-v, --verbose` | Enable debug output |

## Programmatic API

```python
from scripts.biorxiv_client import PreprintClient

client = PreprintClient(debug=True)

# Search by keywords
results = client.find_by_terms(
    terms=["enzyme engineering"],
    since="2024-01-01",
    until="2024-12-31",
    subject="biochemistry"
)

# Search by author
papers = client.find_by_author(name="Garcia", since="2023-01-01")

# Get paper by DOI
metadata = client.get_by_doi("10.1101/2024.05.22.594321")

# Download PDF
client.fetch_pdf(doi="10.1101/2024.05.22.594321", destination="paper.pdf")

# Normalize output
formatted = client.normalize(metadata, include_abstract=True)
```

## Subject Categories

| Category | Category |
|----------|----------|
| animal-behavior-and-cognition | molecular-biology |
| biochemistry | neuroscience |
| bioengineering | paleontology |
| bioinformatics | pathology |
| biophysics | pharmacology-and-toxicology |
| cancer-biology | physiology |
| cell-biology | plant-biology |
| clinical-trials | scientific-communication-and-education |
| developmental-biology | synthetic-biology |
| ecology | systems-biology |
| epidemiology | zoology |
| evolutionary-biology | |
| genetics | |
| genomics | |
| immunology | |
| microbiology | |

## Response Structure

```json
{
  "query": {
    "terms": ["protein folding"],
    "since": "2024-03-01",
    "until": "2024-09-30",
    "subject": "biophysics"
  },
  "count": 87,
  "papers": [
    {
      "doi": "10.1101/2024.05.22.594321",
      "title": "Example Preprint Title",
      "authors": "Chen L, Patel R, Kim S",
      "corresponding_author": "Chen L",
      "institution": "Research Institute",
      "posted": "2024-05-22",
      "revision": "1",
      "category": "biophysics",
      "license": "cc_by",
      "paper_type": "new results",
      "abstract": "Abstract content here...",
      "pdf_link": "https://www.biorxiv.org/content/10.1101/2024.05.22.594321v1.full.pdf",
      "web_link": "https://www.biorxiv.org/content/10.1101/2024.05.22.594321v1",
      "journal_ref": ""
    }
  ]
}
```

## Best Practices

| Recommendation | Details |
|----------------|---------|
| Date ranges | Narrow ranges improve response time. Split large queries into chunks. |
| Category filters | Use `--subject` to reduce bandwidth and improve precision. |
| Rate limiting | Built-in 0.5s delay between requests. Add more for bulk operations. |
| Result caching | Save JSON outputs to avoid redundant API calls. |
| Version awareness | Preprints may have multiple versions. PDF URLs encode version numbers. |
| Error checking | Verify `count` in outputs. Zero results may indicate date or connectivity issues. |
| Debug mode | Use `--verbose` for detailed request/response logging. |

## Reference Files

| File | Contents |
|------|----------|
| [api-reference.md](references/api-reference.md) | Complete bioRxiv REST API documentation |
| [examples.md](references/examples.md) | Extended code examples and workflow patterns |
