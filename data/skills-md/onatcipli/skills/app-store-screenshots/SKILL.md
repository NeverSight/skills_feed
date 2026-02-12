---
name: app-store-screenshots
description: >
  App Store screenshot research, competitor analysis, and planning tool for iOS/macOS
  apps. Use this skill when working with App Store screenshots for any of these tasks:
  (1) Finding and analyzing competitor screenshots in your category,
  (2) Downloading competitor screenshots locally for reference,
  (3) Analyzing screenshot strategies (styles, captions, features),
  (4) Planning your screenshot sequence and messaging,
  (5) Generating a local preview website to view and compare screenshots,
  (6) Understanding screenshot requirements and best practices,
  (7) Creating exportable screenshot assets at correct dimensions.
---

# App Store Screenshots

Research competitor screenshots, plan your strategy, and preview your App Store
screenshots using a lightweight local tool.

## Overview

Screenshots are critical for App Store conversion—90% of users don't scroll past
the third screenshot. This skill helps you research what works, plan your strategy,
and preview your screenshots before uploading.

## Workflow 0 — Onboarding Interview

Before starting, gather information about the user's app and goals.

### Questions to Ask

```
1. Is this a new app or an existing app?
   □ New app (focus on competitor research)
   □ Existing app (can also analyze current performance)

2. What is your app's category?
   [Select from App Store categories - see category-codes in references]

3. Describe your app in one sentence:
   [Used to extract keywords for competitor search]

4. What is your app name?
   [Used for folder organization]

5. What are your main competitors? (optional)
   [If known, provide app names or IDs]

6. Do you have Sensor Tower API access?
   □ Yes (enhanced competitor finding)
   □ No (use iTunes API + RSS feeds only)
```

### Output

Create project folder structure:

```
{app_name}_screenshots/
├── competitors/
├── analysis/
├── your_app/
│   ├── iphone/
│   ├── ipad/
│   └── assets/
├── preview/
└── README.md
```

---

## Workflow 1 — Find Competitors

Identify the top competitors in your category to analyze.

### Step 1: Search by Keywords

Extract keywords from app description and search iTunes:

```
GET https://itunes.apple.com/search?term={keywords}&entity=software&country=us&limit=25
```

### Step 2: Fetch Top Charts

Get top apps in the category via RSS feed:

```
GET https://rss.applemarketingtools.com/api/v2/us/apps/top-free/50/apps.json?genre={genreId}
```

### Step 3: Filter & Rank (Optional with Sensor Tower)

If Sensor Tower API available:
```
GET https://app.sensortower.com/api/ios/apps?app_ids={ids}
```

Use download/revenue estimates to find "winning" apps.

### Step 4: Select Top 3 Competitors

Present candidates to user:

```markdown
## Competitor Candidates

| # | App Name | Rating | Reviews | Category Rank |
|---|----------|--------|---------|---------------|
| 1 | Calm | 4.8★ | 1.2M | #1 Health |
| 2 | Headspace | 4.9★ | 850K | #2 Health |
| 3 | Insight Timer | 4.9★ | 450K | #5 Health |

Select 3 competitors to analyze (enter numbers): [1, 2, 3]
```

---

## Workflow 2 — Download & Analyze Screenshots

Download competitor screenshots and generate analysis.

### Step 1: Fetch Screenshot URLs

For each competitor:

```
GET https://itunes.apple.com/lookup?id={appId}&country=us
```

Extract from response:
- `screenshotUrls` — iPhone screenshots
- `ipadScreenshotUrls` — iPad screenshots

### Step 2: Download Screenshots

Save to organized folder structure:

```python
import requests
import os

def download_screenshots(app_id, app_name, output_dir):
    # Fetch app data
    response = requests.get(f"https://itunes.apple.com/lookup?id={app_id}")
    data = response.json()["results"][0]

    # Create directories
    iphone_dir = f"{output_dir}/competitors/{app_name}/iphone"
    ipad_dir = f"{output_dir}/competitors/{app_name}/ipad"
    os.makedirs(iphone_dir, exist_ok=True)
    os.makedirs(ipad_dir, exist_ok=True)

    # Download iPhone screenshots
    for i, url in enumerate(data.get("screenshotUrls", []), 1):
        img = requests.get(url)
        with open(f"{iphone_dir}/{i:02d}.png", "wb") as f:
            f.write(img.content)

    # Download iPad screenshots
    for i, url in enumerate(data.get("ipadScreenshotUrls", []), 1):
        img = requests.get(url)
        with open(f"{ipad_dir}/{i:02d}.png", "wb") as f:
            f.write(img.content)

    # Save metadata
    with open(f"{output_dir}/competitors/{app_name}/metadata.json", "w") as f:
        json.dump(data, f, indent=2)
```

### Step 3: Analyze Each Competitor

For each competitor, analyze and document:

```markdown
## Screenshot Analysis: {App Name}

### Overview
- **iPhone Screenshots:** {count}
- **iPad Screenshots:** {count}
- **Visual Style:** [Device mockup / Lifestyle / UI-only / Hybrid]
- **Color Palette:** [Primary colors observed]

### Screenshot Breakdown

| # | Type | Caption/Text | Feature Shown | Notes |
|---|------|--------------|---------------|-------|
| 1 | {type} | "{caption}" | {feature} | {notes} |
| 2 | {type} | "{caption}" | {feature} | {notes} |
...

### Strategy Analysis
- **Hook (Screenshot 1):** {description}
- **Flow:** {how screenshots progress}
- **Text Style:** {short/long, benefit/feature focused}
- **Device Frames:** {yes/no, style}

### Strengths
- {strength 1}
- {strength 2}

### Weaknesses
- {weakness 1}
- {weakness 2}
```

Save as `competitors/{app_name}/README.md`

---

## Workflow 3 — Compare & Identify Patterns

Generate a cross-competitor analysis.

### Comparison Table

```markdown
## Competitor Comparison

### Visual Style

| Aspect | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|--------------|--------------|--------------|
| Screenshot Count | 8 | 6 | 10 |
| Style | Device mockup | Lifestyle | Hybrid |
| Text Amount | Minimal | Heavy | Medium |
| Color Theme | Blue/Purple | Green/White | Orange/Black |
| Device Frames | Yes | No | Yes |
| Shows Hands | No | Yes | No |

### Caption Patterns

| Screenshot | Competitor 1 | Competitor 2 | Competitor 3 |
|------------|--------------|--------------|--------------|
| 1 (Hook) | "Find Peace" | "Sleep Better" | "Meditate Daily" |
| 2 | "Sleep Stories" | "Guided Sessions" | "Track Progress" |
| 3 | "Daily Calm" | "Reduce Stress" | "Join Community" |

### Common Patterns
1. {pattern 1}
2. {pattern 2}
3. {pattern 3}

### Differentiation Opportunities
1. {opportunity 1}
2. {opportunity 2}
```

Save as `analysis/competitor_comparison.md`

---

## Workflow 4 — Plan Your Screenshots

Based on analysis, create a screenshot plan.

### Screenshot Strategy Framework

```
The "Value-Usage-Trust" Formula:
1. VALUE — What the user gets (hook)
2. USAGE — How it works (key features)
3. TRUST — Social proof (ratings, awards)
```

### Generate Screenshot Plan

```markdown
## Screenshot Plan: {Your App Name}

### Strategy
- **Style:** {chosen style based on analysis}
- **Count:** {recommended: 6-8}
- **Text Approach:** {based on competitor analysis}
- **Differentiator:** {what makes yours unique}

### Screenshot Sequence

#### Screenshot 1: Hook / Value Proposition
- **Caption:** "{suggested caption}"
- **Visual:** {description of what to show}
- **Goal:** Grab attention, communicate core value

#### Screenshot 2: Key Feature #1
- **Caption:** "{suggested caption}"
- **Visual:** {description}
- **Goal:** Show most important feature

#### Screenshot 3: Key Feature #2
- **Caption:** "{suggested caption}"
- **Visual:** {description}
- **Goal:** Demonstrate second key benefit

#### Screenshot 4: Key Feature #3
- **Caption:** "{suggested caption}"
- **Visual:** {description}
- **Goal:** Continue feature story

#### Screenshot 5: Use Case / Lifestyle
- **Caption:** "{suggested caption}"
- **Visual:** {description}
- **Goal:** Show app in context

#### Screenshot 6: Social Proof / Trust
- **Caption:** "{suggested caption}"
- **Visual:** Show ratings, awards, press
- **Goal:** Build credibility

### Design Guidelines
- **Colors:** {recommended palette}
- **Font:** {recommendation}
- **Device Frame:** {yes/no, which style}
- **Safe Zones:** Keep text 120px from edges

### Export Checklist
- [ ] iPhone 6.9" (1290 x 2796 or 1320 x 2868)
- [ ] iPad 13" (2064 x 2752)
- [ ] PNG format, no transparency
- [ ] Under 8 MB each
- [ ] sRGB color space
```

Save as `your_app/plan.md`

---

## Workflow 5 — Generate Preview Website

Create a lightweight local HTML tool for viewing and planning screenshots.

### Features

1. **Competitor Gallery** — View all competitor screenshots side-by-side
2. **Your Screenshots** — Preview your screenshots in device frames
3. **Comparison View** — Compare yours vs competitors
4. **Export Helper** — Guides for correct dimensions

### Generate the Website

Create `preview/index.html` with:

```html
<!-- See templates/preview-website.html for full implementation -->
```

The website includes:
- Responsive grid layout
- Device frame overlays
- Zoom/lightbox functionality
- Tab navigation
- Export dimension reference
- Works offline (no dependencies)

### How to Use

```bash
# Navigate to preview folder
cd {app_name}_screenshots/preview

# Open in browser
open index.html
# or
python -m http.server 8000
# then visit http://localhost:8000
```

---

## Workflow 6 — Export Screenshots

Guide for exporting final screenshots.

### Required Dimensions

| Device | Dimensions | Aspect Ratio |
|--------|------------|--------------|
| **iPhone 6.9" (Required)** | 1290 x 2796 or 1320 x 2868 | 9:19.5 |
| **iPad 13" (Required)** | 2064 x 2752 | 3:4 |

### Export Checklist

```markdown
## Export Checklist

### Technical Requirements
- [ ] Format: PNG (no transparency) or JPEG
- [ ] Size: Under 8 MB per image
- [ ] Color: sRGB color space
- [ ] Resolution: 72 dpi

### iPhone Screenshots
- [ ] 01_hook.png (1290 x 2796)
- [ ] 02_feature1.png (1290 x 2796)
- [ ] 03_feature2.png (1290 x 2796)
- [ ] 04_feature3.png (1290 x 2796)
- [ ] 05_usecase.png (1290 x 2796)
- [ ] 06_trust.png (1290 x 2796)

### iPad Screenshots
- [ ] 01_hook.png (2064 x 2752)
- [ ] 02_feature1.png (2064 x 2752)
- [ ] 03_feature2.png (2064 x 2752)
- [ ] 04_feature3.png (2064 x 2752)
- [ ] 05_usecase.png (2064 x 2752)
- [ ] 06_trust.png (2064 x 2752)

### Final Review
- [ ] Text readable at thumbnail size (min 28pt)
- [ ] Critical content not in top 160px (Dynamic Island)
- [ ] No competitor names or logos
- [ ] Consistent style across all screenshots
- [ ] Screenshots tell a coherent story
```

---

## Quick Reference — APIs

| Task | Endpoint |
|------|----------|
| Search apps | `itunes.apple.com/search?term={q}&entity=software` |
| Lookup app | `itunes.apple.com/lookup?id={id}` |
| Top Free | `rss.applemarketingtools.com/api/v2/{cc}/apps/top-free/{limit}/apps.json` |
| Top Paid | `rss.applemarketingtools.com/api/v2/{cc}/apps/top-paid/{limit}/apps.json` |
| By Category | Add `?genre={genreId}` to RSS feeds |

---

## Folder Structure

```
{app_name}_screenshots/
├── competitors/
│   ├── {competitor_1}/
│   │   ├── iphone/
│   │   │   ├── 01.png
│   │   │   └── ...
│   │   ├── ipad/
│   │   │   └── ...
│   │   ├── metadata.json
│   │   └── README.md
│   ├── {competitor_2}/
│   └── {competitor_3}/
├── analysis/
│   ├── competitor_comparison.md
│   └── patterns.md
├── your_app/
│   ├── plan.md
│   ├── iphone/
│   │   ├── 01_hook.png
│   │   └── ...
│   ├── ipad/
│   │   └── ...
│   └── assets/
│       ├── ui_screenshots/
│       └── photos/
├── preview/
│   ├── index.html
│   └── exports/
└── README.md
```

---

## Reference Files

| File | Purpose |
|------|---------|
| [screenshot-specs.md](references/screenshot-specs.md) | All device sizes and technical requirements |
| [analysis-templates.md](references/analysis-templates.md) | Templates for competitor analysis |
| [itunes-api.md](references/itunes-api.md) | API endpoints for fetching screenshots |
| [preview-website.html](templates/preview-website.html) | Lightweight preview tool template |
