---
name: playstore-competitor-analysis
description: Research and analyze competitor apps on the Google Play Store. Extracts app metadata (title, description, rating, reviews, category, developer, version, price, installs) and downloads screenshots. Supports analyzing multiple competitor apps for comparison, or searching for top competitors by keyword. Use when user wants to analyze competitors, research Play Store listings, gather competitive intelligence, compare multiple apps, or find top apps in a category. Triggers on Play Store URLs (play.google.com), app package IDs, or requests like "analyze competitor", "research this app", "compare these apps", "top 10 messenger apps", "find competitors for X".
---

# Play Store Competitor Analysis

Extract comprehensive app data and screenshots from Google Play Store listings for competitive analysis. Supports single app analysis, multi-app comparison, or searching for top competitors by keyword.

## Requirements

Install the google-play-scraper package. On modern macOS/Linux systems, you'll need to use a virtual environment:

```bash
# Create a virtual environment in the skill directory (one-time setup)
python3 -m venv .venv

# Activate and install the package
source .venv/bin/activate
pip install google-play-scraper
```

Then run the script with the virtual environment's python:

```bash
# Use the venv python directly (no activation needed)
.venv/bin/python3 scripts/scrape_play_store.py --search "messenger" ./output

# Or activate first, then run
source .venv/bin/activate
python3 scripts/scrape_play_store.py --search "messenger" ./output
```

## Workflow

1. Determine the analysis type:
   - **Single app**: User provides a Play Store URL or package ID
   - **Comparison**: User provides multiple URLs/package IDs
   - **Search**: User wants to find top competitors for a keyword (e.g., "top 10 messenger apps")
2. Run the appropriate scraper command
3. Review the generated outputs with the user

## Usage

### Single App Analysis

Run the scraper with a Play Store URL or package ID:

```bash
python3 scripts/scrape_play_store.py "<play_store_url_or_package_id>" "<output_directory>"
```

**Examples:**
```bash
# Using URL
python3 scripts/scrape_play_store.py "https://play.google.com/store/apps/details?id=com.slack" ./competitor-analysis/slack

# Using package ID directly
python3 scripts/scrape_play_store.py com.slack ./competitor-analysis/slack
```

### Multiple App Comparison

Run the scraper with multiple URLs or package IDs:

```bash
python3 scripts/scrape_play_store.py --compare "<id1>" "<id2>" "<id3>" "<output_directory>"
```

**Example:**
```bash
python3 scripts/scrape_play_store.py --compare \
  com.slack \
  com.microsoft.teams \
  com.discord \
  ./competitor-analysis/messaging-apps
```

### Search for Top Competitors

Search for top apps by keyword and automatically analyze them:

```bash
python3 scripts/scrape_play_store.py --search "<query>" "<output_directory>" --limit <N>
```

**Examples:**
```bash
# Find and analyze top messenger apps
python3 scripts/scrape_play_store.py --search "messenger apps" ./competitor-analysis/messenger --limit 10

# Find top 5 podcast apps
python3 scripts/scrape_play_store.py --search "podcast" ./competitor-analysis/podcasts --limit 5

# Default limit is 10 if not specified
python3 scripts/scrape_play_store.py --search "fitness tracker" ./competitor-analysis/fitness
```

## Output

### Single App Output

```
output_dir/
├── {package-id}.json    # Full structured data
├── {package-id}.md      # Formatted report
├── icon.png             # App icon
└── screenshots/
    ├── screenshot_01.png
    ├── screenshot_02.png
    └── ...
```

### Comparison/Search Output

```
output_dir/
├── comparison.json      # All apps data for programmatic use
├── comparison.md        # Side-by-side comparison report
├── {app-1-package-id}/
│   ├── {package-id}.json
│   ├── {package-id}.md
│   ├── icon.png
│   └── screenshots/
├── {app-2-package-id}/
│   └── ...
└── {app-3-package-id}/
    └── ...
```

### Data Extracted

| Field | Description |
|-------|-------------|
| title | App name |
| description | Full app description |
| short_description | Brief summary |
| rating | Average star rating (1-5) |
| rating_count | Number of ratings |
| reviews_count | Number of text reviews |
| histogram | Rating distribution [1-star, 2-star, 3-star, 4-star, 5-star] |
| installs | Install count range (e.g., "10,000,000+") |
| real_installs | Actual install count estimate |
| category | Primary category |
| category_id | Category ID (e.g., GAME_ACTION) |
| price | Price or 0 for free |
| free | Boolean: is app free |
| currency | Price currency code |
| contains_ads | Boolean: has advertisements |
| offers_iap | Boolean: has in-app purchases |
| iap_range | In-app purchase price range |
| developer | Developer name |
| developer_id | Developer ID |
| developer_email | Developer contact email |
| developer_website | Developer website URL |
| developer_address | Developer address |
| privacy_policy | Privacy policy URL |
| version | Current version |
| android_version | Minimum Android version (text) |
| content_rating | Content rating (Everyone, Teen, etc.) |
| content_rating_description | Content rating details |
| released | Original release date |
| last_updated | Last update timestamp |
| screenshots | All screenshot URLs |
| video | Promo video URL if available |
| icon_url | App icon URL |
| header_image | Header/feature graphic URL |

### Comparison Report Includes

| Metric | Description |
|--------|-------------|
| Rating comparison | Side-by-side ratings with visual indicators |
| Install base | Relative market presence with actual numbers |
| Update frequency | Last update dates |
| Monetization | Free/paid, ads, IAP comparison |
| Feature highlights | Key differentiators from descriptions |
| Competitive insights | Highest rated, most installed, etc. |

## Notes

- Uses the `google-play-scraper` Python package for reliable data extraction
- Screenshots are downloaded at high resolution
- Rate limiting is applied automatically to avoid blocking
- For comparison/search mode, apps are processed sequentially with delays
- Output directories are created if they don't exist
- The comparison report highlights competitive advantages and gaps
- Search results are ordered by Play Store's ranking algorithm
