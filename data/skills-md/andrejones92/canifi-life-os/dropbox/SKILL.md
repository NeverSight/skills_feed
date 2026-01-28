---
name: dropbox
description: Cloud storage and file synchronization service.
category: utilities
---
# Dropbox Skill

Cloud storage and file synchronization service.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/dropbox/install.sh | bash
```

Or manually:
```bash
cp -r skills/dropbox ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DROPBOX_ACCESS_TOKEN "your_token"
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

1. **File Operations**: Upload, download, manage files
2. **Folder Sync**: Sync folders across devices
3. **Share Links**: Create sharing links
4. **Paper Docs**: Create and edit documents
5. **Search Files**: Find content quickly

## Usage Examples

### Upload File
```
User: "Upload this file to Dropbox"
Assistant: Uploads to specified location
```

### Share File
```
User: "Create a share link for this folder"
Assistant: Generates sharing URL
```

### Search
```
User: "Find my tax documents"
Assistant: Returns matching files
```

### Download
```
User: "Download the project files"
Assistant: Retrieves files from Dropbox
```

## Authentication Flow

1. OAuth2 authentication
2. Access token for API
3. App permissions scoped
4. Refresh token support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid token | Re-authorize |
| File Not Found | Wrong path | Verify location |
| Storage Full | Quota exceeded | Upgrade or cleanup |
| Permission Denied | Access issue | Check sharing |

## Notes

- Full REST API
- Official SDKs
- Paper for docs
- Smart Sync
- Team features
- Version history
