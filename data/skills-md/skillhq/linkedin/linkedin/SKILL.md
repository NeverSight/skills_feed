---
name: linkedin
description: LinkedIn integration for reading feed, profiles, connections, search results, and messages using browser automation
version: 0.2.0
tools: [Bash, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find]
alwaysApply: false
---

# LinkedIn Skill

Access LinkedIn data through browser automation. This approach is reliable because it uses your actual browser session, avoiding LinkedIn's aggressive bot detection that blocks API-only traffic.

## Setup Requirements

### Chrome Profile Setup (One-Time)

1. **Create a dedicated Chrome profile for automation:**
   - Open Chrome → click your profile icon (top right) → "Add"
   - Name it something memorable (e.g., "Claude" or "Automation")
   - This keeps automation separate from personal browsing

2. **In your automation profile:**
   - Log into LinkedIn (www.linkedin.com)
   - Install the Claude browser extension from https://claude.ai/chrome
   - Keep this Chrome window open when using LinkedIn commands

3. **Before using LinkedIn commands:**
   - Ensure Chrome is open with your automation profile
   - The Claude browser extension must be connected

## Browser Automation Commands

When the user asks for LinkedIn data, use the claude-in-chrome tools to navigate and extract information.

### Connecting to Chrome

Always start by checking the browser connection:

```
1. Call mcp__claude-in-chrome__tabs_context_mcp with createIfEmpty: true
2. If not connected, ask user to open Chrome with their automation profile
3. Create a new tab or use existing one
```

### Reading Feed

When user asks to see their LinkedIn feed:

```
1. Navigate to https://www.linkedin.com/feed/
2. Use read_page to extract feed content
3. Parse and format the feed items
```

Example flow:
1. `mcp__claude-in-chrome__navigate` to `https://www.linkedin.com/feed/`
2. `mcp__claude-in-chrome__read_page` with filter: "all" to get post content
3. Extract post authors, content, engagement metrics from the accessibility tree

### Viewing Profiles

When user asks about a LinkedIn profile:

```
1. Navigate to https://www.linkedin.com/in/{username}/
2. Use read_page to extract profile information
3. Parse name, headline, about, experience, etc.
```

### Searching

When user wants to search LinkedIn:

```
People:    https://www.linkedin.com/search/results/people/?keywords={query}
Jobs:      https://www.linkedin.com/search/results/jobs/?keywords={query}
Companies: https://www.linkedin.com/search/results/companies/?keywords={query}
Posts:     https://www.linkedin.com/search/results/content/?keywords={query}
```

### Reading Messages

When user wants to check messages:

```
1. Navigate to https://www.linkedin.com/messaging/
2. Use read_page to extract conversation list
3. Click on a conversation to read messages
```

## Data Extraction Patterns

### Feed Posts
Look for these patterns in the accessibility tree:
- Post author: Links with profile URLs
- Post content: Text nodes within post containers
- Engagement: Like/comment/share counts
- Timestamps: Relative time indicators

### Profile Data
Navigate to profile and extract:
- Name and headline from main header
- About section text
- Experience entries (company, title, duration)
- Education entries
- Skills section

### Search Results
Parse result items containing:
- Name/title link
- Subtitle (headline, location)
- Connection degree
- Profile picture

## Example Interactions

### "Show my LinkedIn feed"
```
1. Connect to Chrome: tabs_context_mcp
2. Navigate: navigate to linkedin.com/feed/
3. Wait for load: computer action=wait duration=2
4. Read content: read_page with depth=10
5. Parse and summarize top posts
```

### "Look up John Smith on LinkedIn"
```
1. Connect to Chrome: tabs_context_mcp
2. Navigate: navigate to linkedin.com/search/results/people/?keywords=John%20Smith
3. Read results: read_page filter=interactive
4. Present matching profiles
```

### "What's my profile looking like?"
```
1. Connect to Chrome: tabs_context_mcp
2. Navigate: navigate to linkedin.com/in/me/
3. Read profile: read_page
4. Summarize profile stats, recent activity
```

## CLI Fallback (Less Reliable)

The CLI tool is available but LinkedIn often invalidates API sessions:

```bash
# Install
cd /Users/derekrein/Code/cyberdrk305/linkedin && npm install && npm run build && npm link

# Commands (may require fresh cookies frequently)
linkedin setup              # Setup instructions
linkedin check              # Verify credentials
linkedin whoami             # Show logged-in user
linkedin feed -n 10         # Get feed posts
linkedin profile <username> # View profile
```

### Manual Cookie Setup

If using the CLI, you'll need to manually extract cookies:

1. Open Chrome DevTools (F12) on linkedin.com
2. Go to: Application → Cookies → linkedin.com
3. Copy `li_at` and `JSESSIONID` values
4. Run: `linkedin setup --li-at "VALUE" --jsessionid "VALUE"`

Note: LinkedIn aggressively invalidates these sessions after a few API calls.

## Troubleshooting

### Browser extension not connected
- Ensure Chrome is open with your automation profile
- Click the Claude extension icon to activate it
- Try restarting Chrome

### LinkedIn checkpoint/verification page
- LinkedIn may require verification for new browser sessions
- Complete the verification manually, then retry

### Session expired
- Log back into LinkedIn in your automation Chrome profile
- Refresh the page and try again
