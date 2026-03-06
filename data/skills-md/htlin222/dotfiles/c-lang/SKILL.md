---
name: c-lang
description: Write efficient C code with proper memory management and system calls. Use for C optimization, memory issues, or system programming.
---

# C Development

Write safe, efficient C code for systems programming.

## When to use

- Writing C code
- Memory management issues
- System programming
- Embedded systems
- Performance-critical code

## Memory management

### Allocation patterns

```c
// Always check malloc
void* ptr = malloc(size);
if (ptr == NULL) {
    fprintf(stderr, "malloc failed\n");
    return -1;
}

// Pair malloc with free
char* buffer = malloc(1024);
// ... use buffer ...
free(buffer);
buffer = NULL;  // Prevent use-after-free

// Use calloc for zero-initialized memory
int* array = calloc(count, sizeof(int));

// Realloc safely
void* new_ptr = realloc(ptr, new_size);
if (new_ptr == NULL) {
    free(ptr);  // Original still valid on failure
    return -1;
}
ptr = new_ptr;
```

### Common patterns

```c
// RAII-style cleanup with goto
int process_file(const char* path) {
    int result = -1;
    FILE* fp = NULL;
    char* buffer = NULL;

    fp = fopen(path, "r");
    if (!fp) goto cleanup;

    buffer = malloc(1024);
    if (!buffer) goto cleanup;

    // ... process ...
    result = 0;

cleanup:
    free(buffer);
    if (fp) fclose(fp);
    return result;
}
```

## Data structures

```c
// Linked list node
typedef struct Node {
    void* data;
    struct Node* next;
} Node;

// Dynamic array
typedef struct {
    void** items;
    size_t count;
    size_t capacity;
} DynArray;

int dynarray_push(DynArray* arr, void* item) {
    if (arr->count >= arr->capacity) {
        size_t new_cap = arr->capacity ? arr->capacity * 2 : 8;
        void** new_items = realloc(arr->items, new_cap * sizeof(void*));
        if (!new_items) return -1;
        arr->items = new_items;
        arr->capacity = new_cap;
    }
    arr->items[arr->count++] = item;
    return 0;
}
```

## Error handling

```c
// Check all system calls
int fd = open(path, O_RDONLY);
if (fd == -1) {
    perror("open");
    return -1;
}

ssize_t n = read(fd, buf, sizeof(buf));
if (n == -1) {
    perror("read");
    close(fd);
    return -1;
}
```

## Debugging

```bash
# Compile with debug symbols
gcc -g -Wall -Wextra -Werror -o prog prog.c

# Run with valgrind
valgrind --leak-check=full ./prog

# GDB debugging
gdb ./prog
(gdb) break main
(gdb) run
(gdb) print variable
(gdb) backtrace
```

## Best practices

- Check all return values
- Initialize all variables
- Use `const` where possible
- Prefer stack over heap when size is known
- Use `-Wall -Wextra -Werror` flags

## Examples

**Input:** "Fix memory leak"
**Action:** Run valgrind, trace allocation, ensure every malloc has free

**Input:** "Optimize this C code"
**Action:** Profile with perf, identify hotspots, optimize critical path
