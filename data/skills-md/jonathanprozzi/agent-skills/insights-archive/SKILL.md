---
name: insights-archive
description: Archive Claude Code /insights reports for historical tracking. Supports archiving, listing, comparing, and opening reports.
license: MIT
metadata:
  author: jonathanprozzi
  version: "1.0.0"
argument-hint: "[archive|list|open|diff] [args...]"
allowed-tools: "Bash, Read"
---

# Insights Archive

Archive and manage Claude Code `/insights` reports to track how your usage patterns evolve over time.

## Usage

```
/insights-archive archive      # Save current report with timestamp
/insights-archive list         # See all archived reports
/insights-archive open         # Open current report in browser
/insights-archive open <date>  # Open archived report by date
/insights-archive diff <d1> <d2>  # Compare two archived reports
/insights-archive              # Show help
```

## Commands

### archive

Saves the current `/insights` report with a timestamp.

```
/insights-archive archive
```

**Output:**
```
Archived to: ~/.claude/usage-data/archives/report-2026-02-04-1335.html
```

**Note:** Run `/insights` first to generate a fresh report before archiving.

### list

Shows all archived reports with their dates.

```
/insights-archive list
```

**Output:**
```
Archived insights reports:

  2026-02-01-1422
  2026-02-04-1335

Use '/insights-archive open <date>' to view one.
```

### open

Opens the current report or an archived report by date.

```
/insights-archive open           # Opens current report
/insights-archive open current   # Same as above
/insights-archive open 2026-02-04  # Opens archived report matching date
```

### diff

Opens two archived reports side-by-side for manual comparison.

```
/insights-archive diff 2026-02-01 2026-02-04
```

Both reports open in browser tabs for comparison.

---

## Why Archive?

Tracking how your Claude Code usage patterns evolve over time is valuable:

- **See workflow improvements** — Are git operations decreasing as you add custom skills?
- **Track friction resolution** — Did the suggestions from last month's report get addressed?
- **Measure learning** — How are your interaction patterns maturing?

This aligns with the "knowledge compounds" thesis — your usage data is another form of knowledge that benefits from historical context.

---

## Prerequisites

Requires the `insights-archive` shell script in your PATH.

**Setup (if not already installed):**

```bash
# Clone dotfiles or copy the script
curl -o ~/.local/bin/insights-archive \
  https://raw.githubusercontent.com/jonathanprozzi/dotfiles/main/bin/insights-archive
chmod +x ~/.local/bin/insights-archive
```

Or if using jonathanprozzi/dotfiles, the script is at `bin/insights-archive`.

---

## Implementation

Execute the command using the shell script:

```bash
insights-archive <command> [args]
```

Parse the user's arguments and pass them through. Report the output back to the user.

**Commands map directly:**
- `/insights-archive archive` → `insights-archive archive`
- `/insights-archive list` → `insights-archive list`
- `/insights-archive open <date>` → `insights-archive open <date>`
- `/insights-archive diff <d1> <d2>` → `insights-archive diff <d1> <d2>`

If no arguments provided, show the help output from the script.
