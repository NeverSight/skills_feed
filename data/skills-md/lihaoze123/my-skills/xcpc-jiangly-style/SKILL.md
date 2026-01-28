---
name: xcpc-jiangly-style
description: Use when writing C++ competitive programming solutions for Codeforces, ICPC, or similar contests. Apply when creating XCPC solutions to ensure code follows jiangly's proven style patterns.
license: MIT
metadata:
  author: chumeng
  version: "2.1.0"
  source: jiangly Codeforces submissions
---

# XCPC: jiangly C++ Style

## Overview

Proven C++ coding style from jiangly's Codeforces submissions. Focuses on safety, maintainability, and modern C++ features for competitive programming.

**Core principle:** Zero global pollution, zero global arrays, explicit types, modern C++.

## When to Use

- Writing C++ solutions for Codeforces, ICPC, AtCoder, etc.
- Creating competitive programming templates
- Reviewing contest solutions
- Teaching competitive programming best practices

**Don't use for:**
- Production C++ code (different requirements)
- Non-competitive programming projects

## Quick Reference

| Category | Rule | File |
|----------|------|------|
| Namespace | Never `using namespace std;` | [no-global-namespace](rules/no-global-namespace.md) |
| Arrays | Zero global arrays | [zero-global-arrays](rules/zero-global-arrays.md) |
| Types | Use `using i64 = long long;` | [explicit-types](rules/explicit-types.md) |
| Indexing | Follow problem's natural indexing | [keep-indexing-consistent](rules/keep-indexing-consistent.md) |
| I/O | Disable sync, use `\n` | [fast-io](rules/fast-io.md) |
| Naming | `snake_case` for vars, `PascalCase` for structs | [naming](rules/naming.md) |
| Formatting | 4-space indent, K&R braces, no line compression | [formatting](rules/formatting.md) |
| Simplicity | Prefer simple data structures | [simplicity-first](rules/simplicity-first.md) |
| Memory | Use in-place operations | [in-place-operations](rules/in-place-operations.md) |
| DFS | Use depth array, avoid parent parameter | [dfs-techniques](rules/dfs-techniques.md) |
| Recursion | Lambda + self pattern | [recursion](rules/recursion.md) |
| Structs | Constructor patterns, const correctness | [struct-patterns](rules/struct-patterns.md) |
| Operators | Overload patterns for custom types | [operator-overloading](rules/operator-overloading.md) |
| Helpers | chmax, ceilDiv, gcd, power, etc. | [helper-functions](rules/helper-functions.md) |
| DP | Use `vector`, never `memset` | [dp-patterns](rules/dp-patterns.md) |
| Modern C++ | CTAD, structured binding, C++20 features | [modern-cpp-features](rules/modern-cpp-features.md) |

## Code Template

```cpp
#include <bits/stdc++.h>

using i64 = long long;

void solve() {
    int n;
    std::cin >> n;

    std::vector<int> a(n);
    for (int i = 0; i < n; i++) {
        std::cin >> a[i];
    }

    std::cout << ans << "\n";
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    std::cin >> t;

    while (t--) {
        solve();
    }

    return 0;
}
```

## Red Flags - STOP

| Anti-pattern | Correct approach |
|--------------|------------------|
| `using namespace std;` | Use `std::` prefix |
| `int a[100005];` global | `std::vector<int> a(n);` in solve() |
| `#define int long long` | `using i64 = long long;` |
| `for (int i = 1; i <= n; i++)` | `for (int i = 0; i < n; i++)` **OR** keep problem's indexing |
| `void dfs(int u, int p)` global | Lambda with self capture |
| `std::endl` | Use `"\n"` |
| `if (x) do_something();` | Always use braces |
| **Over-engineered** HLD + segment tree | Use binary lifting for simple path queries |
| **Creating** `e1, e2` containers | Use `vis` boolean array |
| **Converting** 1-indexed to 0-indexed | Keep original indexing |
| **Passing** parent in DFS | Use depth array to check visited |
| **Explicit** template parameters | Use CTAD where possible |

## Full Documentation

For complete details on all rules: [AGENTS.md](AGENTS.md)
