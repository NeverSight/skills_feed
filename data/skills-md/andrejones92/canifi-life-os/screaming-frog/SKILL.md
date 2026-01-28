---
name: screaming-frog
description: Crawl and analyze websites with Screaming Frog SEO Spider.
category: marketing
---
# Screaming Frog Skill

Crawl and analyze websites with Screaming Frog SEO Spider.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/screaming-frog/install.sh | bash
```

Or manually:
```bash
cp -r skills/screaming-frog ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SCREAMING_FROG_LICENSE "your_license_key"
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

1. **Site Crawling**: Crawl websites and analyze structure
2. **Technical SEO Audit**: Find broken links, errors, and issues
3. **On-page Analysis**: Analyze titles, meta descriptions, headings
4. **Redirect Chains**: Map and analyze redirects
5. **XML Sitemap**: Generate XML sitemaps

## Usage Examples

### Crawl Site
```
User: "Crawl example.com for SEO issues"
Assistant: Initiates crawl and returns findings
```

### Find Broken Links
```
User: "Find all broken links on my website"
Assistant: Returns list of 404 errors and broken links
```

### Analyze Titles
```
User: "Show me pages with duplicate titles"
Assistant: Returns pages with title issues
```

### Generate Sitemap
```
User: "Create an XML sitemap from the crawl"
Assistant: Generates sitemap file
```

## Authentication Flow

1. Purchase license from Screaming Frog
2. Install desktop application
3. Enter license key to unlock full features
4. CLI available for automation

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| License Invalid | Wrong license | Verify license key |
| Crawl Blocked | Robots.txt | Check crawl permissions |
| Memory Error | Site too large | Increase memory allocation |
| Timeout | Slow response | Adjust timeout settings |

## Notes

- Desktop application (Windows, Mac, Linux)
- Free version crawls 500 URLs
- Paid version unlimited URLs
- CLI for automation
- Integration with APIs
- Custom extraction support
