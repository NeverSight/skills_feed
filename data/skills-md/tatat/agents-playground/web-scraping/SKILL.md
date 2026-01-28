---
name: web-scraping
description: Extract structured data from web pages using CSS selectors and XPath
---

# Web Scraping

Extract structured data from web pages.

## Capabilities

- Fetch HTML content from URLs
- Parse and extract specific elements (tables, lists, text)
- Handle pagination
- Output in JSON or CSV format

## Supported Selectors

- CSS selectors: `.class`, `#id`, `tag`
- XPath expressions
- Text patterns (regex)

## Rate Limiting

Always respect robots.txt and implement delays between requests.
Default delay: 1 second between requests.

## Example

```
Scrape product names and prices from example.com/products
Output as JSON with fields: name, price, url
```
