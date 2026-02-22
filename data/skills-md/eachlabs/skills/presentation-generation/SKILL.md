---
name: presentation-generation
description: Generate professional presentations and slide decks using each::sense AI. Create pitch decks, business presentations, training materials, conference talks, and more with AI-powered slide generation.
metadata:
  author: eachlabs
  version: "1.0"
---

# Presentation Generation

Generate professional presentations and slide decks using each::sense. This skill creates visually compelling slides for business presentations, pitch decks, educational content, and more.

## Features

- **Business Presentations**: Professional slides for corporate meetings and reports
- **Pitch Decks**: Compelling investor presentations with clear narratives
- **Sales Presentations**: Persuasive slides for client proposals and demos
- **Educational Slides**: Lecture and course materials with clear visuals
- **Training Materials**: Onboarding and skill development presentations
- **Product Launches**: Announcement decks with impact
- **Quarterly Reports**: Data-driven presentations with visualizations
- **Conference Talks**: Engaging slides for keynotes and sessions

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide business presentation about digital transformation strategy for enterprise companies. Include title slide, agenda, key challenges, solutions, case studies, implementation roadmap, and closing slide.",
    "mode": "max"
  }'
```

## Presentation Types & Use Cases

| Type | Slides | Best For |
|------|--------|----------|
| Pitch Deck | 10-15 | Investor meetings, fundraising |
| Sales Deck | 8-12 | Client proposals, product demos |
| Business Presentation | 10-20 | Strategy meetings, executive briefings |
| Training Presentation | 15-30 | Onboarding, skill development |
| Conference Talk | 20-40 | Keynotes, technical sessions |
| Quarterly Report | 10-15 | Stakeholder updates, board meetings |
| Product Launch | 10-15 | Announcements, marketing events |

## Use Case Examples

### 1. Business Presentation from Topic

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 12-slide business presentation on AI adoption in healthcare. Include: title slide, executive summary, current state of healthcare AI, key use cases (diagnosis, drug discovery, patient care), implementation challenges, ROI analysis, case study examples, future trends, recommendations, and conclusion with next steps. Professional corporate style with blue color scheme.",
    "mode": "max"
  }'
```

### 2. Pitch Deck for Investors

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide startup pitch deck for a fintech company that provides AI-powered expense management for small businesses. Include: cover slide with company name TechExpense, problem statement showing SMB pain points, solution overview, product demo screenshots, market size ($50B TAM), business model (SaaS subscription), traction (10K users, 40% MoM growth), competitive landscape, team slide, and ask slide ($5M Series A). Modern, clean design with fintech aesthetic.",
    "mode": "max"
  }'
```

### 3. Sales Presentation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an 8-slide sales presentation for enterprise cloud security software. Include: title slide, client pain points (data breaches, compliance, complexity), our solution overview, key features (real-time monitoring, automated compliance, AI threat detection), customer success stories with metrics, pricing tiers, implementation timeline, and call-to-action slide. Professional but engaging style, use security-themed visuals.",
    "mode": "max"
  }'
```

### 4. Educational/Lecture Slides

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 15-slide educational presentation on Machine Learning fundamentals for university students. Include: title slide, learning objectives, what is ML (definition), types of ML (supervised, unsupervised, reinforcement), key algorithms overview, neural networks basics, real-world applications, hands-on exercise introduction, common pitfalls, best practices, resources for further learning, summary, and Q&A slide. Academic style with diagrams and visualizations.",
    "mode": "max"
  }'
```

### 5. Training Presentation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 20-slide employee onboarding training presentation for a tech company. Include: welcome slide, company history and mission, organizational structure, core values, team introductions section, key policies (remote work, PTO, benefits), tools and systems overview (Slack, Jira, GitHub), security and compliance training, first week checklist, 30-60-90 day goals, mentorship program, career development paths, FAQ section, key contacts, and closing slide with encouragement. Friendly, approachable design with company brand colors (teal and orange).",
    "mode": "max"
  }'
```

### 6. Product Launch Deck

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 12-slide product launch presentation for a new AI-powered fitness app called FitGenius. Include: dramatic title slide, the fitness problem (lack of personalization), introducing FitGenius, key features (AI coach, adaptive workouts, nutrition tracking, progress analytics), how it works (3-step process), app screenshots showcase, early user testimonials, pricing plans, launch timeline, press and influencer strategy, and closing call-to-action. Energetic, modern design with gradient colors (purple to orange).",
    "mode": "max"
  }'
```

### 7. Quarterly Report Presentation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide Q4 2024 quarterly report presentation for a SaaS company. Include: title slide with company logo placeholder, executive summary with key metrics, revenue performance (show $12M ARR, 25% YoY growth), customer metrics (500 new customers, 95% retention), product updates shipped this quarter, team growth (20 new hires), challenges faced and lessons learned, Q1 2025 priorities and goals, financial outlook, and thank you slide. Data-driven with charts and graphs, professional corporate style.",
    "mode": "max"
  }'
```

### 8. Conference Talk Slides

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 25-slide conference talk presentation titled Building Scalable Microservices: Lessons from 1 Million RPS. Include: title slide with speaker name placeholder, about me slide, agenda, the scaling journey story (monolith to microservices), architecture evolution diagrams, key technical decisions, database strategies, caching layers, message queues, monitoring and observability, failure stories and recovery, performance benchmarks, cost optimization, team structure, lessons learned (5 slides with one key insight each), what we would do differently, future roadmap, resources and references, Q&A slide, and contact/social media slide. Tech conference style, dark theme with code snippets.",
    "mode": "max"
  }'
```

### 9. Webinar Slides

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 15-slide webinar presentation on Email Marketing Best Practices for E-commerce in 2025. Include: title slide with webinar branding, host introduction, agenda with timing, why email still matters (stats), building your list ethically, segmentation strategies, personalization techniques, automation workflows (welcome, abandoned cart, win-back), subject line optimization, mobile-first design, A/B testing framework, deliverability tips, measuring success (KPIs), live Q&A slide, and special offer slide with CTA. Marketing-focused design, vibrant but professional.",
    "mode": "max"
  }'
```

### 10. Team Meeting Presentation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an 8-slide weekly team meeting presentation for an engineering team. Include: title slide with date placeholder, sprint progress (velocity chart, completed vs planned), blockers and dependencies, demo highlights (2 features shipped), upcoming priorities for next sprint, team announcements (new hire, PTO), metrics dashboard (bugs fixed, deployment frequency, incident count), and open discussion slide. Simple, functional design focused on clarity, light theme.",
    "mode": "max"
  }'
```

## Best Practices

### Content Structure
- **Start with impact**: Hook your audience with a compelling opening
- **One idea per slide**: Keep slides focused and scannable
- **Visual hierarchy**: Use headings, subheadings, and bullet points effectively
- **Data visualization**: Use charts and graphs for complex data
- **Consistent design**: Maintain visual consistency throughout

### Slide Design
- **Minimal text**: Aim for 6 words per bullet, 6 bullets max per slide
- **High contrast**: Ensure readability with proper color contrast
- **White space**: Give content room to breathe
- **Consistent fonts**: Use 2-3 fonts maximum
- **Quality images**: Use relevant, high-resolution visuals

### Presentation Types
- **Pitch decks**: Focus on story, problem-solution, and clear ask
- **Sales presentations**: Lead with value, support with proof
- **Training materials**: Progressive disclosure, include exercises
- **Conference talks**: Big ideas, memorable visuals, minimal text

## Prompt Tips for Presentations

When creating presentations, include these details in your prompt:

1. **Slide count**: Specify how many slides you need
2. **Structure**: List the sections/slides you want included
3. **Audience**: Who will view this presentation?
4. **Style**: Corporate, modern, playful, academic, etc.
5. **Colors**: Brand colors or preferred color scheme
6. **Data points**: Include specific numbers, metrics, or statistics
7. **Visuals**: Request charts, diagrams, or specific imagery

### Example Prompt Structure

```
"Create a [number]-slide [type] presentation about [topic].
Include: [list of slides/sections].
Audience: [who will view it].
Style: [design preferences].
[Additional requirements like colors, data points, etc.]"
```

## Mode Selection

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final presentations, client-facing decks, important meetings | Slower | Highest |
| `eco` | Quick drafts, internal meetings, concept exploration | Faster | Good |

## Multi-Turn Presentation Iteration

Use `session_id` to iterate and refine your presentation:

```bash
# Initial presentation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide pitch deck for a sustainable fashion marketplace",
    "session_id": "pitch-deck-project"
  }'

# Add more slides
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add 3 more slides: one for partnerships, one for sustainability metrics, and one for media coverage",
    "session_id": "pitch-deck-project"
  }'

# Refine specific slide
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Update the market size slide with more detailed TAM/SAM/SOM breakdown",
    "session_id": "pitch-deck-project"
  }'

# Change design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the design more minimalist with earth tones to match our sustainability brand",
    "session_id": "pitch-deck-project"
  }'
```

## Batch Presentation Variations

Generate multiple versions for different audiences:

```bash
# Version for investors
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide pitch deck for our AI analytics product - investor focused, emphasize market size, growth metrics, and funding ask",
    "mode": "eco"
  }'

# Version for enterprise clients
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide sales deck for our AI analytics product - enterprise client focused, emphasize ROI, security, integration capabilities",
    "mode": "eco"
  }'

# Version for technical audience
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-slide technical overview for our AI analytics product - developer focused, emphasize architecture, APIs, and technical capabilities",
    "mode": "eco"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Meta ad creatives
- `product-photo-generation` - Product imagery for slides
