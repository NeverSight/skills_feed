---
name: notion
description: Enables Claude to create, edit, and manage pages and databases in Notion via MCP and Playwright
category: productivity
---

# Notion Skill

## Overview
Claude can fully interact with Notion via the Notion MCP integration (preferred) or Playwright browser automation. Create pages, manage databases, organize workspaces, and maintain your knowledge base. This is the PRIMARY tool for LifeOS data storage.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/notion/install.sh | bash
```

Or manually:
```bash
cp -r skills/notion ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NOTION_EMAIL "your-email@example.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Create and edit pages
- Manage databases and properties
- Search across workspace
- Add and organize content blocks
- Create database entries
- Filter and sort database views
- Share and collaborate on pages
- Create templates
- Manage page properties
- Link between pages
- Add comments and mentions
- Export and import content

## Usage Examples

### Example 1: Create Page
```
User: "canifi, create a note about today's meeting"
Claude: Uses Notion MCP to create page in appropriate database.
        Returns: "Created 'Meeting Notes - [Date]' in Journal"
```

### Example 2: Add Database Entry
```
User: "canifi, add 'Atomic Habits' to my reading list"
Claude: Uses MCP to add entry to Reading List database.
        Confirms: "Added 'Atomic Habits' to Reading List"
```

### Example 3: Search Content
```
User: "canifi, find my notes about productivity"
Claude: Searches Notion for "productivity".
        Reports: "Found 8 pages: Research Hub, Ideas, Goals..."
```

### Example 4: Update Page
```
User: "canifi, mark the project proposal as complete"
Claude: Updates page status property to Complete.
        Confirms: "Project Proposal marked as complete"
```

## Integration Methods

### Primary: Notion MCP (Preferred)
```
Tools: mcp__notion__*
- notion-search: Search pages and databases
- notion-fetch: Get page content
- notion-create-pages: Create new pages
- notion-update-page: Update existing pages
- notion-create-database: Create databases
- notion-update-database: Update database schema
```

### Secondary: Playwright Browser Automation
Use when MCP cannot accomplish the task (complex UI interactions, specific views).

## LifeOS Database Reference
```
Daily: Habits, Journal, Weekly Review
Work: Goals, Tasks, Projects
Mind: Ideas, Concepts, Research Hub, Media Library, Reading List, Entertainment, Personal Development, Blogs
Health: Exercise Library, Workout Log, Sleep Log, Body Metrics, Supplements, Nutrition, Recipes, Meal Plans, Grocery Lists
Relationships: Personal CRM, Gift Ideas
Environment: Wardrobe, Trips
Finance: Subscriptions, Budgets
```

## Error Handling
- **MCP Failed**: Fall back to Playwright automation
- **Page Not Found**: Search for similar pages, ask user
- **Permission Denied**: Notify user of access issue
- **Rate Limited**: Wait and retry with backoff
- **Sync Issues**: Refresh and retry
- **Database Full**: Notify user, suggest archiving

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Notion:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific MCP calls or selectors that work better
4. Note any API limitations discovered

## Notes
- MCP is preferred for all Notion operations
- Browser automation only when MCP insufficient
- LifeOS uses Notion as central data hub
- All research outputs stored in Notion
- Pages support rich formatting and embeds
- Databases have flexible schemas
- Synced blocks for shared content
- Relations link databases together
