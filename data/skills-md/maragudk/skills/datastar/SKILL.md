---
name: datastar
description: Guide for building interactive web UIs with Datastar and gomponents-datastar. Use this skill when adding frontend interactivity to Go web applications with Datastar attributes.
license: MIT
---

# Datastar

## Overview

Datastar is a lightweight frontend framework that enables backend-driven, interactive UIs through a hypermedia-first approach. It combines backend reactivity (similar to htmx) with frontend reactivity (like Alpine.js) using standard HTML `data-*` attributes.

## When to Use This Skill

Use this skill when:
- Adding frontend interactivity to server-rendered HTML
- Building reactive UIs driven by backend state
- Using Datastar with gomponents in Go applications
- Working with Server-Sent Events (SSE) for real-time updates

**Prerequisite:** When using Datastar with Go, also use the **gomponents** skill for HTML component patterns.

## Installation

### Browser (CDN)

```html
<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@v1.0.0-RC.7/bundles/datastar.js"></script>
```

### Go (gomponents-datastar)

```
go get maragu.dev/gomponents-datastar
```

---

# Part 1: Datastar Fundamentals

## Core Concepts

### Signals

Signals are reactive state containers. When a signal's value changes, all dependent expressions automatically update.

```html
<div data-signals="{count: 0}">
    <span data-text="$count"></span>
    <button data-on:click="$count++">Increment</button>
</div>
```

- Signal names are prefixed with `$` in expressions
- Setting a signal to `null` or `undefined` removes it
- Use dot-notation for nested signals: `$user.name`

### DOM Patching

Datastar uses morphing to update only changed DOM parts while preserving state. The backend sends HTML fragments that patch into the existing page.

## Attributes Reference

### State Management

**data-signals** - Initialize reactive signals:
```html
<div data-signals="{name: 'World', count: 0}"></div>
```

**data-computed** - Create derived read-only signals:
```html
<div data-computed="{doubled: $count * 2}"></div>
```

**data-init** - Run expressions when element loads:
```html
<div data-init="console.log('Loaded')"></div>
```

### Data Binding

**data-text** - Bind text content to an expression:
```html
<span data-text="'Hello, ' + $name"></span>
```

**data-bind** - Two-way binding for form elements:
```html
<input data-bind="$name" type="text">
```

**data-show** - Conditionally show/hide elements:
```html
<div data-show="$isVisible">Only shown when true</div>
```

### Styling

**data-class** - Conditionally apply CSS classes:
```html
<div data-class="{'active': $isActive, 'error': $hasError}"></div>
```

**data-style** - Set inline styles dynamically:
```html
<div data-style="{'color': $textColor, 'opacity': $opacity}"></div>
```

**data-attr** - Set HTML attributes dynamically:
```html
<button data-attr="{'disabled': $isLoading}">Submit</button>
```

### Events

**data-on** - Attach event listeners:
```html
<button data-on:click="$count++">Click me</button>
<input data-on:input="$search = evt.target.value">
<form data-on:submit__prevent="@post('/submit')">
```

The `evt` variable references the event object.

**data-on-intersect** - Trigger when element enters viewport:
```html
<div data-on-intersect="@get('/load-more')">Loading...</div>
```

**data-on-interval** - Run at regular intervals:
```html
<div data-on-interval="$elapsed++">Timer: <span data-text="$elapsed"></span></div>
```

**data-on-signal-patch** - Execute when signals update:
```html
<div data-on-signal-patch="console.log('Signals changed:', patch)"></div>
```

### DOM Control

**data-ref** - Create signal referencing DOM element:
```html
<input data-ref="$inputEl" type="text">
```

**data-ignore** - Exclude element from Datastar processing:
```html
<div data-ignore>Third-party widget here</div>
```

**data-ignore-morph** - Keep Datastar active but skip morphing:
```html
<div data-ignore-morph>Preserve this DOM structure</div>
```

**data-preserve-attr** - Preserve attributes during morphing:
```html
<input data-preserve-attr="value" type="text">
```

### Backend Actions

**@get(), @post(), @put(), @patch(), @delete()** - Send requests to backend:
```html
<button data-on:click="@get('/api/data')">Load</button>
<button data-on:click="@post('/api/submit')">Submit</button>
```

## Modifiers

Modifiers extend attribute behavior using double-underscore syntax:

### Timing Modifiers
- `__debounce` / `__debounce_500ms` - Debounce execution
- `__throttle` / `__throttle_1s` - Throttle execution
- `__delay` / `__delay_200ms` - Delay execution

### Event Modifiers
- `__prevent` - Call `preventDefault()`
- `__stop` - Call `stopPropagation()`
- `__capture` - Use capture phase
- `__passive` - Mark as passive listener
- `__once` - Execute only once
- `__self` - Only trigger if target is the element itself
- `__outside` - Trigger when event occurs outside element
- `__window` - Attach listener to window

### Example with Modifiers
```html
<input data-on:input__debounce_300ms="@get('/search?q=' + $query)">
<button data-on:click__once="@post('/track-click')">Track</button>
<form data-on:submit__prevent="@post('/submit')">
```

## Server-Sent Events (SSE)

Datastar uses SSE for streaming responses. The backend sends events with `text/event-stream` content type.

### SSE Event Types

**datastar-patch-elements** - Patch HTML into the DOM:
```
event: datastar-patch-elements
data: elements <div id="content">Updated content</div>
```

**datastar-patch-signals** - Update signal values:
```
event: datastar-patch-signals
data: signals {count: 42}
```

**datastar-remove-elements** - Remove elements by selector:
```
event: datastar-remove-elements
data: selector #old-element
```

---

# Part 2: gomponents-datastar

## Overview

gomponents-datastar provides Go functions that generate Datastar attributes as gomponents nodes. It integrates seamlessly with the gomponents library.

## Import Convention

Use dot imports for a clean DSL:

```go
import (
    . "maragu.dev/gomponents"
    . "maragu.dev/gomponents/html"
    data "maragu.dev/gomponents-datastar"
)
```

Note: The `data` alias is recommended for datastar.

For up-to-date API documentation, run:
```
go doc maragu.dev/gomponents-datastar
```

## Function Reference

### State Management

**Signals** - Initialize reactive signals:
```go
data.Signals(map[string]any{
    "count": 0,
    "name":  "World",
})
```

**Computed** - Create computed signals (key-value pairs):
```go
data.Computed("doubled", "$count * 2")
```

**Init** - Run expression on load:
```go
data.Init("console.log('Component loaded')")
```

### Data Binding

**Text** - Bind text content:
```go
Span(data.Text("'Hello, ' + $name"))
```

**Bind** - Two-way form binding:
```go
Input(Type("text"), data.Bind("$name"))
```

**Show** - Conditional visibility:
```go
Div(data.Show("$isVisible"), Text("Shown when visible"))
```

### Styling

**Class** - Conditional classes (key-value pairs):
```go
data.Class("active", "$isActive", "error", "$hasError")
```

**Style** - Dynamic inline styles (key-value pairs):
```go
data.Style("color", "$textColor", "opacity", "$opacity")
```

**Attr** - Dynamic attributes (key-value pairs):
```go
data.Attr("disabled", "$isLoading", "aria-busy", "$isLoading")
```

### Events

**On** - Attach event listeners:
```go
data.On("click", "$count++")
data.On("click", "@post('/submit')", data.ModifierPrevent)
data.On("input", "$search = evt.target.value", data.ModifierDebounce)
```

**OnIntersect** - Viewport intersection:
```go
data.OnIntersect("@get('/load-more')")
```

**OnInterval** - Periodic execution:
```go
data.OnInterval("$elapsed++")
```

**OnSignalPatch** - React to signal changes:
```go
data.OnSignalPatch("console.log('Updated')")
```

### DOM Control

**Ref** - Reference DOM element:
```go
data.Ref("$inputEl")
```

**Ignore** - Skip Datastar processing:
```go
data.Ignore()
```

**IgnoreMorph** - Skip morphing only:
```go
data.IgnoreMorph()
```

**PreserveAttr** - Preserve attributes during morph:
```go
data.PreserveAttr("value", "checked")
```

### Request Helpers

**Indicator** - Show loading state:
```go
data.Indicator("$isLoading")
```

**JSONSignals** - Control which signals are sent:
```go
data.JSONSignals(data.Filter{Include: "form.*"})
data.JSONSignals(data.Filter{Exclude: "internal.*"})
```

## Modifiers

Use modifier constants with event functions:

```go
// Timing
data.ModifierDebounce  // __debounce
data.ModifierThrottle  // __throttle
data.ModifierDelay     // __delay

// Event behavior
data.ModifierPrevent   // __prevent
data.ModifierStop      // __stop
data.ModifierCapture   // __capture
data.ModifierPassive   // __passive
data.ModifierOnce      // __once
data.ModifierSelf      // __self
data.ModifierOutside   // __outside
data.ModifierWindow    // __window

// Duration/threshold helpers
data.Duration(500 * time.Millisecond)  // __500ms
data.Threshold(0.5)                     // __threshold_0.5
```

## Complete Example

```go
package views

import (
    "net/http"

    . "maragu.dev/gomponents"
    . "maragu.dev/gomponents/html"
    ghttp "maragu.dev/gomponents/http"
    ds "maragu.dev/gomponents-datastar"
)

func CounterPage() Node {
    return HTML5(HTML5Props{
        Title:    "Counter",
        Language: "en",
        Head: []Node{
            Script(
                Type("module"),
                Src("https://cdn.jsdelivr.net/gh/starfederation/[email protected]/bundles/datastar.js"),
            ),
        },
        Body: []Node{
            Div(
                data.Signals(map[string]any{"count": 0}),

                H1(data.Text("'Count: ' + $count")),

                Button(
                    data.On("click", "$count++"),
                    Text("Increment"),
                ),

                Button(
                    data.On("click", "$count--"),
                    Text("Decrement"),
                ),

                Button(
                    data.On("click", "@post('/api/save')"),
                    Text("Save to Server"),
                ),
            ),
        },
    })
}

func SearchForm() Node {
    return Form(
        data.Signals(map[string]any{"query": "", "results": []any{}}),
        data.On("submit", "@get('/search?q=' + $query)", data.ModifierPrevent),

        Input(
            Type("text"),
            data.Bind("$query"),
            data.On("input", "@get('/search?q=' + $query)", data.ModifierDebounce, data.Duration(300*time.Millisecond)),
            Placeholder("Search..."),
        ),

        Div(
            ID("results"),
            data.Show("$results.length > 0"),
            data.Text("'Found ' + $results.length + ' results'"),
        ),
    )
}
```

## SSE Handler Pattern

```go
func handleSSE(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")

    flusher, ok := w.(http.Flusher)
    if !ok {
        http.Error(w, "SSE not supported", http.StatusInternalServerError)
        return
    }

    // Patch HTML elements
    fmt.Fprintf(w, "event: datastar-patch-elements\n")
    fmt.Fprintf(w, "data: elements <div id=\"content\">Updated!</div>\n\n")
    flusher.Flush()

    // Update signals
    fmt.Fprintf(w, "event: datastar-patch-signals\n")
    fmt.Fprintf(w, "data: signals {\"count\": 42}\n\n")
    flusher.Flush()
}
```

## Tips

1. **Signal naming:** Use `$` prefix in expressions, not in Go code
2. **Avoid conflicts:** Use `data.Text()` for Datastar text binding, gomponents `Text()` for static content
3. **Modifiers:** Chain multiple modifiers: `data.On("click", "...", data.ModifierPrevent, data.ModifierOnce)`
4. **SSE IDs:** Elements patched via SSE need matching `id` attributes
5. **Morphing:** Datastar preserves form input state during DOM updates by default
