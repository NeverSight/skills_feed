---
name: android-kotlin-compose
description: Create production-quality Android applications following Google's official Android architecture guidance with Kotlin, Jetpack Compose, MVVM architecture, Hilt dependency injection, Room database, and multi-module architecture. Triggers on requests to create Android projects, modules, screens, ViewModels, repositories, or when asked about Android architecture patterns and best practices.
---
# Android Kotlin Compose Development

Create production-quality Android applications following Google's official architecture guidance and best practices.
Use when building Android apps with Kotlin, Jetpack Compose, MVVM architecture, Hilt dependency injection, Room database, or Android multi-module projects.
Triggers on requests to create Android projects, screens, ViewModels, repositories, feature modules, or when asked about Android architecture patterns.


## Quick Reference

| Task                                                 | Reference File                                              |
|------------------------------------------------------|-------------------------------------------------------------|
| Project structure & modules                          | [modularization.md](references/modularization.md)           |
| Architecture layers (Presentation, Domain, Data, UI) | [architecture.md](references/architecture.md)               |
| Jetpack Compose patterns                             | [compose-patterns.md](references/compose-patterns.md)       |
| Kotlin best practices                                | [kotlin-patterns.md](references/kotlin-patterns.md)         |
| Coroutines best practices                            | [coroutines-patterns.md](references/coroutines-patterns.md) |
| Gradle & build configuration                         | [gradle-setup.md](references/gradle-setup.md)               |
| Testing approach                                     | [testing.md](references/testing.md)                         |
| Runtime permissions                                  | [android-permissions.md](references/android-permissions.md) |
| Kotlin delegation patterns                           | [kotlin-delegation.md](references/kotlin-delegation.md)     |
| Crash reporting                                      | [crashlytics.md](references/crashlytics.md)                 |
| StrictMode guardrails                                | [android-strictmode.md](references/android-strictmode.md)   |
| Multi-module dependencies                            | [dependencies.md](references/dependencies.md)               |
| Code quality (Detekt)                                | [code-quality.md](references/code-quality.md)               |
| Design patterns                                      | [design-patterns.md](references/design-patterns.md)         |
| Android performance benchmarking                     | [android-performance.md](references/android-performance.md) |

## Workflow Decision Tree

**Creating a new project?**
→ Start with `templates/settings.gradle.kts.template` for settings and module includes  
→ Start with `templates/libs.versions.toml.template` for the version catalog  
→ Read [modularization.md](references/modularization.md) for structure and module types  
→ Use [gradle-setup.md](references/gradle-setup.md) for build files and build logic  

**Configuring Gradle/build files?**
→ Use [gradle-setup.md](references/gradle-setup.md) for module `build.gradle.kts` patterns  
→ Keep convention plugins and build logic in `build-logic/` as described in [gradle-setup.md](references/gradle-setup.md)  

**Setting up code quality / Detekt?**
→ Use [code-quality.md](references/code-quality.md) for Detekt convention plugin setup  
→ Start from `templates/detekt.yml.template` for rules and enable Compose rules  

**Adding or updating dependencies?**
→ Follow [dependencies.md](references/dependencies.md)  
→ Update `templates/libs.versions.toml.template` if the dependency is missing  

**Adding a new feature/module?**
→ Follow module naming in [modularization.md](references/modularization.md)  
→ Implement Presentation in the feature module  
→ Follow dependency flow: Feature → Core/Domain → Core/Data

**Building UI screens/components?**
→ Read [compose-patterns.md](references/compose-patterns.md)
→ **Always** align Kotlin code with [kotlin-patterns.md](references/kotlin-patterns.md)  
→ Create Screen + ViewModel + UiState in the feature module  
→ Use shared components from `core/ui` when possible

**Writing any Kotlin code?**
→ **Always** follow [kotlin-patterns.md](references/kotlin-patterns.md)  
→ Ensure practices align with [architecture.md](references/architecture.md), [modularization.md](references/modularization.md), and [compose-patterns.md](references/compose-patterns.md)

**Setting up data/domain layers?**
→ Read [architecture.md](references/architecture.md)  
→ Create Repository interfaces in `core/domain`
→ Implement Repository in `core/data`
→ Create DataSource + DAO in `core/data`

**Setting up navigation?**
→ Follow Navigation Coordination in [modularization.md](references/modularization.md)  
→ Configure navigation graph in the app module  
→ Use feature navigation destinations and navigator interfaces  

**Adding tests?**
→ Use [testing.md](references/testing.md) for patterns and examples  
→ Keep test doubles in `core/testing`  

**Handling runtime permissions?**
→ Follow [android-permissions.md](references/android-permissions.md) for manifest declarations and Compose permission patterns  
→ Request permissions contextually and handle "Don't ask again" flows  

**Sharing logic across ViewModels or avoiding base classes?**
→ Use delegation via interfaces as described in [kotlin-delegation.md](references/kotlin-delegation.md)  
→ Prefer small, injected delegates for validation, analytics, or feature flags  

**Adding crash reporting / monitoring?**
→ Follow [crashlytics.md](references/crashlytics.md) for provider-agnostic interfaces and module placement  
→ Use DI bindings to swap between Firebase Crashlytics or Sentry  

**Enabling StrictMode guardrails?**
→ Follow [android-strictmode.md](references/android-strictmode.md) for app-level setup and Compose compiler diagnostics  
→ Use Sentry/Firebase init from [crashlytics.md](references/crashlytics.md) to ship StrictMode logs  

**Choosing design patterns for a new feature, business logic, or system?**
→ Use [design-patterns.md](references/design-patterns.md) for Android-focused pattern guidance  
→ Align with [architecture.md](references/architecture.md) and [modularization.md](references/modularization.md)  

**Measuring performance regressions or startup/jank?**
→ Use [android-performance.md](references/android-performance.md) for Macrobenchmark setup and commands  
→ Keep benchmark module aligned with `benchmark` build type in [gradle-setup.md](references/gradle-setup.md)  