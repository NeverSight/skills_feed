---
name: rspec
description: Comprehensive RSpec testing for Ruby and Rails applications. Covers model specs, request specs, system specs, factories, mocks, and TDD workflow. Automatically triggers on RSpec-related keywords and testing scenarios.
---

# RSpec Testing Skill

Expert guidance for writing comprehensive tests in RSpec for Ruby and Rails applications. This skill provides immediate, actionable testing strategies with deep-dive references for complex scenarios.

## Quick Start

### Basic RSpec Structure

```ruby
# spec/models/user_spec.rb
RSpec.describe User, type: :model do
  describe '#full_name' do
    it 'returns the first and last name' do
      user = User.new(first_name: 'John', last_name: 'Doe')
      expect(user.full_name).to eq('John Doe')
    end
  end
end
```

**Key concepts:**

- `describe`: Groups related tests (classes, methods)
- `context`: Describes specific scenarios
- `it`: Individual test example
- `expect`: Makes assertions using matchers

### Running Tests

```bash
# Run all specs
bundle exec rspec

# Run specific file
bundle exec rspec spec/models/user_spec.rb

# Run specific line
bundle exec rspec spec/models/user_spec.rb:12

# Run with documentation format
bundle exec rspec --format documentation

# Run only failures from last run
bundle exec rspec --only-failures
```

## Core Testing Patterns

### 1. Model Specs

Test business logic, validations, associations, and methods:

```ruby
RSpec.describe Article, type: :model do
  # Test validations
  describe 'validations' do
    it { should validate_presence_of(:title) }
    it { should validate_length_of(:title).is_at_most(100) }
  end

  # Test associations
  describe 'associations' do
    it { should belong_to(:author) }
    it { should have_many(:comments) }
  end

  # Test instance methods
  describe '#published?' do
    context 'when publish_date is in the past' do
      it 'returns true' do
        article = Article.new(publish_date: 1.day.ago)
        expect(article.published?).to be true
      end
    end

    context 'when publish_date is in the future' do
      it 'returns false' do
        article = Article.new(publish_date: 1.day.from_now)
        expect(article.published?).to be false
      end
    end
  end

  # Test scopes
  describe '.recent' do
    it 'returns articles from the last 30 days' do
      old = create(:article, created_at: 31.days.ago)
      recent = create(:article, created_at: 1.day.ago)

      expect(Article.recent).to include(recent)
      expect(Article.recent).not_to include(old)
    end
  end
end
```

### 2. Request Specs

Test HTTP requests and responses across the entire stack:

```ruby
RSpec.describe 'Articles API', type: :request do
  describe 'GET /articles' do
    it 'returns all articles' do
      create_list(:article, 3)

      get '/articles'

      expect(response).to have_http_status(:success)
      expect(JSON.parse(response.body).size).to eq(3)
    end
  end

  describe 'POST /articles' do
    context 'with valid params' do
      it 'creates a new article' do
        article_params = { article: { title: 'New Article', body: 'Content' } }

        expect {
          post '/articles', params: article_params
        }.to change(Article, :count).by(1)

        expect(response).to have_http_status(:created)
      end
    end

    context 'with invalid params' do
      it 'returns errors' do
        invalid_params = { article: { title: '' } }

        post '/articles', params: invalid_params

        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end

  describe 'authentication' do
    it 'requires authentication for create' do
      post '/articles', params: { article: { title: 'Test' } }

      expect(response).to have_http_status(:unauthorized)
    end

    it 'allows authenticated users to create' do
      user = create(:user)

      post '/articles',
        params: { article: { title: 'Test' } },
        headers: { 'Authorization' => "Bearer #{user.token}" }

      expect(response).to have_http_status(:created)
    end
  end
end
```

### 3. System Specs (End-to-End)

Test user workflows through the browser with Capybara:

```ruby
RSpec.describe 'Article management', type: :system do
  before { driven_by(:selenium_chrome_headless) }

  scenario 'user creates an article' do
    visit new_article_path

    fill_in 'Title', with: 'My Article'
    fill_in 'Body', with: 'Article content'
    click_button 'Create Article'

    expect(page).to have_content('Article was successfully created')
    expect(page).to have_content('My Article')
  end

  scenario 'user edits an article' do
    article = create(:article, title: 'Original Title')

    visit article_path(article)
    click_link 'Edit'

    fill_in 'Title', with: 'Updated Title'
    click_button 'Update Article'

    expect(page).to have_content('Updated Title')
    expect(page).not_to have_content('Original Title')
  end

  # Test JavaScript interactions
  scenario 'user filters articles', js: true do
    create(:article, title: 'Ruby Article', category: 'ruby')
    create(:article, title: 'Python Article', category: 'python')

    visit articles_path

    select 'Ruby', from: 'filter'

    expect(page).to have_content('Ruby Article')
    expect(page).not_to have_content('Python Article')
  end
end
```

## Factory Bot Integration

### Defining Factories

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    first_name { 'John' }
    last_name { 'Doe' }
    sequence(:email) { |n| "user#{n}@example.com" }
    password { 'password123' }

    # Traits for variations
    trait :admin do
      role { 'admin' }
    end

    trait :with_articles do
      transient do
        articles_count { 3 }
      end

      after(:create) do |user, evaluator|
        create_list(:article, evaluator.articles_count, author: user)
      end
    end
  end

  factory :article do
    sequence(:title) { |n| "Article #{n}" }
    body { 'Article content' }
    association :author, factory: :user
  end
end

# Using factories
user = create(:user)                        # Persisted
user = build(:user)                         # Not persisted
admin = create(:user, :admin)               # With trait
user = create(:user, :with_articles)        # With association
users = create_list(:user, 5)               # Multiple records
attributes = attributes_for(:user)          # Hash of attributes
```

## Essential Matchers

### Equality and Identity

```ruby
expect(actual).to eq(expected)           # ==
expect(actual).to eql(expected)          # .eql?
expect(actual).to be(expected)           # .equal?
expect(actual).to equal(expected)        # same object
```

### Truthiness and Types

```ruby
expect(actual).to be_truthy              # not nil or false
expect(actual).to be_falsy               # nil or false
expect(actual).to be_nil
expect(actual).to be_a(Class)
expect(actual).to be_an_instance_of(Class)
```

### Collections

```ruby
expect(array).to include(item)
expect(array).to contain_exactly(1, 2, 3)   # any order
expect(array).to match_array([1, 2, 3])     # any order
expect(array).to start_with(1, 2)
expect(array).to end_with(2, 3)
```

### Errors and Changes

```ruby
expect { action }.to raise_error(ErrorClass)
expect { action }.to raise_error('message')
expect { action }.to change(User, :count).by(1)
expect { action }.to change { user.reload.name }.from('old').to('new')
```

### Rails-Specific

```ruby
expect(response).to have_http_status(:success)
expect(response).to have_http_status(200)
expect(response).to redirect_to(path)
expect { action }.to have_enqueued_job(JobClass)
```

## Mocks, Stubs, and Doubles

### Test Doubles

```ruby
# Basic double
book = double('book', title: 'RSpec Book', pages: 300)

# Verifying double (checks against real class)
book = instance_double('Book', title: 'RSpec Book')
```

### Stubbing Methods

```ruby
# On test doubles
allow(book).to receive(:title).and_return('New Title')
allow(book).to receive(:available?).and_return(true)

# On real objects
user = User.new
allow(user).to receive(:admin?).and_return(true)

# Chaining
allow(user).to receive_message_chain(:articles, :published).and_return([article])
```

### Message Expectations

```ruby
# Expect method to be called
expect(mailer).to receive(:deliver).and_return(true)

# With specific arguments
expect(service).to receive(:call).with(user, { notify: true })

# Number of times
expect(logger).to receive(:info).once
expect(logger).to receive(:info).twice
expect(logger).to receive(:info).exactly(3).times
expect(logger).to receive(:info).at_least(:once)
```

### Spies

```ruby
# Create spy
invitation = spy('invitation')
user.accept_invitation(invitation)

# Verify after the fact
expect(invitation).to have_received(:accept)
expect(invitation).to have_received(:accept).with(mailer)
```

## DRY Testing Techniques

### Before Hooks

```ruby
RSpec.describe ArticlesController do
  before(:each) do
    @user = create(:user)
    sign_in @user
  end

  # OR using subject
  subject { create(:article) }

  it 'has a title' do
    expect(subject.title).to be_present
  end
end
```

### Let and Let

```ruby
describe Article do
  let(:article) { create(:article) }           # Lazy-loaded
  let!(:published) { create(:article, :published) }  # Eager-loaded

  it 'can access article' do
    expect(article).to be_valid
  end
end
```

### Shared Examples

```ruby
# Define shared examples
RSpec.shared_examples 'a timestamped model' do
  it 'has created_at' do
    expect(subject).to respond_to(:created_at)
  end

  it 'has updated_at' do
    expect(subject).to respond_to(:updated_at)
  end
end

# Use shared examples
describe Article do
  it_behaves_like 'a timestamped model'
end

describe Comment do
  it_behaves_like 'a timestamped model'
end
```

### Shared Contexts

```ruby
RSpec.shared_context 'authenticated user' do
  let(:current_user) { create(:user) }

  before do
    sign_in current_user
  end
end

describe ArticlesController do
  include_context 'authenticated user'

  # Tests use current_user and are signed in
end
```

## TDD Workflow

### Red-Green-Refactor Cycle

1. **Red**: Write a failing test first

```ruby
describe User do
  it 'has a full name' do
    user = User.new(first_name: 'John', last_name: 'Doe')
    expect(user.full_name).to eq('John Doe')
  end
end
# Fails: undefined method `full_name'
```

2. **Green**: Write minimal code to pass

```ruby
class User
  def full_name
    "#{first_name} #{last_name}"
  end
end
# Passes!
```

3. **Refactor**: Improve code while keeping tests green

### Testing Strategy

**Start with system specs** for user-facing features:

- Tests complete workflows
- Highest confidence
- Slowest to run

**Drop to request specs** for API/controller logic:

- Test HTTP interactions
- Faster than system specs
- Cover authentication, authorization, edge cases

**Use model specs** for business logic:

- Test calculations, validations, scopes
- Fast and focused
- Most of your test suite

## Configuration Best Practices

### spec/rails_helper.rb

```ruby
require 'spec_helper'
ENV['RAILS_ENV'] ||= 'test'
require_relative '../config/environment'
abort("Run in production!") if Rails.env.production?
require 'rspec/rails'

# Auto-require support files
Dir[Rails.root.join('spec', 'support', '**', '*.rb')].sort.each { |f| require f }

RSpec.configure do |config|
  # Use transactional fixtures
  config.use_transactional_fixtures = true

  # Infer spec type from file location
  config.infer_spec_type_from_file_location!

  # Filter Rails backtrace
  config.filter_rails_from_backtrace!

  # Include FactoryBot methods
  config.include FactoryBot::Syntax::Methods

  # Include request helpers
  config.include RequestHelpers, type: :request

  # Capybara configuration for system specs
  config.before(:each, type: :system) do
    driven_by :selenium_chrome_headless
  end
end
```

### spec/spec_helper.rb

```ruby
RSpec.configure do |config|
  # Show detailed failure messages
  config.example_status_persistence_file_path = "spec/examples.txt"

  # Disable monkey patching (use expect syntax only)
  config.disable_monkey_patching!

  # Output warnings
  config.warnings = true

  # Profile slowest tests
  config.profile_examples = 10 if ENV['PROFILE']

  # Run specs in random order
  config.order = :random
  Kernel.srand config.seed
end
```

## Common Patterns

### Testing Background Jobs

```ruby
describe 'background jobs', type: :job do
  it 'enqueues the job' do
    expect {
      SendEmailJob.perform_later(user)
    }.to have_enqueued_job(SendEmailJob).with(user)
  end

  it 'performs the job' do
    expect {
      SendEmailJob.perform_now(user)
    }.to change { ActionMailer::Base.deliveries.count }.by(1)
  end
end
```

### Testing Mailers

```ruby
describe UserMailer, type: :mailer do
  describe '#welcome_email' do
    let(:user) { create(:user) }
    let(:mail) { UserMailer.welcome_email(user) }

    it 'renders the subject' do
      expect(mail.subject).to eq('Welcome!')
    end

    it 'renders the receiver email' do
      expect(mail.to).to eq([user.email])
    end

    it 'renders the sender email' do
      expect(mail.from).to eq(['noreply@example.com'])
    end

    it 'contains the user name' do
      expect(mail.body.encoded).to include(user.name)
    end
  end
end
```

### Testing File Uploads

```ruby
describe 'file upload', type: :system do
  it 'allows user to upload avatar' do
    user = create(:user)
    sign_in user

    visit edit_profile_path
    attach_file 'Avatar', Rails.root.join('spec', 'fixtures', 'avatar.jpg')
    click_button 'Update Profile'

    expect(page).to have_content('Profile updated')
    expect(user.reload.avatar).to be_attached
  end
end
```

## Performance Tips

1. **Use let instead of before** for lazy loading
2. **Avoid database calls** when testing logic (use mocks)
3. **Use build instead of create** when persistence isn't needed
4. **Use build_stubbed** for non-persisted objects with associations
5. **Tag slow tests** and exclude them during development:

   ```ruby
   it 'slow test', :slow do
     # test code
   end

   # Run with: rspec --tag ~slow
   ```

## When to Use Each Spec Type

- **Model specs**: Business logic, calculations, validations, scopes
- **Request specs**: API endpoints, authentication, authorization, JSON responses
- **System specs**: User workflows, JavaScript interactions, form submissions
- **Mailer specs**: Email content, recipients, attachments
- **Job specs**: Background job enqueueing and execution
- **Helper specs**: View helper methods
- **Routing specs**: Custom routes (usually not needed)

## Quick Reference

**Most Common Commands:**

```bash
rspec                          # Run all specs
rspec spec/models              # Run model specs
rspec --tag ~slow              # Exclude slow specs
rspec --only-failures          # Rerun failures
rspec --format documentation   # Readable output
rspec --profile               # Show slowest specs
```

**Most Common Matchers:**

- `eq(expected)` - value equality
- `be_truthy` / `be_falsy` - truthiness
- `include(item)` - collection membership
- `raise_error(Error)` - exceptions
- `change { }.by(n)` - state changes

**Most Common Stubs:**

- `allow(obj).to receive(:method)` - stub method
- `expect(obj).to receive(:method)` - expect call
- `double('name', method: value)` - create double

---

## Reference Documentation

For detailed information on specific topics, see the references directory:

- **[Core Concepts](./references/core_concepts.md)** - Describe blocks, contexts, hooks, subject, let
- **[Matchers Guide](./references/matchers.md)** - Complete matcher reference with examples
- **[Mocking and Stubbing](./references/mocking.md)** - Test doubles, stubs, spies, message expectations
- **[Rails Testing](./references/rails_testing.md)** - Rails-specific spec types and helpers
- **[Factory Bot](./references/factory_bot.md)** - Test data strategies and patterns
- **[Best Practices](./references/best_practices.md)** - Testing philosophy, patterns, and anti-patterns
- **[Configuration](./references/configuration.md)** - Setup, formatters, and optimization

## Common Scenarios

### Debugging Failing Tests

```ruby
# Use save_and_open_page in system specs
scenario 'user creates article' do
  visit new_article_path
  save_and_open_page  # Opens browser with current page state
  # ...
end

# Print response body in request specs
it 'creates article' do
  post '/articles', params: { ... }
  puts response.body  # Debug API responses
  expect(response).to be_successful
end

# Use binding.pry for interactive debugging
it 'calculates total' do
  order = create(:order)
  binding.pry  # Pause execution here
  expect(order.total).to eq(100)
end
```

### Testing Complex Queries

```ruby
describe '.search' do
  let!(:ruby_article) { create(:article, title: 'Ruby Guide', body: 'Ruby content') }
  let!(:rails_article) { create(:article, title: 'Rails Guide', body: 'Rails content') }

  it 'finds articles by title' do
    results = Article.search('Ruby')
    expect(results).to include(ruby_article)
    expect(results).not_to include(rails_article)
  end

  it 'finds articles by body' do
    results = Article.search('Rails content')
    expect(results).to include(rails_article)
  end
end
```

### Testing Callbacks

```ruby
describe 'callbacks' do
  describe 'after_create' do
    it 'sends welcome email' do
      expect(UserMailer).to receive(:welcome_email)
        .with(an_instance_of(User))
        .and_return(double(deliver_later: true))

      create(:user)
    end
  end

  describe 'before_save' do
    it 'normalizes email' do
      user = create(:user, email: 'USER@EXAMPLE.COM')
      expect(user.email).to eq('user@example.com')
    end
  end
end
```

This skill provides comprehensive RSpec testing guidance. For specific scenarios or advanced techniques, refer to the detailed reference documentation in the `references/` directory.
