---
name: refactoring-catalog
description: Identifies code smells and applies refactoring techniques from Martin Fowler's catalog. Use when improving code structure, reducing complexity, or eliminating smells without changing behavior.
---

# Refactoring Catalog

Systematic techniques for improving code structure without changing its observable behavior. Based on Martin Fowler's Refactoring Catalog.

---

## Composing Methods

### Extract Function

**Smell**: Long method, code fragment that can be grouped  
**Action**: Turn the fragment into a method with a name explaining its purpose  
**Cookbook**: [extract-function.md](./cookbook/extract-function.md)

### Inline Function

**Smell**: Function body is as clear as its name  
**Action**: Replace calls with the function body and remove the function  
**Cookbook**: [inline-function.md](./cookbook/inline-function.md)

### Extract Variable

**Smell**: Complex expression that's hard to understand  
**Action**: Place the result in a temporary variable with a meaningful name  
**Cookbook**: [extract-variable.md](./cookbook/extract-variable.md)

### Inline Variable

**Smell**: Variable name doesn't communicate more than the expression  
**Action**: Replace references with the expression itself  
**Cookbook**: [inline-variable.md](./cookbook/inline-variable.md)

### Replace Temp with Query

**Smell**: Temporary variable holding the result of an expression  
**Action**: Extract the expression into a method and replace temp with query  
**Cookbook**: [replace-temp-with-query.md](./cookbook/replace-temp-with-query.md)

### Split Variable

**Smell**: Variable assigned more than once (not a loop variable)  
**Action**: Make a separate variable for each assignment  
**Cookbook**: [split-variable.md](./cookbook/split-variable.md)

---

## Moving Features

### Move Function

**Smell**: Function references elements from another context more than its own  
**Action**: Move it to the context it references most  
**Cookbook**: [move-function.md](./cookbook/move-function.md)

### Move Field

**Smell**: Field used more by another class than its own  
**Action**: Move it to the class that uses it most  
**Cookbook**: [move-field.md](./cookbook/move-field.md)

### Move Statements into Function

**Smell**: Same code executed around a function call  
**Action**: Move those statements into the function  
**Cookbook**: [move-statements-into-function.md](./cookbook/move-statements-into-function.md)

### Move Statements to Callers

**Smell**: Function with behavior that some callers don't need  
**Action**: Move the varying behavior to the callers  
**Cookbook**: [move-statements-to-callers.md](./cookbook/move-statements-to-callers.md)

### Replace Inline Code with Function Call

**Smell**: Inline code doing the same thing as an existing function  
**Action**: Replace with a call to the function  
**Cookbook**: [replace-inline-code-with-function-call.md](./cookbook/replace-inline-code-with-function-call.md)

### Slide Statements

**Smell**: Related code fragments not next to each other  
**Action**: Slide statements to be adjacent  
**Cookbook**: [slide-statements.md](./cookbook/slide-statements.md)

### Split Loop

**Smell**: Loop doing multiple things  
**Action**: Split into separate loops for each task  
**Cookbook**: [split-loop.md](./cookbook/split-loop.md)

### Split Phase

**Smell**: Code dealing with two different things  
**Action**: Split into separate phases with intermediate data structure  
**Cookbook**: [split-phase.md](./cookbook/split-phase.md)

---

## Organizing Data

### Replace Primitive with Object

**Smell**: Primitive used to represent a domain concept  
**Action**: Create a class with the primitive as its data  
**Cookbook**: [replace-primitive-with-object.md](./cookbook/replace-primitive-with-object.md)

### Change Value to Reference

**Smell**: Multiple copies of the same conceptual data  
**Action**: Replace copies with a single reference object  
**Cookbook**: [change-value-to-reference.md](./cookbook/change-value-to-reference.md)

### Change Reference to Value

**Smell**: Reference object that's hard to work with  
**Action**: Replace with a value object  
**Cookbook**: [change-reference-to-value.md](./cookbook/change-reference-to-value.md)

### Replace Magic Literal

**Smell**: Literal with special meaning that's not obvious  
**Action**: Replace with a named constant  
**Cookbook**: [replace-magic-literal.md](./cookbook/replace-magic-literal.md)

### Rename Variable

**Smell**: Variable name doesn't clearly communicate its purpose  
**Action**: Change the name to something more communicative  
**Cookbook**: [rename-variable.md](./cookbook/rename-variable.md)

### Rename Field

**Smell**: Field name doesn't clearly communicate its purpose  
**Action**: Change the name to something more communicative  
**Cookbook**: [rename-field.md](./cookbook/rename-field.md)

### Change Function Declaration

**Smell**: Function name/parameters don't clearly communicate purpose  
**Action**: Rename function and/or add/remove parameters  
**Cookbook**: [change-function-declaration.md](./cookbook/change-function-declaration.md)

### Encapsulate Variable

**Smell**: Public field accessed directly  
**Action**: Create getter/setter functions  
**Cookbook**: [encapsulate-variable.md](./cookbook/encapsulate-variable.md)

### Encapsulate Collection

**Smell**: Collection returned directly, allowing modification  
**Action**: Return a copy or read-only view  
**Cookbook**: [encapsulate-collection.md](./cookbook/encapsulate-collection.md)

### Encapsulate Record

**Smell**: Record/hash used for mutable data  
**Action**: Create a class with accessors  
**Cookbook**: [encapsulate-record.md](./cookbook/encapsulate-record.md)

---

## Simplifying Conditional Logic

### Decompose Conditional

**Smell**: Complex conditional (if-else) with complicated conditions  
**Action**: Extract condition and each branch into separate functions  
**Cookbook**: [decompose-conditional.md](./cookbook/decompose-conditional.md)

### Consolidate Conditional Expression

**Smell**: Multiple conditionals with the same result  
**Action**: Combine them into a single conditional  
**Cookbook**: [consolidate-conditional-expression.md](./cookbook/consolidate-conditional-expression.md)

### Replace Nested Conditional with Guard Clauses

**Smell**: Deeply nested if-else structure  
**Action**: Use guard clauses for special cases, return early  
**Cookbook**: [replace-nested-conditional-with-guard-clauses.md](./cookbook/replace-nested-conditional-with-guard-clauses.md)

### Replace Conditional with Polymorphism

**Smell**: Switch/if-else selecting behavior based on type  
**Action**: Create subclasses and override methods  
**Cookbook**: [replace-conditional-with-polymorphism.md](./cookbook/replace-conditional-with-polymorphism.md)

### Introduce Special Case

**Smell**: Many places check for a special value (often null)  
**Action**: Create a special case object encapsulating the behavior  
**Cookbook**: [introduce-special-case.md](./cookbook/introduce-special-case.md)

### Introduce Assertion

**Smell**: Code assumes something about program state  
**Action**: Make the assumption explicit with an assertion  
**Cookbook**: [introduce-assertion.md](./cookbook/introduce-assertion.md)

### Replace Control Flag with Break

**Smell**: Boolean variable controlling loop exit  
**Action**: Use break, continue, or return instead  
**Cookbook**: [replace-control-flag-with-break.md](./cookbook/replace-control-flag-with-break.md)

### Replace Exception with Precheck

**Smell**: Exception used for expected condition  
**Action**: Check the condition first  
**Cookbook**: [replace-exception-with-precheck.md](./cookbook/replace-exception-with-precheck.md)

---

## Refactoring APIs

### Separate Query from Modifier

**Smell**: Function that returns a value and has side effects  
**Action**: Create two functions: one for query, one for modifier  
**Cookbook**: [separate-query-from-modifier.md](./cookbook/separate-query-from-modifier.md)

### Parameterize Function

**Smell**: Multiple functions doing similar things with literals  
**Action**: Combine into one function with a parameter  
**Cookbook**: [parameterize-function.md](./cookbook/parameterize-function.md)

### Remove Flag Argument

**Smell**: Boolean argument that changes function behavior  
**Action**: Create separate functions for each case  
**Cookbook**: [remove-flag-argument.md](./cookbook/remove-flag-argument.md)

### Preserve Whole Object

**Smell**: Passing several values from one object to a function  
**Action**: Pass the whole object instead  
**Cookbook**: [preserve-whole-object.md](./cookbook/preserve-whole-object.md)

### Replace Parameter with Query

**Smell**: Parameter that can be derived from another parameter  
**Action**: Remove the parameter and let the function calculate it  
**Cookbook**: [replace-parameter-with-query.md](./cookbook/replace-parameter-with-query.md)

### Replace Query with Parameter

**Smell**: Function references a global or internal value directly  
**Action**: Pass the value as a parameter  
**Cookbook**: [replace-query-with-parameter.md](./cookbook/replace-query-with-parameter.md)

### Remove Setting Method

**Smell**: Field should be set at construction time only  
**Action**: Remove the setter and set in constructor  
**Cookbook**: [remove-setting-method.md](./cookbook/remove-setting-method.md)

### Replace Constructor with Factory Function

**Smell**: Constructor has limitations (name, return type)  
**Action**: Replace with a factory function  
**Cookbook**: [replace-constructor-with-factory-function.md](./cookbook/replace-constructor-with-factory-function.md)

### Replace Function with Command

**Smell**: Function needs to be undone, queued, or has complex state  
**Action**: Encapsulate the function in a command object  
**Cookbook**: [replace-function-with-command.md](./cookbook/replace-function-with-command.md)

### Replace Command with Function

**Smell**: Command object is too simple  
**Action**: Replace with a plain function  
**Cookbook**: [replace-command-with-function.md](./cookbook/replace-command-with-function.md)

### Return Modified Value

**Smell**: Function updates data but doesn't return it  
**Action**: Return the modified value  
**Cookbook**: [return-modified-value.md](./cookbook/return-modified-value.md)

### Replace Error Code with Exception

**Smell**: Function returns error code to indicate failure  
**Action**: Throw an exception instead  
**Cookbook**: [replace-error-code-with-exception.md](./cookbook/replace-error-code-with-exception.md)

### Introduce Parameter Object

**Smell**: Group of parameters that travel together  
**Action**: Replace them with an object  
**Cookbook**: [introduce-parameter-object.md](./cookbook/introduce-parameter-object.md)

---

## Dealing with Inheritance

### Pull Up Method

**Smell**: Identical methods in sibling classes  
**Action**: Move to the superclass  
**Cookbook**: [pull-up-method.md](./cookbook/pull-up-method.md)

### Pull Up Field

**Smell**: Identical field in sibling classes  
**Action**: Move to the superclass  
**Cookbook**: [pull-up-field.md](./cookbook/pull-up-field.md)

### Pull Up Constructor Body

**Smell**: Constructors in subclasses have common code  
**Action**: Move common code to superclass constructor  
**Cookbook**: [pull-up-constructor-body.md](./cookbook/pull-up-constructor-body.md)

### Push Down Method

**Smell**: Method only relevant to one subclass  
**Action**: Move it to that subclass  
**Cookbook**: [push-down-method.md](./cookbook/push-down-method.md)

### Push Down Field

**Smell**: Field only used by one subclass  
**Action**: Move it to that subclass  
**Cookbook**: [push-down-field.md](./cookbook/push-down-field.md)

### Replace Type Code with Subclasses

**Smell**: Field/parameter that indicates type with conditional behavior  
**Action**: Replace with subclasses  
**Cookbook**: [replace-type-code-with-subclasses.md](./cookbook/replace-type-code-with-subclasses.md)

### Remove Subclass

**Smell**: Subclass does too little to justify its existence  
**Action**: Replace with a field in the superclass  
**Cookbook**: [remove-subclass.md](./cookbook/remove-subclass.md)

### Extract Superclass

**Smell**: Multiple classes with similar features  
**Action**: Create a superclass with the common elements  
**Cookbook**: [extract-superclass.md](./cookbook/extract-superclass.md)

### Collapse Hierarchy

**Smell**: Subclass is no different from its superclass  
**Action**: Merge them together  
**Cookbook**: [collapse-hierarchy.md](./cookbook/collapse-hierarchy.md)

### Replace Subclass with Delegate

**Smell**: Inheritance used for a single axis of variation  
**Action**: Replace with a delegate field  
**Cookbook**: [replace-subclass-with-delegate.md](./cookbook/replace-subclass-with-delegate.md)

### Replace Superclass with Delegate

**Smell**: Subclass doesn't want all of superclass behavior  
**Action**: Replace inheritance with delegation  
**Cookbook**: [replace-superclass-with-delegate.md](./cookbook/replace-superclass-with-delegate.md)

### Extract Class

**Smell**: Class doing too much, has too many responsibilities  
**Action**: Split into two classes  
**Cookbook**: [extract-class.md](./cookbook/extract-class.md)

---

## Other Refactorings

### Inline Class

**Smell**: Class does too little to justify its existence  
**Action**: Move all features to another class  
**Cookbook**: [inline-class.md](./cookbook/inline-class.md)

### Hide Delegate

**Smell**: Client calls through one object to reach another  
**Action**: Create a delegating method  
**Cookbook**: [hide-delegate.md](./cookbook/hide-delegate.md)

### Remove Middle Man

**Smell**: Class has too many simple delegating methods  
**Action**: Let clients call the delegate directly  
**Cookbook**: [remove-middle-man.md](./cookbook/remove-middle-man.md)

### Substitute Algorithm

**Smell**: Algorithm can be replaced with a clearer one  
**Action**: Replace the body with the new algorithm  
**Cookbook**: [substitute-algorithm.md](./cookbook/substitute-algorithm.md)

### Combine Functions into Class

**Smell**: Group of functions operating on the same data  
**Action**: Form a class with the data and functions  
**Cookbook**: [combine-functions-into-class.md](./cookbook/combine-functions-into-class.md)

### Combine Functions into Transform

**Smell**: Reading data, computing derived values, passing around  
**Action**: Create a transform function that enriches the data  
**Cookbook**: [combine-functions-into-transform.md](./cookbook/combine-functions-into-transform.md)

### Replace Loop with Pipeline

**Smell**: Loop processing a collection  
**Action**: Replace with pipeline operations (map, filter, reduce)  
**Cookbook**: [replace-loop-with-pipeline.md](./cookbook/replace-loop-with-pipeline.md)

### Remove Dead Code

**Smell**: Code that's never executed  
**Action**: Delete it  
**Cookbook**: [remove-dead-code.md](./cookbook/remove-dead-code.md)

### Replace Derived Variable with Query

**Smell**: Variable calculated from other values and stored  
**Action**: Calculate it on demand  
**Cookbook**: [replace-derived-variable-with-query.md](./cookbook/replace-derived-variable-with-query.md)

---

## Quick Reference Table

| Category                 | Refactoring                                   | Primary Smell                |
| ------------------------ | --------------------------------------------- | ---------------------------- |
| Composing Methods        | Extract Function                              | Long method, code fragment   |
| Composing Methods        | Inline Function                               | Trivial function body        |
| Composing Methods        | Extract Variable                              | Complex expression           |
| Composing Methods        | Inline Variable                               | Unnecessary variable         |
| Composing Methods        | Replace Temp with Query                       | Temp holding expression      |
| Composing Methods        | Split Variable                                | Multiple assignments         |
| Moving Features          | Move Function                                 | Feature envy                 |
| Moving Features          | Move Field                                    | Field envy                   |
| Moving Features          | Move Statements into Function                 | Repeated code around call    |
| Moving Features          | Move Statements to Callers                    | Varying behavior in function |
| Moving Features          | Replace Inline Code with Function Call        | Duplicate logic              |
| Moving Features          | Slide Statements                              | Separated related code       |
| Moving Features          | Split Loop                                    | Loop doing multiple things   |
| Moving Features          | Split Phase                                   | Mixed concerns               |
| Organizing Data          | Replace Primitive with Object                 | Primitive obsession          |
| Organizing Data          | Change Value to Reference                     | Inconsistent data            |
| Organizing Data          | Change Reference to Value                     | Complex reference handling   |
| Organizing Data          | Replace Magic Literal                         | Mysterious numbers           |
| Organizing Data          | Rename Variable                               | Unclear naming               |
| Organizing Data          | Rename Field                                  | Unclear naming               |
| Organizing Data          | Change Function Declaration                   | Bad signature                |
| Organizing Data          | Encapsulate Variable                          | Public field                 |
| Organizing Data          | Encapsulate Collection                        | Exposed collection           |
| Organizing Data          | Encapsulate Record                            | Naked record                 |
| Simplifying Conditionals | Decompose Conditional                         | Complex conditional          |
| Simplifying Conditionals | Consolidate Conditional Expression            | Duplicate conditions         |
| Simplifying Conditionals | Replace Nested Conditional with Guard Clauses | Deep nesting                 |
| Simplifying Conditionals | Replace Conditional with Polymorphism         | Type-based switching         |
| Simplifying Conditionals | Introduce Special Case                        | Null checks                  |
| Simplifying Conditionals | Introduce Assertion                           | Hidden assumptions           |
| Simplifying Conditionals | Replace Control Flag with Break               | Control flag                 |
| Simplifying Conditionals | Replace Exception with Precheck               | Exception for expected case  |
| Refactoring APIs         | Separate Query from Modifier                  | Mixed query/command          |
| Refactoring APIs         | Parameterize Function                         | Similar functions            |
| Refactoring APIs         | Remove Flag Argument                          | Boolean argument             |
| Refactoring APIs         | Preserve Whole Object                         | Data clump                   |
| Refactoring APIs         | Replace Parameter with Query                  | Derivable parameter          |
| Refactoring APIs         | Replace Query with Parameter                  | Hidden dependency            |
| Refactoring APIs         | Remove Setting Method                         | Mutable after construction   |
| Refactoring APIs         | Replace Constructor with Factory Function     | Constructor limitations      |
| Refactoring APIs         | Replace Function with Command                 | Complex function             |
| Refactoring APIs         | Replace Command with Function                 | Over-engineered command      |
| Refactoring APIs         | Return Modified Value                         | Side effect only             |
| Refactoring APIs         | Replace Error Code with Exception             | Error code                   |
| Refactoring APIs         | Introduce Parameter Object                    | Data clump                   |
| Dealing with Inheritance | Pull Up Method                                | Duplicate methods            |
| Dealing with Inheritance | Pull Up Field                                 | Duplicate fields             |
| Dealing with Inheritance | Pull Up Constructor Body                      | Duplicate constructor code   |
| Dealing with Inheritance | Push Down Method                              | Unused in superclass         |
| Dealing with Inheritance | Push Down Field                               | Unused field                 |
| Dealing with Inheritance | Replace Type Code with Subclasses             | Type code                    |
| Dealing with Inheritance | Remove Subclass                               | Trivial subclass             |
| Dealing with Inheritance | Extract Superclass                            | Duplicate features           |
| Dealing with Inheritance | Collapse Hierarchy                            | Identical class levels       |
| Dealing with Inheritance | Replace Subclass with Delegate                | Single variation axis        |
| Dealing with Inheritance | Replace Superclass with Delegate              | Partial inheritance          |
| Dealing with Inheritance | Extract Class                                 | Large class                  |
| Other                    | Inline Class                                  | Lazy class                   |
| Other                    | Hide Delegate                                 | Law of Demeter violation     |
| Other                    | Remove Middle Man                             | Message chain wrapper        |
| Other                    | Substitute Algorithm                          | Inferior algorithm           |
| Other                    | Combine Functions into Class                  | Feature envy group           |
| Other                    | Combine Functions into Transform              | Derived data passing         |
| Other                    | Replace Loop with Pipeline                    | Loop collection processing   |
| Other                    | Remove Dead Code                              | Dead code                    |
| Other                    | Replace Derived Variable with Query           | Stored calculation           |

---

## Cookbook Index

All 66 refactoring techniques with detailed mechanics:

**Composing Methods (6)**: [Extract Function](./cookbook/extract-function.md) · [Inline Function](./cookbook/inline-function.md) · [Extract Variable](./cookbook/extract-variable.md) · [Inline Variable](./cookbook/inline-variable.md) · [Replace Temp with Query](./cookbook/replace-temp-with-query.md) · [Split Variable](./cookbook/split-variable.md)

**Moving Features (8)**: [Move Function](./cookbook/move-function.md) · [Move Field](./cookbook/move-field.md) · [Move Statements into Function](./cookbook/move-statements-into-function.md) · [Move Statements to Callers](./cookbook/move-statements-to-callers.md) · [Replace Inline Code with Function Call](./cookbook/replace-inline-code-with-function-call.md) · [Slide Statements](./cookbook/slide-statements.md) · [Split Loop](./cookbook/split-loop.md) · [Split Phase](./cookbook/split-phase.md)

**Organizing Data (10)**: [Replace Primitive with Object](./cookbook/replace-primitive-with-object.md) · [Change Value to Reference](./cookbook/change-value-to-reference.md) · [Change Reference to Value](./cookbook/change-reference-to-value.md) · [Replace Magic Literal](./cookbook/replace-magic-literal.md) · [Rename Variable](./cookbook/rename-variable.md) · [Rename Field](./cookbook/rename-field.md) · [Change Function Declaration](./cookbook/change-function-declaration.md) · [Encapsulate Variable](./cookbook/encapsulate-variable.md) · [Encapsulate Collection](./cookbook/encapsulate-collection.md) · [Encapsulate Record](./cookbook/encapsulate-record.md)

**Simplifying Conditional Logic (8)**: [Decompose Conditional](./cookbook/decompose-conditional.md) · [Consolidate Conditional Expression](./cookbook/consolidate-conditional-expression.md) · [Replace Nested Conditional with Guard Clauses](./cookbook/replace-nested-conditional-with-guard-clauses.md) · [Replace Conditional with Polymorphism](./cookbook/replace-conditional-with-polymorphism.md) · [Introduce Special Case](./cookbook/introduce-special-case.md) · [Introduce Assertion](./cookbook/introduce-assertion.md) · [Replace Control Flag with Break](./cookbook/replace-control-flag-with-break.md) · [Replace Exception with Precheck](./cookbook/replace-exception-with-precheck.md)

**Refactoring APIs (13)**: [Separate Query from Modifier](./cookbook/separate-query-from-modifier.md) · [Parameterize Function](./cookbook/parameterize-function.md) · [Remove Flag Argument](./cookbook/remove-flag-argument.md) · [Preserve Whole Object](./cookbook/preserve-whole-object.md) · [Replace Parameter with Query](./cookbook/replace-parameter-with-query.md) · [Replace Query with Parameter](./cookbook/replace-query-with-parameter.md) · [Remove Setting Method](./cookbook/remove-setting-method.md) · [Replace Constructor with Factory Function](./cookbook/replace-constructor-with-factory-function.md) · [Replace Function with Command](./cookbook/replace-function-with-command.md) · [Replace Command with Function](./cookbook/replace-command-with-function.md) · [Return Modified Value](./cookbook/return-modified-value.md) · [Replace Error Code with Exception](./cookbook/replace-error-code-with-exception.md) · [Introduce Parameter Object](./cookbook/introduce-parameter-object.md)

**Dealing with Inheritance (12)**: [Pull Up Method](./cookbook/pull-up-method.md) · [Pull Up Field](./cookbook/pull-up-field.md) · [Pull Up Constructor Body](./cookbook/pull-up-constructor-body.md) · [Push Down Method](./cookbook/push-down-method.md) · [Push Down Field](./cookbook/push-down-field.md) · [Replace Type Code with Subclasses](./cookbook/replace-type-code-with-subclasses.md) · [Remove Subclass](./cookbook/remove-subclass.md) · [Extract Superclass](./cookbook/extract-superclass.md) · [Collapse Hierarchy](./cookbook/collapse-hierarchy.md) · [Replace Subclass with Delegate](./cookbook/replace-subclass-with-delegate.md) · [Replace Superclass with Delegate](./cookbook/replace-superclass-with-delegate.md) · [Extract Class](./cookbook/extract-class.md)

**Other Refactorings (9)**: [Inline Class](./cookbook/inline-class.md) · [Hide Delegate](./cookbook/hide-delegate.md) · [Remove Middle Man](./cookbook/remove-middle-man.md) · [Substitute Algorithm](./cookbook/substitute-algorithm.md) · [Combine Functions into Class](./cookbook/combine-functions-into-class.md) · [Combine Functions into Transform](./cookbook/combine-functions-into-transform.md) · [Replace Loop with Pipeline](./cookbook/replace-loop-with-pipeline.md) · [Remove Dead Code](./cookbook/remove-dead-code.md) · [Replace Derived Variable with Query](./cookbook/replace-derived-variable-with-query.md)
