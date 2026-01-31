---
name: site-crawler
description: Crawl and extract content from websites
---


# Site Crawler Skill

> Respectfully crawl documentation sites and web content for RAG ingestion.

## Overview

Documentation sites, blogs, and knowledge bases contain valuable structured content. This skill covers:
- Respectful crawling (robots.txt, rate limiting)
- Structure-preserving extraction
- Incremental updates (only fetch changed pages)
- Sitemap-based discovery

## Prerequisites

```bash
# HTTP client
pip install httpx

# HTML parsing
pip install beautifulsoup4 lxml

# Clean article extraction
pip install trafilatura

# Markdown conversion
pip install markdownify
```

## Crawling Principles

### 1. Be Respectful
- Always check robots.txt
- Rate limit requests (1-2 seconds between)
- Identify yourself with a User-Agent
- Don't overload servers

### 2. Be Efficient
- Use sitemaps when available
- Track what's been crawled
- Only re-fetch changed content
- Skip non-content pages (login, search results)

### 3. Be Smart
- Preserve document structure
- Extract meaningful content only
- Handle pagination
- Detect and follow documentation structure

## Core Implementation

### Robots.txt Handling

```python
#!/usr/bin/env python3
"""Robots.txt compliance."""

from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from typing import Optional
import httpx

class RobotsChecker:
    """Check robots.txt compliance before crawling."""

    def __init__(self, user_agent: str = "ContentHarvester/1.0"):
        self.user_agent = user_agent
        self.parsers: dict = {}

    async def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt."""
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        if base_url not in self.parsers:
            await self._load_robots(base_url)

        parser = self.parsers.get(base_url)
        if parser is None:
            return True  # No robots.txt = allow all

        return parser.can_fetch(self.user_agent, url)

    async def _load_robots(self, base_url: str):
        """Load and parse robots.txt."""
        robots_url = f"{base_url}/robots.txt"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(robots_url, timeout=10)

            if response.status_code == 200:
                parser = RobotFileParser()
                parser.parse(response.text.split("
"))
                self.parsers[base_url] = parser
            else:
                self.parsers[base_url] = None

        except Exception:
            self.parsers[base_url] = None

    def get_crawl_delay(self, base_url: str) -> Optional[float]:
        """Get crawl delay from robots.txt."""
        parser = self.parsers.get(base_url)
        if parser:
            delay = parser.crawl_delay(self.user_agent)
            return delay if delay else None
        return None
```

### Content Extractor

```python
#!/usr/bin/env python3
"""Clean content extraction from HTML."""

from bs4 import BeautifulSoup
import trafilatura
from markdownify import markdownify as md
from typing import Dict, Optional
import re

def extract_content(html: str, url: str) -> Dict:
    """
    Extract clean content from HTML.

    Uses multiple strategies for best results.
    """
    result = {
        "title": "",
        "content": "",
        "markdown": "",
        "headings": [],
        "links": [],
        "metadata": {}
    }

    soup = BeautifulSoup(html, 'lxml')

    # Get title
    title_tag = soup.find('title')
    if title_tag:
        result["title"] = title_tag.get_text().strip()

    # Try trafilatura for clean extraction
    extracted = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
        include_links=True,
        output_format='markdown'
    )

    if extracted:
        result["markdown"] = extracted
        result["content"] = trafilatura.extract(html, output_format='txt') or ""
    else:
        # Fallback to manual extraction
        result["markdown"] = extract_main_content(soup)
        result["content"] = soup.get_text(separator=' ', strip=True)

    # Extract headings for structure
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        result["headings"].append({
            "level": int(heading.name[1]),
            "text": heading.get_text().strip()
        })

    # Extract metadata
    for meta in soup.find_all('meta'):
        name = meta.get('name', meta.get('property', ''))
        content = meta.get('content', '')
        if name and content:
            result["metadata"][name] = content

    # Extract internal links for crawling
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/') or href.startswith(url):
            result["links"].append(href)

    return result


def extract_main_content(soup: BeautifulSoup) -> str:
    """Extract main content area, removing navigation/footer."""
    # Remove unwanted elements
    for tag in soup.find_all(['nav', 'footer', 'aside', 'script', 'style', 'header']):
        tag.decompose()

    # Try to find main content area
    main = (
        soup.find('main') or
        soup.find('article') or
        soup.find('div', class_=re.compile(r'content|main|post|article', re.I)) or
        soup.find('body')
    )

    if main:
        # Convert to markdown
        return md(str(main), heading_style="ATX", strip=['script', 'style'])

    return ""


def extract_docs_structure(html: str, url: str) -> Dict:
    """
    Extract documentation-specific structure.

    Handles common doc frameworks: Docusaurus, MkDocs, Sphinx, GitBook, etc.
    """
    soup = BeautifulSoup(html, 'lxml')

    structure = {
        "title": "",
        "breadcrumbs": [],
        "sidebar_links": [],
        "content": "",
        "prev_page": None,
        "next_page": None
    }

    # Title
    title = soup.find('h1') or soup.find('title')
    if title:
        structure["title"] = title.get_text().strip()

    # Breadcrumbs (common in docs)
    breadcrumb = soup.find(class_=re.compile(r'breadcrumb', re.I))
    if breadcrumb:
        structure["breadcrumbs"] = [
            a.get_text().strip()
            for a in breadcrumb.find_all('a')
        ]

    # Sidebar navigation
    sidebar = soup.find(class_=re.compile(r'sidebar|nav|menu', re.I))
    if sidebar:
        for link in sidebar.find_all('a', href=True):
            structure["sidebar_links"].append({
                "text": link.get_text().strip(),
                "href": link['href']
            })

    # Prev/Next navigation
    prev_link = soup.find('a', class_=re.compile(r'prev', re.I))
    next_link = soup.find('a', class_=re.compile(r'next', re.I))

    if prev_link:
        structure["prev_page"] = prev_link.get('href')
    if next_link:
        structure["next_page"] = next_link.get('href')

    # Main content
    structure["content"] = extract_main_content(soup)

    return structure
```

### Site Crawler

```python
#!/usr/bin/env python3
"""Full site crawler implementation."""

import asyncio
import httpx
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set, Optional
from datetime import datetime
import hashlib
import xml.etree.ElementTree as ET

class SiteCrawler:
    """Crawl a site respectfully and extract content."""

    def __init__(
        self,
        base_url: str,
        user_agent: str = "ContentHarvester/1.0",
        rate_limit: float = 1.0,  # seconds between requests
        max_pages: int = 100
    ):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self.max_pages = max_pages

        self.robots = RobotsChecker(user_agent)
        self.visited: Set[str] = set()
        self.results: List[Dict] = []

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication."""
        # Remove fragments
        url = url.split('#')[0]
        # Remove trailing slash
        url = url.rstrip('/')
        return url

    def _is_same_domain(self, url: str) -> bool:
        """Check if URL is on same domain."""
        return urlparse(url).netloc == self.domain

    def _should_skip(self, url: str) -> bool:
        """Check if URL should be skipped."""
        skip_patterns = [
            '/search', '/login', '/signup', '/auth',
            '/api/', '/_', '/tag/', '/category/',
            '.pdf', '.zip', '.png', '.jpg', '.gif'
        ]
        return any(pattern in url.lower() for pattern in skip_patterns)

    async def get_sitemap_urls(self) -> List[str]:
        """Try to get URLs from sitemap."""
        urls = []
        sitemap_locations = [
            f"{self.base_url}/sitemap.xml",
            f"{self.base_url}/sitemap_index.xml",
        ]

        async with httpx.AsyncClient() as client:
            for sitemap_url in sitemap_locations:
                try:
                    response = await client.get(sitemap_url, timeout=10)
                    if response.status_code == 200:
                        urls.extend(self._parse_sitemap(response.text))
                        break
                except Exception:
                    continue

        return urls

    def _parse_sitemap(self, xml_content: str) -> List[str]:
        """Parse sitemap XML."""
        urls = []
        try:
            root = ET.fromstring(xml_content)
            # Handle namespace
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # Check for sitemap index
            for sitemap in root.findall('.//sm:sitemap/sm:loc', ns):
                # This is an index, would need to fetch sub-sitemaps
                pass

            # Get URLs
            for url in root.findall('.//sm:url/sm:loc', ns):
                if url.text:
                    urls.append(url.text)

        except ET.ParseError:
            pass

        return urls

    async def crawl(
        self,
        start_urls: List[str] = None,
        use_sitemap: bool = True
    ) -> List[Dict]:
        """
        Crawl the site starting from given URLs.

        Args:
            start_urls: URLs to start crawling from
            use_sitemap: Whether to try sitemap first

        Returns:
            List of extracted page contents
        """
        # Initialize URL queue
        to_visit = []

        if use_sitemap:
            sitemap_urls = await self.get_sitemap_urls()
            to_visit.extend(sitemap_urls[:self.max_pages])

        if start_urls:
            to_visit.extend(start_urls)

        if not to_visit:
            to_visit = [self.base_url]

        # Crawl loop
        async with httpx.AsyncClient(
            headers={"User-Agent": self.user_agent},
            follow_redirects=True,
            timeout=30
        ) as client:

            while to_visit and len(self.visited) < self.max_pages:
                url = self._normalize_url(to_visit.pop(0))

                if url in self.visited:
                    continue

                if not self._is_same_domain(url):
                    continue

                if self._should_skip(url):
                    continue

                # Check robots.txt
                if not await self.robots.can_fetch(url):
                    continue

                try:
                    # Rate limit
                    await asyncio.sleep(self.rate_limit)

                    # Fetch page
                    response = await client.get(url)

                    if response.status_code != 200:
                        continue

                    # Skip non-HTML
                    content_type = response.headers.get('content-type', '')
                    if 'text/html' not in content_type:
                        continue

                    self.visited.add(url)

                    # Extract content
                    extracted = extract_content(response.text, url)
                    extracted["url"] = url
                    extracted["fetched_at"] = datetime.now().isoformat()
                    extracted["status_code"] = response.status_code

                    self.results.append(extracted)

                    # Add discovered links to queue
                    for link in extracted.get("links", []):
                        full_url = urljoin(url, link)
                        normalized = self._normalize_url(full_url)
                        if normalized not in self.visited:
                            to_visit.append(normalized)

                except Exception as e:
                    print(f"Error crawling {url}: {e}")
                    continue

        return self.results

    async def crawl_docs(
        self,
        start_url: str = None
    ) -> List[Dict]:
        """
        Crawl documentation site following prev/next links.

        Better for linear documentation structure.
        """
        current_url = start_url or self.base_url

        async with httpx.AsyncClient(
            headers={"User-Agent": self.user_agent},
            follow_redirects=True,
            timeout=30
        ) as client:

            while current_url and len(self.visited) < self.max_pages:
                url = self._normalize_url(current_url)

                if url in self.visited:
                    break

                try:
                    await asyncio.sleep(self.rate_limit)

                    response = await client.get(url)
                    if response.status_code != 200:
                        break

                    self.visited.add(url)

                    # Extract with docs structure
                    extracted = extract_docs_structure(response.text, url)
                    extracted["url"] = url
                    extracted["fetched_at"] = datetime.now().isoformat()

                    self.results.append(extracted)

                    # Follow next link
                    if extracted.get("next_page"):
                        current_url = urljoin(url, extracted["next_page"])
                    else:
                        current_url = None

                except Exception as e:
                    print(f"Error: {e}")
                    break

        return self.results
```

## Full Harvesting Pipeline

```python
#!/usr/bin/env python3
"""Complete site harvesting pipeline."""

from datetime import datetime
from typing import Dict, List
import hashlib

async def harvest_site(
    url: str,
    collection: str,
    max_pages: int = 100,
    crawl_mode: str = "full",  # full, docs, sitemap
    rate_limit: float = 1.0
) -> Dict:
    """
    Harvest a website into RAG.

    Args:
        url: Base URL to crawl
        collection: Target RAG collection
        max_pages: Maximum pages to crawl
        crawl_mode: Crawling strategy
        rate_limit: Seconds between requests
    """
    crawler = SiteCrawler(
        base_url=url,
        rate_limit=rate_limit,
        max_pages=max_pages
    )

    # Crawl based on mode
    if crawl_mode == "docs":
        pages = await crawler.crawl_docs()
    elif crawl_mode == "sitemap":
        pages = await crawler.crawl(use_sitemap=True, start_urls=[])
    else:
        pages = await crawler.crawl(start_urls=[url])

    # Ingest pages
    ingested = 0
    errors = 0

    for page in pages:
        try:
            # Skip empty pages
            content = page.get("markdown") or page.get("content", "")
            if len(content.strip()) < 100:
                continue

            # Generate document ID
            url_hash = hashlib.md5(page["url"].encode()).hexdigest()[:12]
            doc_id = f"web_{url_hash}"

            # Metadata
            metadata = {
                "source_type": "webpage",
                "source_url": page["url"],
                "domain": urlparse(page["url"]).netloc,
                "title": page.get("title", ""),
                "harvested_at": datetime.now().isoformat(),
                "headings": [h["text"] for h in page.get("headings", [])[:5]],
            }

            # Add breadcrumbs if present
            if page.get("breadcrumbs"):
                metadata["breadcrumbs"] = page["breadcrumbs"]
                metadata["section"] = " > ".join(page["breadcrumbs"])

            # Chunk if content is large
            chunks = chunk_content(content, max_size=500)

            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }

                await ingest(
                    content=chunk,
                    collection=collection,
                    metadata=chunk_metadata,
                    doc_id=f"{doc_id}_chunk_{i}"
                )

            ingested += 1

        except Exception as e:
            errors += 1
            print(f"Error ingesting {page.get('url')}: {e}")

    return {
        "status": "success",
        "base_url": url,
        "pages_crawled": len(pages),
        "pages_ingested": ingested,
        "errors": errors,
        "collection": collection
    }


def chunk_content(content: str, max_size: int = 500) -> List[str]:
    """Chunk content by paragraphs."""
    paragraphs = content.split('

')
    chunks = []
    current = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para.split())

        if current_size + para_size > max_size and current:
            chunks.append('

'.join(current))
            current = []
            current_size = 0

        current.append(para)
        current_size += para_size

    if current:
        chunks.append('

'.join(current))

    return chunks
```

## Metadata Schema

```yaml
source_type: webpage
source_url: https://docs.example.com/page
domain: docs.example.com
title: "Page Title"
section: "Getting Started > Installation"
breadcrumbs: ["Getting Started", "Installation"]
headings: ["Overview", "Prerequisites", "Steps"]
chunk_index: 0
total_chunks: 3
harvested_at: "2024-01-01T12:00:00Z"
```

## Usage Examples

```python
# Full site crawl
result = await harvest_site(
    url="https://docs.example.com",
    collection="example_docs",
    max_pages=200,
    crawl_mode="full"
)

# Documentation (follow prev/next)
result = await harvest_site(
    url="https://docs.example.com/getting-started",
    collection="example_docs",
    crawl_mode="docs"
)

# Sitemap-based
result = await harvest_site(
    url="https://blog.example.com",
    collection="blog_posts",
    crawl_mode="sitemap",
    max_pages=50
)
```

## Refinement Notes

> Track improvements as you use this skill.

- [ ] Robots.txt handling tested
- [ ] Rate limiting working
- [ ] Content extraction clean
- [ ] Sitemap parsing working
- [ ] Incremental updates implemented
- [ ] Documentation structure preserved
