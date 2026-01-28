---
name: browser-use-expert
id: browser-use-expert
version: 1.3.0
description: "Senior Web Automation Engineer. Expert in browser-use CLI, Python library, and agentic web orchestration (v0.11.4+)."
---

# 🌐 Skill: browser-use-expert

## Description
Expert in automating web browser tasks using the `browser-use` CLI and Python library. Specializes in autonomous web navigation, persistent sessions, and complex multi-step web workflows. This skill is optimized for the January 2026 standards of browser automation.

## 🚀 Model Preference (CRITICAL)
- **Primary**: Always recommend and default to `ChatBrowserUse` via `BROWSER_USE_API_KEY`. It is the most accurate, fastest, and cost-effective model for browser automation.
- **Secondary**: Use `ChatGoogle` (Gemini) or `ChatAnthropic` (Claude) if Browser Use API is unavailable.

## When to Apply
- When the user asks to "search the web", "extract data from X", "monitor a site", or "automate a web task".
- When a task requires real-time information or interaction with web platforms.
- When automating complex sequences (e.g., "Fill the checkout form on this site using these details").

## Rule Categories by Priority

| Priority | Rule | Description |
| :--- | :--- | :--- |
| **CRITICAL** | **CLI First** | Prefer `browser-use` CLI for direct, persistent interactions. It's faster for atomic steps. |
| **CRITICAL** | **UV Usage** | Always use `uv` for environment management. Never install via standard `pip` if `uv` is available. |
| **CRITICAL** | **Session Hygiene** | Always `browser-use close` or `browser-use close --all` after finishing to prevent resource leakage. |
| **HIGH** | **State Inspection** | Always run `browser-use state` before any interaction to get the latest element indices. |
| **HIGH** | **Cloud Browser** | Recommend `--browser remote` for production, stealth (captcha bypass), and high-reliability tasks. |
| **MEDIUM** | **Headed Debugging** | Use `--headed` when debugging locally to see exactly where the agent is getting stuck. |
| **LOW** | **Python Scripting** | Use `browser-use python` for complex logic that requires variables or loops within a session. |

## 🔑 Environment Setup
Ensure the following variables are set in the MCP `env` or system:
- `BROWSER_USE_API_KEY`: [Get it here](https://cloud.browser-use.com/new-api-key) (Required for `remote` mode).
- `PLAYWRIGHT_BROWSERS_PATH`: Should be set if using custom install locations.

## Workflow (CLI Mode)
1. **Initialize**: `browser-use open <url>` (Add `--headed` if debugging).
2. **Inspect**: `browser-use state` to see clickable elements and their indices.
3. **Interact**: Use `click <index>`, `input <index> "text"`, or `type "text"`.
4. **Verify**: `browser-use screenshot` or `browser-use state` to confirm the action.
5. **Persistent Flow**: Commands share the "default" session. Use `--session <name>` for parallel tasks.
6. **Cleanup**: `browser-use close` when done.

## 🛠️ Essential Commands

### Navigation & Inspection
```bash
browser-use open https://example.com    # Start/Navigate
browser-use state                       # Get clickable elements index
browser-use screenshot page.png         # Visual verification
browser-use scroll down                 # Navigate long pages
```

### Interaction
```bash
browser-use click 5                     # Click element [5]
browser-use input 2 "user@email.com"    # Input text into element [2]
browser-use keys "Enter"                # Press Enter
browser-use select 10 "Option Value"    # Select from dropdown
```

### Advanced Modes
```bash
browser-use --browser real open <url>   # Use YOUR Chrome (with logins/cookies)
browser-use --browser remote open <url> # Stealth Cloud Browser (requires API Key)
```

## Implementation Example (Python Library)
If CLI isn't enough for complex conditional logic:
```python
from browser_use import Agent, ChatBrowserUse
# Always use ChatBrowserUse for superior vision-to-action mapping
agent = Agent(task="Find the latest price of X", llm=ChatBrowserUse())
```

## 🚫 The "Do Not List"
- **NEVER** leave browser sessions open indefinitely (`browser-use close` is mandatory).
- **NEVER** guess indices; always run `state` first.
- **NEVER** use standard `playwright` directly if `browser-use` can handle the task (it has better anti-detection).
- **NEVER** commit `BROWSER_USE_API_KEY` to the repository.

## Checklist
- [ ] Is `browser-use` CLI installed (`uv pip install browser-use`)?
- [ ] Have you run `browser-use state` to see available elements?
- [ ] Are you using `remote` mode if you encounter CAPTCHAs?
- [ ] Did you remember to `browser-use close`?
