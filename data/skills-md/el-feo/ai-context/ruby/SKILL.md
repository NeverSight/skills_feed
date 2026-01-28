---
name: ruby
description: Comprehensive Ruby development skill covering language fundamentals, object-oriented design patterns, error handling strategies, performance optimization, modern Ruby 3.x features (pattern matching, ractors, typed Ruby), testing patterns, metaprogramming, concurrency, and Rails-specific best practices. Use when writing Ruby code, refactoring, implementing design patterns, handling exceptions, optimizing performance, writing tests, or applying Ruby idioms and conventions.
---

# Ruby Development Skill

## Purpose

This skill provides comprehensive guidance for Ruby development, covering language fundamentals, object-oriented design, error handling, performance optimization, and modern Ruby (3.x+) features. It synthesizes knowledge from Ruby internals, best practices, and official documentation to help Claude write idiomatic, maintainable, and performant Ruby code.

## When to Use This Skill

Use this skill when:

- Writing or reviewing Ruby code
- Debugging Ruby applications
- Optimizing Ruby performance
- Implementing object-oriented designs
- Handling errors and exceptions
- Working with Ruby's standard library
- Using modern Ruby features (pattern matching, types, fibers, ractors)
- Building Rails applications or Ruby gems

## Ruby Philosophy and Core Principles

### Matz's Design Philosophy

Ruby is designed to make programmers happy. It prioritizes:

1. **Developer Productivity** - Write less code to accomplish more
2. **Readability** - Code should read like natural language
3. **Flexibility** - Multiple ways to accomplish tasks (TMTOWTDI - There's More Than One Way To Do It)
4. **Object-Oriented Everything** - Everything is an object, including primitives
5. **Duck Typing** - "If it walks like a duck and quacks like a duck, it's a duck"

### Ruby's Core Characteristics

```ruby
# Everything is an object
5.times { puts "Hello" }          # Integer is an object
"hello".upcase                    # String is an object
nil.class                         # => NilClass

# Blocks are first-class citizens
[1, 2, 3].map { |n| n * 2 }      # => [2, 4, 6]

# Open classes - can modify any class
class String
  def shout
    "#{upcase}!"
  end
end

"hello".shout                     # => "HELLO!"

# Duck typing - focus on behavior, not type
def process(thing)
  thing.call if thing.respond_to?(:call)
end
```

## Object-Oriented Design in Ruby

### The Ruby Object Model

Understanding Ruby's object model is crucial for effective programming:

```ruby
# Class hierarchy
class Animal
  def speak
    "Some sound"
  end
end

class Dog < Animal
  def speak
    "Woof!"
  end
end

# Every class is an instance of Class
Dog.class                         # => Class
Dog.superclass                    # => Animal
Animal.superclass                 # => Object
Object.superclass                 # => BasicObject

# Singleton methods (eigenclass/metaclass)
dog = Dog.new
def dog.name
  "Buddy"
end

dog.name                          # => "Buddy"
Dog.new.name                      # NoMethodError
```

### Composition Over Inheritance

Prefer composition and modules over deep inheritance hierarchies:

```ruby
# ❌ Bad: Deep inheritance
class Vehicle
end

class LandVehicle < Vehicle
end

class Car < LandVehicle
end

class SportsCar < Car
end

# ✅ Good: Composition with modules
module Drivable
  def drive
    "Driving..."
  end
end

module Flyable
  def fly
    "Flying..."
  end
end

class Car
  include Drivable
end

class Plane
  include Flyable
  include Drivable  # Can taxi on ground
end
```

### Single Responsibility Principle

Each class should have one reason to change:

```ruby
# ❌ Bad: Multiple responsibilities
class User
  def save
    # Database logic
  end

  def send_email
    # Email logic
  end

  def generate_report
    # Report logic
  end
end

# ✅ Good: Separate concerns
class User
  def save
    UserRepository.new.save(self)
  end
end

class UserMailer
  def send_welcome_email(user)
    # Email logic
  end
end

class UserReportGenerator
  def generate(user)
    # Report logic
  end
end
```

### Dependency Injection

Inject dependencies rather than hardcoding them:

```ruby
# ❌ Bad: Hard dependency
class OrderProcessor
  def process(order)
    PaymentGateway.new.charge(order.amount)
    EmailService.new.send_confirmation(order)
  end
end

# ✅ Good: Dependency injection
class OrderProcessor
  def initialize(payment_gateway: PaymentGateway.new,
                 email_service: EmailService.new)
    @payment_gateway = payment_gateway
    @email_service = email_service
  end

  def process(order)
    @payment_gateway.charge(order.amount)
    @email_service.send_confirmation(order)
  end
end
```

### Law of Demeter (Principle of Least Knowledge)

Avoid reaching through multiple objects:

```ruby
# ❌ Bad: Train wreck
customer.orders.last.line_items.first.price

# ✅ Good: Delegate or encapsulate
class Customer
  def last_order_first_item_price
    orders.last&.first_item_price
  end
end

class Order
  def first_item_price
    line_items.first&.price
  end
end

customer.last_order_first_item_price
```

## Error Handling and Exceptions

### The Exception Hierarchy

```
Exception
├── NoMemoryError
├── ScriptError
│   ├── LoadError
│   ├── NotImplementedError
│   └── SyntaxError
├── SignalException
│   └── Interrupt
├── StandardError (Default rescue catches this)
│   ├── ArgumentError
│   ├── IOError
│   │   └── EOFError
│   ├── IndexError
│   ├── LocalJumpError
│   ├── NameError
│   │   └── NoMethodError
│   ├── RangeError
│   ├── RegexpError
│   ├── RuntimeError (Default raise creates this)
│   ├── SecurityError
│   ├── SystemCallError
│   ├── ThreadError
│   ├── TypeError
│   └── ZeroDivisionError
├── SystemExit
└── SystemStackError
```

### Exception Handling Best Practices

#### 1. Exceptions Should Be Exceptional

Use exceptions for exceptional cases, not control flow:

```ruby
# ❌ Bad: Using exceptions for control flow
def find_user(id)
  user = User.find(id)
rescue ActiveRecord::RecordNotFound
  nil
end

# ✅ Good: Use explicit checks
def find_user(id)
  User.find_by(id: id)
end
```

#### 2. Rescue Specific Exceptions

Always rescue specific exceptions, never bare rescue:

```ruby
# ❌ Bad: Catches everything, including SystemExit
begin
  dangerous_operation
rescue
  # Too broad!
end

# ✅ Good: Rescue specific exceptions
begin
  dangerous_operation
rescue NetworkError, TimeoutError => e
  logger.error("Network issue: #{e.message}")
  retry_operation
end
```

#### 3. Fail Fast, Fail Loudly

Let errors propagate unless you can handle them meaningfully:

```ruby
# ❌ Bad: Swallowing exceptions
def process_data(data)
  result = parse(data)
rescue => e
  nil  # Silent failure!
end

# ✅ Good: Let it fail or handle meaningfully
def process_data(data)
  parse(data)
rescue ParseError => e
  logger.error("Failed to parse data: #{e.message}")
  raise  # Re-raise to propagate
end
```

#### 4. Use ensure for Cleanup

Always use `ensure` for cleanup code:

```ruby
# ✅ Proper resource management
def process_file(filename)
  file = File.open(filename)
  process(file)
ensure
  file&.close
end

# Better: Use blocks that auto-close
def process_file(filename)
  File.open(filename) do |file|
    process(file)
  end  # Automatically closed
end
```

#### 5. Custom Exceptions for Domain Logic

Create custom exceptions for your domain:

```ruby
# Define custom exceptions
class PaymentError < StandardError; end
class InsufficientFundsError < PaymentError; end
class InvalidCardError < PaymentError; end

# Use them meaningfully
def charge_card(card, amount)
  raise InvalidCardError, "Card expired" if card.expired?
  raise InsufficientFundsError if balance < amount

  process_charge(card, amount)
end

# Caller can handle appropriately
begin
  charge_card(card, 100)
rescue InsufficientFundsError => e
  notify_user("Insufficient funds")
rescue InvalidCardError => e
  notify_user("Please update your card")
rescue PaymentError => e
  # Catch all payment errors
  logger.error("Payment failed: #{e.message}")
end
```

#### 6. The Weirich raise/fail Convention

Use `fail` for exceptions you expect to be rescued, `raise` for re-raising:

```ruby
def process_order(order)
  fail ArgumentError, "Order cannot be nil" if order.nil?

  begin
    payment_gateway.charge(order)
  rescue PaymentError => e
    logger.error("Payment failed: #{e.message}")
    raise  # Re-raise with raise
  end
end
```

#### 7. Provide Context in Exceptions

Include helpful information in exception messages:

```ruby
# ❌ Bad: Vague message
raise "Invalid input"

# ✅ Good: Descriptive message with context
raise ArgumentError, "Expected positive integer for age, got: #{age.inspect}"
```

### Alternative Error Handling Patterns

#### Result Objects

Return result objects instead of raising exceptions:

```ruby
class Result
  attr_reader :value, :error

  def initialize(value: nil, error: nil)
    @value = value
    @error = error
  end

  def success?
    error.nil?
  end

  def failure?
    !success?
  end
end

def divide(a, b)
  return Result.new(error: "Division by zero") if b.zero?
  Result.new(value: a / b)
end

result = divide(10, 2)
if result.success?
  puts result.value
else
  puts "Error: #{result.error}"
end
```

#### Caller-Supplied Fallback Strategy

Let callers define error handling:

```ruby
def fetch_user(id, &fallback)
  User.find(id)
rescue ActiveRecord::RecordNotFound => e
  fallback ? fallback.call(e) : raise
end

# Usage
user = fetch_user(999) { |e| User.new(name: "Guest") }
```

## Ruby Performance and Optimization

### Understanding Ruby's VM (YARV)

Ruby 3.x uses YARV (Yet Another Ruby VM) with JIT compilation:

```ruby
# Enable JIT (YJIT in Ruby 3.1+)
# Run with: ruby --yjit your_script.rb

# Check JIT status
puts "JIT enabled: #{defined?(RubyVM::YJIT)}"

# Profile JIT compilation
RubyVM::YJIT.runtime_stats if defined?(RubyVM::YJIT)
```

### Memory Management and Garbage Collection

Ruby uses generational garbage collection:

```ruby
# Check GC stats
GC.stat
# => {:count=>23, :heap_allocated_pages=>145, ...}

# Manual GC control (rarely needed)
GC.disable  # Disable GC temporarily
# ... do intensive work
GC.enable
GC.start    # Force GC

# Monitor object allocations
before = GC.stat(:total_allocated_objects)
# ... your code
after = GC.stat(:total_allocated_objects)
puts "Allocated: #{after - before} objects"
```

### Performance Best Practices

#### 1. Avoid Creating Unnecessary Objects

```ruby
# ❌ Bad: Creates many string objects
1000.times do |i|
  "User #{i}"  # New string each time
end

# ✅ Good: Reuse strings with interpolation
template = "User %d"
1000.times do |i|
  template % i
end

# ✅ Even better: Use frozen strings
MESSAGE = "Processing".freeze
```

#### 2. Use Symbols for Repeated Strings

```ruby
# ❌ Bad: Creates new string objects
hash = { "name" => "John", "age" => 30 }

# ✅ Good: Symbols are immutable and reused
hash = { name: "John", age: 30 }
```

#### 3. Prefer Enumerable Methods Over Loops

```ruby
# ❌ Bad: Manual loop
result = []
array.each do |item|
  result << item * 2 if item > 0
end

# ✅ Good: Chained enumerable methods
result = array.select { |item| item > 0 }
              .map { |item| item * 2 }

# ✅ Even better: Single pass with each_with_object
result = array.each_with_object([]) do |item, acc|
  acc << item * 2 if item > 0
end
```

#### 4. Use Lazy Enumerables for Large Collections

```ruby
# ❌ Bad: Creates intermediate arrays
(1..1_000_000).select { |n| n.even? }
              .map { |n| n * 2 }
              .first(10)

# ✅ Good: Lazy evaluation
(1..1_000_000).lazy
              .select { |n| n.even? }
              .map { |n| n * 2 }
              .first(10)
```

#### 5. Cache Expensive Computations

```ruby
# ❌ Bad: Recomputes every time
class User
  def full_name
    "#{first_name} #{last_name}".strip
  end
end

# ✅ Good: Memoization
class User
  def full_name
    @full_name ||= "#{first_name} #{last_name}".strip
  end
end

# ⚠️ Careful with nil/false values
def expensive_check
  return @result if defined?(@result)
  @result = compute_result
end
```

## Modern Ruby Features (3.x+)

### Pattern Matching (Ruby 2.7+)

```ruby
# Basic pattern matching
case [1, 2, 3]
in [a, b, c]
  puts "#{a}, #{b}, #{c}"
end

# Hash patterns
case { name: "John", age: 30 }
in { name: "John", age: age }
  puts "John is #{age}"
in { name:, age: }  # Variable punning
  puts "#{name} is #{age}"
end

# Array patterns with rest
case [1, 2, 3, 4, 5]
in [first, *rest, last]
  puts "First: #{first}, Last: #{last}, Rest: #{rest}"
end

# Rightward assignment (Ruby 3.0+)
{ name: "John", age: 30 } => { name:, age: }
puts name  # => "John"

# Guard clauses
case value
in String => s if s.length > 10
  puts "Long string: #{s}"
in String => s
  puts "Short string: #{s}"
end
```

### Endless Method Definition (Ruby 3.0+)

```ruby
# Traditional
def square(x)
  x * x
end

# Endless method (for simple one-liners)
def square(x) = x * x
def full_name = "#{first_name} #{last_name}"
def admin? = role == "admin"
```

### Numbered Parameters (Ruby 2.7+)

```ruby
# Traditional block parameters
[1, 2, 3].map { |n| n * 2 }

# Numbered parameters
[1, 2, 3].map { _1 * 2 }

# Multiple numbered parameters
hash.map { [_1, _2 * 2] }
```

### Rightward Assignment (Ruby 3.0+)

```ruby
# Traditional assignment
result = compute_value()
puts result

# Rightward assignment (useful in method chains)
compute_value() => result
puts result

# Useful for debugging
calculate_price.tap { p _1 } => price
```

### Ractors (Ruby 3.0+) - True Parallelism

```ruby
# Create parallel-safe ractor
r = Ractor.new do
  received = Ractor.receive
  received * 2
end

r.send(21)
r.take  # => 42

# Multiple ractors
results = 4.times.map do |i|
  Ractor.new(i) do |n|
    # Heavy computation
    (1..1000000).reduce(:+) + n
  end
end

results.map(&:take)  # Runs in parallel
```

### Typed Ruby with RBS (Ruby 3.0+)

```ruby
# Define types in .rbs files
# user.rbs
class User
  attr_reader name: String
  attr_reader age: Integer

  def initialize: (name: String, age: Integer) -> void
  def adult?: () -> bool
end

# Use TypeProf to generate signatures
# $ typeprof user.rb

# Validate with Steep or RBS
# $ steep check
```

### Fiber Scheduler (Ruby 3.0+) - Non-blocking I/O

```ruby
require 'async'

# Async execution with fibers
Async do
  Async do
    puts "Task 1 start"
    sleep 2
    puts "Task 1 end"
  end

  Async do
    puts "Task 2 start"
    sleep 1
    puts "Task 2 end"
  end
end
# Both tasks run concurrently
```

## Ruby Standard Library Essentials

### Working with Collections

```ruby
# Array operations
arr = [1, 2, 3, 4, 5]

arr.first(2)                # => [1, 2]
arr.last(2)                 # => [4, 5]
arr.sample                  # Random element
arr.shuffle                 # Randomize order
arr.rotate(2)               # => [3, 4, 5, 1, 2]
arr.combination(2).to_a     # All 2-element combinations
arr.permutation(2).to_a     # All 2-element permutations

# Hash operations
hash = { a: 1, b: 2, c: 3 }

hash.fetch(:d, 0)           # => 0 (default value)
hash.dig(:nested, :key)     # Safe nested access
hash.transform_values(&:to_s)  # => { a: "1", b: "2", c: "3" }
hash.slice(:a, :b)          # => { a: 1, b: 2 }
hash.merge(d: 4)            # Non-destructive merge

# Set operations
require 'set'
s1 = Set[1, 2, 3]
s2 = Set[2, 3, 4]

s1 | s2                     # Union => #<Set: {1, 2, 3, 4}>
s1 & s2                     # Intersection => #<Set: {2, 3}>
s1 - s2                     # Difference => #<Set: {1}>
```

### String Manipulation

```ruby
# String methods
str = "  Hello, World!  "

str.strip                   # => "Hello, World!"
str.split(", ")             # => ["Hello", "World!"]
str.gsub("World", "Ruby")   # => "  Hello, Ruby!  "
str.scan(/\w+/)             # => ["Hello", "World"]
str.start_with?("Hello")    # => false (has spaces)
str.include?("World")       # => true

# String interpolation
name = "John"
age = 30
"#{name} is #{age}"         # => "John is 30"
"2 + 2 = #{2 + 2}"          # => "2 + 2 = 4"

# Heredocs
text = <<~TEXT
  This is a heredoc.
  Indentation is removed.
  Very useful for multi-line strings.
TEXT

# Frozen strings (immutable)
CONSTANT = "immutable".freeze
# Or with magic comment:
# frozen_string_literal: true
```

### File I/O

```ruby
# Reading files
content = File.read("file.txt")
lines = File.readlines("file.txt")

# Block-based reading (auto-closes)
File.open("file.txt") do |file|
  file.each_line do |line|
    puts line
  end
end

# Writing files
File.write("output.txt", "Hello, World!")

File.open("output.txt", "w") do |file|
  file.puts "Line 1"
  file.puts "Line 2"
end

# File operations
File.exist?("file.txt")
File.directory?("path")
File.size("file.txt")
File.mtime("file.txt")      # Modification time

# Directory operations
Dir.glob("**/*.rb")         # Find all Ruby files recursively
Dir.foreach("path") { |file| puts file }
Dir.mkdir("new_dir")
```

### Regular Expressions

```ruby
# Pattern matching
text = "Hello, my email is john@example.com"

# Match operator
text =~ /\w+@\w+\.\w+/      # => 18 (match position)

# Match method
match = text.match(/(\w+)@(\w+)\.(\w+)/)
match[0]                     # => "john@example.com"
match[1]                     # => "john"
match[2]                     # => "example"

# Named captures
match = text.match(/(?<user>\w+)@(?<domain>\w+)\.(?<tld>\w+)/)
match[:user]                 # => "john"
match[:domain]               # => "example"

# Scan for all matches
emails = text.scan(/\w+@\w+\.\w+/)

# Replace with regex
text.gsub(/\b\w{4}\b/, "****")  # Mask 4-letter words
```

## Testing Ruby Code

### Minitest (Standard Library)

```ruby
require 'minitest/autorun'

class UserTest < Minitest::Test
  def setup
    @user = User.new(name: "John", age: 30)
  end

  def test_adult_with_age_over_18
    assert @user.adult?
  end

  def test_name_is_capitalized
    assert_equal "John", @user.name
  end

  def test_invalid_age_raises_error
    assert_raises(ArgumentError) do
      User.new(name: "John", age: -5)
    end
  end

  def teardown
    # Cleanup if needed
  end
end
```

### RSpec (Popular Testing Framework)

```ruby
require 'rspec'

RSpec.describe User do
  let(:user) { User.new(name: "John", age: 30) }

  describe '#adult?' do
    context 'when age is over 18' do
      it 'returns true' do
        expect(user.adult?).to be true
      end
    end

    context 'when age is under 18' do
      let(:user) { User.new(name: "Jane", age: 15) }

      it 'returns false' do
        expect(user.adult?).to be false
      end
    end
  end

  describe '#initialize' do
    it 'raises error for negative age' do
      expect { User.new(name: "John", age: -5) }
        .to raise_error(ArgumentError, /negative age/)
    end
  end

  describe '#name' do
    it 'returns capitalized name' do
      expect(user.name).to eq("John")
    end
  end
end
```

### Testing Best Practices

```ruby
# 1. Use descriptive test names
def test_user_is_adult_when_age_is_over_18
  # Clear what is being tested
end

# 2. Arrange-Act-Assert pattern
def test_order_total
  # Arrange
  order = Order.new
  order.add_item(item: "Book", price: 10)
  order.add_item(item: "Pen", price: 2)

  # Act
  total = order.total

  # Assert
  assert_equal 12, total
end

# 3. Test one thing per test
# ❌ Bad: Tests multiple things
def test_user
  assert user.valid?
  assert_equal "John", user.name
  assert_equal 30, user.age
end

# ✅ Good: Separate tests
def test_user_is_valid
  assert user.valid?
end

def test_user_name
  assert_equal "John", user.name
end

# 4. Use fixtures/factories for test data
# factories.rb
FactoryBot.define do
  factory :user do
    name { "John" }
    age { 30 }
    email { "john@example.com" }
  end
end

# In tests
user = create(:user)
user_attrs = attributes_for(:user)
```

## Common Ruby Patterns and Idioms

### Method Chaining (Fluent Interface)

```ruby
class QueryBuilder
  def initialize
    @conditions = []
    @order = nil
  end

  def where(condition)
    @conditions << condition
    self  # Return self for chaining
  end

  def order(field)
    @order = field
    self
  end

  def to_sql
    sql = "SELECT * FROM users"
    sql += " WHERE #{@conditions.join(' AND ')}" unless @conditions.empty?
    sql += " ORDER BY #{@order}" if @order
    sql
  end
end

# Usage
query = QueryBuilder.new
         .where("age > 18")
         .where("active = true")
         .order("name")
         .to_sql
```

### Builder Pattern

```ruby
class UserBuilder
  def initialize
    @user = User.new
  end

  def with_name(name)
    @user.name = name
    self
  end

  def with_email(email)
    @user.email = email
    self
  end

  def build
    @user
  end
end

# Usage
user = UserBuilder.new
        .with_name("John")
        .with_email("john@example.com")
        .build
```

### Null Object Pattern

```ruby
class NullUser
  def name
    "Guest"
  end

  def admin?
    false
  end

  def logged_in?
    false
  end
end

class UserSession
  def current_user
    @current_user || NullUser.new
  end
end

# Usage - no nil checks needed
session = UserSession.new
puts session.current_user.name  # "Guest" instead of error
```

### Strategy Pattern

```ruby
# Define strategies
class CreditCardPayment
  def process(amount)
    # Credit card logic
  end
end

class PayPalPayment
  def process(amount)
    # PayPal logic
  end
end

# Use strategy
class Order
  def initialize(payment_strategy)
    @payment_strategy = payment_strategy
  end

  def checkout(amount)
    @payment_strategy.process(amount)
  end
end

# Usage
order = Order.new(CreditCardPayment.new)
order.checkout(100)
```

### Observer Pattern

```ruby
require 'observer'

class Order
  include Observable

  attr_reader :status

  def status=(new_status)
    @status = new_status
    changed
    notify_observers(self)
  end
end

class Logger
  def update(order)
    puts "Order status changed to: #{order.status}"
  end
end

class Emailer
  def update(order)
    puts "Sending email about: #{order.status}"
  end
end

# Usage
order = Order.new
order.add_observer(Logger.new)
order.add_observer(Emailer.new)
order.status = "shipped"
```

## Ruby Code Style and Conventions

### Naming Conventions

```ruby
# Classes and Modules: PascalCase
class UserAccount
end

module PaymentProcessing
end

# Methods and Variables: snake_case
def calculate_total_price
  total_amount = 0
end

# Constants: SCREAMING_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Predicate methods: end with ?
def valid?
  errors.empty?
end

def admin?
  role == 'admin'
end

# Dangerous methods: end with !
def save!  # Raises exception on failure
  raise "Invalid" unless valid?
  persist
end

def downcase!  # Mutates the object
  @value = @value.downcase
end
```

### Code Organization

```ruby
# Class organization
class User
  # 1. Extend and include statements
  extend SomeModule
  include AnotherModule

  # 2. Constants
  MAX_NAME_LENGTH = 100

  # 3. Attribute macros
  attr_reader :id
  attr_accessor :name

  # 4. Class methods
  def self.find(id)
    # ...
  end

  # 5. Initialization
  def initialize(name)
    @name = name
  end

  # 6. Public instance methods
  def full_name
    "#{first_name} #{last_name}"
  end

  # 7. Protected methods
  protected

  def internal_helper
    # ...
  end

  # 8. Private methods
  private

  def calculate_something
    # ...
  end
end
```

### Ruby Style Guidelines

```ruby
# Use 2 spaces for indentation
def method_name
  if condition
    do_something
  end
end

# Avoid ternary operators for multi-line
# ❌ Bad
result = some_long_condition ?
         long_true_value :
         long_false_value

# ✅ Good
result = if some_long_condition
          long_true_value
        else
          long_false_value
        end

# Use %w for word arrays
# ❌ Bad
STATES = ['draft', 'published', 'archived']

# ✅ Good
STATES = %w[draft published archived]

# Use symbols for hash keys
# ❌ Bad (when strings aren't needed)
{ 'name' => 'John', 'age' => 30 }

# ✅ Good
{ name: 'John', age: 30 }

# Use guard clauses
# ❌ Bad
def process(value)
  if value
    if value.valid?
      # ... main logic
    end
  end
end

# ✅ Good
def process(value)
  return unless value
  return unless value.valid?

  # ... main logic
end

# Avoid returning from ensure
# ❌ Bad - return value is ignored
def bad_example
  return 42
ensure
  return 0  # This overrides!
end

# ✅ Good
def good_example
  result = 42
ensure
  cleanup
end
```

## Debugging Ruby Code

### Using pry for Debugging

```ruby
require 'pry'

def complex_method(data)
  result = transform(data)
  binding.pry  # Execution pauses here
  result * 2
end

# In pry session:
# - ls: List available methods
# - show-method method_name: Show method source
# - cd object: Enter object context
# - whereami: Show context
# - continue: Resume execution
```

### Using ruby/debug (Ruby 3.1+)

```ruby
require 'debug'

def calculate(x, y)
  debugger  # Execution pauses here
  result = x + y
  result
end

# Commands:
# - step: Step into
# - next: Step over
# - continue: Resume
# - info: Show information
# - break: Set breakpoint
```

### Logging Best Practices

```ruby
require 'logger'

logger = Logger.new(STDOUT)
logger.level = Logger::INFO

# Different log levels
logger.debug("Detailed debug information")
logger.info("Informational messages")
logger.warn("Warning messages")
logger.error("Error messages")
logger.fatal("Fatal errors")

# Structured logging
logger.info("User logged in") do
  { user_id: 123, ip: "192.168.1.1" }
end
```

## Concurrency and Threading

### Thread Basics

```ruby
# Create threads
threads = 3.times.map do |i|
  Thread.new(i) do |thread_num|
    puts "Thread #{thread_num} starting"
    sleep 1
    puts "Thread #{thread_num} done"
  end
end

# Wait for all threads
threads.each(&:join)

# Thread-local variables
Thread.current[:user_id] = 123
Thread.current[:user_id]  # => 123
```

### Thread Safety

```ruby
# ❌ Bad: Race condition
class Counter
  def initialize
    @count = 0
  end

  def increment
    @count += 1  # Not atomic!
  end
end

# ✅ Good: Thread-safe with mutex
class Counter
  def initialize
    @count = 0
    @mutex = Mutex.new
  end

  def increment
    @mutex.synchronize do
      @count += 1
    end
  end
end

# ✅ Better: Use Concurrent::AtomicFixnum
require 'concurrent'

counter = Concurrent::AtomicFixnum.new(0)
counter.increment
```

### Ractors for Parallelism (Ruby 3.0+)

```ruby
# True parallel execution
def parallel_map(array, &block)
  ractors = array.map do |item|
    Ractor.new(item, block) do |value, transform|
      transform.call(value)
    end
  end

  ractors.map(&:take)
end

# Usage
results = parallel_map([1, 2, 3, 4]) { |n| n * 2 }
# => [2, 4, 6, 8]
```

## Metaprogramming

### method_missing

```ruby
class DynamicAccessor
  def initialize(data)
    @data = data
  end

  def method_missing(method, *args)
    if @data.key?(method)
      @data[method]
    else
      super
    end
  end

  def respond_to_missing?(method, include_private = false)
    @data.key?(method) || super
  end
end

# Usage
obj = DynamicAccessor.new(name: "John", age: 30)
obj.name  # => "John"
obj.age   # => 30
```

### define_method

```ruby
class Model
  %w[name email age].each do |attr|
    define_method(attr) do
      instance_variable_get("@#{attr}")
    end

    define_method("#{attr}=") do |value|
      instance_variable_set("@#{attr}", value)
    end
  end
end

# Creates name, name=, email, email=, age, age= methods
```

### class_eval and instance_eval

```ruby
# class_eval: Evaluates in class context
String.class_eval do
  def shout
    upcase + "!"
  end
end

"hello".shout  # => "HELLO!"

# instance_eval: Evaluates in instance context
str = "hello"
str.instance_eval do
  def custom_method
    "Custom: #{self}"
  end
end

str.custom_method  # => "Custom: hello"
```

## Memory and Performance Profiling

### Benchmark Module

```ruby
require 'benchmark'

n = 1_000_000
Benchmark.bm(20) do |x|
  x.report("Array#each:") do
    arr = []
    n.times { |i| arr << i }
  end

  x.report("Array#map:") do
    (0...n).map { |i| i }
  end

  x.report("Array.new:") do
    Array.new(n) { |i| i }
  end
end
```

### Memory Profiler

```ruby
require 'memory_profiler'

report = MemoryProfiler.report do
  # Code to profile
  1000.times { "string" + "concatenation" }
end

report.pretty_print
```

### Ruby Profiler

```ruby
require 'ruby-prof'

result = RubyProf.profile do
  # Code to profile
  10_000.times { expensive_operation }
end

printer = RubyProf::FlatPrinter.new(result)
printer.print(STDOUT)
```

## Common Pitfalls and How to Avoid Them

### 1. Modifying Collections During Iteration

```ruby
# ❌ Bad: Modifies while iterating
array = [1, 2, 3, 4, 5]
array.each do |item|
  array.delete(item) if item.even?  # Unpredictable!
end

# ✅ Good: Use reject or delete_if
array.reject! { |item| item.even? }
# Or
array.delete_if { |item| item.even? }
```

### 2. Unintended Global Variable Modification

```ruby
# ❌ Bad: Global variable
$user_count = 0

# ✅ Good: Class or instance variable
class UserCounter
  @count = 0

  class << self
    attr_accessor :count
  end
end
```

### 3. String Concatenation in Loops

```ruby
# ❌ Bad: Creates many string objects
result = ""
1000.times { |i| result += "#{i} " }

# ✅ Good: Use array join
result = 1000.times.map { |i| "#{i} " }.join

# ✅ Better: Use string builder
result = String.new
1000.times { |i| result << "#{i} " }
```

### 4. Forgetting to Return Values

```ruby
# ❌ Bad: No explicit return
def calculate
  total = items.sum
  # Implicitly returns total, but unclear
end

# ✅ Good: Explicit return for clarity
def calculate
  total = items.sum
  return total
end

# ✅ Best: Last expression is return value
def calculate
  items.sum
end
```

## Framework-Specific Guidance

### Rails-Specific Best Practices

```ruby
# Use scopes for reusable queries
class User < ApplicationRecord
  scope :active, -> { where(active: true) }
  scope :recent, -> { where('created_at > ?', 1.week.ago) }
end

# Use concerns for shared behavior
module Timestampable
  extend ActiveSupport::Concern

  included do
    before_save :update_timestamp
  end

  def update_timestamp
    self.updated_at = Time.current
  end
end

# Use strong parameters
class UsersController < ApplicationController
  def create
    @user = User.new(user_params)
    # ...
  end

  private

  def user_params
    params.require(:user).permit(:name, :email, :age)
  end
end

# Eager loading to avoid N+1 queries
# ❌ Bad: N+1 query
users = User.all
users.each { |user| puts user.posts.count }

# ✅ Good: Eager load
users = User.includes(:posts).all
users.each { |user| puts user.posts.count }
```

## Quick Reference Commands

```bash
# Ruby version
ruby -v

# Run Ruby file
ruby script.rb

# Interactive Ruby (IRB)
irb

# Execute inline Ruby
ruby -e "puts 'Hello, World!'"

# Check syntax without executing
ruby -c script.rb

# Run with warnings
ruby -w script.rb

# Install gem
gem install gem_name

# List installed gems
gem list

# Update gems
gem update

# Bundle install (Rails)
bundle install

# Run tests
ruby test/my_test.rb
rake test
rspec spec/

# Ruby documentation
ri String#upcase
ri Array

# Generate documentation
rdoc
yard doc
```

## Resources and Further Learning

- **Official Ruby Documentation**: <https://docs.ruby-lang.org>
- **Ruby Style Guide**: <https://rubystyle.guide>
- **Ruby Weekly Newsletter**: <https://rubyweekly.com>
- **The Ruby Toolbox**: <https://www.ruby-toolbox.com>
- **RubyGems**: <https://rubygems.org>

## Summary

Ruby is designed for developer happiness and productivity. When writing Ruby code:

1. **Write readable code** - Code is read more than it's written
2. **Follow conventions** - Consistency helps teams collaborate
3. **Test thoroughly** - Tests give confidence in refactoring
4. **Handle errors explicitly** - Fail fast and provide context
5. **Optimize when necessary** - Profile before optimizing
6. **Embrace Ruby's features** - Use blocks, modules, and metaprogramming appropriately
7. **Stay current** - Ruby 3.x brings significant improvements

Remember: Ruby rewards simple, expressive code that clearly communicates intent.
