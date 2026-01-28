---
name: ios-app-store-competitor-research
description: Research competitor apps on the Apple App Store. Extracts app metadata (title, subtitle, description, rating, reviews, category, developer, version, price) and downloads all screenshots. Use when user wants to analyze a competitor's app, research app store listings, gather competitive intelligence, or download app screenshots. Triggers on App Store URLs (apps.apple.com) or requests like "research this app", "analyze competitor", "get app store info", "download app screenshots".
---

# iOS App Store Competitor Research

Extract comprehensive app data and screenshots from Apple App Store listings for competitive analysis.

## Workflow

1. Get the App Store URL from the user
2. Run the scraper script to fetch data and download screenshots
3. Review the generated outputs with the user

## Usage

Run the scraper with an App Store URL:

```bash
python3 scripts/scrape_app_store.py "<app_store_url>" "<output_directory>"
```

**Example:**
```bash
python3 scripts/scrape_app_store.py "https://apps.apple.com/us/app/slack/id618783545" ./competitor-analysis/slack
```

## Output

The script generates in the output directory:

```
output_dir/
├── {app-slug}.json      # Full structured data
├── {app-slug}.md        # Formatted report
├── icon.png             # App icon
└── screenshots/
    ├── screenshot_01.png
    ├── screenshot_02.png
    └── ...
```

### Data Extracted

| Field | Description |
|-------|-------------|
| title | App name |
| subtitle | App tagline |
| description | Full app description |
| rating | Average star rating (1-5) |
| rating_count | Number of ratings |
| category | Primary category |
| genres | All categories |
| price | Price or "Free" |
| developer | Developer name |
| version | Current version |
| size_bytes | App size |
| age_rating | Content rating (4+, 12+, 17+) |
| minimum_os_version | Required iOS version |
| release_notes | What's New text |
| languages | Supported languages |
| screenshots | All screenshot URLs |
| bundle_id | App bundle identifier |

## Multiple Apps

To research several competitors, run the script for each app:

```bash
python3 scripts/scrape_app_store.py "https://apps.apple.com/us/app/competitor-a/id123" ./research/competitor-a
python3 scripts/scrape_app_store.py "https://apps.apple.com/us/app/competitor-b/id456" ./research/competitor-b
```

## Notes

- The script uses the iTunes Lookup API as the primary data source (most reliable)
- Screenshots are downloaded at the highest available resolution
- Both iPhone and iPad screenshots are captured when available
- Output directory is created if it doesn't exist
