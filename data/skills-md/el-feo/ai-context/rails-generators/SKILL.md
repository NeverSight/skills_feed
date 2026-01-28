---
name: rails-generators
description: Create expert-level Ruby on Rails generators for models, services, controllers, and full-stack features. Use when building custom generators, scaffolds, or code generation tools for Rails applications, or when the user mentions Rails generators, Thor DSL, or automated code generation.
---

<objective>
Build production-ready Rails generators that automate repetitive coding tasks and enforce architectural patterns. This skill covers creating custom generators for models, service objects, API scaffolds, and complete features with migrations, tests, and documentation.
</objective>

<quick_start>
<basic_generator>
Create a simple service object generator:

```ruby
# lib/generators/service/service_generator.rb
module Generators
  class ServiceGenerator < Rails::Generators::NamedBase
    source_root File.expand_path('templates', __dir__)

    def create_service_file
      template 'service.rb.tt', "app/services/#{file_name}_service.rb"
    end

    def create_service_test
      template 'service_test.rb.tt', "test/services/#{file_name}_service_test.rb"
    end
  end
end
```

Template file (templates/service.rb.tt):
```ruby
class <%= class_name %>Service
  def initialize
  end

  def call
    # Implementation goes here
  end
end
```

Invoke with: `rails generate service payment_processor`
</basic_generator>

<usage_pattern>
**Generator location**: `lib/generators/[name]/[name]_generator.rb`
**Template location**: `lib/generators/[name]/templates/`
**Test location**: `test/generators/[name]_generator_test.rb`
</usage_pattern>
</quick_start>

<context>
<when_to_create>
Create custom generators when you need to:

- **Enforce architectural patterns**: Service objects, form objects, presenters, query objects
- **Reduce boilerplate**: API controllers with standard CRUD, serializers, policy objects
- **Maintain consistency**: Team conventions for file structure, naming, and organization
- **Automate complex setup**: Multi-file features with migrations, tests, and documentation
- **Override Rails defaults**: Customize scaffold behavior for your application's needs
</when_to_create>

<rails_8_updates>
Rails 8 introduced the authentication generator (`rails generate authentication`) which demonstrates modern generator patterns including:
- ActionCable integration for real-time features
- Controller concerns for shared behavior
- Mailer generation with templates
- Comprehensive view scaffolding

Study Rails 8 built-in generators for current best practices.
</rails_8_updates>
</context>

<workflow>
<step_1>
**Choose base class**:

- `Rails::Generators::Base`: Simple generators without required arguments
- `Rails::Generators::NamedBase`: Generators requiring a name argument

```ruby
class ServiceGenerator < Rails::Generators::NamedBase
  # Automatically provides: name, class_name, file_name, plural_name
end
```
</step_1>

<step_2>
**Define source root and options**:

```ruby
source_root File.expand_path('templates', __dir__)

class_option :namespace, type: :string, default: nil, desc: "Namespace for the service"
class_option :skip_tests, type: :boolean, default: false, desc: "Skip test files"
```

Access options with: `options[:namespace]`
</step_2>

<step_3>
**Add public methods** (executed in definition order):

```ruby
def create_service_file
  template 'service.rb.tt', service_file_path
end

def create_test_file
  return if options[:skip_tests]
  template 'service_test.rb.tt', test_file_path
end

private

def service_file_path
  if options[:namespace]
    "app/services/#{options[:namespace]}/#{file_name}_service.rb"
  else
    "app/services/#{file_name}_service.rb"
  end
end
```
</step_3>

<step_4>
**Create ERB templates** (`.tt` extension):

```erb
<% if options[:namespace] -%>
module <%= options[:namespace].camelize %>
  class <%= class_name %>Service
    def call
      # Implementation
    end
  end
end
<% else -%>
class <%= class_name %>Service
  def call
    # Implementation
  end
end
<% end -%>
```

**Important**: Use `<%%` to output literal `<%` in generated files.
</step_4>

<step_5>
**Test the generator** (see [Testing](#testing) section):

```ruby
rails generate service payment_processor --namespace=billing
rails generate service notifier --skip-tests
```
</step_5>
</workflow>

<common_patterns>
<model_generator>
**Custom model with associations and scopes**:

```ruby
class CustomModelGenerator < Rails::Generators::NamedBase
  source_root File.expand_path('templates', __dir__)

  class_option :parent, type: :string, desc: "Parent model for belongs_to"
  class_option :scope, type: :array, desc: "Scopes to generate"

  def create_migration
    migration_template 'migration.rb.tt',
      "db/migrate/create_#{table_name}.rb"
  end

  def create_model_file
    template 'model.rb.tt', "app/models/#{file_name}.rb"
  end

  def create_test_file
    template 'model_test.rb.tt', "test/models/#{file_name}_test.rb"
  end
end
```

See [references/model-generator.md](references/model-generator.md) for complete example.
</model_generator>

<service_object_generator>
**Service object with result object pattern**:

```ruby
class ServiceGenerator < Rails::Generators::NamedBase
  source_root File.expand_path('templates', __dir__)

  class_option :result_object, type: :boolean, default: true

  def create_service
    template 'service.rb.tt', "app/services/#{file_name}_service.rb"
  end

  def create_result_object
    return unless options[:result_object]
    template 'result.rb.tt', "app/services/#{file_name}_result.rb"
  end
end
```

See [references/service-generator.md](references/service-generator.md) for complete example.
</service_object_generator>

<api_controller_generator>
**API controller with serializer**:

```ruby
class ApiControllerGenerator < Rails::Generators::NamedBase
  source_root File.expand_path('templates', __dir__)

  class_option :serializer, type: :string, default: 'active_model_serializers'
  class_option :actions, type: :array, default: %w[index show create update destroy]

  def create_controller
    template 'controller.rb.tt',
      "app/controllers/api/v1/#{file_name.pluralize}_controller.rb"
  end

  def create_serializer
    template "serializer_#{options[:serializer]}.rb.tt",
      "app/serializers/#{file_name}_serializer.rb"
  end

  def add_routes
    route "namespace :api do\n    namespace :v1 do\n      resources :#{file_name.pluralize}\n    end\n  end"
  end
end
```

See [references/api-generator.md](references/api-generator.md) for complete example.
</api_controller_generator>

<full_stack_scaffold>
**Complete feature scaffold**:

```ruby
class FeatureGenerator < Rails::Generators::NamedBase
  source_root File.expand_path('templates', __dir__)

  class_option :api, type: :boolean, default: false

  def create_model
    invoke 'model', [name], migration: true
  end

  def create_controller
    if options[:api]
      invoke 'api_controller', [name]
    else
      invoke 'controller', [name], actions: %w[index show new create edit update destroy]
    end
  end

  def create_views
    return if options[:api]
    %w[index show new edit _form].each do |view|
      template "views/#{view}.html.erb.tt",
        "app/views/#{file_name.pluralize}/#{view}.html.erb"
    end
  end

  def create_tests
    invoke 'test_unit:model', [name]
    invoke 'test_unit:controller', [name]
    invoke 'test_unit:system', [name] unless options[:api]
  end
end
```

See [references/scaffold-generator.md](references/scaffold-generator.md) for complete example.
</full_stack_scaffold>
</common_patterns>

<advanced_features>
<hooks>
**Generator hooks** enable modular composition and test framework integration:

```ruby
class ServiceGenerator < Rails::Generators::NamedBase
  hook_for :test_framework, as: :service
end
```

This automatically invokes `test_unit:service` or `rspec:service` based on configuration.

**Creating hook responders**:

```ruby
# lib/generators/rspec/service/service_generator.rb
module Rspec
  module Generators
    class ServiceGenerator < Rails::Generators::NamedBase
      source_root File.expand_path('templates', __dir__)

      def create_service_spec
        template 'service_spec.rb.tt',
          "spec/services/#{file_name}_service_spec.rb"
      end
    end
  end
end
```

See [references/hooks.md](references/hooks.md) for hook patterns and fallback configuration.
</hooks>

<generator_composition>
**Invoke other generators** from your generator:

```ruby
def create_dependencies
  invoke 'model', [name], migration: true
  invoke 'service', ["#{name}_processor"]
  invoke 'serializer', [name]
end
```

**Conditional invocation**:

```ruby
def create_optional_files
  invoke 'mailer', [name] if options[:mailer]
  invoke 'job', ["#{name}_job"] if options[:background_job]
end
```
</generator_composition>

<namespacing>
**Namespace generators** for organization:

```ruby
# lib/generators/admin/resource/resource_generator.rb
module Admin
  module Generators
    class ResourceGenerator < Rails::Generators::NamedBase
      source_root File.expand_path('templates', __dir__)

      def create_admin_resource
        template 'resource.rb.tt',
          "app/admin/#{file_name}.rb"
      end
    end
  end
end
```

Invoke with: `rails generate admin:resource User`

**Generator search path**:
1. `rails/generators/[name]/[name]_generator.rb`
2. `generators/[name]/[name]_generator.rb`
3. `rails/generators/[name]_generator.rb`
4. `generators/[name]_generator.rb`

See [references/namespacing.md](references/namespacing.md) for fallback patterns.
</namespacing>

<file_manipulation>
**Thor::Actions methods** available in generators:

```ruby
# Create files
create_file 'config/settings.yml', yaml_content
copy_file 'template.rb', 'config/template.rb'
template 'config.rb.tt', 'config/settings.rb'

# Modify existing files
insert_into_file 'config/routes.rb', route_content, after: "Rails.application.routes.draw do\n"
gsub_file 'config/application.rb', /old_value/, 'new_value'
comment_lines 'config/environments/production.rb', /config.assets.compile/

# Directory operations
empty_directory 'app/services'
directory 'templates/views', 'app/views/admin'

# Rails-specific helpers
initializer 'service_config.rb', config_content
lib 'custom_validator.rb', validator_content
rakefile 'import_tasks.rake', rake_content
route "namespace :api do\n  resources :users\n end"
```

See [references/file-actions.md](references/file-actions.md) for complete reference.
</file_manipulation>

<template_system>
**ERB template features**:

```erb
<%# Variables from generator available automatically %>
class <%= class_name %>Service
  <%- if options[:async] -%>
  include AsyncService
  <%- end -%>

  def initialize(<%= attributes.map(&:name).join(', ') %>)
    <%- attributes.each do |attr| -%>
    @<%= attr.name %> = <%= attr.name %>
    <%- end -%>
  end
end
```

**Escaping for nested ERB** (template generates another template):

```erb
<%# This will be evaluated when user uses the generated file %>
<%%= render partial: 'form', locals: { <%= singular_name %>: @<%= singular_name %> } %>
```

**Conditional whitespace control** with `-`:
- `<%-` suppresses leading whitespace
- `-%>` suppresses trailing whitespace

See [references/templates.md](references/templates.md) for template patterns.
</template_system>
</advanced_features>

<testing>
<rails_test_framework>
**Testing with Rails::Generators::Testing::Behavior**:

```ruby
require 'test_helper'
require 'generators/service/service_generator'

class ServiceGeneratorTest < Rails::Generators::TestCase
  tests ServiceGenerator
  destination File.expand_path('../tmp', __dir__)
  setup :prepare_destination

  test "generates service file" do
    run_generator ["payment_processor"]

    assert_file "app/services/payment_processor_service.rb" do |content|
      assert_match(/class PaymentProcessorService/, content)
      assert_match(/def call/, content)
    end
  end

  test "generates with namespace option" do
    run_generator ["payment", "--namespace=billing"]

    assert_file "app/services/billing/payment_service.rb" do |content|
      assert_match(/module Billing/, content)
      assert_match(/class PaymentService/, content)
    end
  end

  test "skips tests when flag provided" do
    run_generator ["payment", "--skip-tests"]

    assert_file "app/services/payment_service.rb"
    assert_no_file "test/services/payment_service_test.rb"
  end
end
```

**Available assertions**:
- `assert_file(path) { |content| ... }` - File exists with expected content
- `assert_no_file(path)` - File does not exist
- `assert_migration(path)` - Migration file exists
- `assert_class_method(method, content)` - Class method defined
- `assert_instance_method(method, content)` - Instance method defined

See [references/testing-rails.md](references/testing-rails.md) for comprehensive testing patterns.
</rails_test_framework>

<rspec_testing>
**Testing with RSpec and generator_spec**:

Add to Gemfile: `gem 'generator_spec', group: :development`

```ruby
require 'generator_spec'

RSpec.describe ServiceGenerator, type: :generator do
  destination File.expand_path('../../tmp', __FILE__)

  before do
    prepare_destination
  end

  context "with default options" do
    before do
      run_generator ["payment_processor"]
    end

    it "creates service file" do
      expect(destination_root).to have_structure {
        directory "app/services" do
          file "payment_processor_service.rb" do
            contains "class PaymentProcessorService"
            contains "def call"
          end
        end
      }
    end

    it "creates test file" do
      expect(destination_root).to have_structure {
        directory "test/services" do
          file "payment_processor_service_test.rb"
        end
      }
    end
  end

  context "with namespace option" do
    before do
      run_generator ["payment", "--namespace=billing"]
    end

    it "creates namespaced service" do
      assert_file "app/services/billing/payment_service.rb" do |content|
        expect(content).to match(/module Billing/)
        expect(content).to match(/class PaymentService/)
      end
    end
  end
end
```

**Alternative: Test against dummy app**:

```ruby
RSpec.describe "ServiceGenerator" do
  it "generates correct service file" do
    Dir.chdir(dummy_app_path) do
      `rails generate service payment_processor`

      service_file = File.read('app/services/payment_processor_service.rb')
      expect(service_file).to include('class PaymentProcessorService')

      # Cleanup
      FileUtils.rm_rf('app/services/payment_processor_service.rb')
    end
  end
end
```

See [references/testing-rspec.md](references/testing-rspec.md) for RSpec patterns and generator_spec usage.
</rspec_testing>

<manual_testing>
**Manual testing workflow**:

1. Generate in test Rails app:
```bash
cd test/dummy
rails generate service payment_processor --namespace=billing
```

2. Verify generated files:
```bash
tree app/services
cat app/services/billing/payment_processor_service.rb
```

3. Test destruction (if implemented):
```bash
rails destroy service payment_processor --namespace=billing
```

4. Test edge cases:
```bash
rails generate service payment_processor --skip-tests
rails generate service payment_processor --namespace=very/deep/namespace
```
</manual_testing>
</testing>

<validation>
<checklist>
Before considering a generator complete, verify:

- [ ] Generator inherits from appropriate base class
- [ ] `source_root` points to templates directory
- [ ] All options have appropriate types and defaults
- [ ] Public methods execute in correct order
- [ ] Templates use correct ERB syntax (`.tt` extension)
- [ ] File paths handle namespacing correctly
- [ ] Generator works with and without options
- [ ] Tests cover default behavior and all options
- [ ] Generator can be destroyed (if applicable)
- [ ] Documentation includes usage examples
- [ ] Edge cases handled (special characters, deep namespacing)
</checklist>

<common_issues>
**Missing source_root**: Templates not found
```ruby
# Add this to generator class
source_root File.expand_path('templates', __dir__)
```

**Incorrect template syntax**: File generated with wrong ERB tags
```ruby
# Use <%% for literal ERB in generated files
<%%= @user.name %>  # Generates: <%= @user.name %>
```

**Option not recognized**: Check option definition
```ruby
class_option :namespace, type: :string  # Not :namespace_option
# Access with: options[:namespace]
```

**Method order issues**: Methods execute in definition order
```ruby
# This runs first
def create_model
end

# This runs second
def create_controller
end
```
</common_issues>
</validation>

<examples>
<service_with_dependencies>
**Service generator with dependency injection**:

```ruby
class AdvancedServiceGenerator < Rails::Generators::NamedBase
  source_root File.expand_path('templates', __dir__)

  class_option :dependencies, type: :array, default: []
  class_option :async, type: :boolean, default: false

  def create_service
    template 'service.rb.tt', service_path
  end

  def create_test
    template 'service_test.rb.tt', test_path
  end

  private

  def service_path
    "app/services/#{file_name}_service.rb"
  end

  def test_path
    "test/services/#{file_name}_service_test.rb"
  end

  def dependency_params
    options[:dependencies].map { |dep| "#{dep}:" }.join(', ')
  end
end
```

Template (service.rb.tt):
```erb
class <%= class_name %>Service
  <%- if options[:async] -%>
  include ActiveJob::Helpers
  <%- end -%>

  <%- if options[:dependencies].any? -%>
  def initialize(<%= dependency_params %>)
    <%- options[:dependencies].each do |dep| -%>
    @<%= dep %> = <%= dep %>
    <%- end -%>
  end
  <%- else -%>
  def initialize
  end
  <%- end -%>

  def call
    # Implementation
  end
end
```
</service_with_dependencies>

<query_object_generator>
**Query object generator**:

```ruby
class QueryGenerator < Rails::Generators::NamedBase
  source_root File.expand_path('templates', __dir__)

  class_option :model, type: :string, required: true
  class_option :scopes, type: :array, default: []

  def create_query
    template 'query.rb.tt', "app/queries/#{file_name}_query.rb"
  end

  def create_test
    template 'query_test.rb.tt', "test/queries/#{file_name}_query_test.rb"
  end
end
```
</query_object_generator>
</examples>

<reference_guides>
**Detailed references**:

- [Model generator patterns](references/model-generator.md) - Custom models with migrations and associations
- [Service generator patterns](references/service-generator.md) - Service objects with result objects
- [API generator patterns](references/api-generator.md) - Controllers, serializers, and routes
- [Scaffold patterns](references/scaffold-generator.md) - Full-stack feature generation
- [Hooks and composition](references/hooks.md) - Generator hooks and fallbacks
- [Namespacing](references/namespacing.md) - Organizing generators with namespaces
- [File manipulation](references/file-actions.md) - Thor::Actions reference
- [Template system](references/templates.md) - ERB template patterns
- [Rails testing](references/testing-rails.md) - Rails::Generators::TestCase patterns
- [RSpec testing](references/testing-rspec.md) - generator_spec and RSpec patterns
</reference_guides>

<success_criteria>
A well-built Rails generator has:

- Clear inheritance from Rails::Generators::Base or NamedBase
- Properly configured source_root pointing to templates
- Well-defined class_option declarations with appropriate types
- Public methods that execute in logical order
- ERB templates with correct syntax and variable interpolation
- Comprehensive tests covering default and optional behaviors
- Error handling for edge cases (missing arguments, invalid options)
- Documentation with usage examples
- Consistent naming following Rails conventions
- Works correctly with generator hooks and composition
</success_criteria>

**Sources**:
- [Creating and Customizing Rails Generators & Templates — Ruby on Rails Guides](https://guides.rubyonrails.org/generators.html)
- [Rails 8 adds built in authentication generator | Saeloun Blog](https://blog.saeloun.com/2025/05/12/rails-8-adds-built-in-authentication-generator/)
- [Shaping Rails to Your Needs, Customizing Rails Generators using Thor Templates | Saeloun Blog](https://blog.saeloun.com/2023/05/31/customizing-rails-generators-using-thor-templates/)
- [Generators · rails/thor Wiki · GitHub](https://github.com/rails/thor/wiki/Generators)
- [GitHub: generator_spec](https://github.com/stevehodgkiss/generator_spec)
- [A Deep Dive Into RSpec Tests in Ruby on Rails | AppSignal Blog](https://blog.appsignal.com/2024/02/07/a-deep-dive-into-rspec-tests-in-ruby-on-rails.html)
