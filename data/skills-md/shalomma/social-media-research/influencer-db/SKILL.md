---
name: influencer-db
description: SQLite database for Israeli Tech Nano-Influencers with direct sqlite3 command-line access. Execute any SQL query or inspect schema. Simple and agent-friendly.
---

# Israeli Tech Nano-Influencers Database

A SQLite database with direct sqlite3 command-line access for managing Israeli tech nano-influencer data. Pure SQL with no abstractions.

## Features

- **Direct sqlite3 Access**: Execute any SQL query using the sqlite3 CLI
- **Schema Inspection**: View database schema and table structures
- **Flexible**: Craft any query you need with full SQL power
- **Version Controlled**: Database file is tracked in git for easy collaboration

## Database Schema

### Tables

**`influencers`** - Single table for all influencers (active and excluded)

**Profile & Identity:**
- `twitter_handle` (TEXT PRIMARY KEY) - Twitter/X username
- `name` (TEXT NOT NULL) - Full name
- `role` (TEXT) - Professional role/title
- `focus` (TEXT) - Areas of expertise or interest
- `background` (TEXT) - Professional background
- `profile_url` (TEXT) - Link to Twitter/X profile

**Engagement & Activity:**
- `recent_activity` (TEXT) - Description of recent posts/activity
- `engagement_potential` (TEXT) - Assessment of engagement value (HIGH/MEDIUM/LOW)
- `last_tweet_date` (TEXT) - Date of most recent tweet
- `last_reply_date` (TEXT) - Date of most recent reply

**Location & Language:**
- `location` (TEXT) - Geographic location
- `language` (TEXT) - Languages used in content
- `hebrew_writer` (BOOLEAN) - Whether they write in Hebrew (0/1)

**X API Metrics (matching UserInfoResponse model):**
- `followers` (INTEGER) - Number of followers
- `following` (INTEGER) - Number of accounts they follow
- `statuses_count` (INTEGER) - Total number of tweets/statuses
- `media_count` (INTEGER) - Total media items posted

**Discovery & Tracking:**
- `discovery_path` (TEXT) - How the influencer was discovered/found (e.g., web search query, xai-grok search, website URL, referral path, Twitter list, recommendation from another influencer, etc.)
- `rationale` (TEXT) - Why this influencer was added to the database (e.g., specific expertise, notable projects, unique perspective, community influence, content quality, etc.)
- `added_date` (TEXT NOT NULL) - Date added to database (ISO 8601 format)
- `last_verified_date` (TEXT) - Date profile was last verified (ISO 8601 format)

**Exclusion Management:**
- `excluded` (BOOLEAN DEFAULT 0) - Whether excluded from active list (0=active, 1=excluded)
- `excluded_date` (TEXT) - Date of exclusion (ISO 8601 format, nullable)
- `exclusion_reason` (TEXT) - Reason for exclusion (nullable)

**Metadata:**
- `notes` (TEXT) - Additional notes or observations
- `created_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) - Record creation timestamp
- `updated_at` (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) - Last update timestamp (auto-updated)

**Indexes:**
- `idx_influencers_location` - Fast queries by location
- `idx_influencers_hebrew_writer` - Fast queries by language
- `idx_influencers_followers` - Fast queries by follower count
- `idx_influencers_excluded` - Fast queries for active vs excluded

## Using sqlite3

The database is accessed using the `sqlite3` command-line tool (pre-installed on most systems).

### Basic Usage

```bash
# Open database in interactive mode
sqlite3 influencers.db

# Execute a single query
sqlite3 influencers.db "SELECT * FROM influencers LIMIT 5"

# Get JSON output
sqlite3 influencers.db ".mode json" "SELECT * FROM influencers LIMIT 5"
```

### Common sqlite3 Commands

**Meta commands (start with `.`):**
```bash
.tables                    # List all tables
.schema influencers        # Show table schema
.mode json                 # Set output to JSON format
.mode column               # Set output to column format
.headers on                # Show column headers
.quit                      # Exit sqlite3
```

### SQL Query Examples

#### SELECT Queries

```bash
# Get all influencers
sqlite3 influencers.db "SELECT * FROM influencers"

# Get specific influencer
sqlite3 influencers.db "SELECT * FROM influencers WHERE twitter_handle = 'oriSomething'"

# Get with JSON output
sqlite3 influencers.db -json "SELECT * FROM influencers WHERE location LIKE '%Tel Aviv%'"

# Count by location
sqlite3 influencers.db "SELECT location, COUNT(*) as count FROM influencers GROUP BY location"
```

#### INSERT Queries

```bash
# Add new influencer
sqlite3 influencers.db "INSERT INTO influencers (twitter_handle, name, location, followers, hebrew_writer, added_date, last_verified_date) VALUES ('test_user', 'Test User', 'Tel Aviv', 1500, 1, '2025-10-26', '2025-10-26')"

# Add with more fields
sqlite3 influencers.db "INSERT INTO influencers (twitter_handle, name, role, focus, location, language, followers, following, statuses_count, media_count, hebrew_writer, engagement_potential, discovery_path, added_date) VALUES ('example', 'Example User', 'Developer', 'AI/ML', 'Israel', 'Hebrew, English', 2000, 500, 1500, 300, 1, 'HIGH', 'web search: Israeli AI developers', '2025-10-26')"
```

#### UPDATE Queries

```bash
# Update follower count
sqlite3 influencers.db "UPDATE influencers SET followers = 2000 WHERE twitter_handle = 'test_user'"

# Update multiple X API metrics
sqlite3 influencers.db "UPDATE influencers SET followers = 2500, following = 600, statuses_count = 2000, media_count = 400 WHERE twitter_handle = 'test_user'"
```

#### DELETE Queries

```bash
# Delete specific influencer
sqlite3 influencers.db "DELETE FROM influencers WHERE twitter_handle = 'test_user'"
```

## Architecture

```
.claude/skills/influencer-db/
├── SKILL.md              # This documentation
└── src/
    └── schema.sql       # Database schema (for reference)
influencers.db           # SQLite database (version controlled in git)
```

## Tips for Agents

- **Use JSON output**: Add `-json` flag for JSON output: `sqlite3 influencers.db -json "SELECT ..."`
- **Use transactions**: For multiple operations, wrap in transaction (BEGIN/COMMIT)
- **Check constraints**: twitter_handle is PRIMARY KEY - handle conflicts gracefully
- **Use indexes**: location, followers, hebrew_writer, and excluded are indexed for fast queries
- **Track discovery**: Always populate `discovery_path` (how found) and `rationale` (why added) when adding new influencers to track sourcing and decision-making
