---
name: nullables
description: "Guide for implementing James Shore's Nullables pattern and A-Frame architecture for testing without mocks. Use when implementing or refactoring code to follow patterns of: (1) Separating logic, infrastructure, and application layers, (2) Creating testable infrastructure with create/createNull factory methods, (3) Writing narrow, sociable, state-based tests without mocks, (4) Implementing value objects, (5) Building infrastructure wrappers that use embedded stubs, or (6) Designing dependency injection through static factory methods."
---

# Nullables and A-Frame Architecture

## Overview

This skill guides implementation of James Shore's Nullables pattern and A-Frame architecture. This approach enables fast, reliable testing without mocks through:

- **A-Frame Architecture**: Separation of Logic, Infrastructure, and Application layers
- **Nullables Pattern**: Production code with an "off switch" for testing
- **Static Factory Methods**: `.create()` for production, `.createNull()` for tests
- **State-Based Testing**: Narrow, sociable tests that verify outputs instead of interactions

## When to Use This Pattern

Apply this pattern when:

- If the code uses a dependency injection framework (eg effect-ts) then use it to perform injections; also inform me where this happens as we might need to think about where the boundary lies between a 3rd party injection approach and the use of Nullables (`.create` / `.createNull`.
- Writing new code
- Refactoring existing code to eliminate mocks and improve test reliability
- Writing tests for code that uses nullable patterns such as classes that use static factory method `.create`.

## Core Principles

### 1. Three-Layer Architecture

Organize code into distinct layers:

- **Logic**: Pure business logic and value objects (no external dependencies)
- **Infrastructure**: Code interfacing with external systems (network, filesystem, databases)
- **Application**: High-level orchestration coordinating logic and infrastructure
  - application code is effectively infrastructure code because it contains instances of instrastructure that talk to the outside world

### 2. Dual Factory Methods

Every application and infrastructure class implements:

```javascript
class ServiceClass {
  static create(config) {
    // Production instance - calls .create() on dependencies
    const dependency = Dependency.create();
    return new ServiceClass(dependency);
  }

  static createNull(config = {}) {
    // Test instance - calls .createNull() on dependencies
    const dependency = Dependency.createNull();
    return new ServiceClass(dependency);
  }

  constructor(dependency) {
    // Constructor receives instantiated dependencies
  }
}
```

### 3. Testing Without Mocks

- **Unit tests**: Use `.createNull()` - fast, sociable, no external calls to the outside world
- **Integration tests**: Use `.create()` sparingly - verify live infrastructure
- Configure responses via factory: `Service.createNull({ response: data })`
- Track outputs: `service.trackSentEmails()`
- Verify state and outputs, not interaction patterns

### 4. Value Objects

- Immutable by default - represent data without behavior
- Mutable value objects allowed - use methods for in-memory transformations only
- Infrastructure operations (network, I/O) should take/return value objects, not be methods on them

## Nullable algorithm for writing and testing code

Suppose `Foo` is the class under test.  We will use names like `Foo`, `foo`, `Bar`, `Client` etc for the purposes of describing this algorithm, but more descriptive names should be used in the code.

The use of static methods `Foo.create` and `Foo.createNull` for classes in the code is similar to a dependency injection approach with the addition of creating nulled instances via `Foo.createNull` for unit tests that pretend to talk to the outside world.  

- If `Foo` is application layer or infrastructure layer
  - `Foo` should be a class (the only exception might be logic code where a function might suffice, in which case call it `foo`)
  - most code should be classes except potentially for logic code
  - always use a static .create in order to instantiate: `Foo.create,` `Bar.create`
  - `Foo.create` should set valid production defaults as much as possible reducing the need to pass parameters to `Foo.create`
- If `Foo` is is logic layer code:
  - if it's stateless, pure functions should be fine so it would be `foo` not `Foo`
  - if it involves non-I/O non-network in-memory manipulation, a class may be suitable
  - use `Foo.create`
  - no need to create `Foo.createNull` since there should be no I/O or network operations
- If `Val` is a a value object (immutable or mutable)
  - `Val` should be a class
  - we should have a static `Val.create` but we don't need a `Val.createNull` so some of the procedures below may not apply; this is because value objects shouldn't be doing I/O operations so we don't need nulled versions
  - it may not make sense to set defaults for all parameters when creating value objects;  so `Val.create` may end up requiring the consumer to specify many or all parameters and should be typed accordingly
  - use a static `Val.createTestInstance` to create test values; this is to indicate that the value create is a test value; it's fine for `.createTestInstance` to set defaults to make tests less verbose

The following is the algorithm for refactoring and creating new code.  It doesn't need to be followed precisely, it is meant to convery the end result.

- Find the code (eg a class `Foo`) that you think is the most important to write or test
  - we want to be able to test `Foo` using narrow, sociable unit tests without mocks...
  - suppose `Bar` represents any another class that an instance of `Foo` needs to perform its actions
  - take class `Foo`
  - (1) ensure `Foo.create` calls `Bar.create` and passes the instance to `Foo`s constructor
  - (2) or: we pass in a factory `createBar` that returns an instance of `Bar` and let the instance of `Foo` create `Bar` at a later time
  - take note of calls to instances of `Bar` within `Foo's` instance code and refactor to inject them using either (1) or (2)
  - if you had to create `Bar.create`, repeat this process but with `Bar` in place of `Foo`
  - keep recursing as required
- Now repeat the above but for `Foo.createNull` (if applicable)
  - this means `Foo.createNull` will either (1) call `Bar.createNull` and pass to `Foo`s constructor (2) or it will pass `createBar` and this version of `createBar` will call `Bar.createNull`
  - the point of `.createNull` is to ensure any infrastructure code is "nulled" and returns a configured response rather than perform an I/O operation (network, disk etc)
- Code that directly makes I/O calls to access an external service or resource such as the network (eg `fetch`) or disk etc is infrastrucure layer code and should be wrapped up in a class with `.create` and `.createNull` making it into a client we can instantiate;
  - call this `Client` (here) but give it an appropriately descriptive class name  eg `HttpClient`, `DiskClient` etc
  - `Client` sole purpose is to interface with the outside world but have minimal business logic
  - we also call `Client` an "infrastructure wrapper"
  - `Client` should make an effort to provide data to the rest of the application in the form the application needs and no more
  - `Client.createNull` should instantiate a nulled version
  - `Client.createNull` mimics I/O calls (eg mimics calls to fetch)
    - by default it should return a default "happy-path" response
    - it should take parameters (use a param object) that can configure the responses ("configurable response parameters")
    - "configurable response parameters" should configure for possible responses or outcomes we might have to test for; as a human reading the tests I should be able to easily see at a glance what outcome is being configured for in the nulled object; let the implementation within `.createNull` worry about the details
  - in some situations an "embedded stub" might be appropriate that stubs out a built-in I/O or network operation; the embedded stub should be configued within `Client.createNull`.
  - if `Client` is not using a framework like effect-ts to manage errors, then use `neverthrow` and use an object with a `.type` field to discriminate the error at compile time; if there is an underlying error from a throw or a rejection, assign it to `.cause`
- value objects (instances of `Val`) are often returned by `Client`'s
- If `Foo` is infrastructure or application layer code and its methods contain I/O or network operations, replace these operations with a client and inject an instance of `Client` via `Foo.create` as per the above algorithm.
  - Where possible make `Foo.create` generate a default production-ready instance of `Client` without the need to specifying anything to `Foo.create`.
- If the code makes use of a 3rd party library to perform I/O eg tanstack-query / react-query / effect.runPromise etc, then...
  - determine if this library provides a test client and use it for the tests
  - think about how it should be incorporated into the `.create`/`.createNull` architecture and let me know
- Now go back to `Foo`
  - write narrow sociable unit tests against instances of `Foo` using `Foo.createNull`
- For insfrastructure wrapper code (`Client`),
  - we should test `Client.createNull`
  - in a separate folder designated for live integration tests we should also test `Client.create`
  - these shouldn't be too numerous, we're testing against a live service to test the actual non-nulled code and also that we get back the responses we expect
  - these live integration tests should be run in a separate command to the unit tests above
- If there are standalone functions that perform I/O or network operations (`foo`), favour re-writing `foo` as a class `Client` and treating it as a client / infrastructure wrapper and implement `.createNull` accordingly.
- Sometimes we want to know that changes to the outside world occurred in tests, maybe also in a certain order.
  - this allows us to keep tests state-based and outcome-focused rather than relying on mocks and testing internal interactions
  - Usually this happens in a `Client`
  - `Client` should implement an `EventEmitter` or a similar mechanism using `.emit` and `.on`/`.off`;  when some interaction with the outside world (`X`) occurs, it should emit an event for `X`
  - `Client` should additionally implement a `trackX` function where `X` represents the outcome we're tracking
  - `.trackX` should return a tracking object (let's call it `tracker` which is an instance of `Tracker`)
  - `Tracker` should have access to the event emitter in the instance of `Client`
  - `Tracker` can add itself as a listener for `X` using the event listener and log the events usually in sequential order
  - `tracker.stop()` should get `Tracker` to remove itself
  - `tracker.clear()` should clear the previously logged data
  - `tracker.data` should be a getter to access the data
  - in some cases, tracking may be useful to the application, in which this event emitter should be exposed publicly; we can still implement a `Tracker` using the above so tests can track the outcomes

End of algorithm.

### Implementing a New Feature

1. **Identify the layer**:
   - Pure computation? → Logic layer
   - External system interaction? → Infrastructure layer
   - Coordinating workflow? → Application layer

2. **Create the class with factory methods**:
   - Add `static create()` with reasonable defaults
   - Add `static createNull()` for infrastructure and application classes
   - Use constructor for dependency injection

3. **Implement dependencies through factories**:
   - `.create()` calls `.create()` on dependencies
   - `.createNull()` calls `.createNull()` on dependencies
   - Pass instantiated dependencies to constructor

4. **Write tests**:
   - Use `.createNull()` for unit tests
   - Configure responses via factory: `Service.createNull({ response: data })`
   - Track outputs: `service.trackOutput()`
   - Verify state and return values

5. **Add integration tests (sparingly)**:
   - Use `.create()` for a few narrow integration tests
   - Verify infrastructure wrappers correctly mimic third-party behavior

### Refactoring Existing Code

1. **Separate concerns**:
   - Extract logic into pure functions/classes
   - Wrap external dependencies in infrastructure classes
   - Create application layer to orchestrate

2. **Add factory methods**:
   - Replace direct instantiation with `.create()`
   - Add `.createNull()` to infrastructure and application classes
   - Update constructors to receive dependencies

3. **Replace mocks with nullables**:
   - Remove mock setup
   - Use `.createNull()` instances
   - Configure responses on nullable infrastructure

4. **Refactor tests to be state-based**:
   - Remove interaction assertions (verify/toHaveBeenCalled)
   - Add state and output assertions
   - Use event emitters for observable state changes

## Implementation Patterns

### Pattern: Infrastructure Wrapper

Wrap third-party code. Use an embedded stub that mimics the third-party library:

```javascript
class HttpClient {
  static create() {
    return new HttpClient(realHttp); // Real HTTP library
  }

  static createNull() {
    return new HttpClient(new StubbedHttp()); // Embedded stub
  }

  constructor(http) {
    this._http = http;
  }

  async request(options) {
    return await this._http.request(options);
  }
}

// Embedded stub - mimics third-party library interface
class StubbedHttp {
  async request(options) {
    return { status: 200, body: {} };
  }
}
```

### Pattern: Logic Sandwich

Application code: Read → Process → Write

```javascript
async transfer(fromId, toId, amount) {
  // Read from infrastructure
  const accounts = await this._repo.getAccounts(fromId, toId);

  // Process with logic
  const result = this._logic.transfer(accounts, amount);

  // Write through infrastructure
  await this._repo.saveAccounts(result);
}
```

### Pattern: Event Emitters for State

Expose state changes for testing:

```javascript
class Account extends EventEmitter {
  deposit(amount) {
    this._balance += amount;
    this.emit('balance-changed', { balance: this._balance });
  }
}

// Test by observing events
account.on('balance-changed', (event) => events.push(event));
```

## Detailed Reference

For comprehensive implementation details, see **[nullables-guide.md](references/nullables-guide.md)**:

- Complete A-Frame architecture details
- Nullables pattern implementation
- Value objects (immutable and mutable)
- Testing strategies and examples
- Infrastructure wrappers and embedded stubs
- Configurable responses and output tracking
- Event emitters for state-based tests
- Implementation checklist
