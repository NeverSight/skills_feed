---
name: code-refactor
description: "代码重构与代码整洁知识体系 — 基于《代码整洁之道》(Clean Code) 与《重构: 改善既有代码设计 第二版》(Refactoring 2nd Edition) 提炼整合。涵盖 24 种代码坏味道、70+ 重构手法、SOLID 原则、代码质量规范、重构时机决策矩阵。Keywords: refactor, code smell, clean code, naming, function design, extract function, move function, encapsulate, simplify, guard clause, polymorphism, inheritance, SRP, DRY, DIP, OCP, TDD, unit test, error handling, null, exception, code review, 代码整洁, 重构, 命名, 函数, 注释, 格式, 错误处理, 测试, 类设计, 代码坏味道, 提炼函数, 搬移函数, 封装, 简化条件, 多态, 继承, 卫语句, 委托, 代码质量, 代码审查. Triggers on: refactor, code smell, clean code, extract, inline, move, encapsulate, simplify, naming, function, class, comment, error, test, SRP, DRY, polymorphism, delegate, guard clause, 提炼, 内联, 搬移, 封装, 简化, 命名规范, 函数设计, 坏味道, 重构建议, how to refactor, code quality, 代码质量, 代码整洁之道, 重构名录"
version: "1.0.0"
license: MIT
metadata:
  author: weibaohui
  tags: [refactoring, clean-code, code-quality, code-review, technical-debt, 重构, 代码整洁, 代码质量]
  docs-url: github.com/weibaohui/skills
---

# Code Refactoring Skill

Unified reference combining *Clean Code* (Robert C. Martin) and *Refactoring 2nd Edition* (Martin Fowler).

---

## PART 1: PRINCIPLES

### The Four Rules of Simple Design (Kent Beck)

1. **Runs all the tests** — Testable systems naturally push toward small, single-purpose classes and low coupling
2. **Contains no duplication** — Code, implementation, algorithm duplication. Even small duplication signals an unexpressed idea
3. **Expresses intent** — Good names, small functions/classes, standard nomenclature, well-written tests
4. **Minimizes classes and methods** — Keep small, but don't overdo it. Lowest priority

### SOLID Principles

| Principle | Rule | Refactoring Link |
|-----------|------|-----------------|
| **SRP** | One reason to change | Extract Class, Split Phase |
| **OCP** | Open for extension, closed for modification | Replace Conditional with Polymorphism |
| **LSP** | Subtypes must be substitutable | Replace Subclass with Delegate |
| **ISP** | Many specific interfaces over general one | Extract Superclass → Split Interface |
| **DIP** | Depend on abstractions | Extract Superclass, Introduce Parameter Object |

### Law of Demeter

A method should only call methods of: (a) itself, (b) objects it creates, (c) passed arguments, (d) instance variables. **"Talk to friends, not strangers."**

- **Train wrecks**: `a.b.c.d()` — avoid chaining method calls on returned objects
- Refactoring: Hide Delegate → tell the object to do something, don't ask for internals

### Command-Query Separation

Functions either do something OR answer something, never both. Refactoring: Separate Query from Modifier.

### Immutability

Prefer immutable data. When data must change: Split Variable, Replace Derived Variable with Query, Remove Setting Method.

### Abstraction

- **Objects**: Hide data behind abstractions, expose operations
- **Data structures**: Expose data, have no meaningful functions
- **Hybrids** (half object, half data): Worst of both worlds — avoid
- **DTOs**: Public vars, no functions — ok for DB/message parsing

---

## PART 2: CODE SMELLS (24 smells)

### Naming
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Mysterious Name** | Names don't convey purpose | Rename (Change Function Declaration, Rename Variable, Rename Field) |

### Duplication
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Duplicated Code** | Same code in multiple places | Extract Function → Move Function → Pull Up Method |
| **Data Clumps** | Same 3-4 fields always together | Extract Class, Introduce Parameter Object, Preserve Whole Object |

### Functions
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Long Function** | Functions too long | Extract Function; if many temp vars: Replace Temp with Query, Introduce Parameter Object; last resort: Replace Function with Command |
| **Long Parameter List** | Too many parameters | Replace Parameter with Query, Preserve Whole Object, Introduce Parameter Object, Remove Flag Argument |
| **Feature Envy** | Function uses more data from another module | Move Function (or Extract + Move) |
| **Loops** | Loops when pipelines would be clearer | Replace Loop with Pipeline |

### Data
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Global Data** | Data visible/modifiable from anywhere | Encapsulate Variable |
| **Mutable Data** | Data changes unexpectedly | Encapsulate Variable, Split Variable, Separate Query from Modifier, Remove Setting Method, Replace Derived Variable with Query |
| **Primitive Obsession** | Using primitives instead of small objects | Replace Primitive with Object, Replace Type Code with Subclasses + Replace Conditional with Polymorphism |

### Structure
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Divergent Change** | Module changed for different reasons | Split Phase, Move Function, Extract Class |
| **Shotgun Surgery** | One change requires edits in many places | Move Function, Move Field, Combine Functions into Class/Transform, Inline Function/Class |
| **Large Class** | Class doing too much | Extract Class, Extract Superclass |
| **Lazy Element** | Unnecessary program elements | Inline Function, Inline Class, Collapse Hierarchy |
| **Speculative Generality** | Unused features built "just in case" | Collapse Hierarchy, Inline Function/Class, Remove Dead Code |
| **Temporary Field** | Fields used only in special cases | Extract Class, Introduce Special Case |

### Coupling
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Message Chains** | `a.b.c.d` chain of calls | Hide Delegate |
| **Middle Man** | Class delegates too much | Remove Middle Man |
| **Insider Trading** | Excessive data exchange between modules | Move Function/Field, Hide Delegate, Replace Subclass/Superclass with Delegate |
| **Alternative Classes** | Similar classes with incompatible interfaces | Change Function Declaration, Move Function, Extract Superclass |

### Inheritance
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Repeated Switches** | Same switch logic in different places | Replace Conditional with Polymorphism |
| **Refused Bequest** | Subclass doesn't use inherited features | Push Down Method/Field, Replace Subclass/Superclass with Delegate |
| **Data Class** | Classes with only fields and getters/setters | Encapsulate Record, Move Function to bring behavior to data |

### Comments
| Smell | What It Is | Refactoring |
|-------|-----------|-------------|
| **Comments** | Comments explaining what code does | Extract Function, Change Function Declaration (better naming), Introduce Assertion |

---

## PART 3: REFACTORING TECHNIQUES

### Ch6: First Set

**Extract Function** — When code needs comments; create function named by purpose → copy code → handle scope vars → replace original → test.

**Inline Function** — Reverse of Extract. When body = name clarity. Replace call sites with body → delete → test.

**Extract Variable** — Complex expression hard to read. Declare const with expression result → replace expression → test.

**Inline Variable** — Reverse of Extract Variable. Name doesn't add clarity. Verify no side effects → make const → replace all uses → delete.

**Change Function Declaration** — Simple: update declaration + call sites. Migratory: extract new → inline old → rename. Published: deprecate, wait, remove.

**Encapsulate Variable** — Data accessed from many places. Create getter/setter → replace direct accesses → restrict visibility.

**Rename Variable** — Wide-scope: encapsulate first → rename internal. Constants: create new → migrate → delete old.

**Introduce Parameter Object** — Data items always travel together. Create class/record for group → add parameter → migrate callers → replace individual params.

**Combine Functions into Class** — Functions always operate on same data. Encapsulate record → Move functions into class.

**Combine Functions into Transform** — Same derived data in multiple places. Create transform function → deep-copy input → add derived fields → update callers.

**Split Phase** — Two concerns handled sequentially. Extract second phase → introduce intermediate data structure → migrate params.

### Ch7: Encapsulation

**Encapsulate Record** — Record structure used widely. Encapsulate variable → create class wrapping record → add getters/setters → replace record accesses.

**Encapsulate Collection** — Getter returns mutable collection. Add add/remove methods; return copies from getter.

**Replace Primitive with Object** — Simple type needs behaviors. Encapsulate variable → create simple value class → modify accessors → add business logic.

**Replace Temp with Query** — Temp var used once but computation could be shared. Extract variable assignment to query function → inline original variable.

**Extract Class** — Class has too many responsibilities. Create new class → establish connection → Move Field → Move Function → clean up.

**Inline Class** — Reverse of Extract Class. Create delegation methods on target → redirect callers → move all → delete source.

**Hide Delegate** — Client calls `a.b.method()`. Add delegation method on service object → redirect callers.

**Remove Middle Man** — Reverse of Hide Delegate. Add accessor for delegate → redirect callers → remove delegation methods.

**Substitute Algorithm** — Simpler algorithm available. Extract algorithm to function → prepare tests → write new → test.

### Ch8: Moving Features

**Move Function** — Function references more from target context. Check references → copy to target → adjust → make source delegate → optionally inline.

**Move Field** — Data used with another record. Ensure field encapsulated → create field + accessors on target → remove source field.

**Move Statements into Function** — Same code runs alongside a function call. If single caller: paste. Multiple: Extract Function → redirect → inline → rename.

**Move Statements to Callers** — Function boundary shifted. Cut and paste, or Extract Function → inline original → rename.

**Replace Inline Code with Function Call** — Code duplicates library function. Replace with function call; test.

**Slide Statements** — Related code separated. Check side effects → cut and paste → test.

**Split Loop** — Loop does two unrelated things. Duplicate loop → remove cross-concern code → Extract Function on each.

**Replace Loop with Pipeline** — Loop expressible as filter/map. Create pipeline variable → progressively replace with pipeline ops → delete loop.

**Remove Dead Code** — Code no longer referenced. Remove it; test; rely on version control.

### Ch9: Data

**Split Variable** — Variable serves multiple purposes. Rename at first assignment → create new const at second → update references. Exception: accumulators (i++, sum += x).

**Rename Field** — Wide-scope: Encapsulate Record first → rename internal. Small scope: direct rename.

**Replace Derived Variable with Query** — Variable can be computed from other data. Create calculation function → assert equality → switch readers to query → remove variable.

**Change Reference to Value** — Internal object should be immutable. Make object immutable → add value-based equals → override hashCode.

**Change Value to Reference** — Multiple copies need to stay consistent. Create repository → ensure constructor finds instance → modify constructor to use repository.

### Ch10: Conditionals

**Decompose Conditional** — Complex condition logic. Extract condition, then-branch, else-branch into named functions. Pattern: `if (summer()) return summerCharge(); else return regularCharge();`

**Consolidate Conditional Expression** — Multiple conditions lead to same result. Combine with `||` or `&&` → Extract Function with descriptive name.

**Replace Nested Conditional with Guard Clauses** — One branch is main logic; others are pre-checks. Convert outermost condition to early return → repeat → remove result variable.

**Replace Conditional with Polymorphism** — Multiple switch statements on same type code. Create class hierarchy → factory function → move type-specific logic to subclasses.

**Introduce Special Case** — Multiple places check for same special value. Extract check to function → create special case object with default behaviors → replace conditional with polymorphic calls.

**Introduce Assertion** — Code assumes a condition is always true. Add assert statement; should never change behavior.

### Ch11: API Refactoring

**Separate Query from Modifier** — Function returns value AND has side effects. Duplicate function as query → remove side effects → redirect callers → remove return from modifier.

**Parameterize Function** — Two functions differ only in literal values. Add parameter for varying value → update callers → merge similar functions.

**Remove Flag Argument** — Parameter is boolean/enum controlling behavior. Create explicit functions for each behavior → replace flag-based calls.

**Preserve Whole Object** — Multiple values extracted from one object and passed together. Create new function accepting whole object → redirect callers → inline old function.

**Replace Parameter with Query** — Parameter can be derived from another parameter or context. Extract parameter computation to query → replace parameter usage → remove parameter.

**Replace Query with Parameter** — Reverse of above. Remove dependency on global/unwanted element; restore referential transparency.

**Remove Setting Method** — Field should not change after construction. Move value to constructor parameter → redirect setter calls → inline setter → make field immutable.

**Replace Constructor with Factory Function** — Constructor limited (can't return subclass, fixed name). Create factory function calling constructor → redirect callers → narrow constructor visibility.

**Replace Function with Command** — Complex function needs decomposition beyond Extract Function. Create class → Move function → promote params to constructor fields → Extract Function on pieces.

**Replace Command with Function** — Reverse of above. Extract create+execute to function → inline all command methods → delete command class.

### Ch12: Inheritance

**Pull Up Method** — Identical methods in multiple subclasses. Verify identical → ensure features accessible from super → copy to super → remove from subclasses.

**Pull Up Field** — Same field duplicated in subclasses. Verify same usage → create in super (protected) → remove from subclasses.

**Pull Up Constructor Body** — Common initialization in subclass constructors. Ensure super has constructor → move common statements after super().

**Push Down Method** — Function in super only relevant to some subclasses. Copy to relevant subclasses → remove from super.

**Push Down Field** — Field only used by some subclasses. Declare in relevant subclasses → remove from super.

**Replace Type Code with Subclasses** — Type code with different behavior per value. Self-encapsulate type code → create subclass overriding type getter → Factory Function → repeat for each type → remove type code.

**Remove Subclass** — Subclass no longer needed. Encapsulate construction with factory → move type checks to super → add type field → delete subclass.

**Extract Superclass** — Two classes doing similar things. Create empty super → Pull Up Constructor Body → Pull Up Field → Pull Up Method.

**Collapse Hierarchy** — Subclass and super too similar. Choose which to keep → Pull Up/Push Down all elements → delete empty class.

**Replace Subclass with Delegate** — Inheritance misused; need dynamic type changes. Factory function → create delegate class → add delegate field → Move subclass methods to delegate → add dispatch logic → change factory → delete subclass.

**Replace Superclass with Delegate** — Superclass operations not all applicable. Create field referencing super → create forwarding methods → remove inheritance.

---

## PART 4: CODE QUALITY

### Naming Rules

- **Intention-revealing**: Name answers *why it exists*, *what it does*, *how it is used*. If name needs a comment → not good enough.
- **Avoid disinformation**: Don't use near-misses of established concepts.
- **Meaningful distinctions**: No arbitrary suffixes (`a1, a2`), noise words (`ProductInfo` vs `ProductData`).
- **Pronounceable**: `genymdhms` → `generationTimestamp`
- **Searchable**: Single-letter names and magic numbers are unsearchable. Name length ↔ scope size.
- **No encoding**: No Hungarian Notation (`m_` prefix, type prefixes).
- **No mental mapping**: Don't make readers translate names.
- **By type**: Class = noun phrase (never verb). Method = verb phrase. Pick one word per concept. Use solution domain names when available.
- **Anti-patterns**: Number-series naming, noise words, cute names, `l` and `O` as variable names.

### Function Design Rules

- **Small**: First rule: be small. Second rule: be smaller. Hardly ever >20 lines.
- **Do one thing**: Extract another function whose name is not a restatement of implementation → does more than one thing.
- **One abstraction level per function**: Follow **Stepdown Rule** — read like top-down narrative.
- **Arguments**: Ideal = 0 (niladic). Next = 1 (monadic). 2 is ok. Avoid 3+.
  - Flag arguments are ugly (boolean params splitting behavior)
  - Use argument objects when groups travel together
  - No output arguments — in OO, `this` is the output
- **No side effects**: `checkPassword` should not initialize sessions.
- **Command-Query Separation**: Either do something OR answer something, never both.
- **DRY**: Duplication is the root of all evil.
- **Prefer exceptions to returning error codes**: Avoids deep nesting.
- **Anti-patterns**: Long functions (100+ lines), flag arguments, output arguments, functions with side effects, deeply nested error code checking.

### Comments Rules

**Don't comment bad code — rewrite it.** Comments are a necessary evil — compensation for failure to express yourself in code.

**Good comments**: Legal, informative, intent (explaining *why*), clarification (translating obscure API params), warning, TODO, public API Javadocs.

**Bad comments**: Mumbling, redundant, misleading, mandated, journal (use version control), noise, position markers, closing brace comments, attributions, commented-out code, HTML comments, function headers on small functions.

### Formatting Rules

- **File size**: ~200 lines, max 500. Small files easier to understand.
- **Newspaper metaphor**: Top = high-level concepts. Details increase downward.
- **Vertical openness**: Blank lines separate distinct thoughts.
- **Vertical density**: Related code should be vertically dense.
- **Line length**: ~45 chars. No more than 100-120.
- **Indentation**: Essential for hierarchy. Don't collapse scopes to one line.

### Class Design Rules

- **Small**: Measured by *responsibilities*, not lines. Can't name it → too big.
- **SRP**: One and only one reason to change.
- **High cohesion**: Methods should use instance variables. When cohesion drops → split class.
- **Encapsulation**: Keep variables and utility functions private.
- **Organization**: Constants → static vars → instance vars → public functions → private utilities (Stepdown Rule).
- **OCP**: Open for extension, closed for modification.
- **DIP**: Depend on abstractions, not concrete details. Use interfaces and DI.
- **Anti-patterns**: "God classes", classes with multiple reasons to change, mixed responsibilities, hybrid objects.

### Error Handling Rules

- **Use exceptions rather than return codes**: Return codes clutter caller, easily forgotten.
- **Write try-catch-finally first**: Try blocks define scope like transactions.
- **Use unchecked exceptions**: Checked exceptions violate OCP.
- **Provide context with exceptions**: Each exception should contain enough info to determine source.
- **Define exception classes by caller's needs**: Wrap third-party APIs.
- **Don't return/null**: Creates cascading null checks. Return special case objects instead.
- **Don't pass null**: Forbid passing null. Use assertions or throw exceptions.
- **Special Case Pattern**: Create objects that handle special cases, so client code doesn't need exceptional behavior.
- **Anti-patterns**: Deep nesting of if-checks, checked exceptions cascading, returning null, passing null, scattered error handling.

### Boundary Rules

- **Don't pass Map (or other boundary interfaces) around your system**: Keep boundary interfaces inside classes.
- **Learning Tests**: Write tests that explore and verify your understanding of third-party APIs.
- **Design the interface you wish you had**: Create your own ideal interface, then use an ADAPTER to bridge.
- **Clean boundaries**: Minimize the places that reference third-party code. Depend on what you control.
- **Patterns**: ADAPTER pattern, Facade over third-party APIs.
- **Anti-patterns**: Passing collection types in public APIs, scattered references to third-party APIs.

### Testing Rules

**TDD Three Laws**: (1) Write failing test first, (2) Write minimum test to fail, (3) Write minimum code to pass.

**Core rules**: Test code is as important as production code. Tests enable change, flexibility, maintainability. Clean tests = readability.

**Patterns**: BUILD-OPERATE-CHECK. Domain-Specific Testing Language. One assert per test (guideline).

**F.I.R.S.T.**: Fast, Independent, Repeatable, Self-Validating, Timely.

**Self-testing code**: Ensure all tests are completely automated. Run tests after every small change. Characterization tests for legacy code.

**Anti-patterns**: Tests that depend on execution order, long test methods, tests that aren't self-validating, manual test execution.

### System Design Rules

- **Separate construction from use**: Move construction to `main` or dedicated modules. Use Factories for runtime object creation. **Dependency Injection**: Objects should not instantiate their own dependencies.
- **Scaling up incrementally**: Systems don't need to be "right the first time." Implement today's stories, refactor.
- **Cross-cutting concerns**: Use AOP for persistence, security, transactions.
- **Test-Drive architecture**: No Big Design Up Front (BDUF).
- **Domain-Specific Languages (DSLs)**: Minimize communication gap between domain concepts and code.
- **Anti-patterns**: Lazy initialization scattered throughout, heavyweight containers, over-engineered APIs, tight coupling.

### Concurrency Rules

- **SRP**: Keep concurrency code separate from other code.
- **Limit scope of data**: Use data encapsulation; severely limit access to shared data.
- **Use copies of data**: Avoid sharing by copying objects as read-only.
- **Threads as independent as possible**: Each thread processes one client request with unshared data.
- **Know your library**: Use concurrent collections, executor framework, nonblocking solutions.
- **Keep synchronized sections small**: Locks are expensive, minimize critical sections.
- **Shut-down code is hard**: Think about shut-down early.
- **Anti-patterns**: Embedding concurrency in business code, sharing mutable data without synchronization, large critical sections, ignoring spurious failures.

### Emergence Rules

- **Refactoring**: Write code, then refactor incrementally. Each few lines, ask "Did I degrade the design?"
- **TEMPLATE METHOD pattern**: Remove higher-level duplication by extracting invariant algorithm skeleton.
- **Reuse in the small leads to reuse in the large**: Extracting tiny commonalities can lead to recognizing SRP violations.
- **Expressiveness through care**: Choose better names, split large functions, take care of what you've created.
- **Anti-patterns**: Pointless dogmatism, creating too many tiny classes in the name of SRP, skipping the refactoring step.

---

## PART 5: WHEN TO REFACTOR

### Why Refactor

- **Improves software design**: Without refactoring, code accumulates technical debt.
- **Makes software easier to understand**: Refactoring helps people understand the code.
- **Helps find bugs**: By understanding the system, we can see where bugs are.
- **Helps programming speed**: Well-factored code allows us to go faster in the long run.

### When to Refactor

- **Preparatory Refactoring**: Make it easier to add a feature. First refactor to make the feature easy to add.
- **Comprehension Refactoring**: Understanding code before modifying. Refactor to make it clearer.
- **Litter-Pickup Refactoring**: Small cleanup. Do it — don't let it pile up.
- **Planned vs. Opportunistic**: Refactoring as part of planned work or as you go.
- **Code Review Refactoring**: Refactor as part of code review to incorporate feedback.

### When NOT to Refactor

- When existing code is a mess (sometimes easier to rewrite)
- When you're about to throw the code away
- When you're on a tight deadline

### Challenges

- Delaying new features, code ownership, branches, testing, legacy code, database refactoring.

### Performance

- Refactoring usually makes programs slower, but degradation is small and manageable.
- Profile first, then refactor. Clean code is easier to tune.

### YAGNI

Don't write code for the future. Write only what you need now. Refactor when the future arrives.

---

## QUICK DECISION MATRIX

| Problem | Clean Code Principle | Refactoring Technique |
|---------|---------------------|----------------------|
| Function too long | One thing, small, one abstraction level | Extract Function → Inline if over-used |
| Long parameter list | 0-2 args ideal | Introduce Parameter Object / Preserve Whole Object |
| Duplicate code | DRY | Extract Function → Move Function → Pull Up Method |
| Conditional logic | Guard Clauses | Decompose Conditional / Replace Nested with Guard |
| Switch statements | Polymorphism over switch | Replace Conditional with Polymorphism |
| Mutable data bugs | Immutability preferred | Split Variable / Replace Derived with Query |
| Class too big | SRP, high cohesion | Extract Class → Extract Superclass |
| Tight coupling | Depend on abstractions (DIP) | Hide Delegate / Extract Interface |
| Inheritance misuse | Composition over inheritance | Replace Subclass with Delegate |
| Side effects | Command-Query Separation | Separate Query from Modifier |
| Null returns/passes | Don't return/pass null | Introduce Special Case (Null Object) |
| Long functions | Stepdown Rule, narrative flow | Extract Variable → Slide Statements → Split Loop |
| Bad names | Intention-revealing, searchable | Rename Variable / Rename Field / Change Function Declaration |
| Boundary issues | Wrap third-party code | ADAPTER / Facade pattern |
