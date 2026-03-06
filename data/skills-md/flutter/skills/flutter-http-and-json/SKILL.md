---
name: "flutter-http-and-json"
description: "Make HTTP requests and encode / decode JSON in a Flutter app"
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Wed, 04 Mar 2026 17:55:17 GMT"

---
# flutter-http-json-networking

## Goal
Manages HTTP networking and JSON data handling in Flutter applications. Implements secure, asynchronous REST API calls (GET, POST, PUT, DELETE) using the `http` package. Handles JSON serialization, background parsing via isolates for large datasets, and structured JSON schemas for AI model integrations. Assumes the `http` package is added to `pubspec.yaml` and the environment supports Dart 3 pattern matching and null safety.

## Decision Logic
When implementing JSON parsing and serialization, evaluate the following decision tree:
1. **Payload Size:** 
   * If the JSON payload is small, parse synchronously on the main thread.
   * If the JSON payload is large (takes >16ms to parse), use background parsing via `compute()` to avoid UI jank.
2. **Model Complexity:**
   * If the data model is simple or a quick prototype, use manual serialization (`dart:convert`).
   * If the data model is highly nested or part of a large production app, **STOP AND ASK THE USER:** "Should we configure `json_serializable` and `build_runner` for automated code generation?"

## Instructions

### 1. Configure Platform Permissions
Before making network requests, ensure the target platforms have the required internet permissions.

**Android (`android/app/src/main/AndroidManifest.xml`):**
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Required to fetch data from the internet. -->
    <uses-permission android:name="android.permission.INTERNET" />
    <application ...>
</manifest>
```

**macOS (`macos/Runner/DebugProfile.entitlements` and `Release.entitlements`):**
```xml
<dict>
    <!-- Required to fetch data from the internet. -->
    <key>com.apple.security.network.client</key>
    <true/>
</dict>
```

### 2. Define the JSON Data Model
Create a strongly typed Dart class to represent the JSON data. Use factory constructors for deserialization and a `toJson` method for serialization.

```dart
import 'dart:convert';

class ItemModel {
  final int id;
  final String title;

  const ItemModel({required this.id, required this.title});

  // Deserialize using Dart 3 pattern matching
  factory ItemModel.fromJson(Map<String, dynamic> json) {
    return switch (json) {
      {'id': int id, 'title': String title} => ItemModel(id: id, title: title),
      _ => throw const FormatException('Failed to parse ItemModel.'),
    };
  }

  // Serialize to JSON
  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
      };
}
```

### 3. Implement HTTP Operations (CRUD)
Use the `http` package to perform network requests. Always use `Uri.https` for safe URL encoding. Validate the status code and throw exceptions on failure.

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final http.Client client;
  ApiService(this.client);

  // GET Request
  Future<ItemModel> fetchItem(int id) async {
    final uri = Uri.https('api.example.com', '/items/$id');
    final response = await client.get(uri);

    if (response.statusCode == 200) {
      return ItemModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      throw Exception('Failed to load item: ${response.statusCode}');
    }
  }

  // POST Request
  Future<ItemModel> createItem(String title) async {
    final uri = Uri.https('api.example.com', '/items');
    final response = await client.post(
      uri,
      headers: <String, String>{'Content-Type': 'application/json; charset=UTF-8'},
      body: jsonEncode(<String, String>{'title': title}),
    );

    if (response.statusCode == 201) {
      return ItemModel.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      throw Exception('Failed to create item: ${response.statusCode}');
    }
  }

  // DELETE Request
  Future<void> deleteItem(int id) async {
    final uri = Uri.https('api.example.com', '/items/$id');
    final response = await client.delete(
      uri,
      headers: <String, String>{'Content-Type': 'application/json; charset=UTF-8'},
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to delete item: ${response.statusCode}');
    }
  }
}
```

### 4. Implement Background Parsing for Large JSON Arrays
If fetching a large list of objects, move the JSON decoding and mapping to a separate isolate using `compute()`.

```dart
import 'package:flutter/foundation.dart';

// Top-level function required for compute()
List<ItemModel> parseItems(String responseBody) {
  final parsed = (jsonDecode(responseBody) as List<Object?>).cast<Map<String, Object?>>();
  return parsed.map<ItemModel>(ItemModel.fromJson).toList();
}

Future<List<ItemModel>> fetchLargeItemList(http.Client client) async {
  final uri = Uri.https('api.example.com', '/items');
  final response = await client.get(uri);

  if (response.statusCode == 200) {
    // Run parseItems in a separate isolate
    return compute(parseItems, response.body);
  } else {
    throw Exception('Failed to load items');
  }
}
```

### 5. Define Structured JSON Output for AI Models
When integrating LLMs (like Gemini), enforce reliable JSON output by passing a strict schema in the generation configuration and system instructions.

```dart
import 'package:firebase_vertexai/firebase_vertexai.dart';

// Define the expected JSON schema
final _responseSchema = Schema(
  SchemaType.object,
  properties: {
    'width': Schema(SchemaType.integer),
    'height': Schema(SchemaType.integer),
    'items': Schema(
      SchemaType.array,
      items: Schema(
        SchemaType.object,
        properties: {
          'id': Schema(SchemaType.integer),
          'name': Schema(SchemaType.string),
        },
      ),
    ),
  },
);

// Initialize the model with the schema
final model = FirebaseAI.googleAI().generativeModel(
  model: 'gemini-2.5-pro',
  generationConfig: GenerationConfig(
    responseMimeType: 'application/json',
    responseSchema: _responseSchema,
  ),
);

Future<Map<String, dynamic>> analyzeData(String prompt) async {
  final content = [Content.text(prompt)];
  final response = await model.generateContent(content);
  
  // Safely decode the guaranteed JSON response
  return jsonDecode(response.text!) as Map<String, dynamic>;
}
```

## Constraints
* **Immutable URL Construction:** Always use `Uri.https()` or `Uri.parse()` to build URLs. Never use raw string concatenation for endpoints with query parameters.
* **Error Handling:** Never return `null` on a failed network request. Always throw an `Exception` or a custom error class so the UI (e.g., `FutureBuilder`) can catch and display the error state via `snapshot.hasError`.
* **Status Code Validation:** Always validate `response.statusCode`. Use `200` for successful GET/PUT/DELETE and `201` for successful POST.
* **Library Restriction:** Do not use `dart:io` `HttpClient` directly for standard cross-platform networking. Always use the `http` package to ensure web compatibility.
* **Isolate Communication:** When using `compute()`, ensure the parsing function is a top-level function or a static method, and only pass primitive values or simple objects (like `String` response bodies) across the isolate boundary. Do not pass `http.Response` objects.
