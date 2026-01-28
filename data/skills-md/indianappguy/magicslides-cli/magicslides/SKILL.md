---
name: magicslides
description: Create AI-powered presentations from topics or URLs. Use this skill when users need to generate presentation slides, PowerPoint decks, or pitch decks. Triggers on requests for presentations, slide decks, or converting articles/content into slides.
license: MIT
metadata:
  author: IndianAppGuy
  version: "1.0.3"
---

# MagicSlides - AI Presentation Generator

Create professional presentations in seconds from topics or web content using AI.

## When to Use This Skill

Use this skill when:
- User asks to create a presentation or slide deck
- User wants to convert an article or URL into slides
- User needs a PowerPoint or Google Slides presentation
- User asks "make me a presentation about..."
- User needs a pitch deck or educational slides
- User wants to summarize content as slides

**Keywords:** presentation, slides, PowerPoint, PPT, slide deck, pitch deck, create slides, generate presentation, topic to slides, URL to presentation

## Prerequisites

The `magicslides` CLI must be installed and authenticated:

```bash
# Check if installed
which magicslides

# If not installed
npm install -g magicslides

# Authenticate (requires API key from magicslides.app/dashboard/settings)
magicslides login
```

## Commands

### Create Presentation from Topic

```bash
magicslides create --topic "<topic>" --slides <number> --language <code>
```

**Parameters:**
- `--topic` (required): The presentation topic
- `--slides` (optional): Number of slides (1-50, default: 10)
- `--language` (optional): Language code (default: en)
- `--template` (optional): Template name (e.g., default, modern, minimal)

**Examples:**
```bash
# Basic presentation
magicslides create --topic "Introduction to Machine Learning" --slides 10

# Presentation in Spanish
magicslides create --topic "Inteligencia Artificial" --slides 15 --language es

# With specific template
magicslides create --topic "Q1 Sales Report" --slides 8 --template modern
```

### Create Presentation from URL

Convert any web article or blog post into a presentation:

```bash
magicslides create-url --url "<url>" --slides <number> --language <code>
```

**Parameters:**
- `--url` (required): URL of the article/content
- `--slides` (optional): Number of slides (1-50, default: 10)
- `--language` (optional): Language code (default: en)
- `--template` (optional): Template name

**Examples:**
```bash
# Create from a blog post
magicslides create-url --url "https://techcrunch.com/article" --slides 12

# Create from documentation in German
magicslides create-url --url "https://docs.example.com/guide" --slides 8 --language de
```

## Workflow for Agents

1. **When user asks for a presentation on a topic:**
   ```bash
   magicslides create --topic "<user's topic>" --slides 10
   ```

2. **When user shares a URL and wants slides:**
   ```bash
   magicslides create-url --url "<user's url>" --slides 10
   ```

3. **For specific requirements:**
   - Adjust `--slides` based on how detailed the user wants it
   - Use `--language` if user specifies a language
   - Use `--template` for specific styling needs

## Response Format

The CLI returns the URL to the generated presentation. Present it to the user:

```
Your presentation has been created!

🎨 View and edit your presentation:
[presentation URL from output]

The presentation contains [X] slides about [topic].
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Authentication required" | Run `magicslides login` with API key |
| "Invalid API key" | Get new key from magicslides.app/dashboard/settings |
| "Rate limit exceeded" | User needs to upgrade plan or wait |
| "Invalid URL" | Verify the URL is accessible and valid |

## Supported Languages

40+ languages supported using ISO 639-1 codes:

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | en | Spanish | es |
| French | fr | German | de |
| Portuguese | pt | Italian | it |
| Chinese | zh | Japanese | ja |
| Korean | ko | Russian | ru |
| Arabic | ar | Hindi | hi |

## Limitations

- API key required (free tier: 10 presentations/month)
- Slides range: 1-50 per presentation
- URL content must be publicly accessible
- Generation takes 30-60 seconds

## Examples for Common Tasks

### Quick Presentation
```bash
magicslides create --topic "Project Status Update" --slides 5
```

### Detailed Educational Presentation
```bash
magicslides create --topic "Complete Guide to Python Programming" --slides 30 --language en
```

### Convert Article to Slides
```bash
magicslides create-url --url "https://medium.com/@author/article" --slides 15
```

### Sales Pitch Deck
```bash
magicslides create --topic "Product Launch Pitch - Feature Benefits and Pricing" --slides 12 --template modern
```

### Multi-language Presentation
```bash
# Japanese presentation
magicslides create --topic "人工知能入門" --slides 10 --language ja

# French presentation  
magicslides create --topic "Introduction à l'IA" --slides 10 --language fr
```

## Links

- Website: https://magicslides.app
- npm Package: https://npmjs.com/package/magicslides
- Dashboard: https://magicslides.app/dashboard
- API Keys: https://magicslides.app/dashboard/settings
