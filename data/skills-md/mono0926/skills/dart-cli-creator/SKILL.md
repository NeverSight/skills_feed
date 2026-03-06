---
name: dart-cli-creator
description: A skill for creating and improving robust, highly maintainable CLI tools using Dart. It covers comprehensive best practices.
---

# Dart CLI Creator Skill

This skill provides guidelines and procedures for creating and improving top-quality Command-Line Interface (CLI) tools using Dart.
As an agent, you must consistently follow these best practices when requested by the user to create or modify a Dart CLI.

## 🎯 Core Best Practices

### 1. Project Structure and Design

- **`bin/` directory**: Place the entry point executable files for the CLI (e.g., `bin/my_cli.dart`). Keep this as a thin wrapper that only calls top-level functions or classes from `lib/` or `src/`, avoiding complex logic here.
- **`lib/` directory**: Place business logic, command implementations, and reusable utilities here (e.g., `lib/src/commands/`, `lib/src/utils/`).
- **Separation of Concerns**: Always separate the CLI input/output handling (argument parsing, UI rendering) from the core business logic to maximize testability.

### 2. Command-Line Arguments and Routing

- **Leverage the `args` package**: Use `CommandRunner` and `Command` classes from the standard `args` package to build a Git-like CLI with subcommands.
- **Self-documenting**: Carefully write `description` and `help` for each command, flag, and option, ensuring that `--help` provides sufficient usage information.

### 3. Rich UX (User Experience) and Logging

- **Actively use `mason_logger`**: Avoid standard `print` statements; use the `mason_logger` package instead.
  - Output color-coded messages with `logger.info()`, `logger.success()`, `logger.err()`, and `logger.warn()`.
  - Display a spinner for time-consuming tasks using `logger.progress('Doing something...')`.
  - Utilize `logger.confirm()` or `logger.prompt()` for user confirmations (y/n) or text input. If more advanced menu selections or spinners are needed, combine it with the `interact` package.
  - **Tip:** For a practical setup, define `final logger = Logger();` at the top level in `lib/logger.dart` and import it across the project. This reduces boilerplate and is highly convenient (ideal for small to medium-sized CLI tools where DI is not mandatory).
- **`cli_completion`**: Consider using the `cli_completion` package to provide shell completion features by extending `CompletionCommandRunner`.

### 4. Proper Error Handling and Exit Strategies

- **Exit Code**: Always treat the result of the process as an appropriate exit code (`0` for success, `1` or `sysexits`-compliant error codes for errors).
- **Avoid direct `exit()` calls**: Calling `exit()` directly causes the Dart VM to terminate immediately, potentially bypassing resource cleanup (like `finally` blocks). Instead, return an `int` from `CommandRunner.run()`, propagate it to the `main` function, set it to the `exitCode` property, and allow the process to exit naturally (e.g., after waiting for `Process.stdout.close()`).
- **Custom Exception Classes and Handling**: Define custom domain-specific exception classes (e.g., `AppException`) and throw them from deep within the call stack.
- **Global Exception Catching**: Wrap the entire execution of `CommandRunner` in a `try-catch` block to handle `AppException`, `UsageException`, and any uncaught exceptions. Rather than showing stack traces directly to the user, output errors gracefully using `logger.err(e.message)` and return an appropriate exit code.

### 5. Static Analysis and Code Formatting

- **Apply `pedantic_mono`**: Configure `pedantic_mono` in `analysis_options.yaml` and adhere to strict static analysis rules.
- Always resolve all errors and warnings after making code changes, ensuring a clean slate.

### 6. Distribution and Execution Configuration

- **Shebang**: Always include `#!/usr/bin/env dart` as the very first line of executable files directly under `bin/`.
- **Pubspec Configuration**: Define the CLI command name in the `executables:` section of `pubspec.yaml` to enable easy installation via `dart pub global activate`.

### 7. Auto-Update Check Feature

- **Leverage `pub_updater`**: Use `pub_updater` to check `pub.dev` or other registries for new version releases, either on every command execution or periodically.
- If a new version is available, provide an interactive UI prompting the user to update using `logger.warn('Update available!')` or an `interact`-based prompt.

### 8. Version Management and Release Process

- **Robust Version Manipulation**: When manipulating SemVer versions, avoid parsing versions manually whenever possible. Always rely on the `pub_semver` package (e.g., `Version.parse`, `nextMajor`, `nextMinor`) to prevent parsing failures related to edge cases like pre-release tags or build metadata.
- **Automated Releases**: To handle version bumping, CHANGELOG generation, git committing, and publishing to GitHub or pub.dev, utilize the **`release-pub`** skill. If creating an advanced Dart CLI, recommend using this agentic skill to coordinate complex CI/CD and release pipelines safely rather than instructing users to perform these steps manually.

---

## 🛠️ Project Skeleton (Basic Implementation Example)

When creating a CLI, use a structure and implementation similar to the following as a foundation.

### Excerpt from `pubspec.yaml`

```yaml
environment:
  sdk: ^3.11.0 # Always specify the latest stable version

dependencies:
  args: ^2.5.0
  cli_completion: ^0.4.0
  mason_logger: ^0.2.16
  pub_updater: ^0.4.0

dev_dependencies:
  pedantic_mono: any
  test: ^1.24.0

executables:
  my_cli:
```

### `bin/my_cli.dart`

```dart
#!/usr/bin/env dart
import 'dart:io';

import 'package:my_cli/command_runner.dart';

Future<void> main(List<String> arguments) async {
  final exitCode = await MyCliCommandRunner().run(arguments);
  await flushThenExit(exitCode ?? 0);
}

/// Helper method to set the [status] to exitCode, and wait for the standard output/error to flush before exiting
Future<void> flushThenExit(int status) async {
  exitCode = status;
  await Future.wait<void>([
    stdout.close(),
    stderr.close(),
  ]);
}
```

### `lib/logger.dart`

```dart
import 'package:mason_logger/mason_logger.dart';

/// The [Logger] shared across the application.
final logger = Logger();
```

### `lib/command_runner.dart`

```dart
import 'package:args/args.dart';
import 'package:cli_completion/cli_completion.dart';
import 'package:mason_logger/mason_logger.dart';
import 'package:my_cli/logger.dart';
import 'package:pub_updater/pub_updater.dart';

class MyCliCommandRunner extends CompletionCommandRunner<int> {
  MyCliCommandRunner({PubUpdater? pubUpdater})
      : _pubUpdater = pubUpdater ?? PubUpdater(),
        super('my_cli', 'A highly robust Dart CLI tool.') {
    argParser
      ..addFlag(
        'version',
        abbr: 'v',
        negatable: false,
        help: 'Print the current version.',
      )
      ..addFlag(
        'verbose',
        help: 'Enable verbose logging.',
      );
    // TODO: addCommand(MyCustomCommand());
  }

  final PubUpdater _pubUpdater;

  Future<void> _checkForUpdates() async {
    try {
      final isUpToDate = await _pubUpdater.isUpToDate(
        packageName: 'my_cli',
        currentVersion: '1.0.0', // Optionally link to a packageVersion constant
      );
      if (!isUpToDate) {
        final latestVersion = await _pubUpdater.getLatestVersion('my_cli');
        logger.info('\nUpdate available: $latestVersion');
      }
    } catch (_) {}
  }

  @override
  Future<int> run(Iterable<String> args) async {
    try {
      final argResults = parse(args);
      if (argResults['verbose'] == true) {
        logger.level = Level.verbose;
      }

      // Check for version updates (consider asynchronous background execution)
      await _checkForUpdates();

      return await runCommand(argResults) ?? 0;
    } on FormatException catch (e) {
      logger
        ..err(e.message)
        ..info('')
        ..info(usage);
      return 64; // usage error
    } on UsageException catch (e) {
      logger
        ..err(e.message)
        ..info('')
        ..info(usage);
      return 64;
    } on AppException catch (e) {
      // Gracefully output custom domain exceptions
      logger.err(e.message);
      return 1;
    } catch (e, stackTrace) {
      logger
        ..err('An unexpected error occurred: $e')
        ..err('$stackTrace');
      return 1;
    }
  }

  @override
  Future<int?> runCommand(ArgResults topLevelResults) async {
    if (topLevelResults['version'] == true) {
      logger.info('my_cli version: 1.0.0');
      return 0;
    }
    return super.runCommand(topLevelResults);
  }
}

/// A custom exception specific to the domain.
class AppException implements Exception {
  const AppException(this.message);
  final String message;

  @override
  String toString() => message;
}
```

### `lib/src/commands/my_custom_command.dart`

```dart
import 'package:args/command_runner.dart';
import 'package:my_cli/logger.dart';

class MyCustomCommand extends Command<int> {
  MyCustomCommand() {
    argParser.addOption(
      'name',
      abbr: 'n',
      help: 'Your name.',
      mandatory: true,
    );
  }

  @override
  String get description => 'A custom command example.';

  @override
  String get name => 'hello';

  @override
  Future<int> run() async {
    final name = argResults?['name'] as String?;
    final progress = logger.progress('Saying hello to $name...');

    // Simulate a time-consuming task
    await Future<void>.delayed(const Duration(seconds: 1));

    progress.complete('Hello, $name!');
    return 0; // Success
  }
}
```

## 🤖 Instructions for the Agent

When requested by the user to "create a CLI tool for doing X", etc.:

1. Follow the contents of this skill to structure a project centered around `args` and `mason_logger`. Always specify the latest stable Dart SDK version (where the patch version is 0, e.g., `^3.11.0`) in `pubspec.yaml`.
2. Determine the directory structure and orchestrate/propose a set of commands based on the requirements.
3. Introduce `pedantic_mono` and generate high-quality code that adheres to strict static analysis.
4. (If necessary) After development is complete, document the usage instructions in `README.md` and present the user with installation steps, such as using `dart pub global activate --source path .`.
