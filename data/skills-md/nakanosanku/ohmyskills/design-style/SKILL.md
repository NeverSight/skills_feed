---
name: design-style
description: |
  Use this skill when the user asks to build, create, design, develop, or improve ANY frontend interface, web page, UI component, or visual element. This includes:
  - Building landing pages, websites, web apps, dashboards, portfolios, or any web interface
  - Creating UI components (buttons, forms, cards, navbars, modals, etc.)
  - Designing pages with React, Vue, Next.js, Svelte, or any frontend framework
  - Adding styling or improving visual design of existing components
  - Implementing specific design aesthetics (modern, dark, minimalist, brutalist, etc.)
  - User mentions "frontend", "UI", "UX", "design", "interface", "web design", or "styling"
  - User asks for "beautiful", "modern", "professional", "clean", or any aesthetic adjective
  - User requests help with CSS, Tailwind, styled-components, or any styling approach

  This skill automatically retrieves the appropriate design system prompt (Neo-brutalism, Modern Dark, Bauhaus, Cyberpunk, Material, etc.) to help create visually distinctive, production-grade frontend code instead of generic UI.

  IMPORTANT: Trigger this skill proactively for ANY frontend/UI work, not just when design style is explicitly mentioned.
allowed-tools: Read, Glob, Grep
---

# Design Style Skill

## Purpose

This skill helps Claude Code create beautiful, distinctive frontend interfaces by automatically retrieving design system prompts from the `prompts/` directory. Instead of producing generic UI, this skill enables Claude to build interfaces with specific design aesthetics like Neo-brutalism, Modern Dark, Luxury, Cyberpunk, and more.

## When to Use

This skill is **automatically invoked** when:
- User asks to build a web page, landing page, or web application
- User requests a UI component with a specific design style
- User mentions frontend, React, Vue, or web development
- User asks for a specific aesthetic (e.g., "make it look modern and dark" or "use a brutalist style")

## Available Design Styles

The following design systems are available in the `prompts/` directory:

- **Academia** - Scholarly, classic, refined
- **ArtDeco** - Luxurious 1920s glamour
- **Bauhaus** - Functionalist, geometric minimalism
- **BoldTypography** - Type-driven design
- **Botanical** - Nature-inspired, organic
- **Claymorphism** - Soft, clay-like 3D elements
- **Cyberpunk** - Futuristic, neon, high-tech
- **Enterprise** - Professional, corporate, scalable
- **FlatDesign** - Clean, minimal, 2D
- **Fluent2** - Microsoft Fluent 2 Design System
- **HumanistLiterary** - Warm, literary, conversational (Claude aesthetic)
- **Industrial** - Raw, mechanical, utilitarian
- **Kinetic** - Dynamic, motion-focused
- **Luxury** - Premium, elegant, sophisticated
- **Material** - Google Material Design
- **Maximalism** - Bold, expressive, abundant
- **MinimalDrak** - Minimal dark theme (note: typo in original)
- **ModernDark** - Contemporary dark UI with depth
- **Monochrome** - Black and white, high contrast
- **Neo-brutalism** - Bold, raw, colorful brutalism
- **Neumorphism** - Soft UI, skeuomorphic
- **Newsprint** - Newspaper-inspired
- **Organic** - Natural, flowing forms
- **PlayfulGeometric** - Fun geometric shapes
- **Professional** - Clean, business-focused
- **Retro** - Vintage, nostalgic
- **Saas** - Modern SaaS aesthetic
- **Sketch** - Hand-drawn, artistic
- **Swiss** - International Typographic Style
- **TerminalCLI** - Command-line interface aesthetic
- **Vaporwave** - 80s/90s aesthetic, nostalgic
- **Web3** - Decentralized, crypto-inspired

## How It Works

### Step 1: Understand User Intent

When the user requests frontend work, first determine:
1. **Tech stack** - What framework are they using? (React, Vue, Next.js, etc.)
2. **Design preference** - Did they mention a specific style or aesthetic?
3. **Component scope** - Single component, full page, or entire application?

### Step 2: Select Design Style

**If user specifies a style:**
- Match their request to available styles (e.g., "brutalist" → Neo-brutalism)
- Case-insensitive matching (brutalism, Brutalism, BRUTALISM all work)

**If user doesn't specify:**
- For modern, professional projects → **ModernDark** or **Professional**
- For creative, bold projects → **Neo-brutalism** or **BoldTypography**
- For minimal, clean projects → **FlatDesign** or **Swiss**
- For enterprise/corporate → **Enterprise**

Ask the user if you're uncertain about which style fits their needs.

### Step 3: Retrieve Design System

Use the Read tool to load the appropriate prompt file:

```
Read: prompts/<StyleName>.md
```

For example:
- `prompts/Neo-brutalism.md`
- `prompts/ModernDark.md`
- `prompts/Cyberpunk.md`

### Step 4: Apply Design System

Once you've loaded the design system prompt:

1. **Internalize the design philosophy** - Understand the core principles, visual signatures, and differentiation factors
2. **Extract design tokens** - Colors, typography, spacing, shadows, borders
3. **Follow component patterns** - Use the specified button styles, card layouts, etc.
4. **Apply the "Bold Factor"** - Implement signature elements that make the design authentic
5. **Avoid anti-patterns** - Don't use techniques that break the aesthetic

### Step 5: Build with Context

**Before writing code:**
- Identify the user's existing tech stack
- Understand their component architecture
- Note any constraints (CSS frameworks, design libraries, etc.)

**When writing code:**
- Match their existing patterns and conventions
- Centralize design tokens in CSS variables or a config file
- Create reusable, composable components
- Explain your architectural choices briefly

**Quality standards:**
- Preserve or improve accessibility
- Ensure responsive design across devices
- Make deliberate, creative design choices (not generic boilerplate)
- Leave the codebase cleaner than you found it

## Examples

### Example 1: User Specifies Style

**User:** "Create a landing page for my SaaS product with a neo-brutalist design"

**Skill Actions:**
1. Detect keywords: "landing page", "neo-brutalist"
2. Map "neo-brutalist" → `prompts/Neo-brutalism.md`
3. Read the design system prompt
4. Ask clarifying questions: "What tech stack are you using? React, Vue, or plain HTML/CSS?"
5. Build the landing page following Neo-brutalism principles (thick borders, hard shadows, bold colors, etc.)

### Example 2: User Doesn't Specify Style

**User:** "Help me build a portfolio website"

**Skill Actions:**
1. Detect: "portfolio website" (creative context)
2. Suggest options: "Would you like a specific design style? I can create it in Modern Dark (sophisticated), Neo-brutalism (bold and creative), or Swiss (minimal and clean)."
3. User responds with preference
4. Load appropriate prompt and build

### Example 3: Component Request

**User:** "Add a contact form to my Next.js app. Make it look modern and professional."

**Skill Actions:**
1. Keywords: "Next.js", "modern and professional"
2. Select: `ModernDark.md` (modern) or `Professional.md` (professional)
3. Read design system
4. Build form component matching their Next.js patterns
5. Use design tokens from the prompt (colors, typography, shadows, etc.)

## Quick Reference Commands

When implementing, you can quickly reference specific sections:

**Colors:**
```
Grep: pattern "Token|Value|Usage" path "prompts/<Style>.md"
```

**Typography:**
```
Grep: pattern "Font|Weight|Size" path "prompts/<Style>.md"
```

**Component Patterns:**
```
Grep: pattern "Button|Card|Input" path "prompts/<Style>.md"
```

## Tips for Best Results

1. **Read the full prompt** - Don't just skim. The design philosophy and differentiation sections are critical.
2. **Implement signature elements** - Every design system has a "Bold Factor" section. These elements are what make it authentic.
3. **Avoid anti-patterns** - Each prompt lists what NOT to do. Follow these rules strictly.
4. **Ask questions** - If the user's needs are unclear, ask before building.
5. **Match existing code** - Don't fight their tech stack. Integrate the design system into their existing patterns.

## Notes

- All design system prompts follow the same structure: `<role>` and `<design-system>` sections
- Prompts include detailed color palettes, typography scales, component patterns, and implementation examples
- Each style is production-ready and has been carefully crafted for visual distinctiveness
- The prompts are designed to prevent generic, AI-looking interfaces

## Future Enhancements

Potential improvements to this skill:
- Style combination support (e.g., "Cyberpunk + Minimal")
- Custom style creation workflow
- Design token extraction to JSON/CSS
- Component library generation from prompts
