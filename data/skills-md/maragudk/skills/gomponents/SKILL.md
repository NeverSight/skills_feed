---
name: gomponents
description: Guide for working with gomponents, a pure Go HTML component library. Use this skill when reading or writing gomponents code, or when building HTML views in Go applications.
license: MIT
---

# gomponents

## Overview

gomponents is a pure Go HTML component library that treats HTML elements as composable Go values. Everything is built on the `Node` interface, making HTML construction type-safe and composable.

## When to Use This Skill

Use this skill when:
- Reading or writing gomponents code
- Building server-side HTML views in Go applications
- Creating reusable HTML components in Go

## Core Interface

Everything in gomponents implements the `Node` interface:

```go
type Node interface {
    Render(w io.Writer) error
}
```

## Essential Functions

### Element and Attribute Creation

- `El(name string, children ...Node)` - Create custom HTML elements
- `Attr(name string, value ...string)` - Create custom attributes

Most standard HTML5 elements and attributes are available as functions in the `html` package:
- Elements: `Div()`, `Span()`, `P()`, `A()`, etc.
- Attributes: `Class()`, `ID()`, `Href()`, `Src()`, etc.

**Note:** `nil` Nodes are ignored during rendering, so it's safe to pass nil nodes to elements.

### Text Content

- `Text(string)` - HTML-escaped text content
- `Textf(format string, args...)` - Formatted, escaped text
- `Raw(string)` - Unescaped HTML
- `Rawf(format string, args...)` - Formatted, unescaped content

### Composition

- `Group([]Node)` - Combine multiple nodes
- `Map[T]([]T, func(T) Node)` - Transform slices into node sequences
- `If(condition bool, node Node)` - Conditional rendering
- `Iff(condition bool, func() Node)` - Lazy conditional rendering (deferred evaluation)

## Import Convention

Contrary to common Go idioms, **dot imports are recommended** for gomponents to achieve DSL-like syntax:

```go
import (
    . "maragu.dev/gomponents"
    . "maragu.dev/gomponents/html"
    . "maragu.dev/gomponents/components"
)
```

This allows writing clean, HTML-like code:

```go
Div(Class("container"),
    H1(Text("Hello World")),
    P(Text("Welcome to gomponents")),
)
```

## Package Organization

- `maragu.dev/gomponents` - Core interface and helper functions
- `maragu.dev/gomponents/html` - All HTML5 elements and attributes
- `maragu.dev/gomponents/http` - HTTP helpers for rendering components as responses
- `maragu.dev/gomponents/components` - Higher-level utilities (HTML5 document structure, dynamic classes)

## Common Patterns

### Basic Component

```go
func UserCard(name, email string) Node {
    return Div(Class("user-card"),
        H2(Text(name)),
        P(Text(email)),
    )
}
```

### Conditional Rendering

```go
func Alert(message string, isError bool) Node {
    return Div(
        If(isError, Class("error")),
        If(!isError, Class("info")),
        P(Text(message)),
    )
}
```

Use `If` when the node is always safe to evaluate. Use `Iff` when the node might be nil and shouldn't be evaluated unless the condition is true.

```go
func UserProfile(user *User) Node {
    return Div(
        H1(Text(user.Name)),
        // Use Iff to avoid nil pointer dereference when user.Avatar is nil
        Iff(user.Avatar != nil, func() Node {
            return Img(Src(user.Avatar.URL))
        }),
    )
}
```

### Grouping Without a Parent Element

Use `Group` to group multiple nodes without wrapping them in a parent element:

```go
func FormFields(required bool) Node {
    return Group{
        Label(For("email"), Text("Email")),
        Input(Type("email"), ID("email")),
        If(required, Span(Class("required"), Text("*"))),
    }
}
```

### List Rendering

```go
func TodoList(todos []Todo) Node {
    return Ul(Class("todo-list"),
        Map(todos, func(t Todo) Node {
            return Li(Text(t.Title))
        }),
    )
}
```

### HTML Document

```go
func Page(title string, body Node) Node {
    return HTML5(HTML5Props{
        Title:    title,
        Language: "en",
        Head: []Node{
            Link(Rel("stylesheet"), Href("/styles.css")),
        },
        Body: []Node{body},
    })
}
```

### HTTP Handler

```go
import ghttp "maragu.dev/gomponents/http"

func HomeHandler(w http.ResponseWriter, r *http.Request) (Node, error) {
    return Page("My App",
        Div(Class("container"),
            H1(Text("Hello, World!")),
        ),
    ), nil
}

// In main:
http.HandleFunc("/", ghttp.Adapt(HomeHandler))
```

The `http` package provides:
- `Handler` type - function signature that returns `(Node, error)`
- `Adapt(Handler)` - converts Handler to `http.HandlerFunc`
- Error handling with custom status codes via `StatusCode() int` interface
