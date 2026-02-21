---
name: industry-research
description: Comprehensive industry research skill providing methodologies, frameworks, and best practices for analyzing industry trends, key companies, market dynamics, and industry-specific developments across consumer, tech, healthcare, and finance sectors
tools: Read, Write, Bash, mcp__playwright_*
model: inherit
thinking:
  type: enabled
  budget_tokens: 10000
max_turns: 5
max_budget: 0.10
---

# Industry Research Skill

A comprehensive skill for conducting deep industry research across multiple sectors including consumer, technology, healthcare, and finance industries.

## Description

This skill provides reusable methodologies, frameworks, and best practices for analyzing industry trends, identifying key market players, understanding market dynamics, tracking industry news, and forecasting future outlooks.

## Core Research Areas

### 1. Industry Trends Analysis
- Current market trends and growth patterns
- Emerging technologies and innovations
- Consumer behavior shifts
- Regulatory and policy changes
- Market disruptions and transformations

### 2. Key Companies & Market Leaders
- Market leaders and their market share
- Notable players and emerging competitors
- Competitive positioning
- Company performance metrics
- Strategic initiatives and investments

### 3. Market Dynamics
- Market size and growth rates
- Key performance indicators (KPIs)
- Market segmentation
- Pricing trends
- Supply chain dynamics

### 4. Industry News & Developments
- Recent industry news and events
- Regulatory changes and compliance updates
- Major mergers and acquisitions
- Product launches and innovations
- Industry conferences and announcements

### 5. Future Outlook
- Emerging trends and opportunities
- Market predictions and forecasts
- Technology disruptions on the horizon
- Regulatory changes expected
- Investment and growth opportunities

## Research Methodology

### Phase 1: Source Identification
1. **Industry-Specific News Sources**
   - Identify top industry publications
   - Track industry trade publications
   - Monitor industry association websites
   - Follow industry analysts and thought leaders

2. **Market Data Sources**
   - Financial data platforms (Yahoo Finance, Finviz)
   - Market research reports (Gartner, Statista, industry reports)
   - Government data sources
   - Industry databases

3. **Company Information Sources**
   - Company websites and investor relations
   - Financial filings and reports
   - Industry databases (Crunchbase, PitchBook)
   - News aggregators

### Phase 2: Data Collection
1. **Browser Automation Workflow**
   - Navigate to each source using Playwright MCP servers
   - Capture screenshots for visual analysis
   - Extract structured data from pages
   - Verify data accuracy against screenshots

2. **Screenshot Analysis**
   - Always capture screenshots before extraction
   - Use Read tool to visually analyze screenshots
   - Extract only what is visible in screenshots
   - Verify extracted data matches screenshot content

### Phase 3: Analysis & Synthesis
1. **Trend Identification**
   - Group related information by theme
   - Identify patterns across multiple sources
   - Distinguish between trends and isolated events
   - Note confidence levels based on source diversity

2. **Market Analysis**
   - Compile market size and growth data
   - Compare metrics across companies
   - Identify market leaders and their positions
   - Analyze competitive dynamics

3. **Insight Generation**
   - Synthesize information into actionable insights
   - Connect trends to market implications
   - Identify opportunities and threats
   - Provide forward-looking analysis

## Industry-Specific Frameworks

### Consumer Industry Framework
- **Focus Areas:** Retail performance, e-commerce growth, consumer spending, brand analysis
- **Key Metrics:** Same-store sales, online vs. offline growth, consumer sentiment, brand value
- **Sources:** Retail Dive, Consumer Reports, NRF, Statista consumer data

### Technology Industry Framework
- **Focus Areas:** Innovation trends, market leaders, sector performance, emerging technologies
- **Key Metrics:** Market share, R&D spending, patent activity, adoption rates
- **Sources:** TechCrunch, The Verge, Ars Technica, Gartner reports

### Healthcare Industry Framework
- **Focus Areas:** Healthcare trends, regulatory changes, biotech developments, market dynamics
- **Key Metrics:** FDA approvals, clinical trial results, market size, growth rates
- **Sources:** STAT News, Fierce Healthcare, Healthcare Dive, industry reports

### Finance Industry Framework
- **Focus Areas:** Banking trends, fintech innovation, regulatory changes, market performance
- **Key Metrics:** Assets under management, loan growth, fintech adoption, regulatory compliance
- **Sources:** American Banker, Financial Times banking, Fintech News, industry reports

## Best Practices

### Data Quality Standards
- ✅ All data should be current (latest available)
- ✅ Verify data against multiple sources when possible
- ✅ Extract only what is visible in screenshots
- ✅ Note data recency and source reliability
- ✅ Distinguish between facts and opinions

### Research Workflow
1. **Start Broad:** Begin with industry overview and major trends
2. **Narrow Focus:** Drill down into specific companies and metrics
3. **Cross-Reference:** Verify information across multiple sources
4. **Synthesize:** Combine insights into coherent analysis
5. **Document:** Save all screenshots and raw data for reference

### Source Evaluation
- **Primary Sources:** Company websites, financial filings, official reports
- **Secondary Sources:** News articles, industry publications, analyst reports
- **Tertiary Sources:** Aggregators, summaries, third-party analysis
- **Reliability:** Prioritize primary sources, cross-check secondary sources

## Output Structure

All research outputs follow this directory structure:

```
outputs/
└── <agent_name>/
    └── <customer_name>/
        ├── reports/        # Final markdown research reports
        ├── scripts/         # Generated research code
        ├── raw/            # JSON/CSV data files
        └── screenshots/    # PNG screenshots of sources
```

## Report Template

```markdown
## [Industry] Research Report

**Generated:** [Date/Time]
**Research Period:** [Date range]
**Sources Analyzed:** [List of sources]

---

### Executive Summary
[2-3 paragraph overview of key findings]

---

### Industry Trends
[Current trends with analysis and sources]

---

### Key Companies & Market Leaders
[Top companies with market position and analysis]

---

### Market Dynamics
[Market size, growth rates, key metrics with sources]

---

### Recent Developments
[Industry news and events with dates and sources]

---

### Future Outlook
[Emerging trends, predictions, and opportunities]

---

### Source Attribution
[List of all sources and URLs used]
```

## Code Examples

### Basic Industry Research Workflow

```python
import asyncio
from playwright.async_api import async_playwright

async def research_industry_trends(industry_sources):
    """
    Research industry trends from multiple sources.
    
    Args:
        industry_sources (list): List of URLs to research
        
    Returns:
        dict: Research findings organized by source
    """
    findings = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        for source_url in industry_sources:
            try:
                # Navigate and capture
                await page.goto(source_url, wait_until="domcontentloaded", timeout=120000)
                await page.screenshot(path=f"screenshot_{source_url.replace('/', '_')}.png", full_page=True)
                
                # Extract data (implement based on page structure)
                # ... extraction logic ...
                
                findings[source_url] = extracted_data
            except Exception as e:
                print(f"Error researching {source_url}: {e}")
        
        await browser.close()
    
    return findings
```

### Market Data Extraction

```python
async def extract_market_metrics(page, selector_mapping):
    """
    Extract market metrics from a financial data page.
    
    Args:
        page: Playwright page object
        selector_mapping (dict): Mapping of metric names to CSS selectors
        
    Returns:
        dict: Extracted metrics
    """
    metrics = {}
    
    for metric_name, selector in selector_mapping.items():
        try:
            element = await page.query_selector(selector)
            if element:
                text = await element.inner_text()
                metrics[metric_name] = text.strip()
        except Exception as e:
            print(f"Error extracting {metric_name}: {e}")
    
    return metrics
```

## Common Research Tasks

### 1. Industry Trend Analysis
- Identify recurring themes across multiple sources
- Track trend evolution over time
- Distinguish between fads and lasting trends
- Analyze trend drivers and implications

### 2. Competitive Landscape Mapping
- Identify market leaders and their positions
- Map competitive relationships
- Analyze market share distribution
- Identify emerging competitors

### 3. Market Size Estimation
- Gather market size data from multiple sources
- Compare estimates across sources
- Note methodology differences
- Provide range estimates when sources differ

### 4. Regulatory Impact Assessment
- Track regulatory changes and proposals
- Assess impact on industry players
- Identify compliance requirements
- Forecast regulatory trends

## Integration with Agents

This skill is designed to be used by specialized industry researcher agents:
- `consumer_researcher.md` - Consumer/retail industry
- `tech_researcher.md` - Technology industry
- `healthcare_researcher.md` - Healthcare/biotech industry
- `finance_researcher.md` - Finance/banking industry

Each agent applies this skill's methodologies to their specific industry domain.

## Dependencies

- Playwright for browser automation
- Screenshot capture capabilities
- Visual analysis tools (Read tool)
- Data extraction and processing capabilities

## Performance Notes

- Research multiple sources in parallel when possible
- Cache screenshots for reference
- Save raw data for future analysis
- Organize findings by research area for easy access

