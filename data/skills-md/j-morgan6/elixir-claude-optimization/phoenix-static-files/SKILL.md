---
name: phoenix-static-files
description: Use when serving uploaded files, assets, or any static content. Covers static_paths configuration, Plug.Static setup, and troubleshooting file serving issues.
---

# Phoenix Static File Serving

## When to Use

Use when serving uploaded files, assets, or any static content through Phoenix.

## Critical Concept

**If you reference a path like `/uploads/photo.jpg` in your app, the directory "uploads" MUST be in `static_paths()` or the file won't be served!**

## Configuration Required

### 1. Define static_paths/0

```elixir
# lib/my_app_web.ex
def static_paths do
  ~w(assets fonts images uploads favicon.ico robots.txt)
end
```

**Rule:** Any directory you serve files from must be listed here.

### 2. Verify Plug.Static Configuration

```elixir
# lib/my_app_web/endpoint.ex
plug Plug.Static,
  at: "/",
  from: :my_app,
  gzip: false,
  only: MyAppWeb.static_paths()
```

The `only: MyAppWeb.static_paths()` line ensures only configured directories are served.

## Common Patterns

### User Uploads

```elixir
# Save uploaded file
dest = Path.join(["priv", "static", "uploads", filename])
File.mkdir_p!(Path.dirname(dest))
File.cp!(source, dest)

# Store path in database
path = "/uploads/#{filename}"

# MUST add to static_paths
def static_paths, do: ~w(assets uploads favicon.ico)
```

### Generated Content

```elixir
# For dynamically generated images, charts, PDFs
def static_paths, do: ~w(assets uploads generated exports favicon.ico)
```

### Multiple Upload Directories

```elixir
# Different directories for different content types
def static_paths do
  ~w(
    assets
    uploads/images
    uploads/documents
    uploads/avatars
    generated
    favicon.ico
  )
end
```

## File Structure

Static files must be in `priv/static/`:

```
my_app/
├── priv/
│   └── static/
│       ├── assets/        # CSS, JS (from esbuild)
│       ├── uploads/       # User uploads
│       │   ├── image1.jpg
│       │   └── doc.pdf
│       ├── generated/     # Generated files
│       └── favicon.ico
```

## Serving Files

### From Templates

```heex
<!-- Image -->
<img src="/uploads/photo.jpg" alt="Photo" />

<!-- Document download -->
<.link href="/uploads/document.pdf" download>Download</.link>

<!-- Static asset -->
<img src={~p"/images/logo.png"} alt="Logo" />
```

### From Controllers

```elixir
def download(conn, %{"filename" => filename}) do
  path = Path.join(["priv", "static", "uploads", filename])

  if File.exists?(path) do
    send_download(conn, {:file, path}, filename: filename)
  else
    conn
    |> put_status(:not_found)
    |> text("File not found")
  end
end
```

## Troubleshooting

### Files Return 404

**Problem:** Accessing `/uploads/file.jpg` returns 404

**Fixes:**
1. Check static_paths includes "uploads"
2. Verify file exists in `priv/static/uploads/`
3. Restart server after changing static_paths
4. Check file permissions (should be readable)

```elixir
# Debug helper
def check_static_file(path) do
  full_path = Path.join(["priv", "static", path])

  cond do
    not File.exists?(full_path) ->
      "File does not exist: #{full_path}"

    not File.readable?(full_path) ->
      "File exists but not readable: #{full_path}"

    true ->
      "File OK: #{full_path}"
  end
end
```

### Files Work in Dev but Not Production

**Problem:** Files serve correctly locally but fail in production

**Fixes:**

1. **Run `mix phx.digest` before deployment:**
```bash
MIX_ENV=prod mix phx.digest
```

2. **Check production endpoint config:**
```elixir
# config/runtime.exs
config :my_app, MyAppWeb.Endpoint,
  cache_static_manifest: "priv/static/cache_manifest.json"
```

3. **Ensure files are deployed:**
```
# Check your deployment includes priv/static/
```

### Large Files Slow Down Server

**Problem:** Serving large files (videos, archives) through Phoenix

**Solution:** Use a CDN or reverse proxy (nginx, CloudFront)

```elixir
# For large files, consider streaming
def download_large(conn, %{"id" => id}) do
  file = get_file!(id)

  conn
  |> put_resp_header("content-type", file.content_type)
  |> put_resp_header("content-disposition", ~s(attachment; filename="#{file.name}"))
  |> send_chunked(200)
  |> stream_file(file.path)
end

defp stream_file(conn, path) do
  File.stream!(path, [], 2048)
  |> Enum.reduce_while(conn, fn chunk, conn ->
    case chunk(conn, chunk) do
      {:ok, conn} -> {:cont, conn}
      {:error, :closed} -> {:halt, conn}
    end
  end)
end
```

## Security Best Practices

### 1. Sanitize File Paths

**Never** use user input directly in file paths:

```elixir
# ❌ DANGEROUS - Path traversal attack
def serve_file(conn, %{"path" => user_path}) do
  send_file(conn, 200, "priv/static/#{user_path}")
end

# ✅ SAFE - Validate and constrain
def serve_file(conn, %{"filename" => filename}) do
  safe_name = Path.basename(filename)  # Remove directory traversal
  path = Path.join(["priv", "static", "uploads", safe_name])

  if File.exists?(path) and String.starts_with?(path, "priv/static/uploads") do
    send_file(conn, 200, path)
  else
    send_resp(conn, 404, "Not found")
  end
end
```

### 2. Content-Type Headers

Set proper content types to prevent XSS:

```elixir
def serve_image(conn, %{"id" => id}) do
  image = get_image!(id)

  conn
  |> put_resp_header("content-type", image.content_type)
  |> put_resp_header("x-content-type-options", "nosniff")
  |> send_file(200, image.path)
end
```

### 3. Access Control

Protect sensitive files:

```elixir
def download_private(conn, %{"id" => id}) do
  user = conn.assigns.current_user
  file = get_file!(id)

  if authorized?(user, file) do
    send_file(conn, 200, file.path)
  else
    send_resp(conn, 403, "Forbidden")
  end
end
```

## CDN Integration

For production, serve static files via CDN:

```elixir
# config/runtime.exs
config :my_app, MyAppWeb.Endpoint,
  static_url: [host: "cdn.example.com", port: 443, scheme: "https"]

# Now ~p"/uploads/file.jpg" generates:
# https://cdn.example.com/uploads/file.jpg
```

## Cache Control

Set appropriate cache headers:

```elixir
# In endpoint.ex
plug Plug.Static,
  at: "/",
  from: :my_app,
  only: MyAppWeb.static_paths(),
  cache_control_for_etags: "public, max-age=86400",
  headers: %{"cache-control" => "public, max-age=31536000"}
```

## Development vs Production

```elixir
# Development - serve files directly
# config/dev.exs
config :my_app, MyAppWeb.Endpoint,
  debug_errors: true,
  code_reloader: true,
  check_origin: false,
  watchers: [...]

# Production - optimize serving
# config/prod.exs
config :my_app, MyAppWeb.Endpoint,
  cache_static_manifest: "priv/static/cache_manifest.json",
  server: true
```

## Quick Reference

```elixir
# 1. Add directory to static_paths
def static_paths, do: ~w(assets uploads favicon.ico)

# 2. Create directory structure
priv/static/uploads/

# 3. Save files there
Path.join(["priv", "static", "uploads", filename])

# 4. Reference in templates
<img src="/uploads/#{filename}" />

# 5. Restart server to apply changes
mix phx.server
```

## Common Mistakes

❌ Forgetting to add directory to static_paths
❌ Not creating the physical directory
❌ Using relative paths in templates
❌ Not restarting server after config change
❌ Trusting user-provided paths
❌ Serving files from outside priv/static/

✅ Always add directories to static_paths
✅ Create directories with File.mkdir_p!
✅ Use absolute paths like "/uploads/file"
✅ Restart after static_paths changes
✅ Validate and sanitize file paths
✅ Keep all static files in priv/static/
