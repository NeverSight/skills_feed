---
name: google-apps-script
description: Comprehensive guide for Google Apps Script development covering all built-in services (SpreadsheetApp, DocumentApp, GmailApp, DriveApp, CalendarApp, FormApp, SlidesApp), triggers, authorization, error handling, and performance optimization. Use when automating Google Sheets operations, creating Google Docs, managing Gmail/email, working with Google Drive files, automating Calendar events, implementing triggers (time-based, event-based), building custom functions, creating add-ons, handling OAuth scopes, optimizing Apps Script performance, working with UrlFetchApp for API calls, using PropertiesService for persistent storage, or implementing CacheService for temporary data. Covers batch operations, error recovery, and JavaScript ES6+ runtime.
---

# Google Apps Script

## Overview

This skill provides comprehensive guidance for developing Google Apps Script applications that automate Google Workspace services. Google Apps Script is a cloud-based JavaScript platform that enables automation across Google Sheets, Docs, Gmail, Drive, Calendar, and more, with server-side execution and automatic OAuth integration.

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
- Handling OAuth scopes and authorization
- Making HTTP requests to external APIs with UrlFetchApp
- Using persistent storage with PropertiesService
- Implementing caching strategies with CacheService
- Optimizing performance with batch operations
- Debugging Apps Script code or authorization issues

## Core Services

### 1. SpreadsheetApp (Google Sheets Automation)

Automate all aspects of Google Sheets including reading, writing, formatting, and data manipulation.

**Common operations:**
- Read/write cell values and ranges
- Format cells (fonts, colors, borders)
- Create/delete sheets
- Insert/delete rows and columns
- Apply formulas and data validation
- Batch operations for performance

### 2. DocumentApp (Google Docs Creation)

Create and edit Google Docs programmatically including text, tables, images, and formatting.

**Common operations:**
- Create documents and add content
- Format paragraphs and text
- Insert tables and images
- Find and replace text
- Manage document structure

### 3. GmailApp & MailApp (Email Management)

Automate email operations including sending, searching, and managing Gmail messages.

**Common operations:**
- Send emails with attachments
- Search and read Gmail messages
- Manage labels and threads
- Send HTML emails
- Process inbox automatically

### 4. DriveApp (File Operations)

Manage Google Drive files and folders programmatically.

**Common operations:**
- Create, copy, move, delete files
- Search for files and folders
- Share files and manage permissions
- Convert file formats
- Organize with folders

### 5. CalendarApp (Calendar Automation)

Automate Google Calendar operations including events, reminders, and recurring appointments.

**Common operations:**
- Create and modify events
- Set up recurring events
- Add guests and reminders
- Query calendar for events
- Manage multiple calendars

### 6. Triggers & Automation

Implement time-based and event-driven automation.

**Trigger types:**
- Time-based (hourly, daily, weekly)
- On edit (spreadsheet changes)
- On form submit
- On open (document/spreadsheet open)

## Quick Start Examples

### Example 1: Automated Spreadsheet Report

```javascript
function generateWeeklyReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Data');

  // Batch read for performance
  const data = sheet.getRange('A2:D').getValues();

  // Process data
  const report = data
    .filter(row => row[0])  // Filter empty rows
    .map(row => ({
      name: row[0],
      value: row[1],
      status: row[2],
      date: row[3]
    }));

  // Write summary
  const summarySheet = ss.getSheetByName('Summary') || ss.insertSheet('Summary');
  summarySheet.clear();
  summarySheet.appendRow(['Name', 'Total Value', 'Status']);

  report.forEach(item => {
    summarySheet.appendRow([item.name, item.value, item.status]);
  });

  // Email notification
  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(),
    subject: 'Weekly Report Generated',
    body: `Report generated with ${report.length} records.`
  });
}
```

### Example 2: Gmail Auto-Responder

```javascript
function processUnreadEmails() {
  const threads = GmailApp.search('is:unread from:specific@example.com');

  threads.forEach(thread => {
    const messages = thread.getMessages();
    const latestMessage = messages[messages.length - 1];

    const subject = latestMessage.getSubject();
    const body = latestMessage.getPlainBody();

    // Process and respond
    thread.reply(`Thank you for your email regarding: ${subject}\n\nWe will respond within 24 hours.`);

    // Mark as read and label
    thread.markRead();
    const label = GmailApp.getUserLabelByName('Auto-Responded');
    thread.addLabel(label);
  });
}
```

### Example 3: Document Generation from Template

```javascript
function generateDocumentFromTemplate() {
  // Get template
  const templateId = 'YOUR_TEMPLATE_ID';
  const template = DriveApp.getFileById(templateId);

  // Make copy
  const newDoc = template.makeCopy('Generated Document - ' + new Date());

  // Open and edit
  const doc = DocumentApp.openById(newDoc.getId());
  const body = doc.getBody();

  // Replace placeholders
  body.replaceText('{{NAME}}', 'John Doe');
  body.replaceText('{{DATE}}', new Date().toDateString());
  body.replaceText('{{AMOUNT}}', '$1,234.56');

  // Save
  doc.saveAndClose();

  // Share with user
  newDoc.addEditor('recipient@example.com');

  Logger.log('Document created: ' + newDoc.getUrl());
}
```

### Example 4: Time-Based Trigger Setup

```javascript
function setupDailyTrigger() {
  // Delete existing triggers to avoid duplicates
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'dailyReport') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create new trigger for 9 AM daily
  ScriptApp.newTrigger('dailyReport')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .create();

  Logger.log('Daily trigger configured');
}

function dailyReport() {
  // This function runs daily at 9 AM
  generateWeeklyReport();
}
```

## Working with References

For comprehensive API documentation, code patterns, and detailed examples, see:

- **references/apps-script-api-reference.md** - Complete Apps Script API reference for all built-in services

The reference file contains:
- Core architecture and execution model
- Complete SpreadsheetApp reference
- Complete DocumentApp reference
- GmailApp & MailApp methods
- DriveApp operations
- CalendarApp functionality
- Trigger implementation patterns
- Advanced services & utilities
- Authorization & OAuth scopes
- Error handling strategies
- Performance optimization techniques
- Quotas and limits reference

## Best Practices

### 1. Use Batch Operations for Performance

Minimize API calls by batching reads and writes:

```javascript
// ✅ Good - Single batch read
const values = sheet.getRange('A1:Z1000').getValues();

// ❌ Bad - 1000 individual reads
for (let i = 1; i <= 1000; i++) {
  const value = sheet.getRange(`A${i}`).getValue();
}
```

### 2. Cache Frequently Accessed Data

Use CacheService for temporary data (25 min TTL):

```javascript
function getCachedData(key) {
  const cache = CacheService.getScriptCache();
  let data = cache.get(key);

  if (!data) {
    // Fetch from source
    data = expensiveOperation();
    cache.put(key, JSON.stringify(data), 600);  // 10 minutes
  }

  return JSON.parse(data);
}
```

### 3. Handle Errors Gracefully

Implement comprehensive error handling:

```javascript
function safeOperation() {
  try {
    // Operation code
    const range = sheet.getRange('A1');
    range.setValue('Value');
  } catch (error) {
    Logger.log('Error: ' + error.message);
    Logger.log('Stack: ' + error.stack);

    // Notify user
    const ui = SpreadsheetApp.getUi();
    ui.alert('Error: ' + error.message);

    // Log to sheet for audit trail
    const logSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Error Log');
    if (logSheet) {
      logSheet.appendRow([new Date(), error.message, error.stack]);
    }
  }
}
```

### 4. Respect Execution Limits

Scripts have a 6-minute timeout. For large operations:
- Process in batches
- Use triggers to split work
- Implement progress tracking

### 5. Minimize OAuth Scopes

Request only necessary permissions in `appscript.json`:

```json
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets.currentonly",
    "https://www.googleapis.com/auth/script.send_mail"
  ]
}
```

### 6. Use PropertiesService for Persistence

Store configuration and state:

```javascript
function saveConfig(key, value) {
  const props = PropertiesService.getScriptProperties();
  props.setProperty(key, value);
}

function getConfig(key) {
  const props = PropertiesService.getScriptProperties();
  return props.getProperty(key);
}
```

## Integration with Other Skills

- **google-ads-scripts** - Use for exporting Google Ads data to Sheets for reporting
- **gtm-datalayer** - Coordinate with GTM for tracking events triggered by Apps Script
- **ga4-bigquery** - Query BigQuery from Apps Script and write results to Sheets

## Common Patterns

### Pattern: Spreadsheet Data Validation

```javascript
function setupDataValidation() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getRange('A2:A100');

  // Create dropdown rule
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Option 1', 'Option 2', 'Option 3'])
    .setAllowInvalid(false)
    .build();

  range.setDataValidation(rule);
}
```

### Pattern: Retry Logic for API Calls

```javascript
function fetchWithRetry(url, maxRetries = 3) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = UrlFetchApp.fetch(url);
      return JSON.parse(response.getContentText());
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }
      Utilities.sleep(Math.pow(2, attempt) * 1000);  // Exponential backoff
    }
  }
}
```

### Pattern: Form Response Processing

```javascript
function onFormSubmit(e) {
  const response = e.values;  // Form responses
  const email = response[1];  // Assuming email is column B
  const name = response[2];   // Name in column C

  // Send confirmation email
  MailApp.sendEmail({
    to: email,
    subject: 'Form Submission Received',
    body: `Hi ${name},\n\nThank you for your submission.`
  });

  // Log to separate sheet
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const logSheet = ss.getSheetByName('Processed') || ss.insertSheet('Processed');
  logSheet.appendRow([new Date(), name, email, 'Processed']);
}
```

## Validation & Testing

Use the validation scripts in `scripts/` for pre-deployment checks:

- **scripts/validators.py** - Validate spreadsheet operations, range notations, and data structures

## Troubleshooting

**Common Issues:**

1. **Execution timeout** - Split work into smaller batches or use multiple triggers
2. **Authorization error** - Check OAuth scopes in manifest file
3. **Quota exceeded** - Reduce API call frequency, use caching
4. **Null reference error** - Always validate that objects exist before accessing properties

**Debug with Logger:**

```javascript
Logger.log('Debug info: ' + JSON.stringify(object));
// View: View > Logs (Cmd/Ctrl + Enter)
```

**Use Breakpoints:**
1. Add breakpoints in Apps Script editor
2. Run with debugger
3. Inspect variables and execution flow

---

This skill provides production-ready patterns for Google Workspace automation. Consult the comprehensive API reference for detailed method signatures and advanced use cases.
