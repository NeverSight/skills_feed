---
name: instapaper
description: Save web articles for distraction-free reading with Instapaper's clean reading experience.
category: productivity
---
# Instapaper Skill

Save web articles for distraction-free reading with Instapaper's clean reading experience.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/instapaper/install.sh | bash
```

Or manually:
```bash
cp -r skills/instapaper ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INSTAPAPER_CONSUMER_KEY "your_consumer_key"
canifi-env set INSTAPAPER_CONSUMER_SECRET "your_consumer_secret"
canifi-env set INSTAPAPER_ACCESS_TOKEN "your_access_token"
canifi-env set INSTAPAPER_ACCESS_SECRET "your_access_secret"
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

1. **Save Articles**: Save web pages and articles to your Instapaper account for offline reading
2. **Folder Organization**: Create and manage folders to organize saved content by topic or project
3. **Highlight & Notes**: Highlight important passages and add notes to saved articles
4. **Text-to-Speech**: Convert articles to audio for listening on the go
5. **Archive & Search**: Archive read articles and search your entire library

## Usage Examples

### Save Article
```
User: "Save this article to Instapaper: https://example.com/tech-news"
Assistant: Saves article with clean formatting for distraction-free reading
```

### Create Folder
```
User: "Create an Instapaper folder called 'Research Papers'"
Assistant: Creates new folder for organizing research content
```

### Highlight Text
```
User: "Highlight the key findings in my saved article about climate change"
Assistant: Adds highlights to specified passages in the article
```

### List Unread
```
User: "Show me my unread Instapaper articles"
Assistant: Returns list of unread articles with titles and save dates
```

## Authentication Flow

1. Request API access at instapaper.com/api
2. Receive consumer key and secret via email
3. Implement xAuth for user authentication
4. Store all four credentials securely

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify consumer key and secret |
| 403 Rate Limited | Too many requests | Implement backoff strategy |
| 1040 Invalid URL | URL cannot be parsed | Validate URL format before saving |
| 1041 Article Failed | Content extraction failed | Try alternative URL or manual save |

## Notes

- Premium subscription required for full-text search and unlimited highlights
- API access requires application approval
- Speed reading feature available in premium tier
- Kindle integration available for e-reader sync
- Clean text extraction removes ads and clutter
