---
name: writing-test-code
description: Guidelines for writing BDD-style test code using Ginkgo/Gomega framework in Go. Use when writing tests for Kubernetes operators, controllers, or Go services. Focuses on behavior-driven development with Given-When-Then patterns and table-driven tests.
---

# ROLE AND EXPERTISE

You are a senior Go software engineer specializing in Behavior-Driven Development (BDD) for Kubernetes operators. Your expertise includes Ginkgo/Gomega testing framework, controller-runtime envtest, and Go testing best practices. You guide development using behavior specifications, Given-When-Then patterns, and example-driven testing.

# CORE BDD PRINCIPLES

- **Behavior over implementation**: Focus on what the system does, not how it does it
- **Specification by Example**: Use concrete examples to clarify requirements
- **Ubiquitous language**: Use domain terminology shared by developers, testers, and business stakeholders
- **Outside-in development**: Start from user behavior and work inward to implementation
- **Living documentation**: Tests serve as executable specifications and documentation
- **Three Amigos collaboration**: Involve developers, testers, and business stakeholders in defining behavior

# GIVEN-WHEN-THEN PATTERN

Every scenario follows this structure:

- **Given** (Context): Establish the initial state and preconditions
- **When** (Action): Describe the user action or event that triggers behavior
- **Then** (Outcome): Verify the expected outcome or system response

**Key principles**:
- Each clause should be clear and atomic
- Use domain language, not technical jargon
- Focus on observable behavior and outcomes
- Avoid implementation details in Given-When-Then descriptions

## Examples

**Good - Behavior-focused**:
```
Scenario: User successfully logs in with valid credentials
  Given a user account exists with email "user@example.com" and password "secret123"
  When the user submits login credentials with email "user@example.com" and password "secret123"
  Then the user should be redirected to the dashboard
  And the user should see a welcome message with their name
```

**Bad - Implementation-focused**:
```
Test: testLoginMethod
  Given database has user record with id=1
  When POST request to /api/auth endpoint with JSON payload
  Then HTTP 200 status code returned
  And JWT token in response body
```

# SCENARIO WRITING GUIDELINES

## Structure scenarios for clarity

- **Title**: Use descriptive, behavior-focused names
  - Format: `[Actor] [Action] [Expected Outcome]`
  - Good: "Customer cancels order before shipment"
  - Bad: "testCancelOrder" or "test_cancel_order_method"

- **Context (Given)**: Set up only necessary preconditions
  - Be specific about relevant state
  - Avoid irrelevant details
  - Use background scenarios for common setup

- **Action (When)**: Describe one primary action
  - Focus on user intent, not UI mechanics
  - Good: "When the user cancels the order"
  - Bad: "When the user clicks the cancel button in the order details modal"

- **Outcome (Then)**: Verify observable results
  - Check business-relevant outcomes
  - Verify multiple aspects when needed using "And"
  - Good: "Then the order status should be 'cancelled' / And the customer should receive a cancellation confirmation email"
  - Bad: "Then the cancel_order() method returns true"

## Organize scenarios by features

Group related scenarios under feature files:

```gherkin
Feature: Order Cancellation
  As a customer
  I want to cancel my order before it ships
  So that I can avoid unwanted purchases

  Scenario: Cancel order within cancellation window
    Given I have placed an order 2 hours ago
    And the order has not been shipped
    When I cancel the order
    Then the order status should be "cancelled"
    And I should receive a full refund
    And I should receive a cancellation confirmation email

  Scenario: Attempt to cancel shipped order
    Given I have placed an order 5 days ago
    And the order has already been shipped
    When I attempt to cancel the order
    Then I should see an error message "Cannot cancel shipped orders"
    And the order status should remain "shipped"
```

# TEST NAMING CONVENTIONS

## For BDD-style tests

Use descriptive, sentence-like names that express behavior:

**Recommended patterns**:
- `should[Expected behavior]When[Condition]`
- `[Actor]Can[Action]When[Condition]`
- `[Action]Results in[Outcome]`

**Examples**:
- `shouldRefundFullAmountWhenOrderCancelledBeforeShipment`
- `customerCanViewOrderHistoryWhenLoggedIn`
- `submittingInvalidEmailResultsInValidationError`

**Avoid**:
- Technical method names: `testCancelOrder`, `test_refund_calculation`
- Generic names: `testCase1`, `scenario2`
- Implementation-focused: `testCancelOrderMethodReturnsTrue`

# BDD DEVELOPMENT WORKFLOW

## 1. Discovery phase (Three Amigos)

Collaborate with stakeholders to define behavior:
- **Developer**: Technical feasibility and implementation approach
- **Tester**: Edge cases, error scenarios, and validation criteria
- **Business/Product**: Business rules, user needs, and acceptance criteria

## 2. Formulation phase

Write scenarios using Given-When-Then:
- Start with happy path scenarios
- Add alternative paths and edge cases
- Use examples to clarify ambiguous requirements
- Review scenarios with stakeholders for validation

## 3. Automation phase

Implement scenario steps:
1. Write scenario in natural language (Given-When-Then)
2. Create step definitions that map to code
3. Implement the minimum code to make the scenario pass
4. Refactor for clarity and maintainability
5. Ensure scenario remains readable and focused on behavior

## 4. Evolution phase

Maintain living documentation:
- Update scenarios when behavior changes
- Remove obsolete scenarios
- Refactor step definitions for reusability
- Keep scenarios synchronized with actual system behavior

# CODE QUALITY STANDARDS

- **Readability first**: Tests should read like specifications
- **Single responsibility**: Each scenario tests one specific behavior
- **Arrange-Act-Assert**: Structure test code clearly (maps to Given-When-Then)
- **Avoid test interdependence**: Each scenario should be independently executable
- **Use descriptive assertions**: Assertion messages should clearly indicate what failed
- **Minimize test data**: Use only data relevant to the scenario
- **Encapsulate common setup**: Extract reusable setup into helper methods or background scenarios

# SEPARATION OF CHANGES

Follow Tidy First principles for clean commits:

- **Structural changes** (refactoring): Improve test organization without changing behavior
  - Extract common setup into helper methods
  - Rename tests for clarity
  - Reorganize test files
  - Refactor step definitions

- **Behavioral changes**: Add or modify scenarios
  - New scenarios for new features
  - Updated scenarios for changed behavior
  - Additional assertions for expanded verification

- **Never mix**: Keep structural and behavioral changes in separate commits
- **Validate**: Ensure structural changes don't alter test outcomes

# COMMIT DISCIPLINE

Only commit when:
1. **All scenarios pass**: Both new and existing scenarios are green
2. **No warnings**: Linter and compiler warnings are resolved
3. **Single logical unit**: Commit represents one complete behavior or refactoring
4. **Clear commit message**: Message indicates whether commit is structural or behavioral
   - Behavioral: "feat: add scenario for order cancellation refund"
   - Structural: "refactor: extract common authentication setup into helper"

Use small, frequent commits organized by behavior or refactoring.

# CODE QUALITY VERIFICATION

Before committing any test code, **ALWAYS** run the following command to ensure code quality:

```bash
make lint test
```

This command performs two critical checks:

1. **`make lint`**: Runs linters (golangci-lint, gofmt, etc.) to ensure:
   - Code follows project style guidelines
   - No formatting issues exist
   - No common code smells or anti-patterns
   - All imports are properly organized
   - No unused variables or imports

2. **`make test`**: Executes all test suites to verify:
   - All existing tests still pass (no regressions)
   - Newly written tests execute correctly
   - Test coverage meets project standards
   - No test flakiness or race conditions

## Verification Workflow

**Step 1: Write or modify test code**
```bash
# Your BDD test implementation here
```

**Step 2: Run verification**
```bash
make lint test
```

**Step 3: Fix any issues**
- If linter fails: Address formatting and style issues
- If tests fail: Debug and fix test logic or implementation

**Step 4: Re-verify**
```bash
make lint test  # Run again until all checks pass
```

**Step 5: Commit only when all checks pass**
```bash
git add .
git commit -m "test: add BDD scenarios for orphan cleanup behavior"
```

## Common Linter Issues and Fixes

**Issue: Formatting errors**
```bash
# Fix automatically
make fmt
# Or manually
gofmt -w .
```

**Issue: Import organization**
```bash
# Use goimports
goimports -w .
```

**Issue: Unused variables in tests**
```go
// Bad
result := someFunction()
// Good
_ = someFunction()  // Explicitly ignore if not needed
```

## Integration with Development Workflow

The verification step should be integrated into your BDD workflow:

1. Write Given-When-Then scenario
2. Implement test code
3. **Run `make lint test`** ✅
4. Fix any issues
5. **Run `make lint test`** again ✅
6. Commit when all checks pass
7. Repeat for next scenario

## Continuous Integration

These same checks run in CI/CD pipelines. Running `make lint test` locally ensures:
- Faster feedback loop (catch issues before push)
- Reduced CI build failures
- Cleaner git history without "fix lint" commits
- Better code review experience

## Never Skip Verification

**❌ DON'T:**
```bash
git commit -m "test: add scenarios" # Without running make lint test
```

**✅ DO:**
```bash
make lint test                      # Verify first
git commit -m "test: add scenarios" # Commit only if checks pass
```

**Why this matters:**
- Prevents broken tests from entering the codebase
- Maintains consistent code style across the project
- Catches subtle bugs early
- Respects the team's time by not breaking CI

# EXAMPLE WORKFLOW

When implementing a new feature:

1. **Collaborate on scenarios** with stakeholders (Three Amigos)
2. **Write first scenario** describing simplest happy path behavior
3. **Implement step definitions** that fail (red phase)
4. **Write minimum code** to make scenario pass (green phase)
5. **Refactor** for clarity while keeping scenario green
6. **Commit behavioral change** separately
7. **Make structural improvements** if needed (extract methods, rename, etc.)
8. **Run all scenarios** to ensure no regression
9. **Commit structural change** separately
10. **Add next scenario** for alternative path or edge case
11. **Repeat** until feature behavior is fully specified and implemented

# COMMON PATTERNS

## Scenario Outline for data-driven tests

```gherkin
Scenario Outline: Calculate shipping cost based on weight
  Given an order with weight of <weight> kg
  When the shipping cost is calculated
  Then the cost should be <cost> dollars

  Examples:
    | weight | cost |
    | 1      | 5    |
    | 5      | 10   |
    | 10     | 15   |
    | 20     | 25   |
```

## Background for common setup

```gherkin
Feature: Order Management

  Background:
    Given a customer is logged in
    And the customer has items in their cart

  Scenario: Place order with valid payment
    When the customer completes checkout with valid payment
    Then an order should be created
    And the customer should receive an order confirmation

  Scenario: Place order with invalid payment
    When the customer completes checkout with invalid payment
    Then no order should be created
    And the customer should see a payment error message
```

# TOOLS AND FRAMEWORKS

This project uses:
- **Ginkgo v2**: BDD testing framework for Go
- **Gomega**: Matcher/assertion library used with Ginkgo
- **envtest**: Kubernetes controller integration testing
- **go-sqlmock**: SQL database mocking
- **stretchr/testify**: Alternative assertion library for table-driven tests

# ANTI-PATTERNS TO AVOID

- **Testing implementation details**: Focus on observable behavior, not internal mechanics
- **Overly technical scenarios**: Use domain language accessible to all stakeholders
- **Scenario interdependence**: Each scenario must be independently executable
- **Too many scenarios**: Focus on key behaviors; avoid exhaustive permutation testing
- **Replicating unit tests**: BDD scenarios should test integrated behavior, not individual methods
- **Ignoring stakeholder collaboration**: BDD value comes from shared understanding

---

# GO-SPECIFIC GUIDELINES

## Project Context: Lynq Operator (Kubernetes Operator)

This project is a Kubernetes operator built with controller-runtime. Tests focus on:
- **Controller reconciliation behavior**: How controllers respond to CR changes
- **CRD lifecycle**: LynqHub, LynqForm, LynqNode creation, updates, deletion
- **Resource provisioning**: Kubernetes resources created by the operator
- **External integrations**: MySQL datasource synchronization
- **Status management**: Conditions, metrics, and resource tracking

## Ginkgo/Gomega BDD Framework

### Test Suite Structure

Every package with tests needs a suite setup:

```go
package controller

import (
    "testing"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"
)

func TestControllers(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Controller Suite")
}
```

### Ginkgo BDD Blocks

Use these building blocks to structure behavior scenarios:

- **`Describe`**: Group related behaviors (e.g., "LynqNode Controller")
- **`Context`**: Specify preconditions (e.g., "When reconciling a resource")
- **`It`**: Define specific behavior (e.g., "Should create all child resources")
- **`BeforeEach`**: Setup before each test
- **`AfterEach`**: Cleanup after each test
- **`By`**: Document test steps for readability

**Example structure**:

```go
var _ = Describe("LynqNode Controller", func() {
    Context("When reconciling a resource", func() {
        const resourceName = "test-lynqnode"

        ctx := context.Background()

        BeforeEach(func() {
            By("creating prerequisite LynqHub")
            hub := &lynqv1.LynqHub{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "test-hub",
                    Namespace: "default",
                },
                Spec: lynqv1.LynqHubSpec{
                    Source: lynqv1.DataSource{
                        Type:         lynqv1.SourceTypeMySQL,
                        SyncInterval: "30s",
                    },
                },
            }
            Expect(k8sClient.Create(ctx, hub)).To(Succeed())
        })

        It("Should successfully reconcile the resource", func() {
            By("creating the LynqNode CR")
            lynqNode := &lynqv1.LynqNode{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      resourceName,
                    Namespace: "default",
                },
                Spec: lynqv1.LynqNodeSpec{
                    HubID: "test-hub",
                },
            }
            Expect(k8sClient.Create(ctx, lynqNode)).To(Succeed())

            By("checking that the LynqNode becomes Ready")
            Eventually(func() bool {
                err := k8sClient.Get(ctx,
                    types.NamespacedName{Name: resourceName, Namespace: "default"},
                    lynqNode)
                if err != nil {
                    return false
                }
                return meta.IsStatusConditionTrue(lynqNode.Status.Conditions, "Ready")
            }, timeout, interval).Should(BeTrue())
        })

        AfterEach(func() {
            By("cleaning up test resources")
            // Cleanup code
        })
    })
})
```

### Gomega Matchers

Use Gomega matchers for expressive assertions:

**Basic matchers**:
- `Expect(value).To(Equal(expected))` - Exact equality
- `Expect(value).To(BeNil())` - Nil check
- `Expect(value).To(BeTrue())` / `BeFalse()` - Boolean checks
- `Expect(err).ToNot(HaveOccurred())` - No error check
- `Expect(err).To(MatchError("expected error"))` - Error matching

**Collection matchers**:
- `Expect(slice).To(HaveLen(3))` - Length check
- `Expect(slice).To(ContainElement(item))` - Element presence
- `Expect(slice).To(ConsistOf(item1, item2))` - Exact elements (order-independent)
- `Expect(slice).To(BeEmpty())` - Empty check

**Kubernetes-specific matchers**:
- `Expect(k8sClient.Get(ctx, key, obj)).To(Succeed())` - Object exists
- `Expect(errors.IsNotFound(err)).To(BeTrue())` - Object not found

**Asynchronous matchers**:
- `Eventually(func() {...}, timeout, interval).Should(...)` - Retry until success
- `Consistently(func() {...}, duration, interval).Should(...)` - Verify stability

**Example**:

```go
It("Should create Deployment with correct replicas", func() {
    deployment := &appsv1.Deployment{}
    Eventually(func() error {
        return k8sClient.Get(ctx,
            types.NamespacedName{Name: "test-deployment", Namespace: "default"},
            deployment)
    }, timeout, interval).Should(Succeed())

    Expect(deployment.Spec.Replicas).To(Equal(pointer.Int32(3)))
    Expect(deployment.Spec.Template.Spec.Containers).To(HaveLen(1))
    Expect(deployment.Status.ReadyReplicas).To(Equal(int32(3)))
})
```

## Table-Driven Tests (Standard Go Testing)

For unit tests with multiple test cases, use table-driven pattern:

```go
func TestDependencyGraph_AddResource(t *testing.T) {
    tests := []struct {
        name      string
        resources []lynqv1.TResource
        wantErr   bool
        errMsg    string
    }{
        {
            name: "add single resource",
            resources: []lynqv1.TResource{
                {ID: "resource1"},
            },
            wantErr: false,
        },
        {
            name: "add resource with empty ID",
            resources: []lynqv1.TResource{
                {ID: ""},
            },
            wantErr: true,
            errMsg:  "resource ID cannot be empty",
        },
        {
            name: "add duplicate resource ID",
            resources: []lynqv1.TResource{
                {ID: "resource1"},
                {ID: "resource1"},
            },
            wantErr: true,
            errMsg:  "duplicate resource ID",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            graph := NewDependencyGraph()

            var err error
            for _, res := range tt.resources {
                err = graph.AddResource(res)
                if err != nil {
                    break
                }
            }

            if tt.wantErr {
                if err == nil {
                    t.Errorf("expected error but got none")
                }
                if tt.errMsg != "" && !strings.Contains(err.Error(), tt.errMsg) {
                    t.Errorf("expected error containing %q, got %q", tt.errMsg, err.Error())
                }
            } else {
                if err != nil {
                    t.Errorf("unexpected error: %v", err)
                }
            }
        })
    }
}
```

**Table-driven test best practices**:
- Use descriptive `name` field for each test case
- Group related test cases together
- Use `t.Run()` for subtests to enable parallel execution
- Define expected behavior clearly in struct fields
- Test both happy path and error cases

## Kubernetes Controller Testing with envtest

### Setup envtest Suite

```go
var (
    cfg       *rest.Config
    k8sClient client.Client
    testEnv   *envtest.Environment
    ctx       context.Context
    cancel    context.CancelFunc
)

var _ = BeforeSuite(func() {
    ctx, cancel = context.WithCancel(context.TODO())

    By("bootstrapping test environment")
    testEnv = &envtest.Environment{
        CRDDirectoryPaths:     []string{filepath.Join("..", "..", "config", "crd", "bases")},
        ErrorIfCRDPathMissing: true,
    }

    var err error
    cfg, err = testEnv.Start()
    Expect(err).NotTo(HaveOccurred())
    Expect(cfg).NotTo(BeNil())

    err = lynqv1.AddToScheme(scheme.Scheme)
    Expect(err).NotTo(HaveOccurred())

    k8sClient, err = client.New(cfg, client.Options{Scheme: scheme.Scheme})
    Expect(err).NotTo(HaveOccurred())
    Expect(k8sClient).NotTo(BeNil())
})

var _ = AfterSuite(func() {
    cancel()
    By("tearing down the test environment")
    err := testEnv.Stop()
    Expect(err).NotTo(HaveOccurred())
})
```

### Controller Reconciliation Testing Pattern

```go
It("Should reconcile and create child resources", func() {
    By("creating the parent CR")
    parentCR := &lynqv1.LynqNode{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "test-node",
            Namespace: "default",
        },
        Spec: lynqv1.LynqNodeSpec{
            HubID: "test-hub",
            Deployments: []lynqv1.TDeployment{
                {
                    TResource: lynqv1.TResource{
                        ID:           "app-deployment",
                        NameTemplate: "{{ .uid }}-app",
                    },
                    Spec: runtime.RawExtension{
                        Raw: []byte(`{"replicas": 3}`),
                    },
                },
            },
        },
    }
    Expect(k8sClient.Create(ctx, parentCR)).To(Succeed())

    By("checking that child Deployment is created")
    deployment := &appsv1.Deployment{}
    Eventually(func() error {
        return k8sClient.Get(ctx,
            types.NamespacedName{Name: "test-node-app", Namespace: "default"},
            deployment)
    }, timeout, interval).Should(Succeed())

    By("verifying Deployment specifications")
    Expect(deployment.Spec.Replicas).To(Equal(pointer.Int32(3)))
    Expect(deployment.OwnerReferences).To(HaveLen(1))
    Expect(deployment.OwnerReferences[0].Name).To(Equal("test-node"))

    By("checking that parent CR status is updated")
    Eventually(func() int32 {
        err := k8sClient.Get(ctx,
            types.NamespacedName{Name: "test-node", Namespace: "default"},
            parentCR)
        if err != nil {
            return 0
        }
        return parentCR.Status.DesiredResources
    }, timeout, interval).Should(Equal(int32(1)))
})
```

### Testing Deletion and Finalizers

```go
It("Should handle deletion with finalizer cleanup", func() {
    By("creating resource with finalizer")
    resource := &lynqv1.LynqNode{
        ObjectMeta: metav1.ObjectMeta{
            Name:       "test-node",
            Namespace:  "default",
            Finalizers: []string{"lynqnode.operator.lynq.sh/finalizer"},
        },
        Spec: lynqv1.LynqNodeSpec{HubID: "test-hub"},
    }
    Expect(k8sClient.Create(ctx, resource)).To(Succeed())

    By("creating child resources")
    // Create child resources...

    By("deleting the parent resource")
    Expect(k8sClient.Delete(ctx, resource)).To(Succeed())

    By("verifying child resources are cleaned up")
    Eventually(func() bool {
        childResource := &appsv1.Deployment{}
        err := k8sClient.Get(ctx,
            types.NamespacedName{Name: "child", Namespace: "default"},
            childResource)
        return errors.IsNotFound(err)
    }, timeout, interval).Should(BeTrue())

    By("verifying parent resource is deleted after finalizer removal")
    Eventually(func() bool {
        err := k8sClient.Get(ctx,
            types.NamespacedName{Name: "test-node", Namespace: "default"},
            resource)
        return errors.IsNotFound(err)
    }, timeout, interval).Should(BeTrue())
})
```

## Testing External Integrations

### Mocking SQL Database

```go
import (
    "github.com/DATA-DOG/go-sqlmock"
)

func TestMySQLDataSource_FetchNodes(t *testing.T) {
    db, mock, err := sqlmock.New()
    if err != nil {
        t.Fatalf("failed to create mock: %v", err)
    }
    defer db.Close()

    rows := sqlmock.NewRows([]string{"id", "url", "isActive"}).
        AddRow("node1", "https://example.com", true).
        AddRow("node2", "https://test.com", true)

    mock.ExpectQuery("SELECT (.+) FROM nodes WHERE isActive = ?").
        WithArgs(true).
        WillReturnRows(rows)

    datasource := &MySQLDataSource{db: db}
    nodes, err := datasource.FetchNodes(context.Background())

    if err != nil {
        t.Errorf("unexpected error: %v", err)
    }
    if len(nodes) != 2 {
        t.Errorf("expected 2 nodes, got %d", len(nodes))
    }

    if err := mock.ExpectationsWereMet(); err != nil {
        t.Errorf("unfulfilled expectations: %v", err)
    }
}
```

## Test Organization

### File Naming Conventions

- `*_test.go`: Test files (must end with `_test.go`)
- `suite_test.go`: Ginkgo suite setup (one per package)
- `*_unit_test.go`: Pure unit tests (no Kubernetes API)
- `*_integration_test.go`: Integration tests with envtest
- `e2e_test.go`: End-to-end tests

### Test Categories

**Unit Tests** (fast, no external dependencies):
- Pure business logic
- Template rendering
- Dependency graph algorithms
- Validation functions

**Integration Tests** (with envtest):
- Controller reconciliation
- CRD lifecycle
- Resource creation/update/deletion
- Status management

**E2E Tests** (full cluster):
- Complete operator workflows
- External datasource integration
- Multi-controller coordination

## Go Testing Best Practices

### Test Naming

Use descriptive test names that express behavior:

**Ginkgo style**:
```go
It("Should create Deployment when LynqNode is created")
It("Should update status to Ready when all resources are ready")
It("Should clean up child resources when parent is deleted")
```

**Table-driven style**:
```go
{
    name: "create resource with valid spec",
    name: "reject resource with empty ID",
    name: "handle duplicate resource IDs",
}
```

### Assertion Style

**Preferred (Gomega)**:
```go
Expect(err).ToNot(HaveOccurred())
Expect(deployment.Status.ReadyReplicas).To(Equal(int32(3)))
```

**Alternative (testify)**:
```go
require.NoError(t, err)
assert.Equal(t, int32(3), deployment.Status.ReadyReplicas)
```

### Context and Timeouts

Always use context and reasonable timeouts:

```go
const (
    timeout  = 10 * time.Second
    interval = 250 * time.Millisecond
)

Eventually(func() bool {
    // Polling function
}, timeout, interval).Should(BeTrue())
```

### Cleanup and Isolation

Ensure test isolation:

```go
BeforeEach(func() {
    // Create fresh namespace for each test
    namespace := &corev1.Namespace{
        ObjectMeta: metav1.ObjectMeta{
            GenerateName: "test-",
        },
    }
    Expect(k8sClient.Create(ctx, namespace)).To(Succeed())
    testNamespace = namespace.Name
})

AfterEach(func() {
    // Clean up test namespace
    namespace := &corev1.Namespace{
        ObjectMeta: metav1.ObjectMeta{
            Name: testNamespace,
        },
    }
    Expect(k8sClient.Delete(ctx, namespace)).To(Succeed())
})
```

## Running Tests

### Run all tests

```bash
go test ./... -v
```

### Run specific package

```bash
go test ./internal/controller -v
```

### Run specific test

```bash
# Ginkgo style
go test ./internal/controller -v -ginkgo.focus="Should create Deployment"

# Table-driven style
go test ./internal/graph -v -run=TestDependencyGraph_AddResource
```

### Run with coverage

```bash
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out
```

### Skip long-running tests

```bash
go test ./... -short
```

```go
if testing.Short() {
    t.Skip("skipping integration test in short mode")
}
```

---

Follow these Go-specific guidelines to create clear, maintainable, behavior-focused tests that serve as living documentation of the Lynq Operator's behavior.
