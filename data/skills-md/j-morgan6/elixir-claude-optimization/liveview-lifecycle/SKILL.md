---
name: liveview-lifecycle
description: Use when working with LiveView rendering phases and lifecycle. Covers static vs connected rendering, safe assign access, mount initialization, and avoiding KeyError crashes.
---

# LiveView Rendering Lifecycle

## Critical Understanding

**LiveView renders happen in TWO phases:**

1. **Static/Disconnected Render** - Initial HTTP request, server-side HTML
   - No WebSocket connection
   - No live functionality yet
   - `connected?(socket)` returns `false`

2. **Connected Render** - WebSocket established, full LiveView active
   - Live updates work
   - Events are handled
   - `connected?(socket)` returns `true`

## The Problem: Uninitialized Assigns

During static render, socket assigns may not be fully initialized:

```elixir
# ❌ DANGEROUS - Can crash during static render
def render(assigns) do
  user_name = assigns.current_user.name  # KeyError if not set!
  ~H"<p>Hello <%= user_name %></p>"
end
```

**Error:** `KeyError: key :current_user not found`

## The Solution: Defensive Access

Always use safe access patterns:

```elixir
# ✅ SAFE - Works in both render phases
def render(assigns) do
  user_name = Map.get(assigns, :current_user, %{name: "Guest"}).name
  ~H"<p>Hello <%= user_name %></p>"
end

# ✅ BETTER - Initialize in mount
@impl true
def mount(_params, session, socket) do
  socket = assign(socket, :current_user, get_user(session))
  {:ok, socket}
end
```

## Best Practices

### 1. Initialize All Assigns in mount/3

**Always initialize every assign you'll use:**

```elixir
@impl true
def mount(_params, _session, socket) do
  socket =
    socket
    |> assign(:user, nil)
    |> assign(:loading, false)
    |> assign(:data, [])
    |> assign(:error, nil)

  {:ok, socket}
end
```

### 2. Use Map.get for Optional Assigns

**When accessing assigns that might not exist:**

```elixir
# ❌ BAD
defp render_user(socket) do
  socket.assigns.current_user.name
end

# ✅ GOOD
defp render_user(socket) do
  case Map.get(socket.assigns, :current_user) do
    nil -> "Guest"
    user -> user.name
  end
end

# ✅ ALSO GOOD
defp render_user(socket) do
  Map.get(socket.assigns, :current_user, %{name: "Guest"}).name
end
```

### 3. Use Pattern Matching Safely

```elixir
# ❌ BAD - Crashes if not a map with :name
defp format_user(%{name: name}), do: name

# ✅ GOOD - Handles nil case
defp format_user(%{name: name}), do: name
defp format_user(_), do: "Unknown"

# ✅ ALSO GOOD - Check first
defp format_user(user) when is_map(user), do: Map.get(user, :name, "Unknown")
defp format_user(_), do: "Unknown"
```

### 4. Use assigns_to_attributes for Components

```elixir
# Component with dynamic assigns
def card(assigns) do
  ~H"""
  <div class="card" {@rest}>
    <%= render_slot(@inner_block) %>
  </div>
  """
end

# Usage
<.card id="my-card" data-role="admin">
  Content
</.card>
```

## Connected Check

Use `connected?/1` for operations that only work with WebSocket:

```elixir
@impl true
def mount(_params, _session, socket) do
  socket =
    if connected?(socket) do
      # Only run when WebSocket is connected
      Phoenix.PubSub.subscribe(MyApp.PubSub, "updates")
      schedule_refresh()
      socket
    else
      # Static render - skip expensive operations
      socket
    end

  socket = assign(socket, :data, load_initial_data())
  {:ok, socket}
end
```

**Why?** PubSub subscriptions, timers, and live updates only work when connected.

## Handle Params Considerations

`handle_params/3` is called in **both** render phases:

```elixir
@impl true
def handle_params(%{"id" => id}, _uri, socket) do
  # This runs during static AND connected render
  post = Posts.get_post!(id)  # OK - database queries work in both phases

  if connected?(socket) do
    # Only subscribe when connected
    Phoenix.PubSub.subscribe(MyApp.PubSub, "post:#{id}")
  end

  {:noreply, assign(socket, :post, post)}
end
```

## Common Lifecycle Mistakes

### ❌ Mistake 1: Assuming Assigns Exist

```elixir
def render(assigns) do
  ~H"""
  <p>Count: <%= @count %></p>  <!-- Crash if @count not initialized -->
  """
end
```

### ✅ Fix: Initialize in mount

```elixir
@impl true
def mount(_params, _session, socket) do
  {:ok, assign(socket, :count, 0)}
end

def render(assigns) do
  ~H"""
  <p>Count: <%= @count %></p>  <!-- Safe now -->
  """
end
```

### ❌ Mistake 2: Subscribing in Both Phases

```elixir
@impl true
def mount(_params, _session, socket) do
  # BAD - Subscribes during static render (doesn't work)
  Phoenix.PubSub.subscribe(MyApp.PubSub, "topic")
  {:ok, socket}
end
```

### ✅ Fix: Check connected?

```elixir
@impl true
def mount(_params, _session, socket) do
  if connected?(socket) do
    Phoenix.PubSub.subscribe(MyApp.PubSub, "topic")
  end

  {:ok, socket}
end
```

### ❌ Mistake 3: Expensive Operations in Static Render

```elixir
@impl true
def mount(_params, _session, socket) do
  # BAD - Runs expensive query twice (static + connected)
  data = run_expensive_query()
  {:ok, assign(socket, :data, data)}
end
```

### ✅ Fix: Defer to connected phase

```elixir
@impl true
def mount(_params, _session, socket) do
  socket =
    if connected?(socket) do
      # Only run expensive operations when connected
      assign(socket, :data, run_expensive_query())
    else
      # Use placeholder data for static render
      assign(socket, :data, [])
    end

  {:ok, socket}
end
```

## Lifecycle Flow

```
1. HTTP Request arrives
   ↓
2. mount/3 called (connected? = false)
   ↓
3. handle_params/3 called (connected? = false)
   ↓
4. render/1 called (STATIC HTML generated)
   ↓
5. HTML sent to browser
   ↓
6. Browser connects WebSocket
   ↓
7. mount/3 called AGAIN (connected? = true)
   ↓
8. handle_params/3 called AGAIN (connected? = true)
   ↓
9. render/1 called (sent over WebSocket)
   ↓
10. LiveView now active and reactive
```

## Debugging Tips

### Check if LiveView is connected

```elixir
def render(assigns) do
  ~H"""
  <div data-connected={@connected?}>
    <!-- Shows connection state -->
  </div>
  """
end

@impl true
def mount(_params, _session, socket) do
  {:ok, assign(socket, :connected?, connected?(socket))}
end
```

### Log render phases

```elixir
@impl true
def mount(_params, _session, socket) do
  IO.puts("Mount called - Connected: #{connected?(socket)}")
  {:ok, socket}
end

@impl true
def handle_params(params, _uri, socket) do
  IO.puts("Handle params - Connected: #{connected?(socket)}")
  {:noreply, socket}
end
```

## Safe Assign Access Helpers

Create helper functions for safe access:

```elixir
defp get_assign(socket, key, default \\ nil) do
  Map.get(socket.assigns, key, default)
end

defp has_assign?(socket, key) do
  Map.has_key?(socket.assigns, key)
end

# Usage
def some_function(socket) do
  if has_assign?(socket, :current_user) do
    user = get_assign(socket, :current_user)
    # Do something with user
  end
end
```

## Testing Both Phases

```elixir
test "renders correctly in both phases", %{conn: conn} do
  # Static render (disconnected)
  {:ok, _view, html} = live(conn, "/page")
  assert html =~ "Expected content"

  # Now connected
  # Can test live interactions
end

test "initializes assigns in mount", %{conn: conn} do
  {:ok, view, _html} = live(conn, "/page")

  # Check assigns are set
  assert view.assigns.count == 0
  assert view.assigns.user != nil
end
```

## Quick Reference

### Safe Patterns

```elixir
# ✅ Initialize in mount
assign(socket, :key, default_value)

# ✅ Use Map.get for optional
Map.get(socket.assigns, :key, default)

# ✅ Check connected for side effects
if connected?(socket), do: subscribe()

# ✅ Pattern match with fallback
def helper(%{name: name}), do: name
def helper(_), do: "default"
```

### Unsafe Patterns

```elixir
# ❌ Direct access without initialization
socket.assigns.key

# ❌ Subscribe without checking
Phoenix.PubSub.subscribe(...)

# ❌ Expensive ops in both phases
mount(...) do
  data = expensive_query()
end

# ❌ Pattern match without fallback
def helper(%{name: name}), do: name
```
