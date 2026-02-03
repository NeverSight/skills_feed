---
name: sanskrit-skills
description: Suite of Sanskrit learning skills covering verse analysis, grammar, vocabulary, literature, and devotional hymns. Use as an entry point when users ask general Sanskrit questions or need guidance on which specific skill to use.
---

# Sanskrit Skills Suite

Comprehensive Sanskrit learning tools organized by domain.

## Prerequisites

This skill suite requires **Python 3.10+** and **[uv](https://github.com/astral-sh/uv)** (Universal Python Packaging) to be installed on your system.

## Initial Setup

Before using the grammar or meter analysis tools for the first time, you must install the Sanskrit parser dependencies:

```bash
cd shared/scripts
uv sync --extra full
```

## Routing Instructions

1. **Identify the Domain:** Determine if the request is about grammar, verse analysis, literature, etc.
2. **Load Instructions:** Read the corresponding `SKILL.md` file (e.g., `vyakarana/SKILL.md`) to get specialized workflows and reference paths.
3. **Execute:** Follow the domain-specific instructions. Use `shared/` for common scripts and terminology.

## Available Modules

| Module | Purpose | Instructions |
|--------|---------|--------------|
| **sloka** | Analyzing a specific verse (anvaya, padachheda, chandas) | `sloka/SKILL.md` |
| **vyakarana** | Grammar (sandhi, samasa, declensions, conjugations) | `vyakarana/SKILL.md` |
| **kosha** | Word meanings, synonyms, etymology, gender | `kosha/SKILL.md` |
| **sahitya** | Literature (texts, authors, genres, rasa theory) | `sahitya/SKILL.md` |
| **stotra** | Devotional hymns, prayers, recitation guidance | `stotra/SKILL.md` |
| **shared** | Common scripts, Devanagari, and terminology | `shared/SKILL.md` |

## Quick Routing Table

| User Asks About | Route To |
|-----------------|----------|
| "Explain this shloka..." | sloka |
| "What is the sandhi in..." | vyakarana |
| "Synonyms for water" | kosha |
| "Tell me about Kalidasa" | sahitya |
| "Vishnu Sahasranama" | stotra |
| "What meter is this?" | sloka (chandas) |
| "Decline rāma" | vyakarana (vibhakti) |
| "What does X mean?" | kosha |

## Shared Resources

Common resources in `shared/`:

- **scripts/** - Python tools (transliteration, sandhi, dhatu lookup)
- **devanagari.md** - Script reference
- **transliteration.md** - IAST, HK, ITRANS systems
- **terminology.md** - Common Sanskrit terms
- **online-resources.md** - Ambuda, Sanskrit Sahitya, Ashtadhyayi.com, Dharmamitra

## Online Resources

| Purpose | Platform |
|---------|----------|
| Kavya with commentary | sanskritsahitya.org |
| Paninian grammar | ashtadhyayi.com |
| Text library | ambuda.org |
| Meter Identification | github.com/hrishikeshrt/chanda |
| Morphological Analysis | github.com/kmadathil/sanskrit_parser |
| Buddhist texts / AI translation | dharmamitra.org |
