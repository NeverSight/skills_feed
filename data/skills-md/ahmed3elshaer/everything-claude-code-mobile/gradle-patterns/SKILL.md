---
name: gradle-patterns
description: Gradle build configuration patterns for Android including Version Catalogs, convention plugins, build optimization, and multi-module setup.
---

# Gradle Build Patterns

Modern Gradle configuration for Android.

## Version Catalog

```toml
# gradle/libs.versions.toml
[versions]
agp = "8.2.2"
kotlin = "1.9.22"
ksp = "1.9.22-1.0.17"
compose-compiler = "1.5.10"
compose-bom = "2024.02.00"
coroutines = "1.8.0"
koin = "3.5.3"
ktor = "2.3.8"

[libraries]
# Compose BOM
compose-bom = { module = "androidx.compose:compose-bom", version.ref = "compose-bom" }
compose-ui = { module = "androidx.compose.ui:ui" }
compose-material3 = { module = "androidx.compose.material3:material3" }
compose-ui-tooling = { module = "androidx.compose.ui:ui-tooling" }

# Koin
koin-android = { module = "io.insert-koin:koin-android", version.ref = "koin" }
koin-compose = { module = "io.insert-koin:koin-androidx-compose", version.ref = "koin" }

# Ktor Client
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-client-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-serialization-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }

# Testing
junit5 = { module = "org.junit.jupiter:junit-jupiter", version = "5.10.0" }
mockk = { module = "io.mockk:mockk", version = "1.13.8" }
turbine = { module = "app.cash.turbine:turbine", version = "1.0.0" }
coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }

[bundles]
compose = ["compose-ui", "compose-material3", "compose-ui-tooling"]
ktor = ["ktor-client-core", "ktor-client-okhttp", "ktor-client-content-negotiation", "ktor-serialization-json"]
testing = ["junit5", "mockk", "turbine", "coroutines-test"]

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
android-library = { id = "com.android.library", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
```

## Convention Plugins

```kotlin
// build-logic/convention/build.gradle.kts
plugins {
    `kotlin-dsl`
}

dependencies {
    compileOnly(libs.android.gradlePlugin)
    compileOnly(libs.kotlin.gradlePlugin)
}

// AndroidLibraryConventionPlugin.kt
class AndroidLibraryConventionPlugin : Plugin<Project> {
    override fun apply(target: Project) = with(target) {
        with(pluginManager) {
            apply("com.android.library")
            apply("org.jetbrains.kotlin.android")
        }
        
        extensions.configure<LibraryExtension> {
            compileSdk = 34
            defaultConfig.minSdk = 24
            
            compileOptions {
                sourceCompatibility = JavaVersion.VERSION_17
                targetCompatibility = JavaVersion.VERSION_17
            }
        }
    }
}
```

## Build Optimization

```properties
# gradle.properties
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.jvmargs=-Xmx4g -XX:+UseParallelGC

# Kotlin
kotlin.incremental=true
kotlin.caching.enabled=true

# Android
android.useAndroidX=true
android.nonTransitiveRClass=true
android.nonFinalResIds=true
```

## Multi-Module Setup

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

include(":app")
include(":core:common")
include(":core:ui")
include(":core:network")
include(":feature:home")
include(":feature:detail")
```

## Dependency Declarations

```kotlin
// Feature module build.gradle.kts
plugins {
    id("convention.android.library")
    id("convention.android.compose")
}

dependencies {
    implementation(project(":core:common"))
    implementation(project(":core:ui"))
    
    implementation(libs.bundles.compose)
    implementation(libs.koin.compose)
    
    testImplementation(libs.bundles.testing)
}
```

## Build Commands

```bash
# Full build with timing
./gradlew build --profile

# Specific module
./gradlew :feature:home:assembleDebug

# Dependency tree
./gradlew :app:dependencies --configuration releaseRuntimeClasspath

# Clear caches
./gradlew cleanBuildCache
rm -rf ~/.gradle/caches

# Build scan
./gradlew build --scan
```

---

**Remember**: Configure once, optimize daily.
