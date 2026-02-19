---
name: rust-ui-architecture
description: Architecture patterns for Rust UI applications including GPUI-specific patterns, code organization, modularity, and scalability. Use when user needs guidance on application architecture, code organization, or scaling UI applications.
---

# Rust UI Architecture

## Metadata

This skill provides comprehensive guidance on architecting scalable, maintainable Rust UI applications using GPUI, covering project structure, design patterns, and best practices.

## Instructions

### Application Structure

#### Recommended Project Layout

```
my-gpui-app/
├── Cargo.toml
├── src/
│   ├── main.rs                 # Application entry point
│   ├── app.rs                  # Main application struct
│   ├── ui/                     # UI layer
│   │   ├── mod.rs
│   │   ├── views/              # High-level views
│   │   │   ├── mod.rs
│   │   │   ├── main_view.rs
│   │   │   ├── sidebar.rs
│   │   │   └── editor.rs
│   │   ├── components/         # Reusable components
│   │   │   ├── mod.rs
│   │   │   ├── button.rs
│   │   │   ├── input.rs
│   │   │   └── modal.rs
│   │   └── theme.rs           # Theme definitions
│   ├── models/                 # Application state
│   │   ├── mod.rs
│   │   ├── document.rs
│   │   ├── project.rs
│   │   └── settings.rs
│   ├── services/              # External integrations
│   │   ├── mod.rs
│   │   ├── file_service.rs
│   │   └── api_client.rs
│   ├── domain/                # Core business logic
│   │   ├── mod.rs
│   │   └── operations.rs
│   └── utils/                 # Utilities
│       ├── mod.rs
│       └── helpers.rs
├── examples/                   # Example applications
│   └── basic.rs
└── tests/                     # Integration tests
    ├── integration/
    └── ui/
```

### Layer Separation

#### Four-Layer Architecture

```
┌─────────────────────────────────┐
│     UI Layer (Views)            │  - GPUI views and components
│                                 │  - User interactions
│                                 │  - Render logic
├─────────────────────────────────┤
│   Application Layer (Models)    │  - Application state (Model<T>)
│                                 │  - State coordination
│                                 │  - Business logic orchestration
├─────────────────────────────────┤
│    Service Layer (Services)     │  - File I/O
│                                 │  - Network requests
│                                 │  - External APIs
├─────────────────────────────────┤
│     Domain Layer (Core)         │  - Pure business logic
│                                 │  - Domain types
│                                 │  - No dependencies on UI/GPUI
└─────────────────────────────────┘
```

#### Example Implementation

```rust
// Domain Layer (pure logic)
pub mod domain {
    #[derive(Clone, Debug)]
    pub struct Document {
        pub id: DocumentId,
        pub content: String,
        pub language: Language,
    }

    impl Document {
        pub fn word_count(&self) -> usize {
            self.content.split_whitespace().count()
        }

        pub fn is_empty(&self) -> bool {
            self.content.trim().is_empty()
        }
    }
}

// Service Layer (external integration)
pub mod services {
    use super::domain::*;

    pub trait FileService: Send + Sync {
        fn read(&self, path: &Path) -> Result<String>;
        fn write(&self, path: &Path, content: &str) -> Result<()>;
    }

    pub struct RealFileService;

    impl FileService for RealFileService {
        fn read(&self, path: &Path) -> Result<String> {
            std::fs::read_to_string(path)
                .map_err(|e| anyhow::anyhow!("Failed to read: {}", e))
        }

        fn write(&self, path: &Path, content: &str) -> Result<()> {
            std::fs::write(path, content)
                .map_err(|e| anyhow::anyhow!("Failed to write: {}", e))
        }
    }
}

// Application Layer (state management)
pub mod models {
    use super::domain::*;
    use super::services::*;

    pub struct DocumentModel {
        document: Document,
        file_service: Arc<dyn FileService>,
        is_modified: bool,
    }

    impl DocumentModel {
        pub fn new(document: Document, file_service: Arc<dyn FileService>) -> Self {
            Self {
                document,
                file_service,
                is_modified: false,
            }
        }

        pub fn update_content(&mut self, content: String) {
            self.document.content = content;
            self.is_modified = true;
        }

        pub async fn save(&mut self) -> Result<()> {
            self.file_service.write(&self.document.path, &self.document.content)?;
            self.is_modified = false;
            Ok(())
        }
    }
}

// UI Layer (views)
pub mod ui {
    use gpui::*;
    use super::models::*;

    pub struct DocumentView {
        model: Model<DocumentModel>,
        _subscription: Subscription,
    }

    impl DocumentView {
        pub fn new(model: Model<DocumentModel>, cx: &mut ViewContext<Self>) -> Self {
            let _subscription = cx.observe(&model, |_, _, cx| cx.notify());
            Self { model, _subscription }
        }
    }

    impl Render for DocumentView {
        fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
            let model = self.model.read(cx);

            div()
                .child(format!("Words: {}", model.document.word_count()))
                .when(model.is_modified, |this| {
                    this.child("(modified)")
                })
        }
    }
}
```

### Component Hierarchies

#### Container-Presenter Pattern

```rust
// Container: Manages state and logic
pub struct EditorContainer {
    document: Model<DocumentModel>,
    _subscription: Subscription,
}

impl EditorContainer {
    pub fn new(document: Model<DocumentModel>, cx: &mut ViewContext<Self>) -> Self {
        let _subscription = cx.observe(&document, |_, _, cx| cx.notify());
        Self { document, _subscription }
    }

    fn handle_save(&mut self, cx: &mut ViewContext<Self>) {
        let document = self.document.clone();

        cx.spawn(|_, mut cx| async move {
            cx.update_model(&document, |doc, _| {
                doc.save().await
            }).await?;

            Ok::<_, anyhow::Error>(())
        }).detach();
    }
}

impl Render for EditorContainer {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let doc = self.document.read(cx);

        EditorPresenter::new(
            doc.document.content.clone(),
            doc.is_modified,
            cx.listener(|this, content, cx| {
                this.document.update(cx, |doc, _| {
                    doc.update_content(content);
                });
            }),
        )
    }
}

// Presenter: Pure rendering
pub struct EditorPresenter {
    content: String,
    is_modified: bool,
    on_change: Box<dyn Fn(String, &mut WindowContext)>,
}

impl EditorPresenter {
    pub fn new(
        content: String,
        is_modified: bool,
        on_change: impl Fn(String, &mut WindowContext) + 'static,
    ) -> Self {
        Self {
            content,
            is_modified,
            on_change: Box::new(on_change),
        }
    }
}

impl Render for EditorPresenter {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        div()
            .flex()
            .flex_col()
            .child(
                textarea()
                    .value(&self.content)
                    .on_input(|value, cx| {
                        (self.on_change)(value, cx);
                    })
            )
            .when(self.is_modified, |this| {
                this.child("Unsaved changes")
            })
    }
}
```

### Module Organization

#### Feature-Based Structure

```
src/
├── features/
│   ├── editor/
│   │   ├── mod.rs
│   │   ├── model.rs          # EditorModel
│   │   ├── view.rs           # EditorView
│   │   ├── commands.rs       # Editor actions
│   │   └── components/       # Editor-specific components
│   ├── sidebar/
│   │   ├── mod.rs
│   │   ├── model.rs
│   │   ├── view.rs
│   │   └── components/
│   └── statusbar/
│       ├── mod.rs
│       ├── model.rs
│       └── view.rs
```

**Benefits**:
- Clear feature boundaries
- Easy to understand and navigate
- Scales well with team size
- Enables feature-based development

### State Management Architecture

#### Unidirectional Data Flow

```
User Action → Action Dispatch → State Update → View Rerender
     ↑                                              ↓
     └──────────────── Event Handlers ─────────────┘
```

**Implementation**:

```rust
// Define actions
actions!(app, [AddTodo, ToggleTodo, DeleteTodo]);

// State model
pub struct TodoListModel {
    todos: Vec<Todo>,
}

impl TodoListModel {
    pub fn add_todo(&mut self, text: String) {
        self.todos.push(Todo {
            id: TodoId::new(),
            text,
            completed: false,
        });
    }

    pub fn toggle_todo(&mut self, id: TodoId) {
        if let Some(todo) = self.todos.iter_mut().find(|t| t.id == id) {
            todo.completed = !todo.completed;
        }
    }
}

// View with action handlers
pub struct TodoListView {
    model: Model<TodoListModel>,
}

impl TodoListView {
    fn register_actions(&mut self, cx: &mut ViewContext<Self>) {
        cx.on_action(cx.listener(|this, action: &AddTodo, cx| {
            this.model.update(cx, |model, cx| {
                model.add_todo(action.text.clone());
                cx.notify();
            });
        }));

        cx.on_action(cx.listener(|this, action: &ToggleTodo, cx| {
            this.model.update(cx, |model, cx| {
                model.toggle_todo(action.id);
                cx.notify();
            });
        }));
    }
}
```

#### State Ownership Patterns

**Single Source of Truth**:
```rust
pub struct AppModel {
    // Root owns all state
    documents: Vec<Model<DocumentModel>>,
    settings: Model<Settings>,
    ui_state: Model<UiState>,
}
```

**Hierarchical Ownership**:
```rust
pub struct WorkspaceModel {
    // Workspace owns workspace-level state
    panes: Vec<Model<PaneModel>>,
}

pub struct PaneModel {
    // Pane owns pane-level state
    tabs: Vec<Model<TabModel>>,
    active_index: usize,
}
```

### Separation of Concerns

#### Clear Boundaries

```rust
// ✓ GOOD: Clear responsibilities

// Domain logic (no GPUI)
pub mod document {
    pub struct Document {
        content: String,
    }

    impl Document {
        pub fn insert(&mut self, pos: usize, text: &str) {
            self.content.insert_str(pos, text);
        }
    }
}

// Application logic (uses GPUI models)
pub mod editor_model {
    use gpui::*;
    use super::document::Document;

    pub struct EditorModel {
        document: Document,
        cursor_position: usize,
    }

    impl EditorModel {
        pub fn insert_at_cursor(&mut self, text: &str) {
            self.document.insert(self.cursor_position, text);
            self.cursor_position += text.len();
        }
    }
}

// UI logic (GPUI views)
pub mod editor_view {
    use gpui::*;
    use super::editor_model::EditorModel;

    pub struct EditorView {
        model: Model<EditorModel>,
    }

    impl Render for EditorView {
        fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
            // Rendering logic
        }
    }
}
```

### Testability Patterns

#### Dependency Injection

```rust
// Define trait for external dependencies
pub trait FileService: Send + Sync {
    fn read(&self, path: &Path) -> Result<String>;
    fn write(&self, path: &Path, content: &str) -> Result<()>;
}

// Production implementation
pub struct RealFileService;

impl FileService for RealFileService {
    // Real implementation
}

// Test implementation
#[cfg(test)]
pub struct MockFileService {
    read_results: HashMap<PathBuf, Result<String>>,
    written_files: RefCell<Vec<(PathBuf, String)>>,
}

#[cfg(test)]
impl FileService for MockFileService {
    fn read(&self, path: &Path) -> Result<String> {
        self.read_results
            .get(path)
            .cloned()
            .unwrap_or_else(|| Err(anyhow::anyhow!("File not found")))
    }

    fn write(&self, path: &Path, content: &str) -> Result<()> {
        self.written_files
            .borrow_mut()
            .push((path.to_path_buf(), content.to_string()));
        Ok(())
    }
}

// Model accepts any FileService
pub struct DocumentModel {
    file_service: Arc<dyn FileService>,
}

// Tests use mock
#[cfg(test)]
mod tests {
    #[test]
    fn test_save() {
        let mock_service = Arc::new(MockFileService::new());
        let model = DocumentModel::new(mock_service.clone());

        model.save().unwrap();

        assert_eq!(mock_service.written_files.borrow().len(), 1);
    }
}
```

### Plugin Architecture

#### Extension System

```rust
// Define plugin trait
pub trait EditorPlugin: Send + Sync {
    fn name(&self) -> &str;
    fn on_document_open(&self, doc: &Document) -> Result<()>;
    fn on_document_save(&self, doc: &Document) -> Result<()>;
}

// Plugin manager
pub struct PluginManager {
    plugins: Vec<Box<dyn EditorPlugin>>,
}

impl PluginManager {
    pub fn register(&mut self, plugin: Box<dyn EditorPlugin>) {
        self.plugins.push(plugin);
    }

    pub fn notify_document_open(&self, doc: &Document) -> Result<()> {
        for plugin in &self.plugins {
            plugin.on_document_open(doc)?;
        }
        Ok(())
    }
}

// Example plugin
pub struct AutoSavePlugin {
    interval: Duration,
}

impl EditorPlugin for AutoSavePlugin {
    fn name(&self) -> &str {
        "AutoSave"
    }

    fn on_document_open(&self, doc: &Document) -> Result<()> {
        // Start auto-save timer
        Ok(())
    }

    fn on_document_save(&self, doc: &Document) -> Result<()> {
        println!("Document saved: {}", doc.path.display());
        Ok(())
    }
}
```

## Resources

### Design Patterns

**Architectural Patterns**:
- Model-View pattern (GPUI-specific)
- Container-Presenter (separation of concerns)
- Service-oriented (external dependencies)
- Plugin architecture (extensibility)

**Code Organization**:
- Feature-based modules
- Layer separation
- Clear boundaries
- Dependency injection

**State Management**:
- Unidirectional data flow
- Single source of truth
- Hierarchical ownership
- Reactive updates

### Best Practices

1. **Separation of Concerns**: Keep UI, logic, and data separate
2. **Dependency Injection**: Use traits for testability
3. **Feature Organization**: Group related code by feature
4. **State Ownership**: Clear ownership hierarchy
5. **Testable Design**: Design for testing from the start
6. **Documentation**: Document architecture decisions
7. **Modularity**: Small, focused modules
8. **Scalability**: Design for growth

### Common Patterns

- **Repository Pattern**: Data access abstraction
- **Command Pattern**: Action system
- **Observer Pattern**: Subscriptions
- **Factory Pattern**: Component creation
- **Strategy Pattern**: Pluggable behaviors
- **Facade Pattern**: Simplified interfaces
