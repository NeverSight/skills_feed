---
name: testing-quality
description: pytest, data validation, Great Expectations, and quality assurance for data systems
sasmp_version: "1.3.0"
bonded_agent: 02-backend-developer
bond_type: SECONDARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 80
prerequisites: [python-programming]
unlocks: [cicd-pipelines, data-engineering]
---

# Testing & Data Quality

Production testing strategies with pytest, data validation, and quality frameworks.

## Quick Start

```python
import pytest
from unittest.mock import Mock, patch
import pandas as pd

# Fixtures for test data
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "amount": [100.0, 200.0, 300.0]
    })

@pytest.fixture
def mock_database():
    with patch("app.db.connection") as mock:
        mock.query.return_value = [{"id": 1, "value": 100}]
        yield mock

# Unit test with AAA pattern
class TestDataTransformer:

    def test_calculates_total_correctly(self, sample_dataframe):
        # Arrange
        transformer = DataTransformer()

        # Act
        result = transformer.calculate_total(sample_dataframe)

        # Assert
        assert result == 600.0

    def test_handles_empty_dataframe(self):
        # Arrange
        empty_df = pd.DataFrame()
        transformer = DataTransformer()

        # Act & Assert
        with pytest.raises(ValueError, match="Empty dataframe"):
            transformer.calculate_total(empty_df)

    @pytest.mark.parametrize("input_val,expected", [
        (100, 110),
        (0, 0),
        (-50, -55),
    ])
    def test_apply_tax(self, input_val, expected):
        result = apply_tax(input_val, rate=0.10)
        assert result == expected
```

## Core Concepts

### 1. Data Validation with Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class DataRecord(BaseModel):
    id: str = Field(..., min_length=1)
    amount: float = Field(..., ge=0)
    timestamp: datetime
    category: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v):
        if not v.startswith("REC-"):
            raise ValueError("ID must start with 'REC-'")
        return v

    @field_validator("amount")
    @classmethod
    def round_amount(cls, v):
        return round(v, 2)

# Validation
def process_records(raw_data: list[dict]) -> list[DataRecord]:
    valid_records = []
    for item in raw_data:
        try:
            record = DataRecord(**item)
            valid_records.append(record)
        except ValidationError as e:
            logger.warning(f"Invalid record: {e}")
    return valid_records
```

### 2. Great Expectations

```python
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

# Initialize context
context = gx.get_context()

# Create expectations
validator = context.sources.pandas_default.read_csv("data/orders.csv")

# Column expectations
validator.expect_column_to_exist("order_id")
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_unique("order_id")

# Value expectations
validator.expect_column_values_to_be_between("amount", min_value=0, max_value=10000)
validator.expect_column_values_to_be_in_set("status", ["pending", "completed", "cancelled"])

# Pattern matching
validator.expect_column_values_to_match_regex("email", r"^[\w\.-]+@[\w\.-]+\.\w+$")

# Run validation
results = validator.validate()

if not results.success:
    failed_expectations = [r for r in results.results if not r.success]
    raise DataQualityError(f"Validation failed: {failed_expectations}")
```

### 3. Integration Testing

```python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine

@pytest.fixture(scope="module")
def postgres_container():
    """Spin up real Postgres for integration tests."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture
def db_engine(postgres_container):
    """Create engine with test database."""
    engine = create_engine(postgres_container.get_connection_url())

    # Setup schema
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT)"))
        conn.commit()

    yield engine

    # Cleanup
    engine.dispose()

class TestDatabaseOperations:

    def test_insert_and_query(self, db_engine):
        # Arrange
        repo = UserRepository(db_engine)

        # Act
        repo.insert(User(name="Test User"))
        users = repo.get_all()

        # Assert
        assert len(users) == 1
        assert users[0].name == "Test User"

    def test_transaction_rollback(self, db_engine):
        repo = UserRepository(db_engine)

        with pytest.raises(IntegrityError):
            repo.insert(User(name=None))  # Violates constraint

        # Verify rollback
        assert repo.count() == 0
```

### 4. Mocking External Services

```python
from unittest.mock import Mock, patch, MagicMock
import responses

class TestAPIClient:

    @responses.activate
    def test_fetch_data_success(self):
        # Mock HTTP response
        responses.add(
            responses.GET,
            "https://api.example.com/data",
            json={"items": [{"id": 1}]},
            status=200
        )

        client = APIClient()
        result = client.fetch_data()

        assert len(result["items"]) == 1

    @responses.activate
    def test_handles_api_error(self):
        responses.add(
            responses.GET,
            "https://api.example.com/data",
            json={"error": "Server error"},
            status=500
        )

        client = APIClient()

        with pytest.raises(APIError):
            client.fetch_data()

    @patch("app.services.external_api")
    def test_with_mock_service(self, mock_api):
        mock_api.get_user.return_value = {"id": 1, "name": "Test"}

        result = process_user_data(user_id=1)

        mock_api.get_user.assert_called_once_with(1)
        assert result["name"] == "Test"
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **pytest** | Testing framework | 8.0+ |
| **Great Expectations** | Data validation | 0.18+ |
| **Pydantic** | Data validation | 2.5+ |
| **pytest-cov** | Code coverage | 4.1+ |
| **testcontainers** | Integration testing | 3.7+ |
| **responses** | HTTP mocking | 0.25+ |
| **hypothesis** | Property-based testing | 6.98+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Flaky Tests** | Random failures | Shared state, timing | Isolate tests, use fixtures |
| **Slow Tests** | Long test runs | No mocking, real I/O | Mock external services |
| **Low Coverage** | Uncovered code | Missing edge cases | Add parametrized tests |
| **Test Data Issues** | Inconsistent results | Hardcoded data | Use factories/fixtures |

## Best Practices

```python
# ✅ DO: Use fixtures for setup
@pytest.fixture
def client():
    return TestClient(app)

# ✅ DO: Test edge cases
@pytest.mark.parametrize("input_data", [None, [], {}, ""])
def test_handles_empty_input(input_data):
    assert process(input_data) == default_result

# ✅ DO: Name tests descriptively
def test_user_creation_fails_with_invalid_email():
    ...

# ✅ DO: Use marks for slow tests
@pytest.mark.slow
def test_full_pipeline():
    ...

# ❌ DON'T: Test implementation details
# ❌ DON'T: Share state between tests
# ❌ DON'T: Skip error path testing
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Great Expectations](https://greatexpectations.io/)
- [Testing Python Applications](https://testdriven.io/)

---

**Skill Certification Checklist:**
- [ ] Can write unit tests with pytest
- [ ] Can use fixtures and parametrization
- [ ] Can implement data validation
- [ ] Can write integration tests
- [ ] Can mock external dependencies
