---
name: google-forms
description: |
  Create and manage Google Forms programmatically via MCP. Use when: (1) creating survey forms,
  (2) adding questions/sections to forms, (3) getting form responses, (4) converting AskUserQuestion
  to shareable forms. Covers setup, all tools, item ordering, and API limitations.
---

# Google Forms MCP

## Setup

1. Enable **Google Forms API** + **Google Drive API** at console.cloud.google.com
2. Create OAuth 2.0 credentials (Desktop app type)
3. Get refresh token:
   ```bash
   cd ~/.claude/mcp/google-forms-mcp
   bun install && bun run build
   GOOGLE_CLIENT_ID="..." GOOGLE_CLIENT_SECRET="..." bun run token
   ```
4. Add to `.mcp.json` (use full path, not `~`):
   ```json
   {
     "mcpServers": {
       "google-forms-mcp": {
         "command": "bun",
         "args": ["/Users/USERNAME/.claude/mcp/google-forms-mcp/build/index.js"],
         "env": {
           "GOOGLE_CLIENT_ID": "...",
           "GOOGLE_CLIENT_SECRET": "...",
           "GOOGLE_REFRESH_TOKEN": "..."
         }
       }
     }
   }
   ```
5. Run `/mcp reset` to load

## Tools

| Tool | Description |
|------|-------------|
| `create_form` | Create form (returns formId) |
| `update_form` | Update title/description |
| `get_form` | Get form structure |
| `list_forms` | List all forms |
| `delete_form` | Delete form permanently |
| `add_section` | Visual divider (no page break) |
| `add_page` | Page break (requires Next button) |
| `add_text_question` | Free text input |
| `add_multiple_choice_question` | Radio or checkbox |
| `update_question` | Modify existing question |
| `delete_question` | Remove question by index |
| `get_form_responses` | Get submitted responses |

## Item Ordering (CRITICAL)

**All items are added at index 0.** The LAST item you add appears FIRST.

For a multi-section form, add in reverse order:

```
1. create_form → update_form (description)
2. Additional Notes (last item)
3. Last section questions (e.g., 4.2, 4.1)
4. Last section header (Section 4)
5. Previous section questions (e.g., 3.4, 3.3, 3.2, 3.1)
6. Previous section header (Section 3)
7. ... continue for all sections ...
8. First section questions (e.g., 1.3, 1.2, 1.1)
9. First section header (Section 1) ← ADD LAST, APPEARS FIRST
```

## Multiple Choice Options

Two formats supported:

```javascript
// Simple strings
options: ["Option A", "Option B", "Option C"]

// With descriptions (renders as "Label – Description")
options: [
  { label: "Option A", description: "Details about A" },
  { label: "Option B", description: "Details about B" }
]
```

Parameters:
- `includeOther: true` - Adds "Other" with text field
- `multiSelect: true` - Checkboxes (multi-select)
- `multiSelect: false` - Radio buttons (single choice, default)

## API Limitations

| Error | Cause | Solution |
|-------|-------|----------|
| `Only info.title can be set when creating a form` | Can't set description on create | Use `update_form` after `create_form` |
| `Displayed text cannot contain newlines` | Options can't have `\n` | Use " – " (en-dash) to separate label from description |
| `Cannot set option.value when isOther is true` | Other option can't have value | Fixed in MCP - just use `includeOther: true` |

## Section vs Page

- **`add_section`** - Visual divider only, stays on same page (uses `textItem`)
- **`add_page`** - Creates page break, user clicks "Next" (uses `pageBreakItem`)

For single-page surveys, always use `add_section`.
