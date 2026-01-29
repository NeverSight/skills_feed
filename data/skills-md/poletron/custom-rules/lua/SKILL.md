---
name: lua
description: >
  Lua scripting best practices for games and embedded systems.
  Trigger: When writing Lua scripts or game development.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with lua"

## When to Use

Use this skill when:
- Writing Lua scripts
- Developing games with Lua
- Embedding Lua in applications
- Configuring systems with Lua

---

## Critical Patterns

### Table Patterns (REQUIRED)

```lua
-- ✅ ALWAYS: Use tables for structured data
local user = {
    name = "John",
    age = 30,
    greet = function(self)
        print("Hello, " .. self.name)
    end
}

user:greet()  -- method call with self
```

### Module Pattern (REQUIRED)

```lua
-- ✅ ALWAYS: Return table for modules
local M = {}

function M.process(data)
    return data:upper()
end

return M
```

### Error Handling (REQUIRED)

```lua
-- ✅ Use pcall for protected calls
local ok, result = pcall(function()
    return risky_operation()
end)

if not ok then
    print("Error: " .. result)
end
```

---

## Decision Tree

```
Need class-like?           → Use metatables
Need error handling?       → Use pcall/xpcall
Need iteration?            → Use pairs/ipairs
Need configuration?        → Use external .lua files
```

---

## Commands

```bash
lua script.lua             # Run script
luac -o out.luac script.lua  # Compile
luarocks install package   # Install package
```

---

## Resources

- **Best Practices**: [best-practices.md](best-practices.md)
- **Performance**: [performance.md](performance.md)
- **Scripting**: [scripting.md](scripting.md)
