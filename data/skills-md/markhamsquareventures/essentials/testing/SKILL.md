---
name: testing
description: How to effectively test the application, always use when writing tests
---

# Testing

## Instructions

- All tests must be written using Pest.
- Tests use Pest PHP with Laravel plugin. Feature tests extend `Tests\TestCase` with RefreshDatabase trait available (commented out in `tests/Pest.php` by default).
- Always start all work using TDD–write tests before writing any code.
- If you need to verify a feature is working, write or update a Unit / Feature test.
- You must not remove any tests or test files from the tests directory without approval. These are not temporary or helper files - these are core to the application.
- Tests should test all of the happy paths, failure paths, and weird paths.
- Tests live in the `tests/Feature` and `tests/Unit` directories.

### Running Tests

- Run the minimal number of tests using an appropriate filter before finalizing code edits.
- To run all tests: `php artisan test`.
- To run all tests in a file: `php artisan test tests/Feature/ExampleTest.php`.
- To filter on a particular test name: `php artisan test --filter=testName` (recommended after making a change to a related file).
- When the tests relating to your changes are passing, ask the user if they would like to run the entire test suite to ensure everything is still passing.
