---
name: elixir-patterns
description: Use when writing Elixir code. Covers pattern matching, pipe operators, with statements, guards, list comprehensions, and Elixir naming conventions.
---

# Elixir Patterns and Conventions

## Pattern Matching

Pattern matching is the primary control flow mechanism in Elixir. Prefer it over conditional statements.

### Prefer Pattern Matching Over if/else

**Bad:**
```elixir
def process(result) do
  if result.status == :ok do
    result.data
  else
    nil
  end
end
```

**Good:**
```elixir
def process(%{status: :ok, data: data}), do: data
def process(_), do: nil
```

### Use Case for Multiple Patterns

**Bad:**
```elixir
def handle_response(response) do
  if response.status == 200 do
    {:ok, response.body}
  else if response.status == 404 do
    {:error, :not_found}
  else
    {:error, :unknown}
  end
end
```

**Good:**
```elixir
def handle_response(%{status: 200, body: body}), do: {:ok, body}
def handle_response(%{status: 404}), do: {:error, :not_found}
def handle_response(_), do: {:error, :unknown}
```

## Pipe Operator

Use the pipe operator `|>` to chain function calls for improved readability.

### Basic Piping

**Bad:**
```elixir
String.upcase(String.trim(user_input))
```

**Good:**
```elixir
user_input
|> String.trim()
|> String.upcase()
```

### Pipe into Function Heads

**Bad:**
```elixir
def process_user(user) do
  validated = validate_user(user)
  transformed = transform_user(validated)
  save_user(transformed)
end
```

**Good:**
```elixir
def process_user(user) do
  user
  |> validate_user()
  |> transform_user()
  |> save_user()
end
```

## With Statement

Use `with` for sequential operations that can fail.

**Bad:**
```elixir
def create_post(params) do
  case validate_params(params) do
    {:ok, valid_params} ->
      case create_changeset(valid_params) do
        {:ok, changeset} ->
          Repo.insert(changeset)
        error -> error
      end
    error -> error
  end
end
```

**Good:**
```elixir
def create_post(params) do
  with {:ok, valid_params} <- validate_params(params),
       {:ok, changeset} <- create_changeset(valid_params),
       {:ok, post} <- Repo.insert(changeset) do
    {:ok, post}
  end
end
```

## Immutability

All data structures are immutable. Functions return new values rather than modifying in place.

```elixir
# Always returns a new list
list = [1, 2, 3]
new_list = [0 | list]  # [0, 1, 2, 3]
# list is still [1, 2, 3]
```

## Guards

Use guards for simple type and value checks in function heads.

```elixir
def calculate(x) when is_integer(x) and x > 0 do
  x * 2
end

def calculate(_), do: {:error, :invalid_input}
```

## Anonymous Functions

Use the capture operator `&` for concise anonymous functions.

**Verbose:**
```elixir
Enum.map(list, fn x -> x * 2 end)
```

**Concise:**
```elixir
Enum.map(list, &(&1 * 2))
```

**Named function capture:**
```elixir
Enum.map(users, &User.format/1)
```

## List Comprehensions

Use `for` comprehensions for complex transformations and filtering.

**Bad (multiple passes):**
```elixir
list
|> Enum.map(&transform/1)
|> Enum.filter(&valid?/1)
|> Enum.map(&format/1)
```

**Good (single pass):**
```elixir
for item <- list,
    transformed = transform(item),
    valid?(transformed) do
  format(transformed)
end
```

## Naming Conventions

- Module names: `PascalCase`
- Function names: `snake_case`
- Variables: `snake_case`
- Atoms: `:snake_case`
- Predicate functions end with `?`: `valid?`, `empty?`
- Dangerous functions end with `!`: `save!`, `update!`

## Boolean Checks

Functions returning booleans should end with `?`.

```elixir
def admin?(user), do: user.role == :admin
def empty?(list), do: list == []
```

## Error Tuples

Return `{:ok, result}` or `{:error, reason}` tuples for operations that can fail.

```elixir
def fetch_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end
```

## Documentation

Use `@doc` for public functions and `@moduledoc` for modules.

```elixir
defmodule MyModule do
  @moduledoc """
  This module handles user operations.
  """

  @doc """
  Fetches a user by ID.

  Returns `{:ok, user}` or `{:error, :not_found}`.
  """
  def fetch_user(id), do: # ...
end
```
