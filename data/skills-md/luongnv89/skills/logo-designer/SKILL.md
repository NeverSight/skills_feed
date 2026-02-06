---
name: logo-designer
description: Design professional, modern logos with automatic project context detection. Use when users ask to "create a logo", "design a logo", "generate brand identity", "make a favicon", or need visual brand assets. Analyzes project files (README, package.json, etc.) to understand product name, purpose, and existing brand colors before generating logo concepts.
---

# Logo Designer

Design modern, professional logos by analyzing project context and generating SVG-based brand assets.

## Workflow

### Phase 1: Project Analysis

Automatically analyze the current project to understand brand context:

1. **Detect product identity** - Check these files in order:
   - `README.md` - Product name, description, tagline
   - `package.json` - Name, description, keywords
   - `pyproject.toml` - Project name and description
   - `Cargo.toml` - Package name and description
   - `go.mod` - Module name

2. **Find existing brand assets** - Search for:
   - `/docs/brand_kit.md`, `/.docs/brand_kit.md`, `brand_kit.md`
   - `/docs/prd.md`, `prd.md` - Product requirements with brand info
   - `/assets/logo/`, `/public/logo`, `/static/logo` - Existing logos
   - Tailwind config for existing color palette

3. **Identify project type** from codebase structure:
   - Developer/CLI/Open Source - `.github/`, CLI entry points, MIT license
   - SaaS/Productivity - Web app structure, auth, dashboard patterns
   - Startup - Lean structure, MVP patterns
   - Enterprise/B2B - Complex architecture, integrations
   - Consumer/Mobile - React Native, Flutter, mobile-first patterns

4. **Summarize findings** before proceeding:
   ```
   Product: [name]
   Type: [Developer Tool / SaaS / Startup / Enterprise / Consumer]
   Purpose: [1-sentence description]
   Audience: [target users]
   Existing colors: [hex codes if found, or "None detected"]
   Assets found: [list or "None"]
   ```

### Phase 2: Logo Design

Generate logo based on project type and context.

#### Style Selection (auto-select based on project type)

| Project Type | Style | Examples |
|--------------|-------|----------|
| Developer/CLI/Open Source | Clean, technical, monochrome | GitHub, Linear, Vercel |
| SaaS/Productivity | Ultra-minimal, Apple-style | Notion, Stripe, Figma |
| Startup | Bold, distinctive, high-contrast | YC-style companies |
| Enterprise/B2B | Professional, trustworthy | Salesforce, IBM |
| Consumer/Mobile | Friendly, vibrant, icon-first | Instagram, Spotify |

#### Design Principles

**Visual:**
- Minimalist, clean, strong geometry
- Abstract symbol or monogram related to core purpose
- Works at all sizes (16px favicon to hero banner)
- Flat or semi-flat design, no gradients or visual clichés

**Colors:**
- Use detected brand colors OR suggest based on industry
- High contrast, WCAG AA compliant (4.5:1 minimum)
- Always provide light, dark, and transparent versions

**Typography:**
- Modern sans-serif (Inter, SF Pro, Geist, or match detected fonts)
- Medium to Bold weight
- Confident and readable at small sizes

### Phase 3: Deliverables

Generate these SVG files:

```
/assets/logo/
├── logo-full.svg      # Mark + wordmark (horizontal)
├── logo-mark.svg      # Symbol/icon only
├── logo-wordmark.svg  # Text only
├── logo-icon.svg      # App icon (square, padded)
├── favicon.svg        # 16x16 optimized
├── logo-white.svg     # White version for dark backgrounds
└── logo-black.svg     # Black version for light backgrounds
```

**SVG Requirements:**
- Vector-style, crisp edges
- No embedded rasters
- Optimized paths
- viewBox properly set

### Phase 4: Documentation

After generating logos, provide:

1. **Design Rationale**
   - Why these colors were chosen
   - Symbol meaning and connection to product
   - Typography choice reasoning

2. **Color Specification**
   ```
   Primary: #HEXCODE
   Secondary: #HEXCODE (if applicable)
   Background Light: #FFFFFF
   Background Dark: #0A0A0A
   ```

3. **Tailwind Config Addition**
   ```js
   colors: {
     brand: {
       primary: '#HEXCODE',
       secondary: '#HEXCODE',
     }
   }
   ```

4. **Next Steps**
   - Create or update `brand_kit.md`
   - Add logo to README
   - Update favicon in HTML/framework config

## Example Output

For a CLI tool called "fastbuild":

```
## Analysis Summary
Product: fastbuild
Type: Developer/CLI Tool
Purpose: Fast incremental build system for large codebases
Audience: Software developers, DevOps engineers
Existing colors: None detected
Assets found: None

## Design Rationale
- **Symbol**: Abstract "F" formed by stacked horizontal bars suggesting speed and layered builds
- **Colors**: Monochrome (#0A0A0A) for technical credibility, matching Vercel/Linear aesthetic
- **Typography**: Geist Mono for CLI tool authenticity

## Colors
Primary: #0A0A0A
Accent: #3B82F6 (optional highlight)
```

## Notes

- Always show logo previews on both light (#FFFFFF) and dark (#0A0A0A) backgrounds
- For wordmarks, ensure the product name is spelled exactly as found in project files
- If no project context is found, ask the user for: product name, type, and purpose
- Prefer simplicity - a logo should be recognizable at 16x16 pixels
