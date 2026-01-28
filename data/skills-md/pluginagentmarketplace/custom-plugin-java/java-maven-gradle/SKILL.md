---
name: java-maven-gradle
description: Master Maven and Gradle - build configuration, dependencies, plugins, CI/CD
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 05-java-build-tools
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  build_tool:
    type: string
    enum: [maven, gradle]
    description: Preferred build tool
  project_type:
    type: string
    enum: [single, multi_module, library]
    description: Project structure type
---

# Java Maven Gradle Skill

Master Java build tools for efficient project management and CI/CD integration.

## Overview

This skill covers Maven and Gradle configuration including dependency management, plugin setup, multi-module projects, and CI/CD pipeline integration. Follows 2024-2025 best practices for both tools.

## When to Use This Skill

Use when you need to:
- Set up Maven/Gradle projects
- Manage dependencies with BOMs
- Configure build plugins
- Optimize build performance
- Set up CI/CD pipelines

## Topics Covered

### Maven
- POM structure and inheritance
- Dependency management with BOMs
- Plugin configuration
- Profiles and properties
- Multi-module projects

### Gradle
- Kotlin DSL (build.gradle.kts)
- Dependency catalogs
- Task configuration
- Build cache optimization
- Composite builds

### CI/CD Integration
- GitHub Actions workflows
- Dependency caching
- Matrix builds
- Artifact publishing

## Quick Reference

### Maven POM
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>

    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>${java.version}</maven.compiler.source>
        <maven.compiler.target>${java.version}</maven.compiler.target>
        <spring-boot.version>3.2.1</spring-boot.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-enforcer-plugin</artifactId>
                <version>3.4.1</version>
            </plugin>
        </plugins>
    </build>
</project>
```

### Gradle Kotlin DSL
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

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
    maxParallelForks = Runtime.getRuntime().availableProcessors() / 2
}
```

### Version Catalog (libs.versions.toml)
```toml
[versions]
spring-boot = "3.2.1"
junit = "5.10.1"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
```

## CI/CD Templates

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'maven'  # or 'gradle'
      - run: ./mvnw -B verify
```

## Useful Commands

```bash
# Maven
mvn dependency:tree
mvn versions:display-dependency-updates
mvn help:effective-pom

# Gradle
gradle dependencies
gradle dependencyInsight --dependency log4j
gradle build --scan
```

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Dependency not found | Wrong version | Check Maven Central |
| Version conflict | Transitive deps | Use BOM or enforcer |
| Build OOM | Heap too small | Set MAVEN_OPTS |
| Slow builds | No caching | Enable build cache |

### Debug Checklist
```
□ Check effective POM/build
□ Analyze dependency tree
□ Verify repository order
□ Check plugin versions
□ Review build cache
```

## Usage

```
Skill("java-maven-gradle")
```

## Related Skills
- `java-maven` - Maven specific
- `java-gradle` - Gradle specific
