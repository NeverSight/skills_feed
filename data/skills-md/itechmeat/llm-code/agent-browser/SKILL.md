---

name: agent-browser
description: "Headless browser automation CLI for AI agents. Covers commands, refs, sessions, snapshots, cloud providers, profiles. Keywords: agent-browser, browser automation, refs, snapshot."
version: "0.8.4"
release_date: "2026-01-27"

# Agent Browser

Headless browser automation CLI for AI agents. Fast Rust CLI with Node.js fallback.

Works with: Claude Code, Cursor, GitHub Copilot, OpenAI Codex, Google Gemini, opencode.

## Quick Navigation

| Topic        | Reference                                     |
| ------------ | --------------------------------------------- |
| Installation | [installation.md](references/installation.md) |
| Commands     | [commands.md](references/commands.md)         |
| Refs         | [refs.md](references/refs.md)                 |
| Advanced     | [advanced.md](references/advanced.md)         |

## When to Use

- Automating browser tasks in AI agent workflows
- Web scraping with AI-friendly output
- Testing web applications with LLM agents
- Managing multiple browser sessions with isolated auth

## Core Concepts

### Refs (Element References)

The `snapshot` command returns an accessibility tree where each element has a unique ref like `@e1`, `@e2`:

- **Deterministic** - ref points to exact element from snapshot
- **Fast** - no DOM re-query needed
- **AI-friendly** - LLMs can reliably parse and use refs

### Architecture

Client-daemon architecture:

1. **Rust CLI** - parses commands, communicates with daemon
2. **Node.js Daemon** - manages Playwright browser instance

Daemon starts automatically and persists between commands.

## Quick Example

```bash
# Navigate and get snapshot
agent-browser open example.com
agent-browser snapshot                    # Get accessibility tree with refs
agent-browser click @e2                   # Click by ref from snapshot
agent-browser fill @e3 "test@example.com" # Fill input by ref
agent-browser get text @e1                # Get text by ref
agent-browser screenshot page.png         # Save screenshot
agent-browser close
```

## AI Workflow Pattern

Optimal workflow for AI agents:

```bash
# 1. Navigate and get snapshot
agent-browser open example.com
agent-browser snapshot -i --json   # AI parses tree and refs

# 2. AI identifies target refs from snapshot

# 3. Execute actions using refs
agent-browser click @e2
agent-browser fill @e3 "input text"

# 4. Get new snapshot if page changed
agent-browser snapshot -i --json
```

## Headed Mode (Debugging)

```bash
agent-browser open example.com --headed
```

## JSON Output

Use `--json` for machine-readable output:

```bash
agent-browser snapshot --json
agent-browser get text @e1 --json
agent-browser is visible @e2 --json
```

## Critical Prohibitions

- Do not use CSS/XPath selectors when refs are available (use @e1, @e2, etc.)
- Do not forget to close sessions when done
- Do not assume element positions without taking a fresh snapshot
- Do not use old refs after page navigation or content changes (re-snapshot)

## Common Commands

```bash
# Navigation
agent-browser open <url>
agent-browser back / forward / reload
agent-browser close

# Interaction
agent-browser click <sel>
agent-browser fill <sel> <text>
agent-browser press <key>
agent-browser hover <sel>
agent-browser select <sel> <val>
agent-browser download <sel> <path>  # v0.7+

# Info
agent-browser get text <sel>
agent-browser get url
agent-browser get title
agent-browser is visible <sel>

# Snapshots & Screenshots
agent-browser snapshot -i --json
agent-browser screenshot [path]
```

## Links

- Official docs: https://agent-browser.dev/
- Changelog: https://agent-browser.dev/changelog
- GitHub: https://github.com/vercel-labs/agent-browser
