---
name: advanced-array-patterns
description: Advanced bash array patterns including mapfile, readarray, associative arrays, and array manipulation (2025)
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

# Advanced Bash Array Patterns (2025)

## Overview

Comprehensive guide to bash arrays including indexed arrays, associative arrays, mapfile/readarray, and advanced manipulation patterns following 2025 best practices.

## Indexed Arrays

### Declaration and Initialization

```bash
#!/usr/bin/env bash
set -euo pipefail

# Method 1: Direct assignment
files=("file1.txt" "file2.txt" "file with spaces.txt")

# Method 2: Compound assignment
declare -a numbers=(1 2 3 4 5)

# Method 3: Individual assignment
fruits[0]="apple"
fruits[1]="banana"
fruits[2]="cherry"

# Method 4: From command output (CAREFUL with word splitting)
# ✗ DANGEROUS - splits on spaces
files_bad=$(ls)

# ✓ SAFE - preserves filenames with spaces
mapfile -t files_good < <(find . -name "*.txt")

# Method 5: Brace expansion
numbers=({1..100})
letters=({a..z})
```

### Array Operations

```bash
#!/usr/bin/env bash
set -euo pipefail

arr=("first" "second" "third" "fourth" "fifth")

# Length
echo "Length: ${#arr[@]}"  # 5

# Access elements
echo "First: ${arr[0]}"
echo "Last: ${arr[-1]}"  # Bash 4.3+
echo "Second to last: ${arr[-2]}"

# All elements (properly quoted for spaces)
for item in "${arr[@]}"; do
    echo "Item: $item"
done

# All indices
for idx in "${!arr[@]}"; do
    echo "Index $idx: ${arr[$idx]}"
done

# Slice (offset:length)
echo "${arr[@]:1:3}"  # second third fourth

# Slice from offset to end
echo "${arr[@]:2}"  # third fourth fifth

# Append element
arr+=("sixth")

# Insert at position (complex)
arr=("${arr[@]:0:2}" "inserted" "${arr[@]:2}")

# Remove element by index
unset 'arr[2]'

# Remove by value (all occurrences)
arr_new=()
for item in "${arr[@]}"; do
    [[ "$item" != "second" ]] && arr_new+=("$item")
done
arr=("${arr_new[@]}")

# Check if empty
if [[ ${#arr[@]} -eq 0 ]]; then
    echo "Array is empty"
fi

# Check if element exists
contains() {
    local needle="$1"
    shift
    local item
    for item in "$@"; do
        [[ "$item" == "$needle" ]] && return 0
    done
    return 1
}

if contains "third" "${arr[@]}"; then
    echo "Found 'third'"
fi
```

### Array Transformation

```bash
#!/usr/bin/env bash
set -euo pipefail

arr=("apple" "banana" "cherry" "date")

# Map (transform each element)
upper_arr=()
for item in "${arr[@]}"; do
    upper_arr+=("${item^^}")  # Uppercase
done

# Filter
filtered=()
for item in "${arr[@]}"; do
    [[ ${#item} -gt 5 ]] && filtered+=("$item")
done

# Join array to string
IFS=','
joined="${arr[*]}"
unset IFS
echo "$joined"  # apple,banana,cherry,date

# Split string to array
IFS=',' read -ra split_arr <<< "one,two,three"

# Unique values
declare -A seen
unique=()
for item in "${arr[@]}"; do
    if [[ -z "${seen[$item]:-}" ]]; then
        seen[$item]=1
        unique+=("$item")
    fi
done

# Sort array
readarray -t sorted < <(printf '%s\n' "${arr[@]}" | sort)

# Reverse array
reversed=()
for ((i=${#arr[@]}-1; i>=0; i--)); do
    reversed+=("${arr[$i]}")
done

# Or using tac
readarray -t reversed < <(printf '%s\n' "${arr[@]}" | tac)
```

## Associative Arrays (Bash 4+)

### Declaration and Usage

```bash
#!/usr/bin/env bash
set -euo pipefail

# MUST declare with -A
declare -A config

# Assignment
config["host"]="localhost"
config["port"]="8080"
config["debug"]="true"

# Or compound assignment
declare -A user=(
    [name]="John Doe"
    [email]="john@example.com"
    [role]="admin"
)

# Access
echo "Host: ${config[host]}"
echo "User: ${user[name]}"

# Default value if key missing
echo "${config[missing]:-default}"

# Check if key exists
if [[ -v config[host] ]]; then
    echo "Host is set"
fi

# Alternative check
if [[ -n "${config[host]+x}" ]]; then
    echo "Host key exists (even if empty)"
fi

# All keys
echo "Keys: ${!config[@]}"

# All values
echo "Values: ${config[@]}"

# Length (number of keys)
echo "Size: ${#config[@]}"

# Iterate
for key in "${!config[@]}"; do
    echo "$key = ${config[$key]}"
done

# Delete key
unset 'config[debug]'

# Clear entire array
config=()
```

### Real-World Associative Array Patterns

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration parser
parse_config() {
    local config_file="$1"
    declare -gA CONFIG  # Global associative array

    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$key" ]] && continue

        # Trim whitespace
        key="${key//[[:space:]]/}"
        value="${value#"${value%%[![:space:]]*}"}"  # Left trim
        value="${value%"${value##*[![:space:]]}"}"  # Right trim

        CONFIG["$key"]="$value"
    done < "$config_file"
}

# Usage
parse_config "/etc/myapp.conf"
echo "Database: ${CONFIG[database]:-not set}"

# Counter/frequency map
count_words() {
    local file="$1"
    declare -A word_count

    while read -ra words; do
        for word in "${words[@]}"; do
            # Normalize: lowercase, remove punctuation
            word="${word,,}"
            word="${word//[^a-z]/}"
            [[ -n "$word" ]] && ((word_count[$word]++))
        done
    done < "$file"

    # Print sorted by count
    for word in "${!word_count[@]}"; do
        echo "${word_count[$word]} $word"
    done | sort -rn | head -10
}

# Caching pattern
declare -A CACHE

cached_expensive_operation() {
    local key="$1"

    # Check cache
    if [[ -n "${CACHE[$key]+x}" ]]; then
        echo "${CACHE[$key]}"
        return 0
    fi

    # Compute and cache
    local result
    result=$(expensive_computation "$key")
    CACHE["$key"]="$result"
    echo "$result"
}

# JSON-like nested data (using delimited keys)
declare -A data
data["user.name"]="John"
data["user.email"]="john@example.com"
data["user.address.city"]="NYC"
data["user.address.zip"]="10001"

# Access nested
echo "City: ${data[user.address.city]}"
```

## mapfile / readarray (Bash 4+)

### Basic Usage

```bash
#!/usr/bin/env bash
set -euo pipefail

# Read file into array (each line = element)
mapfile -t lines < file.txt
# Or equivalently:
readarray -t lines < file.txt

# -t removes trailing newlines
# Without -t, each element includes \n

# Process each line
for line in "${lines[@]}"; do
    echo "Line: $line"
done

# Read from command output
mapfile -t files < <(find . -name "*.sh")

# Read from here-doc
mapfile -t data <<'EOF'
line1
line2
line3
EOF
```

### Advanced mapfile Options

```bash
#!/usr/bin/env bash
set -euo pipefail

# -n COUNT: Read at most COUNT lines
mapfile -t -n 10 first_10 < large_file.txt

# -s COUNT: Skip first COUNT lines
mapfile -t -s 1 skip_header < data.csv  # Skip header row

# -O INDEX: Start at INDEX instead of 0
existing_array=("a" "b")
mapfile -t -O "${#existing_array[@]}" existing_array < more_data.txt

# -d DELIM: Use DELIM instead of newline (Bash 4.4+)
# Read NUL-delimited data (safe for filenames with newlines)
mapfile -t -d '' files < <(find . -name "*.txt" -print0)

# -C CALLBACK: Execute callback every QUANTUM lines
# -c QUANTUM: Number of lines between callbacks (default 5000)
process_chunk() {
    local index=$1
    echo "Processing lines around index $index" >&2
}
export -f process_chunk
mapfile -t -c 1000 -C process_chunk lines < huge_file.txt
```

### CSV Processing with mapfile

```bash
#!/usr/bin/env bash
set -euo pipefail

# Parse CSV file
parse_csv() {
    local csv_file="$1"
    local -n result_array="$2"  # nameref (Bash 4.3+)

    while IFS=',' read -ra row; do
        result_array+=("${row[*]}")  # Store as delimited string
    done < "$csv_file"
}

# Better: Store as 2D array simulation
declare -A csv_data
row_num=0

while IFS=',' read -ra fields; do
    for col_num in "${!fields[@]}"; do
        csv_data["$row_num,$col_num"]="${fields[$col_num]}"
    done
    ((row_num++))
done < data.csv

# Access cell
echo "Row 2, Col 3: ${csv_data[2,3]}"
```

## Performance Patterns

### Efficient Array Building

```bash
#!/usr/bin/env bash
set -euo pipefail

# ✗ SLOW - Command substitution in loop
slow_build() {
    local arr=()
    for i in {1..1000}; do
        arr+=("$(echo "$i")")  # Subshell for each!
    done
}

# ✓ FAST - Direct assignment
fast_build() {
    local arr=()
    for i in {1..1000}; do
        arr+=("$i")  # No subshell
    done
}

# ✓ FASTEST - mapfile for file data
fastest_file_read() {
    mapfile -t arr < file.txt
}
```

### Avoid Subshells in Loops

```bash
#!/usr/bin/env bash
set -euo pipefail

# ✗ SLOW - Subshell each iteration
slow_process() {
    local sum=0
    for num in "${numbers[@]}"; do
        result=$(echo "$num * 2" | bc)  # Subshell!
        ((sum += result))
    done
}

# ✓ FAST - Bash arithmetic
fast_process() {
    local sum=0
    for num in "${numbers[@]}"; do
        ((sum += num * 2))
    done
}

# ✓ FAST - Process substitution for parallel reads
while read -r line1 <&3 && read -r line2 <&4; do
    echo "$line1 | $line2"
done 3< <(command1) 4< <(command2)
```

### Large Array Operations

```bash
#!/usr/bin/env bash
set -euo pipefail

# For very large arrays, consider:
# 1. Process in chunks
# 2. Use external tools (awk, sort)
# 3. Stream processing instead of loading all

# Chunk processing
process_in_chunks() {
    local -n arr="$1"
    local chunk_size="${2:-1000}"
    local len="${#arr[@]}"

    for ((i=0; i<len; i+=chunk_size)); do
        local chunk=("${arr[@]:i:chunk_size}")
        process_chunk "${chunk[@]}"
    done
}

# Stream processing (memory efficient)
# Instead of:
#   mapfile -t all_lines < huge_file.txt
#   process "${all_lines[@]}"
# Use:
while IFS= read -r line; do
    process_line "$line"
done < huge_file.txt
```

## Bash 5.3+ Array Features

### Enhanced Array Subscripts

```bash
#!/usr/bin/env bash
# Requires Bash 5.2+

set -euo pipefail

declare -A config

# Subscript expressions evaluated once (5.2+)
key="host"
config[$key]="localhost"  # Evaluated correctly

# '@' and '*' subscripts for associative arrays
# Can now unset just the key '@' instead of entire array
declare -A special
special[@]="at sign value"
special[*]="asterisk value"
special[normal]="normal value"

# Unset specific key (Bash 5.2+)
unset 'special[@]'  # Only removes '@' key, not whole array
```

### GLOBSORT with Arrays

```bash
#!/usr/bin/env bash
# Requires Bash 5.3

set -euo pipefail

# Sort glob results by modification time (newest first)
GLOBSORT="-mtime"
recent_files=(*.txt)

# Sort by size
GLOBSORT="size"
files_by_size=(*.log)

# Reset to default (alphabetical)
GLOBSORT="name"
```

## Common Array Patterns

### Stack Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

declare -a STACK=()

push() {
    STACK+=("$1")
}

pop() {
    if [[ ${#STACK[@]} -eq 0 ]]; then
        echo "Stack empty" >&2
        return 1
    fi
    echo "${STACK[-1]}"
    unset 'STACK[-1]'
}

peek() {
    if [[ ${#STACK[@]} -gt 0 ]]; then
        echo "${STACK[-1]}"
    fi
}

# Usage
push "first"
push "second"
push "third"
echo "Top: $(peek)"     # third
echo "Pop: $(pop)"      # third
echo "Pop: $(pop)"      # second
```

### Queue Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

declare -a QUEUE=()

enqueue() {
    QUEUE+=("$1")
}

dequeue() {
    if [[ ${#QUEUE[@]} -eq 0 ]]; then
        echo "Queue empty" >&2
        return 1
    fi
    echo "${QUEUE[0]}"
    QUEUE=("${QUEUE[@]:1}")
}

# Usage
enqueue "task1"
enqueue "task2"
enqueue "task3"
echo "Next: $(dequeue)"  # task1
echo "Next: $(dequeue)"  # task2
```

### Set Operations

```bash
#!/usr/bin/env bash
set -euo pipefail

# Union
array_union() {
    local -n arr1="$1"
    local -n arr2="$2"
    local -A seen
    local result=()

    for item in "${arr1[@]}" "${arr2[@]}"; do
        if [[ -z "${seen[$item]:-}" ]]; then
            seen[$item]=1
            result+=("$item")
        fi
    done

    printf '%s\n' "${result[@]}"
}

# Intersection
array_intersection() {
    local -n arr1="$1"
    local -n arr2="$2"
    local -A set1
    local result=()

    for item in "${arr1[@]}"; do
        set1[$item]=1
    done

    for item in "${arr2[@]}"; do
        if [[ -n "${set1[$item]:-}" ]]; then
            result+=("$item")
        fi
    done

    printf '%s\n' "${result[@]}"
}

# Difference (arr1 - arr2)
array_difference() {
    local -n arr1="$1"
    local -n arr2="$2"
    local -A set2
    local result=()

    for item in "${arr2[@]}"; do
        set2[$item]=1
    done

    for item in "${arr1[@]}"; do
        if [[ -z "${set2[$item]:-}" ]]; then
            result+=("$item")
        fi
    done

    printf '%s\n' "${result[@]}"
}
```

## Resources

- [Bash Arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html)
- [BashFAQ/005 - Arrays](https://mywiki.wooledge.org/BashFAQ/005)
- [Bash Hackers - Arrays](https://wiki.bash-hackers.org/syntax/arrays)

---

**Master bash arrays for efficient data manipulation and avoid common pitfalls like word splitting and subshell overhead.**
