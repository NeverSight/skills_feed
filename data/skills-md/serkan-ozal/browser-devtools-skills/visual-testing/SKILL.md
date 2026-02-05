---
name: visual-testing
description: Visual testing, UI verification, and design comparison using screenshots and Figma integration. Use when the user wants to verify UI appearance, compare with Figma designs, test responsive layouts, check for visual regressions, or validate design implementation.
allowed-tools: Bash(browser-devtools-cli:*)
---

# Visual Testing Skill

Perform visual testing, UI verification, and design comparison using screenshots, responsive testing, and Figma integration.

## When to Use

This skill activates when:
- User wants to verify UI appearance
- User asks to compare page with design or Figma
- User needs responsive design testing
- User wants to check for visual regressions
- User mentions UI bugs or styling issues
- User asks about design parity
- User wants to validate implementation against design

## Capabilities

### Screenshot Capture
```bash
browser-devtools-cli content take-screenshot --name "homepage"
browser-devtools-cli content take-screenshot --name "element" --selector ".hero"
browser-devtools-cli content take-screenshot --name "fullpage" --full-page
browser-devtools-cli content take-screenshot --name "photo" --type jpeg --quality 80
browser-devtools-cli content save-as-pdf --name "page" --format A4
```

### Responsive Testing
```bash
browser-devtools-cli interaction resize-viewport --width 375 --height 667   # Mobile
browser-devtools-cli interaction resize-viewport --width 768 --height 1024  # Tablet
browser-devtools-cli interaction resize-viewport --width 1920 --height 1080 # Desktop
```

### Figma Design Comparison
```bash
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123xyz" \
  --figma-node-id "12:34"

browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123xyz" \
  --figma-node-id "12:34" \
  --selector ".hero-section"

browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123xyz" \
  --figma-node-id "12:34" \
  --mssim-mode semantic
```

### DOM Inspection
```bash
browser-devtools-cli content get-as-html
browser-devtools-cli content get-as-html --selector ".component"
browser-devtools-cli content get-as-text --selector ".content"
```

## Viewport Presets

| Device | Width | Height | Command |
|--------|-------|--------|---------|
| Mobile S | 320px | 568px | `--width 320 --height 568` |
| Mobile M | 375px | 667px | `--width 375 --height 667` |
| Mobile L | 425px | 812px | `--width 425 --height 812` |
| Tablet | 768px | 1024px | `--width 768 --height 1024` |
| Laptop | 1366px | 768px | `--width 1366 --height 768` |
| Desktop | 1920px | 1080px | `--width 1920 --height 1080` |

## Prerequisites for Figma Comparison

**Figma API Access:**
- Set `FIGMA_ACCESS_TOKEN` environment variable
- Get token from Figma account settings

**Optional (for enhanced comparison):**
- AWS credentials for image/text embeddings
- Cloud inference profile configuration

## Visual Testing Workflow

```bash
SESSION="--session-id visual-test"

# 1. Navigate
browser-devtools-cli $SESSION navigation go-to --url "https://example.com"
browser-devtools-cli $SESSION sync wait-for-network-idle

# 2. Capture desktop
browser-devtools-cli $SESSION content take-screenshot --name "desktop"

# 3. Test mobile viewport
browser-devtools-cli $SESSION interaction resize-viewport --width 375 --height 667
browser-devtools-cli $SESSION content take-screenshot --name "mobile"

# 4. Test tablet viewport
browser-devtools-cli $SESSION interaction resize-viewport --width 768 --height 1024
browser-devtools-cli $SESSION content take-screenshot --name "tablet"

# 5. Cleanup
browser-devtools-cli session delete visual-test
```

## Figma Comparison Workflow

### 1. Get Figma Reference

Find the Figma file key and node ID:
- File key: From URL `figma.com/file/{FILE_KEY}/...`
- Node ID: Select frame → Copy link → Extract node-id parameter

### 2. Compare with Live Page

```bash
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123xyz" \
  --figma-node-id "12:34" \
  --selector ".hero-section"
```

### 3. Analyze Results

- **Score 0.9-1.0**: Excellent match
- **Score 0.7-0.9**: Minor differences
- **Score 0.5-0.7**: Significant differences
- **Score < 0.5**: Major mismatch

### 4. Investigate Differences

If score is low:
```bash
# Take screenshot of the area
browser-devtools-cli content take-screenshot --name "mismatch" --selector ".hero-section"

# Check HTML structure
browser-devtools-cli content get-as-html --selector ".hero-section"
```

## Comparison Modes

### Semantic Mode (Default)
- More tolerant of text/data differences
- Focuses on layout and structure
- Good for comparing sample vs real data

```bash
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123" \
  --figma-node-id "1:2" \
  --mssim-mode semantic
```

### Raw Mode
- Stricter pixel comparison
- Expects near-identical output
- Good for static content

```bash
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123" \
  --figma-node-id "1:2" \
  --mssim-mode raw
```

## Common Scenarios

### Full Page Comparison
```bash
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123" \
  --figma-node-id "1:2" \
  --full-page true
```

### Component Comparison
```bash
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123" \
  --figma-node-id "5:10" \
  --selector ".card-component"
```

### Responsive Testing with Figma
```bash
# Resize viewport first
browser-devtools-cli interaction resize-viewport --width 375 --height 667

# Then compare with mobile design
browser-devtools-cli figma compare-page-with-design \
  --figma-file-key "ABC123" \
  --figma-node-id "20:30"
```

## Common Visual Checks

- Element visibility at breakpoints
- Text overflow and truncation
- Image aspect ratios
- Color and typography consistency
- Spacing and alignment
- Interactive state styling

## Best Practices

1. **Use semantic mode** for real data vs sample data
2. **Compare components** not just full pages
3. **Test multiple viewports** for responsive designs
4. **Document Figma references** for CI/CD
5. **Set baseline scores** for regression testing
6. **Review notes** in response for signal details
7. **Take screenshots at key states** (initial, hover, active)
