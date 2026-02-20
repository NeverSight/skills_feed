---
name: tui-component-design
description: Best practices for building maintainable, testable TUI components using Bubbletea v2 and the Charm ecosystem. Covers component organization, state management, async operations, visual modes, and common pitfalls.
compatibility: claude
---

# TUI Component Design Patterns

Best practices for building maintainable, testable TUI components using Bubbletea v2 and the Charm ecosystem, based on the hive diff viewer implementation.

## Component Organization

### Single Responsibility Per File

Each component should be in its own file with clear boundaries:

```
internal/tui/diff/
├── model.go           # Top-level compositor that orchestrates sub-components
├── diffviewer.go      # Diff content display with scrolling and selection
├── filetree.go        # File navigation tree with expand/collapse
├── lineparse.go       # Pure function utilities for parsing diff lines
├── delta.go           # External tool integration (syntax highlighting)
└── utils.go           # Shared utilities
```

**Key principle:** Each file should represent ONE component with its own Model, Update, and View methods.

### Component Hierarchy Pattern

For complex UIs, use a compositor pattern:

```go
// Top-level Model composes sub-components
type Model struct {
    fileTree      FileTreeModel      // Left panel
    diffViewer    DiffViewerModel    // Right panel
    focused       FocusedPanel       // Which component has focus
    helpDialog    *components.HelpDialog  // Modal overlay
    showHelp      bool               // Dialog visibility state
}

// Update delegates to focused component
func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    switch m.focused {
    case FocusFileTree:
        m.fileTree, cmd = m.fileTree.Update(msg)
    case FocusDiffViewer:
        m.diffViewer, cmd = m.diffViewer.Update(msg)
    }
    return m, cmd
}
```

**Benefits:**
- Each sub-component is independently testable
- Clear ownership of state and behavior
- Easy to reason about message flow

## Component Structure

### Standard Component Template

```go
// 1. Model struct with all state
type ComponentModel struct {
    // Data
    items []Item

    // UI State
    selected int
    offset   int
    width    int
    height   int

    // Feature flags
    iconStyle IconStyle
    expanded  bool
}

// 2. Constructor with dependencies
func NewComponent(data []Item, cfg *config.Config) ComponentModel {
    return ComponentModel{
        items:     data,
        selected:  0,
        iconStyle: determineIconStyle(cfg),
    }
}

// 3. Update handles messages
func (m ComponentModel) Update(msg tea.Msg) (ComponentModel, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyPressMsg:
        return m.handleKeyPress(msg)
    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height
    }
    return m, nil
}

// 4. View renders output
func (m ComponentModel) View() string {
    return m.render()
}

// 5. Helper methods for complex logic
func (m ComponentModel) render() string {
    // Rendering logic here
}
```

## State Management

### Avoid Hidden State

**Bad:**
```go
// State hidden in closures or package variables
var currentSelection int

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    currentSelection++ // Modifying hidden state
}
```

**Good:**
```go
// All state explicit in model
type Model struct {
    currentSelection int
}

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    m.currentSelection++ // Clear, traceable state change
    return m, nil
}
```

### Separate UI State from Data

```go
type DiffViewerModel struct {
    // Immutable data
    file    *gitdiff.File
    content string
    lines   []string

    // Mutable UI state
    offset         int  // Scroll position
    cursorLine     int  // Current line
    selectionMode  bool // Visual mode active
    selectionStart int  // Selection anchor
}
```

**Benefits:**
- Easy to test rendering at different scroll positions
- Data can be shared/cached without UI state interference
- Clear separation of concerns

## Async Operations and Caching

### Pattern: Command-Based Async with Caching

For expensive operations like syntax highlighting or external tool calls:

```go
type ComponentModel struct {
    cache   map[string]*CachedResult
    loading bool
}

// 1. Initiate async operation, return immediately
func (m *ComponentModel) SetData(data *Data) tea.Cmd {
    filePath := data.Path

    // Check cache first
    if cached, ok := m.cache[filePath]; ok {
        m.content = cached.content
        m.lines = cached.lines
        return nil
    }

    // Mark as loading, start async
    m.loading = true
    return func() tea.Msg {
        content, lines := generateContent(data)
        return contentGeneratedMsg{filePath, content, lines}
    }
}

// 2. Handle completion message
func (m ComponentModel) Update(msg tea.Msg) (ComponentModel, tea.Cmd) {
    switch msg := msg.(type) {
    case contentGeneratedMsg:
        // Cache result
        m.cache[msg.filePath] = &CachedResult{
            content: msg.content,
            lines:   msg.lines,
        }
        // Update display
        m.content = msg.content
        m.lines = msg.lines
        m.loading = false
    }
    return m, nil
}
```

**Key points:**
- Never block the UI thread
- Cache expensive computations
- Show loading state while processing
- Custom messages for async results

### External Tool Integration

For tools like `delta` (syntax highlighting):

```go
// 1. Check availability once at init
func NewDiffViewer(file *gitdiff.File) DiffViewerModel {
    deltaAvailable := CheckDeltaAvailable() == nil
    return DiffViewerModel{
        deltaAvailable: deltaAvailable,
    }
}

// 2. Separate pure function for testability
func generateDiffContent(file *gitdiff.File, deltaAvailable bool) (string, []string) {
    diff := buildUnifiedDiff(file)

    if !deltaAvailable {
        return diff, strings.Split(diff, "\n")
    }

    // Apply syntax highlighting
    return applyDelta(diff)
}

// 3. Make it async with proper error handling
func (m *ComponentModel) loadContent(file *gitdiff.File) tea.Cmd {
    return func() tea.Msg {
        content, lines := generateDiffContent(file, m.deltaAvailable)
        return contentReadyMsg{content, lines}
    }
}
```

## Visual Modes and Complex Interactions

### Mode-Based Keybindings

For vim-style interfaces with normal/visual modes:

```go
type Model struct {
    mode          Mode  // Normal, Visual, Insert
    selectionMode bool  // Visual mode active
}

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyPressMsg:
        // Handle mode transitions first
        if msg.Code == 'v' && !m.selectionMode {
            m.selectionMode = true
            m.selectionStart = m.cursorLine
            return m, nil
        }

        if msg.Code == tea.KeyEscape && m.selectionMode {
            m.selectionMode = false
            return m, nil
        }

        // Handle mode-specific behavior
        if m.selectionMode {
            return m.handleVisualMode(msg)
        }
        return m.handleNormalMode(msg)
    }
    return m, nil
}
```

### Selection State Management

For visual selection (highlighting lines):

```go
type Model struct {
    selectionMode  bool
    selectionStart int  // Anchor point
    cursorLine     int  // Active end
}

// Helper to get normalized selection range
func (m Model) SelectionRange() (start, end int, active bool) {
    if !m.selectionMode {
        return 0, 0, false
    }

    start = m.selectionStart
    end = m.cursorLine
    if start > end {
        start, end = end, start
    }
    return start, end, true
}

// Use in rendering
func (m Model) View() string {
    start, end, active := m.SelectionRange()

    for i, line := range m.lines {
        if active && i >= start && i <= end {
            line = highlightStyle.Render(line)
        }
        // ... render line
    }
}
```

## Scroll Management

### Viewport Pattern

For scrollable content with fixed dimensions:

```go
type Model struct {
    lines   []string
    offset  int  // Top visible line
    height  int  // Viewport height
}

// Calculate visible range
func (m Model) visibleLines() []string {
    start := m.offset
    end := min(m.offset + m.contentHeight(), len(m.lines))
    return m.lines[start:end]
}

// Content height (excluding fixed UI elements)
func (m Model) contentHeight() int {
    return m.height - headerHeight - footerHeight
}

// Scroll with cursor tracking
func (m Model) scrollDown() Model {
    // Move cursor first
    if m.cursorLine < len(m.lines)-1 {
        m.cursorLine++
    }

    // Adjust viewport if cursor moved out of view
    visibleBottom := m.offset + m.contentHeight() - 1
    if m.cursorLine > visibleBottom {
        m.offset++
    }

    return m
}
```

**Key principle:** Cursor moves first, viewport follows to keep cursor visible.

## Editor Integration

### Opening External Editors

Pattern for jumping to specific line in editor:

```go
func (m Model) openInEditor(filePath string, lineNum int) tea.Cmd {
    return func() tea.Msg {
        editor := os.Getenv("EDITOR")
        if editor == "" {
            editor = "vim"
        }

        // Format: editor +line file
        arg := fmt.Sprintf("+%d", lineNum)
        cmd := exec.Command(editor, arg, filePath)

        // Important: Connect to terminal for interactive editors
        cmd.Stdin = os.Stdin
        cmd.Stdout = os.Stdout
        cmd.Stderr = os.Stderr

        err := cmd.Run()
        return editorFinishedMsg{err: err}
    }
}
```

**Critical:** For vim/interactive editors, you must connect stdin/stdout/stderr or the editor won't work properly.

## Component Communication

### Message-Based Coordination

```go
// Custom messages for component coordination
type (
    fileSelectedMsg struct {
        file *gitdiff.File
    }

    diffLoadedMsg struct {
        content string
    }
)

// Parent handles coordination
func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    switch msg := msg.(type) {
    case fileSelectedMsg:
        // FileTree selected a file, tell DiffViewer
        return m, m.diffViewer.LoadFile(msg.file)
    }

    // Delegate to children
    var cmd tea.Cmd
    m.fileTree, cmd = m.fileTree.Update(msg)
    return m, cmd
}
```

### Focus Management

```go
type FocusedPanel int

const (
    FocusFileTree FocusedPanel = iota
    FocusDiffViewer
)

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    if msg, ok := msg.(tea.KeyPressMsg); ok && msg.Code == tea.KeyTab {
        // Switch focus
        m.focused = (m.focused + 1) % 2
        return m, nil
    }

    // Only focused component handles input
    switch m.focused {
    case FocusFileTree:
        m.fileTree, cmd = m.fileTree.Update(msg)
    case FocusDiffViewer:
        m.diffViewer, cmd = m.diffViewer.Update(msg)
    }
    return m, cmd
}
```

## Helper Modal Pattern

For overlays like help dialogs:

```go
type Model struct {
    helpDialog *components.HelpDialog
    showHelp   bool
}

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    // Help dialog intercepts input when visible
    if m.showHelp {
        if msg, ok := msg.(tea.KeyPressMsg); ok && msg.Code == '?' {
            m.showHelp = false
            return m, nil
        }
        // Help dialog handles all input
        *m.helpDialog, cmd = m.helpDialog.Update(msg)
        return m, cmd
    }

    // Toggle help
    if msg, ok := msg.(tea.KeyPressMsg); ok && msg.Code == '?' {
        m.showHelp = true
        return m, nil
    }

    // Normal input handling
    // ...
}

func (m Model) View() string {
    view := m.renderNormal()

    if m.showHelp {
        // Overlay help on top
        return m.helpDialog.View(view)
    }

    return view
}
```

## Common Pitfalls

### ❌ Modifying State Outside Update

```go
// BAD: State modified in View
func (m Model) View() string {
    m.offset++ // NEVER modify state in View!
    return m.render()
}
```

View must be pure - no side effects!

### ❌ Blocking Operations in Update

```go
// BAD: Blocking I/O in Update
func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    content := os.ReadFile("large-file.txt") // BLOCKS UI!
    m.content = string(content)
    return m, nil
}
```

Use commands for I/O.

### ❌ Complex Logic in Update

```go
// BAD: 200 lines of logic in Update
func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyPressMsg:
        // ... 200 lines of key handling ...
    }
}
```

Extract to helper methods:

```go
func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyPressMsg:
        return m.handleKeyPress(msg)
    }
}

func (m Model) handleKeyPress(msg tea.KeyPressMsg) (Model, tea.Cmd) {
    // Clear logic here
}
```

## Summary

1. **One component per file** with clear boundaries
2. **Compositor pattern** for complex UIs (parent coordinates, children handle specifics)
3. **All state in Model** - no hidden variables
4. **Commands for async** - never block Update
5. **Cache expensive operations** - external tools, rendering
6. **Mode-based behavior** for complex interactions (vim-style)
7. **Focus management** for multi-panel UIs
8. **Extract helper methods** - keep Update readable
9. **Pure View** - no side effects, deterministic output
10. **Message-based coordination** - components communicate via messages
