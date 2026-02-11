---
name: supalytics
description: Query web analytics data using the Supalytics CLI. Use when the user wants to check pageviews, visitors, top pages, traffic sources, referrers, countries, revenue metrics, conversions, funnels, events, or realtime visitors.
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["supalytics"]},"homepage":"https://supalytics.co"}}
---

# Supalytics CLI

Query web analytics data from [Supalytics](https://supalytics.co) - simple, fast, GDPR-compliant analytics with revenue attribution.

## Installation

**Requires [Bun](https://bun.sh) runtime** (not Node.js):

```bash
# Install Bun first
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"

# Install Supalytics CLI
bun add -g @supalytics/cli
```

## Authentication

### Important: OAuth in Agent Contexts

The `supalytics login` command uses OAuth device flow which requires user interaction in a browser. In agent contexts (OpenClaw, etc.), the process may be killed before OAuth completes.

**Solution for OpenClaw:** Use `background: true` mode:

```javascript
await exec({
  command: 'supalytics login',
  background: true,
  yieldMs: 2000  // Wait 2s to capture the verification URL
});
```

The agent should:
1. Run login in background mode
2. Extract and present the verification URL to the user
3. Wait for user to complete browser authorization
4. Poll background session to check completion

### Quick Setup

```bash
supalytics init    # Opens browser, creates site, shows tracking snippet
```

### Manual Setup

```bash
supalytics login        # Opens browser for OAuth
supalytics sites add    # Create a new site
```

## Commands

### Quick Stats

```bash
supalytics stats                # Last 30 days (default)
supalytics stats -p today       # Today only
supalytics stats -p yesterday   # Yesterday
supalytics stats -p week        # This week
supalytics stats -p month       # This month
supalytics stats -p 7d          # Last 7 days
supalytics stats -p 5d          # Any arbitrary days
supalytics stats -p 2mo         # Any arbitrary months
supalytics stats -p all         # All time
supalytics stats --all          # Include breakdowns (pages, referrers, countries, etc.)
supalytics stats --start 2026-01-01 --end 2026-01-31  # Explicit date range
```

### Realtime Visitors

```bash
supalytics realtime           # Current visitors on site
supalytics realtime --watch   # Auto-refresh every 30s
```

### Trend (Time Series)

```bash
supalytics trend              # Daily visitor trend with bar chart
supalytics trend --period 7d  # Last 7 days
supalytics trend --compact    # Sparkline only
```

### Breakdowns

```bash
supalytics pages              # Top pages by visitors
supalytics referrers          # Top referrers
supalytics countries          # Traffic by country
```

### Annotations

```bash
supalytics annotations                    # List annotations (last 30 days)
supalytics annotations -p 90d             # Annotations from last 90 days
supalytics annotations -p all             # All annotations
supalytics annotations add 2026-01-15 "Launched v2.0"                          # Add annotation
supalytics annotations add 2026-01-15 "Launched v2.0" -d "Major redesign"      # With description
supalytics annotations remove <id>        # Remove an annotation
```

### Funnels

```bash
supalytics funnels                         # List all funnels
supalytics funnels <id>                    # View funnel with conversion analysis
supalytics funnels <id> -p 90d             # View with custom period
supalytics funnels <id> --start 2026-01-01 --end 2026-01-31  # Explicit date range

# Create a funnel with steps (page paths, events, or "purchase")
supalytics funnels create "Signup Flow" --step "page:/pricing" --step "event:signup_clicked" --step "purchase"

# Page matching with starts_with
supalytics funnels create "Blog to Signup" --step "page:starts_with:/blog" --step "page:/signup" --step "event:account_created"

# Ordered funnel (steps must happen in sequence)
supalytics funnels create "Checkout" --mode ordered --step "page:/cart" --step "page:/checkout" --step "purchase"

# Update funnel
supalytics funnels update <id> --name "New Name"
supalytics funnels update <id> --step "page:/pricing" --step "purchase"
```

### Events

```bash
supalytics events                          # List all custom events
supalytics events signup                   # Properties for specific event
supalytics events signup --property plan   # Breakdown by property value
supalytics events -p 7d                    # Events from last 7 days
supalytics events --start 2026-01-01 --end 2026-01-31  # Explicit date range
```

### Custom Queries

The `query` command is the most flexible:

```bash
# Top pages with revenue
supalytics query -d page -m visitors,revenue

# Traffic by country and device
supalytics query -d country,device -m visitors

# Blog traffic from US only
supalytics query -d page -f "page:contains:/blog" -f "country:is:US"

# Hourly breakdown
supalytics query -d hour -m visitors -p 7d

# UTM campaign performance
supalytics query -d utm_source,utm_campaign -m visitors,revenue

# Sort by revenue descending
supalytics query -d page --sort revenue:desc

# Pages visited by users who signed up
supalytics query -d page -f "event:is:signup"

# Filter by event property
supalytics query -d country -f "event_property:is:plan:premium"
```

**Available metrics:** `visitors`, `pageviews`, `bounce_rate`, `avg_session_duration`, `revenue`, `conversions`, `conversion_rate`

**Available dimensions:** `page`, `referrer`, `country`, `region`, `city`, `browser`, `os`, `device`, `date`, `hour`, `event`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`

### Site Management

```bash
supalytics sites                              # List all sites
supalytics sites add example.com              # Create site
supalytics sites update my-site -d example.com  # Update domain
supalytics default example.com                # Set default site
supalytics remove example.com                 # Remove site
```

## Global Options

All analytics commands support:

| Option | Description |
|--------|-------------|
| `-s, --site <domain>` | Query specific site (otherwise uses default) |
| `-p, --period <period>` | Time period: `today`, `yesterday`, `week`, `month`, `7d`, `30d`, `90d`, `3mo`, `12mo`, `all` (any `Nd` or `Nmo` works) |
| `--start <date>` | Start date (YYYY-MM-DD) |
| `--end <date>` | End date (YYYY-MM-DD) |
| `-f, --filter <filter>` | Filter: `field:operator:value` |
| `--json` | Output raw JSON (for programmatic use) |
| `--no-revenue` | Exclude revenue metrics |
| `-t, --test` | Query localhost/test data |

## Filter Syntax

Format: `field:operator:value`

**Operators:** `is`, `is_not`, `contains`, `not_contains`, `starts_with`

**Examples:**
```bash
-f "country:is:US"
-f "page:contains:/blog"
-f "device:is:mobile"
-f "referrer:is:twitter.com"
-f "utm_source:is:newsletter"
-f "event:is:signup"
-f "event_property:is:plan:premium"
```

## Output Formats

**Human-readable (default):** Formatted tables with colors

**JSON (`--json`):** Raw JSON for parsing - use this when you need to process the data programmatically:

```bash
supalytics stats --json | jq '.data[0].metrics.visitors'
supalytics query -d page -m visitors --json
```

## Examples by Use Case

### "How's my site doing?"
```bash
supalytics stats
```

### "What are my top traffic sources?"
```bash
supalytics referrers
# or with revenue
supalytics query -d referrer -m visitors,revenue
```

### "Which pages generate the most revenue?"
```bash
supalytics query -d page -m revenue --sort revenue:desc
```

### "How's my newsletter campaign performing?"
```bash
supalytics query -d utm_campaign -f "utm_source:is:newsletter" -m visitors,conversions,revenue
```

### "Who's on my site right now?"
```bash
supalytics realtime
```

### "Show me the visitor trend this week"
```bash
supalytics trend -p 7d
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: supalytics` | Ensure Bun is installed and `~/.bun/bin` is in PATH, or symlink to system path (see below) |
| `No site specified` | Run `supalytics default <domain>` to set default site |
| `Unauthorized` | Run `supalytics login` to re-authenticate |
| No data returned | Check site has tracking installed, try `-t` for test mode |

### OpenClaw / Daemon Usage

Bun installs to `~/.bun/bin` which isn't in PATH for daemon processes like OpenClaw. After installation, symlink to system path:

```bash
sudo ln -sf ~/.bun/bin/bun /usr/local/bin/bun
sudo ln -sf ~/.bun/bin/supalytics /usr/local/bin/supalytics
```
