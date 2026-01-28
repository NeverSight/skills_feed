---
name: design-patterns-ruby
description: Comprehensive Ruby implementations of Gang of Four (GoF) design patterns. Use when implementing object-oriented design solutions, refactoring to reduce coupling, solving architecture problems, or when user mentions specific patterns (Factory, Singleton, Observer, Strategy, etc.) in Ruby context.
---

<objective>
Provide Ruby implementations and guidance for all 23 GoF design patterns. Help agents identify which pattern solves a given problem and implement it idiomatically in Ruby.
</objective>

<quick_start>
<pattern_selection>
**Object Creation Problems** → Creational Patterns

- Decouple creation from usage → Factory Method
- Families of related objects → Abstract Factory
- Complex objects with many params → Builder
- Clone without concrete class dependency → Prototype
- Single shared instance → Singleton

**Structural Problems** → Structural Patterns

- Incompatible interfaces → Adapter
- Multiple independent dimensions → Bridge
- Tree structures treated uniformly → Composite
- Add behavior dynamically → Decorator
- Simplify complex subsystems → Facade
- Memory with many similar objects → Flyweight
- Access control/logging/caching → Proxy

**Behavioral Problems** → Behavioral Patterns

- Multiple handlers in sequence → Chain of Responsibility
- Decouple UI from business logic → Command
- Traverse without exposing internals → Iterator
- Reduce chaotic dependencies → Mediator
- Undo/restore functionality → Memento
- Notify about state changes → Observer
- Behavior varies by state → State
- Switch algorithms at runtime → Strategy
- Algorithm skeleton with custom steps → Template Method
- Operations on complex structures → Visitor
</pattern_selection>

<ruby_abstract_method>
Ruby doesn't have built-in abstract methods. Use:

```ruby
def abstract_method
  raise NotImplementedError, "#{self.class} has not implemented method '#{__method__}'"
end
```

</ruby_abstract_method>
</quick_start>

<when_to_use>
Use this skill when encountering:

- "How do I create objects without specifying exact classes?" → Factory Method/Abstract Factory
- "Constructor has too many parameters" → Builder
- "Need to copy objects without knowing their concrete type" → Prototype
- "Ensure only one instance exists" → Singleton
- "Legacy class interface doesn't match what I need" → Adapter
- "Class explosion from combining multiple features" → Bridge
- "Work with tree/hierarchy uniformly" → Composite
- "Add features without modifying class" → Decorator
- "Simplify interaction with complex library" → Facade
- "Too many similar objects consuming memory" → Flyweight
- "Control access/add logging to object" → Proxy
- "Request goes through chain of handlers" → Chain of Responsibility
- "Need undo/redo or queue operations" → Command
- "Custom iteration over collection" → Iterator
- "Components too tightly coupled" → Mediator
- "Save and restore object state" → Memento
- "Notify multiple objects of changes" → Observer
- "Object behavior depends on state" → State
- "Swap algorithms at runtime" → Strategy
- "Subclasses customize algorithm steps" → Template Method
- "Add operations to class hierarchy" → Visitor
</when_to_use>

<pattern_quick_reference>
<creational>
**Factory Method** - Define interface for creation, let subclasses decide type

```ruby
class Creator
  def factory_method
    raise NotImplementedError
  end

  def operation
    product = factory_method
    "Working with #{product.operation}"
  end
end

class ConcreteCreator < Creator
  def factory_method
    ConcreteProduct.new
  end
end
```

File: `Ruby/src/factory_method/conceptual/main.rb`

**Singleton** (thread-safe)

```ruby
class Singleton
  @instance_mutex = Mutex.new
  private_class_method :new

  def self.instance
    return @instance if @instance
    @instance_mutex.synchronize { @instance ||= new }
    @instance
  end
end
```

File: `Ruby/src/singleton/conceptual/thread_safe/main.rb`

See [references/creational-patterns.md](references/creational-patterns.md) for Abstract Factory, Builder, Prototype.
</creational>

<structural>
**Decorator** - Wrap objects to add behavior dynamically
```ruby
class Decorator < Component
  def initialize(component)
    @component = component
  end

  def operation
    @component.operation
  end
end

class ConcreteDecorator < Decorator
  def operation
    "Decorated(#{@component.operation})"
  end
end

# Stack decorators

decorated = DecoratorB.new(DecoratorA.new(ConcreteComponent.new))

```
File: `Ruby/src/decorator/conceptual/main.rb`

**Adapter** - Convert interface to expected format
```ruby
class Adapter < Target
  def initialize(adaptee)
    @adaptee = adaptee
  end

  def request
    "Adapted: #{@adaptee.specific_request}"
  end
end
```

File: `Ruby/src/adapter/conceptual/main.rb`

See [references/structural-patterns.md](references/structural-patterns.md) for Bridge, Composite, Facade, Flyweight, Proxy.
</structural>

<behavioral>
**Strategy** - Swap algorithms at runtime
```ruby
class Context
  attr_writer :strategy

  def initialize(strategy)
    @strategy = strategy
  end

  def execute
    @strategy.do_algorithm(data)
  end
end

# Switch strategy at runtime

context = Context.new(StrategyA.new)
context.strategy = StrategyB.new

```
File: `Ruby/src/strategy/conceptual/main.rb`

**Observer** - Notify subscribers of state changes
```ruby
class Subject
  def initialize
    @observers = []
  end

  def attach(observer)
    @observers << observer
  end

  def detach(observer)
    @observers.delete(observer)
  end

  def notify
    @observers.each { |observer| observer.update(self) }
  end
end
```

File: `Ruby/src/observer/conceptual/main.rb`

**State** - Object behavior changes based on internal state

```ruby
class Context
  attr_accessor :state

  def transition_to(state)
    @state = state
    @state.context = self
  end

  def request
    @state.handle
  end
end
```

File: `Ruby/src/state/conceptual/main.rb`

See [references/behavioral-patterns.md](references/behavioral-patterns.md) for Chain of Responsibility, Command, Iterator, Mediator, Memento, Template Method, Visitor.
</behavioral>
</pattern_quick_reference>

<ruby_idioms>
<deep_copy>
For Prototype pattern, use Marshal for deep copying:

```ruby
Marshal.load(Marshal.dump(object))
```

</deep_copy>

<thread_safety>
For Singleton and shared resources, use Mutex:

```ruby
@mutex = Mutex.new
@mutex.synchronize { @instance ||= new }
```

</thread_safety>

<private_constructor>
For Singleton pattern:

```ruby
private_class_method :new
```

</private_constructor>

<accessors>
- `attr_reader :name` - read-only
- `attr_writer :name` - write-only
- `attr_accessor :name` - read/write
</accessors>

<type_docs>
Use YARD-style documentation:

```ruby
# @param [String] value
# @return [Boolean]
def method(value)
end
```

</type_docs>
</ruby_idioms>

<running_examples>

```bash
ruby Ruby/src/<pattern>/conceptual/main.rb

# Examples:
ruby Ruby/src/singleton/conceptual/thread_safe/main.rb
ruby Ruby/src/observer/conceptual/main.rb
ruby Ruby/src/strategy/conceptual/main.rb
ruby Ruby/src/decorator/conceptual/main.rb
```

Requires Ruby 3.2+.
</running_examples>

<detailed_references>

- [references/creational-patterns.md](references/creational-patterns.md) - Factory Method, Abstract Factory, Builder, Prototype, Singleton
- [references/structural-patterns.md](references/structural-patterns.md) - Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- [references/behavioral-patterns.md](references/behavioral-patterns.md) - Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor
</detailed_references>

<success_criteria>

- Pattern correctly solves the identified design problem
- Ruby idioms used appropriately (NotImplementedError, Marshal, Mutex)
- Code follows Ruby conventions (snake_case, attr_* accessors)
- Example runs without errors via `ruby Ruby/src/<pattern>/conceptual/main.rb`
</success_criteria>
