---
name: ddgr
description: Search the web using DuckDuckGo via the ddgr CLI tool. Use when the user asks to search the web, look something up online, find information on the internet, get instant answers, or needs current/real-time data. Also use for DuckDuckGo Bang searches (e.g., "!w" for Wikipedia, "!so" for StackOverflow).
license: MIT
metadata:
  author: ysm-dev
  version: "1.0.1"
---

# ddgr Web Search

Search DuckDuckGo from the terminal using [ddgr](https://github.com/jarun/ddgr).

## When to Use

- User asks to search the web or look something up
- Need current/real-time information not in training data
- User wants to find documentation, tutorials, or resources
- DuckDuckGo Bang searches (Wikipedia, StackOverflow, GitHub, etc.)

## Prerequisites

ddgr must be installed: `brew install ddgr` or `pip install ddgr`

## Basic Usage

```bash
ddgr --noua --np --json "search query"
```

**Required flags:**
- `--noua`: Disable user agent (always use this)
- `--np` (noprompt): Exit after showing results, no interactive prompt
- `--json`: Output in JSON format for parsing (implies --np)

## Options

| Flag | Description |
|------|-------------|
| `-n N` | Number of results (0-25, default 10) |
| `-t SPAN` | Time filter: `d` (day), `w` (week), `m` (month), `y` (year) |
| `-w SITE` | Search within a specific site |
| `-r REG` | Region-specific search (e.g., `us-en`, `uk-en`, `in-en`) |
| `-x` | Show full URLs instead of domain only |
| `-j` | "I'm Feeling Ducky" - open first result in browser |
| `-i` | Retrieve instant answer only |
| `--unsafe` | Disable safe search |
| `--rev` | List results in reversed order |
| `-p URI` | HTTPS proxy (also reads `https_proxy` env var) |

## DuckDuckGo Bangs

Bangs redirect searches to other sites. Escape `!` in bash/zsh:

```bash
ddgr --noua --np \!w "search term"      # Wikipedia
ddgr --noua --np \!so "python error"    # StackOverflow  
ddgr --noua --np \!gh "repo name"       # GitHub
ddgr --noua --np \!yt "video topic"     # YouTube
ddgr --noua --np \!a "product"          # Amazon
```

Full bang list: https://duckduckgo.com/bang

## Search Keywords

```bash
ddgr --noua --np --json "filetype:pdf annual report"
ddgr --noua --np --json "site:reddit.com python tips"
```

## Examples

**Basic search:**
```bash
ddgr --noua --np --json "python asyncio tutorial"
```

**Recent results (last week):**
```bash
ddgr --noua --np --json -t w "latest news topic"
```

**Site-specific search:**
```bash
ddgr --noua --np --json -w stackoverflow.com "parse JSON"
```

**Region-specific (India, English):**
```bash
ddgr --noua --np --json -r in-en "IPL cricket"
```

**Instant answer:**
```bash
ddgr --noua --np -i "weather new york"
```

**Limit to 5 results:**
```bash
ddgr --noua --np --json -n 5 "quick query"
```

## JSON Output Structure

Each result contains:
- `title`: Page title
- `url`: Full URL
- `abstract`: Description/snippet

Parse with `jq`:
```bash
ddgr --noua --np --json "query" | jq '.[].title'
ddgr --noua --np --json "query" | jq -r '.[0].url'  # First result URL
```
