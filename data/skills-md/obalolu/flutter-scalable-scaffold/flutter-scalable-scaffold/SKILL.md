---
name: flutter-scalable-scaffold
description: Create production-ready Flutter mobile app projects with clean architecture, feature-based structure, state management (flutter_bloc/riverpod), routing, theming, networking, secure storage, and reusable components. Includes dependency injection, custom widgets, flavors (dev/prod), environment variables, and backend integration (custom/Firebase/Supabase). Use this skill when users want to scaffold a complete Flutter project with a scalable, production-ready structure.
---

# Flutter Scalable Scaffold Skill

This skill creates a complete, production-ready Flutter mobile application with clean architecture, proper separation of concerns, and all the essential building blocks for a scalable app.

## When to Use This Skill

Use this skill when a user wants to:
- Create a new Flutter mobile app project from scratch
- Set up a production-ready Flutter project structure
- Configure state management (flutter_bloc or riverpod)
- Set up backend integration (custom API, Firebase, or Supabase)
- Configure app flavors (dev/prod)
- Add testing infrastructure

## High-Level Workflow

### Phase 1: Mode Selection & User Input Collection

1. Ask user to choose mode: create_new or integrate_existing
2. If `create_new`: Follow the full workflow (Phase 2-5)
3. If `integrate_existing`: Follow integration workflow (Phase 1b)

### Phase 1b: Integration Mode (Existing Project)

**For integrate_existing mode:**
1. Detect existing Flutter project in working directory
2. Parse existing pubspec.yaml to derive project name
3. Analyze existing dependencies to avoid conflicts
4. Ask which components to add (core, network, feature, testing)
5. Check for existing files and decide merge strategy
6. Install missing dependencies
7. Create folder structure (only missing directories)
8. Create core files (only if not present)
9. Create network layer (if custom backend selected)
10. Create router (only if not present)
11. Create dependency injection (merge with existing if needed)
12. Create new feature module
13. Run code generation

### Phase 2: Confirmation (Create New Mode Only)
3. Display configuration summary and confirm with user

### Phase 3: Project Creation (Create New Mode Only)
4. Create Flutter project with organization and platforms
5. Set up flavors (dev/prod)
6. Install dependencies using flutter pub add
7. Clean up default files
8. Create environment files
9. Set up folder structure
10. Create core files (config, theme, errors, utils)
11. Create network layer (if custom backend)
12. Create router and utilities
13. Create shared widgets
14. Set up dependency injection
15. Create example feature
16. Create main app files
17. Run code generation

### Phase 4: Testing Setup (Create New Mode Only)
18. Configure testing infrastructure
19. Create test examples

### Phase 5: Finalization (Create New Mode Only)
20. Configure run/launch configurations
21. Create README
22. Initialize git (if selected)

## Variable Summary

Store these variables for use throughout the skill:

| Variable | Description | Example |
|----------|-------------|---------|
| `PROJECT_MODE` | Mode: create_new or integrate_existing | `create_new` |
| `PROJECT_NAME` | Project name (lowercase, underscores) | `my_awesome_app` |
| `WORKING_DIR` | Working directory path | `/home/claude` |
| `ORG_ID` | Organization identifier | `com.mycompany` |
| `PLATFORMS` | Platform list | `android,ios` |
| `BACKEND_TYPE` | Backend type | `custom/firebase/supabase/custom+firebase/custom+supabase` |
| `DEV_API_URL` | Development API URL | `https://dev-api.example.com` |
| `PROD_API_URL` | Production API URL | `https://api.example.com` |
| `REQUIRES_API_KEY` | Boolean for API key requirement | `true/false` |
| `FIREBASE_SERVICES` | Array of Firebase services | `["auth", "firestore"]` |
| `SUPABASE_URL` | Supabase URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anon key | `xxx` |
| `STATE_MANAGEMENT` | flutter_bloc or riverpod | `flutter_bloc` |
| `INITIAL_FEATURE` | Initial feature name | `home` |
| `INIT_GIT` | Boolean for git initialization | `true/false` |
| `ENABLE_TESTING` | Boolean for testing setup | `true/false` |
| `TEST_TYPES` | Array of test types | `["unit", "widget", "integration"]` |
| `SETUP_ICONS_SPLASH` | Boolean for app icons/splash | `true/false` |
| `ADD_FORM_VALIDATION` | Boolean for form validators | `true/false` |
| `INTEGRATION_COMPONENTS` | Components to add in integration mode | Array of components |

## Step-by-Step Execution

### Step 1: Verify Prerequisites
- Run `flutter --version` to confirm Flutter SDK is installed
- Check if Flutter project exists in working directory (for integration mode)

### Step 2: Mode Selection
Ask user to choose:
- `create_new` - Create a new Flutter project from scratch
- `integrate_existing` - Add scalable architecture to existing Flutter project

### Step 3: User Input Collection
Follow the questions in `references/user-input-questions.md` to collect all required information from the user.

### Step 4: Create Project (create_new mode only)
Execute the following:
1. Create Flutter project: `flutter create --org ORG_ID --platforms PLATFORMS PROJECT_NAME`
2. Set up flavors as described in `references/project-creation.md`
3. Install dependencies using `flutter pub add` commands
4. Create folder structure
5. Generate all core files using templates from `templates/` folder
6. Set up dependency injection
7. Create example feature
8. Configure testing

See `references/project-creation.md` for detailed instructions on each step.

### Step 4b: Integrate Existing Project (integrate_existing mode only)
Execute the following:
1. Detect existing project: check for `pubspec.yaml`
2. Parse existing project configuration (name, org, dependencies)
3. Ask which components to add (core architecture, network, feature, testing)
4. Install missing dependencies
5. Create missing folder structure
6. Create core files only if not present
7. Create network layer if using custom backend
8. Set up dependency injection (merge if exists)
9. Create new feature module
10. Configure testing infrastructure

See `references/project-creation.md` for integration-specific instructions.

### Step 5: Code Generation
After creating all files, run code generation:
``` Step 6: Testing
If testing is enabled, see `references/testing-setup.md` for testing infrastructure details.

### Step 7: Final Verification
- Verify project builds: `flutter build apk` (Android) or `flutter build ios` (iOS)
- Run tests: `flutter test`

## Template Files

The `templates/` folder contains all code templates. Reference these files when creating the project:

### Core Configuration
- `templates/flavor_config.dart` - Flavor configuration (dev/prod)
- `templates/env_config.dart` - Environment variables configuration
- `templates/app_constants.dart` - App-wide constants

### Utilities
- `templates/app_logger.dart` - Logging utility
- `templates/session_manager.dart` - Session/token management
- `templates/error_handler.dart` - Error handling utility

### Errors
- `templates/exceptions.dart` - Custom exception classes
- `templates/failures.dart` - Failure classes for repositories

### Theme
- `templates/app_colors.dart` - Color constants
- `templates/app_typography.dart` - Text styles
- `templates/app_theme.dart` - ThemeData configuration

### Network (if custom backend)
- `templates/network_dio_client.dart` - Dio client setup
- `templates/api_service.dart` - API service base class

### Routing
- `templates/go_router.dart` - Router configuration

### Dependency Injection
- `templates/dependency_injection.dart` - DI setup with GetIt

### Feature Example (INITIAL_FEATURE)
- `templates/home_screen.dart` - Example screen
- `templates/home_bloc.dart` - BLoC class
- `templates/home_event.dart` - BLoC events
- `templates/home_state.dart` - BLoC states
- `templates/home_repository.dart` - Repository
- `templates/home_entity.dart` - Domain entity

### Main App Files
- `templates/app.dart` - Root app widget
- `templates/main_dev.dart` - Dev entry point
- `templates/main_prod.dart` - Prod entry point

### Configuration Files
- `templates/pubspec.yaml` - Dependencies
- `templates/pubspec_overrides.yaml` - flutter_gen config

### Testing
- `templates/test_helper.dart` - Test utilities

## Code Generation

After creating the project structure, run code generation for:
- Freezed models: `dart run build_runner build --delete-conflicting-outputs`
- Envied: `dart run build_runner build`
- Injectable: `dart run build_runner build`

## Important Notes

1. **State Management**: Use `templates/home_bloc.dart` for flutter_bloc, or create provider equivalents for riverpod
2. **Backend**: Only create network files if using custom backend (not pure Firebase/Supabase)
3. **Assets**: Add actual images to `assets/images/` and `assets/icons/` after creation
4. **Firebase**: Run `flutterfire configure` after project creation if using Firebase
5. **Environment**: Update `.env.dev` and `.env.prod` with actual API keys

## References

- `references/user-input-questions.md` - Detailed questions to ask users
- `references/project-creation.md` - Step-by-step project creation guide
- `references/testing-setup.md` - Testing infrastructure details
