---
name: scraping
description: Fetches web pages, parses HTML with CSS selectors, calls REST APIs, and scrapes dynamic content. Use when extracting data from websites, querying JSON APIs, or automating browser interactions.
---

# Scraping

Web scraping using nu-shell and browser tools for data extraction.

## Prerequisites

- nu-shell installed (`nu`)
- `query web` plugin installed (for HTML scraping): `nu -c "plugin add query web"`
- Browser extension enabled (for dynamic content): Enable the `browser` extension in your agent configuration

## Common Tasks

### Fetching Web Pages

Use `http get` to retrieve HTML content:

```bash
# Simple GET request
nu -c 'http get https://example.com'

# With headers
nu -c 'http get -H [User-Agent "My Scraper"] https://example.com'
```

### HTML Parsing and Data Extraction

Use the `query web` plugin to parse HTML and extract data using CSS selectors:

```bash
# Extract text from elements
nu -c 'http get https://example.com | query web -q "h1, h2" | str trim'

# Extract attributes
nu -c 'http get https://example.com | query web -a href "a"'

# Parse tables as structured data
nu -c 'http get https://example.com/table-page | query web --as-table ["Column1" "Column2"]'
```

### Browser-Based Scraping for Dynamic Content

For websites requiring JavaScript execution or complex DOM interactions, use browser automation tools.

```bash
# Start browser
start-browser

# Navigate to page
navigate-browser --url https://example.com

# Extract data with JavaScript evaluation
evaluate-javascript --code "Array.from(document.querySelectorAll('selector')).map(e => e.textContent)"

# Screenshot for visual inspection
take-screenshot

# Query HTML fragments
query-html-elements --selector ".content"
```

### API Interactions

For JSON APIs, use `http get` and parse with `from json`:

```bash
# GET JSON API
nu -c 'http get https://api.example.com/data | from json'

# POST requests
nu -c 'http post https://api.example.com/submit -t application/json {key: value}'
```

### Handling Authentication

```bash
# Basic auth
nu -c 'http get -u username:password https://api.example.com'

# Bearer token
nu -c 'http get -H [Authorization "Bearer YOUR_TOKEN"] https://api.example.com'

# Custom headers
nu -c 'http get -H [X-API-Key "YOUR_KEY" User-Agent "Scraper"] https://api.example.com'
```

### Rate Limiting and Delays

```bash
# Add delays between requests
nu -c '$urls | each { |url| http get $url; sleep 1sec }'
```

### Parallel Processing

```bash
# Scrape multiple pages in parallel
nu -c '$urls | par-each { |url| http get $url | query web -q ".data" }'
```

## One-liner Examples

### Basic HTML Scraping

```bash
# Extract all h1 titles
nu -c 'http get https://example.com | query web -q "h1"'

# Get all links
nu -c 'http get https://example.com | query web -a href "a"'

# Scrape product prices
nu -c 'http get https://store.example.com | query web -q ".price"'
```

### HTML Scraping Example: Hacker News

```bash
# Scrape HN front page titles and URLs
nu -c 'http get https://news.ycombinator.com/ | query web -q ".titleline a" | get text | zip (http get https://news.ycombinator.com/ | query web -a href ".titleline a" | get href) | each { |pair| echo $"($pair.0) - ($pair.1)" }'
```

For static sites like HN, use `http get` directly. Reserve browser tools for dynamic content requiring JavaScript execution.

### GitHub Stars Scraper

```bash
# Get star count for a repo
nu -c 'http get https://api.github.com/repos/nushell/nushell | get stargazers_count'
```

### API Data Extraction

```bash
# Fetch JSON and extract fields
nu -c 'http get https://api.example.com/users | from json | get -i 0.name'
```

### API Authentication

```bash
# Bearer token
nu -c 'http get -H [Authorization "Bearer YOUR_TOKEN"] https://api.example.com/data'

# API key
nu -c 'http get -H [X-API-Key "YOUR_API_KEY"] https://api.example.com/data'

# Basic auth
nu -c 'http get -u username:password https://api.example.com/protected'
```

## Related Skills

- **nu-shell**: Core nu-shell scripting patterns and commands.

## Related Tools

- **start-browser**: Start Cromite browser via Puppeteer.
- **navigate-browser**: Navigate to a URL in the browser.
- **evaluate-javascript**: Evaluate JavaScript code in the active browser tab.
- **take-screenshot**: Take a screenshot of the active browser tab.
- **query-html-elements**: Extract HTML elements by CSS selector.
- **list-browser-tabs**: List all open browser tabs with their titles and URLs.
- **close-tab**: Close a browser tab by index or title.
- **switch-tab**: Switch to a specific tab by index.
- **refresh-tab**: Refresh the current tab.
- **current-url**: Get the URL of the current active tab.
- **page-title**: Get the title of the current active tab.
- **wait-for-element**: Wait for a CSS selector to appear on the page.
- **click-element**: Click on an element by CSS selector.
- **type-text**: Type text into an input field.
- **extract-text**: Extract text content from elements by CSS selector.
- **search-web**: Perform web searches and extract information from search results.
