---
name: resume-design-generation
description: Generate professional resume and CV designs using each::sense AI. Create modern, creative, minimalist, executive, tech, academic, infographic, two-column, ATS-friendly, and portfolio-style resumes optimized for various industries and career stages.
metadata:
  author: eachlabs
  version: "1.0"
---

# Resume Design Generation

Generate visually stunning and professionally designed resumes and CVs using each::sense. This skill creates resume layouts and designs optimized for different industries, career levels, and personal branding styles.

## Features

- **Modern Professional**: Clean, contemporary designs for corporate environments
- **Creative Designer**: Bold, artistic layouts for creative industries
- **Minimalist**: Simple, elegant designs with focus on content
- **Executive/Corporate**: Sophisticated designs for senior-level positions
- **Tech/Developer**: Code-inspired layouts for software professionals
- **Academic CV**: Formal layouts for researchers and educators
- **Infographic**: Visual data-driven resume designs
- **Two-Column**: Space-efficient layouts with sidebar sections
- **ATS-Friendly**: Clean formats optimized for applicant tracking systems
- **Portfolio Resume**: Designs that incorporate work samples and projects

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern professional resume design for a marketing manager with a clean blue and white color scheme, include sections for summary, experience, skills, and education",
    "mode": "max"
  }'
```

## Resume Design Formats & Layouts

| Style | Best For | Key Elements |
|-------|----------|--------------|
| Modern Professional | Corporate roles | Clean lines, professional colors, balanced layout |
| Creative Designer | Design/Art roles | Bold typography, unique layouts, creative elements |
| Minimalist | Any industry | White space, simple fonts, content-focused |
| Executive | C-suite/Directors | Elegant, sophisticated, achievement-focused |
| Tech/Developer | Engineering roles | Code aesthetics, skill bars, GitHub-style |
| Academic CV | Academia/Research | Publications section, formal structure |
| Infographic | Marketing/Data | Charts, icons, visual data representation |
| Two-Column | Space-efficient | Sidebar for skills/contact, main content area |
| ATS-Friendly | Online applications | Simple formatting, no graphics, parseable |
| Portfolio | Creatives/Designers | Work samples, project showcases, visual gallery |

## Use Case Examples

### 1. Modern Professional Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern professional resume design for a senior marketing manager. Use a clean navy blue and white color scheme. Include a professional header with name and title, a summary section, work experience timeline, skills section with progress bars, and education. The layout should be single-column, easy to read, and print-ready at A4 size.",
    "mode": "max"
  }'
```

### 2. Creative Designer Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a bold and creative resume for a graphic designer. Use vibrant colors like coral pink and teal accents on a dark charcoal background. Include asymmetric layout elements, custom typography, a personal logo placeholder, portfolio preview section, and creative skill visualization. Make it visually striking and memorable while remaining professional.",
    "mode": "max"
  }'
```

### 3. Minimalist Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist resume design with maximum white space. Use only black text on white background with subtle gray accents for section dividers. Clean sans-serif typography, ample margins, and elegant simplicity. Include name at top, contact info, professional summary, experience, skills as simple tags, and education. No decorative elements - let the content speak.",
    "mode": "max"
  }'
```

### 4. Executive/Corporate Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a sophisticated executive resume for a C-level executive (CEO/CFO). Use premium colors - deep burgundy header with gold accents on cream background. Elegant serif typography for headings, clean sans-serif for body. Include executive summary with key achievements, career highlights, board positions section, education with prestigious credentials, and professional affiliations. Two pages, dignified and authoritative.",
    "mode": "max"
  }'
```

### 5. Tech/Developer Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a developer-style resume design with a dark theme (dark gray/black background with green or cyan accent colors like a terminal). Include a code-style header, tech stack section with language/framework icons, GitHub contribution graph style visualization, project cards with tech badges, experience in commit-log style format, and skills with proficiency indicators. Monospace font for headings.",
    "mode": "max"
  }'
```

### 6. Academic CV

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a formal academic CV template for a university professor or researcher. Classic, traditional layout with navy blue accents on white. Include sections for: contact information, research interests, education with thesis titles, academic positions, publications (with proper citation formatting), grants and funding, teaching experience, conference presentations, professional memberships, and references. Multi-page format, formal typography.",
    "mode": "max"
  }'
```

### 7. Infographic Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an infographic-style resume design for a data analyst or marketing professional. Include circular skill charts, timeline infographic for career progression, bar graphs for proficiency levels, icon-based representations for achievements (e.g., trophy icons for awards), geographic map for locations worked, and pie charts for time allocation. Use a cohesive color palette of blues and oranges. Visual, data-driven, and engaging.",
    "mode": "max"
  }'
```

### 8. Two-Column Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a two-column resume layout. Left sidebar (narrower, dark teal background) contains: profile photo placeholder, contact information with icons, skills with rating dots, languages, and interests. Right main column (white background) contains: professional name and title header, summary, detailed work experience, and education. Clean dividers between sections, modern yet professional appearance.",
    "mode": "max"
  }'
```

### 9. ATS-Friendly Resume

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an ATS-optimized resume design that will parse correctly through applicant tracking systems. Single column layout, no tables or complex formatting, no images or graphics, no headers/footers. Standard section headings (Summary, Experience, Education, Skills), clear hierarchy with bold headings, bullet points for achievements, standard fonts (Arial or Calibri style), and consistent formatting. Clean and parseable while still looking professional.",
    "mode": "max"
  }'
```

### 10. Portfolio Resume (with Work Samples)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a portfolio-style resume for a creative professional (photographer, architect, or UX designer). Include a header section with name and title, a grid layout showcasing 4-6 project thumbnails with brief descriptions, condensed work experience section, skills as visual icons, client logo section, awards with visual badges, and contact information. Visual-heavy design that doubles as a mini portfolio. Modern, gallery-style aesthetic.",
    "mode": "max"
  }'
```

## Best Practices

### Design Principles
- **Hierarchy**: Use clear visual hierarchy with consistent heading sizes
- **White Space**: Don't overcrowd - breathing room improves readability
- **Color Scheme**: Stick to 2-3 colors maximum for professionalism
- **Typography**: Use maximum 2 font families (one for headings, one for body)
- **Alignment**: Maintain consistent alignment throughout the document

### Industry-Specific Tips
- **Corporate/Finance**: Conservative colors (navy, gray), formal layouts
- **Tech/Startup**: Modern designs, skill visualizations, GitHub-style elements
- **Creative/Design**: Bold layouts, unique elements, portfolio integration
- **Healthcare/Legal**: Traditional formats, professional colors, clean structure
- **Academia**: Comprehensive sections, formal structure, publication formatting

### Format Considerations
- **Single Page**: Best for early-career professionals (0-10 years)
- **Two Pages**: Appropriate for senior professionals (10+ years)
- **Multi-Page CV**: Standard for academic and research positions
- **A4/Letter**: Ensure design works for both paper sizes

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final resume designs, professional use | Slower | Highest |
| `eco` | Quick drafts, concept exploration, testing layouts | Faster | Good |

## Multi-Turn Design Iteration

Use `session_id` to iterate on resume designs:

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern two-column resume design with a blue sidebar",
    "session_id": "resume-design-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the sidebar color to dark green and add a circular photo placeholder at the top",
    "session_id": "resume-design-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an alternative version with the same content but a single-column layout",
    "session_id": "resume-design-project"
  }'
```

## Style Variation Batch Generation

Generate multiple style variations for comparison:

```bash
# Variation A - Modern
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern resume design for a product manager with blue accents",
    "mode": "eco"
  }'

# Variation B - Minimalist
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist resume design for a product manager with black and white only",
    "mode": "eco"
  }'

# Variation C - Creative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a creative resume design for a product manager with bold colors and unique layout",
    "mode": "eco"
  }'
```

## Prompt Tips for Resume Designs

When creating resume designs, include these details in your prompt:

1. **Target Role/Industry**: Specify the job type and industry context
2. **Color Scheme**: Mention preferred colors or brand colors
3. **Layout Style**: Single-column, two-column, or multi-page
4. **Section Requirements**: List specific sections needed
5. **Visual Elements**: Skill bars, icons, charts, photo placeholder
6. **Typography Style**: Modern, classic, creative, formal
7. **Print/Digital**: Optimize for print, screen, or both

### Example Prompt Structure

```
"Create a [style] resume design for a [role/industry].
Use [color scheme] with [accent details].
Include sections for [list sections].
The layout should be [layout type].
[Additional requirements like visual elements, typography, etc.]"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Marketing creatives
- `product-photo-generation` - Professional product imagery
