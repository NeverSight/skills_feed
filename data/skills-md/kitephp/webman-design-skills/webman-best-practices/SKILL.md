---
name: webman-best-practices
description: MUST be used for Webman framework projects. Covers DDD architecture with controller/service/domain/infrastructure layers, strict dependency rules, lowercase directory naming, PER Coding Style with declare(strict_types=1) and final classes. Use when building Webman applications, implementing domain-driven design, or working with service layer patterns.
license: MIT
metadata:
  author: webman-design
  version: "1.0.0"
---

Webman framework best practices following DDD architecture, dependency rules, and PER Coding Style.

## Architecture & Dependencies

- Controller directly depends on Model, skipping Service layer → See [controller-skip-service](references/architecture/controller-skip-service.md)
- Domain layer depends on framework classes (Request, DB, etc.) → See [domain-framework-dependency](references/architecture/domain-framework-dependency.md)
- Service layer has circular dependencies with another Service → See [service-circular-dependency](references/architecture/service-circular-dependency.md)
- Infrastructure layer not implementing Contract interface → See [infrastructure-without-contract](references/architecture/infrastructure-without-contract.md)
- Using Model directly in Service instead of Repository → See [service-direct-model-access](references/architecture/service-direct-model-access.md)

## Naming Conventions

- Using camelCase or PascalCase for directories → See [directory-lowercase](references/naming/directory-lowercase.md)
- Interface without Interface suffix → See [interface-naming](references/naming/interface-naming.md)
- Service not following VerbNounService pattern → See [service-naming-pattern](references/naming/service-naming-pattern.md)
- Repository implementation without descriptive prefix → See [repository-implementation-naming](references/naming/repository-implementation-naming.md)
- Namespace not matching directory structure → See [namespace-directory-mismatch](references/naming/namespace-directory-mismatch.md)

## Code Style (PER Coding Style)

- Missing declare(strict_types=1) at file start → See [strict-types-declaration](references/code-style/strict-types-declaration.md)
- Not using final class by default → See [prefer-final-classes](references/code-style/prefer-final-classes.md)
- Not using readonly for immutable properties → See [readonly-properties](references/code-style/readonly-properties.md)
- Missing type declarations for parameters or return types → See [complete-type-declarations](references/code-style/complete-type-declarations.md)
- Not using constructor property promotion → See [constructor-property-promotion](references/code-style/constructor-property-promotion.md)

## Domain Patterns

- Entity without unique identity → See [entity-identity](references/domain/entity-identity.md)
- Value object that is mutable → See [value-object-immutability](references/domain/value-object-immutability.md)
- Business logic in Service instead of Domain → See [business-logic-in-domain](references/domain/business-logic-in-domain.md)
- Not using domain events for side effects → See [domain-events](references/domain/domain-events.md)
- Anemic domain model with only getters/setters → See [rich-domain-model](references/domain/rich-domain-model.md)

## Dependency Injection

- Using static methods instead of dependency injection → See [avoid-static-methods](references/architecture/avoid-static-methods.md)
- Not using constructor injection → See [constructor-injection](references/architecture/constructor-injection.md)
- Service locator pattern instead of dependency injection → See [no-service-locator](references/architecture/no-service-locator.md)
