---
name: infographic-generation
description: Generate professional infographics using each::sense AI. Create statistical, process, comparison, timeline, list, geographic, hierarchical, resume, report, and social media infographics optimized for visual communication.
metadata:
  author: eachlabs
  version: "1.0"
---

# Infographic Generation

Generate professional, visually compelling infographics using each::sense. This skill creates data-driven visual content optimized for presentations, reports, social media, and marketing materials.

## Features

- **Statistical Infographics**: Data visualizations with charts, graphs, and key metrics
- **Process/How-To Infographics**: Step-by-step visual guides and tutorials
- **Comparison Infographics**: Side-by-side product, service, or concept comparisons
- **Timeline Infographics**: Historical events, project milestones, company history
- **List Infographics**: Top 10 lists, tips, features, and curated content
- **Geographic/Map Infographics**: Location-based data and regional statistics
- **Hierarchical Infographics**: Organizational charts, taxonomies, flowcharts
- **Resume Infographics**: Visual CVs and professional profiles
- **Report Infographics**: Annual reports, quarterly summaries, research findings
- **Social Media Infographics**: Platform-optimized visual content for engagement

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a statistical infographic showing global renewable energy adoption rates with bar charts and key statistics",
    "mode": "max"
  }'
```

## Infographic Types & Best Practices

| Type | Best For | Key Elements |
|------|----------|--------------|
| Statistical | Data presentation, research findings | Charts, graphs, percentages, icons |
| Process | Tutorials, workflows, instructions | Numbered steps, arrows, icons |
| Comparison | Product comparisons, decision guides | Side-by-side layout, checkmarks, ratings |
| Timeline | History, roadmaps, project plans | Linear flow, dates, milestones |
| List | Tips, features, rankings | Numbers, bullet points, icons |
| Geographic | Regional data, market analysis | Maps, location markers, regional stats |
| Hierarchical | Org charts, taxonomies, structures | Tree diagrams, boxes, connectors |
| Resume | Job applications, portfolios | Skills bars, timeline, icons |
| Report | Business summaries, analytics | Multiple sections, KPIs, graphs |
| Social Media | Engagement, sharing | Platform dimensions, bold text, simple graphics |

## Use Case Examples

### 1. Statistical Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a statistical infographic about global coffee consumption. Include: bar chart showing top 5 consuming countries, pie chart of coffee types (espresso, latte, cappuccino, etc.), key stats like 2.25 billion cups consumed daily, and icons representing coffee culture. Modern minimal design with warm brown and cream color palette. Portrait orientation.",
    "mode": "max"
  }'
```

### 2. Process/How-To Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a how-to infographic for making sourdough bread. Show 8 steps: 1) Create starter, 2) Feed starter, 3) Mix dough, 4) Autolyse, 5) Stretch and fold, 6) Bulk ferment, 7) Shape and proof, 8) Bake. Use illustrated icons for each step, numbered circles, arrows showing flow. Rustic warm color scheme. Vertical layout.",
    "mode": "max"
  }'
```

### 3. Comparison Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comparison infographic: Electric Cars vs Gas Cars. Compare: Initial cost, Fuel/charging costs, Maintenance costs, Environmental impact, Range, Charging/refueling time. Use side-by-side layout with green for electric and gray for gas. Include icons for each category, checkmarks for advantages. Clean modern design.",
    "mode": "max"
  }'
```

### 4. Timeline Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a timeline infographic showing the history of artificial intelligence. Key milestones: 1950 Turing Test proposed, 1956 Dartmouth Conference (AI term coined), 1966 ELIZA chatbot, 1997 Deep Blue beats Kasparov, 2011 IBM Watson wins Jeopardy, 2012 Deep Learning breakthrough, 2016 AlphaGo beats Lee Sedol, 2022 ChatGPT released. Horizontal timeline with alternating above/below entries, tech-inspired blue color scheme, circuit board design elements.",
    "mode": "max"
  }'
```

### 5. List Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a list infographic: Top 10 Productivity Tips for Remote Workers. Include: 1) Create dedicated workspace, 2) Set regular hours, 3) Take scheduled breaks, 4) Use time-blocking, 5) Minimize distractions, 6) Dress for work, 7) Stay connected with team, 8) Set boundaries, 9) Exercise daily, 10) End work ritual. Use numbered list format with icons for each tip, modern gradient purple and blue color scheme, clean typography.",
    "mode": "max"
  }'
```

### 6. Geographic/Map Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a geographic infographic showing internet penetration rates across continents. Include a world map with color-coded regions: North America 93%, Europe 89%, South America 75%, Asia 64%, Africa 43%. Add data callouts for top 5 countries by users. Use a tech-inspired blue gradient for high penetration to gray for low. Include legend and source citation area.",
    "mode": "max"
  }'
```

### 7. Hierarchical Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a hierarchical infographic showing a typical tech startup organizational structure. CEO at top, branching to: CTO (with Engineering Manager, then Frontend/Backend/DevOps teams), CPO (with Product Managers, UX Designers), CFO (with Finance, HR), CMO (with Marketing, Sales). Use tree diagram format with connecting lines, professional corporate blue and gray colors, rounded rectangles for each role, icons representing each department.",
    "mode": "max"
  }'
```

### 8. Resume Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a visual resume infographic for a UX Designer. Include sections: Profile summary with placeholder for photo, Skills with horizontal progress bars (Figma 95%, User Research 90%, Prototyping 85%, HTML/CSS 70%), Work experience as vertical timeline (2020-2023 Senior UX at TechCorp, 2017-2020 UX Designer at StartupXYZ), Education icons, Contact info with icons. Modern minimalist design, teal and dark gray color scheme, A4 portrait.",
    "mode": "max"
  }'
```

### 9. Report Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an annual report infographic for a SaaS company. Include: Header with company logo placeholder and year 2024, Key metrics section (Revenue $12M up 45%, Customers 5,000+ up 60%, Team size 85 up 30%, NPS score 72), Revenue growth line chart, Customer acquisition funnel, Geographic expansion map showing presence in 25 countries, Product milestones timeline. Professional corporate design, navy blue and gold accent colors.",
    "mode": "max"
  }'
```

### 10. Social Media Infographic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a square 1:1 social media infographic about benefits of meditation. Title: 5 Science-Backed Benefits of Daily Meditation. Points: 1) Reduces stress hormones by 23%, 2) Improves focus and concentration, 3) Better sleep quality, 4) Lower blood pressure, 5) Increased emotional well-being. Bold readable text, calming purple and teal gradient background, simple icons for each benefit, Instagram-optimized with high contrast for mobile viewing.",
    "mode": "max"
  }'
```

## Multi-Turn Creative Iteration

Use `session_id` to iterate on infographic designs:

```bash
# Initial infographic
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an infographic about climate change impacts with key statistics and a world map",
    "session_id": "climate-infographic-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more emphasis on ocean temperature data and include a temperature anomaly chart",
    "session_id": "climate-infographic-001"
  }'

# Request color variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an alternate version with a warmer color palette using oranges and reds to emphasize urgency",
    "session_id": "climate-infographic-001"
  }'
```

## Batch Generation for A/B Testing

Generate multiple infographic variations:

```bash
# Variation A - Minimalist style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist infographic about healthy eating habits, white background, simple line icons, lots of whitespace",
    "mode": "eco"
  }'

# Variation B - Bold colorful style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bold colorful infographic about healthy eating habits, vibrant gradients, filled icons, energetic design",
    "mode": "eco"
  }'

# Variation C - Corporate professional style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate professional infographic about healthy eating habits, navy and gray colors, formal typography, business report style",
    "mode": "eco"
  }'
```

## Best Practices

### Design Principles
- **Visual Hierarchy**: Use size, color, and positioning to guide the viewer's eye
- **Consistency**: Maintain consistent icons, colors, and typography throughout
- **White Space**: Don't overcrowd; let elements breathe
- **Data Accuracy**: Represent data proportionally and accurately
- **Readability**: Use sufficient contrast and readable font sizes

### Content Guidelines
- **One Key Message**: Focus on a single main takeaway
- **Scannable**: Design for quick scanning with clear headers
- **Source Citations**: Include data sources for credibility
- **Call to Action**: Include next steps when appropriate

### Platform Optimization
| Platform | Recommended Size | Notes |
|----------|-----------------|-------|
| Pinterest | 1000x1500 (2:3) | Tall format performs best |
| Instagram Feed | 1080x1080 (1:1) | Square for feed |
| Instagram Stories | 1080x1920 (9:16) | Full screen vertical |
| LinkedIn | 1200x627 (1.91:1) | Horizontal for feed |
| Twitter/X | 1200x675 (16:9) | Horizontal format |
| Blog/Web | 800x2000+ | Long-form vertical |
| Presentation | 1920x1080 (16:9) | Slide format |

## Prompt Tips for Infographics

When creating infographics, include these details in your prompt:

1. **Type**: Specify infographic type (statistical, process, timeline, etc.)
2. **Topic**: Clearly describe the subject matter
3. **Data Points**: Provide specific numbers, statistics, or content items
4. **Layout**: Mention orientation (portrait/landscape) and structure
5. **Style**: Describe desired aesthetic (minimal, bold, corporate, playful)
6. **Colors**: Specify color palette or brand colors
7. **Platform**: Mention intended use (social media, presentation, print)

### Example Prompt Structure

```
"Create a [type] infographic about [topic].
Include: [specific data points, sections, or elements].
Layout: [orientation and structure].
Style: [aesthetic description].
Colors: [color palette].
For: [intended platform/use]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final designs, client presentations, print materials | Slower | Highest |
| `eco` | Quick drafts, concept exploration, A/B testing | Faster | Good |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt content |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `data-visualization` - Charts and graphs
- `presentation-design` - Slide decks and pitch materials
- `social-media-graphics` - Platform-optimized visuals
