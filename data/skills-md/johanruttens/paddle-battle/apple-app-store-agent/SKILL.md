---
name: apple-app-store-agent
description: Comprehensive agent for preparing and generating all assets needed for Apple App Store submission. Use when user needs to prepare an iOS/iPadOS/macOS app for App Store release, including generating app metadata (descriptions, promotional text, keywords), creating app icons, designing screenshots, preparing privacy policy URLs, and organizing fastlane-compatible folder structures. Triggers on requests like "prepare my app for App Store", "create App Store screenshots", "generate app description", "make app icon", or "set up fastlane metadata".
---

# Apple App Store Agent

Automate preparation of all assets required for Apple App Store submission: metadata, screenshots, icons, and fastlane configuration.

## Workflow Decision Tree

```
User Request
    │
    ├─► "Full App Store preparation" ──► Run complete workflow (all steps)
    │
    ├─► "Generate metadata" ──► Step 1: Gather app info → Generate descriptions, keywords
    │
    ├─► "Create screenshots" ──► Step 2: Get app screens → Generate styled screenshots  
    │
    ├─► "Make app icon" ──► Step 3: Get concept → Generate icon in all sizes
    │
    ├─► "Set up fastlane" ──► Step 4: Create folder structure with all metadata files
    │
    └─► "Prepare review info" ──► Step 5: Generate review notes, demo credentials template
```

## Step 1: Generate App Metadata

Gather information from user about their app:
- App name and bundle identifier
- Core functionality (what problem it solves)
- Target audience
- Key features (3-5 main features)
- Competitor apps (for positioning)

### Output Files

Generate these localized text files (start with en-US):

| File | Max Length | Purpose |
|------|------------|---------|
| `name.txt` | 30 chars | App name on App Store |
| `subtitle.txt` | 30 chars | Brief tagline below app name |
| `description.txt` | 4000 chars | Full app description |
| `promotional_text.txt` | 170 chars | Updatable promo text (top of description) |
| `keywords.txt` | 100 chars | Comma-separated, no spaces after commas |
| `release_notes.txt` | 4000 chars | What's new in this version |
| `support_url.txt` | URL | Support page link |
| `marketing_url.txt` | URL | Marketing page link |
| `privacy_url.txt` | URL | Privacy policy link (REQUIRED) |

### Writing Guidelines

**Description structure:**
1. Opening hook (1-2 sentences) - immediately convey value
2. Key features with bullet points (use ● not -)
3. Social proof if available
4. Call to action

**Keywords strategy:**
- Use all 100 characters
- No duplicates of words in app name
- Include common misspellings
- Mix head terms and long-tail
- Separate with commas, no spaces

## Step 2: Create App Screenshots

### Required Dimensions (2024/2025)

**iPhone (Required: ONE of these):**
- 6.9" display: 1320 x 2868 px (portrait) / 2868 x 1320 px (landscape) - iPhone 16 Pro Max
- 6.5" display: 1242 x 2688 px (portrait) / 2688 x 1242 px (landscape) - fallback

**iPad (Required if app runs on iPad):**
- 13" display: 2064 x 2752 px (portrait) / 2752 x 2064 px (landscape)

**Optional (auto-scaled from above):**
- All other iPhone sizes scale from 6.9"/6.5"
- All other iPad sizes scale from 13"

### Screenshot Design Process

1. **Identify key screens** - Focus on 5-10 most compelling features
2. **Create device mockups** - Use scripts/generate_screenshot_mockup.py
3. **Add marketing text** - Short, benefit-focused headlines
4. **Maintain consistency** - Same style, colors, typography across all

### Screenshot Content Guidelines

- First 3 screenshots are critical (visible in search results)
- Show actual app UI (Apple rejects misleading screenshots)
- Text overlays: 6-8 words max per screenshot
- Include device frame for professional look
- Use app's brand colors for backgrounds

See `references/screenshot-specs.md` for detailed dimensions and file naming.

## Step 3: Generate App Icon

### Icon Specifications

**App Store icon:** 1024 x 1024 px (PNG, no transparency, no rounded corners)

Apple applies corner radius automatically. Submit square icon.

### Icon Design Principles

- Simple, recognizable silhouette
- Limited color palette (2-3 colors)
- No text (illegible at small sizes)
- Avoid photos (don't scale well)
- Test at 29x29 px for clarity

Use `scripts/generate_app_icon.py` to create icon or provide concept for AI generation.

## Step 4: Set Up Fastlane Structure

Create this folder structure for `fastlane deliver`:

```
fastlane/
├── Appfile
├── Deliverfile
├── metadata/
│   ├── copyright.txt
│   ├── primary_category.txt
│   ├── secondary_category.txt
│   ├── en-US/
│   │   ├── name.txt
│   │   ├── subtitle.txt
│   │   ├── description.txt
│   │   ├── keywords.txt
│   │   ├── promotional_text.txt
│   │   ├── release_notes.txt
│   │   ├── privacy_url.txt
│   │   ├── support_url.txt
│   │   └── marketing_url.txt
│   └── review_information/
│       ├── demo_password.txt
│       ├── demo_user.txt
│       ├── email_address.txt
│       ├── first_name.txt
│       ├── last_name.txt
│       ├── notes.txt
│       └── phone_number.txt
└── screenshots/
    └── en-US/
        ├── iphone_6.9_inch/
        │   ├── 1_feature_one.png
        │   ├── 2_feature_two.png
        │   └── ...
        └── ipad_13_inch/
            ├── 1_feature_one.png
            └── ...
```

Use `scripts/init_fastlane_structure.py` to generate this structure.

## Step 5: App Review Preparation

### Review Information Checklist

- [ ] Demo account credentials (if login required)
- [ ] Notes explaining non-obvious features
- [ ] Contact information for reviewer questions
- [ ] Any required hardware/conditions explained

### Common Rejection Reasons to Address

1. **Incomplete metadata** - Fill ALL required fields
2. **Placeholder content** - Remove "lorem ipsum" or test data
3. **Broken links** - Test privacy_url and support_url
4. **Login issues** - Demo account must work
5. **Misleading screenshots** - Must show actual app

### Privacy Policy Requirements

Privacy URL is **mandatory**. Must include:
- What data is collected
- How data is used
- Third-party sharing
- Data retention policy
- Contact information

Provide GitHub Pages URL or hosted policy link.

## App Categories

Primary category is required. See `references/app-categories.md` for full list.

Common categories:
- Games (with subcategory)
- Business
- Education
- Entertainment
- Finance
- Health & Fitness
- Lifestyle
- Productivity
- Social Networking
- Utilities

## Scripts

| Script | Purpose |
|--------|---------|
| `init_fastlane_structure.py` | Create complete fastlane folder structure |
| `generate_screenshot_mockup.py` | Add device frames and text to screenshots |
| `generate_app_icon.py` | Create app icon in required size |
| `validate_metadata.py` | Check character limits and required fields |

## Quick Start

For full preparation, run:

```bash
python scripts/init_fastlane_structure.py --app-name "My App" --bundle-id "com.company.app"
```

Then populate the generated text files with content.
