---
name: screaming-architecture
description: Follow the clean and maintainable code architecture pattern for project structure.
---

# Screaming Architecture

Clean and maintainable code architecture pattern for project structure.

## Purpose

Follow the clean and maintainable code architecture pattern for project structure.

## When to Use

Use when you need to create or modify project structure following the clean and maintainable code architecture pattern.

## Instructions

1. Create the project directory structure.

For example, a todo list microservice could have the following structure:
```
src/
  todo/
    application/
      add-todo.use-case.ts
      update-todo.use-case.ts
      get-todos.use-case.ts
    domain/
      todo.entity.ts
      todo.repository.ts   // interface
    infrastructure/
      todo.repository.impl.ts
    presentation/
      todo.controller.ts
    dto/
      add-todo.dto.ts
      update-todo.dto.ts
```
