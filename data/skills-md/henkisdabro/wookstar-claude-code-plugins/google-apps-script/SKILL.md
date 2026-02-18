---
name: google-apps-script
description: Comprehensive guide for Google Apps Script development covering all built-in services (SpreadsheetApp, DocumentApp, GmailApp, DriveApp, CalendarApp, FormApp, SlidesApp), triggers, authorization, error handling, and performance optimization. Use when automating Google Sheets operations, creating Google Docs, managing Gmail/email, working with Google Drive files, automating Calendar events, implementing triggers (time-based, event-based), building custom functions, creating add-ons, handling OAuth scopes, optimizing Apps Script performance, working with UrlFetchApp for API calls, using PropertiesService for persistent storage, or implementing CacheService for temporary data. Covers batch operations, error recovery, and JavaScript ES6+ runtime.
---

# Google Apps Script

## Overview

Cloud-based JavaScript platform for automating Google Workspace services. Server-side V8 runtime with automatic OAuth integration across Sheets, Docs, Gmail, Drive, Calendar, and more.

## When to Use This Skill

Invoke this skill when:

- Automating Google Sheets operations (reading, writing, formatting)
- Creating or editing Google Docs programmatically
- Managing Gmail messages and sending emails
- Working with Google Drive files and folders
- Automating Google Calendar events
- Implementing triggers (time-based or event-based)
- Building custom functions for Sheets
- Creating Google Workspace add-ons
- Handling OAuth scopes and authorisation
- Making HTTP requests to external APIs with UrlFetchApp
- Using persistent storage with PropertiesService
- Implementing caching strategies with CacheService
- Optimising performance with batch operations
- Debugging Apps Script code or authorisation issues

## Core Services

1. **SpreadsheetApp** - Google Sheets automation (read, write, format, data validation)
2. **DocumentApp** - Google Docs creation and editing
3. **GmailApp & MailApp** - Email operations (send, search, manage labels)
4. **DriveApp** - File and folder management, sharing, permissions
5. **CalendarApp** - Calendar events, recurring appointments, reminders
6. **Triggers & ScriptApp** - Time-based and event-driven automation

## Quick Start

```javascript
function generateWeeklyReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Data');
  const data = sheet.getRange('A2:D').getValues();

  const report = data.filter(row => row[0]);
  const summarySheet = ss.getSheetByName('Summary') || ss.insertSheet('Summary');
  summarySheet.clear();
  summarySheet.appendRow(['Name', 'Value', 'Status']);
  report.forEach(row => summarySheet.appendRow([row[0], row[1], row[2]]));

  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(),
    subject: 'Weekly Report Generated',
    body: `Report generated with ${report.length} records.`
  });
}
```

## Best Practices

- **Batch operations** - read/write ranges in bulk, never cell-by-cell in loops
- **Cache data** - use CacheService (25 min TTL) for frequently accessed data
- **Error handling** - wrap operations in try/catch, log errors to a sheet for audit trails
- **Respect limits** - 6-minute execution timeout; split large jobs across triggers
- **Minimise scopes** - request only necessary OAuth permissions in `appscript.json`
- **Persistent storage** - use PropertiesService for configuration and state
- **Validate inputs** - always check objects exist before accessing properties

See [references/best-practices.md](references/best-practices.md) for detailed examples of each practice.

## Validation & Testing

Use the validation scripts in `scripts/` for pre-deployment checks:

- **scripts/validators.py** - Validate spreadsheet operations, range notations, and data structures

Debug with `Logger.log()` and view output via View > Logs (Cmd/Ctrl + Enter). Use breakpoints in the Apps Script editor for step-through debugging.

## Integration with Other Skills

- **google-ads-scripts** - Export Google Ads data to Sheets for reporting
- **gtm-datalayer** - Coordinate with GTM for tracking events triggered by Apps Script
- **ga4-bigquery** - Query BigQuery from Apps Script and write results to Sheets

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Execution timeout | Split work into smaller batches or use multiple triggers |
| Authorisation error | Check OAuth scopes in manifest file |
| Quota exceeded | Reduce API call frequency, use caching |
| Null reference error | Validate objects exist before accessing properties |

## References

Detailed content is available in reference files (loaded on demand):

- [references/apps-script-api-reference.md](references/apps-script-api-reference.md) - Complete API reference for all built-in services, triggers, authorisation, and performance optimisation
- [references/examples.md](references/examples.md) - Production-ready code examples (spreadsheet reports, Gmail auto-responder, document generation, trigger setup)
- [references/best-practices.md](references/best-practices.md) - Detailed best practices with code blocks for batch operations, caching, error handling, scopes, and persistence
- [references/patterns.md](references/patterns.md) - Common reusable patterns (data validation, retry logic, form response processing)
