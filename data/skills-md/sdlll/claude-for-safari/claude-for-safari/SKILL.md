---
name: claude-for-safari
description: Control the user's real Safari browser on macOS using AppleScript and screencapture. This skill should be used when the user asks to interact with Safari, browse websites, read web pages, automate browser tasks, take screenshots of web content, or when any task would benefit from seeing or interacting with what's in their browser. Triggers on keywords like "safari", "browser", "web page", "open tab", "screenshot the page", "read this site", "browse", "click on", "fill in the form".
---

# Claude for Safari

Operate the user's real Safari browser on macOS via AppleScript (`osascript`) and `screencapture`. This provides full access to the user's actual browser session — including login state, cookies, and open tabs — without any extensions or additional software.

## Prerequisites

Before first use, verify two settings are enabled. Run this check at the start of every session:

```bash
osascript -e 'tell application "Safari" to get name of front window' 2>&1
```

If this fails, instruct the user to enable:
1. **System Settings > Privacy & Security > Automation** — grant terminal app permission to control Safari
2. **Safari > Settings > Advanced** — enable "Show features for web developers", then **Develop menu > Allow JavaScript from Apple Events**

## Core Capabilities

### 1. List All Open Tabs

```bash
osascript -e '
tell application "Safari"
  set output to ""
  repeat with w from 1 to (count of windows)
    repeat with t from 1 to (count of tabs of window w)
      set tabName to name of tab t of window w
      set tabURL to URL of tab t of window w
      set output to output & "W" & w & "T" & t & " | " & tabName & " | " & tabURL & linefeed
    end repeat
  end repeat
  return output
end tell'
```

### 2. Read Page Content

Read the full text content of the current tab:

```bash
osascript -e '
tell application "Safari"
  do JavaScript "document.body.innerText" in current tab of front window
end tell'
```

Read structured content (title, URL, meta description, headings):

```bash
osascript -e '
tell application "Safari"
  do JavaScript "JSON.stringify({
    title: document.title,
    url: location.href,
    description: document.querySelector(\"meta[name=description]\")?.content || \"\",
    h1: [...document.querySelectorAll(\"h1\")].map(e => e.textContent).join(\" | \"),
    h2: [...document.querySelectorAll(\"h2\")].map(e => e.textContent).join(\" | \")
  })" in current tab of front window
end tell'
```

Read a simplified DOM (similar to Chrome ACP's `browser_read`):

```bash
osascript -e '
tell application "Safari"
  do JavaScript "
    (function() {
      const walk = (node, depth) => {
        let result = \"\";
        for (const child of node.childNodes) {
          if (child.nodeType === 3) {
            const text = child.textContent.trim();
            if (text) result += text + \"\\n\";
          } else if (child.nodeType === 1) {
            const tag = child.tagName.toLowerCase();
            if ([\"script\",\"style\",\"noscript\",\"svg\"].includes(tag)) continue;
            const style = getComputedStyle(child);
            if (style.display === \"none\" || style.visibility === \"hidden\") continue;
            if ([\"h1\",\"h2\",\"h3\",\"h4\",\"h5\",\"h6\"].includes(tag))
              result += \"#\".repeat(parseInt(tag[1])) + \" \";
            if (tag === \"a\") result += \"[\";
            if (tag === \"img\") result += \"[Image: \" + (child.alt || \"\") + \"]\\n\";
            else if (tag === \"input\") result += \"[Input \" + child.type + \": \" + (child.value || child.placeholder || \"\") + \"]\\n\";
            else if (tag === \"button\") result += \"[Button: \" + child.textContent.trim() + \"]\\n\";
            else result += walk(child, depth + 1);
            if (tag === \"a\") result += \"](\" + child.href + \")\\n\";
            if ([\"p\",\"div\",\"li\",\"tr\",\"br\",\"h1\",\"h2\",\"h3\",\"h4\",\"h5\",\"h6\"].includes(tag))
              result += \"\\n\";
          }
        }
        return result;
      };
      return walk(document.body, 0).substring(0, 50000);
    })()
  " in current tab of front window
end tell'
```

### 3. Execute JavaScript

Run arbitrary JavaScript in the page context and get the return value:

```bash
osascript -e '
tell application "Safari"
  do JavaScript "YOUR_JS_CODE_HERE" in current tab of front window
end tell'
```

For multi-line scripts, use a heredoc:

```bash
osascript << 'APPLESCRIPT'
tell application "Safari"
  do JavaScript "
    (function() {
      // Multi-line JS here
      return 'result';
    })()
  " in current tab of front window
end tell
APPLESCRIPT
```

### 4. Screenshot

Two approaches are available. Auto-detect which to use at session start:

```bash
# Test if Screen Recording permission is granted (background screenshot available)
/tmp/safari_wid 2>/dev/null && echo "BACKGROUND_SCREENSHOT=true" || echo "BACKGROUND_SCREENSHOT=false"
```

#### Background Screenshot (requires Screen Recording permission)

If the user has granted Screen Recording permission to the terminal app, use `screencapture -l` to capture Safari **without activating it**:

```bash
# Compile the helper once per session (if not already compiled)
if [ ! -f /tmp/safari_wid ]; then
cat > /tmp/safari_wid.swift << 'SWIFT'
import CoreGraphics
import Foundation
let options: CGWindowListOption = [.optionOnScreenOnly, .excludeDesktopElements]
guard let windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else { exit(1) }
for window in windowList {
    guard let owner = window[kCGWindowOwnerName as String] as? String,
          owner == "Safari",
          let layer = window[kCGWindowLayer as String] as? Int,
          layer == 0,
          let wid = window[kCGWindowNumber as String] as? Int else { continue }
    print(wid)
    exit(0)
}
exit(1)
SWIFT
swiftc /tmp/safari_wid.swift -o /tmp/safari_wid
fi

# Capture Safari window in background (no activation needed)
WID=$(/tmp/safari_wid)
screencapture -l "$WID" -o -x /tmp/safari_screenshot.png
```

To enable this, instruct the user: **System Settings > Privacy & Security > Screen Recording** — grant permission to the terminal app (Terminal / iTerm / Warp).

#### Foreground Screenshot (no extra permissions needed)

If Screen Recording is not granted, fall back to region-based capture. This briefly activates Safari (~0.5s), then switches back:

```bash
# Remember current frontmost app
FRONT_APP=$(osascript -e 'tell application "System Events" to get name of first process whose frontmost is true')

# Activate Safari and capture its window region
osascript -e 'tell application "Safari" to activate'
sleep 0.3
BOUNDS=$(osascript -e '
tell application "System Events"
  tell process "Safari"
    -- Safari may expose a thin toolbar as window 1; find the largest window
    set bestW to 0
    set bestBounds to ""
    repeat with i from 1 to (count of windows)
      set {x, y} to position of window i
      set {w, h} to size of window i
      if w * h > bestW then
        set bestW to w * h
        set bestBounds to (x as text) & "," & (y as text) & "," & (w as text) & "," & (h as text)
      end if
    end repeat
    return bestBounds
  end tell
end tell')
screencapture -x -R "$BOUNDS" /tmp/safari_screenshot.png

# Switch back to the previous app
osascript -e "tell application \"$FRONT_APP\" to activate"
```

After capturing with either method, read the screenshot to see what's on screen:

```
Use the Read tool on /tmp/safari_screenshot.png to view the captured image.
```

### 5. Navigate

Open a URL in the current tab:

```bash
osascript -e '
tell application "Safari"
  set URL of current tab of front window to "https://example.com"
end tell'
```

Open a URL in a new tab:

```bash
osascript -e '
tell application "Safari"
  tell front window
    set newTab to make new tab with properties {URL:"https://example.com"}
    set current tab to newTab
  end tell
end tell'
```

Open a URL in a new window:

```bash
osascript -e 'tell application "Safari" to make new document with properties {URL:"https://example.com"}'
```

### 6. Click Elements

Click using JavaScript (preferred — works with SPAs and reactive frameworks):

```bash
osascript -e '
tell application "Safari"
  do JavaScript "
    const el = document.querySelector(\"button.submit\");
    if (el) {
      el.dispatchEvent(new MouseEvent(\"click\", {bubbles: true, cancelable: true}));
      \"clicked\";
    } else {
      \"element not found\";
    }
  " in current tab of front window
end tell'
```

**Important**: Use `dispatchEvent(new MouseEvent(..., {bubbles: true}))` instead of `.click()` for React/Vue/Angular compatibility. Native `.click()` may bypass synthetic event handlers.

### 7. Type and Fill Forms

Set input values via JavaScript:

```bash
osascript -e '
tell application "Safari"
  do JavaScript "
    const input = document.querySelector(\"input[name=search]\");
    const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, \"value\").set;
    nativeSetter.call(input, \"search text\");
    input.dispatchEvent(new Event(\"input\", {bubbles: true}));
    input.dispatchEvent(new Event(\"change\", {bubbles: true}));
  " in current tab of front window
end tell'
```

**Important**: For React-controlled inputs, use the native setter + `dispatchEvent` pattern shown above. Directly setting `.value` will not trigger React's state update.

Type via System Events (simulates real keyboard — useful when JS injection is blocked):

```bash
osascript -e '
tell application "Safari" to activate
delay 0.3
tell application "System Events"
  keystroke "hello world"
end tell'
```

Press special keys:

```bash
osascript -e '
tell application "System Events"
  key code 36  -- Enter/Return
  key code 48  -- Tab
  key code 51  -- Delete/Backspace
  keystroke "a" using command down  -- Cmd+A (select all)
  keystroke "c" using command down  -- Cmd+C (copy)
end tell'
```

### 8. Scroll

```bash
# Scroll down 500px
osascript -e 'tell application "Safari" to do JavaScript "window.scrollBy(0, 500)" in current tab of front window'

# Scroll to top
osascript -e 'tell application "Safari" to do JavaScript "window.scrollTo(0, 0)" in current tab of front window'

# Scroll to bottom
osascript -e 'tell application "Safari" to do JavaScript "window.scrollTo(0, document.body.scrollHeight)" in current tab of front window'

# Scroll element into view
osascript -e 'tell application "Safari" to do JavaScript "document.querySelector(\"#target\").scrollIntoView({behavior: \"smooth\"})" in current tab of front window'
```

### 9. Switch Tabs

```bash
# Switch to tab 2 in the front window
osascript -e 'tell application "Safari" to set current tab of front window to tab 2 of front window'

# Switch to a tab by URL match
osascript -e '
tell application "Safari"
  repeat with t from 1 to (count of tabs of front window)
    if URL of tab t of front window contains "github.com" then
      set current tab of front window to tab t of front window
      exit repeat
    end if
  end repeat
end tell'
```

### 10. Wait for Page Load

```bash
osascript -e '
tell application "Safari"
  -- Wait until page finishes loading (max 10 seconds)
  repeat 20 times
    set readyState to do JavaScript "document.readyState" in current tab of front window
    if readyState is "complete" then exit repeat
    delay 0.5
  end repeat
end tell'
```

## Workflow: Browsing with Screenshot Feedback Loop

For tasks that require visual confirmation, use the screenshot loop:

1. Perform action (navigate, click, scroll, etc.)
2. Wait for page load if needed
3. Take screenshot (background or foreground) → Read the image to see result
4. Decide next action based on what is visible

## Operating on Specific Tabs

To operate on a tab other than the current one, use `tab N of window M` syntax:

```bash
# Read content of tab 3 in window 1
osascript -e 'tell application "Safari" to do JavaScript "document.title" in tab 3 of window 1'

# Execute JS in a specific tab
osascript -e 'tell application "Safari" to do JavaScript "document.body.innerText.substring(0, 1000)" in tab 2 of front window'
```

Note: Background screenshots capture the entire Safari window (whichever tab is active). To screenshot a specific tab, first switch to it via AppleScript.

## Limitations

- **macOS only** — AppleScript and screencapture are macOS-specific
- **Cannot intercept network requests** — only page content and JS execution
- **Cannot access cross-origin iframes** — browser security applies
- **Private browsing windows** — AppleScript cannot control private windows
- **System Events keystroke is "blind"** — it types into whatever is focused; ensure Safari is frontmost before using
