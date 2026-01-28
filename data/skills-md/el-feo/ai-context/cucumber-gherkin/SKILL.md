---
name: cucumber-gherkin
description: Comprehensive BDD testing with Cucumber and Gherkin syntax. Use when writing feature files (.feature), step definitions, hooks, or implementing Behaviour-Driven Development. Covers Gherkin keywords (Feature, Scenario, Given/When/Then, Background, Scenario Outline, Rule), step definition patterns for Ruby/JavaScript/Java/Python, hooks (Before/After/BeforeAll/AfterAll), tags, data tables, doc strings, and best practices. Triggers on cucumber, gherkin, BDD, feature files, step definitions, acceptance testing, executable specifications.
---

# Cucumber & Gherkin Skill

BDD testing framework with plain-text executable specifications. Gherkin syntax with step definitions in Ruby, JavaScript, Java, or Python.

## Core Concepts

**Cucumber** reads executable specifications in plain text and validates software behavior. **Gherkin** is the structured grammar making plain text machine-readable.

```
┌────────────┐                 ┌──────────────┐                 ┌───────────┐
│   Steps    │                 │     Step     │                 │           │
│ in Gherkin ├──matched with──>│ Definitions  ├───manipulates──>│  System   │
└────────────┘                 └──────────────┘                 └───────────┘
```

## Gherkin Syntax Quick Reference

### Primary Keywords

```gherkin
Feature: Short description
  Optional multi-line description explaining the feature.
  
  Background:
    Given common setup steps for all scenarios
  
  Rule: Business rule grouping (Gherkin 6+)
    
    Scenario: Concrete example illustrating the rule
      Given an initial context (past tense, setup)
      When an action occurs (present tense, trigger)
      Then expected outcome (assertion)
      And additional step
      But negative assertion
    
    Scenario Outline: Parameterized scenario
      Given there are <start> items
      When I remove <remove> items
      Then I should have <remaining> items
      
      Examples:
        | start | remove | remaining |
        |    12 |      5 |         7 |
        |    20 |      5 |        15 |
```

### Step Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Given` | Setup/precondition | `Given I am logged in as "admin"` |
| `When` | Action/trigger | `When I click the submit button` |
| `Then` | Assertion/outcome | `Then I should see "Success"` |
| `And` | Continue previous type | `And I have 3 items in my cart` |
| `But` | Negative continuation | `But I should not see "Error"` |
| `*` | Bullet-style step | `* I have eggs` |

### Data Structures

**Data Tables** - tabular data:
```gherkin
Given the following users exist:
  | name   | email              | role  |
  | Alice  | alice@example.com  | admin |
  | Bob    | bob@example.com    | user  |
```

**Doc Strings** - multi-line text:
```gherkin
Given a blog post with content:
  """markdown
  # My Post Title
  
  This is the content of my blog post.
  """
```

### Tags

```gherkin
@smoke @critical
Feature: User authentication

  @wip
  Scenario: Login with valid credentials
    ...
  
  @slow @database
  Scenario: Bulk user import
    ...
```

Tag expressions: `@smoke and not @slow`, `@gui or @api`, `(@smoke or @critical) and not @wip`

## Step Definitions

Match Gherkin steps to code. Use Cucumber Expressions (preferred) or Regular Expressions.

### Ruby

```ruby
Given('I have {int} cucumbers in my belly') do |count|
  @belly = Belly.new
  @belly.eat(count)
end

When('I wait {int} hour(s)') do |hours|
  @belly.wait(hours)
end

Then('my belly should growl') do
  expect(@belly.growling?).to be true
end

# With data table
Given('the following users exist:') do |table|
  table.hashes.each do |row|
    User.create!(row)
  end
end
```

### JavaScript

```javascript
const { Given, When, Then } = require('@cucumber/cucumber');

Given('I have {int} cucumbers in my belly', function(count) {
  this.belly = new Belly();
  this.belly.eat(count);
});

When('I wait {int} hour(s)', async function(hours) {
  await this.belly.wait(hours);
});

Then('my belly should growl', function() {
  expect(this.belly.isGrowling()).toBe(true);
});

// With data table
Given('the following users exist:', async function(dataTable) {
  for (const row of dataTable.hashes()) {
    await User.create(row);
  }
});
```

### Java

```java
public class StepDefinitions {
    @Given("I have {int} cucumbers in my belly")
    public void iHaveCucumbersInMyBelly(int count) {
        belly = new Belly();
        belly.eat(count);
    }
    
    @When("I wait {int} hour(s)")
    public void iWaitHours(int hours) {
        belly.wait(hours);
    }
    
    @Then("my belly should growl")
    public void myBellyShouldGrowl() {
        assertTrue(belly.isGrowling());
    }
}
```

## Cucumber Expressions

Built-in parameter types: `{int}`, `{float}`, `{word}`, `{string}`, `{}` (anonymous)

Optional text: `cucumber(s)` matches "cucumber" or "cucumbers"
Alternative text: `color/colour` matches "color" or "colour"

## Hooks

### Scenario Hooks

```ruby
# Ruby
Before do |scenario|
  # runs before each scenario
end

After do |scenario|
  # runs after each scenario
  screenshot if scenario.failed?
end
```

```javascript
// JavaScript
const { Before, After } = require('@cucumber/cucumber');

Before(async function(scenario) {
  // runs before each scenario
});

After(async function(scenario) {
  // runs after each scenario
  if (scenario.result.status === 'FAILED') {
    await this.screenshot();
  }
});
```

### Conditional Hooks (with tags)

```ruby
Before('@database') do
  DatabaseCleaner.start
end

After('@database') do
  DatabaseCleaner.clean
end
```

```javascript
Before({ tags: '@browser and not @headless' }, async function() {
  this.browser = await launchBrowser();
});
```

### Global Hooks

```ruby
BeforeAll do
  # once before any scenario
end

AfterAll do
  # once after all scenarios
end
```

## Best Practices

### Declarative over Imperative

**Good (declarative):**
```gherkin
When "Bob" logs in
Then he sees his dashboard
```

**Avoid (imperative):**
```gherkin
When I visit "/login"
And I enter "bob" in "username"
And I enter "secret" in "password"
And I click "Login"
Then I should see "Dashboard"
```

### Focus on Behavior, Not Implementation

- Describe *what* the system does, not *how*
- Use domain language stakeholders understand
- Keep scenarios short (3-5 steps recommended)
- One behavior per scenario

### Background Usage

- Keep backgrounds short (≤4 lines)
- Use only for essential shared context
- Move implementation details to step definitions

## Running Cucumber

```bash
# Ruby
bundle exec cucumber
cucumber --tags "@smoke and not @wip"
cucumber features/login.feature:10  # specific line

# JavaScript
npx cucumber-js
npx cucumber-js --tags "@smoke"

# Java (with Maven)
mvn test -Dcucumber.filter.tags="@smoke"
```

## Additional References

For comprehensive details, see reference files:

- `references/gherkin-syntax.md` - Complete Gherkin language reference
- `references/step-definitions.md` - Step definition patterns by language
- `references/hooks-config.md` - Hooks, configuration, and runners
- `references/best-practices.md` - Anti-patterns and advanced patterns
