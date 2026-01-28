---
name: hackernews
description: Enables Claude to manage Hacker News submissions, comments, and tech community engagement
version: 1.0.0
author: Canifi
category: news
---

# Hacker News Skill

## Overview
Automates Hacker News operations including submitting stories, commenting, voting, and engaging with the tech/startup community through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hackernews/install.sh | bash
```

Or manually:
```bash
cp -r skills/hackernews ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HACKERNEWS_USERNAME "your-username"
canifi-env set HACKERNEWS_PASSWORD "your-password"
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
- Submit stories and links
- Comment on posts
- Upvote content
- View top, new, and best stories
- Search posts and comments
- Access user profile
- View Ask HN and Show HN
- Track karma and submissions

## Usage Examples

### Example 1: Submit a Story
```
User: "Submit this article to Hacker News"
Claude: I'll submit that story.
- Navigate to news.ycombinator.com
- Click submit
- Enter URL and title
- Submit story
- Confirm posted
```

### Example 2: Comment on Post
```
User: "Comment on the top story about AI"
Claude: I'll add that comment.
- Navigate to top stories
- Find AI-related story
- Click to view comments
- Write thoughtful comment
- Submit reply
```

### Example 3: Browse Show HN
```
User: "Check out recent Show HN posts"
Claude: I'll browse Show HN.
- Navigate to show section
- List recent Show HN submissions
- Present projects and demos
- Note upvote counts
```

### Example 4: Search Content
```
User: "Find HN discussions about remote work"
Claude: I'll search for that.
- Navigate to HN search (Algolia)
- Search "remote work"
- Filter by date and relevance
- Present top discussions
```

## Authentication Flow
1. Navigate to news.ycombinator.com/login via Playwright MCP
2. Enter username and password from canifi-env
3. Verify login by checking username in header
4. Maintain session cookies

## Error Handling
- **Login Failed**: Verify credentials, may need to wait
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Wait before posting (HN is strict)
- **Duplicate Submission**: Link to existing post
- **Low Karma**: Some features restricted
- **Dead Post**: Flagged or removed content
- **Comment Depth**: May need to post at different level
- **Submission Failed**: Check URL format

## Self-Improvement Instructions
When encountering new HN features:
1. Document UI changes (HN rarely changes)
2. Note karma thresholds for features
3. Log successful submission patterns
4. Track community guidelines

## Notes
- HN has strict quality standards
- Karma earned through upvotes
- Submissions may be flagged quickly
- Comments can be downvoted with karma
- No edit after brief window
- Rate limits strictly enforced
- Show HN for your own projects
- Ask HN for questions to community
