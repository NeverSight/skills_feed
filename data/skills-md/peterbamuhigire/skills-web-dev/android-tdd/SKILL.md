---
name: android-tdd
description: "Android Test-Driven Development standards. Enforces Red-Green-Refactor cycle, test pyramid (70/20/10), layer-specific testing strategies, and CI integration. Use when building or reviewing Android apps with TDD methodology."
---

# Android Test-Driven Development (TDD)

## Overview

TDD is a development process where you write tests **before** feature code, following the **Red-Green-Refactor** cycle. Every feature starts with a failing test, gets minimal implementation, then is refined.

**Core Principle:** No production code without a failing test first.

**Icon Policy:** If UI code is generated as part of TDD, use custom PNG icons and maintain `PROJECT_ICONS.md` (see `android-custom-icons`).

**Report Table Policy:** If UI tests cover reports that can exceed 25 rows, the UI must use table layouts (see `android-report-tables`).

## Quick Reference

| Topic                   | Reference File                      | When to Use                                       |
| ----------------------- | ----------------------------------- | ------------------------------------------------- |
| **TDD Workflow**        | `references/tdd-workflow.md`        | Step-by-step Red-Green-Refactor with examples     |
| **Testing by Layer**    | `references/testing-by-layer.md`    | Unit, integration, persistence, network, UI tests |
| **Advanced Techniques** | `references/advanced-techniques.md` | Factories, behavior verification, LiveData/Flow   |
| **Tools & CI Setup**    | `references/tools-and-ci.md`        | Dependencies, CI pipelines, test configuration    |
| **Team Adoption**       | `references/team-adoption.md`       | Legacy code, team onboarding, troubleshooting     |

## The Red-Green-Refactor Cycle

```
1. RED    → Write a failing test for desired behavior
2. GREEN  → Write MINIMUM code to make it pass
3. REFACTOR → Clean up while keeping tests green
4. REPEAT → Next behavior
```

**Critical Rules:**

- Never skip the Red phase (verify the test actually fails)
- Never write more code than needed in Green phase
- Never refactor with failing tests
- Each cycle should take minutes, not hours

## Test Pyramid (70/20/10)

```
        /  UI  \        10% - Espresso, end-to-end flows
       /--------\
      / Integra- \      20% - ViewModel+Repository, Room, API
     /  tion      \
    /--------------\
   /   Unit Tests   \   70% - Pure Kotlin, fast, isolated
  /==================\
```

| Type            | Speed       | Scope                  | Location                  | Tools                     |
| --------------- | ----------- | ---------------------- | ------------------------- | ------------------------- |
| **Unit**        | <1ms each   | Single class/method    | `test/`                   | JUnit, Mockito            |
| **Integration** | ~100ms each | Component interactions | `test/` or `androidTest/` | JUnit, Robolectric        |
| **UI**          | ~1s each    | User flows             | `androidTest/`            | Espresso, Compose Testing |

## TDD Workflow for Android Features

### Step 1: Define the Requirement

Start with a clear user story or acceptance criteria:

> _As a user, I want to add items to my cart so I can purchase them later._

### Step 2: Write the Failing Test (Red)

```kotlin
@Test
fun addItemToCart_increasesCartCount() {
    val cart = ShoppingCart()
    cart.addItem(Product("Phone", 999.99))
    assertEquals(1, cart.itemCount)
}
```

Run it. It must fail (class doesn't exist yet).

### Step 3: Write Minimal Code (Green)

```kotlin
class ShoppingCart {
    private val items = mutableListOf<Product>()
    fun addItem(product: Product) { items.add(product) }
    val itemCount: Int get() = items.size
}
```

Run test. It passes. Stop writing code.

### Step 4: Add Next Test, Then Refactor

```kotlin
@Test
fun addMultipleItems_calculatesTotal() {
    val cart = ShoppingCart()
    cart.addItem(Product("Phone", 999.99))
    cart.addItem(Product("Case", 29.99))
    assertEquals(1029.98, cart.totalPrice, 0.01)
}
```

Implement `totalPrice`, then refactor both test and production code.

## Layer-Specific Testing Summary

### Unit Tests (Domain & ViewModel)

```kotlin
class ScoreTest {
    @Test
    fun increment_increasesCurrentScore() {
        val score = Score()
        score.increment()
        assertEquals(1, score.current)
    }
}
```

- Mock all dependencies with Mockito
- Test one behavior per test
- No Android framework dependencies

### Integration Tests (Repository + Database)

```kotlin
@RunWith(AndroidJUnit4::class)
class WishlistDaoTest {
    private lateinit var db: AppDatabase

    @Before
    fun setup() {
        db = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java
        ).build()
    }

    @After
    fun teardown() { db.close() }
}
```

### Network Tests (API Layer)

```kotlin
class ApiServiceTest {
    private val mockWebServer = MockWebServer()

    @Test
    fun fetchData_returnsExpectedResponse() {
        mockWebServer.enqueue(
            MockResponse().setBody("""{"id":1,"name":"Test"}""").setResponseCode(200)
        )
        val response = service.fetchData().execute()
        assertEquals("Test", response.body()?.name)
    }
}
```

### UI Tests (Espresso / Compose)

```kotlin
@Test
fun clickSaveButton_showsConfirmation() {
    onView(withId(R.id.saveButton)).perform(click())
    onView(withText("Saved!")).check(matches(isDisplayed()))
}
```

## Essential Test Dependencies

```groovy
dependencies {
    // Unit
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'org.mockito.kotlin:mockito-kotlin:5.2.1'
    testImplementation 'org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3'

    // Integration & UI
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    androidTestImplementation 'androidx.arch.core:core-testing:2.2.0'

    // Room & Network
    testImplementation 'androidx.room:room-testing:2.6.1'
    testImplementation 'com.squareup.okhttp3:mockwebserver:4.12.0'
}
```

## Test Naming Convention

Use descriptive names following: `methodUnderTest_condition_expectedResult`

```kotlin
fun addItem_emptyCart_cartHasOneItem()
fun calculateTotal_multipleItems_returnsSumOfPrices()
fun login_invalidCredentials_returnsError()
fun fetchUsers_networkError_showsErrorState()
```

## Patterns & Anti-Patterns

### DO

- Write tests first (always Red before Green)
- Keep tests small and focused (one assertion per concept)
- Use descriptive test names that document behavior
- Use test data factories for complex objects
- Test edge cases and error conditions
- Refactor tests alongside production code

### DON'T

- Test implementation details (test behavior, not internals)
- Write tests for generated code (Hilt, Room DAOs)
- Test third-party libraries (Retrofit, Gson)
- Chase 100% coverage at expense of test quality
- Write slow, flaky, or order-dependent tests
- Skip the Red phase (you won't catch false positives)

## Integration with Other Skills

```
feature-planning → Define specs & acceptance criteria
      ↓
android-tdd → Write tests first, then implement (THIS SKILL)
      ↓
android-development → Follow architecture & Kotlin standards
      ↓
ai-error-handling → Validate AI-generated implementations
      ↓
vibe-security-skill → Security review
```

**Key Integrations:**

- **android-development**: Follow MVVM + Clean Architecture for testable design
- **feature-planning**: Use acceptance criteria as test scenarios
- **ai-error-handling**: Validate AI output against test expectations
- **superpowers:test-driven-development**: General TDD workflow orchestration

## CI Pipeline

```yaml
name: Android TDD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Unit Tests
        run: ./gradlew test
      - name: Instrumented Tests
        run: ./gradlew connectedAndroidTest
      - name: Coverage Report
        run: ./gradlew jacocoTestReport
```

**CI Rules:**

- All tests must pass before merge
- Coverage reports generated on every PR
- Unit tests and instrumented tests run in parallel

## References

- **Google Testing Guide**: developer.android.com/training/testing
- **Mockito Kotlin**: github.com/mockito/mockito-kotlin
- **Espresso**: developer.android.com/training/testing/espresso
- **Architecture Samples**: github.com/android/architecture-samples
