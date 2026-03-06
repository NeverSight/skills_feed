---
name: cpp
description: Write modern C++ with RAII, smart pointers, and STL. Use for C++ development, memory safety, or performance optimization.
---

# C++ Development

Write safe, performant modern C++ code.

## When to Use

- Writing C++ code
- Memory management issues
- Template metaprogramming
- Performance optimization
- Legacy C++ modernization

## Modern C++ Patterns

### Smart Pointers

```cpp
// Unique ownership
auto ptr = std::make_unique<Resource>();
process(std::move(ptr));

// Shared ownership
auto shared = std::make_shared<Resource>();
auto copy = shared;  // Reference count: 2

// Weak reference (no ownership)
std::weak_ptr<Resource> weak = shared;
if (auto locked = weak.lock()) {
    // Use locked
}
```

### RAII

```cpp
class FileHandle {
    FILE* handle_;
public:
    explicit FileHandle(const char* path)
        : handle_(fopen(path, "r")) {
        if (!handle_) throw std::runtime_error("Failed to open");
    }
    ~FileHandle() { if (handle_) fclose(handle_); }

    // Rule of 5
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& other) noexcept
        : handle_(std::exchange(other.handle_, nullptr)) {}
    FileHandle& operator=(FileHandle&& other) noexcept {
        std::swap(handle_, other.handle_);
        return *this;
    }
};
```

### Containers and Algorithms

```cpp
std::vector<int> nums = {3, 1, 4, 1, 5};

// Prefer algorithms over raw loops
std::sort(nums.begin(), nums.end());

auto it = std::find_if(nums.begin(), nums.end(),
    [](int n) { return n > 3; });

// Range-based for
for (const auto& num : nums) {
    std::cout << num << '\n';
}

// Structured bindings (C++17)
std::map<std::string, int> scores;
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << '\n';
}
```

### Templates

```cpp
// Concepts (C++20)
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T sum(const std::vector<T>& values) {
    return std::accumulate(values.begin(), values.end(), T{});
}

// SFINAE (pre-C++20)
template<typename T,
    typename = std::enable_if_t<std::is_arithmetic_v<T>>>
T multiply(T a, T b) { return a * b; }
```

## Best Practices

- Prefer `const` and `constexpr`
- Use smart pointers over raw pointers
- Follow Rule of 0/5
- Prefer STL algorithms
- Use `std::string_view` for read-only strings
- Enable warnings: `-Wall -Wextra -Wpedantic`

## Common Issues

| Issue           | Symptom            | Fix                  |
| --------------- | ------------------ | -------------------- |
| Memory leak     | Growing memory     | Use smart pointers   |
| Dangling ptr    | Crash/UB           | Check lifetime       |
| Buffer overflow | Crash/security     | Use std::vector/span |
| Data race       | Inconsistent state | mutex/atomic         |

## Examples

**Input:** "Fix memory leak"
**Action:** Replace raw pointers with smart pointers, ensure RAII

**Input:** "Modernize this C++ code"
**Action:** Apply C++17/20 features, use STL, improve safety
