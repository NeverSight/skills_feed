---
name: knowledge-ingestion-patterns
description: Patterns for ingesting knowledge into vector databases and RAG systems
---


# Knowledge Ingestion Patterns Skill

> Systematic approaches for ingesting different content types into RAG with optimal chunking, metadata, and retrieval quality.

## Overview

Different content types require different ingestion strategies. This skill documents best practices for:
- Websites and web content
- PDF documents
- Code repositories
- Conversation exports
- Research notes
- API documentation

## Core Principles

1. **Chunk for retrieval** - Optimize chunk size for the questions you'll ask
2. **Metadata matters** - Rich metadata enables filtered search
3. **Preserve context** - Don't lose meaning when splitting
4. **Deduplicate** - Avoid ingesting the same content twice

## Content Type Patterns


### Pattern 2: PDF Documents

**When to use**: Research papers, reports, ebooks, scanned documents

**Chunking Strategy**: Page-aware with overlap, handle tables/figures specially

```python
import fitz  # PyMuPDF
from typing import List, Dict

def chunk_pdf(pdf_path: str, chunk_size: int = 500) -> List[Dict]:
    """Extract and chunk PDF content with page awareness."""
    doc = fitz.open(pdf_path)
    chunks = []

    for page_num, page in enumerate(doc, 1):
        text = page.get_text()

        # Skip empty pages
        if not text.strip():
            continue

        # Split into paragraphs
        paragraphs = text.split('

')

        current_chunk = ""
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += " " + para
            else:
                if current_chunk:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": {
                            "type": "pdf",
                            "source": pdf_path,
                            "page": page_num,
                            "total_pages": len(doc)
                        }
                    })
                current_chunk = para

        # Don't forget last chunk of page
        if current_chunk:
            chunks.append({
                "content": current_chunk.strip(),
                "metadata": {
                    "type": "pdf",
                    "source": pdf_path,
                    "page": page_num,
                    "total_pages": len(doc)
                }
            })

    return chunks

def extract_pdf_tables(pdf_path: str) -> List[Dict]:
    """Extract tables from PDF as separate chunks."""
    import pdfplumber

    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            for table_num, table in enumerate(page.extract_tables(), 1):
                # Convert table to markdown format
                if table:
                    headers = table[0]
                    rows = table[1:]

                    md_table = "| " + " | ".join(str(h) for h in headers) + " |
"
                    md_table += "| " + " | ".join("---" for _ in headers) + " |
"
                    for row in rows:
                        md_table += "| " + " | ".join(str(c) for c in row) + " |
"

                    tables.append({
                        "content": md_table,
                        "metadata": {
                            "type": "pdf_table",
                            "source": pdf_path,
                            "page": page_num,
                            "table_number": table_num
                        }
                    })

    return tables
```

**Metadata Schema**:
```yaml
type: pdf | pdf_table
source: file path
page: page number
total_pages: document length
table_number: (for tables) which table on page
```


### Pattern 4: Websites / Web Content

**When to use**: Documentation sites, articles, blog posts

**Chunking Strategy**: Clean HTML, respect structure, handle navigation

```python
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import urljoin, urlparse

def chunk_webpage(url: str) -> List[Dict]:
    """Fetch and chunk a webpage."""
    response = httpx.get(url, follow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove noise
    for tag in soup.find_all(['nav', 'footer', 'aside', 'script', 'style']):
        tag.decompose()

    chunks = []

    # Find main content
    main = soup.find('main') or soup.find('article') or soup.find('body')

    # Chunk by sections
    for section in main.find_all(['section', 'div'], class_=lambda x: x and 'content' in str(x).lower()):
        text = section.get_text(separator=' ', strip=True)
        if len(text) > 100:  # Skip tiny sections
            chunks.append({
                "content": text,
                "metadata": {
                    "type": "webpage",
                    "source": url,
                    "domain": urlparse(url).netloc,
                    "title": soup.title.string if soup.title else ""
                }
            })

    # If no sections found, chunk the whole page
    if not chunks:
        text = main.get_text(separator=' ', strip=True)
        # Split into ~500 word chunks
        words = text.split()
        for i in range(0, len(words), 450):
            chunk_text = ' '.join(words[i:i+500])
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    "type": "webpage",
                    "source": url,
                    "domain": urlparse(url).netloc,
                    "title": soup.title.string if soup.title else ""
                }
            })

    return chunks


async def crawl_site(start_url: str, max_pages: int = 50) -> List[Dict]:
    """Crawl a site and chunk all pages."""
    from urllib.parse import urlparse

    base_domain = urlparse(start_url).netloc
    visited = set()
    to_visit = [start_url]
    all_chunks = []

    async with httpx.AsyncClient() as client:
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue

            try:
                response = await client.get(url, follow_redirects=True)
                visited.add(url)

                # Chunk this page
                all_chunks.extend(chunk_webpage(url))

                # Find links to follow
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = urljoin(url, link['href'])
                    if urlparse(href).netloc == base_domain and href not in visited:
                        to_visit.append(href)

            except Exception as e:
                print(f"Failed to fetch {url}: {e}")

    return all_chunks
```

**Metadata Schema**:
```yaml
type: webpage
source: full URL
domain: domain name
title: page title
crawl_depth: (for crawls) how many links from start
```


### Pattern 6: Research Notes

**When to use**: Personal notes, research findings, learnings

**Chunking Strategy**: By paragraph with topic extraction

```python
from typing import List, Dict
from datetime import datetime

def chunk_research_notes(content: str, topic: str = None) -> List[Dict]:
    """Chunk research notes with topic awareness."""

    # Split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in content.split('

') if p.strip()]

    chunks = []
    current_topic = topic or "general"

    for para in paragraphs:
        # Check if this is a topic header
        if para.startswith('#') or (len(para) < 50 and para.endswith(':')):
            current_topic = para.strip('#: ')
            continue

        chunks.append({
            "content": para,
            "metadata": {
                "type": "research",
                "topic": current_topic,
                "ingested_at": datetime.now().isoformat(),
                "word_count": len(para.split())
            }
        })

    return chunks


def chunk_with_source_attribution(
    content: str,
    source_url: str = None,
    source_title: str = None,
    researcher: str = None
) -> List[Dict]:
    """Chunk research with full source attribution."""

    chunks = chunk_research_notes(content)

    for chunk in chunks:
        chunk["metadata"].update({
            "source_url": source_url,
            "source_title": source_title,
            "researcher": researcher
        })

    return chunks
```

**Metadata Schema**:
```yaml
type: research
topic: extracted or assigned topic
source_url: where the info came from
source_title: title of source
researcher: who did the research
ingested_at: timestamp
word_count: chunk size
```
