---
name: cpp
description: >
  Modern C++ best practices with C++17/20 features.
  Trigger: When writing C++ code with modern standards.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with cpp"

## When to Use

Use this skill when:
- Writing C++17/20 code
- Managing memory with smart pointers
- Using STL containers and algorithms
- Implementing RAII patterns

---

## Critical Patterns

### Smart Pointers (REQUIRED)

```cpp
// ✅ ALWAYS: Use smart pointers
auto user = std::make_unique<User>("John");
auto shared = std::make_shared<Config>();

// ❌ NEVER: Raw new/delete
User* user = new User("John");
delete user;
```

### RAII (REQUIRED)

```cpp
// ✅ ALWAYS: Resource management through constructors/destructors
class FileHandle {
    std::fstream file_;
public:
    FileHandle(const std::string& path) : file_(path) {}
    ~FileHandle() { if (file_.is_open()) file_.close(); }
};
```

### Modern Patterns (REQUIRED)

```cpp
// ✅ Use auto for type deduction
auto items = std::vector<int>{1, 2, 3};

// ✅ Use range-based for loops
for (const auto& item : items) {
    process(item);
}

// ✅ Use structured bindings
auto [name, age] = getPerson();
```

---

## Decision Tree

```
Need unique ownership?     → std::unique_ptr
Need shared ownership?     → std::shared_ptr
Need optional value?       → std::optional
Need multiple types?       → std::variant
Need string views?         → std::string_view
```

---

## Commands

```bash
g++ -std=c++20 -Wall -Wextra main.cpp -o app
clang++ -std=c++20 main.cpp -o app
cmake -B build && cmake --build build
```
