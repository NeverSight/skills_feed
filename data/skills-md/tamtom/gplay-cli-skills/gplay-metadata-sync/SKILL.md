---
name: gplay-metadata-sync
description: Metadata and localization sync (including Fastlane format) for Google Play Store listings. Use when updating app descriptions, screenshots, or managing multi-locale metadata.
---

# Metadata Sync for Google Play

Use this skill when you need to update or sync Play Store metadata and localizations.

## Fastlane Directory Structure

```
fastlane/metadata/android/
├── en-US/
│   ├── title.txt
│   ├── short_description.txt
│   ├── full_description.txt
│   ├── video.txt
│   └── images/
│       ├── phoneScreenshots/
│       │   ├── 1.png
│       │   └── 2.png
│       ├── sevenInchScreenshots/
│       ├── tenInchScreenshots/
│       ├── tvScreenshots/
│       ├── wearScreenshots/
│       ├── icon.png
│       └── featureGraphic.png
├── es-ES/
│   ├── title.txt
│   └── ...
└── fr-FR/
    └── ...
```

## Export Metadata from Play Store

```bash
# Export all listings to Fastlane format
gplay sync export-listings \
  --package com.example.app \
  --dir ./fastlane/metadata/android

# Export images
gplay sync export-images \
  --package com.example.app \
  --dir ./fastlane/metadata/android
```

## Import Metadata to Play Store

```bash
# Validate before importing (offline check)
gplay validate listing \
  --dir ./fastlane/metadata/android \
  --locale en-US

# Import all listings
gplay sync import-listings \
  --package com.example.app \
  --dir ./fastlane/metadata/android

# Import images
gplay sync import-images \
  --package com.example.app \
  --dir ./fastlane/metadata/android
```

## Compare Local vs Remote

```bash
# See what would change
gplay sync diff-listings \
  --package com.example.app \
  --dir ./fastlane/metadata/android
```

## Manual Metadata Management

### List all listings
```bash
gplay listings list \
  --package com.example.app \
  --edit $EDIT_ID
```

### Get specific locale
```bash
gplay listings get \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US
```

### Update listing
```bash
gplay listings update \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --json @listing.json
```

### listing.json format
```json
{
  "title": "My Awesome App",
  "shortDescription": "A short description under 80 characters",
  "fullDescription": "A full description under 4000 characters...",
  "video": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

## Image Management

### Upload screenshots
```bash
gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --file screenshot1.png

gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --file screenshot2.png
```

### Image types
- `phoneScreenshots` - Phone screenshots (required)
- `sevenInchScreenshots` - 7" tablet screenshots
- `tenInchScreenshots` - 10" tablet screenshots
- `tvScreenshots` - TV screenshots
- `wearScreenshots` - Wear OS screenshots
- `icon` - App icon
- `featureGraphic` - Feature graphic (1024x500)

### List images
```bash
gplay images list \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots
```

### Delete image
```bash
gplay images delete \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --image-id IMAGE_ID \
  --confirm
```

## App Details

### Get app details
```bash
gplay details get \
  --package com.example.app \
  --edit $EDIT_ID
```

### Update contact info
```bash
gplay details update \
  --package com.example.app \
  --edit $EDIT_ID \
  --contact-email support@example.com \
  --contact-phone "+1234567890" \
  --contact-website "https://example.com"
```

## Character Limits

Validate against Google Play limits:

| Field | Limit |
|-------|-------|
| Title | 50 characters |
| Short Description | 80 characters |
| Full Description | 4000 characters |

```bash
# Validate before upload
gplay validate listing \
  --dir ./fastlane/metadata/android \
  --locale en-US
```

## Workflow Example

Complete metadata update workflow:

```bash
# 1. Export current metadata
gplay sync export-listings \
  --package com.example.app \
  --dir ./metadata

# 2. Edit files locally
vi ./metadata/en-US/full_description.txt

# 3. Validate changes
gplay validate listing \
  --dir ./metadata \
  --locale en-US

# 4. See what will change
gplay sync diff-listings \
  --package com.example.app \
  --dir ./metadata

# 5. Import changes
gplay sync import-listings \
  --package com.example.app \
  --dir ./metadata
```

## Multi-Locale Management

### Create new locale
1. Copy existing locale directory:
   ```bash
   cp -r fastlane/metadata/android/en-US fastlane/metadata/android/es-ES
   ```

2. Translate all text files

3. Import:
   ```bash
   gplay sync import-listings \
     --package com.example.app \
     --dir ./fastlane/metadata/android
   ```

### Supported Locales
Use Play Console locale codes:
- `en-US` - English (United States)
- `es-ES` - Spanish (Spain)
- `fr-FR` - French (France)
- `de-DE` - German (Germany)
- `ja-JP` - Japanese (Japan)
- etc.

## Best Practices

1. **Keep metadata in version control** - Track changes over time
2. **Validate before importing** - Catch character limit errors
3. **Use consistent formatting** - Follow style guide
4. **Test on different devices** - Screenshots should represent actual app
5. **Update regularly** - Keep descriptions current with features
6. **Localize properly** - Don't use machine translation without review
