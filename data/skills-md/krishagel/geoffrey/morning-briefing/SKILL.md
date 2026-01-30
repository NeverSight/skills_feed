---
name: morning-briefing
description: Generate comprehensive morning briefing with calendar, tasks, tickets, news, and weather. Saves to Obsidian, sends email with audio podcast attached.
triggers:
  - "morning briefing"
  - "daily briefing"
  - "start my day"
  - "what's on today"
disable-model-invocation: true
allowed-tools: Read, Write, Bash, WebSearch, WebFetch, mcp__obsidian-vault__*
version: 1.4.0
---

# Morning Briefing Workflow

## Overview

Generates a daily morning briefing and delivers it three ways:
1. **Terminal**: Summary displayed immediately
2. **Obsidian**: Full briefing saved to daily note
3. **Email**: Briefing text + audio podcast attachment

## Location

- **Gig Harbor, WA** - Use for weather queries

## Phase 1: Gather Data

Execute these data gathering steps:

### 1.1 Calendar (Today's Events)

```bash
cd /Users/hagelk/non-ic-code/geoffrey/skills/google-workspace && bun calendar/list_events.js psd --today
```

Returns JSON with today's events including:
- Event summary, location, start/end times
- Attendees and response status
- Hangout/meet links

**Account**: Use `psd` for work calendar

### 1.2 OmniFocus Tasks (Due & Flagged)

```bash
osascript -l JavaScript /Users/hagelk/non-ic-code/geoffrey/skills/morning-briefing/scripts/get_due_flagged.js
```

Returns tasks that are:
- Due today or overdue
- Flagged
- Available (not blocked, not deferred to future)

### 1.3 Recent Emails (Last 24 Hours)

```bash
# Get yesterday's date in Gmail query format
YESTERDAY=$(date -v-1d +%Y/%m/%d)
cd /Users/hagelk/non-ic-code/geoffrey/skills/google-workspace && bun gmail/list_messages.js psd --query "in:inbox after:$YESTERDAY" --max 15
```

Returns recent inbox messages with:
- From, subject, date, snippet
- Whether read or unread
- Thread ID for context
- Labels array

**Filtering**: Only show emails still in inbox (not already labeled/processed).
- Emails with custom labels (Label_XXXXX) have been sorted and should be excluded
- Exception: Include emails with SaneCC or SaneLater labels (worth knowing about)
- System labels (UNREAD, INBOX, CATEGORY_*, IMPORTANT) don't count as "processed"

**Philosophy**: Any email still in inbox from last 24 hours needs attention, read or not.

**Account**: Use `psd` for work email

### 1.4 Open Freshservice Tickets

```bash
bun /Users/hagelk/non-ic-code/geoffrey/skills/freshservice-manager/scripts/list_tickets.js '{"workspace_id": 2, "filter": "new_and_my_open"}'
```

Returns open tickets assigned to or created by user in Technology workspace.

### 1.5 Pending Approvals

```bash
bun /Users/hagelk/non-ic-code/geoffrey/skills/freshservice-manager/scripts/get_approvals.js requested
```

Returns service requests awaiting approval.

### 1.6 Weather

Use WebSearch:
```
Gig Harbor WA weather today forecast
```

Extract:
- Current conditions
- High/low temperature
- Precipitation chance
- Any alerts

### 1.7 EdTech News (with Synopses)

Use WebSearch:
```
K-12 education technology news past 24 hours January 2026
```

For each article found (3-5 articles):
1. Use WebFetch to read the full article
2. Extract a 2-3 sentence synopsis covering:
   - What happened / what's new
   - Why it matters for K-12 education
   - Key takeaway or action item

**Freshness check**: Verify article dates before including. Only include articles published within the last 24 hours. Skip older articles even if they appear in results.

**Topics to cover:**
- EdTech product launches and updates
- School technology policy changes
- Cybersecurity in schools
- Digital learning trends

### 1.8 AI News (with Synopses)

Use WebSearch:
```
artificial intelligence news past 24 hours January 2026 latest
```

For each article found (3-5 articles):
1. Use WebFetch to read the full article
2. Extract a 2-3 sentence synopsis covering:
   - What's the development
   - Industry impact
   - Relevance to education/work

**Freshness check**: Verify article dates before including. Only include articles published within the last 24 hours. Skip older articles even if they appear in results.

**Topics to cover:**
- Major AI model releases and capabilities
- AI policy and regulation
- Enterprise AI adoption
- AI research breakthroughs

### 1.9 K-12 Leadership News (with Synopses)

Use WebSearch:
```
K-12 school leadership superintendent news past 24 hours January 2026
```

For each article found (2-3 articles):
1. Use WebFetch to read the full article
2. Extract a 2-3 sentence synopsis covering:
   - Policy or leadership development
   - Impact on districts/schools
   - Relevance to CIO/technology leadership

**Freshness check**: Verify article dates before including. Only include articles published within the last 24 hours. Skip older articles even if they appear in results.

**Topics to cover:**
- State and federal education policy
- Superintendent and board news
- School funding and budgets
- Workforce and staffing trends

### 1.9b School Safety & Security News (with Synopses)

Use WebSearch:
```
K-12 school safety security news past 24 hours January 2026
```

For each article found (3 articles):
1. Use WebFetch to read the full article
2. Extract a 2-3 sentence synopsis covering:
   - What happened / what's new
   - Impact on school safety practices
   - Key takeaway for districts

**Freshness check**: Verify article dates before including. Only include articles published within the last 24 hours. Skip older articles even if they appear in results.

**Topics to cover:**
- School security incidents and responses
- Safety policy changes
- Emergency preparedness
- Mental health and threat assessment
- Physical security technology

### 1.10 Technology Team EOD Messages (Last Business Day) - DETAILED

Get end-of-day check-in messages from the Technology Staff space:

```bash
cd /Users/hagelk/non-ic-code/geoffrey/skills/google-workspace && bun chat/get_eod_messages.js psd spaces/AAAAxOtpv10 last-business-day
```

**CRITICAL - NO HALLUCINATION:**
- ONLY use names that appear in the `sender` field of the script output
- If script returns no messages, say "No EOD messages found"
- If script returns messages with sender IDs instead of names, display the ID (e.g., "users/12345...")
- NEVER invent names, locations, or accomplishments
- Copy-paste approach: treat script output as source of truth

**Before extracting team data:**
1. Examine the raw JSON output from the script
2. List the exact `sender` values returned
3. Use ONLY those names - no paraphrasing, no "improving"

**CRITICAL**: Extract FULL details from each team member's EOD message. Look for messages that contain "Today:" prefix - these are the detailed EOD summaries.

For each team member who posted an EOD summary:
1. **Name**: Who posted (use EXACTLY the name from `sender` field)
2. **Location(s)**: Where they worked (WFH, DCRC, school sites)
3. **Key accomplishments**: Specific tasks completed (not just "tickets")
4. **Notable items**: Interesting problems solved, projects worked on
5. **Issues/blockers**: Any problems mentioned

**Example extraction from raw message:**
```
Brad White:
- Location: TSD (Tech Services)
- Accomplished: Packaged Cinema 4D plugin for deployment, fixed OAuth blocking for Maxon App sign-in, created SwiftDialog notification for plugin installs, used Claude Code for first time to create Installomator label for Godot game engine
- Notable: Working on Unity deployment troubleshooting, burning comp time leaving early
```

**Note**: If today is Monday, "last business day" = Friday (or Thursday if Friday was a holiday).

### 1.10b Safety & Security Team EOD Messages (Last Business Day)

Get end-of-day check-in messages from the Safety & Security Staff space:

```bash
cd /Users/hagelk/non-ic-code/geoffrey/skills/google-workspace && bun chat/get_eod_messages.js psd spaces/AAAAFpQaAnA last-business-day
```

**Space**: PSD Safety & Security Team

**CRITICAL - NO HALLUCINATION:**
- ONLY use names that appear in the `sender` field of the script output
- If script returns no messages, say "No EOD messages found"
- If script returns messages with sender IDs (e.g., "users/12345...") instead of names:
  - Display as: **Unknown (users/123456...)** - [Location from message content]
  - Add note: "Name not in mapping - update chat_user_mapping.json"
- NEVER invent names, locations, or accomplishments
- Copy-paste approach: treat script output as source of truth

**Before extracting team data:**
1. Examine the raw JSON output from the script
2. List the exact `sender` values returned
3. Use ONLY those names - no paraphrasing, no "improving"

Extract using same format as Technology Team - names, locations, accomplishments, issues.

**Note**: If today is Monday, "last business day" = Friday (or Thursday if Friday was a holiday).

### 1.11 Team Completed Tickets (Last Business Day)

Get tickets closed by the Technology team on the last business day:

```bash
# First get the last business day
LAST_BIZ_DAY=$(bun /Users/hagelk/non-ic-code/geoffrey/skills/morning-briefing/scripts/get_last_business_day.js | jq -r '.date')

# Then get daily summary for that date
bun /Users/hagelk/non-ic-code/geoffrey/skills/freshservice-manager/scripts/get_daily_summary.js "$LAST_BIZ_DAY"
```

**CRITICAL - NO HALLUCINATION:**
- ONLY use agent names that appear in the `byAgent` section of script output
- Use EXACTLY the ticket counts returned by the script
- NEVER invent names or ticket counts
- If an agent's name shows as ID or email, display it as-is

**Before reporting ticket stats:**
1. Examine the raw JSON output from `get_daily_summary.js`
2. List the exact agent names from `byAgent` field
3. Use ONLY those names and counts

Returns:
- Total tickets closed
- Breakdown by agent
- Breakdown by category (Password Reset, Chromebook, etc.)
- Automated vs agent-resolved

**Workspace**: Technology (workspace_id: 2)

### 1.12 Ticket Trends Analysis

Compare last business day to previous days for trends:

```bash
# Get last 5 business days of summaries for trend analysis
# The get_daily_summary.js script supports date parsing
bun /Users/hagelk/non-ic-code/geoffrey/skills/freshservice-manager/scripts/get_daily_summary.js "last monday"
bun /Users/hagelk/non-ic-code/geoffrey/skills/freshservice-manager/scripts/get_daily_summary.js "last tuesday"
# etc.
```

Analyze for:
- Volume trends (increasing/decreasing)
- Category spikes (sudden increase in specific issue types)
- Agent workload distribution
- Unusual patterns

### 1.13 Software Development Workspace Tickets

Get open tickets in the Software Development workspace:

```bash
bun /Users/hagelk/non-ic-code/geoffrey/skills/freshservice-manager/scripts/search_tickets.js "status:2 OR status:3" 13
```

Returns all open (status:2) and pending (status:3) tickets in the Software Development workspace.

**Workspace ID**: 13 (Software Development)
**Note**: This is the user's internal software development bug tracker for AI Studio and other PSD applications.

### 1.14 Legislative Activity (Last Business Day)

Get K-12 education bills with activity since the last business day:

```bash
# Get lookback info and bills to check
bun /Users/hagelk/non-ic-code/geoffrey/skills/legislative-tracker/scripts/get_recent_bill_activity.js --last-business-day
```

This returns:
- Date range to check (last business day → today)
- List of ~143 confirmed education bill IDs
- WebFetch instructions for each bill

**Workflow:**
1. Get the output from `get_recent_bill_activity.js`
2. WebFetch each bill URL (batch 5-6 in parallel for speed)
3. Extract latest action date from each bill page
4. Filter to bills where latest_action_date >= lookback_start
5. Apply priority framework (HIGH/MEDIUM/LOW based on district impact)
6. Include summary of what each bill does

**On Monday**: Lookback starts on Friday (or earlier if Friday was a holiday), so includes all weekend activity (hearings, votes, committee actions).

**Example URLs to WebFetch:**
- `https://app.leg.wa.gov/billsummary?BillNumber=1020&Year=2025`
- `https://app.leg.wa.gov/billsummary?BillNumber=5038&Year=2025`

**Note**: Only include bills that actually had activity. If no bills moved, output "No legislative activity since [date]".

## Phase 2: Generate Briefing

### 2.1 Analyze & Prioritize

Review gathered data and identify:
- **Conflicts**: Overlapping calendar events
- **Urgencies**: Overdue tasks, high-priority tickets
- **Themes**: Patterns across data sources

### 2.2 Format Markdown Briefing

Use this structure:

```markdown
# Daily Briefing - [DATE]

## Weather
[Current conditions, high/low, precipitation]

## Today's Calendar
| Time | Event | Location |
|------|-------|----------|
| ... | ... | ... |

**Conflicts/Notes**: [any issues]

## Priority Tasks
### Due Today
- [ ] Task 1
- [ ] Task 2

### Flagged
- [ ] Task 3

### Overdue
- [ ] Task 4 (due [date])

## Recent Emails (Last 24h)
[X emails in inbox from last 24 hours]

### Needs Response
- From: [sender] - [subject] (snippet)
- From: [sender] - [subject] (snippet)

### FYI/Notifications
- [sender] - [subject]

## Freshservice
### Technology Tickets: [count] open
[Top 3-5 tickets by priority/age]

### Software Development Tickets: [count] open
[List tickets in Software Dev workspace]

### Pending Approvals: [count]
[List with ticket #, requester, summary]

## Team Activity (Last Business Day: [DAY, DATE])

**Data Source Verification (REQUIRED):**
- Technology EOD script returned: [X] messages from [list exact sender names from JSON]
- Safety & Security EOD script returned: [X] messages from [list exact sender names from JSON]
- Freshservice daily summary returned: [X] tickets by [list exact agent names from JSON]

*Use ONLY the names listed above. Never invent or paraphrase names.*

### Technology Team EOD Summaries

**[Name from sender field]** - [Location(s)]
- [Key accomplishment 1 - be specific about what they did]
- [Key accomplishment 2]
- [Notable: any interesting problems solved or projects]

**[Name from sender field]** - [Location(s)]
- [Key accomplishment 1]
- [Key accomplishment 2]
- [Issues: any blockers or problems mentioned]

*[Continue for each team member who posted an EOD summary]*

### Safety & Security Team EOD Summaries

**[Name from sender field]** - [Location(s)]
- [Key accomplishment 1]
- [Key accomplishment 2]
- [Notable: any issues or incidents handled]

*If sender shows as user ID (users/12345...), display: **Unknown (users/12345...)** - [Location]*

*[Continue for each team member who posted an EOD summary]*

### Tickets Completed by Team: [count]
| Agent | Tickets | Top Categories |
|-------|---------|----------------|
| [Name from byAgent field] | X | Password Reset (Y), Chromebook (Z) |

### Ticket Trends
- Volume: [up/down/stable] vs previous days
- Notable patterns: [any spikes or anomalies]

## EdTech News

### [Article Title 1] - [Source]
[2-3 sentence synopsis: what happened, why it matters, key takeaway]

### [Article Title 2] - [Source]
[2-3 sentence synopsis]

### [Article Title 3] - [Source]
[2-3 sentence synopsis]

## AI News

### [Article Title 1] - [Source]
[2-3 sentence synopsis: what's the development, industry impact, relevance]

### [Article Title 2] - [Source]
[2-3 sentence synopsis]

### [Article Title 3] - [Source]
[2-3 sentence synopsis]

## K-12 Leadership News

### [Article Title 1] - [Source]
[2-3 sentence synopsis: policy/leadership development, impact, relevance to tech leadership]

### [Article Title 2] - [Source]
[2-3 sentence synopsis]

## School Safety & Security News

### [Article Title 1] - [Source]
[2-3 sentence synopsis: what happened, impact on safety practices, takeaway for districts]

### [Article Title 2] - [Source]
[2-3 sentence synopsis]

### [Article Title 3] - [Source]
[2-3 sentence synopsis]

## Legislative Activity ([Last Biz Day] - Today)

[X] education bills had movement:

### 🔴 HIGH Priority

#### [Bill ID] - [Short Title]
**Action**: [What happened - hearing, vote, committee action, etc.]
**Summary**: [1-2 sentences: what the bill does, potential district impact]

### 🟡 MEDIUM Priority

#### [Bill ID] - [Short Title]
**Action**: [What happened]
**Summary**: [1-2 sentences]

### 🟢 LOW Priority
- [Bill ID]: [Action type] - [One line summary]

*No legislative activity since [date]* - if no bills moved

## Quick Stats
- Calendar events: X
- Tasks overdue: X | Due today: X | Flagged: X
- Open tickets (Tech): X
- Open tickets (Software Dev): X
- Pending approvals: X
- Recent emails (24h): X
- Team tickets closed [last biz day]: X
- News articles: EdTech (X) | AI (X) | Leadership (X)
- Legislative bills with activity: X
```

### 2.3 Generate Podcast Script (Extended Format)

Transform the briefing into a comprehensive conversational audio script:
- First person, casual professional tone
- **10-15 minutes speaking time (~1500-2000 words)**
- Address listener directly ("Here's what you need to know today...")

**Required Sections (in order):**

1. **Opening** (~100 words)
   - Day, date, weather summary
   - Quick preview of key items

2. **Calendar & Schedule** (~150 words)
   - Today's events with context
   - Highlight key meetings/events
   - Note any conflicts or prep needed

3. **Tasks & Priorities** (~150 words)
   - Overdue items that need attention
   - Due today items
   - Flagged priorities

4. **Tickets & Service Desk** (~150 words)
   - Open Technology tickets
   - Software Development tickets
   - Pending approvals

5. **Team Activity - DETAILED** (~400 words)
   - What the Technology team accomplished on last business day
   - Highlight 3-5 team members by name with specifics
   - Notable projects, interesting problems solved
   - What the Safety & Security team accomplished
   - Overall ticket closure stats

   **CRITICAL - NO HALLUCINATION:**
   - Use ONLY names from the script output `sender` fields
   - Use ONLY ticket counts from the `get_daily_summary.js` output
   - If script returned no messages, say "No EOD messages were posted"
   - NEVER invent names, locations, or accomplishments

6. **EdTech News** (~200 words)
   - 2-3 articles with synopses
   - Why each matters for K-12

7. **AI News** (~200 words)
   - 2-3 articles with synopses
   - Industry impact and relevance

8. **K-12 Leadership News** (~150 words)
   - 1-2 articles with synopses
   - Policy/leadership implications

8b. **School Safety & Security News** (~150 words)
   - 2-3 articles with synopses
   - Safety practices and district implications

9. **Legislative Update** (~150 words)
   - Bills that had hearings, votes, or readings since last business day
   - Highlight any with direct district impact (fiscal, operational, staffing)
   - Note upcoming hearing dates if relevant
   - On Mondays, include weekend activity summary

10. **Closing** (~100 words)
    - Top 3 priorities for the day
    - Sign off

**Style Guidelines:**
- Use team members' first names when discussing their work
- Include specific details (not "worked on tickets" but "resolved 34 Chromebook repairs")
- Transition smoothly between sections
- Add brief commentary/analysis on news items

Save to `/tmp/morning_briefing_podcast.txt`

## Phase 3: Create Podcast

```bash
uv run --with mlx-audio --with pydub /Users/hagelk/non-ic-code/geoffrey/skills/local-tts/scripts/generate_audio.py \
  --file /tmp/morning_briefing_podcast.txt \
  --voice af_heart \
  --output ~/Desktop/morning_briefing_[DATE].mp3
```

**Voice Selection**: af_heart (warm, friendly - good for morning briefing)
**Note**: Uses local MLX TTS (Kokoro model) - no API costs

## Phase 3.5: Generate Infographic (MANDATORY)

**CRITICAL:** The infographic MUST be generated. Do not skip this phase.

Create a visual summary infographic using the image-gen skill.

### 3.5.1 Build Infographic Prompt

Based on gathered data, construct a prompt for the infographic:

```
Create an infographic summarizing a daily work briefing for [DATE].

Visual concept: A clean dashboard layout with distinct sections for different data categories.

Key data to display:
- Weather: [conditions], High [X]°F, Low [Y]°F
- Calendar: [X] events today, highlight: [key meeting]
- Tasks: [X] overdue, [Y] due today, [Z] flagged
- Tickets: [X] Technology open, [Y] Software Dev open
- Team Activity: [X] tickets closed by team yesterday
- Emails: [X] in inbox from last 24h

Style: Professional, clean design with PSD brand colors (navy blue #003366, gold accent #FFD700).
Flat design, clear sections, modern sans-serif typography.

Layout: Horizontal 16:9, organized as a dashboard with weather top-left, calendar top-right,
tasks and tickets in middle row, team stats at bottom.

Title: "Daily Briefing - [DATE]"
Subtitle: "Gig Harbor, WA"
```

### 3.5.2 Generate Image

```bash
uv run /Users/hagelk/non-ic-code/geoffrey/skills/image-gen/scripts/generate.py \
  "[infographic prompt]" \
  ~/Desktop/morning_briefing_[DATE].png \
  16:9 \
  2K
```

**Settings:**
- Aspect ratio: 16:9 (landscape dashboard)
- Size: 2K (ensures text readability)
- Output: `~/Desktop/morning_briefing_[DATE].png`

## Phase 4: Save to Obsidian

### 4.1 Copy Infographic to Obsidian Assets

```bash
cp ~/Desktop/morning_briefing_[DATE].png \
  ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Personal_Notes/Geoffrey/Daily\ Briefings/assets/
```

### 4.2 Add Infographic to Briefing Markdown

At the top of the briefing (after the title), add:

```markdown
![Daily Briefing Infographic](assets/morning_briefing_[DATE].png)
```

### 4.3 Save Briefing File

Use Obsidian MCP tools:

1. **Check if daily note exists**:
   ```
   mcp__obsidian-vault__get_vault_file
   filename: "Geoffrey/Daily Briefings/[YYYY-MM-DD].md"
   ```

2. **Create or update**:
   ```
   mcp__obsidian-vault__create_vault_file
   filename: "Geoffrey/Daily Briefings/[YYYY-MM-DD].md"
   content: [full briefing markdown with infographic embed]
   ```

**File path pattern**: `Geoffrey/Daily Briefings/YYYY-MM-DD.md`

**Fallback** (if MCP unavailable): Write directly to iCloud path:
```bash
/Users/hagelk/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal_Notes/Geoffrey/Daily Briefings/[YYYY-MM-DD].md
```

## Phase 5: Send Email (HTML with Inline Infographic)

### 5.1 Generate HTML Email Body

Create a professional HTML email (NOT markdown). Use the template at `skills/morning-briefing/templates/email.html` as reference.

**Key HTML structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 0 auto; }
    .header { text-align: center; border-bottom: 2px solid #003366; padding: 16px; }
    .stat-box { background: #f8f9fa; padding: 12px; text-align: center; }
    /* ... more styles from template ... */
  </style>
</head>
<body>
  <!-- Infographic at TOP - referenced via cid:briefing_image -->
  <img src="cid:briefing_image" alt="Daily Briefing" style="width: 100%; max-width: 600px; border-radius: 8px; margin-bottom: 20px;">

  <div class="header">
    <h1 style="color: #003366;">Daily Briefing</h1>
    <p>[DAY_OF_WEEK], [DATE_FORMATTED]</p>
  </div>

  <!-- Weather, Stats, Calendar, Tasks, Team, News sections -->
  <!-- See templates/email.html for full structure -->

  <div style="background: #e8f4f8; padding: 16px; border-radius: 8px; margin-top: 20px;">
    <strong>Attachments:</strong><br>
    🎧 Audio Podcast (~10-15 min)<br>
    📊 Infographic (also shown above)
  </div>

  <p style="text-align: center; color: #666; font-size: 12px;">
    Full briefing: Obsidian/Geoffrey/Daily Briefings/[DATE].md
  </p>
</body>
</html>
```

**CRITICAL:** The `<img src="cid:briefing_image">` displays the infographic inline at the top of the email.

Save to `/tmp/morning_briefing_email.html`

### 5.2 Send with Inline Image + Attachments

```bash
cd /Users/hagelk/non-ic-code/geoffrey/skills/google-workspace && bun gmail/send_with_attachments.js psd \
  --to "hagelk@psd401.net" \
  --subject "Daily Briefing - [DATE]" \
  --body-file /tmp/morning_briefing_email.html \
  --html \
  --inline-image "~/Desktop/morning_briefing_[DATE].png" \
  --attachments "~/Desktop/morning_briefing_[DATE].mp3"
```

**Options explained:**
- `--html` - Treat body as HTML (required for formatting)
- `--inline-image` - Embeds image at top of email (referenced as `cid:briefing_image`)
- `--attachments` - Additional files to attach (podcast)

**Result:**
- Infographic displays INLINE at top of email (visible without downloading)
- Podcast attached for download
- Email renders nicely in Gmail with professional styling

## Output

Return standardized summary:

```markdown
## Summary
Generated daily briefing for [DATE]

## Actions
- Gathered calendar events: X
- Gathered tasks: X (Y due today, Z flagged)
- Gathered Technology tickets: X open, Y approvals pending
- Gathered Software Dev tickets: X open
- Gathered team EOD messages: X from [last business day]
- Gathered team completed tickets: X from [last business day]
- Weather: [conditions]
- News: X headlines
- Generated podcast: ~/Desktop/morning_briefing_[DATE].mp3
- Saved to Obsidian: Geoffrey/Daily Briefings/[DATE].md
- Email: [sent/skipped - reason]

## Status
[Status emoji] [Complete/Partial]

## Quick View
[2-3 line summary of most important items]
```

## Error Handling

### Missing Google Workspace Scripts
If calendar/email scripts don't exist:
- Skip those sections
- Note "Integration pending" in output
- Continue with available data sources

### OmniFocus Not Running
```
Status: Partial
Note: OmniFocus not running - task data unavailable
```

### Freshservice API Error
```
Status: Partial
Note: Freshservice API error - ticket data unavailable
```

### Local TTS Generation Failed
```
Status: Partial
Note: Audio generation failed - check mlx-audio setup
Briefing saved to Obsidian without podcast
```

## Dependencies

| Skill/Tool | Required For | Fallback |
|------------|--------------|----------|
| google-workspace | Calendar, email, team EOD | Skip sections |
| omnifocus-manager | Tasks | Skip section |
| freshservice-manager | Tickets, approvals, team stats | Skip section |
| local-tts | Audio podcast | Text-only briefing |
| obsidian-vault (MCP) | Save briefing | Display only |
| WebSearch | News, weather | Skip sections |

## Configuration

### User Preferences
- **Location**: Gig Harbor, WA (weather)
- **Work Email**: psd account
- **Technology Workspace**: workspace_id: 2
- **Software Dev Workspace**: workspace_id: 13
- **Technology Chat Space**: spaces/AAAAxOtpv10 (Technology Staff Check-Ins & Logs)
- **Safety & Security Chat Space**: spaces/AAAAFpQaAnA (PSD Safety & Security Team)
- **Voice**: af_heart (warm, friendly - local Kokoro TTS)
- **Podcast Length**: 10-15 minutes (~1500-2000 words)

### Customization
Users can request:
- "Skip news" - omit news section
- "No podcast" - text only
- "Just calendar and tasks" - minimal briefing
