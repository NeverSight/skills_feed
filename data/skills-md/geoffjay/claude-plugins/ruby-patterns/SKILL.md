---
name: ruby-patterns
description: Modern Ruby idioms, design patterns, metaprogramming techniques, and best practices. Use when writing Ruby code or refactoring for clarity.
---

# Ruby Patterns Skill

## Tier 1: Quick Reference - Common Idioms

### Conditional Assignment

```ruby
# Set if nil
value ||= default_value

# Set if falsy (nil or false)
value = value || default_value

# Safe navigation
user&.profile&.avatar&.url
```

### Array and Hash Shortcuts

```ruby
# Array creation
%w[apple banana orange]  # ["apple", "banana", "orange"]
%i[name email age]        # [:name, :email, :age]

# Hash creation
{ name: 'John', age: 30 }  # Symbol keys
{ 'name' => 'John' }       # String keys

# Hash access with default
hash.fetch(:key, default)
hash[:key] || default
```

### Enumerable Shortcuts

```ruby
# Transformation
array.map(&:upcase)
array.select(&:active?)
array.reject(&:empty?)

# Aggregation
array.sum
array.max
array.min
numbers.reduce(:+)

# Finding
array.find(&:valid?)
array.any?(&:present?)
array.all?(&:valid?)
```

### String Operations

```ruby
# Interpolation
"Hello #{name}!"

# Safe interpolation
"Result: %{value}" % { value: result }

# Multiline
<<~TEXT
  Heredoc with indentation
  removed automatically
TEXT
```

### Block Syntax

```ruby
# Single line - use braces
array.map { |x| x * 2 }

# Multi-line - use do/end
array.each do |item|
  process(item)
  log(item)
end

# Symbol to_proc
array.map(&:to_s)
array.select(&:even?)
```

### Guard Clauses

```ruby
def process(user)
  return unless user
  return unless user.active?

  # Main logic here
end
```

### Case Statements

```ruby
# Traditional
case status
when 'active'
  activate
when 'inactive'
  deactivate
end

# With ranges
case age
when 0..17
  'minor'
when 18..64
  'adult'
else
  'senior'
end
```

---

## Tier 2: Detailed Instructions - Design Patterns

### Creational Patterns

**Factory Pattern:**
```ruby
class UserFactory
  def self.create(type, attributes)
    case type
    when :admin
      AdminUser.new(attributes)
    when :member
      MemberUser.new(attributes)
    when :guest
      GuestUser.new(attributes)
    else
      raise ArgumentError, "Unknown user type: #{type}"
    end
  end
end

# Usage
user = UserFactory.create(:admin, name: 'John', email: 'john@example.com')
```

**Builder Pattern:**
```ruby
class QueryBuilder
  def initialize
    @conditions = []
    @order = nil
    @limit = nil
  end

  def where(condition)
    @conditions << condition
    self
  end

  def order(column)
    @order = column
    self
  end

  def limit(count)
    @limit = count
    self
  end

  def build
    query = "SELECT * FROM users"
    query += " WHERE #{@conditions.join(' AND ')}" if @conditions.any?
    query += " ORDER BY #{@order}" if @order
    query += " LIMIT #{@limit}" if @limit
    query
  end
end

# Usage
query = QueryBuilder.new
  .where("active = true")
  .where("age > 18")
  .order("created_at DESC")
  .limit(10)
  .build
```

**Singleton Pattern:**
```ruby
require 'singleton'

class Configuration
  include Singleton

  attr_accessor :api_key, :timeout

  def initialize
    @api_key = ENV['API_KEY']
    @timeout = 30
  end
end

# Usage
config = Configuration.instance
config.api_key = 'new_key'
```

### Structural Patterns

**Decorator Pattern:**
```ruby
# Simple decorator
class User
  attr_accessor :name, :email

  def initialize(name, email)
    @name = name
    @email = email
  end
end

class AdminUser < SimpleDelegator
  def permissions
    [:read, :write, :delete, :admin]
  end

  def admin?
    true
  end
end

# Usage
user = User.new('John', 'john@example.com')
admin = AdminUser.new(user)
admin.name  # Delegates to user
admin.admin?  # From decorator

# Using Ruby's Forwardable
require 'forwardable'

class UserDecorator
  extend Forwardable
  def_delegators :@user, :name, :email

  def initialize(user)
    @user = user
  end

  def display_name
    "#{@user.name} (#{@user.email})"
  end
end
```

**Adapter Pattern:**
```ruby
# Adapting third-party API
class LegacyPaymentGateway
  def make_payment(amount, card)
    # Legacy implementation
  end
end

class PaymentAdapter
  def initialize(gateway)
    @gateway = gateway
  end

  def process(amount:, card_number:)
    card = { number: card_number }
    @gateway.make_payment(amount, card)
  end
end

# Usage
legacy = LegacyPaymentGateway.new
adapter = PaymentAdapter.new(legacy)
adapter.process(amount: 100, card_number: '1234')
```

**Composite Pattern:**
```ruby
class File
  attr_reader :name, :size

  def initialize(name, size)
    @name = name
    @size = size
  end

  def total_size
    size
  end
end

class Directory
  attr_reader :name

  def initialize(name)
    @name = name
    @contents = []
  end

  def add(item)
    @contents << item
  end

  def total_size
    @contents.sum(&:total_size)
  end
end

# Usage
root = Directory.new('root')
root.add(File.new('file1.txt', 100))
subdir = Directory.new('subdir')
subdir.add(File.new('file2.txt', 200))
root.add(subdir)
root.total_size  # 300
```

### Behavioral Patterns

**Strategy Pattern:**
```ruby
class PaymentProcessor
  def initialize(strategy)
    @strategy = strategy
  end

  def process(amount)
    @strategy.process(amount)
  end
end

class CreditCardStrategy
  def process(amount)
    puts "Processing #{amount} via credit card"
  end
end

class PayPalStrategy
  def process(amount)
    puts "Processing #{amount} via PayPal"
  end
end

# Usage
processor = PaymentProcessor.new(CreditCardStrategy.new)
processor.process(100)

processor = PaymentProcessor.new(PayPalStrategy.new)
processor.process(100)
```

**Observer Pattern:**
```ruby
require 'observer'

class Order
  include Observable

  attr_reader :status

  def initialize
    @status = :pending
  end

  def complete!
    @status = :completed
    changed
    notify_observers(self)
  end
end

class EmailNotifier
  def update(order)
    puts "Sending email: Order #{order.object_id} is #{order.status}"
  end
end

class SMSNotifier
  def update(order)
    puts "Sending SMS: Order #{order.object_id} is #{order.status}"
  end
end

# Usage
order = Order.new
order.add_observer(EmailNotifier.new)
order.add_observer(SMSNotifier.new)
order.complete!  # Both notifiers triggered
```

**Command Pattern:**
```ruby
class Command
  def execute
    raise NotImplementedError
  end

  def undo
    raise NotImplementedError
  end
end

class CreateUserCommand < Command
  def initialize(user_service, params)
    @user_service = user_service
    @params = params
    @user = nil
  end

  def execute
    @user = @user_service.create(@params)
  end

  def undo
    @user_service.delete(@user.id) if @user
  end
end

class CommandInvoker
  def initialize
    @history = []
  end

  def execute(command)
    command.execute
    @history << command
  end

  def undo
    command = @history.pop
    command&.undo
  end
end

# Usage
invoker = CommandInvoker.new
command = CreateUserCommand.new(user_service, { name: 'John' })
invoker.execute(command)
invoker.undo  # Rolls back
```

### Metaprogramming Techniques

**Dynamic Method Definition:**
```ruby
class Model
  ATTRIBUTES = [:name, :email, :age]

  ATTRIBUTES.each do |attr|
    define_method(attr) do
      instance_variable_get("@#{attr}")
    end

    define_method("#{attr}=") do |value|
      instance_variable_set("@#{attr}", value)
    end
  end
end

# Usage
model = Model.new
model.name = 'John'
model.name  # 'John'
```

**Method Missing:**
```ruby
class DynamicFinder
  def initialize(data)
    @data = data
  end

  def method_missing(method_name, *args)
    if method_name.to_s.start_with?('find_by_')
      attribute = method_name.to_s.sub('find_by_', '')
      @data.find { |item| item[attribute.to_sym] == args.first }
    else
      super
    end
  end

  def respond_to_missing?(method_name, include_private = false)
    method_name.to_s.start_with?('find_by_') || super
  end
end

# Usage
data = [
  { name: 'John', email: 'john@example.com' },
  { name: 'Jane', email: 'jane@example.com' }
]
finder = DynamicFinder.new(data)
finder.find_by_name('John')  # { name: 'John', ... }
finder.find_by_email('jane@example.com')  # { name: 'Jane', ... }
```

**Class Macros (DSL):**
```ruby
class Validator
  def self.validates(attribute, rules)
    @validations ||= []
    @validations << [attribute, rules]

    define_method(:valid?) do
      self.class.instance_variable_get(:@validations).all? do |attr, rules|
        value = send(attr)
        validate_rules(value, rules)
      end
    end
  end

  def validate_rules(value, rules)
    rules.all? do |rule, param|
      case rule
      when :presence
        !value.nil? && !value.empty?
      when :length
        value.length <= param
      when :format
        value.match?(param)
      else
        true
      end
    end
  end
end

class User < Validator
  attr_accessor :name, :email

  validates :name, presence: true, length: 50
  validates :email, presence: true, format: /@/

  def initialize(name, email)
    @name = name
    @email = email
  end
end

# Usage
user = User.new('John', 'john@example.com')
user.valid?  # true
```

**Module Inclusion Hooks:**
```ruby
module Timestampable
  def self.included(base)
    base.class_eval do
      attr_accessor :created_at, :updated_at

      define_method(:touch) do
        self.updated_at = Time.now
      end
    end
  end
end

# Using ActiveSupport::Concern for cleaner syntax
module Trackable
  extend ActiveSupport::Concern

  included do
    attr_accessor :tracked_at
  end

  class_methods do
    def tracking_enabled?
      true
    end
  end

  def track!
    self.tracked_at = Time.now
  end
end

class Model
  include Timestampable
  include Trackable
end

# Usage
model = Model.new
model.touch
model.track!
```

---

## Tier 3: Resources & Examples

### Performance Patterns

**Memoization:**
```ruby
# Basic memoization
def expensive_calculation
  @expensive_calculation ||= begin
    # Expensive operation
    sleep 1
    'result'
  end
end

# Memoization with parameters
def user_posts(user_id)
  @user_posts ||= {}
  @user_posts[user_id] ||= Post.where(user_id: user_id).to_a
end

# Thread-safe memoization
require 'concurrent'

class Service
  def initialize
    @cache = Concurrent::Map.new
  end

  def get(key)
    @cache.compute_if_absent(key) do
      expensive_operation(key)
    end
  end
end
```

**Lazy Evaluation:**
```ruby
# Lazy enumeration for large datasets
(1..Float::INFINITY)
  .lazy
  .select { |n| n % 3 == 0 }
  .first(10)

# Lazy file processing
File.foreach('large_file.txt').lazy
  .select { |line| line.include?('ERROR') }
  .map(&:strip)
  .first(100)

# Custom lazy enumerator
def lazy_range(start, finish)
  Enumerator.new do |yielder|
    current = start
    while current <= finish
      yielder << current
      current += 1
    end
  end.lazy
end
```

**Struct for Value Objects:**
```ruby
# Simple value object
User = Struct.new(:name, :email, :age) do
  def adult?
    age >= 18
  end

  def to_s
    "#{name} <#{email}>"
  end
end

# Keyword arguments (Ruby 2.5+)
User = Struct.new(:name, :email, :age, keyword_init: true)
user = User.new(name: 'John', email: 'john@example.com', age: 30)

# Data class (Ruby 3.2+)
User = Data.define(:name, :email, :age) do
  def adult?
    age >= 18
  end
end
```

### Error Handling Patterns

**Custom Exceptions:**
```ruby
class ApplicationError < StandardError; end
class ValidationError < ApplicationError; end
class NotFoundError < ApplicationError; end
class AuthenticationError < ApplicationError; end

class UserService
  def create(params)
    raise ValidationError, 'Name is required' if params[:name].nil?

    User.create(params)
  rescue ActiveRecord::RecordNotFound => e
    raise NotFoundError, e.message
  end
end

# Usage with rescue
begin
  user_service.create(params)
rescue ValidationError => e
  render json: { error: e.message }, status: 422
rescue NotFoundError => e
  render json: { error: e.message }, status: 404
rescue ApplicationError => e
  render json: { error: e.message }, status: 500
end
```

**Result Object Pattern:**
```ruby
class Result
  attr_reader :value, :error

  def initialize(success, value, error = nil)
    @success = success
    @value = value
    @error = error
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def self.success(value)
    new(true, value)
  end

  def self.failure(error)
    new(false, nil, error)
  end

  def on_success(&block)
    block.call(value) if success?
    self
  end

  def on_failure(&block)
    block.call(error) if failure?
    self
  end
end

# Usage
def create_user(params)
  user = User.new(params)
  if user.valid?
    user.save
    Result.success(user)
  else
    Result.failure(user.errors)
  end
end

result = create_user(params)
result
  .on_success { |user| send_welcome_email(user) }
  .on_failure { |errors| log_errors(errors) }
```

### Testing Patterns

**Shared Examples:**
```ruby
RSpec.shared_examples 'a timestamped model' do
  it 'has created_at' do
    expect(subject).to respond_to(:created_at)
  end

  it 'has updated_at' do
    expect(subject).to respond_to(:updated_at)
  end

  it 'sets timestamps on create' do
    subject.save
    expect(subject.created_at).to be_present
    expect(subject.updated_at).to be_present
  end
end

RSpec.describe User do
  it_behaves_like 'a timestamped model'
end
```

### Functional Programming Patterns

**Composition:**
```ruby
# Function composition
add_one = ->(x) { x + 1 }
double = ->(x) { x * 2 }
square = ->(x) { x ** 2 }

# Manual composition
result = square.call(double.call(add_one.call(5)))  # ((5+1)*2)^2 = 144

# Compose helper
def compose(*fns)
  ->(x) { fns.reverse.reduce(x) { |acc, fn| fn.call(acc) } }
end

composed = compose(square, double, add_one)
composed.call(5)  # 144
```

**Immutability:**
```ruby
# Frozen objects
class ImmutablePoint
  attr_reader :x, :y

  def initialize(x, y)
    @x = x
    @y = y
    freeze
  end

  def move(dx, dy)
    ImmutablePoint.new(@x + dx, @y + dy)
  end
end

# Frozen literals (Ruby 3+)
# frozen_string_literal: true

NAME = 'John'  # Frozen by default
```

### Additional Resources

See `assets/` directory for:
- `idioms-cheatsheet.md` - Quick reference for Ruby idioms
- `design-patterns.rb` - Complete implementations of all patterns
- `metaprogramming-examples.rb` - Advanced metaprogramming techniques

See `references/` directory for:
- Style guides and best practices
- Performance optimization examples
- Testing pattern library
