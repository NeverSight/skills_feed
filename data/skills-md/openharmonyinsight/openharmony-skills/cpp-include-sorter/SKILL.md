---
name: cpp-include-sorter
description: Automatically sorts C/C++ header files (#include statements) with full support for conditional compilation blocks. Use when Claude needs to organize #include statements in .cpp/.h files. Handles: (1) Corresponding header placement first (e.g., file.cpp includes file.h), (2) System headers (<>) sorted alphabetically, (3) Local headers ("") sorted alphabetically, (4) Conditional compilation blocks (#ifdef/#ifndef/#if defined) where headers participate in global sort while preserving block structure. Key features: prefers longer paths for duplicate includes, preserves inline/preceding comments, handles #elif/#else blocks, validates no headers are lost.
---

# C/C++ Include Sorter

Automatically sorts `#include` statements in C/C++ source files with intelligent handling of conditional compilation blocks.

## Quick Start

Sort all `.cpp` files in a directory:

```bash
python scripts/sort_includes.py <directory-path>
```

Preview changes without modifying files:

```bash
python scripts/sort_includes.py <directory-path> --dry-run
```

## Sorting Rules

Includes are organized into **3 categories** with blank lines between each group:

1. **Corresponding header** - For `file.cpp`, `file.h` is placed first (prefers longest path if duplicates exist)
2. **System headers** - Headers with angle brackets `<>` (sorted alphabetically)
3. **Local headers** - Headers with double quotes `""` (sorted alphabetically)

### Conditional Compilation Blocks

`#ifdef`/`#ifndef`/`#if defined` blocks are treated as units:

- Blocks participate in global sorting based on their first include
- Headers **inside** each block are also sorted (system headers first, then local headers)
- Block structure (`#ifdef`...`#endif`) is preserved
- `#elif` and `#else` blocks are supported

## Example

**Before:**
```cpp
#include "common/rs_log.h"
#include "rs_trace.h"
#include <memory>
#ifdef RS_ENABLE_GPU
#include "feature/uifirst/rs_sub_thread_manager.h"
#include "feature/capture/rs_ui_capture_task_parallel.h"
#endif
#include "platform/common/rs_system_properties.h"
```

**After:**
```cpp
#include "rs_trace.h"        // 1. Corresponding header (longest path preferred)

#include <memory>             // 2. System headers (alphabetical)

#include "common/rs_log.h"    // 3. Local headers (alphabetical)
#ifdef RS_ENABLE_GPU
#include "feature/capture/rs_ui_capture_task_parallel.h"
#include "feature/uifirst/rs_sub_thread_manager.h"
#endif
#include "platform/common/rs_system_properties.h"
```

## Features

- **Duplicate include handling**: When multiple includes with same filename but different paths exist (e.g., `"file.h"` and `"path/to/file.h"`), the longest path is used as the corresponding header and placed first
- **Comment preservation**: Inline comments (`// comment`) and preceding comments are preserved
- **Nested conditional blocks**: Handles `#elif` and `#else` within `#ifdef` blocks
- **Validation**: Verifies no headers are lost during sorting

## Script Reference

See `scripts/sort_includes.py` for implementation details.

Key functions:
- `extract_includes_with_ifdef()` - Parses includes and conditional blocks
- `sort_includes_with_ifdef()` - Sorts with 3-category rule
- `format_ifdef_block()` - Formats conditional blocks with sorted includes

## Verification

After sorting, verify:
1. All `#ifdef` blocks contain same number of headers as before
2. Corresponding header has complete path (not shortened)
3. Total include count unchanged
4. Comments preserved

Use `git diff` to compare before/after:
```bash
git diff <file.cpp> | grep "^[-+]" | grep "include"
```
