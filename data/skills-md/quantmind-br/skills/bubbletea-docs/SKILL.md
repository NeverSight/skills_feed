---
name: bubbletea-docs
description: |
  Bubble Tea is a Go framework for building elegant terminal user interfaces (TUIs).
  Use when building CLI applications with interactive menus, forms, lists, tables, or any terminal UI.
  Based on The Elm Architecture (Model-View-Update). Key features: keyboard/mouse input, responsive layouts, 
  async commands, Bubbles components (spinner, list, table, viewport, textinput, progress).
  Includes Lip Gloss for styling and Huh for forms.
compatibility: Requires Go 1.18+. Works with github.com/charmbracelet/bubbles, github.com/charmbracelet/lipgloss, and github.com/charmbracelet/huh.
allowed-tools: Read, Bash, Write, Edit
metadata:
  source: https://github.com/charmbracelet/bubbletea
  version: "v1.3+"
  updated: "2026-01-19"
---

# Bubble Tea TUI Framework Skill

## Overview

Bubble Tea is a powerful TUI framework for Go based on The Elm Architecture. Every program has a **Model** (state) and three methods: `Init()` (initial command), `Update()` (handle messages), `View()` (render UI as string).

This skill covers the complete Charm ecosystem:
- **Bubble Tea** - Core TUI framework
- **Bubbles** - Reusable UI components
- **Lip Gloss** - Terminal styling
- **Huh** - Interactive forms

## Installation

```bash
go get github.com/charmbracelet/bubbletea
go get github.com/charmbracelet/bubbles    # UI components
go get github.com/charmbracelet/lipgloss   # Styling
go get github.com/charmbracelet/huh        # Forms
```

## Quick Start

```go
package main

import (
    "fmt"
    "log"
    tea "github.com/charmbracelet/bubbletea"
)

type model struct {
    cursor   int
    choices  []string
    selected map[int]struct{}
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit
        case "up", "k":
            if m.cursor > 0 { m.cursor-- }
        case "down", "j":
            if m.cursor < len(m.choices)-1 { m.cursor++ }
        case "enter", " ":
            if _, ok := m.selected[m.cursor]; ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }
        }
    }
    return m, nil
}

func (m model) View() string {
    s := "Choose:\n\n"
    for i, choice := range m.choices {
        cursor, checked := " ", " "
        if m.cursor == i { cursor = ">" }
        if _, ok := m.selected[i]; ok { checked = "x" }
        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }
    return s + "\nq to quit.\n"
}

func main() {
    p := tea.NewProgram(model{
        choices:  []string{"Option A", "Option B", "Option C"},
        selected: make(map[int]struct{}),
    })
    if _, err := p.Run(); err != nil { log.Fatal(err) }
}
```

## Core Concepts

### Messages and Commands

```go
// Custom messages
type tickMsg time.Time
type dataMsg struct{ data string }
type errMsg struct{ error }

// Command returns a message (runs async)
func fetchData() tea.Msg {
    resp, err := http.Get("https://api.example.com")
    if err != nil { return errMsg{err} }
    defer resp.Body.Close()
    // ... process response
    return dataMsg{data: "result"}
}

// Handle in Update
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case dataMsg:
        m.data = msg.data
    case errMsg:
        m.err = msg.error
    }
    return m, nil
}

// Start command in Init
func (m model) Init() tea.Cmd {
    return fetchData  // Runs async, sends message when done
}
```

### Batch and Sequence Commands

```go
// Parallel execution
return tea.Batch(cmd1, cmd2, cmd3)

// Sequential execution
return tea.Sequence(step1, step2, tea.Quit)
```

### Window Size Handling

```go
type model struct {
    width, height int
    viewport      viewport.Model
    ready         bool
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.width, m.height = msg.Width, msg.Height
        if !m.ready {
            m.viewport = viewport.New(msg.Width, msg.Height-4)
            m.viewport.SetContent(m.content)
            m.ready = true
        } else {
            m.viewport.Width = msg.Width
            m.viewport.Height = msg.Height - 4
        }
    }
    return m, nil
}
```

## Common Patterns

### Program Options

```go
// Fullscreen
p := tea.NewProgram(m, tea.WithAltScreen())

// Mouse support
p := tea.NewProgram(m, tea.WithMouseCellMotion())

// Combined
p := tea.NewProgram(m, tea.WithAltScreen(), tea.WithMouseCellMotion())
```

### Key Bindings with bubbles/key

```go
import "github.com/charmbracelet/bubbles/key"

type keyMap struct {
    Up   key.Binding
    Down key.Binding
    Quit key.Binding
}

var keys = keyMap{
    Up:   key.NewBinding(key.WithKeys("up", "k"), key.WithHelp("↑/k", "up")),
    Down: key.NewBinding(key.WithKeys("down", "j"), key.WithHelp("↓/j", "down")),
    Quit: key.NewBinding(key.WithKeys("q", "ctrl+c"), key.WithHelp("q", "quit")),
}

// In Update
case tea.KeyMsg:
    switch {
    case key.Matches(msg, keys.Up):
        m.cursor--
    case key.Matches(msg, keys.Quit):
        return m, tea.Quit
    }
```

### Multiple Views

```go
type model struct {
    state int  // 0=menu, 1=detail
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch m.state {
    case 0: return m.updateMenu(msg)
    case 1: return m.updateDetail(msg)
    }
    return m, nil
}

func (m model) View() string {
    switch m.state {
    case 0: return m.menuView()
    case 1: return m.detailView()
    }
    return ""
}
```

---

## Bubbles Components

### Component Quick Reference

| Component | Import | Init | Key Method |
|-----------|--------|------|------------|
| Spinner | `bubbles/spinner` | `spinner.New()` | `.Tick` in Init |
| TextInput | `bubbles/textinput` | `textinput.New()` | `.Focus()`, `.Value()` |
| TextArea | `bubbles/textarea` | `textarea.New()` | `.Focus()`, `.Value()` |
| List | `bubbles/list` | `list.New(items, delegate, w, h)` | `.SelectedItem()` |
| Table | `bubbles/table` | `table.New(opts...)` | `.SelectedRow()` |
| Viewport | `bubbles/viewport` | `viewport.New(w, h)` | `.SetContent()`, `.ScrollUp()`, `.ScrollDown()` |
| Progress | `bubbles/progress` | `progress.New()` | `.SetPercent()` |
| Help | `bubbles/help` | `help.New()` | `.View(keyMap)` |
| FilePicker | `bubbles/filepicker` | `filepicker.New()` | `.DidSelectFile()` |
| Timer | `bubbles/timer` | `timer.New(duration)` | `.Toggle()` |
| Stopwatch | `bubbles/stopwatch` | `stopwatch.New()` | `.Elapsed()` |

### Focus Management (Multiple Inputs)

```go
type model struct {
    inputs     []textinput.Model
    focusIndex int
}

func (m *model) nextInput() tea.Cmd {
    m.inputs[m.focusIndex].Blur()
    m.focusIndex = (m.focusIndex + 1) % len(m.inputs)
    return m.inputs[m.focusIndex].Focus()
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            return m, m.nextInput()
        }
    }
    // Update all inputs
    cmds := make([]tea.Cmd, len(m.inputs))
    for i := range m.inputs {
        m.inputs[i], cmds[i] = m.inputs[i].Update(msg)
    }
    return m, tea.Batch(cmds...)
}
```

### Component Composition

```go
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmds []tea.Cmd
    var cmd tea.Cmd

    // Update all components and collect commands
    m.spinner, cmd = m.spinner.Update(msg)
    cmds = append(cmds, cmd)

    m.textInput, cmd = m.textInput.Update(msg)
    cmds = append(cmds, cmd)

    m.viewport, cmd = m.viewport.Update(msg)
    cmds = append(cmds, cmd)

    return m, tea.Batch(cmds...)
}
```

### Spinner Example

```go
s := spinner.New()
s.Spinner = spinner.Dot  // Line, Dot, MiniDot, Jump, Pulse, Points, Globe, Moon, Monkey
s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))

// In Init(): return m.spinner.Tick
// In Update(): handle spinner.TickMsg
```

### List with Custom Items

```go
type item struct{ title, desc string }

func (i item) Title() string       { return i.title }
func (i item) Description() string { return i.desc }
func (i item) FilterValue() string { return i.title }  // Required for filtering

items := []list.Item{item{"One", "Description"}}
l := list.New(items, list.NewDefaultDelegate(), 30, 10)
l.Title = "Select Item"
```

### Table

```go
columns := []table.Column{
    {Title: "ID", Width: 10},
    {Title: "Name", Width: 20},
}
rows := []table.Row{
    {"1", "Alice"},
    {"2", "Bob"},
}
t := table.New(
    table.WithColumns(columns),
    table.WithRows(rows),
    table.WithFocused(true),
    table.WithHeight(7),
)
```

---

## Lip Gloss Styling

### Basic Styling

```go
import "github.com/charmbracelet/lipgloss"

var style = lipgloss.NewStyle().
    Bold(true).
    Foreground(lipgloss.Color("205")).
    Background(lipgloss.Color("#7D56F4")).
    Border(lipgloss.RoundedBorder()).
    Padding(1, 2)

output := style.Render("Hello, World!")
```

### Colors

```go
// Hex colors
lipgloss.Color("#FF00FF")

// ANSI 256 colors
lipgloss.Color("205")

// Adaptive colors (auto light/dark background)
lipgloss.AdaptiveColor{Light: "#000000", Dark: "#FFFFFF"}

// Complete color profiles
lipgloss.CompleteColor{
    TrueColor: "#FF00FF",
    ANSI256:   "205",
    ANSI:      "5",
}
```

### Layout Composition

```go
// Horizontal layout
left := lipgloss.NewStyle().Width(20).Render("Left")
right := lipgloss.NewStyle().Width(20).Render("Right")
row := lipgloss.JoinHorizontal(lipgloss.Top, left, right)

// Vertical layout
header := "Header"
body := "Body content"
footer := "Footer"
page := lipgloss.JoinVertical(lipgloss.Left, header, body, footer)

// Center content in box
centered := lipgloss.Place(80, 24, lipgloss.Center, lipgloss.Center, content)
```

### Frame Size for Calculations

```go
// Account for padding/border/margin in calculations
h, v := docStyle.GetFrameSize()
m.list.SetSize(m.width-h, m.height-v)

// Dynamic content height
headerH := lipgloss.Height(m.header())
footerH := lipgloss.Height(m.footer())
m.viewport.Height = m.height - headerH - footerH
```

### Border Styles

```go
lipgloss.NormalBorder()   // Standard box
lipgloss.RoundedBorder()  // Rounded corners
lipgloss.ThickBorder()    // Thick lines
lipgloss.DoubleBorder()   // Double lines
lipgloss.HiddenBorder()   // Invisible (for spacing)
```

---

## Huh Forms

### Quick Start

```go
import "github.com/charmbracelet/huh"

var name string
var confirmed bool

form := huh.NewForm(
    huh.NewGroup(
        huh.NewInput().
            Title("What's your name?").
            Value(&name),
        
        huh.NewConfirm().
            Title("Ready to proceed?").
            Value(&confirmed),
    ),
)

err := form.Run()
if err != nil {
    if err == huh.ErrUserAborted {
        fmt.Println("Cancelled")
        return
    }
    log.Fatal(err)
}
```

### Field Types (GENERIC TYPES REQUIRED)

```go
// Input - single line text
huh.NewInput().Title("Name").Value(&name)

// Text - multi-line
huh.NewText().Title("Bio").Lines(5).Value(&bio)

// Select - MUST specify type
huh.NewSelect[string]().
    Title("Choose").
    Options(
        huh.NewOption("Option A", "a"),
        huh.NewOption("Option B", "b"),
    ).
    Value(&choice)

// MultiSelect - MUST specify type  
huh.NewMultiSelect[string]().
    Title("Choose many").
    Options(huh.NewOptions("A", "B", "C")...).
    Limit(2).
    Value(&choices)

// Confirm
huh.NewConfirm().
    Title("Sure?").
    Affirmative("Yes").
    Negative("No").
    Value(&confirmed)

// FilePicker
huh.NewFilePicker().
    Title("Select file").
    AllowedTypes([]string{".go", ".md"}).
    Value(&filepath)
```

### Validation

```go
huh.NewInput().
    Title("Email").
    Value(&email).
    Validate(func(s string) error {
        if !strings.Contains(s, "@") {
            return errors.New("invalid email")
        }
        return nil
    })
```

### Dynamic Forms (OptionsFunc/TitleFunc)

```go
var country string
var state string

huh.NewSelect[string]().
    Value(&state).
    TitleFunc(func() string {
        if country == "Canada" { return "Province" }
        return "State"
    }, &country).  // Recompute when country changes
    OptionsFunc(func() []huh.Option[string] {
        return huh.NewOptions(getStatesFor(country)...)
    }, &country)
```

### Bubble Tea Integration

```go
type Model struct {
    form *huh.Form
}

func (m Model) Init() tea.Cmd {
    return m.form.Init()
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    form, cmd := m.form.Update(msg)
    if f, ok := form.(*huh.Form); ok {
        m.form = f
    }
    
    if m.form.State == huh.StateCompleted {
        // Form completed - access values
        name := m.form.GetString("name")
        return m, tea.Quit
    }
    
    return m, cmd
}

func (m Model) View() string {
    if m.form.State == huh.StateCompleted {
        return "Done!"
    }
    return m.form.View()
}
```

### Themes

```go
form.WithTheme(huh.ThemeCharm())      // Default pink/purple
form.WithTheme(huh.ThemeDracula())    // Dark purple/pink
form.WithTheme(huh.ThemeCatppuccin()) // Pastel
form.WithTheme(huh.ThemeBase16())     // Muted
form.WithTheme(huh.ThemeBase())       // Minimal
```

### Spinner for Loading

```go
import "github.com/charmbracelet/huh/spinner"

err := spinner.New().
    Title("Processing...").
    Action(func() {
        time.Sleep(2 * time.Second)
        processData()
    }).
    Run()
```

---

## Common Gotchas

### Bubble Tea Core

1. **Blocking in Update/View**: Never block. Use commands for I/O:
   ```go
   // BAD
   time.Sleep(time.Second)  // Blocks event loop!
   
   // GOOD
   return m, func() tea.Msg {
       time.Sleep(time.Second)
       return doneMsg{}
   }
   ```

2. **Goroutines modifying model**: Race condition! Use commands instead:
   ```go
   // BAD
   go func() { m.data = fetch() }()  // Race!
   
   // GOOD
   return m, func() tea.Msg { return dataMsg{fetch()} }
   ```

3. **Viewport before WindowSizeMsg**: Initialize after receiving dimensions:
   ```go
   if !m.ready {
       m.viewport = viewport.New(msg.Width, msg.Height)
       m.ready = true
   }
   ```

4. **Using receiver methods incorrectly**: Only use `func (m *model)` for internal helpers. Model interface methods must use value receivers `func (m model)`.

5. **Startup commands via Init**: Don't use `tea.EnterAltScreen` in Init. Use `tea.WithAltScreen()` option instead.

6. **Messages not in order**: `tea.Batch` results arrive in ANY order. Use `tea.Sequence` when order matters.

### Bubbles Components

7. **Spinner not animating**: Must return `m.spinner.Tick` from `Init()` and handle `spinner.TickMsg` in Update.

8. **TextInput not accepting input**: Must call `.Focus()` before input accepts keystrokes.

9. **Component updates not reflected**: Always reassign after Update:
   ```go
   m.spinner, cmd = m.spinner.Update(msg)  // Must reassign!
   ```

10. **Multiple components losing commands**: Use `tea.Batch(cmds...)` to combine all commands.

11. **List items not filtering**: Must implement `FilterValue() string` on items.

12. **Table not responding**: Must set `table.WithFocused(true)` or call `t.Focus()`.

### Lip Gloss

13. **Style method has no effect**: Styles are immutable, must reassign:
    ```go
    // BAD
    style.Bold(true)  // Result discarded!
    
    // GOOD
    style = style.Bold(true)
    ```

14. **Alignment not working**: Requires explicit Width:
    ```go
    style := lipgloss.NewStyle().Width(40).Align(lipgloss.Center)
    ```

15. **Width calculation wrong**: Use `lipgloss.Width()` not `len()` for unicode.

16. **Layout arithmetic errors**: Use `style.GetFrameSize()` to account for padding/border/margin.

### Huh Forms

17. **Generic types required**: `Select` and `MultiSelect` MUST have type parameter:
    ```go
    // BAD - won't compile
    huh.NewSelect()
    
    // GOOD
    huh.NewSelect[string]()
    ```

18. **Value takes pointer**: Always pass pointer: `.Value(&myVar)` not `.Value(myVar)`.

19. **OptionsFunc not updating**: Must pass binding variable:
    ```go
    .OptionsFunc(fn, &country)  // Recomputes when country changes
    ```

20. **Don't use Placeholder() in huh forms**: Causes rendering bugs. Put examples in Description instead:
    ```go
    // BAD
    huh.NewInput().Placeholder("example@email.com")
    
    // GOOD
    huh.NewInput().Description("e.g. example@email.com")
    ```

21. **Loop variable closure capture**: Capture explicitly in loops:
    ```go
    for _, name := range items {
        currentName := name  // Capture!
        huh.NewInput().Value(&configs[currentName].Field)
    }
    ```

22. **Don't intercept Enter before form**: Let huh handle Enter for navigation.

---

## Debugging

```go
// Log to file (stdout is the TUI)
if os.Getenv("DEBUG") != "" {
    f, _ := tea.LogToFile("debug.log", "app")
    defer f.Close()
}
log.Println("Debug message")
```

## Best Practices

1. **Keep Update/View fast** - The event loop blocks on these
2. **Use tea.Cmd for all I/O** - HTTP, file, database operations
3. **Use tea.Batch for parallel** - Multiple independent commands
4. **Use tea.Sequence for ordered** - Commands that must run in order
5. **Store window dimensions** - Handle tea.WindowSizeMsg, update components
6. **Initialize viewport after WindowSizeMsg** - Dimensions aren't available at start
7. **Use value receivers** - `func (m model) Update` not `func (m *model) Update`
8. **Define styles as package variables** - Reuse instead of creating in loops
9. **Use AdaptiveColor** - For light/dark terminal support
10. **Handle ErrUserAborted** - Graceful Ctrl+C handling in huh forms

## Additional Resources

- [references/API.md](references/API.md) - Complete API reference
- [references/EXAMPLES.md](references/EXAMPLES.md) - Extended code examples  
- [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - Common errors and solutions

## Essential Imports

```go
import (
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
    "github.com/charmbracelet/lipgloss/table"  // Static tables
    "github.com/charmbracelet/lipgloss/tree"   // Hierarchical data
    "github.com/charmbracelet/bubbles/spinner"
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/bubbles/textarea"
    "github.com/charmbracelet/bubbles/list"
    "github.com/charmbracelet/bubbles/table"   // Interactive tables
    "github.com/charmbracelet/bubbles/viewport"
    "github.com/charmbracelet/bubbles/help"
    "github.com/charmbracelet/bubbles/key"
    "github.com/charmbracelet/bubbles/filepicker"
    "github.com/charmbracelet/bubbles/progress"
    "github.com/charmbracelet/bubbles/timer"
    "github.com/charmbracelet/bubbles/stopwatch"
    "github.com/charmbracelet/huh"
    "github.com/charmbracelet/huh/spinner"
    "github.com/charmbracelet/wish"            // SSH TUI server
    "github.com/lrstanley/bubblezone"          // Mouse zones
)
```

---

## Lip Gloss Tree (Hierarchical Data)

Render tree structures with customizable enumerators:

```go
import "github.com/charmbracelet/lipgloss/tree"

t := tree.Root("Root").
    Child("Child 1").
    Child(
        tree.Root("Child 2").
            Child("Grandchild 1").
            Child("Grandchild 2"),
    ).
    Child("Child 3")

// Custom enumerator
t.Enumerator(tree.RoundedEnumerator)  // ├── └──
t.Enumerator(tree.BulletEnumerator)   // • bullets
t.Enumerator(tree.NumberedEnumerator) // 1. 2. 3.

// Custom styling
t.EnumeratorStyle(lipgloss.NewStyle().Foreground(lipgloss.Color("99")))
t.ItemStyle(lipgloss.NewStyle().Bold(true))

fmt.Println(t)
```

---

## Lip Gloss Table (Static Rendering)

For high-performance static tables (reports, logs). Use `bubbles/table` for interactive selection.

```go
import "github.com/charmbracelet/lipgloss/table"

t := table.New().
    Border(lipgloss.NormalBorder()).
    BorderStyle(lipgloss.NewStyle().Foreground(lipgloss.Color("99"))).
    Headers("NAME", "AGE", "CITY").
    Row("Alice", "30", "NYC").
    Row("Bob", "25", "LA").
    Wrap(true).  // Enable text wrapping
    StyleFunc(func(row, col int) lipgloss.Style {
        if row == table.HeaderRow {
            return lipgloss.NewStyle().Bold(true)
        }
        return lipgloss.NewStyle()
    })

fmt.Println(t)
```

**When to use which table:**
- `lipgloss/table`: Static rendering, reports, logs, non-interactive
- `bubbles/table`: Interactive selection, keyboard navigation, focused rows

---

## Custom Component Pattern (Sub-Model)

Create reusable Bubble Tea components by exposing `Init`, `Update`, `View`:

```go
// counter.go - Reusable component
package counter

import tea "github.com/charmbracelet/bubbletea"

type Model struct {
    Count int
    Min   int
    Max   int
}

func New(min, max int) Model {
    return Model{Min: min, Max: max}
}

func (m Model) Init() tea.Cmd { return nil }

func (m Model) Update(msg tea.Msg) (Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "+", "=":
            if m.Count < m.Max { m.Count++ }
        case "-":
            if m.Count > m.Min { m.Count-- }
        }
    }
    return m, nil
}

func (m Model) View() string {
    return fmt.Sprintf("Count: %d", m.Count)
}

// parent.go - Using the component
type parentModel struct {
    counter counter.Model
}

func (m parentModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    m.counter, cmd = m.counter.Update(msg)
    return m, cmd
}
```

---

## ProgramContext Pattern (Production)

Share global state across components without prop drilling:

```go
// context.go
type ProgramContext struct {
    Config     *Config
    Theme      *Theme
    Width      int
    Height     int
    StartTask  func(Task) tea.Cmd  // Callback for background tasks
}

// model.go
type Model struct {
    ctx       *ProgramContext
    sidebar   sidebar.Model
    main      main.Model
    tasks     map[string]Task
    spinner   spinner.Model
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.ctx.Width = msg.Width
        m.ctx.Height = msg.Height
        // Sync all components
        m.sidebar.SetHeight(msg.Height)
        m.main.SetSize(msg.Width - sidebarWidth, msg.Height)
    }
    return m, nil
}

// Initialize context with task callback
func NewModel(cfg *Config) Model {
    ctx := &ProgramContext{Config: cfg}
    m := Model{ctx: ctx, tasks: make(map[string]Task)}
    
    ctx.StartTask = func(t Task) tea.Cmd {
        m.tasks[t.ID] = t
        return m.spinner.Tick
    }
    
    return m
}
```

---

## Testing with teatest

```go
import (
    "testing"
    "time"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/x/exp/teatest"
)

func TestModel(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))
    
    // Send key presses
    tm.Send(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune{'j'}})
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
    
    // Wait for specific output
    teatest.WaitFor(t, tm.Output(), func(bts []byte) bool {
        return strings.Contains(string(bts), "Selected")
    }, teatest.WithDuration(time.Second))
    
    // Check final state
    tm.Send(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune{'q'}})
    tm.WaitFinished(t, teatest.WithFinalTimeout(time.Second))
    
    final := tm.FinalModel(t).(Model)
    if final.selected != "expected" {
        t.Errorf("expected 'expected', got %q", final.selected)
    }
}
```

---

## SSH Integration with Wish

Serve TUI apps over SSH:

```go
import (
    "github.com/charmbracelet/wish"
    "github.com/charmbracelet/wish/bubbletea"
    "github.com/charmbracelet/ssh"
)

func main() {
    s, err := wish.NewServer(
        wish.WithAddress(":2222"),
        wish.WithHostKeyPath(".ssh/term_info_ed25519"),
        wish.WithMiddleware(
            bubbletea.Middleware(teaHandler),
        ),
    )
    if err != nil { log.Fatal(err) }
    
    log.Println("Starting SSH server on :2222")
    if err := s.ListenAndServe(); err != nil {
        log.Fatal(err)
    }
}

func teaHandler(s ssh.Session) (tea.Model, []tea.ProgramOption) {
    pty, _, _ := s.Pty()
    m := NewModel(pty.Window.Width, pty.Window.Height)
    return m, []tea.ProgramOption{tea.WithAltScreen()}
}
```

---

## Mouse Zones with bubblezone

Define clickable regions without coordinate math:

```go
import zone "github.com/lrstanley/bubblezone"

type model struct {
    zone *zone.Manager
}

func newModel() model {
    return model{zone: zone.New()}
}

func (m model) View() string {
    // Wrap clickable elements
    button1 := m.zone.Mark("btn1", "[Button 1]")
    button2 := m.zone.Mark("btn2", "[Button 2]")
    
    return lipgloss.JoinHorizontal(lipgloss.Top, button1, " ", button2)
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.MouseMsg:
        // Check which zone was clicked
        if m.zone.Get("btn1").InBounds(msg) {
            // Button 1 clicked
        }
        if m.zone.Get("btn2").InBounds(msg) {
            // Button 2 clicked
        }
    }
    return m, nil
}

// Wrap program with zone.NewGlobal() for simpler API
func main() {
    zone.NewGlobal()
    p := tea.NewProgram(newModel(), tea.WithMouseCellMotion())
    p.Run()
}
```
