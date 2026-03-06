---
name: freeUnlimited-websearch
description: Free unlimited web search using DuckDuckGo. No API key required.
---

# Free Unlimited Web Search

Search the web for free using DuckDuckGo - no API key or rate limits.

## Features
- **Free**: No API key required
- **Unlimited**: No rate limits or quotas
- **Private**: Uses DuckDuckGo's privacy-focused search

## Requirements
- Python 3.8+
- `ddgs` package (`pip install ddgs`)

## Installation

1. Install the `ddgs` package in a Python environment:
   ```bash
   pip install ddgs
   ```

2. Clone this skill to your openclaw skills directory:
   ```bash
   git clone https://github.com/YOUR_USERNAME/openclaw-skill-freeUnlimited-websearch ~/.openclaw/skills/freeUnlimited-websearch
   ```

3. Update `search.py` shebang to point to your Python with `ddgs` installed:
   ```bash
   # Edit the first line of search.py to your python path, e.g.:
   #!/path/to/your/venv/bin/python
   ```

4. Enable the skill in `~/.openclaw/openclaw.json`:
   ```json
   {
     "skills": {
       "entries": {
         "freeUnlimited-websearch": {
           "enabled": true
         }
       }
     }
   }
   ```

5. Restart openclaw:
   ```bash
   openclaw gateway restart
   ```

## Usage
The skill is automatically invoked when OpenClaw needs to search the web for current information.

## Output
Returns JSON array of search results with `title`, `href`, and `body` fields.
