---
name: rss-agent-viewer
description: 'AI agent-friendly CLI RSS/Atom feed viewer with discovery, search, and OPML import/export. Use when an agent needs to manage RSS feeds, read articles, or run feed discovery from the terminal. Triggered by: "read RSS feeds", "view RSS", "RSS reader CLI", "rss-viewer", "discover RSS feeds", "import OPML", "search feeds", or "discover-search feeds".'
license: MIT
---

# RSS Agent Viewer

CLI RSS/Atom feed viewer with built-in discovery, caching, and search.

## Quick start

```bash
npx -y rss-agent-viewer init
npx -y rss-agent-viewer discover https://vercel.com
npx -y rss-agent-viewer add https://vercel.com/atom
npx -y rss-agent-viewer read
```

## Core workflow

```bash
# Initialize config + database
rss-viewer init

# Discover feeds for a site
rss-viewer discover https://example.com

# Subscribe to a feed
rss-viewer add https://example.com/feed.xml

# List feeds and read articles
rss-viewer feeds
rss-viewer read
```

## Common commands

```bash
rss-viewer init
rss-viewer add <url>
rss-viewer discover <url>
rss-viewer feeds
rss-viewer remove <url>
rss-viewer read [url]
rss-viewer search <query>
rss-viewer discover-search <query>
rss-viewer import <file>
rss-viewer export
rss-viewer cache <action>
```

## Usage patterns

### Discover and subscribe
```bash
rss-viewer discover https://example.com
rss-viewer add https://example.com/rss.xml
```

### Read a single feed
```bash
rss-viewer read https://example.com/rss.xml
```

### Search across all feeds
```bash
# Local database search (enhanced with full-text search)
rss-viewer search "open source"

# Web search + discovery + add + search in one command
rss-viewer discover-search "Rust programming" --auto-add --read

# Using Exa API (BYOK)
rss-viewer discover-search "AI safety" \
  --provider exa \
  --max-results 5 \
  --auto-add \
  --read
```

### Import OPML
```bash
rss-viewer import feeds.opml
```

### Export feeds
```bash
rss-viewer export
```

## Search Options

### Local Database Search
```bash
rss-viewer search "React 19" --limit 10
rss-viewer search "TypeScript" --author "Dan" --since "2024-01-01"
```

### Web Search with Discovery
```bash
# Use agent's built-in search (default)
rss-viewer discover-search "micro-frontends" --auto-add --read

# Use Exa API (requires EXA_API_KEY)
export EXA_API_KEY="your-api-key"
rss-viewer discover-search "WebGPU" \
  --provider exa \
  --max-results 5 \
  --category Development \
  --auto-add \
  --read \
  --limit 20
```

### Configuration

**Environment Variables:**
```bash
EXA_API_KEY="your-api-key"                    # Exa API key (optional)
RSS_VIEWER_SEARCH_PROVIDER="agent|exa"        # Search provider (default: agent)
RSS_VIEWER_MAX_WEB_RESULTS=10                 # Max web search results
RSS_VIEWER_SEARCH_LIMIT=20                    # Max article results
RSS_VIEWER_BOOST_RECENT=false                # Boost recent articles in search
EXA_API_URL="https://api.exa.ai/search"      # Custom Exa endpoint (optional)
```

**Config File (~/.config/rss-viewer/config.json):**
```json
{
  "webSearchProvider": "exa",
  "exaApiKey": "your-api-key",
  "maxWebResults": 10,
  "searchResultsLimit": 20,
  "boostRecentSearch": false
}
```

## When to use this tool

- Manage and read RSS/Atom feeds from the terminal
- Discover feed URLs from a website
- Search across multiple subscriptions with full-text search
- Discover new feeds from web search queries
- Automate feed discovery and subscription workflow
- Import or export subscriptions via OPML

## More information

- GitHub: https://github.com/brooksy4503/rss-agent-viewer
