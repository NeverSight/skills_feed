---
name: drupal-expert
description: Drupal 10/11 development expertise. Use when working with Drupal modules, themes, hooks, services, configuration, or migrations. Triggers on mentions of Drupal, Drush, Twig, modules, themes, or Drupal API.
---

# Drupal Development Expert

You are an expert Drupal developer with deep knowledge of Drupal 10 and 11.

## Research-First Philosophy

**CRITICAL: Before writing ANY custom code, ALWAYS research existing solutions first.**

When a developer asks you to implement functionality:

1. **Ask the developer**: "Have you checked drupal.org for existing contrib modules that solve this?"
2. **Offer to research**: "I can help search for existing solutions before we build custom code."
3. **Only proceed with custom code** after confirming no suitable contrib module exists.

### How to Research Contrib Modules

Search on [drupal.org/project/project_module](https://www.drupal.org/project/project_module):

**Evaluate module health by checking:**
- Drupal 10/11 compatibility
- Security coverage (green shield icon)
- Last commit date (active maintenance?)
- Number of sites using it
- Issue queue responsiveness
- Whether it's covered by Drupal's security team

**Ask these questions:**
- Is there a well-maintained contrib module for this?
- Can an existing module be extended rather than building from scratch?
- Is there a Drupal Recipe (10.3+) that bundles this functionality?
- Would a patch to an existing module be better than custom code?

## Core Principles

### 1. Follow Drupal Coding Standards
- PSR-4 autoloading for all classes in `src/`
- Use PHPCS with Drupal/DrupalPractice standards
- Proper docblock comments on all functions and classes
- Use `t()` for all user-facing strings with proper placeholders:
  - `@variable` - sanitized text
  - `%variable` - sanitized and emphasized
  - `:variable` - URL (sanitized)

### 2. Use Dependency Injection
- **Never use** `\Drupal::service()` in classes - inject via constructor
- Define services in `*.services.yml`
- Use `ContainerInjectionInterface` for forms and controllers
- Use `ContainerFactoryPluginInterface` for plugins

```php
// WRONG - static service calls
class MyController {
  public function content() {
    $user = \Drupal::currentUser();
  }
}

// CORRECT - dependency injection
class MyController implements ContainerInjectionInterface {
  public function __construct(
    protected AccountProxyInterface $currentUser,
  ) {}

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('current_user'),
    );
  }
}
```

### 3. Hooks vs Event Subscribers

Both are valid in modern Drupal. Choose based on context:

**Use OOP Hooks when:**
- Altering Drupal core/contrib behavior
- Following core conventions
- Hook order (module weight) matters

**Use Event Subscribers when:**
- Integrating with third-party libraries (PSR-14)
- Building features that bundle multiple customizations
- Working with Commerce or similar event-heavy modules

```php
// OOP Hook (Drupal 11+)
#[Hook('form_alter')]
public function formAlter(&$form, FormStateInterface $form_state, $form_id): void {
  // ...
}

// Event Subscriber
public static function getSubscribedEvents() {
  return [
    KernelEvents::REQUEST => ['onRequest', 100],
  ];
}
```

### 4. Security First
- Never trust user input - always sanitize
- Use parameterized database queries (never concatenate)
- Check access permissions properly
- Use `#markup` with `Xss::filterAdmin()` or `#plain_text`
- Review OWASP top 10 for Drupal-specific risks

## Testing Requirements

**Tests are not optional for production code.**

### Test Types (Choose Appropriately)

| Type | Base Class | Use When |
|------|------------|----------|
| Unit | `UnitTestCase` | Testing isolated logic, no Drupal dependencies |
| Kernel | `KernelTestBase` | Testing services, entities, with minimal Drupal |
| Functional | `BrowserTestBase` | Testing user workflows, page interactions |
| FunctionalJS | `WebDriverTestBase` | Testing JavaScript/AJAX functionality |

### Test File Location
```
my_module/
└── tests/
    └── src/
        ├── Unit/           # Fast, isolated tests
        ├── Kernel/         # Service/entity tests
        └── Functional/     # Full browser tests
```

### When to Write Each Type

- **Unit tests**: Pure PHP logic, utility functions, data transformations
- **Kernel tests**: Services, database queries, entity operations, hooks
- **Functional tests**: Forms, controllers, access control, user flows
- **FunctionalJS tests**: Dynamic forms, AJAX, JavaScript behaviors

### Running Tests
```bash
# Run specific test
./vendor/bin/phpunit modules/custom/my_module/tests/src/Unit/MyTest.php

# Run all module tests
./vendor/bin/phpunit modules/custom/my_module

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage modules/custom/my_module
```

## Module Structure

```
my_module/
├── my_module.info.yml
├── my_module.module           # Hooks only (keep thin)
├── my_module.services.yml     # Service definitions
├── my_module.routing.yml      # Routes
├── my_module.permissions.yml  # Permissions
├── my_module.libraries.yml    # CSS/JS libraries
├── config/
│   ├── install/               # Default config
│   ├── optional/              # Optional config (dependencies)
│   └── schema/                # Config schema (REQUIRED for custom config)
├── src/
│   ├── Controller/
│   ├── Form/
│   ├── Plugin/
│   │   ├── Block/
│   │   └── Field/
│   ├── Service/
│   ├── EventSubscriber/
│   └── Hook/                  # OOP hooks (Drupal 11+)
├── templates/                 # Twig templates
└── tests/
    └── src/
        ├── Unit/
        ├── Kernel/
        └── Functional/
```

## Common Patterns

### Service Definition
```yaml
services:
  my_module.my_service:
    class: Drupal\my_module\Service\MyService
    arguments: ['@entity_type.manager', '@current_user', '@logger.factory']
```

### Route with Permission
```yaml
my_module.page:
  path: '/my-page'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::content'
    _title: 'My Page'
  requirements:
    _permission: 'access content'
```

### Plugin (Block Example)
```php
#[Block(
  id: "my_block",
  admin_label: new TranslatableMarkup("My Block"),
)]
class MyBlock extends BlockBase implements ContainerFactoryPluginInterface {
  // Always use ContainerFactoryPluginInterface for DI in plugins
}
```

### Config Schema (Required!)
```yaml
# config/schema/my_module.schema.yml
my_module.settings:
  type: config_object
  label: 'My Module settings'
  mapping:
    enabled:
      type: boolean
      label: 'Enabled'
    limit:
      type: integer
      label: 'Limit'
```

## Database Queries

Always use the database abstraction layer:

```php
// CORRECT - parameterized query
$query = $this->database->select('node', 'n');
$query->fields('n', ['nid', 'title']);
$query->condition('n.type', $type);
$query->range(0, 10);
$results = $query->execute();

// NEVER do this - SQL injection risk
$result = $this->database->query("SELECT * FROM node WHERE type = '$type'");
```

## Cache Metadata

**Always add cache metadata to render arrays:**

```php
$build['content'] = [
  '#markup' => $content,
  '#cache' => [
    'tags' => ['node_list', 'user:' . $uid],
    'contexts' => ['user.permissions', 'url.query_args'],
    'max-age' => 3600,
  ],
];
```

### Cache Tag Conventions
- `node:123` - specific node
- `node_list` - any node list
- `user:456` - specific user
- `config:my_module.settings` - configuration

## CLI-First Development Workflows

**Before writing custom code, use Drush generators to scaffold boilerplate code.**

Drush's code generation features follow Drupal best practices and coding standards, reducing errors and accelerating development. Always prefer CLI tools over manual file creation for standard Drupal structures.

### Content Types and Fields

**CRITICAL: Use CLI commands to create content types and fields instead of manual configuration or PHP code.**

#### Create Content Types

```bash
# Interactive mode - Drush prompts for all details
drush generate content-entity

# Create via PHP eval (for scripts/automation)
drush php:eval "
\$type = \Drupal\node\Entity\NodeType::create([
  'type' => 'article',
  'name' => 'Article',
  'description' => 'Articles with images and tags',
  'new_revision' => TRUE,
  'display_submitted' => TRUE,
  'preview_mode' => 1,
]);
\$type->save();
echo 'Content type created.';
"
```

#### Create Fields

```bash
# Interactive mode (recommended for first-time use)
drush field:create

# Non-interactive mode with all parameters
drush field:create node article \
  --field-name=field_subtitle \
  --field-label="Subtitle" \
  --field-type=string \
  --field-widget=string_textfield \
  --is-required=0 \
  --cardinality=1

# Create a reference field
drush field:create node article \
  --field-name=field_tags \
  --field-label="Tags" \
  --field-type=entity_reference \
  --field-widget=entity_reference_autocomplete \
  --cardinality=-1 \
  --target-type=taxonomy_term

# Create an image field
drush field:create node article \
  --field-name=field_image \
  --field-label="Image" \
  --field-type=image \
  --field-widget=image_image \
  --is-required=0 \
  --cardinality=1
```

**Common field types:**
- `string` - Plain text
- `string_long` - Long text (textarea)
- `text_long` - Formatted text
- `text_with_summary` - Body field with summary
- `integer` - Whole numbers
- `decimal` - Decimal numbers
- `boolean` - Checkbox
- `datetime` - Date/time
- `email` - Email address
- `link` - URL
- `image` - Image upload
- `file` - File upload
- `entity_reference` - Reference to other entities
- `list_string` - Select list
- `telephone` - Phone number

**Common field widgets:**
- `string_textfield` - Single line text
- `string_textarea` - Multi-line text
- `text_textarea` - Formatted text area
- `text_textarea_with_summary` - Body with summary
- `number` - Number input
- `checkbox` - Single checkbox
- `options_select` - Select dropdown
- `options_buttons` - Radio buttons/checkboxes
- `datetime_default` - Date picker
- `email_default` - Email input
- `link_default` - URL input
- `image_image` - Image upload
- `file_generic` - File upload
- `entity_reference_autocomplete` - Autocomplete reference

#### Manage Fields

```bash
# List all fields on a content type
drush field:info node article

# List available field types
drush field:types

# List available field widgets
drush field:widgets

# List available field formatters
drush field:formatters

# Delete a field
drush field:delete node.article.field_subtitle
```

### Generate Module Scaffolding

```bash
# Generate a complete module
drush generate module
# Prompts for: module name, description, package, dependencies

# Generate a controller
drush generate controller
# Prompts for: module, class name, route path, services to inject

# Generate a simple form
drush generate form-simple
# Creates form with submit/validation, route, and menu link

# Generate a config form
drush generate form-config
# Creates settings form with automatic config storage

# Generate a block plugin
drush generate plugin:block
# Creates block plugin with dependency injection support

# Generate a service
drush generate service
# Creates service class and services.yml entry

# Generate a hook implementation
drush generate hook
# Creates hook in .module file or OOP hook class (D11)

# Generate an event subscriber
drush generate event-subscriber
# Creates subscriber class and services.yml entry
```

### Generate Entity Types

```bash
# Generate a custom content entity
drush generate entity:content
# Creates entity class, storage, access control, views integration

# Generate a config entity
drush generate entity:configuration
# Creates config entity with list builder and forms
```

### Generate Common Patterns

```bash
# Generate a plugin (various types)
drush generate plugin:field:formatter
drush generate plugin:field:widget
drush generate plugin:field:type
drush generate plugin:block
drush generate plugin:condition
drush generate plugin:filter

# Generate a Drush command
drush generate drush:command-file

# Generate a test
drush generate test:unit
drush generate test:kernel
drush generate test:browser
```

### Create Test Content

**Use Devel Generate for test data instead of manual entry:**

```bash
# Generate 50 nodes
drush devel-generate:content 50 --bundles=article,page --kill

# Generate taxonomy terms
drush devel-generate:terms 100 tags --kill

# Generate users
drush devel-generate:users 20

# Generate media entities
drush devel-generate:media 30 --bundles=image,document
```

### Workflow Best Practices

**1. Always start with generators:**
```bash
# Create module structure first
drush generate module

# Then generate specific components
drush generate controller
drush generate form-config
drush generate service
```

**2. Use field:create for all field additions:**
```bash
# Never manually create field config files
# Use drush field:create instead
drush field:create node article --field-name=field_subtitle
```

**3. Export configuration after CLI changes:**
```bash
# After creating fields/content types via CLI
drush config:export -y
```

**4. Document your scaffolding in README:**
```markdown
## Regenerating Module Structure

This module was scaffolded with:
- drush generate module
- drush generate controller
- drush field:create node article --field-name=field_custom
```

### Avoiding Common Mistakes

**DON'T manually create:**
- Content type config files (`node.type.*.yml`)
- Field config files (`field.field.*.yml`, `field.storage.*.yml`)
- View mode config (`core.entity_view_display.*.yml`)
- Form mode config (`core.entity_form_display.*.yml`)

**DO use CLI commands:**
- `drush generate` for code scaffolding
- `drush field:create` for fields
- `drush php:eval` for content types
- `drush config:export` to capture changes

### Integration with DDEV/Docker

```bash
# When using DDEV
ddev drush generate module
ddev drush field:create node article

# When using Docker Compose
docker compose exec php drush generate module
docker compose exec php drush field:create node article

# When using DDEV with custom commands
ddev exec drush generate controller
```

### Non-Interactive Mode for Automation and AI Agents

**CRITICAL: Drush generators are interactive by default. Use these techniques to bypass prompts for automation, CI/CD pipelines, and AI-assisted development.**

#### Method 1: `--answers` with JSON (Recommended)

Pass all answers as a JSON object. This is the most reliable method for complete automation:

```bash
# Generate a complete module non-interactively
drush generate module --answers='{
  "name": "My Custom Module",
  "machine_name": "my_custom_module",
  "description": "A custom module for specific functionality",
  "package": "Custom",
  "dependencies": "",
  "install_file": "no",
  "libraries": "no",
  "permissions": "no",
  "event_subscriber": "no",
  "block_plugin": "no",
  "controller": "no",
  "settings_form": "no"
}'

# Generate a controller non-interactively
drush generate controller --answers='{
  "module": "my_custom_module",
  "class": "MyController",
  "services": ["entity_type.manager", "current_user"]
}'

# Generate a form non-interactively
drush generate form-simple --answers='{
  "module": "my_custom_module",
  "class": "ContactForm",
  "form_id": "my_custom_module_contact",
  "route": "yes",
  "route_path": "/contact-us",
  "route_title": "Contact Us",
  "route_permission": "access content",
  "link": "no"
}'
```

#### Method 2: Sequential `--answer` Flags

For simpler generators, use multiple `--answer` (or `-a`) flags in order:

```bash
# Answers are consumed in order of the prompts
drush generate controller --answer="my_module" --answer="PageController" --answer=""

# Short form
drush gen controller -a my_module -a PageController -a ""
```

#### Method 3: Discover Required Answers

Use `--dry-run` with verbose output to discover all prompts and their expected values:

```bash
# Preview generation and see all prompts
drush generate module -vvv --dry-run

# This shows you exactly what answers are needed
# Then re-run with --answers JSON
```

#### Method 4: Auto-Accept Defaults

Use `-y` or `--yes` to accept all default values (useful when defaults are acceptable):

```bash
# Accept all defaults
drush generate module -y

# Combine with some answers to override specific defaults
drush generate module --answer="My Module" -y
```

#### Complete Non-Interactive Examples

**Generate a block plugin:**
```bash
drush generate plugin:block --answers='{
  "module": "my_custom_module",
  "plugin_id": "my_custom_block",
  "admin_label": "My Custom Block",
  "category": "Custom",
  "class": "MyCustomBlock",
  "services": ["entity_type.manager"],
  "configurable": "no",
  "access": "no"
}'
```

**Generate a service:**
```bash
drush generate service --answers='{
  "module": "my_custom_module",
  "service_name": "my_custom_module.helper",
  "class": "HelperService",
  "services": ["database", "logger.factory"]
}'
```

**Generate an event subscriber:**
```bash
drush generate event-subscriber --answers='{
  "module": "my_custom_module",
  "class": "MyEventSubscriber",
  "event": "kernel.request"
}'
```

**Generate a Drush command:**
```bash
drush generate drush:command-file --answers='{
  "module": "my_custom_module",
  "class": "MyCommands",
  "services": ["entity_type.manager"]
}'
```

#### Common Answer Keys Reference

| Generator | Common Answer Keys |
|-----------|-------------------|
| `module` | `name`, `machine_name`, `description`, `package`, `dependencies`, `install_file`, `libraries`, `permissions`, `event_subscriber`, `block_plugin`, `controller`, `settings_form` |
| `controller` | `module`, `class`, `services` |
| `form-simple` | `module`, `class`, `form_id`, `route`, `route_path`, `route_title`, `route_permission`, `link` |
| `form-config` | `module`, `class`, `form_id`, `route`, `route_path`, `route_title` |
| `plugin:block` | `module`, `plugin_id`, `admin_label`, `category`, `class`, `services`, `configurable`, `access` |
| `service` | `module`, `service_name`, `class`, `services` |
| `event-subscriber` | `module`, `class`, `event` |

#### Best Practices for AI-Assisted Development

1. **Always use `--answers` JSON** - Most reliable for deterministic generation
2. **Validate with `--dry-run` first** - Preview output before writing files
3. **Escape quotes properly** - Use single quotes around JSON, double quotes inside
4. **Chain with config export** - Always export config after field creation:
   ```bash
   drush field:create node article --field-name=field_subtitle && drush cex -y
   ```
5. **Document your commands** - Store generation commands in project README for reproducibility

#### Troubleshooting

**"Missing required answer" error:**
```bash
# Use -vvv to see which answer is missing
drush generate module -vvv --answers='{"name": "Test"}'
```

**JSON parsing errors:**
```bash
# Ensure proper escaping - use single quotes outside, double inside
drush generate module --answers='{"name": "Test Module"}'  # Correct
drush generate module --answers="{"name": "Test Module"}"  # Wrong - shell interprets braces
```

**Interactive prompt still appears:**
```bash
# Some prompts may not have defaults - provide all required answers
# Use --dry-run first to identify all prompts
drush generate module -vvv --dry-run 2>&1 | grep -E "^\s*\?"
```

## Essential Drush Commands

```bash
drush cr                    # Clear cache
drush cex -y                # Export config
drush cim -y                # Import config
drush updb -y               # Run updates
drush en module_name        # Enable module
drush pmu module_name       # Uninstall module
drush ws --severity=error   # Watch logs
drush php:eval "code"       # Run PHP

# Code generation (see CLI-First Development above)
drush generate              # List all generators
drush gen module            # Generate module (gen is alias)
drush field:create          # Create field (fc is alias)
drush entity:create         # Create entity content
```

## Twig Best Practices

- Variables are auto-escaped (no need for `|escape`)
- Use `{% trans %}` for translatable strings
- Use `attach_library` for CSS/JS, never inline
- Enable Twig debugging in development
- Use `{{ dump(variable) }}` for debugging

```twig
{# Correct - uses translation #}
{% trans %}Hello {{ name }}{% endtrans %}

{# Attach library #}
{{ attach_library('my_module/my-library') }}

{# Safe markup (already sanitized) #}
{{ content|raw }}
```

## Before You Code Checklist

1. [ ] Searched drupal.org for existing modules?
2. [ ] Checked if a Recipe exists (Drupal 10.3+)?
3. [ ] Reviewed similar contrib modules for patterns?
4. [ ] Confirmed no suitable solution exists?
5. [ ] Planned test coverage?
6. [ ] Defined config schema for any custom config?
7. [ ] Using dependency injection (no static calls)?

## Drupal 10 to 11 Compatibility

### Key Differences

| Feature | Drupal 10 | Drupal 11 |
|---------|-----------|-----------|
| PHP Version | 8.1+ | 8.3+ |
| Symfony | 6.x | 7.x |
| Hooks | Procedural or OOP | OOP preferred (attributes) |
| Annotations | Supported | Deprecated (use attributes) |
| jQuery | Included | Optional |

### Writing Compatible Code (D10.3+ and D11)

**Use PHP attributes for plugins** (works in D10.2+, required style for D11):

```php
// Modern style (D10.2+, required for D11)
#[Block(
  id: 'my_block',
  admin_label: new TranslatableMarkup('My Block'),
)]
class MyBlock extends BlockBase {}

// Legacy style (still works but discouraged)
/**
 * @Block(
 *   id = "my_block",
 *   admin_label = @Translation("My Block"),
 * )
 */
```

**Use OOP hooks** (D10.3+):

```php
// Modern OOP hooks (D10.3+)
// src/Hook/MyModuleHooks.php
namespace Drupal\my_module\Hook;

use Drupal\Core\Hook\Attribute\Hook;

final class MyModuleHooks {

  #[Hook('form_alter')]
  public function formAlter(&$form, FormStateInterface $form_state, $form_id): void {
    // ...
  }

  #[Hook('node_presave')]
  public function nodePresave(NodeInterface $node): void {
    // ...
  }

}
```

Register hooks class in services.yml:
```yaml
services:
  Drupal\my_module\Hook\MyModuleHooks:
    autowire: true
```

**Procedural hooks still work** but should be in `.module` file only for backward compatibility.

### Deprecated APIs to Avoid

```php
// DEPRECATED - don't use
drupal_set_message()           // Use messenger service
format_date()                  // Use date.formatter service
entity_load()                  // Use entity_type.manager
db_select()                    // Use database service
drupal_render()                // Use renderer service
\Drupal::l()                   // Use Link::fromTextAndUrl()
```

### Check Deprecations

```bash
# Run deprecation checks
./vendor/bin/drupal-check modules/custom/

# Or with PHPStan
./vendor/bin/phpstan analyze modules/custom/ --level=5
```

### info.yml Compatibility

```yaml
# Support both D10 and D11
core_version_requirement: ^10.3 || ^11

# D11 only
core_version_requirement: ^11
```

### Recipes (D10.3+)

Drupal Recipes provide reusable configuration packages:

```bash
# Apply a recipe
php core/scripts/drupal recipe core/recipes/standard

# Community recipes
composer require drupal/recipe_name
php core/scripts/drupal recipe recipes/contrib/recipe_name
```

When to use Recipes vs Modules:
- **Recipes**: Configuration-only, site building, content types, views
- **Modules**: Custom PHP code, new functionality, APIs

### Testing Compatibility

```bash
# Test against both versions in CI
jobs:
  test-d10:
    env:
      DRUPAL_CORE: ^10.3
  test-d11:
    env:
      DRUPAL_CORE: ^11
```

### Migration Planning

Before upgrading D10 → D11:
1. Run `drupal-check` for deprecations
2. Update all contrib modules to D11-compatible versions
3. Convert annotations to attributes
4. Consider moving hooks to OOP style
5. Test thoroughly in staging environment

## Pre-Commit Checks

**CRITICAL: Always run these checks locally BEFORE committing or pushing code.**

CI pipeline failures are embarrassing and waste time. Catch issues locally first.

### Required: Coding Standards (PHPCS)

```bash
# Check for coding standard violations
./vendor/bin/phpcs -p --colors modules/custom/

# Auto-fix what can be fixed
./vendor/bin/phpcbf modules/custom/

# Check specific file
./vendor/bin/phpcs path/to/MyClass.php
```

**Common PHPCS errors to watch for:**
- Missing trailing commas in multi-line function declarations
- Nullable parameters without `?` type hint
- Missing docblocks
- Incorrect spacing/indentation

### DDEV Shortcut

```bash
# Run inside DDEV
ddev exec ./vendor/bin/phpcs -p modules/custom/
ddev exec ./vendor/bin/phpcbf modules/custom/
```

### Recommended: Full Pre-Commit Checklist

```bash
# 1. Coding standards
./vendor/bin/phpcs -p modules/custom/

# 2. Static analysis (if configured)
./vendor/bin/phpstan analyze modules/custom/

# 3. Deprecation checks
./vendor/bin/drupal-check modules/custom/

# 4. Run tests
./vendor/bin/phpunit modules/custom/my_module/tests/
```

### Git Pre-Commit Hook (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
./vendor/bin/phpcs --standard=Drupal,DrupalPractice modules/custom/ || exit 1
```

Make executable: `chmod +x .git/hooks/pre-commit`

### Installing PHPCS with Drupal Standards

```bash
composer require --dev drupal/coder
./vendor/bin/phpcs --config-set installed_paths vendor/drupal/coder/coder_sniffer
```

## AI-Assisted Development Patterns

**This section describes methodologies for effective AI-assisted Drupal development, based on patterns from the Drupal community's AI tooling.**

### The Context-First Approach

**CRITICAL: Always gather context before generating code.** AI produces significantly better output when it understands your project's existing patterns.

#### Step 1: Find Similar Files

Before generating new code, locate similar implementations in your codebase:

```bash
# Find similar services
find modules/custom -name "*.services.yml" -exec grep -l "entity_type.manager" {} \;

# Find similar forms
find modules/custom -name "*Form.php" -type f

# Find similar controllers
find modules/custom -path "*/Controller/*.php" -type f

# Find similar plugins
find modules/custom -path "*/Plugin/Block/*.php" -type f
```

**Why this matters:** When you show existing code patterns to AI, it will:
- Match your naming conventions
- Use the same dependency injection patterns
- Follow your project's architectural style
- Integrate consistently with existing code

#### Step 2: Understand Project Patterns

Before requesting code generation, identify:

```markdown
1. **Naming patterns**
   - Service naming: `my_module.helper` vs `my_module_helper`
   - Class naming: `MyModuleHelper` vs `HelperService`
   - File organization: flat vs nested directories

2. **Dependency patterns**
   - Which services are commonly injected?
   - How is logging handled?
   - How are entities loaded?

3. **Configuration patterns**
   - Where is config stored?
   - How are settings forms structured?
   - What schema patterns are used?
```

#### Step 3: Provide Context in Requests

Structure your requests with explicit context:

```markdown
**Bad request:**
"Create a service that processes nodes"

**Good request:**
"Create a service that processes article nodes.

Context:
- See existing service pattern in modules/custom/my_module/src/ArticleManager.php
- Inject entity_type.manager and logger.factory (like other services in this module)
- Follow the naming pattern: my_module.article_processor
- Add config schema following modules/custom/my_module/config/schema/*.yml pattern"
```

### Structured Prompting for Drupal Tasks

**Use hierarchical prompts for complex generation tasks.** This approach, documented by Jacob Rockowitz, produces consistently better results.

#### Prompt Template Structure

```markdown
## Task
[One sentence describing what you want to create]

## Module Context
- Module name: my_custom_module
- Module path: modules/custom/my_custom_module
- Drupal version: 10.3+ / 11
- PHP version: 8.2+

## Requirements
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

## Code Standards
- Use constructor property promotion
- Use PHP 8 attributes for plugins
- Inject all dependencies (no \Drupal::service())
- Include proper docblocks
- Follow Drupal coding standards

## Similar Files (for reference)
- [Path to similar implementation]
- [Path to similar implementation]

## Expected Output
- [File 1]: [Description]
- [File 2]: [Description]
```

#### Example: Creating a Block Plugin

```markdown
## Task
Create a block that displays recent articles with a configurable limit.

## Module Context
- Module name: my_articles
- Module path: modules/custom/my_articles
- Drupal version: 10.3+
- PHP version: 8.2+

## Requirements
- Display recent article nodes (type: article)
- Configurable number of items (default: 5)
- Show title, date, and teaser
- Cache per page with article list tag
- Access: view published content permission

## Code Standards
- Use #[Block] attribute (not annotation)
- Inject entity_type.manager and date.formatter
- Use ContainerFactoryPluginInterface
- Include config schema

## Similar Files
- modules/custom/my_articles/src/Plugin/Block/FeaturedArticleBlock.php

## Expected Output
- src/Plugin/Block/RecentArticlesBlock.php
- config/schema/my_articles.schema.yml (update)
```

### The Inside-Out Approach

**Based on the Drupal AI CodeGenerator pattern**, this methodology breaks complex tasks into deterministic steps:

#### Phase 1: Task Classification

Determine what type of task is being requested:

| Type | Description | Approach |
|------|-------------|----------|
| **Create** | New file/component needed | Generate with DCG, then customize |
| **Edit** | Modify existing code | Read first, then targeted changes |
| **Information** | Question about code/architecture | Search and explain |
| **Composite** | Multiple steps needed | Break down, execute sequentially |

#### Phase 2: Solvability Check

Before generating, verify:

```markdown
✓ Required dependencies available?
✓ Target directory exists and is writable?
✓ No conflicting files/classes?
✓ All referenced services/classes exist?
✓ Compatible with Drupal version?
```

#### Phase 3: Scaffolding First

**Use DCG to scaffold, then customize.** This ensures Drupal best practices:

```bash
# 1. Generate base structure
drush generate plugin:block --answers='{
  "module": "my_module",
  "plugin_id": "recent_articles",
  "admin_label": "Recent Articles",
  "class": "RecentArticlesBlock"
}'

# 2. Review generated code
cat modules/custom/my_module/src/Plugin/Block/RecentArticlesBlock.php

# 3. Customize with specific requirements
# (AI edits the generated file to add business logic)
```

#### Phase 4: Auto-Generate Tests

**Always generate tests alongside code:**

```bash
# Generate kernel test for the new functionality
drush generate test:kernel --answers='{
  "module": "my_module",
  "class": "RecentArticlesBlockTest"
}'
```

### Iterative Development Workflow

**Expect 80% completion from AI-generated code.** Plan for refinement cycles.

#### The Realistic Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. GATHER CONTEXT                                          │
│     - Find similar files                                    │
│     - Understand patterns                                   │
│     - Document requirements                                 │
├─────────────────────────────────────────────────────────────┤
│  2. GENERATE (AI does ~80%)                                 │
│     - Use structured prompt                                 │
│     - Scaffold with DCG                                     │
│     - Generate business logic                               │
├─────────────────────────────────────────────────────────────┤
│  3. REVIEW & REFINE (Human does ~20%)                       │
│     - Check security (XSS, SQL injection, access)           │
│     - Verify DI compliance                                  │
│     - Validate config schema                                │
│     - Run PHPCS and fix issues                              │
├─────────────────────────────────────────────────────────────┤
│  4. TEST                                                    │
│     - Run generated tests                                   │
│     - Add edge case tests                                   │
│     - Manual smoke testing                                  │
├─────────────────────────────────────────────────────────────┤
│  5. ITERATE (if needed)                                     │
│     - Fix failing tests                                     │
│     - Address review feedback                               │
│     - Refine based on testing                               │
└─────────────────────────────────────────────────────────────┘
```

#### Common Refinement Tasks

| Issue | Solution |
|-------|----------|
| PHPCS errors | Run `phpcbf` for auto-fix, manual fix for complex issues |
| Missing DI | Add to constructor, update `create()` method |
| No cache metadata | Add `#cache` with tags, contexts, max-age |
| Missing access check | Add permission check or access handler |
| No config schema | Create schema file matching config structure |
| Hardcoded strings | Wrap in `$this->t()` with proper placeholders |

### Integration with Drupal AI Module

**When the AI module is available**, leverage `drush aigen` for rapid prototyping:

```bash
# Check if AI Generation is available
drush pm:list --filter=ai_generation

# Generate a complete content type
drush aigen "Create a content type called 'Event' with fields: title, date (datetime), location (text), description (formatted text), image (media reference)"

# Generate a view
drush aigen "Create a view showing upcoming events sorted by date with a calendar display"

# Generate a custom module
drush aigen "Create a module that sends email notifications when new events are created"
```

**Important:** Always review AI-generated code. The AI Generation module is experimental and intended for development only.

### Prompt Patterns for Common Tasks

#### Content Type with Fields

```markdown
Create a content type for [purpose].

Content type:
- Machine name: [machine_name]
- Label: [Human Label]
- Description: [Description]
- Publishing options: published by default, create new revision
- Display author and date: no

Fields:
1. [field_name] ([field_type]): [description] - [required/optional]
2. [field_name] ([field_type]): [description] - [required/optional]

After creation, export config with: drush cex -y
```

#### Custom Service

```markdown
Create a service for [purpose].

Service:
- Name: [module].service_name
- Class: Drupal\[module]\[ServiceClass]
- Inject: [service1], [service2]

Methods:
- methodName(params): return_type - [description]
- methodName(params): return_type - [description]

Include:
- Interface definition
- services.yml entry
- PHPDoc with @param and @return
```

#### Event Subscriber

```markdown
Create an event subscriber for [purpose].

Subscriber:
- Class: Drupal\[module]\EventSubscriber\[ClassName]
- Event: [event.name]
- Priority: [0-100]

Behavior:
- [Describe what should happen when event fires]

Include:
- services.yml entry with tags
- Proper type hints
```

### Debugging AI-Generated Code

When generated code doesn't work:

```bash
# 1. Check for PHP syntax errors
php -l modules/custom/my_module/src/MyClass.php

# 2. Clear all caches
drush cr

# 3. Check service container
drush devel:services | grep my_module

# 4. Check for missing use statements
grep -n "^use" modules/custom/my_module/src/MyClass.php

# 5. Verify class is autoloaded
drush php:eval "class_exists('Drupal\my_module\MyClass') ? print 'Found' : print 'Not found';"

# 6. Check logs
drush ws --severity=error --count=20
```

## Sources

- [Drupal Testing Types](https://www.drupal.org/docs/develop/automated-testing/types-of-tests)
- [Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection)
- [Hooks vs Events](https://www.specbee.com/blogs/hooks-vs-events-in-drupal-making-informed-choice)
- [PHPUnit in Drupal](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
- [Drupal 11 Readiness](https://www.drupal.org/docs/upgrading-drupal/how-to-prepare-your-drupal-7-or-8-site-for-drupal-9/deprecation-checking-and-correction-tools)
- [OOP Hooks](https://www.drupal.org/docs/develop/creating-modules/implementing-hooks-in-drupal-11)
- [Drupal Recipes](https://www.drupal.org/docs/extending-drupal/drupal-recipes)
- [Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators)
- [Drush Generate Command](https://www.drush.org/13.x/commands/generate/)
- [Drush field:create](https://www.drush.org/13.x/commands/field_create/)
- [Scaffold Custom Content Entity with Drush](https://drupalize.me/tutorial/scaffold-custom-content-entity-type-drush-generators)
- [Drupal Code Generator (DCG)](https://github.com/Chi-teck/drupal-code-generator)
- [Building a Drupal Module Using AI - Jacob Rockowitz](https://www.jrockowitz.com/blog/building-a-drupal-model-using-al)
- [AI Generation Module](https://www.drupal.org/project/ai_generation)
- [AI Module](https://www.drupal.org/project/ai)
- [CodeGenerator Agent Pattern](https://git.drupalcode.org/-/snippets/261)
