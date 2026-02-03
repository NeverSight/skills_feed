---
name: nicegui-development
description: Use when building UI with NiceGUI, creating components, fixing styling issues, or when user mentions "nicegui", "quasar", "tailwind", "ui.row", "ui.column", "gap spacing", "state management", "controller", "dialog", "modal", "ui component", "ui layout".
---

# NiceGUI Development Best Practices

## Core Philosophy

**Understand the user workflow before building. Same data MUST look the same everywhere. Extract business logic from UI into testable controllers.**

## Quick Start

```bash
# Search for existing similar UI
grep -r "ui.card" src/ | head -20
grep -r "ui.dialog" src/ | head -20

# Check for existing components
ls src/*/ui/components/
```

## Critical Rules - NiceGUI Styling

```python
# ALWAYS use inline style for gap (NiceGUI bug #2171)
with ui.row().classes("items-center").style("gap: 0.75rem"):
    ui.icon("info")
    ui.label("Message")

# NEVER use Tailwind gap-* classes
with ui.row().classes("items-center gap-3"):  # Breaks on Ubuntu!

# Gap conversion: gap-2->0.5rem, gap-3->0.75rem, gap-4->1rem

# CORRECT: Explicit height for percentage children
with ui.card().style("height: 80vh"):
    with ui.scroll_area().style("height: 100%"):
        ui.label("Content")

# NEVER use height: 100% inside max-height container
with ui.card().style("max-height: 80vh"):
    with ui.scroll_area().style("height: 100%"):  # Collapses to 0!

# CORRECT: Side-by-side with charts (use min-width: 0)
with ui.element("div").style("display: flex; width: 100%; gap: 24px"):
    with ui.element("div").style("flex: 1; min-width: 0"):
        ui.highchart(options)
```

## Critical Rules - Product Thinking

```python
# BEFORE building any data display, answer:
# 1. Where else does this data type appear?
# 2. Should this be ONE component with modes?
# 3. Can user navigate from reference to source?

# Create reusable component with modes
class ItemReference:
    def __init__(self, item, mode: Literal["LIBRARY", "REFERENCE", "PREVIEW"]):
        if mode == "LIBRARY":
            # Full card with edit actions
        elif mode == "REFERENCE":
            # Compact with navigation to source

# NEVER copy-paste UI code
# If same data in 2+ places, extract component
```

## Critical Rules - UI Architecture

```python
# Extract business logic to controller
class PageController:
    async def handle_task_change(self, new_task: str) -> PageUpdate:
        data = await self.fetcher.fetch_data(new_task)
        return PageUpdate.refresh_all(data)

# UI layer is thin - delegates to controller
async def on_task_change(e):
    logger.info(f"User selected task: {e.value}")
    update = await controller.handle_task_change(e.value)
    apply_ui_update(update)

# NEVER put business logic in UI handlers
async def on_task_change(e):
    overview = await service.get_overview()  # Fetching in UI!
    if overview.tasks:
        selected = overview.tasks[0]  # Logic in UI!
    chart.refresh(...)  # All mixed together
```

## Modal/Dialog Button Docking

```python
# Primary actions MUST be always visible
with ui.dialog() as dialog, ui.card().style(
    "height: 85vh; display: flex; flex-direction: column;"
):
    # Scrollable content
    with ui.scroll_area().style("flex: 1; overflow-y: auto;"):
        # ... form content ...

    # Sticky bottom action bar
    with ui.element("div").style(
        "position: sticky; bottom: 0; padding: 1rem; "
        "border-top: 1px solid var(--border-color);"
    ):
        with ui.row().classes("justify-end"):
            ui.button("Cancel", on_click=dialog.close)
            ui.button("Save", on_click=save_handler)
```

## Checklists

### Data Display Component Checklist
- [ ] Listed ALL locations where this data appears
- [ ] Designed component with modes for each context
- [ ] User can navigate from reference to source
- [ ] Same icon, typography, color coding everywhere
- [ ] Actions appropriate for each mode (edit only in library)

### UI Architecture Checklist
- [ ] Business logic in controller, not UI handlers
- [ ] Data fetching returns Pydantic models
- [ ] All user actions logged at start of handlers
- [ ] UI feedback when actions deferred/blocked
- [ ] No implicit boolean flags (use state enums)
- [ ] Controller has integration tests

### NiceGUI Styling Checklist
- [ ] No `gap-*` Tailwind classes (use inline style)
- [ ] No `height: 100%` inside `max-height` container
- [ ] No `table-layout: fixed` with percentage widths in ui.html()
- [ ] Side-by-side layouts use `min-width: 0` on flex children
- [ ] Modal buttons are docked (always visible)

## Reference Files

- [references/nicegui-styling.md](references/nicegui-styling.md) - Gap spacing, height issues, flexbox
- [references/product-thinking.md](references/product-thinking.md) - Component design, data display checklist
- [references/ui-architecture.md](references/ui-architecture.md) - Controllers, state management, testing

**Remember**: Ask "where else does this data appear?" before building any UI component.
