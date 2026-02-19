---
name: test-quality-inspector
description: "Test quality inspection framework for reviewing test coverage, identifying gaps, and ensuring comprehensive validation"
progressive_disclosure:
  entry_point:
    summary: "Test quality inspection framework for reviewing test coverage, identifying gaps, and ensuring comprehensive validation"
    when_to_use: "When writing tests, implementing test-quality-inspector, or ensuring code quality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - assertion-quality.md
    - inspection-checklist.md
    - red-flags.md
---
# Example Test Inspection Report

## Scenario: User Registration Feature

### Engineer's Test Suite

```python
# test_user_registration.py

def test_user_creation():
    """Test user creation"""
    user = create_user("test@example.com", "password123")
    assert user

def test_login():
    """Test login"""
    user = create_user("test@example.com", "password123")
    result = login("test@example.com", "password123")
    assert result

def test_duplicate_email():
    """Test duplicate email"""
    create_user("test@example.com", "password123")
    user2 = create_user("test@example.com", "password456")
    assert user2
```

---

## QA Inspection Report

### Test 1: test_user_creation()

**Claimed Intent:** Test user creation
**Actually Tests:** Object instantiation only

#### Issues Found

🔴 **CRITICAL: Worthless Assertion**
```python
assert user  # Line 5
```
- Would pass with corrupt data
- Would pass with wrong email
- Would pass with invalid password hash
- Would pass if database save failed

**Mental Debug:** User object with garbage data would pass this test.

🟠 **HIGH: Missing Validation Tests**
- No test for invalid email format
- No test for weak password
- No test for duplicate email (separate test exists but broken)
- No test for SQL injection in email

🟠 **HIGH: No Persistence Verification**
- Test doesn't verify user is saved to database
- Test doesn't verify user can be retrieved
- Transaction might be rolled back

🟡 **MEDIUM: Vague Test Name**
- "test_user_creation" doesn't describe what should happen
- Better: "test_user_creation_with_valid_data_persists_to_database"

#### Suggested Improvements

```python
def test_user_creation_with_valid_data_persists_to_database():
    """Creating a user with valid email and password should:
    1. Create user object with correct attributes
    2. Save to database
    3. Hash password (not store plaintext)
    4. Set default role and active status
    """
    email = "test@example.com"
    password = "SecurePass123!"

    user = create_user(email, password)

    # Verify user object
    assert user.id is not None, "User should have an ID after creation"
    assert user.email == email, "Email should match input"
    assert user.is_active is True, "New users should be active by default"
    assert user.role == "user", "New users should have 'user' role"
    assert user.created_at is not None, "Created timestamp should be set"

    # Verify password is hashed, not plaintext
    assert user.password_hash != password, "Password should be hashed"
    assert len(user.password_hash) > 50, "Password hash should be substantial"

    # Verify persistence
    retrieved_user = User.get_by_email(email)
    assert retrieved_user is not None, "User should be retrievable from database"
    assert retrieved_user.id == user.id, "Retrieved user should match created user"

def test_user_creation_with_invalid_email_format_raises_validation_error():
    """Creating a user with malformed email should raise ValidationError"""
    invalid_emails = [
        "not-an-email",
        "@example.com",
        "test@",
        "test space@example.com",
        "",
    ]

    for invalid_email in invalid_emails:
        with pytest.raises(ValidationError) as exc:
            create_user(invalid_email, "password123")

        assert "email" in str(exc.value).lower()
        assert "invalid" in str(exc.value).lower()

def test_user_creation_with_weak_password_raises_validation_error():
    """Creating a user with weak password should raise ValidationError"""
    weak_passwords = [
        "123",          # Too short
        "password",     # No numbers
        "12345678",     # No letters
        "",             # Empty
    ]

    for weak_password in weak_passwords:
        with pytest.raises(ValidationError) as exc:
            create_user("test@example.com", weak_password)

        assert "password" in str(exc.value).lower()
```

**Risk Level:** 🔴 CRITICAL
**Action:** ❌ BLOCK - Core functionality not tested
**Estimated Fix Time:** 30 minutes

---

### Test 2: test_login()

**Claimed Intent:** Test login
**Actually Tests:** Function call completes

#### Issues Found

🔴 **CRITICAL: Worthless Assertion**
```python
assert result  # Line 11
```
- Passes with any truthy value
- Doesn't verify session/token
- Doesn't verify user authentication state

🔴 **CRITICAL: Missing Negative Tests**
- No test for wrong password
- No test for non-existent user
- No test for locked account
- No test for expired credentials

🟠 **HIGH: No Session Verification**
- Doesn't verify authentication token
- Doesn't verify session expiry
- Doesn't verify user context in session

🟡 **MEDIUM: Test Depends on Previous Test**
- Creates user in this test
- Should use fixture or setup
- Tests should be independent

#### Suggested Improvements

```python
@pytest.fixture
def registered_user():
    """Fixture providing a registered user for login tests"""
    user = create_user("test@example.com", "SecurePass123!")
    yield user
    # Cleanup if needed
    User.delete(user.id)

def test_login_with_valid_credentials_returns_authenticated_session(registered_user):
    """Logging in with correct email and password should:
    1. Return authentication token/session
    2. Set authenticated state
    3. Include user context
    4. Set appropriate expiry
    """
    session = login(registered_user.email, "SecurePass123!")

    assert session is not None, "Login should return session"
    assert session.is_authenticated is True, "Session should be authenticated"
    assert session.user_id == registered_user.id, "Session should contain user ID"
    assert session.token is not None, "Session should have authentication token"
    assert session.expires_at > datetime.now(), "Session should have future expiry"
    assert (session.expires_at - datetime.now()).seconds >= 3600, "Session should last at least 1 hour"

def test_login_with_wrong_password_raises_authentication_error(registered_user):
    """Logging in with incorrect password should raise AuthenticationError"""
    with pytest.raises(AuthenticationError) as exc:
        login(registered_user.email, "WrongPassword")

    assert "Invalid credentials" in str(exc.value)
    assert "password" in str(exc.value).lower()

def test_login_with_nonexistent_email_raises_authentication_error():
    """Logging in with non-existent email should raise AuthenticationError"""
    with pytest.raises(AuthenticationError) as exc:
        login("doesnotexist@example.com", "password")

    assert "Invalid credentials" in str(exc.value)
    # Note: Don't reveal if email exists (security)

def test_login_with_locked_account_raises_account_locked_error(registered_user):
    """Logging in to locked account should raise AccountLockedError"""
    lock_account(registered_user.id)

    with pytest.raises(AccountLockedError) as exc:
        login(registered_user.email, "SecurePass123!")

    assert registered_user.email in str(exc.value)

def test_login_with_empty_password_raises_validation_error(registered_user):
    """Logging in with empty password should raise ValidationError"""
    with pytest.raises(ValidationError) as exc:
        login(registered_user.email, "")

    assert "password" in str(exc.value).lower()
    assert "required" in str(exc.value).lower()
```

**Risk Level:** 🔴 CRITICAL
**Action:** ❌ BLOCK - Authentication not actually tested
**Estimated Fix Time:** 45 minutes

---

### Test 3: test_duplicate_email()

**Claimed Intent:** Test duplicate email handling
**Actually Tests:** Second user creation succeeds (WRONG!)

#### Issues Found

🔴 **CRITICAL: Test is Backwards**
```python
user2 = create_user("test@example.com", "password456")
assert user2  # Line 17
```
- This test expects duplicate creation to SUCCEED
- It should expect it to FAIL with an error
- Test passes when it should fail
- **This is testing the opposite of what's needed**

🔴 **CRITICAL: False Confidence**
- Production bug: duplicate emails are allowed
- Test claims to verify duplicate prevention
- Test actually verifies duplicates work
- QA might approve thinking it's covered

🟡 **MEDIUM: Same Email Issue as Other Tests**
- If this fixed to expect error, needs all improvements from Test 1

#### Suggested Fix

```python
def test_create_user_with_duplicate_email_raises_integrity_error():
    """Creating a user with an email that already exists should:
    1. Raise IntegrityError or ValidationError
    2. Not create duplicate user in database
    3. Preserve existing user data
    """
    email = "test@example.com"

    # Create first user
    user1 = create_user(email, "FirstPassword123!")
    initial_count = User.count()

    # Attempt to create duplicate
    with pytest.raises((IntegrityError, ValidationError)) as exc:
        create_user(email, "SecondPassword456!")

    assert "email" in str(exc.value).lower()
    assert "duplicate" in str(exc.value).lower() or "exists" in str(exc.value).lower()

    # Verify no new user created
    assert User.count() == initial_count, "User count should not increase"

    # Verify original user unchanged
    original_user = User.get_by_email(email)
    assert original_user.id == user1.id, "Original user should be intact"
    assert original_user.verify_password("FirstPassword123!"), "Original password should work"
    assert not original_user.verify_password("SecondPassword456!"), "New password should not work"
```

**Risk Level:** 🔴 CRITICAL
**Action:** ❌ BLOCK - Test verifies opposite of requirement
**Estimated Fix Time:** 20 minutes

---

## Summary Report

### Overall Assessment

**Test Suite Quality:** 🔴 FAILING

**Critical Issues:** 3
- Test 1: Doesn't actually test user creation
- Test 2: Doesn't actually test authentication
- Test 3: Tests opposite of requirement

**Total Tests:** 3
**Effective Tests:** 0
**Coverage:** High (claims)
**Protection:** None (reality)

### Risk Assessment

**Production Risk:** 🔴 EXTREME

Current test suite provides **zero protection** against:
- Data corruption in user creation
- Authentication bypass
- Duplicate email registration
- Password security issues
- Database integrity issues

**Confidence Level:** 0% - Tests passing means nothing

### Required Actions

#### Immediate (Block Merge)
1. Rewrite all three tests with proper assertions
2. Add negative test cases (12+ tests needed)
3. Verify tests catch intentional bugs
4. Add fixture for test user management

#### Follow-up (Required for completion)
1. Add edge case tests (15+ additional tests)
2. Add integration tests for full registration flow
3. Add security tests (SQL injection, XSS, etc.)
4. Add performance tests for registration endpoint

### Estimated Timeline
- Fix critical issues: 2-3 hours
- Complete test suite: 1 day
- Review and iteration: 0.5 days

**Total:** 1.5-2 days for proper test coverage

### Recommendation

❌ **BLOCK MERGE**

Do not approve this PR. Tests provide false confidence and mask critical bugs.

**Evidence:**
- All tests would pass with completely broken functionality
- Duplicate email test verifies the opposite of requirements
- No actual behavior is verified

**Next Steps:**
1. Engineer rewrites tests following examples above
2. QA re-inspects rewritten tests
3. QA verifies tests catch intentional bugs
4. Only then approve merge

---

## Lessons for Engineer

### What Went Wrong

1. **Wrote tests after code** - Led to tests that just confirm code runs
2. **Weak assertions** - "assert x" proves nothing
3. **No mental debugging** - Didn't verify tests catch bugs
4. **No negative testing** - Only tested happy path
5. **Misunderstood duplicate test** - Test verified opposite

### How to Improve

1. **Write tests first** (TDD) - Prevents these issues
2. **Specific assertions** - Verify exact values
3. **Mental debugging** - Break code, ensure test fails
4. **Test failures explicitly** - Every success needs failure test
5. **Read test name carefully** - Test what you claim to test

### TDD Would Have Prevented This

If tests were written first:
```python
# Write this FIRST (it will fail):
def test_user_creation_with_valid_data_persists_to_database():
    user = create_user("test@example.com", "password")
    assert user.email == "test@example.com"  # Will fail until create_user works
    ...

# Then implement create_user to make it pass
```

See the Test-Driven Development skill for complete TDD workflow (available in the skill library for comprehensive TDD guidance).

---

## Sign-off

**QA Inspector:** [Your name]
**Date:** [Date]
**Status:** ❌ REJECTED
**Reason:** Tests provide zero protection, must be rewritten
**Re-inspection Required:** Yes

---

*This is what thorough test inspection looks like. Better to catch these issues now than in production.*
