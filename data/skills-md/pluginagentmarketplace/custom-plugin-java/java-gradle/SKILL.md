---
name: java-gradle
description: Master Gradle - Kotlin DSL, task configuration, build optimization, caching
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 05-java-build-tools
bond_type: SECONDARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  dsl:
    type: string
    enum: [kotlin, groovy]
    default: kotlin
    description: Gradle DSL preference
---

# Java Gradle Skill

Master Gradle build tool with Kotlin DSL for Java projects.

## Overview

This skill covers Gradle configuration with Kotlin DSL including task configuration, dependency management with catalogs, build cache optimization, and CI/CD integration.

## When to Use This Skill

Use when you need to:
- Configure Gradle builds (Kotlin DSL)
- Manage dependencies with catalogs
- Optimize build performance
- Set up build cache
- Create custom tasks

## Quick Reference

```kotlin
// build.gradle.kts
plugins {
    java
    id("org.springframework.boot") version "3.2.1"
    id("io.spring.dependency-management") version "1.1.4"
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<JavaCompile> {
    options.compilerArgs.addAll(listOf("-parameters", "-Xlint:all"))
    options.isFork = true
    options.isIncremental = true
}

tasks.test {
    useJUnitPlatform()
    maxParallelForks = Runtime.getRuntime().availableProcessors() / 2
}
```

## Version Catalog

```toml
# gradle/libs.versions.toml
[versions]
spring-boot = "3.2.1"

[libraries]
spring-boot-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

## Useful Commands

```bash
gradle dependencies              # View dependencies
gradle dependencyInsight --dependency log4j  # Analyze dep
gradle build --scan              # Build scan
gradle build --build-cache       # Use cache
gradle wrapper --gradle-version 8.5  # Update wrapper
```

## Build Optimization

```kotlin
// settings.gradle.kts
enableFeaturePreview("STABLE_CONFIGURATION_CACHE")

// Enable parallel and caching
org.gradle.parallel=true
org.gradle.caching=true
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Slow builds | Enable --build-cache |
| Version conflict | Use platform() or constraints |
| Cache issues | gradle --refresh-dependencies |

## Usage

```
Skill("java-gradle")
```
