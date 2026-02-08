---
name: nu-shell
description: Processes structured data through pipelines, filters tables, transforms JSON/CSV/YAML, and defines custom commands. Use when scripting with typed parameters or working with tabular data.
---

# nu-shell

Structured data scripting through pipelines with tables, lists, and records.

## Core Concepts

### Data Types

- **Record**: `{ name: "John", age: 30 }`
- **List**: `[1, 2, 3]`
- **Table**: A list of records with the same keys

### Pipelines

```nu
ls | where size > 10mb | sort-by size
```

## Running Scripts

```bash
nu myscript.nu           # Run script file
nu -c 'ls | length'      # Run inline command
source myscript.nu       # Run in current session
```

## Data Manipulation

### Loading and Saving

```nu
let config = (open config.json)
let data = (open data.csv)

$data | save output.yaml
$data | to json | save output.json
```

### Filtering and Selecting

```nu
ls | where name =~ "test"        # Filter rows
ls | select name size            # Select columns
(open package.json).version      # Access fields
```

### Processing Tables

```nu
ls | where size > 10mb           # Filter by condition
ls | select name size            # Select columns
ls | sort-by size                # Sort
ls | group-by name               # Group
ls | length                      # Count rows
```

### Processing Records

```nu
let user = { name: "John", age: 30 }
echo $user.name                  # Access field

let updated = { ...$user, age: 31 }  # Update field
let merged = { ...$config, debug: true }  # Merge
```

### Processing Lists

```nu
[1, 2, 3, 4, 5] | where $it > 2           # Filter
[1, 2, 3] | each { |x| $x * 2 }           # Map
[1, 2, 3, 4, 5] | reduce { |acc, x| $acc + $x }  # Reduce
```

## Scripting

### Basic Script Structure

```nu
#!/usr/bin/env nu

def "my command" [param: string] {
    echo $"Hello, ($param)"
}

my command "world"
```

### Control Flow

```nu
# If statement
if true { echo "Hello" }

# If-else
if true { echo "Yes" } else { echo "No" }

# For loop
for i in 1..10 { echo $i }

# While loop
mut i = 1
while $i <= 10 {
    echo $i
    $i = $i + 1
}
```

### Custom Commands

```nu
# With typed parameters
def "create project" [name: string, type: string = "typescript"] {
    echo $"Creating ($name) with ($type)"
}

# With flags
def "deploy" [--env: string = "production"] {
    echo $"Deploying to ($env)"
}
```

## File Operations

```nu
let content = (open "file.txt")       # Read
$content | save "output.txt"          # Write
$content | save --append "file.txt"   # Append
```

## Tips

- Use `nu -c 'command'` to run commands inline
- Use `open` to load data from various formats
- Use `save` to write data to various formats
- Use `where` to filter tables
- Use `select` to choose columns
- Use `sort-by` to sort tables
- Use `each` to map over lists
- Use `reduce` to combine list elements
