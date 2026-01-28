---
name: ruby
description: >
  Ruby best practices for clean code and Rails development.
  Trigger: When writing Ruby code or Rails applications.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with ruby"

## When to Use

Use this skill when:
- Writing Ruby applications
- Developing Ruby on Rails apps
- Following Ruby style conventions
- Writing RSpec tests

---

## Critical Patterns

### Ruby Idioms (REQUIRED)

```ruby
# ✅ ALWAYS: Use Ruby idioms
users.map(&:name)                    # Symbol to proc
user&.address&.city                  # Safe navigation
name ||= "Default"                   # Memoization
```

### Class Structure (REQUIRED)

```ruby
# ✅ ALWAYS: Clear class structure
class User
  attr_reader :name, :email
  
  def initialize(name:, email:)
    @name = name
    @email = email
  end
  
  def admin?
    role == 'admin'
  end
end
```

### Error Handling (REQUIRED)

```ruby
# ✅ Use custom exceptions
class UserNotFoundError < StandardError; end

def find_user!(id)
  user = User.find_by(id: id)
  raise UserNotFoundError, "User #{id} not found" unless user
  user
end
```

---

## Decision Tree

```
Need attribute access?     → Use attr_reader/writer
Need boolean check?        → Use predicate method (?)
Need dangerous operation?  → Use bang method (!)
Need configuration?        → Use block with yield
```

---

## Commands

```bash
ruby script.rb             # Run script
irb                        # Interactive Ruby
bundle install             # Install dependencies
rspec                      # Run tests
rubocop                    # Lint code
```

---

## Resources

- **Clean Code**: [clean-code.md](clean-code.md)
- **TDD with RSpec**: [tdd-rspec.md](tdd-rspec.md)
