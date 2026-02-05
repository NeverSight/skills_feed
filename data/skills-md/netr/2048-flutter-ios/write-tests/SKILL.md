---
name: write-tests
description: Write meaningful Flutter tests that prove behavior works, not tests for the sake of tests. Covers unit, widget, and integration testing.
triggers:
  - write tests
  - add tests
  - test
  - testing
  - unit test
  - widget test
  - integration test
role: specialist
scope: implementation
output-format: code
---

# Write Tests

Write meaningful tests that prove behavior works. Tests exist to prove YOUR code's behavior works, not to test Flutter framework internals or duplicate implementation details.

## Core Philosophy: The One Question

Before writing ANY test, ask: **"What behavior am I proving works?"**

If your answer is:
- "That Flutter's setState works" → **DON'T WRITE IT** (Flutter is already tested)
- "That my widget has these fields" → **DON'T WRITE IT** (the compiler already checks this)
- "That Provider/Riverpod notifies listeners" → **DON'T WRITE IT** (the package tests this)
- "That my game logic produces the right output" → **WRITE IT** (this is YOUR logic)
- "That this function handles edge cases correctly" → **WRITE IT** (this is YOUR behavior)
- "That these components integrate correctly" → **WRITE IT** (this is YOUR integration)

---

## The Three Test Types

### 1. Unit Tests (70-80% of tests)

Test pure logic without Flutter widgets. Fast, isolated, most valuable.

```dart
// test/game_logic_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('GameController', () {
    late GameController controller;

    setUp(() {
      controller = GameController();
    });

    // ✅ GOOD: Clear scenario AND expected outcome
    test('merge combines adjacent tiles with same value', () {
      controller.setBoard([
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ]);

      controller.move(Direction.left);

      expect(controller.board[0][0], 4);
    });

    // ✅ GOOD: Tests edge case in YOUR logic
    test('move does nothing when no tiles can move', () {
      controller.setBoard([
        [2, 4, 2, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
      ]);
      final boardBefore = controller.board.map((r) => [...r]).toList();

      controller.move(Direction.left);

      expect(controller.board, boardBefore);
    });
  });
}
```

### 2. Widget Tests (15-25% of tests)

Test widgets in isolation. Verify UI responds correctly to state.

```dart
// test/widgets/game_tile_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  // ✅ GOOD: Tests YOUR widget's behavior
  testWidgets('GameTile displays value when non-zero', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: GameTile(value: 2048),
      ),
    );

    expect(find.text('2048'), findsOneWidget);
  });

  // ✅ GOOD: Tests YOUR conditional rendering logic
  testWidgets('GameTile shows nothing for zero value', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: GameTile(value: 0),
      ),
    );

    expect(find.text('0'), findsNothing);
  });

  // ✅ GOOD: Tests YOUR gesture handling
  testWidgets('GameBoard calls onMove when swiped right', (tester) async {
    Direction? capturedDirection;

    await tester.pumpWidget(
      MaterialApp(
        home: GameBoard(
          onMove: (dir) => capturedDirection = dir,
        ),
      ),
    );

    await tester.fling(find.byType(GameBoard), const Offset(300, 0), 500);

    expect(capturedDirection, Direction.right);
  });
}
```

### 3. Integration Tests (5-10% of tests)

Test complete user flows. Run on device/emulator.

```dart
// integration_test/game_flow_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // ✅ GOOD: Tests complete user journey
  testWidgets('new game starts with score zero and two tiles', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    expect(find.text('0'), findsWidgets); // Score display
    // Verify initial board state
  });

  // ✅ GOOD: Tests that interactions work end-to-end
  testWidgets('game over dialog appears when no moves left', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Play until game over (or set up game over state)
    // ...

    expect(find.text('Game Over'), findsOneWidget);
  });
}
```

---

## Writing Quality Tests

### Descriptive Test Names

Test names should include **both the scenario being tested and the expected outcome**.

```dart
// ❌ BAD: What's the expected outcome?
test('test move left', () { ... });

// ✅ GOOD: Clear scenario AND expected outcome
test('move left merges adjacent tiles with same value', () { ... });

// ❌ BAD: Too vague
test('test score', () { ... });

// ✅ GOOD: Specific behavior
test('score increases by merged tile value after merge', () { ... });
```

### One Scenario Per Test

Each test should exercise **one scenario**. A red flag: after asserting one thing, the test does more actions.

```dart
// ❌ BAD: Tests multiple scenarios
test('game logic', () {
  // Scenario 1: merge
  controller.setBoard([[2, 2, 0, 0], ...]);
  controller.move(Direction.left);
  expect(controller.board[0][0], 4);

  // Scenario 2: score
  expect(controller.score, 4);

  // Scenario 3: game over
  controller.setBoard([[2, 4, 2, 4], ...]);
  expect(controller.isGameOver, true);
});

// ✅ GOOD: Each scenario is its own test
test('move left merges adjacent tiles with same value', () { ... });
test('merge adds merged value to score', () { ... });
test('game is over when no moves are possible', () { ... });
```

### Narrow Assertions

Test only what matters for this specific behavior.

```dart
// ❌ BAD: Broad assertion - breaks when any field changes
test('move updates state', () {
  controller.move(Direction.left);
  expect(controller.state, GameState(
    board: [[4, 0, 0, 0], ...],
    score: 4,
    isGameOver: false,
    hasWon: false,
    moveCount: 1,
    // ... 10 more fields
  ));
});

// ✅ GOOD: Only checks what matters
test('move left merges tiles', () {
  controller.setBoard([[2, 2, 0, 0], ...]);
  controller.move(Direction.left);
  expect(controller.board[0][0], 4);
});
```

### Cause and Effect Together

The action being tested should appear immediately before the assertion.

```dart
// ❌ BAD: Setup is far from assertion
test('score updates', () {
  controller.setBoard([[2, 2, 0, 0], ...]); // Line 10
  controller.move(Direction.left);
  controller.move(Direction.right);
  controller.move(Direction.up);
  // ... 20 more lines ...
  expect(controller.score, 4); // Why 4? Have to hunt for it
});

// ✅ GOOD: Cause and effect are adjacent
test('merge adds merged value to score', () {
  controller.setBoard([[2, 2, 0, 0], ...]);
  controller.move(Direction.left); // Merges 2+2=4

  expect(controller.score, 4); // Obvious: merged tile value
});
```

---

## What Makes a Test Wasteful

### Testing Flutter/Package Internals

```dart
// ❌ DELETE: You're testing Provider, not your code
test('ChangeNotifier notifies listeners', () {
  final controller = GameController();
  var notified = false;
  controller.addListener(() => notified = true);
  controller.move(Direction.left);
  expect(notified, true);
});
```

Provider already tests this. You don't need to.

### Testing That Code Compiles

```dart
// ❌ DELETE: If it compiles, it works
test('can create GameController', () {
  final controller = GameController();
  expect(controller, isNotNull);
});
```

The Dart compiler guarantees this.

### Duplicating Implementation in Assertions

```dart
// ❌ DELETE: This just mirrors the implementation
test('default board is 4x4', () {
  final controller = GameController();
  expect(controller.board.length, 4);
  expect(controller.board[0].length, 4);
});
```

If you change the default, you change the test. Zero value.

---

## The Bug-First Testing Pattern

**When you find a bug, write a test FIRST that proves the bug exists, then fix the bug.**

```dart
// 1. Bug reported: "Tiles don't merge when moving into wall"

// 2. Write a failing test that demonstrates the bug
test('tiles merge when pushed against wall', () {
  controller.setBoard([
    [0, 0, 2, 2],  // Should merge to [0, 0, 0, 4]
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
  ]);

  controller.move(Direction.right);

  expect(controller.board[0][3], 4);  // FAILS before fix
});

// 3. Fix the bug
// 4. Test passes
// 5. You now have a regression test forever
```

This ensures:
- The bug is reproducible
- The fix actually works
- The bug never comes back

---

## Test File Organization

```
test/
├── unit/
│   ├── game_controller_test.dart
│   ├── board_logic_test.dart
│   └── score_calculator_test.dart
├── widgets/
│   ├── game_tile_test.dart
│   ├── game_board_test.dart
│   └── score_display_test.dart
└── helpers/
    └── test_helpers.dart

integration_test/
└── game_flow_test.dart
```

---

## Test Helpers

Create helpers for common setup, but keep assertions inline:

```dart
// test/helpers/test_helpers.dart

/// Creates a board with specific tile positions
List<List<int>> boardWith(Map<(int, int), int> tiles) {
  final board = List.generate(4, (_) => List.filled(4, 0));
  for (final entry in tiles.entries) {
    board[entry.key.$1][entry.key.$2] = entry.value;
  }
  return board;
}

/// Creates a controller with a preset board
GameController controllerWith(List<List<int>> board) {
  final controller = GameController();
  controller.setBoard(board);
  return controller;
}
```

Usage:
```dart
test('tiles slide to edge', () {
  final controller = controllerWith([
    [0, 0, 0, 2],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
  ]);

  controller.move(Direction.left);

  expect(controller.board[0][0], 2);
});
```

---

## Decision Framework

| Question | If Yes | If No |
|----------|--------|-------|
| Does this test YOUR logic? | Write it | Don't write it |
| Would a bug here cause user-visible problems? | Write it | Probably skip |
| Am I testing Flutter/package internals? | Don't write it | N/A |
| Am I duplicating the implementation? | Don't write it | N/A |
| Does the test name describe scenario AND outcome? | Good | Rename it |
| Does this test exercise only ONE scenario? | Good | Split it |
| Is cause immediately before effect? | Good | Restructure |

---

## Running Tests

```bash
# All unit + widget tests
flutter test

# With coverage report
flutter test --coverage

# Single file
flutter test test/unit/game_controller_test.dart

# Integration tests (requires device/emulator)
flutter test integration_test/
```

---

## Summary

**Write tests that:**
- Prove YOUR code's behavior works
- Have descriptive names (scenario + expected outcome)
- Test ONE scenario per test
- Use narrow assertions (only check relevant fields)
- Keep cause and effect adjacent
- Start with a failing test when fixing bugs

**Don't write tests that:**
- Test Flutter/package internals
- Duplicate the implementation in assertions
- Check that widgets have fields
- Verify defaults equal what you wrote
- Combine multiple scenarios in one test
