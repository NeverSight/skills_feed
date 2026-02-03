---
name: crawl4ai
version: 0.1.0
description: High-performance web crawler skill using Sidecar Execution Pattern
author: Omni Team
routing_keywords:
  - "crawl" # Primary: crawl web pages
  - "scrape" # Secondary: scrape web content
  - "fetch" # Alternative: fetch URL content
  # Removed "web" to avoid over-matching URL queries
execution_mode: subprocess
intents:
  - "Crawl a webpage and extract its content"
  - "Fetch website content as markdown"
  - "Scrape web pages for information"
---
