---
name: ecto-database
description: Use when working with Ecto and database operations. Covers schemas, changesets, queries, associations, preloading, transactions, and migrations.
---

# Ecto Database Patterns

## Schema Definition

Define schemas with proper types and associations.

```elixir
defmodule MyApp.Media.Image do
  use Ecto.Schema
  import Ecto.Changeset

  schema "images" do
    field :title, :string
    field :description, :string
    field :filename, :string
    field :file_path, :string
    field :content_type, :string
    field :file_size, :integer

    belongs_to :folder, MyApp.Media.Folder

    timestamps()
  end
end
```

## Changesets

Always use changesets for data validation and casting.

```elixir
def changeset(image, attrs) do
  image
  |> cast(attrs, [:title, :description, :filename, :file_path, :content_type, :file_size, :folder_id])
  |> validate_required([:title, :filename, :file_path, :content_type, :file_size])
  |> validate_length(:title, min: 1, max: 255)
  |> validate_inclusion(:content_type, ["image/jpeg", "image/png", "image/gif"])
  |> validate_number(:file_size, greater_than: 0, less_than: 10_000_000)
  |> foreign_key_constraint(:folder_id)
end
```

## Query Composition

Build queries composably using `Ecto.Query`.

```elixir
import Ecto.Query

def list_images_by_folder(folder_id) do
  Image
  |> where([i], i.folder_id == ^folder_id)
  |> order_by([i], desc: i.inserted_at)
  |> Repo.all()
end

def search_images(query_string) do
  search = "%#{query_string}%"

  Image
  |> where([i], ilike(i.title, ^search) or ilike(i.description, ^search))
  |> Repo.all()
end
```

## Preloading Associations

Use `preload` to avoid N+1 queries.

**Bad:**
```elixir
images = Repo.all(Image)
# Later accessing image.folder causes N queries
Enum.each(images, fn image -> image.folder.name end)
```

**Good:**
```elixir
images =
  Image
  |> preload(:folder)
  |> Repo.all()

Enum.each(images, fn image -> image.folder.name end)
```

## Transactions

Use `Repo.transaction` for operations that must succeed together.

```elixir
def transfer_images(image_ids, from_folder_id, to_folder_id) do
  Repo.transaction(fn ->
    with {:ok, from_folder} <- get_folder(from_folder_id),
         {:ok, to_folder} <- get_folder(to_folder_id),
         {count, nil} <- update_images(image_ids, to_folder_id) do
      {:ok, count}
    else
      {:error, reason} -> Repo.rollback(reason)
      _ -> Repo.rollback(:unknown_error)
    end
  end)
end
```

## Insert and Update

Use `Repo.insert` and `Repo.update` with changesets.

```elixir
def create_image(attrs) do
  %Image{}
  |> Image.changeset(attrs)
  |> Repo.insert()
end

def update_image(%Image{} = image, attrs) do
  image
  |> Image.changeset(attrs)
  |> Repo.update()
end
```

## Upsert Operations

Use `on_conflict` for upsert behavior.

```elixir
def create_or_update_folder(attrs) do
  %Folder{}
  |> Folder.changeset(attrs)
  |> Repo.insert(
    on_conflict: {:replace, [:name, :updated_at]},
    conflict_target: :name
  )
end
```

## Associations

Define associations properly in schemas.

```elixir
# Parent schema
defmodule MyApp.Media.Folder do
  use Ecto.Schema

  schema "folders" do
    field :name, :string
    has_many :images, MyApp.Media.Image

    timestamps()
  end
end

# Child schema
defmodule MyApp.Media.Image do
  use Ecto.Schema

  schema "images" do
    field :title, :string
    belongs_to :folder, MyApp.Media.Folder

    timestamps()
  end
end
```

## Building Associations

Use `Ecto.build_assoc` to create associated records.

```elixir
def add_image_to_folder(folder, image_attrs) do
  folder
  |> Ecto.build_assoc(:images)
  |> Image.changeset(image_attrs)
  |> Repo.insert()
end
```

## Casting Associations

Use `cast_assoc` when working with nested data.

```elixir
def changeset(folder, attrs) do
  folder
  |> cast(attrs, [:name])
  |> cast_assoc(:images, with: &Image.changeset/2)
  |> validate_required([:name])
end
```

## Dynamic Queries

Build queries dynamically based on filters.

```elixir
def list_images(filters) do
  Image
  |> apply_filters(filters)
  |> Repo.all()
end

defp apply_filters(query, filters) do
  Enum.reduce(filters, query, fn
    {:folder_id, folder_id}, query ->
      where(query, [i], i.folder_id == ^folder_id)

    {:search, term}, query ->
      where(query, [i], ilike(i.title, ^"%#{term}%"))

    {:min_size, size}, query ->
      where(query, [i], i.file_size >= ^size)

    _, query ->
      query
  end)
end
```

## Aggregations

Use aggregation functions for statistics.

```elixir
def count_images_by_folder do
  Image
  |> group_by([i], i.folder_id)
  |> select([i], {i.folder_id, count(i.id)})
  |> Repo.all()
  |> Map.new()
end

def total_storage_used do
  Image
  |> select([i], sum(i.file_size))
  |> Repo.one()
end
```

## Repo Functions

Common `Repo` operations:

```elixir
# Fetch single record
Repo.get(Image, id)           # Returns record or nil
Repo.get!(Image, id)          # Returns record or raises
Repo.get_by(Image, title: "Photo")

# Fetch all records
Repo.all(Image)

# Insert
Repo.insert(changeset)        # Returns {:ok, record} or {:error, changeset}
Repo.insert!(changeset)       # Returns record or raises

# Update
Repo.update(changeset)
Repo.update!(changeset)

# Delete
Repo.delete(record)
Repo.delete!(record)

# Delete all matching
Repo.delete_all(Image)
Repo.delete_all(where(Image, [i], i.folder_id == ^folder_id))
```

## Migrations

Write clear, reversible migrations.

```elixir
defmodule MyApp.Repo.Migrations.CreateImages do
  use Ecto.Migration

  def change do
    create table(:images) do
      add :title, :string, null: false
      add :description, :text
      add :filename, :string, null: false
      add :file_path, :string, null: false
      add :content_type, :string, null: false
      add :file_size, :integer, null: false
      add :folder_id, references(:folders, on_delete: :nilify_all)

      timestamps()
    end

    create index(:images, [:folder_id])
    create index(:images, [:inserted_at])
  end
end
```

## Unique Constraints

Add unique constraints in schema and migration.

```elixir
# Migration
create unique_index(:folders, [:name])

# Schema changeset
def changeset(folder, attrs) do
  folder
  |> cast(attrs, [:name])
  |> validate_required([:name])
  |> unique_constraint(:name)
end
```

## Virtual Fields

Use virtual fields for computed or temporary data.

```elixir
schema "images" do
  field :title, :string
  field :file_path, :string
  field :url, :string, virtual: true

  timestamps()
end

def with_url(%Image{} = image) do
  %{image | url: "/uploads/#{Path.basename(image.file_path)}"}
end
```

## Custom Types

Define custom Ecto types for special data.

```elixir
defmodule MyApp.FileSize do
  use Ecto.Type

  def type, do: :integer

  def cast(size) when is_integer(size) and size >= 0, do: {:ok, size}
  def cast(_), do: :error

  def load(size), do: {:ok, size}
  def dump(size), do: {:ok, size}
end
```

## Context Pattern

Organize database operations in contexts.

```elixir
defmodule MyApp.Media do
  alias MyApp.Media.{Image, Folder}
  alias MyApp.Repo

  def list_images, do: Repo.all(Image)

  def get_image!(id), do: Repo.get!(Image, id)

  def create_image(attrs) do
    %Image{}
    |> Image.changeset(attrs)
    |> Repo.insert()
  end

  def update_image(%Image{} = image, attrs) do
    image
    |> Image.changeset(attrs)
    |> Repo.update()
  end

  def delete_image(%Image{} = image) do
    Repo.delete(image)
  end
end
```
