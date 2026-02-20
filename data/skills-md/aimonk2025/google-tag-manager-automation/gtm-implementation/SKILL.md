---
name: gtm-implementation
description: Implements complete GTM tracking including dataLayer events in code and GTM configuration via API. Use when users need to "implement GTM tracking", "add dataLayer events", "create GTM variables and tags", "set up CTA tracking", "implement event tracking", or want to execute a tracking plan. Handles both code implementation (dataLayer.push) and GTM container configuration (variables/triggers/tags) automatically via API. Supports incremental updates and framework-specific patterns (React, Next.js, Vue, etc.).
---

# GTM Implementation - DataLayer + GTM API

Implement complete GTM tracking by adding dataLayer events to your code AND creating GTM variables, triggers, and tags via API.

## Core Mission

Transform analytics-ready DOM elements into fully tracked events with:
1. **Code Implementation**: Add dataLayer.push() calls to React/Next.js/Vue components
2. **GTM Configuration**: Create variables, triggers, and tags via GTM API

## Workflow

### Phase 1: Context & Prerequisites

**Step 1.1: Load Tracking Plan**
```
Check for gtm-tracking-plan.json (from gtm-strategy skill):
- If exists → Load events and parameters
- If missing → Ask user which events to implement OR suggest running gtm-strategy first

Check for gtm-config.json and gtm-token.json (from gtm-setup skill):
- If missing → Suggest running gtm-setup skill first
- If exists → Verify API connection
```

**Step 1.2: Detect Framework**
```
Check package.json:
- React version
- Next.js version and router type (App Router vs Pages Router)
- Vue version
- TypeScript vs JavaScript

This determines:
- Component file extensions (.tsx vs .jsx vs .vue)
- Import patterns
- Syntax for className vs class
- 'use client' directive for Next.js App Router
```

**Step 1.3: Scan for Target Elements**
```
Using Glob and Grep, find elements to instrument:

For CTA tracking:
- Search for: class=".*js-cta.*" or id="cta_.*"
- Search for: <button, <Link components

For form tracking:
- Search for: class=".*js-form.*" or id="form_.*"
- Search for: <form tags with onSubmit handlers

For navigation tracking:
- Search for: class=".*js-nav.*" or id="nav_.*"
- Search for: <Link, <a tags

Match found elements against events in tracking plan.
```

### Phase 2: DataLayer Implementation (Code Changes)

For each event in tracking plan, implement dataLayer.push() in actual code files.

**Step 2.1: CTA Click Implementation**

**Find target** (example):
```jsx
// File: app/page.tsx
<button
  className="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
>
  Get Started
</button>
```

**Implement tracking** using Edit tool:

**Before**:
```jsx
<button
  className="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
>
  Get Started
</button>
```

**After**:
```jsx
<button
  className="btn primary js-track js-cta js-click js-hero"
  id="cta_hero_get_started"
  onClick={() => {
    if (typeof window !== 'undefined' && window.dataLayer) {
      window.dataLayer.push({
        event: 'cta_click',
        cta_location: 'hero',
        cta_type: 'primary',
        cta_text: 'Get Started',
        cta_destination: '/signup'
      })
    }
  }}
>
  Get Started
</button>
```

**Framework-Specific Considerations**:

**Next.js App Router** (requires 'use client'):
```tsx
'use client'

import { useRouter } from 'next/navigation'

export default function HeroCTA() {
  const router = useRouter()

  return (
    <button
      className="btn primary js-track js-cta js-click js-hero"
      id="cta_hero_get_started"
      onClick={() => {
        // Track event
        if (typeof window !== 'undefined' && window.dataLayer) {
          window.dataLayer.push({
            event: 'cta_click',
            cta_location: 'hero',
            cta_type: 'primary',
            cta_text: 'Get Started',
            cta_destination: '/signup'
          })
        }
        // Navigate
        router.push('/signup')
      }}
    >
      Get Started
    </button>
  )
}
```

**Step 2.2: Form Submit Implementation**

**Find target**:
```jsx
<form
  className="contact-form js-track js-form js-submit js-hero"
  id="form_hero_contact"
  onSubmit={handleSubmit}
>
```

**Implement tracking**:

**Before**:
```jsx
<form
  className="contact-form js-track js-form js-submit js-hero"
  id="form_hero_contact"
  onSubmit={handleSubmit}
>
```

**After**:
```jsx
<form
  className="contact-form js-track js-form js-submit js-hero"
  id="form_hero_contact"
  onSubmit={(e) => {
    // Track form submission
    if (typeof window !== 'undefined' && window.dataLayer) {
      window.dataLayer.push({
        event: 'form_submit',
        form_name: 'contact',
        form_location: 'hero',
        form_type: 'contact_request'
      })
    }
    // Call original handler
    handleSubmit(e)
  }}
>
```

**Step 2.3: Navigation Click Implementation**

**Find target** (Next.js Link):
```jsx
<Link href="/pricing">Pricing</Link>
```

**Implement tracking**:

**Before**:
```jsx
<Link
  href="/pricing"
  className="nav-link js-track js-nav js-click js-header"
  id="nav_header_pricing"
>
  Pricing
</Link>
```

**After**:
```jsx
<Link
  href="/pricing"
  className="nav-link js-track js-nav js-click js-header"
  id="nav_header_pricing"
  onClick={() => {
    if (typeof window !== 'undefined' && window.dataLayer) {
      window.dataLayer.push({
        event: 'navigation_click',
        nav_location: 'header',
        nav_type: 'menu_link',
        nav_text: 'Pricing',
        nav_destination: '/pricing'
      })
    }
  }}
>
  Pricing
</Link>
```

**Step 2.4: Parameter Extraction Logic**

Extract parameters from DOM elements intelligently:

**cta_location**: From ID attribute
```javascript
// id="cta_hero_get_started" → location: "hero"
const id = element.getAttribute('id') // "cta_hero_get_started"
const location = id.split('_')[1] // "hero"
```

**cta_text**: From button innerText
```jsx
// <button>Get Started</button> → cta_text: "Get Started"
cta_text: 'Get Started'
```

**cta_destination**: From href or programmatic navigation
```javascript
// <Link href="/signup"> → cta_destination: "/signup"
// onClick={() => router.push('/pricing')} → cta_destination: "/pricing"
```

**cta_type**: From CSS classes
```javascript
// className includes "btn-primary" → type: "primary"
// className includes "btn-secondary" → type: "secondary"
```

### Phase 3: GTM Container Configuration (API Calls)

Create variables, triggers, and tags via GTM API to process the dataLayer events.

**Step 3.1: Create Data Layer Variables**

For each parameter in each event, create a GTM variable:

**Example**: cta_click event needs 4 variables

```javascript
// Variable 1: CTA Location
{
  name: "DLV - CTA Location",
  type: "v",
  parameter: [
    { type: "TEMPLATE", key: "name", value: "cta_location" },
    { type: "INTEGER", key: "dataLayerVersion", value: "2" }
  ]
}

// Variable 2: CTA Type
{
  name: "DLV - CTA Type",
  type: "v",
  parameter: [
    { type: "TEMPLATE", key: "name", value: "cta_type" },
    { type: "INTEGER", key: "dataLayerVersion", value: "2" }
  ]
}

// Variable 3: CTA Text
{
  name: "DLV - CTA Text",
  type: "v",
  parameter: [
    { type: "TEMPLATE", key: "name", value: "cta_text" },
    { type: "INTEGER", key: "dataLayerVersion", value: "2" }
  ]
}

// Variable 4: CTA Destination
{
  name: "DLV - CTA Destination",
  type: "v",
  parameter: [
    { type: "TEMPLATE", key: "name", value: "cta_destination" },
    { type: "INTEGER", key: "dataLayerVersion", value: "2" }
  ]
}
```

Use GTM API to create:
```javascript
tagmanager.accounts.containers.workspaces.variables.create({
  parent: `accounts/${accountId}/containers/${containerId}/workspaces/${workspaceId}`,
  requestBody: variableConfig
})
```

**Step 3.2: Create Custom Event Triggers**

For each event, create a trigger that fires on that custom event:

**Example**: cta_click trigger

```javascript
{
  name: "CE - CTA Click",
  type: "CUSTOM_EVENT",
  customEventFilter: [
    {
      type: "EQUALS",
      parameter: [
        { type: "TEMPLATE", key: "arg0", value: "{{_event}}" },
        { type: "TEMPLATE", key: "arg1", value: "cta_click" }
      ]
    }
  ]
}
```

Use GTM API to create:
```javascript
tagmanager.accounts.containers.workspaces.triggers.create({
  parent: `accounts/${accountId}/containers/${containerId}/workspaces/${workspaceId}`,
  requestBody: triggerConfig
})
```

**Step 3.3: Create GA4 Event Tags**

For each event, create a GA4 event tag that fires on the trigger:

**Example**: CTA Click tag

```javascript
{
  name: "GA4 - CTA Click",
  type: "gaawe", // GA4 Event tag type
  parameter: [
    {
      type: "TEMPLATE",
      key: "eventName",
      value: "cta_click"
    },
    {
      type: "LIST",
      key: "eventParameters",
      list: [
        {
          type: "MAP",
          map: [
            { type: "TEMPLATE", key: "name", value: "cta_location" },
            { type: "TEMPLATE", key: "value", value: "{{DLV - CTA Location}}" }
          ]
        },
        {
          type: "MAP",
          map: [
            { type: "TEMPLATE", key: "name", value: "cta_type" },
            { type: "TEMPLATE", key: "value", value: "{{DLV - CTA Type}}" }
          ]
        },
        {
          type: "MAP",
          map: [
            { type: "TEMPLATE", key: "name", value: "cta_text" },
            { type: "TEMPLATE", key: "value", value: "{{DLV - CTA Text}}" }
          ]
        },
        {
          type: "MAP",
          map: [
            { type: "TEMPLATE", key: "name", value: "cta_destination" },
            { type: "TEMPLATE", key: "value", value: "{{DLV - CTA Destination}}" }
          ]
        }
      ]
    },
    {
      type: "TAG_REFERENCE",
      key: "measurementId",
      value: "{{GA4 Configuration Tag}}" // Reference to GA4 config tag
    }
  ],
  firingTriggerId: ["{{CE - CTA Click trigger ID}}"]
}
```

Use GTM API to create:
```javascript
tagmanager.accounts.containers.workspaces.tags.create({
  parent: `accounts/${accountId}/containers/${containerId}/workspaces/${workspaceId}`,
  requestBody: tagConfig
})
```

**Step 3.4: Handle Incremental Updates**

Check for existing variables/triggers/tags before creating:

```javascript
// List existing variables
const existingVariables = await tagmanager.accounts.containers.workspaces.variables.list({
  parent: `accounts/${accountId}/containers/${containerId}/workspaces/${workspaceId}`
})

// Check if "DLV - CTA Location" already exists
const exists = existingVariables.data.variable?.find(v => v.name === "DLV - CTA Location")

if (exists) {
  // Update existing variable
  tagmanager.accounts.containers.workspaces.variables.update({
    path: exists.path,
    requestBody: variableConfig
  })
} else {
  // Create new variable
  tagmanager.accounts.containers.workspaces.variables.create({...})
}
```

### Phase 4: Container Version Creation

After all variables/triggers/tags are created, create a new container version:

```javascript
const version = await tagmanager.accounts.containers.workspaces.create_version({
  path: `accounts/${accountId}/containers/${containerId}/workspaces/${workspaceId}`,
  requestBody: {
    name: `GTM Automation - ${new Date().toISOString()}`,
    notes: `Automated implementation via gtm-implementation skill

Events implemented:
- cta_click (12 elements)
- form_submit (3 elements)
- navigation_click (8 elements)

Variables created: 12
Triggers created: 3
Tags created: 3`
  }
})

console.log(`✓ Container version created: ${version.data.containerVersionId}`)
console.log(`→ Preview in GTM: ${version.data.containerVersion.tagManagerUrl}`)
```

### Phase 5: Summary Report

Generate comprehensive implementation summary:

```
=== GTM Implementation Complete ===

--- Code Changes ---
Files modified: 8

app/page.tsx:
  ✓ Added CTA click tracking (3 buttons)
  ✓ Added form submit tracking (1 form)

components/Navbar.tsx:
  ✓ Added navigation click tracking (5 links)

components/Footer.tsx:
  ✓ Added navigation click tracking (3 links)
  ✓ Added form submit tracking (1 newsletter form)

... (4 more files)

--- DataLayer Events Implemented ---
✓ cta_click (12 elements tracked)
✓ form_submit (3 elements tracked)
✓ navigation_click (8 elements tracked)

Total events: 23

--- GTM Container Configuration ---
Account: 1234567890
Container: GTM-ABC1234
Workspace: Default Workspace

Created via API:
  ✓ 12 Data Layer Variables
  ✓ 3 Custom Event Triggers
  ✓ 3 GA4 Event Tags

Container version created: 42
Preview URL: https://tagmanager.google.com/#/versions/accounts/123/containers/456/versions/42

--- Next Steps ---
1. Test tracking in GTM Preview mode
   → Invoke gtm-testing skill for guided testing

2. Review container version in GTM:
   → Open GTM → Versions → Version 42
   → Check variables, triggers, tags

3. Publish when ready:
   → GTM → Submit → Publish

Ready to test tracking? Invoke gtm-testing skill.
```

## Important Guidelines

### Code Implementation Best Practices

**1. Preserve Existing Functionality**
- NEVER remove existing onClick handlers
- Call original handlers AFTER tracking
- Use wrapper functions when needed

**2. Type Safety (TypeScript)**
```tsx
// Add proper typing
onClick={(e: React.MouseEvent<HTMLButtonElement>) => {
  // Track
  window.dataLayer?.push({...})
  // Original handler
  originalHandler(e)
}}
```

**3. Framework-Specific Patterns**

**Next.js App Router**:
- Add 'use client' directive to files with onClick
- Use useRouter from 'next/navigation'

**React**:
- Use functional components with hooks
- Maintain existing state management

**Vue**:
- Use @click syntax
- Maintain reactivity

**4. Avoid Redundant Tracking**
- If element already has dataLayer.push, UPDATE it (don't duplicate)
- Check for existing tracking code before adding new

### GTM API Best Practices

**1. Naming Conventions**
- Variables: "DLV - {Parameter Name}" (DLV = Data Layer Variable)
- Triggers: "CE - {Event Name}" (CE = Custom Event)
- Tags: "GA4 - {Event Name}"

**2. Error Handling**
```javascript
try {
  await tagmanager.accounts.containers.workspaces.variables.create({...})
} catch (error) {
  if (error.code === 409) {
    // Variable already exists - update instead
  } else if (error.code === 403) {
    // Permission denied
  } else {
    throw error
  }
}
```

**3. Batch Operations**
- Create all variables first
- Then create triggers (which may reference variables)
- Finally create tags (which reference both)

### Parameter Extraction Intelligence

Be smart about extracting parameters:

**From ID attributes**:
```javascript
// id="cta_hero_get_started"
const [category, location, ...action] = id.split('_')
// category: "cta", location: "hero", action: ["get", "started"]
```

**From class names**:
```javascript
// className="btn btn-primary"
const isPrimary = className.includes('primary')
const type = isPrimary ? 'primary' : 'secondary'
```

**From content**:
```jsx
// <button>Get Started</button>
const text = element.innerText // "Get Started"
```

**From href/destination**:
```jsx
// <Link href="/pricing">
const destination = href // "/pricing"

// onClick={() => router.push('/signup')}
// Parse from handler → destination: "/signup"
```

## Scripts

### scripts/gtm-api-client.js
Core GTM API wrapper for creating variables/triggers/tags (extracted from gtm-setup-auto.js logic)

### scripts/create-variables.js
Variable creation logic with duplicate detection

### scripts/create-triggers.js
Trigger creation logic for custom events

### scripts/create-tags.js
GA4 event tag creation with parameter mapping

### scripts/implement-datalayer.js
Analyzes tracking plan and implements dataLayer.push() in code using Edit tool

## References

### references/datalayer-patterns.md
Framework-specific dataLayer implementation patterns:
- Next.js App Router ('use client' directive)
- Next.js Pages Router
- React (hooks, class components)
- Vue (composition API, options API)
- Vanilla JavaScript

### references/gtm-ui-guide.md
Manual GTM UI instructions as fallback if API fails

### references/event-taxonomies.md
Common event naming patterns (object_action vs action_object)

## Assets

### assets/templates/saas.json
Pre-built GTM config for SaaS product tracking:
- trial_start, feature_usage, upgrade_click
- account_created, plan_selected

### assets/templates/ecommerce.json
Pre-built GTM config for e-commerce tracking:
- product_view, add_to_cart, checkout_start
- purchase_complete, product_search

## Supporting Files

- `template.md` - Framework-specific dataLayer push code patterns and GTM API payload templates
- `examples/sample.md` - Example implementation output showing before/after code changes and console output

### assets/templates/lead-generation.json
Pre-built GTM config for lead-gen tracking:
- form_start, form_submit, content_download
- demo_request, newsletter_signup

## Execution Checklist

- [ ] Tracking plan loaded or events specified
- [ ] GTM API credentials validated
- [ ] Framework detected
- [ ] Target elements identified
- [ ] DataLayer events implemented in code
- [ ] Variables created via GTM API
- [ ] Triggers created via GTM API
- [ ] Tags created via GTM API
- [ ] Container version created
- [ ] Implementation summary generated
- [ ] Testing instructions provided

## Common Questions

**Q: What if I don't have a tracking plan?**
A: Run gtm-strategy skill first to create one, OR specify events manually and we'll implement them.

**Q: Can I implement tracking without using the GTM API?**
A: Yes. We'll implement dataLayer events in code and provide manual GTM UI instructions.

**Q: Will this overwrite existing GTM configuration?**
A: No. We check for existing variables/triggers/tags and update them. New configs are added, not replaced.

**Q: Can I implement tracking for only specific events?**
A: Yes. Specify which events to implement (e.g., "only implement cta_click tracking").

**Q: What if my framework isn't supported?**
A: The dataLayer.push pattern works in any JavaScript environment. We'll provide vanilla JS implementation.
