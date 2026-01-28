---
name: medical-imaging-review
description: Write comprehensive literature reviews for medical imaging AI research. Use when writing survey papers, systematic reviews, or literature analyses on topics like segmentation, detection, classification in CT, MRI, X-ray imaging. Triggers on requests for "review paper", "survey", "literature review", "综述", or mentions of writing academic reviews on deep learning for medical imaging.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - TodoWrite
---

# Medical Imaging AI Literature Review Writing Skill

A systematic workflow for writing comprehensive literature reviews in medical imaging AI.

## Quick Start

When user requests a literature review:

1. **Initialize project** with three core files:
   - `CLAUDE.md` - Writing guidelines and terminology
   - `IMPLEMENTATION_PLAN.md` - Staged execution plan
   - `manuscript_draft.md` - Main manuscript

2. **Follow the 7-phase workflow** (see [WORKFLOW.md](WORKFLOW.md))

3. **Use standard templates** (see [TEMPLATES.md](TEMPLATES.md))

## Core Principles

### Writing Style
- Use **hedging language**: "may", "suggests", "appears to", "has shown promising results"
- Avoid absolute claims: Never say "X is the best method"
- Every claim needs citation support
- Each method section needs a **Limitations** paragraph

### Required Elements
- **Key Points box** (3-5 bullets) after title
- **Comparison table** for each major section
- **Performance metrics** with consistent format (Dice: 0.XXX, HD95: X.XX mm)
- **Figure placeholders** with detailed captions
- **References organized by topic** (80-120 typical)

### Paragraph Structure
1. Topic sentence (main claim)
2. Supporting evidence (citations + data)
3. Analysis (critical evaluation)
4. Transition to next paragraph

## Literature Sources

### ArXiv MCP (Preprints & Latest Research)

GitHub: https://github.com/blazickjp/arxiv-mcp-server

**Available Tools:**
- `search_papers` - Search by keywords with date range and category filters
- `download_paper` - Download paper by arXiv ID
- `list_papers` - List all downloaded papers
- `read_paper` - Read downloaded paper content

**Configuration:**
```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-mcp-server"],
      "env": {
        "ARXIV_STORAGE_PATH": "~/.arxiv-mcp-server/papers"
      }
    }
  }
}
```

**Usage Example:**
```
Search: "medical image segmentation transformer"
Categories: cs.CV, eess.IV
Date range: 2023-01-01 to present
Max results: 50
```

### PubMed MCP (Biomedical Literature)

GitHub: https://github.com/grll/pubmedmcp

Access 35+ million biomedical literature citations.

**Configuration:**
```json
{
  "mcpServers": {
    "pubmedmcp": {
      "command": "uvx",
      "args": ["pubmedmcp@latest"],
      "env": {
        "UV_PRERELEASE": "allow",
        "UV_PYTHON": "3.12"
      }
    }
  }
}
```

**Search Tips:**
- Use MeSH terms for precise medical searches
- Combine with publication type filters (Review, Clinical Trial)
- Filter by date for recent literature

### Zotero Integration (Reference Management)

Access local Zotero database (Requires the user to provide their user ID.):
```bash
# List collections
curl -s "http://localhost:23119/api/users/[USER_ID]/collections"

# Get items from collection
curl -s "http://localhost:23119/api/users/[USER_ID]/collections/[KEY]/items"
```

Alternatively, Zotero-MCP can be used, but it requires users to perform manual configuration in advance.

Extract: title, abstractNote, date, creators, publicationTitle, DOI

### Source Selection Guide

| Source | Best For | Strengths |
|--------|----------|-----------|
| **ArXiv** | Latest methods, deep learning advances | Preprints, fast access, CS/AI focus |
| **PubMed** | Clinical validation, medical context | Peer-reviewed, MeSH indexing, clinical |
| **Zotero** | Organized collections, existing library | Local management, annotations, PDFs |

## Standard Review Structure

```markdown
# [Title]: State of the Art and Future Directions

## Key Points
- [3-5 bullets summarizing main findings]

## Abstract

## 1. Introduction
### 1.1 Clinical Background
### 1.2 Technical Challenges
### 1.3 Scope and Contributions

## 2. Datasets and Evaluation Metrics
### 2.1 Public Datasets
**Table 1. Public Datasets**
| Dataset | Year | Cases | Annotation | Access |

### 2.2 Evaluation Metrics

## 3. Deep Learning Methods
### 3.1 [Category 1]
### 3.2 [Category 2]
...
**Table 2. Method Comparison**
| Reference | Category | Architecture | Dataset | Performance | Innovation |

## 4. Downstream Applications

## 5. Commercial Products & Clinical Translation
**Table 3. Commercial Products**

## 6. Discussion
### 6.1 Current Limitations
### 6.2 Future Directions

## 7. Conclusion

## References
```

## Method Description Template

```markdown
### 3.X [Method Category]

[1-2 paragraph introduction with motivation]

**[Method Name]:** [Author] et al. [ref] proposed [method], which [innovation]:
- [Key component 1]
- [Key component 2]
Achieves Dice of X.XX on [dataset].

**Mathematical Formulation:** (if applicable)
$$\mathcal{L} = \mathcal{L}_{seg} + \lambda \mathcal{L}_{aux}$$

**Limitations:** Despite advantages, [category] methods face: (1) [limit 1]; (2) [limit 2].
```

## Citation Patterns

```markdown
# Data citation
"...achieved Dice of 0.89 [23]"

# Method citation
"Gu et al. [45] proposed..."

# Multi-citation
"Several studies demonstrated... [12, 15, 23]"

# Comparative
"While [12] focused on..., [15] addressed..."
```

## Quality Checklist

Before completion, verify:
- [ ] Key Points present (3-5 bullets)
- [ ] Table per major section
- [ ] Limitations for each method category
- [ ] Consistent terminology throughout
- [ ] Hedging language used appropriately
- [ ] 80-120 references, organized by topic
- [ ] Figure placeholders with captions

## File References

- [WORKFLOW.md](WORKFLOW.md) - Detailed 7-phase workflow
- [TEMPLATES.md](TEMPLATES.md) - CLAUDE.md and IMPLEMENTATION_PLAN.md templates
- [DOMAINS.md](DOMAINS.md) - Domain-specific method categories
