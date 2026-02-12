---
name: article-extractor
description: Extract clean article content from URLs, removing ads, navigation, and clutter. Save as readable text files for research, archiving, or offline reading.
original_source: https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor
author: michalparkola
license: MIT
---

# Article Extractor Skill

This skill extracts clean article content from web URLs, removing ads, navigation, sidebars, and other clutter to save readable text files.

## When to Use This Skill

- Downloading article text from a URL
- Saving blog posts as clean text
- Removing distractions from web articles
- Archiving content for offline reading
- Extracting content for research
- Creating a local reading library

## How to Use

### Basic Extraction
```
Extract the article from https://example.com/article
```

### Save to Specific Location
```
Extract this article and save to ~/reading/
https://example.com/interesting-post
```

### Multiple Articles
```
Extract these articles:
- https://example.com/post-1
- https://example.com/post-2
- https://example.com/post-3
```

## Extraction Methods

The skill uses multiple tools in priority order:

### 1. Reader (Mozilla Readability)
- Uses Firefox Reader View algorithm
- Excellent at removing clutter
- Preserves article structure

### 2. Trafilatura (Python)
- Very accurate extraction
- Works great for blogs and news
- Options: `--no-comments`, `--precision`

### 3. Fallback (curl + parsing)
- No dependencies required
- Basic HTML parsing
- Less reliable but always works

## What Gets Preserved

- Article text and paragraphs
- Section headings
- Author information
- Publication date
- Article structure

## What Gets Removed

- Navigation bars
- Advertisements
- Newsletter signup forms
- Sidebars
- Comments sections
- Social sharing buttons
- Cookie notices
- Related article widgets

## Filename Generation

Files are named based on:
1. Article title (cleaned)
2. Special characters removed (/, :, ?, ", <, >, |)
3. Length limited to 80-100 characters
4. Extension: `.txt`

**Example:**
```
"How to Build a Great Product: A Guide"
  → "How to Build a Great Product - A Guide.txt"
```

## Output Format

After extraction:
```
Title: [Article Title]
Author: [Author Name]
Date: [Publication Date]
Source: [Original URL]

---

[Clean article content...]
```

## Error Handling

The skill handles:
- **Paywalled content**: Extracts available preview
- **Missing tools**: Falls back to alternatives
- **Invalid URLs**: Provides clear error message
- **Failed extraction**: Suggests manual copy
- **Filename issues**: Auto-sanitizes problematic characters

## Advanced Options

### With Metadata Only
```
Extract just the title and author from this URL
```

### Specific Format
```
Extract this article as markdown
```

### Research Mode
```
Extract and summarize the key points from this article
```

## Best Practices

1. **Check Output**: Always verify extraction quality
2. **Save Originals**: Keep the source URL for reference
3. **Organize Files**: Use meaningful folder structures
4. **Batch Processing**: Extract multiple related articles together
5. **Respect Copyright**: Use for personal research only

## Dependencies

For best results, install:
```bash
# Mozilla Readability
npm install -g @nicolo-ribaudo/readability-cli

# Or Trafilatura (Python)
pip install trafilatura
```

Without dependencies, the skill uses fallback methods.
