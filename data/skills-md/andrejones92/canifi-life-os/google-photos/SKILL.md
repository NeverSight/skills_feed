---
name: google-photos
description: Enables Claude to browse, organize, and manage photos and videos in Google Photos via Playwright MCP
category: google
---

# Google Photos Skill

## Overview
Claude can manage your Google Photos library to browse images, create albums, search photos, and organize your memories. This includes using AI-powered search, creating collages, and managing storage.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-photos/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-photos ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Browse and view photos and videos
- Search photos by content, people, places, or dates
- Create and manage albums
- Share albums and photos
- Edit photos with built-in tools
- Create collages, animations, and movies
- Organize by people and faces
- Archive and delete photos
- View storage usage
- Download photos and albums
- Add photos to favorites
- View photo metadata and location

## Usage Examples

### Example 1: Find Photos
```
User: "Find photos from my trip to Hawaii"
Claude: Searches for "Hawaii" and/or date range of trip.
        Reports: "Found 156 photos from Hawaii. Showing beach, sunset,
        and hiking categories..."
```

### Example 2: Create Album
```
User: "Create an album called 'Best of 2024' with my favorite photos"
Claude: Creates album "Best of 2024", adds starred/favorited photos.
        Returns: "Created album with 43 photos: [link]"
```

### Example 3: Share Album
```
User: "Share the vacation album with my family"
Claude: Opens album, creates share link or adds specific people.
        Confirms: "Album shared. Link: [shareable link]"
```

### Example 4: Search by Content
```
User: "Find all photos with dogs"
Claude: Uses AI search for "dog", shows results.
        Reports: "Found 28 photos containing dogs across 12 dates"
```

## Authentication Flow
1. Claude navigates to photos.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Photos operations

## Selectors Reference
```javascript
// Search box
'input[aria-label="Search your photos"]'

// Photo grid
'.p137Zd' // Photo thumbnails

// Individual photo
'[data-latest-bg]'

// Create button
'[aria-label="Create"]'

// Album option
'[aria-label="Album"]'

// Share button
'[aria-label="Share"]'

// Favorite button
'[aria-label="Add to favorites"]'

// Delete button
'[aria-label="Delete"]'

// Download button
'[aria-label="Download"]'

// Edit button
'[aria-label="Edit"]'

// Albums navigation
'[aria-label="Albums"]'

// Upload button
'[aria-label="Upload"]'
```

## Search Operators
```
dog                    // Content search
beach sunset          // Multiple terms
"vacation 2024"       // Exact phrase
selfie                // Photo type
screenshot            // Photo type
food                  // Content category
wedding               // Event type
Tokyo                 // Location
2024-06               // Date (June 2024)
last week             // Relative date
videos                // Media type
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Photo Not Found**: Broaden search, check archive and trash
- **Album Creation Failed**: Retry, verify photo selection
- **Share Failed**: Check sharing settings, verify recipients
- **Storage Full**: Notify user, suggest storage management
- **Download Failed**: Retry, try individual photos vs batch

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Photos:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific search terms that work well
4. Note any face recognition or AI search improvements

## Notes
- Free storage ended June 2021; now counts against Google One quota
- AI search can find objects, scenes, text in photos
- Face grouping requires enabling in settings
- Partner sharing allows automatic sharing with one person
- Location data from EXIF or estimated from content
- Original quality vs storage saver affects file size
- Live Photos from iPhone preserved as motion photos
- Trash items deleted after 60 days
