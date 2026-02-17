---
name: stealth-browser
description: Invisible Chrome automation for web scraping via CDP. Use when WebFetch fails or gets blocked (403, 429, Cloudflare, bot protection, JS-rendered pages). Launches your real Chrome install completely hidden, sends commands via Chrome DevTools Protocol. Sites see a normal browser with real extensions - no detectable automation. Learns which domains block and skips straight to stealth on future requests. Also handles form filling, clicking, screenshots, and scraping dynamic content.
compatibility: macOS only. Requires Google Chrome, agent-browser (npm), python3, d2m (npm).
allowed-tools: Bash Read Write
metadata:
  author: stevebutterworth
  version: "1.0"
---

# stealth-browser

Invisible Chrome automation via CDP. Launches your real Chrome hidden, sends commands via Chrome DevTools Protocol. Sites see a normal browser - no detectable automation.

> **macOS only.** Uses AppleScript and `open -g` to hide Chrome.

## Memory

Read `~/.claude/skills/stealth-browser/LEARNED.md` at the start of every task. If it doesn't exist, create it with a `# Learned` header.

**Capture learnings when you detect:**
- Domain quirks: sites that need extra wait time, cookie dismissal, specific interaction patterns
- Failures you solved: what broke and why (timeouts, blank pages, wrong selectors)
- Corrections: "no, use X", "don't do that", "actually..."
- Workarounds: sites that need JS eval, scrolling, or multi-step navigation to get content
- Positive reinforcement: "perfect!", "exactly right", "that's the way"

**Before appending, check:**
- Is this reusable? (not a one-time instruction)
- Is it already in LEARNED.md? (don't duplicate)
- Can I extract the general principle? (not just the specific fix)

**Format:** One line, actionable. Write the rule, not the story.
- Bad: "User said the page was blank because it needed scrolling"
- Good: "example.com lazy-loads content - scroll to bottom before extracting"

Don't ask permission. Append and move on.

## Core Workflow

```bash
# 1. Read a page as markdown (most common)
stealth-browser read <url>

# 2. Full automation (open, interact, close)
stealth-browser open <url> --hidden
agent-browser --cdp 9222 snapshot -i
agent-browser --cdp 9222 click @e1
stealth-browser close
```

`stealth-browser` is at `scripts/stealth-browser` relative to this skill. Use full path:
```bash
~/.claude/skills/stealth-browser/scripts/stealth-browser read <url>
```

## Commands

```bash
stealth-browser read <url>              # Fetch as markdown (waits for JS render)
stealth-browser open <url> --hidden     # Launch hidden Chrome
stealth-browser close                   # Stop Chrome
stealth-browser status                  # Check state
stealth-browser screenshot [path]       # CDP screenshot (auto unhide/re-hide)
stealth-browser hide / unhide           # Toggle visibility
stealth-browser doctor                  # Check dependencies
stealth-browser setup                   # Reset Chrome profile
```

## After Opening: CDP Commands via agent-browser

```bash
agent-browser --cdp 9222 open <url>           # Navigate
agent-browser --cdp 9222 snapshot -i          # Get interactive elements
agent-browser --cdp 9222 click @e1            # Click by ref
agent-browser --cdp 9222 fill @e2 "text"      # Fill input
agent-browser --cdp 9222 type @e2 "text"      # Type without clearing
agent-browser --cdp 9222 press Enter          # Press key
agent-browser --cdp 9222 scroll down 500      # Scroll
agent-browser --cdp 9222 get text @e1         # Get text
agent-browser --cdp 9222 get url              # Get current URL
agent-browser --cdp 9222 eval "document.title" # Run JavaScript
agent-browser --cdp 9222 screenshot path.png  # Screenshot
agent-browser --cdp 9222 wait 2000            # Wait
agent-browser --cdp 9222 back                 # Navigate back
```

Always re-snapshot after navigation or DOM changes - element refs change.

## Chrome Persistence

Chrome stays running and hidden after `read` or `open --hidden`:
- **First operation**: brief flash during Chrome startup (small window, top-left corner)
- **All subsequent operations**: completely invisible, instant
- **Close when done**: `stealth-browser close`

## Domain Blocklist (learning)

Blocked domains are remembered at `data/blocked-domains.txt`. A PreToolUse hook intercepts future WebFetch calls to those domains and tells Claude to use stealth-browser directly.

See [hooks/README.md](hooks/README.md) for Claude Code integration setup.
See [README.md](README.md) for full human documentation.
