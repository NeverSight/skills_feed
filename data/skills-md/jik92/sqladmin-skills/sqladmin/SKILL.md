---
name: sqladmin
description: Build and maintain SQLAdmin admin interfaces for SQLAlchemy models in FastAPI or Starlette apps. Use when you need to add an admin UI, configure ModelView behavior (lists, forms, filters, exports), add authentication/authorization or role-based permissions, customize templates, add custom views/actions, integrate file/image uploads, or set up async SQLAlchemy engines/sessions.
---

# SQLAdmin

## Overview
Use this skill to implement SQLAdmin in FastAPI/Starlette apps, wire SQLAlchemy engines/sessions (sync or async), and tailor the admin UI via ModelView configuration, authentication, templates, and extensions.

## Trigger examples
- “Add an admin dashboard for my SQLAlchemy models in FastAPI.”
- “Lock down the admin so only users with role=admin can access certain models.”
- “Make SQLAdmin work with an async engine and async sessionmaker.”
- “Customize list columns and add a custom action button.”
- “Override SQLAdmin templates for a custom layout.”

## Quick start
1) Create the SQLAlchemy engine (sync or async) and your models.
2) Initialize `Admin(app, engine)` (or pass a `session_maker`).
3) Define a `ModelView` for each model and `add_view` it.
4) Visit `/admin` (or your custom base URL).

See `references/quickstart.md` for a minimal setup pattern.

## Core tasks

### Configure ModelView behavior
- Lists, details, sorting, searching, filtering, pagination, and export options.
- Form scaffolding, overrides, and relationship field behaviors.
- Permissions and metadata (labels, icons, categories).

Use `references/configurations.md` for all ModelView options and examples.

### Add authentication and access control
- Add `AuthenticationBackend` to the `Admin` instance.
- Implement per-view visibility and access checks via `is_visible` / `is_accessible`.

Use `references/authentication.md` for the required methods and patterns.

### Role-based permissions
- Implement role checks in `is_accessible` and `is_visible`.
- Apply per-model restrictions and per-action guards.

Use `references/permissions.md` for role and policy patterns.

### Async SQLAlchemy integration
- Use `create_async_engine` and async `sessionmaker`.
- Ensure ModelView hooks handle async sessions correctly.

Use `references/async.md` for async engine/session patterns.

### Customize templates and add custom views
- Override built-in templates or point views to custom templates.
- Add custom pages with `BaseView` and `@expose`.

Use `references/templates-and-views.md` for template and custom view patterns.

### File and image fields
- Use `fastapi-storages` integrations for `FileType` / `ImageType` columns.

Use `references/files.md` for the storage-backed field setup.

### Admin initialization options
- Customize base URL, title, logo, favicon, middlewares, and template directory.

Use `references/admin-init.md` for the `Admin` constructor options.

## References
- `references/quickstart.md`
- `references/configurations.md`
- `references/authentication.md`
- `references/permissions.md`
- `references/async.md`
- `references/templates-and-views.md`
- `references/files.md`
- `references/admin-init.md`
