---
name: anytype
description: Enables Claude to create and manage objects in Anytype via Playwright MCP
category: productivity
---

# Anytype Skill

## Overview
Claude can manage your Anytype space to create objects, define types, and build a private knowledge base. A local-first, open-source tool for managing all types of information.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/anytype/install.sh | bash
```

Or manually:
```bash
cp -r skills/anytype ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ANYTYPE_EMAIL "your-email@example.com"
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
- Create objects of any type
- Define custom types and relations
- Build sets and collections
- Create templates
- Link objects together
- Use graph view
- Search across content
- Organize with tags
- Create databases
- Build widgets
- Export and import
- Sync across devices

## Usage Examples

### Example 1: Create Object
```
User: "Create a Note object about the meeting"
Claude: Creates Note object with meeting content.
        Confirms: "Note created: Meeting Notes"
```

### Example 2: Build Set
```
User: "Create a set of all my Task objects"
Claude: Creates Set with Task type filter.
        Returns: "Task set created with 15 objects"
```

### Example 3: Define Type
```
User: "Create a 'Recipe' type with ingredients and instructions relations"
Claude: Creates custom type with relations.
        Confirms: "Recipe type created with 2 relations"
```

### Example 4: Link Objects
```
User: "Link this project to the client object"
Claude: Creates relation between objects.
        Confirms: "Project linked to Client"
```

## Authentication Flow
1. Claude navigates to Anytype web/app via Playwright MCP
2. Enters ANYTYPE_EMAIL for authentication
3. Handles encryption key if required
4. Maintains session for operations

## Selectors Reference
```javascript
// Object list
'.object-list'

// Object content
'.object-content'

// Block
'.block-container'

// Type selector
'.type-selector'

// Relation
'.relation-container'

// Set view
'.set-view'

// Graph view
'.graph-view'

// Search
'.search-input'

// Widget
'.widget-container'

// Link block
'.link-block'
```

## Anytype Concepts
```
Object      // Any piece of content
Type        // Template for objects
Relation    // Property/field on objects
Set         // Filtered collection of objects
Collection  // Manual grouping of objects
Template    // Reusable object structure
Graph       // Visual object connections
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Object Not Found**: Search with variations, ask user
- **Type Error**: Check type definition, suggest fix
- **Sync Failed**: Wait and retry
- **Encryption Error**: Verify key

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Anytype:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific type configurations
4. Note useful relation patterns

## Notes
- Local-first with E2E encryption
- Open-source and self-hostable
- Object-based data model
- Flexible type system
- Relations for connections
- Graph for visualization
- Sets for filtered views
- Cross-platform apps
