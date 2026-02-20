---
name: tui-testing
description: Comprehensive testing strategies for Bubbletea v2 applications. Covers unit tests, component tests, golden file testing, async operations, external tool integration, and common testing pitfalls.
compatibility: claude
---

# TUI Testing Best Practices

Comprehensive testing strategies for Bubbletea v2 applications, based on the hive diff viewer implementation.

## Testing Strategy Overview

Use a layered approach with different test types for different concerns:

```
Unit Tests          → Pure logic, state transformations
Component Tests     → Update/View behavior with synthetic messages
Golden File Tests   → Visual regression testing of rendered output
Integration Tests   → End-to-end workflows with teatest
```

## Test Organization

### File Structure

Match test files to implementation files:

```
internal/tui/diff/
├── diffviewer.go
├── diffviewer_test.go           # Component behavior tests
├── diffviewer_editor_test.go    # Feature-specific tests
├── filetree.go
├── filetree_test.go
├── lineparse.go
├── lineparse_test.go            # Pure function tests
├── model.go
├── model_test.go
└── testdata/                    # Golden files
    ├── TestFileTreeView_Empty.golden
    ├── TestFileTreeView_SingleFile.golden
    └── TestDiffViewerView_NormalMode.golden
```

**Naming convention:**
- `<component>_test.go` - Main component tests
- `<component>_<feature>_test.go` - Feature-specific tests
- `Test<Component><Method>_<Scenario>` - Test function names
- `Test<Component><Method>_<Scenario>.golden` - Golden file names

## Unit Testing Pure Functions

### Parse/Transform Logic

For functions that transform data without UI state:

```go
func TestParseDiffLines_SimpleDiff(t *testing.T) {
    diff := `--- a/file.go
+++ b/file.go
@@ -1,3 +1,4 @@
 package main
 func main() {
+	fmt.Println("hello")
 }`

    lines, err := ParseDiffLines(diff)
    require.NoError(t, err)
    require.Len(t, lines, 7) // 2 headers + 1 hunk + 4 content lines

    // Test specific line properties
    assert.Equal(t, LineTypeFileHeader, lines[0].Type)
    assert.Equal(t, "--- a/file.go", lines[0].Content)

    assert.Equal(t, LineTypeAdd, lines[5].Type)
    assert.Equal(t, "\tfmt.Println(\"hello\")", lines[5].Content)
    assert.Equal(t, 0, lines[5].OldLineNum) // Not in old file
    assert.Equal(t, 3, lines[5].NewLineNum)
}
```

**Key principles:**
- Use `require.*` for preconditions that must pass
- Use `assert.*` for actual test conditions
- Test edge cases (empty, single item, boundaries)
- Test error conditions

### Edge Cases to Cover

```go
func TestParseDiffLines_EmptyDiff(t *testing.T) {
    lines, err := ParseDiffLines("")
    require.NoError(t, err)
    assert.Empty(t, lines)
}

func TestParseDiffLines_MultipleHunks(t *testing.T) {
    // Test line number tracking across hunks
}

func TestParseDiffLines_WithDeletions(t *testing.T) {
    // Test that deleted lines have NewLineNum = 0
}
```

## Component Testing

### Testing Update Logic

Test state transitions directly:

```go
func TestDiffViewerScrollDown(t *testing.T) {
    file := &gitdiff.File{
        // ... file with 10 lines ...
    }

    m := NewDiffViewer(file)
    loadFileSync(&m, file)  // Helper for async loading
    m.SetSize(80, 8) // Height 8 = 3 header + 5 content

    // Initial position
    assert.Equal(t, 0, m.offset)
    assert.Equal(t, 0, m.cursorLine)

    // Move cursor down
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, 1, m.cursorLine)
    assert.Equal(t, 0, m.offset) // Viewport doesn't scroll yet

    // Move to bottom of viewport (line 4)
    for i := 0; i < 3; i++ {
        m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    }
    assert.Equal(t, 4, m.cursorLine)
    assert.Equal(t, 0, m.offset)

    // One more scroll triggers viewport scroll
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, 5, m.cursorLine)
    assert.Equal(t, 1, m.offset) // Viewport scrolled down
}
```

### Test Helper Pattern

For async operations, create sync helpers:

```go
// loadFileSync executes async loading synchronously for tests
func loadFileSync(m *DiffViewerModel, file *gitdiff.File) {
    cmd := m.SetFile(file)
    if cmd != nil {
        // Execute command to get message
        msg := cmd()
        // Apply message
        *m, _ = m.Update(msg)
    }
}
```

This lets tests control timing without dealing with async complexity.

### Navigation Testing Pattern

```go
func TestFileTreeNavigationDown(t *testing.T) {
    files := []*gitdiff.File{
        {NewName: "file1.go"},
        {NewName: "file2.go"},
        {NewName: "file3.go"},
    }

    m := NewFileTree(files, &config.Config{})
    assert.Equal(t, 0, m.selected)

    // Test down with 'j'
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, 1, m.selected)

    // Test down with arrow key
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: tea.KeyDown}))
    assert.Equal(t, 2, m.selected)

    // Test boundary - can't go past last
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, 2, m.selected) // Still at last item
}
```

**Test both keybindings** when multiple keys do the same thing (vim-style).

## Golden File Testing

### When to Use Golden Files

Golden files are ideal for:
- **Visual regression testing** - Catch unintended rendering changes
- **Complex rendering logic** - Easier than manual string building
- **Layout verification** - Ensure components render correctly at different sizes

### Basic Golden File Test

```go
func TestFileTreeView_SingleFile(t *testing.T) {
    files := []*gitdiff.File{
        {NewName: "main.go"},
    }

    cfg := &config.Config{
        TUI: config.TUIConfig{},
    }

    m := NewFileTree(files, cfg)
    m.SetSize(40, 10)

    output := m.View()

    // Strip ANSI for readable golden files
    golden.RequireEqual(t, []byte(tuitest.StripANSI(output)))
}
```

**Golden file (`testdata/TestFileTreeView_SingleFile.golden`):**
```
 main.go
```

### Selection and Highlighting Tests

For visual modes with highlighting:

```go
func TestDiffViewerView_SingleLineSelection(t *testing.T) {
    file := createTestFile()

    m := NewDiffViewer(file)
    loadFileSync(&m, file)
    m.SetSize(80, 15)

    // Enter visual mode
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'v'}))
    assert.True(t, m.selectionMode)

    output := m.View()

    // Keep ANSI codes to verify highlighting
    golden.RequireEqual(t, []byte(output))
}
```

**Decision point:** Keep ANSI codes for highlighting tests, strip for layout tests.

### Testing Multiple Scenarios

Use table-driven pattern with golden files:

```go
func TestFileTreeView_Icons(t *testing.T) {
    tests := []struct {
        name      string
        iconStyle IconStyle
    }{
        {"ASCII", IconStyleASCII},
        {"NerdFonts", IconStyleNerdFonts},
    }

    files := []*gitdiff.File{
        {NewName: "main.go"},
        {NewName: "README.md"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            m := NewFileTree(files, &config.Config{})
            m.iconStyle = tt.iconStyle
            m.SetSize(40, 10)

            output := m.View()
            golden.RequireEqual(t, []byte(tuitest.StripANSI(output)))
        })
    }
}
```

This generates:
- `testdata/TestFileTreeView_Icons/ASCII.golden`
- `testdata/TestFileTreeView_Icons/NerdFonts.golden`

### Updating Golden Files

```bash
# Update all golden files
go test ./... -update

# Update specific test
go test ./internal/tui/diff -run TestFileTreeView_SingleFile -update
```

## Test Utilities

### Standard Test Helpers

Create shared utilities in `pkg/tuitest`:

```go
// StripANSI removes escape codes and trailing whitespace
func StripANSI(s string) string {
    s = ansi.Strip(s)
    lines := strings.Split(s, "\n")
    var result []string
    for _, line := range lines {
        trimmed := strings.TrimRight(line, " ")
        result = append(result, trimmed)
    }
    return strings.TrimRight(strings.Join(result, "\n"), "\n")
}

// Helper functions for creating messages
func KeyPress(key rune) tea.Msg {
    return tea.KeyPressMsg(tea.Key{Code: key})
}

func KeyDown() tea.Msg {
    return tea.KeyPressMsg(tea.Key{Code: tea.KeyDown})
}

func WindowSize(w, h int) tea.WindowSizeMsg {
    return tea.WindowSizeMsg{Width: w, Height: h}
}
```

### Test Data Builders

For complex test data:

```go
func createTestFile() *gitdiff.File {
    return &gitdiff.File{
        OldName: "test.go",
        NewName: "test.go",
        TextFragments: []*gitdiff.TextFragment{
            {
                OldPosition: 1,
                OldLines:    3,
                NewPosition: 1,
                NewLines:    3,
                Lines: []gitdiff.Line{
                    {Op: gitdiff.OpContext, Line: "package main\n"},
                    {Op: gitdiff.OpDelete, Line: "old line\n"},
                    {Op: gitdiff.OpAdd, Line: "new line\n"},
                },
            },
        },
    }
}

func createMultiHunkFile() *gitdiff.File {
    // ... builder for multi-hunk scenarios
}
```

## Testing Async Operations

### Pattern: Synchronous Execution in Tests

```go
func TestDiffViewerAsyncLoading(t *testing.T) {
    file := createLargeFile()
    m := NewDiffViewer(file)

    // SetFile returns a command
    cmd := m.SetFile(file)
    require.NotNil(t, cmd)

    // Execute synchronously
    msg := cmd()
    m, _ = m.Update(msg)

    // Verify content loaded
    assert.NotEmpty(t, m.content)
    assert.False(t, m.loading)
}
```

### Testing Loading States

```go
func TestDiffViewerLoadingState(t *testing.T) {
    m := NewDiffViewer(nil)

    // Before loading
    assert.False(t, m.loading)
    assert.Empty(t, m.content)

    // Initiate load (but don't execute command)
    file := createTestFile()
    cmd := m.SetFile(file)
    assert.NotNil(t, cmd)
    // Note: loading state is set when command executes,
    // not when it's created

    // After load completes
    msg := cmd()
    m, _ = m.Update(msg)
    assert.False(t, m.loading)
    assert.NotEmpty(t, m.content)
}
```

## Testing External Tool Integration

### Delta/Syntax Highlighting

```go
func TestDeltaIntegration(t *testing.T) {
    // Skip if delta not available
    if err := CheckDeltaAvailable(); err != nil {
        t.Skip("delta not available")
    }

    diff := "--- a/file.go\n+++ b/file.go\n@@ -1 +1 @@\n-old\n+new\n"

    // Test with delta enabled
    highlighted, _ := ApplyDelta(diff)
    assert.NotEqual(t, diff, highlighted)
    assert.Contains(t, highlighted, "\x1b[") // Contains ANSI codes

    // Test without delta
    plain, _ := generateDiffContent(nil, false)
    assert.NotContains(t, plain, "\x1b[")
}
```

### Mock External Dependencies

For tests that shouldn't depend on external tools:

```go
func TestDiffViewerWithoutDelta(t *testing.T) {
    // Force delta unavailable
    m := NewDiffViewer(createTestFile())
    m.deltaAvailable = false

    cmd := m.SetFile(createTestFile())
    msg := cmd()
    m, _ = m.Update(msg)

    // Should still work, just without highlighting
    assert.NotEmpty(t, m.content)
}
```

## Editor Integration Testing

### Testing Editor Launch

```go
func TestOpenInEditor(t *testing.T) {
    // Set test editor
    oldEditor := os.Getenv("EDITOR")
    defer os.Setenv("EDITOR", oldEditor)
    os.Setenv("EDITOR", "echo")

    m := NewDiffViewer(createTestFile())
    loadFileSync(&m, createTestFile())

    // Get line number to open
    lineNum := 5

    // Open editor command
    cmd := m.openInEditor("/tmp/test.go", lineNum)
    msg := cmd()

    // Should receive editor finished message
    if finishMsg, ok := msg.(editorFinishedMsg); ok {
        assert.NoError(t, finishMsg.err)
    }
}
```

**Note:** Use `echo` or similar non-interactive command for testing.

## Component Boundary Testing

### File Tree State

```go
func TestFileTreeCollapse(t *testing.T) {
    files := []*gitdiff.File{
        {NewName: "src/main.go"},
        {NewName: "src/util.go"},
    }

    m := NewFileTree(files, &config.Config{})
    m.SetSize(40, 20)

    // Should start hierarchical and expanded
    assert.True(t, m.hierarchical)
    assert.NotEmpty(t, m.tree)
    assert.False(t, m.tree[0].Collapsed)

    // Collapse first directory
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: tea.KeyLeft}))

    // Directory should be collapsed
    assert.True(t, m.tree[0].Collapsed)

    // Selection should stay valid
    assert.GreaterOrEqual(t, m.selected, 0)
    assert.Less(t, m.selected, len(m.tree))
}
```

## Integration Testing Patterns

### End-to-End Workflows

```go
func TestDiffReviewWorkflow(t *testing.T) {
    files := []*gitdiff.File{
        {NewName: "file1.go"},
        {NewName: "file2.go"},
    }

    m := New(files, &config.Config{})
    m.SetSize(120, 40)

    // 1. Start in file tree
    assert.Equal(t, FocusFileTree, m.focused)

    // 2. Navigate to second file
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, 1, m.fileTree.selected)

    // 3. Switch to diff viewer
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: tea.KeyTab}))
    assert.Equal(t, FocusDiffViewer, m.focused)

    // 4. Scroll in diff viewer
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, 1, m.diffViewer.cursorLine)

    // 5. Open help
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: '?'}))
    assert.True(t, m.showHelp)

    // 6. Close help
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: '?'}))
    assert.False(t, m.showHelp)
}
```

## Common Testing Pitfalls

### ❌ Don't Test Implementation Details

```go
// BAD: Testing internal state that could change
func TestDiffViewerInternals(t *testing.T) {
    m := NewDiffViewer(file)
    assert.NotNil(t, m.cache) // Implementation detail!
}

// GOOD: Test observable behavior
func TestDiffViewerCaching(t *testing.T) {
    m := NewDiffViewer(file)

    // First load
    cmd1 := m.SetFile(file)
    msg1 := cmd1()
    m, _ = m.Update(msg1)
    content1 := m.content

    // Second load of same file
    cmd2 := m.SetFile(file)
    msg2 := cmd2()
    m, _ = m.Update(msg2)
    content2 := m.content

    // Should get same content (implying cache worked)
    assert.Equal(t, content1, content2)
}
```

### ❌ Don't Ignore Dimensions

```go
// BAD: Testing without setting size
func TestScrolling(t *testing.T) {
    m := NewDiffViewer(file)
    // m.height is 0, viewport calculations will break!
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
}

// GOOD: Always set size before testing
func TestScrolling(t *testing.T) {
    m := NewDiffViewer(file)
    m.SetSize(80, 40) // Realistic dimensions
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
}
```

### ❌ Don't Skip Boundaries

```go
// GOOD: Test edge cases
func TestScrollBoundaries(t *testing.T) {
    // Test scroll up at top
    m.offset = 0
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'k'}))
    assert.Equal(t, 0, m.offset) // Shouldn't go negative

    // Test scroll down at bottom
    m.offset = len(m.lines) - m.contentHeight()
    m, _ = m.Update(tea.KeyPressMsg(tea.Key{Code: 'j'}))
    assert.Equal(t, len(m.lines)-m.contentHeight(), m.offset)
}
```

## Test Coverage Goals

Aim for:
- **Unit tests:** 100% for pure functions (parsers, transformers)
- **Component tests:** 80%+ for Update logic (state transitions, navigation)
- **Golden files:** Key scenarios for each component (normal, edge cases, modes)
- **Integration tests:** Critical workflows only (don't test every combination)

## Running Tests

```bash
# All tests
mise run test

# Watch specific tasks
mise watch test

# Specific package
go test ./internal/tui/diff

# Specific test
go test ./internal/tui/diff -run TestDiffViewerScrollDown

# With coverage
mise run coverage

# Update golden files
go test ./... -update

# Verbose output
go test ./internal/tui/diff -v
```

## Summary

1. **Layer your tests** - Unit for logic, component for behavior, golden for visuals
2. **Test observable behavior** - Not implementation details
3. **Use golden files** for visual regression testing
4. **Create sync helpers** for async operations in tests
5. **Test boundaries** - Empty, single, full, overflows
6. **Set realistic dimensions** - Always call SetSize before testing
7. **Use test utilities** - StripANSI, KeyPress helpers, data builders
8. **Test both keybindings** when multiple keys do the same thing
9. **Skip gracefully** when external tools unavailable
10. **Focus integration tests** on critical workflows, not every combination
