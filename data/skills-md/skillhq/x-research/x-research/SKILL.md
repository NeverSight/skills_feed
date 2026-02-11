---
name: x-research
description: >
  General-purpose X/Twitter research agent. Searches X for real-time perspectives,
  dev discussions, product feedback, cultural takes, breaking news, and expert opinions.
  Works like a web research agent but uses X as the source.
  Use when: (1) user says "x research", "search x for", "search twitter for",
  "what are people saying about", "what's twitter saying", "check x for", "x search",
  "/x-research", (2) user is working on something where recent X discourse would provide
  useful context (new library releases, API changes, product launches, cultural events,
  industry drama), (3) user wants to find what devs/experts/community thinks about a topic.
  NOT for: posting tweets, account management, or historical archive searches beyond 7 days.
---

# X Research

General-purpose agentic research over X/Twitter. Decompose any research question into targeted searches, iteratively refine, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

Uses the `bird` CLI for all X/Twitter data access.

## Prerequisites

`bird` must be installed and authenticated:

```bash
# Install
brew install steipete/tap/bird
# or: npm install -g @steipete/bird

# Verify auth
bird check
bird whoami
```

If query IDs go stale (404 errors): `bird query-ids --fresh`

## CLI Reference

### Search

```bash
bird search "<query>" -n <limit>
bird search "<query>" --all --max-pages 3
```

**Search operators** (used inside the query string):
- `from:username` — tweets from a specific user
- `-is:retweet` — exclude retweets
- `-is:reply` — exclude replies
- `has:links` — only tweets with links
- `url:github.com` — tweets linking to a domain
- `OR` — combine terms: `(opus OR claude)`
- `-keyword` — exclude keyword
- `min_faves:N` — minimum likes
- `min_retweets:N` — minimum retweets

**Examples:**
```bash
bird search "BNKR" -n 10
bird search "from:frankdegods" -n 20
bird search "(opus 4.6 OR claude) trading" --max-pages 2
bird search "$BNKR (revenue OR fees) min_faves:5"
bird search "AI agents -is:retweet -is:reply has:links" -n 15
bird search "from:steipete" --all --max-pages 3
```

### Profile / User Tweets

```bash
bird user-tweets @handle -n 20        # User's recent tweets
bird about @handle                     # Account origin/location info
```

### Thread

```bash
bird thread <url-or-id>               # Full conversation thread
```

### Single Tweet

```bash
bird read <url-or-id>                 # Read a single tweet
bird <url-or-id>                      # Shorthand
```

### Replies

```bash
bird replies <url-or-id>              # List replies to a tweet
bird replies <id> --all --delay 1000  # Paginate all replies
```

### Mentions

```bash
bird mentions                         # Tweets mentioning you
bird mentions --user @handle          # Mentions of another user
```

### Output Modes

```bash
--json          # JSON output (useful for programmatic processing)
--plain         # No emoji, no color (script-friendly)
```

## Research Loop (Agentic)

When doing deep research (not just a quick search), follow this loop:

### 1. Decompose the Question into Queries

Turn the research question into 3-5 keyword queries using X search operators:

- **Core query**: Direct keywords for the topic
- **Expert voices**: `from:` specific known experts
- **Pain points**: Keywords like `(broken OR bug OR issue OR migration)`
- **Positive signal**: Keywords like `(shipped OR love OR fast OR benchmark)`
- **Links**: `url:github.com` or `url:` specific domains
- **Noise reduction**: Add `-is:retweet -is:reply` for cleaner results
- **Crypto spam**: Add `-airdrop -giveaway -whitelist` if crypto topics flooding

### 2. Search and Extract

Run each query via `bird search`. After each, assess:
- Signal or noise? Adjust operators.
- Key voices worth searching `from:` specifically?
- Threads worth following via `bird thread`?
- Linked resources worth deep-diving with `web_fetch`?

### 3. Follow Threads

When a tweet has high engagement or is a thread starter:
```bash
bird thread <url-or-id>
```

### 4. Deep-Dive Linked Content

When tweets link to GitHub repos, blog posts, or docs, fetch with `web_fetch`. Prioritize links that:
- Multiple tweets reference
- Come from high-engagement tweets
- Point to technical resources directly relevant to the question

### 5. Synthesize

Group findings by theme, not by query:

```
### [Theme/Finding Title]

[1-2 sentence summary]

- @username: "[key quote]" (NL, NI) [Tweet](url)
- @username2: "[another perspective]" (NL, NI) [Tweet](url)

Resources shared:
- [Resource title](url) -- [what it is]
```

### 6. Save

Save research output to `~/clawd/drafts/x-research-{topic-slug}-{YYYY-MM-DD}.md`.

## Refinement Heuristics

- **Too much noise?** Add `-is:reply`, use `min_faves:N`, narrow keywords
- **Too few results?** Broaden with `OR`, remove restrictive operators, increase `--max-pages`
- **Crypto spam?** Add `-$ -airdrop -giveaway -whitelist`
- **Expert takes only?** Use `from:` or `min_faves:50`
- **Substance over hot takes?** Search with `has:links`

## Watchlist (Manual)

Maintain a list of key accounts to periodically check:

```bash
bird user-tweets @account1 -n 5
bird user-tweets @account2 -n 5
```

Store your watchlist in `data/watchlist.md` and run through it when doing periodic checks.

## File Structure

```
x-research-skill/
├── SKILL.md           (this file)
└── data/
    └── watchlist.md   (accounts to monitor)
```
