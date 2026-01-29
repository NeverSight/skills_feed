---
name: shoqai-automation
description: Automate browsing and article searching on shoqai.com with screenshot capture
---

# Shoqai Automation

This skill automates web interactions on shoqai.com. It opens the website, clicks Explore, searches for articles by name, opens them, and captures screenshots at each step.

## Usage

```bash
# Find and open Tesla article (default)
node automate-shoqai.js

# Find specific article
node automate-shoqai.js "Apple"
node automate-shoqai.js "Microsoft"
```

## Installation

```bash
npm install
npx playwright install chromium
mkdir screenshots
```

## Features

- Automated browser navigation with Playwright
- Handles links that open in new tabs
- Automatic screenshot capture at each step
- Configurable article search

## Screenshots

Screenshots are saved to the `screenshots/` folder:
- `1-homepage.png` - Homepage loaded
- `2-after-explore-click.png` - After clicking Explore
- `3-article-opened.png` - Article opened
- `4-final.png` - Final state

## Requirements

- Node.js (v14 or higher)
- npm
- Internet connection
