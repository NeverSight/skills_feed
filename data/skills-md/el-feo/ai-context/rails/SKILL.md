---
name: rails
description: Comprehensive Ruby on Rails v8.1 development guide with detailed documentation for Active Record, controllers, views, routing, testing, jobs, mailers, and more. Use when working on Rails applications, building Rails features, debugging Rails code, writing migrations, setting up associations, configuring Rails apps, or answering questions about Rails best practices and patterns.
---

<objective>
Provide comprehensive guidance for Ruby on Rails development based on the official Rails Guides v8.1.1. Use this skill for all Rails-related development tasks, from basic CRUD operations to advanced features like Action Cable, Active Job, and performance tuning.
</objective>

<context>
Rails follows the "Convention over Configuration" principle. When building Rails applications:

- Follow Rails naming conventions for models, controllers, and routes
- Use Rails generators for consistency
- Leverage Rails magic (associations, validations, callbacks) rather than reinventing
- Write tests using Rails testing conventions
- Use Rails helpers and built-in functionality before custom code
</context>

<quick_start>
<common_commands>
```bash
# Database
rails db:create              # Create database
rails db:migrate             # Run pending migrations
rails db:rollback            # Rollback last migration

# Console and server
rails console                # Start Rails console
rails server                 # Start development server
rails test                   # Run all tests

# Generators
rails generate model NAME    # Generate model
rails generate controller NAME # Generate controller
rails generate scaffold NAME # Generate full CRUD
```
</common_commands>

<typical_workflow>
1. Generate model: `rails generate model Article title:string body:text`
2. Run migration: `rails db:migrate`
3. Add associations and validations to model
4. Generate controller: `rails generate controller Articles`
5. Define routes in `config/routes.rb`
6. Build views with ERB templates
7. Write tests and iterate
</typical_workflow>
</quick_start>

<reference_guides>
This skill includes detailed reference documentation organized by topic. **Always consult the relevant reference file** when working on specific Rails components:

**Active Record** ([references/active_record.md](references/active_record.md))

Read this when working with:
- Models and database operations (CRUD, queries, scopes)
- Database migrations and schema changes
- Model associations (has_many, belongs_to, has_one, has_and_belongs_to_many)
- Validations and custom validators
- Callbacks and lifecycle hooks
- PostgreSQL-specific features
- Multiple database configurations
- Composite primary keys
- Encryption

Common patterns:
- Defining associations: Always specify inverse_of for better performance
- Writing migrations: Use reversible changes when possible
- Query optimization: Use includes/joins to avoid N+1 queries
- Validations: Validate at the model level, not just in controllers

**Controllers & Views** ([references/controllers_views.md](references/controllers_views.md))

Read this when working with:
- Action Controller basics and advanced topics
- Rendering views, partials, and layouts
- Strong parameters and params handling
- Action View helpers and form builders
- Request/response cycle
- Filters (before_action, after_action, around_action)
- Streaming and file downloads

Common patterns:
- Use strong parameters to whitelist permitted attributes
- Keep controllers thin - business logic belongs in models
- Use partials for reusable view components
- Leverage view helpers for common formatting tasks

**Routing** ([references/routing.md](references/routing.md))

Read this when working with:
- Defining routes (resources, match, get, post, etc.)
- RESTful routing conventions
- Nested routes and namespaces
- Route constraints and custom matchers
- Route helpers and URL generation
- Routing concerns for DRY routes

Common patterns:
- Use `resources` for RESTful routes
- Nest routes only when truly hierarchical (limit to 1 level deep)
- Use shallow nesting for cleaner URLs
- Utilize route concerns for shared routing patterns

**Testing & Debugging** ([references/testing_debugging.md](references/testing_debugging.md))

Read this when working with:
- Writing unit tests (models, helpers)
- Controller tests and integration tests
- System tests with browser automation
- Fixtures, factories, and test data
- Testing mailers, jobs, and cables
- Debugging techniques (byebug, rails console)
- Rails logger and debugging helpers

Common patterns:
- Write tests first (TDD) or immediately after (test-driven design)
- Use fixtures for simple cases, factories for complex scenarios
- Test edge cases and error conditions
- Use system tests for critical user flows

**Jobs, Mailers & Cable** ([references/jobs_mailers_cable.md](references/jobs_mailers_cable.md))

Read this when working with:
- Active Job for background processing
- Action Mailer for email sending
- Action Mailbox for receiving emails
- Action Cable for WebSocket connections
- Queue adapters (Sidekiq, Resque, etc.)
- Email delivery and testing

Common patterns:
- Always use Active Job for async work (don't block requests)
- Test mailers with ActionMailer::TestCase
- Use Action Cable for real-time features (chat, notifications)
- Configure proper queue backends for production

**Assets & Frontend** ([references/assets_frontend.md](references/assets_frontend.md))

Read this when working with:
- Asset pipeline and Sprockets
- JavaScript bundling (import maps, esbuild, webpack)
- CSS and preprocessors (Sass, Tailwind)
- Action Text for rich text editing
- Frontend frameworks integration

Common patterns:
- Use asset helpers (image_tag, javascript_include_tag, etc.)
- Configure proper asset compilation for production
- Leverage Rails UJS/Turbo for dynamic interactions
- Use Action Text for WYSIWYG content

**Storage & Caching** ([references/storage_caching.md](references/storage_caching.md))

Read this when working with:
- Active Storage for file uploads
- Attaching files to models
- Image variants and transformations
- Caching strategies (page, action, fragment, low-level)
- Cache stores (Redis, Memcached)
- Russian Doll caching patterns

Common patterns:
- Use Active Storage for all file uploads
- Generate image variants on-demand
- Cache expensive computations and queries
- Use fragment caching for dynamic pages

**Configuration & Internals** ([references/configuration_internals.md](references/configuration_internals.md))

Read this when working with:
- Rails configuration options
- Environment-specific settings
- Initialization process
- Autoloading and eager loading
- Threading and concurrency
- Rack integration
- Rails engines
- Command-line tools and generators
- Custom generators

Common patterns:
- Keep environment configs DRY using shared settings
- Use Rails.application.config for app-wide settings
- Understand autoloading in development vs eager loading in production
- Create custom generators for repeated patterns

**Security & Performance** ([references/security_performance.md](references/security_performance.md))

Read this when working with:
- Security best practices
- XSS, CSRF, SQL injection prevention
- Authentication and authorization patterns
- Performance tuning and optimization
- Database query optimization
- Asset optimization
- Error reporting and monitoring

Common patterns:
- Always use strong parameters (never trust user input)
- Enable CSRF protection (on by default)
- Use prepared statements to prevent SQL injection
- Add database indexes for frequently queried columns
- Profile before optimizing (use tools like rack-mini-profiler)

**I18n & Support** ([references/i18n_support.md](references/i18n_support.md))

Read this when working with:
- Internationalization (I18n) setup
- Locale files and translations
- Active Support core extensions
- Time zones and date formatting
- Active Support instrumentation
- Custom extensions and monkey patches

Common patterns:
- Use I18n.t for all user-facing strings
- Organize translations by controller/view hierarchy
- Leverage Active Support extensions (1.day.ago, "hello".pluralize)
- Use instrumentation for performance monitoring

**API Development** ([references/api_development.md](references/api_development.md))

Read this when working with:
- Building JSON APIs with Rails
- API-only applications
- Serialization patterns
- Authentication for APIs (tokens, JWT)
- API versioning strategies
- CORS configuration

Common patterns:
- Use Rails API mode for API-only apps
- Implement proper authentication (OAuth, JWT, API keys)
- Version your APIs from the start
- Use proper HTTP status codes and error responses
</reference_guides>

<workflow>
<starting_new_feature>
**Plan the data model**
- Identify models and their relationships
- Sketch out the database schema
- Consider validations and constraints

**Generate migrations and models**
```bash
rails generate model Article title:string body:text published_at:datetime
rails generate migration AddUserRefToArticles user:references
```

**Set up associations and validations**
- Define relationships in models
- Add validations for data integrity
- Write model tests

**Create controllers and routes**
```bash
rails generate controller Articles index show new create edit update destroy
```
- Or use `rails generate scaffold` for full CRUD

**Build views**
- Create templates using ERB or other templating engines
- Use partials for reusable components
- Leverage form helpers

**Write tests**
- Model tests for validations and associations
- Controller tests for actions
- System tests for user flows

**Iterate and refactor**
- Extract common logic to concerns or service objects
- Optimize database queries
- Improve user experience
</starting_new_feature>
</workflow>

<best_practices>
<code_organization>
- Keep controllers thin (delegate to models/services)
- Use concerns for shared behavior
- Extract complex queries to scopes or query objects
- Use service objects for complex business logic
</code_organization>

<database>
- Always add indexes for foreign keys
- Use database constraints where appropriate
- Write reversible migrations
- Use database-level validations when possible
</database>

<performance>
- Eager load associations to avoid N+1 queries
- Use counter caches for expensive counts
- Implement caching strategically
- Profile before optimizing
</performance>

<security>
- Never trust user input (use strong parameters)
- Keep Rails and gems updated
- Use HTTPS in production
- Implement proper authorization (use gems like Pundit/CanCanCan)
</security>

<testing>
- Aim for high model test coverage
- Write integration tests for critical paths
- Use fixtures or factories, not both
- Keep tests fast and focused
</testing>
</best_practices>

<common_patterns>
<model_example>
```ruby
class Article < ApplicationRecord
  belongs_to :user
  has_many :comments, dependent: :destroy
  has_many_attached :images

  validates :title, presence: true, length: { minimum: 5 }
  validates :body, presence: true

  scope :published, -> { where.not(published_at: nil) }
  scope :recent, -> { order(created_at: :desc).limit(10) }

  def published?
    published_at.present? && published_at <= Time.current
  end
end
```
</model_example>

<controller_example>
```ruby
class ArticlesController < ApplicationController
  before_action :set_article, only: [:show, :edit, :update, :destroy]
  before_action :authenticate_user!, except: [:index, :show]

  def index
    @articles = Article.published.includes(:user)
  end

  def show
  end

  def create
    @article = current_user.articles.build(article_params)

    if @article.save
      redirect_to @article, notice: 'Article was successfully created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def article_params
    params.require(:article).permit(:title, :body, :published_at, images: [])
  end
end
```
</controller_example>

<routes_example>
```ruby
# config/routes.rb
Rails.application.routes.draw do
  root 'articles#index'

  resources :articles do
    resources :comments, only: [:create, :destroy]
  end

  namespace :admin do
    resources :articles
  end
end
```
</routes_example>
</common_patterns>

<version_notes>
This skill is based on Rails 8.1.1. Key recent features:

- Solid Queue, Solid Cache, and Solid Cable for built-in infrastructure
- Enhanced Turbo integration
- Improved authentication generators
- Better type checking with RBS support
- Progressive Web App features

When working with older Rails versions, check the upgrade guides in the references for migration paths and deprecated features.
</version_notes>

<troubleshooting>
When stuck on a Rails problem:

1. Check the relevant reference file first
2. Use `rails console` to experiment with code
3. Review the Rails guides at guides.rubyonrails.org
4. Check the API documentation at api.rubyonrails.org
5. Search GitHub issues for known problems

Remember: Rails is designed to make common tasks easy and follow sensible conventions. If something feels too difficult, there's likely a Rails way to do it more simply.
</troubleshooting>

<success_criteria>
You're using this skill effectively when:

- You consult the appropriate reference file before implementing Rails features
- You follow Rails conventions (RESTful routes, naming patterns, file organization)
- You leverage Rails generators and built-in functionality
- Your code follows the best practices outlined above
- Tests are written alongside feature development
- Security and performance considerations are addressed proactively
</success_criteria>
