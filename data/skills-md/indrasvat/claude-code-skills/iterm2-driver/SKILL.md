---
name: iterm2-driver
description: Drive iTerm2 programmatically using Python scripts to automate terminal tasks, run tests, or manage sessions. Use when the user needs to test TUIs, CLIs, terminal apps, terminal automation, interactive terminal testing, terminal UI, command-line interface automation, REPL automation, screen monitoring, or terminal screenshots. Supports iTerm2 and iterm automation.
---

# iTerm2 Driver Skill

This skill enables you to fully control the iTerm2 terminal emulator using its Python API. You can create windows, tabs, and splits, inject commands, read screen content, and interact with running applications (CLI/TUI/REPL).

## CRITICAL: Script Format

Every Python script **MUST** use `uv` with inline metadata:

```python
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "iterm2",
#   "pyobjc",
# ]
# ///
```

For screenshots, add `"pyobjc-framework-Quartz"` to dependencies.

**Execution:** `uv run script_name.py`

## CRITICAL: Docstring Planning

Every script MUST begin with a comprehensive docstring covering: Tests, Verification Strategy, Screenshots, Key Bindings, and Usage. See `examples/00-comprehensive-template.py` for the canonical format.

## Core Concepts

- **Connection**: `iterm2.run_until_complete(main)` for standalone scripts
- **Hierarchy**: `App` -> `Window` -> `Tab` -> `Session`
- **Key Methods**:
    - `session.async_send_text("command\n")`: Send input
    - `session.async_get_screen_contents()`: Read screen
    - `session.async_split_pane(vertical=True/False)`: Create splits
    - `session.async_close()`: Close session

## Quick Reference

| Task | Code |
|------|------|
| Get app | `app = await iterm2.async_get_app(connection)` |
| Get window | `window = app.current_terminal_window` |
| New tab | `tab = await window.async_create_tab()` |
| Get session | `session = tab.current_session` |
| Send text | `await session.async_send_text("ls\n")` |
| Read screen | `screen = await session.async_get_screen_contents()` |
| Get line | `screen.line(i).string` |
| Ctrl+C | `await session.async_send_text("\x03")` |
| Enter (TUI) | `await session.async_send_text("\r")` |

## CRITICAL: Multi-Level Cleanup

Always use try-except-finally with multi-level cleanup:

```python
try:
    # Test logic
except Exception as e:
    print(f"ERROR: {e}")
    raise
finally:
    await session.async_send_text("\x03")  # Ctrl+C
    await asyncio.sleep(0.2)
    await session.async_send_text("q")     # TUI quit
    await asyncio.sleep(0.2)
    await session.async_send_text("exit\n")
    await asyncio.sleep(0.2)
    await session.async_close()
```

## CRITICAL: TUI Layout Verification

TUI elements (borders, modals, status bars) frequently misalign. **Always verify layout integrity.**

Common issues:
- Box corners not connected to edges (╭ not followed by ─)
- Help modals cut off at screen edges
- Status bars with gaps or truncated content

Quick check pattern:

```python
BOX_CORNERS = '┌┐└┘╭╮╰╯╔╗╚╝'
BOX_HORIZONTAL = '─═━'

# Check corner connectivity
for j, char in enumerate(line):
    if char in '┌╭╔' and j + 1 < len(line) and line[j+1] not in BOX_HORIZONTAL:
        print(f"LAYOUT ERROR: Corner not connected at col {j}")
```

See `references/verification-patterns.md` for complete layout verification helpers.

## Screenshot Capture (Quartz)

Use `pyobjc-framework-Quartz` for window-targeted screenshots (not full screen). The pattern uses `CGWindowListCopyWindowInfo` to find the iTerm2 window ID, then `screencapture -l <id>`. See `examples/00-comprehensive-template.py` or `references/templates.md` for complete implementation.

## Test Reporting

Track results with a `results` dict containing `passed`, `failed`, and `tests` list. Use `log_result(name, status, details)` for each test and `print_summary()` to show final counts and return exit code. See `references/reporting.md` for complete patterns including JSON/JUnit export.

## Special Keys Reference

| Key | Code |
|-----|------|
| Enter | `\r` (prefer over `\n` in TUIs) |
| Esc | `\x1b` |
| Ctrl+C | `\x03` |
| Ctrl+X | `\x18` |
| Up Arrow | `\x1b[A` |
| Down Arrow | `\x1b[B` |

## Guidelines

1. **Always use `uv run`** - never suggest running python directly
2. **Check window exists** - `if window is not None:` before operations
3. **Use `\r` for Enter in TUIs** - safer than `\n` for prompts
4. **Dump screen on failure** - always show what went wrong
5. **Track resources** - close all created sessions in finally block
6. **Verify layout** - check box-drawing characters connect properly

## Script Storage

| Scope | Location |
|-------|----------|
| Project-specific | `./.claude/automations/{script}.py` |
| General utility | `~/.claude/automations/{script}.py` |

Use descriptive names: `watch_build_logs.py`, `drive_k9s_debug.py`

## Examples & References

**Examples** (`examples/` directory):
- `00-comprehensive-template.py` - Complete template with all patterns
- `01-basic-tab.py` - Simple tab creation
- `02-dev-layout.py` - Multi-pane layout
- `03-repl-driver.py` - REPL automation with verification
- `04-nano-automation.py` - TUI editor with cleanup
- `05-screen-monitor.py` - ScreenStreamer for real-time monitoring
- `06-environment-vars.py` - Environment variable handling
- `07-cleanup-sessions.py` - Session cleanup patterns
- `08-badge-control.py` - Badge and tab control
- `09-special-keys.py` - Special key sequences
- `10-session-reuse.py` - Session reuse patterns
- `11-layout-verification.py` - TUI layout alignment checks

**References** (`references/` directory):
- `templates.md` - Complete copy-paste script templates
- `verification-patterns.md` - All verification helpers including layout checks
- `reporting.md` - Test reporting patterns, JSON/JUnit export

## Links

- [iTerm2 Python API](https://iterm2.com/python-api/)
- [iTerm2 Scripting Tutorial](https://iterm2.com/python-api/tutorial/index.html)
- [UV Documentation](https://github.com/astral-sh/uv)
