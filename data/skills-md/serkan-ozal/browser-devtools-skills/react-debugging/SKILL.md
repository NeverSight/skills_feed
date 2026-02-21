---
name: react-debugging
description: Debug React applications by inspecting components, props, and the component tree. Use when the user is debugging React apps, wants to inspect component props/state, find which component renders an element, or understand the React component hierarchy.
allowed-tools: Bash(browser-devtools-cli:*)
---

# React Debugging Skill

Debug React applications by inspecting components, props, and the component tree.

## When to Use

This skill activates when:
- User is debugging a React application
- User wants to inspect React component props/state
- User needs to find which component renders an element
- User asks about React DevTools
- User mentions React Fiber or component tree

## Capabilities

### Component Inspection
```bash
browser-devtools-cli react get-component-for-element --selector ".user-card"
browser-devtools-cli --json react get-component-for-element --selector "#root > div"
```

### Element Mapping
```bash
browser-devtools-cli react get-element-for-component --component-name "UserCard"
browser-devtools-cli --json react get-element-for-component --component-name "Button"
```

## Prerequisites

**Important:** React tools work best with:

1. **Persistent Browser Context**: Enable `BROWSER_PERSISTENT_ENABLE=true`
2. **React DevTools Extension**: Manually install in browser profile
   - [Chrome Web Store](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)

Without the extension, tools use best-effort DOM scanning which is less reliable.

## Debugging Workflow

### Find Component for Element

```bash
SESSION="--session-id react-debug"

# Navigate to React app
browser-devtools-cli $SESSION navigation go-to --url "http://localhost:3000"
browser-devtools-cli $SESSION sync wait-for-network-idle

# Find component for a DOM element
browser-devtools-cli $SESSION --json react get-component-for-element \
  --selector ".user-profile-card"

# Cleanup
browser-devtools-cli session delete react-debug
```

### Find Elements for Component

```bash
SESSION="--session-id react-debug"

# Navigate to React app
browser-devtools-cli $SESSION navigation go-to --url "http://localhost:3000"
browser-devtools-cli $SESSION sync wait-for-network-idle

# Find all DOM elements rendered by a component
browser-devtools-cli $SESSION --json react get-element-for-component \
  --component-name "UserCard"

# Cleanup
browser-devtools-cli session delete react-debug
```

## Common Use Cases

### Debugging Props Issues
```bash
# Find component and check its props
browser-devtools-cli --json react get-component-for-element --selector ".broken-component"
```

### Understanding Render Boundaries
```bash
# See what DOM elements a component renders
browser-devtools-cli --json react get-element-for-component --component-name "DataTable"
```

### Identifying Component Names
```bash
# Click on an element to find its component name
browser-devtools-cli --json react get-component-for-element --selector "#unknown-element"
```

### Combined with DOM Inspection
```bash
SESSION="--session-id react-debug"

# Get component info
browser-devtools-cli $SESSION --json react get-component-for-element --selector ".card"

# Also check DOM structure
browser-devtools-cli $SESSION content get-as-html --selector ".card"

# And accessibility
browser-devtools-cli $SESSION a11y take-aria-snapshot --selector ".card"
```

### Combined with Console Inspection
```bash
SESSION="--session-id react-debug"

# Check for React errors in console
browser-devtools-cli $SESSION --json o11y get-console-messages --types error,warn

# Look for component info
browser-devtools-cli $SESSION --json react get-component-for-element --selector ".error-boundary"
```

## Limitations

- **Development builds only**: Best results with React dev mode
- **Component names**: May be minified in production
- **Source info**: Best-effort, depends on source maps
- **State access**: Limited without DevTools extension

## Best Practices

1. **Use persistent context** for React DevTools extension
2. **Install extension manually** in browser profile
3. **Test in development mode** for better component names
4. **Combine with DOM inspection** for full picture
5. **Use console inspection** for runtime state
6. **Check for React warnings** in console messages
