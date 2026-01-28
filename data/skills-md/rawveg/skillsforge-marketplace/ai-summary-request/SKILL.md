---
name: ai-summary-request
description: Adds an "AI Summary Request" footer component with clickable AI platform icons (ChatGPT, Claude, Gemini, Grok, Perplexity) that pre-populate prompts for users to get AI summaries of the website. Optionally creates an llms.txt file for enhanced AI discoverability. Use when users want to add AI platform integration buttons or make their website AI-friendly.
---

# AI Summary Request

## Overview

This skill creates a footer component with AI platform icons that allow visitors to request AI summaries of a website. The workflow begins by detecting and confirming the website domain, then asks whether to optionally generate an `llms.txt` file for enhanced AI discoverability.

## When to Use This Skill

Use this skill when:
- User wants to add AI platform integration buttons to their site
- User wants visitors to easily get AI summaries of their business
- User mentions "AI summary" or AI platform buttons
- User wants to create an `llms.txt` file for their website (optional)
- User asks about making their website AI-discoverable

## Workflow

### PREREQUISITE: Domain Detection and Confirmation

Before proceeding with any steps, you MUST determine the website domain:

#### Step 1: Attempt automatic detection

Search for domain information in this priority order:

1. **Environment files** (`.env`, `.env.local`, `.env.production`) - look for `SITE_URL`, `BASE_URL`, `NEXT_PUBLIC_URL`, `NUXT_PUBLIC_SITE_URL`, `VITE_SITE_URL`, or similar
2. **Deployment configs** (`vercel.json`, `netlify.toml`, `firebase.json`, `fly.toml`) - check for domain/alias settings
3. **CNAME files** in `public/` or root directory
4. **Configuration files** (`package.json` homepage field, `next.config.js`, `nuxt.config.js`, `vite.config.js`)
5. **HTML files** - meta tags or `<base>` tags in index files
6. **README or documentation** mentioning the live site URL

#### Step 2: Confirm or request domain

**If a domain is detected**, ask the user to confirm or provide an alternative:
> "I detected that this site appears to use the domain **[DETECTED_DOMAIN]**. Is this correct? If not, please provide the correct domain."

**If no domain can be detected**, ask the user directly:
> "I couldn't automatically detect the domain for this website. What domain should be used for the AI summary links? (e.g., https://example.com)"

#### Step 3: Normalize and store the domain

- If the user provides a domain without a protocol, prepend `https://`
- Remove any trailing slashes
- Store the normalized domain as `${WEBSITE_URL}` for use in subsequent steps

**Example normalizations:**
- `example.com` → `https://example.com`
- `https://example.com/` → `https://example.com`
- `http://example.com` → keep as-is (user may have specific requirements)

---

### PREREQUISITE: llms.txt Decision

After confirming the domain, ask the user:

> "Would you like me to also generate an `llms.txt` file for this website? This file helps AI models better understand your site's content and structure, which can improve the quality of AI-generated summaries.
>
> - **Yes**: I'll create a curated llms.txt file and the footer component will reference it
> - **No**: I'll create just the footer component, and the AI prompt will direct users to explore the website directly"

Store the user's choice as `${INCLUDE_LLMS_TXT}` (true/false).

---

## STEP 1: Generate llms.txt File (OPTIONAL - Only if user chose "Yes")

**Skip this step entirely if the user chose not to generate an llms.txt file.**

Generate a high-quality `llms.txt` file for a given website that helps language models quickly understand and reference the site's most valuable content.

### Analyze the Website's Content Hierarchy

- Inspect any available XML or HTML sitemaps (product, page, post) and explore navigation menus to identify major product categories, services, key informational pages, and blog or news posts
- Focus on top-level categories and representative subcategories or key products, rather than listing every single URL
- Identify important support or policy pages (e.g., About, Contact, Terms, Privacy, Shipping & Returns)

### Select and Curate Content

- For each major category, select a primary landing page and a few representative subcategories or high-value product pages
- Include links to authoritative guides, how-to articles, calculators, training programs or other resources
- Choose a handful of blog posts or case studies that showcase different topics (tutorials, industry insights, success stories). Avoid listing dozens of posts
- Exclude low-value pages such as checkout flows, login pages, or marketing fluff

### Draft Clear Descriptions

- Use concise, factual descriptions (10-15 words) that explain what each page covers
- Avoid hype or redundant repetition of the page title
- When summarizing subcategories, group them in parentheses for brevity

### Build the llms.txt in Markdown

- Start with an H1 title containing the website or company name and a short descriptor
- Add a blockquote (prefaced by >) that succinctly describes what the business does and who it serves
- Optionally include a sentence explaining that the list is curated for AI consumption
- Organize content with H2 headings such as:
  - ## Product categories (or Services if it's a service business)
  - ## Representative pages or ## Popular products
  - ## Guides & resources
  - ## Articles & case studies
  - ## Policies & support
- List each link as a bullet (`- [Title](URL): description`) under the appropriate section
- Keep the file in UTF-8 encoding and ensure it stays well under 100 KB by curating rather than exhaustively listing every URL
- Add an optional "Usage guidelines" section stating how you'd like AI models to attribute or use the content, and include an HTML comment like `<!-- Last updated: YYYY-MM-DD -->` for version tracking

### Validate and Publish

- Verify that all URLs return HTTP 200 and are publicly accessible
- Check the Markdown structure (one H1, proper headings and bullets)
- Place the final `llms.txt` at the website's root and, if possible, add a line in `robots.txt` (`Llmstxt: /llms.txt`) to aid discovery
- Plan regular updates (e.g., quarterly) to reflect changes in products, services or content

### Deliverable

Provide the full `llms.txt` file content, formatted as described above, in the served web root of the current website.

---

## STEP 2: Create AI Summary Request Footer Component

Create an "AI Summary Request" footer component with the following specifications.

### Component Structure

- Centered section containing a header and icon row
- Header text: "Request an AI summary of [COMPANY_NAME]"
- Row of 5 clickable AI platform icons in this exact order: ChatGPT, Claude, Gemini, Grok, Perplexity

### Visual Styling

- Container: flex column, centered alignment, 16px vertical gap
- Header: centered text, base font size (16px), medium font-weight, semantic gray color (#111827 or equivalent)
- Icon container: flex row, centered, 12px horizontal gap, wrap-enabled
- Each icon link: 40x40px clickable area with 28x28px visible icon, rounded-full background
- Icons: Apply CSS filter: `brightness(0)` for monochrome black effect
- Padding within circle: 6px (1.5rem equivalent)
- Hover effect: transform scale(1.1) with cubic-bezier(0.4, 0, 0.2, 1) transition, 150ms duration

### Icon Assets

**CRITICAL**: This skill includes bundled SVG icon files in the `resources/` directory. You MUST use these exact icons - do NOT use generic icon libraries, search for alternatives, or create substitutes.

#### Bundled Icons (Required)

Copy these SVG files from `resources/` to the user's project assets directory:

| Platform | File | Description |
|----------|------|-------------|
| ChatGPT | `resources/chatgpt.svg` | Hexagonal flower/aperture pattern with interlocking curved segments |
| Claude | `resources/claude.svg` | Abstract geometric pattern (NOT the Anthropic backslash logo) |
| Gemini | `resources/gemini.svg` | Four-pointed star/sparkle icon |
| Grok | `resources/grok.svg` | Angular crystalline/triangular pattern (NOT the X/Twitter logo) |
| Perplexity | `resources/perplexity.svg` | Hexagonal pattern with isometric cube perspective |

#### Implementation Steps

1. **Copy icons to project**: Copy all 5 SVG files from this skill's `resources/` directory to the user's project (e.g., `/public/icons/ai/` or `/assets/icons/`)
2. **Reference in component**: Use relative paths to the copied SVG files in the footer component
3. **Do NOT substitute**: These are the only approved icons - do not use CDN links, icon libraries, or recreate from descriptions

#### Icon Validation

Before finalizing, visually confirm:
- ChatGPT icon is NOT a speech bubble or generic chat icon
- Claude icon is NOT a simple backslash or text character
- Gemini icon is NOT a constellation or zodiac twins symbol
- Grok icon is NOT the X/Twitter bird or logo
- Perplexity icon is NOT a question mark or generic markdown symbol

### AI Platform Links

Generate URL-encoded links to each AI platform with pre-composed prompt:

1. ChatGPT: `https://chat.openai.com/?q=[ENCODED_PROMPT]`
2. Claude: `https://claude.ai/new?q=[ENCODED_PROMPT]`
3. Gemini: `https://gemini.google.com/?q=[ENCODED_PROMPT]`
4. Grok: `https://grok.com?q=[ENCODED_PROMPT]`
5. Perplexity: `https://www.perplexity.ai/?q=[ENCODED_PROMPT]`

### Prompt Templates (Select based on llms.txt decision)

Use the appropriate template based on the user's llms.txt decision from the prerequisite step.

**Template variables:**
- `${WEBSITE_URL}` - The confirmed/normalized domain from prerequisite step
- `${COMPANY_NAME}` - The company/site name (ask user if not obvious from codebase)
- `${KEY_ASPECTS}` - Customize based on the business type (e.g., "features, pricing, deliverables" for services; "products, shipping, returns" for e-commerce)

#### WITH llms.txt (if user chose to generate llms.txt)

```
Please read the structured information at ${WEBSITE_URL}/llms.txt to understand ${COMPANY_NAME}.

As a potential client, I want to concretely understand what I will receive with ${COMPANY_NAME} (${WEBSITE_URL}).

Detail step by step what the service includes: ${KEY_ASPECTS}.

Explain it simply, as if you were describing the real experience of the service.
```

#### WITHOUT llms.txt (if user chose not to generate llms.txt)

```
Please visit and analyze ${WEBSITE_URL} to understand ${COMPANY_NAME}.

As a potential client, I want to concretely understand what I will receive with ${COMPANY_NAME} (${WEBSITE_URL}).

Detail step by step what the service includes: ${KEY_ASPECTS}.

Explain it simply, as if you were describing the real experience of the service.
```

### Implementation Checklist

- [ ] Detect or ask for website domain and get user confirmation
- [ ] Ask user whether to generate llms.txt file
- [ ] If llms.txt chosen: Generate and place llms.txt at website root
- [ ] Copy all 5 SVG icons from `resources/` to project assets directory
- [ ] Select correct prompt template based on llms.txt decision
- [ ] Place component in footer, above copyright notice
- [ ] URL-encode prompt using `encodeURIComponent()` or equivalent
- [ ] Each link opens in new tab: `target="_blank" rel="noopener noreferrer"`
- [ ] Add aria-label: "Get AI summary from [Platform Name]"
- [ ] Test all 5 platform links verify prompt pre-population works
- [ ] Verify icons are using the bundled SVGs (NOT generic alternatives)
- [ ] Apply `brightness(0)` filter for consistent monochrome appearance
- [ ] Ensure 44x44px minimum touch target for mobile accessibility
- [ ] Responsive: icons wrap on screens < 640px width

---

## Technical Notes

- The `llms.txt` file follows the emerging standard for AI-readable site documentation
- The footer component should be framework-agnostic but can be adapted for React, Vue, Svelte, or vanilla HTML/CSS
- All URLs must be properly encoded to handle special characters in the prompt
- The component should be accessible and follow WCAG 2.1 guidelines

## Bundled Resources

### resources/

Contains the official SVG icons for each AI platform:

- **chatgpt.svg** - OpenAI ChatGPT hexagonal aperture icon
- **claude.svg** - Anthropic Claude geometric pattern icon
- **gemini.svg** - Google Gemini four-pointed star icon
- **grok.svg** - xAI Grok crystalline pattern icon
- **perplexity.svg** - Perplexity hexagonal cube icon

These icons MUST be copied to the user's project and used directly. Do not substitute with alternatives.

## Success Criteria

A successful implementation should:
1. Confirm the website domain with the user before proceeding
2. Ask the user whether to include llms.txt generation
3. If llms.txt chosen: Produce a curated, well-structured `llms.txt` file under 100KB
4. Create a visually consistent footer component with correct branding
5. Use the appropriate prompt template based on the user's llms.txt decision
6. Generate working links that pre-populate prompts in each AI platform
7. Be accessible on both desktop and mobile devices
8. Use the bundled SVG icons from `resources/` (no substitutes)
