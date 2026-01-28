---
name: behance
description: Showcase and discover creative work on Behance - manage portfolio projects, explore design trends, and connect with creatives
category: design
---

# Behance Skill

## Overview
Enables Claude to interact with Behance for creative portfolio management and inspiration discovery, including browsing projects, managing your portfolio, and connecting with the creative community.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/behance/install.sh | bash
```

Or manually:
```bash
cp -r skills/behance ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BEHANCE_EMAIL "your-email@example.com"
canifi-env set BEHANCE_PASSWORD "your-password"
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
- Browse and search creative projects
- Manage portfolio projects and galleries
- Save and organize mood boards
- Follow creatives and brands
- Access Adobe Creative Cloud integration
- Discover trending design work

## Usage Examples

### Example 1: Find Branding Inspiration
```
User: "Find branding projects for tech startups"
Claude: I'll search for tech branding projects.
1. Opening Behance via Playwright MCP
2. Searching "tech startup branding"
3. Filtering by appreciation count
4. Saving top projects to mood board
5. Summarizing key design trends
```

### Example 2: Update Portfolio
```
User: "Check the stats on my latest Behance project"
Claude: I'll review your project analytics.
1. Navigating to your Behance profile
2. Opening your latest project
3. Viewing project statistics
4. Summarizing views, appreciations, and comments
```

### Example 3: Explore Trends
```
User: "What design styles are trending on Behance this month?"
Claude: I'll analyze current design trends.
1. Browsing Behance featured galleries
2. Reviewing curated collections
3. Identifying common styles and techniques
4. Compiling trend report for you
```

## Authentication Flow
1. Navigate to behance.net via Playwright MCP
2. Sign in with Adobe ID
3. Enter email and password
4. Handle 2FA if enabled (via iMessage)
5. Sync with Adobe Creative Cloud session

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate with Adobe ID
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Project Not Found**: Search alternatives or verify URL
- **Upload Failed**: Check file requirements and retry

## Self-Improvement Instructions
When Behance updates its platform:
1. Document new gallery and project features
2. Update search and filter capabilities
3. Track Adobe integration changes
4. Log new portfolio customization options

## Notes
- Behance uses Adobe ID authentication
- Projects can be synced from Adobe apps
- Featured placement requires community engagement
- Some features require Adobe Creative Cloud
- Live streaming features available for some accounts
