---
name: name
description: Suggests clear, descriptive names for functions and variables following consistent naming conventions. Use when naming new code constructs, renaming for clarity, or reviewing naming in code reviews.
---

# Naming Conventions

Act as a top-tier software engineer who knows how to give clear, descriptive names to functions and variables.

Suggest names for: $ARGUMENTS

Apply these naming rules and give your recommendation with reasoning:

## General

- Use active voice and clear, consistent naming.
- Functions should be verbs, e.g. increment(), filter().
- Boolean variables should read like yes/no questions, e.g. isActive, hasPermission.
- Prefer standalone verbs over noun.method, e.g. createUser() not User.create().
- Avoid noun-heavy and redundant names.
- Avoid "doSomething" style names.
- Lifecycle methods: prefer beforeX / afterX over willX / didX.
- Use strong negatives over weak ones: isEmpty(thing) not !isDefined(thing).
- Mixins and function decorators: with${Thing}, e.g. withUser, withAuth.
- Follow framework specific naming conventions (React PascalCase components, hooks prefixed with use, etc.).

## Facade Functions (only for *-model.ts files)

- Pattern: `<action><Entity><OptionalWith...><DataSource><OptionalBy...>()`
- Allowed actions: save | retrieve | update | delete
- Entity names: singular, PascalCase
- Use "With..." for included relations, "By..." for lookup keys
- DataSource: "ToDatabase" (create), "FromDatabase" (reads), "InDatabase" (updates)

## Factory Functions (only for *-factories files)

- Start with createPopulated for base/compound entities.
- Compound names enumerate included relations with With...And...

## Boolean Functions

- Variables in active voice: isActive, hasExpired, isDeactivated
- Standalone functions: prefix with get -> getIsActive(entity), getHasExpired(date)
