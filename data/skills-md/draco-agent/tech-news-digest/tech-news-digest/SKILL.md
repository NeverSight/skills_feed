---
name: tech-news-digest
description: Generate tech news digests with unified source model, quality scoring, and multi-format output. Five-layer data collection from RSS feeds, Twitter/X KOLs, GitHub releases, Reddit, and web search. Pipeline-based scripts with retry mechanisms and deduplication. Supports Discord, email, and markdown templates.
version: "3.6.0"
homepage: https://github.com/draco-agent/tech-news-digest
source: https://github.com/draco-agent/tech-news-digest
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalBins: ["mail", "msmtp", "gog", "gh", "openssl"]
env:
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key for web search layer
  - name: GITHUB_TOKEN
    required: false
    description: GitHub token for higher API rate limits (auto-generated from GitHub App if not set)
  - name: GH_APP_ID
    required: false
    description: GitHub App ID for automatic installation token generation
  - name: GH_APP_INSTALL_ID
    required: false
    description: GitHub App Installation ID for automatic token generation
  - name: GH_APP_KEY_FILE
    required: false
    description: Path to GitHub App private key PEM file
tools:
  - python3: Required. Runs data collection and merge scripts.
  - mail: Optional. msmtp-based mail command for email delivery (preferred).
  - gog: Optional. Gmail CLI for email delivery (fallback if mail not available).
files:
  read:
    - config/defaults/: Default source and topic configurations
    - references/: Prompt templates and output templates
    - scripts/: Python pipeline scripts
    - <workspace>/archive/tech-news-digest/: Previous digests for dedup
  write:
    - /tmp/td-*.json: Temporary pipeline intermediate outputs
    - /tmp/td-email.html: Temporary email HTML body
    - <workspace>/archive/tech-news-digest/: Saved digest archives
---

# Tech News Digest

Automated tech news digest system with unified data source model, quality scoring pipeline, and template-based output generation.

## Quick Start

1. **Configuration Setup**: Default configs are in `config/defaults/`. Copy to workspace for customization:
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/
   cp config/defaults/topics.json workspace/config/
   ```

2. **Environment Variables**: 
   - `X_BEARER_TOKEN` - Twitter API bearer token (optional)
   - `BRAVE_API_KEY` - Brave Search API key (optional)
   - `GITHUB_TOKEN` - GitHub personal access token (optional, improves rate limits)

3. **Generate Digest**:
   ```bash
   # Unified pipeline (recommended) — runs all 5 sources in parallel + merge
   python3 scripts/run-pipeline.py \
     --defaults config/defaults \
     --config workspace/config \
     --hours 48 --freshness pd \
     --archive-dir workspace/archive/tech-news-digest/ \
     --output /tmp/td-merged.json --verbose --force
   ```

4. **Use Templates**: Apply Discord, email, or markdown templates to merged output

## Configuration Files

### `sources.json` - Unified Data Sources
```json
{
  "sources": [
    {
      "id": "openai-rss",
      "type": "rss",
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "ai-agent"],
      "note": "Official OpenAI updates"
    },
    {
      "id": "sama-twitter",
      "type": "twitter", 
      "name": "Sam Altman",
      "handle": "sama",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "frontier-tech"],
      "note": "OpenAI CEO"
    }
  ]
}
```

### `topics.json` - Enhanced Topic Definitions
```json
{
  "topics": [
    {
      "id": "llm",
      "emoji": "🧠",
      "label": "LLM / Large Models",
      "description": "Large Language Models, foundation models, breakthroughs",
      "search": {
        "queries": ["LLM latest news", "large language model breakthroughs"],
        "must_include": ["LLM", "large language model", "foundation model"],
        "exclude": ["tutorial", "beginner guide"]
      },
      "display": {
        "max_items": 8,
        "style": "detailed"
      }
    }
  ]
}
```

## Scripts Pipeline

### `run-pipeline.py` - Unified Pipeline (Recommended)
```bash
python3 scripts/run-pipeline.py \
  --defaults config/defaults [--config CONFIG_DIR] \
  --hours 48 --freshness pd \
  --archive-dir workspace/archive/tech-news-digest/ \
  --output /tmp/td-merged.json --verbose --force
```
- **Features**: Runs all 5 fetch steps in parallel, then merges + deduplicates + scores
- **Output**: Final merged JSON ready for report generation (~30s total)
- **Metadata**: Saves per-step timing and counts to `*.meta.json`
- **GitHub Auth**: Auto-generates GitHub App token if `$GITHUB_TOKEN` not set
- **Fallback**: If this fails, run individual scripts below

### Individual Scripts (Fallback)

#### `fetch-rss.py` - RSS Feed Fetcher
```bash
python3 scripts/fetch-rss.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE] [--verbose]
```
- Parallel fetching (10 workers), retry with backoff, feedparser + regex fallback
- Timeout: 30s per feed, ETag/Last-Modified caching

#### `fetch-twitter.py` - Twitter/X KOL Monitor  
```bash
python3 scripts/fetch-twitter.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE]
```
- Requires `X_BEARER_TOKEN`, rate limit handling, engagement metrics

#### `fetch-web.py` - Web Search Engine
```bash
python3 scripts/fetch-web.py [--defaults DIR] [--config DIR] [--freshness pd] [--output FILE]
```
- Auto-detects Brave API rate limit: paid plans → parallel queries, free → sequential
- Without API: generates search interface for agents

#### `fetch-github.py` - GitHub Releases Monitor
```bash
python3 scripts/fetch-github.py [--defaults DIR] [--config DIR] [--hours 168] [--output FILE]
```
- Parallel fetching (10 workers), 30s timeout
- Auth priority: `$GITHUB_TOKEN` → GitHub App auto-generate → `gh` CLI → unauthenticated (60 req/hr)

#### `fetch-reddit.py` - Reddit Posts Fetcher
```bash
python3 scripts/fetch-reddit.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE]
```
- Parallel fetching (4 workers), public JSON API (no auth required)
- 13 subreddits with score filtering

#### `merge-sources.py` - Quality Scoring & Deduplication
```bash
python3 scripts/merge-sources.py --rss FILE --twitter FILE --web FILE --github FILE --reddit FILE
```
- Quality scoring, title similarity dedup (85%), previous digest penalty
- Output: topic-grouped articles sorted by score

#### `validate-config.py` - Configuration Validator
```bash
python3 scripts/validate-config.py [--defaults DIR] [--config DIR] [--verbose]
```
- JSON schema validation, topic reference checks, duplicate ID detection

## User Customization

### Workspace Configuration Override
Place custom configs in `workspace/config/` to override defaults:

- **Sources**: Append new sources, disable defaults with `"enabled": false`
- **Topics**: Override topic definitions, search queries, display settings
- **Merge Logic**: 
  - Sources with same `id` → user version takes precedence
  - Sources with new `id` → appended to defaults
  - Topics with same `id` → user version completely replaces default

### Example Workspace Override
```json
// workspace/config/sources.json
{
  "sources": [
    {
      "id": "simonwillison-rss",
      "enabled": false,
      "note": "Disabled: too noisy for my use case"
    },
    {
      "id": "my-custom-blog", 
      "type": "rss",
      "name": "My Custom Tech Blog",
      "url": "https://myblog.com/rss",
      "enabled": true,
      "priority": true,
      "topics": ["frontier-tech"]
    }
  ]
}
```

## Templates & Output

### Discord Template (`references/templates/discord.md`)
- Bullet list format with link suppression (`<link>`)
- Mobile-optimized, emoji headers
- 2000 character limit awareness

### Email Template (`references/templates/email.md`) 
- Rich metadata, technical stats, archive links
- Executive summary, top articles section
- HTML-compatible formatting

### Markdown Template (`references/templates/markdown.md`)
- GitHub-compatible tables and formatting
- Technical details section
- Expandable sections support

## Default Sources (133 total)

- **RSS Feeds (49)**: AI labs, tech blogs, crypto news, Chinese tech media
- **Twitter/X KOLs (49)**: AI researchers, crypto leaders, tech executives
- **GitHub Repos (22)**: Major open-source projects (LangChain, vLLM, DeepSeek, Llama, etc.)
- **Reddit (13)**: r/MachineLearning, r/LocalLLaMA, r/CryptoCurrency, r/ChatGPT, r/OpenAI, etc.
- **Web Search (4 topics)**: LLM, AI Agent, Crypto, Frontier Tech

All sources pre-configured with appropriate topic tags and priority levels.

## Dependencies

```bash
pip install -r requirements.txt
```

**Optional but Recommended**:
- `feedparser>=6.0.0` - Better RSS parsing (fallback to regex if unavailable)
- `jsonschema>=4.0.0` - Configuration validation

**All scripts work with Python 3.8+ standard library only.**

## Monitoring & Operations

### Health Checks
```bash
# Validate configuration
python3 scripts/validate-config.py --verbose

# Test RSS feeds
python3 scripts/fetch-rss.py --hours 1 --verbose

# Check Twitter API
python3 scripts/fetch-twitter.py --hours 1 --verbose
```

### Archive Management
- Digests automatically archived to `<workspace>/archive/tech-news-digest/`
- Previous digest titles used for duplicate detection
- Old archives cleaned automatically (90+ days)

### Error Handling
- **Network Failures**: Retry with exponential backoff
- **Rate Limits**: Automatic retry with appropriate delays
- **Invalid Content**: Graceful degradation, detailed logging
- **Configuration Errors**: Schema validation with helpful messages

## API Keys & Environment

Set in `~/.zshenv` or similar:
```bash
export X_BEARER_TOKEN="your_twitter_bearer_token"
export BRAVE_API_KEY="your_brave_search_api_key"  # Optional
```

- **Twitter**: Read-only bearer token, pay-per-use pricing
- **Brave Search**: Optional, fallback to agent web_search if unavailable

## Cron / Scheduled Task Integration

### OpenClaw Cron (Recommended)

The cron prompt should **NOT** hardcode the pipeline steps. Instead, reference `references/digest-prompt.md` and only pass configuration parameters. This ensures the pipeline logic stays in the skill repo and is consistent across all installations.

#### Daily Digest Cron Prompt
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a daily digest.

Replace placeholders with:
- MODE = daily
- TIME_WINDOW = past 1-2 days
- FRESHNESS = pd
- RSS_HOURS = 48
- ITEMS_PER_SECTION = 3-5
- BLOG_PICKS_COUNT = 2-3
- EXTRA_SECTIONS = (none)
- SUBJECT = Daily Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### Weekly Digest Cron Prompt
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a weekly digest.

Replace placeholders with:
- MODE = weekly
- TIME_WINDOW = past 7 days
- FRESHNESS = pw
- RSS_HOURS = 168
- ITEMS_PER_SECTION = 5-8
- BLOG_PICKS_COUNT = 3-5
- EXTRA_SECTIONS = 📊 Weekly Trend Summary (2-3 sentences summarizing macro trends)
- SUBJECT = Weekly Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### Why This Pattern?
- **Single source of truth**: Pipeline logic lives in `digest-prompt.md`, not scattered across cron configs
- **Portable**: Same skill on different OpenClaw instances, just change paths and channel IDs
- **Maintainable**: Update the skill → all cron jobs pick up changes automatically
- **Anti-pattern**: Do NOT copy pipeline steps into the cron prompt — it will drift out of sync

#### Multi-Channel Delivery Limitation
OpenClaw enforces **cross-provider isolation**: a single session can only send messages to one provider (e.g., Discord OR Telegram, not both). If you need to deliver digests to multiple platforms, create **separate cron jobs** for each provider:

```
# Job 1: Discord + Email
- DISCORD_CHANNEL_ID = <your-discord-channel-id>
- EMAIL = user@example.com
- TEMPLATE = discord

# Job 2: Telegram DM
- DISCORD_CHANNEL_ID = (none)
- EMAIL = (none)
- TEMPLATE = telegram
```
Replace `DISCORD_CHANNEL_ID` delivery with Telegram delivery in the second job's prompt (use `message` tool with `channel=telegram`).

This is a security feature, not a bug — it prevents accidental cross-context data leakage.

## Security Notes

### Execution Model
This skill uses a **prompt template pattern**: the agent reads `digest-prompt.md` and follows its instructions. This is the standard OpenClaw skill execution model — the agent interprets structured instructions from skill-provided files. All instructions are shipped with the skill bundle and can be audited before installation.

### Network Access
The Python scripts make outbound requests to:
- RSS feed URLs (configured in `sources.json`)
- Twitter/X API (`api.x.com`)
- Brave Search API (`api.search.brave.com`)
- GitHub API (`api.github.com`)

No data is sent to any other endpoints. All API keys are read from environment variables declared in the skill metadata.

### Shell Safety
Email delivery supports two CLIs: `mail` (msmtp) and `gog` (fallback). Both use hardcoded subject formats (`Daily Tech Digest - YYYY-MM-DD`) and read HTML body from a temp file (`/tmp/td-email.html`). The prompt template explicitly prohibits interpolating untrusted content (article titles, tweet text, etc.) into shell arguments. Email addresses and subjects must be static placeholder values only.

### File Access
Scripts read from `config/` and write to `workspace/archive/`. No files outside the workspace are accessed.

## Support & Troubleshooting

### Common Issues
1. **RSS feeds failing**: Check network connectivity, use `--verbose` for details
2. **Twitter rate limits**: Reduce sources or increase interval
3. **Configuration errors**: Run `validate-config.py` for specific issues
4. **No articles found**: Check time window (`--hours`) and source enablement

### Debug Mode
All scripts support `--verbose` flag for detailed logging and troubleshooting.

### Performance Tuning
- **Parallel Workers**: Adjust `MAX_WORKERS` in scripts for your system
- **Timeout Settings**: Increase `TIMEOUT` for slow networks
- **Article Limits**: Adjust `MAX_ARTICLES_PER_FEED` based on needs
## Security Considerations

### Shell Execution
The digest prompt instructs agents to run Python scripts via shell commands. All script paths and arguments are skill-defined constants — no user input is interpolated into commands. Two scripts use `subprocess`:
- `run-pipeline.py` orchestrates child fetch scripts (all within `scripts/` directory)
- `fetch-github.py` has two subprocess calls:
  1. `openssl dgst -sha256 -sign` for JWT signing (only if `GH_APP_*` env vars are set — signs a self-constructed JWT payload, no user content involved)
  2. `gh auth token` CLI fallback (only if `gh` is installed — reads from gh's own credential store)

No user-supplied or fetched content is ever interpolated into subprocess arguments. Email delivery writes HTML to a temp file (`/tmp/td-email.html`) before passing to `mail` (msmtp) or `gog` CLI via stdin redirection or `--body-html-file`, avoiding shell interpolation. Email subjects are static format strings only — never constructed from fetched data.

### Credential & File Access
Scripts do **not** directly read `~/.config/`, `~/.ssh/`, or any credential files. All API tokens are read from environment variables declared in the skill metadata. The GitHub auth cascade is:
1. `$GITHUB_TOKEN` env var (you control what to provide)
2. GitHub App token generation (only if you set `GH_APP_ID`, `GH_APP_INSTALL_ID`, and `GH_APP_KEY_FILE` — uses inline JWT signing via `openssl` CLI, no external scripts involved)
3. `gh auth token` CLI (delegates to gh's own secure credential store)
4. Unauthenticated (60 req/hr, safe fallback)

If you prefer no automatic credential discovery, simply set `$GITHUB_TOKEN` and the script will use it directly without attempting steps 2-3.

### Dependency Installation
This skill does **not** install any packages. `requirements.txt` lists optional dependencies (`feedparser`, `jsonschema`) for reference only. All scripts work with Python 3.8+ standard library. Users should install optional deps in a virtualenv if desired — the skill never runs `pip install`.

### Input Sanitization
- URL resolution rejects non-HTTP(S) schemes (javascript:, data:, etc.)
- RSS fallback parsing uses simple, non-backtracking regex patterns (no ReDoS risk)
- All fetched content is treated as untrusted data for display only

### Network Access
Scripts make outbound HTTP requests to configured RSS feeds, Twitter API, GitHub API, Reddit JSON API, and Brave Search API. No inbound connections or listeners are created.
