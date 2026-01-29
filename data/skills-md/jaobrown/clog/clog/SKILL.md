---
name: clog
description: Daily coding diary that tracks Claude Code usage. Run /clog to log sessions, /clog init to set up, /clog status to view stats.
---

# clog - Claude Code Session Logger

A personal coding diary that tracks your Claude Code sessions, summarizes what you worked on, and optionally shares stats on a public leaderboard.

## Commands

- `/clog` - Log recent sessions since your last sync
- `/clog init` - First-time setup (fork repo, configure settings)
- `/clog status` - View your coding stats

## How to Use

When the user runs `/clog`, `/clog init`, or `/clog status`, follow the instructions below for the appropriate command.

---

## /clog init

First-time setup to configure clog for the user.

### Steps

1. **Check GitHub authentication**
   ```bash
   gh auth status
   ```
   If not authenticated, tell the user to run `gh auth login` first.

2. **Get GitHub username**
   ```bash
   gh api user --jq '.login'
   ```
   Store this as `$GITHUB_USER`.

3. **Check if clog repo already exists**
   ```bash
   gh repo view $GITHUB_USER/clog --json name 2>/dev/null
   ```

4. **If repo doesn't exist, fork the template**
   ```bash
   gh repo fork jaobrown/clog --clone=false --fork-name clog
   ```

5. **Check if ~/.clog directory exists**
   ```bash
   ls -la ~/.clog 2>/dev/null
   ```

6. **If ~/.clog doesn't exist, clone the repo**
   ```bash
   gh repo clone $GITHUB_USER/clog ~/.clog
   ```

7. **Initialize config.json if it doesn't exist**
   First check if it exists:
   ```bash
   cat ~/.clog/config.json 2>/dev/null
   ```

   If it doesn't exist, create `~/.clog/config.json`:
   ```json
   {
     "user": "<github-username>",
     "repoUrl": "https://github.com/<github-username>/clog",
     "leaderboard": false
   }
   ```

   Also initialize `~/.clog/clog.json` if it doesn't exist:
   ```json
   {
     "user": "<github-username>",
     "lastSync": null,
     "sessions": []
   }
   ```

   And create the logs directory:
   ```bash
   mkdir -p ~/.clog/logs
   ```

8. **Ask about leaderboard participation**
   Ask the user: "Would you like to join the public clog leaderboard? This will make your coding stats visible to others."

   If yes:
   - Update `config.json` with `"leaderboard": true`
   - Add the leaderboard topic to their repo:
     ```bash
     gh repo edit $GITHUB_USER/clog --add-topic clog-leaderboard
     ```
   - Tell them: "You're on the leaderboard! Your stats are now discoverable at github.com/$GITHUB_USER/clog"

   If no:
   - Keep `"leaderboard": false` in config

9. **Commit and push initial config**
   ```bash
   cd ~/.clog && git add config.json && git commit -m "Initialize clog config" && git push
   ```

10. **Success message**
    ```
    clog initialized successfully!

    Your clog repo: https://github.com/$GITHUB_USER/clog
    Local directory: ~/.clog
    Leaderboard: [yes/no]

    Run /clog to log your first sessions!
    ```

---

## /clog (Main Command)

Log recent Claude Code sessions since the last sync.

### Steps

1. **Read config**
   ```bash
   cat ~/.clog/config.json
   ```
   If file doesn't exist, tell user to run `/clog init` first.

2. **Get lastSync timestamp**
   Read `~/.clog/clog.json` and extract `lastSync`. If null or file doesn't exist, this is the first run.

   For first run, calculate 7 days ago:
   ```bash
   # macOS
   date -v-7d -u +"%Y-%m-%dT%H:%M:%SZ"
   # or Linux
   date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%SZ"
   ```

3. **Find all Claude project directories**
   ```bash
   ls -d ~/.claude/projects/*/ 2>/dev/null
   ```

4. **For each project directory, gather sessions**

   For each project folder:

   a. **Check for sessions-index.json**
      ```bash
      cat ~/.claude/projects/<project>/sessions-index.json 2>/dev/null
      ```

   b. **If sessions-index.json exists:**
      - Parse JSON to get session entries
      - Filter entries where `modified` > `lastSync`
      - Extract: `sessionId`, `summary`, `firstPrompt`, `created`, `modified`, `projectPath`

   c. **If no sessions-index.json, parse JSONL files directly:**
      ```bash
      ls ~/.claude/projects/<project>/*.jsonl 2>/dev/null
      ```
      For each .jsonl file:
      - Read the file and parse JSON lines
      - Get timestamps from messages to determine if session is recent
      - Get first user message for context

5. **Extract project name from folder path**
   The folder name is like `-Users-jared-Developer-apps-spool` (the actual path with dashes instead of slashes).

   To get the project name, use the `projectPath` field from sessions-index.json if available, or extract from the folder name:
   ```bash
   # If projectPath is available (e.g., "/Users/jared/Developer/apps/spool")
   basename "$projectPath"  # Returns: spool

   # If only folder name (e.g., "-Users-jared-Developer-apps-spool")
   # Remove leading dash, replace dashes with slashes, get basename
   folder_name="-Users-jared-Developer-apps-spool"
   echo "$folder_name" | sed 's/^-//' | tr '-' '/' | xargs basename
   ```

   The `projectPath` field in sessions-index.json is the cleanest source.

6. **Calculate tokens for each session**

   For sessions needing token counts, parse the JSONL file and sum tokens from assistant messages with `usage` data.

   Token counting formula (per message):
   - `cache_creation_input_tokens` = new input tokens cached (billable at full rate)
   - `output_tokens` = generated output tokens
   - Note: `cache_read_input_tokens` are cached reads (billed at reduced rate, don't add to main count)

   **For simplicity, count:** `cache_creation_input_tokens + output_tokens` per message, summed across session.

   This represents the "new work" in each session. The actual token field values can be extracted with:
   ```bash
   # Extract usage from assistant messages
   cat <session>.jsonl | grep '"usage"' | head -20
   ```

   Parse each line as JSON and sum the relevant token fields.

7. **Calculate duration for each session**
   - Find first and last timestamps in the session
   - Duration = last - first
   - Format as "Xh Ym" (e.g., "2h 10m")

8. **Generate summaries for sessions without them**

   For sessions that don't have a pre-computed summary:
   - Read the conversation content from JSONL
   - Generate a one-line summary describing what was accomplished
   - Example summaries:
     - "Refactored video pipeline to use R2 storage"
     - "Fixed analytics event firing twice"
     - "Added user authentication flow"

9. **Display results**

   Format output like:
   ```
   Found X sessions since your last log (Jan 25)

   - spool: "Refactored video pipeline to use R2 storage" (34k tokens, 2h 10m)
   - contra: "Debugged repost timing issue" (12k tokens, 30m)
   - contra: "Added social post analytics" (8k tokens, 20m)

   Total: 54k tokens across 3h

   Push to github.com/username/clog? (Y/n)
   ```

10. **If user confirms, update clog data**

    a. **Read existing clog.json**
       ```bash
       cat ~/.clog/clog.json
       ```

       If the file doesn't exist or is empty, initialize it:
       ```json
       {
         "user": "<github-username>",
         "lastSync": null,
         "sessions": []
       }
       ```

    b. **Add new sessions to clog.json**
       Generate a UUID for each session:
       ```bash
       uuidgen  # macOS/Linux
       # or: python3 -c "import uuid; print(uuid.uuid4())"
       ```

       Append sessions to the `sessions` array:
       ```json
       {
         "id": "<generated-uuid>",
         "date": "<session-start-date as YYYY-MM-DD>",
         "project": "spool",
         "summary": "Refactored video pipeline",
         "tokens": 34000,
         "durationMins": 130
       }
       ```

    c. **Update lastSync timestamp**
       Set to current ISO timestamp.

    d. **Update monthly log file**
       Append to `~/.clog/logs/YYYY-MM.md` in the format:
       ```markdown
       **Monday, Jan 27**
       - spool: Refactored video pipeline to use R2 storage (34k tokens, 2h 10m)
       - contra: Debugged repost timing issue (12k tokens, 30m)
       ```

    e. **Update README.md with latest stats**
       Regenerate stats section showing total tokens, sessions, etc.

    f. **Commit and push**
       ```bash
       cd ~/.clog && git pull --rebase && git add -A && git commit -m "clog: $(date +%Y-%m-%d)" && git push
       ```

       Note: Pull first to avoid conflicts if repo was updated elsewhere.

11. **Success message**
    ```
    Logged X sessions to your clog!
    View at: https://github.com/username/clog
    ```

---

## /clog status

Display coding statistics.

### Steps

1. **Read clog.json**
   ```bash
   cat ~/.clog/clog.json
   ```
   If doesn't exist, tell user to run `/clog init` first.

2. **Calculate statistics**

   From the sessions array, calculate:
   - **Total sessions**: Count of all sessions
   - **Total tokens**: Sum of all session tokens
   - **Total time**: Sum of all durationMins, format as hours
   - **This week**: Sessions in current week
   - **Current streak**: Consecutive days with sessions
   - **Longest streak**: Longest consecutive day streak
   - **Most active project**: Project with most sessions

3. **Display formatted stats**
   ```
   clog stats for @username

   All Time
   --------
   Sessions: 142
   Tokens: 2.4M
   Time: 86h

   This Week
   ---------
   Sessions: 12
   Tokens: 180k
   Time: 8h 30m

   Streaks
   -------
   Current: 5 days
   Longest: 23 days

   Top Projects
   ------------
   1. spool (52 sessions)
   2. contra (38 sessions)
   3. gaia (24 sessions)

   View full history: https://github.com/username/clog
   ```

---

## Data Structures Reference

### ~/.clog/config.json
```json
{
  "user": "githubusername",
  "repoUrl": "https://github.com/githubusername/clog",
  "leaderboard": true
}
```

Note: `lastSync` is stored in `clog.json`, not config.json.

### ~/.clog/clog.json
```json
{
  "user": "githubusername",
  "lastSync": "2025-01-27T18:30:00Z",
  "sessions": [
    {
      "id": "uuid",
      "date": "2025-01-27",
      "project": "spool",
      "summary": "Added profile completion modal",
      "tokens": 12400,
      "durationMins": 45
    }
  ]
}
```

### ~/.clog/logs/YYYY-MM.md
```markdown
# January 2025

## Week 4 (Jan 20-26)

**Monday, Jan 20**
- spool: Refactored video pipeline to use R2 storage (34k tokens, 2h 10m)
- contra: Fixed repost timing bug (12k tokens, 30m)

**Tuesday, Jan 21**
- spool: Built sidebar UI for connected repos (18k tokens, 45m)

### Weekly Stats
- Sessions: 8
- Tokens: 142k
- Time: 6h 20m

---

## Week 3 (Jan 13-19)
...
```

---

## Error Handling

- **Not initialized**: If `~/.clog/config.json` doesn't exist, prompt user to run `/clog init`
- **GitHub not authenticated**: If `gh auth status` fails, tell user to run `gh auth login`
- **No sessions found**: If no sessions since lastSync, show "No new sessions since [date]. Run /clog status to see your stats."
- **Empty projects**: Skip project directories with no .jsonl files or empty sessions-index.json
- **Parse errors**: If a JSONL file is corrupted, skip it and continue with others

---

## Notes for Claude

- When generating summaries, focus on the **outcome** or **change made**, not the process
- Good summary: "Added dark mode support to settings page"
- Bad summary: "Worked with user on implementing feature"
- Keep summaries under 60 characters when possible
- Use sentence case, no period at end
- Token counts should be formatted with 'k' suffix (e.g., 34k, 1.2M)
- Duration should be formatted as "Xh Ym" or just "Xm" if under an hour
