---
name: spring-ai-zhipuai
description: Configure ZhipuAI, apply Swagger, and run tests in Spring AI projects
---

# Spring AI ZhipuAI & Swagger Configuration Skill

This skill automates migrating Spring AI projects to ZhipuAI and configuring Swagger.

## Prerequisites

- Kotlin-based Spring Boot project
- Gradle (Kotlin DSL recommended)
- JDK 21 or higher
- ZhipuAI API Key (obtain from [ZhipuAI Platform](https://open.bigmodel.cn/))

## Steps

### 1. Install/Update Gradle Wrapper (Run First!)

> ⚠️ **Important**: This step must be executed first. The build will fail without Gradle Wrapper.

```bash
# Navigate to the folder containing the nearest gradle configuration file (build.gradle.kts or build.gradle)
cd path/to/project
gradle wrapper --gradle-version=8.12
```

**Verification:**

- Check if `gradle/wrapper/gradle-wrapper.jar` exists
- Verify `gradlew`, `gradlew.bat` scripts are executable

### 2. Modify build.gradle.kts

**JDK 21 Configuration:**

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

**Add Spring AI ZhipuAI Dependency:**

```kotlin
dependencies {
    // Spring AI ZhipuAI (replace existing Ollama/OpenAI dependency)
    implementation("org.springframework.ai:spring-ai-starter-model-zhipuai:1.1.2")

    // Swagger (SpringDoc OpenAPI) - Compatible with Spring Boot 3.3.x
    implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.5.0")
}
```

**Kotlin JVM Target Configuration:**

```kotlin
tasks.withType<KotlinCompile> {
    kotlinOptions {
        freeCompilerArgs = listOf("-Xjsr305=strict")
        jvmTarget = "21"
    }
}
```

### 3. Configure application.yml

```yaml
spring:
  ai:
    zhipuai:
      api-key: ${ZHIPUAI_API_KEY} # or enter directly
      chat:
        options:
          model: glm-4.7-flash # or glm-4-air, glm-4.5, glm-4.6
          temperature: 0.7

# SpringDoc OpenAPI (Swagger)
springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html
    tags-sorter: alpha
    operations-sorter: alpha
```

### 4. Add Swagger Annotations (with Testable Example Data)

> 💡 **Example Data Guidelines**: Reference `*.http` files if available. Otherwise, refer to Controller comments (e.g., `POST http://localhost:8080/api/xxx Body: {...}`) or generate appropriate example data based on API logic.

**Add @Schema to Model Classes (with example data):**

```kotlin
import io.swagger.v3.oas.annotations.media.Schema

@Schema(description = "AI 파싱 요청")
data class ParseRequest(
    @Schema(
        description = "AI에게 질문할 내용",
        example = "5가지 프로그래밍 언어를 나열해주세요",
        required = true
    )
    val question: String
)

@Schema(description = "카테고리 항목")
data class CategoryItem(
    @Schema(description = "카테고리 이름", example = "프로그래밍 언어")
    val name: String,
    @Schema(description = "항목 목록", example = "[\"Python\", \"Java\", \"JavaScript\"]")
    val items: List<String>
)
```

**Add @Tag, @Operation to Controllers:**

```kotlin
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag

@RestController
@RequestMapping("/api/example")
@Tag(name = "Example API", description = "예제 API 설명")
class ExampleController {

    @Operation(
        summary = "기능 요약",
        description = "상세 설명"
    )
    @PostMapping("/endpoint")
    fun example(@RequestBody request: ParseRequest): Map<String, Any> {
        // ...
    }
}
```

**Example Data Format Tips:**

| Field Type | Example Format                       |
| ---------- | ------------------------------------ |
| String     | `example = "text value"`             |
| Int/Long   | `example = "123"`                    |
| Boolean    | `example = "true"`                   |
| List       | `example = "[\"item1\", \"item2\"]"` |
| Object     | `example = "{\"key\": \"value\"}"`   |

### 5. Build and Test

```bash
# Build test
./gradlew clean build -x test

# Run unit tests
./gradlew test

# Run application
./gradlew bootRun
# Or pass API Key via environment variable
ZHIPUAI_API_KEY=your-api-key ./gradlew bootRun
```

### 6. Verification

- **Swagger UI**: http://localhost:8080/swagger-ui.html
- **API Docs (JSON)**: http://localhost:8080/api-docs

**Testing in Swagger UI:**

1. Access Swagger UI
2. Select API to test
3. Click "Try it out" button
4. Verify example data is auto-filled
5. Click "Execute" button to test

**HTTP Test:**

```bash
curl -X POST http://localhost:8080/api/client/list/parse \
  -H "Content-Type: application/json" \
  -d '{"question": "5가지 프로그래밍 언어를 나열해주세요"}'
```

## Version Compatibility

| Component         | Recommended Version |
| ----------------- | ------------------- |
| Spring Boot       | 3.3.x               |
| Spring AI         | 1.1.2               |
| SpringDoc OpenAPI | 2.5.0               |
| Gradle            | 8.12+               |
| JDK               | 21                  |

## ZhipuAI Model Options

| Model Name      | Description                    |
| --------------- | ------------------------------ |
| `glm-4.7-flash` | Fast response, general purpose |
| `glm-4-air`     | Lightweight model              |
| `glm-4.5`       | Standard performance           |
| `glm-4.6`       | Enhanced performance           |

## Troubleshooting

### Gradle Wrapper Missing (GradleWrapperMain ClassNotFoundException)

```bash
# Error: java.lang.ClassNotFoundException: org.gradle.wrapper.GradleWrapperMain
# Solution: Regenerate gradle wrapper
gradle wrapper --gradle-version=8.12
```

### Port Already in Use

```bash
lsof -ti:8080 | xargs kill -9
```

### SpringDoc Compatibility Error

- Use `springdoc-openapi-starter-webmvc-ui:2.5.0` for Spring Boot 3.3.x
- Version 2.8.x causes compatibility issues (LiteWebJarsResourceResolver ClassNotFoundException)
