---
name: google-tagmanager
description: Comprehensive Google Tag Manager guide covering container setup, tags, triggers, variables, data layer, debugging, custom templates, and API automation. Use when working with GTM implementation, configuration, optimisation, troubleshooting, or any GTM-related tasks.
---

# Google Tag Manager

## Overview

This skill provides comprehensive expertise for Google Tag Manager (GTM), covering container setup, tag configuration, triggers, variables, data layer implementation, debugging, custom templates, and API automation. Whether you are implementing a new GTM setup, optimising an existing configuration, or troubleshooting issues, this skill has you covered.

## When to Use This Skill

Invoke this skill when:

- Setting up a new GTM container
- Configuring tags (GA4, Google Ads, Facebook Pixel, etc.)
- Creating triggers (page views, clicks, form submissions, etc.)
- Defining variables (data layer, custom JavaScript, constants, etc.)
- Implementing the data layer for e-commerce or custom events
- Debugging GTM issues using Preview mode or Tag Assistant
- Building custom templates with sandboxed JavaScript
- Automating GTM operations via the REST API
- Optimising container performance and organisation
- Ensuring privacy compliance and consent management

## Quick Start

### Container Setup

1. Create a GTM account at [tagmanager.google.com](https://tagmanager.google.com)
2. Create a container (Web, iOS, Android, or Server)
3. Install the container snippet on your website
4. Configure tags, triggers, and variables
5. Test in Preview mode
6. Publish

See [setup.md](references/setup.md) for detailed installation instructions.

### Basic Tag Configuration

```javascript
// Example: GA4 Configuration Tag
Tag Type: Google Analytics: GA4 Configuration
Measurement ID: G-XXXXXXXXXX
Trigger: All Pages
```

See [tags.md](references/tags.md) for comprehensive tag documentation.

### Data Layer Push

```javascript
// Push custom event to data layer
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  'event': 'custom_event',
  'category': 'engagement',
  'action': 'button_click',
  'label': 'CTA Button'
});
```

See [datalayer.md](references/datalayer.md) for data layer patterns.

## Core Concepts

### Tags, Triggers, and Variables

**Tags** are snippets of code that execute on your site (e.g., GA4, Google Ads, Facebook Pixel).

**Triggers** define when tags fire (e.g., page views, clicks, form submissions).

**Variables** capture dynamic values for use in tags and triggers (e.g., page URL, click text, data layer values).

### How They Work Together

```
User Action --> Trigger Fires --> Tag Executes --> Data Sent
     ^                                    |
     |                                    v
     +--- Variables provide values -------+
```

## Topic Reference Guide

### Container Setup and Installation

For container creation, snippet installation, and initial configuration:

- **Reference**: [setup.md](references/setup.md)
- **Topics**: Container types, snippet placement, noscript fallback, verification

### Tag Configuration

For configuring analytics, advertising, and custom tags:

- **Reference**: [tags.md](references/tags.md)
- **Topics**: GA4 tags, Google Ads conversions, Facebook Pixel, custom HTML, tag sequencing

### Trigger Types

For setting up firing conditions:

- **Reference**: [triggers.md](references/triggers.md)
- **Topics**: Page views, clicks, form submissions, custom events, trigger groups, blocking triggers

### Variable Configuration

For capturing and formatting data:

- **Reference**: [variables.md](references/variables.md)
- **Topics**: Built-in variables, data layer variables, custom JavaScript, URL variables, lookup tables

### Data Layer Implementation

For implementing the data layer:

- **Reference**: [datalayer.md](references/datalayer.md)
- **Topics**: Data layer structure, e-commerce tracking, SPA tracking, best practices

### Debugging and Testing

For troubleshooting GTM implementations:

- **Reference**: [debugging.md](references/debugging.md)
- **Topics**: Preview mode, Tag Assistant, debug console, common issues, testing workflows

### Best Practices

For naming conventions, performance, and security:

- **Reference**: [best-practices.md](references/best-practices.md)
- **Topics**: Naming conventions, container organisation, performance optimisation, security, deployment strategies

### Custom Templates

For building custom tag and variable templates:

- **Reference**: [custom-templates.md](references/custom-templates.md)
- **Topics**: Sandboxed JavaScript, template APIs, permissions, testing, publishing to Gallery

### API Automation

For programmatic GTM management:

- **Reference**: [api.md](references/api.md)
- **Topics**: Authentication, REST API operations, bulk operations, backup/restore, CI/CD integration

## Common Workflows

### Implement GA4 Page View Tracking

1. Create GA4 Configuration tag with Measurement ID
2. Set trigger to "All Pages"
3. Test in Preview mode
4. Verify in GA4 DebugView
5. Publish

### Track Form Submissions

1. Create Form Submission trigger
2. Create GA4 Event tag with event name `form_submit`
3. Add form ID/name as event parameter
4. Test submission in Preview mode
5. Publish

### Implement E-commerce Tracking

1. Implement data layer with e-commerce events
2. Create data layer variables for product data
3. Create GA4 Event tags for each e-commerce event
4. Map data layer variables to event parameters
5. Test complete purchase flow
6. Publish

### Debug Tag Not Firing

1. Enable Preview mode
2. Perform the action that should fire the tag
3. Check "Tags Not Fired" section
4. Review trigger conditions in Variables tab
5. Check data layer for required values
6. Fix conditions and retest

See [debugging.md](references/debugging.md) for detailed debugging workflows.

## Technical Constraints

### JavaScript (ES5 Requirement)

GTM Custom JavaScript Variables and Custom HTML Tags require ES5 syntax:

```javascript
// Use var instead of const/let
var myVar = 'value';

// Use function instead of arrow functions
var myFunc = function(x) { return x * 2; };

// Use string concatenation instead of template literals
var message = 'Hello, ' + name;
```

**Exception**: Custom Templates support some ES6 features in their sandboxed environment.

### Regular Expressions (RE2 Format)

GTM uses RE2 regex syntax, which differs from standard JavaScript regex:

**Supported**: Character classes, quantifiers, anchors, groups, alternation
**Not Supported**: Lookahead, lookbehind, backreferences, possessive quantifiers

```regex
# Match product pages
^/products/[^/]+$

# Case-insensitive matching
(?i)^/checkout
```

## Naming Conventions

### Tags

Format: `[Platform] - [Type] - [Description]`

Examples:
- `GA4 - Event - Form Submit`
- `Google Ads - Conversion - Purchase`
- `FB - Pixel - Page View`

### Triggers

Format: `[Event Type] - [Description]`

Examples:
- `Click - CTA Button`
- `Page View - Homepage`
- `Form Submit - Contact Form`

### Variables

Format: `[Type] - [Description]`

Examples:
- `DL - User ID` (Data Layer)
- `CJS - Format Price` (Custom JavaScript)
- `Constant - GA4 Measurement ID`

## Performance Tips

1. **Use native tag templates** instead of Custom HTML when possible
2. **Minimise Custom JavaScript** execution time
3. **Remove unused tags, triggers, and variables** regularly
4. **Use tag sequencing wisely** to avoid unnecessary delays
5. **Defer non-critical tags** to improve page load

## Security Best Practices

1. **Vet all Custom HTML tags** for malicious code
2. **Never push PII to the data layer** - hash sensitive identifiers
3. **Implement consent mode** for privacy compliance
4. **Limit container admin access** to trusted users
5. **Review third-party templates** before using

## Quick Reference

### Built-in Variables to Enable

- Page URL, Page Path, Page Hostname
- Click Element, Click Classes, Click ID, Click URL, Click Text
- Form Element, Form ID, Form Classes
- Scroll Depth Threshold, Scroll Direction

### Common Trigger Types

- Page View (All Pages, Some Pages)
- Click (All Elements, Just Links)
- Form Submission
- Custom Event
- History Change (for SPAs)
- Timer
- Scroll Depth

### Essential Data Layer Events

```javascript
// Page view
window.dataLayer.push({ 'event': 'page_view' });

// User login
window.dataLayer.push({ 'event': 'login', 'method': 'Google' });

// Purchase
window.dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'AUD',
    'items': [...]
  }
});
```

## Reference Files

| Topic | Reference File |
|-------|----------------|
| Container setup | [setup.md](references/setup.md) |
| Tag configuration | [tags.md](references/tags.md) |
| Trigger configuration | [triggers.md](references/triggers.md) |
| Variable configuration | [variables.md](references/variables.md) |
| Data layer | [datalayer.md](references/datalayer.md) |
| Debugging | [debugging.md](references/debugging.md) |
| Best practices | [best-practices.md](references/best-practices.md) |
| Custom templates | [custom-templates.md](references/custom-templates.md) |
| API automation | [api.md](references/api.md) |

## External Resources

- [GTM Help Center](https://support.google.com/tagmanager)
- [GTM Developer Documentation](https://developers.google.com/tag-platform/tag-manager)
- [GA4 Implementation Guide](https://developers.google.com/analytics/devguides/collection/ga4)
- [GTM API Reference](https://developers.google.com/tag-platform/tag-manager/api/v2)
