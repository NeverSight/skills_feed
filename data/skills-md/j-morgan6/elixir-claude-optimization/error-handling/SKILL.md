---
name: error-handling
description: Use when handling errors in Elixir. Covers tagged tuples, with statements, try/rescue, bang functions, supervision trees, and error boundaries in LiveView.
---

# Elixir Error Handling Patterns

## Tagged Tuples

The idiomatic way to handle success and failure in Elixir.

```elixir
def fetch_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end

# Usage
case fetch_user(123) do
  {:ok, user} -> IO.puts("Found: #{user.name}")
  {:error, :not_found} -> IO.puts("User not found")
end
```

## With Statement

Chain operations that return tagged tuples. Stops at first error.

```elixir
def create_post(user_id, params) do
  with {:ok, user} <- fetch_user(user_id),
       {:ok, validated} <- validate_params(params),
       {:ok, post} <- insert_post(user, validated) do
    {:ok, post}
  else
    {:error, :not_found} -> {:error, :user_not_found}
    {:error, %Ecto.Changeset{}} -> {:error, :invalid_params}
    error -> error
  end
end
```

## With Statement - Inline Error Handling

Handle specific errors in the else block.

```elixir
def transfer_money(from_id, to_id, amount) do
  with {:ok, from_account} <- get_account(from_id),
       {:ok, to_account} <- get_account(to_id),
       :ok <- validate_balance(from_account, amount),
       {:ok, _} <- debit(from_account, amount),
       {:ok, _} <- credit(to_account, amount) do
    {:ok, :transfer_complete}
  else
    {:error, :insufficient_funds} ->
      {:error, "Not enough money in account"}

    {:error, :not_found} ->
      {:error, "Account not found"}

    error ->
      {:error, "Transfer failed: #{inspect(error)}"}
  end
end
```

## Case Statements

Pattern match on results.

```elixir
def process_upload(file) do
  case save_file(file) do
    {:ok, path} ->
      Logger.info("File saved to #{path}")
      create_record(path)

    {:error, :invalid_format} ->
      {:error, "File format not supported"}

    {:error, reason} ->
      Logger.error("Upload failed: #{inspect(reason)}")
      {:error, "Upload failed"}
  end
end
```

## Bang Functions

Functions ending with `!` raise errors instead of returning tuples.

```elixir
# Returns {:ok, user} or {:error, changeset}
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end

# Returns user or raises
def create_user!(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert!()
end

# Usage
try do
  user = create_user!(invalid_attrs)
  IO.puts("Created #{user.name}")
rescue
  e in Ecto.InvalidChangesetError ->
    IO.puts("Failed: #{inspect(e)}")
end
```

## Try/Rescue

Catch exceptions when needed (use sparingly).

```elixir
def parse_json(string) do
  try do
    {:ok, Jason.decode!(string)}
  rescue
    Jason.DecodeError -> {:error, :invalid_json}
  end
end
```

## Try/Catch

Handle thrown values (rare).

```elixir
def risky_operation do
  try do
    do_something()
    :ok
  catch
    :throw, value -> {:error, value}
    :exit, reason -> {:error, {:exit, reason}}
  end
end
```

## Supervision Trees

Let processes fail and restart (preferred over defensive coding).

```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      MyApp.Repo,
      MyAppWeb.Endpoint,
      {MyApp.Worker, []}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

## GenServer Error Handling

Handle errors in GenServer callbacks.

```elixir
def handle_call(:risky_operation, _from, state) do
  case perform_operation() do
    {:ok, result} ->
      {:reply, {:ok, result}, update_state(state, result)}

    {:error, reason} ->
      Logger.error("Operation failed: #{inspect(reason)}")
      {:reply, {:error, reason}, state}
  end
end

# Let it crash for unexpected errors
def handle_cast(:dangerous_work, state) do
  # If this raises, supervisor will restart the process
  result = dangerous_function!()
  {:noreply, Map.put(state, :result, result)}
end
```

## Validation Errors

Return clear, actionable error messages.

```elixir
def validate_image_upload(file) do
  with :ok <- validate_file_type(file),
       :ok <- validate_file_size(file),
       :ok <- validate_dimensions(file) do
    {:ok, file}
  else
    {:error, :invalid_type} ->
      {:error, "Only JPEG, PNG, and GIF files are allowed"}

    {:error, :too_large} ->
      {:error, "File must be less than 10MB"}

    {:error, :invalid_dimensions} ->
      {:error, "Image must be at least 100x100 pixels"}
  end
end
```

## Multiple Error Types

Use atoms or custom structs for different error categories.

```elixir
def process_request(params) do
  with {:ok, validated} <- validate(params),
       {:ok, authorized} <- authorize(validated),
       {:ok, result} <- execute(authorized) do
    {:ok, result}
  else
    {:error, :validation, details} ->
      {:error, :bad_request, details}

    {:error, :unauthorized} ->
      {:error, :forbidden, "Access denied"}

    {:error, :not_found} ->
      {:error, :not_found, "Resource not found"}

    {:error, reason} ->
      Logger.error("Unexpected error: #{inspect(reason)}")
      {:error, :internal_server_error, "Something went wrong"}
  end
end
```

## Changeset Errors

Extract and format Ecto changeset errors.

```elixir
def changeset_errors(changeset) do
  Ecto.Changeset.traverse_errors(changeset, fn {msg, opts} ->
    Enum.reduce(opts, msg, fn {key, value}, acc ->
      String.replace(acc, "%{#{key}}", to_string(value))
    end)
  end)
end

# Usage
case create_user(attrs) do
  {:ok, user} -> {:ok, user}
  {:error, changeset} ->
    errors = changeset_errors(changeset)
    {:error, errors}
end
```

## Logging Errors

Log errors with appropriate levels.

```elixir
require Logger

def process_item(item) do
  case dangerous_operation(item) do
    {:ok, result} ->
      Logger.info("Processed item #{item.id}")
      {:ok, result}

    {:error, reason} ->
      Logger.error("Failed to process #{item.id}: #{inspect(reason)}")
      {:error, reason}
  end
end
```

## Default Values

Use pattern matching or `||` for default values.

```elixir
def get_config(key, default \\ nil) do
  case Application.get_env(:my_app, key) do
    nil -> default
    value -> value
  end
end

# Or simpler
def get_config(key, default \\ nil) do
  Application.get_env(:my_app, key) || default
end
```

## Early Returns

Use pattern matching in function heads for early returns.

```elixir
def process_data(nil), do: {:error, :no_data}
def process_data([]), do: {:error, :empty_list}
def process_data(data) when is_list(data) do
  # Process the list
  {:ok, Enum.map(data, &transform/1)}
end
```

## Error Boundaries in LiveView

Handle errors gracefully in Phoenix LiveView.

```elixir
def handle_event("save", params, socket) do
  case save_record(params) do
    {:ok, record} ->
      socket =
        socket
        |> put_flash(:info, "Saved successfully")
        |> assign(:record, record)

      {:noreply, socket}

    {:error, %Ecto.Changeset{} = changeset} ->
      socket =
        socket
        |> put_flash(:error, "Please correct the errors")
        |> assign(:changeset, changeset)

      {:noreply, socket}

    {:error, reason} ->
      socket = put_flash(socket, :error, "An error occurred: #{reason}")
      {:noreply, socket}
  end
end
```

## Avoid Defensive Programming

Don't check for things that can't happen. Let it crash.

**Bad (defensive):**
```elixir
def get_username(user) do
  if user && user.name do
    user.name
  else
    "Unknown"
  end
end
```

**Good (trust your types):**
```elixir
def get_username(%User{name: name}), do: name
```

If the user is nil or doesn't have a name, it's a bug that should crash and be fixed.
