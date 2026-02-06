---
name: debug:rails
description: Debug Rails issues systematically. Use when encountering ActiveRecord errors like RecordNotFound, routing issues, N+1 query problems detected by Bullet, asset pipeline issues, migration failures, gem conflicts, ActionController errors, CSRF token problems, or any Ruby on Rails application errors requiring diagnosis.
---

# Rails Debugging Guide

This skill provides a systematic approach to debugging Ruby on Rails applications, covering common error patterns, modern debugging tools, and proven troubleshooting techniques.

## Common Error Patterns

### 1. ActiveRecord::RecordNotFound

**Symptoms:** Rails fails to find a record in the database when using `find` or `find_by!` methods.

**Diagnosis:**
```ruby
# Check if record exists
rails console
> Model.exists?(id)
> Model.where(conditions).count

# Inspect the query being generated
> Model.where(conditions).to_sql
```

**Common Causes:**
- Record was deleted but reference still exists
- Incorrect ID passed from params
- Scopes filtering out the record
- Multi-tenancy issues (wrong tenant context)

**Solutions:**
```ruby
# Use find_by instead of find (returns nil instead of raising)
Model.find_by(id: params[:id])

# Handle gracefully in controller
def show
  @record = Model.find_by(id: params[:id])
  render_not_found unless @record
end

# Or rescue the exception
rescue_from ActiveRecord::RecordNotFound, with: :record_not_found
```

### 2. ActionController::RoutingError

**Symptoms:** 404 error - requested URL doesn't exist in the application.

**Diagnosis:**
```bash
# List all routes
rails routes

# Search for specific route
rails routes | grep resource_name

# Check route with specific path
rails routes -g path_pattern
```

**Common Causes:**
- Missing route definition in `config/routes.rb`
- Typo in URL or route helper
- Wrong HTTP verb
- Namespace/scope mismatch
- Engine routes not mounted

**Solutions:**
```ruby
# Verify route exists
Rails.application.routes.recognize_path('/your/path', method: :get)

# Add missing route
resources :users, only: [:show, :index]

# Check for namespace issues
namespace :api do
  resources :users
end
```

### 3. NoMethodError (undefined method for nil:NilClass)

**Symptoms:** Calling a method on `nil` object.

**Diagnosis:**
```ruby
# Add debugging breakpoint
binding.break  # Ruby 3.1+ / Rails 7+
debugger       # Alternative
byebug         # Legacy

# Check object state
puts object.inspect
Rails.logger.debug object.inspect
```

**Common Causes:**
- Database query returned no results
- Association not loaded
- Hash key doesn't exist
- Typo in variable/method name

**Solutions:**
```ruby
# Safe navigation operator
user&.profile&.name

# Null object pattern
user.profile || NullProfile.new

# Use presence
params[:key].presence || default_value

# Guard clauses
return unless user.present?
```

### 4. N+1 Query Problems

**Symptoms:** Slow page loads, excessive database queries in logs.

**Diagnosis:**
```ruby
# Check logs for repeated queries
tail -f log/development.log | grep SELECT

# Use Bullet gem for automatic detection
# Gemfile
gem 'bullet', group: :development

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.rails_logger = true
end
```

**Common Causes:**
- Iterating over collection and accessing associations
- Missing `includes` or `preload`
- Calling methods that trigger queries in views

**Solutions:**
```ruby
# Eager loading with includes
User.includes(:posts, :comments).all

# Preload for large datasets
User.preload(:posts).find_each do |user|
  user.posts.each { |post| ... }
end

# Use joins for filtering
User.joins(:posts).where(posts: { published: true })

# Counter cache for counts
belongs_to :user, counter_cache: true
```

### 5. Database Migration Failures

**Symptoms:** Migrations fail, schema out of sync, rollback errors.

**Diagnosis:**
```bash
# Check migration status
rails db:migrate:status

# View pending migrations
rails db:abort_if_pending_migrations

# Check current schema version
rails runner "puts ActiveRecord::Migrator.current_version"
```

**Common Causes:**
- Column/table already exists
- Foreign key constraint violations
- Data type incompatibility
- Missing index
- Irreversible migration

**Solutions:**
```bash
# Rollback and retry
rails db:rollback
rails db:migrate

# Reset database (development only!)
rails db:drop db:create db:migrate

# Fix stuck migration
rails runner "ActiveRecord::SchemaMigration.where(version: 'XXXXXX').delete_all"

# Use Strong Migrations gem for safety
gem 'strong_migrations'
```

### 6. ActionController::InvalidAuthenticityToken

**Symptoms:** CSRF token mismatch on POST/PUT/PATCH/DELETE requests.

**Diagnosis:**
```ruby
# Check if token is present in form
<%= csrf_meta_tags %>

# Verify token in request headers
request.headers['X-CSRF-Token']
```

**Common Causes:**
- Missing CSRF meta tags in layout
- JavaScript not sending token with AJAX
- Session expired
- Caching issues with forms

**Solutions:**
```erb
<!-- Add to layout head -->
<%= csrf_meta_tags %>

<!-- JavaScript AJAX setup -->
<script>
  $.ajaxSetup({
    headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content }
  });
</script>
```

```ruby
# For API endpoints, skip verification
skip_before_action :verify_authenticity_token, only: [:api_action]

# Or use null session
protect_from_forgery with: :null_session
```

### 7. ActionView::Template::Error

**Symptoms:** View rendering fails with template errors.

**Diagnosis:**
```ruby
# Error message shows file and line number
# Check the specific template mentioned

# Debug variables in view
<%= debug @variable %>
<%= @variable.inspect %>

# Use better_errors gem for interactive debugging
gem 'better_errors', group: :development
gem 'binding_of_caller', group: :development
```

**Common Causes:**
- Undefined variable in view
- Missing partial
- Syntax error in ERB
- Helper method not defined
- Nil object method call

**Solutions:**
```erb
<!-- Check for nil before rendering -->
<% if @user.present? %>
  <%= @user.name %>
<% end %>

<!-- Use try for potentially nil objects -->
<%= @user.try(:name) %>

<!-- Safe navigation -->
<%= @user&.name %>
```

### 8. Asset Pipeline Issues

**Symptoms:** CSS/JS not loading, missing assets in production, Sprockets errors.

**Diagnosis:**
```bash
# Check asset paths
rails assets:precompile --trace

# View compiled assets
ls -la public/assets/

# Check manifest
cat public/assets/.sprockets-manifest*.json
```

**Common Causes:**
- Asset not in load path
- Missing precompile directive
- Incorrect asset helper usage
- Webpacker/esbuild configuration issues

**Solutions:**
```ruby
# Add to precompile list
# config/initializers/assets.rb
Rails.application.config.assets.precompile += %w( custom.js custom.css )

# Use correct helpers
<%= javascript_include_tag 'application' %>
<%= stylesheet_link_tag 'application' %>
<%= image_tag 'logo.png' %>

# For Rails 7+ with import maps
<%= javascript_importmap_tags %>
```

### 9. Gem Conflicts and Bundler Issues

**Symptoms:** Bundle install fails, version conflicts, LoadError.

**Diagnosis:**
```bash
# Check gem versions
bundle info gem_name

# View dependency tree
bundle viz

# Check for outdated gems
bundle outdated

# Verify Bundler version
bundle --version
```

**Common Causes:**
- Incompatible gem versions
- Platform-specific gems
- Missing native extensions
- Lockfile out of sync

**Solutions:**
```bash
# Update specific gem
bundle update gem_name

# Clean reinstall
rm Gemfile.lock
bundle install

# Use specific version
gem 'problematic_gem', '~> 1.0'

# Platform constraints
gem 'specific_gem', platforms: :ruby
```

### 10. NameError (Uninitialized Constant)

**Symptoms:** Ruby can't find class, module, or constant.

**Diagnosis:**
```ruby
# Check if constant is defined
defined?(MyClass)

# View autoload paths
puts ActiveSupport::Dependencies.autoload_paths

# Check zeitwerk loader
Rails.autoloaders.main.dirs
```

**Common Causes:**
- File not in autoload path
- Typo in class/module name
- Wrong file naming convention
- Circular dependency
- Missing require statement

**Solutions:**
```ruby
# Ensure file naming matches class name
# app/models/user_profile.rb -> class UserProfile

# Add to autoload paths if needed
# config/application.rb
config.autoload_paths << Rails.root.join('lib')

# Explicit require for lib files
require_relative '../lib/my_library'
```

## Debugging Tools

### Built-in Debug Gem (Rails 7+ / Ruby 3.1+)

The modern default debugger for Rails applications.

```ruby
# Add breakpoint
debugger
binding.break
binding.b

# Configuration
# Gemfile
gem 'debug', group: [:development, :test]

# Disable in CI
# Set RUBY_DEBUG_ENABLE=0
```

**Common Commands:**
```
# Navigation
n / next     - Step over
s / step     - Step into
c / continue - Continue execution
q / quit     - Exit debugger

# Inspection
p / pp       - Print/pretty print
info         - Show local variables
bt / backtrace - Show call stack

# Breakpoints
break file.rb:10  - Set breakpoint
break Class#method - Break on method
delete 1          - Delete breakpoint
```

### Byebug (Legacy Projects)

```ruby
# Gemfile
gem 'byebug', group: [:development, :test]

# Add breakpoint
byebug

# Commands similar to debug gem
next, step, continue, quit
display @variable
where  # backtrace
```

### Rails Console

```bash
# Start console
rails console
rails c

# Sandbox mode (rollback all changes)
rails console --sandbox

# Specific environment
RAILS_ENV=production rails console
```

**Useful Console Techniques:**
```ruby
# Reload code changes
reload!

# Run SQL directly
ActiveRecord::Base.connection.execute("SELECT 1")

# Time queries
Benchmark.measure { Model.all.to_a }

# Find slow queries
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Test helpers
app.get '/path'
app.response.body
```

### Better Errors Gem

```ruby
# Gemfile
group :development do
  gem 'better_errors'
  gem 'binding_of_caller'
end
```

Provides interactive error pages with:
- Full stack trace with source code
- Interactive REPL at each frame
- Variable inspection
- Local variable values

### Bullet Gem (N+1 Detection)

```ruby
# Gemfile
gem 'bullet', group: :development

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.bullet_logger = true
  Bullet.console = true
  Bullet.rails_logger = true
  Bullet.add_footer = true
end
```

### Rails Panel (Chrome Extension)

Provides browser-based debugging:
- Request/response details
- Database queries with timing
- Rendered views
- Log messages
- Route information

### Pry and Pry-Rails

```ruby
# Gemfile
gem 'pry-rails', group: [:development, :test]

# Add breakpoint
binding.pry

# Pry commands
ls          # List methods/variables
cd object   # Change context
show-source method  # View source
```

## The Four Phases of Rails Debugging

### Phase 1: Reproduce and Isolate

**Goal:** Understand exactly what triggers the error.

```bash
# Check recent changes
git diff HEAD~5
git log --oneline -10

# Reproduce in console
rails console
> # Try to trigger the error

# Check logs
tail -f log/development.log
```

**Questions to Answer:**
- Can you reproduce it consistently?
- What changed recently?
- Does it happen in all environments?
- What are the exact steps to trigger it?

### Phase 2: Gather Information

**Goal:** Collect all relevant data about the error.

```ruby
# Add logging
Rails.logger.debug "Variable state: #{@variable.inspect}"
Rails.logger.tagged("DEBUG") { Rails.logger.info "Custom message" }

# Check stack trace
raise "Debug checkpoint"

# Inspect request/response
request.inspect
response.status
params.inspect
session.inspect
```

**Data to Collect:**
- Full stack trace
- Request parameters
- Session state
- Database state
- Environment variables
- Gem versions

### Phase 3: Form and Test Hypothesis

**Goal:** Identify the root cause.

```ruby
# Add strategic breakpoints
debugger

# Test assumptions
Model.find(id) rescue "Not found"

# Check database state
rails dbconsole
SELECT * FROM table WHERE condition;

# Verify configuration
Rails.configuration.inspect
ENV['KEY']
```

**Common Hypotheses:**
- Data issue (missing/corrupt records)
- Code logic error
- Configuration mismatch
- Race condition
- External service failure

### Phase 4: Fix and Verify

**Goal:** Implement fix and prevent regression.

```ruby
# Write failing test first
test "should handle missing record" do
  assert_raises(ActiveRecord::RecordNotFound) do
    get :show, params: { id: 0 }
  end
end

# Apply fix
# Run tests
rails test test/path/to_test.rb

# Verify in development
rails server
# Test the scenario manually
```

**Verification Checklist:**
- [ ] Original error no longer occurs
- [ ] Test covers the fix
- [ ] No new errors introduced
- [ ] Works in all environments

## Quick Reference Commands

### Routes

```bash
# All routes
rails routes

# Filtered routes
rails routes -c users
rails routes -g api
rails routes | grep pattern

# Specific route
rails routes -E # Expanded format
```

### Database

```bash
# Migration status
rails db:migrate:status

# Run migrations
rails db:migrate
rails db:migrate VERSION=XXXXXX

# Rollback
rails db:rollback
rails db:rollback STEP=3

# Reset (drops, creates, migrates)
rails db:reset

# Seed data
rails db:seed

# Direct SQL access
rails dbconsole
```

### Rails Runner

```bash
# Execute Ruby code
rails runner "puts User.count"
rails runner "User.find(1).update(active: true)"
rails runner path/to/script.rb

# With environment
RAILS_ENV=production rails runner "puts User.count"
```

### Generators and Tasks

```bash
# List all tasks
rails -T

# List generators
rails generate --help

# Task info
rails -D task_name
```

### Cache

```bash
# Clear cache
rails tmp:cache:clear

# Clear all tmp
rails tmp:clear

# In console
Rails.cache.clear
```

### Logs and Debugging

```bash
# Tail logs
tail -f log/development.log

# Clear logs
rails log:clear

# With grep filtering
tail -f log/development.log | grep -E "(ERROR|WARN)"
```

### Testing

```bash
# Run all tests
rails test

# Specific file
rails test test/models/user_test.rb

# Specific test
rails test test/models/user_test.rb:42

# With verbose output
rails test -v

# RSpec (if using)
bundle exec rspec
bundle exec rspec spec/models/user_spec.rb
```

### Console Tricks

```ruby
# Reload after code changes
reload!

# Suppress output
User.all; nil

# Time execution
Benchmark.measure { Model.expensive_query }

# SQL logging
ActiveRecord::Base.logger = Logger.new(STDOUT)
ActiveRecord::Base.logger = nil  # Disable

# Trace method calls
require 'tracer'
Tracer.on { Model.method_call }

# Find where method is defined
User.instance_method(:method_name).source_location
User.method(:class_method).source_location
```

## Environment-Specific Debugging

### Development

```ruby
# config/environments/development.rb
config.consider_all_requests_local = true
config.action_controller.perform_caching = false
config.log_level = :debug
```

### Production

```ruby
# Enable detailed errors temporarily (DANGEROUS)
RAILS_ENV=production rails console
> Rails.application.config.consider_all_requests_local = true

# Check production logs
heroku logs --tail
# or
ssh server 'tail -f /app/log/production.log'

# Safe debugging with exception tracking
# Use Sentry, Rollbar, Honeybadger, etc.
```

### Test

```ruby
# Verbose test output
rails test -v

# Debug test database
rails dbconsole -e test

# Keep test database
RAILS_ENV=test rails db:migrate
```

## Security Considerations

When debugging, be careful about:

```ruby
# Never log sensitive data
Rails.logger.info params.except(:password, :credit_card)

# Filter parameters
# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :password, :password_confirmation, :credit_card,
  :cvv, :ssn, :secret, :token, :api_key
]

# Don't expose stack traces in production
config.consider_all_requests_local = false

# Use exception tracking services instead
# Sentry, Rollbar, Honeybadger, Bugsnag
```

## Additional Resources

- [Ruby on Rails Guides - Debugging](https://guides.rubyonrails.org/debugging_rails_applications.html)
- [Ruby Debugging Tips 2025](https://railsatscale.com/2025-03-14-ruby-debugging-tips-and-recommendations-2025/)
- [Better Stack - Common Ruby Errors](https://betterstack.com/community/guides/scaling-ruby/solutions-to-common-errors/)
- [Rollbar - Top 10 Rails Errors](https://rollbar.com/blog/top-10-errors-from-1000-ruby-on-rails-projects-and-how-to-avoid-them/)
