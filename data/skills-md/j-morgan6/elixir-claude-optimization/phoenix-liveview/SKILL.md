---
name: phoenix-liveview
description: Use when working with Phoenix LiveView. Covers lifecycle, mount/handle_event/handle_info callbacks, file uploads, navigation, PubSub, and LiveView testing.
---

# Phoenix LiveView Patterns

## LiveView Lifecycle

A LiveView goes through two phases:
1. **Static Mount**: Initial HTTP request (connected?: false)
2. **Connected Mount**: WebSocket upgrade (connected?: true)

```elixir
def mount(_params, _session, socket) do
  if connected?(socket) do
    # Subscribe to topics, start timers, etc.
    Phoenix.PubSub.subscribe(MyApp.PubSub, "topic")
  end

  {:ok, assign(socket, :data, [])}
end
```

## Handle Event

Use pattern matching in `handle_event/3` for different actions.

```elixir
def handle_event("save", %{"post" => post_params}, socket) do
  case Posts.create_post(post_params) do
    {:ok, post} ->
      {:noreply, socket |> put_flash(:info, "Created!") |> assign(:post, post)}
    {:error, changeset} ->
      {:noreply, assign(socket, :changeset, changeset)}
  end
end

def handle_event("delete", %{"id" => id}, socket) do
  Posts.delete_post(id)
  {:noreply, assign(socket, :posts, Posts.list_posts())}
end
```

## Handle Info

Handle async messages and PubSub broadcasts with `handle_info/2`.

```elixir
def handle_info({:post_created, post}, socket) do
  {:noreply, update(socket, :posts, fn posts -> [post | posts] end)}
end

def handle_info(%{event: "presence_diff"}, socket) do
  {:noreply, assign(socket, :online_users, get_presence_count())}
end
```

## Socket Assigns

Use `assign/2` or `assign/3` to update socket state.

```elixir
# Single assign
socket = assign(socket, :count, 0)

# Multiple assigns
socket = assign(socket, count: 0, name: "User", active: true)

# Update existing assign
socket = update(socket, :count, &(&1 + 1))
```

## Temporary Assigns

Use temporary assigns for large collections that don't need to persist.

```elixir
def mount(_params, _session, socket) do
  socket = assign(socket, :posts, [])
  {:ok, socket, temporary_assigns: [posts: []]}
end
```

## LiveView Uploads

Use built-in upload functionality for file uploads.

```elixir
def mount(_params, _session, socket) do
  socket =
    socket
    |> assign(:uploaded_files, [])
    |> allow_upload(:image,
        accept: ~w(.jpg .jpeg .png),
        max_entries: 5,
        max_file_size: 10_000_000
      )

  {:ok, socket}
end

def handle_event("validate", _params, socket) do
  {:noreply, socket}
end

def handle_event("save", _params, socket) do
  uploaded_files =
    consume_uploaded_entries(socket, :image, fn %{path: path}, entry ->
      dest = Path.join("priv/static/uploads", entry.client_name)
      File.cp!(path, dest)
      {:ok, "/uploads/#{entry.client_name}"}
    end)

  {:noreply, update(socket, :uploaded_files, &(&1 ++ uploaded_files))}
end
```

## Flash Messages

Use `put_flash/3` and `clear_flash/2` for user feedback.

```elixir
def handle_event("save", params, socket) do
  case save_data(params) do
    {:ok, _} ->
      socket = put_flash(socket, :info, "Saved successfully!")
      {:noreply, socket}
    {:error, _} ->
      socket = put_flash(socket, :error, "Failed to save")
      {:noreply, socket}
  end
end
```

## Live Navigation

Use `push_navigate/2` or `push_patch/2` for navigation.

```elixir
# Full page reload (new LiveView)
{:noreply, push_navigate(socket, to: ~p"/users")}

# Patch (same LiveView, different params)
{:noreply, push_patch(socket, to: ~p"/posts/#{post}")}
```

## Handle Params

Use `handle_params/3` to respond to URL changes.

```elixir
def handle_params(%{"id" => id}, _uri, socket) do
  post = Posts.get_post!(id)
  {:noreply, assign(socket, :post, post)}
end

def handle_params(_params, _uri, socket) do
  {:noreply, socket}
end
```

## Streams

Use streams for efficient rendering of large lists.

```elixir
def mount(_params, _session, socket) do
  {:ok, stream(socket, :posts, Posts.list_posts())}
end

def handle_event("add", %{"post" => attrs}, socket) do
  {:ok, post} = Posts.create_post(attrs)
  {:noreply, stream_insert(socket, :posts, post, at: 0)}
end

def handle_event("delete", %{"id" => id}, socket) do
  Posts.delete_post(id)
  {:noreply, stream_delete_by_dom_id(socket, :posts, "posts-#{id}")}
end
```

## Components

Extract reusable UI into function components.

```elixir
def card(assigns) do
  ~H"""
  <div class="card">
    <h3><%= @title %></h3>
    <p><%= @content %></p>
  </div>
  """
end

# Usage in template
<.card title="Hello" content="World" />
```

## Form Binding

Bind forms to changesets for validation.

```elixir
<.simple_form for={@form} phx-change="validate" phx-submit="save">
  <.input field={@form[:title]} label="Title" />
  <.input field={@form[:body]} type="textarea" label="Body" />
  <:actions>
    <.button>Save</.button>
  </:actions>
</.simple_form>
```

```elixir
def mount(_params, _session, socket) do
  changeset = Post.changeset(%Post{}, %{})
  {:ok, assign(socket, form: to_form(changeset))}
end

def handle_event("validate", %{"post" => params}, socket) do
  changeset =
    %Post{}
    |> Post.changeset(params)
    |> Map.put(:action, :validate)

  {:noreply, assign(socket, form: to_form(changeset))}
end
```

## Error Handling

Always handle errors gracefully in LiveViews.

```elixir
def handle_event("risky_operation", _params, socket) do
  case perform_operation() do
    {:ok, result} ->
      {:noreply, assign(socket, :result, result)}
    {:error, reason} ->
      {:noreply, put_flash(socket, :error, "Operation failed: #{reason}")}
  end
end
```

## PubSub Broadcasting

Use PubSub for real-time updates across LiveViews.

```elixir
# Subscribe in mount
def mount(_params, _session, socket) do
  if connected?(socket) do
    Phoenix.PubSub.subscribe(MyApp.PubSub, "posts")
  end
  {:ok, assign(socket, :posts, list_posts())}
end

# Broadcast when data changes
def create_post(attrs) do
  with {:ok, post} <- Repo.insert(changeset) do
    Phoenix.PubSub.broadcast(MyApp.PubSub, "posts", {:post_created, post})
    {:ok, post}
  end
end

# Handle broadcast
def handle_info({:post_created, post}, socket) do
  {:noreply, update(socket, :posts, fn posts -> [post | posts] end)}
end
```

## Testing LiveViews

Use `Phoenix.LiveViewTest` for testing.

```elixir
test "uploads and displays image", %{conn: conn} do
  {:ok, lv, _html} = live(conn, "/gallery")

  image = file_input(lv, "#upload-form", :image, [
    %{name: "test.png", content: File.read!("test/support/test.png")}
  ])

  assert render_upload(image, "test.png") =~ "100%"

  lv
  |> form("#upload-form")
  |> render_submit()

  assert has_element?(lv, "img[alt='test.png']")
end
```

## Callbacks Implementation

Always add `@impl true` before callback implementations.

```elixir
defmodule MyAppWeb.PostLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, :posts, [])}
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    # ...
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div>Content</div>
    """
  end
end
```
