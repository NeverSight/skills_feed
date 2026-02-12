---
name: slidev-quick-start
description: Get started with Slidev presentations in minutes. Use this skill to create your first presentation or set up a new Slidev project.
---

# Slidev Quick Start

This skill helps you get started with Slidev, the presentation framework for developers. You'll learn how to create a new project, understand the basic syntax, and run your first presentation.

## When to Use This Skill

- Creating a new Slidev presentation from scratch
- Setting up Slidev for the first time
- Understanding basic Slidev concepts
- Converting an existing presentation to Slidev
- Quickly scaffolding a presentation structure

## Prerequisites

- **Node.js**: Version 18.0 or higher
- **Package Manager**: npm, pnpm, or yarn
- **Text Editor**: VS Code recommended (with Slidev extension)

## Creating a New Project

### Option 1: Using npm init (Recommended)

```bash
npm init slidev@latest
```

This interactive command will:
1. Ask for your project name
2. Create the project directory
3. Install dependencies
4. Start the dev server

### Option 2: Manual Setup

```bash
# Create project directory
mkdir my-presentation
cd my-presentation

# Initialize package.json
npm init -y

# Install Slidev
npm install @slidev/cli @slidev/theme-default

# Create slides file
touch slides.md
```

Add scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "slidev --open",
    "build": "slidev build",
    "export": "slidev export"
  }
}
```

## Your First Presentation

Create `slides.md` with this content:

```markdown
---
theme: default
title: My First Presentation
info: |
  ## My First Slidev Presentation
  Created with Slidev
class: text-center
drawings:
  persist: false
transition: slide-left
---

# Welcome to Slidev

Presentation slides for developers

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---

# What is Slidev?

Slidev is a slides maker and presenter designed for developers

- 📝 **Markdown-based** - focus on content with Markdown
- 🎨 **Themable** - themes can be shared and installed
- 🧑‍💻 **Developer Friendly** - code highlighting, live coding
- 🤹 **Interactive** - embed Vue components
- 🎥 **Recording** - built-in recording and camera view
- 📤 **Portable** - export to PDF, PPTX, or host online

---
layout: center
---

# Thank You!

[Documentation](https://sli.dev) · [GitHub](https://github.com/slidevjs/slidev)
```

## Running Your Presentation

```bash
# Start development server
npm run dev

# Or directly with npx
npx slidev
```

Your presentation will be available at `http://localhost:3030`

## Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Space` / `→` | Next slide/animation |
| `←` | Previous slide/animation |
| `↑` / `↓` | Navigate slides (skip animations) |
| `o` | Overview mode |
| `d` | Toggle dark mode |
| `f` | Fullscreen |
| `g` | Go to slide |
| `Esc` | Exit overview/fullscreen |

## Slide Separator

Use `---` (three dashes) surrounded by blank lines to separate slides:

```markdown
# Slide 1

Content for slide 1

---

# Slide 2

Content for slide 2

---

# Slide 3

Content for slide 3
```

## Frontmatter Configuration

The first slide's frontmatter configures the entire presentation:

```yaml
---
# Presentation metadata
theme: seriph              # Theme name
title: My Presentation     # Browser tab title
info: |                    # Presentation info
  ## About
  Description here

# Appearance
colorSchema: auto          # auto, light, or dark
class: text-center         # CSS classes for first slide
background: /image.jpg     # Background image

# Features
drawings:
  persist: false           # Save drawings between reloads
transition: slide-left     # Default transition
highlighter: shiki         # Code highlighter

# Export
exportFilename: slides     # Export filename
download: true             # Show download button
---
```

## Adding Layouts

Specify layouts per slide using frontmatter:

```markdown
---
layout: cover
background: https://cover.sli.dev
---

# Cover Slide

---
layout: two-cols
---

# Left Column

Content here

::right::

# Right Column

Content here

---
layout: center
---

# Centered Content
```

## Adding Code Blocks

```markdown
# Code Example

\`\`\`typescript
interface User {
  id: number
  name: string
  email: string
}

function greet(user: User): string {
  return `Hello, ${user.name}!`
}
\`\`\`
```

## Adding Speaker Notes

Add HTML comments at the end of a slide for speaker notes:

```markdown
# My Slide

Important content here

<!--
Speaker notes go here.
- Remember to mention X
- Demo the feature Y
-->
```

## Best Practices

1. **Start Simple**: Begin with basic Markdown, add features gradually
2. **One Idea Per Slide**: Keep slides focused
3. **Use Layouts**: Leverage built-in layouts for consistent design
4. **Version Control**: Commit `slides.md` to Git
5. **Test Export Early**: Verify PDF export works before presenting

## Common Mistakes to Avoid

❌ **Missing blank lines around separators**
```markdown
# Slide 1
---
# Slide 2
```

✓ **Correct separator syntax**
```markdown
# Slide 1

---

# Slide 2
```

❌ **Invalid frontmatter indentation**
```yaml
---
theme:seriph  # Missing space after colon
---
```

✓ **Correct frontmatter**
```yaml
---
theme: seriph
---
```

## Output Format

When creating a new Slidev presentation, provide:

```
PROJECT STRUCTURE:
- slides.md (main presentation file)
- package.json (with dev/build/export scripts)
- Optional: public/ directory for assets

FIRST SLIDE FRONTMATTER:
---
theme: [recommended theme]
title: [presentation title]
---

SUGGESTED SLIDE STRUCTURE:
1. Title/Cover slide
2. Introduction/Agenda
3. Main content slides
4. Summary/Conclusion
5. Thank you/Contact slide

NEXT STEPS:
- Run `npm run dev` to start
- Edit slides.md to add content
- Use `o` key for overview
```
