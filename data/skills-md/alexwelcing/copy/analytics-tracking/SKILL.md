---
name: analytics-tracking
description: Implement comprehensive analytics tracking for marketing insights
tags: [analytics, tracking, measurement]
---

# Analytics Tracking Skill

You are an expert in marketing analytics and tracking implementation. Your goal is to help create measurement frameworks that provide actionable insights for optimization.

## Analytics Fundamentals

### Measurement Hierarchy
1. **Business objectives**: Revenue, growth, retention
2. **KPIs**: Metrics that indicate progress
3. **Supporting metrics**: Diagnostic details
4. **Dimensions**: How to slice data

### Common Tools

**Web Analytics**: GA4, Mixpanel, Amplitude, Heap
**Tag Management**: GTM, Segment, Tealium
**Attribution**: UTM tracking, multi-touch
**Heatmaps**: Hotjar, FullStory, Microsoft Clarity
**A/B Testing**: Optimizely, VWO, LaunchDarkly

## Tracking Architecture

### Event-Based Model

Modern analytics uses events:
```
Event: signup_completed
Properties:
  - method: google_sso
  - plan_selected: pro
  - referral_source: twitter
  - device_type: mobile
```

### Event Naming Convention

**Format**: `object_action` or `action_object`

**Examples**:
- `page_viewed`
- `button_clicked`
- `form_submitted`
- `signup_completed`
- `purchase_made`

**Rules**:
- Lowercase with underscores
- Past tense for completed actions
- Consistent across product
- Documented in tracking plan

## Tracking Plan Template

### Document Structure

```markdown
# Tracking Plan: [Product Name]
Last Updated: [Date]

## Event Inventory

### Page Views
| Event | Properties | Trigger |
|-------|------------|---------|
| page_viewed | page_name, page_url, referrer | On page load |

### User Actions
| Event | Properties | Trigger |
|-------|------------|---------|
| button_clicked | button_name, button_location | On click |
| form_submitted | form_name, form_fields | On submit |

### Conversions
| Event | Properties | Trigger |
|-------|------------|---------|
| signup_completed | method, plan | After signup |
| purchase_completed | amount, product | After payment |

## User Properties
| Property | Description | When Set |
|----------|-------------|----------|
| user_id | Unique identifier | On signup |
| plan_type | Current plan | On signup/upgrade |
| signup_date | First signup | On signup |

## UTM Parameters
| Parameter | Usage |
|-----------|-------|
| utm_source | Traffic source (google, twitter) |
| utm_medium | Marketing medium (cpc, email) |
| utm_campaign | Campaign name |
| utm_content | Creative variant |
| utm_term | Search keywords |
```

## Essential Events

### Acquisition Events
- `page_viewed` - Page loads
- `cta_clicked` - Marketing CTA clicks
- `utm_captured` - Attribution data

### Activation Events
- `signup_started` - Began registration
- `signup_completed` - Finished registration
- `onboarding_step_completed` - Each step
- `activation_event` - Your key activation

### Engagement Events
- `feature_used` - Key feature usage
- `session_started` - Return visits
- `content_consumed` - Content engagement

### Revenue Events
- `trial_started` - Free trial begins
- `upgrade_initiated` - Started upgrade
- `purchase_completed` - Transaction done
- `subscription_renewed` - Renewal

### Retention Events
- `return_visit` - Came back
- `churn_risk_signal` - Inactivity
- `feedback_submitted` - User feedback

## UTM Tracking

### Structure
```
https://site.com/page?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale&utm_content=banner_a
```

### Best Practices
- Consistent naming convention
- Lowercase only
- No spaces (use underscores)
- Document all campaigns
- Use URL builder tools

### Attribution Windows
- **First touch**: Credit to first interaction
- **Last touch**: Credit to final interaction
- **Linear**: Equal credit to all
- **Time decay**: More credit to recent

## GA4 Implementation

### Core Setup
1. Create GA4 property
2. Install gtag.js or GTM
3. Configure data streams
4. Enable enhanced measurement
5. Set up conversions

### Custom Events

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'pro'
});
```

### Enhanced Ecommerce

```javascript
gtag('event', 'purchase', {
  'transaction_id': 'T12345',
  'value': 99.00,
  'currency': 'USD',
  'items': [{ ... }]
});
```

## Google Tag Manager Setup

### Container Structure
- **Tags**: What fires (GA4, Meta Pixel, etc.)
- **Triggers**: When it fires (page view, click, etc.)
- **Variables**: Data to include

### Common Tags
- GA4 Configuration
- GA4 Event
- Meta/Facebook Pixel
- LinkedIn Insight
- Google Ads Conversion

### Trigger Types
- Page View (DOM Ready, Window Loaded)
- Click (All Clicks, Link Clicks)
- Form Submission
- Custom Events (dataLayer)
- Timer
- Scroll Depth

### DataLayer Implementation

```javascript
// Push events to dataLayer
dataLayer.push({
  'event': 'signup_completed',
  'method': 'google_sso',
  'plan': 'pro'
});
```

## Conversion Tracking

### Define Conversions
Primary: Revenue-generating actions
Secondary: Engagement milestones

### Track Funnel Steps
```
Page View → Signup Click → Form Start → Form Complete → Activation
   100%        45%           30%           22%            15%
```

### Revenue Attribution
- Track transaction value
- Attribute to marketing source
- Calculate CAC and ROAS
- Monitor LTV by channel

## Dashboard Design

### Marketing Dashboard

**Acquisition**:
- Traffic by source/medium
- Campaign performance
- Landing page conversion

**Activation**:
- Signup conversion rate
- Activation rate
- Time to activation

**Revenue**:
- MRR/ARR
- Conversion to paid
- ARPU by segment

**Retention**:
- Churn rate
- Return visitor rate
- Engagement metrics

## QA Checklist

### Pre-Launch
- [ ] Tracking plan documented
- [ ] Events match plan
- [ ] Properties capture correctly
- [ ] Test environment verified
- [ ] PII compliance checked

### Post-Launch
- [ ] Events firing correctly
- [ ] Data appearing in tool
- [ ] Conversions tracking
- [ ] Segments working
- [ ] Reports accurate

### Ongoing
- [ ] Regular data audits
- [ ] Documentation updated
- [ ] New features tracked
- [ ] Team trained

## Output Format

When setting up tracking, provide:

1. **Tracking plan** spreadsheet/document
2. **Implementation spec** for developers
3. **GTM container** setup instructions
4. **QA checklist** with test cases
5. **Dashboard template** with key metrics
6. **Documentation** for team reference

## Related Skills

- `ab-test-setup` - For experiment tracking
- `page-cro` - For conversion optimization
- `seo-audit` - For organic tracking
