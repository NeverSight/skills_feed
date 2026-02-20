---
name: gtm-reporting
description: Generates GTM implementation documentation, reporting impact analysis, GA4 report configurations, and stakeholder summaries. Use when users need to "document GTM implementation", "what reports can I build", "create event schema docs", "generate stakeholder summary", "analyze reporting impact", or want to understand business value of tracking data. Creates technical documentation, suggests GA4 explorations, defines remarketing audiences, and translates technical events into business insights.
---

# GTM Reporting - Documentation & Impact Analysis

Generate comprehensive documentation and analyze the reporting impact of your GTM tracking implementation.

## Core Mission

Transform technical tracking implementation into business-focused documentation that:
1. Explains what was implemented (technical docs)
2. Shows what insights are now possible (reporting impact)
3. Recommends specific reports to build (GA4 configurations)
4. Defines high-value audiences (remarketing/segmentation)
5. Translates events into business value (stakeholder summary)

## Workflow

### Phase 1: Context Loading

**Step 1.1: Load Implementation Details**
```
Check for implementation artifacts:
- gtm-tracking-plan.json (from gtm-strategy)
- gtm-implementation-log.json (from gtm-implementation)
- gtm-test-results.json (from gtm-testing)

If missing → Ask user to describe what was implemented
```

**Step 1.2: Analyze Implementation Scope**
```
Extract key information:
- Events implemented (names, parameters)
- Elements tracked (CTAs, forms, navigation, etc.)
- Business model (SaaS, e-commerce, lead-gen)
- Primary goals (conversions, engagement, leads)
```

### Phase 2: Technical Documentation Generation

Create comprehensive implementation documentation for developers and analysts.

**Document 2.1: Event Schema Documentation**

```markdown
# GTM Tracking Implementation - Event Schema

Last Updated: [Date]
GTM Container: GTM-XXXXXX
Implementation Version: 1.0

## Events Overview

This document describes all custom events implemented in Google Tag Manager.

### Event: cta_click

**Description**: Fires when a user clicks any call-to-action button on the site

**Trigger**: Custom Event "cta_click"

**Parameters**:
| Parameter | Type | Description | Example Values | Required |
|-----------|------|-------------|----------------|----------|
| cta_location | string | Section of page where CTA is located | "hero", "pricing", "footer" | Yes |
| cta_type | string | Visual style of CTA | "primary", "secondary", "text" | No |
| cta_text | string | Text content of button | "Get Started", "Book Demo" | Yes |
| cta_destination | string | Target URL or action | "/signup", "/pricing" | Yes |

**Sample DataLayer Push**:
```javascript
{
  event: 'cta_click',
  cta_location: 'hero',
  cta_type: 'primary',
  cta_text: 'Get Started',
  cta_destination: '/signup'
}
```

**GTM Configuration**:
- Variables: DLV - CTA Location, DLV - CTA Type, DLV - CTA Text, DLV - CTA Destination
- Trigger: CE - CTA Click
- Tag: GA4 - CTA Click

**Elements Tracked**: 12 CTA buttons across site

---

### Event: form_submit

**Description**: Fires when a user submits any form on the site

**Trigger**: Custom Event "form_submit"

**Parameters**:
| Parameter | Type | Description | Example Values | Required |
|-----------|------|-------------|----------------|----------|
| form_name | string | Identifier for the form | "contact", "newsletter", "demo" | Yes |
| form_location | string | Page section where form is located | "hero", "footer", "sidebar" | Yes |
| form_type | string | Purpose/category of form | "contact_request", "email_capture" | Yes |

**Sample DataLayer Push**:
```javascript
{
  event: 'form_submit',
  form_name: 'newsletter',
  form_location: 'footer',
  form_type: 'email_capture'
}
```

**GTM Configuration**:
- Variables: DLV - Form Name, DLV - Form Location, DLV - Form Type
- Trigger: CE - Form Submit
- Tag: GA4 - Form Submit

**Elements Tracked**: 3 forms across site

[Continue for all events...]
```

**Document 2.2: Implementation Summary**

```markdown
# GTM Implementation Summary

## Overview

This document summarizes the GTM tracking implementation completed on [Date].

## Scope

**Events Implemented**: 5 custom events
**Elements Tracked**: 23 total elements
- 12 CTA buttons
- 8 navigation links
- 3 forms

**Code Changes**: 8 files modified

## Technical Stack

- Framework: Next.js 16.1.6 (App Router)
- GTM Container: GTM-XXXXXX
- GA4 Property: [Property ID]
- Implementation Method: DataLayer + GTM API

## Events Summary

| Event Name | Purpose | Elements | Priority |
|------------|---------|----------|----------|
| cta_click | Track conversion intent via CTA clicks | 12 | P0 |
| form_submit | Capture lead submissions | 3 | P0 |
| form_start | Measure form abandonment | 3 | P0 |
| navigation_click | Understand user journey | 8 | P1 |
| video_play | Measure content engagement | 1 | P1 |

## GTM Configuration

**Created via API**:
- 12 Data Layer Variables
- 5 Custom Event Triggers
- 5 GA4 Event Tags

**Container Version**: 42
**Published**: [Date]

## Files Modified

1. `app/page.tsx` - Added CTA and form tracking (4 elements)
2. `components/Navbar.tsx` - Added navigation tracking (5 elements)
3. `components/Footer.tsx` - Added navigation and form tracking (4 elements)
... [list all files]

## Testing Status

All events validated across 3 tiers:
✓ Tier 1: Browser Console (dataLayer)
✓ Tier 2: GTM Preview Mode
✓ Tier 3: GA4 DebugView

## Maintenance

**Adding New Tracking**:
1. Add analytics classes to element (js-track js-cta js-click js-location)
2. Implement dataLayer.push() in onClick handler
3. Create GTM variable/trigger/tag (or use existing)
4. Test in Preview mode
5. Publish container

**Modifying Existing Tracking**:
1. Update dataLayer.push() parameters in code
2. Update GTM tag event parameters if needed
3. Test and publish

## Support

For questions or issues, contact: [Technical Owner]
```

### Phase 3: Reporting Impact Analysis

Analyze what reports and insights are now possible with this tracking.

**Analysis 3.1: GA4 Reports Enabled**

```markdown
# Reporting Capabilities - GA4

## New Reports Enabled by Implementation

### 1. CTA Performance Dashboard

**Purpose**: Understand which CTAs drive conversions

**Metrics**:
- CTA clicks by location (hero vs pricing vs footer)
- CTA clicks by type (primary vs secondary)
- CTA click-through rate by page
- CTA → Form submission conversion rate

**How to Build**:
1. GA4 → Explore → Free Form
2. Dimensions: Event name, CTA location, CTA type, CTA text
3. Metrics: Event count, Conversions
4. Segment: Users who clicked CTA → Users who submitted form

**Business Value**: Optimize CTA placement and copy based on conversion data

---

### 2. Form Funnel Analysis

**Purpose**: Measure form abandonment and completion

**Funnel Steps**:
1. form_start (user begins filling form)
2. form_submit (user submits form)
3. /thank-you (confirmation page view)

**Metrics**:
- Abandonment rate: (form_start - form_submit) / form_start
- Completion rate: form_submit / form_start
- Average time to complete: form_submit timestamp - form_start timestamp

**How to Build**:
1. GA4 → Explore → Funnel Exploration
2. Step 1: form_start
3. Step 2: form_submit
4. Step 3: page_view (page_location contains /thank-you)
5. Breakdown by form_name

**Business Value**: Identify form friction points and improve conversion rates

---

### 3. User Journey Mapping

**Purpose**: Understand how users navigate the site

**Path Analysis**:
- Entry page → First navigation click → Second click → Conversion
- Most common paths to pricing page
- Navigation patterns of converting vs non-converting users

**How to Build**:
1. GA4 → Explore → Path Exploration
2. Starting point: page_view OR navigation_click
3. Step types: Events and pages
4. Ending point: form_submit OR trial_start

**Business Value**: Optimize site structure and content flow based on user behavior

[Continue for all report types...]
```

**Analysis 3.2: Custom Dashboards**

Recommend specific dashboard configurations:

```markdown
## Recommended Dashboards

### Executive Dashboard: Conversion Overview

**Audience**: C-suite, Marketing leadership

**Metrics** (Weekly):
- Total CTA clicks (trend)
- Form submissions (trend)
- CTA → Form conversion rate
- Top converting CTAs (by location)
- Form abandonment rate

**Format**: Looker Studio dashboard

**Value**: High-level conversion health monitoring

---

### Marketing Dashboard: Campaign Performance

**Audience**: Marketing team

**Metrics** (Daily):
- CTA clicks by traffic source (organic, paid, social)
- Form submissions by campaign
- Cost per form submission (CPC data + form_submit count)
- Landing page → CTA → Form funnel by campaign

**Format**: GA4 Custom Report

**Value**: Measure campaign ROI and optimize spend

---

### Product Dashboard: Engagement Metrics

**Audience**: Product team

**Metrics** (Weekly):
- Navigation patterns (top clicked links)
- Video engagement (play rate, completion rate)
- Feature page views → CTA clicks
- Time on site by engagement level

**Format**: GA4 Explorations

**Value**: Understand product interest and optimize content
```

### Phase 4: Audience Definitions

Define high-value remarketing audiences based on tracked events.

**Audience 4.1: Remarketing Audiences**

```markdown
# Remarketing Audience Definitions

## Audience: High-Intent Visitors

**Criteria**:
- Clicked pricing CTA (cta_click where cta_destination = /pricing)
  OR
- Submitted contact form (form_submit where form_type = contact_request)

Within last 7 days

**Size Estimate**: 5-10% of traffic

**Business Value**: Users showing strong purchase intent

**Remarketing Strategy**:
- Message: Case studies, testimonials, urgency ("Limited time offer")
- Channel: Google Ads, Facebook Ads
- Bid adjustment: +50% (high conversion probability)

**Expected ROI**: 3-5x higher conversion rate vs cold traffic

---

## Audience: Demo Requesters

**Criteria**:
- Clicked "Book Demo" CTA (cta_click where cta_text contains "Demo")
  OR
- Submitted demo form (form_submit where form_name = demo)

Within last 14 days

**Size Estimate**: 1-3% of traffic

**Business Value**: Highest-intent audience, sales-ready

**Use Cases**:
1. Sales follow-up priority list
2. Email nurture sequence
3. Retargeting with customer success stories

**Expected ROI**: 10-20x higher conversion rate

---

## Audience: Engaged Browsers

**Criteria**:
- Viewed 3+ pages
  AND
- Clicked 2+ CTAs (any type)
  AND
- Time on site > 2 minutes

Within last 30 days

**Size Estimate**: 15-20% of traffic

**Business Value**: Researching actively, not yet converted

**Remarketing Strategy**:
- Message: Educational content, comparison guides
- Channel: Display ads, email (if captured)
- Goal: Move to high-intent with valuable content

**Expected ROI**: 2-3x higher conversion rate

[Continue for all audience definitions...]
```

### Phase 5: Stakeholder Summary

Create non-technical summary for business stakeholders.

**Summary 5.1: Executive Summary**

```markdown
# GTM Tracking Implementation - Executive Summary

## What We Built

We implemented comprehensive website analytics tracking that captures user behavior across all key conversion points.

## What This Means for the Business

### Before
- Limited visibility into which marketing efforts drive conversions
- No data on where users drop off in conversion funnel
- Guesswork for website optimization decisions
- Unable to identify high-value visitors for remarketing

### After
- Full visibility into user journey from landing to conversion
- Precise data on CTA performance and form abandonment
- Data-driven optimization of website and campaigns
- Ability to target high-intent visitors with personalized messaging

## Key Capabilities Unlocked

1. **CTA Optimization** ($)
   - See which call-to-action buttons drive conversions
   - A/B test button copy and placement with real data
   - **Impact**: 10-30% increase in conversion rate typical

2. **Form Funnel Analysis** ($$)
   - Identify exactly where users abandon forms
   - Reduce friction, improve completion rates
   - **Impact**: 5-15% increase in leads typical

3. **Campaign Attribution** ($$$)
   - Know which campaigns drive qualified leads
   - Optimize ad spend based on conversion data
   - **Impact**: 20-40% improvement in CAC typical

4. **High-Intent Audiences** ($$)
   - Target visitors who clicked pricing or requested demo
   - 3-5x higher conversion rate on retargeting
   - **Impact**: Significant ROI improvement on ad spend

## Investment vs Return

**Implementation Cost**:
- Time: 8 hours total (mostly automated)
- Ongoing: No additional cost (built on existing GA4/GTM)

**Expected Annual Value**:
- Improved conversion rates: $XXk-XXXk (depends on traffic)
- Reduced CAC from better targeting: $XXk
- Time saved vs manual reporting: $XXk

**ROI**: 10-50x typical (based on industry benchmarks)

## Next Steps

1. **Week 1-2**: Monitor data collection, validate accuracy
2. **Week 3-4**: Build recommended dashboards
3. **Month 2**: Launch remarketing to high-intent audiences
4. **Month 3**: Begin A/B testing CTAs based on data

## Questions?

Contact [Technical Owner] for implementation details or [Marketing Owner] for strategic questions.
```

### Phase 6: Output Generation

Generate all documentation files:

**Files to Create**:
1. `gtm-event-schema.md` - Technical event documentation
2. `gtm-implementation-summary.md` - Implementation overview
3. `gtm-reporting-capabilities.md` - Reports and insights enabled
4. `gtm-audience-definitions.md` - Remarketing audience specs
5. `gtm-executive-summary.md` - Stakeholder summary (non-technical)

**Naming Convention**: All files prefixed with `gtm-` for easy identification

### Phase 7: Next Steps Recommendations

Provide actionable next steps:

```
=== GTM Implementation Documentation Complete ===

Documentation generated:
✓ Event schema (technical)
✓ Implementation summary
✓ Reporting capabilities analysis
✓ Audience definitions
✓ Executive summary (stakeholder-friendly)

All files saved to project root.

--- Recommended Next Steps ---

Week 1-2: Data Validation
[ ] Monitor events in GA4 Reports (not DebugView)
[ ] Verify event counts match expectations
[ ] Check that parameters are populating correctly
[ ] Identify any gaps or issues

Week 3-4: Build Dashboards
[ ] Create CTA Performance dashboard in Looker Studio
[ ] Set up Form Funnel in GA4 Explorations
[ ] Build User Journey path analysis
[ ] Configure conversion tracking

Month 2: Activate Audiences
[ ] Create "High-Intent Visitors" audience in GA4
[ ] Export to Google Ads for remarketing
[ ] Set up personalized ad campaigns
[ ] Monitor performance vs cold traffic

Month 3: Optimize & Iterate
[ ] A/B test top-performing CTAs (new copy/placement)
[ ] Optimize forms based on abandonment data
[ ] Adjust marketing spend based on attribution data
[ ] Refine audience definitions based on conversion data

--- Support Resources ---

Technical Documentation: See gtm-event-schema.md
Business Case: See gtm-executive-summary.md
Reporting Guide: See gtm-reporting-capabilities.md

Questions? Review documentation or contact implementation team.
```

## Assets

### assets/doc-templates/implementation-summary.md
Template for technical implementation documentation

### assets/doc-templates/stakeholder-summary.md
Template for executive/business summary

## Important Guidelines

### Documentation Principles

**1. Two Audiences, Two Formats**:
- Technical docs (engineers, analysts): Detailed, code examples, schema
- Business docs (executives, marketing): High-level, ROI-focused, no jargon

**2. Actionable Recommendations**:
- Don't just describe tracking - explain what to do with data
- Provide specific report configurations, not generic ideas
- Include expected business impact for each recommendation

**3. Realistic ROI Estimates**:
- Base estimates on industry benchmarks or conservative assumptions
- Explain methodology (e.g., "10% conversion lift typical for CTA optimization")
- Avoid overpromising - underpromise and overdeliver

**4. Maintenance Focus**:
- Include instructions for adding new tracking
- Document where to find configurations in GTM
- Provide troubleshooting for common issues

### Translation: Technical → Business

**Technical**: "Implemented cta_click event with 4 parameters"

**Business**: "Now tracking which call-to-action buttons drive conversions, enabling data-driven optimization of button copy and placement (typical 10-30% conversion lift)"

**Technical**: "Created form_start and form_submit events"

**Business**: "Measuring form abandonment to identify friction points and improve lead capture (typical 5-15% increase in form completions)"

**Technical**: "Configured 3 Data Layer Variables for navigation tracking"

**Business**: "Understanding user journey through site to optimize content flow and increase engagement"

## Supporting Files

- `template.md` - Documentation templates Claude fills in (event-schema, implementation-summary, reporting-capabilities, audience-definitions, executive-summary)
- `examples/sample.md` - Example reporting output including console output and event-schema.md excerpt

## Execution Checklist

- [ ] Implementation details loaded
- [ ] Event schema documentation generated
- [ ] Implementation summary created
- [ ] Reporting capabilities analyzed
- [ ] GA4 report configurations specified
- [ ] Audience definitions documented
- [ ] ROI estimates calculated
- [ ] Executive summary created
- [ ] Next steps recommendations provided
- [ ] All documentation files saved

## Common Questions

**Q: Who should receive which documentation?**
A: Technical docs → Engineers/Analysts. Executive summary → Business stakeholders. Reporting guide → Marketing team.

**Q: How often should documentation be updated?**
A: Update when events are added/modified. Review quarterly to ensure accuracy.

**Q: Can I customize the templates?**
A: Yes. Templates are starting points. Adapt to your organization's needs.

**Q: What if I don't know the ROI estimates?**
A: Use industry benchmarks (10-30% conversion lift typical) or skip estimates and focus on capabilities.
