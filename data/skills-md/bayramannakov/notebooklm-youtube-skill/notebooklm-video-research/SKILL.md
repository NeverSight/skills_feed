---
name: notebooklm-video-research
description: Automate NotebookLM notebook creation from YouTube videos. Given a YouTube video URL, extract information about people featured in the video, research them online, create a new NotebookLM notebook with the video and research as sources, and generate an audio overview. Uses screenshot-first automation to reliably target UI elements.
---

# NotebookLM Video Research Skill

Automate NotebookLM notebook creation from YouTube videos with automatic research and Audio Overview generation.

## Core Principle

**Screenshot before every action** — verify UI state, identify correct elements, confirm success.

```
📸 Screenshot → 👀 Analyze → 🎯 Target → ✅ Verify → 🖱️ Execute → 📸 Screenshot → ✓ Confirm
```

---

## Quick Start Workflow

### Phase 1: Research

```python
# 1. Get video info
Control Chrome:open_url("https://www.youtube.com/watch?v=VIDEO_ID")
Control Chrome:get_page_content()

# 2. Research people mentioned
web_search("[Person Name] background career")

# 3. Create research document (keep under 500k chars)
```

### Phase 2: NotebookLM Automation

```python
# 1. Navigate
Control Chrome:open_url("https://notebooklm.google.com/")

# 2. Create notebook
# Click "Create new" button

# 3. Add YouTube source
# Click "Websites" → Enter URL → Click "Insert"

# 4. Add research document  
# Click "Add sources" → "Copied text" → Paste content → Click "Insert"

# 5. Generate audio
# Click "Audio Overview" in Studio panel
```

---

## Critical: Element Targeting

### ⚠️ The Main Trap

NotebookLM has **multiple textareas**. Generic selectors grab the wrong one!

```
SIDEBAR (wrong)          CENTER MODAL (correct)
┌──────────────┐         ┌──────────────────┐
│ Search box   │         │ URL/Text input   │
│ query-input  │         │ "Paste any links"|
└──────────────┘         └──────────────────┘
```

### Correct Selectors

| Element | Selector |
|---------|----------|
| URL input | `textarea[placeholder="Paste any links"]` |
| Text input | `textarea[placeholder="Paste text here"]` |
| Sidebar (AVOID) | `textarea[placeholder*="Search"]` |

### Angular Event Pattern

```javascript
// Simple .value = doesn't work! Use this:
var setter = Object.getOwnPropertyDescriptor(
    HTMLTextAreaElement.prototype, 'value'
).set;
setter.call(textarea, 'content');
textarea.dispatchEvent(new Event('input', {bubbles: true}));
textarea.dispatchEvent(new Event('change', {bubbles: true}));
```

### Button State Check

```javascript
var btn = document.querySelector('button');
if (btn && !btn.disabled && !btn.className.includes('disabled')) {
    btn.click();
}
```

---

## Complete Code Snippets

### Enter YouTube URL

```javascript
var urlTextarea = document.querySelector('textarea[placeholder="Paste any links"]');
if (urlTextarea) {
    var setter = Object.getOwnPropertyDescriptor(
        HTMLTextAreaElement.prototype, 'value'
    ).set;
    setter.call(urlTextarea, 'https://www.youtube.com/watch?v=VIDEO_ID');
    urlTextarea.dispatchEvent(new Event('input', {bubbles: true}));
    urlTextarea.dispatchEvent(new Event('change', {bubbles: true}));
}
```

### Enter Research Text

```javascript
var pasteTextarea = document.querySelector('textarea[placeholder="Paste text here"]');
if (pasteTextarea) {
    var setter = Object.getOwnPropertyDescriptor(
        HTMLTextAreaElement.prototype, 'value'
    ).set;
    setter.call(pasteTextarea, RESEARCH_CONTENT);
    pasteTextarea.dispatchEvent(new Event('input', {bubbles: true}));
    pasteTextarea.dispatchEvent(new Event('change', {bubbles: true}));
}
```

### Click Button by Text

```javascript
var buttons = Array.from(document.querySelectorAll('button'));
var btn = buttons.find(b => b.textContent.includes('Insert'));
if (btn && !btn.disabled) {
    btn.click();
}
```

### Verify State

```javascript
// Check what textareas exist
var textareas = Array.from(document.querySelectorAll('textarea'));
textareas.map(t => ({
    placeholder: t.placeholder,
    value: t.value.substring(0, 50)
}));
```

---

## Checkpoint Summary

| Step | Verify Before | Verify After |
|------|---------------|--------------|
| Navigate | - | Home page loaded |
| Create notebook | Create button visible | Notebook opened |
| Add URL | **Correct textarea identified** | URL in center, not sidebar |
| Click Insert | **Button ENABLED** | Source added |
| Add text | **Correct textarea identified** | Text in center, not sidebar |
| Click Insert | **Button ENABLED** | 2 sources shown |
| Audio Overview | Studio panel visible | Generation started |

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `document.querySelector('textarea')` | `textarea[placeholder="Paste any links"]` |
| Click without checking state | Verify button enabled first |
| Assume action succeeded | Screenshot to confirm |
| Rush through steps | Wait for async operations |

---

## Wait Times

| Action | Wait |
|--------|------|
| Page navigation | 3s |
| Dialog open | 2s |
| YouTube source processing | 8-10s |
| Text source processing | 5s |
| Audio generation | 5-10 minutes |

---

## Error Recovery

**Wrong input targeted:**
1. Clear sidebar: `document.querySelectorAll('.query-input').forEach(el => el.value = '')`
2. Re-target with specific selector

**Button disabled:**
1. Re-dispatch events on textarea
2. Verify content actually entered

**Modal didn't open:**
1. Wait longer
2. Click trigger button again
