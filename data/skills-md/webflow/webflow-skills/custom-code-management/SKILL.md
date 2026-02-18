---
name: custom-code-management
description: Add, review, or remove inline custom scripts on a Webflow site (up to 10,000 chars). Use for analytics, tracking pixels, chat widgets, or any custom JavaScript.
---

# Custom Code Management

## Concepts

Webflow custom code: **register** (store script) → **apply** (attach to site). Inline scripts only via MCP (max 10,000 chars).

## Important note

**ALWAYS use Webflow MCP tools for all operations:**
Use the following tools for all operations:
- `data_scripts_tool` with actions `list_registered_scripts` / `list_applied_scripts` - List scripts
- `data_scripts_tool` with action `add_inline_site_script` - Register inline script (no `<script>` tags)
- `data_scripts_tool` with action `delete_all_site_scripts` - Remove ALL scripts (no selective delete)
- `data_sites_tool` with action `list_sites` - List available sites

## Instructions

### View Scripts
1. Call `data_sites_tool` with action `list_sites` if needed, then call both list tools in parallel
2. Display registration and application status

### Add Script
1. Gather: name, code, location (header/footer)
2. Validate: under 10,000 chars, no `<script>` tags
3. Preview with character count, require **"add"** to confirm
4. Call `data_scripts_tool` with action `add_inline_site_script` with displayName, sourceCode, version, location, canCopy
5. Remind user to publish

### Remove Scripts
1. List current scripts
2. Warn: removes ALL scripts (no selective delete)
3. Require **"delete all"** to confirm
4. Remind user to publish

## Constraints

- Max 10,000 characters per script
- Do NOT include `<script>` tags (Webflow adds them)
- displayName + version must be unique
- Site-level only (no page-specific via MCP)
- Hosted scripts not available via MCP

## Response Format

After adding a script, respond with the script name, location, and version. Suggest using the `safe-publish` skill to publish changes.
