---
name: aso-optimizer
description: Comprehensive App Store Optimization (ASO) toolkit for iOS and Android apps. Use when user needs help with keyword research, competitor analysis, optimizing app store metadata (title, subtitle, description, keywords), or localizing app store content across multiple languages. Guides through ASO workflow from keyword discovery to final metadata optimization.
---

# ASO Optimizer

Comprehensive toolkit for optimizing app store presence on iOS App Store and Google Play Store.

## When to Use This Skill

Use this skill when the user needs help with:
- Generating keyword ideas for their app
- Analyzing competitor apps and keywords
- Optimizing app name, subtitle, description, or keyword field
- Localizing app store content for different markets
- Creating ASO tracking spreadsheets
- Understanding character limits and ASO best practices

## Core Workflow

The typical ASO workflow follows these steps:

### 1. Information Gathering

Ask the user for:
- **App description**: What does the app do? Key features?
- **Target audience**: Who is it for?
- **Platform(s)**: iOS, Android, or both?
- **Languages**: Which languages/markets to target?
- **Current keywords** (if any): What are they using now?

### 2. Keyword Research

Generate comprehensive keyword list using multiple approaches:

**A. Semantic Analysis**
- Extract core concepts from app description
- Generate action verbs, feature nouns, user benefits
- Create variations using synonyms and related terms
- Reference: `references/keyword-strategies.md` for detailed methods

**B. Competitor Analysis**
- Use `web_search` to find top competitor apps
- Search patterns: 
  - `"best [category] apps" iOS/Android`
  - `"[app name]" site:apps.apple.com` for specific competitors
  - `"[category] app keywords"` for ASO discussions
- Extract keywords from competitor titles, subtitles, descriptions
- Reference: `references/competitor-analysis.md` for analysis framework

**C. User Intent Mapping**
- Generate keywords based on user search behavior
- Include: navigational, informational, transactional intents
- Create long-tail keyword variations

**D. Categorization**
Organize keywords into tiers:
- **Tier 1**: Primary keywords (high relevance, high volume) → for title/subtitle
- **Tier 2**: Secondary keywords (medium relevance/volume) → for keyword field
- **Tier 3**: Long-tail keywords (specific, lower competition) → for description

### 3. Metadata Optimization

Generate optimized metadata for each platform:

**iOS App Store:**
- **App Name** (30 chars): Include primary keyword
- **Subtitle** (30 chars): Include secondary keyword
- **Keyword Field** (100 chars): Comma-separated, no spaces, no duplicates from name/subtitle
- **Description** (4000 chars): Not indexed, focus on conversion

**Google Play:**
- **Title** (30 chars): Include primary keyword
- **Short Description** (80 chars): Include keywords, indexed by search
- **Long Description** (4000 chars): Fully indexed, use keywords naturally throughout

Reference `references/store-guidelines.md` for character limits and best practices.

### 4. Localization

For each target language:
- Translate keywords (not just word-for-word, consider local search behavior)
- Research local competitors
- Adapt positioning for cultural differences
- Create localized metadata optimized for each market

### 5. Output Delivery

Create organized deliverables:

**Option A: Markdown Report**
- Keyword research findings
- Competitor analysis summary
- Optimized metadata for each platform/language
- Recommendations and next steps

**Option B: Excel Spreadsheet**
Use the xlsx skill to create tracking spreadsheet with sheets for:
- Keyword inventory (with scores/tiers)
- Competitor analysis
- Metadata variations
- Localization matrix
- Performance tracking template

**Option C: Both**
Comprehensive report + spreadsheet for tracking

## Advanced Features

### Competitor Deep Dive

When user requests detailed competitor analysis:
1. Use `web_search` to find top 5-10 competitors
2. For each competitor:
   - Extract all visible metadata
   - Identify keywords used
   - Note positioning and value proposition
   - Check ranking indicators (ratings, reviews)
3. Create competitive keyword gap analysis
4. Reference `references/competitor-analysis.md` for complete framework

### Multi-Language Optimization

When user supports multiple languages:
1. Start with primary language (usually English)
2. For each additional language:
   - Research local search behavior
   - Check local top apps in category
   - Translate and adapt keywords
   - Create localized metadata
3. Output: Matrix showing all languages side-by-side

### Keyword Iteration

When user has existing keywords to improve:
1. Analyze current keyword performance (if data available)
2. Identify gaps vs competitors
3. Suggest additions, removals, replacements
4. Prioritize changes by expected impact

## Important Reminders

### ASO Best Practices
- Never use competitor brand names in keywords
- Avoid keyword stuffing (unnatural, hurts conversion)
- Focus on relevance over volume
- Test and iterate based on results
- Keep descriptions user-focused, not just keyword-focused

### Character Limits
Always check character counts against limits:
- iOS: 30/30/100 (name/subtitle/keywords)
- Android: 30/80/4000 (title/short/long description)

### Search Tool Usage
- Use `web_search` liberally for competitor research
- Search for actual App Store listings
- Look for review sites and "best of" lists
- Extract natural language keywords from reviews

### Reference Files
- Load `references/store-guidelines.md` when user needs ASO basics or character limits
- Load `references/keyword-strategies.md` for keyword generation techniques
- Load `references/competitor-analysis.md` for systematic competitor research

## Example Interactions

**Example 1: Complete ASO from scratch**
```
User: "I need help with ASO for my photo editing app"
1. Ask about app features, target audience, platforms, languages
2. Generate keyword list using semantic analysis and competitor research
3. Create optimized metadata for iOS and Android
4. Deliver markdown report with all recommendations
```

**Example 2: Competitor analysis**
```
User: "Analyze my competitors for my fitness tracking app"
1. Use web_search to find top fitness tracking apps
2. Extract keywords from their metadata
3. Identify gaps and opportunities
4. Create competitive analysis report
```

**Example 3: Localization**
```
User: "I need to localize my app for Italian and Spanish markets"
1. Start with English keywords
2. Research local competitors in Italy and Spain
3. Translate and adapt keywords culturally
4. Create localized metadata for each market
5. Output spreadsheet with language comparison
```

**Example 4: Keyword refresh**
```
User: "My current keywords aren't working well"
1. Review current keywords
2. Analyze competitor keywords they're missing
3. Suggest specific replacements with rationale
4. Prioritize changes by expected impact
```

## Workflow Checklist

For every ASO project, ensure:
- [ ] Understand app functionality and target users
- [ ] Generate comprehensive keyword list (50+ keywords)
- [ ] Analyze at least 3-5 competitors
- [ ] Create metadata for all requested platforms
- [ ] Verify all character limits are respected
- [ ] Organize keywords by priority/tier
- [ ] Provide actionable recommendations
- [ ] Include localization if multi-language
- [ ] Create tracking spreadsheet if requested
- [ ] Explain the reasoning behind keyword choices

## Output Quality Standards

Every ASO deliverable should:
- Be immediately actionable (ready to copy-paste into app store)
- Include variety of keyword types (brand, category, feature, benefit, long-tail)
- Respect all platform guidelines and limits
- Show clear reasoning for keyword selection
- Provide context about competition and difficulty
- Include next steps or testing recommendations

## Tools Integration

This skill works well with:
- `web_search`: For competitor research and market analysis
- `xlsx` skill: For creating comprehensive tracking spreadsheets
- `docx` skill: For formal ASO reports or client deliverables
