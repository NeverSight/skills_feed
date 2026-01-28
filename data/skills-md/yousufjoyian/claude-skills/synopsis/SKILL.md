---
name: synopsis
description: Generate a manager-focused synopsis with current context - ALWAYS includes save button
---

# Synopsis Skill

Generate a **manager-focused synopsis** that explains what's happening NOW and recent work.

## MANDATORY ELEMENTS (NEVER SKIP)

Before outputting HTML, verify ALL of these are present:

| Element | Required | Check |
|---------|----------|-------|
| **Current Context box** | YES | Blue box at top showing what we're doing RIGHT NOW |
| **Hero section** | YES | Most recent completed task |
| **Save button** | YES | Orange button at bottom with `exportSynopsis()` |
| **Project path in JS** | YES | Replace `[PROJECT_PATH]` with actual path |

**If any element is missing, the synopsis is INVALID. Do not output.**

## Trigger Phrases

- "show synopsis" / "synopsis" / "session summary" - Display in A2UI panel
- "export synopsis" - Display AND save to project folder

## Structure (Top to Bottom)

1. **CURRENT CONTEXT** (blue box) - What is actively happening right now
2. **HERO** (gradient box) - Most recent completed task
3. **TABS** - What Changed / Why It Matters / Technical
4. **SAVE BUTTON** (orange) - ALWAYS present at bottom

## Execution Steps

### Step 1: Gather Current Context

Ask yourself: **What are we doing RIGHT NOW?**
- What task is in progress?
- What is the user trying to accomplish?
- What's the immediate next step?

```bash
# Get project context
cat <project>/.claude/CONTEXT.md 2>/dev/null
git status --short
git log --oneline -3
```

### Step 2: Identify Recent Completed Work

What did we JUST finish? Pull from:
- Current conversation
- What the user asked for
- What was actually implemented

### Step 3: Get A2UI Log Path

Use the path from your terminal startup message:
```
A2UI VISUALIZATION: Write HTML to /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/<terminal_id>/a2ui_input.log
```

Or discover dynamically:
```bash
python3 << 'PY'
import json, urllib.request
data = json.loads(urllib.request.urlopen("http://localhost:7690/api/projects").read())
active_proj_id = data.get('activeProjectId')
for p in data.get('projects', []):
    if p.get('id') == active_proj_id:
        term_id = p.get('activeTerminalId')
        for t in p.get('terminals', []):
            if t.get('id') == term_id:
                print(f"TERMINAL_ID={term_id}")
                print(f"A2UI_LOG=/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/{term_id}/a2ui_input.log")
PY
```

### Step 4: Generate Synopsis HTML

**CRITICAL: Copy the ENTIRE template below. Do not skip any section.**

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:system-ui;font-size:12px;padding:16px;line-height:1.5}
.context{background:#1e3a5f;padding:14px;border-radius:10px;border:2px solid #3b82f6;margin-bottom:14px}
.context-label{font-size:10px;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;display:flex;align-items:center;gap:6px}
.context-label::before{content:"";width:8px;height:8px;background:#3b82f6;border-radius:50%;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.context h2{font-size:14px;color:#f8fafc;margin-bottom:4px}
.context p{color:#94a3b8;font-size:12px}
.context .next{margin-top:8px;padding-top:8px;border-top:1px solid #334155;font-size:11px;color:#60a5fa}
.hero{background:linear-gradient(135deg,#1e3a5f,#0f172a);padding:16px;border-radius:10px;border-left:4px solid #22c55e;margin-bottom:16px}
.hero h1{font-size:15px;color:#f8fafc;margin-bottom:8px}
.hero p{color:#94a3b8;font-size:13px}
.status{display:inline-block;padding:3px 10px;border-radius:12px;font-size:10px;font-weight:600;margin-bottom:8px}
.status.done{background:#22c55e;color:#0f172a}
.status.active{background:#f59e0b;color:#0f172a}
.status.blocked{background:#ef4444;color:#fff}
.tabs{display:flex;gap:6px;margin-bottom:14px}
.tab{padding:8px 14px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:500;background:#1e293b;color:#94a3b8;border:none;transition:all 0.2s}
.tab:hover{background:#334155}
.tab.active{background:#3b82f6;color:#fff}
.content{display:none}
.content.active{display:block}
.section{background:#1e293b;border-radius:8px;padding:14px;margin-bottom:12px}
.section h2{font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.section h2 span{font-size:14px}
.item{padding:10px 12px;background:#0f172a;border-radius:6px;margin-bottom:8px}
.item:last-child{margin-bottom:0}
.item-title{font-weight:600;color:#f8fafc;margin-bottom:4px}
.item-desc{color:#94a3b8;font-size:11px}
.impact{color:#4ade80;font-size:11px;margin-top:6px}
.tech{font-family:monospace;font-size:10px;color:#64748b;background:#1e293b;padding:2px 6px;border-radius:3px}
.pending{border-left:3px solid #f59e0b}
.export-btn{width:100%;margin-top:12px;padding:12px;background:#f59e0b;color:#0f172a;border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer}
.export-btn:hover{background:#fbbf24}
</style>
</head>
<body>

<!-- ========== CURRENT CONTEXT (MANDATORY) ========== -->
<!-- This section shows what is happening RIGHT NOW -->
<div class="context">
<div class="context-label">Current Context</div>
<h2>[WHAT_WE_ARE_DOING_NOW]</h2>
<p>[Brief description of active task - what is the user trying to accomplish?]</p>
<div class="next">Next → [Immediate next step]</div>
</div>

<!-- ========== HERO: Recent completed work ========== -->
<div class="hero">
<span class="status done">✓ JUST COMPLETED</span>
<h1>[COMPLETED_TASK_HEADLINE]</h1>
<p>[ONE_SENTENCE_SUMMARY - plain English, what did we do and why]</p>
</div>

<div class="tabs">
<div class="tab active" onclick="showTab('what')">What Changed</div>
<div class="tab" onclick="showTab('why')">Why It Matters</div>
<div class="tab" onclick="showTab('details')">Technical</div>
</div>

<!-- TAB 1: What Changed - Plain English -->
<div id="what" class="content active">
<div class="section">
<h2><span>🔧</span> Changes Made</h2>

<div class="item">
<div class="item-title">[CHANGE_1_TITLE]</div>
<div class="item-desc">[Plain English description - what does this do for the user?]</div>
<div class="impact">→ [Practical benefit]</div>
</div>

<div class="item">
<div class="item-title">[CHANGE_2_TITLE]</div>
<div class="item-desc">[Description]</div>
<div class="impact">→ [Benefit]</div>
</div>

</div>

<!-- Show pending items if any -->
<div class="section pending">
<h2><span>📋</span> Still Pending</h2>
<div class="item">
<div class="item-title">[PENDING_ITEM]</div>
<div class="item-desc">[What still needs to be done]</div>
</div>
</div>
</div>

<!-- TAB 2: Why It Matters - Impact/Value -->
<div id="why" class="content">
<div class="section">
<h2><span>💡</span> Why This Matters</h2>

<div class="item">
<div class="item-title">[BENEFIT_1_TITLE]</div>
<div class="item-desc">[Explain the value - what problem does this solve? Who benefits?]</div>
</div>

<div class="item">
<div class="item-title">[BENEFIT_2_TITLE]</div>
<div class="item-desc">[Another angle on the value]</div>
</div>

</div>
</div>

<!-- TAB 3: Technical - For those who want details -->
<div id="details" class="content">
<div class="section">
<h2><span>⚙️</span> Technical Details</h2>

<div class="item">
<div class="item-title">Files Modified</div>
<div class="item-desc"><span class="tech">[file1.ts]</span> <span class="tech">[file2.py]</span></div>
</div>

<div class="item">
<div class="item-title">What Was Wrong</div>
<div class="item-desc">[Root cause in technical terms]</div>
</div>

<div class="item">
<div class="item-title">How It Was Fixed</div>
<div class="item-desc">[Technical solution - function names, approach]</div>
</div>

</div>
</div>

<!-- ========== SAVE BUTTON (MANDATORY - NEVER REMOVE) ========== -->
<button class="export-btn" onclick="exportSynopsis()">📥 Save This Synopsis</button>

<!-- ========== JAVASCRIPT (MANDATORY - NEVER REMOVE) ========== -->
<script>
function showTab(id) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById(id).classList.add('active');
}

function getApiUrl() {
  try {
    const p = window.parent.location;
    return p.protocol === 'https:'
      ? p.protocol + '//' + p.host + '/api/save-synopsis'
      : 'http://' + p.hostname + ':7690/api/save-synopsis';
  } catch(e) { return 'http://localhost:7690/api/save-synopsis'; }
}

async function exportSynopsis() {
  const btn = document.querySelector('.export-btn');
  btn.textContent = 'Saving...'; btn.disabled = true;
  try {
    const res = await fetch(getApiUrl(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectPath: '[PROJECT_PATH]', html: document.documentElement.outerHTML })
    });
    const data = await res.json();
    btn.textContent = data.success ? '✓ Saved!' : 'Error: ' + (data.error || 'failed');
    btn.style.background = data.success ? '#22c55e' : '#ef4444';
  } catch (e) {
    btn.textContent = 'Error: ' + e.message;
    btn.style.background = '#ef4444';
  }
  setTimeout(() => { btn.textContent = '📥 Save This Synopsis'; btn.style.background = '#f59e0b'; btn.disabled = false; }, 3000);
}
</script>
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

## Example: Good vs Bad

### BAD (old style):
```
Project: TriClaude
Status: Complete
Files Changed:
- src/services/consigliereService.ts
- skills/synopsis/SKILL.md
Recent Commits: 6be15c3, 5e91989
```
*Problem: Doesn't tell me what happened or why I should care*

### GOOD (new style):
```
✓ JUST COMPLETED
Fixed Synopsis Export Button

The export button was failing on HTTPS. Updated it to
detect the connection type and route correctly.

What Changed:
• Smart URL Detection
  Button now works on both localhost and mobile
  → Export works everywhere now

Why It Matters:
• Mobile Access Fixed
  When accessing from phone via Tailscale, export was broken
```
*Better: I know what happened, what changed, and why it matters*

## Export Location

Synopses save to:
```
<project>/.claude/synopses/synopsis_YYYYMMDD_HHMMSS.html
```

## HTTPS Note

The `getApiUrl()` function handles both:
- **HTTP** (localhost:3001): Direct call to port 7690
- **HTTPS** (Tailscale:3443): Routes through Caddy proxy at `/api/*`

---

## FINAL VERIFICATION (Run Before Output)

**STOP. Before writing to A2UI, verify:**

```
□ Current Context box present? (blue box with pulsing dot)
□ Hero section present? (completed task)
□ Save button present? (<button class="export-btn">)
□ [PROJECT_PATH] replaced with actual path?
□ All [PLACEHOLDERS] filled with real content?
```

**If ANY checkbox fails → Do NOT output. Fix first.**

### Common Mistakes to Avoid

| Mistake | Why It's Bad | Fix |
|---------|--------------|-----|
| Skipping Current Context | User loses track of where they are | Always include - even if just "Reviewing code" |
| Missing save button | User can't export the synopsis | Copy the ENTIRE template including `<button>` and `<script>` |
| Generic placeholders | "[TASK_HEADLINE]" is useless | Replace with actual content from conversation |
| Wrong project path | Save fails silently | Use actual path like `/home/yousuf/local_workspaces/triclaude` |

### Minimal Valid Synopsis

At minimum, a valid synopsis MUST have:
1. `<div class="context">` with real content
2. `<div class="hero">` with real content
3. `<button class="export-btn">` with working `exportSynopsis()`
4. `<script>` block with `showTab()`, `getApiUrl()`, `exportSynopsis()`

**No exceptions.**
