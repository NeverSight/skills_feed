---
name: nextdoor
description: Enables Claude to manage Nextdoor neighborhood posts and community engagement
version: 1.0.0
author: Canifi
category: social
---

# Nextdoor Skill

## Overview
Automates Nextdoor operations including posting to neighborhood, browsing local discussions, and engaging with community through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/nextdoor/install.sh | bash
```

Or manually:
```bash
cp -r skills/nextdoor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NEXTDOOR_EMAIL "your-email@example.com"
canifi-env set NEXTDOOR_PASSWORD "your-password"
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
- Create neighborhood posts
- Comment on discussions
- Browse local classifieds
- View and post to groups
- Recommend local businesses
- Search neighborhood content
- Report issues
- View local events

## Usage Examples

### Example 1: Create a Post
```
User: "Post to Nextdoor about the lost dog sighting"
Claude: I'll create that neighborhood post.
- Navigate to nextdoor.com
- Click create post
- Select category (Lost & Found)
- Write about lost dog sighting
- Include location details
- Publish post
```

### Example 2: Browse Classifieds
```
User: "Check what's for sale on Nextdoor"
Claude: I'll browse local classifieds.
- Navigate to For Sale section
- Browse recent listings
- Filter by category if requested
- Present available items
```

### Example 3: Recommend Business
```
User: "Recommend the local coffee shop on Nextdoor"
Claude: I'll post that recommendation.
- Navigate to Recommendations
- Search for coffee shop
- Write positive review
- Post recommendation
```

### Example 4: View Events
```
User: "What local events are happening this weekend?"
Claude: I'll check local events.
- Navigate to Events section
- Browse weekend events
- Filter by nearby area
- Present event listings
```

## Authentication Flow
1. Navigate to nextdoor.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle verification if location-based
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify neighborhood feed access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify credentials and address
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Location Verification**: May need address confirmation
- **Post Failed**: Check community guidelines
- **Category Required**: Select appropriate category
- **Neighborhood Issue**: Verify address membership
- **Rate Limited**: Wait before posting again

## Self-Improvement Instructions
When encountering new Nextdoor features:
1. Document new UI elements
2. Add support for new post types
3. Log successful community patterns
4. Update for platform changes

## Notes
- Nextdoor requires address verification
- Posts visible to nearby neighborhoods
- Categories help organize content
- Business pages separate from personal
- Safety alerts for local issues
- Recommendations build local reputation
- Groups for specific interests
