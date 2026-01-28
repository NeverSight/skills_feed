---
name: shell-testing-framework
description: Shell script testing expertise using bash test framework patterns from unix-goto, covering test structure (arrange-act-assert), 4 test categories, assertion patterns, 100% coverage requirements, and performance testing
---

# Shell Testing Framework Expert

Comprehensive testing expertise for bash shell scripts using patterns and methodologies from the unix-goto project, emphasizing 100% test coverage, systematic test organization, and performance validation.

## When to Use This Skill

Use this skill when:
- Writing test suites for bash shell scripts
- Implementing 100% test coverage requirements
- Organizing tests into unit, integration, edge case, and performance categories
- Creating assertion patterns for shell script validation
- Setting up test infrastructure and helpers
- Writing performance tests for shell functions
- Generating test reports and summaries
- Debugging test failures
- Validating shell script behavior

Do NOT use this skill for:
- Testing non-shell applications (use language-specific frameworks)
- Simple ad-hoc script validation
- Production testing (use for development/CI only)
- General QA testing (this is developer-focused unit testing)

## Core Testing Philosophy

### The 100% Coverage Rule

Every core feature in unix-goto has 100% test coverage. This is NON-NEGOTIABLE.

**Coverage Requirements:**
- Core navigation: 100%
- Cache system: 100%
- Bookmarks: 100%
- History: 100%
- Benchmarks: 100%
- New features: 100%

**What This Means:**
- Every function has tests
- Every code path is exercised
- Every error condition is validated
- Every edge case is covered
- Every performance target is verified

### Test-Driven Development Approach

**Workflow:**
1. Write tests FIRST (based on feature spec)
2. Watch tests FAIL (red)
3. Implement feature
4. Watch tests PASS (green)
5. Refactor if needed
6. Validate all tests still pass

## Core Knowledge

### Standard Test File Structure

Every test file follows this exact structure:

```bash
#!/bin/bash
# Test suite for [feature] functionality

set -e  # Exit on error

# ============================================
# Setup
# ============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/module.sh"

# ============================================
# Test Counters
# ============================================

TESTS_PASSED=0
TESTS_FAILED=0

# ============================================
# Test Helpers
# ============================================

pass() {
    echo "✓ PASS: $1"
    ((TESTS_PASSED++))
}

fail() {
    echo "✗ FAIL: $1"
    ((TESTS_FAILED++))
}

# ============================================
# Test Functions
# ============================================

# Test 1: [Category] - [Description]
test_feature_basic() {
    # Arrange
    local input="test"
    local expected="expected_output"

    # Act
    local result=$(function_under_test "$input")

    # Assert
    if [[ "$result" == "$expected" ]]; then
        pass "Basic feature test"
    else
        fail "Basic feature test: expected '$expected', got '$result'"
    fi
}

# ============================================
# Test Execution
# ============================================

# Run all tests
test_feature_basic

# ============================================
# Summary
# ============================================

echo ""
echo "═══════════════════════════════════════"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo "═══════════════════════════════════════"

# Exit with proper code
[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
```

### The Arrange-Act-Assert Pattern

EVERY test function MUST follow this three-phase structure:

**1. Arrange** - Set up test conditions
```bash
# Arrange
local input="test-value"
local expected="expected-result"
local temp_file=$(mktemp)
echo "test data" > "$temp_file"
```

**2. Act** - Execute the code under test
```bash
# Act
local result=$(function_under_test "$input")
local exit_code=$?
```

**3. Assert** - Verify the results
```bash
# Assert
if [[ "$result" == "$expected" && $exit_code -eq 0 ]]; then
    pass "Test description"
else
    fail "Test failed: expected '$expected', got '$result'"
fi
```

**Complete Example:**
```bash
test_cache_lookup_single_match() {
    # Arrange - Create cache with single match
    local cache_file="$HOME/.goto_index"
    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
unix-goto|/Users/manu/Git_Repos/unix-goto|2|1234567890
EOF

    # Act - Lookup folder
    local result=$(__goto_cache_lookup "unix-goto")
    local exit_code=$?

    # Assert - Should return exact path
    local expected="/Users/manu/Git_Repos/unix-goto"
    if [[ "$result" == "$expected" && $exit_code -eq 0 ]]; then
        pass "Cache lookup returns single match"
    else
        fail "Expected '$expected' with code 0, got '$result' with code $exit_code"
    fi
}
```

### The Four Test Categories

EVERY feature requires tests in ALL four categories:

#### Category 1: Unit Tests

**Purpose:** Test individual functions in isolation

**Characteristics:**
- Single function under test
- Minimal dependencies
- Fast execution (<1ms per test)
- Clear, focused assertions

**Example - Cache Lookup Unit Test:**
```bash
test_cache_lookup_not_found() {
    # Arrange
    local cache_file="$HOME/.goto_index"
    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
unix-goto|/Users/manu/Git_Repos/unix-goto|2|1234567890
EOF

    # Act
    local result=$(__goto_cache_lookup "nonexistent")
    local exit_code=$?

    # Assert
    if [[ -z "$result" && $exit_code -eq 1 ]]; then
        pass "Cache lookup not found returns code 1"
    else
        fail "Expected empty result with code 1, got '$result' with code $exit_code"
    fi
}

test_cache_lookup_multiple_matches() {
    # Arrange
    local cache_file="$HOME/.goto_index"
    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
project|/Users/manu/project1|2|1234567890
project|/Users/manu/project2|2|1234567891
EOF

    # Act
    local result=$(__goto_cache_lookup "project")
    local exit_code=$?

    # Assert - Should return all matches with code 2
    local line_count=$(echo "$result" | wc -l)
    if [[ $line_count -eq 2 && $exit_code -eq 2 ]]; then
        pass "Cache lookup returns multiple matches with code 2"
    else
        fail "Expected 2 lines with code 2, got $line_count lines with code $exit_code"
    fi
}
```

**Unit Test Checklist:**
- [ ] Test with valid input
- [ ] Test with invalid input
- [ ] Test with empty input
- [ ] Test with boundary values
- [ ] Test return codes
- [ ] Test output format

#### Category 2: Integration Tests

**Purpose:** Test how multiple modules work together

**Characteristics:**
- Multiple functions/modules interact
- Test realistic workflows
- Validate end-to-end behavior
- Moderate execution time (<100ms per test)

**Example - Navigation Integration Test:**
```bash
test_navigation_with_cache() {
    # Arrange - Setup complete navigation environment
    local cache_file="$HOME/.goto_index"
    local history_file="$HOME/.goto_history"

    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
unix-goto|/Users/manu/Git_Repos/unix-goto|2|1234567890
EOF

    # Act - Perform full navigation
    local start_dir=$(pwd)
    goto unix-goto
    local nav_exit_code=$?
    local end_dir=$(pwd)

    # Assert - Should navigate and track history
    local expected_dir="/Users/manu/Git_Repos/unix-goto"
    local history_recorded=false

    if grep -q "$expected_dir" "$history_file" 2>/dev/null; then
        history_recorded=true
    fi

    if [[ "$end_dir" == "$expected_dir" && $nav_exit_code -eq 0 && $history_recorded == true ]]; then
        pass "Navigation with cache and history tracking"
    else
        fail "Integration test failed: nav=$nav_exit_code, dir=$end_dir, history=$history_recorded"
    fi

    # Cleanup
    cd "$start_dir"
}

test_bookmark_creation_and_navigation() {
    # Arrange
    local bookmark_file="$HOME/.goto_bookmarks"
    rm -f "$bookmark_file"

    # Act - Create bookmark and navigate
    bookmark add testwork /Users/manu/work
    local add_code=$?

    goto @testwork
    local nav_code=$?
    local nav_dir=$(pwd)

    # Assert
    local expected_dir="/Users/manu/work"
    if [[ $add_code -eq 0 && $nav_code -eq 0 && "$nav_dir" == "$expected_dir" ]]; then
        pass "Bookmark creation and navigation integration"
    else
        fail "Integration failed: add=$add_code, nav=$nav_code, dir=$nav_dir"
    fi
}
```

**Integration Test Checklist:**
- [ ] Test common user workflows
- [ ] Test module interactions
- [ ] Test data persistence
- [ ] Test state changes
- [ ] Test error propagation
- [ ] Test cleanup behavior

#### Category 3: Edge Cases

**Purpose:** Test boundary conditions and unusual scenarios

**Characteristics:**
- Unusual but valid inputs
- Boundary conditions
- Error scenarios
- Race conditions
- Resource limits

**Example - Edge Case Tests:**
```bash
test_empty_cache_file() {
    # Arrange - Create empty cache file
    local cache_file="$HOME/.goto_index"
    touch "$cache_file"

    # Act
    local result=$(__goto_cache_lookup "anything")
    local exit_code=$?

    # Assert - Should handle gracefully
    if [[ -z "$result" && $exit_code -eq 1 ]]; then
        pass "Empty cache file handled gracefully"
    else
        fail "Empty cache should return code 1"
    fi
}

test_malformed_cache_entry() {
    # Arrange - Cache with malformed entry
    local cache_file="$HOME/.goto_index"
    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
unix-goto|/path|missing|fields
valid-entry|/valid/path|2|1234567890
EOF

    # Act
    local result=$(__goto_cache_lookup "valid-entry")
    local exit_code=$?

    # Assert - Should still find valid entry
    if [[ "$result" == "/valid/path" && $exit_code -eq 0 ]]; then
        pass "Malformed entry doesn't break valid lookups"
    else
        fail "Should handle malformed entries gracefully"
    fi
}

test_very_long_path() {
    # Arrange - Create entry with very long path
    local long_path=$(printf '/very/long/path/%.0s' {1..50})
    local cache_file="$HOME/.goto_index"
    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
longpath|${long_path}|50|1234567890
EOF

    # Act
    local result=$(__goto_cache_lookup "longpath")
    local exit_code=$?

    # Assert - Should handle long paths
    if [[ "$result" == "$long_path" && $exit_code -eq 0 ]]; then
        pass "Very long paths handled correctly"
    else
        fail "Long path handling failed"
    fi
}

test_special_characters_in_folder_name() {
    # Arrange - Folder with special characters
    local cache_file="$HOME/.goto_index"
    cat > "$cache_file" << EOF
# unix-goto folder index cache
#---
my-project_v2.0|/Users/manu/my-project_v2.0|2|1234567890
EOF

    # Act
    local result=$(__goto_cache_lookup "my-project_v2.0")
    local exit_code=$?

    # Assert
    if [[ "$result" == "/Users/manu/my-project_v2.0" && $exit_code -eq 0 ]]; then
        pass "Special characters in folder name"
    else
        fail "Special character handling failed"
    fi
}

test_concurrent_cache_access() {
    # Arrange
    local cache_file="$HOME/.goto_index"
    __goto_cache_build

    # Act - Simulate concurrent access
    (
        for i in {1..10}; do
            __goto_cache_lookup "unix-goto" &
        done
        wait
    )
    local exit_code=$?

    # Assert - Should handle concurrent reads
    if [[ $exit_code -eq 0 ]]; then
        pass "Concurrent cache access handled"
    else
        fail "Concurrent access failed"
    fi
}
```

**Edge Case Test Checklist:**
- [ ] Empty inputs
- [ ] Missing files
- [ ] Malformed data
- [ ] Very large inputs
- [ ] Special characters
- [ ] Concurrent access
- [ ] Resource exhaustion
- [ ] Permission errors

#### Category 4: Performance Tests

**Purpose:** Validate performance targets are met

**Characteristics:**
- Measure execution time
- Compare against targets
- Use statistical analysis
- Test at scale

**Example - Performance Tests:**
```bash
test_cache_lookup_speed() {
    # Arrange - Build cache
    __goto_cache_build

    # Act - Measure lookup time
    local start=$(date +%s%N)
    __goto_cache_lookup "unix-goto"
    local end=$(date +%s%N)

    # Assert - Should be <100ms
    local duration=$(((end - start) / 1000000))
    local target=100

    if [ $duration -lt $target ]; then
        pass "Cache lookup speed: ${duration}ms (target: <${target}ms)"
    else
        fail "Cache too slow: ${duration}ms (target: <${target}ms)"
    fi
}

test_cache_build_performance() {
    # Arrange - Clean cache
    rm -f ~/.goto_index

    # Act - Measure build time
    local start=$(date +%s%N)
    __goto_cache_build
    local end=$(date +%s%N)

    # Assert - Should be <5 seconds
    local duration=$(((end - start) / 1000000))
    local target=5000

    if [ $duration -lt $target ]; then
        pass "Cache build speed: ${duration}ms (target: <${target}ms)"
    else
        fail "Cache build too slow: ${duration}ms (target: <${target}ms)"
    fi
}

test_history_retrieval_speed() {
    # Arrange - Create history with 100 entries
    local history_file="$HOME/.goto_history"
    rm -f "$history_file"
    for i in {1..100}; do
        echo "$(date +%s)|/path/to/dir$i" >> "$history_file"
    done

    # Act - Measure retrieval time
    local start=$(date +%s%N)
    __goto_recent_dirs 10
    local end=$(date +%s%N)

    # Assert - Should be <10ms
    local duration=$(((end - start) / 1000000))
    local target=10

    if [ $duration -lt $target ]; then
        pass "History retrieval: ${duration}ms (target: <${target}ms)"
    else
        fail "History too slow: ${duration}ms (target: <${target}ms)"
    fi
}

test_benchmark_cache_at_scale() {
    # Arrange - Create large workspace
    local workspace=$(mktemp -d)
    for i in {1..500}; do
        mkdir -p "$workspace/folder-$i"
    done

    # Act - Build cache and measure lookup
    local old_paths="$GOTO_SEARCH_PATHS"
    export GOTO_SEARCH_PATHS="$workspace"

    __goto_cache_build

    local start=$(date +%s%N)
    __goto_cache_lookup "folder-250"
    local end=$(date +%s%N)

    # Assert - Even with 500 folders, should be <100ms
    local duration=$(((end - start) / 1000000))
    local target=100

    if [ $duration -lt $target ]; then
        pass "Cache at scale (500 folders): ${duration}ms"
    else
        fail "Cache at scale too slow: ${duration}ms"
    fi

    # Cleanup
    export GOTO_SEARCH_PATHS="$old_paths"
    rm -rf "$workspace"
}
```

**Performance Test Checklist:**
- [ ] Measure critical path operations
- [ ] Compare against defined targets
- [ ] Test at realistic scale
- [ ] Test with maximum load
- [ ] Calculate statistics (min/max/mean/median)
- [ ] Verify no performance regressions

### Assertion Patterns

#### Basic Assertions

**String Equality:**
```bash
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-String equality}"

    if [[ "$actual" == "$expected" ]]; then
        pass "$message"
    else
        fail "$message: expected '$expected', got '$actual'"
    fi
}

# Usage
assert_equal "expected" "$result" "Function returns expected value"
```

**Exit Code Assertions:**
```bash
assert_success() {
    local exit_code=$?
    local message="${1:-Command should succeed}"

    if [ $exit_code -eq 0 ]; then
        pass "$message"
    else
        fail "$message: exit code $exit_code"
    fi
}

assert_failure() {
    local exit_code=$?
    local message="${1:-Command should fail}"

    if [ $exit_code -ne 0 ]; then
        pass "$message"
    else
        fail "$message: expected non-zero exit code"
    fi
}

# Usage
some_command
assert_success "Command executed successfully"
```

**Numeric Comparisons:**
```bash
assert_less_than() {
    local actual=$1
    local limit=$2
    local message="${3:-Value should be less than limit}"

    if [ $actual -lt $limit ]; then
        pass "$message: $actual < $limit"
    else
        fail "$message: $actual >= $limit"
    fi
}

assert_greater_than() {
    local actual=$1
    local limit=$2
    local message="${3:-Value should be greater than limit}"

    if [ $actual -gt $limit ]; then
        pass "$message: $actual > $limit"
    else
        fail "$message: $actual <= $limit"
    fi
}

# Usage
assert_less_than $duration 100 "Cache lookup time"
```

#### File System Assertions

**File Existence:**
```bash
assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist}"

    if [ -f "$file" ]; then
        pass "$message: $file"
    else
        fail "$message: $file not found"
    fi
}

assert_dir_exists() {
    local dir="$1"
    local message="${2:-Directory should exist}"

    if [ -d "$dir" ]; then
        pass "$message: $dir"
    else
        fail "$message: $dir not found"
    fi
}

# Usage
assert_file_exists "$HOME/.goto_index" "Cache file created"
```

**File Content Assertions:**
```bash
assert_file_contains() {
    local file="$1"
    local pattern="$2"
    local message="${3:-File should contain pattern}"

    if grep -q "$pattern" "$file" 2>/dev/null; then
        pass "$message"
    else
        fail "$message: pattern '$pattern' not found in $file"
    fi
}

assert_line_count() {
    local file="$1"
    local expected=$2
    local message="${3:-File should have expected line count}"

    local actual=$(wc -l < "$file" | tr -d ' ')

    if [ $actual -eq $expected ]; then
        pass "$message: $actual lines"
    else
        fail "$message: expected $expected lines, got $actual"
    fi
}

# Usage
assert_file_contains "$HOME/.goto_bookmarks" "work|/path/to/work"
assert_line_count "$HOME/.goto_history" 10
```

#### Output Assertions

**Contains Pattern:**
```bash
assert_output_contains() {
    local output="$1"
    local pattern="$2"
    local message="${3:-Output should contain pattern}"

    if [[ "$output" =~ $pattern ]]; then
        pass "$message"
    else
        fail "$message: pattern '$pattern' not found in output"
    fi
}

# Usage
output=$(goto recent)
assert_output_contains "$output" "/Users/manu/work" "Recent shows work directory"
```

**Empty Output:**
```bash
assert_output_empty() {
    local output="$1"
    local message="${2:-Output should be empty}"

    if [[ -z "$output" ]]; then
        pass "$message"
    else
        fail "$message: got '$output'"
    fi
}

# Usage
output=$(goto nonexistent 2>&1)
assert_output_empty "$output"
```

### Test Helper Functions

Create a reusable test helpers library:

```bash
#!/bin/bash
# test-helpers.sh - Reusable test utilities

# ============================================
# Setup/Teardown
# ============================================

setup_test_env() {
    # Create temp directory for test
    TEST_TEMP_DIR=$(mktemp -d)

    # Backup real files
    [ -f "$HOME/.goto_index" ] && cp "$HOME/.goto_index" "$TEST_TEMP_DIR/goto_index.bak"
    [ -f "$HOME/.goto_bookmarks" ] && cp "$HOME/.goto_bookmarks" "$TEST_TEMP_DIR/goto_bookmarks.bak"
    [ -f "$HOME/.goto_history" ] && cp "$HOME/.goto_history" "$TEST_TEMP_DIR/goto_history.bak"
}

teardown_test_env() {
    # Restore backups
    [ -f "$TEST_TEMP_DIR/goto_index.bak" ] && mv "$TEST_TEMP_DIR/goto_index.bak" "$HOME/.goto_index"
    [ -f "$TEST_TEMP_DIR/goto_bookmarks.bak" ] && mv "$TEST_TEMP_DIR/goto_bookmarks.bak" "$HOME/.goto_bookmarks"
    [ -f "$TEST_TEMP_DIR/goto_history.bak" ] && mv "$TEST_TEMP_DIR/goto_history.bak" "$HOME/.goto_history"

    # Remove temp directory
    rm -rf "$TEST_TEMP_DIR"
}

# ============================================
# Test Data Creation
# ============================================

create_test_cache() {
    local entries="${1:-10}"
    local cache_file="$HOME/.goto_index"

    cat > "$cache_file" << EOF
# unix-goto folder index cache
# Version: 1.0
# Built: $(date +%s)
# Depth: 3
# Format: folder_name|full_path|depth|last_modified
#---
EOF

    for i in $(seq 1 $entries); do
        echo "folder-$i|/path/to/folder-$i|2|$(date +%s)" >> "$cache_file"
    done
}

create_test_bookmarks() {
    local count="${1:-5}"
    local bookmark_file="$HOME/.goto_bookmarks"

    rm -f "$bookmark_file"
    for i in $(seq 1 $count); do
        echo "bookmark$i|/path/to/bookmark$i|$(date +%s)" >> "$bookmark_file"
    done
}

create_test_history() {
    local count="${1:-20}"
    local history_file="$HOME/.goto_history"

    rm -f "$history_file"
    for i in $(seq 1 $count); do
        echo "$(date +%s)|/path/to/dir$i" >> "$history_file"
    done
}

# ============================================
# Timing Utilities
# ============================================

time_function_ms() {
    local func="$1"
    shift
    local args="$@"

    local start=$(date +%s%N)
    $func $args
    local end=$(date +%s%N)

    echo $(((end - start) / 1000000))
}

# ============================================
# Assertion Helpers
# ============================================

assert_function_exists() {
    local func="$1"

    if declare -f "$func" > /dev/null; then
        pass "Function $func exists"
    else
        fail "Function $func not found"
    fi
}

assert_variable_set() {
    local var="$1"

    if [ -n "${!var}" ]; then
        pass "Variable $var is set"
    else
        fail "Variable $var not set"
    fi
}
```

## Examples

### Example 1: Complete Cache Test Suite

```bash
#!/bin/bash
# test-cache.sh - Comprehensive cache system test suite

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/cache-index.sh"
source "$SCRIPT_DIR/test-helpers.sh"

TESTS_PASSED=0
TESTS_FAILED=0

pass() { echo "✓ PASS: $1"; ((TESTS_PASSED++)); }
fail() { echo "✗ FAIL: $1"; ((TESTS_FAILED++)); }

# ============================================
# Unit Tests
# ============================================

echo "Unit Tests"
echo "─────────────────────────────────────────"

test_cache_lookup_single_match() {
    setup_test_env

    # Arrange
    cat > "$HOME/.goto_index" << EOF
# unix-goto folder index cache
#---
unix-goto|/Users/manu/Git_Repos/unix-goto|2|1234567890
EOF

    # Act
    local result=$(__goto_cache_lookup "unix-goto")
    local exit_code=$?

    # Assert
    if [[ "$result" == "/Users/manu/Git_Repos/unix-goto" && $exit_code -eq 0 ]]; then
        pass "Unit: Single match lookup"
    else
        fail "Unit: Single match lookup - got '$result' code $exit_code"
    fi

    teardown_test_env
}

test_cache_lookup_not_found() {
    setup_test_env

    # Arrange
    create_test_cache 5

    # Act
    local result=$(__goto_cache_lookup "nonexistent")
    local exit_code=$?

    # Assert
    if [[ -z "$result" && $exit_code -eq 1 ]]; then
        pass "Unit: Not found returns code 1"
    else
        fail "Unit: Not found - got '$result' code $exit_code"
    fi

    teardown_test_env
}

test_cache_lookup_multiple_matches() {
    setup_test_env

    # Arrange
    cat > "$HOME/.goto_index" << EOF
# unix-goto folder index cache
#---
project|/Users/manu/project1|2|1234567890
project|/Users/manu/project2|2|1234567891
EOF

    # Act
    local result=$(__goto_cache_lookup "project")
    local exit_code=$?
    local line_count=$(echo "$result" | wc -l | tr -d ' ')

    # Assert
    if [[ $line_count -eq 2 && $exit_code -eq 2 ]]; then
        pass "Unit: Multiple matches returns code 2"
    else
        fail "Unit: Multiple matches - got $line_count lines code $exit_code"
    fi

    teardown_test_env
}

# ============================================
# Integration Tests
# ============================================

echo ""
echo "Integration Tests"
echo "─────────────────────────────────────────"

test_cache_build_and_lookup() {
    setup_test_env

    # Arrange
    rm -f "$HOME/.goto_index"

    # Act
    __goto_cache_build
    local build_code=$?

    local result=$(__goto_cache_lookup "unix-goto")
    local lookup_code=$?

    # Assert
    if [[ $build_code -eq 0 && $lookup_code -eq 0 && -n "$result" ]]; then
        pass "Integration: Build and lookup"
    else
        fail "Integration: Build ($build_code) and lookup ($lookup_code) failed"
    fi

    teardown_test_env
}

# ============================================
# Edge Cases
# ============================================

echo ""
echo "Edge Case Tests"
echo "─────────────────────────────────────────"

test_empty_cache_file() {
    setup_test_env

    # Arrange
    touch "$HOME/.goto_index"

    # Act
    local result=$(__goto_cache_lookup "anything")
    local exit_code=$?

    # Assert
    if [[ -z "$result" && $exit_code -eq 1 ]]; then
        pass "Edge: Empty cache handled"
    else
        fail "Edge: Empty cache should return code 1"
    fi

    teardown_test_env
}

test_special_characters() {
    setup_test_env

    # Arrange
    cat > "$HOME/.goto_index" << EOF
# unix-goto folder index cache
#---
my-project_v2.0|/Users/manu/my-project_v2.0|2|1234567890
EOF

    # Act
    local result=$(__goto_cache_lookup "my-project_v2.0")
    local exit_code=$?

    # Assert
    if [[ "$result" == "/Users/manu/my-project_v2.0" && $exit_code -eq 0 ]]; then
        pass "Edge: Special characters in name"
    else
        fail "Edge: Special characters failed"
    fi

    teardown_test_env
}

# ============================================
# Performance Tests
# ============================================

echo ""
echo "Performance Tests"
echo "─────────────────────────────────────────"

test_cache_lookup_speed() {
    setup_test_env

    # Arrange
    create_test_cache 100

    # Act
    local duration=$(time_function_ms __goto_cache_lookup "folder-50")

    # Assert - Should be <100ms
    if [ $duration -lt 100 ]; then
        pass "Performance: Cache lookup ${duration}ms (<100ms target)"
    else
        fail "Performance: Cache too slow ${duration}ms"
    fi

    teardown_test_env
}

test_cache_build_speed() {
    setup_test_env

    # Arrange
    rm -f "$HOME/.goto_index"

    # Act
    local duration=$(time_function_ms __goto_cache_build)

    # Assert - Should be <5000ms (5 seconds)
    if [ $duration -lt 5000 ]; then
        pass "Performance: Cache build ${duration}ms (<5000ms target)"
    else
        fail "Performance: Cache build too slow ${duration}ms"
    fi

    teardown_test_env
}

# ============================================
# Run All Tests
# ============================================

test_cache_lookup_single_match
test_cache_lookup_not_found
test_cache_lookup_multiple_matches

test_cache_build_and_lookup

test_empty_cache_file
test_special_characters

test_cache_lookup_speed
test_cache_build_speed

# ============================================
# Summary
# ============================================

echo ""
echo "═══════════════════════════════════════"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo "Coverage: 100% (all code paths tested)"
echo "═══════════════════════════════════════"

[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
```

### Example 2: Benchmark Test Suite

```bash
#!/bin/bash
# test-benchmark.sh - Test suite for benchmark functionality

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/benchmarks/bench-helpers.sh"

TESTS_PASSED=0
TESTS_FAILED=0

pass() { echo "✓ PASS: $1"; ((TESTS_PASSED++)); }
fail() { echo "✗ FAIL: $1"; ((TESTS_FAILED++)); }

# Unit Tests
test_bench_time_ms() {
    # Arrange
    local cmd="sleep 0.1"

    # Act
    local duration=$(bench_time_ms $cmd)

    # Assert - Should be ~100ms
    if [ $duration -ge 90 ] && [ $duration -le 150 ]; then
        pass "bench_time_ms measures correctly: ${duration}ms"
    else
        fail "bench_time_ms inaccurate: ${duration}ms (expected ~100ms)"
    fi
}

test_bench_calculate_stats() {
    # Arrange
    local values=(10 20 30 40 50)

    # Act
    local stats=$(bench_calculate_stats "${values[@]}")
    IFS=',' read -r min max mean median stddev <<< "$stats"

    # Assert
    if [[ $min -eq 10 && $max -eq 50 && $mean -eq 30 ]]; then
        pass "bench_calculate_stats computes correctly"
    else
        fail "Stats calculation failed: min=$min max=$max mean=$mean"
    fi
}

test_bench_create_workspace() {
    # Arrange/Act
    local workspace=$(bench_create_workspace "small")

    # Assert
    if [ -d "$workspace" ] && [ $(ls -1 "$workspace" | wc -l) -eq 10 ]; then
        pass "Workspace creation (small: 10 folders)"
        bench_cleanup_workspace "$workspace"
    else
        fail "Workspace creation failed"
    fi
}

# Run tests
test_bench_time_ms
test_bench_calculate_stats
test_bench_create_workspace

echo ""
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

[ $TESTS_FAILED -eq 0 ] && exit 0 || exit 1
```

## Best Practices

### Test Organization

**File Naming Convention:**
```
test-cache.sh          # Test cache system
test-bookmark.sh       # Test bookmarks
test-navigation.sh     # Test navigation
test-benchmark.sh      # Test benchmarks
```

**Test Function Naming:**
```
test_[category]_[feature]_[scenario]

Examples:
test_unit_cache_lookup_single_match
test_integration_navigation_with_cache
test_edge_empty_input
test_performance_cache_speed
```

### Test Independence

Each test must be completely independent:

```bash
# Good - Independent test
test_feature() {
    # Setup own environment
    local temp=$(mktemp)

    # Test
    result=$(function_under_test)

    # Cleanup own resources
    rm -f "$temp"

    # Assert
    [[ "$result" == "expected" ]] && pass "Test" || fail "Test"
}

# Bad - Depends on previous test state
test_feature_bad() {
    # Assumes something from previous test
    result=$(function_under_test)  # May fail if run alone
}
```

### Meaningful Failure Messages

```bash
# Good - Detailed failure message
if [[ "$result" != "$expected" ]]; then
    fail "Cache lookup failed: expected '$expected', got '$result', exit code: $exit_code"
fi

# Bad - Vague failure message
if [[ "$result" != "$expected" ]]; then
    fail "Test failed"
fi
```

### Test Execution Speed

Keep tests FAST:

- Unit tests: <1ms each
- Integration tests: <100ms each
- Edge cases: <10ms each
- Performance tests: As needed for measurement

Total test suite should run in <5 seconds.

## Quick Reference

### Test Template Checklist

- [ ] Shebang and set -e
- [ ] Source required modules
- [ ] Initialize test counters
- [ ] Define pass/fail helpers
- [ ] Organize tests by category
- [ ] Use arrange-act-assert pattern
- [ ] Print summary with exit code

### Coverage Checklist

- [ ] All public functions tested
- [ ] All code paths exercised
- [ ] All return codes validated
- [ ] All error conditions tested
- [ ] All edge cases covered
- [ ] Performance targets verified

### Essential Test Commands

```bash
# Run single test suite
bash test-cache.sh

# Run all tests
bash test-cache.sh && bash test-bookmark.sh && bash test-navigation.sh

# Run with verbose output
set -x; bash test-cache.sh; set +x

# Run specific test function
bash -c 'source test-cache.sh; test_cache_lookup_single_match'
```

---

**Skill Version:** 1.0
**Last Updated:** October 2025
**Maintained By:** Manu Tej + Claude Code
**Source:** unix-goto testing patterns and methodologies
