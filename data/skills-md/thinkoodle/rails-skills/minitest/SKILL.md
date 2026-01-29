---
name: minitest
description: Expert guidance for writing fast, maintainable Minitest tests in Rails applications. Use when writing tests, converting from RSpec, debugging test failures, improving test performance, or following testing best practices. Covers model tests, policy tests, request tests, system tests, fixtures, and TDD workflows.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(bin/rails test:*), Bash(bin/rails test), Bash(bundle exec rails test:*)
---

# Rails Minitest Expert

Write performant, maintainable, and non-brittle tests for Rails applications using Minitest and fixtures.

## Philosophy

**Core Principles:**
1. **Test behavior, not implementation** - Focus on WHAT code does, not HOW
2. **Fast feedback loops** - Prefer unit tests over integration tests, fixtures over factories
3. **Tests as documentation** - Test names should describe expected behavior
4. **Minimal test data** - Create only what's necessary; 2 records == many records
5. **Non-brittle assertions** - Test outcomes, not exact values that may change

**Testing Pyramid:**
```
    /\     System Tests (Few - critical paths only)
   /  \    
  /____\   Request/Integration Tests (Some)
 /      \  
/________\ Unit Tests (Many - models, policies, services)
```

## When To Use This Skill

- Writing new Minitest tests for Rails models, policies, controllers, or requests
- Converting RSpec tests to Minitest
- Debugging slow or flaky tests
- Improving test suite performance
- Following Rails testing conventions
- Writing fixture-based test data
- Implementing TDD workflows

## Instructions

### Step 1: Identify Test Type

Before writing, determine the appropriate test type:

| Test Type | Location | Use For |
|-----------|----------|---------|
| Model | `test/models/` | Validations, associations, business logic methods |
| Policy | `test/policies/` | Pundit authorization policies |
| Request | `test/requests/` | Full HTTP request/response cycle |
| Controller | `test/controllers/` | Controller actions (prefer request tests) |
| System | `test/system/` | Critical user flows with real browser |
| Service | `test/services/` | Service objects and complex operations |
| Job | `test/jobs/` | Background job behavior |
| Mailer | `test/mailers/` | Email content and delivery |

### Step 2: Check Existing Patterns

**ALWAYS search for existing tests first:**

```bash
# Find similar test files
rg "class.*Test < " test/

# Find existing fixtures
ls test/fixtures/

# Check for test helpers
cat test/test_helper.rb
cat test/support/*.rb
```

**Match existing project conventions** - consistency is more important than "best" patterns.

### Step 3: Use Fixtures (Not Factories)

**Fixtures are 10-100x faster than Factory Bot.**

```ruby
# AVOID - Factory Bot (slow, implicit)
let(:user) { create(:user) }
let(:project) { create(:project, workspace: workspace) }

# PREFER - Fixtures (fast, explicit)
setup do
  @workspace = workspaces(:main_workspace)
  @user = users(:admin_user)
  @project = projects(:active_project)
end
```

**Fixture Best Practices:**
- Create purpose-specific fixtures with descriptive names
- Use `<%= %>` for dynamic values and UUIDs
- Reference associations by fixture name, not ID
- Keep fixtures minimal - only include required attributes

```yaml
# test/fixtures/users.yml
admin_user:
  id: <%= Digest::UUID.uuid_v5(Digest::UUID::OID_NAMESPACE, "admin_user") %>
  email: "admin@example.com"
  name: "Admin User"
  created_at: <%= 1.week.ago %>

member_user:
  id: <%= Digest::UUID.uuid_v5(Digest::UUID::OID_NAMESPACE, "member_user") %>
  email: "member@example.com"
  name: "Member User"
  workspace: main_workspace  # Reference by fixture name
```

### Step 4: Write Test Structure

**Standard Test Structure:**

```ruby
require "test_helper"

class ModelTest < ActiveSupport::TestCase
  setup do
    # Load fixtures - MINIMAL setup only
    @record = models(:fixture_name)
  end

  # Group related tests with comments or test naming
  
  # Validation tests
  test "requires name" do
    @record.name = nil
    refute @record.valid?
    assert_includes @record.errors[:name], "can't be blank"
  end

  # Method tests
  test "#full_name returns formatted name" do
    @record.first_name = "John"
    @record.last_name = "Doe"
    assert_equal "John Doe", @record.full_name
  end
end
```

### Step 5: Follow Performance Guidelines

**Avoid Database When Possible:**

```ruby
# SLOW - Creates database records
test "validates email format" do
  user = User.create!(email: "invalid", name: "Test")
  refute user.valid?
end

# FAST - Uses in-memory object
test "validates email format" do
  user = User.new(email: "invalid", name: "Test")
  refute user.valid?
end
```

**Minimize Records Created:**

```ruby
# SLOW - Creates 25 records
test "paginates results" do
  create_list(:post, 25)
  # ...
end

# FAST - Configure pagination threshold for tests
# config/environments/test.rb: Pagy::DEFAULT[:limit] = 2
test "paginates results" do
  # Only need 3 records to test pagination with limit of 2
  assert_operator posts.count, :>=, 3
  # ...
end
```

**Avoid Browser Tests When Possible:**

```ruby
# SLOW - Full browser simulation
class PostsSystemTest < ApplicationSystemTestCase
  test "creates a post" do
    visit new_post_path
    fill_in "Title", with: "Test"
    click_on "Create"
    assert_text "Post created"
  end
end

# FAST - Request test (no browser)
class PostsRequestTest < ActionDispatch::IntegrationTest
  test "creates a post" do
    post posts_path, params: { post: { title: "Test" } }
    assert_response :redirect
    follow_redirect!
    assert_response :success
  end
end
```

### Step 6: Write Non-Brittle Assertions

**Test Behavior, Not Exact Values:**

```ruby
# BRITTLE - Exact timestamp match
assert_equal "2025-01-15T10:00:00Z", response["created_at"]

# ROBUST - Just verify presence
assert response["created_at"].present?

# BRITTLE - Exact error message
assert_equal "Name can't be blank", record.errors.full_messages.first

# ROBUST - Check for key content
assert_includes record.errors[:name], "can't be blank"
```

**Use Inclusive Assertions:**

```ruby
# BRITTLE - Exact match
assert_equal({ id: 1, name: "Test", email: "test@example.com" }, response)

# ROBUST - Check key attributes only
assert_equal 1, response[:id]
assert_equal "Test", response[:name]
# OR
assert response.slice(:id, :name) == { id: 1, name: "Test" }
```

### Step 7: Handle Multi-Tenancy

**For acts_as_tenant projects, always wrap in tenant context:**

```ruby
# WRONG - Missing tenant context
test "admin can view project" do
  assert policy(@admin, @project).show?
end

# CORRECT - Proper tenant scoping
test "admin can view project" do
  with_workspace(@workspace) do
    assert policy(@admin, @project).show?
  end
end
```

### Step 8: Test Permission Flows Correctly

**Always test denial BEFORE granting, then allow AFTER:**

```ruby
test "member requires permission to create" do
  with_workspace(@workspace) do
    # 1. Test denial WITHOUT permission
    refute policy(@member, Project).create?
    
    # 2. Grant permission
    set_workspace_permissions(@member, @workspace, :allowed_to_create_projects)
    
    # 3. Test allow WITH permission
    assert policy(@member, Project).create?
  end
end
```

## Quick Reference

### Assertion Mapping (RSpec to Minitest)

| RSpec | Minitest |
|-------|----------|
| `expect(x).to eq(y)` | `assert_equal y, x` |
| `expect(x).to be_truthy` | `assert x` |
| `expect(x).to be_falsey` | `refute x` |
| `expect(x).to be_nil` | `assert_nil x` |
| `expect(arr).to include(x)` | `assert_includes arr, x` |
| `expect(arr).not_to include(x)` | `refute_includes arr, x` |
| `expect { }.to change { X.count }.by(1)` | `assert_difference "X.count", 1 do ... end` |
| `expect { }.to raise_error(E)` | `assert_raises(E) { ... }` |
| `expect(x).to be_valid` | `assert x.valid?` |
| `expect(x).not_to be_valid` | `refute x.valid?` |
| `expect(x).to match(/pattern/)` | `assert_match /pattern/, x` |

### Rails-Specific Assertions

```ruby
# Record changes
assert_difference "Post.count", 1 do
  Post.create!(title: "Test")
end

assert_no_difference "Post.count" do
  Post.new.save  # Invalid, doesn't save
end

# Value changes
assert_changes -> { post.reload.title }, from: "Old", to: "New" do
  post.update!(title: "New")
end

# Response assertions
assert_response :success
assert_response :redirect
assert_redirected_to post_path(post)

# DOM assertions
assert_select "h1", "Expected Title"
assert_select ".post", count: 3

# Query assertions
assert_queries_count(2) { User.find(1); User.find(2) }
assert_no_queries { cached_value }
```

### Test File Templates

**Model Test:**
```ruby
require "test_helper"

class UserTest < ActiveSupport::TestCase
  setup do
    @user = users(:active_user)
  end

  test "valid fixture" do
    assert @user.valid?
  end

  test "requires email" do
    @user.email = nil
    refute @user.valid?
    assert_includes @user.errors[:email], "can't be blank"
  end

  test "#display_name returns formatted name" do
    @user.name = "John Doe"
    assert_equal "John Doe", @user.display_name
  end
end
```

**Request Test:**
```ruby
require "test_helper"

class PostsRequestTest < ActionDispatch::IntegrationTest
  setup do
    @user = users(:active_user)
    @post = posts(:published_post)
    sign_in @user
  end

  test "GET /posts returns success" do
    get posts_path
    assert_response :success
  end

  test "POST /posts creates record" do
    assert_difference "Post.count", 1 do
      post posts_path, params: { post: { title: "New Post", body: "Content" } }
    end
    assert_redirected_to post_path(Post.last)
  end

  test "POST /posts with invalid data returns error" do
    assert_no_difference "Post.count" do
      post posts_path, params: { post: { title: "" } }
    end
    assert_response :unprocessable_entity
  end
end
```

**Policy Test:**
```ruby
require "test_helper"

class PostPolicyTest < ActiveSupport::TestCase
  include PolicyTestHelpers

  setup do
    @workspace = workspaces(:main_workspace)
    @admin = users(:admin_user)
    @member = users(:member_user)
    @post = posts(:workspace_post)
    Current.user = nil
  end

  test "admin can always edit" do
    with_workspace(@workspace) do
      assert policy(@admin, @post).edit?
    end
  end

  test "member requires permission to edit" do
    with_workspace(@workspace) do
      refute policy(@member, @post).edit?
      
      set_workspace_permissions(@member, @workspace, :allowed_to_edit_posts)
      assert policy(@member, @post).edit?
    end
  end

  test "scope excludes other workspace posts" do
    with_workspace(@other_workspace) do
      scope = PostPolicy::Scope.new(@admin, Post.all).resolve
      refute_includes scope, @post
    end
  end
end
```

## Performance Optimization Checklist

Before submitting tests, verify:

- [ ] Using fixtures instead of factories
- [ ] Using `User.new` instead of `User.create` when DB not needed
- [ ] Testing validation errors on in-memory objects
- [ ] Minimal fixture data (only what's needed)
- [ ] Request tests instead of system tests where possible
- [ ] Pagination thresholds configured low for tests
- [ ] No unnecessary associations in fixtures
- [ ] BCrypt cost set to minimum in test environment
- [ ] Logging disabled in test environment
- [ ] Using `build_stubbed` pattern where applicable

## Anti-Patterns to Avoid

1. **Testing implementation details** - Test outcomes, not internal method calls
2. **Overly complex setup** - If setup is > 10 lines, refactor to fixtures
3. **Shared state between tests** - Each test should be independent
4. **Testing private methods** - Only test public interface
5. **Brittle assertions** - Don't assert on timestamps, exact errors, or order
6. **Too many system tests** - Reserve for critical user paths only
7. **Missing negative tests** - Always test what should fail/be denied
8. **Factory cascades** - Avoid factories that create many associated records

## Running Tests

```bash
# Run all tests
bin/rails test

# Run specific file
bin/rails test test/models/user_test.rb

# Run specific test by line
bin/rails test test/models/user_test.rb:42

# Run specific test by name
bin/rails test -n "test_requires_email"

# Run directory
bin/rails test test/policies/

# Run with verbose output
bin/rails test -v

# Run in parallel
bin/rails test --parallel

# Run with coverage
COVERAGE=true bin/rails test

# Run and fail fast
bin/rails test --fail-fast
```

## Debugging Tips

```ruby
# Print response body in request tests
puts response.body

# Print validation errors
pp @record.errors.full_messages

# Use breakpoint (Rails 7+)
debugger

# Check SQL queries
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Inspect fixture data
pp users(:admin_user).attributes
```
