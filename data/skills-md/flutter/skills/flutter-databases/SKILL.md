---
name: "flutter-databases"
description: "Work with databases in a Flutter app"
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Wed, 04 Mar 2026 18:34:08 GMT"

---
# flutter-data-layer-persistence

## Goal
Architects and implements a robust, MVVM-compliant data layer in Flutter applications. Establishes a single source of truth using the Repository pattern, isolates external API and local database interactions into stateless Services, and implements optimal local caching strategies (e.g., SQLite via `sqflite`) based on data requirements. Assumes a pre-configured Flutter environment.

## Decision Logic
Evaluate the user's data persistence requirements using the following decision tree to select the appropriate caching strategy:

*   **Is the data small, simple key-value pairs (e.g., user preferences, theme settings)?**
    *   *Yes:* Use `shared_preferences`.
*   **Is the data a large, structured, relational dataset requiring fast inserts/queries?**
    *   *Yes:* Use On-device relational databases (`sqflite` or `drift`).
*   **Is the data a large, unstructured/non-relational dataset?**
    *   *Yes:* Use On-device non-relational databases (`hive_ce` or `isar_community`).
*   **Is the data primarily API response caching?**
    *   *Yes:* Use a lightweight remote caching system or interceptors.
*   **Is the data primarily images?**
    *   *Yes:* Use `cached_network_image` to store images on the file system.
*   **Is the data too large for `shared_preferences` but doesn't require querying?**
    *   *Yes:* Use direct File System I/O.

## Instructions

1. **Analyze Data Requirements**
   **STOP AND ASK THE USER:** "What specific data entities need to be managed in the data layer, and what are their persistence requirements (e.g., size, relational complexity, offline-first capabilities)?"
   *Wait for the user's response before proceeding to step 2.*

2. **Configure Dependencies**
   Based on the decision logic, add the required dependencies. For a standard SQLite implementation, execute:
   ```bash
   flutter pub add sqflite path
   ```

3. **Define Domain Models**
   Create pure Dart data classes representing the domain models. These models should contain only the information needed by the rest of the app.
   ```dart
   class Todo {
     final int? id;
     final String title;
     final bool isCompleted;

     const Todo({this.id, required this.title, required this.isCompleted});

     Map<String, dynamic> toMap() {
       return {
         'id': id,
         'title': title,
         'isCompleted': isCompleted ? 1 : 0,
       };
     }

     factory Todo.fromMap(Map<String, dynamic> map) {
       return Todo(
         id: map['id'] as int?,
         title: map['title'] as String,
         isCompleted: map['isCompleted'] == 1,
       );
     }
   }
   ```

4. **Implement the Database Service**
   Create a stateless service class to handle direct interactions with the SQLite database.
   ```dart
   import 'package:path/path.dart';
   import 'package:sqflite/sqflite.dart';

   class DatabaseService {
     Database? _database;

     Future<void> open() async {
       if (_database != null && _database!.isOpen) return;
       
       _database = await openDatabase(
         join(await getDatabasesPath(), 'app_database.db'),
         onCreate: (db, version) {
           return db.execute(
             'CREATE TABLE todos(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, isCompleted INTEGER)',
           );
         },
         version: 1,
       );
     }

     bool get isOpen => _database != null && _database!.isOpen;

     Future<int> insertTodo(Todo todo) async {
       return await _database!.insert(
         'todos',
         todo.toMap(),
         conflictAlgorithm: ConflictAlgorithm.replace,
       );
     }

     Future<List<Todo>> fetchTodos() async {
       final List<Map<String, dynamic>> maps = await _database!.query('todos');
       return maps.map((map) => Todo.fromMap(map)).toList();
     }

     Future<void> deleteTodo(int id) async {
       await _database!.delete(
         'todos',
         where: 'id = ?',
         whereArgs: [id],
       );
     }
   }
   ```

5. **Implement the API Client Service (Optional/If Applicable)**
   Create a stateless service for remote data fetching.
   ```dart
   class ApiClient {
     Future<List<dynamic>> fetchRawTodos() async {
       // Implementation for HTTP GET request
       return []; 
     }
   }
   ```

6. **Implement the Repository**
   Create the Repository class. This is the single source of truth for the application data. It must encapsulate the services as private members.
   ```dart
   class TodoRepository {
     final DatabaseService _databaseService;
     final ApiClient _apiClient;

     TodoRepository({
       required DatabaseService databaseService,
       required ApiClient apiClient,
     })  : _databaseService = databaseService,
           _apiClient = apiClient;

     Future<List<Todo>> getTodos() async {
       await _ensureDbOpen();
       // Example of offline-first logic: fetch local, optionally sync with remote
       return await _databaseService.fetchTodos();
     }

     Future<void> createTodo(Todo todo) async {
       await _ensureDbOpen();
       await _databaseService.insertTodo(todo);
       // Trigger API sync here if necessary
     }

     Future<void> removeTodo(int id) async {
       await _ensureDbOpen();
       await _databaseService.deleteTodo(id);
     }

     Future<void> _ensureDbOpen() async {
       if (!_databaseService.isOpen) {
         await _databaseService.open();
       }
     }
   }
   ```

7. **Validate-and-Fix**
   Review the generated implementation against the following checks:
   *   *Check:* Are the services (`_databaseService`, `_apiClient`) private members of the Repository? If not, refactor to restrict UI layer access.
   *   *Check:* Does the Repository explicitly ensure the database is open before executing queries? If not, inject the `_ensureDbOpen()` pattern.
   *   *Check:* Are primary keys (`id`) used effectively in SQLite queries to optimize update/delete times?

## Constraints
*   **Single Source of Truth:** The UI layer MUST NEVER interact directly with a Service (e.g., `DatabaseService` or `ApiClient`). All data requests must route through the Repository.
*   **Stateless Services:** Service classes must remain stateless and contain no side effects outside of their specific external API/DB wrapper responsibilities.
*   **Domain Model Isolation:** Repositories must transform raw data (from APIs or DBs) into Domain Models before passing them to the UI layer.
*   **SQL Injection Prevention:** Always use parameterized queries (e.g., `whereArgs: [id]`) in `sqflite` operations. Never use string interpolation for SQL queries.
*   **Database State:** The Repository must guarantee the database connection is open before attempting any read/write operations.
