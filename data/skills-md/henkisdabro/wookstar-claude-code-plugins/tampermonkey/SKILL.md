---
name: tampermonkey
description: |
  Write Tampermonkey userscripts for browser automation, page modification, and web enhancement.
  Use when: creating browser scripts, writing greasemonkey scripts, automating user interactions,
  injecting CSS or JavaScript into web pages, modifying website behaviour, building browser extensions,
  hiding unwanted page elements, adding form auto-fill, scraping website data, intercepting requests,
  detecting URL changes in SPAs, or storing persistent user preferences.
  Covers userscript headers (@match, @grant, @require), synchronous and async GM_* API functions,
  common patterns (DOM mutation, URL change detection, element waiting), security sandboxing,
  and cross-browser compatibility (Chrome, Firefox, Edge).
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
---

# Tampermonkey Userscript Development

Expert guidance for writing Tampermonkey userscripts - browser scripts that modify web pages, automate tasks, and enhance browsing experience.

## Quick Start Template

```javascript
// ==UserScript==
// @name         My Script Name                    // ← CUSTOMISE: Unique script name
// @namespace    https://example.com/scripts/      // ← CUSTOMISE: Your unique namespace
// @version      1.0.0                             // ← INCREMENT on updates
// @description  Brief description of the script   // ← CUSTOMISE: What it does
// @author       Your Name                         // ← CUSTOMISE: Your name
// @match        https://example.com/*             // ← CUSTOMISE: Target URL pattern
// @grant        none                              // ← ADD permissions as needed
// @run-at       document-idle                     // ← ADJUST timing if needed
// ==/UserScript==

(function() {
    'use strict';

    // Your code here
    console.log('Script loaded!');
})();
```

---

## Essential Header Tags

| Tag | Required | Purpose | Example |
|-----|----------|---------|---------|
| `@name` | Yes | Script name (supports i18n with `:locale`) | `@name My Script` |
| `@namespace` | Recommended | Unique identifier namespace | `@namespace https://yoursite.com/` |
| `@version` | Yes* | Version for updates (*required for auto-update) | `@version 1.2.3` |
| `@description` | Recommended | What the script does | `@description Enhances page layout` |
| `@match` | Yes** | URLs to run on (**or @include) | `@match https://example.com/*` |
| `@grant` | Situational | API permissions (use `none` for no GM_* APIs) | `@grant GM_setValue` |
| `@run-at` | Optional | When to inject (default: `document-idle`) | `@run-at document-start` |

**For complete header documentation, see:** [header-reference.md](references/header-reference.md)

---

## URL Matching Quick Reference

```javascript
// Exact domain
// @match https://example.com/*

// All subdomains
// @match https://*.example.com/*

// HTTP and HTTPS
// @match *://example.com/*

// Specific path
// @match https://example.com/app/*

// Exclude paths (use with @match)
// @exclude https://example.com/admin/*
```

**For advanced patterns (regex, @include), see:** [url-matching.md](references/url-matching.md)

---

## @grant Permissions Quick Reference

| You Need To... | Grant This |
|----------------|------------|
| Store persistent data | `@grant GM_setValue` + `@grant GM_getValue` |
| Make cross-origin requests | `@grant GM_xmlhttpRequest` + `@connect domain` |
| Add custom CSS | `@grant GM_addStyle` |
| Access page's window | `@grant unsafeWindow` |
| Show notifications | `@grant GM_notification` |
| Add menu commands | `@grant GM_registerMenuCommand` |
| Detect URL changes (SPA) | `@grant window.onurlchange` |

```javascript
// Disable sandbox (no GM_* except GM_info)
// @grant none

// Cross-origin requests require @connect
// @grant GM_xmlhttpRequest
// @connect api.example.com
// @connect *.googleapis.com
```

**For complete permissions guide, see:** [header-reference.md](references/header-reference.md)

---

## @run-at Injection Timing

| Value | When Script Runs | Use Case |
|-------|------------------|----------|
| `document-start` | Before DOM exists | Block resources, modify globals early |
| `document-body` | When body exists | Early DOM manipulation |
| `document-end` | At DOMContentLoaded | Most scripts - DOM ready |
| `document-idle` | After DOMContentLoaded (default) | Safe default |
| `context-menu` | On right-click menu | User-triggered actions |

---

## Common Patterns

### Wait for Element

```javascript
function waitForElement(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const element = document.querySelector(selector);
        if (element) return resolve(element);

        const observer = new MutationObserver((mutations, obs) => {
            const el = document.querySelector(selector);
            if (el) {
                obs.disconnect();
                resolve(el);
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });

        setTimeout(() => {
            observer.disconnect();
            reject(new Error(`Element ${selector} not found`));
        }, timeout);
    });
}

// Usage
waitForElement('#my-element').then(el => {
    console.log('Found:', el);
});
```

### SPA URL Change Detection

```javascript
// @grant window.onurlchange

if (window.onurlchange === null) {
    window.addEventListener('urlchange', (info) => {
        console.log('URL changed to:', info.url);
        // Re-run your modifications
    });
}
```

### Cross-Origin Request

```javascript
// @grant GM_xmlhttpRequest
// @connect api.example.com

GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.example.com/data',
    headers: { 'Content-Type': 'application/json' },
    onload: function(response) {
        const data = JSON.parse(response.responseText);
        console.log(data);
    },
    onerror: function(error) {
        console.error('Request failed:', error);
    }
});
```

### Add Custom Styles

```javascript
// @grant GM_addStyle

GM_addStyle(`
    .my-custom-class {
        background: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }

    #hide-this-element {
        display: none !important;
    }
`);
```

### Persistent Settings

```javascript
// @grant GM_setValue
// @grant GM_getValue
// @grant GM_registerMenuCommand

const settings = {
    enabled: GM_getValue('enabled', true),
    theme: GM_getValue('theme', 'dark')
};

GM_registerMenuCommand('Toggle Enabled', () => {
    settings.enabled = !settings.enabled;
    GM_setValue('enabled', settings.enabled);
    location.reload();
});
```

**For more patterns, see:** [patterns.md](references/patterns.md)

---

## External Resources

### @require - Load External Scripts

```javascript
// @require https://code.jquery.com/jquery-3.6.0.min.js

// With integrity hash (recommended)
// @require https://code.jquery.com/jquery-3.6.0.min.js#sha256-/xUj+3OJU...

// Built-in libraries
// @require tampermonkey://vendor/jquery.js
```

### @resource - Preload Resources

```javascript
// @resource myCSS https://example.com/style.css
// @grant GM_getResourceText
// @grant GM_addStyle

const css = GM_getResourceText('myCSS');
GM_addStyle(css);
```

---

## What Tampermonkey Cannot Do

Userscripts have limitations:

- **Access local files** - Cannot read/write files on your computer
- **Run before page scripts** - In isolated sandbox mode, page scripts run first
- **Access cross-origin iframes** - Browser security prevents this
- **Persist across machines** - GM storage is local to each browser
- **Bypass all CSP** - Some very strict CSP cannot be bypassed

Most limitations have **workarounds** - see [common-pitfalls.md](references/common-pitfalls.md).

---

## When Generating Userscripts

Always include in your response:

1. **Explanation** - What the script does (1-2 sentences)
2. **Complete userscript** - Full code with all headers in a code block
3. **Installation** - "Copy/paste into Tampermonkey dashboard" or "Save as .user.js"
4. **Customisation points** - What the user can safely modify (selectors, timeouts, etc.)
5. **Permissions used** - Which @grants and why they're needed
6. **Browser support** - If Chrome-only, Firefox-only, or universal

**Example response format:**

> This script adds a dark mode toggle to Example.com and remembers the user's preference.

```javascript
// ==UserScript==
// @name         Example.com Dark Mode
// ...
// ==/UserScript==
```

> **Installation:** Copy/paste into Tampermonkey dashboard
> **Customisation:** Change `DARK_BG_COLOR` to adjust the background colour
> **Permissions:** Uses `GM_setValue`/`GM_getValue` to remember preference
> **Browsers:** Chrome and Firefox

---

## Pre-Delivery Checklist

Before returning a userscript, verify:

### Critical (Must Pass)
- [ ] No hardcoded API keys, tokens, or passwords
- [ ] @match is specific (not `*://*/*`)
- [ ] All external URLs use HTTPS
- [ ] User input sanitised before DOM insertion

### Important (Should Pass)
- [ ] Wrapped in IIFE with 'use strict'
- [ ] All @grant statements are necessary
- [ ] @connect includes all external domains
- [ ] Error handling for async operations
- [ ] Null checks before DOM manipulation

### Recommended
- [ ] @version follows semantic versioning (X.Y.Z)
- [ ] Works in both Chrome and Firefox
- [ ] Comments explain non-obvious code

**For complete security checklist, see:** [security-checklist.md](references/security-checklist.md)

---

## Reference Files Guide

Load these on-demand based on user needs:

### Core Documentation

| File | When to Load | Content |
|------|--------------|---------|
| [header-reference.md](references/header-reference.md) | Header syntax questions | All @tags with examples |
| [url-matching.md](references/url-matching.md) | URL pattern questions | @match, @include, @exclude |
| [patterns.md](references/patterns.md) | Implementation patterns | Common script patterns |
| [sandbox-modes.md](references/sandbox-modes.md) | Security/isolation | Execution contexts |

### API Reference

| File | When to Load | Content |
|------|--------------|---------|
| [api-sync.md](references/api-sync.md) | GM_* function usage | Sync API documentation |
| [api-async.md](references/api-async.md) | GM.* promise usage | Async API documentation |
| [api-storage.md](references/api-storage.md) | Data persistence | setValue, getValue, listeners |
| [http-requests.md](references/http-requests.md) | HTTP requests | GM_xmlhttpRequest |
| [web-requests.md](references/web-requests.md) | Request interception | GM_webRequest (Firefox) |
| [api-cookies.md](references/api-cookies.md) | Cookie manipulation | GM_cookie |
| [api-dom-ui.md](references/api-dom-ui.md) | DOM/UI manipulation | addElement, addStyle, unsafeWindow |
| [api-tabs.md](references/api-tabs.md) | Tab management | getTab, saveTab, openInTab |
| [api-audio.md](references/api-audio.md) | Audio control | Mute/unmute tabs |

### Troubleshooting & Quality

| File | When to Load | Content |
|------|--------------|---------|
| [common-pitfalls.md](references/common-pitfalls.md) | Script issues | What breaks scripts |
| [debugging.md](references/debugging.md) | Troubleshooting | How to debug |
| [browser-compatibility.md](references/browser-compatibility.md) | Cross-browser | Chrome vs Firefox |
| [security-checklist.md](references/security-checklist.md) | Pre-delivery | Security validation |
| [version-numbering.md](references/version-numbering.md) | Version strings | Comparison rules |
