---
name: linkedin-scraper
description: Scrape LinkedIn profiles using the user's Chrome profile. Use when asked to find leads, scrape LinkedIn profiles, extract contact data from LinkedIn, or build prospect lists. Triggers include "find founders on LinkedIn", "scrape this LinkedIn profile", "get LinkedIn data for these people", "build a lead list from LinkedIn".
metadata: { "openclaw": { "emoji": "🔍" } }
---

# LinkedIn Scraper — Chrome Profile Web Scraping

Scrape LinkedIn profiles and search results using the user's authenticated Chrome browser session. No API keys needed — uses the browser tool with the Chrome profile relay.

## Prerequisites

- Chrome browser with active LinkedIn login
- Browser relay connected (Chrome extension or openclaw browser profile)
- DuckDB workspace for storing results (optional)

## Core Workflow

### 1. Single Profile Scrape

```
browser → open LinkedIn profile URL
browser → snapshot (extract structured data)
→ Parse: name, headline, title, company, location, education, experience, connections, about
→ Return structured JSON or insert into DuckDB
```

### 2. Search + Bulk Scrape

```
browser → open LinkedIn search URL with filters
browser → snapshot (extract result cards)
→ Parse each result: name, title, company, profile URL
→ For each profile URL: open → snapshot → parse full profile
→ Batch insert into DuckDB
```

### 3. Company Page Scrape

```
browser → open LinkedIn company page
→ Parse: company name, industry, size, description, specialties, employee count
→ Navigate to /people tab for employee list
```

## Implementation Rules

### Rate Limiting (CRITICAL)
- **Minimum 3-5 second delay** between page loads
- **Maximum 80 profiles per session** (LinkedIn rate limits)
- **Randomize delays** between 3-8 seconds (avoid detection)
- After every 20 profiles, take a **60-second break**
- If CAPTCHA or "unusual activity" detected, **stop immediately** and alert user

### Stealth Patterns
- Use natural scrolling (scroll down slowly, pause, scroll more)
- Don't scrape the same search results page more than twice
- Vary the order of profile visits (don't go sequentially)
- Close and reopen tabs periodically

### Data Extraction — Profile Page
From a LinkedIn profile snapshot, extract these fields:

| Field | Location | Notes |
|-------|----------|-------|
| name | Main heading h1 | Full name |
| headline | Below name | Title + Company usually |
| location | Location section | City, State/Country |
| current_title | Experience section, first entry | Most recent role |
| current_company | Experience section, first entry | Company name |
| education | Education section | School, degree, dates |
| connections | Connections count | Number or "500+" |
| about | About section | Bio text (may need "see more" click) |
| experience | Experience section | All roles with dates |
| profile_url | Browser URL bar | Canonical LinkedIn URL |

### Data Extraction — Search Results
From LinkedIn search results page:

| Field | Location |
|-------|----------|
| name | Result card heading |
| headline | Below name in card |
| location | Card metadata |
| profile_url | Link href on name |
| mutual_connections | Card footer |

## Search URL Patterns

```
# People search
https://www.linkedin.com/search/results/people/?keywords={query}

# With filters
&geoUrn=%5B%22103644278%22%5D          # United States
&network=%5B%22F%22%2C%22S%22%5D        # 1st + 2nd connections
&currentCompany=%5B%22{company_id}%22%5D # Current company
&schoolFilter=%5B%22{school_id}%22%5D    # School filter

# YC founders (common query)
https://www.linkedin.com/search/results/people/?keywords=Y%20Combinator%20founder

# Company employees
https://www.linkedin.com/company/{slug}/people/
```

## DuckDB Integration

When storing to DuckDB, use the Ironclaw workspace database:

```sql
-- Check if leads/contacts object exists
SELECT * FROM objects WHERE name = 'leads' OR name = 'contacts';

-- Insert via the EAV pattern or direct pivot view
INSERT INTO v_leads ("Name", "Title", "Company", "LinkedIn URL", "Location", "Source")
VALUES (?, ?, ?, ?, ?, 'LinkedIn Scrape');
```

If no suitable object exists, create one:
```sql
-- Use Ironclaw's object creation pattern from the dench skill
```

## Error Handling

| Error | Action |
|-------|--------|
| "Sign in" page | LinkedIn session expired — alert user to re-login in Chrome |
| CAPTCHA / Security check | Stop immediately, wait 30+ min, alert user |
| "Profile not found" | Skip, log URL as invalid |
| Rate limit (429) | Stop, wait 15 min, retry with longer delays |
| Empty snapshot | Page still loading — wait 3s and re-snapshot |

## Output Formats

### JSON (default)
```json
{
  "name": "Jane Doe",
  "headline": "CEO at Acme Corp",
  "current_title": "CEO",
  "current_company": "Acme Corp",
  "location": "San Francisco, CA",
  "linkedin_url": "https://www.linkedin.com/in/janedoe",
  "connections": "500+",
  "education": [{"school": "Stanford", "degree": "BS CS", "years": "2010-2014"}],
  "experience": [{"title": "CEO", "company": "Acme Corp", "duration": "2020-Present"}],
  "scraped_at": "2026-02-17T14:30:00Z"
}
```

### Progress Reporting
For bulk scrapes, report progress:
```
Scraping: 15/50 profiles (30%) — Last: Jane Doe (Acme Corp)
Rate: ~4 profiles/min — ETA: 9 min remaining
```

## Safety
- Never scrape private/restricted profiles
- Respect LinkedIn's robots.txt for public pages
- Store data locally only (DuckDB) — never exfiltrate
- User must have legitimate LinkedIn access
- This tool assists the user's own manual browsing at scale
