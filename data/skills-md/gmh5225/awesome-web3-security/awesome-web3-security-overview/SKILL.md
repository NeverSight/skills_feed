---
name: awesome-web3-security-overview
description: Guide for understanding and contributing to the awesome-web3-security curated resource list. Use this skill when adding resources, organizing categories, or maintaining README.md consistency (no duplicates).
---

# Awesome Web3 Security - Project Overview

## Purpose

This is a curated collection of Web3 security materials and resources for pentesters, auditors, and bug hunters. The goal is to keep the list **high-signal**, **well-categorized**, and **non-duplicated**.

## Project Structure

```
awesome-web3-security/
├── README.md                # Main resource list (curated)
├── LICENSE                  # License
├── .claude/
│   └── skills/              # Claude skills (this directory)
└── ref/                     # Optional reference notes (not curated)
    ├── notes/               # Personal notes, drafts, checklists
    └── Crypto-resources/    # Reference lists (used for gap checks)
```

## README.md Format Convention

### Heading Structure

- Top-level categories use `##`.
- Subcategories use `###` (e.g., inside `Development`).
- Starter Pack uses bold bullets for sub-sections (e.g., `- **Bug Bounties**`).

### Link Format

- Use full URLs, one per bullet line.
- Add a short description in square brackets: `- https://... [Short description]`
- Keep descriptions **English** and concise.
- Do not add the same URL in multiple places.

### Example Entry

```markdown
### Decompilers
- https://example.com/tool [EVM decompiler]
```

## Categorization Rules (How to Place a New Link)

- **Security Starter Pack**: learning, CTFs, audits/bounties, newsletters, beginner tools.
- **Blockchain Guide**: ecosystem overviews, protocol primers, learning roadmaps (broad).
- **Development**: frameworks, SDKs, tools, compilers, decompilers, test suites, contract source code.
- **Security**: security references, standards, vulnerability catalogs, analyzers, audit methodology.
- **DeFi Topics**: Stablecoin/MEV and other DeFi-focused topics.

## Duplicate Policy

**No duplicate URLs in README.md.** If a link fits multiple categories, pick the primary one.

## Contribution Checklist

1. Check for duplicates in `README.md` before adding.
2. Verify the link points to the canonical source (avoid low-value forks).
3. Keep the description English and useful.
4. Put it into the most appropriate category.
5. Prefer minimal changes over reformatting large sections.

## Data Source

For detailed and up-to-date resources, fetch the full list from:
```
https://raw.githubusercontent.com/gmh5225/awesome-web3-security/refs/heads/main/README.md
```

