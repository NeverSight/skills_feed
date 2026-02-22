---
name: nebula-scrape-url
description:
  Capture web page screenshots and HTML for design reference. Use when the user
  provides a URL and asks to build, recreate, or implement a design. Runs
  `scripts/scrape-page.js` to capture desktop/tablet/mobile screenshots and
  HTML. Not for Figma, GitHub, or documentation URLs.
---

# Scraping URLs for design reference

**This applies to web page URLs only.** Do not use this for:

- Figma URLs (use the Figma MCP instead)
- GitHub URLs (read the code directly)
- Documentation URLs (read or search as needed)

## Workflow

1. **Run the scraper** to capture screenshots and HTML:

   ```bash
   node scripts/scrape-page.js <url>
   ```

2. **Review the output** in `scraped/<timestamp>/`:
   - `screenshot-desktop.png` - Desktop layout reference
   - `screenshot-tablet.png` - Tablet layout reference
   - `screenshot-mobile.png` - Mobile layout reference
   - `page.html` - Full HTML for structure reference

3. **Use the screenshots** to understand the visual design (layout, spacing,
   colors, typography).

4. **Use the HTML** to understand the content structure and hierarchy.

5. **Build the components** using the `nebula-component-creation` skill.

## Example

User prompt: "Build me this page: https://example.com/pricing"

1. Run: `node scripts/scrape-page.js https://example.com/pricing`
2. Review the screenshots to understand the layout
3. Review the HTML to understand the structure
4. Create components that match the design using Tailwind CSS
