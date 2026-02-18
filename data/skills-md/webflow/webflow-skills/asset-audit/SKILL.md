---
name: asset-audit
description: Analyze assets on a Webflow site for SEO optimization. Identifies assets missing alt text and assets with non-SEO-friendly names, then generates and applies improvements.
---

# Asset Audit

Analyze assets on a Webflow site for SEO optimization.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**
- Use Webflow MCP's `asset_tool` for fetching and updating assets
- Use Webflow MCP's `get_image_preview` for analyzing image content
- Use Webflow MCP's `data_sites_tool` with action `list_sites` for listing available sites
- Use Webflow MCP's `webflow_guide_tool` to get best practices before starting
- DO NOT use any other tools or methods for Webflow operations
- All tool calls must include the required `context` parameter (15-25 words, third-person perspective)

## Instructions

### Phase 1: Site Selection & Asset Discovery
1. **Get site**: Identify the target site. If user does not provide site ID, ask for it.
2. **Fetch all assets**: Use Webflow MCP's `asset_tool` to get all assets from the site
   - For sites with 50+ assets, process in batches of 20
   - Show progress: "Processing assets 1-20 of 150..."
3. **Detect patterns**: Analyze asset naming for common patterns:
   - Camera uploads (IMG_, DSC_, etc.)
   - Screenshots (screenshot, Screen Shot, etc.)
   - Generic names (untitled, image-1, etc.)
   - Date-based names (2024-01-10, etc.)

### Phase 2: Issue Analysis & Pattern Recognition
4. **Identify issues**: List all assets which:
   - Do not have alt text set (null or empty string)
   - Have existing alt text but it's poor quality (too short, redundant phrases, etc.)
   - Do not have SEO-friendly asset names
   - Are duplicates or very similar
5. **Pattern detection report**: Show detected patterns:
   ```
   🔍 Detected patterns:
   - 15 assets start with "IMG_" (camera uploads)
   - 8 assets contain "screenshot"
   - Suggest: Bulk rename these patterns
   ```
6. **Ask user preference**: Ask if they want to generate:
   - Alt text only
   - SEO-friendly names only
   - Both
   - Apply naming pattern/template

### Phase 3: Analysis & Suggestion Generation
7. **Analyze assets**: Use Webflow MCP's `get_image_preview` tool to analyze the assets that need updates
   - **Error handling**: If Webflow MCP's `get_image_preview` fails, use fallback:
     - Extract description from existing filename
     - Use generic placeholder with warning
     - Continue with other assets
   - Process in batches to avoid timeout
8. **Generate suggestions with validation**:
   - **Alt text validation**:
     - Max 125 characters (warn if longer)
     - No redundant phrases ("image of", "picture of", "photo of")
     - Must end with punctuation
     - Flag generic descriptions (confidence < 50%)
   - **SEO name validation**:
     - Only lowercase a-z, 0-9, hyphens
     - No double extensions (.webp.webp) - strip existing extension first
     - Max 100 characters
     - Replace spaces/underscores with hyphens
     - No special characters
9. **Folder organization suggestions**: If patterns detected, suggest folder structure:
   ```
   💡 Organization suggestions:
   - Create "team-photos" folder for 8 team images
   - Create "product-images" folder for 15 product shots
   ```

### Phase 4: Granular Approval & Application
10. **Present suggestions with granular approval**:
    - Show numbered list with checkboxes
    - Allow individual toggle: "Enter numbers to skip (e.g., '2,4')"
    - Options: "all", "none", or specific numbers
    - Show validation warnings for each suggestion
11. **Offer naming template** (if many similar assets):
    ```
    🎨 Apply naming pattern?
    1. [category]-[description] (e.g., team-john-headshot)
    2. [description]-[location] (e.g., office-workspace-desk)
    3. Custom pattern...
    4. Skip patterns, use individual names
    ```
12. **Store rollback data**: Before applying changes, store:
    - Original asset names
    - Original alt text
    - Timestamp
    - Assets modified
13. **Apply updates**: Use Webflow MCP's `asset_tool` to update approved assets only
    - Show progress for batch updates
    - Handle partial failures gracefully
    - Report successes and failures separately
14. **Offer rollback option**: After changes applied:
    ```
    📋 Rollback Available:
    Last update: 4 assets modified 2 minutes ago
    Type "undo" to revert these changes
    ```

## Examples

**User prompt:**
```
Run an asset audit on my site.
```

**Step 1: Initial Audit Report**
```
📊 SEO Asset Audit: MCP Demo #2

Total: 4 assets

🔍 Detected patterns:
- 4 assets have generic numeric names (1.webp, 2.webp, 3.webp, 4.webp)
- All assets are in WebP format ✓

⚠️ Missing Alt Text (4 assets):
├── 1.webp (empty alt text)
├── 2.webp (empty alt text)
├── 3.webp (empty alt text)
└── 4.webp (empty alt text)

⚠️ Non-SEO-Friendly Names (4 assets):
├── 1.webp (generic numeric name)
├── 2.webp (generic numeric name)
├── 3.webp (generic numeric name)
└── 4.webp (generic numeric name)

---

What would you like to generate?
1. Alt text only
2. SEO-friendly names only
3. Both alt text and SEO-friendly names

Please select an option (1, 2, or 3).
```

**Example with Validation Warnings:**
```
📋 Suggested Improvements:

[1] ✓ IMG_1234.jpg
    Alt text: "Professional team member headshot with blue background."
    New name: professional-team-member-headshot.jpg
    ✅ Validation passed

[2] ✓ screenshot-2024.png
    Alt text: "Dashboard analytics overview showing user engagement metrics."
    New name: dashboard-analytics-overview.png
    ✅ Validation passed

[3] ⚠️ untitled-image.webp
    Alt text: "Photo"
    ⚠️ Warning: Alt text too short (< 10 chars) - needs more detail
    New name: untitled-image.webp
    ⚠️ Warning: Unable to generate better name (image preview failed)

[4] ⚠️ TeamPhoto2024!!!.jpg
    Alt text: "Image of a person working on laptop in modern office with plants and natural lighting through large windows in the background."
    ⚠️ Warning: Alt text too long (137 chars) - consider shortening for screen readers
    New name: team-photo-2024.jpg
    ✅ Validation passed (special characters removed)

Which assets would you like to update?
```

**Step 2: After user selects option 3 and images are analyzed**
```
📋 Suggested Improvements:

[1] ✓ 1.webp
    Alt text: "Podcast host with headphones and microphone recording Webflow podcast episode in studio."
    New name: webflow-podcast-host-recording-studio.webp
    ✅ Validation passed

[2] ✓ 2.webp
    Alt text: "Professional developer wearing glasses working on laptop with Webflow logo in modern office."
    New name: developer-working-laptop-webflow-office.webp
    ✅ Validation passed

[3] ✓ 3.webp
    Alt text: "Webflow homepage hero section with tagline and email signup form."
    New name: webflow-homepage-hero-section.webp
    ✅ Validation passed

[4] ✓ 4.webp
    Alt text: "Speaker presenting on stage at Webflow Conf with audience watching."
    New name: webflow-conf-speaker-presentation-stage.webp
    ✅ Validation passed

---

Which assets would you like to update?
- Type numbers to skip (e.g., "2,4" to skip items 2 and 4)
- Type "all" to proceed with all
- Type "none" to cancel
```

**Step 3: After user confirms with "all"**
```
🔄 Applying updates...

Progress: ████████████████████ 100% (4/4 assets)

✅ Updates Applied Successfully!

SEO Asset Audit Complete: MCP Demo #2

Summary:
- ✅ 4 assets updated successfully
- ❌ 0 assets failed
- ⏭️ 0 assets skipped

Changes Applied:
┌─────────────────────────────────────────────────────────────────┐
│ [1] webflow-podcast-host-recording-studio.webp                  │
│     ✓ Alt text added                                            │
│     ✓ Filename updated                                          │
├─────────────────────────────────────────────────────────────────┤
│ [2] developer-working-laptop-webflow-office.webp                │
│     ✓ Alt text added                                            │
│     ✓ Filename updated                                          │
├─────────────────────────────────────────────────────────────────┤
│ [3] webflow-homepage-hero-section.webp                          │
│     ✓ Alt text added                                            │
│     ✓ Filename updated                                          │
├─────────────────────────────────────────────────────────────────┤
│ [4] webflow-conf-speaker-presentation-stage.webp                │
│     ✓ Alt text added                                            │
│     ✓ Filename updated                                          │
└─────────────────────────────────────────────────────────────────┘

📋 Rollback Available:
Last update: 4 assets modified just now
Type "undo" to revert these changes

---

🎉 Your site's assets are now fully optimized for SEO and accessibility!
```

**Alternative Step 3: User selects specific assets (e.g., "1,3")**
```
🔄 Applying updates to assets 1 and 3...

Progress: ████████████████████ 100% (2/2 assets)

✅ Partial Update Complete!

Summary:
- ✅ 2 assets updated successfully
- ❌ 0 assets failed
- ⏭️ 2 assets skipped (as requested)

Changes Applied:
┌─────────────────────────────────────────────────────────────────┐
│ [1] webflow-podcast-host-recording-studio.webp                  │
│     ✓ Alt text added                                            │
│     ✓ Filename updated                                          │
├─────────────────────────────────────────────────────────────────┤
│ [3] webflow-homepage-hero-section.webp                          │
│     ✓ Alt text added                                            │
│     ✓ Filename updated                                          │
└─────────────────────────────────────────────────────────────────┘

Skipped Assets (can run audit again later):
- [2] 2.webp
- [4] 4.webp

📋 Rollback Available:
Type "undo" to revert these 2 changes
```

## Guidelines

### Phase 1: Critical Validations (Must Follow)

**File Extension Handling:**
- ALWAYS strip existing extension before adding new one
- Bad: `image.webp` → `new-name.webp.webp`
- Good: `image.webp` → `new-name.webp`
- Implementation: Use filename without extension + new extension

**Alt Text Quality Rules:**
- Max length: 125 characters (accessibility best practice)
- Must end with punctuation (period, exclamation, question mark)
- Remove redundant phrases:
  - ❌ "Image of a person" → ✅ "Person working at desk"
  - ❌ "Picture of logo" → ✅ "Company logo on blue background"
  - ❌ "Photo showing" → ✅ Direct description
- Flag if too short (< 10 chars): ⚠️ "Too generic - needs more detail"
- Flag if too long (> 125 chars): ⚠️ "Consider shortening for screen readers"

**SEO Filename Rules:**
- Only allow: lowercase a-z, numbers 0-9, hyphens
- Max length: 100 characters (before extension)
- Convert spaces to hyphens: `team photo` → `team-photo`
- Convert underscores to hyphens: `team_photo` → `team-photo`
- Remove special characters: `photo!@#$` → `photo`
- Convert to lowercase: `TeamPhoto` → `team-photo`
- Remove consecutive hyphens: `team--photo` → `team-photo`
- Trim leading/trailing hyphens: `-photo-` → `photo`

### Phase 2: Batch Processing & Performance

**Large Site Handling:**
- Sites with 50+ assets: Process in batches of 20
- Show progress: "Processing batch 1 of 5 (assets 1-20)..."
- Allow user to process specific batches
- Timeout protection: If Webflow MCP's `get_image_preview` takes > 30s, skip to next batch

**Pattern Detection:**
Detect and report these patterns:
- Camera uploads: `IMG_`, `DSC_`, `DCIM_`, `P_`
- Screenshots: `screenshot`, `Screen Shot`, `Capture`
- Generic names: `untitled`, `image-1`, `photo`, `asset`
- Date formats: `2024-01-10`, `20240110`, `01-10-2024`
- Suggest bulk rename when 3+ assets match a pattern

**Error Handling:**
- If Webflow MCP's `get_image_preview` fails:
  1. Log the error (don't show to user)
  2. Use fallback: Extract description from filename
  3. Mark with ⚠️ warning: "Generated from filename (image preview failed)"
  4. Continue with other assets
- Partial success handling:
  - Report successes separately from failures
  - Show: "✅ 15 updated, ❌ 2 failed, ⏭️ 3 skipped"
  - Offer to retry failed assets

### Phase 3: Advanced Features

**Granular Approval System:**
- Number each suggestion: `[1]`, `[2]`, `[3]`, etc.
- Show checkmark status: `✓` or `✗`
- Accept multiple formats:
  - "all" - approve all
  - "none" - cancel operation
  - "1,3,5" - skip items 1, 3, and 5
  - "2-5" - skip items 2 through 5
- Always show validation status per item

**Naming Templates:**
Offer templates when 5+ similar assets detected:
1. `[category]-[description]-[modifier]`
   - Example: `product-laptop-front-view.jpg`
2. `[description]-[location]-[year]`
   - Example: `team-photo-office-2024.jpg`
3. `[type]-[name]-[variant]`
   - Example: `icon-arrow-blue.svg`

**Folder Organization:**
Suggest folders when detecting:
- 5+ images with "team", "staff", "employee" → `team-photos` folder
- 5+ images with "product", "item" → `product-images` folder
- 5+ images with "logo", "brand" → `branding` folder
- 5+ images with "screenshot", "capture" → `screenshots` folder

**Rollback System:**
Before any update, store in memory:
```json
{
  "timestamp": "2026-01-10T00:45:00Z",
  "assets": [
    {
      "id": "asset-id",
      "originalName": "1.webp",
      "originalAltText": "",
      "newName": "podcast-host.webp",
      "newAltText": "Podcast host recording..."
    }
  ]
}
```
- Offer undo for 5 minutes after changes
- Clear rollback data after next audit starts
- Show rollback option in final summary

**Duplicate Detection:**
- Compare asset sizes (exact match = likely duplicate)
- Compare filenames (similar names = potential duplicate)
- Report: "⚠️ Potential duplicates: asset1.jpg (2.4MB) and asset1-copy.jpg (2.4MB)"
- Don't auto-delete - let user decide

### General Best Practices

- Always use Webflow MCP's `get_image_preview` to understand image content
- Generate specific, descriptive suggestions (not generic)
- Validate all suggestions before presenting to user
- Handle partial operations gracefully
- Provide clear progress indicators for long operations
- Group similar issues together in reports
- Use visual indicators: ✅ ⚠️ ❌ 🔍 💡 📋 🎉
- Be conversational but concise
- Always offer rollback after changes

