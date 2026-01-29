---
name: leap-edge-sdk
description: Liquid AI LEAP Edge SDK for on-device AI inference on Android and iOS. This skill should be used when building mobile apps with local LLM capabilities, implementing chat interfaces with streaming responses, or deploying small language models to edge devices. Triggers on tasks involving LeapSDK, LeapClient, ModelRunner, on-device inference, or mobile AI integration.
license: MIT
metadata:
  author: liquid-ai
  version: "1.0.0"
---

# LEAP Edge SDK Integration Guide

Comprehensive guide for integrating Liquid AI's LEAP (Liquid Edge AI Platform) Edge SDK into Android and iOS applications, enabling on-device AI inference without network connectivity.

## When to Apply These Guidelines

Use this skill when:
- Building mobile apps with on-device AI capabilities
- Implementing chat interfaces with streaming LLM responses
- Integrating Liquid Foundational Models (LFM) into Android/iOS apps
- Deploying small language models to edge devices
- Converting cloud LLM API calls to local inference

## Platform Requirements

### Android
- Kotlin Android plugin v2.2.0+
- Android Gradle Plugin v8.12.0+
- arm64-v8a ABI device with developer mode
- Minimum SDK: API 31
- Recommended: 3GB+ RAM

### iOS
- Xcode 15.0+ with Swift 5.9
- iOS 18.0+ / macOS 14.0+
- Physical device with 3GB+ RAM (simulator supported but slower)

---

## Android Integration (Kotlin)

### Installation

Add to `build.gradle.kts`:

```kotlin
api("ai.liquid.leap:leap-sdk-android:0.9.2")
```

### Loading a Model

**From local path:**

```kotlin
// Bad: Loading on main thread
val modelRunner = LeapClient.loadModel(MODEL_PATH) // Blocks UI

// Good: Loading on background coroutine
lifecycleScope.launch {
    try {
        val modelRunner = LeapClient.loadModel(MODEL_PATH)
    } catch (e: LeapModelLoadingException) {
        Log.e(TAG, "Failed to load model: ${e.message}")
    }
}
```

**With custom options:**

```kotlin
val modelRunner = LeapClient.loadModel(
    MODEL_PATH,
    ModelLoadingOptions.build {
        cpuThread = 4
    }
)
```

**Using LeapDownloader (auto-download):**

```kotlin
val baseDir = File(context.filesDir, "model_files").absolutePath
val modelDownloader = LeapDownloader(
    config = LeapDownloaderConfig(saveDir = baseDir)
)

val modelRunner = modelDownloader.loadModel(
    modelSlug = "LFM2-1.2B",
    quantizationSlug = "Q5_K_M"
)
```

### Creating Conversations

```kotlin
// Basic conversation
val conversation = modelRunner.createConversation()

// With system prompt
val conversation = modelRunner.createConversation(
    systemPrompt = "You are a helpful assistant."
)
```

### Generating Responses (Streaming)

```kotlin
// Bad: Blocking call without proper flow handling
val response = conversation.generateResponse(input).first()

// Good: Streaming with proper flow collection
conversation.generateResponse(userMessage)
    .onEach { response ->
        when (response) {
            is MessageResponse.Chunk -> {
                // Append token to UI
                updateUI(response.text)
            }
            is MessageResponse.ReasoningChunk -> {
                // Handle reasoning tokens if needed
            }
            is MessageResponse.Complete -> {
                // Generation finished
                Log.d(TAG, "Tokens used: ${response.usage}")
            }
        }
    }
    .onCompletion { Log.d(TAG, "Generation complete") }
    .catch { e -> Log.e(TAG, "Error: ${e.message}") }
    .collect()
```

### Complete ViewModel Example

```kotlin
import ai.liquid.leap.*
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

class ChatViewModel : ViewModel() {

    private var modelRunner: ModelRunner? = null
    private var conversation: Conversation? = null

    private val _messages = MutableStateFlow<List<Message>>(emptyList())
    val messages: StateFlow<List<Message>> = _messages.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    fun loadModel(context: Context) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val baseDir = File(context.filesDir, "models").absolutePath
                val downloader = LeapDownloader(
                    config = LeapDownloaderConfig(saveDir = baseDir)
                )
                modelRunner = downloader.loadModel(
                    modelSlug = "LFM2-1.2B",
                    quantizationSlug = "Q5_K_M"
                )
                conversation = modelRunner?.createConversation()
            } catch (e: Exception) {
                Log.e("ChatViewModel", "Failed to load model", e)
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun sendMessage(text: String) {
        val conv = conversation ?: return
        _messages.value += Message(role = "user", content = text)

        viewModelScope.launch {
            val responseBuilder = StringBuilder()
            conv.generateResponse(text)
                .onEach { response ->
                    when (response) {
                        is MessageResponse.Chunk -> {
                            responseBuilder.append(response.text)
                            updateAssistantMessage(responseBuilder.toString())
                        }
                        is MessageResponse.Complete -> {}
                        else -> {}
                    }
                }
                .catch { e -> Log.e("ChatViewModel", "Error", e) }
                .collect()
        }
    }

    private fun updateAssistantMessage(content: String) {
        val messages = _messages.value.toMutableList()
        val lastIndex = messages.indexOfLast { it.role == "assistant" }
        if (lastIndex >= 0) {
            messages[lastIndex] = messages[lastIndex].copy(content = content)
        } else {
            messages += Message(role = "assistant", content = content)
        }
        _messages.value = messages
    }
}

data class Message(val role: String, val content: String)
```

---

## iOS Integration (Swift)

### Installation

**Swift Package Manager (Recommended):**

1. Xcode → File → Add Package Dependencies
2. Enter: `https://github.com/Liquid4All/leap-ios.git`
3. Select version 0.7.7+
4. Add `LeapSDK` and optionally `LeapModelDownloader`

**CocoaPods:**

```ruby
pod 'Leap-SDK', '~> 0.7.7'
```

### Loading a Model

**From bundle:**

```swift
import LeapSDK

let modelURL = Bundle.main.url(forResource: "model", withExtension: "bundle")!
let modelRunner = try await Leap.load(options: .init(bundlePath: modelURL.path()))
```

**With LeapModelDownloader:**

```swift
import LeapSDK
import LeapModelDownloader

let downloader = LeapModelDownloader()
let modelRunner = try await downloader.loadModel(
    modelSlug: "LFM2-1.2B",
    quantizationSlug: "Q5_K_M"
)
```

### Creating Conversations

```swift
// Basic conversation
let conversation = Conversation(modelRunner: modelRunner, history: [])

// With system prompt
let systemMessage = ChatMessage(
    role: .system,
    content: [.text("You are a helpful assistant.")]
)
let conversation = Conversation(modelRunner: modelRunner, history: [systemMessage])
```

### Generating Responses (Streaming)

```swift
let userMessage = ChatMessage(
    role: .user,
    content: [.text("Hello, how are you?")]
)

// Good: Proper async stream handling
for await response in conversation.generateResponse(message: userMessage) {
    switch response {
    case .chunk(let text):
        // Append token to UI
        appendToResponse(text)
    case .reasoningChunk(let text):
        // Handle reasoning if needed
        break
    case .complete(let usage, let reason):
        print("Done! Tokens: \(usage)")
    }
}
```

### Complete ViewModel Example

```swift
import SwiftUI
import LeapSDK
import LeapModelDownloader

@MainActor
final class ChatViewModel: ObservableObject {

    @Published var messages: [Message] = []
    @Published var isLoading = false
    @Published var isGenerating = false

    private var modelRunner: ModelRunner?
    private var conversation: Conversation?
    private var generationTask: Task<Void, Never>?

    func loadModel() async {
        isLoading = true
        defer { isLoading = false }

        do {
            let downloader = LeapModelDownloader()
            modelRunner = try await downloader.loadModel(
                modelSlug: "LFM2-1.2B",
                quantizationSlug: "Q5_K_M"
            )
            if let runner = modelRunner {
                conversation = Conversation(modelRunner: runner, history: [])
            }
        } catch {
            print("Failed to load model: \(error)")
        }
    }

    func sendMessage(_ text: String) {
        guard let conversation = conversation else { return }

        messages.append(Message(role: .user, content: text))
        messages.append(Message(role: .assistant, content: ""))
        let assistantIndex = messages.count - 1

        let userMessage = ChatMessage(role: .user, content: [.text(text)])
        isGenerating = true

        generationTask = Task {
            defer { isGenerating = false }
            do {
                for await response in conversation.generateResponse(message: userMessage) {
                    switch response {
                    case .chunk(let text):
                        messages[assistantIndex].content += text
                    case .complete(_, _):
                        break
                    default:
                        break
                    }
                }
            } catch {
                print("Generation error: \(error)")
            }
        }
    }

    func stopGeneration() {
        generationTask?.cancel()
        isGenerating = false
    }
}

struct Message: Identifiable {
    let id = UUID()
    let role: Role
    var content: String
    enum Role { case user, assistant }
}
```

### SwiftUI Chat View

```swift
struct ChatView: View {
    @StateObject private var viewModel = ChatViewModel()
    @State private var inputText = ""

    var body: some View {
        VStack {
            if viewModel.isLoading {
                ProgressView("Loading model...")
            } else {
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 12) {
                        ForEach(viewModel.messages) { message in
                            MessageBubble(message: message)
                        }
                    }
                    .padding()
                }

                HStack {
                    TextField("Message", text: $inputText)
                        .textFieldStyle(.roundedBorder)
                    Button(action: sendMessage) {
                        Image(systemName: "arrow.up.circle.fill")
                    }
                    .disabled(inputText.isEmpty || viewModel.isGenerating)
                }
                .padding()
            }
        }
        .task { await viewModel.loadModel() }
    }

    private func sendMessage() {
        let text = inputText
        inputText = ""
        viewModel.sendMessage(text)
    }
}
```

---

## Available Models

| Model | Parameters | Size | Best For |
|-------|------------|------|----------|
| LFM2-350M | 350M | ~300MB | Fast responses, low memory |
| LFM2-700M | 700M | ~600MB | Balanced performance |
| LFM2-1.2B | 1.2B | ~1GB | Best quality |

**Quantization Options:** `Q4_K_M`, `Q5_K_M`, `Q8_0`

---

## Best Practices

| Practice | Impact | Description |
|----------|--------|-------------|
| Load models on background thread | CRITICAL | Model loading is CPU-intensive, blocks UI |
| Reuse ModelRunner instance | HIGH | Don't reload for each conversation |
| Handle errors gracefully | HIGH | Network/storage issues during download |
| Test on physical devices | MEDIUM | Simulators are significantly slower |
| Monitor memory usage | MEDIUM | Large models require 3GB+ RAM |
| Cancel ongoing generation | MEDIUM | When user navigates away or sends new message |
