---
name: google-ads-scripts
description: Expert guidance for Google Ads Script development including AdsApp API, campaign management, ad groups, keywords, bidding strategies, performance reporting, budget management, automated rules, and optimization patterns. Use when automating Google Ads campaigns, managing keywords and bids, creating performance reports, implementing automated rules, optimizing ad spend, working with campaign budgets, monitoring quality scores, tracking conversions, pausing low-performing keywords, adjusting bids based on ROAS, or building Google Ads automation scripts. Covers campaign operations, keyword targeting, bid optimization, conversion tracking, error handling, and JavaScript-based automation in Google Ads editor.
---

# Google Ads Scripts

## Overview

This skill provides comprehensive guidance for developing Google Ads Scripts using the AdsApp API. Google Ads Scripts enable automation of campaign management, bid optimization, performance reporting, and bulk operations through JavaScript code that runs directly in the Google Ads editor.

## When to Use This Skill

Invoke this skill when:

- Automating Google Ads campaign management operations
- Managing keywords and adjusting bids programmatically
- Creating performance reports and dashboards
- Implementing automated rules for campaign optimization
- Optimizing ad spend based on ROAS or CPA targets
- Working with campaign budgets and spend limits
- Monitoring quality scores and pausing low-performers
- Tracking conversions and adjusting strategies
- Building bulk operations for large-scale account management
- Implementing time-based or performance-based automation
- Debugging Google Ads Script code or API issues

## Core Capabilities

### 1. Campaign Operations

Manage campaigns programmatically including creation, modification, status changes, and bulk updates. The AdsApp.campaigns() selector provides filtering and iteration patterns.

**Common operations:**
- Get campaigns with conditions (status, budget, name patterns)
- Modify campaign properties (name, budget, dates, status)
- Apply labels for organization
- Pause/enable campaigns based on performance criteria

### 2. Keyword & Bid Management

Automate keyword targeting and bid adjustments based on performance metrics.

**Common operations:**
- Get keywords with quality score filtering
- Adjust max CPC bids based on ROAS/CPA targets
- Add/remove negative keywords
- Monitor keyword-level conversions
- Implement bid optimization algorithms

### 3. Performance Reporting

Generate custom reports using campaign, ad group, keyword, and ad statistics.

**Common operations:**
- Retrieve metrics for custom date ranges
- Calculate derived metrics (CTR, CPC, conversion rate)
- Export data to Google Sheets
- Create automated dashboards
- Monitor KPIs and trigger alerts

### 4. Budget Management

Control spending and allocate budgets across campaigns.

**Common operations:**
- Get/set daily campaign budgets
- Monitor spend against thresholds
- Pause campaigns when budget limits reached
- Distribute budgets based on performance

### 5. Automated Rules & Optimization

Build intelligence into campaign management with automated decision-making.

**Common operations:**
- Pause low-performing keywords (low QS, high CPC, no conversions)
- Increase bids for high-performers
- Adjust budgets based on day-of-week patterns
- Implement custom bidding strategies

### 6. Error Handling & Resilience

Implement robust error handling to manage API limits, quota issues, and runtime errors.

**Key patterns:**
- Try-catch blocks for error handling
- Null checks for optional properties
- Logging to sheets for audit trails
- Rate limiting awareness (30-minute execution limit)

## Quick Start Examples

### Example 1: Pause Low-Quality Keywords

```javascript
function pauseLowQualityKeywords() {
  const keywords = AdsApp.keywords()
    .withCondition('keyword.status = ENABLED')
    .withCondition('keyword.quality_info.quality_score < 4')
    .withCondition('keyword.metrics.cost > 100000000')  // >100 spend
    .get();

  let count = 0;
  while (keywords.hasNext()) {
    const keyword = keywords.next();
    keyword.pause();
    count++;
  }

  Logger.log(`Paused ${count} low-quality keywords`);
}
```

### Example 2: Optimize Bids Based on ROAS

```javascript
function optimizeBidsByROAS() {
  const TARGET_ROAS = 3.0;  // 300%

  const keywords = AdsApp.keywords()
    .withCondition('keyword.status = ENABLED')
    .withCondition('keyword.metrics.conversions > 5')  // Min conversions
    .get();

  while (keywords.hasNext()) {
    const keyword = keywords.next();
    const stats = keyword.getStatsFor('LAST_30_DAYS');
    const roas = stats.getReturnOnAdSpend();
    const currentBid = keyword.getMaxCpc();

    if (roas > TARGET_ROAS) {
      // Increase bid by 10%
      keyword.setMaxCpc(Math.floor(currentBid * 1.1));
    } else if (roas < TARGET_ROAS * 0.7) {
      // Decrease bid by 5%
      keyword.setMaxCpc(Math.floor(currentBid * 0.95));
    }
  }
}
```

### Example 3: Export Campaign Performance to Sheets

```javascript
function exportCampaignPerformance() {
  const campaigns = AdsApp.campaigns()
    .withCondition('campaign.status = ENABLED')
    .orderBy('campaign.metrics.cost DESC')
    .get();

  const report = [['Campaign', 'Clicks', 'Cost', 'Conversions', 'CPC', 'ROAS']];

  while (campaigns.hasNext()) {
    const campaign = campaigns.next();
    const stats = campaign.getStatsFor('LAST_30_DAYS');

    report.push([
      campaign.getName(),
      stats.getClicks(),
      stats.getCost() / 1000000,  // Convert from micros
      stats.getConversions(),
      stats.getAverageCpc() / 1000000,
      stats.getReturnOnAdSpend()
    ]);
  }

  // Write to Google Sheets
  const ss = SpreadsheetApp.openById('YOUR_SHEET_ID');
  const sheet = ss.getSheetByName('Campaign Report') || ss.insertSheet('Campaign Report');
  sheet.clear();
  sheet.getRange(1, 1, report.length, report[0].length).setValues(report);
}
```

## Working with References

For comprehensive API documentation, code patterns, and detailed examples, see:

- **references/ads-api-reference.md** - Complete AdsApp API reference including all selectors, methods, conditions, statistics, and enterprise patterns

The reference file contains:
- Complete API hierarchy and object model
- All selector patterns and conditions
- Statistics methods and date ranges
- Campaign, ad group, keyword, and ad operations
- Bidding strategy implementation details
- Performance reporting patterns
- Budget management techniques
- Advanced targeting options
- Error handling patterns
- Performance optimization strategies
- Quotas and limits reference

## Best Practices

### 1. Use Batch Operations

Avoid individual API calls in loops. Instead, collect entities and perform batch operations:

```javascript
// ✅ Good - Batch collection
const keywords = AdsApp.keywords()
  .withCondition('keyword.quality_info.quality_score < 5')
  .get();

const toUpdate = [];
while (keywords.hasNext()) {
  toUpdate.push(keywords.next());
}

toUpdate.forEach(keyword => keyword.setMaxCpc(50000));
```

### 2. Filter with Conditions

Use `.withCondition()` to filter at the API level rather than in JavaScript:

```javascript
// ✅ Good - API-level filtering
const campaigns = AdsApp.campaigns()
  .withCondition('campaign.status = ENABLED')
  .withCondition('campaign.budget_information.budget_amount > 100000000')
  .get();
```

### 3. Handle Errors Gracefully

Always wrap operations in try-catch blocks and log errors:

```javascript
function safeOperation() {
  try {
    // Operation code
  } catch (error) {
    Logger.log('Error: ' + error.message);
    Logger.log('Stack: ' + error.stack);

    // Optionally email alert
    MailApp.sendEmail(
      Session.getEffectiveUser().getEmail(),
      'Ads Script Error',
      error.message
    );
  }
}
```

### 4. Respect Execution Limits

Scripts have a 30-minute execution timeout. For large accounts:
- Limit result sets with `.withLimit()`
- Process in batches
- Use early termination when needed

### 5. Convert Micros Correctly

Google Ads API uses micros (1/1,000,000) for currency values:

```javascript
const costMicros = stats.getCost();
const costCurrency = costMicros / 1000000;  // Convert to dollars/local currency

const bidCurrency = 5.00;  // $5.00
const bidMicros = bidCurrency * 1000000;  // 5000000 micros
```

### 6. Log Operations for Auditing

Maintain audit trails by logging changes to Google Sheets:

```javascript
function logChange(operation, entity, details) {
  const ss = SpreadsheetApp.openById('LOG_SHEET_ID');
  const sheet = ss.getSheetByName('Audit Log');
  sheet.appendRow([
    new Date(),
    operation,
    entity,
    JSON.stringify(details)
  ]);
}
```

## Integration with Other Skills

- **google-apps-script** - Use for Google Sheets reporting, Gmail notifications, Drive file management, and trigger setup
- **ga4-measurement-protocol** - Combine with GA4 for tracking script-triggered events
- **gtm-api** - Coordinate with GTM configurations for holistic tracking

## Common Patterns

### Pattern: Conditional Bid Adjustment

```javascript
function adjustBidsBasedOnDayOfWeek() {
  const today = new Date().getDay();  // 0 = Sunday, 6 = Saturday
  const isWeekend = today === 0 || today === 6;

  const campaigns = AdsApp.campaigns()
    .withCondition('campaign.status = ENABLED')
    .get();

  while (campaigns.hasNext()) {
    const campaign = campaigns.next();
    const budget = campaign.getBudget().getAmount();

    if (isWeekend) {
      campaign.getBudget().setAmount(budget * 1.2);  // +20% on weekends
    }
  }
}
```

### Pattern: Quality Score Monitoring

```javascript
function monitorQualityScores() {
  const threshold = 5;

  const lowQualityKeywords = AdsApp.keywords()
    .withCondition(`keyword.quality_info.quality_score < ${threshold}`)
    .withCondition('keyword.status = ENABLED')
    .orderBy('keyword.metrics.cost DESC')  // Most expensive first
    .withLimit(100)
    .get();

  const alerts = [];
  while (lowQualityKeywords.hasNext()) {
    const keyword = lowQualityKeywords.next();
    alerts.push({
      keyword: keyword.getText(),
      qualityScore: keyword.getQualityScore(),
      cost: keyword.getStatsFor('LAST_7_DAYS').getCost() / 1000000
    });
  }

  if (alerts.length > 0) {
    // Send email or log to sheet
    Logger.log(`${alerts.length} keywords with QS < ${threshold}`);
  }
}
```

## Validation & Testing

Use the validation scripts in `scripts/` for pre-deployment checks:

- **scripts/validators.py** - Validate campaign data, bid values, budget amounts before applying changes

## Troubleshooting

**Common Issues:**

1. **Execution timeout** - Reduce scope with `.withLimit()` or process in batches
2. **Quota exceeded** - Reduce API call frequency, use cached data
3. **Type errors** - Remember micros conversion for currency values
4. **Null values** - Always check for null before accessing properties

**Debug with Logger:**

```javascript
Logger.log('Debug info: ' + JSON.stringify(data));
// View logs: View > Logs in script editor
```

---

This skill provides production-ready patterns for Google Ads automation. Consult the comprehensive API reference for detailed method signatures and advanced use cases.
