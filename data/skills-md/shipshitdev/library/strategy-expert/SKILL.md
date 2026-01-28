---
name: strategy-expert
description: This skill should be used when users need help with content strategy, persona building, competitive analysis, content planning, or brand voice consistency. It activates when users ask about content strategy, building personas or target audiences, competitive analysis requests, content planning and ideation, or brand voice questions.
---

# Content Strategy Expert

## Overview

This skill enables Claude to assist users with comprehensive content strategy tasks including building customer personas from analytics data, conducting competitive content analysis, planning content calendars, managing research-to-content workflows, and ensuring brand voice consistency across all content.

## When to Use This Skill

This skill activates automatically when users:

- Ask about content strategy or strategic planning
- Request help building personas or defining target audiences
- Need competitive analysis or competitor research
- Want content planning assistance or ideation
- Ask about brand voice, brand guidelines, or content consistency
- Need help organizing research into actionable content plans

## Core Capabilities

### 1. Build Customer Personas from Analytics Data

To build customer personas from analytics data:

1. **Analyze Engagement Data**

   - Review analytics data from analytics platform (discover from project)
   - Identify patterns in audience engagement
   - Segment audiences by content preferences, platform behavior, and engagement patterns
   - Extract demographics, goals, and pain points from content performance data

2. **Synthesize Persona Profiles**

   - Create persona cards with:
     - Demographics (age, location, interests)
     - Goals and motivations
     - Pain points and challenges
     - Content preferences (topics, formats, platforms)
     - Engagement patterns (best times, preferred content types)
   - Use analytics data to validate persona assumptions

3. **Generate Persona Documentation**
   - Create structured persona profiles in content management platform
   - Link personas to content performance data
   - Enable persona-based content targeting in content creation tools

**Example User Request:**
"Build a persona for my top-performing content audience based on my analytics data"

**Integration (discover from project):**

- Analytics Platform: Extract engagement data
- Content Management Platform: Store and manage personas
- Content Creation Tools: Use personas for content targeting

### 2. Competitive Content Analysis

To conduct competitive content analysis:

1. **Identify Competitors**

   - Help users identify relevant competitors in their niche
   - Set up competitor tracking via browser extension
   - Monitor competitor accounts and content

2. **Analyze Competitor Content**

   - Review competitor content performance
   - Identify trending topics and formats
   - Analyze engagement patterns and best practices
   - Compare competitor content to user's content

3. **Generate Competitive Intelligence**
   - Create competitive analysis reports
   - Identify content gaps and opportunities
   - Recommend content strategies based on competitor insights
   - Benchmark user's content performance against competitors

**Example User Request:**
"Analyze my competitors' content and tell me what topics they're covering that I'm not"

**Integration (discover from project):**

- Browser Extension: Track competitor accounts
- Analytics Platform: Compare performance metrics
- Content Management Platform: Store competitive intelligence

### 3. Content Calendar Planning

To help users plan content calendars:

1. **Analyze Historical Performance**

   - Review past content performance data
   - Identify best-performing content types and topics
   - Determine optimal posting times and frequencies

2. **Create Content Calendar**

   - Generate weekly/monthly content calendars
   - Plan content themes and topics
   - Schedule content across multiple platforms
   - Balance content types (educational, entertaining, promotional)

3. **Optimize Calendar Strategy**
   - Recommend content mix based on performance data
   - Suggest optimal posting times per platform
   - Plan content series and campaigns
   - Align calendar with business goals and events

**Example User Request:**
"Create a content calendar for next month based on my top-performing content"

**Integration (discover from project):**

- Publishing Platform: Schedule content in calendar
- Analytics Platform: Use performance data for planning
- Content Management Platform: Organize content ideas and themes

### 4. Research-to-Content Workflow

To convert research into actionable content:

1. **Organize Research**

   - Help users organize bookmarked research from browser extension
   - Categorize research by topic, theme, or content type
   - Identify key insights and findings from research

2. **Generate Content Outlines**

   - Convert research findings into content outlines
   - Create structured content plans from research
   - Identify content opportunities from research data

3. **Create Content from Research**
   - Generate video/article scripts from research outlines
   - Convert research into presentation-style content
   - Ensure research is properly cited and attributed

**Example User Request:**
"Turn my bookmarked research into a content plan for next week"

**Integration (discover from project):**

- Browser Extension: Import bookmarked research
- Content Creation Tools: Generate content from research outlines
- Content Management Platform: Organize research and content plans

### 5. Brand Voice Consistency

To ensure brand voice consistency across content:

1. **Understand Brand Guidelines**

   - Review user's brand guidelines (if available)
   - Identify brand voice characteristics
   - Understand brand values and messaging

2. **Enforce Brand Voice**

   - Ensure all generated content matches brand voice
   - Review content for brand consistency
   - Suggest improvements to align with brand guidelines

3. **Maintain Brand Standards**
   - Check content for brand compliance
   - Ensure consistent messaging across platforms
   - Recommend brand voice improvements

**Example User Request:**
"Review my content to ensure it matches my brand voice"

**Integration (discover from project):**

- Content Creation Tools: Apply brand voice in content generation
- Content Management Platform: Store and manage brand guidelines
- Publishing Platform: Ensure brand consistency in distribution

## Project Context Discovery

**Before providing strategy recommendations, discover the project's context:**

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for platform architecture
   - Review `.agent/SYSTEM/SUMMARY.md` for capabilities overview
   - Look for brand voice guidelines in project docs

2. **Identify Platform Components:**
   - Scan codebase for content creation tools
   - Look for publishing/distribution integrations
   - Check for analytics platform integrations

3. **Discover Brand Voice:**
   - Look for brand guidelines or style guides
   - Check for copywriting documentation
   - Review existing content examples

**Common Content Platform Architecture:**

- Browser Extension: Trend discovery and bookmarking
- Content Creation Tools: AI content generation
- Publishing Platform: Multi-platform distribution
- Analytics Platform: Performance tracking
- Content Management Platform: Content library and organization

**Content Intelligence Workflow:**

```
Trend Detection → Content Generation → Distribution → Analytics → Optimization
```

## Best Practices

1. **Discover Project Context First**: Scan project documentation to understand platform, brand voice, and workflows
2. **Data-Driven Decisions**: Always base recommendations on actual analytics data from the project
3. **Platform-Specific Strategy**: Consider platform-specific requirements and best practices
4. **Brand Consistency**: Ensure all content recommendations align with brand guidelines
5. **Competitive Intelligence**: Use competitor analysis to identify opportunities, not to copy
6. **Continuous Optimization**: Recommend iterative improvements based on performance data

## Resources

### references/

- `platform-architecture.md`: Platform architecture and features (discover from project docs)
- `content-strategy-guide.md`: Content strategy best practices and frameworks

### assets/

- `persona-template.md`: Template for creating customer personas
- `content-calendar-template.md`: Template for content calendar planning
- `competitive-analysis-template.md`: Template for competitive analysis reports
