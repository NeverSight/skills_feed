---
name: phoenix-uploads
description: Use when implementing file upload functionality with Phoenix LiveView. Covers upload configuration, manual vs auto-upload patterns, error handling, and static file serving.
---

# Phoenix LiveView File Upload Patterns

## When to Use

Use when implementing file upload functionality with Phoenix LiveView.

## Upload Configuration

### Manual Upload (Recommended for Most Cases)

```elixir
allow_upload(:upload_name,
  accept: ~w(.jpg .jpeg .png .pdf),
  max_entries: 10,
  max_file_size: 10_000_000
)
```

**Template Requirements:**
- Form with `phx-submit` event
- Submit button to trigger upload
- `<.live_file_input>` component
- Progress indicators

### Auto Upload (Advanced)

Only use `auto_upload: true` when:
- Files should upload immediately on selection
- You have `handle_progress/3` callback
- You consume entries outside form submission

**⚠️ Never use auto_upload: true with form submission patterns!**

## Complete Upload Pattern

### LiveView Module

```elixir
@impl true
def mount(_params, _session, socket) do
  socket =
    socket
    |> assign(:uploaded_files, [])
    |> allow_upload(:photos,
         accept: ~w(.jpg .jpeg .png),
         max_entries: 5,
         max_file_size: 10_000_000
       )

  {:ok, socket}
end

@impl true
def handle_event("validate", _params, socket) do
  {:noreply, socket}
end

@impl true
def handle_event("save", _params, socket) do
  uploaded_files =
    consume_uploaded_entries(socket, :photos, fn %{path: path}, entry ->
      dest = Path.join(["priv", "static", "uploads", entry.client_name])
      File.mkdir_p!(Path.dirname(dest))
      File.cp!(path, dest)
      {:ok, ~s(/uploads/#{entry.client_name})}
    end)

  # Save to database with uploaded_files paths
  {:noreply, assign(socket, :uploaded_files, uploaded_files)}
end
```

### Template

```heex
<.simple_form for={@form} phx-change="validate" phx-submit="save">
  <.input field={@form[:title]} label="Title" />

  <div>
    <.label>Upload Photos</.label>
    <.live_file_input upload={@uploads.photos} />
  </div>

  <!-- Upload errors -->
  <%= for err <- upload_errors(@uploads.photos) do %>
    <p class="error"><%= error_to_string(err) %></p>
  <% end %>

  <!-- Entry previews and errors -->
  <%= for entry <- @uploads.photos.entries do %>
    <div>
      <.live_img_preview entry={entry} />
      <progress value={entry.progress} max="100"><%= entry.progress %>%</progress>

      <%= for err <- upload_errors(@uploads.photos, entry) do %>
        <p class="error"><%= error_to_string(err) %></p>
      <% end %>
    </div>
  <% end %>

  <:actions>
    <.button phx-disable-with="Uploading...">Upload</.button>
  </:actions>
</.simple_form>
```

## Error Handling

Always implement `error_to_string/1`:

```elixir
defp error_to_string(:too_large), do: "File is too large (max 10MB)"
defp error_to_string(:not_accepted), do: "File type not accepted"
defp error_to_string(:too_many_files), do: "Too many files selected"
defp error_to_string(:external_client_failure), do: "Upload failed"
```

## Static File Serving

After upload, ensure static_paths includes your upload directory:

```elixir
# lib/my_app_web.ex
def static_paths, do: ~w(assets uploads favicon.ico robots.txt)
```

**Critical:** Without this, uploaded files won't be accessible!

## Image Previews

For image uploads, show previews:

```heex
<%= for entry <- @uploads.photos.entries do %>
  <div class="preview">
    <.live_img_preview entry={entry} width={200} />
    <button type="button" phx-click="cancel-upload" phx-value-ref={entry.ref}>
      Cancel
    </button>
  </div>
<% end %>
```

```elixir
@impl true
def handle_event("cancel-upload", %{"ref" => ref}, socket) do
  {:noreply, cancel_upload(socket, :photos, ref)}
end
```

## Multiple Upload Slots

You can have multiple upload configurations:

```elixir
socket
|> allow_upload(:photos, accept: ~w(.jpg .jpeg .png), max_entries: 5)
|> allow_upload(:documents, accept: ~w(.pdf .docx), max_entries: 3)
```

## External Storage (S3, etc.)

For external storage, use the `:external` option:

```elixir
allow_upload(:photos,
  accept: ~w(.jpg .jpeg .png),
  max_entries: 5,
  external: &presign_upload/2
)

defp presign_upload(entry, socket) do
  # Generate presigned URL for S3
  {:ok, %{uploader: "S3", key: key, url: url}, socket}
end
```

## Common Pitfalls

### ❌ Using auto_upload with form submit
```elixir
# DON'T DO THIS
allow_upload(:photos, auto_upload: true, ...)

def handle_event("save", _params, socket) do
  consume_uploaded_entries(socket, :photos, ...)  # Won't work!
end
```

### ✅ Use manual upload instead
```elixir
# DO THIS
allow_upload(:photos, ...)

def handle_event("save", _params, socket) do
  consume_uploaded_entries(socket, :photos, ...)  # Works!
end
```

### ❌ Not handling upload errors
```heex
<!-- Missing error display -->
<.live_file_input upload={@uploads.photos} />
```

### ✅ Always show errors
```heex
<.live_file_input upload={@uploads.photos} />
<%= for err <- upload_errors(@uploads.photos) do %>
  <p class="error"><%= error_to_string(err) %></p>
<% end %>
```

### ❌ Forgetting static_paths
```elixir
# File saved to priv/static/uploads/
# But "uploads" not in static_paths
def static_paths, do: ~w(assets favicon.ico)  # Missing uploads!
```

### ✅ Include upload directory
```elixir
def static_paths, do: ~w(assets uploads favicon.ico)
```

## Testing Uploads

```elixir
test "uploads image successfully", %{conn: conn} do
  {:ok, lv, _html} = live(conn, "/gallery")

  image =
    file_input(lv, "#upload-form", :photos, [
      %{
        name: "test.png",
        content: File.read!("test/fixtures/test.png"),
        type: "image/png"
      }
    ])

  assert render_upload(image, "test.png") =~ "100%"

  lv
  |> form("#upload-form")
  |> render_submit()

  assert has_element?(lv, "img[alt='test.png']")
end
```

## Security Considerations

1. **Validate file types** - Don't trust client MIME types
2. **Scan for malware** - Use external scanning service
3. **Limit file sizes** - Prevent DoS attacks
4. **Sanitize filenames** - Avoid path traversal
5. **Use unique names** - Prevent overwriting files

```elixir
defp safe_filename(original_name) do
  # Generate unique name to prevent collisions and attacks
  ext = Path.extname(original_name)
  "#{Ecto.UUID.generate()}#{ext}"
end
```
